#!/usr/bin/env python3
"""Generate the sellable 'Willow the Bunny Lovey' pattern PDF (Etsy-ready).

Two editions from one source of truth:
  * Retail (full colour)
  * Print-friendly (greyscale, low ink)

All content is the VALIDATED v2 pattern (see patterns/willow_bunny_lovey_v2_fixed.txt
and the validation summary in the appendix). US terminology throughout.
"""
from __future__ import annotations

from pathlib import Path

from fpdf import FPDF
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
COVER_SRC = ROOT / "assets" / "willow_cover.png"
OUT_DIR = ROOT / "deliverables"

PAGE_W, PAGE_H = 210, 297
M = 16  # margin, mm
CW = PAGE_W - 2 * M  # content width

# ---------------------------------------------------------------- palette
class Palette:
    ink = (56, 54, 52)
    grey = (118, 114, 109)
    sage_dark = (58, 92, 64)
    sage_mid = (122, 154, 122)
    sage_light = (233, 239, 231)
    pink = (196, 126, 140)
    pink_light = (247, 236, 239)
    cream = (250, 247, 241)
    line = (208, 213, 205)
    white = (255, 255, 255)


class Grey:
    ink = (45, 45, 45)
    grey = (110, 110, 110)
    sage_dark = (60, 60, 60)
    sage_mid = (130, 130, 130)
    sage_light = (238, 238, 238)
    pink = (90, 90, 90)
    pink_light = (242, 242, 242)
    cream = (251, 251, 251)
    line = (205, 205, 205)
    white = (255, 255, 255)


class PatternPDF(FPDF):
    P = Palette()

    def set_palette(self, P):
        self.P = P

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("DejaVu", "", 7.5)
        self.set_text_color(*self.P.grey)
        self.set_y(8)
        self.cell(0, 4, "WILLOW THE BUNNY LOVEY  •  DESIGN CODE NS 10  •  US TERMS",
                  align="L")
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


pdf: PatternPDF = None  # set in build()


# ---------------------------------------------------------------- helpers
def setup(P):
    global pdf
    pdf = PatternPDF(orientation="P", unit="mm", format="A4")
    pdf.set_palette(P)
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_font("DejaVu", "", f"{FONT_DIR}/DejaVuSans.ttf")
    pdf.add_font("DejaVu", "B", f"{FONT_DIR}/DejaVuSans-Bold.ttf")
    pdf.add_font("Story", "", f"{FONT_DIR}/DejaVuSerif.ttf")
    pdf.add_font("Story", "B", f"{FONT_DIR}/DejaVuSerif-Bold.ttf")
    pdf.set_text_color(*P.ink)
    pdf.set_title("Willow the Bunny Lovey — Crochet Pattern (NS 10)")
    pdf.set_author("Novality Store — Novality Crochet Studio")
    pdf.set_subject("Validated crochet pattern: bunny comforter lovey, US terms")
    pdf.set_creator("Crochet Pattern Checker — validated edition")
    return pdf


def h1(text, first=False):
    """Section banner."""
    p = pdf.P
    h = 11
    y = pdf.get_y() + (0 if first else 5)
    pdf.set_fill_color(*p.sage_dark)
    pdf.rect(M, y, CW, h, style="F")
    pdf.set_xy(M + 4, y)
    pdf.set_font("Story", "B", 12.5)
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
    p = pdf.P
    pdf.set_font("DejaVu", "", size)
    pdf.set_text_color(*(color or p.ink))
    pdf.multi_cell(CW, lh, text, align="L")
    pdf.ln(after)
    pdf.set_text_color(*p.ink)


def bullet(text, bold_lead=None, size=9, lh=4.6):
    p = pdf.P
    pdf.set_font("DejaVu", "", size)
    x0 = pdf.get_x()
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


