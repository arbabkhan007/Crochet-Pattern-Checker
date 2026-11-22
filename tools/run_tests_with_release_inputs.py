#!/usr/bin/env python3
"""Fetch external release-test inputs, build exact-member ZIPs, then run pytest.

PDFs and the two NS01 concept images stay in an external checksum-verified
cache. Collection archives are generated from the current checkout's Markdown
masters and the pinned release PDFs. The test process receives the cache root
through CROCHET_RELEASE_INPUT_CACHE; nothing is copied into the checkout.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

from fetch_release_test_inputs import (
    DEFAULT_CACHE,
    EXPECTED_COMMIT,
    validate_external_cache,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
FETCHER = Path(__file__).with_name("fetch_release_test_inputs.py")
NS01_NS15_ARCHIVE = (
    "Novality_Crochet_Studio_NS01-NS15_COMPLETE_PDF_AND_MARKDOWN_COLLECTION.zip"
)
NS16_NS17_ARCHIVE = (
    "Novality_Crochet_Studio_NS16-NS17_PDF_AND_MARKDOWN_COLLECTION.zip"
)


def exactly_one(paths: list[Path], description: str) -> Path:
    if len(paths) != 1:
        raise FileNotFoundError(
            f"expected exactly one {description}, found {len(paths)}: "
            + ", ".join(str(path) for path in paths)
        )
    return paths[0]


def ns01_ns15_members(cache_root: Path) -> dict[str, Path]:
    release = cache_root / "release"
    patterns = REPO_ROOT / "patterns"
    members: dict[str, Path] = {}
    for number in range(1, 16):
        code = f"NS{number:02d}"
        colour = exactly_one(
            sorted(release.glob(f"{code}_*_Crochet_Pattern.pdf")),
            f"{code} full-colour release PDF",
        )
        printer = exactly_one(
            sorted(release.glob(f"{code}_*_PRINTER_SAVER.pdf")),
            f"{code} printer-saver release PDF",
        )
        markdown = exactly_one(
            sorted(patterns.glob(f"{number:02d}_*.md")),
            f"{code} canonical Markdown master",
        )
        members[f"01_COLOURFUL_PDFS/{colour.name}"] = colour
        members[f"02_BLACK_AND_WHITE_PRINT_PDFS/{printer.name}"] = printer
        members[f"03_AUDITED_MARKDOWN_MASTERS/{markdown.name}"] = markdown
    if len(members) != 45:
        raise ValueError(f"NS01–NS15 collection should have 45 members, got {len(members)}")
    return members


def ns16_ns17_members(cache_root: Path) -> dict[str, Path]:
    release = cache_root / "release"
    patterns = REPO_ROOT / "patterns"
    members = {
        "Full_Colour_PDFs/NS16_Crochet_Mini_Stocking_Advent_Garland_Crochet_Pattern.pdf": release
        / "NS16_Crochet_Mini_Stocking_Advent_Garland_Crochet_Pattern.pdf",
        "Full_Colour_PDFs/NS17_Year_of_the_Fire_Goat_2027_Plushie_Set_Crochet_Pattern.pdf": release
        / "NS17_Year_of_the_Fire_Goat_2027_Plushie_Set_Crochet_Pattern.pdf",
        "Printer_Saver_PDFs/NS16_Crochet_Mini_Stocking_Advent_Garland_PRINTER_SAVER.pdf": release
        / "NS16_Crochet_Mini_Stocking_Advent_Garland_PRINTER_SAVER.pdf",
        "Printer_Saver_PDFs/NS17_Year_of_the_Fire_Goat_2027_Plushie_Set_PRINTER_SAVER.pdf": release
        / "NS17_Year_of_the_Fire_Goat_2027_Plushie_Set_PRINTER_SAVER.pdf",
        "Markdown_Masters/16_Crochet_Mini_Stocking_Advent_Garland.md": patterns
        / "16_Crochet_Mini_Stocking_Advent_Garland.md",
        "Markdown_Masters/17_Year_of_the_Fire_Goat_2027_Plushie_Set.md": patterns
        / "17_Year_of_the_Fire_Goat_2027_Plushie_Set.md",
    }
    missing = [str(path) for path in members.values() if not path.is_file()]
    if missing:
        raise FileNotFoundError("missing NS16–NS17 archive source(s): " + ", ".join(missing))
    return members


def verify_archive(archive_path: Path, members: dict[str, Path]) -> None:
    expected_names = set(members)
    with zipfile.ZipFile(archive_path) as archive:
        names = archive.namelist()
        if len(names) != len(expected_names) or set(names) != expected_names:
            raise ValueError(f"generated archive has an unexpected member list: {archive_path}")
        corrupt = archive.testzip()
        if corrupt is not None:
            raise ValueError(f"CRC failure in {archive_path}: {corrupt}")
        for archived_name, source in members.items():
            if archive.read(archived_name) != source.read_bytes():
                raise ValueError(
                    f"archive member is not byte-identical to its source: "
                    f"{archived_name} in {archive_path}"
                )
    if archive_path.stat().st_size >= 20 * 1024 * 1024:
        raise ValueError(f"generated archive exceeds the 20 MiB test limit: {archive_path}")


def write_archive(archive_path: Path, members: dict[str, Path]) -> None:
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary_name = tempfile.mkstemp(
        prefix=f".{archive_path.name}.", suffix=".tmp", dir=archive_path.parent
    )
    os.close(fd)
    temporary = Path(temporary_name)
    try:
        with zipfile.ZipFile(
            temporary, mode="w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
        ) as archive:
            for archived_name, source in members.items():
                archive.write(source, arcname=archived_name)
        verify_archive(temporary, members)
        os.replace(temporary, archive_path)
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass


def prepare_archives(cache_root: Path) -> list[Path]:
    first = cache_root / "release" / NS01_NS15_ARCHIVE
    second = cache_root / "release" / NS16_NS17_ARCHIVE
    write_archive(first, ns01_ns15_members(cache_root))
    write_archive(second, ns16_ns17_members(cache_root))
    print(f"[built] {first} (current Markdown + pinned release PDFs)")
    print(f"[built] {second} (current Markdown + pinned release PDFs)")
    return [first, second]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cache-dir",
        type=Path,
        default=None,
        help="external cache root (default: CROCHET_RELEASE_INPUT_CACHE or ~/.cache/.../<commit>)",
    )
    parser.add_argument(
        "--prepare-only",
        action="store_true",
        help="fetch inputs and build the two archives, without invoking pytest",
    )
    args, pytest_args = parser.parse_known_args()
    if pytest_args and pytest_args[0] == "--":
        pytest_args = pytest_args[1:]

    try:
        cache_arg = args.cache_dir or Path(
            os.environ.get("CROCHET_RELEASE_INPUT_CACHE", DEFAULT_CACHE)
        )
        cache_root = validate_external_cache(cache_arg)
        if not (REPO_ROOT / "pyproject.toml").is_file() or not (REPO_ROOT / "patterns").is_dir():
            raise RuntimeError(f"does not look like a repository checkout: {REPO_ROOT}")

        subprocess.run(
            [
                sys.executable,
                str(FETCHER),
                "--group",
                "all",
                "--cache-dir",
                str(cache_root),
            ],
            cwd=REPO_ROOT,
            check=True,
        )
        prepare_archives(cache_root)
        if args.prepare_only:
            print(f"Prepared test inputs under external cache: {cache_root}")
            return 0

        env = os.environ.copy()
        env["CROCHET_RELEASE_INPUT_CACHE"] = str(cache_root)
        command = [sys.executable, "-m", "pytest", *(pytest_args or ["tests/"])]
        print(
            f"Running tests with release inputs cached outside the checkout: {cache_root}",
            flush=True,
        )
        return subprocess.run(command, cwd=REPO_ROOT, env=env, check=False).returncode
    except subprocess.CalledProcessError as exc:
        return exc.returncode or 1
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
