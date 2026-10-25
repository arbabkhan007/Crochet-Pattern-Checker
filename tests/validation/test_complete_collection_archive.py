"""Integrity test for the complete 45-file customer collection archive."""

from __future__ import annotations

import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RELEASE = ROOT / "release"
PATTERNS = ROOT / "patterns"
ARCHIVE = RELEASE / "Novality_Crochet_Studio_NS01-NS15_COMPLETE_PDF_AND_MARKDOWN_COLLECTION.zip"


def test_complete_collection_archive_matches_release_files_byte_for_byte():
    expected: dict[str, Path] = {}
    for number in range(1, 16):
        code = f"NS{number:02d}"
        colour = next(RELEASE.glob(f"{code}_*_Crochet_Pattern.pdf"))
        printer = next(RELEASE.glob(f"{code}_*_PRINTER_SAVER.pdf"))
        markdown = next(PATTERNS.glob(f"{number:02d}_*.md"))
        expected[f"01_COLOURFUL_PDFS/{colour.name}"] = colour
        expected[f"02_BLACK_AND_WHITE_PRINT_PDFS/{printer.name}"] = printer
        expected[f"03_AUDITED_MARKDOWN_MASTERS/{markdown.name}"] = markdown

    with zipfile.ZipFile(ARCHIVE) as archive:
        assert len(archive.namelist()) == 45
        assert len(set(archive.namelist())) == 45
        assert set(archive.namelist()) == set(expected)
        assert archive.testzip() is None
        for archived_name, source in expected.items():
            assert archive.read(archived_name) == source.read_bytes()

    assert ARCHIVE.stat().st_size < 20 * 1024 * 1024