def table(headers, rows, widths, aligns=None, size=8.6, lh=6.0, bold_cols=()):
    p = pdf.P
    aligns = aligns or ["L"] * len(headers)
    # header
    pdf.set_font("DejaVu", "B", size)
    pdf.set_fill_color(*p.sage_dark)
    pdf.set_text_color(*p.white)
    pdf.set_draw_color(*p.line)
    pdf.set_line_width(0.2)
    x0 = M
    y = pdf.get_y()
    for i, (hd, w) in enumerate(zip(headers, widths)):
        pdf.set_xy(x0, y)
        pdf.cell(w, lh, " " + hd, border=1, align="L", fill=True)
        x0 += w
    pdf.set_y(y + lh)
    # rows
    pdf.set_text_color(*p.ink)
    for r, row in enumerate(rows):
        h = lh
        # measure needed height for wrapping cells
        for cell, w, a in zip(row, widths, aligns):
            pdf.set_font("DejaVu", "B" if r in () else "", size)
            n = pdf.multi_cell(w - 2, 4.4, cell, dry_run=True, output="LINES")
            h = max(h, 4.4 * len(n) + 1.8)
        fill = p.sage_light if r % 2 == 0 else p.white
        x0 = M
        for i, (cell, w, a) in enumerate(zip(row, widths, aligns)):
            pdf.set_xy(x0, pdf.get_y())
            pdf.set_font("DejaVu", "B" if i in bold_cols else "", size)
            pdf.set_fill_color(*fill)
            pdf.cell(w, h, " " + cell if a == "L" else cell + " ",
                     border=1, align=a, fill=True)
            x0 += w
        pdf.set_y(pdf.get_y() + h)
    pdf.ln(2.5)
    pdf.set_font("DejaVu", "", 9)


def box(title, lines, fill_key="pink_light", border_key="pink", size=8.8):
    """Rounded call-out box; lines = list of (text, bold?) or plain str."""
    p = pdf.P
    pdf.set_font("DejaVu", "", size)
    # measure
    w_eff = CW - 10
    h = 7
    for ln in lines:
        t = ln if isinstance(ln, str) else ln[0]
        n = pdf.multi_cell(w_eff, 4.3, t, dry_run=True, output="LINES")
        h += 4.3 * len(n) + 1.2
    y = pdf.get_y() + 1
    pdf.set_fill_color(*getattr(p, fill_key))
    pdf.set_draw_color(*getattr(p, border_key))
    pdf.set_line_width(0.35)
    pdf.rect(M, y, CW, h, style="DF", round_corners=True, corner_radius=2.5)
    pdf.set_xy(M + 5, y + 2.4)
    if title:
        pdf.set_font("DejaVu", "B", 9.6)
        pdf.set_text_color(*getattr(p, border_key))
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


def badge(label, w, fill, text_color):
    p = pdf.P
    y = pdf.get_y()
    pdf.set_fill_color(*fill)
    pdf.rect(M, y, w, 7.6, style="F", round_corners=True, corner_radius=3.8)
    pdf.set_xy(M, y)
    pdf.set_font("DejaVu", "B", 8)
    pdf.set_text_color(*text_color)
    pdf.cell(w, 7.6, label, align="C")
    pdf.set_y(y + 7.6)
    pdf.set_text_color(*p.ink)


# ---------------------------------------------------------------- cover
def cover():
    p = pdf.P
    pdf.add_page()
    pdf.set_auto_page_break(auto=False)  # cover is fully hand-positioned

    # cover image: crop square -> 210 x 131 mm band
    img = Image.open(COVER_SRC).convert("RGB")
    tgt_h = int(1024 * 131 / 210)
    top = int((1024 - tgt_h) * 0.42)  # keep the bunny slightly above centre
    img.crop((0, top, 1024, top + tgt_h)).save("/tmp/willow_cover_crop.png")
    pdf.image("/tmp/willow_cover_crop.png", x=0, y=0, w=PAGE_W, h=131)

    # sage band under the image
    pdf.set_fill_color(*p.sage_dark)
    pdf.rect(0, 131, PAGE_W, 2.2, style="F")

    pdf.set_y(140)
    pdf.set_font("Story", "B", 30)
    pdf.set_text_color(*p.ink)
    pdf.cell(0, 14, "Willow the Bunny Lovey", align="C")
    pdf.ln(15)
    pdf.set_font("DejaVu", "", 11)
    pdf.set_text_color(*p.sage_dark)
    pdf.cell(0, 6, "A crocheted comforter pattern  •  Design Code NS 10", align="C")
    pdf.ln(13)

    # badges
    labels = ["No small parts", "Advanced beginner", "2–3 hours",
              "Stitch counts verified"]
    pdf.set_font("DejaVu", "B", 8.6)
    ws = [pdf.get_string_width(s) + 9 for s in labels]
    total = sum(ws) + 4 * (len(ws) - 1)
    x = (PAGE_W - total) / 2
    y = pdf.get_y()
    fills = [p.pink_light, p.sage_light, p.sage_light, p.sage_light]
    tcols = [p.pink, p.sage_dark, p.sage_dark, p.sage_dark]
    for s, w, f, t in zip(labels, ws, fills, tcols):
        pdf.set_fill_color(*f)
        pdf.rect(x, y, w, 8.4, style="F", round_corners=True, corner_radius=4.2)
        pdf.set_xy(x, y)
        pdf.set_font("DejaVu", "B", 8.6)
        pdf.set_text_color(*t)
        pdf.cell(w, 8.4, s, align="C")
        x += w + 4
    pdf.set_y(y + 14)

    pdf.set_font("DejaVu", "", 9.6)
    pdf.set_text_color(*p.grey)
    pdf.multi_cell(CW, 5.2,
                   "Finished size: blanket approx. 26 cm (10 in) square after 20 rounds  •  "
                   "head approx. 4.9 cm across  •  approx. 25 cm from ear tips to corner\n"
                   "DK cotton on a 3.5 mm hook  •  embroidered face, no safety eyes  •  "
                   "make 1 head + 2 ears + 1 granny square", align="C")
    pdf.ln(3)

    # bottom band
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


