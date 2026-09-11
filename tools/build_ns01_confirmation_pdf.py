#!/usr/bin/env python3
"""Build the NS 01 branded confirmation proof from its audited Markdown master.

This proof intentionally labels the generated cover artwork as concept imagery. Replace
it with photographs of a physically tested sample before creating a retail PDF.
"""

from __future__ import annotations

import argparse
import re
import tempfile
from dataclasses import dataclass
from hashlib import sha256
from html import escape
from pathlib import Path
from typing import Iterable, Sequence

from PIL import Image as PILImage
from PIL import ImageDraw, ImageFont
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    CondPageBreak,
    Flowable,
    Frame,
    HRFlowable,
    Image,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.platypus.tableofcontents import TableOfContents
from pypdf import PdfReader
from pypdf.generic import IndirectObject


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "patterns/01_Hamish_the_Highland_Cow.md"
HERO = ROOT / "assets/patterns/ns01/hamish_cover_concept.png"
DEFAULT_OUTPUT = ROOT / "proofs/NS01_Hamish_the_Highland_Cow_CONFIRMATION_PROOF.pdf"
ASSET_DIR = Path(tempfile.gettempdir()) / "novality-pdf-assets/ns01"

PAGE_WIDTH, PAGE_HEIGHT = A4
BRAND = "Novality Crochet Studio"
DESIGN_CODE = "NS 01"
TITLE = "Hamish"
SUBTITLE = "the Highland Cow"
REVISION = "Confirmation proof · 11 September 2026"

INK = HexColor("#28231F")
FOREST = HexColor("#31473B")
FOREST_DARK = HexColor("#213229")
GINGER = HexColor("#B9652B")
GINGER_LIGHT = HexColor("#D08A4B")
OAT = HexColor("#E7D7B8")
PARCHMENT = HexColor("#F7F1E7")
PAPER = HexColor("#FFFDF8")
CHOCOLATE = HexColor("#4A2B23")
RUST = HexColor("#9A4630")
MOSS = HexColor("#76836A")
MUTED = HexColor("#6F665E")
LINE = HexColor("#D8CDBE")
PALE_GINGER = HexColor("#F3E1D2")
PALE_GREEN = HexColor("#E7ECE7")
WARNING_BG = HexColor("#F5E5D7")


@dataclass(frozen=True)
class Fonts:
    sans: str
    sans_bold: str
    serif: str
    serif_bold: str


@dataclass(frozen=True)
class Block:
    kind: str
    value: object
    level: int = 0


def register_fonts() -> Fonts:
    """Register embedded DejaVu faces, with PDF core-font fallbacks."""

    font_dir = Path("/usr/share/fonts/truetype/dejavu")
    candidates = {
        "NovalitySans": font_dir / "DejaVuSans.ttf",
        "NovalitySansBold": font_dir / "DejaVuSans-Bold.ttf",
        "NovalitySerif": font_dir / "DejaVuSerif.ttf",
        "NovalitySerifBold": font_dir / "DejaVuSerif-Bold.ttf",
    }
    if all(path.exists() for path in candidates.values()):
        for name, path in candidates.items():
            pdfmetrics.registerFont(TTFont(name, str(path)))
        return Fonts(
            "NovalitySans",
            "NovalitySansBold",
            "NovalitySerif",
            "NovalitySerifBold",
        )
    return Fonts("Helvetica", "Helvetica-Bold", "Times-Roman", "Times-Bold")


def pil_font(size: int, bold: bool = False, serif: bool = False) -> ImageFont.FreeTypeFont:
    font_dir = Path("/usr/share/fonts/truetype/dejavu")
    if serif:
        name = "DejaVuSerif-Bold.ttf" if bold else "DejaVuSerif.ttf"
    else:
        name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    try:
        return ImageFont.truetype(str(font_dir / name), size=size)
    except OSError:
        return ImageFont.load_default()


def create_palette_asset(path: Path) -> None:
    """Create the original-colour palette figure used in the proof."""

    path.parent.mkdir(parents=True, exist_ok=True)
    canvas = PILImage.new("RGB", (1800, 820), "#F7F1E7")
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((40, 40, 1760, 780), radius=38, fill="#FFFDF8", outline="#D8CDBE", width=3)
    draw.text((105, 90), "ORIGINAL COLOUR STORY", font=pil_font(52, bold=True, serif=True), fill="#28231F")
    draw.text(
        (107, 160),
        "Warm Highland tones · keep dye-lot labels with the sample record",
        font=pil_font(26),
        fill="#6F665E",
    )

    swatches = [
        ("YARN A", "GINGER", "body + fringe · about 25 g", "#B9652B"),
        ("YARN B", "OAT CREAM", "muzzle + horns + inner ears · 12 g", "#E7D7B8"),
        ("YARN C", "DARK CHOCOLATE", "hooves + nostrils · 5 g", "#4A2B23"),
        ("YARN D", "RUST / TARTAN", "optional scarf · about 6 g", "#9A4630"),
    ]
    start_x = 105
    card_w = 380
    gap = 34
    for index, (code, name, use, colour) in enumerate(swatches):
        x = start_x + index * (card_w + gap)
        draw.rounded_rectangle((x, 245, x + card_w, 690), radius=26, fill="#FAF6EF", outline="#E4D8C9", width=3)
        draw.rounded_rectangle((x + 28, 273, x + card_w - 28, 465), radius=22, fill=colour)
        contrast = "#FFFDF8" if name != "OAT CREAM" else "#4A2B23"
        draw.text((x + 50, 303), code, font=pil_font(23, bold=True), fill=contrast)
        draw.text((x + 28, 503), name, font=pil_font(30, bold=True, serif=True), fill="#28231F")
        wrapped = wrap_words(use, 29)
        draw.multiline_text((x + 28, 560), wrapped, font=pil_font(21), fill="#6F665E", spacing=8)

    draw.text(
        (107, 721),
        "Screen colours are a guide only. Use the yarn description—not a hex value—to select materials.",
        font=pil_font(20),
        fill="#6F665E",
    )
    canvas.save(path, quality=95)


