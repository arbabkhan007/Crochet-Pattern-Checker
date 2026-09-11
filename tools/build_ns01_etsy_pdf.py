#!/usr/bin/env python3
"""Build the branded NS 01 Etsy-edition PDF from its audited Markdown master.

The layout treats the supplied visuals as illustrations, never as physical test evidence.
Product testing, image disclosure, and listing compliance remain owner responsibilities.
"""

from __future__ import annotations

import argparse
import re
import tempfile
from dataclasses import dataclass
from hashlib import sha256
from html import escape, unescape
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
from pypdf.generic import ContentStream, IndirectObject


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "patterns/01_Hamish_the_Highland_Cow.md"
HERO = ROOT / "assets/patterns/ns01/hamish_cover_concept.png"
MATERIALS_IMAGE = ROOT / "assets/patterns/ns01/hamish_materials_concept.png"
DEFAULT_OUTPUT = ROOT / "release/NS01_Hamish_the_Highland_Cow_Crochet_Pattern.pdf"
DEFAULT_PRINTER_OUTPUT = ROOT / "release/NS01_Hamish_the_Highland_Cow_PRINTER_SAVER.pdf"
ASSET_DIR = Path(tempfile.gettempdir()) / "novality-pdf-assets/ns01"

PAGE_WIDTH, PAGE_HEIGHT = A4
BRAND = "Novality Crochet Studio"
DESIGN_CODE = "NS 01"
TITLE = "Hamish"
SUBTITLE = "the Highland Cow"
REVISION = "First edition · 2026"

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
    """Apply the owner-requested customer-facing studio brand and spelling."""

    return (
        text.replace("Novality Store", BRAND)
        .replace("#NovalityStore", "#NovalityCrochetStudio")
        .replace("## Colorways", "## Colourways")
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


def make_printer_styles(fonts: Fonts) -> dict[str, ParagraphStyle]:
    """Return ink-light black-on-white variants of the customer styles."""

    styles = make_styles(fonts)
    for style in styles.values():
        style.textColor = colors.black
    for key in ("quote", "callout"):
        styles[key].backColor = colors.white
        styles[key].borderColor = HexColor("#666666")
        styles[key].borderWidth = 0.6
    styles["table_header"].textColor = colors.black
    styles["caption"].textColor = HexColor("#444444")
    return styles


class HeadingParagraph(Paragraph):
    """Paragraph carrying outline and table-of-contents metadata."""

    def __init__(self, text: str, style: ParagraphStyle, level: int, key: str):
        super().__init__(text, style)
        self.outline_level = level
        self.bookmark_key = key
        self.plain_heading = unescape(re.sub(r"<[^>]+>", "", text))


class CoverFlowable(Flowable):
    """Full-page editorial cover for the customer PDF."""

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
        canvas.drawRightString(PAGE_WIDTH - 14 * mm, 34.5 * mm, "DIGITAL CROCHET PATTERN")
        canvas.setFont(self.fonts.sans, 6.3)
        canvas.drawString(
            14 * mm,
            27 * mm,
            "ILLUSTRATIVE COVER ART · ORIGINAL GINGER COLOURWAY · WRITTEN INSTRUCTIONS CONTROL",
        )
        canvas.setFillColor(FOREST_DARK)
        canvas.rect(0, 0, PAGE_WIDTH, 14 * mm, stroke=0, fill=1)
        canvas.setFillColor(colors.white)
        canvas.setFont(self.fonts.sans_bold, 7.2)
        canvas.drawCentredString(PAGE_WIDTH / 2, 5.1 * mm, "NOVALITY CROCHET STUDIO  ·  ORIGINAL PATTERN")
        canvas.restoreState()


class PrinterCoverFlowable(Flowable):
    """Black-on-white cover for the companion printer-saver edition."""

    def __init__(self, fonts: Fonts):
        super().__init__()
        self.fonts = fonts
        self.width = PAGE_WIDTH
        self.height = PAGE_HEIGHT - 0.2 * mm

    def wrap(self, available_width, available_height):  # noqa: ANN001
        return self.width, min(self.height, available_height)

    def draw(self) -> None:
        canvas = self.canv
        canvas.saveState()
        canvas.setFillColor(colors.white)
        canvas.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, stroke=0, fill=1)
        canvas.setStrokeColor(colors.black)
        canvas.setLineWidth(0.8)
        canvas.rect(14 * mm, 14 * mm, PAGE_WIDTH - 28 * mm, PAGE_HEIGHT - 28 * mm, stroke=1, fill=0)

        canvas.setFillColor(colors.black)
        canvas.setFont(self.fonts.sans_bold, 9)
        canvas.drawString(20 * mm, PAGE_HEIGHT - 25 * mm, BRAND.upper())
        canvas.setFont(self.fonts.sans, 8)
        canvas.drawRightString(PAGE_WIDTH - 20 * mm, PAGE_HEIGHT - 25 * mm, "PRINTER-SAVER EDITION")
        canvas.line(20 * mm, PAGE_HEIGHT - 31 * mm, PAGE_WIDTH - 20 * mm, PAGE_HEIGHT - 31 * mm)

        canvas.setFont(self.fonts.sans_bold, 12)
        canvas.drawString(20 * mm, 235 * mm, f"DESIGN CODE {DESIGN_CODE}")
        canvas.setFont(self.fonts.serif_bold, 34)
        canvas.drawString(20 * mm, 211 * mm, TITLE.upper())
        canvas.setFont(self.fonts.serif, 20)
        canvas.drawString(20 * mm, 198 * mm, SUBTITLE)
        canvas.setLineWidth(1.2)
        canvas.line(20 * mm, 188 * mm, 92 * mm, 188 * mm)

        canvas.setFont(self.fonts.sans_bold, 10)
        canvas.drawString(20 * mm, 172 * mm, "BLACK + WHITE · WHITE BACKGROUNDS · PROGRESS BOXES")
        canvas.setFont(self.fonts.sans, 9)
        canvas.drawString(20 * mm, 160 * mm, "US terms · Intermediate · 6–8 hours · About 15 cm / 6 in")
        canvas.drawString(20 * mm, 151 * mm, "Worsted / aran yarn · 3.5 mm hook")

        canvas.setLineWidth(0.5)
        canvas.rect(20 * mm, 112 * mm, PAGE_WIDTH - 40 * mm, 26 * mm, stroke=1, fill=0)
        canvas.setFont(self.fonts.sans_bold, 8.5)
        canvas.drawString(25 * mm, 130 * mm, "NAMED ORIGINAL COLOURWAY")
        canvas.setFont(self.fonts.sans, 8.5)
        canvas.drawString(
            25 * mm,
            120 * mm,
            "Yarn A Ginger · Yarn B Oat Cream · Yarn C Dark Chocolate · Yarn D Rust / Tartan",
        )

        canvas.setFont(self.fonts.sans_bold, 8.5)
        canvas.drawString(20 * mm, 91 * mm, "ABOUT THIS COMPANION FILE")
        canvas.setFont(self.fonts.sans, 8.2)
        canvas.drawString(20 * mm, 81 * mm, "Designed for economical home printing and handwritten progress tracking.")
        canvas.drawString(20 * mm, 73 * mm, "Large raster artwork is omitted. Use the full-colour edition for the materials")
        canvas.drawString(20 * mm, 66 * mm, "visual and assembly illustration; the written instructions in both files are the same.")

        canvas.line(20 * mm, 47 * mm, PAGE_WIDTH - 20 * mm, 47 * mm)
        canvas.setFont(self.fonts.sans, 7)
        canvas.drawString(20 * mm, 37 * mm, f"© 2026 {BRAND} · All rights reserved")
        canvas.drawRightString(PAGE_WIDTH - 20 * mm, 37 * mm, "PERSONAL LICENSE · SEE TERMS")
        canvas.setFont(self.fonts.sans_bold, 7)
        canvas.drawCentredString(PAGE_WIDTH / 2, 24 * mm, f"{DESIGN_CODE} · PRINTER-SAVER CROCHET PATTERN")
        canvas.restoreState()


