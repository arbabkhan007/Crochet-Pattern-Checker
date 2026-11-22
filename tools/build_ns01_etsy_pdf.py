#!/usr/bin/env python3
"""Build the branded NS 01 Etsy-edition PDF from its audited Markdown master.

The layout treats the supplied visuals as illustrations, never as physical test evidence.
Product testing, image disclosure, and listing compliance remain owner responsibilities.
"""

from __future__ import annotations

import argparse
import re
import tempfile
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from hashlib import sha256
from html import escape, unescape
from pathlib import Path

from PIL import Image as PILImage
from PIL import ImageDraw, ImageFont
import pymupdf as fitz
from pypdf import PdfReader
from pypdf.generic import ContentStream, IndirectObject
from reportlab.graphics import renderPDF, renderSVG
from reportlab.graphics.shapes import Circle, Drawing, Ellipse, Line, Rect, String
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

try:  # Support direct script execution and package-style imports in tests.
    from .ns01_pdf_model import (
        COVER_IMAGE_BOX_MM,
        HERO_ASSET,
        MATERIALS_ASSET,
        MATERIALS_IMAGE_BOX_MM,
        compile_ns01_pdf_model,
    )
except ImportError:  # pragma: no cover - exercised by direct CLI invocation.
    from ns01_pdf_model import (
        COVER_IMAGE_BOX_MM,
        HERO_ASSET,
        MATERIALS_ASSET,
        MATERIALS_IMAGE_BOX_MM,
        compile_ns01_pdf_model,
    )

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "patterns/01_Hamish_the_Highland_Cow.md"
HERO = HERO_ASSET
MATERIALS_IMAGE = MATERIALS_ASSET
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


def pil_font(
    size: int, bold: bool = False, serif: bool = False
) -> ImageFont.FreeTypeFont:
    font_dir = Path("/usr/share/fonts/truetype/dejavu")
    if serif:
        name = "DejaVuSerif-Bold.ttf" if bold else "DejaVuSerif.ttf"
    else:
        name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    try:
        return ImageFont.truetype(str(font_dir / name), size=size)
    except OSError:
        return ImageFont.load_default()


def assembly_steps(model: dict) -> list[tuple[str, str, str]]:
    """Return source-derived assembly callouts for the raster overview figure."""

    head = model["components"]["head"]
    body = model["components"]["body"]
    head_features = head["features"]
    body_features = body["features"]
    join = head["neck_join"]
    ending = body["ending"]
    horns = head_features["horns"]
    ears = head_features["ears"]
    fringe_rounds = head_features["fringe"]["rounds"]
    back_legs = body_features["back_legs"]
    front_legs = body_features["front_legs"]
    belly_patch = body_features["belly_patch"]
    tail = body_features["tail"]

    return [
        (
            "01",
            "MUZZLE + FACE",
            f"Lock both eye washers before Head Rnd {head['closure']['round']}.",
        ),
        (
            "02",
            "HORNS",
            f"Rnds {horns['round_start']}–{horns['round_end']} · "
            f"{horns['spacing_stitches']} sts apart · angle out/back.",
        ),
        (
            "03",
            "EARS",
            f"Outside horns · centre R{ears['round_start']}–R{ears['round_end']} · cup forward.",
        ),
        (
            "04",
            "FRINGE",
            f"Rnds {min(fringe_rounds)}–{max(fringe_rounds)} · attach after horns/ears.",
        ),
        (
            "05",
            "HEAD → BODY",
            f"Match {ending['stitches']} body R{ending['round']} sts to "
            f"{join['stitches']} head R{join['round']} sts.",
        ),
        (
            "06",
            "BACK LEGS",
            f"Rnds {back_legs['round_start']}–{back_legs['round_end']} · "
            "low on base, near horizontal.",
        ),
        (
            "07",
            "FRONT LEGS",
            f"Rnds {front_legs['round_start']}–{front_legs['round_end']} · "
            f"about {front_legs['gap_stitches']} sts apart.",
        ),
        (
            "08",
            "BELLY PATCH",
            f"Optional · lower edge ~{belly_patch['lower_edge_offset_from_base_rounds']} rounds above base.",
        ),
        (
            "09",
            "TAIL + SCARF",
            f"Tail at {tail['anchor_note']}; tie scarf, weave ends and fluff fringe.",
        ),
    ]


def create_assembly_asset(path: Path, model: dict) -> None:
    """Create a source-derived assembly overview without replacing written directions."""

    path.parent.mkdir(parents=True, exist_ok=True)
    canvas = PILImage.new("RGB", (1800, 1180), "#F7F1E7")
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle(
        (40, 40, 1760, 1140), radius=38, fill="#FFFDF8", outline="#D8CDBE", width=3
    )
    draw.text(
        (105, 85),
        "ASSEMBLY MAP",
        font=pil_font(54, bold=True, serif=True),
        fill="#28231F",
    )
    draw.text(
        (107, 158),
        "Pin first. Check symmetry. Then sew in this exact order.",
        font=pil_font(27),
        fill="#6F665E",
    )

    steps = assembly_steps(model)
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
        draw.rounded_rectangle(
            (x, y, x + card_w, y + card_h),
            radius=24,
            fill=fill,
            outline=outline,
            width=4,
        )
        draw.ellipse((x + 24, y + 25, x + 106, y + 107), fill="#31473B")
        number_box = draw.textbbox((0, 0), number, font=pil_font(27, bold=True))
        number_w = number_box[2] - number_box[0]
        draw.text(
            (x + 65 - number_w / 2, y + 47),
            number,
            font=pil_font(27, bold=True),
            fill="#FFFDF8",
        )
        draw.text(
            (x + 128, y + 27), label, font=pil_font(25, bold=True), fill="#28231F"
        )
        draw.multiline_text(
            (x + 128, y + 80),
            wrap_words(note, 36),
            font=pil_font(20),
            fill="#5F5750",
            spacing=7,
        )

    draw.rounded_rectangle((105, 1010, 1695, 1090), radius=20, fill="#31473B")
    head_join = model["components"]["head"]["neck_join"]
    body_ending = model["components"]["body"]["ending"]
    critical = (
        "CRITICAL NECK JOIN   "
        f"{body_ending['stitches']} BODY STS ↔ "
        f"{head_join['stitches']} HEAD R{head_join['round']} STS   ·   LADDER-STITCH TWICE"
    )
    box = draw.textbbox((0, 0), critical, font=pil_font(25, bold=True))
    text_w = box[2] - box[0]
    draw.text(
        ((1800 - text_w) / 2, 1031),
        critical,
        font=pil_font(25, bold=True),
        fill="#FFFDF8",
    )
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
    return stripped.startswith("|") and is_table_separator(next_line)


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
        if (
            line.startswith("|")
            and i + 1 < len(lines)
            and is_table_separator(lines[i + 1].strip())
        ):
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
            blocks.append(
                Block(kind, body, int(marker[:-1]) if kind == "ordered" else 0)
            )
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