def create_assembly_asset(path: Path) -> None:
    """Create a visual assembly-order figure without replacing written directions."""

    path.parent.mkdir(parents=True, exist_ok=True)
    canvas = PILImage.new("RGB", (1800, 1180), "#F7F1E7")
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((40, 40, 1760, 1140), radius=38, fill="#FFFDF8", outline="#D8CDBE", width=3)
    draw.text((105, 85), "ASSEMBLY MAP", font=pil_font(54, bold=True, serif=True), fill="#28231F")
    draw.text(
        (107, 158),
        "Pin first. Check symmetry. Then sew in this exact order.",
        font=pil_font(27),
        fill="#6F665E",
    )

    steps = [
        ("01", "MUZZLE + FACE", "Lock eye washers before the head closes."),
        ("02", "HORNS", "Rnds 5–7 · angle out and slightly back."),
        ("03", "EARS", "Outside horns · cup the nested layers forward."),
        ("04", "FRINGE", "Attach after horns and ears; trim unevenly."),
        ("05", "HEAD → BODY", "Match 18 neck sts to 18 Head Rnd-14 sts."),
        ("06", "BACK LEGS", "Rnds 3–6 · low and almost horizontal."),
        ("07", "FRONT LEGS", "Rnds 8–9 · about 8 sts apart."),
        ("08", "BELLY PATCH", "Optional · centre after the legs are checked."),
        ("09", "TAIL + SCARF", "Add last; weave and inspect every end."),
    ]
    columns = 3
    card_w = 500
    card_h = 215
    x0, y0 = 105, 245
    x_gap, y_gap = 45, 38
    for i, (number, label, note) in enumerate(steps):
        row, col = divmod(i, columns)
        x = x0 + col * (card_w + x_gap)
        y = y0 + row * (card_h + y_gap)
        fill = "#F3E1D2" if i == 4 else "#F6F4EE"
        outline = "#B9652B" if i == 4 else "#D8CDBE"
        draw.rounded_rectangle((x, y, x + card_w, y + card_h), radius=24, fill=fill, outline=outline, width=4)
        draw.ellipse((x + 24, y + 25, x + 106, y + 107), fill="#31473B")
        number_box = draw.textbbox((0, 0), number, font=pil_font(27, bold=True))
        number_w = number_box[2] - number_box[0]
        draw.text((x + 65 - number_w / 2, y + 47), number, font=pil_font(27, bold=True), fill="#FFFDF8")
        draw.text((x + 128, y + 27), label, font=pil_font(25, bold=True), fill="#28231F")
        draw.multiline_text(
            (x + 128, y + 80),
            wrap_words(note, 36),
            font=pil_font(20),
            fill="#5F5750",
            spacing=7,
        )

    draw.rounded_rectangle((105, 1010, 1695, 1090), radius=20, fill="#31473B")
    critical = "CRITICAL NECK JOIN   18 BODY STS ↔ 18 HEAD STS   ·   LADDER-STITCH TWICE"
    box = draw.textbbox((0, 0), critical, font=pil_font(25, bold=True))
    text_w = box[2] - box[0]
    draw.text(((1800 - text_w) / 2, 1031), critical, font=pil_font(25, bold=True), fill="#FFFDF8")
    canvas.save(path, quality=95)


def wrap_words(text: str, width: int) -> str:
    words = text.split()
    lines: list[str] = []
    line: list[str] = []
    for word in words:
        candidate = " ".join([*line, word])
        if line and len(candidate) > width:
            lines.append(" ".join(line))
            line = [word]
        else:
            line.append(word)
    if line:
        lines.append(" ".join(line))
    return "\n".join(lines)


def normalize_branding(text: str) -> str:
    """Apply the owner-requested customer-facing studio brand to this proof."""

    return (
        text.replace("Novality Store", BRAND)
        .replace("#NovalityStore", "#NovalityCrochetStudio")
        .replace(
            "including all instructions, stitch counts, photography and design elements",
            "including all instructions, stitch counts, editorial layout and design elements",
        )
        .replace("© 2026 Novality Crochet Studio", f"© 2026 {BRAND}")
    )


def is_table_separator(line: str) -> bool:
    cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)


def is_special(line: str, next_line: str = "") -> bool:
    stripped = line.strip()
    if not stripped:
        return True
    if re.match(r"^#{1,4}\s+", stripped):
        return True
    if stripped == "---" or stripped.startswith("> "):
        return True
    if re.match(r"^(?:[-*]|\d+\.)\s+", stripped):
        return True
    if stripped.startswith("|") and is_table_separator(next_line):
        return True
    return False


