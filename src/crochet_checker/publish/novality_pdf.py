"""Novality Store — branded customer-facing PDF builder (ReportLab).

Renders each validated pattern as a clean, minimal, warm pattern booklet:
cover page, overview, materials, finished size, gauge, abbreviations,
notes, instructions, finishing, tips, and the Novality Store copyright
notice on every PDF.

Usage:
    python -m crochet_checker.publish.build            # all 10 patterns
    python -m crochet_checker.publish.build --slug scarf
"""
from __future__ import annotations

import textwrap
from dataclasses import dataclass
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from . import novality_patterns as np

HERE = Path(__file__).parent
FONTS = HERE / "fonts"

# ---------------------------------------------------------------------------
# Design tokens
# ---------------------------------------------------------------------------
INK = colors.HexColor("#33302B")
ACCENT = colors.HexColor("#A9622F")
ACCENT_DARK = colors.HexColor("#8C4F27")
CREAM = colors.HexColor("#FAF7F2")
CARD = colors.HexColor("#F4EEE5")
CARD_LINE = colors.HexColor("#E7DFD2")
MUTED = colors.HexColor("#8B8275")
WHITE = colors.white

PAGE_W, PAGE_H = A4
M_L = M_R = 17 * mm
M_T = 16 * mm
M_B = 20 * mm

# ---------------------------------------------------------------------------
# Fonts
# ---------------------------------------------------------------------------
_registered = False


def _fonts():
    global _registered
    if _registered:
        return
    spec = [
        ("DVSerif", "DejaVuSerif.ttf"),
        ("DVSerif-Bold", "DejaVuSerif-Bold.ttf"),
        ("DVSerif-Italic", "DejaVuSerif-Italic.ttf"),
        ("DVSerif-BoldItalic", "DejaVuSerif-BoldItalic.ttf"),
        ("DVSans", "DejaVuSans.ttf"),
        ("DVSans-Bold", "DejaVuSans-Bold.ttf"),
        ("DVSans-Oblique", "DejaVuSans-Oblique.ttf"),
        ("DVSans-BoldOblique", "DejaVuSans-BoldOblique.ttf"),
    ]
    for name, file in spec:
        pdfmetrics.registerFont(TTFont(name, str(FONTS / file)))
    pdfmetrics.registerFontFamily(
        "DVSerif", normal="DVSerif", bold="DVSerif-Bold",
        italic="DVSerif-Italic", boldItalic="DVSerif-BoldItalic")
    pdfmetrics.registerFontFamily(
        "DVSans", normal="DVSans", bold="DVSans-Bold",
        italic="DVSans-Oblique", boldItalic="DVSans-BoldOblique")
    _registered = True


# ---------------------------------------------------------------------------
# Source parsing into pieces + rounds
# ---------------------------------------------------------------------------
import re  # noqa: E402  (kept late to mirror module layout)

PIECE_RE = re.compile(r"^([A-Z][A-Z &/]+?)\s*\(make (\d+)\)\s*$", re.IGNORECASE)
ROUND_LINE_RE = re.compile(
    r"^(Round|Rnd|Row)\s+(\d+)(?:\s*[-\u2013]\s*(\d+))?\s*[:.]\s*(.*)", re.IGNORECASE
)
STATED_RE = re.compile(r"\s*\((\d+)\)\s*$")


@dataclass
class RoundBlock:
    """One rendered instruction line (or a merged range of identical rounds)."""
    label: str
    text: str
    count: int | None
    note: str | None = None
    piece: str | None = None


def parse_source(source_path: Path):
    """Split the raw pattern into [(piece_title|None, [round lines...])]."""
    lines = [l.strip() for l in source_path.read_text(encoding="utf-8").splitlines()]
    pieces = []
    current = (None, [])
    header_seen = False
    for l in lines:
        if not l:
            continue
        pm = PIECE_RE.match(l)
        if pm and not ROUND_LINE_RE.match(l):
            pieces.append(current)
            current = (pm.group(1).strip().title(), [])
            header_seen = True
            continue
        rm = ROUND_LINE_RE.match(l)
        if rm:
            kind = rm.group(1).lower()
            start = int(rm.group(2))
            end = int(rm.group(3)) if rm.group(3) else start
            text = rm.group(4).strip()
            sm = STATED_RE.search(text)
            stated = int(sm.group(1)) if sm else None
            clean = STATED_RE.sub("", text).strip()
            current[1].append((kind, start, end, clean, stated))
            continue
        # prose lines (bunny intro, assembly steps) are ignored here;
        # assembly is carried in the publisher content module
    pieces.append(current)
    return pieces