def expected_progress_box_count(markdown_text: str) -> int:
    """Count source rows for which the PDF renderer adds a progress checkbox."""

    count = 0
    for block in parse_markdown(markdown_text):
        if (
            block.kind != "table"
            or not isinstance(block.value, list)
            or not block.value
        ):
            continue
        rows = block.value
        if rows[0][0].strip().lower() == "rnd":
            count += max(0, len(rows) - 1)
    return count


def inline_markup(text: str) -> str:
    """Escape text and convert the limited inline Markdown used by the masters."""

    value = escape(text, quote=False)
    value = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", value)
    value = re.sub(r"`(.+?)`", r'<font name="Courier">\1</font>', value)
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


def _round_position(
    component: dict, round_number: float, bottom: float, top: float
) -> float:
    total = max(row["end"] for row in component["rounds"])
    fraction = (round_number - 1) / max(1, total - 1)
    if component["direction"] == "TOP_DOWN":
        return top - fraction * (top - bottom)
    return bottom + fraction * (top - bottom)


def make_placement_drawing(model: dict, *, printer_saver: bool = False) -> Drawing:
    """Create a vector-only placement schematic from the compiled NS01 model."""

    if printer_saver:
        ink = colors.black
        ginger = HexColor("#D8D8D8")
        oat = HexColor("#F1F1F1")
        accent = HexColor("#777777")
        panel = colors.white
    else:
        ink = FOREST_DARK
        ginger = PALE_GINGER
        oat = OAT
        accent = GINGER
        panel = PAPER

    drawing = Drawing(492, 166)
    drawing.add(
        String(
            246,
            156,
            "NS 01 · COMPONENT PLACEMENT (SCHEMATIC, NOT TO SCALE)",
            textAnchor="middle",
            fontName="Helvetica-Bold",
            fontSize=8.1,
            fillColor=ink,
        )
    )
    drawing.add(
        Rect(7, 19, 235, 130, fillColor=panel, strokeColor=accent, strokeWidth=0.7)
    )
    drawing.add(
        Rect(250, 19, 235, 130, fillColor=panel, strokeColor=accent, strokeWidth=0.7)
    )

    head = model["components"]["head"]
    head_features = head["features"]
    head_bottom, head_top = 45, 124
    head_x, head_y, head_w, head_h = 22, 47, 64, 72
    drawing.add(
        Ellipse(
            head_x + head_w / 2,
            head_y + head_h / 2,
            head_w / 2,
            head_h / 2,
            fillColor=ginger,
            strokeColor=ink,
            strokeWidth=1.1,
        )
    )

    # Horns and ears are visual markers for the source-derived round bands.
    horn_y = _round_position(
        head, head_features["horns"]["round_start"], head_bottom, head_top
    )
    drawing.add(Line(38, horn_y, 31, horn_y + 12, strokeColor=oat, strokeWidth=4.2))
    drawing.add(Line(69, horn_y, 76, horn_y + 12, strokeColor=oat, strokeWidth=4.2))
    ear_y = _round_position(
        head, head_features["ears"]["round_start"], head_bottom, head_top
    )
    drawing.add(
        Ellipse(21, ear_y + 2, 7, 4, fillColor=ginger, strokeColor=ink, strokeWidth=0.7)
    )
    drawing.add(
        Ellipse(87, ear_y + 2, 7, 4, fillColor=ginger, strokeColor=ink, strokeWidth=0.7)
    )

    fringe_y = [
        _round_position(head, round_number, head_bottom, head_top)
        for round_number in head_features["fringe"]["rounds"]
    ]
    for y_value in fringe_y:
        drawing.add(Line(37, y_value, 71, y_value, strokeColor=accent, strokeWidth=1.0))

    eye_diameter = head_features["eyes"]["diameter_mm"]
    eye_start = head_features["eyes"]["round_start"]
    eye_end = head_features["eyes"]["round_end"]
    eye_y = (
        _round_position(head, eye_start, head_bottom, head_top)
        + _round_position(head, eye_end, head_bottom, head_top)
    ) / 2
    drawing.add(Circle(42, eye_y, 2.2, fillColor=ink, strokeColor=ink))
    drawing.add(Circle(66, eye_y, 2.2, fillColor=ink, strokeColor=ink))
    drawing.add(Line(45, eye_y, 63, eye_y, strokeColor=ink, strokeWidth=0.4))

    muzzle = head_features["muzzle"]
    muzzle_top = _round_position(head, muzzle["round_start"], head_bottom, head_top)
    muzzle_bottom = (
        _round_position(head, muzzle["lower_edge_round_start"], head_bottom, head_top)
        + _round_position(head, muzzle["lower_edge_round_end"], head_bottom, head_top)
    ) / 2
    muzzle_height = max(12, muzzle_top - muzzle_bottom + 4)
    drawing.add(
        Ellipse(
            54,
            muzzle_bottom - 2 + muzzle_height / 2,
            25,
            muzzle_height / 2,
            fillColor=oat,
            strokeColor=ink,
            strokeWidth=0.8,
        )
    )

    def head_label(y: float, text: str, bold: bool = False) -> None:
        drawing.add(
            String(
                101,
                y,
                text,
                fontName="Helvetica-Bold" if bold else "Helvetica",
                fontSize=6.7 if not bold else 7.2,
                fillColor=ink,
            )
        )

    head_total = max(row["end"] for row in head["rounds"])
    head_label(134, f"Head · TOP DOWN · R1–R{head_total}", True)
    head_label(
        119,
        f"Horns R{head_features['horns']['round_start']}–R{head_features['horns']['round_end']} · {head_features['horns']['spacing_stitches']} sts apart",
    )
    fringe_rounds = head_features["fringe"]["rounds"]
    head_label(
        106,
        f"Ears R{head_features['ears']['round_start']}–R{head_features['ears']['round_end']} · fringe R{min(fringe_rounds)}–R{max(fringe_rounds)}",
    )
    head_label(
        93,
        f"Eyes {eye_diameter:g} mm · R{eye_start}–R{eye_end} · "
        f"{head_features['eyes']['spacing_stitches']} sts apart",
    )
    head_label(80, f"Muzzle top: R{muzzle['round_start']}")
    head_label(
        67,
        f"Lower edge: R{muzzle['lower_edge_round_start']}–R{muzzle['lower_edge_round_end']}",
    )
    head_label(
        54,
        f"Join ring: R{head['neck_join']['round']} · {head['neck_join']['stitches']} sts",
    )
    head_label(
        41, f"Closes at R{head['closure']['round']} · {head['closure']['stitches']} sts"
    )

    body = model["components"]["body"]
    body_features = body["features"]
    body_bottom, body_top = 47, 120
    drawing.add(
        Ellipse(297.5, 84, 28.5, 35, fillColor=ginger, strokeColor=ink, strokeWidth=1.1)
    )
    back_mid = (
        body_features["back_legs"]["round_start"]
        + body_features["back_legs"]["round_end"]
    ) / 2
    back_y = _round_position(body, back_mid, body_bottom, body_top)
    front_mid = (
        body_features["front_legs"]["round_start"]
        + body_features["front_legs"]["round_end"]
    ) / 2
    front_y = _round_position(body, front_mid, body_bottom, body_top)
    drawing.add(
        Ellipse(
            266.5,
            back_y + 4,
            7.5,
            9,
            fillColor=ginger,
            strokeColor=ink,
            strokeWidth=0.7,
        )
    )
    drawing.add(
        Ellipse(
            328.5,
            front_y + 4,
            7.5,
            9,
            fillColor=ginger,
            strokeColor=ink,
            strokeWidth=0.7,
        )
    )

    def body_label(y: float, text: str, bold: bool = False) -> None:
        drawing.add(
            String(
                342,
                y,
                text,
                fontName="Helvetica-Bold" if bold else "Helvetica",
                fontSize=6.6 if not bold else 7.2,
                fillColor=ink,
            )
        )

    body_total = max(row["end"] for row in body["rounds"])
    belly_offset = body_features["belly_patch"]["lower_edge_offset_from_base_rounds"]
    body_label(134, f"Body · BOTTOM UP · R1–R{body_total}", True)
    body_label(
        119, f"Open neck: R{body['ending']['round']} · {body['ending']['stitches']} sts"
    )
    body_label(
        106,
        f"Front legs: R{body_features['front_legs']['round_start']}–R{body_features['front_legs']['round_end']} · ~{body_features['front_legs']['gap_stitches']} sts gap",
    )
    body_label(
        93,
        f"Back legs: R{body_features['back_legs']['round_start']}–R{body_features['back_legs']['round_end']}",
    )
    body_label(80, "Belly patch: optional; lower edge")
    body_label(68, f"~{belly_offset} rounds above base")
    body_label(54, "Tail anchor: centre-back")
    body_label(41, "above last increase round")

    return drawing