class ClosingPanel(Flowable):
    """Light closing page that matches the interior rather than a colour flood."""

    def __init__(self, width: float, fonts: Fonts):
        super().__init__()
        self.fonts = fonts
        self.width = width
        self.height = 172 * mm

    def wrap(self, available_width, available_height):  # noqa: ANN001
        return min(self.width, available_width), min(self.height, available_height)

    def draw(self) -> None:
        canvas = self.canv
        canvas.saveState()
        canvas.setFillColor(PALE_GREEN)
        canvas.setStrokeColor(MOSS)
        canvas.setLineWidth(0.8)
        canvas.roundRect(0, 19 * mm, self.width, 144 * mm, 5 * mm, stroke=1, fill=1)

        center = self.width / 2
        canvas.setFillColor(GINGER)
        canvas.circle(center, 139 * mm, 14 * mm, stroke=0, fill=1)
        canvas.setFillColor(colors.white)
        canvas.setFont(self.fonts.sans_bold, 12)
        canvas.drawCentredString(center, 136.4 * mm, DESIGN_CODE)

        canvas.setFillColor(FOREST_DARK)
        canvas.setFont(self.fonts.serif_bold, 25)
        canvas.drawCentredString(center, 111 * mm, "HAPPY CROCHETING")
        canvas.setFont(self.fonts.serif, 12)
        canvas.drawCentredString(center, 99 * mm, "Make it slowly. Check every seam. Make it yours.")

        canvas.setStrokeColor(GINGER_LIGHT)
        canvas.setLineWidth(1.2)
        canvas.line(36 * mm, 88 * mm, self.width - 36 * mm, 88 * mm)
        canvas.setFillColor(INK)
        canvas.setFont(self.fonts.sans_bold, 8.2)
        canvas.drawCentredString(center, 76 * mm, "SHARE YOUR FINISHED HAMISH")
        canvas.setFont(self.fonts.sans, 8)
        canvas.drawCentredString(center, 67 * mm, "#NovalityCrochetStudio   ·   #HamishTheHighlandCow")

        canvas.setFont(self.fonts.sans, 7.4)
        canvas.setFillColor(MUTED)
        canvas.drawCentredString(center, 50 * mm, "Keep this design code with support questions and pattern revisions.")
        canvas.setFont(self.fonts.sans_bold, 8)
        canvas.setFillColor(FOREST_DARK)
        canvas.drawCentredString(center, 39 * mm, BRAND.upper())
        canvas.setFont(self.fonts.sans, 7)
        canvas.drawCentredString(center, 29 * mm, f"© 2026 {BRAND} · ALL RIGHTS RESERVED · {DESIGN_CODE}")
        canvas.restoreState()


