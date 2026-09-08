"""Data-driven pattern PDF builder (ReportLab) for all Novality kits.

Usage: python engine/build_pdf.py <slug> [<slug>...]     -> out/<slug>/<Title>_Pattern.pdf
Requires assets/img_pdf/<slug>/*.jpg (run prep_images.py first).
"""
from __future__ import annotations

import io
import sys
from pathlib import Path

from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Flowable, Frame, Image, KeepTogether, NextPageTemplate, PageBreak,
                                PageTemplate, Paragraph, Spacer, Table, TableStyle)

sys.path.insert(0, str(Path(__file__).parent))
from common import FONTS, IMG_PDF_ROOT, OUT_ROOT, SAFETY_BLOCK, load_pattern  # noqa: E402

for name, f in (("Fredoka", "FredokaOne-Regular.ttf"), ("Sans", "SourceSansPro-Regular.ttf"), ("Sans-Bold", "SourceSansPro-Bold.ttf"),
                ("Sans-Semi", "SourceSansPro-Semibold.ttf"), ("Sans-It", "SourceSansPro-It.ttf"), ("Serif-It", "Caladea-Italic.ttf")):
    pdfmetrics.registerFont(TTFont(name, str(FONTS / f)))
pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-Bold", italic="Sans-It", boldItalic="Sans-Bold")

PAGE_W, PAGE_H = A4
MARGIN = 18 * mm
W = PAGE_W - 2 * MARGIN


class Theme:
    def __init__(self, P):
        pal = P["palette"]; self.P = P
        self.ACC = colors.HexColor(pal["accent"]); self.DEEP = colors.HexColor(pal["deep"]); self.PALE = colors.HexColor(pal["pale"])
        self.CREAM = colors.HexColor(pal["cream"]); self.INK = colors.HexColor(pal["ink"]); self.SOFT = colors.HexColor(pal["ink_soft"])
        self.RULE = colors.HexColor(pal["rule"]); self.HILITE = colors.HexColor(pal["hilite"]); self.deep_hex = pal["deep"]
        self.img_dir = IMG_PDF_ROOT / P["slug"]
        self.S = self._styles()

    def _styles(self):
        def st(name, **kw):
            base = dict(fontName="Sans", fontSize=10.2, leading=14.5, textColor=self.INK, spaceAfter=4); base.update(kw)
            return ParagraphStyle(name, **base)
        return {
            "body": st("body"), "body_small": st("body_small", fontSize=9, leading=12.5, textColor=self.SOFT),
            "lead": st("lead", fontName="Serif-It", fontSize=12.5, leading=18, textColor=self.SOFT, spaceAfter=8),
            "h1": st("h1", fontName="Fredoka", fontSize=26, leading=30, textColor=self.DEEP, spaceBefore=2, spaceAfter=6),
            "h2": st("h2", fontName="Fredoka", fontSize=15, leading=19, textColor=self.DEEP, spaceBefore=10, spaceAfter=4),
            "kicker": st("kicker", fontName="Sans-Semi", fontSize=8.5, leading=11, textColor=self.DEEP, spaceAfter=2),
            "caption": st("caption", fontName="Sans-It", fontSize=8.5, leading=11, textColor=self.SOFT, alignment=TA_CENTER),
            "cell": st("cell", fontSize=9.6, leading=12, spaceAfter=0), "cell_b": st("cell_b", fontName="Sans-Semi", fontSize=9.6, leading=12, spaceAfter=0),
            "cell_note": st("cell_note", fontName="Sans-It", fontSize=8.6, leading=11, textColor=self.SOFT, spaceAfter=0),
            "cell_count": st("cell_count", fontName="Fredoka", fontSize=10, leading=12, textColor=self.DEEP, alignment=TA_CENTER, spaceAfter=0),
            "toc": st("toc", fontSize=11, leading=17),
            "big_number": st("big_number", fontName="Fredoka", fontSize=22, leading=24, textColor=self.DEEP, alignment=TA_CENTER, spaceAfter=0),
            "stat_label": st("stat_label", fontName="Sans-Semi", fontSize=8, leading=10, textColor=self.SOFT, alignment=TA_CENTER, spaceAfter=0),
            "step": st("step", leftIndent=14, spaceAfter=5),
        }

    def para(self, text, style="body"): return Paragraph(text, self.S[style])

    def image(self, key, width):
        p = self.img_dir / (Path(self.P["images"][key]).stem + ".jpg")
        im = Image(str(p)); ratio = im.imageHeight / im.imageWidth
        im.drawWidth = width; im.drawHeight = width * ratio
        return im