def _customer_text(raw: str) -> str:
    """Lightly expand raw instruction wording for beginners.

    Standard abbreviations stay (they are defined in the Abbreviations
    section); awkward phrasing is smoothed out.
    """
    t = raw.strip().rstrip(".")
    t = STATED_RE.sub("", t).strip()
    times = "\u00d7"  # multiplication sign, used as the repeat marker
    subs = [
        (r"\binto magic ring\b", "in a magic ring (MR)"),
        (r"\binto MR\b", "in a magic ring (MR)"),
        (r"\binc in each st around\b", "inc in every stitch around"),
        (r"\bsc in each st around\b", "sc in every stitch around"),
        (r"\bsc in each ch across\b", "sc in every chain across"),
        (r"\bsc in each st across\b", "sc in every stitch across"),
        (r"\bsc in 2nd ch from hook\b", "sc in the 2nd chain from your hook"),
        (r"\bch 40, sl st to join\b", "ch 40, then sl st to join into a ring"),
        (r"\binc x (\d+)", f"inc {times} \\1"),
        (r"\bdec x (\d+)", f"dec {times} \\1"),
        (r"\)\s*x\s*(\d+)\b", f") {times} \\1"),
        (r"\b(sc|hdc|dc|tr|sl st)\s+x\s+(\d+)", f"\\1 {times} \\2"),
    ]
    for pat, rep in subs:
        t = re.sub(pat, rep, t, flags=re.IGNORECASE)
    t = re.sub(r"\s+", " ", t).strip()
    return t + "."


def _range_note(label_unit: str, start: int, end: int) -> str:
    n = end - start + 1
    if n == 2:
        return (f"Work this {label_unit.lower()} twice \u2014 "
                f"{label_unit.lower()}s {start} and {end}.")
    return (f"Work this {label_unit.lower()} {n} times \u2014 "
            f"{label_unit.lower()}s {start} to {end}, keeping the same stitch count.")


def rounds_to_blocks(pieces, unit="Round", special_notes=None):
    """Convert parsed round lines into customer-facing blocks.

    Consecutive identical single rounds are merged into one block
    (e.g. eleven 'sc in each st around (40)' lines become 'Rounds 2-12').
    ``special_notes`` maps (unit, start, end) to a custom helper note.
    """
    special_notes = special_notes or {}
    flat = []
    for piece, rows in pieces:
        for kind, start, end, text, stated in rows:
            flat.append((piece, "Round" if kind in ("round", "rnd") else "Row",
                         start, end, text, stated))
    blocks = []
    i = 0
    while i < len(flat):
        piece, lu, start, end, text, stated = flat[i]
        if end > start:
            n = end - start + 1
            note = _range_note(lu, start, end) if n > 1 else None
            blocks.append(RoundBlock(label=f"{lu}s {start}\u2013{end}",
                                     text=_customer_text(text), count=stated,
                                     note=note, piece=piece))
            i += 1
            continue
        j = i
        while (j + 1 < len(flat)
               and flat[j + 1][0] == piece and flat[j + 1][1] == lu
               and flat[j + 1][3] == flat[j + 1][2]        # next is a single round
               and flat[j + 1][2] == flat[j][2] + 1         # consecutive numbering
               and flat[j + 1][4] == text and flat[j + 1][5] == stated):
            j += 1
        if j > i:
            m_end = flat[j][2]
            key = (lu, start, m_end)
            note = special_notes.get(key, _range_note(lu, start, m_end))
            blocks.append(RoundBlock(label=f"{lu}s {start}\u2013{m_end}",
                                     text=_customer_text(text), count=stated,
                                     note=note, piece=piece))
        else:
            blocks.append(RoundBlock(label=f"{lu} {start}", text=_customer_text(text),
                                     count=stated, note=None, piece=piece))
        i = j + 1
    return blocks


SPECIAL_NOTES = {
    "beginner-scarf": {
        ("Row", 2, 5): ("Repeat rows 2\u20135 until your scarf is as long as you "
                        "want it to be. End on a row that works like row 5."),
    },
}


