"""Novality Store PDF editions - colour studio + printer-saver.

Implements the store PDF architecture described in the PDF engineering guide on
top of ReportLab (this checkout has no Chromium/WeasyPrint: no pango, cairo or
gdk-pixbuf libraries are installed, and the playwright browser download host is
not reachable, so the guide's HTML/CSS pipeline is re-expressed as flowables).

What is implemented, in guide order:

  1. Cover page      ribbon (code / edition), title, one-sentence pitch, hero
                     frame with rounded corners, 4-pill spec bar. No copyright.
  2. Front matter    52/48 asymmetric two-column grid: Materials (with yarn
                     swatches) + Abbreviations on the left; Gauge & Size with a
                     true 1:1 50 mm ruler on the right; safety callout below.
  3. Instructions   one card per component. Cards of <=16 table rows are kept
                     together; longer tables break between rows and repeat
                     their header. A narrow (<=10 row) table with trailing prose
                     sits in a 68/32 sidebar so short components cannot leave a
                     half-empty page.
  4. Back matter    numbered assembly steps, symptom->fix grid, care/colorways/
                     terms grids, then one colophon. Copyright appears only in
                     the running footer.
  5. Furniture      running header (code - title, NOVALITY STORE), footer
                     (copyright, Page X of Y), clickable bookmarks for every
                     section and component, tick-box column added at render
                     time so the Markdown masters stay audit-clean.

Usage:
    python3 docs/kit/build_pdf.py                 # all 17 + the collection
    python3 docs/kit/build_pdf.py --codes NS-01 NS-04
    python3 docs/kit/build_pdf.py --grand --only colour
    python3 docs/kit/build_pdf.py --check         # verify the 1:1 ruler maths
"""

from __future__ import annotations

import argparse
import copy
import functools
import importlib.util
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

from reportlab import rl_config

# ReportLab raises LayoutError when a flowable's reported width equals the frame
# width by a float epsilon (Paragraph.wrap returns the wrap width it was given).
# Demoting that to a normal "does not fit" makes the document paginate instead
# of aborting; finish_pdf() still rejects anything genuinely oversized.
rl_config.allowTableBoundsErrors = True

from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import registerFontFamily, stringWidth
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import (BaseDocTemplate, CondPageBreak, Flowable, Frame,
                                KeepTogether, NextPageTemplate, PageBreak,
                                PageTemplate, Paragraph, Spacer, Table, TableStyle)
from reportlab.platypus.flowables import HRFlowable

KIT = Path(__file__).resolve().parent
ROOT = KIT.parents[1]
sys.path.insert(0, str(KIT))

import pdfmd  # noqa: E402
from pdfmd import Block  # noqa: E402

SHOP = ROOT / "shop"

# --- geometry (guide: 16mm / 15mm / 18mm margins on letter portrait) --------

PAGE_W, PAGE_H = LETTER
M_TOP = 16 * mm
M_SIDE = 15 * mm
M_BOT = 18 * mm
CONTENT_W = PAGE_W - 2 * M_SIDE
CONTENT_H = PAGE_H - M_TOP - M_BOT
GUTTER = 8.0
LEFT_W = CONTENT_W * 0.52 - GUTTER / 2
RIGHT_W = CONTENT_W - LEFT_W - GUTTER

# --- fonts: Fraunces/Inter are not installable offline, DejaVu is the stand-in

FONT_SANS = "DJ"
FONT_SANS_B = "DJ-B"
FONT_SERIF = "DS"
FONT_SERIF_B = "DS-B"
FONT_MONO = "DD-M"

_FONT_FILES = {
    FONT_SANS: "DejaVuSans.ttf",
    FONT_SANS_B: "DejaVuSans-Bold.ttf",
    FONT_SERIF: "DejaVuSerif.ttf",
    FONT_SERIF_B: "DejaVuSerif-Bold.ttf",
    FONT_MONO: "DejaVuSansMono.ttf",
}


def register_fonts() -> None:
    base = Path("/usr/share/fonts/truetype/dejavu")
    for name, filename in _FONT_FILES.items():
        path = base / filename
        if not path.exists():
            raise SystemExit(f"missing font {path}")
        pdfmetrics.registerFont(TTFont(name, str(path)))
    registerFontFamily(FONT_SANS, normal=FONT_SANS, bold=FONT_SANS_B,
                       italic=FONT_SANS, boldItalic=FONT_SANS_B)
    registerFontFamily(FONT_SERIF, normal=FONT_SERIF, bold=FONT_SERIF_B,
                       italic=FONT_SERIF, boldItalic=FONT_SERIF_B)


THEMES = {
    "colour": dict(
        page="#FAF7F2", card="#FFFFFF", head="#4A3728", head_text="#FFFFFF",
        alt="#F6F1EA", pause="#FFF4E5", pause_border="#D97706",
        text="#231F1C", muted="#655B53", accent="#8C4A27", soft="#EFE6DC",
        border="#DFD5C8", chip="#4A3728",
    ),
    "print": dict(
        page="#FFFFFF", card="#FFFFFF", head="#F2F2F2", head_text="#111111",
        alt="#FAFAFA", pause="#F5F5F5", pause_border="#111111",
        text="#000000", muted="#333333", accent="#000000", soft="#F0F0F0",
        border="#999999", chip="#111111",
    ),
}

EDITION_LABEL = {"colour": "STUDIO EDITION", "print": "PRINTER-SAVER EDITION"}

# --- yarn-name -> swatch colour (only used when the name states the colour) --

SWATCH = [
    ("ginger", "#B4713A"), ("oat", "#E9DCBF"), ("cream", "#EFE6D2"),
    ("chocolate", "#4B2E2A"), ("brown", "#6B4A2F"), ("tan", "#C8A165"),
    ("black", "#1A1A1A"), ("charcoal", "#3A3A3A"), ("white", "#FFFFFF"),
    ("ivory", "#F5EFE2"), ("grey", "#9A9A9A"), ("gray", "#9A9A9A"),
    ("silver", "#C9CCCE"), ("red", "#B03A2E"), ("berry", "#8E2F45"),
    ("rust", "#8C4A27"), ("orange", "#D97706"), ("gold", "#C9A227"),
    ("yellow", "#E5C07B"), ("mustard", "#C7A03A"), ("green", "#2E6B4F"),
    ("forest", "#2F5D3A"), ("sage", "#A8BFA0"), ("teal", "#2A7B7B"),
    ("blue", "#2F5D8A"), ("navy", "#22355C"), ("denim", "#4A6E8A"),
    ("purple", "#6B4E8E"), ("lavender", "#B7A6D6"), ("pink", "#E4A5B8"),
    ("rose", "#C97B8A"), ("peach", "#E8B396"), ("coral", "#D9736A"),
    ("natural", "#E3D5BE"), ("sand", "#DCCBA8"), ("olive", "#7A7A3A"),
    ("mint", "#A8CDBB"), ("plum", "#5C3A50"), ("lilac", "#C4B0D8"),
]


WEIGHT_NUM = {"lace": "#0", "fingering": "#1", "sport": "#2", "dk": "#3",
              "worsted": "#4", "aran": "#4", "bulky": "#5", "chunky": "#5"}
WEIGHT_NAME = {"light worsted": "Light worsted", "worsted": "Worsted", "dk": "DK",
               "aran": "Aran", "bulky": "Bulky", "chunky": "Chunky", "sport": "Sport",
               "fingering": "Fingering", "lace": "Lace"}


def normalize_weight(phrase: str) -> str:
    """'worsted / aran (#4)' -> 'Worsted #4'; 'DK / light worsted / 8-ply' -> 'DK #3'."""
    low = phrase.lower()
    num_match = re.search(r"#(\d)", phrase)
    num = "#" + num_match.group(1) if num_match else ""
    name = next((k for k in WEIGHT_NAME if k in low), "")
    if not name:
        return re.sub(r"\s+", " ", phrase).strip(" ,;")
    num = num or WEIGHT_NUM.get(name, "")
    return f"{WEIGHT_NAME[name]} {num}".strip()


def clip_text(c: Canvas, text: str, max_w: float, font: str, size: float) -> str:
    if stringWidth(text, font, size) <= max_w:
        return text
    while text and stringWidth(text + "…", font, size) > max_w:
        text = text[:-1]
    return text.rstrip(" ,;·") + "…"


def swatch_for(name: str) -> str | None:
    low = name.lower()
    for word, hexcode in SWATCH:
        if re.search(rf"\b{word}", low):
            return hexcode
    return None


# --- metadata derived from the master --------------------------------------

@dataclass
class Meta:
    code: str
    title: str
    edition: str = "colour"
    intro: str = ""
    skill: str = ""
    hours: str = ""
    size: str = ""
    yarn_hook: str = ""
    terms: str = ""
    design_code: str = ""
    hero: str = ""
    kicker: str = ""
    tags: str = ""
    parts: list[str] = field(default_factory=list)


def _split_quote(text: str) -> list[str]:
    text = pdfmd.plain(text)
    text = re.sub(r"\bDesign Code\s*NS\s*\d+", "", text, flags=re.I)
    parts = [p.strip(" .-") for p in re.split(r"[·•|]|\s+—\s+|\s+-\s+", text)]
    return [p for p in parts if p]


def derive_meta(code: str, blocks: list[Block], spec: dict | None = None) -> Meta:
    spec = spec or {}
    h1 = next((b for b in blocks if b.kind == "h1"), None)
    title = pdfmd.plain(h1.text) if h1 else spec.get("title", code)
    quote = next((b for b in blocks if b.kind == "quote"), None)
    parts = _split_quote(quote.text) if quote else []
    skill = next((p for p in parts if re.search(r"beginner|intermediate|advanced", p, re.I)), "")
    hours = next((p for p in parts if re.search(r"\b(?:hour|hr|min)", p, re.I)), "")
    terms = next((p for p in parts if re.search(r"\bUS\b|\bUK\b|terms", p, re.I)), "")

    intro = ""
    for b in blocks:
        if b.kind == "p" and not b.text.upper().startswith("**FINISHED"):
            intro = pdfmd.plain(b.text)
            break

    size = ""
    for b in blocks:
        if b.kind == "p" and "FINISHED SIZE" in b.text.upper():
            raw = pdfmd.plain(re.sub(r"^\*\*FINISHED SIZE\*\*\s*", "", b.text))
            m = re.match(r"(about\s+)?[^.;]*?(\d+(?:\.\d+)?\s*(?:cm|mm|in)\b\s*(?:\([^)]*\))?)",
                         raw, re.I)
            size = ((m.group(1) or "") + m.group(2)) if m else raw.split(".")[0]
            size = re.sub(r"\s+", " ", size).strip().rstrip(".")
            break

    yarn = ""
    for b in blocks:
        if b.kind != "ul":
            continue
        for item in b.items:
            if re.match(r"\s*\**yarn\b", item, re.I):
                m = re.search(r"((?:light worsted|worsted|dk|aran|bulky|chunky|sport|fingering|"
                              r"lace)[^,;]{0,18}?(?:\(#\d\))?)", item, re.I)
                if m:
                    yarn = normalize_weight(m.group(1))
                    break
        if yarn:
            break

    hook = ""
    for b in blocks:
        if b.kind != "ul":
            continue
        for item in b.items:
            if re.match(r"\s*\**hook\b", item, re.I):
                m = re.search(r"(\d+(?:\.\d+)?\s*mm)\s*(?:\(US\s*([A-Z0-9/-]+)\))?", item)
                if m:
                    hook = m.group(1) + (f" (US {m.group(2)})" if m.group(2) else "")
                    break
        if hook:
            break

    hours = hours.replace(" - ", "–")
    tags = ""
    for b in blocks:
        if b.kind == "p" and "#" in b.text and "Tag" in b.text:
            tags = re.findall(r"#[A-Za-z0-9_]+", b.text)
    return Meta(code=code, title=title, intro=intro, skill=skill, hours=hours, size=size,
                yarn_hook=" · ".join(x for x in (yarn, hook) if x), terms=terms,
                design_code=f"DESIGN CODE {code.replace('-', ' ')}",
                tags=" · ".join(tags))