def export_placement_svg(
    model: dict, output: Path, *, printer_saver: bool = False
) -> None:
    """Export the same vector drawing used in the PDF as standalone SVG."""

    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    renderSVG.drawToFile(
        make_placement_drawing(model, printer_saver=printer_saver), str(output)
    )


class PlacementDiagramFlowable(Flowable):
    """Place the round-referenced drawing as vector paths/text in the PDF."""

    def __init__(self, drawing: Drawing):
        super().__init__()
        self.drawing = drawing
        self.scale_factor = 1.0

    def wrap(
        self, available_width: float, available_height: float
    ) -> tuple[float, float]:
        self.scale_factor = min(1.0, available_width / self.drawing.width)
        self.width = self.drawing.width * self.scale_factor
        self.height = self.drawing.height * self.scale_factor
        return self.width, self.height

    def draw(self) -> None:
        self.canv.saveState()
        self.canv.scale(self.scale_factor, self.scale_factor)
        renderPDF.draw(self.drawing, self.canv, 0, 0)
        self.canv.restoreState()


class GaugeRulerFlowable(Flowable):
    """A true 50 mm square with explicit print-scaling instructions."""

    side = 50 * mm

    def __init__(self, fonts: Fonts, model: dict, *, printer_saver: bool = False):
        super().__init__()
        self.fonts = fonts
        self.gauge = model["pattern"]["gauge"]
        self.printer_saver = printer_saver
        self.width = 0
        self.height = 55 * mm

    def wrap(
        self, available_width: float, available_height: float
    ) -> tuple[float, float]:
        self.width = available_width
        return self.width, self.height

    def draw(self) -> None:
        canvas = self.canv
        canvas.saveState()
        ink = colors.black if self.printer_saver else FOREST_DARK
        fill = colors.white if self.printer_saver else PARCHMENT
        box_x = self.width - self.side
        canvas.setFillColor(fill)
        canvas.setStrokeColor(ink)
        canvas.setLineWidth(0.6)
        canvas.rect(box_x, 0, self.side, self.side, stroke=1, fill=1)
        canvas.setFillColor(ink)
        canvas.setFont(self.fonts.sans_bold, 8.1)
        canvas.drawString(0, 48 * mm, "PRINT-SCALE CHECK")
        canvas.setFont(self.fonts.sans, 7.1)
        canvas.drawString(
            0,
            38 * mm,
            f"Master gauge: {self.gauge['stitches']} sc × {self.gauge['rounds']} "
            f"rounds = {self.gauge['measure_cm']:g} cm.",
        )
        canvas.drawString(
            0, 28 * mm, "Print at Actual Size / 100%; disable Fit to Page."
        )
        canvas.drawString(0, 18 * mm, "Measure the square with a ruler after printing.")
        canvas.setFont(self.fonts.sans_bold, 7.4)
        canvas.drawCentredString(box_x + self.side / 2, 29 * mm, "50 mm × 50 mm")
        canvas.setFont(self.fonts.sans, 6.4)
        canvas.drawCentredString(box_x + self.side / 2, 23 * mm, "(5 cm × 5 cm)")
        canvas.restoreState()


