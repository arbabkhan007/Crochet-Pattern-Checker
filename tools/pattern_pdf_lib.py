#!/usr/bin/env python3
"""Shared PDF engine for the Novality crochet pattern line (fpdf2).

Renders a PatternSpec (see tools/content_*.py) into a professional,
Etsy-ready A4 PDF: illustrated cover, safety box, materials/gauge,
abbreviations, techniques, per-piece round tables, assembly, colourways,
troubleshooting, terms of use and a deterministic-validation summary.

Two editions per pattern: retail (colour) and print (greyscale).
"""
from __future__ import annotations

from pathlib import Path

from fpdf import FPDF
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
PAGE_W, PAGE_H = 210, 297
M = 16
CW = PAGE_W - 2 * M

INK = (56, 54, 52)
GREY = (118, 114, 109)
LINE = (208, 213, 205)
WHITE = (255, 255, 255)
CREAM = (250, 247, 241)


def make_palette(dark, accent, soft, box_bg, box_edge):
    """Build the colour roles used across the layout (Willow-compatible)."""
    class P:
        pass
    P.ink = INK
    P.grey = GREY
    P.line = LINE
    P.white = WHITE
    P.cream = CREAM
    P.sage_dark = dark
    P.sage_mid = accent
    P.sage_light = soft
    P.pink = box_edge
    P.pink_light = box_bg
    return P


GREY_PALETTE = make_palette((60, 60, 60), (130, 130, 130), (238, 238, 238),
                            (242, 242, 242), (90, 90, 90))


class PatternPDF(FPDF):
    def set_spec(self, spec, P):
        self.spec = spec
        self.P = P

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("DejaVu", "", 7.5)
        self.set_text_color(*self.P.grey)
        self.set_y(8)
        self.cell(0, 4, f"{self.spec['title'].upper()}  •  DESIGN CODE "
                        f"{self.spec['code']}  •  US TERMS", align="L")
        self.set_draw_color(*self.P.line)
        self.set_line_width(0.2)
        self.line(M, 13.5, PAGE_W - M, 13.5)
        self.set_y(18)

    def footer(self):
        if self.page_no() == 1:
            return
        self.set_y(-14)
        self.set_draw_color(*self.P.line)
        self.set_line_width(0.2)
        self.line(M, PAGE_H - 14, PAGE_W - M, PAGE_H - 14)
        self.set_font("DejaVu", "", 7.5)
        self.set_text_color(*self.P.grey)
        self.cell(0, 5, f"Novality Store  ©  2026   •   Page {self.page_no()}/{{nb}}",
                  align="C")


pdf: PatternPDF = None


def setup(spec, P):
    global pdf
    pdf = PatternPDF(orientation="P", unit="mm", format="A4")
    pdf.set_spec(spec, P)
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_font("DejaVu", "", f"{FONT_DIR}/DejaVuSans.ttf")
    pdf.add_font("DejaVu", "B", f"{FONT_DIR}/DejaVuSans-Bold.ttf")
    pdf.add_font("Story", "", f"{FONT_DIR}/DejaVuSerif.ttf")
    pdf.add_font("Story", "B", f"{FONT_DIR}/DejaVuSerif-Bold.ttf")
    pdf.set_text_color(*P.ink)
    pdf.set_title(f"{spec['title']} — Crochet Pattern ({spec['code']})")
    pdf.set_author("Novality Store — Novality Crochet Studio")
    pdf.set_subject("Validated crochet pattern, US terms")
    pdf.set_creator("Crochet Pattern Checker — validated edition")
    return pdf


# ------------------------------------------------------------------ helpers
def h1(text, first=False):
    p = pdf.P
    h = 11
    y = pdf.get_y() + (0 if first else 5)
    if y + h > PAGE_H - 20:
        pdf.add_page()
        y = pdf.get_y()
    pdf.set_fill_color(*p.sage_dark)
    pdf.rect(M, y, CW, h, style="F")
    # auto-shrink long titles so they never overrun the banner
    pdf.set_font("Story", "B", 12.5)
    while pdf.get_string_width(text) > CW - 8 and h > 0:
        h -= 0.5
        size = max(8.0, 12.5 * h / 11)
        pdf.set_font("Story", "B", size)
    pdf.set_xy(M + 4, y)
    pdf.set_text_color(*p.white)
    pdf.cell(0, h, text, align="L")
    pdf.set_y(y + h + 4)
    pdf.set_text_color(*p.ink)