# ---------------------------------------------------------------- pages
def page_safety_materials():
    p = pdf.P
    pdf.add_page()

    box("SAFETY — A BABY ITEM, READ THIS", [
        ("No safety eyes, buttons, beads or removable parts. The face is fully "
         "embroidered and every floss end is knotted inside the head.", True),
        "Willow is not a tested toy (ASTM F963 / EN 71). Never list or describe her as “baby-safe”.",
        "Comforters are not recommended in the cot for babies under 12 months — use with "
        "supervision, and say so in your listing.",
        ("Sew every seam twice. Weave every end in at least 5 cm (2 in).", True),
    ])

    h2("Materials")
    bullet("DK (#3) 100% cotton (or a baby-safe certified blend), approx. 60 g / 140–150 m — "
           "cream, sage, dusty pink or pale grey, plus a scrap of contrast cotton for embroidery. "
           "Only the head is stuffed.", bold_lead="Yarn")
    bullet("3.5 mm (US E/4) for the blanket; 3.0 mm for the head if your tension is loose.",
           bold_lead="Hook")
    bullet("dark brown or charcoal cotton floss. No safety eyes.", bold_lead="Face")
    bullet("approx. 8 g fibre fill, tapestry needle, stitch marker.", bold_lead="Also")

    h2("The three pieces")
    table(
        ["Piece", "Qty", "Hook", "Rounds", "Finished size"],
        [
            ["Head (stuffed)", "1", "3.0–3.5 mm", "1–15", "≈ 4.9 cm across, 5.7 cm tall"],
            ["Ears (unstuffed)", "2", "3.0–3.5 mm", "1–11", "long + floppy, sewn flat"],
            ["Granny-square blanket", "1", "3.5 mm", "1–20 + border", "≈ 26 cm square"],
        ],
        widths=[44, 12, 26, 30, 66],
        aligns=["L", "C", "C", "C", "L"],
        bold_cols=(0,),
    )

    h2("Gauge")
    box(None, [
        ("1 dc ≈ 4.3 mm wide and 1 round ≈ 3.8 mm deep. After blanket Rnd 3, 9 dc along an "
         "edge should measure ≈ 39 mm (1.5 in).", True),
        "Narrower? Go up a hook size — or keep the hook and add rounds (22 rounds ≈ 28 cm).",
    ], fill_key="sage_light", border_key="sage_mid")

    h2("Abbreviations — US terms (UK in parentheses)")
    para("MR = magic ring  •  ch = chain  •  sl st = slip stitch  •  sc = single crochet "
         "(UK dc)  •  dc = double crochet (UK tr)  •  inc = increase — work 2 sc in the same "
         "stitch  •  dec = decrease — sc2tog over 2 sts  •  Rnd = round  •  ( ) = stitch count "
         "at the end of the round.\n"
         "On the head and ears, chains are never counted as stitches. On the blanket, the "
         "beginning ch-3 of each round counts as one dc.", size=8.8)