class CoverFlowable(Flowable):
    """Full-page editorial cover for the customer PDF."""

    def __init__(self, hero: Path, fonts: Fonts, model: dict):
        super().__init__()
        self.hero = hero
        self.fonts = fonts
        self.model = model
        self.width = PAGE_WIDTH
        self.height = PAGE_HEIGHT - 0.2 * mm

    def wrap(self, available_width, available_height):
        return self.width, min(self.height, available_height)

    def draw(self) -> None:
        canvas = self.canv
        pattern = self.model["pattern"]
        canvas.saveState()
        canvas.setFillColor(PARCHMENT)
        canvas.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, stroke=0, fill=1)

        canvas.setFillColor(FOREST_DARK)
        canvas.rect(0, PAGE_HEIGHT - 18 * mm, PAGE_WIDTH, 18 * mm, stroke=0, fill=1)
        canvas.setFillColor(colors.white)
        canvas.setFont(self.fonts.sans_bold, 9)
        canvas.drawString(15 * mm, PAGE_HEIGHT - 11.2 * mm, BRAND.upper())
        canvas.setFont(self.fonts.sans, 7.5)
        canvas.drawRightString(
            PAGE_WIDTH - 15 * mm, PAGE_HEIGHT - 11.2 * mm, "ORIGINAL CROCHET PATTERN"
        )

        image_x, image_y = 88 * mm, 55 * mm
        image_w = COVER_IMAGE_BOX_MM[0] * mm
        image_h = COVER_IMAGE_BOX_MM[1] * mm
        canvas.setFillColor(PAPER)
        canvas.roundRect(
            image_x - 3 * mm,
            image_y - 3 * mm,
            image_w + 6 * mm,
            image_h + 6 * mm,
            5 * mm,
            stroke=0,
            fill=1,
        )
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
        canvas.roundRect(
            14 * mm, 224 * mm, 54 * mm, 11 * mm, 5.5 * mm, stroke=0, fill=1
        )
        canvas.setFillColor(colors.white)
        canvas.setFont(self.fonts.sans_bold, 9.5)
        canvas.drawCentredString(
            41 * mm, 227.7 * mm, f"DESIGN CODE  {pattern['design_code']}"
        )

        canvas.setFillColor(FOREST_DARK)
        canvas.setFont(self.fonts.serif_bold, 33)
        canvas.drawString(14 * mm, 202 * mm, pattern["title"].upper())
        canvas.setFont(self.fonts.serif, 18)
        canvas.drawString(14 * mm, 191 * mm, pattern["subtitle"])

        canvas.setStrokeColor(GINGER)
        canvas.setLineWidth(2)
        canvas.line(14 * mm, 181 * mm, 70 * mm, 181 * mm)
        canvas.setFillColor(MUTED)
        canvas.setFont(self.fonts.sans, 8.4)
        canvas.drawString(14 * mm, 170 * mm, "A shaggy, sturdy Highland character")
        canvas.drawString(14 * mm, 164 * mm, "with a broad oat-cream muzzle and")
        canvas.drawString(14 * mm, 158 * mm, "a weather-beaten ginger fringe.")

        time_hours = pattern["time_hours"]
        size_cm = pattern["finished_size_cm"]
        stats = [
            (f"{pattern['terminology']} TERMS", 137),
            (pattern["skill_level"].upper(), 126),
            (f"{time_hours['minimum']}–{time_hours['maximum']} HOURS", 115),
            (f"ABOUT {size_cm:g} CM", 104),
        ]
        for label, y in stats:
            canvas.setFillColor(FOREST)
            canvas.circle(17 * mm, y * mm + 1.4 * mm, 1.6 * mm, stroke=0, fill=1)
            canvas.setFillColor(INK)
            canvas.setFont(self.fonts.sans_bold, 8.2)
            canvas.drawString(23 * mm, y * mm, label)

        yarns = {yarn["id"]: yarn["name"] for yarn in pattern["yarns"]}
        canvas.setFillColor(PALE_GINGER)
        canvas.roundRect(14 * mm, 57 * mm, 62 * mm, 32 * mm, 3 * mm, stroke=0, fill=1)
        canvas.setFillColor(CHOCOLATE)
        canvas.setFont(self.fonts.sans_bold, 7.5)
        canvas.drawString(19 * mm, 81 * mm, "ORIGINAL COLOURWAY")
        canvas.setFont(self.fonts.sans, 7.0)
        canvas.drawString(19 * mm, 74 * mm, f"A {yarns['A']} · B {yarns['B']}")
        canvas.drawString(19 * mm, 68.5 * mm, f"C {yarns['C']} · D {yarns['D']}")
        canvas.drawString(
            19 * mm,
            62.5 * mm,
            f"{pattern['yarn_weight']} · {pattern['hook_mm']:g} mm / {pattern['hook_us']}",
        )

        canvas.setStrokeColor(LINE)
        canvas.setLineWidth(0.7)
        canvas.line(14 * mm, 42 * mm, PAGE_WIDTH - 14 * mm, 42 * mm)
        canvas.setFillColor(MUTED)
        canvas.setFont(self.fonts.sans, 6.8)
        canvas.drawString(14 * mm, 34.5 * mm, REVISION.upper())
        canvas.drawRightString(
            PAGE_WIDTH - 14 * mm, 34.5 * mm, "DIGITAL CROCHET PATTERN"
        )
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
        canvas.drawCentredString(
            PAGE_WIDTH / 2, 5.1 * mm, "NOVALITY CROCHET STUDIO  ·  ORIGINAL PATTERN"
        )
        canvas.restoreState()


