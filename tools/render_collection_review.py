#!/usr/bin/env python3
"""Render every NS 02–NS 15 PDF page and create visual-review galleries.

Outputs go under build/, which is intentionally excluded from release artifacts.
This is a production-review utility, not part of the customer download.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pymupdf
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
RELEASE = ROOT / "release"
OUT = ROOT / "build" / "collection_render_review"


@dataclass(frozen=True)
class RenderedPdf:
    code: str
    edition: str
    pdf: Path
    pages: tuple[Path, ...]
    char_counts: tuple[int, ...]


def font(size: int, *, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    paths = (
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
        if bold
        else Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
        Path("/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf")
        if bold
        else Path("/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"),
    )
    for path in paths:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def render_pdf(pdf: Path, code: str, edition: str) -> RenderedPdf:
    output = OUT / f"{code}_{edition}"
    output.mkdir(parents=True, exist_ok=True)
    document = pymupdf.open(pdf)
    paths: list[Path] = []
    counts: list[int] = []
    for index, page in enumerate(document):
        text = page.get_text()
        if "�" in text:
            raise ValueError(f"{pdf.name} page {index + 1}: replacement glyph detected")
        counts.append(len(text))
        for block in page.get_text("blocks"):
            x0, y0, x1, y1 = block[:4]
            if x0 < -1 or y0 < -1 or x1 > page.rect.width + 1 or y1 > page.rect.height + 1:
                raise ValueError(f"{pdf.name} page {index + 1}: text block out of bounds {block[:4]}")
        pixmap = page.get_pixmap(matrix=pymupdf.Matrix(1.35, 1.35), alpha=False)
        path = output / f"page-{index + 1:02d}.jpg"
        pixmap.pil_image().save(path, quality=86, optimize=True)
        image = Image.open(path).convert("RGB")
        # Every page must contain a meaningful amount of non-white rendered ink.
        sample = image.resize((120, 170), Image.Resampling.BILINEAR)
        nonwhite = sum(1 for pixel in sample.getdata() if min(pixel) < 244)
        if nonwhite < 115:
            raise ValueError(f"{pdf.name} page {index + 1}: visually near-blank ({nonwhite} sampled pixels)")
        paths.append(path)
    document.close()
    return RenderedPdf(code, edition, pdf, tuple(paths), tuple(counts))


def gallery(name: str, items: list[tuple[Path, str]], *, columns: int = 4, thumb_width: int = 315) -> Path:
    if not items:
        raise ValueError("Gallery has no items")
    first = Image.open(items[0][0])
    thumb_height = round(first.height * thumb_width / first.width)
    label_height = 37
    rows = (len(items) + columns - 1) // columns
    sheet = Image.new("RGB", (columns * thumb_width, rows * (thumb_height + label_height)), "#D5D1CB")
    draw = ImageDraw.Draw(sheet)
    label_font = font(14, bold=True)
    for index, (path, label) in enumerate(items):
        image = Image.open(path).convert("RGB")
        image.thumbnail((thumb_width, thumb_height), Image.Resampling.LANCZOS)
        x = (index % columns) * thumb_width + (thumb_width - image.width) // 2
        y = (index // columns) * (thumb_height + label_height)
        sheet.paste(image, (x, y))
        draw.text(((index % columns) * thumb_width + 7, y + thumb_height + 8), label, fill="black", font=label_font)
    destination = OUT / f"{name}.jpg"
    sheet.save(destination, quality=90, optimize=True)
    return destination


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    rendered: list[RenderedPdf] = []
    for number in range(2, 16):
        code = f"NS{number:02d}"
        main_pdf = next(RELEASE.glob(f"{code}_*_Crochet_Pattern.pdf"))
        print_pdf = next(RELEASE.glob(f"{code}_*_PRINTER_SAVER.pdf"))
        rendered.append(render_pdf(main_pdf, code, "main"))
        rendered.append(render_pdf(print_pdf, code, "print"))

    main_pdfs = [item for item in rendered if item.edition == "main"]
    print_pdfs = [item for item in rendered if item.edition == "print"]
    outputs = []
    outputs.append(gallery("01_full_colour_covers", [(item.pages[0], f"{item.code} · COVER") for item in main_pdfs], columns=4))
    outputs.append(gallery("02_profiles_and_maker_maps", [(item.pages[1], f"{item.code} · PROFILE") for item in main_pdfs], columns=3, thumb_width=360))
    outputs.append(gallery("03_contents", [(item.pages[2], f"{item.code} · CONTENTS") for item in main_pdfs], columns=4))

    dense_main: list[tuple[Path, str]] = []
    for item in main_pdfs:
        candidates = range(3, max(4, len(item.pages) - 1))
        index = max(candidates, key=lambda candidate: item.char_counts[candidate])
        dense_main.append((item.pages[index], f"{item.code} · DENSE PAGE {index + 1} · {item.char_counts[index]} CHARS"))
    outputs.append(gallery("04_densest_full_colour_pages", dense_main, columns=3, thumb_width=360))
    outputs.append(gallery("05_full_colour_closing_pages", [(item.pages[-1], f"{item.code} · CLOSING") for item in main_pdfs], columns=4))

    print_selection: list[tuple[Path, str]] = []
    for item in print_pdfs:
        candidates = range(3, max(4, len(item.pages) - 1))
        index = max(candidates, key=lambda candidate: item.char_counts[candidate])
        print_selection.extend(
            [
                (item.pages[0], f"{item.code} · PRINT COVER"),
                (item.pages[index], f"{item.code} · PRINT DENSE {index + 1}"),
                (item.pages[-1], f"{item.code} · NOTES"),
            ]
        )
    outputs.append(gallery("06_printer_saver_representative", print_selection, columns=3, thumb_width=360))

    total_pages = sum(len(item.pages) for item in rendered)
    print(f"Render audit: PASS — {len(rendered)} PDFs, {total_pages} pages rendered")
    for output in outputs:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
