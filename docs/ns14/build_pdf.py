"""Build the full-colour, sale-ready NS 14 pattern PDF.

Single source of truth for every instruction line is NS14_corrected.md (the
validated file): tables are parsed out of it, so the PDF cannot drift from the
verified stitch counts. Layout, colour and cover art are added here.
"""

from __future__ import annotations

import re
from pathlib import Path
from xml.sax.saxutils import escape

from PIL import Image as PILImage
from reportlab.lib.colors import Color, HexColor, white
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    CondPageBreak,
    Frame,
    Image,
    KeepTogether,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.platypus.tableofcontents import TableOfContents

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "NS14_corrected.md"
HERO = ROOT / "assets/ns14_cover_hero.png"
DETAIL = ROOT / "assets/ns14_detail_bobble.png"
OUT = ROOT / "NS14_Bobble_Snowflake_Tree_Skirt.pdf"   # git-ignored; committed copy lives in shop/

W, H = letter                      # 612 x 792 pt
M = 0.62 * inch                    # page margin
CW = W - 2 * M                     # content width

# ----------------------------------------------------------------- palette
FOREST = HexColor("#1E5B3A")
FOREST_DK = HexColor("#123B25")
FOREST_MID = HexColor("#2E7A50")
CREAM = HexColor("#F6EDDA")
OAT = HexColor("#E7D7B8")
CREAM_ROW = HexColor("#F4EAD3")
GREEN_ROW = HexColor("#EFF5EE")
GOLD = HexColor("#C9A227")
GOLD_DK = HexColor("#9A7B14")
BERRY = HexColor("#9E2B25")
BERRY_LT = HexColor("#F7E7E5")
INK = HexColor("#22312A")
GREY = HexColor("#5C6B62")
PAPER = HexColor("#FFFDF8")
RULE = HexColor("#D8CDB6")

pdfmetrics.registerFont(TTFont("DJ", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DJ-B", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DS", "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"))
pdfmetrics.registerFont(TTFont("DS-B", "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"))
registerFontFamily("DJ", normal="DJ", bold="DJ-B", italic="DJ", boldItalic="DJ-B")
registerFontFamily("DS", normal="DS", bold="DS-B", italic="DS", boldItalic="DS-B")

S = {
    "body": ParagraphStyle("body", fontName="DJ", fontSize=9, leading=13.2, textColor=INK,
                           alignment=TA_JUSTIFY, spaceAfter=6),
    "bodyL": ParagraphStyle("bodyL", fontName="DJ", fontSize=9, leading=13.2, textColor=INK,
                            alignment=TA_LEFT, spaceAfter=6),
    "bullet": ParagraphStyle("bullet", parent=None, fontName="DJ", fontSize=9, leading=13,
                             textColor=INK, leftIndent=14, bulletIndent=3, spaceAfter=4,
                             alignment=TA_LEFT),
    "num": ParagraphStyle("num", fontName="DJ", fontSize=9, leading=13, textColor=INK,
                          leftIndent=18, bulletIndent=2, spaceAfter=5, alignment=TA_LEFT),
    "h1": ParagraphStyle("h1", fontName="DS-B", fontSize=17, leading=20, textColor=FOREST,
                         spaceBefore=2, spaceAfter=3),
    "h2": ParagraphStyle("h2", fontName="DS-B", fontSize=12.5, leading=15, textColor=FOREST_DK,
                         spaceBefore=10, spaceAfter=4),
    "h3": ParagraphStyle("h3", fontName="DJ-B", fontSize=10, leading=13, textColor=BERRY,
                         spaceBefore=8, spaceAfter=3),
    "small": ParagraphStyle("small", fontName="DJ", fontSize=7.4, leading=9.6, textColor=GREY),
    "tiny": ParagraphStyle("tiny", fontName="DJ", fontSize=6.8, leading=8.6, textColor=GREY),
    "cell": ParagraphStyle("cell", fontName="DJ", fontSize=7.7, leading=9.7, textColor=INK),
    "cellC": ParagraphStyle("cellC", fontName="DJ", fontSize=7.7, leading=9.7, textColor=INK,
                            alignment=TA_CENTER),
    "cellB": ParagraphStyle("cellB", fontName="DJ-B", fontSize=7.9, leading=9.9, textColor=FOREST_DK,
                            alignment=TA_CENTER),
    "head": ParagraphStyle("head", fontName="DJ-B", fontSize=7.9, leading=9.9, textColor=white),
    "headC": ParagraphStyle("headC", fontName="DJ-B", fontSize=7.9, leading=9.9, textColor=white,
                            alignment=TA_CENTER),
    "callT": ParagraphStyle("callT", fontName="DJ-B", fontSize=9.2, leading=12, textColor=FOREST_DK,
                            spaceAfter=2),
    "callB": ParagraphStyle("callB", fontName="DJ", fontSize=8.6, leading=12, textColor=INK),
    "toc0": ParagraphStyle("toc0", fontName="DJ-B", fontSize=9.6, leading=16, textColor=FOREST_DK),
    "toc1": ParagraphStyle("toc1", fontName="DJ", fontSize=8.8, leading=13.5, textColor=INK,
                           leftIndent=16),
    "cap": ParagraphStyle("cap", fontName="DJ", fontSize=7.2, leading=9.4, textColor=GREY,
                          alignment=TA_CENTER, spaceBefore=2, spaceAfter=8),
}


def md(text: str) -> str:
    """Escape then convert the little markdown we use into ReportLab markup."""
    t = escape(text)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"<i>\1</i>", t)
    return t