def page_construction():
    pdf.add_page()
    h1("Before you begin")

    h2("Construction at a glance")
    bullet("The head and ears are worked in a continuous spiral — no joins, stitch marker "
           "in the first stitch of every round, never turn.", bold_lead="Spiral pieces.")
    bullet("The blanket is worked in joined rounds — each round closes with a slip stitch "
           "and the next begins with a ch-3 that counts as your first dc. Never turn.",
           bold_lead="Blanket.")
    bullet("Work every stitch through both loops unless noted.", bold_lead="Loops.")

    h2("Three techniques that make this pattern")
    bullet("the head and each ear begin with a magic ring; pull the tail tight after "
           "round one.", bold_lead="1. Magic ring & spiral —")
    bullet("every blanket corner is (3 dc, ch 2, 3 dc) into one corner space. Those four "
           "corners make the piece square instead of round. Miss one corner group and the "
           "whole square pulls out of true — check all four at the end of every round.",
           bold_lead="2. The granny-square corner —")
    bullet("a final round of single crochet around the edge, with 3 sc into each corner "
           "space, squares the edge and stops the blanket curling. Do not skip it.",
           bold_lead="3. The border round —")

    h2("Sizing the blanket")
    table(
        ["Rounds", "Approx. size (square)", "Use"],
        [
            ["18 rounds", "≈ 23 cm (9 in)", "small comforter / preemie gift"],
            ["20 rounds", "≈ 26 cm (10 in)", "the classic Willow (this pattern)"],
            ["22 rounds", "≈ 28 cm (11 in)", "bigger lovey, same recipe"],
        ],
        widths=[30, 60, 88],
        aligns=["C", "L", "L"],
        bold_cols=(0,),
    )
    para("The square grows ≈ 1.3 cm per side per round — add rounds two at a time to grow "
         "Willow gracefully.", size=8.8, color=pdf.P.grey)


def page_head_ears():
    pdf.add_page()
    h1("1 · Head — make 1")
    para("Continuous spiral, no joins. Marker in the first stitch of every round.", size=8.6,
         color=pdf.P.grey, after=1.5)
    table(
        ["Rnd", "Instruction", "Sts", "Notes"],
        [
            ["1", "6 sc in MR", "6", "pull ring tight"],
            ["2", "inc in each st around", "12", ""],
            ["3", "[sc, inc] × 6", "18", ""],
            ["4", "[2 sc, inc] × 6", "24", "ears attach at Rnds 4–6"],
            ["5", "[3 sc, inc] × 6", "30", ""],
            ["6", "[4 sc, inc] × 6", "36", "full width"],
            ["7", "sc in each st around", "36", ""],
            ["8", "sc in each st around", "36", "face on Rnds 8–9"],
            ["9", "sc in each st around", "36", ""],
            ["10", "sc in each st around", "36", ""],
            ["11", "[4 sc, dec] × 6", "30", "begin stuffing firmly"],
            ["12", "[3 sc, dec] × 6", "24", ""],
            ["13", "[2 sc, dec] × 6", "18", "top up stuffing"],
            ["14", "[sc, dec] × 6", "12", ""],
            ["15", "dec × 6", "6", "fasten off, close the hole"],
        ],
        widths=[13, 62, 15, 88],
        aligns=["C", "L", "C", "L"],
    )
    box(None, [
        ("The decrease ladder must step 36 → 30 → 24 → 18 → 12 → 6 — one round each for "
         "[4 sc, dec], [3 sc, dec], [2 sc, dec], [sc, dec], then dec. That is why the head "
         "has 15 rounds.", False),
        ("Stuff FIRMLY — a soft head collapses when gripped and the face distorts. "
         "Finished head ≈ 4.9 cm across and 5.7 cm tall. Fasten off and close with the tail.",
         True),
    ])

    pdf.add_page()
    h1("2 · Ears — make 2 (do not stuff)")
    table(
        ["Rnd", "Instruction", "Sts", "Notes"],
        [
            ["1", "6 sc in MR", "6", ""],
            ["2", "[sc, inc] × 3", "9", ""],
            ["3", "[2 sc, inc] × 3", "12", "widest point"],
            ["4–8", "sc in each st around (5 rnds)", "12", "the long, floppy part"],
            ["9", "[2 sc, dec] × 3", "9", ""],
            ["10", "sc in each st around", "9", "taper to the base"],
            ["11", "[sc, dec] × 3", "6", "flatten, fasten off long tail"],
        ],
        widths=[13, 62, 15, 88],
        aligns=["C", "L", "C", "L"],
    )
    para("Pinch each ear base flat and fasten off with a long tail. Sew the ears to "
         "Rnds 4–6 of the head, about 10 stitches apart, pinching each base so the ear "
         "flops forward. A drop of invisible stitching across the base keeps the flop "
         "in place after washing.", size=9)