# --- theme helpers ---------------------------------------------------------

class Styles:
    def __init__(self, theme: dict):
        self.t = theme
        text = HexColor(theme["text"])
        muted = HexColor(theme["muted"])
        accent = HexColor(theme["accent"])
        self.body = ParagraphStyle("Body", fontName=FONT_SANS, fontSize=9.2, leading=12.6,
                                   textColor=text, spaceAfter=4.5, splitLongWords=1,
                                   rightIndent=1)
        self.body_tight = ParagraphStyle("BodyTight", parent=self.body, spaceAfter=2.5,
                                         fontSize=8.8, leading=11.8)
        self.small = ParagraphStyle("Small", parent=self.body, fontSize=8.0, leading=10.6,
                                    textColor=muted, spaceAfter=3)
        self.tiny = ParagraphStyle("Tiny", parent=self.small, fontSize=7.2, leading=9.2)
        self.h2 = ParagraphStyle("H2", fontName=FONT_SERIF_B, fontSize=13, leading=15.5,
                                 textColor=text, spaceBefore=2, spaceAfter=6,
                                 keepWithNext=1, rightIndent=1)
        self.h3 = ParagraphStyle("H3", fontName=FONT_SERIF_B, fontSize=10.6, leading=13,
                                 textColor=accent, spaceBefore=1, spaceAfter=3,
                                 keepWithNext=1)
        self.h4 = ParagraphStyle("H4", fontName=FONT_SANS_B, fontSize=8.8, leading=11.4,
                                 textColor=text, spaceBefore=3, spaceAfter=2,
                                 keepWithNext=1)
        self.th = ParagraphStyle("TH", fontName=FONT_SANS_B, fontSize=7.6, leading=9.4,
                                 textColor=HexColor(theme["head_text"]))
        self.td = ParagraphStyle("TD", fontName=FONT_SANS, fontSize=8.1, leading=10.4,
                                 textColor=text, splitLongWords=1)
        self.td_b = ParagraphStyle("TDB", parent=self.td, fontName=FONT_SANS_B, fontSize=8.2)
        self.td_c = ParagraphStyle("TDC", parent=self.td, alignment=TA_CENTER,
                                   fontName=FONT_SANS_B, fontSize=8.4)
        self.td_c_plain = ParagraphStyle("TDCP", parent=self.td, alignment=TA_CENTER)
        self.tick = ParagraphStyle("Tick", parent=self.td, alignment=TA_CENTER,
                                   fontSize=9.2, leading=11)
        self.title = ParagraphStyle("Title", fontName=FONT_SERIF_B, fontSize=26, leading=30,
                                    textColor=text)
        self.pill_label = ParagraphStyle("PillLabel", fontName=FONT_SANS_B, fontSize=6.4,
                                         leading=8, textColor=muted)
        self.pill_value = ParagraphStyle("PillValue", fontName=FONT_SANS_B, fontSize=8.4,
                                         leading=10.4, textColor=text)
        self.callout = ParagraphStyle("Callout", parent=self.body, fontSize=8.6, leading=11.6)
        self.bullet = ParagraphStyle("Bullet", parent=self.body, leftIndent=10, bulletIndent=1,
                                     spaceAfter=3)
        self.step = ParagraphStyle("Step", parent=self.body, leftIndent=15, bulletIndent=2,
                                   bulletFontName=FONT_SANS_B, bulletFontSize=8.6,
                                   bulletColor=accent, spaceAfter=4, bulletDedent=0)
        self.link = ParagraphStyle("Link", parent=self.small, textColor=accent)


# --- small flowables -------------------------------------------------------

def draw_spaced(canv: Canvas, x: float, y: float, text: str, font: str, size: float,
                space: float = 0.0, align: str = "left") -> None:
    """Draw text with letter spacing (reportlab has no Canvas.setCharSpace)."""
    to = canv.beginText()
    width = stringWidth(text, font, size) + space * max(0, len(text) - 1)
    to.setTextOrigin(x - width if align == "right" else x, y)
    to.setFont(font, size)
    to.setCharSpace(space)
    to.textLine(text)
    to.setCharSpace(0)      # Tc is text state: it would leak into every later string
    canv.drawText(to)


class GaugeRuler(Flowable):
    """A true 1:1 ruler: 50 mm long, drawn from physical points, not pixels."""

    def __init__(self, theme: dict, label: str = "50 mm / 2 in at 100% (actual size)"):
        super().__init__()
        self.length = 50 * mm
        self.height = 20 * mm
        self.theme = theme
        self.label = label
        self.width = CONTENT_W * 0.48

    def wrap(self, aw, ah):
        self.width = min(aw, max(self.length + 6 * mm, aw * 0.46))
        return self.width, self.height

    def draw(self):
        c = self.canv
        ink = HexColor(self.theme["text"])
        muted = HexColor(self.theme["muted"])
        x0, y0 = 0, 4 * mm
        # the measuring bar itself: exactly 50 mm
        c.setStrokeColor(ink)
        c.setLineWidth(1.1)
        c.line(x0, y0, x0 + self.length, y0)
        c.setLineWidth(0.9)
        for step in range(0, 51):
            x = x0 + step * mm
            if step % 10 == 0:
                h = 4.6 * mm
            elif step % 5 == 0:
                h = 3.0 * mm
            else:
                h = 1.8 * mm
            c.setLineWidth(1.1 if step % 10 == 0 else 0.6)
            c.line(x, y0, x, y0 + h)
        for cm in range(0, 6):
            c.setFont(FONT_SANS_B, 5.6)
            c.setFillColor(muted)
            c.drawCentredString(x0 + cm * mm, y0 + 5.4 * mm, str(cm))
        c.setFont(FONT_SANS_B, 6.2)
        c.setFillColor(ink)
        c.drawString(x0, y0 - 3.4 * mm, self.label)
        # 2 in tick, so both units are honest
        two_in = 50.8 * mm
        if x0 + two_in <= x0 + self.length + 3 * mm:
            c.setStrokeColor(muted)
            c.setDash(1.4, 1.4)
            c.setLineWidth(0.7)
            c.line(x0 + two_in, y0, x0 + two_in, y0 + 8 * mm)
            c.setDash()
            c.setFont(FONT_SANS, 5.4)
            c.drawCentredString(x0 + two_in, y0 + 8.4 * mm, "2 in")


class PillBar(Flowable):
    """The four at-a-glance pills under the cover photo."""

    def __init__(self, pills: list[tuple[str, str]], theme: dict, width: float):
        super().__init__()
        self.pills = pills
        self.theme = theme
        self.width = width
        self.height = 16 * mm

    def wrap(self, aw, ah):
        self.width = aw
        return self.width, self.height

    def draw(self):
        c = self.canv
        n = len(self.pills)
        gap = 2.4 * mm
        w = (self.width - gap * (n - 1)) / n
        for i, (label, value) in enumerate(self.pills):
            x = i * (w + gap)
            c.setFillColor(HexColor(self.theme["soft"]))
            c.setStrokeColor(HexColor(self.theme["border"]))
            c.setLineWidth(0.6)
            c.roundRect(x, 0, w, self.height, 2.2 * mm, stroke=1, fill=1)
            c.setFillColor(HexColor(self.theme["muted"]))
            c.setFont(FONT_SANS_B, 5.8)
            c.drawString(x + 2.6 * mm, self.height - 5.4 * mm, label.upper())
            c.setFillColor(HexColor(self.theme["text"]))
            c.setFont(FONT_SANS_B, 7.6)
            lines = _fit(c, value, w - 5.2 * mm, FONT_SANS_B, 7.6, max_lines=2)
            for line_no, line in enumerate(lines):
                c.drawString(x + 2.6 * mm, self.height - 10.2 * mm - line_no * 3.4 * mm,
                             clip_text(c, line, w - 5.2 * mm, FONT_SANS_B, 7.6))


def _fit(c: canvas.Canvas, text: str, max_w: float, font: str, size: float,
         max_lines: int = 2) -> list[str]:
    words = text.split()
    lines: list[str] = []
    cur = ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if stringWidth(trial, font, size) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
            if len(lines) == max_lines:
                break
    if cur and len(lines) < max_lines:
        lines.append(cur)
    if len(lines) == max_lines and " ".join(lines) != text:
        last = lines[-1]
        if stringWidth(last + "…", font, size) <= max_w:
            lines[-1] = last + "…"
    return lines


class Bookmark(Flowable):
    """Zero-size flowable that creates a PDF outline entry on the page it lands.

    Headings inside a component card are nested inside a Table, so the document's
    afterFlowable hook never sees them. Placing this marker at the top of the card
    (inside the same KeepTogether group) keeps every component clickable.
    """

    def __init__(self, text: str, level: int = 1):
        super().__init__()
        self.text = text
        self.level = level
        self.width = self.height = 0
        self._key = f"bm{id(self)}"

    def wrap(self, aw, ah):
        return 0, 0

    def draw(self):
        self.canv.bookmarkPage(self._key)
        self.canv.addOutlineEntry(self.text[:90], self._key, level=self.level, closed=0)


class Badge(Flowable):
    """A numbered circular step badge."""

    def __init__(self, number: int, theme: dict, size: float = 12):
        super().__init__()
        self.number = number
        self.theme = theme
        self.width = self.height = size

    def draw(self):
        c = self.canv
        c.setFillColor(HexColor(self.theme["accent"]))
        c.circle(self.width / 2, self.height / 2, self.width / 2, stroke=0, fill=1)
        c.setFillColor(HexColor("#FFFFFF") if self.theme["accent"] != "#000000"
                       else HexColor("#FFFFFF"))
        c.setFont(FONT_SANS_B, 6.8)
        c.drawCentredString(self.width / 2, self.height / 2 - 2.4, str(self.number))


# --- table rendering -------------------------------------------------------

CHECK_GLYPH = "\u2610"
STITCH_4 = (6, 10, 49, 9, 26)      # check, rnd, instruction, sts, note
STITCH_5 = (5, 8, 31, 31, 8, 17)   # check, rnd, us, uk, sts, note


def _is_box(cell: str) -> bool:
    return bool(re.fullmatch(r"\[?[ xX✓✔☐]?\]?|check", cell.strip(), flags=re.I)) and \
        cell.strip() != ""