class Panel(Flowable):
    def __init__(self, title, flowables, fill, accent, pad=9, width=None):
        super().__init__(); self.title = title; self.items = flowables; self.fill = fill; self.accent = accent
        self.pad = pad; self.width = width; self._h = 0; self._parts = []
    def wrap(self, aw, ah):
        self.width = self.width or aw; inner = self.width - 2 * self.pad - 4
        h = self.pad + (14 if self.title else 0); self._parts = []
        for f in self.items:
            w, fh = f.wrap(inner, ah); self._parts.append((f, fh)); h += fh
        h += self.pad; self._h = h
        return self.width, h
    def split(self, aw, ah): return []
    def draw(self):
        c = self.canv; c.saveState()
        c.setFillColor(self.fill); c.roundRect(0, 0, self.width, self._h, 6, fill=1, stroke=0)
        c.setFillColor(self.accent); c.roundRect(0, 0, 4, self._h, 2, fill=1, stroke=0)
        y = self._h - self.pad
        if self.title:
            c.setFont("Fredoka", 10.5); c.setFillColor(self.accent); c.drawString(self.pad + 4, y - 9, self.title.upper()); y -= 14
        for f, fh in self._parts:
            y -= fh; f.drawOn(c, self.pad + 4, y)
        c.restoreState()


class Swatch(Flowable):
    def __init__(self, name, main, second, ink, size=40):
        super().__init__(); self.name = name; self.main = main; self.second = second; self.s = size; self.ink = ink
    def wrap(self, aw, ah): return self.s + 8, self.s + 16
    def draw(self):
        c = self.canv; s = self.s
        c.setFillColor(colors.HexColor(self.second)); c.setStrokeColor(colors.HexColor("#DDD5D0"))
        c.circle(s * 0.5 + 4, s * 0.22, s * 0.28, fill=1, stroke=0)
        c.setFillColor(colors.HexColor(self.main)); c.circle(s * 0.5 + 4, s * 0.58, s * 0.40, fill=1, stroke=1)
        c.setFont("Sans-Semi", 7.5); c.setFillColor(self.ink); c.drawCentredString(s / 2 + 4, 0, self.name)


class Badge(Flowable):
    def __init__(self, text, fill, width=None):
        super().__init__(); self.text = text; self.fill = fill; self.w = width
    def wrap(self, aw, ah):
        self.w = self.w or pdfmetrics.stringWidth(self.text, "Sans-Semi", 8) + 14; return self.w, 16
    def draw(self):
        c = self.canv; c.setFillColor(self.fill); c.roundRect(0, 0, self.w, 14, 7, fill=1, stroke=0)
        c.setFillColor(colors.white); c.setFont("Sans-Semi", 8); txt = self.text
        while pdfmetrics.stringWidth(txt, "Sans-Semi", 8) > self.w - 8 and len(txt) > 3: txt = txt[:-1]
        c.drawCentredString(self.w / 2, 4, txt)


HILITE_KEYS = ("STUFF", "NECK", "OPEN", "LOCK", "FINISH", "finish here", "check gauge", "full", "join", "eyes", "waist")