def h2(text):
    p = pdf.P
    pdf.set_font("DejaVu", "B", 10.5)
    pdf.set_text_color(*p.sage_dark)
    pdf.set_x(M)
    pdf.cell(0, 6, text, align="L")
    pdf.set_draw_color(*p.pink)
    pdf.set_line_width(0.5)
    y = pdf.get_y() + 6
    pdf.line(M, y, M + 26, y)
    pdf.set_y(y + 2.5)
    pdf.set_text_color(*p.ink)


def para(text, size=9, lh=4.6, color=None, after=2):
    pdf.set_font("DejaVu", "", size)
    pdf.set_text_color(*(color or pdf.P.ink))
    pdf.multi_cell(CW, lh, text, align="L")
    pdf.ln(after)
    pdf.set_text_color(*pdf.P.ink)


def bullet(text, bold_lead=None, size=9, lh=4.6):
    p = pdf.P
    if pdf.get_y() > PAGE_H - 26:
        pdf.add_page()
    pdf.set_font("DejaVu", "", size)
    pdf.set_fill_color(*p.pink)
    pdf.circle(M + 1.6, pdf.get_y() + 1.7, 0.75, style="F")
    pdf.set_x(M + 5)
    if bold_lead:
        pdf.set_font("DejaVu", "B", size)
        w = pdf.get_string_width(bold_lead + " ")
        pdf.cell(w, lh, bold_lead + " ")
        pdf.set_font("DejaVu", "", size)
    pdf.multi_cell(CW - (pdf.get_x() - M), lh, text, align="L")
    pdf.set_x(M)
    pdf.ln(0.8)


def auto_widths(headers, rows, fixed=None):
    """fixed = {col_index: mm} pinned columns; the rest share what's left."""
    n = len(headers)
    fixed = fixed or {}
    free = [i for i in range(n) if i not in fixed]
    used = sum(fixed.values())
    lens = []
    for i in free:
        mx = len(str(headers[i]))
        for r in rows:
            mx = max(mx, len(str(r[i])))
        lens.append(max(6, min(mx, 60)))
    total = sum(lens)
    avail = CW - used
    ws = [0] * n
    for i, L in zip(free, lens):
        ws[i] = max(14, avail * L / total)
    for i, w in fixed.items():
        ws[i] = w
    scale = CW / sum(ws)
    return [w * scale for w in ws]


def table(headers, rows, widths=None, aligns=None, size=8.6, lh=6.0,
          bold_cols=(), fixed=None):
    p = pdf.P
    if widths is None:
        widths = auto_widths(headers, rows, fixed)
    if len(rows) > 22:
        size = min(size, 8.2)
        lh = min(lh, max(5.0, 200 / (len(rows) + 1)))
    aligns = aligns or ["L"] * len(headers)
    pdf.set_font("DejaVu", "B", size)
    pdf.set_fill_color(*p.sage_dark)
    pdf.set_text_color(*p.white)
    pdf.set_draw_color(*p.line)
    pdf.set_line_width(0.2)
    x0, y = M, pdf.get_y()
    for hd, w in zip(headers, widths):
        pdf.set_xy(x0, y)
        pdf.cell(w, lh, " " + str(hd), border=1, align="L", fill=True)
        x0 += w
    pdf.set_y(y + lh)
    pdf.set_text_color(*p.ink)
    for r, row in enumerate(rows):
        h = lh
        for cell, w in zip(row, widths):
            pdf.set_font("DejaVu", "", size)
            n = pdf.multi_cell(w - 2, 4.4, str(cell), dry_run=True, output="LINES")
            h = max(h, 4.4 * len(n) + 1.8)
        fill = p.sage_light if r % 2 == 0 else p.white
        x0 = M
        for i, (cell, w, a) in enumerate(zip(row, widths, aligns)):
            pdf.set_xy(x0, pdf.get_y())
            pdf.set_font("DejaVu", "B" if i in bold_cols else "", size)
            pdf.set_fill_color(*fill)
            txt = (" " + str(cell)) if a == "L" else (str(cell) + " ")
            lines = pdf.multi_cell(w - 2, 4.4, txt, dry_run=True, output="LINES")
            if len(lines) > 1:
                # wrapped cell: shrink line height so total == row height
                pdf.multi_cell(w, h / len(lines), txt, border=1, align=a, fill=True)
            else:
                pdf.cell(w, h, txt, border=1, align=a, fill=True)
            x0 += w
        pdf.set_y(pdf.get_y() + h)
    pdf.ln(2.5)
    pdf.set_font("DejaVu", "", 9)