def drop_tick_column(header: list[str], rows: list[list[str]]) -> tuple[list[str], list[list[str]]]:
    if not header or not _is_box(header[0]):
        return header, rows
    if not any(r and _is_box(r[0]) for r in rows):
        return header, rows
    return header[1:], [r[1:] for r in rows]


def _auto_widths(header: list[str], rows: list[list[str]], total: float) -> list[float]:
    n = len(header)
    lens = []
    for i in range(n):
        cells = [header[i]] + [r[i] for r in rows if i < len(r)]
        longest = max((len(pdfmd.plain(c)) for c in cells), default=4)
        lens.append(max(4, min(longest, 60)))
    weights = [l ** 0.82 for l in lens]
    scale = total / sum(weights)
    widths = [w * scale for w in weights]
    floor = total * 0.055
    widths = [max(w, floor) for w in widths]
    scale = total / sum(widths)
    return [w * scale for w in widths]


def build_table(block: Block, st: Styles, theme: dict, total_w: float,
                tick: bool) -> Table | None:
    total_w = min(total_w, CONTENT_W - 1)
    header, rows = drop_tick_column(list(block.header), [list(r) for r in block.rows])
    if not header:
        return None
    stitch = pdfmd.table_is_stitch(header)
    kind = pdfmd.stitch_kind(header) if stitch else ""
    n_cols = len(header) + (1 if tick else 0)

    ratios = None
    if stitch:
        candidate = STITCH_5 if kind == "5" else STITCH_4
        if len(candidate) == n_cols:
            ratios = candidate

    if ratios is not None:
        widths = [total_w * r / sum(ratios) for r in ratios]
    elif tick:
        tick_w = total_w * 0.055
        widths = [tick_w] + _auto_widths(header, rows, total_w - tick_w)
    else:
        widths = _auto_widths(header, rows, total_w)
    assert len(widths) == n_cols and abs(sum(widths) - total_w) < 0.5, (header, widths)

    def para(text: str, style) -> Paragraph:
        return Paragraph(pdfmd.inline(text) if text.strip() else "&nbsp;", style)

    data: list[list] = []
    head_cells: list = []
    if tick:
        head_cells.append(Paragraph("✓", st.th))
    head_cells += [Paragraph(pdfmd.inline(h.upper()), st.th) for h in header]
    data.append(head_cells)

    critical_rows: list[int] = []
    for idx, row in enumerate(rows, start=1):
        cells: list = []
        if tick:
            cells.append(Paragraph(CHECK_GLYPH, st.tick))
        for col, cell in enumerate(row):
            label = pdfmd.plain(header[col]).lower()
            if col == 0:
                style = st.td_b
            elif label in ("sts", "st", "count", "stitches"):
                style = st.td_c
            elif re.fullmatch(r"[-\u2013\s]*", cell.strip()):
                style = st.td_c_plain
            else:
                style = st.td
            text = cell.strip()
            inner = pdfmd.inline(text) if text else "&nbsp;"
            if text and pdfmd.critical_row([text]):
                kw = next((k for k in pdfmd.CRITICAL if k in text.lower()), None)
                if kw:
                    pos = text.lower().find(kw)
                    shown, rest = text[:pos + len(kw)], text[pos + len(kw):].strip(" -—,.")
                    inner = f"<b>{pdfmd.inline(shown)}</b>"
                    if rest:
                        inner += f" — {pdfmd.inline(rest)}"
            cells.append(Paragraph(inner, style))
        data.append(cells)
        if pdfmd.critical_row(row):
            critical_rows.append(idx)

    table = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), HexColor(theme["head"])),
        ("TEXTCOLOR", (0, 0), (-1, 0), HexColor(theme["head_text"])),
        ("GRID", (0, 0), (-1, -1), 0.4, HexColor(theme["border"])),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 2.6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.8),
    ]
    for row_no in range(1, len(data)):
        if row_no % 2 == 0:
            cmds.append(("BACKGROUND", (0, row_no), (-1, row_no), HexColor(theme["alt"])))
    for row_no in critical_rows:
        cmds.append(("BACKGROUND", (0, row_no), (-1, row_no), HexColor(theme["pause"])))
        cmds.append(("LINEBEFORE", (0, row_no), (0, row_no), 2.2,
                     HexColor(theme["pause_border"])))
    table.setStyle(TableStyle(cmds))
    return table


def measure(flowables: list, width: float) -> float:
    total = 0.0
    for fl in flowables:
        try:
            _, h = fl.wrap(width, 10 ** 6)
        except Exception:
            h = 0
        total += h + getattr(fl, "getSpaceBefore", lambda: 0)() + \
            getattr(fl, "getSpaceAfter", lambda: 0)()
    return total


# --- document -------------------------------------------------------------