def parse_markdown(text: str) -> list[Block]:
    """Parse the constrained customer-master Markdown into print flow blocks."""

    lines = text.splitlines()
    blocks: list[Block] = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        heading = re.match(r"^(#{1,4})\s+(.+)$", line)
        if heading:
            blocks.append(Block("heading", heading.group(2), len(heading.group(1))))
            i += 1
            continue
        if line == "---":
            blocks.append(Block("rule", ""))
            i += 1
            continue
        if line.startswith("> "):
            quote_lines = []
            while i < len(lines) and lines[i].strip().startswith("> "):
                quote_lines.append(lines[i].strip()[2:])
                i += 1
            blocks.append(Block("quote", " ".join(quote_lines)))
            continue
        if line.startswith("|") and i + 1 < len(lines) and is_table_separator(lines[i + 1].strip()):
            table_lines = [line]
            i += 2  # Skip the Markdown alignment row.
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i].strip())
                i += 1
            rows = [
                [cell.strip() for cell in row.strip().strip("|").split("|")]
                for row in table_lines
            ]
            blocks.append(Block("table", rows))
            continue
        list_match = re.match(r"^([-*]|\d+\.)\s+(.+)$", line)
        if list_match:
            marker, body = list_match.groups()
            kind = "ordered" if marker[0].isdigit() else "bullet"
            blocks.append(Block(kind, body, int(marker[:-1]) if kind == "ordered" else 0))
            i += 1
            continue

        paragraph = [line]
        i += 1
        while i < len(lines):
            following = lines[i].strip()
            after = lines[i + 1].strip() if i + 1 < len(lines) else ""
            if is_special(following, after):
                break
            paragraph.append(following)
            i += 1
        blocks.append(Block("paragraph", "\n".join(paragraph)))
    return blocks


def inline_markup(text: str) -> str:
    """Escape text and convert the limited inline Markdown used by the masters."""

    value = escape(text, quote=False)
    value = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", value)
    value = re.sub(r"`(.+?)`", r"<font name=\"Courier\">\1</font>", value)
    value = re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"<i>\1</i>", value)
    return value.replace("\n", "<br/>")


def make_styles(fonts: Fonts) -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "body": ParagraphStyle(
            "Body",
            parent=base["BodyText"],
            fontName=fonts.sans,
            fontSize=9.6,
            leading=14.2,
            textColor=INK,
            spaceAfter=6,
            allowWidows=0,
            allowOrphans=0,
        ),
        "body_compact": ParagraphStyle(
            "BodyCompact",
            parent=base["BodyText"],
            fontName=fonts.sans,
            fontSize=8.4,
            leading=11.4,
            textColor=INK,
            spaceAfter=3,
        ),
        "small": ParagraphStyle(
            "Small",
            parent=base["BodyText"],
            fontName=fonts.sans,
            fontSize=7.5,
            leading=10.3,
            textColor=MUTED,
        ),
        "quote": ParagraphStyle(
            "Quote",
            parent=base["BodyText"],
            fontName=fonts.serif_bold,
            fontSize=10.2,
            leading=14.8,
            textColor=FOREST_DARK,
            backColor=PALE_GREEN,
            borderColor=MOSS,
            borderWidth=0.7,
            borderPadding=(8, 10, 8, 10),
            spaceBefore=5,
            spaceAfter=10,
        ),
        "callout": ParagraphStyle(
            "Callout",
            parent=base["BodyText"],
            fontName=fonts.sans,
            fontSize=9.2,
            leading=13.5,
            textColor=INK,
            backColor=WARNING_BG,
            borderColor=GINGER,
            borderWidth=0.8,
            borderPadding=(8, 10, 8, 10),
            spaceAfter=8,
        ),
        "bullet": ParagraphStyle(
            "Bullet",
            parent=base["BodyText"],
            fontName=fonts.sans,
            fontSize=9.2,
            leading=13.3,
            leftIndent=12,
            firstLineIndent=-8,
            bulletIndent=2,
            textColor=INK,
            spaceAfter=4,
        ),
        "number": ParagraphStyle(
            "Number",
            parent=base["BodyText"],
            fontName=fonts.sans,
            fontSize=9.2,
            leading=13.4,
            leftIndent=17,
            firstLineIndent=-15,
            textColor=INK,
            spaceAfter=6,
        ),
        "h1": ParagraphStyle(
            "Heading1",
            parent=base["Heading1"],
            fontName=fonts.serif_bold,
            fontSize=22,
            leading=26,
            textColor=FOREST_DARK,
            spaceBefore=0,
            spaceAfter=10,
        ),
        "h2": ParagraphStyle(
            "Heading2",
            parent=base["Heading2"],
            fontName=fonts.serif_bold,
            fontSize=16,
            leading=20,
            textColor=FOREST,
            spaceBefore=12,
            spaceAfter=7,
            keepWithNext=True,
        ),
        "h3": ParagraphStyle(
            "Heading3",
            parent=base["Heading3"],
            fontName=fonts.sans_bold,
            fontSize=11.5,
            leading=15,
            textColor=GINGER,
            spaceBefore=9,
            spaceAfter=5,
            keepWithNext=True,
        ),
        "h4": ParagraphStyle(
            "Heading4",
            parent=base["Heading4"],
            fontName=fonts.sans_bold,
            fontSize=9.6,
            leading=13,
            textColor=CHOCOLATE,
            spaceBefore=6,
            spaceAfter=4,
            keepWithNext=True,
        ),
        "table_header": ParagraphStyle(
            "TableHeader",
            parent=base["BodyText"],
            fontName=fonts.sans_bold,
            fontSize=7.2,
            leading=9,
            textColor=colors.white,
            alignment=TA_LEFT,
        ),
        "table_cell": ParagraphStyle(
            "TableCell",
            parent=base["BodyText"],
            fontName=fonts.sans,
            fontSize=7.45,
            leading=9.7,
            textColor=INK,
        ),
        "table_cell_bold": ParagraphStyle(
            "TableCellBold",
            parent=base["BodyText"],
            fontName=fonts.sans_bold,
            fontSize=7.45,
            leading=9.7,
            textColor=FOREST_DARK,
        ),
        "caption": ParagraphStyle(
            "Caption",
            parent=base["BodyText"],
            fontName=fonts.sans,
            fontSize=7.2,
            leading=9.4,
            textColor=MUTED,
            alignment=TA_CENTER,
            spaceBefore=3,
            spaceAfter=10,
        ),
        "front_title": ParagraphStyle(
            "FrontTitle",
            parent=base["Heading1"],
            fontName=fonts.serif_bold,
            fontSize=22,
            leading=25,
            textColor=FOREST_DARK,
            spaceAfter=6,
        ),
        "front_body": ParagraphStyle(
            "FrontBody",
            parent=base["BodyText"],
            fontName=fonts.sans,
            fontSize=9.6,
            leading=14,
            textColor=INK,
            spaceAfter=7,
        ),
    }


