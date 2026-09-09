"""Render final PDFs to PNGs (for visual QA) and run structural checks.

Checks per PDF:
  * opens with PyMuPDF, page count sane
  * text extractable on every page (no blank/broken pages)
  * brand + (c) notice present in extracted text
  * no placeholder / debug / internal tokens
Writes PNGs to final_patterns/_qa/<pdfname>/pageNN.png
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import fitz  # PyMuPDF

BASE = Path("final_patterns")
QA = BASE / "_qa"

BAD_TOKENS = re.compile(
    r"(placeholder|lorem|TODO|FIXME|debug|tentative|confirm with studio|"
    r"stitch-count audit|repo parser|hand-computed|crochet_checker)",
    re.IGNORECASE)


def check(pdf_path: Path) -> list[str]:
    issues = []
    doc = fitz.open(str(pdf_path))
    if len(doc) < 3:
        issues.append(f"only {len(doc)} pages")
    outdir = QA / pdf_path.stem
    outdir.mkdir(parents=True, exist_ok=True)
    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=110)
        pix.save(str(outdir / f"page{i + 1:02d}.png"))
        text = page.get_text()
        if not text.strip():
            issues.append(f"page {i + 1}: no text (blank page?)")
        if m := BAD_TOKENS.search(text):
            issues.append(f"page {i + 1}: internal token '{m.group(0)}' present")
    full = "\n".join(page.get_text() for page in doc)
    for needle in ("Novality Store", "© 2026 Novality Store", "Terms of Use",
                   "personal use only"):
        if needle not in full:
            issues.append(f"missing required text: {needle!r}")
    # page-boundary sanity: no text outside printable area
    for i, page in enumerate(doc):
        for x0, y0, x1, y1, *_ in page.get_text("words"):
            if x1 > page.rect.width + 1 or y1 > page.rect.height + 1:
                issues.append(f"page {i + 1}: text overflows page bounds")
                break
    doc.close()
    return issues


def main():
    pdfs = sorted(BASE.glob("Pattern_*.pdf"))
    if len(pdfs) != 10:
        print(f"FAIL: expected 10 PDFs, found {len(pdfs)}")
        sys.exit(1)
    ok = True
    for p in pdfs:
        issues = check(p)
        status = "PASS" if not issues else "ISSUES"
        print(f"[{status}] {p.name}")
        for i in issues:
            ok = False
            print(f"    {i}")
    if not ok:
        sys.exit(1)
    print("Structural QA passed for all 10 PDFs.")


if __name__ == "__main__":
    main()