# ----------------------------------------------------------------- source
sections: dict[str, list[str]] = {}
cur = "PREAMBLE"
for raw in SRC.read_text(encoding="utf-8").splitlines():
    if raw.startswith("## "):
        cur = raw[3:].strip()
        sections[cur] = []
    elif cur in sections:
        sections[cur].append(raw)

ROWS = []          # (label, us, uk, sts, note)
for line in sections.get("Instructions", []) + sections.get("Construction & techniques", []):
    if line.startswith("| [ ] |"):
        c = [x.strip() for x in line.strip("|").split("|")]
        ROWS.append((c[1], c[2], c[3], c[4], c[5]))
for sec in sections:
    if sec.startswith("Optional surface") or sec.startswith("Scalloped"):
        for line in sections[sec]:
            if line.startswith("| [ ] |"):
                c = [x.strip() for x in line.strip("|").split("|")]
                ROWS.append((c[1], c[2], c[3], c[4], c[5]))

SIZE_ROWS = [
    [x.strip() for x in l.strip("|").split("|")]
    for l in sections.get("Helpful tips", []) if l.startswith("| Mini") or l.startswith("| Standard") or l.startswith("| Large")
]
ABBREV = [
    [x.strip() for x in l.strip("|").split("|")]
    for l in sections.get("Abbreviations (US + UK)", [])
    if l.startswith("|") and not l.startswith("| Abbreviation") and not l.startswith("|---")
]