class HeadingParagraph(Paragraph):
    """Paragraph carrying outline and table-of-contents metadata."""

    def __init__(self, text: str, style: ParagraphStyle, level: int, key: str):
        super().__init__(text, style)
        self.outline_level = level
        self.bookmark_key = key
        self.plain_heading = re.sub(r"<[^>]+>", "", text)


class CoverFlowable(Flowable):
    """Full-page editorial cover for the confirmation proof."""

    def __init__(self, hero: Path, fonts: Fonts):
        super().__init__()
        self.hero = hero
        self.fonts = fonts
        self.width = PAGE_WIDTH
        self.height = PAGE_HEIGHT - 0.2 * mm

    def wrap(self, available_width, available_height):  # noqa: ANN001
        return self.width, min(self.height, available_height)

    def draw(self) -> None:
        canvas = self.canv
        canvas.saveState()
        canvas.setFillColor(PARCHMENT)
        canvas.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, stroke=0, fill=1)

        canvas.setFillColor(FOREST_DARK)
        canvas.rect(0, PAGE_HEIGHT - 18 * mm, PAGE_WIDTH, 18 * mm, stroke=0, fill=1)
        canvas.setFillColor(colors.white)
        canvas.setFont(self.fonts.sans_bold, 9)
        canvas.drawString(15 * mm, PAGE_HEIGHT - 11.2 * mm, BRAND.upper())
        canvas.setFont(self.fonts.sans, 7.5)
        canvas.drawRightString(PAGE_WIDTH - 15 * mm, PAGE_HEIGHT - 11.2 * mm, "ORIGINAL CROCHET PATTERN")

        image_x, image_y = 88 * mm, 55 * mm
        image_w, image_h = 107 * mm, 195 * mm
        canvas.setFillColor(PAPER)
        canvas.roundRect(image_x - 3 * mm, image_y - 3 * mm, image_w + 6 * mm, image_h + 6 * mm, 5 * mm, stroke=0, fill=1)
        canvas.drawImage(
            str(self.hero),
            image_x,
            image_y,
            width=image_w,
            height=image_h,
            preserveAspectRatio=True,
            anchor="c",
            mask="auto",
        )

        canvas.setFillColor(GINGER)
        canvas.roundRect(14 * mm, 224 * mm, 54 * mm, 11 * mm, 5.5 * mm, stroke=0, fill=1)
        canvas.setFillColor(colors.white)
        canvas.setFont(self.fonts.sans_bold, 9.5)
        canvas.drawCentredString(41 * mm, 227.7 * mm, f"DESIGN CODE  {DESIGN_CODE}")

        canvas.setFillColor(FOREST_DARK)
        canvas.setFont(self.fonts.serif_bold, 33)
        canvas.drawString(14 * mm, 202 * mm, TITLE.upper())
        canvas.setFont(self.fonts.serif, 18)
        canvas.drawString(14 * mm, 191 * mm, SUBTITLE)

        canvas.setStrokeColor(GINGER)
        canvas.setLineWidth(2)
        canvas.line(14 * mm, 181 * mm, 70 * mm, 181 * mm)
        canvas.setFillColor(MUTED)
        canvas.setFont(self.fonts.sans, 8.4)
        canvas.drawString(14 * mm, 170 * mm, "A shaggy, sturdy Highland character")
        canvas.drawString(14 * mm, 164 * mm, "with a broad oat-cream muzzle and")
        canvas.drawString(14 * mm, 158 * mm, "a weather-beaten ginger fringe.")

        stats = [("US TERMS", 137), ("INTERMEDIATE", 126), ("6–8 HOURS", 115), ("ABOUT 15 CM", 104)]
        for label, y in stats:
            canvas.setFillColor(FOREST)
            canvas.circle(17 * mm, y * mm + 1.4 * mm, 1.6 * mm, stroke=0, fill=1)
            canvas.setFillColor(INK)
            canvas.setFont(self.fonts.sans_bold, 8.2)
            canvas.drawString(23 * mm, y * mm, label)

        canvas.setFillColor(PALE_GINGER)
        canvas.roundRect(14 * mm, 64 * mm, 62 * mm, 25 * mm, 3 * mm, stroke=0, fill=1)
        canvas.setFillColor(CHOCOLATE)
        canvas.setFont(self.fonts.sans_bold, 7.5)
        canvas.drawString(19 * mm, 81 * mm, "ORIGINAL COLOURWAY")
        canvas.setFont(self.fonts.sans, 7.2)
        canvas.drawString(19 * mm, 74 * mm, "Ginger · oat · chocolate · rust")
        canvas.drawString(19 * mm, 68.5 * mm, "Worsted / aran · 3.5 mm hook")

        canvas.setStrokeColor(LINE)
        canvas.setLineWidth(0.7)
        canvas.line(14 * mm, 42 * mm, PAGE_WIDTH - 14 * mm, 42 * mm)
        canvas.setFillColor(MUTED)
        canvas.setFont(self.fonts.sans, 6.8)
        canvas.drawString(14 * mm, 34.5 * mm, REVISION.upper())
        canvas.drawRightString(PAGE_WIDTH - 14 * mm, 34.5 * mm, "NOT FOR RETAIL")
        canvas.setFont(self.fonts.sans, 6.3)
        canvas.drawString(
            14 * mm,
            27 * mm,
            "CONCEPT COVER IMAGE — REPLACE WITH A PHOTOGRAPH OF THE TESTED SAMPLE BEFORE PUBLICATION",
        )
        canvas.setFillColor(FOREST_DARK)
        canvas.rect(0, 0, PAGE_WIDTH, 14 * mm, stroke=0, fill=1)
        canvas.setFillColor(colors.white)
        canvas.setFont(self.fonts.sans_bold, 7.2)
        canvas.drawCentredString(PAGE_WIDTH / 2, 5.1 * mm, "NOVALITY CROCHET STUDIO  ·  CONFIRMATION PROOF")
        canvas.restoreState()