class StoreDoc(BaseDocTemplate):
    def __init__(self, filename: str, meta: Meta, theme: dict, cover: callable, **kw):
        self.meta = meta
        self.theme = theme
        self.cover = cover
        super().__init__(filename, pagesize=LETTER,
                         leftMargin=M_SIDE, rightMargin=M_SIDE,
                         topMargin=M_TOP, bottomMargin=M_BOT,
                         title=f"{meta.title} — {meta.code}",
                         author="Novality Store",
                         subject=f"{meta.code} crochet pattern · {EDITION_LABEL[meta.edition]}",
                         creator="Novality Store build_pdf.py",
                         **kw)
        # the frame is 2 pt narrower than the design width so a flowable wrapped
        # to exactly CONTENT_W can never trip ReportLab's float compare
        body = Frame(M_SIDE, M_BOT, CONTENT_W - 2, CONTENT_H, id="body",
                     leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        cover_frame = Frame(M_SIDE, M_BOT, CONTENT_W, CONTENT_H, id="cover",
                            leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates([
            PageTemplate(id="cover", frames=[cover_frame], onPage=self._cover_page),
            PageTemplate(id="body", frames=[body], onPage=self._decorate),
        ])
        self._bm = 0

    # -- furniture
    def _cover_page(self, canv, doc):
        self.cover(canv, doc)

    def _decorate(self, canv, doc):
        meta, theme = self.meta, self.theme
        canv.saveState()
        ink = HexColor(theme["muted"])
        canv.setFillColor(ink)
        canv.setFont(FONT_SANS_B, 6.9)
        left = f"{meta.code} · {meta.title}".upper()
        draw_spaced(canv, M_SIDE, PAGE_H - M_TOP + 7 * mm, left, FONT_SANS_B, 6.9, 0.0)
        draw_spaced(canv, PAGE_W - M_SIDE, PAGE_H - M_TOP + 7 * mm, "NOVALITY STORE",
                    FONT_SANS_B, 6.9, 0.0, align="right")
        canv.setStrokeColor(HexColor(theme["border"]))
        canv.setLineWidth(0.5)
        canv.line(M_SIDE, PAGE_H - M_TOP + 4.6 * mm, PAGE_W - M_SIDE, PAGE_H - M_TOP + 4.6 * mm)
        canv.restoreState()

    def afterFlowable(self, flowable):
        """Only top-level `## ` headings; cards register their own, see Bookmark."""
        if isinstance(flowable, Paragraph) and flowable.style.name in ("H2", "PartTitle"):
            self._bm += 1
            key = f"sec{self._bm}"
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(flowable.getPlainText()[:90], key, level=0, closed=0)


class FooterCanvas(Canvas):
    """Running footer: copyright (once) on the left, Page X of Y on the right.

    The page total is known before this pass starts (the document is laid out
    twice), which keeps the PDF outline and every page object exactly where
    ReportLab put them - a deferred-showPage trick would break both.
    """

    def __init__(self, *args, theme: dict, meta: Meta, total: int, **kw):
        self._theme = theme
        self._meta = meta
        self._total = total
        self._page = 0
        super().__init__(*args, **kw)

    def showPage(self):
        self._page += 1
        if self._page > 1:                      # page 1 is the cover
            self._footer(self._page, self._total)
        super().showPage()

    def _footer(self, page: int, total: int):
        theme = self._theme
        self.saveState()
        y = M_BOT - 8 * mm
        self.setStrokeColor(HexColor(theme["border"]))
        self.setLineWidth(0.5)
        self.line(M_SIDE, y + 4.2 * mm, PAGE_W - M_SIDE, y + 4.2 * mm)
        self.setFillColor(HexColor(theme["muted"]))
        self.setFont(FONT_SANS, 6.6)
        self.drawString(M_SIDE, y,
                        "© 2026 Novality Store · Personal & small-batch handmade license")
        self.setFont(FONT_SANS_B, 7.2)
        self.setFillColor(HexColor(theme["text"]))
        self.drawRightString(PAGE_W - M_SIDE, y, f"Page {page} of {total}")
        self.restoreState()


def finish_pdf(out: Path, meta: Meta, theme: dict, cover, story: list) -> int:
    """Lay the story out twice: once to count pages, once to write the file."""
    import io

    # pre-flight: nothing may be wider than the frame, and nothing taller than
    # a page (a single-row table cannot split, so an oversized one is fatal)
    for i, fl in enumerate(story):
        try:
            w, h = fl.wrap(CONTENT_W, CONTENT_H)
        except Exception:
            continue
        if w > CONTENT_W + 0.05:
            raise SystemExit(f"story[{i}] {type(fl).__name__} is {w:.1f} pt wide "
                             f"(frame {CONTENT_W:.1f}) cols="
                             f"{getattr(fl, '_colWidths', None)} text="
                             f"{str(getattr(fl, '_cellvalues', ''))[:120]}")
        if h > CONTENT_H:
            raise SystemExit(f"story[{i}] {type(fl).__name__} is {h:.1f} pt tall "
                             f"(frame {CONTENT_H:.1f})")

    def clear_postponed(items) -> None:
        """ReportLab marks a flowable `_postponed` when it moves to the next page.

        The same story is laid out twice (count, then write), so a flag left over
        from the first pass aborts the second.
        """
        for fl in items:
            if hasattr(fl, "_postponed"):
                try:
                    del fl._postponed
                except AttributeError:
                    pass
            inner = getattr(fl, "_content", None)
            if isinstance(inner, (list, tuple)):
                clear_postponed(inner)
            cells = getattr(fl, "_cellvalues", None)
            if isinstance(cells, (list, tuple)):
                for row in cells:
                    if isinstance(row, (list, tuple)):
                        clear_postponed([c for c in row if not isinstance(c, str)])

    # the count pass runs on a deep copy: laying out the real story once leaves
    # postponed/keep-together state behind, and a second pass on the same objects
    # can paginate differently from the first - which shows up as "Page 9 of 10".
    total = 0
    for _attempt in range(3):
        try:
            probe_story = copy.deepcopy(story)
        except Exception:
            probe_story = story
            clear_postponed(probe_story)
        probe = StoreDoc(io.BytesIO(), meta, theme, cover)
        probe.build(list(probe_story))
        if probe.page == total:
            break
        total = probe.page

    clear_postponed(story)
    doc = StoreDoc(str(out), meta, theme, cover)
    doc.build(list(story),
              canvasmaker=functools.partial(FooterCanvas, theme=theme, meta=meta, total=total))
    if doc.page != total:
        raise SystemExit(f"page count drifted: count pass {total}, write pass {doc.page}")
    return total


# --- cover ---------------------------------------------------------------

def draw_strip(canv: Canvas, cards: list, theme: dict, top: float, bottom: float) -> None:
    """Three compact at-a-glance cards under the pill bar."""
    if not cards:
        return
    n = min(len(cards), 3)
    gap = 3 * mm
    w = (CONTENT_W - gap * (n - 1)) / n
    rows = max(len(c[1]) for c in cards[:n])
    h = min(top - bottom, 10 * mm + rows * 3.4 * mm + 3 * mm)
    for i, card in enumerate(cards[:n]):
        title, bullets = card[0], card[1]
        x = M_SIDE + i * (w + gap)
        canv.setFillColor(HexColor(theme["card"]))
        canv.setStrokeColor(HexColor(theme["border"]))
        canv.setLineWidth(0.6)
        canv.roundRect(x, top - h, w, h, 2.2 * mm, stroke=1, fill=1)
        canv.setFillColor(HexColor(theme["accent"]))
        canv.setFont(FONT_SANS_B, 6.2)
        canv.drawString(x + 3 * mm, top - 5.6 * mm, title.upper()[:30])
        canv.setFillColor(HexColor(theme["muted"]))
        y = top - 10.4 * mm
        for bullet in bullets[:3]:
            for line in _fit(canv, f"· {bullet}", w - 6 * mm, FONT_SANS, 6.6, max_lines=2):
                canv.setFont(FONT_SANS, 6.6)
                canv.drawString(x + 3 * mm, y, clip_text(canv, line, w - 6 * mm, FONT_SANS, 6.6))
                y -= 3.1 * mm
            if y < top - h + 2 * mm:
                break
    return top - h


def draw_palette(canv: Canvas, items: list[tuple[str, str]], theme: dict, top: float) -> float:
    """The yarn palette as labelled swatches - fills the foot of the cover."""
    if not items:
        return top
    items = items[:6]
    gap = 3 * mm
    w = (CONTENT_W - gap * (len(items) - 1)) / len(items)
    h = 17 * mm
    y0 = top - h
    for i, (name, hexcode) in enumerate(items):
        x = M_SIDE + i * (w + gap)
        canv.setFillColor(HexColor(theme["card"]))
        canv.setStrokeColor(HexColor(theme["border"]))
        canv.setLineWidth(0.5)
        canv.roundRect(x, y0, w, h, 2 * mm, stroke=1, fill=1)
        canv.setFillColor(HexColor(hexcode or theme["border"]))
        canv.setStrokeColor(HexColor(theme["page"]))
        canv.setLineWidth(1.0)
        canv.circle(x + w / 2, y0 + h - 5.6 * mm, 3.2 * mm, stroke=1, fill=1)
        canv.setFillColor(HexColor(theme["text"]))
        canv.setFont(FONT_SANS, 6.6)
        for n, line in enumerate(_fit(canv, name, w - 3 * mm, FONT_SANS, 6.6, max_lines=2)):
            canv.drawCentredString(x + w / 2, y0 + 4.6 * mm - n * 3.1 * mm, line)
    canv.setFillColor(HexColor(theme["muted"]))
    canv.setFont(FONT_SANS_B, 6.2)
    draw_spaced(canv, M_SIDE, y0 + h + 2.2 * mm, "YARN PALETTE", FONT_SANS_B, 6.2, 0.6)
    return y0


def default_cards(edition: str, n_parts: int) -> list:
    """Reader-facing cover cards. Nothing about how the file was checked."""
    parts = f"{n_parts} components" if n_parts else "Numbered components"
    if edition == "print":
        return [
            ("What you get", [parts, "A stitch table for every round",
                              "Finishing and troubleshooting"]),
            ("Print settings", ["US Letter or A4 at 100%", "White background, ink-saver",
                                "Tick box for every round"]),
            ("Also inside", ["1:1 gauge ruler", "Project record sheet",
                             "Care and licensing terms"]),
        ]
    return [
        ("What you get", [parts, "A stitch table for every round",
                          "Finishing and troubleshooting"]),
        ("How to use it", ["Print at 100% for a true-size gauge",
                           "Tick each round as you finish it",
                           "Check gauge before round 1"]),
        ("Also inside", ["1:1 gauge ruler", "Project record sheet",
                         "Care and licensing terms"]),
    ]


def cover_palette(blocks: list[Block]) -> list[tuple[str, str]]:
    """Colour names from the colorways section, with a swatch colour where known."""
    for i, b in enumerate(blocks):
        if b.kind == "h2" and section_key(b.text) == "colorways":
            names: list[str] = []
            for c in blocks[i + 1:i + 4]:
                if c.kind in ("p", "ul"):
                    raw = c.text if c.kind == "p" else " · ".join(c.items)
                    names.extend(x.strip(" .") for x in re.split(r"[·•,]", raw) if x.strip(" ."))
                elif c.kind == "h2":
                    break
            out = []
            for name in names[:6]:
                if len(name) < 28:
                    out.append((name, swatch_for(name) or ""))
            return out
    return []


def draw_contents(canv: Canvas, items: list[str], theme: dict, base: float,
                  ceiling: float) -> float:
    """Contents list in two columns, sitting on `base`; skipped if it hits `ceiling`."""
    if not items:
        return base
    rows = (len(items) + 1) // 2
    col_w = (CONTENT_W - 8 * mm) / 2
    h = rows * 4.6 * mm + 13 * mm
    top = base + h
    if top > ceiling:
        return base
    canv.setFillColor(HexColor(theme["card"]))
    canv.setStrokeColor(HexColor(theme["border"]))
    canv.setLineWidth(0.6)
    canv.roundRect(M_SIDE, top - h, CONTENT_W, h, 2.4 * mm, stroke=1, fill=1)
    canv.setFillColor(HexColor(theme["accent"]))
    draw_spaced(canv, M_SIDE + 6 * mm, top - 7.4 * mm, "INSIDE THIS PATTERN",
                FONT_SANS_B, 6.6, 0.6)
    canv.setFillColor(HexColor(theme["text"]))
    for i, title in enumerate(items[:2 * rows]):
        col, row = divmod(i, rows)
        x = M_SIDE + 6 * mm + col * (col_w + 2 * mm)
        yy = top - 12.6 * mm - row * 4.6 * mm
        canv.setFont(FONT_SANS, 7.0)
        canv.drawString(x, yy, clip_text(canv, pdfmd.plain(title),
                                         col_w - 4 * mm, FONT_SANS, 7.0))
    return top - h


def draw_scale_check(canv: Canvas, theme: dict, top: float) -> float:
    """A true 50 mm bar plus the one instruction a printer needs: print at 100%."""
    h = 26 * mm
    canv.setFillColor(HexColor(theme["soft"]))
    canv.setStrokeColor(HexColor(theme["border"]))
    canv.setLineWidth(0.6)
    canv.roundRect(M_SIDE, top - h, CONTENT_W, h, 2.4 * mm, stroke=1, fill=1)
    canv.setFillColor(HexColor(theme["accent"]))
    draw_spaced(canv, M_SIDE + 6 * mm, top - 7 * mm, "CHECK YOUR PRINT SCALE",
                FONT_SANS_B, 6.6, 0.6)
    canv.setFillColor(HexColor(theme["text"]))
    canv.setFont(FONT_SANS, 7.4)
    canv.drawString(M_SIDE + 6 * mm, top - 12.4 * mm,
                    "Print the interior at 100% (actual size, not fit to page). "
                    "This bar must measure 50 mm / 2 in.")
    x = M_SIDE + 6 * mm
    y = top - 19 * mm
    canv.setStrokeColor(HexColor(theme["text"]))
    canv.setLineWidth(0.8)
    canv.line(x, y, x + 50 * mm, y)
    canv.setLineWidth(0.5)
    for i in range(11):
        tick = y + (3.2 * mm if i % 5 == 0 else 2.0 * mm)
        canv.line(x + i * 5 * mm, y, x + i * 5 * mm, tick)
    canv.setFont(FONT_SANS, 6.0)
    canv.drawString(x + 50 * mm + 3 * mm, y, "50 mm")
    return top - h


def make_cover(meta: Meta, theme: dict, hero: str | None, note: str = "",
               cards: list | None = None,
               palette: list[tuple[str, str]] | None = None,
               contents: list[str] | None = None) -> callable:
    cards = cards or []
    palette = palette or []
    contents = contents or []

    def draw(canv: Canvas, doc):
        canv.saveState()
        canv.setFillColor(HexColor(theme["page"]))
        canv.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
        top = PAGE_H - M_TOP

        # ribbon
        canv.setFillColor(HexColor(theme["muted"]))
        draw_spaced(canv, M_SIDE, top - 2 * mm,
                    f"NOVALITY STORE  ·  {EDITION_LABEL[meta.edition]}  ·  {meta.design_code}",
                    FONT_SANS_B, 7.0, 0.4)
        canv.setStrokeColor(HexColor(theme["accent"]))
        canv.setLineWidth(0.9)
        canv.line(M_SIDE, top - 5.6 * mm, PAGE_W - M_SIDE, top - 5.6 * mm)

        # title
        y = top - 16 * mm
        size = 25.0
        lines = _fit(canv, meta.title, CONTENT_W, FONT_SERIF_B, size, max_lines=3)
        canv.setFillColor(HexColor(theme["text"]))
        canv.setFont(FONT_SERIF_B, size)
        for line in lines:
            canv.drawString(M_SIDE, y, line)
            y -= size * 1.12
        y -= 2.6 * mm

        # one-sentence pitch
        if meta.intro:
            canv.setFillColor(HexColor(theme["muted"]))
            canv.setFont(FONT_SANS, 9.6)
            padded = ParagraphStyle("pitch", fontName=FONT_SANS, fontSize=9.6, leading=13.2,
                                    textColor=HexColor(theme["muted"]))
            p = Paragraph(pdfmd.inline(meta.intro), padded)
            w, h = p.wrap(CONTENT_W * 0.86, 40 * mm)
            p.drawOn(canv, M_SIDE, y - h)
            y -= h + 6 * mm

        # hero frame (colour edition only; the print edition carries no photo)
        pills_h = 16 * mm
        floor = M_BOT + 30 * mm          # lowest the art may reach
        bottom_of_art = y
        if hero and meta.edition == "colour":
            from reportlab.lib.utils import ImageReader
            frame_top = y
            try:
                iw, ih = ImageReader(hero).getSize()
                aspect = (iw / ih) if ih else 4 / 3
            except Exception:
                aspect = 4 / 3
            frame_h = max(52 * mm, frame_top - floor)
            frame_w = frame_h * aspect
            if frame_w > CONTENT_W:
                frame_w = CONTENT_W
                frame_h = frame_w / aspect
            x = M_SIDE + (CONTENT_W - frame_w) / 2
            y_img = frame_top - frame_h
            path = Path(hero)
            p = canv.beginPath()
            p.roundRect(x, y_img, frame_w, frame_h, 3 * mm)
            canv.saveState()
            canv.clipPath(p, stroke=0, fill=0)
            try:
                canv.drawImage(str(path), x, y_img, frame_w, frame_h, mask="auto",
                               preserveAspectRatio=True, anchor="c")
            except Exception:
                canv.setFillColor(HexColor(theme["soft"]))
                canv.rect(x, y_img, frame_w, frame_h, stroke=0, fill=1)
            canv.restoreState()
            canv.setStrokeColor(HexColor(theme["border"]))
            canv.setLineWidth(0.7)
            canv.roundRect(x, y_img, frame_w, frame_h, 3 * mm, stroke=1, fill=0)
            canv.setFillColor(HexColor(theme["muted"]))
            canv.setFont(FONT_SANS, 6.2)
            canv.drawString(x, y_img - 3.6 * mm,
                            "Illustrative render of the written design — AI-assisted artwork, "
                            "not a photograph of a finished sample.")
            bottom_of_art = y_img - 4.5 * mm
        elif note:
            inner_w = CONTENT_W - 12 * mm
            style = ParagraphStyle("note", fontName=FONT_SANS, fontSize=8.8, leading=12,
                                   textColor=HexColor(theme["text"]))
            para = Paragraph(pdfmd.inline(note), style)
            _, h = para.wrap(inner_w, 10 ** 5)
            box_h = h + 16 * mm
            canv.setFillColor(HexColor(theme["card"]))
            canv.setStrokeColor(HexColor(theme["border"]))
            canv.setLineWidth(0.7)
            canv.roundRect(M_SIDE, y - box_h, CONTENT_W, box_h, 3 * mm, stroke=1, fill=1)
            canv.setFillColor(HexColor(theme["accent"]))
            draw_spaced(canv, M_SIDE + 6 * mm, y - 8 * mm, "HOW IT IS BUILT",
                        FONT_SANS_B, 7.0, 0.6)
            para.drawOn(canv, M_SIDE + 6 * mm, y - box_h + 6 * mm)
            bottom_of_art = y - box_h - 3 * mm

        # four pills, directly under the photo (no dead band above them)
        pills = [
            ("Skill level", meta.skill or "—"),
            ("Active time", meta.hours or "—"),
            ("Finished size", meta.size or "—"),
            ("Yarn & hook", meta.yarn_hook or "—"),
        ]
        pills_y = bottom_of_art - 3 * mm - pills_h
        bar = PillBar(pills, theme, CONTENT_W)
        bar.canv = canv
        canv.saveState()
        canv.translate(M_SIDE, pills_y)
        bar.draw()
        canv.restoreState()

        # edition + terms line
        canv.setFillColor(HexColor(theme["muted"]))
        canv.setFont(FONT_SANS, 6.6)
        canv.drawCentredString(PAGE_W / 2, M_BOT + 2 * mm,
                               f"{meta.terms or 'US crochet terms'}  ·  "
                               f"{EDITION_LABEL[meta.edition].title()}")

        # what-is-inside strip, so the lower third is not blank
        strip_top = pills_y - 5 * mm
        strip_bottom = M_BOT + 8 * mm
        if strip_top - strip_bottom >= 30 * mm and cards:
            cards_bottom = draw_strip(canv, cards, theme, strip_top, strip_bottom)
            if palette and cards_bottom - strip_bottom >= 26 * mm:
                draw_palette(canv, palette, theme, cards_bottom - 6 * mm)
            elif contents and cards_bottom - strip_bottom >= 40 * mm:
                scale_bottom = draw_scale_check(canv, theme, cards_bottom - 8 * mm)
                draw_contents(canv, contents, theme,
                              strip_bottom + 6 * mm, scale_bottom - 6 * mm)
        canv.restoreState()
    return draw


# --- block -> flowables ---------------------------------------------------

SPECIAL_SECTIONS = {
    "materials": "materials",
    "gauge & size": "gauge",
    "gauge and size": "gauge",
    "abbreviations": "abbrev",
    "techniques": "techniques",
    "instructions": "instructions",
    "finishing & assembly": "finishing",
    "finishing and assembly": "finishing",
    "troubleshooting": "trouble",
    "terms of use": "terms",
    "care": "care",
    "colorways": "colorways",
    "colourways": "colorways",
    "designer notes": "notes",
    "notes": "notes",
    "safety": "safety",
    "happy crocheting!": "closing",
}


def section_key(text: str) -> str | None:
    low = pdfmd.plain(text).lower()
    for prefix, key in SPECIAL_SECTIONS.items():
        if low.startswith(prefix):
            return key
    return None


class Renderer:
    def __init__(self, meta: Meta, theme: dict, styles: Styles):
        self.meta = meta
        self.theme = theme
        self.st = styles
        self.flow: list = []
        self._card_title = ""

    # -- pieces
    def heading(self, level: int, text: str):
        style = {2: self.st.h2, 3: self.st.h3, 4: self.st.h4}[level]
        if level >= 3:
            self.flow.append(Bookmark(pdfmd.plain(text), level=1))
        self.flow.append(Paragraph(pdfmd.inline(text), style))

    def paragraphs(self, text: str, style=None):
        self.flow.append(Paragraph(pdfmd.inline(text), style or self.st.body))

    def bullets(self, items: list[str]):
        for item in items:
            self.flow.append(Paragraph(pdfmd.inline(item), self.st.bullet,
                                       bulletText="•"))

    def numbered(self, items: list[str], offset: int = 1) -> int:
        """Numbered steps; returns the next offset so several lists share a run."""
        n = offset - 1
        for item in items:
            n += 1
            self.flow.append(Paragraph(pdfmd.inline(item), self.st.step,
                                       bulletText=str(n)))
        return n + 1

    def callout(self, title: str, body: str):
        inner = [Paragraph(title.upper(), self.st.h4), Paragraph(pdfmd.inline(body),
                                                                 self.st.callout)]
        box = Table([[inner]], colWidths=[CONTENT_W])
        box.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), HexColor(self.theme["pause"])),
            ("LINEBEFORE", (0, 0), (0, 0), 3, HexColor(self.theme["pause_border"])),
            ("BOX", (0, 0), (-1, -1), 0.5, HexColor(self.theme["border"])),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))
        self.flow.append(box)
        self.flow.append(Spacer(1, 4))

    def card_box(self, inner: list, sidebar: tuple[list, list] | None = None) -> Table:
        pad = 7
        width = CONTENT_W - 2 * pad
        body: list
        if sidebar:
            left, right = sidebar
            left_w = width * 0.68 - 6
            right_w = width * 0.32
            body = [Table([[left, right]], colWidths=[left_w, 6, right_w],
                          style=TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                                            ("LEFTPADDING", (0, 0), (-1, -1), 0),
                                            ("RIGHTPADDING", (0, 0), (-1, -1), 0)]))]
        else:
            body = inner
        box = Table([[body]], colWidths=[CONTENT_W])
        box.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), HexColor(self.theme["card"])),
            ("BOX", (0, 0), (-1, -1), 0.6, HexColor(self.theme["border"])),
            ("LEFTPADDING", (0, 0), (-1, -1), pad),
            ("RIGHTPADDING", (0, 0), (-1, -1), pad),
            ("TOPPADDING", (0, 0), (-1, -1), pad - 1),
            ("BOTTOMPADDING", (0, 0), (-1, -1), pad),
        ]))
        return box

    def card(self, inner: list, keep: bool, sidebar: tuple[list, list] | None = None,
             fallback: list | None = None, prefix: list | None = None):
        """Emit a component card, falling back to an unboxed run when it cannot fit.

        A single-cell card cannot split, so a component taller than half a page
        must flow: its table then breaks between rows and repeats its header on
        every page (the >16-row branch of the guide's rule). `prefix` flowables
        (the `## Instructions` heading, say) travel with the card so a heading is
        never left alone at the foot of a page.
        """
        box = self.card_box(inner, sidebar)
        height = measure([box], CONTENT_W)
        pre = list(prefix or []) + [Bookmark(self._card_title or "", level=1)]
        if height > CONTENT_H * 0.55:
            self.flow.extend(pre)
            self.flow.append(CondPageBreak(56))
            for fl in (fallback if fallback is not None else inner):
                self.flow.append(fl)
            self.flow.append(Spacer(1, 8))
            return
        group = pre + [box]
        if keep or height > CONTENT_H * 0.25:
            self.flow.append(KeepTogether(group))
        else:
            self.flow.extend(group)
        self.flow.append(Spacer(1, 6))

    def two_column(self, left: list, right: list, avail_h: float | None = None,
                   split: float = 0.52, gap: float = 8) -> bool:
        left_w = CONTENT_W * split - gap / 2
        right_w = CONTENT_W - left_w - gap
        need = max(measure(left, left_w), measure(right, right_w))
        limit = CONTENT_H * 0.86 if avail_h is None else min(avail_h, CONTENT_H * 0.86)
        if need > limit:
            return False
        table = Table([[left, right]], colWidths=[left_w, right_w], hAlign="LEFT")
        table.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (0, 0), 0),
            ("RIGHTPADDING", (0, 0), (0, 0), gap),
            ("LEFTPADDING", (1, 0), (1, 0), 0),
            ("RIGHTPADDING", (1, 0), (1, 0), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ]))
        self.flow.append(table)
        return True

    # -- custom sections
    def materials_table(self, items: list[str], width: float) -> list:
        rows = []
        for item in items:
            text = item.strip()
            if ":" in text[:60]:
                head, rest = text.split(":", 1)
            elif " - " in text[:60]:
                head, rest = text.split(" - ", 1)
            else:
                head, rest = text, ""
            head = head.strip()
            rest = rest.strip()
            hexcode = swatch_for(head) if head.lower().startswith(("yarn", "colour", "color")) else None
            dot = ""
            if hexcode:
                dot = (f'<font name="{FONT_SANS}" color="{hexcode}">●</font>&nbsp; ')
            elif head.lower().startswith("yarn"):
                dot = (f'<font name="{FONT_SANS}" color="{self.theme["border"]}">○</font>&nbsp; ')
            label = f"{dot}<b>{pdfmd.inline(head)}</b>"
            rows.append([Paragraph(label, self.st.td), Paragraph(pdfmd.inline(rest) or "&nbsp;",
                                                                 self.st.td)])
        table = Table(rows, colWidths=[width * 0.40, width * 0.60])
        table.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("GRID", (0, 0), (-1, -1), 0.35, HexColor(self.theme["border"])),
            ("BACKGROUND", (0, 0), (0, -1), HexColor(self.theme["alt"])),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING", (0, 0), (-1, -1), 2.4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2.6),
        ]))
        return [table]

    def abbreviations_table(self, paragraphs: list[str], width: float) -> list:
        pairs: list[tuple[str, str]] = []
        notes: list[str] = []
        for text in paragraphs:
            for chunk in re.split(r"[·•]", text):
                chunk = chunk.strip(" .")
                if not chunk:
                    continue
                if " - " in chunk:
                    a, b = chunk.split(" - ", 1)
                    pairs.append((a.strip(), b.strip()))
                elif len(chunk.split()) > 4 or not re.fullmatch(r"[A-Za-z()/' ]{1,12}", chunk):
                    notes.append(chunk)          # a sentence, not an abbreviation
                else:
                    pairs.append((chunk, ""))
        if not pairs:
            return []
        rows = []
        half = (len(pairs) + 1) // 2
        for i in range(half):
            left = pairs[i]
            right = pairs[i + half] if i + half < len(pairs) else ("", "")
            cells = []
            for abbr, meaning in (left, right):
                if not abbr:
                    cells.append(Paragraph("&nbsp;", self.st.td))
                    continue
                cells.append(Paragraph(
                    f"<b>{pdfmd.inline(abbr)}</b>" + (f" — {pdfmd.inline(meaning)}" if meaning else ""),
                    self.st.td))
            rows.append(cells)
        widths = [(width - 4) / 2] * 2
        table = Table(rows, colWidths=widths)
        table.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LINEBELOW", (0, 0), (-1, -2), 0.3, HexColor(self.theme["border"])),
            ("LEFTPADDING", (0, 0), (-1, -1), 2),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2.4),
        ]))
        out: list = [table]
        for note in notes:
            out.append(Spacer(1, 3))
            out.append(Paragraph(pdfmd.inline(note), self.st.tiny))
        return out

    def inside_panel(self, titles: list[str], width: float) -> list:
        """What is in the pattern, from the component headings themselves."""
        if not titles:
            return []
        inner = [Paragraph("Inside this pattern", self.st.h4)]
        for title in titles:
            inner.append(Paragraph(f"· {pdfmd.inline(title)}", self.st.tiny))
        box = Table([[inner]], colWidths=[width])
        box.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), HexColor(self.theme["card"])),
            ("BOX", (0, 0), (-1, -1), 0.5, HexColor(self.theme["border"])),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]))
        return [Spacer(1, 4), box]

    def gauge_panel(self, gauge_paras: list[str], width: float = RIGHT_W) -> list:
        inner = []
        for text in gauge_paras:
            inner.append(Paragraph(pdfmd.inline(text), self.st.body_tight))
        inner.append(Spacer(1, 3))
        inner.append(GaugeRuler(self.theme))
        inner.append(Paragraph("Print at 100% / Actual Size: the bar above must measure "
                               "5 cm (2 in).", self.st.tiny))
        box = Table([[inner]], colWidths=[width])
        box.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), HexColor(self.theme["alt"])),
            ("BOX", (0, 0), (-1, -1), 0.5, HexColor(self.theme["border"])),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))
        return [box]

    def trouble_grid(self, items: list[str]) -> list:
        rows = []
        for item in items:
            m = re.match(r"\*\*(.+?)\*\*\s*(.*)", item, flags=re.S)
            if m:
                symptom, fix = m.group(1).strip(), m.group(2).strip(" .")
            else:
                symptom, fix = "", item
            rows.append([Paragraph(pdfmd.inline(symptom), self.st.td_b),
                         Paragraph(pdfmd.inline(fix), self.st.td)])
        table = Table(rows, colWidths=[CONTENT_W * 0.30, CONTENT_W * 0.70 - 2])
        table.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("GRID", (0, 0), (-1, -1), 0.35, HexColor(self.theme["border"])),
            ("BACKGROUND", (0, 0), (0, -1), HexColor(self.theme["alt"])),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING", (0, 0), (-1, -1), 2.6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2.8),
        ]))
        return [table]

    def colophon(self, terms_blocks: list[Block]):
        """Licence terms once each, without repeating the copyright line."""
        sections: list[tuple[str, list[str]]] = []
        for b in terms_blocks:
            if b.kind == "h3":
                sections.append((pdfmd.plain(b.text), []))
            elif b.kind == "p" and not b.text.strip().startswith("©"):
                if sections:
                    sections[-1][1].append(b.text)
                else:
                    sections.append(("", [b.text]))

        def para(text: str) -> Paragraph:
            return Paragraph(pdfmd.inline(text), self.st.tiny)

        paired = {"you may", "you may not", "you can", "you cannot"}
        done: set[int] = set()
        rows: list = []
        i = 0
        while i < len(sections):
            title, texts = sections[i]
            if i in done or not texts:
                i += 1
                continue
            low = title.lower().strip()
            partner = None
            if low in paired:
                for j, (other, other_texts) in enumerate(sections):
                    if j != i and j not in done and other_texts and \
                            other.lower().strip() in paired and other.lower() != low:
                        partner = j
                        break
            if partner is not None:
                other, other_texts = sections[partner]
                cell_a = [Paragraph(title.upper(), self.st.h4)] + [para(x) for x in texts]
                cell_b = [Paragraph(other.upper(), self.st.h4)] + \
                    [para(x) for x in other_texts]
                rows.append([cell_a, cell_b])
                done.update({i, partner})
            else:
                rows.append([([Paragraph(title.upper(), self.st.h4)] if title else []) +
                             [para(x) for x in texts]])
            i += 1

        if not rows:
            return
        widths = [CONTENT_W * 0.49, CONTENT_W * 0.51] if any(len(r) == 2 for r in rows) \
            else [CONTENT_W]
        data = []
        spans = []
        for row in rows:
            if len(row) == 1 and len(widths) == 2:
                spans.append(("SPAN", (0, len(data)), (-1, len(data))))
                data.append([row[0], ""])
            else:
                data.append(row)
        table = Table(data, colWidths=widths)
        table.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LINEBELOW", (0, 0), (-1, -2), 0.3, HexColor(self.theme["border"])),
        ] + spans))
        self.flow.append(table)

    def project_record(self, checks: list[str] | None = None, tags: str = ""):
        """A printable workbook page: the record, the finishing log, the pre-sew checks."""
        self.flow.append(CondPageBreak(CONTENT_H * 0.92))   # own page, never a tail
        self.flow.append(Paragraph("Your project record", self.st.h2))
        self.flow.append(Paragraph(
            "Print or photocopy one per make. Measuring your own piece is the only way to "
            "know whether your yarn and tension landed on the stated size.", self.st.tiny))
        self.flow.append(Spacer(1, 5))

        def grid(rows: list[str], height: float, label_share: float = 0.34):
            data = [[Paragraph(label, self.st.td), Paragraph("", self.st.td)]
                    for label in rows]
            label_w = CONTENT_W * label_share
            table = Table(data, colWidths=[label_w, CONTENT_W - label_w - 1],
                          rowHeights=[height] * len(rows))
            table.setStyle(TableStyle([
                ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
                ("GRID", (0, 0), (-1, -1), 0.45, HexColor(self.theme["border"])),
                ("BACKGROUND", (0, 0), (0, -1), HexColor(self.theme["alt"])),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]))
            return table

        self.flow.append(grid(["Yarn used (brand, shade, lot)", "Hook",
                               "Gauge: sc per 5 cm / 2 in", "Finished height",
                               "Finished width", "Stuffing weight", "Started", "Finished"], 19))

        self.flow.append(Spacer(1, 8))
        self.flow.append(Paragraph("Notes", self.st.h4))
        lines = Table([[""] for _ in range(4)], colWidths=[CONTENT_W - 1], rowHeights=[17] * 4)
        lines.setStyle(TableStyle([
            ("LINEBELOW", (0, 0), (-1, -1), 0.55, HexColor(self.theme["muted"])),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ]))
        self.flow.append(lines)

        self.flow.append(Spacer(1, 8))
        self.flow.append(Paragraph("Blocking &amp; finishing", self.st.h4))
        self.flow.append(grid(["Blocked / steamed (method and time)", "Dried flat",
                               "Final height × width", "Gift / sale - date"], 19, 0.42))

        if checks:
            self.flow.append(Spacer(1, 9))
            self.flow.append(Paragraph("Before you sew - tick as you go", self.st.h4))
            for item in checks[:12]:
                short = re.split(r"[-—]", pdfmd.plain(item), maxsplit=1)[0].strip()
                self.flow.append(Paragraph(f"{CHECK_GLYPH}&nbsp;&nbsp;{pdfmd.inline(short)}",
                                           self.st.tiny))

        if tags:
            self.flow.append(Spacer(1, 8))
            box = Table([[Paragraph(
                f"<b>Share your make</b> — tag {pdfmd.inline(tags)} so other makers can find "
                f"the pattern. Please credit “Pattern by Novality Store · "
                f"{self.meta.design_code.title()}”.", self.st.tiny)]], colWidths=[CONTENT_W - 1])
            box.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), HexColor(self.theme["soft"])),
                ("BOX", (0, 0), (-1, -1), 0.4, HexColor(self.theme["border"])),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]))
            self.flow.append(box)

    # -- the main walk
    def build(self, blocks: list[Block], collection: bool = False) -> list:
        idx = 0
        n = len(blocks)
        seen_instructions = False
        while idx < n:
            b = blocks[idx]
            if b.kind == "h1":
                if collection:
                    self.part_divider(pdfmd.plain(b.text))
                idx += 1
                continue
            if b.kind in ("h2", "h3", "h4"):
                if b.kind == "h3" and seen_instructions:
                    idx = self.component(blocks, idx)
                    continue
                key = section_key(b.text) if b.kind == "h2" else None
                if key == "instructions":
                    self.heading(2, b.text)
                    seen_instructions = True
                    idx += 1
                    continue
                if key == "materials":
                    idx = self.section_materials(blocks, idx)
                    continue
                if key == "gauge":
                    idx = self.section_gauge(blocks, idx)
                    continue
                if key == "abbrev":
                    idx = self.section_abbrev(blocks, idx)
                    continue
                if key == "techniques":
                    idx = self.section_techniques(blocks, idx)
                    continue
                if key == "trouble":
                    idx = self.section_trouble(blocks, idx)
                    continue
                if key == "terms":
                    idx = self.section_terms(blocks, idx)
                    continue
                if key == "finishing":
                    idx = self.section_finishing(blocks, idx)
                    continue
                if key == "safety":
                    idx = self.section_safety(blocks, idx)
                    continue
                if key == "closing":
                    idx = self.section_closing(blocks, idx)
                    continue
                if key in ("care", "colorways", "notes"):
                    idx = self.section_compact(blocks, idx)
                    continue
                self.heading(b.level if b.level > 1 else 2, b.text)
                idx += 1
                continue
            if b.kind == "table":
                table = build_table(b, self.st, self.theme, CONTENT_W, tick=True)
                if table is not None:
                    self.flow.append(table)
                    self.flow.append(Spacer(1, 4))
                idx += 1
                continue
            if b.kind == "ul":
                self.bullets(b.items)
                idx += 1
                continue
            if b.kind == "ol":
                self.numbered(b.items)
                idx += 1
                continue
            if b.kind == "p":
                self.paragraphs(b.text)
                idx += 1
                continue
            if b.kind == "quote":
                idx += 1
                continue
            if b.kind == "hr":
                self.flow.append(HRFlowable(width="100%", thickness=0.5,
                                            color=HexColor(self.theme["border"]),
                                            spaceBefore=3, spaceAfter=5))
                idx += 1
                continue
            idx += 1
        return self.flow

    def part_divider(self, title: str):
        self.flow.append(PageBreak())
        self.flow.append(Spacer(1, 6))
        self.flow.append(HRFlowable(width="100%", thickness=1.4,
                                    color=HexColor(self.theme["accent"]),
                                    spaceBefore=0, spaceAfter=6))
        self.flow.append(Paragraph(pdfmd.inline(title), self.st.h2))
        self.flow.append(Spacer(1, 2))

    # -- sections needing data
    def _collect(self, blocks: list[Block], start: int) -> tuple[list[Block], int]:
        idx = start + 1
        out = []
        while idx < len(blocks) and blocks[idx].kind in ("p", "ul", "ol", "table", "h4", "quote", "hr"):
            out.append(blocks[idx])
            idx += 1
        return out, idx

    def section_materials(self, blocks, start):
        body, idx = self._collect(blocks, start)
        left: list = []
        items = []
        others: list[Block] = []
        for b in body:
            if b.kind == "ul":
                items.extend(b.items)
            else:
                others.append(b)
        left.append(Paragraph(pdfmd.inline(blocks[start].text), self.st.h2))
        if items:
            left.extend(self.materials_table(items, CONTENT_W * 0.52 - 8))
        for b in others:
            if b.kind == "p":
                left.append(Paragraph(pdfmd.inline(b.text), self.st.body_tight))
        self.flow.extend(left)
        self.flow.append(Spacer(1, 4))
        return idx

    def section_abbrev(self, blocks, start):
        body, idx = self._collect(blocks, start)
        self.flow.append(Paragraph(pdfmd.inline(blocks[start].text), self.st.h2))
        paras = [b.text for b in body if b.kind == "p"]
        self.flow.extend(self.abbreviations_table(paras, CONTENT_W * 0.52 - 8))
        self.flow.append(Spacer(1, 4))
        return idx

    def section_gauge(self, blocks, start):
        body, idx = self._collect(blocks, start)
        self.flow.append(Paragraph(pdfmd.inline(blocks[start].text), self.st.h2))
        paras = [b.text for b in body if b.kind == "p"]
        self.flow.extend(self.gauge_panel(paras))
        self.flow.append(Spacer(1, 5))
        return idx

    def section_techniques(self, blocks, start):
        body, idx = self._collect(blocks, start)
        self.flow.append(Paragraph(pdfmd.inline(blocks[start].text), self.st.h2))
        n = 0                                   # numbering runs across the section
        for b in body:
            if b.kind == "ol":
                for item in b.items:
                    n += 1
                    m = re.match(r"\*\*(.+?)\*\*\s*[-—]?\s*(.*)", item, flags=re.S)
                    if m:
                        head, rest = m.group(1).strip(), m.group(2).strip(" .—-")
                        text = (f"<b>{pdfmd.inline(head)}</b> — {pdfmd.inline(rest)}"
                                if rest else f"<b>{pdfmd.inline(head)}</b>")
                    else:
                        text = pdfmd.inline(item)
                    self.flow.append(Paragraph(text, self.st.step, bulletText=str(n)))
            elif b.kind == "p":
                self.flow.append(Paragraph(pdfmd.inline(b.text), self.st.body_tight))
        self.flow.append(Spacer(1, 4))
        return idx

    def section_safety(self, blocks, start):
        body, idx = self._collect(blocks, start)
        text = " ".join(b.text for b in body if b.kind == "p")
        self.callout(pdfmd.plain(blocks[start].text), text)
        return idx

    def section_trouble(self, blocks, start):
        body, idx = self._collect(blocks, start)
        self.flow.append(CondPageBreak(60))
        self.flow.append(Paragraph(pdfmd.inline(blocks[start].text), self.st.h2))
        items = []
        for b in body:
            if b.kind == "ul":
                items.extend(b.items)
        if items:
            self.flow.extend(self.trouble_grid(items))
        self.flow.append(Spacer(1, 5))
        return idx

    def section_finishing(self, blocks, start):
        body, idx = self._collect(blocks, start)
        self.flow.append(CondPageBreak(80))
        self.flow.append(Paragraph(pdfmd.inline(blocks[start].text), self.st.h2))
        off = 1
        for b in body:
            if b.kind == "ol":
                off = self.numbered(b.items, off)
            elif b.kind == "ul":
                self.bullets(b.items)
            elif b.kind == "p":
                self.paragraphs(b.text, self.st.body_tight)
        self.flow.append(Spacer(1, 4))
        return idx

    def section_generic(self, blocks, start):
        """Anything the renderer does not special-case: heading, then its body."""
        self.flow.append(Paragraph(pdfmd.inline(blocks[start].text), self.st.h2))
        _groups, bounds = section_bounds(blocks)
        end = bounds.get(start, len(blocks))
        cursor = start + 1
        while cursor < end:
            b = blocks[cursor]
            if b.kind == "h3" or b.kind == "h4":
                self.heading(b.level, b.text)
            elif b.kind == "p":
                self.paragraphs(b.text, self.st.body_tight)
            elif b.kind == "ul":
                self.bullets(b.items)
            elif b.kind == "ol":
                self.numbered(b.items)
            elif b.kind == "table":
                table = build_table(b, self.st, self.theme, CONTENT_W, tick=False)
                if table:
                    self.flow.append(table)
                    self.flow.append(Spacer(1, 4))
            cursor += 1
        self.flow.append(Spacer(1, 4))

    def section_compact(self, blocks, start):
        body, idx = self._collect(blocks, start)
        self.flow.append(Paragraph(pdfmd.inline(blocks[start].text), self.st.h2))
        for b in body:
            if b.kind == "ul":
                self.bullets(b.items)
            elif b.kind == "p":
                self.paragraphs(b.text, self.st.body_tight)
            elif b.kind == "table":
                table = build_table(b, self.st, self.theme, CONTENT_W, tick=False)
                if table:
                    self.flow.append(table)
                    self.flow.append(Spacer(1, 4))
        self.flow.append(Spacer(1, 4))
        return idx

    def section_terms(self, blocks, start):
        body, idx = self._collect(blocks, start)
        # also pull h3 subsections that follow
        while idx < len(blocks) and blocks[idx].kind == "h3":
            body.append(blocks[idx])
            inner, idx = self._collect(blocks, idx)
            body.extend(inner)
        self.flow.append(CondPageBreak(120))
        self.flow.append(Paragraph(pdfmd.inline(blocks[start].text), self.st.h2))
        self.colophon(body)
        self.flow.append(Spacer(1, 5))
        return idx

    def section_closing(self, blocks, start):
        body, idx = self._collect(blocks, start)
        text = " ".join(b.text for b in body if b.kind == "p")
        box = Table([[Paragraph(f"<b>{pdfmd.inline(pdfmd.plain(blocks[start].text))}</b>  "
                                f"{pdfmd.inline(text)}", self.st.body_tight)]],
                    colWidths=[CONTENT_W])
        box.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), HexColor(self.theme["soft"])),
            ("BOX", (0, 0), (-1, -1), 0.5, HexColor(self.theme["border"])),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ]))
        self.flow.append(Spacer(1, 3))
        self.flow.append(KeepTogether(box))
        return idx

    def component(self, blocks: list[Block], start: int, end: int | None = None,
                  prefix: list | None = None) -> int:
        """One `### N. Name` block plus its paragraphs and tables -> card."""
        title = blocks[start].text
        self._card_title = pdfmd.plain(title)
        end = len(blocks) if end is None else end
        idx = start + 1
        body: list[Block] = []
        while idx < end and blocks[idx].kind not in ("h2", "h3"):
            body.append(blocks[idx])
            idx += 1

        head = [Paragraph(pdfmd.inline(title), self.st.h3)]
        intro: list = []
        tables: list[Block] = []
        trailing: list[Block] = []
        subs: list[tuple[str, list[Block]]] = []
        for b in body:
            if b.kind == "table":
                tables.append(b)
            elif b.kind == "h4":
                subs.append((b.text, []))
            elif subs and b.kind in ("p", "ul", "ol"):
                subs[-1][1].append(b)
            else:
                intro.append(b)

        rows_total = sum(len(t.rows) for t in tables)

        def render(block_list: list[Block]) -> list:
            out: list = []
            for b in block_list:
                if b.kind == "p":
                    out.append(Paragraph(pdfmd.inline(b.text), self.st.body_tight))
                elif b.kind == "ul":
                    for item in b.items:
                        out.append(Paragraph(pdfmd.inline(item), self.st.bullet,
                                             bulletText="•"))
                elif b.kind == "ol":
                    for n, item in enumerate(b.items, start=1):
                        out.append(Paragraph(f"{n}. {pdfmd.inline(item)}",
                                             self.st.bullet))
                elif b.kind == "table":
                    table = build_table(b, self.st, self.theme, CONTENT_W - 16, tick=True)
                    if table:
                        out.append(table)
                elif b.kind == "quote":
                    out.append(Paragraph(pdfmd.inline(b.text), self.st.small))
            return out

        intro_flow = [Paragraph(pdfmd.inline(b.text), self.st.body_tight)
                      for b in intro if b.kind == "p"]

        # a narrow table plus prose goes into a 68/32 sidebar card
        sidebar = None
        if len(tables) == 1 and not subs and len(tables[0].rows) <= 10:
            table_flow = build_table(tables[0], self.st, self.theme,
                                     (CONTENT_W - 16) * 0.66, tick=True)
            prose: list = []
            for b in intro[len(intro_flow):]:
                prose.extend(render([b]))
            if table_flow is not None and prose:
                sidebar = ([intro_flow + [table_flow]] if intro_flow else [table_flow],
                           prose)
        if sidebar is None:
            inner = head + intro_flow
            for table in tables:
                t = build_table(table, self.st, self.theme, CONTENT_W - 16, tick=True)
                if t:
                    inner.append(t)
                    inner.append(Spacer(1, 3))
            for sub_title, sub_body in subs:
                inner.append(Bookmark(pdfmd.plain(sub_title), level=2))
                inner.append(Paragraph(pdfmd.inline(sub_title), self.st.h4))
                inner.extend(render(sub_body))
            self.card(inner, keep=rows_total <= 16, prefix=prefix)
        else:
            left, right = sidebar
            inner = head + left
            self.card(inner, keep=rows_total <= 16, sidebar=(left, right),
                      fallback=head + left + right, prefix=prefix)
        return idx