def page_blanket():
    pdf.add_page()
    h1("3 · Granny-square blanket")
    para("3.5 mm hook, joined rounds (close every round with a slip stitch; the starting "
         "ch-3 counts as a dc; never turn).", size=8.6, color=pdf.P.grey, after=2.5)

    pdf.set_font("DejaVu", "", 9)
    steps = [
        ("Foundation.", "Ch 4 and sl st to the first ch to form a ring."),
        ("Rnd 1.", "Ch 3 (counts as first dc), 2 dc in the ring, [ch 2, 3 dc in the ring] × 3, "
                   "ch 2, sl st to the top of the ch-3.   [12 dc, 4 corner spaces]"),
        ("Rnd 2.", "Sl st into the next corner space; ch 3, 2 dc in that space, ch 2, 3 dc in "
                   "the same space (first corner); then (3 dc, ch 2, 3 dc) into each remaining "
                   "corner space; sl st to close.   [24 dc]"),
        ("Rnd 3 (setup).", "Sl st into the next corner space; ch 3, (2 dc, ch 2, 3 dc) in the "
                           "same space; *3 dc in the next side space, (3 dc, ch 2, 3 dc) in the "
                           "next corner space*; repeat from * around; sl st to close.   [36 dc]"),
        ("Rnds 4–20.", "As Rnd 3 — 3 dc into every side space and (3 dc, ch 2, 3 dc) into every "
                       "corner space. Each round adds one 3-dc group to every side (+12 dc per "
                       "round): Rnd 4 has 2 side spaces per side … Rnd 20 has 18."),
    ]
    for lead, text in steps:
        bullet(text, bold_lead=lead, size=9)

    box("COUNT CHECK — before you close any round", [
        "Four crisp (3 dc, ch 2, 3 dc) corners — every time. Then total double crochets:",
        ("Rnd 3 = 36   |   Rnd 5 = 60   |   Rnd 10 = 120   |   Rnd 15 = 180   |   "
         "Rnd 20 = 240   (60 dc per edge ≈ 26 cm)", True),
    ], fill_key="sage_light", border_key="sage_mid")

    h2("Border — do not skip")
    para("Work one final round of sc all the way around: 1 sc into each dc and 3 sc into "
         "each corner space, then sl st and fasten off. At Rnd 20 that is "
         "240 sc + 12 corner sc = 252 sc. This firms the edge and stops the square curling. "
         "Open dc clusters and crisp (3 dc, ch 2, 3 dc) corners keep the square true round "
         "after round.", size=9)

    h2("Stitch-count journey")
    table(
        ["Rnd", "3", "5", "10", "15", "20", "Border"],
        [["total sts", "36", "60", "120", "180", "240", "252 sc"]],
        widths=[30, 22, 22, 22, 22, 22, 38],
        aligns=["L", "C", "C", "C", "C", "C", "C"],
        bold_cols=(0,),
    )


def page_assembly():
    pdf.add_page()
    h1("4 · Face & assembly")

    h2("The face — embroidery only")
    bullet("two small ovals, about 8 stitches apart, across Rnds 8–9 of the head.",
           bold_lead="Eyes:")
    bullet("a small inverted triangle centred between and just below the eyes.",
           bold_lead="Nose:")
    bullet("a shallow Y from the base of the nose.", bold_lead="Mouth:")
    bullet("knot every floss end inside the head and bury the tails before closing. "
           "Skip blush — chalk rubs off on bedding and is not washable.",
           bold_lead="Ends:")

    h2("Joining the head to the blanket")
    para("Centre the head over one corner of the square, overlapping the blanket by about "
         "3 cm. Sew all the way around the base of the head — then sew it a second time. "
         "This is the only structural seam and it will be pulled, chewed and washed. "
         "Weave every end in at least 5 cm (2 in).", size=9)
    box(None, [
        ("Why two passes? Amigurumi-to-flat seams carry the whole weight of the head. "
         "Two passes with the long tail, worked through both the head base and the blanket "
         "corner rounds, survive chewing and machine washing.", False),
    ])

    h2("For your Etsy listing")
    bullet("100% cotton, embroidered face, no safety eyes, no buttons, beads or removable "
           "parts.", bold_lead="Materials:")
    bullet("machine wash cool on a gentle cycle inside a mesh bag; reshape while damp and "
           "dry flat. Do not tumble dry — cotton can shrink and the stuffing may clump.",
           bold_lead="Care:")
    bullet("comforters are not recommended in the cot for babies under 12 months; use with "
           "supervision. Copy this into your listing.", bold_lead="Supervision:")
    bullet("cream, sage, dusty pink, pale grey and butter yellow — neutrals outsell brights "
           "in the baby category.", bold_lead="Colorways:")