class ClosingFlowable(Flowable):
    """Intentional branded back cover for the proof."""

    def __init__(self, hero: Path, fonts: Fonts):
        super().__init__()
        self.hero = hero
        self.fonts = fonts
        self.width = PAGE_WIDTH
        self.height = PAGE_HEIGHT - 0.2 * mm

    def wrap(self, available_width, available_height):  # noqa: ANN001
        return self.width, min(self.height, available_height)

    def draw(self) -> None:
        canvas = self.canv
        canvas.saveState()
        canvas.setFillColor(FOREST_DARK)
        canvas.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, stroke=0, fill=1)

        canvas.setFillColor(GINGER)
        canvas.circle(PAGE_WIDTH / 2, 237 * mm, 23 * mm, stroke=0, fill=1)
        canvas.setFillColor(colors.white)
        canvas.setFont(self.fonts.sans_bold, 19)
        canvas.drawCentredString(PAGE_WIDTH / 2, 233.5 * mm, DESIGN_CODE)

        canvas.setFont(self.fonts.serif_bold, 28)
        canvas.drawCentredString(PAGE_WIDTH / 2, 199 * mm, "HAPPY CROCHETING")
        canvas.setFont(self.fonts.serif, 13)
        canvas.drawCentredString(PAGE_WIDTH / 2, 187 * mm, "Make it slowly. Check every seam. Make it yours.")

        image_w, image_h = 61 * mm, 88 * mm
        image_x = (PAGE_WIDTH - image_w) / 2
        canvas.setFillColor(PAPER)
        canvas.roundRect(image_x - 2 * mm, 83 * mm, image_w + 4 * mm, image_h + 4 * mm, 4 * mm, stroke=0, fill=1)
        canvas.drawImage(
            str(self.hero),
            image_x,
            85 * mm,
            width=image_w,
            height=image_h,
            preserveAspectRatio=True,
            anchor="c",
            mask="auto",
        )

        canvas.setFillColor(OAT)
        canvas.setFont(self.fonts.sans_bold, 8.3)
        canvas.drawCentredString(PAGE_WIDTH / 2, 69 * mm, "SHARE YOUR FINISHED HAMISH")
        canvas.setFillColor(colors.white)
        canvas.setFont(self.fonts.sans, 8)
        canvas.drawCentredString(PAGE_WIDTH / 2, 61 * mm, "#NovalityCrochetStudio   ·   #HamishTheHighlandCow")

        canvas.setStrokeColor(MOSS)
        canvas.line(28 * mm, 43 * mm, PAGE_WIDTH - 28 * mm, 43 * mm)
        canvas.setFillColor(colors.white)
        canvas.setFont(self.fonts.sans_bold, 8.2)
        canvas.drawCentredString(PAGE_WIDTH / 2, 33 * mm, BRAND.upper())
        canvas.setFont(self.fonts.sans, 6.8)
        canvas.drawCentredString(PAGE_WIDTH / 2, 25 * mm, f"© 2026 {BRAND} · ALL RIGHTS RESERVED · {DESIGN_CODE}")
        canvas.setFillColor(OAT)
        canvas.setFont(self.fonts.sans_bold, 6.6)
        canvas.drawCentredString(PAGE_WIDTH / 2, 13 * mm, "CONFIRMATION PROOF · CONCEPT IMAGE · NOT FOR RETAIL")
        canvas.restoreState()