class PrinterCoverFlowable(Flowable):
    """Black-on-white cover for the companion printer-saver edition."""

    def __init__(self, fonts: Fonts, model: dict):
        super().__init__()
        self.fonts = fonts
        self.model = model
        self.width = PAGE_WIDTH
        self.height = PAGE_HEIGHT - 0.2 * mm

    def wrap(self, available_width, available_height):
        return self.width, min(self.height, available_height)

    def draw(self) -> None:
        canvas = self.canv
        pattern = self.model["pattern"]
        canvas.saveState()
        canvas.setFillColor(colors.white)
        canvas.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, stroke=0, fill=1)
        canvas.setStrokeColor(colors.black)
        canvas.setLineWidth(0.8)
        canvas.rect(
            14 * mm,
            14 * mm,
            PAGE_WIDTH - 28 * mm,
            PAGE_HEIGHT - 28 * mm,
            stroke=1,
            fill=0,
        )

        canvas.setFillColor(colors.black)
        canvas.setFont(self.fonts.sans_bold, 9)
        canvas.drawString(20 * mm, PAGE_HEIGHT - 25 * mm, BRAND.upper())
        canvas.setFont(self.fonts.sans, 8)
        canvas.drawRightString(
            PAGE_WIDTH - 20 * mm, PAGE_HEIGHT - 25 * mm, "PRINTER-SAVER EDITION"
        )
        canvas.line(
            20 * mm, PAGE_HEIGHT - 31 * mm, PAGE_WIDTH - 20 * mm, PAGE_HEIGHT - 31 * mm
        )

        canvas.setFont(self.fonts.sans_bold, 12)
        canvas.drawString(20 * mm, 235 * mm, f"DESIGN CODE {pattern['design_code']}")
        canvas.setFont(self.fonts.serif_bold, 34)
        canvas.drawString(20 * mm, 211 * mm, pattern["title"].upper())
        canvas.setFont(self.fonts.serif, 20)
        canvas.drawString(20 * mm, 198 * mm, pattern["subtitle"])
        canvas.setLineWidth(1.2)
        canvas.line(20 * mm, 188 * mm, 92 * mm, 188 * mm)

        canvas.setFont(self.fonts.sans_bold, 10)
        canvas.drawString(
            20 * mm, 172 * mm, "BLACK + WHITE · WHITE BACKGROUNDS · PROGRESS BOXES"
        )
        time_hours = pattern["time_hours"]
        canvas.setFont(self.fonts.sans, 9)
        canvas.drawString(
            20 * mm,
            160 * mm,
            f"{pattern['terminology']} terms · {pattern['skill_level']} · "
            f"{time_hours['minimum']}–{time_hours['maximum']} hours · "
            f"About {pattern['finished_size_cm']:g} cm",
        )
        canvas.drawString(
            20 * mm,
            151 * mm,
            f"{pattern['yarn_weight']} yarn · {pattern['hook_mm']:g} mm hook / {pattern['hook_us']}",
        )

        yarns = {yarn["id"]: yarn["name"] for yarn in pattern["yarns"]}
        canvas.setLineWidth(0.5)
        canvas.rect(20 * mm, 106 * mm, PAGE_WIDTH - 40 * mm, 32 * mm, stroke=1, fill=0)
        canvas.setFont(self.fonts.sans_bold, 8.5)
        canvas.drawString(25 * mm, 130 * mm, "NAMED ORIGINAL COLOURWAY")
        canvas.setFont(self.fonts.sans, 8.0)
        canvas.drawString(
            25 * mm, 121 * mm, f"Yarn A {yarns['A']} · Yarn B {yarns['B']}"
        )
        canvas.drawString(
            25 * mm, 114 * mm, f"Yarn C {yarns['C']} · Yarn D {yarns['D']}"
        )
        canvas.drawString(
            25 * mm,
            108 * mm,
            "Swatch hues are presentation aids; follow the written yarn names.",
        )

        canvas.setFont(self.fonts.sans_bold, 8.5)
        canvas.drawString(20 * mm, 91 * mm, "ABOUT THIS COMPANION FILE")
        canvas.setFont(self.fonts.sans, 8.2)
        canvas.drawString(
            20 * mm,
            81 * mm,
            "Designed for economical home printing and handwritten progress tracking.",
        )
        canvas.drawString(
            20 * mm,
            73 * mm,
            "Large raster artwork is omitted. Use the full-colour edition for the materials",
        )
        canvas.drawString(
            20 * mm,
            66 * mm,
            "visual and assembly illustration; the written instructions in both files are the same.",
        )

        canvas.line(20 * mm, 47 * mm, PAGE_WIDTH - 20 * mm, 47 * mm)
        canvas.setFont(self.fonts.sans, 7)
        canvas.drawString(20 * mm, 37 * mm, f"© 2026 {BRAND} · All rights reserved")
        canvas.drawRightString(
            PAGE_WIDTH - 20 * mm, 37 * mm, "PERSONAL LICENSE · SEE TERMS"
        )
        canvas.setFont(self.fonts.sans_bold, 7)
        canvas.drawCentredString(
            PAGE_WIDTH / 2, 24 * mm, f"{DESIGN_CODE} · PRINTER-SAVER CROCHET PATTERN"
        )
        canvas.restoreState()