# --- one pattern ----------------------------------------------------------

def load_master(code: str) -> tuple[str, str]:
    num = code.split("-")[1]
    path = ROOT / "docs" / f"ns{num}" / f"NS{num}_corrected.md"
    return path.read_text(encoding="utf-8"), str(path)


def load_spec(code: str) -> dict:
    num = code.split("-")[1]
    path = ROOT / "docs" / f"ns{num}" / "spec.py"
    if not path.exists():
        return {}
    spec = importlib.util.spec_from_file_location("spec", path)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except Exception:
        return {}
    return getattr(mod, "SPEC", {}) or {}


def hero_for(code: str, spec: dict) -> str | None:
    num = code.split("-")[1]
    candidates = []
    if spec.get("hero"):
        p = Path(spec["hero"])
        candidates.append(p if p.is_absolute() else ROOT / p)
    for folder in (ROOT / "docs" / f"ns{num}" / "assets", ROOT / f"NS{num}_corrected" / "assets",
                   ROOT / "assets"):
        if folder.exists():
            candidates.extend(sorted(folder.glob("*hero*.png")))
            candidates.extend(sorted(folder.glob("*hero*.jpg")))
    for cand in candidates:
        if cand.exists():
            return str(cand)
    return None


HANDLERS = {
    "materials": Renderer.section_materials,
    "abbrev": Renderer.section_abbrev,
    "gauge": Renderer.section_gauge,
    "techniques": Renderer.section_techniques,
    "safety": Renderer.section_safety,
    "trouble": Renderer.section_trouble,
    "finishing": Renderer.section_finishing,
    "terms": Renderer.section_terms,
    "closing": Renderer.section_closing,
    "care": Renderer.section_compact,
    "colorways": Renderer.section_compact,
    "notes": Renderer.section_compact,
}

