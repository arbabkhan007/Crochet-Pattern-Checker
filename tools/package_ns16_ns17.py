#!/usr/bin/env python3
"""Build and verify the six-file NS 16–NS 17 customer collection archive."""

from __future__ import annotations

import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RELEASE = ROOT / "release"
PATTERNS = ROOT / "patterns"
OUTPUT = RELEASE / "Novality_Crochet_Studio_NS16-NS17_PDF_AND_MARKDOWN_COLLECTION.zip"

PDFS = (
    "NS16_Crochet_Mini_Stocking_Advent_Garland_Crochet_Pattern.pdf",
    "NS16_Crochet_Mini_Stocking_Advent_Garland_PRINTER_SAVER.pdf",
    "NS17_Year_of_the_Fire_Goat_2027_Plushie_Set_Crochet_Pattern.pdf",
    "NS17_Year_of_the_Fire_Goat_2027_Plushie_Set_PRINTER_SAVER.pdf",
)
MARKDOWN = (
    "16_Crochet_Mini_Stocking_Advent_Garland.md",
    "17_Year_of_the_Fire_Goat_2027_Plushie_Set.md",
)


def members() -> dict[str, Path]:
    result: dict[str, Path] = {}
    for name in PDFS:
        folder = "Printer_Saver_PDFs" if "PRINTER_SAVER" in name else "Full_Colour_PDFs"
        result[f"{folder}/{name}"] = RELEASE / name
    for name in MARKDOWN:
        result[f"Markdown_Masters/{name}"] = PATTERNS / name
    return result


def build_archive() -> Path:
    inventory = members()
    missing = [str(path) for path in inventory.values() if not path.is_file()]
    if missing:
        raise FileNotFoundError("Missing NS 16–NS 17 release inputs: " + ", ".join(missing))

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(OUTPUT, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for archive_name, source in sorted(inventory.items()):
            archive.write(source, arcname=archive_name)

    with zipfile.ZipFile(OUTPUT) as archive:
        if set(archive.namelist()) != set(inventory):
            raise ValueError("NS 16–NS 17 archive inventory mismatch")
        bad_member = archive.testzip()
        if bad_member:
            raise ValueError(f"NS 16–NS 17 archive CRC failure: {bad_member}")
        for archive_name, source in inventory.items():
            if archive.read(archive_name) != source.read_bytes():
                raise ValueError(f"Archive member is not byte-identical: {archive_name}")

    if OUTPUT.stat().st_size >= 20 * 1024 * 1024:
        raise ValueError("NS 16–NS 17 archive exceeds Etsy's 20 MB per-file limit")
    print(
        f"NS 16–NS 17 archive: PASS — {len(inventory)} byte-identical files, "
        f"{OUTPUT.stat().st_size / 1024 / 1024:.2f} MiB"
    )
    print(OUTPUT)
    return OUTPUT


if __name__ == "__main__":
    build_archive()