class ClosingPanel(Flowable):
    """Light closing page that matches the interior rather than a colour flood."""

    def __init__(self, width: float, fonts: Fonts):
        super().__init__()
        self.fonts = fonts
        self.width = width
        self.height = 172 * mm

    def wrap(self, available_width, available_height):
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
        canvas.drawCentredString(
            center, 99 * mm, "Make it slowly. Check every seam. Make it yours."
        )

        canvas.setStrokeColor(GINGER_LIGHT)
        canvas.setLineWidth(1.2)
        canvas.line(36 * mm, 88 * mm, self.width - 36 * mm, 88 * mm)
        canvas.setFillColor(INK)
        canvas.setFont(self.fonts.sans_bold, 8.2)
        canvas.drawCentredString(center, 76 * mm, "SHARE YOUR FINISHED HAMISH")
        canvas.setFont(self.fonts.sans, 8)
        canvas.drawCentredString(
            center, 67 * mm, "#NovalityCrochetStudio   ·   #HamishTheHighlandCow"
        )

        canvas.setFont(self.fonts.sans, 7.4)
        canvas.setFillColor(MUTED)
        canvas.drawCentredString(
            center,
            50 * mm,
            "Keep this design code with support questions and pattern revisions.",
        )
        canvas.setFont(self.fonts.sans_bold, 8)
        canvas.setFillColor(FOREST_DARK)
        canvas.drawCentredString(center, 39 * mm, BRAND.upper())
        canvas.setFont(self.fonts.sans, 7)
        canvas.drawCentredString(
            center, 29 * mm, f"© 2026 {BRAND} · ALL RIGHTS RESERVED · {DESIGN_CODE}"
        )
        canvas.restoreState()


class PrinterNotesPanel(Flowable):
    """Low-ink completion checklist and ruled notes area."""

    def __init__(self, width: float, fonts: Fonts):
        super().__init__()
        self.fonts = fonts
        self.width = width
        self.height = 228 * mm

    def wrap(self, available_width, available_height):
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
        canvas.drawString(
            0, 7 * mm, f"{BRAND} · {DESIGN_CODE} · printer-saver companion"
        )
        canvas.drawRightString(
            self.width, 7 * mm, "Keep this page with your project notes"
        )
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
        edition = (
            "printer-saver crochet pattern" if printer_saver else "crochet pattern"
        )
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
        cover_frame = Frame(
            0,
            0,
            PAGE_WIDTH,
            PAGE_HEIGHT,
            id="cover",
            leftPadding=0,
            rightPadding=0,
            topPadding=0,
            bottomPadding=0,
        )
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
                PageTemplate(
                    id="Cover", frames=[cover_frame], onPage=self.draw_cover_meta
                ),
                PageTemplate(
                    id="Content", frames=[content_frame], onPage=self.draw_content_page
                ),
            ]
        )

    def draw_cover_meta(self, canvas, doc) -> None:
        self.set_pdf_metadata(canvas)

    def draw_content_page(self, canvas, doc) -> None:
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
        canvas.drawCentredString(
            PAGE_WIDTH / 2, 7.2 * mm, "PERSONAL LICENSE · SEE TERMS"
        )
        canvas.setFont(self.fonts.sans_bold, 7)
        canvas.drawRightString(
            PAGE_WIDTH - 18 * mm, 7.2 * mm, f"{DESIGN_CODE}   ·   {doc.page}"
        )
        canvas.restoreState()

    def set_pdf_metadata(self, canvas) -> None:
        canvas.setTitle(f"{DESIGN_CODE} — {TITLE} {SUBTITLE}")
        canvas.setAuthor(BRAND)
        subject = (
            "Printer-saver crochet pattern"
            if self.printer_saver
            else "Branded crochet pattern"
        )
        canvas.setSubject(f"{subject} · {DESIGN_CODE}")
        canvas.setCreator(BRAND)
        canvas.setKeywords(f"crochet, amigurumi, Highland cow, {DESIGN_CODE}, {BRAND}")

    def afterFlowable(self, flowable: Flowable) -> None:
        if isinstance(flowable, HeadingParagraph):
            key = flowable.bookmark_key
            level = flowable.outline_level
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(
                flowable.plain_heading, key, level=level, closed=False
            )
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
        (
            "LINEBELOW",
            (0, 0),
            (-1, 0),
            1.0,
            colors.black if printer_saver else FOREST_DARK,
        ),
    ]
    table.setStyle(TableStyle(commands))
    return table