class PrinterNotesPanel(Flowable):
    """Low-ink completion checklist and ruled notes area."""

    def __init__(self, width: float, fonts: Fonts):
        super().__init__()
        self.fonts = fonts
        self.width = width
        self.height = 228 * mm

    def wrap(self, available_width, available_height):  # noqa: ANN001
        return min(self.width, available_width), min(self.height, available_height)

    def draw(self) -> None:
        canvas = self.canv
        canvas.saveState()
        canvas.setFillColor(colors.black)
        canvas.setFont(self.fonts.serif_bold, 22)
        canvas.drawString(0, 211 * mm, "Finish checklist & notes")
        canvas.setFont(self.fonts.sans, 8.5)
        checks = [
            "[ ] Round counts checked before every decrease",
            "[ ] Both eye washers locked before Head Rnd 16",
            "[ ] Inner and outer ears joined stitch-for-stitch",
            "[ ] Leg option and mirrored angles checked while pinned",
            "[ ] All structural seams completed twice",
            "[ ] All yarn ends, fringe knots and attachments inspected",
        ]
        y = 196 * mm
        for check in checks:
            canvas.drawString(2 * mm, y, check)
            y -= 9 * mm

        canvas.setFont(self.fonts.sans_bold, 9)
        canvas.drawString(0, 132 * mm, "PROJECT NOTES")
        canvas.setStrokeColor(HexColor("#777777"))
        canvas.setLineWidth(0.45)
        for index in range(12):
            line_y = (122 - index * 9) * mm
            canvas.line(0, line_y, self.width, line_y)

        canvas.setFont(self.fonts.sans, 7)
        canvas.setFillColor(colors.black)
        canvas.drawString(0, 7 * mm, f"{BRAND} · {DESIGN_CODE} · printer-saver companion")
        canvas.drawRightString(self.width, 7 * mm, "Keep this page with your project notes")
        canvas.restoreState()


class PatternDocument(BaseDocTemplate):
    """Document template with stable headers, footers, bookmarks, and metadata."""

    def __init__(
        self,
        filename: Path,
        fonts: Fonts,
        *,
        printer_saver: bool = False,
    ):
        edition = "printer-saver crochet pattern" if printer_saver else "crochet pattern"
        super().__init__(
            str(filename),
            pagesize=A4,
            leftMargin=18 * mm,
            rightMargin=18 * mm,
            topMargin=22 * mm,
            bottomMargin=18 * mm,
            title=f"{DESIGN_CODE} — {TITLE} {SUBTITLE}",
            author=BRAND,
            subject=f"{edition.capitalize()}, {DESIGN_CODE}",
            creator=BRAND,
        )
        self.fonts = fonts
        self.printer_saver = printer_saver
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
        line_colour = HexColor("#777777") if self.printer_saver else LINE
        primary = colors.black if self.printer_saver else FOREST_DARK
        accent = colors.black if self.printer_saver else GINGER
        canvas.setStrokeColor(line_colour)
        canvas.setLineWidth(0.5)
        canvas.line(18 * mm, y - 3.2 * mm, PAGE_WIDTH - 18 * mm, y - 3.2 * mm)
        canvas.setFillColor(primary)
        canvas.setFont(self.fonts.sans_bold, 7.2)
        canvas.drawString(18 * mm, y, BRAND.upper())
        canvas.setFillColor(accent)
        edition = " · PRINTER SAVER" if self.printer_saver else ""
        canvas.drawRightString(
            PAGE_WIDTH - 18 * mm,
            y,
            f"DESIGN CODE {DESIGN_CODE}{edition}",
        )

        canvas.setStrokeColor(line_colour)
        canvas.line(18 * mm, 12.5 * mm, PAGE_WIDTH - 18 * mm, 12.5 * mm)
        canvas.setFillColor(HexColor("#444444") if self.printer_saver else MUTED)
        canvas.setFont(self.fonts.sans, 6.6)
        canvas.drawString(18 * mm, 7.2 * mm, f"© 2026 {BRAND} · All rights reserved")
        canvas.drawCentredString(PAGE_WIDTH / 2, 7.2 * mm, "PERSONAL LICENSE · SEE TERMS")
        canvas.setFont(self.fonts.sans_bold, 7)
        canvas.drawRightString(PAGE_WIDTH - 18 * mm, 7.2 * mm, f"{DESIGN_CODE}   ·   {doc.page}")
        canvas.restoreState()

    def set_pdf_metadata(self, canvas) -> None:  # noqa: ANN001
        canvas.setTitle(f"{DESIGN_CODE} — {TITLE} {SUBTITLE}")
        canvas.setAuthor(BRAND)
        subject = "Printer-saver crochet pattern" if self.printer_saver else "Branded crochet pattern"
        canvas.setSubject(f"{subject} · {DESIGN_CODE}")
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
        return [available * 0.14, available * 0.49, available * 0.11, available * 0.26]
    if columns == 4:
        return [available * 0.25, available * 0.36, available * 0.17, available * 0.22]
    if columns == 3:
        return [available * 0.18, available * 0.63, available * 0.19]
    return [available / columns] * columns