# ------------------------------------------------------------ cover crop
def cover_crop():
    import tempfile
    out = Path(tempfile.mkstemp(suffix=".jpg")[1])
    im = PILImage.open(HERO).convert("RGB")
    w, h = im.size
    target = W / (5.05 * inch)
    if w / h > target:
        nw = int(h * target)
        im = im.crop(((w - nw) // 2, 0, (w + nw) // 2, h))
    else:
        nh = int(w / target)
        im = im.crop((0, (h - nh) // 2, w, (h + nh) // 2))
    im.save(out, quality=92)
    return out


CROP = cover_crop()

# ------------------------------------------------------------ page furniture
def _footer(cv, doc, page_label=True):
    cv.saveState()
    cv.setStrokeColor(GOLD)
    cv.setLineWidth(1.1)
    cv.line(M, 0.52 * inch, W - M, 0.52 * inch)
    cv.setFont("DJ", 6.9)
    cv.setFillColor(GREY)
    cv.drawString(M, 0.38 * inch, "© 2026 Novality Crochet Studio")
    cv.drawCentredString(W / 2, 0.38 * inch, "Design Code NS 14 · personal & small-batch finished-item licence")
    cv.drawRightString(W - M - 0.34 * inch, 0.38 * inch, "Bobble Snowflake Tree Skirt")
    cv.setFillColor(FOREST)
    cv.circle(W - M - 0.13 * inch, 0.42 * inch, 9, fill=1, stroke=0)
    cv.setStrokeColor(GOLD)
    cv.setLineWidth(0.7)
    cv.circle(W - M - 0.13 * inch, 0.42 * inch, 9, fill=0, stroke=1)
    cv.setFillColor(CREAM)
    cv.setFont("DJ-B", 7.4)
    cv.drawCentredString(W - M - 0.13 * inch, 0.395 * inch, str(doc.page))
    cv.restoreState()


def on_body(cv, doc):
    cv.saveState()
    cv.setFillColor(FOREST)
    cv.rect(0, H - 0.42 * inch, W, 0.42 * inch, fill=1, stroke=0)
    cv.setFillColor(CREAM)
    cv.setFont("DJ-B", 7.6)
    cv.drawString(M, H - 0.275 * inch, "NS 14 · BOBBLE SNOWFLAKE TREE SKIRT")
    cv.setFillColor(OAT)
    cv.setFont("DJ", 7.2)
    cv.drawRightString(W - M, H - 0.275 * inch, "Novality Crochet Studio · US + UK terms")
    cv.setStrokeColor(GOLD)
    cv.setLineWidth(1.6)
    cv.line(0, H - 0.42 * inch, W, H - 0.42 * inch)
    _footer(cv, doc)
    cv.restoreState()


def on_cover(cv, doc):
    cv.saveState()
    cv.setFillColor(PAPER)
    cv.rect(0, 0, W, H, fill=1, stroke=0)
    # top brand band
    cv.setFillColor(FOREST_DK)
    cv.rect(0, H - 0.62 * inch, W, 0.62 * inch, fill=1, stroke=0)
    cv.setFillColor(CREAM)
    cv.setFont("DS-B", 12.5)
    cv.drawString(M, H - 0.40 * inch, "NOVALITY CROCHET STUDIO")
    cv.setFillColor(GOLD)
    cv.setFont("DJ-B", 9)
    cv.drawRightString(W - M, H - 0.395 * inch, "DESIGN CODE NS 14")
    # hero photo
    img_h = 5.05 * inch
    y_top = H - 0.62 * inch
    cv.drawImage(str(CROP), 0, y_top - img_h, width=W, height=img_h)
    cv.setStrokeColor(GOLD)
    cv.setLineWidth(2.2)
    cv.line(0, y_top - img_h, W, y_top - img_h)
    # render disclaimer over photo, bottom-right, sized to its text
    disc = "Illustrative render of the finished design — not a photograph of a sample"
    cv.setFont("DJ", 6.6)
    dw = cv.stringWidth(disc, "DJ", 6.6) + 14
    cv.setFillColor(Color(0.043, 0.145, 0.102, alpha=0.82))
    cv.roundRect(W - 0.16 * inch - dw, y_top - img_h + 0.13 * inch, dw, 0.24 * inch, 4, fill=1, stroke=0)
    cv.setFillColor(CREAM)
    cv.drawRightString(W - 0.23 * inch, y_top - img_h + 0.205 * inch, disc)
    # title panel
    y0 = y_top - img_h
    cv.setFillColor(FOREST)
    cv.rect(0, 0, W, y0, fill=1, stroke=0)
    cv.setFillColor(FOREST_DK)
    cv.rect(0, 0, W, 0.16 * inch, fill=1, stroke=0)
    cv.setFillColor(GOLD)
    cv.setFont("DJ-B", 10.5)
    cv.drawString(M, y0 - 0.52 * inch, "CROCHET PATTERN  ·  FULL-COLOUR EDITION")
    cv.setFillColor(CREAM)
    cv.setFont("DS-B", 40)
    cv.drawString(M - 1, y0 - 1.18 * inch, "Bobble Snowflake")
    cv.setFillColor(OAT)
    cv.setFont("DS-B", 21)
    cv.drawString(M, y0 - 1.62 * inch, "Tree Skirt")
    cv.setStrokeColor(GOLD)
    cv.setLineWidth(1.4)
    cv.line(M, y0 - 1.80 * inch, W - M, y0 - 1.80 * inch)
    # badges
    badges = ["US + UK TERMS", "EASY–INTERMEDIATE", "3 SIZES", "46–109 CM", "5–5.5 MM HOOK"]
    x = M
    y = y0 - 2.16 * inch
    for b in badges:
        wtxt = cv.stringWidth(b, "DJ-B", 7.6) + 16
        cv.setFillColor(FOREST_MID)
        cv.setStrokeColor(GOLD)
        cv.setLineWidth(0.7)
        cv.roundRect(x, y, wtxt, 0.245 * inch, 6, fill=1, stroke=1)
        cv.setFillColor(CREAM)
        cv.setFont("DJ-B", 7.6)
        cv.drawString(x + 8, y + 6.6, b)
        x += wtxt + 7
    # colourway chips
    y = y0 - 2.72 * inch
    cv.setFillColor(OAT)
    cv.setFont("DJ-B", 8)
    cv.drawString(M, y + 0.30 * inch, "NAMED ORIGINAL COLOURWAY")
    for i, (name, hexv) in enumerate([("FOREST GREEN · MC", "#1E5B3A"), ("OAT CREAM · CC", "#E7D7B8")]):
        cx = M + i * 2.5 * inch
        cv.setFillColor(HexColor(hexv))
        cv.setStrokeColor(CREAM)
        cv.setLineWidth(1.6)
        cv.circle(cx + 7, y + 2, 7.5, fill=1, stroke=1)
        cv.setFillColor(CREAM)
        cv.setFont("DJ", 8.2)
        cv.drawString(cx + 20, y - 1, name)
    # blurb in the lower panel
    cv.setFillColor(CREAM)
    cv.setFont("DS-B", 12)
    cv.drawString(M, y0 - 3.42 * inch, "One verified ladder, three stopping points.")
    cv.setFillColor(OAT)
    cv.setFont("DJ", 8.8)
    cv.drawString(M, y0 - 3.68 * inch,
                  "Mini 46–53 cm · Standard 74–84 cm · Large 97–109 cm — each ends on a count divisible by six,")
    cv.drawString(M, y0 - 3.90 * inch,
                  "so the exact scalloped border closes with 28, 46 or 64 complete scallops and no partial shell.")
    # footer line
    cv.setFillColor(OAT)
    cv.setFont("DJ", 7.2)
    cv.drawString(M, 0.42 * inch, "Closed-centre · twelve surface-crochet spokes · bobble round every third round from R5 · exact scalloped border")
    cv.setFillColor(GOLD)
    cv.setFont("DJ-B", 7.2)
    cv.drawRightString(W - M, 0.42 * inch, "#NovalityCrochetStudio")
    cv.restoreState()


def on_back(cv, doc):
    cv.saveState()
    cv.setFillColor(FOREST)
    cv.rect(0, 0, W, H, fill=1, stroke=0)
    cv.setStrokeColor(GOLD)
    cv.setLineWidth(1.6)
    cv.rect(0.35 * inch, 0.35 * inch, W - 0.7 * inch, H - 0.7 * inch, fill=0, stroke=1)
    cv.setFillColor(CREAM)
    cv.setFont("DS-B", 24)
    cv.drawCentredString(W / 2, H - 1.5 * inch, "Thank you for making with us")
    cv.setFillColor(OAT)
    cv.setFont("DJ", 9.4)
    cv.drawCentredString(W / 2, H - 1.95 * inch, "Every NS 14 pattern is checked row by row before release.")
    cv.drawCentredString(W / 2, H - 2.15 * inch, "Counts, repeats and closures are verified against the written rule.")
    cv.setFillColor(GOLD)
    cv.setFont("DJ-B", 9)
    cv.drawCentredString(W / 2, H - 2.85 * inch, "PATTERN BY NOVALITY CROCHET STUDIO · DESIGN CODE NS 14")
    cv.setStrokeColor(GOLD)
    cv.setLineWidth(1)
    cv.line(W / 2 - 1.4 * inch, H - 3.05 * inch, W / 2 + 1.4 * inch, H - 3.05 * inch)
    cv.setFillColor(OAT)
    cv.setFont("DJ", 8.6)
    cv.drawCentredString(W / 2, 5.62 * inch, "Written directions in US + UK terms · a verified count ladder · printable progress boxes")
    cv.drawCentredString(W / 2, 5.38 * inch, "Three sizes · optional twelve surface spokes · an exact scalloped border")
    cv.drawImage(str(DETAIL), W / 2 - 1.85 * inch, 3.0 * inch, width=3.7 * inch, height=2.08 * inch,
                 preserveAspectRatio=True, anchor="c", mask=None)
    cv.setStrokeColor(CREAM)
    cv.setLineWidth(0.8)
    cv.rect(W / 2 - 1.85 * inch, 3.0 * inch, 3.7 * inch, 2.08 * inch, fill=0, stroke=1)
    cv.setFillColor(OAT)
    cv.setFont("DJ", 7.4)
    cv.drawCentredString(W / 2, 2.68 * inch, "Tag your make:  #NovalityCrochetStudio   #NovalityTreeSkirt")
    cv.setFillColor(CREAM)
    cv.setFont("DJ", 6.8)
    cv.drawCentredString(W / 2, 0.62 * inch, "© 2026 Novality Crochet Studio · All rights reserved · Licensed for personal use and small-batch finished-item sale")
    cv.restoreState()


# ------------------------------------------------------------ flowable helpers
def callout(title, body, accent=FOREST, bg=GREEN_ROW):
    inner = [Paragraph(md(title), S["callT"])]
    if body:
        inner.append(Paragraph(md(body), S["callB"]))
    t = Table([[inner]], colWidths=[CW])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("LINEBEFORE", (0, 0), (0, -1), 3.2, accent),
        ("BOX", (0, 0), (-1, -1), 0.5, accent),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return t


def rule(space_before=2, space_after=8):
    t = Table([[""]], colWidths=[CW], rowHeights=[1.4])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), RULE),
                           ("TOPPADDING", (0, 0), (-1, -1), 0),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                           ("LINEBELOW", (0, 0), (-1, -1), 0, RULE)]))
    t.spaceBefore, t.spaceAfter = space_before, space_after
    return t