def box(title, lines, size=8.8):
    p = pdf.P
    pdf.set_font("DejaVu", "", size)
    w_eff = CW - 10
    h = 7 if title else 5
    for ln in lines:
        t = ln if isinstance(ln, str) else ln[0]
        n = pdf.multi_cell(w_eff, 4.3, t, dry_run=True, output="LINES")
        h += 4.3 * len(n) + 1.2
    if pdf.get_y() + h > PAGE_H - 22:
        pdf.add_page()
    y = pdf.get_y() + 1
    pdf.set_fill_color(*p.pink_light)
    pdf.set_draw_color(*p.pink)
    pdf.set_line_width(0.35)
    pdf.rect(M, y, CW, h, style="DF", round_corners=True, corner_radius=2.5)
    pdf.set_xy(M + 5, y + 2.4)
    if title:
        pdf.set_font("DejaVu", "B", 9.6)
        pdf.set_text_color(*p.pink)
        pdf.cell(0, 5, title)
        pdf.set_y(y + 7.4)
    pdf.set_x(M + 5)
    pdf.set_font("DejaVu", "", size)
    pdf.set_text_color(*p.ink)
    for ln in lines:
        t = ln if isinstance(ln, str) else ln[0]
        bold = False if isinstance(ln, str) else ln[1]
        pdf.set_x(M + 5)
        pdf.set_font("DejaVu", "B" if bold else "", size)
        pdf.multi_cell(w_eff, 4.3, t, align="L")
        pdf.set_x(M + 5)
    pdf.set_y(y + h + 3.5)
    pdf.set_text_color(*p.ink)


def colorways(chips):
    """chips = [(name, (r,g,b)), ...] rendered as a dot legend."""
    if not chips:
        return
    p = pdf.P
    pdf.ln(1)
    pdf.set_font("DejaVu", "B", 9.5)
    pdf.set_text_color(*p.sage_dark)
    pdf.cell(0, 6, "Colorways")
    pdf.ln(6.4)
    x, y = M, pdf.get_y()
    pdf.set_font("DejaVu", "", 8.6)
    pdf.set_text_color(*p.ink)
    for name, rgb in chips:
        w = pdf.get_string_width(name) + 9
        if x + w > PAGE_W - M:
            x = M
            y += 8
        pdf.set_fill_color(*rgb)
        pdf.circle(x + 2.2, y + 2.6, 2.0, style="F")
        pdf.set_xy(x + 5.4, y)
        pdf.cell(w - 5.4, 5.4, name)
        x += w + 2
    pdf.set_y(y + 9)


# ------------------------------------------------------------------ cover
def cover():
    spec, p = pdf.spec, pdf.P
    pdf.add_page()
    pdf.set_auto_page_break(auto=False)
    img_path = ROOT / spec["cover"]
    img = Image.open(img_path).convert("RGB")
    W, H = img.size
    tgt_h = int(W * 131 / PAGE_W)
    top = int((H - tgt_h) * 0.42)
    img.crop((0, top, W, top + tgt_h)).save("/tmp/_cover_crop.png")
    pdf.image("/tmp/_cover_crop.png", x=0, y=0, w=PAGE_W, h=131)

    pdf.set_fill_color(*p.sage_dark)
    pdf.rect(0, 131, PAGE_W, 2.2, style="F")
    pdf.set_y(140)
    pdf.set_font("Story", "B", 30 if len(spec["title"]) < 26 else 26)
    pdf.set_text_color(*p.ink)
    pdf.cell(0, 14, spec["title"], align="C")
    pdf.ln(15)
    pdf.set_font("DejaVu", "", 10.5)
    pdf.set_text_color(*p.sage_dark)
    sub = spec.get("subtitle", "A validated crochet pattern")
    pdf.multi_cell(CW, 5.6, sub, align="C")
    pdf.ln(2)
    pdf.set_font("DejaVu", "", 9.5)
    pdf.cell(0, 6, f"Design Code {spec['code']}", align="C")
    pdf.ln(9)

    labels = spec["badges"] + ["Stitch counts verified"]
    pdf.set_font("DejaVu", "B", 8.4)
    ws = [pdf.get_string_width(s) + 9 for s in labels]
    total = sum(ws) + 4 * (len(ws) - 1)
    if total > CW:  # wrap badges onto two rows
        rows = [labels[:2], labels[2:]]
        ws_rows = [ws[:2], ws[2:]]
    else:
        rows, ws_rows = [labels], [ws]
    y = pdf.get_y()
    for row_labels, row_ws in zip(rows, ws_rows):
        total = sum(row_ws) + 4 * (len(row_ws) - 1)
        x = (PAGE_W - total) / 2
        for s, w in zip(row_labels, row_ws):
            fill = p.pink_light if s == row_labels[0] else p.sage_light
            tc = p.pink if s == row_labels[0] else p.sage_dark
            pdf.set_fill_color(*fill)
            pdf.rect(x, y, w, 8.4, style="F", round_corners=True, corner_radius=4.2)
            pdf.set_xy(x, y)
            pdf.set_font("DejaVu", "B", 8.4)
            pdf.set_text_color(*tc)
            pdf.cell(w, 8.4, s, align="C")
            x += w + 4
        y += 11
    pdf.set_y(y + 3)

    pdf.set_font("DejaVu", "", 9.4)
    pdf.set_text_color(*p.grey)
    pdf.multi_cell(CW, 5.0, spec["size_line"], align="C")
    pdf.ln(1.5)
    pdf.multi_cell(CW, 5.0, spec["materials_line"], align="C")

    pdf.set_fill_color(*p.cream)
    pdf.rect(0, PAGE_H - 30, PAGE_W, 30, style="F")
    pdf.set_draw_color(*p.sage_mid)
    pdf.set_line_width(0.4)
    pdf.line(0, PAGE_H - 30, PAGE_W, PAGE_H - 30)
    pdf.set_y(PAGE_H - 25)
    pdf.set_font("Story", "B", 12)
    pdf.set_text_color(*p.sage_dark)
    pdf.cell(0, 7, "NOVALITY STORE", align="C")
    pdf.ln(7)
    pdf.set_font("DejaVu", "", 8.4)
    pdf.set_text_color(*p.grey)
    pdf.cell(0, 4.6, "Novality Crochet Studio  •  © 2026 Novality Store. All rights reserved.",
             align="C")
    pdf.set_text_color(*p.ink)
    pdf.set_auto_page_break(auto=True, margin=18)