def make_table(
    rows: Sequence[Sequence[str]],
    styles: dict[str, ParagraphStyle],
    available: float,
    *,
    printer_saver: bool = False,
) -> Table:
    formatted: list[list[Paragraph]] = []
    progress_table = rows[0][0].strip().lower() == "rnd"
    for row_index, row in enumerate(rows):
        formatted_row: list[Paragraph] = []
        for column_index, cell in enumerate(row):
            display = cell
            if progress_table and row_index > 0 and column_index == 0:
                display = f"[ ] {cell}"
            style = (
                styles["table_header"]
                if row_index == 0
                else styles["table_cell_bold"]
                if column_index == 0
                else styles["table_cell"]
            )
            formatted_row.append(Paragraph(inline_markup(display), style))
        formatted.append(formatted_row)
    table = Table(
        formatted,
        colWidths=table_widths(rows, available),
        repeatRows=1,
        hAlign="LEFT",
        splitByRow=1,
    )
    header_fill = colors.white if printer_saver else FOREST
    header_text = colors.black if printer_saver else colors.white
    grid_colour = HexColor("#777777") if printer_saver else LINE
    row_fills = [colors.white] if printer_saver else [PAPER, HexColor("#F8F3EB")]
    commands: list[tuple] = [
        ("BACKGROUND", (0, 0), (-1, 0), header_fill),
        ("TEXTCOLOR", (0, 0), (-1, 0), header_text),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.35, grid_colour),
        ("LEFTPADDING", (0, 0), (-1, -1), 4.5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4.5),
        ("TOPPADDING", (0, 0), (-1, -1), 4.2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4.2),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), row_fills),
        ("LINEBELOW", (0, 0), (-1, 0), 1.0, colors.black if printer_saver else FOREST_DARK),
    ]
    table.setStyle(TableStyle(commands))
    return table


def colour_swatch_table(
    styles: dict[str, ParagraphStyle],
    available_width: float,
    *,
    printer_saver: bool = False,
) -> Table:
    """Render named original colours as native PDF vectors and selectable text."""

    labels = [
        ("YARN A", "GINGER", "body + fringe · about 25 g", GINGER),
        ("YARN B", "OAT CREAM", "muzzle + horns + inner ears · 12 g", OAT),
        ("YARN C", "DARK CHOCOLATE", "hooves + nostrils · about 5 g", CHOCOLATE),
        ("YARN D", "RUST / TARTAN", "optional scarf · about 6 g", RUST),
    ]
    width = available_width / len(labels)
    text_cells = [
        Paragraph(f"<b>{code} · {name}</b><br/>{use}", styles["small"])
        for code, name, use, _colour in labels
    ]
    if printer_saver:
        table = Table([text_cells], colWidths=[width] * len(labels))
        table.setStyle(
            TableStyle(
                [
                    ("BOX", (0, 0), (-1, -1), 0.7, HexColor("#777777")),
                    ("INNERGRID", (0, 0), (-1, -1), 0.45, HexColor("#777777")),
                    ("BACKGROUND", (0, 0), (-1, -1), colors.white),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 7),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                    ("TOPPADDING", (0, 0), (-1, -1), 7),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ]
            )
        )
        return table

    table = Table(
        [["" for _ in labels], text_cells],
        colWidths=[width] * len(labels),
        rowHeights=[13 * mm, None],
    )
    commands: list[tuple] = [
        ("BOX", (0, 0), (-1, -1), 0.7, LINE),
        ("INNERGRID", (0, 0), (-1, -1), 0.45, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 1), (-1, -1), 7),
        ("RIGHTPADDING", (0, 1), (-1, -1), 7),
        ("TOPPADDING", (0, 1), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 7),
        ("BACKGROUND", (0, 1), (-1, 1), HexColor("#FAF6EF")),
    ]
    for index, (_code, _name, _use, colour) in enumerate(labels):
        commands.append(("BACKGROUND", (index, 0), (index, 0), colour))
    table.setStyle(TableStyle(commands))
    return table