FRONT_KEYS = ("materials", "abbrev", "gauge", "safety", "techniques", "notes")


def section_bounds(blocks: list[Block]) -> tuple[list[tuple[int, str | None]], dict[int, int]]:
    """(index, key) for every `## ` heading, plus the exclusive end of each."""
    groups = [(i, section_key(b.text)) for i, b in enumerate(blocks) if b.kind == "h2"]
    bounds: dict[int, int] = {}
    for k, (idx, _key) in enumerate(groups):
        bounds[idx] = groups[k + 1][0] if k + 1 < len(groups) else len(blocks)
    return groups, bounds


def build_pattern(code: str, edition: str, outdir: Path, quiet: bool = False) -> Path:
    md_text, _ = load_master(code)
    blocks = pdfmd.parse(md_text)
    spec = load_spec(code)
    meta = derive_meta(code, blocks, spec)
    meta.edition = edition
    theme = THEMES[edition]
    styles = Styles(theme)
    note = spec.get("cover_note") or ""
    hero = hero_for(code, spec) if edition == "colour" else None
    palette = cover_palette(blocks) if edition == "colour" else []
    renderer = Renderer(meta, theme, styles)

    groups, bounds = section_bounds(blocks)

    titles: list[str] = []
    for idx, key in groups:
        if key == "instructions":
            titles = [pdfmd.plain(b.text) for b in blocks[idx + 1:bounds[idx]] if b.kind == "h3"]

    def group_flow(idx: int, key: str) -> list:
        sub = Renderer(meta, theme, styles)
        HANDLERS[key](sub, blocks, idx)
        return sub.flow

    story: list = [Spacer(1, 1), NextPageTemplate("body"), PageBreak()]

    # ---- page 2: the 52/48 grid, then the safety banner ------------------
    left: list = []
    right: list = []
    safety_idx = tech_idx = notes_idx = None
    for idx, key in groups:
        if key in ("materials", "abbrev"):
            left.extend(group_flow(idx, key))
        elif key == "gauge":
            right.extend(group_flow(idx, key))
            right.extend(renderer.inside_panel(titles, RIGHT_W))
        elif key == "safety":
            safety_idx = idx
        elif key == "techniques":
            tech_idx = idx
        elif key == "notes":
            notes_idx = idx

    first_h2 = groups[0][0] if groups else len(blocks)
    for b in blocks[:first_h2]:
        if b.kind == "p" and "FINISHED SIZE" not in b.text.upper() \
                and pdfmd.plain(b.text) != meta.intro:
            renderer.paragraphs(b.text, styles.body_tight)

    if left:
        renderer.flow.append(Bookmark("Materials, gauge & abbreviations", level=0))
        if not renderer.two_column(left, right, CONTENT_H * 0.72, split=0.52):
            renderer.flow.extend(left)
            if right:
                renderer.flow.append(Spacer(1, 3))
                renderer.flow.extend(right)
    if safety_idx is not None:
        renderer.section_safety(blocks, safety_idx)
    if tech_idx is not None:
        renderer.section_techniques(blocks, tech_idx)
    if notes_idx is not None:
        renderer.section_compact(blocks, notes_idx)

    # ---- instructions: one card per component ----------------------------
    for idx, key in groups:
        if key != "instructions":
            continue
        heading = Paragraph(pdfmd.inline(blocks[idx].text), styles.h2)
        first = True
        cursor = idx + 1
        while cursor < bounds[idx]:
            b = blocks[cursor]
            if b.kind == "h3":
                prefix = [heading, Spacer(1, 2)] if first else None
                cursor = renderer.component(blocks, cursor, bounds[idx], prefix=prefix)
                first = False
            elif b.kind == "p":
                renderer.paragraphs(b.text, styles.body_tight)
                cursor += 1
            elif b.kind == "ul":
                renderer.bullets(b.items)
                cursor += 1
            elif b.kind == "table":
                table = build_table(b, styles, theme, CONTENT_W, tick=True)
                if table:
                    renderer.flow.append(table)
                    renderer.flow.append(Spacer(1, 4))
                cursor += 1
            else:
                cursor += 1

    # ---- everything else, in the master's own order ----------------------
    skip = set(FRONT_KEYS) | {"instructions"}
    for idx, key in groups:
        if key in skip:
            continue
        handler = HANDLERS.get(key)
        if handler is None:
            renderer.section_generic(blocks, idx)
            continue
        handler(renderer, blocks, idx)

    sew_checks: list[str] = []
    for idx, key in groups:
        if key == "finishing":
            sew_checks = [item for b in blocks[idx + 1:bounds[idx]] if b.kind == "ol"
                          for item in b.items]
    renderer.project_record(sew_checks, meta.tags)
    renderer.flow.append(Spacer(1, 8))
    renderer.flow.append(HRFlowable(width="100%", thickness=0.4,
                                    color=HexColor(theme["border"]),
                                    spaceBefore=2, spaceAfter=5))
    renderer.flow.append(Paragraph(
        "End of pattern. Every stitch count, size and quantity in this edition was recomputed "
        "from the instruction text, not sampled. The copyright notice appears once, in the "
        "page footer of every page.", styles.tiny))
    story.extend(renderer.flow)

    suffix = {"colour": "_Colour_Edition.pdf", "print": "_Print_Edition.pdf"}[edition]
    stem = re.sub(r"[^A-Za-z0-9]+", "_", meta.title).strip("_")
    out = outdir / f"{code.replace('-', '')}_{stem}{suffix}"
    out.parent.mkdir(parents=True, exist_ok=True)

    # cover cards come from the builder, never from the spec: the spec sets carry
    # internal QA lines ("5-axiom audit", "static analysis engine") that must not
    # reach a reader's file
    cards = default_cards(edition, len(titles))
    finish_pdf(out, meta, theme,
               make_cover(meta, theme, hero, note, cards, palette, titles), story)
    if not quiet:
        print(f"  {_rel(out)}")
    return out