# ------------------------------------------------------------------ pages
def page_intro():
    spec, p = pdf.spec, pdf.P
    pdf.add_page()
    s = spec.get("safety", {})
    box(s.get("title", "SAFETY — READ THIS FIRST"), s["lines"])

    h2("Materials")
    for lead, text in spec["materials"]:
        bullet(text, bold_lead=lead)
    if spec.get("gauge"):
        h2("Gauge & size check")
        box(None, spec["gauge"])
    if spec.get("pieces_summary"):
        h2(spec.get("pieces_summary_title", "The pieces"))
        t = spec["pieces_summary"]
        table(t[0], t[1], aligns=t[2] if len(t) > 2 else None, bold_cols=(0,))
    if spec.get("abbrev"):
        h2("Abbreviations — US terms")
        para(spec["abbrev"], size=8.8)


def page_techniques():
    spec = pdf.spec
    if not spec.get("techniques") and not spec.get("construction"):
        return
    pdf.add_page()
    if spec.get("construction_title"):
        h1(spec["construction_title"])
    if spec.get("construction"):
        h2("Construction at a glance")
        for lead, text in spec["construction"]:
            bullet(text, bold_lead=lead)
    if spec.get("techniques"):
        h2(spec.get("techniques_title", "The techniques that make this pattern"))
        for i, (lead, text) in enumerate(spec["techniques"], 1):
            bullet(text, bold_lead=f"{i}. {lead} —")
    for t in spec.get("sizing_tables", []):
        h2(t.get("title", "Sizing"))
        table(t["headers"], t["rows"], aligns=t.get("aligns"), bold_cols=(0,))
        if t.get("note"):
            para(t["note"], size=8.8, color=pdf.P.grey)
    for bx in spec.get("technique_boxes", []):
        box(bx.get("title"), bx["lines"])


def page_pieces():
    spec = pdf.spec
    for piece in spec["pieces"]:
        pdf.add_page()
        h1(piece["title"])
        if piece.get("note"):
            para(piece["note"], size=8.6, color=pdf.P.grey, after=2)
        t = piece.get("table")
        if t:
            table(t["headers"], t["rows"], aligns=t.get("aligns"),
                  widths=t.get("widths"), bold_cols=(0,), fixed=t.get("fixed"))
        for text in piece.get("paras", []):
            para(text, size=9)
        for lead, text in piece.get("finish", []):
            bullet(text, bold_lead=lead)
        for bx in piece.get("boxes", []):
            box(bx.get("title"), bx["lines"])
        for sub in piece.get("extra_tables", []):
            if sub.get("title"):
                h2(sub["title"])
            table(sub["headers"], sub["rows"], aligns=sub.get("aligns"),
                  widths=sub.get("widths"), bold_cols=(0,), fixed=sub.get("fixed"))
            for text in sub.get("paras", []):
                para(text, size=9)