class PatternDocument(BaseDocTemplate):
    """Document template with stable headers, footers, bookmarks, and metadata."""

    def __init__(self, filename: Path, fonts: Fonts):
        super().__init__(
            str(filename),
            pagesize=A4,
            leftMargin=18 * mm,
            rightMargin=18 * mm,
            topMargin=22 * mm,
            bottomMargin=18 * mm,
            title=f"{DESIGN_CODE} — {TITLE} {SUBTITLE}",
            author=BRAND,
            subject=f"Crochet pattern confirmation proof, {DESIGN_CODE}",
            creator=BRAND,
        )
        self.fonts = fonts
        cover_frame = Frame(0, 0, PAGE_WIDTH, PAGE_HEIGHT, id="cover", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        content_frame = Frame(
            self.leftMargin,
            self.bottomMargin,
            self.width,
            self.height,
            id="content",
            leftPadding=0,
            rightPadding=0,
            topPadding=0,
            bottomPadding=0,
        )
        self.addPageTemplates(
            [
                PageTemplate(id="Cover", frames=[cover_frame], onPage=self.draw_cover_meta),
                PageTemplate(id="Content", frames=[content_frame], onPage=self.draw_content_page),
            ]
        )

    def draw_cover_meta(self, canvas, doc) -> None:  # noqa: ANN001
        self.set_pdf_metadata(canvas)

    def draw_content_page(self, canvas, doc) -> None:  # noqa: ANN001
        self.set_pdf_metadata(canvas)
        canvas.saveState()
        y = PAGE_HEIGHT - 13 * mm
        canvas.setStrokeColor(LINE)
        canvas.setLineWidth(0.5)
        canvas.line(18 * mm, y - 3.2 * mm, PAGE_WIDTH - 18 * mm, y - 3.2 * mm)
        canvas.setFillColor(FOREST_DARK)
        canvas.setFont(self.fonts.sans_bold, 7.2)
        canvas.drawString(18 * mm, y, BRAND.upper())
        canvas.setFillColor(GINGER)
        canvas.drawRightString(PAGE_WIDTH - 18 * mm, y, f"DESIGN CODE {DESIGN_CODE}")

        canvas.setStrokeColor(LINE)
        canvas.line(18 * mm, 12.5 * mm, PAGE_WIDTH - 18 * mm, 12.5 * mm)
        canvas.setFillColor(MUTED)
        canvas.setFont(self.fonts.sans, 6.6)
        canvas.drawString(18 * mm, 7.2 * mm, f"© 2026 {BRAND} · Confirmation proof")
        canvas.drawCentredString(PAGE_WIDTH / 2, 7.2 * mm, "DO NOT DISTRIBUTE")
        canvas.setFont(self.fonts.sans_bold, 7)
        canvas.drawRightString(PAGE_WIDTH - 18 * mm, 7.2 * mm, f"{DESIGN_CODE}   ·   {doc.page}")
        canvas.restoreState()

    @staticmethod
    def set_pdf_metadata(canvas) -> None:  # noqa: ANN001
        canvas.setTitle(f"{DESIGN_CODE} — {TITLE} {SUBTITLE}")
        canvas.setAuthor(BRAND)
        canvas.setSubject(f"Branded crochet pattern confirmation proof · {DESIGN_CODE}")
        canvas.setCreator(BRAND)
        canvas.setKeywords(f"crochet, amigurumi, Highland cow, {DESIGN_CODE}, {BRAND}")

    def afterFlowable(self, flowable: Flowable) -> None:
        if isinstance(flowable, HeadingParagraph):
            key = flowable.bookmark_key
            level = flowable.outline_level
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(flowable.plain_heading, key, level=level, closed=False)
            if level == 0:
                self.notify("TOCEntry", (level, flowable.plain_heading, self.page, key))


def image_for_width(path: Path, width: float, max_height: float) -> Image:
    with PILImage.open(path) as source:
        image_width, image_height = source.size
    ratio = min(width / image_width, max_height / image_height)
    return Image(str(path), width=image_width * ratio, height=image_height * ratio)


def table_widths(rows: Sequence[Sequence[str]], available: float) -> list[float]:
    columns = len(rows[0])
    header = [cell.lower() for cell in rows[0]]
    if columns == 4 and any("instruction" in cell for cell in header):
        return [available * 0.12, available * 0.51, available * 0.11, available * 0.26]
    if columns == 4:
        return [available * 0.25, available * 0.36, available * 0.17, available * 0.22]
    if columns == 3:
        return [available * 0.16, available * 0.65, available * 0.19]
    return [available / columns] * columns


def make_table(rows: Sequence[Sequence[str]], styles: dict[str, ParagraphStyle], available: float) -> Table:
    formatted: list[list[Paragraph]] = []
    for row_index, row in enumerate(rows):
        formatted.append(
            [
                Paragraph(
                    inline_markup(cell),
                    styles["table_header"]
                    if row_index == 0
                    else styles["table_cell_bold"]
                    if column_index == 0
                    else styles["table_cell"],
                )
                for column_index, cell in enumerate(row)
            ]
        )
    table = Table(
        formatted,
        colWidths=table_widths(rows, available),
        repeatRows=1,
        hAlign="LEFT",
        splitByRow=1,
    )
    commands: list[tuple] = [
        ("BACKGROUND", (0, 0), (-1, 0), FOREST),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.35, LINE),
        ("LEFTPADDING", (0, 0), (-1, -1), 4.5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4.5),
        ("TOPPADDING", (0, 0), (-1, -1), 4.2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4.2),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [PAPER, HexColor("#F8F3EB")]),
        ("LINEBELOW", (0, 0), (-1, 0), 1.0, FOREST_DARK),
    ]
    table.setStyle(TableStyle(commands))
    return table