def colour_swatch_table(
    styles: dict[str, ParagraphStyle],
    available_width: float,
    model: dict,
    *,
    printer_saver: bool = False,
) -> Table:
    """Render source-derived yarn names/amounts and presentation-only swatches."""

    display_colours = {"A": GINGER, "B": OAT, "C": CHOCOLATE, "D": RUST}
    labels = [
        (
            f"YARN {yarn['id']}",
            yarn["name"],
            f"{yarn['grams']:g} g in master",
            display_colours[yarn["id"]],
        )
        for yarn in model["pattern"]["yarns"]
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
    styles: dict[str, ParagraphStyle],
    materials_image: Path,
    available_width: float,
    model: dict,
) -> list[Flowable]:
    pattern = model["pattern"]
    time_hours = pattern["time_hours"]
    badge_data = [
        [
            Paragraph(
                f"<b>TERMINOLOGY</b><br/>{pattern['terminology']} crochet terms",
                styles["body_compact"],
            ),
            Paragraph(
                f"<b>SKILL LEVEL</b><br/>{pattern['skill_level']}",
                styles["body_compact"],
            ),
            Paragraph(
                f"<b>ACTIVE TIME</b><br/>{time_hours['minimum']}–{time_hours['maximum']} hours",
                styles["body_compact"],
            ),
            Paragraph(
                f"<b>FINISHED SIZE</b><br/>About {pattern['finished_size_cm']:g} cm",
                styles["body_compact"],
            ),
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
    materials = image_for_width(
        materials_image,
        MATERIALS_IMAGE_BOX_MM[0] * mm,
        MATERIALS_IMAGE_BOX_MM[1] * mm,
    )
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
        colour_swatch_table(styles, available_width, model),
        Paragraph(
            "COLOUR GUIDE · Swatch hues are presentation aids; select yarn by the names in the written Materials section. Screen appearance and dye lots vary.",
            styles["caption"],
        ),
        materials,
        Paragraph(
            "FIGURE 1 · Illustrative materials visual only. Refer to the written Materials section for the canonical yarn colours, amounts, tools and notions.",
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
    styles: dict[str, ParagraphStyle], available_width: float, model: dict
) -> list[Flowable]:
    """Create a low-ink profile page without raster artwork or colour fills."""

    pattern = model["pattern"]
    time_hours = pattern["time_hours"]
    facts = Table(
        [
            [
                Paragraph(
                    f"<b>TERMINOLOGY</b><br/>{pattern['terminology']} crochet terms",
                    styles["body_compact"],
                ),
                Paragraph(
                    f"<b>SKILL LEVEL</b><br/>{pattern['skill_level']}",
                    styles["body_compact"],
                ),
                Paragraph(
                    f"<b>ACTIVE TIME</b><br/>{time_hours['minimum']}–{time_hours['maximum']} hours",
                    styles["body_compact"],
                ),
                Paragraph(
                    f"<b>FINISHED SIZE</b><br/>About {pattern['finished_size_cm']:g} cm",
                    styles["body_compact"],
                ),
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
        colour_swatch_table(styles, available_width, model, printer_saver=True),
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
    model: dict,
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
    join = model["components"]["head"]["neck_join"]
    body_ending = model["components"]["body"]["ending"]
    checkpoint_text = (
        "Three checkpoints: lock both eye washers while the head is open; "
        f"match all {join['stitches']} body R{body_ending['round']} stitches to "
        f"head R{join['round']}; and make two complete passes on structural seams."
    )
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
            checkpoint_text,
            styles["front_body"],
        ),
    ]


def blocks_to_story(
    blocks: Iterable[Block],
    styles: dict[str, ParagraphStyle],
    available_width: float,
    assembly: Path | None,
    *,
    fonts: Fonts,
    model: dict,
    placement_drawing: Drawing | None,
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
            story.append(
                HeadingParagraph(inline_markup(text), styles[style_key], level, key)
            )
            if text == "Gauge & size":
                story.extend(
                    [
                        GaugeRulerFlowable(fonts, model, printer_saver=printer_saver),
                        Spacer(1, 3 * mm),
                    ]
                )
            if text == "Finishing & assembly":
                if assembly is not None and not inserted_assembly:
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
                if placement_drawing is not None:
                    story.extend(
                        [
                            Paragraph(
                                "Round-referenced placement schematic", styles["h3"]
                            ),
                            PlacementDiagramFlowable(placement_drawing),
                            Paragraph(
                                "SCHEMATIC · Not to scale. Use the written pattern for actual placement and construction; no stitch-by-stitch join map is implied.",
                                styles["caption"],
                            ),
                        ]
                    )
            if text == "Colourways":
                story.extend(
                    [
                        colour_swatch_table(
                            styles,
                            available_width,
                            model,
                            printer_saver=printer_saver,
                        ),
                        Paragraph(
                            "ORIGINAL COLOURWAY · Swatches are visual aids; the written source names control yarn selection.",
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
            story.append(
                Paragraph(
                    inline_markup(str(block.value)), styles["bullet"], bulletText="•"
                )
            )
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
            style = (
                styles["callout"] if current_h2.startswith("Safety") else styles["body"]
            )
            value = str(block.value)
            if current_h2 == "Colourways":
                value = f"<b>Optional body-tone variations:</b> {escape(value)}"
                story.append(Paragraph(value, style))
            else:
                story.append(Paragraph(inline_markup(value), style))
    return story


def build_pdf(output: Path, model: dict | None = None) -> None:
    if model is None:
        model = compile_ns01_pdf_model(SOURCE)
    if not SOURCE.exists():
        raise FileNotFoundError(f"Missing audited master: {SOURCE}")
    if not HERO.exists():
        raise FileNotFoundError(f"Missing illustrative cover asset: {HERO}")
    if not MATERIALS_IMAGE.exists():
        raise FileNotFoundError(
            f"Missing illustrative materials asset: {MATERIALS_IMAGE}"
        )

    output.parent.mkdir(parents=True, exist_ok=True)
    assembly = ASSET_DIR / "ns01_assembly_map.png"
    create_assembly_asset(assembly, model)

    fonts = register_fonts()
    styles = make_styles(fonts)
    text = normalize_branding(SOURCE.read_text(encoding="utf-8"))
    blocks = parse_markdown(text)
    placement_drawing = make_placement_drawing(model)

    document = PatternDocument(output, fonts)
    story: list[Flowable] = [
        CoverFlowable(HERO, fonts, model),
        NextPageTemplate("Content"),
        PageBreak(),
        *profile_story(styles, MATERIALS_IMAGE, document.width, model),
        PageBreak(),
        *toc_story(styles, fonts, model),
        PageBreak(),
        *blocks_to_story(
            blocks,
            styles,
            document.width,
            assembly,
            fonts=fonts,
            model=model,
            placement_drawing=placement_drawing,
        ),
        PageBreak(),
        ClosingPanel(document.width, fonts),
    ]
    document.multiBuild(story)


def build_printer_pdf(output: Path, model: dict | None = None) -> None:
    """Build the black-on-white companion without any raster image objects."""

    if model is None:
        model = compile_ns01_pdf_model(SOURCE)
    if not SOURCE.exists():
        raise FileNotFoundError(f"Missing audited master: {SOURCE}")
    output.parent.mkdir(parents=True, exist_ok=True)

    fonts = register_fonts()
    styles = make_printer_styles(fonts)
    text = normalize_branding(SOURCE.read_text(encoding="utf-8"))
    blocks = parse_markdown(text)
    placement_drawing = make_placement_drawing(model, printer_saver=True)

    document = PatternDocument(output, fonts, printer_saver=True)
    story: list[Flowable] = [
        PrinterCoverFlowable(fonts, model),
        NextPageTemplate("Content"),
        PageBreak(),
        *printer_profile_story(styles, document.width, model),
        PageBreak(),
        *toc_story(styles, fonts, model, printer_saver=True),
        PageBreak(),
        *blocks_to_story(
            blocks,
            styles,
            document.width,
            None,
            fonts=fonts,
            model=model,
            placement_drawing=placement_drawing,
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


def check_pdf_text_bounds(output: Path, *, tolerance_points: float = 1.0) -> int:
    """Reject text glyph boxes outside the physical page rectangle.

    This is a page-level bounds check for the ReportLab output. It is not an
    HTML DOM or parent-table-cell overflow test.
    """

    checked_spans = 0
    with fitz.open(output) as document:
        for page_number, page in enumerate(document, start=1):
            bounds = page.rect
            for block in page.get_text("dict")["blocks"]:
                if block.get("type") != 0:
                    continue
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        if not span.get("text", "").strip():
                            continue
                        checked_spans += 1
                        x0, y0, x1, y1 = span["bbox"]
                        if (
                            x0 < bounds.x0 - tolerance_points
                            or y0 < bounds.y0 - tolerance_points
                            or x1 > bounds.x1 + tolerance_points
                            or y1 > bounds.y1 + tolerance_points
                        ):
                            raise ValueError(
                                f"Text extends beyond page {page_number} bounds: {span['text']!r}"
                            )
    return checked_spans


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
    text_spans = check_pdf_text_bounds(output)
    for number, (page, text) in enumerate(
        zip(reader.pages, page_texts, strict=True), 1
    ):
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
        "50 mm × 50 mm",
        "Round-referenced placement schematic",
        "Abbreviations (US terms)",
        "Techniques used, in the order you will meet them",
        "1. Head - Yarn A",
        "2. Muzzle & nostrils - Yarn B",
        "3. Body - Yarn A",
        "4. Belly patch - Yarn B (optional)",
        "5. Legs - start with Yarn C, change to Yarn A (make 4)",
        "All four identical",
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
        "YARN D · RUST (OPTIONAL)",
        "Care",
        "Terms of Use",
        "Copyright & ownership",
        "18 head stitches of Rnd 14",
        "ladder-stitch around TWICE",
        "43 knots",
        f"© 2026 {BRAND}",
    ]
    normalized_text = " ".join(all_text.lower().split())
    for phrase in required_text:
        if phrase.lower() not in normalized_text:
            raise ValueError(f"Required customer text is missing: {phrase!r}")

    head_rnd_11 = r"\[\s*\]\s*R11\s+\[5 sc, dec\] x 6\s+\(36\)"
    if not re.search(head_rnd_11, all_text):
        raise ValueError("Head Rnd 11 is missing its 42-to-36 decrease instruction")
    body_rnd_11 = r"\[\s*\]\s*R11\s+sc in each st around\s+\(48\)"
    if not re.search(body_rnd_11, all_text):
        raise ValueError("Body Rnd 11 is missing its straight-round instruction")
    expected_boxes = expected_progress_box_count(SOURCE.read_text(encoding="utf-8"))
    if all_text.count("[ ]") < expected_boxes:
        raise ValueError(
            "One or more construction-table progress checkboxes were not rendered"
        )

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
        f"{all_text.count('[ ]')} progress boxes, {text_spans} text spans within page bounds, "
        "selectable text, metadata, "
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
    text_spans = check_pdf_text_bounds(output)
    for number, (page, text) in enumerate(
        zip(reader.pages, page_texts, strict=True), 1
    ):
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
    normalized_text = " ".join(all_text.lower().split())
    required_text = [
        "PRINTER-SAVER EDITION",
        "Every construction-table row begins with a printable [ ] box",
        "50 mm × 50 mm",
        "Round-referenced placement schematic",
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
        "YARN D · RUST (OPTIONAL)",
        "Terms of Use",
        f"© 2026 {BRAND}",
    ]
    for phrase in required_text:
        if phrase.lower() not in normalized_text:
            raise ValueError(f"Required printer-saver text is missing: {phrase!r}")
    expected_boxes = expected_progress_box_count(SOURCE.read_text(encoding="utf-8"))
    if all_text.count("[ ]") < expected_boxes:
        raise ValueError("One or more progress checkboxes were not rendered")
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
        f"{all_text.count('[ ]')} progress boxes, {text_spans} text spans within page bounds, "
        "no raster images, grayscale vectors, "
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
    parser.add_argument(
        "--placement-svg",
        type=Path,
        help="Also export the source-derived vector placement figure as SVG",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    model = compile_ns01_pdf_model(SOURCE)
    if args.placement_svg:
        svg_output = args.placement_svg.resolve()
        export_placement_svg(model, svg_output)
        print(svg_output)
    output = args.output.resolve()
    build_pdf(output, model)
    postflight_pdf(output)
    print(output)
    if not args.skip_printer_saver:
        printer_output = args.printer_output.resolve()
        build_printer_pdf(printer_output, model)
        postflight_printer_pdf(printer_output)
        print(printer_output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
