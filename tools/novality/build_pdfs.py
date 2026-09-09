"""Build the final Novality Store customer PDFs in final_patterns/.

Clean, warm, minimal design:
  * A4, generous whitespace, one accent colour (terracotta) on warm sand neutrals
  * typographic cover with brand, badges and finished-size panel
  * hairline section headings, zebra round tables with repeating headers
  * running footer with (c) notice, design code and page number on every page
  * final Terms of Use page with the full copyright notice verbatim
"""
from __future__ import annotations

from pathlib import Path

from fpdf import FPDF, XPos, YPos
from fpdf.enums import MethodReturnValue

from . import PATTERNS, schema

OUT = Path("final_patterns")

# palette (warm, craft-focused, print friendly)
INK = (58, 47, 43)          # warm dark brown
ACCENT = (166, 84, 48)      # terracotta
ACCENT_SOFT = (230, 215, 200)   # soft sand
HAIR = (210, 194, 176)      # hairline
MUTED = (128, 106, 94)      # muted brown-grey
WHITE = (255, 255, 255)
PAPER = (255, 255, 255)

FONTS = {
    ("serif", ""): "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    ("serif", "B"): "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    ("sans", ""): "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ("sans", "B"): "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
}

PAGE_W, PAGE_H = 210.0, 297.0
M_L, M_R, M_T, M_B = 17.0, 17.0, 22.0, 20.0
CONTENT_W = PAGE_W - M_L - M_R
ASSETS = Path(__file__).resolve().parent.parent.parent / "final_patterns" / "assets"

# colourway name -> display swatch hex
COLORWAY_COLORS = {
    "Ginger": "#C57A3A", "Caramel": "#B98A5E", "Highland black": "#2F2A26",
    "Cream": "#F1E7D3", "Roan red": "#B05A36",
    "Classic cream": "#F4EBDC", "Pumpkin orange": "#E08A3C",
    "Bat lavender": "#A98CC9", "Ghostly white": "#FAF6EE", "Charcoal": "#4B4441",
    "Sage & oat": "#A8B69A",
    "Classic pink": "#F2B9C6", "White leucistic": "#FBF3EC",
    "Melanoid black": "#2B2826", "Mint": "#B8DFC9", "Lavender": "#C3AED8",
    "Classic warm brown": "#8B6248", "Soft grey": "#B9B3AC",
    "Sandy beige": "#D8BE9A", "Cocoa": "#6F4E37",
    "Grey tabby": "#9A948B", "Orange ginger": "#D98B45", "Black": "#322D2A",
    "Calico": "#D19468",
    "Sage green": "#A8BE9C", "Dusty teal": "#7FA6A1", "Lilac": "#C4B1D8",
    "Blush pink": "#EFC0CC",
    "Sage": "#A9B79B", "Dusty pink": "#DBAFB2", "Pale grey": "#C8C4BE",
    "Butter yellow": "#F0D689",
}


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def asset(num, kind):
    p = ASSETS / f"p{num:02d}_{kind}.jpg"
    return p if p.exists() else None