def profile_story(styles: dict[str, ParagraphStyle], palette: Path) -> list[Flowable]:
    badge_data = [
        [
            Paragraph("<b>TERMINOLOGY</b><br/>US crochet terms", styles["body_compact"]),
            Paragraph("<b>SKILL LEVEL</b><br/>Intermediate", styles["body_compact"]),
            Paragraph("<b>ACTIVE TIME</b><br/>6–8 hours", styles["body_compact"]),
            Paragraph("<b>FINISHED SIZE</b><br/>About 15 cm / 6 in", styles["body_compact"]),
        ]
    ]
    badges = Table(badge_data, colWidths=[42.5 * mm] * 4)
    badges.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), PALE_GREEN),
                ("BOX", (0, 0), (-1, -1), 0.7, MOSS),
                ("INNERGRID", (0, 0), (-1, -1), 0.4, colors.white),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 9),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
            ]
        )
    )
    checkpoints = Table(
        [
            [
                Paragraph("<b>01 · ACCESS</b><br/>Lock both eye washers while the head is open.", styles["small"]),
                Paragraph("<b>02 · FIT</b><br/>Match all 18 neck stitches one-for-one.", styles["small"]),
                Paragraph("<b>03 · FINISH</b><br/>Make two complete passes on structural seams.", styles["small"]),
            ]
        ],
        colWidths=[56.7 * mm] * 3,
    )
    checkpoints.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), HexColor("#F8F3EB")),
                ("BOX", (0, 0), (-1, -1), 0.6, LINE),
                ("INNERGRID", (0, 0), (-1, -1), 0.4, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    return [
        Paragraph("Pattern profile", styles["front_title"]),
        Paragraph(
            f"<b>{DESIGN_CODE}</b> is the permanent identity of this pattern. Keep the design code with every revision, tester note, photograph and customer-support message.",
            styles["front_body"],
        ),
        Spacer(1, 3 * mm),
        badges,
        Spacer(1, 7 * mm),
        image_for_width(palette, 170 * mm, 76 * mm),
        Paragraph(
            "FIGURE 1 · The specified ginger, oat-cream, dark-chocolate and optional rust colour story. Yarn appearance varies by screen and dye lot.",
            styles["caption"],
        ),
        Paragraph("Read before making", styles["h2"]),
        Paragraph(
            "Use a stitch marker and work in a continuous spiral unless a round explicitly says otherwise. Read each component through before starting; complete eyes, embroidery and internal knots while the relevant opening remains accessible.",
            styles["front_body"],
        ),
        Paragraph(
            "<b>Safety:</b> plastic eyes and attached pieces can become small parts if a component or surrounding fabric fails. This proof does not claim toy-standard compliance. Follow the full Safety section and obtain the market-specific assessment required for any finished item supplied to another person.",
            styles["callout"],
        ),
        Paragraph(
            f"<b>Copyright notice</b><br/>© 2026 {BRAND}. All rights reserved. This pattern is licensed to one purchaser under the Terms of Use in this document. The confirmation-proof artwork is a layout placeholder and must be replaced by photographs of the physically tested sample before retail release.",
            styles["quote"],
        ),
        Spacer(1, 2 * mm),
        Paragraph("Three checkpoints to mark", styles["h3"]),
        checkpoints,
    ]


def toc_story(styles: dict[str, ParagraphStyle], fonts: Fonts) -> list[Flowable]:
    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle(
            "TOC1",
            fontName=fonts.serif_bold,
            fontSize=10,
            leading=15,
            textColor=FOREST_DARK,
            leftIndent=0,
            firstLineIndent=0,
            spaceBefore=4,
        ),
        ParagraphStyle(
            "TOC2",
            fontName=fonts.sans,
            fontSize=8.4,
            leading=12,
            textColor=INK,
            leftIndent=10,
            firstLineIndent=0,
        ),
        ParagraphStyle(
            "TOC3",
            fontName=fonts.sans,
            fontSize=7.8,
            leading=11,
            textColor=MUTED,
            leftIndent=20,
            firstLineIndent=0,
        ),
    ]
    return [
        Paragraph("Contents", styles["front_title"]),
        Paragraph(
            "Headings are bookmarked in the PDF. Table headers repeat after page breaks, and the design code appears on every page.",
            styles["front_body"],
        ),
        Spacer(1, 4 * mm),
        toc,
        Spacer(1, 8 * mm),
        HRFlowable(width="100%", thickness=0.8, color=LINE),
        Spacer(1, 5 * mm),
        Paragraph("Proof status", styles["h2"]),
        Paragraph(
            "This is the first visual-design proof. It preserves the audited written master but is not the retail release: title clearance, physical sample testing, independent tester sign-off, measured yarn/time/size, complete-item care testing and real sample photography remain open gates.",
            styles["callout"],
        ),
    ]


def blocks_to_story(
    blocks: Iterable[Block],
    styles: dict[str, ParagraphStyle],
    available_width: float,
    assembly: Path,
) -> list[Flowable]:
    story: list[Flowable] = []
    heading_count = 0
    current_h2 = ""
    inserted_assembly = False
    for block in blocks:
        if block.kind == "heading":
            text = str(block.value)
            if text == "Happy crocheting!":
                break  # Reframed as the intentional branded back cover.
            if block.level == 1:
                continue  # Represented by the editorial cover.
            if block.level == 2:
                current_h2 = text
                story.append(CondPageBreak(42 * mm))
            style_key = f"h{min(block.level, 4)}"
            level = max(0, block.level - 2)
            key = f"section-{heading_count}"
            heading_count += 1
            story.append(HeadingParagraph(inline_markup(text), styles[style_key], level, key))
            if text == "Finishing & assembly" and not inserted_assembly:
                story.extend(
                    [
                        image_for_width(assembly, available_width, 104 * mm),
                        Paragraph(
                            "FIGURE 2 · Visual sequence only. The numbered written assembly directions below control placement and seam construction.",
                            styles["caption"],
                        ),
                    ]
                )
                inserted_assembly = True
            continue
        if block.kind == "rule":
            story.extend([Spacer(1, 2 * mm), HRFlowable(width="100%", thickness=0.8, color=LINE), Spacer(1, 3 * mm)])
            continue
        if block.kind == "quote":
            story.append(Paragraph(inline_markup(str(block.value)), styles["quote"]))
            continue
        if block.kind == "table":
            story.extend([Spacer(1, 2 * mm), make_table(block.value, styles, available_width), Spacer(1, 4 * mm)])
            continue
        if block.kind == "bullet":
            story.append(Paragraph(inline_markup(str(block.value)), styles["bullet"], bulletText="•"))
            continue
        if block.kind == "ordered":
            story.append(
                Paragraph(
                    inline_markup(str(block.value)),
                    styles["number"],
                    bulletText=f"{block.level}.",
                )
            )
            continue
        if block.kind == "paragraph":
            style = styles["callout"] if current_h2.startswith("Safety") else styles["body"]
            story.append(Paragraph(inline_markup(str(block.value)), style))
    return story