def section_title(text):
    p = Paragraph(md(text), S["h1"])
    return [p, rule(0, 8)]


def round_table(rows, title=None):
    widths = [0.30 * inch, 0.44 * inch, 2.40 * inch, 2.40 * inch, 0.44 * inch, 1.32 * inch]
    data = [[Paragraph("", S["head"]), Paragraph("Rnd", S["headC"]), Paragraph("US terms", S["head"]),
             Paragraph("UK terms", S["head"]), Paragraph("Sts", S["headC"]), Paragraph("Note", S["head"])]]
    styles = [
        ("BACKGROUND", (0, 0), (-1, 0), FOREST),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.4, RULE),
        ("LINEBELOW", (0, 0), (-1, 0), 1.2, GOLD),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3.4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.4),
    ]
    for i, (label, us, uk, sts, note) in enumerate(rows, start=1):
        bobble = "BO in next st" in us
        size_stop = any(k in note for k in ("MINI SIZE", "STANDARD SIZE", "LARGE SIZE"))
        us_html = md(us).replace("BO in next st", '<b><font color="#9A7B14">BO</font> in next st</b>')
        us_html = re.sub(r"\((\d+)\)", r'<b><font color="#1E5B3A">(\1)</font></b>', us_html)
        uk_html = re.sub(r"\((\d+)\)", r'<b><font color="#1E5B3A">(\1)</font></b>', md(uk))
        sts_html = re.sub(r"\((\d+)\)", r'<b><font color="#1E5B3A">(\1)</font></b>', md(sts))
        note_html = md(note)
        if size_stop:
            note_html = f'<b><font color="#9E2B25">{note_html}</font></b>'
        data.append([
            "", Paragraph(f"<b>{label}</b>", S["cellC"]),
            Paragraph(us_html, S["cell"]), Paragraph(f'<font color="#41604E">{uk_html}</font>', S["cell"]),
            Paragraph(sts_html, S["cellC"]), Paragraph(note_html, S["cell"]),
        ])
        bg = CREAM_ROW if bobble else (OAT if size_stop or label in ("Ring", "Border", "Spoke", "Repeat") else GREEN_ROW)
        styles.append(("BACKGROUND", (0, i), (-1, i), bg))
        styles.append(("BOX", (0, i), (0, i), 0.7, FOREST))   # the printable progress box
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle(styles))
    return t


def zebra_table(rows, widths, head_bg=FOREST, first_bold=True):
    data = []
    for r_i, r in enumerate(rows):
        data.append([Paragraph((f"<b>{md(c)}</b>" if (first_bold and c_i == 0) else md(c)),
                               S["head"] if r_i == 0 else S["cell"])
                     for c_i, c in enumerate(r)])
    styles = [
        ("BACKGROUND", (0, 0), (-1, 0), head_bg),
        ("LINEBELOW", (0, 0), (-1, 0), 1.2, GOLD),
        ("GRID", (0, 0), (-1, -1), 0.4, RULE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 3.6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.6),
    ]
    for i in range(1, len(rows)):
        styles.append(("BACKGROUND", (0, i), (-1, i), GREEN_ROW if i % 2 else CREAM_ROW))
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle(styles))
    return t


def figure(path, w, caption):
    im = Image(str(path))
    iw, ih = im.imageWidth, im.imageHeight
    h = w * ih / iw
    im.drawWidth, im.drawHeight = w, h
    im.hAlign = "CENTER"
    return [im, Paragraph(md(caption), S["cap"])]


def chips(pairs):
    """Colourway chips: list of (name, role, hex)."""
    cells = []
    for name, role, hexv in pairs:
        box = Table([[Paragraph(f"<b>{name}</b><br/><font size=7 color='#5C6B62'>{role}</font>",
                                ParagraphStyle("chip", fontName="DJ", fontSize=8.4, leading=11,
                                               textColor=INK))]],
                    colWidths=[CW / len(pairs) - 6])
        box.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), PAPER),
            ("LINEBEFORE", (0, 0), (0, -1), 8, HexColor(hexv)),
            ("BOX", (0, 0), (-1, -1), 0.5, RULE),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ]))
        cells.append(box)
    t = Table([cells], colWidths=[CW / len(pairs)] * len(pairs))
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("LEFTPADDING", (0, 0), (-1, -1), 3),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 3)]))
    return t