# ---------------------------------------------------------------------------
# Paragraph styles
# ---------------------------------------------------------------------------
def _styles():
    S = {}
    S["h2"] = ParagraphStyle("h2", fontName="DVSerif-Bold", fontSize=15,
                             leading=19, textColor=INK, spaceBefore=0)
    S["h2no"] = ParagraphStyle("h2no", fontName="DVSans-Bold", fontSize=8,
                               leading=19, textColor=ACCENT)
    S["body"] = ParagraphStyle("body", fontName="DVSans", fontSize=10,
                               leading=15.5, textColor=INK)
    S["overview"] = ParagraphStyle("overview", fontName="DVSerif", fontSize=11.5,
                                   leading=18, textColor=INK)
    S["small"] = ParagraphStyle("small", fontName="DVSans", fontSize=9,
                                leading=13.5, textColor=INK)
    S["muted"] = ParagraphStyle("muted", fontName="DVSans", fontSize=8.5,
                                leading=12.5, textColor=MUTED)
    S["piece"] = ParagraphStyle("piece", fontName="DVSerif-Bold", fontSize=12.5,
                                leading=16, textColor=ACCENT_DARK)
    S["badge"] = ParagraphStyle("badge", fontName="DVSans-Bold", fontSize=7.8,
                                leading=10, textColor=WHITE, alignment=TA_CENTER)
    S["round"] = ParagraphStyle("round", fontName="DVSans", fontSize=10.5,
                                leading=14.5, textColor=INK)
    S["chip"] = ParagraphStyle("chip", fontName="DVSans-Bold", fontSize=8,
                               leading=10.5, textColor=ACCENT_DARK,
                               alignment=TA_CENTER)
    S["note"] = ParagraphStyle("note", fontName="DVSans", fontSize=8.5,
                               leading=12.5, textColor=MUTED)
    S["factv"] = ParagraphStyle("factv", fontName="DVSans-Bold", fontSize=10,
                                leading=13, textColor=INK)
    S["facts"] = ParagraphStyle("facts", fontName="DVSans-Bold", fontSize=8.8,
                                leading=12, textColor=INK)
    S["factk"] = ParagraphStyle("factk", fontName="DVSans", fontSize=7.5,
                                leading=10, textColor=MUTED)
    S["m1"] = ParagraphStyle("m1", fontName="DVSans-Bold", fontSize=9.5,
                             leading=13.5, textColor=ACCENT_DARK)
    S["cell"] = ParagraphStyle("cell", fontName="DVSans", fontSize=9.5,
                               leading=13.5, textColor=INK)
    S["abbr"] = ParagraphStyle("abbr", fontName="DVSans-Bold", fontSize=9.5,
                               leading=13.5, textColor=INK)
    S["cp"] = ParagraphStyle("cp", fontName="DVSans", fontSize=8.5,
                             leading=13.5, textColor=colors.HexColor("#5C554B"))
    S["cph"] = ParagraphStyle("cph", fontName="DVSans-Bold", fontSize=9,
                              leading=13, textColor=INK)
    S["end"] = ParagraphStyle("end", fontName="DVSans", fontSize=9,
                              leading=12, textColor=MUTED, alignment=TA_CENTER)
    return S


def _esc(t) -> str:
    return (str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


# ---------------------------------------------------------------------------
# Flowables
# ---------------------------------------------------------------------------
def _section(st, num, title):
    h = Paragraph(f"<font name='DVSans-Bold' color='#A9622F' size='8'>{num}</font>"
                  f"&nbsp;&nbsp;{title}", st["h2"])
    return [h, HRFlowable(width="14%", thickness=1.6, color=ACCENT, hAlign="LEFT",
                          spaceBefore=2, spaceAfter=8),
            Spacer(1, 2)]


def _facts(st, d):
    def cell(v, k, small=False):
        return [Paragraph(_esc(v), st["facts"] if small else st["factv"]),
                Spacer(1, 2),
                Paragraph(_esc(k).upper(), st["factk"])]
    t = Table([[cell(d["difficulty"], "Difficulty"),
                cell(d["time"], "Estimated time"),
                cell(d["finished_size"], "Finished size", small=True)]],
              colWidths=[(PAGE_W - M_L - M_R) / 3.0] * 3)
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 2),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LINEABOVE", (0, 0), (-1, 0), 0.6, CARD_LINE),
        ("LINEBELOW", (0, -1), (-1, -1), 0.6, CARD_LINE),
    ]))
    return t


