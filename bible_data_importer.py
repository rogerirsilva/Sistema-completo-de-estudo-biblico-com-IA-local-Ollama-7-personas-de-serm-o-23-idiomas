import json
import re
from io import BytesIO
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple
from zipfile import ZipFile

import requests

BOOK_NAME_KEYS = ("name", "nome", "book", "livro", "titulo", "title")
BOOK_ABBREV_KEYS = ("abbrev", "abrev", "sigla", "code", "short")
CHAPTER_KEYS = ("chapters", "capitulos", "chapter_list", "capitulo", "chapters_list")
VERSE_KEYS = ("verses", "versiculos", "verse_list", "versiculos_list", "verse")
CHAPTER_NUMBER_KEYS = ("chapter", "capitulo", "numero", "n", "id", "chapter_number")
VERSE_NUMBER_KEYS = ("verse", "versiculo", "numero", "n", "id", "verso")
TEXT_KEYS = ("text", "texto", "verse_text", "conteudo", "passage", "value")
ORDER_KEYS = ("order", "ordem", "indice", "book", "seq")
VERSION_KEYS = ("version", "versao", "versão", "nome", "name")


def _value_from_keys(raw: Any, keys: Iterable[str]) -> Optional[Any]:
    if not isinstance(raw, dict):
        return None
    lower_map = {key.lower(): key for key in raw.keys()}
    for key in keys:
        if key in raw and raw[key] not in (None, ""):
            return raw[key]
        normalized = lower_map.get(key.lower())
        if normalized and raw[normalized] not in (None, ""):
            return raw[normalized]
    return None


def _safe_str(value: Any) -> Optional[str]:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _sanitize_key(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "", value.lower())
    return slug or "book"


def _iterate_chapters(source: Any) -> Iterable[Tuple[str, Any]]:
    if isinstance(source, dict):
        for key, value in source.items():
            yield str(key), value
    elif isinstance(source, list):
        for index, item in enumerate(source, start=1):
            if isinstance(item, dict):
                number = _value_from_keys(item, CHAPTER_NUMBER_KEYS) or item.get("chapter")
                chapter_number = number if number is not None else index
                yield str(chapter_number), item
            elif isinstance(item, list):
                yield str(index), item


def _iterate_verses(source: Any) -> Iterable[Tuple[str, str]]:
    if isinstance(source, dict):
        for key, value in source.items():
            if isinstance(value, dict):
                text = _value_from_keys(value, TEXT_KEYS)
                if not text:
                    continue
            else:
                text = _safe_str(value)
                if not text:
                    continue
            yield str(key), text
    elif isinstance(source, list):
        for index, item in enumerate(source, start=1):
            if isinstance(item, dict):
                verse_number = _value_from_keys(item, VERSE_NUMBER_KEYS)
                verse_text = _value_from_keys(item, TEXT_KEYS)
                if verse_number is None or not verse_text:
                    continue
                yield str(verse_number), verse_text.strip()
            else:
                verse_text = _safe_str(item)
                if verse_text:
                    yield str(index), verse_text


def _group_verses_with_chapters(entries: Iterable[Any]) -> Dict[str, Dict[str, str]]:
    grouped: Dict[str, Dict[str, str]] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        chapter_number = _value_from_keys(entry, CHAPTER_NUMBER_KEYS) or 1
        verse_number = _value_from_keys(entry, VERSE_NUMBER_KEYS)
        verse_text = _value_from_keys(entry, TEXT_KEYS)
        if verse_number is None or not verse_text:
            continue
        chapter_key = str(chapter_number)
        grouped.setdefault(chapter_key, {})[str(verse_number)] = verse_text.strip()
    return grouped


def _build_chapter_entry(chapter_data: Any) -> Dict[str, str]:
    if isinstance(chapter_data, list) and not any(isinstance(item, dict) for item in chapter_data):
        verses = {}
        for idx, item in enumerate(chapter_data, start=1):
            text = _safe_str(item)
            if text:
                verses[str(idx)] = text
        return verses
    verse_source = _value_from_keys(chapter_data, VERSE_KEYS)
    if not verse_source:
        verse_source = chapter_data
    return {num: text for num, text in _iterate_verses(verse_source)}


def normalize_book(raw: Dict[str, Any], fallback_book_id: str) -> Optional[Tuple[str, Dict[str, Any]]]:
    if not isinstance(raw, dict):
        return None
    name = _value_from_keys(raw, BOOK_NAME_KEYS) or fallback_book_id
    clean_name = _safe_str(name) or fallback_book_id
    abbrev = _value_from_keys(raw, BOOK_ABBREV_KEYS)
    clean_abbrev = _safe_str(abbrev) or _sanitize_key(clean_name)
    chapters_source = _value_from_keys(raw, CHAPTER_KEYS)
    chapters_map: Dict[str, Dict[str, Any]] = {}

    if chapters_source:
        for chapter_number, chapter_value in _iterate_chapters(chapters_source):
            verses = _build_chapter_entry(chapter_value)
            if not verses:
                continue
            chapter_title = _value_from_keys(chapter_value, ("title", "name", "chapter_title"))
            chapters_map[chapter_number] = {
                "chapter_title": _safe_str(chapter_title),
                "verses": verses,
            }
    else:
        verses_list = raw.get("verses") or raw.get("versiculos")
        grouped = _group_verses_with_chapters(verses_list if isinstance(verses_list, list) else [])
        for chapter_number, verses in grouped.items():
            chapters_map[chapter_number] = {"chapter_title": None, "verses": verses}

    if not chapters_map:
        # try building from flat verse dict
        verses_dict = {num: text for num, text in _iterate_verses(raw)}
        if verses_dict:
            chapters_map["1"] = {"chapter_title": None, "verses": verses_dict}

    if not chapters_map:
        return None

    order = _value_from_keys(raw, ORDER_KEYS)
    try:
        order_value = int(order)
    except (TypeError, ValueError):
        order_value = 0

    book_key = clean_abbrev.lower()
    return book_key, {
        "name": clean_name,
        "abbrev": clean_abbrev,
        "order": order_value,
        "chapters": chapters_map,
    }