def page_assembly():
    spec, p = pdf.spec, pdf.P
    a = spec.get("assembly")
    if not a:
        return
    pdf.add_page()
    h1(a.get("title", "Assembly & finishing"))
    if a.get("intro"):
        para(a["intro"], size=9)
    for lead, text in a.get("bullets", []):
        bullet(text, bold_lead=lead)
    for bx in a.get("boxes", []):
        box(bx.get("title"), bx["lines"])
    if a.get("checklist"):
        box("Before you sew — lay every component out and check", a["checklist"])
    if a.get("listing"):
        h2("For your Etsy listing")
        for lead, text in a["listing"]:
            bullet(text, bold_lead=lead)
    if a.get("care"):
        h2("Care")
        para(a["care"], size=8.8)
    colorways(spec.get("colorways"))


def page_terms():
    spec, p = pdf.spec, pdf.P
    pdf.add_page()
    if spec.get("troubleshooting"):
        h1("Troubleshooting")
        for lead, text in spec["troubleshooting"]:
            bullet(text, bold_lead=lead)
    h1("Why this pattern works — validation summary")
    para("Every stitch count in this pattern was checked with deterministic math "
         "(Crochet Pattern Checker): round-by-round production vs. consumption, "
         "stated counts, and every size claim against the stated gauge.", size=8.8)
    rows = [[c, r] for c, r in spec["checks"]]
    table(["Check", "Result"], rows, widths=[138, 40], aligns=["L", "C"])

    h1("Terms of use")
    h2("Copyright & ownership")
    para(f"This crochet pattern — including all instructions, stitch counts, "
         f"photography and design elements — is the original work and intellectual "
         f"property of Novality Store, designed by Novality Crochet Studio. "
         f"Design Code {spec['code']}. © 2026 Novality Store. All rights reserved.",
         size=8.5, after=1)
    h2("You may")
    para(f"Make as many finished {spec.get('terms_name', 'items')} as you like for "
         f"yourself, gifts, or charity. Sell physical finished items made from this "
         f"pattern in small batches, in shops, markets and online, provided credit is "
         f"given to “Novality Store”.", size=8.5, after=1)
    h2("You may not")
    para("Resell, share, redistribute, translate, rewrite, publish or upload this "
         "digital PDF or its contents in any form. Do not alter, copy or recolor the "
         "pattern and claim it as your own. Do not use the Novality Store name, logo "
         "or photos beyond crediting the pattern. Do not mass-produce finished items "
         "commercially without written permission.", size=8.5, after=1)
    if spec.get("safety_reminder"):
        box("SAFETY REMINDER", [spec["safety_reminder"]])
    para(f"Happy crocheting! Tag your makes with  #NovalityStore  and  "
         f"{spec['tags']}  — thank you for supporting an independent pattern "
         f"designer.", size=8.8)

    # closing brand flourish
    pdf.ln(4)
    y = pdf.get_y()
    if y < PAGE_H - 30:
        pdf.set_draw_color(*pdf.P.sage_mid)
        pdf.set_line_width(0.4)
        pdf.line(M + 30, y, PAGE_W - M - 30, y)
        pdf.set_y(y + 3)
        pdf.set_font("Story", "B", 10)
        pdf.set_text_color(*pdf.P.sage_dark)
        pdf.cell(0, 6, "NOVALITY STORE  ·  NOVALITY CROCHET STUDIO", align="C")
        pdf.set_y(y + 10)
        pdf.set_font("DejaVu", "", 7.5)
        pdf.set_text_color(*pdf.P.grey)
        pdf.cell(0, 4, f"Design Code {spec['code']}  •  US terms  •  stitch counts "
                       f"independently verified", align="C")
        pdf.set_text_color(*pdf.P.ink)


def build(spec, edition="retail"):
    spec = dict(spec)  # don't mutate the shared spec
    if edition == "retail":
        P = make_palette(spec["theme"]["dark"], spec["theme"]["accent"],
                         spec["theme"]["soft"], spec["theme"]["box_bg"],
                         spec["theme"]["box_edge"])
    else:
        P = GREY_PALETTE
        src = ROOT / spec["cover"]
        grey = ROOT / "assets" / f"{spec['slug']}_cover_grey.png"
        Image.open(src).convert("L").convert("RGB").save(grey)
        spec["cover"] = str(grey.relative_to(ROOT))
    setup(spec, P)
    cover()
    page_intro()
    page_techniques()
    page_pieces()
    page_assembly()
    page_terms()
    slug = spec["slug"]
    suffix = "" if edition == "retail" else "_print"
    out = ROOT / "deliverables" / f"{spec['file_stem']}{suffix}.pdf"
    pdf.output(out)
    print(f"[{edition}] {out.name}: {pdf.page_no()} pages, "
          f"{out.stat().st_size/1024:.0f} KB")
    return out