# ------------------------------------------------------------ document
class Doc(BaseDocTemplate):
    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph):
            if flowable.style.name == "h1":
                self.notify("TOCEntry", (0, flowable.getPlainText(), self.page))
            elif flowable.style.name == "h2":
                self.notify("TOCEntry", (1, flowable.getPlainText(), self.page))


frame_body = Frame(M, 0.72 * inch, CW, H - 0.72 * inch - 0.62 * inch, id="body",
                   leftPadding=0, rightPadding=0, topPadding=6, bottomPadding=0)
frame_empty = Frame(0, 0, W, H, id="empty", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)

doc = Doc(str(OUT), pagesize=letter, leftMargin=M, rightMargin=M, topMargin=0.62 * inch,
          bottomMargin=0.72 * inch, title="NS 14 Bobble Snowflake Tree Skirt",
          author="Novality Crochet Studio", subject="Crochet pattern, full-colour edition")
doc.addPageTemplates([
    PageTemplate(id="cover", frames=[frame_empty], onPage=on_cover),
    PageTemplate(id="body", frames=[frame_body], onPage=on_body),
    PageTemplate(id="back", frames=[frame_empty], onPage=on_back),
])

story = [Spacer(1, 1), NextPageTemplate("body"), PageBreak()]

# ---------------------------------------------------------------- p2 welcome
story += section_title("Welcome to Bobble Snowflake")
story.append(Paragraph(
    md("A closed-centre, twelve-spoke double-crochet circle with a contrast bobble round every third round "
       "from R5. Choose the mini, standard or large stopping point, add twelve optional surface-crochet "
       "spokes, then finish with an exact scalloped border. Every construction row carries a printable "
       "**[ ]** progress box and a stated count — tick the box only after the count matches."), S["body"]))
story.extend(figure(DETAIL, 4.5 * inch,
                    "Oat cream five-dc bobbles and the scalloped shell edge, worked over forest green dc. "
                    "Artwork is illustrative of the written design."))
story.append(callout("What is inside this pattern",
                     "Written directions in US and UK terms side by side · a verified count ladder from the "
                     "12-dc centre ring to 384 stitches · three stopping sizes · an optional twelve-spoke "
                     "surface route · an exact scalloped border · gauge, blocking, finishing, troubleshooting, "
                     "four colourways, care and the full licence."))
story.append(Spacer(1, 8))
story.append(Paragraph(md("Pattern profile"), S["h2"]))
story.append(zebra_table([
    ["Format", "US + UK terms, side by side"],
    ["Skill level", "Easy–intermediate"],
    ["Active time", "Unverified — record your own sample time"],
    ["Finished size (target, verify)", "Mini 46–53 cm · Standard 74–84 cm · Large 97–109 cm"],
    ["Yarn", "Worsted / aran (#4): forest green MC, oat cream CC"],
    ["Hook", "5–5.5 mm (US H/8–I/9), or size to meet gauge"],
    ["Construction", "Closed joined rounds, worked without turning"],
], [1.55 * inch, CW - 1.55 * inch]))
story.append(Spacer(1, 10))
story.append(chips([("FOREST GREEN", "MC · every non-bobble growth round", "#1E5B3A"),
                    ("OAT CREAM", "CC · bobble rounds, spokes + border", "#E7D7B8")]))
story.append(Spacer(1, 12))
story.append(callout("How to work from this edition",
                     "Tick each **[ ]** box only after the row's stated count matches your work. The US "
                     "instruction sits on the left of every row and its UK equivalent on the right — work from "
                     "one column only. If a count differs, stop and recount the round before continuing; do not "
                     "add or drop stitches to force a number.", accent=FOREST_MID))

# ---------------------------------------------------------------- p3 contents
story.append(PageBreak())
story += section_title("Contents")
toc = TableOfContents()
toc.levelStyles = [S["toc0"], S["toc1"]]
story.append(toc)
story.append(Spacer(1, 12))
story.append(callout("Read before making",
                     "Read every component and finishing note before beginning. Mark completed rows, confirm "
                     "the count at each row end, and stop immediately if your count differs. Complete the "
                     "centre-ring join, the optional surface spokes and the border in that order, and weave "
                     "every tail while the centre opening is still open and accessible.",
                     accent=GOLD_DK, bg=CREAM_ROW))
story.append(Spacer(1, 8))
story.append(Paragraph(md("Diagrams and illustrations support orientation only; the numbered written "
                          "directions control construction. Artwork in this edition is illustrative and was "
                          "not photographed from a completed sample."), S["small"]))

# ---------------------------------------------------------------- safety
story.append(PageBreak())
story += section_title("Safety — read this first")
story.append(callout("This design is home decor, not a toy",
                     "It is not flameproof. Keep it away from candles, fireplaces, heaters, hot lamps and "
                     "every ignition source. Use only cool-running lights approved for the tree and location. "
                     "Do not cover plugs, adapters, power strips or electrical connections with the skirt, and "
                     "route cords so the skirt cannot pull on them.", accent=BERRY, bg=BERRY_LT))