def _materials(st, materials):
    w = PAGE_W - M_L - M_R
    rows = [[Paragraph(_esc(k), st["m1"]), Paragraph(_esc(v), st["cell"])]
            for k, v in materials]
    t = Table(rows, colWidths=[w * 0.30, w * 0.70])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4.5),
        ("LINEBELOW", (0, 0), (-1, -2), 0.5, CARD_LINE),
    ]))
    return t


def _gauge(st, text):
    t = Table([[Paragraph(f"<b>Gauge:</b> {_esc(text)}", st["small"])]],
              colWidths=[PAGE_W - M_L - M_R])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CARD),
        ("LINEBEFORE", (0, 0), (0, -1), 3, ACCENT),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return t


def _abbreviations(st, specs):
    w = PAGE_W - M_L - M_R
    rows = []
    for a in specs:
        name = np.ABBREVIATIONS.get(a)
        if name:
            rows.append([Paragraph(_esc(a), st["abbr"]), Paragraph(_esc(name), st["cell"])])
    rows.append([Paragraph("( ) &times; N", st["abbr"]),
                 Paragraph("work the group in brackets N times", st["cell"])])
    rows.append([Paragraph("(N) at line end", st["abbr"]),
                 Paragraph("total stitch count after that round or row", st["cell"])])
    t = Table(rows, colWidths=[w * 0.26, w * 0.74])
    style = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 0), (0, -1), CARD),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4.5),
    ]
    t.setStyle(TableStyle(style))
    return t


def _bullet_table(items, st):
    w = PAGE_W - M_L - M_R
    rows = []
    for it in items:
        rows.append([Paragraph("\u2022", st["note"]),
                     Paragraph(_esc(it), st["small"])])
    t = Table(rows, colWidths=[9, w - 9])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (0, -1), 2),
        ("LEFTPADDING", (1, 0), (1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 1.6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1.6),
    ]))
    return t


def _round_table(st, b: RoundBlock):
    w = PAGE_W - M_L - M_R
    badge_w, chip_w = 64, 50
    text_w = w - badge_w - chip_w
    rows = [[Paragraph(_esc(b.label), st["badge"]),
             Paragraph(_esc(b.text), st["round"]),
             Paragraph(f"{b.count} sts", st["chip"]) if b.count else ""]]
    data = [rows[0]]
    if b.note:
        data.append(["", Paragraph(_esc(b.note), st["note"]), ""])
    t = Table(data, colWidths=[badge_w, text_w, chip_w])
    style = [
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BACKGROUND", (0, 0), (0, 0), ACCENT),
        ("LEFTPADDING", (0, 0), (0, 0), 8),
        ("RIGHTPADDING", (0, 0), (0, 0), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 4.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4.5),
        ("LEFTPADDING", (1, 0), (1, -1), 6),
        ("RIGHTPADDING", (2, 0), (2, -1), 6),
        ("BACKGROUND", (2, 0), (2, 0), CARD),
        ("BOX", (2, 0), (2, 0), 0.5, CARD_LINE),
        ("LEFTPADDING", (2, 0), (2, 0), 4),
        ("RIGHTPADDING", (2, 0), (2, 0), 4),
        ("TOPPADDING", (2, 0), (2, 0), 3),
        ("BOTTOMPADDING", (2, 0), (2, 0), 3),
        ("LINEBELOW", (0, 0), (-1, -2 if b.note else -1), 0.5, CARD_LINE),
        ("SPAN", (1, 1), (2, 1)) if b.note else ("LEFTPADDING", (0, 0), (0, 0), 8),
        ("LEFTPADDING", (1, 1), (1, 1), 16) if b.note else ("LEFTPADDING", (0, 0), (0, 0), 8),
        ("TOPPADDING", (1, 1), (1, 1), 1) if b.note else ("TOPPADDING", (0, 0), (0, 0), 4),
        ("BOTTOMPADDING", (1, 1), (1, 1), 5) if b.note else ("BOTTOMPADDING", (0, 0), (0, 0), 4),
    ]
    t.setStyle(TableStyle([s for s in style if isinstance(s, tuple)]))
    return t


