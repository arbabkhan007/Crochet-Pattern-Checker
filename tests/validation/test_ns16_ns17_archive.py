from __future__ import annotations

import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RELEASE = ROOT / "release"
PATTERNS = ROOT / "patterns"
ARCHIVE = RELEASE / "Novality_Crochet_Studio_NS16-NS17_PDF_AND_MARKDOWN_COLLECTION.zip"


def expected_members() -> dict[str, Path]:
    return {
        "Full_Colour_PDFs/NS16_Crochet_Mini_Stocking_Advent_Garland_Crochet_Pattern.pdf": RELEASE
        / "NS16_Crochet_Mini_Stocking_Advent_Garland_Crochet_Pattern.pdf",
        "Full_Colour_PDFs/NS17_Year_of_the_Fire_Goat_2027_Plushie_Set_Crochet_Pattern.pdf": RELEASE
        / "NS17_Year_of_the_Fire_Goat_2027_Plushie_Set_Crochet_Pattern.pdf",
        "Printer_Saver_PDFs/NS16_Crochet_Mini_Stocking_Advent_Garland_PRINTER_SAVER.pdf": RELEASE
        / "NS16_Crochet_Mini_Stocking_Advent_Garland_PRINTER_SAVER.pdf",
        "Printer_Saver_PDFs/NS17_Year_of_the_Fire_Goat_2027_Plushie_Set_PRINTER_SAVER.pdf": RELEASE
        / "NS17_Year_of_the_Fire_Goat_2027_Plushie_Set_PRINTER_SAVER.pdf",
        "Markdown_Masters/16_Crochet_Mini_Stocking_Advent_Garland.md": PATTERNS
        / "16_Crochet_Mini_Stocking_Advent_Garland.md",
        "Markdown_Masters/17_Year_of_the_Fire_Goat_2027_Plushie_Set.md": PATTERNS
        / "17_Year_of_the_Fire_Goat_2027_Plushie_Set.md",
    }


def test_ns16_ns17_archive_is_exact_crc_clean_and_byte_identical():
    expected = expected_members()

    assert ARCHIVE.is_file()
    assert ARCHIVE.stat().st_size < 20 * 1024 * 1024
    assert all(path.is_file() for path in expected.values())

    with zipfile.ZipFile(ARCHIVE) as archive:
        assert set(archive.namelist()) == set(expected)
        assert archive.testzip() is None
        for archive_name, source in expected.items():
            assert archive.read(archive_name) == source.read_bytes()