story.append(Spacer(1, 8))
story.append(callout("Fit and placement",
                     "Keep the skirt clear of walking routes where its edge could cause a trip or slip. It must "
                     "not support, level or stabilize a tree stand. Fit the closed centre without obstructing "
                     "the stand, water reservoir, fasteners or manufacturer-required clearances. Inspect the "
                     "skirt for loose surface stitches, stretched joins and snagged yarn before each season, "
                     "and supervise children and animals around the complete tree arrangement.",
                     accent=BERRY, bg=BERRY_LT))
story.append(Spacer(1, 8))
story.append(callout("No certified claim is made",
                     "No finished NS 14 skirt has been independently crocheted, fit-tested, wash-tested, "
                     "assessed for flammability or shown by Novality Crochet Studio to comply with a "
                     "product-safety regime. Before sale or supply, the finished-item maker or seller must "
                     "determine the applicable classification, assessment, testing, documentation, labelling "
                     "and traceability duties for every destination market.", accent=BERRY, bg=BERRY_LT))

# ---------------------------------------------------------------- materials
story.append(PageBreak())
story += section_title("Materials")
for line in sections["Materials"]:
    if line.startswith("- Worsted"):
        story.append(Paragraph(md(line[2:]), S["bullet"]), )
        story[-1].bulletText = "•"
    elif line.startswith("- Planning quantities"):
        story.append(callout("Planning quantities — estimate, not a weighed result", line[2:],
                             accent=GOLD_DK, bg=CREAM_ROW))
        story.append(Spacer(1, 6))
    elif line.startswith("- "):
        p = Paragraph(md(line[2:]), S["bullet"])
        p.bulletText = "•"
        story.append(p)
story.append(Spacer(1, 10))
story.append(Paragraph(md("Estimated yarn by size (3–4 in of worsted per US dc; a 5-dc bobble uses five dc of "
                          "yarn while counting as one stitch; spokes and border included):"), S["small"]))
story.append(Spacer(1, 4))
story.append(zebra_table([
    ["Size", "Stop", "Growth stitches", "Est. total yarn", "Plan CC share"],
    ["Mini / tabletop", "R14", "1,260", "70–95 g", "about 52 %"],
    ["Standard", "R23", "3,312", "165–225 g", "about 47 %"],
    ["Large", "R32", "6,336", "305–410 g", "about 44 %"],
], [1.5 * inch, 0.7 * inch, 1.5 * inch, 1.7 * inch, CW - 5.4 * inch], head_bg=FOREST_MID))

# ---------------------------------------------------------------- gauge
story.append(PageBreak())
story += section_title("Gauge & size")
for line in sections["Gauge & size"]:
    if not line.strip():
        continue
    if line.startswith("- **R"):
        m = re.match(r"- \*\*(R\d+):\*\* (.*)", line)
        p = Paragraph(f"<b><font color='#1E5B3A'>{m.group(1)}</font></b>  {md(m.group(2))}", S["bullet"])
        p.bulletText = "•"
        story.append(p)
    elif line.startswith("The radial figure"):
        story.append(callout("Why the radial gauge is derived, not independent", line, accent=FOREST))
        story.append(Spacer(1, 6))
    elif line.startswith("The scallops"):
        story.append(callout("Border depth and the mini target", line, accent=GOLD_DK, bg=CREAM_ROW))
    else:
        story.append(Paragraph(md(line), S["body"]))
story.append(Spacer(1, 8))
story.append(callout("Circular gauge swatch",
                     "Make the centre ring and work through R6 as a circular gauge piece; let it rest before "
                     "measuring. Match 12 stitches = 4 in / 10 cm across the stitch direction first, then "
                     "confirm the circle lies flat. A rectangular swatch alone does not verify how this "
                     "twelve-increase circle will lie.", accent=FOREST_MID))

# ---------------------------------------------------------------- abbreviations
story.append(PageBreak())
story += section_title("Abbreviations (US + UK)")
rows = [["Abbreviation", "Meaning"]] + ABBREV
story.append(zebra_table(rows, [1.5 * inch, CW - 1.5 * inch]))
story.append(Spacer(1, 10))
story.append(callout("How to read the two columns",
                     "Every construction round appears twice side by side: the US instruction on the left, its "
                     "UK equivalent on the right. Stitch counts are identical. Prose explanations use US terms "
                     "unless both names are shown.", accent=FOREST_MID))

# ---------------------------------------------------------------- techniques
story.append(PageBreak())
story += section_title("Construction & techniques")
story.append(callout("Joined rounds without turning",
                     "The starting ch 2 never counts as a stitch. Work the first dc or BO into the SAME stitch "
                     "as the join, mark it, and slip stitch to that marked stitch at round end. Do not work "
                     "into the ch 2 or joining slip stitch.", accent=FOREST))
story.append(Spacer(1, 8))
tech = [l for l in sections["Construction & techniques"] if re.match(r"^\d+\. ", l)]
titles = ["Fit the closed centre first", "Twelve-repeat circle", "Five-dc bobble",
          "Original colour route", "Track the increase columns", "Surface slip stitch"]
