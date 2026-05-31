"""Download offline Bible data to power the Streamlit study app."""
import argparse
import json
import sys
import time
from pathlib import Path
from typing import Dict, List

import requests

API_BASE = "https://www.abibliadigital.com.br/api"
DEFAULT_VERSIONS = ["nvi", "almeida"]
OUTPUT_FILE = "bible_data.json"
REQUEST_TIMEOUT = 12
RETRY_DELAY = 1.5
MAX_RETRIES = 5


class DownloadError(Exception):
    pass


def safe_get(url: str, params: Dict[str, str] = None) -> Dict:
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as exc:
            code = exc.response.status_code
            if code == 429 and attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY * attempt)
                continue
            raise DownloadError(f"Failed to fetch {url}: {exc}")
        except requests.RequestException as exc:
            if attempt == MAX_RETRIES:
                raise DownloadError(f"Failed to fetch {url}: {exc}")
            time.sleep(RETRY_DELAY)
    raise DownloadError(f"Unreachable: {url}")


def fetch_books(version: str) -> List[Dict]:
    print(f"Downloading book list for version {version}")
    data = safe_get(f"{API_BASE}/books", params={"version": version})
    return data or []


def fetch_chapter(version: str, book_abbrev: str, chapter_number: int) -> Dict:
    text = safe_get(f"{API_BASE}/verses/{version}/{book_abbrev}/{chapter_number}")
    return text


def build_data_for_version(version: str) -> Dict:
    books = fetch_books(version)
    structured = {"version": version, "books": {}}

    for book in books:
        book_abbrev = book.get("abbrev") or book.get("nameVirtual") or book.get("name")
        book_key = book_abbrev.lower()
        book_entry = {
            "name": book.get("name"),
            "abbrev": book_abbrev,
            "order": book.get("book", 0),
            "chapters": {},
        }

        total_chapters = book.get("chapters", 0)
        print(f"  {book.get('name')} ({total_chapters} chapters)")

        for chapter_idx in range(1, total_chapters + 1):
            chapter_data = fetch_chapter(version, book_abbrev, chapter_idx)
            verses = chapter_data.get("verses", [])
            chapter_entry = {"verses": {}, "chapter_title": chapter_data.get("chapter")}

            for verse in verses:
                verse_number = verse.get("number")
                text = verse.get("text")
                if verse_number and text:
                    chapter_entry["verses"][str(verse_number)] = text.strip()

            book_entry["chapters"][str(chapter_idx)] = chapter_entry
            time.sleep(0.1)

        structured["books"][book_key] = book_entry

    return structured


def main() -> None:
    parser = argparse.ArgumentParser(description="Download bible data for offline use.")
    parser.add_argument(
        "--versions",
        "-v",
        nargs="+",
        default=DEFAULT_VERSIONS,
        help="Bible versions to download (ex: nvi almeida).",
    )
    parser.add_argument(
        "--output",
        "-o",
        default=OUTPUT_FILE,
        help="JSON file where the downloaded data will be stored.",
    )
    parser.add_argument(
        "--force",
        "-f",
        action="store_true",
        help="Force download even if the output file already exists.",
    )

    args = parser.parse_args()
    destination = Path(args.output)

    if destination.exists() and not args.force:
        reply = input(f"{destination} already exists. Overwrite? [y/N]: ")
        if reply.strip().lower() not in {"y", "s", "sim"}:
            print("Operation aborted.")
            sys.exit(0)

    final_data = {"generated_on": time.time(), "versions": {}}

    downloaded_versions = []
    for version in args.versions:
        try:
            final_data["versions"][version] = build_data_for_version(version)
            downloaded_versions.append(version)
        except DownloadError as error:
            print(f"Failed to download {version}: {error}")
            continue

    destination.parent.mkdir(parents=True, exist_ok=True)
    with open(destination, "w", encoding="utf-8") as handle:
        json.dump(final_data, handle, ensure_ascii=False, indent=2)

    if not downloaded_versions:
        print("Warning: No versions were downloaded. Check your network or try again later.")
    else:
        print(f"Data saved to {destination.resolve()}")


if __name__ == "__main__":
    main()