class PatternPDF(FPDF):
    def __init__(self, pdata):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.pdata = pdata
        self.is_cover = True
        for (fam, style), path in FONTS.items():
            self.add_font(fam, style, path)
        self.set_margins(M_L, M_T, M_R)
        self.set_auto_page_break(True, M_B)

    def footer(self):
        if self.page_no() == 1:
            return
        self.set_y(-15)
        self.set_draw_color(*HAIR)
        self.set_line_width(0.2)
        self.line(M_L, PAGE_H - 16, PAGE_W - M_R, PAGE_H - 16)
        self.set_font("sans", "", 7)
        self.set_text_color(*MUTED)
        self.cell(CONTENT_W * 0.6, 8, schema.FOOTER_LINE, new_x=XPos.RIGHT, new_y=YPos.TOP)
        right = f"{self.pdata['design_code']}  ·  page {self.page_no()}"
        self.cell(CONTENT_W * 0.4, 8, right, align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def header(self):
        if self.page_no() == 1:
            return
        self.set_y(10)
        self.set_font("sans", "B", 7.5)
        self.set_text_color(*ACCENT)
        self.set_char_spacing(1.2)
        self.cell(CONTENT_W * 0.5, 5, "NOVALITY STORE", new_x=XPos.RIGHT, new_y=YPos.TOP)
        self.set_char_spacing(0)
        self.set_font("sans", "", 7.5)
        self.set_text_color(*MUTED)
        title = f"{self.pdata['title']}"
        self.cell(CONTENT_W * 0.5, 5, title, align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_draw_color(*HAIR)
        self.set_line_width(0.2)
        self.line(M_L, 18, PAGE_W - M_R, 18)
        self.set_y(M_T + 2)


def _badge_row(pdf, items, y):
    badges = items
    widths = [pdf.get_string_width(b) + 12 for b in badges]
    pdf.set_font("sans", "B", 8)
    widths = [pdf.get_string_width(b) + 14 for b in badges]
    gap = 6
    total = sum(widths) + gap * (len(badges) - 1)
    x = (PAGE_W - total) / 2
    pdf.set_line_width(0.25)
    for b, w in zip(badges, widths):
        pdf.set_draw_color(*ACCENT)
        pdf.set_text_color(*ACCENT)
        pdf.set_fill_color(*PAPER)
        # pill
        r = 4
        pdf.rect(x, y, w, 9, style="DF", round_corners=True, corner_radius=r)
        pdf.set_xy(x, y + 1.6)
        pdf.cell(w, 6, b, align="C")
        x += w + gap


def cover(pdf, p):
    pdf.add_page()
    pdf.is_cover = True
    pdf.set_fill_color(*PAPER)
    pdf.rect(0, 0, PAGE_W, PAGE_H, style="F")
    # double frame
    pdf.set_draw_color(*ACCENT)
    pdf.set_line_width(0.6)
    pdf.rect(12, 12, PAGE_W - 24, PAGE_H - 24)
    pdf.set_line_width(0.2)
    pdf.rect(15, 15, PAGE_W - 30, PAGE_H - 30)
    # brand
    pdf.set_y(34)
    pdf.set_font("sans", "B", 10)
    pdf.set_text_color(*ACCENT)
    pdf.set_char_spacing(4)
    pdf.cell(0, 6, "NOVALITY  STORE", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_char_spacing(0)
    pdf.set_font("sans", "", 7.5)
    pdf.set_text_color(*MUTED)
    pdf.cell(0, 5, "handmade crochet patterns", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    # ornament
    y = pdf.get_y() + 8
    pdf.set_draw_color(*HAIR)
    pdf.set_line_width(0.25)
    cx = PAGE_W / 2
    pdf.line(cx - 32, y, cx - 6, y)
    pdf.line(cx + 6, y, cx + 32, y)
    pdf.set_fill_color(*ACCENT)
    pdf.ellipse(cx - 1.1, y - 1.1, 2.2, 2.2, style="F")
    pdf.set_y(y + 10)
    # title
    pdf.set_font("serif", "B", 23)
    pdf.set_text_color(*INK)
    pdf.multi_cell(0, 10.5, p["title"], align="C")
    pdf.ln(1.5)
    # tagline
    pdf.set_font("serif", "", 9.5)
    pdf.set_text_color(*MUTED)
    pdf.set_x(M_L + 15)
    pdf.multi_cell(CONTENT_W - 30, 5.0, p["tagline"], align="C")
    pdf.ln(6)
    _badge_row(pdf, p["meta"], pdf.get_y())
    pdf.set_y(pdf.get_y() + 13)
    # hero photo
    hero = asset(p["number"], "hero")
    if hero:
        h_w = 72.0
        x = (PAGE_W - h_w) / 2
        y = pdf.get_y()
        pdf.set_fill_color(*ACCENT_SOFT)
        pdf.rect(x - 3, y - 3, h_w + 6, h_w + 6, style="F")
        pdf.image(str(hero), x=x, y=y, w=h_w)
        pdf.set_draw_color(*ACCENT)
        pdf.set_line_width(0.35)
        pdf.rect(x - 3, y - 3, h_w + 6, h_w + 6)
        pdf.set_y(y + h_w + 9)
    # finished size panel
    panel_w = 158
    x = (PAGE_W - panel_w) / 2
    y0 = pdf.get_y()
    pdf.set_fill_color(*ACCENT_SOFT)
    pdf.set_draw_color(*HAIR)
    n = len(p["finished_size"])
    line_h = 5.6
    panel_h = 9 + n * line_h
    pdf.rect(x, y0, panel_w, panel_h, style="DF", round_corners=True, corner_radius=2.5)
    pdf.set_xy(x, y0 + 3)
    pdf.set_font("sans", "B", 7.5)
    pdf.set_text_color(*ACCENT)
    pdf.set_char_spacing(1.5)
    pdf.cell(panel_w, 4.5, "F I N I S H E D   S I Z E", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_char_spacing(0)
    pdf.set_font("sans", "", 8.2)
    pdf.set_text_color(*INK)
    for line in p["finished_size"]:
        pdf.set_x(x + 8)
        pdf.multi_cell(panel_w - 16, line_h, "·  " + line, align="C")
    pdf.set_y(y0 + panel_h + 8)
    # design code
    pdf.set_font("sans", "", 8.5)
    pdf.set_text_color(*MUTED)
    pdf.cell(0, 5, f"Design Code {p['design_code']}",
             align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    # bottom copyright on cover
    pdf.set_y(PAGE_H - 34)
    pdf.set_font("sans", "", 7.5)
    pdf.set_text_color(*MUTED)
    pdf.cell(0, 5, "© 2026 Novality Store. All rights reserved.", align="C",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 5, "This pattern is for personal use only. See Terms of Use on the final page.",
             align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)


def section(pdf, title, space_before=7):
    pdf.ln(space_before)
    if pdf.get_y() > PAGE_H - M_B - 24:
        pdf.add_page()
    pdf.set_font("sans", "B", 10.5)
    pdf.set_text_color(*ACCENT)
    pdf.set_char_spacing(1.4)
    pdf.cell(0, 7, title.upper(), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_char_spacing(0)
    y = pdf.get_y() - 1
    pdf.set_draw_color(*HAIR)
    pdf.set_line_width(0.25)
    pdf.line(M_L, y, PAGE_W - M_R, y)
    pdf.ln(2.5)


def sub_heading(pdf, text, keep_with_next=22):
    need = keep_with_next
    if pdf.get_y() > PAGE_H - M_B - (10 + need):
        pdf.add_page()
    pdf.ln(1.5)
    pdf.set_font("serif", "B", 12)
    pdf.set_text_color(*INK)
    pdf.multi_cell(0, 6.5, text)
    pdf.ln(0.5)


def body(pdf, text, size=9.2, lh=4.9, style="", color=INK, bullet=False, indent=0):
    pdf.set_font("sans", style, size)
    pdf.set_text_color(*color)
    pdf.set_x(M_L + indent)
    prefix = "•  " if bullet else ""
    pdf.multi_cell(CONTENT_W - indent, lh, prefix + text)
    pdf.ln(0.6)


def safety_box(pdf, paragraphs):
    pdf.ln(2)
    # estimate height
    pdf.set_font("sans", "", 9.2)
    total_h = 12
    heights = []
    for t in paragraphs:
        h = pdf.multi_cell(CONTENT_W - 14, 4.9, t, dry_run=True, output=MethodReturnValue.HEIGHT)
        heights.append(h)
        total_h += h + 2.2
    if pdf.get_y() > PAGE_H - M_B - total_h:
        pdf.add_page()
    y0 = pdf.get_y()
    pdf.set_fill_color(*ACCENT_SOFT)
    pdf.set_draw_color(*ACCENT)
    pdf.rect(M_L, y0, CONTENT_W, total_h, style="DF", round_corners=True, corner_radius=2.5)
    pdf.set_xy(M_L + 7, y0 + 4.5)
    pdf.set_font("sans", "B", 8.5)
    pdf.set_text_color(*ACCENT)
    pdf.set_char_spacing(1.5)
    pdf.cell(CONTENT_W - 14, 5, "S A F E T Y   F I R S T", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_char_spacing(0)
    pdf.set_font("sans", "", 9.2)
    pdf.set_text_color(*INK)
    for t, h in zip(paragraphs, heights):
        pdf.set_x(M_L + 7)
        pdf.multi_cell(CONTENT_W - 14, 4.9, t)
        pdf.ln(2.2)
    pdf.set_y(y0 + total_h + 2)


COLS = [16, 90, 14, 56]   # Rnd | Instruction | Sts | Note  (sums to CONTENT_W)


def round_table(pdf, rows):
    header = ["Rnd", "Instruction", "Sts", "Note"]
    pdf.set_line_width(0.2)

    def draw_header():
        pdf.set_font("sans", "B", 8.2)
        pdf.set_fill_color(*ACCENT)
        pdf.set_text_color(*WHITE)
        h = 6.5
        for w, txt in zip(COLS, header):
            pdf.cell(w, h, txt, border=0, align="L", fill=True)
        pdf.ln(h)

    def row_height(row):
        pdf.set_font("sans", "", 8.6)
        cells = [row["label"], row["text"],
                 f"({row['stated']})" if row.get("stated") is not None else "-",
                 row.get("note") or "-"]
        hmax = 0
        for w, txt in zip(COLS, cells):
            h = pdf.multi_cell(w - 3, 4.3, txt, dry_run=True, output=MethodReturnValue.HEIGHT)
            hmax = max(hmax, h)
        return hmax + 2.6

    def draw_row(idx, row, h):
        cells = [row["label"], row["text"],
                 f"({row['stated']})" if row.get("stated") is not None else "-",
                 row.get("note") or "-"]
        y0 = pdf.get_y()
        if idx % 2 == 1:
            pdf.set_fill_color((250, 246, 241))
            pdf.rect(M_L, y0, CONTENT_W, h, style="F")
        x = M_L
        styles = [("sans", "B", INK), ("sans", "", INK), ("sans", "B", ACCENT), ("sans", "", MUTED)]
        for (w, txt, (fam, st, col)) in zip(COLS, cells, styles):
            pdf.set_xy(x + 1.5, y0 + 1.3)
            pdf.set_font(fam, st, 8.6)
            pdf.set_text_color(*col)
            pdf.multi_cell(w - 3, 4.3, txt)
            x += w
        pdf.set_draw_color(*HAIR)
        pdf.line(M_L, y0 + h, PAGE_W - M_R, y0 + h)
        pdf.set_y(y0 + h)

    draw_header()
    for idx, row in enumerate(rows):
        h = row_height(row)
        if pdf.get_y() > PAGE_H - M_B - h:
            pdf.add_page()
            draw_header()
        draw_row(idx, row, h)
    pdf.ln(2)


def generic_table(pdf, headers, rows, widths=None):
    if widths is None:
        widths = [CONTENT_W / len(headers)] * len(headers)
    pdf.set_line_width(0.2)

    def draw_header():
        pdf.set_font("sans", "B", 8.4)
        pdf.set_fill_color(*ACCENT)
        pdf.set_text_color(*WHITE)
        for w, txt in zip(widths, headers):
            pdf.cell(w, 6.5, txt, fill=True)
        pdf.ln(6.5)

    def row_height(cells):
        pdf.set_font("sans", "", 8.8)
        hmax = 6.5
        for w, txt in zip(widths, cells):
            h = pdf.multi_cell(w - 3, 4.6, txt, dry_run=True, output=MethodReturnValue.HEIGHT)
            hmax = max(hmax, h + 2.4)
        return hmax

    def draw(idx, cells, h):
        y0 = pdf.get_y()
        if idx % 2 == 1:
            pdf.set_fill_color((250, 246, 241))
            pdf.rect(M_L, y0, CONTENT_W, h, style="F")
        x = M_L
        for w, txt in zip(widths, cells):
            pdf.set_xy(x + 1.5, y0 + 1.3)
            pdf.set_font("sans", "", 8.8)
            pdf.set_text_color(*INK)
            pdf.multi_cell(w - 3, 4.6, txt)
            x += w
        pdf.set_draw_color(*HAIR)
        pdf.line(M_L, y0 + h, PAGE_W - M_R, y0 + h)
        pdf.set_y(y0 + h)

    draw_header()
    for idx, cells in enumerate(rows):
        h = row_height(cells)
        if pdf.get_y() > PAGE_H - M_B - h:
            pdf.add_page()
            draw_header()
        draw(idx, cells, h)
    pdf.ln(2)


def trouble_table(pdf, items):
    for i, (prob, fix) in enumerate(items):
        text_prob = f"• {prob}"
        pdf.set_font("sans", "B", 9.2)
        h1 = pdf.multi_cell(CONTENT_W - 8, 5, text_prob, dry_run=True, output=MethodReturnValue.HEIGHT)
        pdf.set_font("sans", "", 9.2)
        h2 = pdf.multi_cell(CONTENT_W - 8, 4.9, fix, dry_run=True, output=MethodReturnValue.HEIGHT)
        total = h1 + h2 + 2.4
        if pdf.get_y() > PAGE_H - M_B - total:
            pdf.add_page()
        pdf.set_x(M_L + 3)
        pdf.set_font("sans", "B", 9.2)
        pdf.set_text_color(*ACCENT)
        pdf.multi_cell(CONTENT_W - 8, 5, text_prob)
        pdf.set_x(M_L + 8)
        pdf.set_font("sans", "", 9.2)
        pdf.set_text_color(*INK)
        pdf.multi_cell(CONTENT_W - 8 - 5, 4.9, fix)
        pdf.ln(2.4)


def colorway_swatches(pdf, colors):
    """Named colour swatches in a strict 3-column grid (always aligned)."""
    pdf.ln(2)
    cols = 3
    col_w = CONTENT_W / cols
    row_h = 9.0
    for i, c in enumerate(colors):
        col = i % cols
        if col == 0 and i > 0:
            pdf.ln(row_h)
        x = M_L + col * col_w + 3
        y = pdf.get_y()
        rgb = hex_to_rgb(COLORWAY_COLORS.get(c, "#E8D7C6"))
        pdf.set_fill_color(*rgb)
        pdf.set_draw_color(*HAIR)
        pdf.set_line_width(0.25)
        # swatch: filled circle with soft outline
        pdf.ellipse(x, y + 0.6, 5.6, 5.6, style="DF")
        pdf.set_xy(x + 8.4, y + 1.0)
        pdf.set_font("sans", "", 8.8)
        pdf.set_text_color(*INK)
        pdf.cell(col_w - 12, 6.4, c)
    pdf.ln(row_h + 1)


def copyright_box(pdf, notice):
    pdf.set_font("sans", "", 9.0)
    heights = []
    total_h = 10
    for para in notice.split("\n\n"):
        h = pdf.multi_cell(CONTENT_W - 16, 4.8, para, align="J",
                           dry_run=True, output=MethodReturnValue.HEIGHT)
        heights.append(h)
        total_h += h + 2.4
    if pdf.get_y() > PAGE_H - M_B - total_h:
        pdf.add_page()
    y0 = pdf.get_y()
    pdf.set_draw_color(*ACCENT)
    pdf.set_line_width(0.4)
    pdf.set_fill_color(*PAPER)
    pdf.rect(M_L, y0, CONTENT_W, total_h, style="DF", round_corners=True, corner_radius=2.5)
    pdf.set_xy(M_L + 8, y0 + 5)
    pdf.set_font("sans", "", 9.0)
    pdf.set_text_color(*INK)
    for para, h in zip(notice.split("\n\n"), heights):
        pdf.multi_cell(CONTENT_W - 16, 4.8, para, align="J")
        pdf.ln(2.4)
        pdf.set_x(M_L + 8)
    pdf.set_y(y0 + total_h + 3)
    pdf.set_line_width(0.2)


def build(p):
    pdf = PatternPDF(p)
    pdf.set_title(f"{p['title']} - crochet pattern - Novality Store")
    pdf.set_author("Novality Store")
    pdf.set_subject(f"Crochet pattern {p['design_code']} - {p['title']}")
    pdf.set_keywords(f"crochet, pattern, amigurumi, novality store, {p['id']}")
    cover(pdf, p)
    pdf.add_page()

    section(pdf, "Pattern overview", space_before=1)
    body(pdf, p["tagline"], size=9.6, lh=5.2)
    pdf.ln(1)
    body(pdf, "Finished size:", style="B", size=9.4)
    for fs in p["finished_size"]:
        body(pdf, fs, bullet=True, indent=3)
    for n in p.get("notes", []):
        body(pdf, n)
    if p["meta"]:
        body(pdf, "  ·  ".join(p["meta"]), color=MUTED, size=8.8)

    safety_box(pdf, p["safety"])

    section(pdf, "Materials")
    for m in p["materials"]:
        body(pdf, m, bullet=True, indent=3)

    section(pdf, "Gauge")
    for g in p["gauge"]:
        body(pdf, g)

    section(pdf, "Abbreviations")
    abbr = p["abbreviations"]
    half = (len(abbr) + 1) // 2
    col_w = CONTENT_W / 2
    y0 = pdf.get_y()
    x0 = M_L
    for i, line in enumerate(abbr):
        col = 0 if i < half else 1
        row = i if i < half else i - half
        pdf.set_xy(x0 + col * col_w, y0 + row * 5.2)
        parts = line.split(" - ", 1)
        pdf.set_font("sans", "B", 8.8)
        pdf.set_text_color(*ACCENT)
        w1 = pdf.get_string_width(parts[0] + "  ")
        pdf.cell(w1, 5, parts[0] + "  ")
        pdf.set_font("sans", "", 8.8)
        pdf.set_text_color(*INK)
        pdf.cell(col_w - w1 - 4, 5, parts[1] if len(parts) > 1 else "")
    pdf.set_y(y0 + half * 5.2 + 2)

    if p.get("construction") or p.get("techniques"):
        section(pdf, "Construction & techniques")
        if p.get("construction"):
            body(pdf, p["construction"])
            pdf.ln(1)
        for i, (name, bodytext) in enumerate(p.get("techniques", []), start=1):
            pdf.set_font("serif", "B", 10)
            h1 = pdf.multi_cell(CONTENT_W, 5.4, f"{i}. {name}",
                                dry_run=True, output=MethodReturnValue.HEIGHT)
            pdf.set_font("sans", "", 9.2)
            h2 = pdf.multi_cell(CONTENT_W - 8, 4.9, bodytext,
                                dry_run=True, output=MethodReturnValue.HEIGHT)
            if pdf.get_y() > PAGE_H - M_B - (h1 + h2 + 2):
                pdf.add_page()
            pdf.set_font("serif", "B", 10)
            pdf.set_text_color(*INK)
            pdf.multi_cell(CONTENT_W, 5.4, f"{i}. {name}")
            pdf.set_x(M_L + 5)
            pdf.set_font("sans", "", 9.2)
            pdf.multi_cell(CONTENT_W - 8, 4.9, bodytext)
            pdf.ln(1.6)

    section(pdf, "Instructions")
    for piece in p["pieces"]:
        # piece heading + intro kept with first rows
        sub_heading(pdf, piece["name"])
        if piece.get("intro"):
            body(pdf, piece["intro"], size=9.0, color=MUTED, lh=4.8)
            pdf.ln(0.5)
        for sub in piece["subpieces"]:
            if sub.get("name"):
                pdf.set_font("sans", "B", 9.2)
                h = pdf.multi_cell(CONTENT_W, 5.2, sub["name"],
                                   dry_run=True, output=MethodReturnValue.HEIGHT)
                if pdf.get_y() > PAGE_H - M_B - (h + 14):
                    pdf.add_page()
                pdf.set_text_color(*ACCENT)
                pdf.multi_cell(CONTENT_W, 5.2, sub["name"])
                pdf.ln(0.8)
            if sub.get("rows"):
                round_table(pdf, sub["rows"])
            for note in sub.get("notes", []):
                body(pdf, note, size=9.0, color=INK, lh=4.8)
            pdf.ln(1)

    if p.get("assembly"):
        wip = asset(p["number"], "wip")
        if wip:
            w = 92.0
            if pdf.get_y() > PAGE_H - M_B - 106:
                pdf.add_page()
            x = (PAGE_W - w) / 2
            y = pdf.get_y()
            pdf.set_fill_color(*ACCENT_SOFT)
            pdf.rect(x - 2.5, y - 2.5, w + 5, w + 5, style="F")
            pdf.image(str(wip), x=x, y=y, w=w)
            pdf.set_draw_color(*ACCENT)
            pdf.set_line_width(0.35)
            pdf.rect(x - 2.5, y - 2.5, w + 5, w + 5)
            pdf.set_y(y + w + 7.5)
            pdf.set_font("serif", "", 8.5)
            pdf.set_text_color(*MUTED)
            pdf.cell(0, 5, "On the hook - what your rounds should look like as they grow",
                     align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        section(pdf, "Finishing & assembly")
        for a in p["assembly"]:
            if a == "":
                pdf.ln(2)
                continue
            numbered = len(a) > 2 and a[0].isdigit() and a[1] in "."
            body(pdf, a, bullet=not numbered, indent=3)

    if p.get("troubleshooting"):
        section(pdf, "Troubleshooting")
        trouble_table(pdf, p["troubleshooting"])

    if p.get("colorways"):
        section(pdf, "Colorways")
        colorway_swatches(pdf, p["colorways"])

    tips_present = p.get("extras") or p.get("designer_notes")
    if tips_present:
        section(pdf, "Helpful tips")
        for extra in p.get("extras", []):
            sub_heading(pdf, extra["name"], keep_with_next=16)
            if extra["type"] == "table":
                generic_table(pdf, extra["headers"], extra["rows"])
                if extra.get("outro"):
                    body(pdf, extra["outro"], size=9.0)
            else:
                for ln in extra.get("lines", []):
                    body(pdf, ln)
        for d in p.get("designer_notes", []):
            body(pdf, d, bullet=True, indent=3)

    # ---- terms of use (own page)
    pdf.add_page()
    section(pdf, "Terms of Use", space_before=1)
    sub_heading(pdf, "Copyright & ownership", keep_with_next=30)
    body(pdf, p["terms"]["ownership"])
    copyright_box(pdf, schema.COPYRIGHT_NOTICE)
    sub_heading(pdf, "You may", keep_with_next=18)
    body(pdf, p["terms"]["may"])
    sub_heading(pdf, "You may not", keep_with_next=26)
    body(pdf, p["terms"]["maynot"])
    sub_heading(pdf, "Safety reminder", keep_with_next=22)
    body(pdf, p["terms"]["safety"])

    pdf.ln(8)
    pdf.set_font("serif", "B", 14)
    pdf.set_text_color(*ACCENT)
    pdf.cell(0, 8, "Happy crocheting!", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("sans", "", 9.2)
    pdf.set_text_color(*INK)
    pdf.multi_cell(0, 5.2,
                   f"Tag your makes with #NovalityStore and {p['hashtag']} - "
                   f"{p['closing']}", align="C")
    pdf.ln(4)
    pdf.set_font("sans", "", 8)
    pdf.set_text_color(*MUTED)
    pdf.cell(0, 5, f"{p['title']}  ·  Design Code {p['design_code']}  ·  Novality Store",
             align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    slug = p["title"].replace(" ", "_")
    out = OUT / f"Pattern_{p['number']:02d}_{slug}.pdf"
    pdf.output(str(out))
    return out, pdf.page_no()


def build_all():
    OUT.mkdir(exist_ok=True)
    results = []
    for p in PATTERNS:
        out, pages = build(p)
        results.append((out.name, pages))
        print(f"built {out} ({pages} pages)")
    return results


if __name__ == "__main__":
    build_all()