def _steps(st, steps):
    w = PAGE_W - M_L - M_R
    rows = []
    for i, s in enumerate(steps, 1):
        rows.append([Paragraph(str(i), ParagraphStyle(
            "stepn", fontName="DVSans-Bold", fontSize=9.5, leading=13.5,
            textColor=ACCENT_DARK, alignment=TA_CENTER)),
            Paragraph(_esc(s), st["body"])])
    t = Table(rows, colWidths=[16, w - 16])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 2.6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.6),
        ("LEFTPADDING", (1, 0), (1, -1), 6),
    ]))
    return t


def _copyright_box(st):
    parts = np.COPYRIGHT.split("\n\n")
    data = [[Paragraph("COPYRIGHT &amp; LICENCE", st["cph"])], [Spacer(1, 6)]]
    for i, p in enumerate(parts):
        style = st["cph"] if i == 0 else st["cp"]
        data.append([Paragraph(_esc(p), style)])
        if i < len(parts) - 1:
            data.append([Spacer(1, 5)])
    w = PAGE_W - M_L - M_R
    t = Table(data, colWidths=[w])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CARD),
        ("BOX", (0, 0), (-1, -1), 0.5, CARD_LINE),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (0, 0), 12),
        ("BOTTOMPADDING", (0, -1), (0, -1), 12),
    ]))
    return t


# ---------------------------------------------------------------------------
# Page decoration (drawn in onPage callbacks, BEFORE content)
# ---------------------------------------------------------------------------
def _background(c):
    c.saveState()
    c.setFillColor(CREAM)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.restoreState()


def _footer(c, total):
    c.saveState()
    c.setFillColor(MUTED)
    c.setFont("DVSans", 7)
    c.drawString(M_L, 30, "N O V A L I T Y   S T O R E")
    w = c.stringWidth(np.FOOTER_COPY, "DVSans", 7)
    c.drawString((PAGE_W - w) / 2, 30, np.FOOTER_COPY)
    c.drawRightString(PAGE_W - M_R, 30, f"Page {c.getPageNumber()} of {total}")
    c.restoreState()


def _cover(c, cv):
    _background(c)
    c.saveState()
    c.setFillColor(INK)
    c.setFont("DVSans-Bold", 10.5)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 62, "N O V A L I T Y   S T O R E")
    c.setFillColor(ACCENT)
    c.rect(PAGE_W / 2 - 50, PAGE_H - 71, 100, 1.4, fill=1, stroke=0)

    y = PAGE_H - 190
    c.setFillColor(MUTED)
    c.setFont("DVSans", 8.5)
    c.drawCentredString(PAGE_W / 2, y,
                        f"C R O C H E T   P A T T E R N   \u00b7   "
                        f"NOVALITY NO. {cv['number']}")

    # title (wrap to at most two lines)
    lines = textwrap.wrap(cv["title"], width=24) or [cv["title"]]
    c.setFillColor(INK)
    c.setFont("DVSerif-Bold", 30)
    ty = y - 34
    for ln in lines[:2]:
        c.drawCentredString(PAGE_W / 2, ty, ln)
        ty -= 34

    # stitch wave
    wy = ty + 2
    c.setStrokeColor(ACCENT)
    c.setLineWidth(2)
    x0 = PAGE_W / 2 - 105
    for k in range(5):
        sx = x0 + k * 42
        c.bezier(sx, wy, sx + 10.5, wy + 19, sx + 21, wy + 19, sx + 21, wy)
        c.bezier(sx + 21, wy, sx + 31.5, wy - 19, sx + 42, wy - 19, sx + 42, wy)

    ty = wy - 34
    # tagline (wrap to at most two lines)
    for ln in textwrap.wrap(cv["tagline"], width=46)[:2]:
        c.setFillColor(ACCENT_DARK)
        c.setFont("DVSerif-Italic", 12.5)
        c.drawCentredString(PAGE_W / 2, ty, ln)
        ty -= 18

    ty -= 14
    c.setFillColor(MUTED)
    c.setFont("DVSans", 8.5)
    meta = (f"{cv['difficulty']}   \u00b7   about {cv['time']}   \u00b7   "
            f"{cv['finished_size']}")
    for ln in textwrap.wrap(meta, width=64)[:2]:
        c.drawCentredString(PAGE_W / 2, ty, ln)
        ty -= 12

    c.setFont("DVSans", 7)
    c.setFillColor(MUTED)
    c.drawCentredString(PAGE_W / 2, 42, np.FOOTER_COPY)
    c.restoreState()


def _page_count(path: Path) -> int:
    from PyPDF2 import PdfReader
    return len(PdfReader(str(path)).pages)