def profile_story(
    styles: dict[str, ParagraphStyle], materials_image: Path, available_width: float
) -> list[Flowable]:
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
    materials = image_for_width(materials_image, 160 * mm, 68 * mm)
    materials.hAlign = "CENTER"
    return [
        Paragraph("Pattern profile", styles["front_title"]),
        Paragraph(
            f"<b>{DESIGN_CODE}</b> is the permanent identity of this pattern. Keep the design code with every revision, tester note, photograph and customer-support message.",
            styles["front_body"],
        ),
        Spacer(1, 3 * mm),
        badges,
        Spacer(1, 5 * mm),
        Paragraph("Original colourway", styles["h3"]),
        colour_swatch_table(styles, available_width),
        Paragraph(
            "COLOUR GUIDE · Ginger, oat cream, dark chocolate and optional rust/tartan are the named original colours. Screen appearance and dye lots vary.",
            styles["caption"],
        ),
        materials,
        Paragraph(
            "FIGURE 1 · Materials visual: ginger, oat-cream and dark-chocolate yarn; rust tartan; 3.5 mm hook; two eyes with washers; fibre fill; needle, pins, scissors and marker. Follow the written quantities below.",
            styles["caption"],
        ),
        Paragraph("Read before making", styles["h2"]),
        Paragraph(
            "Use a stitch marker and work in a continuous spiral unless a round explicitly says otherwise. Read each component through before starting; complete eyes, embroidery and internal knots while the relevant opening remains accessible.",
            styles["front_body"],
        ),
        Paragraph(
            "<b>Safety:</b> plastic eyes and attached pieces can become small parts if a component or surrounding fabric fails. This pattern does not claim toy-standard compliance. Follow the full Safety section and obtain the market-specific assessment required for any finished item supplied to another person.",
            styles["callout"],
        ),
        Paragraph(
            f"<b>Copyright notice</b><br/>© 2026 {BRAND}. All rights reserved. Licensed to the purchaser under the Terms of Use in this document. Cover and materials visuals are illustrative; the written materials, counts and construction directions control.",
            styles["quote"],
        ),
    ]


def printer_profile_story(
    styles: dict[str, ParagraphStyle], available_width: float
) -> list[Flowable]:
    """Create a low-ink profile page without raster artwork or colour fills."""

    facts = Table(
        [
            [
                Paragraph("<b>TERMINOLOGY</b><br/>US crochet terms", styles["body_compact"]),
                Paragraph("<b>SKILL LEVEL</b><br/>Intermediate", styles["body_compact"]),
                Paragraph("<b>ACTIVE TIME</b><br/>6–8 hours", styles["body_compact"]),
                Paragraph("<b>FINISHED SIZE</b><br/>About 15 cm / 6 in", styles["body_compact"]),
            ]
        ],
        colWidths=[42.5 * mm] * 4,
    )
    facts.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.white),
                ("BOX", (0, 0), (-1, -1), 0.7, HexColor("#777777")),
                ("INNERGRID", (0, 0), (-1, -1), 0.4, HexColor("#777777")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 9),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
            ]
        )
    )
    return [
        Paragraph("Pattern profile", styles["front_title"]),
        Paragraph(
            f"<b>{DESIGN_CODE}</b> is the permanent identity of this pattern. This companion edition removes large artwork and colour backgrounds to reduce home-printer ink use.",
            styles["front_body"],
        ),
        Spacer(1, 3 * mm),
        facts,
        Spacer(1, 5 * mm),
        Paragraph("Named original colourway", styles["h3"]),
        colour_swatch_table(styles, available_width, printer_saver=True),
        Paragraph(
            "The names above—not a screen or print colour—control yarn selection. See the full-colour companion for visual swatches and illustrative materials.",
            styles["caption"],
        ),
        Paragraph("Progress tracking", styles["h2"]),
        Paragraph(
            "Every construction-table row begins with a printable [ ] box. Tick it by hand or with a PDF annotation tool only after completing the round and confirming the stitch count.",
            styles["front_body"],
        ),
        Paragraph("Read before making", styles["h2"]),
        Paragraph(
            "Use a stitch marker and work in a continuous spiral unless a round explicitly says otherwise. Read each component through before starting; complete eyes, embroidery and internal knots while the relevant opening remains accessible.",
            styles["front_body"],
        ),
        Paragraph(
            "<b>Safety:</b> plastic eyes and attached pieces can become small parts if a component or surrounding fabric fails. This pattern does not claim toy-standard compliance. Follow the full Safety section and obtain the market-specific assessment required for any finished item supplied to another person.",
            styles["callout"],
        ),
        Paragraph(
            f"<b>Copyright notice</b><br/>© 2026 {BRAND}. All rights reserved. Licensed to the purchaser under the Terms of Use in this document. The written materials, counts and construction directions control.",
            styles["quote"],
        ),
    ]