def rounds_table(T, rounds, total_w=None):
    total_w = total_w or W; rest = total_w - 32 * mm
    col_widths = (16 * mm, rest * 0.58, 16 * mm, rest * 0.42)
    data = [[T.para("Rnd", "kicker"), T.para("Instruction", "kicker"), T.para("Sts", "kicker"), T.para("Note", "kicker")]]
    for label, instr, cnt, note in rounds:
        instr_html = instr.replace("invdec", "<b>invdec</b>").replace(" dec", " <b>dec</b>").replace(" inc", " <b>inc</b>")
        cnt_txt = f"({cnt})" if isinstance(cnt, int) else (cnt or "")
        data.append([T.para(label, "cell_b"), T.para(instr_html, "cell"), T.para(cnt_txt, "cell_count"), T.para(note or "", "cell_note")])
    t = Table(data, colWidths=col_widths, repeatRows=1, hAlign="LEFT")
    style = [("BACKGROUND", (0, 0), (-1, 0), T.PALE), ("LINEBELOW", (0, 0), (-1, 0), 0.8, T.ACC), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
             ("TOPPADDING", (0, 0), (-1, -1), 3.2), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.2), ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
             ("ROWBACKGROUNDS", (0, 1), (-1, -1), [T.CREAM, colors.white]), ("LINEBELOW", (0, 1), (-1, -1), 0.4, T.RULE)]
    for i, (_, _, _, note) in enumerate(rounds, start=1):
        if note and (note.isupper() or any(k in note for k in HILITE_KEYS)):
            style.append(("BACKGROUND", (0, i), (-1, i), T.HILITE))
    t.setStyle(TableStyle(style))
    return t


def stat(T, number, label):
    return Table([[T.para(number, "big_number")], [T.para(label, "stat_label")]], colWidths=[38 * mm],
                 style=[("BACKGROUND", (0, 0), (-1, -1), T.PALE), ("ROUNDEDCORNERS", [6, 6, 6, 6]), ("TOPPADDING", (0, 0), (-1, 0), 8),
                        ("BOTTOMPADDING", (0, 1), (-1, 1), 8), ("TOPPADDING", (0, 1), (-1, 1), 0), ("BOTTOMPADDING", (0, 0), (-1, 0), 0)])


def _gradient_png(w, h, rgb):
    im = PILImage.new("RGBA", (1, h))
    for y in range(h):
        a = (y / (h - 1)) ** 1.5; im.putpixel((0, y), (*rgb, int(255 * 0.86 * a)))
    im = im.resize((w, h)); buf = io.BytesIO(); im.save(buf, "PNG"); buf.seek(0); return buf


