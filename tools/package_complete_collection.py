#!/usr/bin/env python3
"""Package all NS 01–NS 15 PDFs and Markdown masters into one ZIP."""

from __future__ import annotations

import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RELEASE = ROOT / "release"
PATTERNS = ROOT / "patterns"
OUTPUT = RELEASE / "Novality_Crochet_Studio_NS01-NS15_COMPLETE_PDF_AND_MARKDOWN_COLLECTION.zip"

COLOUR_FOLDER = "01_COLOURFUL_PDFS"
PRINT_FOLDER = "02_BLACK_AND_WHITE_PRINT_PDFS"
MARKDOWN_FOLDER = "03_AUDITED_MARKDOWN_MASTERS"


def one_match(pattern: str) -> Path:
    matches = sorted(RELEASE.glob(pattern))
    if len(matches) != 1:
        raise ValueError(f"Expected exactly one match for {pattern!r}; found {len(matches)}")
    return matches[0]


def inventory() -> list[tuple[Path, str]]:
    entries: list[tuple[Path, str]] = []
    for number in range(1, 16):
        code = f"NS{number:02d}"
        colour = one_match(f"{code}_*_Crochet_Pattern.pdf")
        printer = one_match(f"{code}_*_PRINTER_SAVER.pdf")
        markdown_matches = sorted(PATTERNS.glob(f"{number:02d}_*.md"))
        if len(markdown_matches) != 1:
            raise ValueError(
                f"Expected one Markdown master for {number:02d}; found {len(markdown_matches)}"
            )
        markdown = markdown_matches[0]
        entries.extend(
            [
                (colour, f"{COLOUR_FOLDER}/{colour.name}"),
                (printer, f"{PRINT_FOLDER}/{printer.name}"),
                (markdown, f"{MARKDOWN_FOLDER}/{markdown.name}"),
            ]
        )
    return entries


def build_archive() -> Path:
    entries = inventory()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(
        OUTPUT,
        "w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
    ) as archive:
        for source, archived_name in entries:
            archive.write(source, archived_name)

    expected_names = {archived_name for _source, archived_name in entries}
    with zipfile.ZipFile(OUTPUT) as archive:
        names = archive.namelist()
        if len(names) != 45 or len(set(names)) != 45:
            raise ValueError(f"Expected 45 unique archive members; found {len(names)}")
        if set(names) != expected_names:
            raise ValueError("Complete collection ZIP inventory mismatch")
        if archive.testzip() is not None:
            raise ValueError("Complete collection ZIP CRC failure")
        for source, archived_name in entries:
            if archive.read(archived_name) != source.read_bytes():
                raise ValueError(f"Archived file differs from source: {archived_name}")

    size = OUTPUT.stat().st_size
    if size >= 20 * 1024 * 1024:
        raise ValueError(f"Complete collection ZIP exceeds 20 MiB: {size} bytes")
    print(
        "Complete collection archive: PASS — "
        "15 colourful PDFs + 15 printer PDFs + 15 Markdown masters; "
        f"45 byte-identical files; {size / 1024 / 1024:.2f} MiB"
    )
    print(OUTPUT)
    return OUTPUT


def main() -> int:
    build_archive()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
