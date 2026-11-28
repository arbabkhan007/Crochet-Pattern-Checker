#!/usr/bin/env python3
"""Check rendered Novality release PDFs for common layout regressions.

Run after building the NS 01 and NS 02–17 release editions:
    python tools/audit_pdf_layouts.py

The checks cover text outside page bounds, orphaned source headings at page
ends, and overlap between the safety and copyright panels on the profile page.
This is a focused regression audit, not a substitute for a complete visual,
content, accessibility, or pattern-accuracy review.
"""
from __future__ import annotations

import argparse
import importlib.util
import re
import sys
import unicodedata
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))


def load_builder(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load PDF builder: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


remaining = load_builder(
    "layout_remaining_builder", TOOLS / "build_remaining_pattern_pdfs.py"
)
ns01 = load_builder("layout_ns01_builder", TOOLS / "build_ns01_etsy_pdf.py")


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).casefold()
    text = re.sub(r"\s+", " ", text)
    return re.sub(r"[^\w]+", " ", text).strip()


def page_text_blocks(page):
    blocks = []
    for block in page.get_text("dict")["blocks"]:
        if "lines" not in block:
            continue
        text = " ".join(
            span["text"]
            for line in block["lines"]
            for span in line["spans"]
        ).strip()
        if text:
            blocks.append((pymupdf.Rect(block["bbox"]), text))
    return blocks


def get_profile_panel_gap(document) -> float:
    safety = copyright = None
    for page in document:
        for text_rect, text in page_text_blocks(page):
            normalized = normalize(text)
            if normalized.startswith("safety this pdf does not claim") or normalized.startswith(
                "safety plastic eyes"
            ):
                safety = (page.number, text_rect)
            if normalized.startswith("copyright notice"):
                copyright = (page.number, text_rect)

    if safety is None or copyright is None:
        raise ValueError("Safety and copyright panels were not both found")

    def enclosing_panel(page, text_rect):
        candidates = [
            drawing["rect"]
            for drawing in page.get_drawings()
            if drawing["rect"].width > 400
            and drawing["rect"].height > 20
            and drawing["rect"].contains(text_rect)
        ]
        return min(candidates, key=lambda rect: rect.width * rect.height) if candidates else None

    safety_box = enclosing_panel(document[safety[0]], safety[1])
    copyright_box = enclosing_panel(document[copyright[0]], copyright[1])
    if safety_box is None or copyright_box is None:
        raise ValueError("Could not locate the safety/copyright panel borders")
    return copyright_box.y0 - safety_box.y1


def source_headings(source: str, parser, normalizer) -> set[str]:
    headings = set()
    for block in parser(normalizer(source)):
        if (
            block.kind == "heading"
            and block.level > 1
            and str(block.value) != "Happy crocheting!"
        ):
            headings.add(normalize(str(block.value)))
    return headings


def audit_pdf(path: Path, headings: set[str]) -> tuple[int, float]:
    if not path.is_file():
        raise FileNotFoundError(path)

    document = pymupdf.open(path)
    out_of_bounds = []
    orphan_headings = []

    for page in document:
        for word in page.get_text("words"):
            x0, y0, x1, y1 = word[:4]
            if (
                x0 < -0.3
                or y0 < -0.3
                or x1 > page.rect.width + 0.3
                or y1 > page.rect.height + 0.3
            ):
                out_of_bounds.append((page.number + 1, word[4]))

        content = [
            (rect, text)
            for rect, text in page_text_blocks(page)
            if 50 < rect.y0 and rect.y1 < page.rect.height - 35
        ]
        content.sort(key=lambda item: (item[0].y1, item[0].x0))
        if content and normalize(content[-1][1]) in headings:
            orphan_headings.append((page.number + 1, content[-1][1]))

    gap = get_profile_panel_gap(document)
    pages = len(document)
    document.close()

    if gap <= 0:
        raise ValueError(f"{path.name}: safety/copyright panels overlap by {-gap:.2f} pt")
    if orphan_headings:
        raise ValueError(f"{path.name}: page-end heading(s) without following content: {orphan_headings}")
    if out_of_bounds:
        raise ValueError(f"{path.name}: text outside page bounds: {out_of_bounds[:3]}")
    return pages, gap


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--release-dir",
        type=Path,
        default=ROOT / "release",
        help="Directory containing the generated release PDFs (default: ./release)",
    )
    args = parser.parse_args()
    release_dir = args.release_dir.expanduser().resolve()

    results = []
    for pattern in remaining.SPECS:
        headings = source_headings(
            pattern.source.read_text(encoding="utf-8"),
            remaining.parse_markdown,
            remaining.normalize_branding,
        )
        for edition, output_name in (
            ("colour", pattern.main_output.name),
            ("printer-saver", pattern.printer_output.name),
        ):
            path = release_dir / output_name
            pages, gap = audit_pdf(path, headings)
            results.append((pattern.number, edition, pages, gap))

    ns01_source = (ROOT / "patterns/01_Hamish_the_Highland_Cow.md").read_text(
        encoding="utf-8"
    )
    headings = source_headings(
        ns01_source, ns01.parse_markdown, ns01.normalize_branding
    )
    for edition, name in (
        ("colour", "NS01_Hamish_the_Highland_Cow_Crochet_Pattern.pdf"),
        ("printer-saver", "NS01_Hamish_the_Highland_Cow_PRINTER_SAVER.pdf"),
    ):
        pages, gap = audit_pdf(release_dir / name, headings)
        results.append((1, edition, pages, gap))

    print(
        f"PASS — {len(results)} PDFs; minimum profile-panel gap "
        f"{min(result[3] for result in results):.2f} pt; "
        "no orphan headings; no text outside page bounds."
    )
    for code, edition, pages, gap in sorted(results):
        print(f"NS{code:02d} {edition:13} {pages:2} pages  gap {gap:.2f} pt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