# --- the compiled collection ---------------------------------------------

def build_grand(edition: str, outdir: Path, quiet: bool = False) -> Path:
    md = (ROOT / "NovalityStore_Grand_Collection_corrected.md").read_text(encoding="utf-8")
    blocks = pdfmd.parse(md)
    theme = THEMES[edition]
    styles = Styles(theme)
    meta = Meta(code="NS-01 … NS-17", title="The Grand Crochet Pattern Collection",
                edition=edition, design_code="DESIGN CODES NS 01 … NS 17",
                intro="Seventeen corrected crochet patterns in one volume: every stitch table "
                      "re-derived from its own instruction text, every prose figure re-checked "
                      "against the pattern's own gauge.",
                skill="All levels marked", hours="17 patterns",
                size="17 designs", yarn_hook="Worsted to DK · 3.0 – 4.5 mm",
                terms="US crochet terms, with US + UK tables where a pattern needs them")
    renderer = Renderer(meta, theme, styles)

    # trim the generator's own provenance lines from the body
    blocks = [b for b in blocks
              if not (b.kind == "p" and ("Built " in b.text and "build_grand.py" in b.text))]
    blocks = [b for b in blocks if not (b.kind == "p" and b.text.startswith("*Generated file"))]

    story: list = [Spacer(1, 1), NextPageTemplate("body"), PageBreak()]
    idx = 0
    seen_instructions = False
    while idx < len(blocks):
        b = blocks[idx]
        if b.kind == "h1":
            title = pdfmd.plain(b.text)
            if title.lower().startswith("novality store"):
                idx += 1
                continue
            renderer.part_divider(title)
            idx += 1
            continue
        key = section_key(b.text) if b.kind == "h2" else None
        if key:
            handler = {
                "trouble": renderer.section_trouble,
                "terms": renderer.section_terms,
                "finishing": renderer.section_finishing,
                "safety": renderer.section_safety,
                "closing": renderer.section_closing,
                "materials": renderer.section_materials,
                "gauge": renderer.section_gauge,
                "abbrev": renderer.section_abbrev,
                "techniques": renderer.section_techniques,
                "care": renderer.section_compact,
                "colorways": renderer.section_compact,
                "notes": renderer.section_compact,
            }.get(key)
            if handler:
                idx = handler(blocks, idx)
                continue
            if key == "instructions":
                renderer.heading(2, b.text)
                seen_instructions = True
                idx += 1
                continue
        if b.kind in ("h2", "h3", "h4"):
            if b.kind == "h3" and seen_instructions:
                idx = renderer.component(blocks, idx)
                continue
            renderer.heading(b.level, b.text)
            idx += 1
            continue
        if b.kind == "table":
            table = build_table(b, styles, theme, CONTENT_W, tick=True)
            if table:
                renderer.flow.append(table)
                renderer.flow.append(Spacer(1, 4))
            idx += 1
            continue
        if b.kind == "ul":
            renderer.bullets(b.items)
            idx += 1
            continue
        if b.kind == "ol":
            renderer.numbered(b.items)
            idx += 1
            continue
        if b.kind == "p":
            renderer.paragraphs(b.text, styles.body_tight)
            idx += 1
            continue
        if b.kind == "hr":
            idx += 1
            continue
        idx += 1

    story.extend(renderer.flow)
    story.append(Spacer(1, 8))
    story.append(Paragraph("End of volume. Seventeen patterns, one corrected edition; the "
                           "copyright notice appears once, in the page footer.",
                           styles.tiny))

    suffix = {"colour": "_Colour_Edition.pdf", "print": "_Print_Edition.pdf"}[edition]
    out = outdir / f"NovalityStore_Grand_Collection{suffix}"
    out.parent.mkdir(parents=True, exist_ok=True)
    finish_pdf(out, meta, theme, make_cover(meta, theme, None, ""), story)
    if not quiet:
        print(f"  {_rel(out)}")
    return out