for i, (t, line) in enumerate(zip(titles, tech), 1):
    body = re.sub(r"^\d+\. \*\*.*?\*\*\s*", "", line)
    card = Table([[Paragraph(f"<b>{i}</b>", ParagraphStyle("n", fontName="DS-B", fontSize=15,
                                                           textColor=white, alignment=TA_CENTER)),
                   [Paragraph(f"<b>{t}</b>", S["callT"]), Paragraph(md(body), S["callB"])]]],
                 colWidths=[0.42 * inch, CW - 0.42 * inch])
    card.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), FOREST),
        ("BACKGROUND", (1, 0), (1, 0), GREEN_ROW if i % 2 else CREAM_ROW),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BOX", (0, 0), (-1, -1), 0.5, RULE),
        ("LEFTPADDING", (1, 0), (1, 0), 9),
        ("RIGHTPADDING", (1, 0), (1, 0), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    story.append(card)
    story.append(Spacer(1, 6))

# ---------------------------------------------------------------- instructions
story.append(PageBreak())
story += section_title("Instructions")
story.append(Paragraph(md("**1 · Skirt — centre ring and growth rounds.** Ch 2 starts every round and is never "
                          "counted. Work the first dc — or first BO on a bobble round — into the same stitch as "
                          "the join, then end with a slip stitch to that first actual stitch. Count after every "
                          "repeat and at the end of every round."), S["body"]))
story.append(Spacer(1, 4))
story.append(Paragraph(md("Legend: <font color='#9A7B14'><b>cream rows</b></font> = bobble round worked in CC · "
                          "<font color='#2E7A50'><b>green rows</b></font> = plain round worked in MC · the "
                          "outlined square in the first column is your printable progress box."), S["small"]))
story.append(Spacer(1, 6))

groups = [
    ("Centre ring", [r for r in ROWS if r[0] == "Ring"]),
    ("Rounds 1–8", [r for r in ROWS if re.match(r"R([1-8])$", r[0])]),
    ("Rounds 9–16", [r for r in ROWS if re.match(r"R(9|1[0-6])$", r[0])]),
    ("Rounds 17–24", [r for r in ROWS if re.match(r"R(1[7-9]|2[0-4])$", r[0])]),
    ("Rounds 25–32", [r for r in ROWS if re.match(r"R(2[5-9]|3[0-2])$", r[0])]),
]
for gi, (title, rows) in enumerate(groups):
    block = [Paragraph(md(title), S["h2"]), Spacer(1, 3), round_table(rows)]
    if title == "Rounds 9–16":
        block += [Spacer(1, 8), callout("Count check for the R11-to-R12 step",
                                        "R11 consumes 10 old stitches per repeat — 1 BO + 8 plain dc + 1 increase "
                                        "anchor — and produces 11, giving 132 stitches. R12 then consumes 11 old "
                                        "stitches per repeat — 10 plain dc + 1 increase anchor — and produces 12, "
                                        "giving 144 stitches. R12 therefore requires 10 plain dc, not 9, before the "
                                        "increase; using 9 would leave 12 old stitches unworked and produce only "
                                        "132 stitches.",
                                        accent=GOLD_DK, bg=CREAM_ROW)]
    story.append(KeepTogether(block))
    story.append(Spacer(1, 12))

# ---------------------------------------------------------------- spokes
story.append(PageBreak())
story += section_title("Optional surface snowflake spokes")
story.append(Paragraph(md("Work before the border. Leave the 12 outer increase-column markers in place. On the "
                          "right side, pin or lay a straight radial guide from the foundation ring to each "
                          "marker. Use a separate CC length for every spoke; do not carry yarn from one outer "
                          "edge back to the centre."), S["body"]))
story.append(Spacer(1, 4))
story.append(round_table([r for r in ROWS if r[0] in ("Spoke", "Repeat")]))
story.append(Spacer(1, 8))
story.append(Paragraph(md("Surface stitches decorate the fabric and do not replace or add to the growth-round "
                          "counts. Their exact number varies with size and placement. After every spoke, lay the "
                          "skirt flat; if the spoke shortens the radius or puckers the body, remove it and remake "
                          "it more loosely or with the main hook."), S["body"]))

# ---------------------------------------------------------------- border
story.append(PageBreak())
story += section_title("Scalloped border")
story.append(Paragraph(md("Work the border into the final growth round only after the size and optional spokes "
                          "are approved."), S["body"]))
story.append(Spacer(1, 4))
story.append(round_table([r for r in ROWS if r[0] == "Border"]))
story.append(Spacer(1, 8))
story.append(callout("Why it closes exactly",
                     "Each repeat consumes six final-round anchors and produces six worked stitches: one sc plus "
                     "a five-dc shell. R14 gives 168 ÷ 6 = 28 scallops; R23 gives 276 ÷ 6 = 46; R32 gives 384 ÷ 6 "
                     "= 64. The stitch you join into is taken by the final skip of the last repeat, so the closing "
                     "slip stitch lands one stitch past the join — that is correct and it is what makes the repeat "
                     "close. If the repeat does not close exactly, undo the border and correct the final-round "
                     "count rather than changing the last scallop.", accent=FOREST))

# ---------------------------------------------------------------- sizes
story.append(PageBreak())
story += section_title("Sizes at a glance")
story.append(zebra_table([["Size", "Stop after round", "Stitches", "Border scallops", "Unverified finished target"]]
                         + SIZE_ROWS,
                         [1.35 * inch, 1.25 * inch, 0.9 * inch, 1.25 * inch, CW - 4.75 * inch],
                         head_bg=FOREST_MID))
story.append(Spacer(1, 10))
story.append(callout("The count rule",
                     "Round N always consumes N − 1 existing stitches and produces N stitches in each of 12 "
                     "repeats. On a plain round that is N − 2 plain dc plus one increase; on a bobble round, one "
                     "of those plain dc is replaced by one BO. This rule verifies the printed ladder but does not "
                     "authorize untested extra sizes or altered increase rates.", accent=FOREST))
story.append(Spacer(1, 8))
story.append(callout("Bobble rounds",
                     "R5, R8, R11, R14, R17, R20, R23, R26, R29 and R32 — every third round from R5. All three "
                     "size stops land on a bobble round, so the final growth round is always worked in CC and the "
                     "border joins into CC.", accent=GOLD_DK, bg=CREAM_ROW))
story.append(Spacer(1, 8))
story.append(Paragraph(md("No active-time claim is supplied. Record hands-on time separately for the selected "
                          "size, optional spokes, border, finishing and blocking before publishing an estimate."),
                       S["small"]))

# ---------------------------------------------------------------- finishing
story.append(PageBreak())
story += section_title("Finishing & assembly")
items = [l for l in sections["Finishing & assembly"] if re.match(r"^\d+\. ", l)]
for i, line in enumerate(items, 1):
    p = Paragraph(md(re.sub(r"^\d+\. ", "", line)), S["num"])
    p.bulletText = f"{i}."
    story.append(p)

# ---------------------------------------------------------------- troubleshooting
story.append(PageBreak())
story += section_title("Troubleshooting")
for line in sections["Troubleshooting"]:
    m = re.match(r"- \*\*(.+?):\*\* (.*)", line)
    if not m:
        continue
    card = Table([[Paragraph(f"<b>{md(m.group(1))}</b>",
                             ParagraphStyle("tp", fontName="DJ-B", fontSize=8.6, leading=11, textColor=BERRY)),
                   Paragraph(md(m.group(2)), S["callB"])]],
                 colWidths=[1.55 * inch, CW - 1.55 * inch])
    card.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BERRY_LT),
        ("LINEBEFORE", (0, 0), (0, -1), 3.2, BERRY),
        ("BOX", (0, 0), (-1, -1), 0.5, BERRY),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(card)
    story.append(Spacer(1, 6))