def convert_books_from_payload(payload: Any, fallback_prefix: str = "book") -> Dict[str, Dict[str, Any]]:
    books: Dict[str, Dict[str, Any]] = {}
    if isinstance(payload, dict) and "books" in payload:
        raw_books = payload["books"]
        if isinstance(raw_books, dict):
            for key, book_data in raw_books.items():
                normalized = normalize_book(book_data, fallback_book_id=key)
                if normalized:
                    books[normalized[0]] = normalized[1]
        elif isinstance(raw_books, list):
            for index, book_data in enumerate(raw_books, start=1):
                normalized = normalize_book(book_data, fallback_book_id=f"{fallback_prefix}{index}")
                if normalized:
                    books[normalized[0]] = normalized[1]
    elif isinstance(payload, list):
        if payload and all(isinstance(item, dict) for item in payload):
            for index, book_data in enumerate(payload, start=1):
                normalized = normalize_book(book_data, fallback_book_id=f"{fallback_prefix}{index}")
                if normalized:
                    books[normalized[0]] = normalized[1]
        else:
            grouped = _group_verses_with_chapters(payload)
            if grouped:
                chapters = {
                    chapter_number: {"chapter_title": None, "verses": verses}
                    for chapter_number, verses in grouped.items()
                }
                books["imported"] = {
                    "name": "Imported",
                    "abbrev": "imported",
                    "order": 0,
                    "chapters": chapters,
                }
    elif isinstance(payload, dict):
        normalized = normalize_book(payload, fallback_book_id=fallback_prefix)
        if normalized:
            books[normalized[0]] = normalized[1]
    return books


def convert_payload_to_versions(payload: Any, version_hint: Optional[str] = None) -> Dict[str, Dict[str, Any]]:
    version_name = (version_hint or _value_from_keys(payload, VERSION_KEYS) or "imported").lower()
    books = convert_books_from_payload(payload, fallback_prefix=version_name)
    if not books:
        return {}
    return {version_name: {"version": version_name, "books": books}}


def convert_archive_to_versions(zip_bytes: bytes, version_filter: Optional[Set[str]] = None) -> Dict[str, Dict[str, Any]]:
    versions: Dict[str, Dict[str, Any]] = {}
    with ZipFile(BytesIO(zip_bytes)) as archive:
        for entry in archive.infolist():
            if entry.is_dir() or not entry.filename.lower().endswith(".json"):
                continue
            path = Path(entry.filename)
            relative = path.parts[1:] if len(path.parts) > 1 else path.parts
            if not relative:
                continue
            try:
                json_index = relative.index("json")
            except ValueError:
                json_index = None
            version_name = None
            if json_index is not None and json_index + 1 < len(relative):
                version_candidate = Path(relative[json_index + 1]).stem.lower()
                version_name = version_candidate
                if version_filter and version_name not in version_filter:
                    continue
            raw = json.load(archive.open(entry))
            if version_name:
                version_entry = versions.setdefault(
                    version_name, {"version": version_name, "books": {}},
                )
                if isinstance(raw, dict) and "books" in raw:
                    new_books = convert_books_from_payload(raw, fallback_prefix=version_name)
                    version_entry["books"].update(new_books)
                    continue
                normalized = normalize_book(raw, fallback_book_id=path.stem)
                if normalized:
                    version_entry["books"][normalized[0]] = normalized[1]
            else:
                version_hint = None
                if version_filter and len(version_filter) == 1:
                    version_hint = next(iter(version_filter))
                inferred = convert_payload_to_versions(raw, version_hint=version_hint)
                for key, value in inferred.items():
                    normalized_key = key.lower()
                    if version_filter and normalized_key not in version_filter:
                        continue
                    versions.setdefault(normalized_key, {"version": normalized_key, "books": {}})["books"].update(value.get("books", {}))
    return versions


def merge_version_maps(existing: Dict[str, Dict[str, Any]], incoming: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    merged = {key: value.copy() for key, value in existing.items()}
    for version, data in incoming.items():
        target = merged.setdefault(version, {"version": version, "books": {}})
        target_books = target.setdefault("books", {})
        target_books.update(data.get("books", {}))
        target["version"] = version
    return merged


def download_github_archive(owner_repo: str, ref: str = "main", timeout: int = 20) -> bytes:
    if "/" not in owner_repo:
        raise ValueError("owner_repo must be in the form owner/repo")
    url = f"https://codeload.github.com/{owner_repo}/zip/{ref}"
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    return response.content
