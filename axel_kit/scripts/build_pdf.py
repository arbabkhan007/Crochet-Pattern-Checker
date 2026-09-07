"""Build the designed Axel the Axolotl pattern PDF with ReportLab.

Usage:  python build_pdf.py  (writes ../Axel_the_Axolotl_Pattern.pdf)
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from PIL import Image as PILImage
import io
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Flowable, Frame, Image, KeepTogether, NextPageTemplate,
                                PageBreak, PageTemplate, Paragraph, Spacer, Table, TableStyle)

sys.path.insert(0, str(Path(__file__).parent))
import pattern_data as P  # noqa: E402

KIT = Path(__file__).resolve().parent.parent
IMG = KIT / "assets" / "img_pdf"
FONTS = KIT / "assets" / "fonts"
OUT = KIT / "Axel_the_Axolotl_Pattern.pdf"

# ------------------------------------------------------------------ palette
PINK = colors.HexColor("#E8A9B8")       # main accent
PINK_DEEP = colors.HexColor("#B8506F")  # gills / fin accent
PINK_PALE = colors.HexColor("#FBEEF1")  # panel fills
CREAM = colors.HexColor("#FFFBF7")      # page background
INK = colors.HexColor("#3B2F33")        # body text
INK_SOFT = colors.HexColor("#7A6A70")   # secondary text
MINT = colors.HexColor("#8FCFC0")       # tiny secondary accent
RULE = colors.HexColor("#EBD7DD")

# ------------------------------------------------------------------ fonts
pdfmetrics.registerFont(TTFont("Fredoka", str(FONTS / "FredokaOne-Regular.ttf")))
pdfmetrics.registerFont(TTFont("Sans", str(FONTS / "SourceSansPro-Regular.ttf")))
pdfmetrics.registerFont(TTFont("Sans-Bold", str(FONTS / "SourceSansPro-Bold.ttf")))
pdfmetrics.registerFont(TTFont("Sans-Semi", str(FONTS / "SourceSansPro-Semibold.ttf")))
pdfmetrics.registerFont(TTFont("Sans-It", str(FONTS / "SourceSansPro-It.ttf")))
pdfmetrics.registerFont(TTFont("Sans-Light", str(FONTS / "SourceSansPro-Light.ttf")))
pdfmetrics.registerFont(TTFont("Serif-It", str(FONTS / "Caladea-Italic.ttf")))
pdfmetrics.registerFont(TTFont("Serif", str(FONTS / "Caladea-Regular.ttf")))
pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-Bold", italic="Sans-It", boldItalic="Sans-Bold")

PAGE_W, PAGE_H = A4
MARGIN = 18 * mm

# ------------------------------------------------------------------ styles
def st(name, **kw):
    base = dict(fontName="Sans", fontSize=10.2, leading=14.5, textColor=INK, spaceAfter=4)
    base.update(kw)
    return ParagraphStyle(name, **base)

S = {
    "body": st("body"),
    "body_small": st("body_small", fontSize=9, leading=12.5, textColor=INK_SOFT),
    "lead": st("lead", fontName="Serif-It", fontSize=12.5, leading=18, textColor=INK_SOFT, spaceAfter=8),
    "h1": st("h1", fontName="Fredoka", fontSize=26, leading=30, textColor=PINK_DEEP, spaceBefore=2, spaceAfter=6),
    "h2": st("h2", fontName="Fredoka", fontSize=15, leading=19, textColor=PINK_DEEP, spaceBefore=10, spaceAfter=4),
    "kicker": st("kicker", fontName="Sans-Semi", fontSize=8.5, leading=11, textColor=PINK_DEEP, spaceAfter=2),
    "caption": st("caption", fontName="Sans-It", fontSize=8.5, leading=11, textColor=INK_SOFT, alignment=TA_CENTER),
    "cell": st("cell", fontSize=9.6, leading=12, spaceAfter=0),
    "cell_b": st("cell_b", fontName="Sans-Semi", fontSize=9.6, leading=12, spaceAfter=0),
    "cell_note": st("cell_note", fontName="Sans-It", fontSize=8.6, leading=11, textColor=INK_SOFT, spaceAfter=0),
    "cell_count": st("cell_count", fontName="Fredoka", fontSize=10, leading=12, textColor=PINK_DEEP, alignment=TA_CENTER, spaceAfter=0),
    "bullet": st("bullet", leftIndent=10, bulletIndent=0),
    "cover_title": st("cover_title", fontName="Fredoka", fontSize=44, leading=48, textColor=colors.white, alignment=TA_LEFT, spaceAfter=4),
    "cover_sub": st("cover_sub", fontName="Serif-It", fontSize=16, leading=20, textColor=colors.white, spaceAfter=10),
    "cover_meta": st("cover_meta", fontName="Sans-Semi", fontSize=10.5, leading=14, textColor=colors.white),
    "toc": st("toc", fontSize=11, leading=17),
    "big_number": st("big_number", fontName="Fredoka", fontSize=22, leading=24, textColor=PINK_DEEP, alignment=TA_CENTER, spaceAfter=0),
    "stat_label": st("stat_label", fontName="Sans-Semi", fontSize=8, leading=10, textColor=INK_SOFT, alignment=TA_CENTER, spaceAfter=0),
}


# ------------------------------------------------------------------ custom flowables
class Rule(Flowable):
    def __init__(self, width=None, color=RULE, thickness=0.8, space=6):
        super().__init__(); self.w = width; self.color = color; self.t = thickness; self.space = space
    def wrap(self, aw, ah): self.w = self.w or aw; return self.w, self.t + self.space * 2
    def draw(self):
        self.canv.setStrokeColor(self.color); self.canv.setLineWidth(self.t)
        self.canv.line(0, self.space, self.w, self.space)


class Panel(Flowable):
    """Rounded soft panel with a title bar and wrapped body flowables."""
    def __init__(self, title, flowables, fill=PINK_PALE, accent=PINK_DEEP, pad=9, width=None):
        super().__init__(); self.title = title; self.items = flowables; self.fill = fill; self.accent = accent
        self.pad = pad; self.width = width; self._h = 0; self._parts = []
    def wrap(self, aw, ah):
        self.width = self.width or aw
        inner = self.width - 2 * self.pad
        h = self.pad + (14 if self.title else 0)
        self._parts = []
        for f in self.items:
            w, fh = f.wrap(inner, ah); self._parts.append((f, fh)); h += fh
        h += self.pad
        self._h = h
        return self.width, h
    def draw(self):
        c = self.canv
        c.saveState()
        c.setFillColor(self.fill); c.setStrokeColor(self.fill)
        c.roundRect(0, 0, self.width, self._h, 6, fill=1, stroke=0)
        c.setFillColor(self.accent); c.roundRect(0, 0, 4, self._h, 2, fill=1, stroke=0)
        y = self._h - self.pad
        if self.title:
            c.setFont("Fredoka", 10.5); c.setFillColor(self.accent)
            c.drawString(self.pad + 4, y - 9, self.title.upper()); y -= 14
        for f, fh in self._parts:
            y -= fh; f.drawOn(c, self.pad + 4, y)
        c.restoreState()


class ShapeStrip(Flowable):
    """Silhouette chart of the body: one bar per round, width proportional to stitch count.
    Layout (bottom -> top): caption (10pt) | round labels (10pt) | bars (self.h) | counts (10pt)."""
    CAP, LBL, TOP = 12, 11, 11
    def __init__(self, rounds, width, height=60):
        super().__init__(); self.rounds = rounds; self.w = width; self.h = height
    def wrap(self, aw, ah): return self.w, self.h + self.CAP + self.LBL + self.TOP
    def draw(self):
        c = self.canv
        n = len(self.rounds); maxc = max(r[2] for r in self.rounds)
        slot = self.w / n
        base = self.CAP + self.LBL            # bottom of the bar area
        mid = base + self.h / 2
        for i, (rn, _, cnt, note) in enumerate(self.rounds):
            bh = (cnt / maxc) * self.h
            x = i * slot + slot * 0.12
            cx = x + slot * 0.38
            col = PINK if cnt == 36 else (PINK_DEEP if cnt <= 12 else colors.HexColor("#F0BFCB"))
            c.setFillColor(col); c.roundRect(x, mid - bh / 2, slot * 0.76, bh, 1.4, fill=1, stroke=0)
            if rn in (1, 6, 13, 16, 26, 36):
                c.setFont("Sans-Semi", 6.5); c.setFillColor(INK_SOFT)
                c.drawCentredString(cx, self.CAP + 1, f"R{rn}")
            if rn in (1, 6, 13, 16, 26, 32):
                c.setFont("Fredoka", 6.5); c.setFillColor(PINK_DEEP)
                c.drawCentredString(cx, base + self.h + 3, str(cnt))
        c.setFont("Sans-It", 7.5); c.setFillColor(INK_SOFT)
        c.drawString(0, 1, "Body silhouette - one bar per round, width = stitch count   ·   head R1-12  ·  neck R13  ·  body R14-26  ·  tail R27-36")


class Swatch(Flowable):
    def __init__(self, name, main, gill, size=40):
        super().__init__(); self.name = name; self.main = main; self.gill = gill; self.s = size
    def wrap(self, aw, ah): return self.s + 8, self.s + 16
    def draw(self):
        c = self.canv; s = self.s
        c.setFillColor(colors.HexColor(self.gill)); c.setStrokeColor(RULE)
        c.circle(s * 0.18 + 4, s * 0.72, s * 0.20, fill=1, stroke=0)
        c.circle(s * 0.82 + 4, s * 0.72, s * 0.20, fill=1, stroke=0)
        c.setFillColor(colors.HexColor(self.main))
        c.circle(s * 0.5 + 4, s * 0.55, s * 0.42, fill=1, stroke=1)
        c.setFillColor(colors.HexColor("#3B2F33"))
        c.circle(s * 0.38 + 4, s * 0.58, 1.6, fill=1, stroke=0); c.circle(s * 0.62 + 4, s * 0.58, 1.6, fill=1, stroke=0)
        c.setStrokeColor(colors.HexColor("#3B2F33")); c.setLineWidth(0.8)
        c.arc(s * 0.42 + 4, s * 0.40, s * 0.58 + 4, s * 0.52, startAng=200, extent=140)
        c.setFont("Sans-Semi", 7.5); c.setFillColor(INK)
        c.drawCentredString(s / 2 + 4, 0, self.name)


class Badge(Flowable):
    def __init__(self, text, width=None, fill=PINK_DEEP, fg=colors.white):
        super().__init__(); self.text = text; self.fill = fill; self.fg = fg; self.w = width
    def wrap(self, aw, ah):
        tw = pdfmetrics.stringWidth(self.text, "Sans-Semi", 8) + 14
        self.w = self.w or tw; return self.w, 16
    def draw(self):
        c = self.canv; c.setFillColor(self.fill); c.roundRect(0, 0, self.w, 14, 7, fill=1, stroke=0)
        c.setFillColor(self.fg); c.setFont("Sans-Semi", 8); c.drawCentredString(self.w / 2, 4, self.text)


# ------------------------------------------------------------------ helpers
def para(text, style="body"): return Paragraph(text, S[style])


def rounds_table(rounds, col_widths=(16 * mm, 66 * mm, 16 * mm, 60 * mm), highlight=()):
    data = [[para("Rnd", "kicker"), para("Instruction", "kicker"), para("Sts", "kicker"), para("Note", "kicker")]]
    for rn, instr, cnt, note in rounds:
        instr_html = instr.replace("invdec", "<b>invdec</b>").replace(" inc", " <b>inc</b>")
        data.append([para(f"R{rn}", "cell_b"), para(instr_html, "cell"), para(f"({cnt})", "cell_count"), para(note, "cell_note")])
    t = Table(data, colWidths=col_widths, repeatRows=1, hAlign="LEFT")
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), PINK_PALE),
        ("LINEBELOW", (0, 0), (-1, 0), 0.8, PINK),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 3.2), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.2),
        ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [CREAM, colors.HexColor("#FDF5F7")]),
        ("LINEBELOW", (0, 1), (-1, -1), 0.4, RULE),
    ]
    for i, (rn, _, cnt, note) in enumerate(rounds, start=1):
        if note.isupper() or "STUFF" in note or "NECK" in note or "FEET" in note:
            style.append(("BACKGROUND", (0, i), (-1, i), colors.HexColor("#F7DCE3")))
    t.setStyle(TableStyle(style))
    return t


def image(name, width, radius=True):
    p = IMG / name
    im = Image(str(p)); ratio = im.imageHeight / im.imageWidth
    im.drawWidth = width; im.drawHeight = width * ratio
    return im


def stat(number, label):
    return Table([[para(number, "big_number")], [para(label, "stat_label")]], colWidths=[38 * mm],
                 style=[("BACKGROUND", (0, 0), (-1, -1), PINK_PALE), ("ROUNDEDCORNERS", [6, 6, 6, 6]),
                        ("TOPPADDING", (0, 0), (-1, 0), 8), ("BOTTOMPADDING", (0, 1), (-1, 1), 8),
                        ("TOPPADDING", (0, 1), (-1, 1), 0), ("BOTTOMPADDING", (0, 0), (-1, 0), 0)])



def _gradient_png(w, h):
    """Vertical gradient: transparent at the top -> deep pink at the bottom (matches PINK_DEEP)."""
    im = PILImage.new("RGBA", (1, h))
    for y in range(h):
        a = ((y / (h - 1)) ** 1.5)
        im.putpixel((0, y), (184, 80, 111, int(255 * 0.86 * a)))
    im = im.resize((w, h))
    buf = io.BytesIO(); im.save(buf, "PNG"); buf.seek(0)
    return buf

# ------------------------------------------------------------------ page decorations
def draw_background(canv, doc):
    canv.saveState()
    canv.setFillColor(CREAM); canv.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    # soft corner blob
    canv.setFillColor(colors.HexColor("#FBEEF1"))
    canv.circle(PAGE_W + 20, PAGE_H + 20, 90, fill=1, stroke=0)
    canv.circle(-30, -30, 70, fill=1, stroke=0)
    # header / footer
    canv.setFont("Fredoka", 9); canv.setFillColor(PINK_DEEP)
    canv.drawString(MARGIN, PAGE_H - 12 * mm, P.TITLE)
    canv.setFont("Sans", 8); canv.setFillColor(INK_SOFT)
    canv.drawRightString(PAGE_W - MARGIN, PAGE_H - 12 * mm, f"{P.DESIGNER}  ·  Design {P.DESIGN_CODE}  ·  {P.TERMS}")
    canv.setStrokeColor(RULE); canv.setLineWidth(0.6); canv.line(MARGIN, PAGE_H - 13.5 * mm, PAGE_W - MARGIN, PAGE_H - 13.5 * mm)
    canv.setFont("Sans", 8); canv.setFillColor(INK_SOFT)
    canv.drawCentredString(PAGE_W / 2, 10 * mm, f"© {P.YEAR} {P.DESIGNER}  ·  for personal use and small-batch sales, see Terms  ·  page {doc.page}")
    # stitch-marker dot
    canv.setFillColor(PINK); canv.circle(PAGE_W - MARGIN - 1, 10 * mm + 2.5, 2.2, fill=1, stroke=0)
    canv.restoreState()


def draw_cover(canv, doc):
    canv.saveState()
    canv.setFillColor(CREAM); canv.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    # full-bleed hero photo, top 62% of the page
    hero = IMG / "hero_axel.jpg"
    photo_h = PAGE_H * 0.64
    canv.drawImage(str(hero), 0, PAGE_H - photo_h, width=PAGE_W, height=photo_h, preserveAspectRatio=True, anchor="c", mask=None)
    # smooth gradient overlay band (pre-rendered RGBA image - no banding)
    grad = _gradient_png(int(PAGE_W), int(70 * mm))
    canv.drawImage(ImageReader(grad), 0, PAGE_H - photo_h, width=PAGE_W, height=70 * mm, mask="auto")
    canv.setFillColor(PINK_DEEP); canv.rect(0, 0, PAGE_W, PAGE_H - photo_h, fill=1, stroke=0)
    # title
    canv.setFillColor(colors.white)
    canv.setFont("Fredoka", 46); canv.drawString(MARGIN, PAGE_H - photo_h + 30 * mm, P.TITLE)
    canv.setFont("Serif-It", 16); canv.drawString(MARGIN + 1, PAGE_H - photo_h + 20 * mm, P.SUBTITLE)
    # meta chips
    chips = [P.TERMS, P.SKILL, P.TIME, "11.5 cm / 4.5 in tall"]
    x = MARGIN
    for chip in chips:
        w = pdfmetrics.stringWidth(chip, "Sans-Semi", 9) + 16
        canv.setFillColor(colors.Color(1, 1, 1, alpha=0.18)); canv.roundRect(x, PAGE_H - photo_h + 8 * mm, w, 16, 8, fill=1, stroke=0)
        canv.setFillColor(colors.white); canv.setFont("Sans-Semi", 9); canv.drawString(x + 8, PAGE_H - photo_h + 8 * mm + 4.5, chip)
        x += w + 6
    # lower cover: intro + three feature columns
    y0 = PAGE_H - photo_h - 16 * mm
    canv.setFont("Serif-It", 12.5); canv.setFillColor(colors.white)
    lines = ["A soft pink axolotl with six fluffy gills, a round head and a shell-edged paddle tail.",
             "Head, neck, body and tail are worked as one continuous spiral - no neck seam to sew."]
    for i, l in enumerate(lines): canv.drawString(MARGIN, y0 - i * 17, l)
    feats = [("36", "stitches around\nhead and body"), ("52", "rounds, all\ncount-checked"), ("6", "fluffy gills,\n3 per side"), ("5", "dc scallops\non the tail fin")]
    colw = (PAGE_W - 2 * MARGIN) / 4
    for i, (num, lab) in enumerate(feats):
        cx = MARGIN + colw * i + colw / 2
        canv.setFillColor(colors.Color(1, 1, 1, alpha=0.12)); canv.roundRect(MARGIN + colw * i + 4, y0 - 92, colw - 8, 58, 8, fill=1, stroke=0)
        canv.setFillColor(colors.white); canv.setFont("Fredoka", 24); canv.drawCentredString(cx, y0 - 66, num)
        canv.setFont("Sans", 8.5)
        for j, ln in enumerate(lab.split("\n")): canv.drawCentredString(cx, y0 - 78 - j * 10, ln)
    canv.setFont("Sans-Semi", 9); canv.setFillColor(colors.Color(1, 1, 1, alpha=0.85))
    canv.drawString(MARGIN, 14 * mm, f"{P.DESIGNER}  ·  designed by {P.STUDIO}  ·  Design Code {P.DESIGN_CODE}")
    canv.drawRightString(PAGE_W - MARGIN, 14 * mm, "  ".join(P.HASHTAGS))
    canv.restoreState()


# ------------------------------------------------------------------ document
def build():
    doc = BaseDocTemplate(str(OUT), pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN, topMargin=20 * mm, bottomMargin=18 * mm,
                          title=f"{P.TITLE} - crochet pattern", author=P.DESIGNER, subject="Amigurumi crochet pattern",
                          creator="Crochet Pattern Checker")
    frame = Frame(MARGIN, 18 * mm, PAGE_W - 2 * MARGIN, PAGE_H - 38 * mm, id="main", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id="cover", frames=[frame], onPage=draw_cover),
                          PageTemplate(id="page", frames=[frame], onPage=draw_background)])
    W = PAGE_W - 2 * MARGIN
    s = []

    # -------- cover (drawn entirely on canvas)
    s += [NextPageTemplate("page"), PageBreak()]

    # -------- page 2: welcome, size, contents, safety
    s.append(para("Welcome", "h1"))
    s.append(para(P.INTRO, "lead"))
    stats = Table([[stat("11.5 cm", "TALL, SEATED"), stat("10 cm", "GILL TIP TO TIP"), stat("4.3 cm", "TAIL"), stat("52 mm", "HEAD SPHERE")]],
                  colWidths=[W / 4] * 4, style=[("ALIGN", (0, 0), (-1, -1), "CENTER"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE")])
    s.append(stats); s.append(Spacer(1, 8))
    left = [para("In this booklet", "h2")]
    toc = ["1  Materials, gauge & abbreviations", "2  Five techniques you will use", "3  Body - one spiral from head to tail",
           "4  Arms & feet", "5  Gills - make 6", "6  Tail fin - shell edging", "7  Assembly", "8  Troubleshooting & colourways", "9  Terms of use"]
    left += [para(t, "toc") for t in toc]
    right = [image("in_hand_scale.jpg", 78 * mm), para("Axel sits about 11.5 cm tall - a true palm-sized plushie.", "caption")]
    s.append(Table([[left, right]], colWidths=[W - 84 * mm, 84 * mm], style=[("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0)]))
    s.append(Spacer(1, 6))
    s.append(Panel("Safety - read this first", [para(P.SAFETY, "body")], fill=colors.HexColor("#FFF4E8"), accent=colors.HexColor("#D98B4A")))
    s.append(PageBreak())

    # -------- page 3: materials / gauge / abbreviations
    s.append(para("1 · Materials", "h1"))
    mat_rows = [[para(f"<b>{k}</b>", "cell"), para(v, "cell")] for k, v in P.MATERIALS]
    mt = Table(mat_rows, colWidths=[28 * mm, W - 96 * mm - 28 * mm], style=[("VALIGN", (0, 0), (-1, -1), "TOP"), ("LINEBELOW", (0, 0), (-1, -2), 0.4, RULE), ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5), ("LEFTPADDING", (0, 0), (-1, -1), 0)])
    s.append(Table([[mt, [image("flatlay_materials.jpg", 88 * mm), para("Everything you need - one 25 g ball of pale pink covers the whole toy.", "caption")]]],
                   colWidths=[W - 92 * mm, 92 * mm], style=[("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0)]))
    s.append(Spacer(1, 6))
    s.append(Panel("Gauge", [para(P.GAUGE, "body")]))
    s.append(Spacer(1, 6))
    s.append(para("Abbreviations (US terms)", "h2"))
    ab = []
    row = []
    for k, v in P.ABBREVIATIONS:
        row.append(para(f"<font name='Fredoka' color='#B8506F'>{k}</font>&nbsp;&nbsp;{v}", "cell"))
        if len(row) == 2: ab.append(row); row = []
    if row: ab.append(row + [""])
    s.append(Table(ab, colWidths=[W / 2, W / 2], style=[("LINEBELOW", (0, 0), (-1, -1), 0.4, RULE), ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4), ("LEFTPADDING", (0, 0), (-1, -1), 0)]))
    s.append(PageBreak())

    # -------- page 4: techniques
    s.append(para("2 · Five techniques", "h1"))
    s.append(para("These are the five techniques Axel uses, in the order you will meet them.", "lead"))
    for i, (name, desc) in enumerate(P.TECHNIQUES, start=1):
        num = Table([[para(str(i), "big_number")]], colWidths=[14 * mm], rowHeights=[14 * mm], style=[("BACKGROUND", (0, 0), (-1, -1), PINK_PALE), ("ROUNDEDCORNERS", [7, 7, 7, 7]), ("VALIGN", (0, 0), (-1, -1), "MIDDLE")])
        s.append(KeepTogether(Table([[num, [para(name, "h2"), para(desc, "body")]]], colWidths=[18 * mm, W - 18 * mm],
                                    style=[("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)])))
    s.append(Spacer(1, 4))
    s.append(Table([[image("wip_hands.jpg", 80 * mm), [para("Working in a spiral", "h2"), para("Keep a stitch marker in the first stitch of every round and move it up each time. There is no join to count from, so the marker is your only landmark - and the reason Axel's head has no seam.", "body"), para("Tip: the invisible decrease is worth practising on a scrap first. Every decrease on the head and neck is visible on the finished toy.", "body_small")]]],
                   colWidths=[84 * mm, W - 84 * mm], style=[("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0)]))
    s.append(PageBreak())

    # -------- pages 5-6: body
    s.append(para("3 · Body - one spiral, head to tail", "h1"))
    s.append(para(P.BODY_INTRO, "lead"))
    s.append(ShapeStrip(P.BODY_ROUNDS, W))
    s.append(Spacer(1, 4))
    s.append(para("Head & neck  ·  R1 - R13", "h2"))
    s.append(rounds_table(P.BODY_ROUNDS[:13]))
    s.append(Spacer(1, 4))
    s.append(Panel("Before you leave the head", [para("Insert the safety eyes between R7 and R8 (6 stitches apart), embroider the smile across R8-R9, then stuff the head <b>firmly</b> at R11 - it must hold a sphere so the eyes stay level. See Assembly for exact placement.", "body")]))
    s.append(PageBreak())
    s.append(para("Body  ·  R14 - R26", "h2"))
    s.append(rounds_table(P.BODY_ROUNDS[13:26]))
    s.append(Spacer(1, 6))
    s.append(para("Tail  ·  R27 - R36", "h2"))
    s.append(rounds_table(P.BODY_ROUNDS[26:]))
    s.append(Spacer(1, 6))
    s.append(Panel("Finish the tail tip", [para(P.BODY_FINISH, "body")]))
    s.append(PageBreak())

    # -------- page 7: arms & feet, gills
    s.append(para("4 · Arms & feet", "h1"))
    s.append(para(P.LIMBS_INTRO, "lead"))
    s.append(Table([[[para("Arms - make 2", "h2"), rounds_table(P.ARM_ROUNDS, col_widths=(12 * mm, 40 * mm, 12 * mm, 22 * mm)), Spacer(1, 4), para(P.ARMS_FINISH, "body_small")],
                     [para("Feet - make 2", "h2"), rounds_table(P.FEET_ROUNDS, col_widths=(12 * mm, 40 * mm, 12 * mm, 22 * mm)), Spacer(1, 4), para(P.FEET_FINISH, "body_small")]]],
                   colWidths=[W / 2, W / 2], style=[("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (0, 0), 6)]))
    s.append(Spacer(1, 8))
    s.append(para("5 · Gills - make 6 (3 per side, fuzzy dark pink)", "h1"))
    s.append(Table([[[rounds_table(P.GILL_ROUNDS, col_widths=(12 * mm, 44 * mm, 12 * mm, 30 * mm)), Spacer(1, 6), Panel("Working with fuzzy yarn", [para(P.FUZZY_TIP, "body_small")], width=98 * mm), Spacer(1, 4), para(P.GILLS_FINISH, "body_small")],
                     [image("detail_gills.jpg", 72 * mm), para("Three lobes fan behind each eye: upper up, middle out, lower down.", "caption")]]],
                   colWidths=[W - 76 * mm, 76 * mm], style=[("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0)]))
    s.append(PageBreak())

    # -------- page 8: fin
    s.append(para("6 · Tail fin - shell edging", "h1"))
    s.append(para("Five loose double-crochet scallops form the shell-edged paddle along the tail ridge.", "lead"))
    fin_left = [para(P.FIN_STEPS[0], "body"),
                Panel("Scallop repeat", [para("<b>*</b> 5 dc in the next ridge stitch, sl st in the next ridge stitch.<br/>Repeat from * a total of <b>5 times</b> (5 scallops). FO and weave in.", "body")]),
                Spacer(1, 6), para(P.FIN_NOTES, "body")]
    s.append(Table([[fin_left, [image("detail_tail.jpg", 72 * mm), para("Each scallop uses 2 ridge stitches - 5 scallops fit the 10-round tail exactly.", "caption")]]],
                   colWidths=[W - 76 * mm, 76 * mm], style=[("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0)]))
    s.append(Spacer(1, 6))
    s.append(Panel("A note on fullness", [para(P.FIN_FULLNESS, "body")], fill=colors.HexColor("#EAF6F2"), accent=colors.HexColor("#3C9C93")))
    s.append(PageBreak())

    # -------- page 9: assembly
    s.append(para("7 · Assembly", "h1"))
    s.append(Panel("Before you sew - lay every component out and check", [para("&nbsp;&nbsp;·&nbsp;&nbsp;".join(f"<b>{c}</b>" for c in P.CHECKLIST) + "&nbsp;&nbsp;-&nbsp;&nbsp;check each against the pattern before attaching anything.", "body")]))
    s.append(Spacer(1, 6))
    rows = [[Badge(k, width=22 * mm), para(v, "body")] for k, v in P.ASSEMBLY]
    s.append(Table(rows, colWidths=[26 * mm, W - 26 * mm], style=[("VALIGN", (0, 0), (-1, -1), "TOP"), ("LINEBELOW", (0, 0), (-1, -2), 0.4, RULE), ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6), ("LEFTPADDING", (0, 0), (-1, -1), 0)]))
    s.append(Spacer(1, 6))
    s.append(Table([[image("hero_axel.jpg", 60 * mm), image("detail_gills.jpg", 60 * mm), image("in_hand_scale.jpg", 60 * mm)]], colWidths=[W / 3] * 3, style=[("ALIGN", (0, 0), (-1, -1), "CENTER")]))
    s.append(PageBreak())

    # -------- page 10: troubleshooting & colourways
    s.append(para("8 · Troubleshooting", "h1"))
    for k, v in P.TROUBLESHOOTING:
        s.append(para(f"<font name='Sans-Bold' color='#B8506F'>{k}</font>  {v}", "body"))
    s.append(Spacer(1, 8))
    s.append(para("Colourways", "h2"))
    s.append(Table([[Swatch(n, m, g) for n, m, g in P.COLORWAYS]], colWidths=[W / 5] * 5, style=[("ALIGN", (0, 0), (-1, -1), "CENTER")]))
    s.append(Spacer(1, 4))
    s.append(image("colorways.jpg", W))
    s.append(para("Left to right: classic pink, white leucistic, melanoid black, mint, lavender. Swap the main and gill yarns - the pattern is unchanged.", "caption"))
    s.append(PageBreak())

    # -------- page 11: terms
    s.append(para("9 · Terms of use", "h1"))
    s.append(para("Copyright & ownership", "h2")); s.append(para(P.TERMS_COPYRIGHT, "body"))
    s.append(Table([[[para("You may", "h2"), para(P.TERMS_MAY, "body")], [para("You may not", "h2"), para(P.TERMS_MAY_NOT, "body")]]],
                   colWidths=[W / 2, W / 2], style=[("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (0, 0), 10)]))
    s.append(Spacer(1, 4))
    s.append(Panel("Safety reminder", [para(P.TERMS_SAFETY, "body")], fill=colors.HexColor("#FFF4E8"), accent=colors.HexColor("#D98B4A")))
    s.append(Spacer(1, 14))
    s.append(para("Happy crocheting!", "h1"))
    s.append(para(P.THANKS, "lead"))
    s.append(image("hero_axel.jpg", 70 * mm))

    doc.build(s)
    return OUT


if __name__ == "__main__":
    out = build()
    print("wrote", out, out.stat().st_size, "bytes")