def page_help_terms():
    pdf.add_page()
    h1("Troubleshooting")
    bullet("you skipped the sc border, or missed a (3 dc, ch 2, 3 dc) corner. Check all "
           "four corners at the end of every round, and do not skip the border round.",
           bold_lead="Blanket curls / not square?")
    bullet("your gauge is tighter than 4.3 mm per dc — go up a hook size or add rounds "
           "(22 rounds ≈ 28 cm). Stuff the head firmly and sew the base seam twice.",
           bold_lead="Came out too small / head flops?")

    h1("Why this pattern works — validation summary")
    para("Every stitch count in this pattern was checked with deterministic math "
         "(Crochet Pattern Checker): round-by-round production vs. consumption, stated "
         "counts, size claims against the stated gauge, and the granny-square growth "
         "model.", size=8.8)
    table(
        ["Check", "Result"],
        [
            ["Head Rnds 1–15: count chain 6 → 36 → 6", "✓ verified"],
            ["Ear Rnds 1–11: count chain 6 → 12 → 6", "✓ verified"],
            ["Granny square: +12 dc per round, 12 → 240 over 20 rnds", "✓ verified"],
            ["Border: 240 dc + 4 × 3 corner sc = 252 sc", "✓ verified"],
            ["Sizes vs. gauge: 18/20/22 rounds ≈ 23/26/28 cm", "✓ verified"],
            ["Gauge probe: 9 dc ≈ 39 mm after Rnd 3", "✓ verified"],
            ["Head size: 36 sts ≈ 4.9 cm across; 15 rnds ≈ 5.7 cm tall", "✓ verified"],
        ],
        widths=[138, 40],
        aligns=["L", "C"],
    )

    h1("5 · Terms of use")
    h2("Copyright & ownership")
    para("This crochet pattern — including all instructions, stitch counts, photography and "
         "design elements — is the original work and intellectual property of Novality "
         "Store, designed by Novality Crochet Studio. Design Code NS 10. "
         "© 2026 Novality Store. All rights reserved.", size=8.5, after=1)
    h2("You may")
    para("Make as many finished loveys as you like for yourself, gifts, or charity. Sell "
         "physical finished items made from this pattern in small batches, in shops, markets "
         "and online, provided credit is given to “Novality Store”.", size=8.8)
    h2("You may not")
    para("Resell, share, redistribute, translate, rewrite, publish or upload this digital PDF "
         "or its contents in any form. Do not alter, copy or recolor the pattern and claim it "
         "as your own. Do not use the Novality Store name, logo or photos beyond crediting "
         "the pattern. Do not mass-produce finished items commercially without written "
         "permission.", size=8.5)
    box("SAFETY REMINDER", [
        "Willow has NO safety eyes, buttons, beads or removable parts — the face is "
        "embroidered and floss ends are knotted inside the head. Even so she is not a "
        "tested toy (ASTM F963 / EN 71): do not claim “baby-safe”. Comforters are not "
        "recommended in a cot for babies under 12 months and should be used with "
        "supervision; sew every seam twice and weave ends in at least 5 cm.",
    ])
    para("Happy crocheting! Tag your makes with  #NovalityStore  and  #WillowTheBunnyLovey  "
         "— thank you for supporting an independent pattern designer.", size=8.8)


def build(edition: str):
    P = Palette if edition == "retail" else Grey
    pdf = setup(P)
    cover()
    page_safety_materials()
    page_construction()
    page_head_ears()
    page_blanket()
    page_assembly()
    page_help_terms()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    suffix = "" if edition == "retail" else "_print"
    out = OUT_DIR / f"Willow_the_Bunny_Lovey_Crochet_Pattern_NS10{suffix}.pdf"
    pdf.output(out)
    print(f"[{edition}] wrote {out} ({pdf.page_no()} pages, "
          f"{out.stat().st_size/1024:.0f} KB)")
    return out


if __name__ == "__main__":
    build("retail")

    # print edition: swap in the greyscale cover, then restore
    grey = ROOT / "assets" / "willow_cover_grey.png"
    img = Image.open(COVER_SRC).convert("L").convert("RGB")
    grey.parent.mkdir(parents=True, exist_ok=True)
    img.save(grey)
    COVER_SRC = grey
    build("print")