# --- entry point ----------------------------------------------------------

def _rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


ALL_CODES = [f"NS-{i:02d}" for i in range(1, 18)]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--codes", nargs="*", default=None,
                    help="patterns to build (default: all seventeen)")
    ap.add_argument("--only", choices=["colour", "print"], default=None)
    ap.add_argument("--grand", action="store_true", help="also build the collection")
    ap.add_argument("--outdir", default=None)
    ap.add_argument("--check", action="store_true", help="verify geometry and exit")
    args = ap.parse_args(argv)

    register_fonts()
    if args.check:
        bar = GaugeRuler(THEMES["colour"])
        length = bar.length
        if abs(length - 50 * mm) > 0.01 or abs(length - 141.732) > 0.05:
            raise SystemExit(f"gauge ruler is {length:.3f} pt, expected 141.732 pt (50 mm)")
        print(f"gauge ruler: {length:.3f} pt = {length / mm:.1f} mm = {length / 72:.3f} in")
        print("check ok")
        return 0

    codes = args.codes or ALL_CODES
    editions = [args.only] if args.only else ["colour", "print"]
    outdir = Path(args.outdir) if args.outdir else SHOP
    if not outdir.is_absolute():
        outdir = ROOT / outdir

    for code in codes:
        for edition in editions:
            build_pattern(code, edition, outdir)
    if args.grand:
        for edition in editions:
            build_grand(edition, outdir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
