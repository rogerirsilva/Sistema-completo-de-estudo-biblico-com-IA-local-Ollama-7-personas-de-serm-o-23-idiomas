from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from backend.config import DATA_PATH, LOCAL_JSON_DIR, TRANSLATIONS_DIR
from book_names_mapping import get_book_name


def _load_json_file(path: Path) -> Any:
    with open(path, "r", encoding="utf-8-sig") as handle:
        content = handle.read().strip()
        if not content:
            return {}
        return json.loads(content)


def load_bible_data_fallback() -> dict[str, Any]:
    if not DATA_PATH.exists():
        return {}
    try:
        data = _load_json_file(DATA_PATH)
        if isinstance(data, dict):
            return data
    except (OSError, json.JSONDecodeError, UnicodeDecodeError):
        return {}
    return {}


def load_bible_data_by_language(lang_code: str) -> dict[str, Any]:
    lang_dir = LOCAL_JSON_DIR / lang_code
    if not lang_dir.exists():
        return load_bible_data_fallback()

    bible_data: dict[str, Any] = {"versions": {}}

    for json_file in lang_dir.glob("*.json"):
        if json_file.name.lower() == "readme.json":
            continue

        try:
            data = _load_json_file(json_file)
            version_name = json_file.stem.upper()

            if isinstance(data, list):
                books: dict[str, Any] = {}
                for idx, book in enumerate(data):
                    book_abbrev = str(book.get("abbrev", "")).lower()
                    book_name_from_json = str(book.get("name", ""))
                    book_name = get_book_name(book_abbrev, lang_code, fallback=book_name_from_json)
                    if not book_name:
                        book_name = f"Book{idx + 1}"

                    chapters_dict: dict[str, Any] = {}
                    for ch_idx, chapter_verses in enumerate(book.get("chapters", [])):
                        ch_num = str(ch_idx + 1)
                        verses_dict: dict[str, str] = {}
                        if isinstance(chapter_verses, list):
                            for v_idx, verse_text in enumerate(chapter_verses):
                                verses_dict[str(v_idx + 1)] = str(verse_text)
                        chapters_dict[ch_num] = {"verses": verses_dict}

                    books[book_name] = {
                        "name": book_name,
                        "abbrev": book_abbrev,
                        "order": idx + 1,
                        "chapters": chapters_dict,
                    }

                bible_data["versions"][version_name] = {"books": books}
            elif isinstance(data, dict) and "versions" in data:
                return data
        except (OSError, json.JSONDecodeError, UnicodeDecodeError, TypeError, ValueError):
            continue

    return bible_data


def list_languages() -> list[dict[str, str]]:
    all_languages = {
        "pt": "Portugues",
        "en": "English",
        "es": "Espanol",
        "fr": "Francais",
        "de": "Deutsch",
        "it": "Italiano",
        "ru": "Russkiy",
        "zh": "Chinese",
        "ja": "Japanese",
        "ar": "Arabic",
        "el": "Greek",
        "eo": "Esperanto",
        "fi": "Suomi",
        "ko": "Korean",
        "ro": "Romanian",
        "vi": "Vietnamese",
        "hi": "Hindi",
        "id": "Indonesian",
        "pl": "Polish",
        "fa": "Persian",
        "sw": "Swahili",
        "th": "Thai",
        "tr": "Turkish",
    }

    available: dict[str, str] = {}

    if TRANSLATIONS_DIR.exists():
        for file in TRANSLATIONS_DIR.glob("*.json"):
            code = file.stem
            if code in all_languages:
                available[code] = all_languages[code]

    if LOCAL_JSON_DIR.exists():
        for lang_dir in LOCAL_JSON_DIR.iterdir():
            if not lang_dir.is_dir():
                continue
            code = lang_dir.name
            if code in all_languages and code not in available:
                if list(lang_dir.glob("*.json")):
                    available[code] = all_languages[code]

    if not available:
        available = {"pt": "Portugues"}

    return [{"code": code, "name": name} for code, name in sorted(available.items())]