# ---------------------------------------------------------------- colourways
story.append(PageBreak())
story += section_title("Colourways")
story.append(chips([("FOREST GREEN", "MC · every non-bobble growth round", "#1E5B3A"),
                    ("OAT CREAM", "CC · bobble rounds, spokes + border", "#E7D7B8")]))
story.append(Spacer(1, 10))
story.append(Paragraph(md("Original colourway: forest green MC for R1–R4 and all later non-bobble growth rounds; "
                          "oat cream CC for each complete bobble round, all 12 optional surface spokes and the "
                          "scalloped border. Use comparable worsted/aran yarns so colour changes do not alter "
                          "gauge."), S["body"]))
story.append(Paragraph(md("Alternative palettes"), S["h3"]))
story.append(chips([("SNOW WHITE + DEEP RED", "white MC · red CC", "#F4F1EA"),
                    ("NAVY + SILVER-GREY", "navy MC · silver CC", "#22304A"),
                    ("SINGLE-COLOUR CREAM", "MC and CC, same yarn", "#EFE6D2")]))
story.append(Spacer(1, 10))
story.append(Paragraph(md("Metallic filament, sequins, beads and battery-light additions are not part of this "
                          "pattern and require separate handling, care and safety review."), S["small"]))

# ---------------------------------------------------------------- care
story.append(PageBreak())
story += section_title("Care & storage")
for line in sections["Care & storage"]:
    if line.strip():
        story.append(Paragraph(md(line), S["body"]))

# ---------------------------------------------------------------- terms
story.append(PageBreak())
story += section_title("Terms of Use")
for sec_name in ["Copyright & ownership", "You may", "You may not", "Safety reminder"]:
    story.append(Paragraph(md(sec_name), S["h2"]))
    for line in sections.get(sec_name, []):
        if line.strip():
            story.append(Paragraph(md(line), S["body"]))
story.append(Spacer(1, 6))
story.append(callout("Credit your finished makes",
                     'Listings for finished skirts must credit "Pattern by Novality Crochet Studio · Design '
                     'Code NS 14" and must not claim unverified safety, testing, size, yarn quantity, fit or '
                     "care results. Tag your projects with #NovalityCrochetStudio and #NovalityTreeSkirt.",
                     accent=GOLD_DK, bg=CREAM_ROW))

# ---------------------------------------------------------------- checklist
story.append(PageBreak())
story += section_title("Finish checklist")
checks = [
    "Centre ring fits the stand relaxed; join and ends secured",
    "Every growth round counted; 12 increase columns aligned",
    "Final count confirmed: 168 / 276 / 384",
    "Optional spokes: 12 separate routes, no puckering or floats",
    "Border closed: 28 / 46 / 64 complete scallops",
    "Blocked dimensions recorded; stand and cord clearances checked",
]
rows = [["", item] for item in checks]
t = Table([[Paragraph("", S["cell"]), Paragraph(md(c), S["cell"])] for c in checks],
          colWidths=[0.34 * inch, CW - 0.34 * inch])
styles = [("GRID", (0, 0), (0, -1), 0.9, FOREST),
          ("LINEBELOW", (0, 0), (-1, -2), 0.4, RULE),
          ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
          ("TOPPADDING", (0, 0), (-1, -1), 7),
          ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
          ("LEFTPADDING", (0, 0), (-1, -1), 6)]
for i in range(len(checks)):
    styles.append(("BACKGROUND", (0, i), (-1, i), GREEN_ROW if i % 2 == 0 else CREAM_ROW))
t.setStyle(TableStyle(styles))
story.append(t)
story.append(Spacer(1, 14))
story.append(Paragraph(md("Project notes"), S["h2"]))
notes = Table([[""] for _ in range(9)], colWidths=[CW], rowHeights=[0.34 * inch] * 9)
notes.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, -2), 0.5, RULE),
                           ("BACKGROUND", (0, 0), (-1, -1), PAPER)]))
story.append(notes)
story.append(Spacer(1, 10))
story.append(Paragraph(md("Novality Crochet Studio · NS 14 · keep this page with your project notes."), S["small"]))

story.append(NextPageTemplate("back"))
story.append(PageBreak())
story.append(Spacer(1, 1))

doc.multiBuild(story)
print("wrote", OUT)