# ---------------------------------------------------------------------------
# Document assembly
# ---------------------------------------------------------------------------
def build_flowables(d: dict, source_path: Path):
    pieces = parse_source(source_path)
    blocks = rounds_to_blocks(pieces, unit="Round",
                              special_notes=SPECIAL_NOTES.get(d["slug"]))
    missing = [b.label for b in blocks if b.count is None]
    if missing:
        raise ValueError(f"{d['slug']}: rounds without stitch counts: {missing}")
    st = _styles()

    flow = [PageBreak()]  # page 1 is the cover (drawn on canvas)

    flow += _section(st, "01", "Overview")
    flow.append(Paragraph(_esc(d["overview"]), st["overview"]))
    flow.append(Spacer(1, 8))
    flow.append(_facts(st, d))
    flow.append(Spacer(1, 6))

    flow += _section(st, "02", "Materials")
    flow.append(_materials(st, d["materials"]))
    if d.get("gauge"):
        flow.append(Spacer(1, 8))
        flow.append(_gauge(st, d["gauge"]))
    flow.append(Spacer(1, 6))

    flow += _section(st, "03", "Abbreviations")
    flow.append(_abbreviations(st, d["abbreviations"]))
    flow.append(Spacer(1, 6))

    if d.get("notes"):
        flow += _section(st, "04", "Notes")
        flow.append(_bullet_table(d["notes"], st))
        flow.append(Spacer(1, 6))

    flow += _section(st, "05", "Instructions")
    cur_piece = object()
    for b in blocks:
        if b.piece != cur_piece:
            cur_piece = b.piece
            if b.piece:
                flow.append(Paragraph(_esc(b.piece), st["piece"]))
                flow.append(HRFlowable(width="100%", thickness=0.5,
                                       color=CARD_LINE, spaceBefore=0, spaceAfter=5))
        flow.append(KeepTogether([_round_table(st, b)]))
        flow.append(Spacer(1, 2))
    flow.append(Spacer(1, 4))

    flow += _section(st, "06", "Finishing")
    flow.append(_steps(st, d["finishing"]))
    flow.append(Spacer(1, 6))

    flow += _section(st, "07", "Helpful Tips")
    flow.append(_bullet_table(d["tips"], st))
    flow.append(Spacer(1, 14))

    flow.append(KeepTogether([_copyright_box(st)]))
    flow.append(Spacer(1, 12))
    flow.append(Paragraph("\u2014  NOVALITY STORE  \u2014", st["end"]))
    return flow


def render_pdf(d: dict, source_path: Path, out_path: Path) -> Path:
    """Render the pattern booklet.

    Two passes: the first counts pages, the second writes the final PDF with
    correct 'Page X of Y' footers.
    """
    _fonts()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cover = dict(number=d["number"], title=d["title"], tagline=d["tagline"],
                 difficulty=d["difficulty"], time=d["time"],
                 finished_size=d["finished_size"])

    def _build(target: Path, total: int | None):
        doc = SimpleDocTemplate(
            str(target), pagesize=A4,
            leftMargin=M_L, rightMargin=M_R, topMargin=M_T, bottomMargin=M_B,
            title=f"{d['title']} \u2014 {np.BRAND}",
            author=np.BRAND,
            subject="Crochet pattern",
            creator=f"{np.BRAND} pattern publisher",
        )
        doc.build(
            build_flowables(d, source_path),
            onFirstPage=lambda c, _d: _cover(c, cover),
            onLaterPages=(
                (lambda c, _d: (_footer(c, total), _background(c)))
                if total is not None
                else (lambda c, _d: _background(c))
            ),
        )

    tmp = out_path.with_suffix(".count.pdf")
    try:
        _build(tmp, None)
        total = _page_count(tmp)
    finally:
        tmp.unlink(missing_ok=True)
    _build(out_path, total)
    return out_path


def build_one(d: dict, repo_root: Path, out_dir: Path) -> Path:
    source_path = repo_root / d["source"]
    out_name = f"NovalityStore_Pattern_{d['number']}_{d['slug'].replace('-', '')}.pdf"
    return render_pdf(d, source_path, out_dir / out_name)


def build_all(repo_root: Path, out_dir: Path, slug: str | None = None) -> list:
    results = []
    for d in np.PATTERNS:
        if slug and d["slug"] != slug:
            continue
        results.append(build_one(d, repo_root, out_dir))
    return results
