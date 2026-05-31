"""Download and convert Bible data from a GitHub repository."""
import argparse
import json
import sys
import time
from pathlib import Path
from typing import Dict, Set

from bible_data_importer import (
    convert_archive_to_versions,
    download_github_archive,
    merge_version_maps,
)


def prompt_overwrite(path: Path) -> bool:
    reply = input(f"{path} already exists. Overwrite? [y/N]: ")
    return reply.strip().lower() in {"y", "s", "sim"}


def parse_versions(versions: list[str] | None) -> Set[str] | None:
    if not versions:
        return None
    return {item.strip().lower() for item in versions if item.strip()}


def main() -> None:
    parser = argparse.ArgumentParser(description="Importa a Biblia de um repo GitHub e salva em JSON offline.")
    parser.add_argument(
        "--repo",
        "-r",
        default="mrk214/bible-data-pt-por",
        help="Formato owner/repo do GitHub que contém o JSON.",
    )
    parser.add_argument(
        "--ref",
        default="main",
        help="Branch, tag ou commit a ser baixado.",
    )
    parser.add_argument(
        "--versions",
        "-v",
        nargs="+",
        help="Versões específicas dentro do repo (ex: nvi almeida).",
    )
    parser.add_argument(
        "--output",
        "-o",
        default="bible_data.json",
        help="Arquivo de destino para o JSON consolidado.",
    )
    parser.add_argument(
        "--replace",
        action="store_true",
        help="Descartar dados antigos e gravar apenas as versões baixadas.",
    )
    parser.add_argument(
        "--force",
        "-f",
        action="store_true",
        help="Ignorar prompt de confirmação ao sobrescrever.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="Timeout (segundos) para baixar o zip do GitHub.",
    )

    args = parser.parse_args()
    try:
        archive = download_github_archive(args.repo, args.ref, timeout=args.timeout)
    except Exception as error:
        print(f"Failed to download archive: {error}")
        sys.exit(1)

    version_filter = parse_versions(args.versions)
    versions = convert_archive_to_versions(archive, version_filter=version_filter)
    if not versions:
        print("No Bible version could be extracted from the archive.")
        sys.exit(1)

    destination = Path(args.output)
    existing: Dict[str, Dict] = {}
    if destination.exists():
        try:
            with destination.open("r", encoding="utf-8") as handle:
                existing = json.load(handle).get("versions", {})
        except (json.JSONDecodeError, OSError):
            existing = {}

    if args.replace and destination.exists() and not args.force:
        if not prompt_overwrite(destination):
            print("Operation aborted.")
            sys.exit(0)

    final_versions = versions if args.replace else merge_version_maps(existing, versions)
    payload = {"generated_on": time.time(), "versions": final_versions}

    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)

    print(f"Saved {len(versions)} version(s) to {destination.resolve()}")


if __name__ == "__main__":
    main()