def toc_story(
    styles: dict[str, ParagraphStyle],
    fonts: Fonts,
    *,
    printer_saver: bool = False,
) -> list[Flowable]:
    toc = TableOfContents()
    primary = colors.black if printer_saver else FOREST_DARK
    secondary = colors.black if printer_saver else INK
    muted = HexColor("#444444") if printer_saver else MUTED
    toc.levelStyles = [
        ParagraphStyle(
            "TOC1",
            fontName=fonts.serif_bold,
            fontSize=10,
            leading=15,
            textColor=primary,
            leftIndent=0,
            firstLineIndent=0,
            spaceBefore=4,
        ),
        ParagraphStyle(
            "TOC2",
            fontName=fonts.sans,
            fontSize=8.4,
            leading=12,
            textColor=secondary,
            leftIndent=10,
            firstLineIndent=0,
        ),
        ParagraphStyle(
            "TOC3",
            fontName=fonts.sans,
            fontSize=7.8,
            leading=11,
            textColor=muted,
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
        HRFlowable(
            width="100%",
            thickness=0.8,
            color=HexColor("#777777") if printer_saver else LINE,
        ),
        Spacer(1, 5 * mm),
        Paragraph("How to use this pattern", styles["h2"]),
        Paragraph(
            "Read each component and its finishing note before beginning. Mark completed rows as you work, use the stitch count at the end of every round, and stop if your count differs. Diagrams support orientation only; the numbered written directions control construction.",
            styles["callout"],
        ),
        Paragraph(
            "Three checkpoints: lock both eye washers while the head is open; match all 18 neck stitches one-for-one; and make two complete passes on structural seams.",
            styles["front_body"],
        ),
    ]


def blocks_to_story(
    blocks: Iterable[Block],
    styles: dict[str, ParagraphStyle],
    available_width: float,
    assembly: Path | None,
    *,
    printer_saver: bool = False,
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
            if text == "Finishing & assembly" and assembly is not None and not inserted_assembly:
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
            if text == "Colourways":
                story.extend(
                    [
                        colour_swatch_table(
                            styles,
                            available_width,
                            printer_saver=printer_saver,
                        ),
                        Paragraph(
                            "ORIGINAL COLOURWAY · Yarn A Ginger · Yarn B Oat Cream · Yarn C Dark Chocolate · Yarn D Rust / Tartan (optional).",
                            styles["caption"],
                        ),
                    ]
                )
            continue
        if block.kind == "rule":
            rule_colour = HexColor("#777777") if printer_saver else LINE
            story.extend(
                [
                    Spacer(1, 2 * mm),
                    HRFlowable(width="100%", thickness=0.8, color=rule_colour),
                    Spacer(1, 3 * mm),
                ]
            )
            continue
        if block.kind == "quote":
            story.append(Paragraph(inline_markup(str(block.value)), styles["quote"]))
            continue
        if block.kind == "table":
            story.extend(
                [
                    Spacer(1, 2 * mm),
                    make_table(
                        block.value,
                        styles,
                        available_width,
                        printer_saver=printer_saver,
                    ),
                    Spacer(1, 4 * mm),
                ]
            )
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
            value = str(block.value)
            if current_h2 == "Colourways":
                value = f"<b>Optional body-tone variations:</b> {escape(value)}"
                story.append(Paragraph(value, style))
            else:
                story.append(Paragraph(inline_markup(value), style))
    return story


def build_pdf(output: Path) -> None:
    if not SOURCE.exists():
        raise FileNotFoundError(f"Missing audited master: {SOURCE}")
    if not HERO.exists():
        raise FileNotFoundError(f"Missing illustrative cover asset: {HERO}")
    if not MATERIALS_IMAGE.exists():
        raise FileNotFoundError(f"Missing illustrative materials asset: {MATERIALS_IMAGE}")

    output.parent.mkdir(parents=True, exist_ok=True)
    assembly = ASSET_DIR / "ns01_assembly_map.png"
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
        *profile_story(styles, MATERIALS_IMAGE, document.width),
        PageBreak(),
        *toc_story(styles, fonts),
        PageBreak(),
        *blocks_to_story(blocks, styles, document.width, assembly),
        PageBreak(),
        ClosingPanel(document.width, fonts),
    ]
    document.multiBuild(story)


def build_printer_pdf(output: Path) -> None:
    """Build the black-on-white companion without any raster image objects."""

    if not SOURCE.exists():
        raise FileNotFoundError(f"Missing audited master: {SOURCE}")
    output.parent.mkdir(parents=True, exist_ok=True)

    fonts = register_fonts()
    styles = make_printer_styles(fonts)
    text = normalize_branding(SOURCE.read_text(encoding="utf-8"))
    blocks = parse_markdown(text)

    document = PatternDocument(output, fonts, printer_saver=True)
    story: list[Flowable] = [
        PrinterCoverFlowable(fonts),
        NextPageTemplate("Content"),
        PageBreak(),
        *printer_profile_story(styles, document.width),
        PageBreak(),
        *toc_story(styles, fonts, printer_saver=True),
        PageBreak(),
        *blocks_to_story(
            blocks,
            styles,
            document.width,
            None,
            printer_saver=True,
        ),
        PageBreak(),
        PrinterNotesPanel(document.width, fonts),
    ]
    document.multiBuild(story)


def image_inventory(reader: PdfReader) -> tuple[set[str], int]:
    """Return distinct decoded raster hashes and total page placements."""

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
    return image_hashes, image_placements


def postflight_pdf(output: Path) -> None:
    """Reject an Etsy PDF with missing pages, identity, imagery, or critical text."""

    reader = PdfReader(output)
    if reader.is_encrypted:
        raise ValueError("The customer PDF must not be encrypted")
    if not 10 <= len(reader.pages) <= 18:
        raise ValueError(f"Unexpected PDF length: {len(reader.pages)} pages")
    if output.stat().st_size >= 20 * 1024 * 1024:
        raise ValueError("The customer PDF exceeds Etsy's 20 MB file limit")
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
        raise ValueError("Legacy branding remains in the customer PDF")
    if "**" in all_text or "|---" in all_text:
        raise ValueError("Raw Markdown leaked into the customer PDF")
    for proof_marker in ("confirmation proof", "not for retail", "do not distribute"):
        if proof_marker in all_text.lower():
            raise ValueError(f"Proof-only marker remains: {proof_marker!r}")

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
        "Standard 16-round legs",
        "Shortened front legs - upright option only (make 2)",
        "Start each leg 25 degrees forward from vertical",
        "6. Ears - make 2 of each layer",
        "7. Horns - Yarn B (make 2)",
        "8. Tail - Yarn A",
        "9. Fringe - Yarn A",
        "10. Tartan scarf - Yarn D (optional)",
        "Finishing & assembly",
        "Troubleshooting",
        "Colourways",
        "YARN A · GINGER",
        "YARN B · OAT CREAM",
        "YARN C · DARK CHOCOLATE",
        "YARN D · RUST / TARTAN",
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
            raise ValueError(f"Required customer text is missing: {phrase!r}")

    head_rnd_11 = r"\[\s*\]\s*R11\s+\[5 sc, dec\] x 6\s+\(36\)"
    if not re.search(head_rnd_11, all_text):
        raise ValueError("Head Rnd 11 is missing its 42-to-36 decrease instruction")
    body_rnd_11 = r"\[\s*\]\s*R11\s+sc in each st around\s+\(48\)"
    if not re.search(body_rnd_11, all_text):
        raise ValueError("Body Rnd 11 is missing its straight-round instruction")
    if all_text.count("[ ]") < 90:
        raise ValueError("Too few construction-table progress checkboxes were rendered")

    image_hashes, image_placements = image_inventory(reader)
    if len(image_hashes) != 3:
        raise ValueError(
            f"Expected exactly 3 distinct visual assets, found {len(image_hashes)}"
        )

    print(
        "PDF postflight: PASS — "
        f"{len(reader.pages)} A4 pages, "
        f"{output.stat().st_size / 1024 / 1024:.2f} MiB, "
        f"3 distinct images ({image_placements} placements), "
        f"{all_text.count('[ ]')} progress boxes, selectable text, metadata, "
        "bookmarks, brand, code, copyright, and critical instructions"
    )


def postflight_printer_pdf(output: Path) -> None:
    """Reject a printer-saver companion that uses images or loses core content."""

    reader = PdfReader(output)
    if reader.is_encrypted:
        raise ValueError("The printer-saver PDF must not be encrypted")
    if not 10 <= len(reader.pages) <= 20:
        raise ValueError(f"Unexpected printer-saver length: {len(reader.pages)} pages")
    if output.stat().st_size >= 5 * 1024 * 1024:
        raise ValueError("The printer-saver PDF is unexpectedly large")
    if reader.metadata.title != f"{DESIGN_CODE} — {TITLE} {SUBTITLE}":
        raise ValueError("Incorrect printer-saver title metadata")
    if reader.metadata.author != BRAND:
        raise ValueError("Incorrect printer-saver author metadata")
    if "printer-saver" not in (reader.metadata.subject or "").lower():
        raise ValueError("Printer-saver metadata is missing its edition label")
    if not reader.outline:
        raise ValueError("Printer-saver bookmarks were not generated")

    page_texts = [page.extract_text() or "" for page in reader.pages]
    for number, (page, text) in enumerate(zip(reader.pages, page_texts, strict=True), 1):
        if len(text) <= 250:
            raise ValueError(f"Printer-saver page {number} is unexpectedly empty")
        if DESIGN_CODE.lower() not in text.lower():
            raise ValueError(f"Printer-saver page {number} is missing the design code")
        if BRAND.lower() not in text.lower():
            raise ValueError(f"Printer-saver page {number} is missing the studio brand")
        if abs(float(page.mediabox.width) - 595.28) >= 1:
            raise ValueError(f"Printer-saver page {number} is not A4 width")
        if abs(float(page.mediabox.height) - 841.89) >= 1:
            raise ValueError(f"Printer-saver page {number} is not A4 height")
        content = ContentStream(page.get_contents(), reader)
        for operands, operator in content.operations:
            if operator in (b"rg", b"RG"):
                channels = [float(value) for value in operands]
                if max(channels) - min(channels) > 0.0001:
                    raise ValueError(
                        f"Printer-saver page {number} contains non-grayscale vector colour"
                    )
            if operator in (b"k", b"K"):
                cyan, magenta, yellow, _black = [float(value) for value in operands]
                if max(cyan, magenta, yellow) > 0.0001:
                    raise ValueError(
                        f"Printer-saver page {number} contains chromatic CMYK colour"
                    )

    all_text = "\n".join(page_texts)
    normalized_text = all_text.lower()
    required_text = [
        "PRINTER-SAVER EDITION",
        "Every construction-table row begins with a printable [ ] box",
        "Safety — read this first",
        "Materials",
        "1. Head - Yarn A",
        "[ ] R11",
        "[5 sc, dec] x 6",
        "3. Body - Yarn A",
        "Shortened front legs - upright option only (make 2)",
        "Start each leg 25 degrees forward from vertical",
        "INNER ear - Yarn B (make 2) & OUTER ear - Yarn A (make 2)",
        "Finishing & assembly",
        "Colourways",
        "YARN A · GINGER",
        "YARN B · OAT CREAM",
        "YARN C · DARK CHOCOLATE",
        "YARN D · RUST / TARTAN",
        "Terms of Use",
        f"© 2026 {BRAND}",
    ]
    for phrase in required_text:
        if phrase.lower() not in normalized_text:
            raise ValueError(f"Required printer-saver text is missing: {phrase!r}")
    if all_text.count("[ ]") < 75:
        raise ValueError("Too few progress checkboxes were rendered")
    head_rnd_11 = r"\[\s*\]\s*R11\s+\[5 sc, dec\] x 6\s+\(36\)"
    if not re.search(head_rnd_11, all_text):
        raise ValueError("Printer-saver Head Rnd 11 instruction is missing")
    body_rnd_11 = r"\[\s*\]\s*R11\s+sc in each st around\s+\(48\)"
    if not re.search(body_rnd_11, all_text):
        raise ValueError("Printer-saver Body Rnd 11 instruction is missing")

    image_hashes, image_placements = image_inventory(reader)
    if image_hashes or image_placements:
        raise ValueError("Printer-saver PDF must not contain raster images")

    print(
        "Printer-saver postflight: PASS — "
        f"{len(reader.pages)} A4 pages, "
        f"{output.stat().st_size / 1024 / 1024:.2f} MiB, "
        f"{all_text.count('[ ]')} progress boxes, no raster images, grayscale vectors, "
        "selectable text, metadata, bookmarks, brand, code, copyright, and critical instructions"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--printer-output",
        type=Path,
        default=DEFAULT_PRINTER_OUTPUT,
        help="Path for the black-on-white printer-saver companion",
    )
    parser.add_argument(
        "--skip-printer-saver",
        action="store_true",
        help="Build only the full-colour customer edition",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output = args.output.resolve()
    build_pdf(output)
    postflight_pdf(output)
    print(output)
    if not args.skip_printer_saver:
        printer_output = args.printer_output.resolve()
        build_printer_pdf(printer_output)
        postflight_printer_pdf(printer_output)
        print(printer_output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
