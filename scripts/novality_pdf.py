#!/usr/bin/env python3
"""Novality Store full-colour pattern renderer.

Renders a pattern markdown file into the house full-colour layout: cover
banner, colour-barred section headers, alternating instruction tables with an
accented stitch-count column, rounded callout boxes, size pill badges, a styled
appendix code block, and the 5-Axiom verified badge on the first and last page.

Pure ReportLab - no WeasyPrint and no system libraries beyond the DejaVu fonts.

    python scripts/novality_pdf.py PATTERN.md OUT.pdf \
        --title "Bobble Snowflake Tree Skirt" \
        --code NS-14 --difficulty "Easy-Intermediate" \
        --colours "Forest Green + Oat Cream"
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.utils import ImageReader

sys.path.insert(0, str(Path(__file__).resolve().parent))
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.platypus import (
    BaseDocTemplate,
    CondPageBreak,
    Flowable,
    Frame,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from novality_figures import FIGURES

# ---------------------------------------------------------------- brand theme

FOREST = colors.HexColor("#1E3A2B")   # primary headers, bars, banner
FOREST_LT = colors.HexColor("#2E5440")
OAT = colors.HexColor("#E6D7C3")      # secondary accent
OAT_LT = colors.HexColor("#F3EADF")   # stitch-count column fill
GOLD = colors.HexColor("#D4AF37")     # badges, rules
SAGE = colors.HexColor("#E8F0EC")     # informational callouts
AMBER = colors.HexColor("#FFF8E7")    # warning callouts
AMBER_EDGE = colors.HexColor("#E0B84C")
INK = colors.HexColor("#1A1A1A")      # body text
MUTED = colors.HexColor("#5F6B64")
RULE = colors.HexColor("#D8DEDA")
ROW_ALT = colors.HexColor("#F8F9FA")
CODE_BG = colors.HexColor("#F4F6F5")

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")


def register_fonts() -> tuple[str, str, str]:
    """Register DejaVu face by face.

    Per-file on purpose: this box has no DejaVuSans-Oblique.ttf, and wrapping
    the set in one try/except let a single missing file silently downgrade the
    whole document to Helvetica (no U+2610, so checkboxes drew as filled
    blocks). Italic falls back to regular rather than taking the run down.
    """

    def reg(name: str, filename: str) -> bool:
        path = FONT_DIR / filename
        if not path.is_file():
            return False
        try:
            pdfmetrics.registerFont(TTFont(name, str(path)))
            return True
        except Exception:
            return False

    if not reg("DejaVu", "DejaVuSans.ttf"):
        return "Helvetica", "Helvetica-Bold", "Courier"
    bold = "DejaVu-Bold" if reg("DejaVu-Bold", "DejaVuSans-Bold.ttf") else "DejaVu"
    mono = "DejaVuMono" if reg("DejaVuMono", "DejaVuSansMono.ttf") else "DejaVu"
    italic = "DejaVu-Oblique" if reg("DejaVu-Oblique", "DejaVuSans-Oblique.ttf") else "DejaVu"

    # registerFontFamily alone leaves ps2tt("DejaVu") == ("dejavu", 1, 1), so the
    # base face reads as already bold+italic and every <b> resolves back to
    # regular. addMapping writes both maps; the (0,0) call must come last
    # because each call also sets _ps2tt_map[psname].
    from reportlab.lib.fonts import addMapping

    addMapping("DejaVu", 1, 1, bold)
    addMapping("DejaVu", 0, 1, italic)
    addMapping("DejaVu", 1, 0, bold)
    addMapping("DejaVu", 0, 0, "DejaVu")
    return "DejaVu", bold, mono


BODY, BOLD, MONO = register_fonts()

import novality_figures as _figs  # noqa: E402

_figs.use_fonts(BODY, BOLD)

SIZE_WORDS = ("MINI", "STANDARD", "LARGE")


def inline(text: str, pill: bool = True) -> str:
    """Markdown inline -> ReportLab markup."""
    out = escape(text)
    out = re.sub(r"`([^`]+)`", rf'<font face="{MONO}" size="8.3">\1</font>', out)
    out = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", out)
    out = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<i>\1</i>", out)
    out = out.replace("\u2610", f'<font face="{BODY}" size="10.5">&#9744;</font>')
    if pill:
        for word in SIZE_WORDS:
            out = out.replace(
                f"<b>{word}</b>",
                f'<font face="{BOLD}" size="7.2" backColor="#1E3A2B" color="#FFFFFF">'
                f"&nbsp;{word}&nbsp;</font>",
            )
    return out


def mk(**kw) -> ParagraphStyle:
    kw.setdefault("fontName", BODY)
    kw.setdefault("textColor", INK)
    return ParagraphStyle(**kw)


S = {
    "h2": mk(name="h2", fontName=BOLD, fontSize=11.4, leading=14, spaceBefore=10,
             spaceAfter=5, textColor=FOREST),
    "h3": mk(name="h3", fontName=BOLD, fontSize=9.9, leading=12.6, spaceBefore=8,
             spaceAfter=3.5, textColor=FOREST_LT),
    "p": mk(name="p", fontSize=9.1, leading=13.4, spaceAfter=5.5),
    # bulletFontName must be the DejaVu face: Helvetica has no U+25B8/U+2610
    # and ReportLab silently draws a filled box for a missing glyph.
    "li": mk(name="li", fontSize=9.1, leading=13.4, spaceAfter=2.5, leftIndent=13,
             bulletIndent=2, bulletFontName=BODY, bulletFontSize=8.2,
             bulletColor=FOREST_LT),
    "code": mk(name="code", fontName=MONO, fontSize=7.7, leading=10.1),
    "cell": mk(name="cell", fontSize=7.9, leading=10.5),
    "cellb": mk(name="cellb", fontName=BOLD, fontSize=7.9, leading=10.5),
    "cellh": mk(name="cellh", fontName=BOLD, fontSize=8.0, leading=10.6, textColor=colors.white),
    "cellnum": mk(name="cellnum", fontName=BOLD, fontSize=8.6, leading=11, textColor=FOREST),
    "callh": mk(name="callh", fontName=BOLD, fontSize=9.6, leading=12.6, textColor=FOREST,
                spaceAfter=3),
    "callp": mk(name="callp", fontSize=8.8, leading=12.4, spaceAfter=4),
    "callli": mk(name="callli", fontSize=8.8, leading=12.4, spaceAfter=2, leftIndent=12,
                 bulletIndent=1, bulletFontName=BODY, bulletFontSize=8.0,
                 bulletColor=FOREST_LT),
}


# ------------------------------------------------------------ custom flowables


class CoverBanner(Flowable):
    """Full-colour title card: monogram badge, title, code and difficulty tags."""

    def __init__(self, width, title, code, imprint, owner, difficulty, colourway):
        super().__init__()
        self.width = width
        self.height = 46 * mm
        self.title, self.code = title, code
        self.imprint, self.owner = imprint, owner
        self.difficulty, self.colourway = difficulty, colourway

    def draw(self):
        c = self.canv
        w, h = self.width, self.height
        c.setFillColor(FOREST)
        c.roundRect(0, 0, w, h, 4 * mm, stroke=0, fill=1)
        c.setFillColor(GOLD)
        c.rect(0, h - 3.2 * mm, w, 3.2 * mm, stroke=0, fill=1)

        # monogram badge
        bx, by, bs = 8 * mm, h - 23 * mm, 15 * mm
        c.setFillColor(GOLD)
        c.roundRect(bx, by, bs, bs, 3 * mm, stroke=0, fill=1)
        c.setFillColor(FOREST)
        c.setFont(BOLD, 14)
        c.drawCentredString(bx + bs / 2, by + bs / 2 - 1.6 * mm, "N")
        c.setFont(BOLD, 5.6)
        c.drawCentredString(bx + bs / 2, by + 2.2 * mm, "STORE")

        tx = bx + bs + 7 * mm
        c.setFillColor(OAT)
        c.setFont(BOLD, 7.4)
        c.drawString(tx, h - 11.5 * mm, self.owner.upper())
        c.setFillColor(colors.white)
        size = 21 if len(self.title) <= 30 else 17
        c.setFont(BOLD, size)
        c.drawString(tx, h - 20.5 * mm, self.title)
        c.setFillColor(OAT)
        c.setFont(BODY, 7.6)
        c.drawString(tx, h - 25.6 * mm, self.imprint)

        # tag pills
        x = 8 * mm
        for label, fill, fg in (
            (f"DESIGN CODE {self.code}", GOLD, FOREST),
            (self.difficulty.upper(), OAT, FOREST),
            (self.colourway.upper(), FOREST_LT, OAT),
        ):
            if not label.strip():
                continue
            tw = pdfmetrics.stringWidth(label, BOLD, 6.8) + 7 * mm
            c.setFillColor(fill)
            c.roundRect(x, 5.4 * mm, tw, 6.4 * mm, 3.2 * mm, stroke=0, fill=1)
            c.setFillColor(fg)
            c.setFont(BOLD, 6.8)
            c.drawCentredString(x + tw / 2, 7.4 * mm, label)
            x += tw + 3 * mm


class VerifiedBadge(Flowable):
    """The 5-Axiom verified badge."""

    def __init__(self, width, compact=False):
        super().__init__()
        self.width = width
        self.height = 11 * mm if compact else 14 * mm
        self.compact = compact

    def draw(self):
        c = self.canv
        w, h = self.width, self.height
        c.setFillColor(SAGE)
        c.setStrokeColor(GOLD)
        c.setLineWidth(0.9)
        c.roundRect(0, 0, w, h, 2.6 * mm, stroke=1, fill=1)
        c.setFillColor(GOLD)
        c.circle(8.5 * mm, h / 2, 3.4 * mm, stroke=0, fill=1)
        c.setFillColor(FOREST)
        c.setFont(BOLD, 8)
        c.drawCentredString(8.5 * mm, h / 2 - 1.05 * mm, "\u2713")
        c.setFont(BOLD, 9 if not self.compact else 8.2)
        c.drawString(15 * mm, h / 2 + (0.6 * mm if not self.compact else 0.2 * mm),
                     "5-AXIOM MATHEMATICALLY VERIFIED")
        if not self.compact:
            c.setFillColor(MUTED)
            c.setFont(BODY, 6.8)
            c.drawString(15 * mm, h / 2 - 3.4 * mm,
                         "Written stitch-count audit. Results published in Appendix B, pass or fail.")


class HeroImage(Flowable):
    """Cover photograph: soft drop shadow, rounded corners, thin gold edge."""

    def __init__(self, width, path, caption=None, ratio=1.0, max_h=62 * mm):
        super().__init__()
        self.width = width
        self.path = str(path)
        self.caption = caption
        # Fit the whole image inside the cap without letterboxing: when it is
        # squarer than the column, narrow the box and centre it rather than
        # padding the sides.
        self.img_h = min(width * ratio, max_h)
        self.img_w = min(self.img_h / ratio, width)
        self.x0 = (width - self.img_w) / 2
        self.cap_h = 16 if caption else 0
        self.height = self.img_h + self.cap_h

    def draw(self):
        c = self.canv
        w, h = self.img_w, self.img_h
        x = self.x0
        y = self.cap_h
        rad = 4.2 * mm
        c.saveState()
        c.translate(x, 0)

        # stacked translucent rounds make a soft shadow without an alpha image
        for i in range(6, 0, -1):
            c.saveState()
            c.setFillColor(colors.Color(0, 0, 0, alpha=0.030))
            c.roundRect(i * 0.5, y - i * 0.75, w - i, h, rad, stroke=0, fill=1)
            c.restoreState()

        c.saveState()
        clip = c.beginPath()
        clip.roundRect(0, y, w, h, rad)
        c.clipPath(clip, stroke=0, fill=0)
        c.drawImage(ImageReader(self.path), 0, y, width=w, height=h,
                    preserveAspectRatio=True, anchor="c", mask="auto")
        c.restoreState()

        c.setStrokeColor(GOLD)
        c.setLineWidth(1.2)
        c.roundRect(0, y, w, h, rad, stroke=1, fill=0)

        c.restoreState()
        if self.caption:
            c.setFillColor(MUTED)
            c.setFont(BODY, 6.9)
            c.drawCentredString(self.width / 2, 5, self.caption)


class FigureBlock(Flowable):
    """A generated vector figure plus its caption, kept together on one page."""

    def __init__(self, drawing, caption=None):
        super().__init__()
        self.drawing = drawing
        self.caption = caption
        self.width = drawing.width
        self.cap_h = 13 if caption else 0
        self.height = drawing.height + self.cap_h

    def wrap(self, aw, ah):
        return self.width, self.height

    def draw(self):
        self.drawing.drawOn(self.canv, 0, self.cap_h)
        if self.caption:
            self.canv.setFillColor(MUTED)
            self.canv.setFont(BODY, 6.9)
            self.canv.drawString(2, 4, self.caption)


class EndCard(Flowable):
    """Closing badge: repeats the 5-Axiom mark and signs the edition off."""

    def __init__(self, width, code, imprint, owner):
        super().__init__()
        self.width = width
        self.height = 41 * mm
        self.code, self.imprint, self.owner = code, imprint, owner

    def draw(self):
        c = self.canv
        w, h = self.width, self.height
        cx = w / 2
        c.setFillColor(SAGE)
        c.setStrokeColor(GOLD)
        c.setLineWidth(1.1)
        c.roundRect(0, 0, w, h, 3.4 * mm, stroke=1, fill=1)
        c.saveState()  # clip so the gold cap follows the rounded corners
        clip = c.beginPath()
        clip.roundRect(0, 0, w, h, 3.4 * mm)
        c.clipPath(clip, stroke=0, fill=0)
        c.setFillColor(GOLD)
        c.rect(0, h - 2.2 * mm, w, 2.2 * mm, stroke=0, fill=1)
        c.restoreState()

        c.setFillColor(FOREST)
        c.circle(cx, h - 12.5 * mm, 5.2 * mm, stroke=0, fill=1)
        c.setFillColor(GOLD)
        c.setFont(BOLD, 11)
        c.drawCentredString(cx, h - 14.2 * mm, "\u2713")

        c.setFillColor(FOREST)
        c.setFont(BOLD, 11)
        c.drawCentredString(cx, h - 23.5 * mm, "5-AXIOM MATHEMATICALLY VERIFIED")
        c.setFillColor(MUTED)
        c.setFont(BODY, 7.4)
        c.drawCentredString(cx, h - 28.2 * mm,
                            "Every axiom result is published in Appendix B, pass or fail.")

        c.setStrokeColor(GOLD)
        c.setLineWidth(0.7)
        c.line(cx - 22 * mm, h - 31.8 * mm, cx + 22 * mm, h - 31.8 * mm)

        c.setFillColor(FOREST_LT)
        c.setFont(BOLD, 8.2)
        c.drawCentredString(cx, h - 36.2 * mm,
                            f"{self.imprint}  \u00b7  Design Code {self.code}")


class SectionBar(Flowable):
    """Colour bar introducing a major section."""

    def __init__(self, width, text):
        super().__init__()
        self.width = width
        self.height = 9.2 * mm
        self.text = text

    def draw(self):
        c = self.canv
        w, h = self.width, self.height
        c.setFillColor(FOREST)
        c.roundRect(0, 0, w, h, 1.8 * mm, stroke=0, fill=1)
        c.setFillColor(GOLD)
        c.rect(0, 0, 2.4 * mm, h, stroke=0, fill=1)
        c.setFillColor(colors.white)
        c.setFont(BOLD, 11.2)
        c.drawString(6.5 * mm, h / 2 - 1.5 * mm, self.text)


class Callout(Flowable):
    """Rounded callout box with a tinted fill, accent border and icon."""

    def __init__(self, width, flows, tone="info", icon="\u2756"):
        super().__init__()
        self.width = width
        self.flows = flows
        self.tone = tone
        self.icon = icon
        self.pad = 5.5 * mm
        self.inner_w = width - 2 * self.pad - 7 * mm
        self._h = 0

    def wrap(self, aw, ah):
        total = 0
        for f in self.flows:
            _, fh = f.wrap(self.inner_w, ah)
            total += fh + getattr(f, "_sa", 0)
        self._h = total + 2 * self.pad
        return self.width, self._h

    def draw(self):
        c = self.canv
        w, h = self.width, self._h
        fill, edge = (AMBER, AMBER_EDGE) if self.tone == "warn" else (SAGE, FOREST)
        c.setFillColor(fill)
        c.setStrokeColor(edge)
        c.setLineWidth(0.8)
        c.roundRect(0, 0, w, h, 2.8 * mm, stroke=1, fill=1)
        c.setFillColor(edge)
        c.setFont(BOLD, 11)
        c.drawString(self.pad, h - self.pad - 3.6 * mm, self.icon)
        y = h - self.pad
        for f in self.flows:
            _, fh = f.wrap(self.inner_w, h)
            f.drawOn(c, self.pad + 7 * mm, y - fh)
            y -= fh


class CodeBlock(Flowable):
    """Appendix code block on a subtle grey panel with a gold spine."""

    def __init__(self, width, lines):
        super().__init__()
        self.width = width
        self.lines = lines
        self.lh = 10.1
        self.pad = 4.5 * mm
        self.height = len(lines) * self.lh + 2 * self.pad

    def draw(self):
        c = self.canv
        w, h = self.width, self.height
        c.setFillColor(CODE_BG)
        c.setStrokeColor(RULE)
        c.setLineWidth(0.5)
        c.roundRect(0, 0, w, h, 2 * mm, stroke=1, fill=1)
        c.setFillColor(GOLD)
        c.rect(0, 0, 1.8 * mm, h, stroke=0, fill=1)
        c.setFillColor(INK)
        c.setFont(MONO, 7.7)
        y = h - self.pad - 7.0
        for ln in self.lines:
            c.drawString(self.pad + 2 * mm, y, ln)
            y -= self.lh


# ------------------------------------------------------------------- markdown


def split_row(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def is_sep(line: str) -> bool:
    return bool(re.fullmatch(r"\|[\s:\-|]+\|", line.strip()))


def _plain(s: str) -> str:
    """Strip inline markdown so measurements reflect what actually prints."""
    s = re.sub(r"`([^`]*)`", r"\1", s)
    s = s.replace("**", "").replace("*", "")
    s = s.replace("\u2610", "MM")  # checkbox occupies roughly two chars
    return s


def build_table(rows: list[list[str]], width: float) -> Table:
    head, body = rows[0], rows[1:]
    n = len(head)
    # A markdown table may legitimately have a blank header row (`| | |`), as the
    # abbreviations glossary does. Rendering the green bar then leaves an empty
    # coloured strip, so drop the header entirely and style it as a plain list.
    has_head = any(c.strip() for c in head)
    data = [[Paragraph(inline(c, pill=False), S["cellh"]) for c in head]] if has_head else []
    for r in body:
        r = (r + [""] * n)[:n]
        data.append([Paragraph(inline(c), S["cell"]) for c in r])

    pad = 8.4 + 2.0  # cell left+right padding, plus a hair of slack

    # Soft target from content volume, hard floor from the longest unbreakable
    # token in the column. Without the floor a short column such as Sts gets
    # squeezed and "(156)" wraps to "(156" / ")".
    weights, floors = [], []
    for i in range(n):
        cells = [_plain(r[i]) for r in rows if i < len(r)]
        weights.append(max(max((len(c) for c in cells), default=6), 6) ** 0.72)
        widest_token = 0.0
        for c in cells:
            for tok in c.split():
                widest_token = max(widest_token, pdfmetrics.stringWidth(tok, BOLD, 8.6))
        floors.append(min(widest_token + pad, width * 0.42))

    total_w = sum(weights)
    widths = [width * w / total_w for w in weights]
    for _ in range(4):  # settle floors, then redistribute the remainder
        fixed = [i for i in range(n) if widths[i] <= floors[i]]
        for i in fixed:
            widths[i] = floors[i]
        free = [i for i in range(n) if i not in fixed]
        spare = width - sum(widths[i] for i in fixed)
        if not free or spare <= 0:
            break
        fw_total = sum(weights[i] for i in free)
        for i in free:
            widths[i] = spare * weights[i] / fw_total
    scale = width / sum(widths)
    widths = [w * scale for w in widths]


    first = 1 if has_head else 0  # index of the first body row
    style = [
        ("ROWBACKGROUNDS", (0, first), (-1, -1), [colors.white, ROW_ALT]),
        ("GRID", (0, 0), (-1, -1), 0.3, RULE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3.4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.4),
        ("LEFTPADDING", (0, 0), (-1, -1), 4.2),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4.2),
    ]

    if has_head:
        style += [
            ("BACKGROUND", (0, 0), (-1, 0), FOREST),
            ("LINEBELOW", (0, 0), (-1, 0), 1.0, GOLD),
        ]
    else:
        # headerless tables read as a glossary: key column in brand green
        style.append(("LINEAFTER", (0, 0), (0, -1), 0.9, GOLD))

    # accent the stitch-count column so the final counts pop
    heads = [h.strip().lower().strip("*") for h in head]
    for i, hh in enumerate(heads):
        if hh in ("sts", "stitches", "count"):
            style.append(("BACKGROUND", (i, first), (i, -1), OAT_LT))
            style.append(("ALIGN", (i, 0), (i, -1), "CENTER"))
            for r in range(first, len(data)):
                src = body[r - first]
                data[r][i] = Paragraph(inline(src[i] if i < len(src) else ""), S["cellnum"])
    # vertical gold divider between the US and UK instruction columns
    if "us terms" in heads and "uk terms" in heads:
        style.append(("LINEAFTER", (heads.index("us terms"), 0),
                      (heads.index("us terms"), -1), 0.9, GOLD))

    t = Table(data, colWidths=widths, repeatRows=first, hAlign="LEFT")
    t.setStyle(TableStyle(style))
    return t


def callout_tone(title: str) -> tuple[str, str]:
    low = title.lower()
    if any(k in low for k in ("safety", "warning", "danger", "not checked", "disregard")):
        return "warn", "\u26a0"
    if "correction" in low:
        return "info", "\u2713"
    if "gauge" in low:
        return "info", "\u2756"
    return "info", "\u2756"


def parse(md: str, width: float, inner: bool = False) -> list:
    lines = md.split("\n")
    flow: list = []
    i = 0
    while i < len(lines):
        ln = lines[i]
        st = ln.strip()
        if not st:
            i += 1
            continue

        if st.startswith("```"):
            i += 1
            buf = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                buf.append(lines[i].rstrip())
                i += 1
            i += 1
            flow += [Spacer(1, 3), CodeBlock(width, buf), Spacer(1, 8)]
            continue

        if st.startswith("|") and i + 1 < len(lines) and is_sep(lines[i + 1]):
            rows = [split_row(st)]
            i += 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(split_row(lines[i]))
                i += 1
            flow += [Spacer(1, 3), build_table(rows, width), Spacer(1, 8)]
            continue

        if st.startswith(">"):
            buf = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                buf.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            text = "\n".join(buf)
            first = next((b for b in buf if b.strip()), "")
            tone, icon = callout_tone(first)
            inner_flows = parse(text, width - 18 * mm, inner=True)
            flow += [Spacer(1, 4), Callout(width, inner_flows, tone, icon), Spacer(1, 9)]
            continue

        if re.fullmatch(r"-{3,}|\*{3,}", st):
            flow.append(Spacer(1, 7))
            i += 1
            continue

        m = re.match(r"^(#{1,6})\s+(.*)$", st)
        if m:
            lvl, txt = len(m.group(1)), m.group(2)
            if lvl == 1:
                i += 1
                continue  # title is handled by the cover banner
            if lvl == 2:
                flow += [CondPageBreak(40 * mm), Spacer(1, 5),
                         SectionBar(width, re.sub(r"\*\*", "", txt)), Spacer(1, 6)]
            else:
                flow += [CondPageBreak(26 * mm), Paragraph(inline(txt), S["h3"])]
            i += 1
            continue

        if re.match(r"^\s*([-*+]|\d+\.)\s+", ln):
            items = []
            while i < len(lines) and re.match(r"^\s*([-*+]|\d+\.)\s+", lines[i]):
                mm_ = re.match(r"^\s*([-*+]|\d+\.)\s+(.*)$", lines[i])
                marker, txt = mm_.group(1), mm_.group(2)
                i += 1
                while (i < len(lines) and lines[i].strip()
                       and not re.match(r"^\s*([-*+]|\d+\.)\s+", lines[i])
                       and not lines[i].strip().startswith(("#", "|", ">", "```"))
                       and not re.fullmatch(r"-{3,}", lines[i].strip())):
                    txt += " " + lines[i].strip()
                    i += 1
                bullet = marker if marker[0].isdigit() else "\u25b8"
                if txt.lstrip().startswith("\u2610"):
                    # A checklist item: the box is the marker, so promote it into
                    # the bullet slot instead of printing it after a second one.
                    txt = txt.lstrip()[1:].lstrip()
                    bullet = "\u2610"
                items.append(Paragraph(inline(txt), S["callli" if inner else "li"],
                                       bulletText=bullet))
            flow += [Spacer(1, 2), *items, Spacer(1, 5)]
            continue

        m_fig = re.match(r"^\[\[figure:([a-z_]+)\]\]\s*(.*)$", st)
        if m_fig:
            name, cap = m_fig.group(1), m_fig.group(2).strip() or None
            i += 1
            if name in FIGURES:
                flow += [Spacer(1, 4),
                         FigureBlock(FIGURES[name](width), cap),
                         Spacer(1, 9)]
            continue

        buf = [st]
        i += 1
        while (i < len(lines) and lines[i].strip()
               and not lines[i].strip().startswith(("#", "|", ">", "```", "- ", "* "))
               and not re.fullmatch(r"-{3,}", lines[i].strip())
               and not re.match(r"^\s*\d+\.\s", lines[i])):
            buf.append(lines[i].strip())
            i += 1
        para = " ".join(buf)
        style = S["callp"] if inner else S["p"]
        if inner and not flow and re.fullmatch(r"\*\*.+\*\*", para.strip()):
            style = S["callh"]
        flow.append(Paragraph(inline(para), style))
    return flow


# ------------------------------------------------------------------ page glue


def make_canvas(header: str, footer: str):
    class NumberedCanvas(rl_canvas.Canvas):
        """Deferred page furniture so the footer can say 'Page X of Y'."""

        def __init__(self, *a, **kw):
            super().__init__(*a, **kw)
            self._saved = []

        def showPage(self):
            self._saved.append(dict(self.__dict__))
            self._startPage()

        def save(self):
            total = len(self._saved)
            for state in self._saved:
                self.__dict__.update(state)
                self._furniture(total)
                super().showPage()
            super().save()

        def _furniture(self, total):
            pw, ph = A4
            lm = rm = 15 * mm
            self.saveState()
            self.setFillColor(FOREST)
            self.rect(0, ph - 7.5 * mm, pw, 7.5 * mm, stroke=0, fill=1)
            self.setFillColor(GOLD)
            self.rect(0, ph - 8.3 * mm, pw, 0.8 * mm, stroke=0, fill=1)
            self.setFillColor(colors.white)
            self.setFont(BOLD, 6.9)
            self.drawString(lm, ph - 5.4 * mm, header)
            self.setFillColor(OAT)
            self.setFont(BODY, 6.9)
            self.drawRightString(pw - rm, ph - 5.4 * mm,
                                 f"Page {self.getPageNumber()} of {total}")
            self.setStrokeColor(RULE)
            self.setLineWidth(0.4)
            self.line(lm, 12.5 * mm, pw - rm, 12.5 * mm)
            self.setFillColor(MUTED)
            self.setFont(BODY, 6.6)
            self.drawString(lm, 9 * mm, footer)
            self.setFillColor(GOLD)
            self.setFont(BOLD, 6.6)
            self.drawRightString(pw - rm, 9 * mm, "\u2713 5-AXIOM VERIFIED")
            self.restoreState()

    return NumberedCanvas


BANNER_DUPES = (
    re.compile(r"^\s*\*\*Design Code .*\*\*\s*$", re.M),       # shown as a tag pill
    re.compile(r"^\s*\*.*crochet pattern line of.*\*\s*$", re.M),  # shown under the title
)


def render(md_path: Path, pdf_path: Path, meta: dict) -> None:
    md = md_path.read_text(encoding="utf-8")
    for pat in BANNER_DUPES:  # the cover banner already carries these
        md = pat.sub("", md)
    pw, ph = A4
    lm = rm = 15 * mm
    tm, bm = 13 * mm, 17 * mm
    fw = pw - lm - rm

    doc = BaseDocTemplate(
        str(pdf_path), pagesize=A4,
        leftMargin=lm, rightMargin=rm, topMargin=tm, bottomMargin=bm,
        title=f"{meta['title']} - {meta['code']} ({meta['edition']})",
        author=meta["owner"], subject="Crochet pattern, full-colour edition",
    )
    frame = Frame(lm, bm, fw, ph - tm - bm, id="body",
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id="main", frames=[frame])])

    story: list = [
        CoverBanner(fw, meta["title"], meta["code"], meta["imprint"],
                    meta["owner"], meta["difficulty"], meta["colourway"]),
        Spacer(1, 7),
    ]
    hero = meta.get("hero")
    if hero and Path(hero).exists():
        from PIL import Image as _PILImage
        with _PILImage.open(hero) as im:
            ratio = im.height / im.width
        story += [HeroImage(fw, hero, meta.get("hero_caption"),
                            ratio=ratio),
                  Spacer(1, 8)]
    story += [
        VerifiedBadge(fw),
        Spacer(1, 9),
    ]
    story += parse(md, fw)
    story += [Spacer(1, 13),
              EndCard(fw, meta["code"], meta["imprint"], meta["owner"])]

    doc.build(story, canvasmaker=make_canvas(meta["header"], meta["footer"]))


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description="Render a pattern markdown into the Novality layout.")
    ap.add_argument("source")
    ap.add_argument("dest")
    ap.add_argument("--title", default="Bobble Snowflake Tree Skirt")
    ap.add_argument("--code", default="NS-14")
    ap.add_argument("--edition", default="Corrected Edition")
    ap.add_argument("--difficulty", default="Easy-Intermediate")
    ap.add_argument("--colourway", default="Forest Green + Oat Cream")
    ap.add_argument("--owner", default="Novality Store")
    ap.add_argument("--hero", default="NS14_corrected/assets/NS14_hero_cover.png",
                    help="cover photograph; omit to keep the typographic banner")
    ap.add_argument("--hero-caption",
                    default="Design illustration - not a photograph of a "
                            "finished sample. No NS-14 skirt has been crocheted.")
    ap.add_argument("--imprint", default="Novality Crochet Studio \u00b7 the crochet pattern line")
    a = ap.parse_args()

    meta = dict(
        title=a.title, code=a.code, edition=a.edition, difficulty=a.difficulty,
        colourway=a.colourway, owner=a.owner, imprint=a.imprint,
        hero=a.hero, hero_caption=a.hero_caption,
        header=f"{a.owner}  |  Design Code {a.code}  |  {a.edition}",
        footer=f"\u00a9 2026 {a.owner}. All rights reserved.",
    )
    dst = Path(a.dest)
    dst.parent.mkdir(parents=True, exist_ok=True)
    render(Path(a.source), dst, meta)
    print(f"wrote {dst}  ({dst.stat().st_size:,} bytes)")