def build_pdf(output: Path) -> None:
    if not SOURCE.exists():
        raise FileNotFoundError(f"Missing audited master: {SOURCE}")
    if not HERO.exists():
        raise FileNotFoundError(f"Missing concept cover asset: {HERO}")

    output.parent.mkdir(parents=True, exist_ok=True)
    palette = ASSET_DIR / "ns01_original_colourway.png"
    assembly = ASSET_DIR / "ns01_assembly_map.png"
    create_palette_asset(palette)
    create_assembly_asset(assembly)

    fonts = register_fonts()
    styles = make_styles(fonts)
    text = normalize_branding(SOURCE.read_text(encoding="utf-8"))
    blocks = parse_markdown(text)

    document = PatternDocument(output, fonts)
    story: list[Flowable] = [
        CoverFlowable(HERO, fonts),
        NextPageTemplate("Content"),
        PageBreak(),
        *profile_story(styles, palette),
        PageBreak(),
        *toc_story(styles, fonts),
        PageBreak(),
        *blocks_to_story(blocks, styles, document.width, assembly),
        NextPageTemplate("Cover"),
        PageBreak(),
        ClosingFlowable(HERO, fonts),
    ]
    document.multiBuild(story)


def postflight_pdf(output: Path) -> None:
    """Reject a proof with missing pages, identity, imagery, or critical text."""

    reader = PdfReader(output)
    if reader.is_encrypted:
        raise ValueError("The confirmation proof must not be encrypted")
    if not 10 <= len(reader.pages) <= 18:
        raise ValueError(f"Unexpected proof length: {len(reader.pages)} pages")
    if output.stat().st_size >= 20 * 1024 * 1024:
        raise ValueError("The confirmation proof exceeds Etsy's 20 MB file limit")
    if reader.metadata.title != f"{DESIGN_CODE} — {TITLE} {SUBTITLE}":
        raise ValueError("Incorrect or missing PDF title metadata")
    if reader.metadata.author != BRAND:
        raise ValueError("Incorrect or missing PDF author metadata")
    if not reader.outline:
        raise ValueError("PDF bookmarks were not generated")

    page_texts = [page.extract_text() or "" for page in reader.pages]
    for number, (page, text) in enumerate(zip(reader.pages, page_texts, strict=True), 1):
        if len(text) <= 250:
            raise ValueError(f"Page {number} is unexpectedly empty")
        if DESIGN_CODE.lower() not in text.lower():
            raise ValueError(f"Page {number} is missing the design code")
        if BRAND.lower() not in text.lower():
            raise ValueError(f"Page {number} is missing the studio brand")
        if abs(float(page.mediabox.width) - 595.28) >= 1:
            raise ValueError(f"Page {number} is not A4 width")
        if abs(float(page.mediabox.height) - 841.89) >= 1:
            raise ValueError(f"Page {number} is not A4 height")

    all_text = "\n".join(page_texts)
    if "Novality Store" in all_text:
        raise ValueError("Legacy branding remains in the proof")
    if "**" in all_text or "|---" in all_text:
        raise ValueError("Raw Markdown leaked into the proof")

    required_text = [
        "Safety — read this first",
        "Materials",
        "Gauge & size",
        "Abbreviations (US terms)",
        "Techniques used, in the order you will meet them",
        "1. Head - Yarn A",
        "2. Muzzle & nostrils - Yarn B",
        "3. Body - Yarn A",
        "4. Belly patch - Yarn B (optional)",
        "5. Legs - start with Yarn C, change to Yarn A (make 4)",
        "6. Ears - make 2 of each layer",
        "7. Horns - Yarn B (make 2)",
        "8. Tail - Yarn A",
        "9. Fringe - Yarn A",
        "10. Tartan scarf - Yarn D (optional)",
        "Finishing & assembly",
        "Troubleshooting",
        "Colorways",
        "Care",
        "Terms of Use",
        "Copyright & ownership",
        "18 head stitches of Rnd 14",
        "ladder-stitch around TWICE",
        "43 knots",
        f"© 2026 {BRAND}",
    ]
    normalized_text = all_text.lower()
    for phrase in required_text:
        if phrase.lower() not in normalized_text:
            raise ValueError(f"Required proof text is missing: {phrase!r}")

    image_hashes: set[str] = set()
    image_placements = 0
    for page in reader.pages:
        resources = page.get("/Resources")
        if isinstance(resources, IndirectObject):
            resources = resources.get_object()
        xobjects = resources.get("/XObject") if resources else None
        if isinstance(xobjects, IndirectObject):
            xobjects = xobjects.get_object()
        for image in (xobjects or {}).values():
            image = image.get_object()
            if image.get("/Subtype") == "/Image":
                image_placements += 1
                image_hashes.add(sha256(image.get_data()).hexdigest())
    if len(image_hashes) != 3:
        raise ValueError(
            f"Expected exactly 3 distinct visual assets, found {len(image_hashes)}"
        )

    print(
        "PDF postflight: PASS — "
        f"{len(reader.pages)} A4 pages, "
        f"{output.stat().st_size / 1024 / 1024:.2f} MiB, "
        f"3 distinct images ({image_placements} placements), selectable text, "
        "metadata, bookmarks, brand, code, copyright, and critical instructions"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output = args.output.resolve()
    build_pdf(output)
    postflight_pdf(output)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