def make_page_callbacks(T):
    P = T.P

    def draw_background(canv, doc):
        canv.saveState()
        canv.setFillColor(T.CREAM); canv.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
        canv.setFillColor(T.PALE); canv.circle(PAGE_W + 20, PAGE_H + 20, 90, fill=1, stroke=0); canv.circle(-30, -30, 70, fill=1, stroke=0)
        canv.setFont("Fredoka", 9); canv.setFillColor(T.DEEP); canv.drawString(MARGIN, PAGE_H - 12 * mm, P["title"])
        canv.setFont("Sans", 8); canv.setFillColor(T.SOFT)
        canv.drawRightString(PAGE_W - MARGIN, PAGE_H - 12 * mm, f"{P['brand']}  ·  Design {P['design_code']}  ·  {P['terms']}")
        canv.setStrokeColor(T.RULE); canv.setLineWidth(0.6); canv.line(MARGIN, PAGE_H - 13.5 * mm, PAGE_W - MARGIN, PAGE_H - 13.5 * mm)
        canv.setFont("Sans", 8); canv.setFillColor(T.SOFT)
        canv.drawCentredString(PAGE_W / 2, 10 * mm, f"© {P['year']} {P['brand']}  ·  for personal use and small-batch sales, see Terms  ·  page {doc.page}")
        canv.setFillColor(T.ACC); canv.circle(PAGE_W - MARGIN - 1, 10 * mm + 2.5, 2.2, fill=1, stroke=0)
        canv.restoreState()

    def draw_cover(canv, doc):
        canv.saveState()
        canv.setFillColor(T.CREAM); canv.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
        hero = T.img_dir / (Path(P["images"]["hero"]).stem + ".jpg"); photo_h = PAGE_H * 0.64
        canv.drawImage(str(hero), 0, PAGE_H - photo_h, width=PAGE_W, height=photo_h, preserveAspectRatio=True, anchor="c")
        rgb = tuple(int(T.deep_hex.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
        canv.drawImage(ImageReader(_gradient_png(int(PAGE_W), int(70 * mm), rgb)), 0, PAGE_H - photo_h, width=PAGE_W, height=70 * mm, mask="auto")
        canv.setFillColor(T.DEEP); canv.rect(0, 0, PAGE_W, PAGE_H - photo_h, fill=1, stroke=0)
        canv.setFillColor(colors.white); size = 46
        while pdfmetrics.stringWidth(P["title"], "Fredoka", size) > PAGE_W - 2 * MARGIN: size -= 2
        canv.setFont("Fredoka", size); canv.drawString(MARGIN, PAGE_H - photo_h + 30 * mm, P["title"])
        canv.setFont("Serif-It", 16); canv.drawString(MARGIN + 1, PAGE_H - photo_h + 20 * mm, P["subtitle"])
        x = MARGIN
        for chip in [P["terms"], P["skill"], P["time"], P["size_chip"]]:
            w = pdfmetrics.stringWidth(chip, "Sans-Semi", 9) + 16
            canv.setFillColor(colors.Color(1, 1, 1, alpha=0.18)); canv.roundRect(x, PAGE_H - photo_h + 8 * mm, w, 16, 8, fill=1, stroke=0)
            canv.setFillColor(colors.white); canv.setFont("Sans-Semi", 9); canv.drawString(x + 8, PAGE_H - photo_h + 8 * mm + 4.5, chip); x += w + 6
        y0 = PAGE_H - photo_h - 16 * mm
        canv.setFont("Serif-It", 12.5); canv.setFillColor(colors.white)
        for i, l in enumerate(P["tagline"]): canv.drawString(MARGIN, y0 - i * 17, l)
        colw = W / 4
        for i, (num, lab) in enumerate(P["feats"]):
            cx = MARGIN + colw * i + colw / 2
            canv.setFillColor(colors.Color(1, 1, 1, alpha=0.12)); canv.roundRect(MARGIN + colw * i + 4, y0 - 92, colw - 8, 58, 8, fill=1, stroke=0)
            canv.setFillColor(colors.white); canv.setFont("Fredoka", 24); canv.drawCentredString(cx, y0 - 66, num)
            canv.setFont("Sans", 8.5)
            for j, ln in enumerate(lab.split("\n")): canv.drawCentredString(cx, y0 - 78 - j * 10, ln)
        canv.setFont("Sans-Semi", 9); canv.setFillColor(colors.Color(1, 1, 1, alpha=0.85))
        canv.drawString(MARGIN, 14 * mm, f"{P['brand']}  ·  Design Code {P['design_code']}  ·  © {P['year']}")
        canv.drawRightString(PAGE_W - MARGIN, 14 * mm, "  ".join(P["hashtags"]))
        canv.restoreState()
    return draw_cover, draw_background


def two_col(left, right, right_w, gap=6 * mm):
    return Table([[left, right]], colWidths=[W - right_w - gap, right_w + gap],
                 style=[("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (0, 0), gap), ("RIGHTPADDING", (1, 0), (1, 0), 0)])


def build(slug):
    P = load_pattern(slug); T = Theme(P); p = T.para
    out_dir = OUT_ROOT / slug; out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{P['file_stem']}_Pattern.pdf"
    draw_cover, draw_background = make_page_callbacks(T)
    doc = BaseDocTemplate(str(out), pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN, topMargin=20 * mm, bottomMargin=18 * mm,
                          title=f"{P['title']} - crochet pattern", author=P["brand"], subject="Amigurumi crochet pattern", creator="Novality kit builder")
    frame = Frame(MARGIN, 18 * mm, W, PAGE_H - 38 * mm, id="main", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id="cover", frames=[frame], onPage=draw_cover), PageTemplate(id="page", frames=[frame], onPage=draw_background)])
    s = [NextPageTemplate("page"), PageBreak()]

    # welcome
    s.append(p("Welcome", "h1")); s.append(p(P["intro"], "lead"))
    s.append(Table([[stat(T, n, l) for n, l in P["stats"]]], colWidths=[W / 4] * 4, style=[("ALIGN", (0, 0), (-1, -1), "CENTER"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    s.append(Spacer(1, 8))
    toc = ["1  Materials, gauge & abbreviations", "2  Techniques you will use"] + [sec["title"] for sec in P["sections"]]
    n_next = len(P["sections"]) + 3
    toc += [f"{n_next}  Assembly & finishing", f"{n_next + 1}  Troubleshooting & colourways", f"{n_next + 2}  Terms of use"]
    left = [p("In this booklet", "h2")] + [p(t, "toc") for t in toc]
    right = [T.image("inhand", 78 * mm), p(P["sections"][0].get("caption") or P["tagline"][0], "caption")]
    s.append(two_col(left, right, 78 * mm))
    if SAFETY_BLOCK and P.get("safety"):
        s.append(Spacer(1, 6)); s.append(Panel("Safety - read this first", [p(P["safety"])], colors.HexColor("#FFF4E8"), colors.HexColor("#D98B4A")))
    s.append(PageBreak())

    # materials
    s.append(p("1 · Materials", "h1"))
    mat_rows = [[p(f"<b>{k}</b>", "cell"), p(v, "cell")] for k, v in P["materials"]]
    mt = Table(mat_rows, colWidths=[30 * mm, W - 88 * mm - 30 * mm - 6 * mm], style=[("VALIGN", (0, 0), (-1, -1), "TOP"), ("LINEBELOW", (0, 0), (-1, -2), 0.4, T.RULE),
                                                                                    ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5), ("LEFTPADDING", (0, 0), (-1, -1), 0)])
    s.append(two_col(mt, [T.image("detail", 88 * mm), p(P["sections"][-1].get("caption") or P["tagline"][1], "caption")], 88 * mm))
    s.append(Spacer(1, 6)); s.append(Panel("Gauge & size", [p(P["gauge"])], T.PALE, T.DEEP))
    if P.get("height_note"):
        s.append(Spacer(1, 6)); s.append(p("How the size adds up", "h2"))
        s.append(Table([[p(a, "cell_b"), p(b, "cell"), p(c, "cell_count")] for a, b, c in P["height_note"]], colWidths=[60 * mm, 60 * mm, W - 120 * mm],
                       style=[("LINEBELOW", (0, 0), (-1, -1), 0.4, T.RULE), ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4), ("LEFTPADDING", (0, 0), (-1, -1), 0)]))
    s.append(Spacer(1, 6)); s.append(p(f"Abbreviations ({P['terms']})", "h2"))
    ab, row = [], []
    for k, v in P["abbreviations"]:
        row.append(p(f"<font name='Fredoka' color='{T.deep_hex}'>{k}</font>&nbsp;&nbsp;{v}", "cell"))
        if len(row) == 2: ab.append(row); row = []
    if row: ab.append(row + [""])
    s.append(Table(ab, colWidths=[W / 2, W / 2], style=[("LINEBELOW", (0, 0), (-1, -1), 0.4, T.RULE), ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4), ("LEFTPADDING", (0, 0), (-1, -1), 0)]))
    s.append(PageBreak())

    # techniques
    s.append(p("2 · Techniques", "h1")); s.append(p("Everything this pattern uses, in the order you will meet it.", "lead"))
    for i, (name, desc) in enumerate(P["techniques"], start=1):
        num = Table([[p(str(i), "big_number")]], colWidths=[14 * mm], rowHeights=[14 * mm], style=[("BACKGROUND", (0, 0), (-1, -1), T.PALE), ("ROUNDEDCORNERS", [7, 7, 7, 7]), ("VALIGN", (0, 0), (-1, -1), "MIDDLE")])
        s.append(KeepTogether(Table([[num, [p(name, "h2"), p(desc)]]], colWidths=[18 * mm, W - 18 * mm], style=[("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)])))
    s.append(PageBreak())

    # pattern sections
    for sec in P["sections"]:
        s.append(p(sec["title"], "h1"))
        if sec.get("lead"): s.append(p(sec["lead"], "lead"))
        body = []; first_w = (W - 64 * mm - 6 * mm) if sec.get("image") else W
        for i, tbl in enumerate(sec.get("tables", [])):
            body.append(p(tbl["heading"], "h2")); body.append(rounds_table(T, tbl["rounds"], first_w if i == 0 else W))
            if tbl.get("finish"): body.append(Spacer(1, 4)); body.append(p(tbl["finish"], "body_small"))
            body.append(Spacer(1, 6))
        for step in sec.get("steps", []):
            body.append(p(f"<font name='Fredoka' color='{T.deep_hex}'>·</font>&nbsp;&nbsp;{step}", "step"))
        for title, text, kind in sec.get("panels", []):
            fill, acc = (colors.HexColor("#EAF6F2"), colors.HexColor("#3C9C93")) if kind == "tip" else (T.PALE, T.DEEP)
            body.append(Spacer(1, 4)); body.append(Panel(title, [p(text)], fill, acc)); body.append(Spacer(1, 4))
        if sec.get("image"):
            img_col = [T.image(sec["image"], 64 * mm), p(sec.get("caption", ""), "caption")]
            if sec.get("tables"):
                s.append(two_col(body[:3], img_col, 64 * mm)); s += body[3:]
            else:
                s.append(two_col(body, img_col, 64 * mm))
        else:
            s += body
        s.append(PageBreak())

    # assembly
    s.append(p(f"{n_next} · Assembly & finishing", "h1"))
    s.append(Panel("Before you sew - lay every component out and check", [p("&nbsp;&nbsp;·&nbsp;&nbsp;".join(f"<b>{c}</b>" for c in P["checklist"]))], T.PALE, T.DEEP))
    s.append(Spacer(1, 6))
    rows = [[Badge(k, T.DEEP, width=30 * mm), p(v)] for k, v in P["assembly"]]
    s.append(Table(rows, colWidths=[34 * mm, W - 34 * mm], style=[("VALIGN", (0, 0), (-1, -1), "TOP"), ("LINEBELOW", (0, 0), (-1, -2), 0.4, T.RULE), ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6), ("LEFTPADDING", (0, 0), (-1, -1), 0)]))
    if P.get("designer_notes"):
        s.append(Spacer(1, 8)); s.append(p("Designer notes", "h2"))
        for k, v in P["designer_notes"]: s.append(p(f"<font name='Sans-Bold' color='{T.deep_hex}'>{k}</font>  {v}"))
    s.append(Spacer(1, 6))
    s.append(Table([[T.image("hero", 56 * mm), T.image("detail", 56 * mm), T.image("inhand", 56 * mm)]], colWidths=[W / 3] * 3, style=[("ALIGN", (0, 0), (-1, -1), "CENTER")]))
    s.append(PageBreak())

    # troubleshooting & colourways
    s.append(p(f"{n_next + 1} · Troubleshooting", "h1"))
    for k, v in P["troubleshooting"]: s.append(p(f"<font name='Sans-Bold' color='{T.deep_hex}'>{k}</font>  {v}"))
    s.append(Spacer(1, 8)); s.append(p("Colourways", "h2"))
    cw = P["colorways"]
    s.append(Table([[Swatch(n, m, g, T.INK) for n, m, g in cw]], colWidths=[W / len(cw)] * len(cw), style=[("ALIGN", (0, 0), (-1, -1), "CENTER")]))
    s.append(Spacer(1, 4)); s.append(T.image("colorways", W)); s.append(p(P["colorways_caption"], "caption"))
    s.append(PageBreak())

    # terms
    s.append(p(f"{n_next + 2} · Terms of use", "h1")); s.append(p("Copyright & ownership", "h2"))
    s.append(p(f"This crochet pattern - including all instructions, stitch counts, photography and design elements - is the original work and intellectual "
               f"property of {P['brand']}. Design Code {P['design_code']}. Copyright (c) {P['year']} {P['brand']}. All rights reserved."))
    may_not = (f"Do not resell, share, redistribute, translate, rewrite, publish or upload this digital PDF or its contents in any form. Do not alter, copy or "
               f"recolor the pattern and claim it as your own. Do not use the {P['brand']} name, logo or photos beyond crediting the pattern. Do not mass-produce "
               f"finished items commercially without written permission.")
    s.append(Table([[[p("You may", "h2"), p(P["terms_may"])], [p("You may not", "h2"), p(may_not)]]], colWidths=[W / 2, W / 2],
                   style=[("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (0, 0), 10)]))
    if SAFETY_BLOCK and P.get("terms_safety"):
        s.append(Spacer(1, 4)); s.append(Panel("Safety reminder", [p(P["terms_safety"])], colors.HexColor("#FFF4E8"), colors.HexColor("#D98B4A")))
    s.append(Spacer(1, 14)); s.append(p("Happy crocheting!", "h1")); s.append(p(P["thanks"], "lead")); s.append(T.image("hero", 70 * mm))
    doc.build(s)
    return out


if __name__ == "__main__":
    for slug in sys.argv[1:]:
        o = build(slug); print("wrote", o, o.stat().st_size // 1024, "KB")
