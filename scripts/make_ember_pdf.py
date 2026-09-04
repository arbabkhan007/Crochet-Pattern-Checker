#!/usr/bin/env python3
"""Generate a sellable, professional PDF for Ember the Baby Dragon (NS08).

Uses ReportLab (pure Python, no system libs) and svglib for the SVG diagrams.
Run:  python scripts/make_ember_pdf.py
"""
from __future__ import annotations

from pathlib import Path
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Image,
    Table, TableStyle, PageBreak, KeepTogether, Flowable,
)
from svglib.svglib import svg2rlg

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "ember"
DIAGRAMS = OUT
PIECES = Path("/home/user/ember_pieces")

# ----------------------------------------------------------------------------
# Theme
# ----------------------------------------------------------------------------
SAGE = colors.HexColor("#7E9B82")
SAGE_DARK = colors.HexColor("#4C6150")
CREAM = colors.HexColor("#F6F0E2")
CREAM_DARK = colors.HexColor("#E9DCC0")
GOLD = colors.HexColor("#C9A45C")
GOLD_DARK = colors.HexColor("#9A7533")
INK = colors.HexColor("#2F3A30")
GREY = colors.HexColor("#6F7770")
PALE = colors.HexColor("#FAF7F0")
RULE = colors.HexColor("#D8CDB6")

PAGE_W, PAGE_H = A4

# ----------------------------------------------------------------------------
# Styles
# ----------------------------------------------------------------------------
ss = getSampleStyleSheet()
styles = {}


def st(name, **kw):
    base = kw.pop("parent", "Normal")
    if base in styles:
        s = ParagraphStyle(name, parent=styles[base], **kw)
    else:
        s = ParagraphStyle(name, parent=ss[base], **kw)
    styles[name] = s
    return s


st("Body", fontName="Helvetica", fontSize=9.4, leading=13.2, textColor=INK, alignment=TA_JUSTIFY, spaceAfter=5)
st("BodyCenter", parent="Body", alignment=TA_CENTER)
st("Title", fontName="Helvetica-Bold", fontSize=30, leading=34, textColor=SAGE_DARK, alignment=TA_CENTER)
st("Subtitle", fontName="Helvetica", fontSize=13, leading=17, textColor=GOLD_DARK, alignment=TA_CENTER)
st("SectionHead", fontName="Helvetica-Bold", fontSize=17, leading=21, textColor=SAGE_DARK, spaceBefore=6, spaceAfter=4)
st("SectionSub", fontName="Helvetica-Oblique", fontSize=9.5, leading=13, textColor=GREY, spaceAfter=6)
st("H3", fontName="Helvetica-Bold", fontSize=12.5, leading=16, textColor=SAGE_DARK, spaceBefore=10, spaceAfter=4)
st("KPI", fontName="Helvetica-Bold", fontSize=14, leading=17, textColor=SAGE_DARK, alignment=TA_CENTER)
st("KPILabel", fontName="Helvetica", fontSize=8.5, leading=11, textColor=GREY, alignment=TA_CENTER)
st("Tiny", fontName="Helvetica", fontSize=8, leading=11, textColor=GREY, alignment=TA_LEFT)
st("Note", fontName="Helvetica-Oblique", fontSize=9, leading=13, textColor=SAGE_DARK, alignment=TA_JUSTIFY, spaceAfter=5)
st("NoteBox", fontName="Helvetica", fontSize=9.2, leading=13, textColor=INK, alignment=TA_LEFT, spaceAfter=0)


def cell_style(text="", font="Helvetica", size=9.2, color=INK, align=TA_LEFT, leading=12):
    return ParagraphStyle(
        "cell",
        fontName=font,
        fontSize=size,
        leading=leading,
        textColor=color,
        alignment=align,
        spaceAfter=0,
        spaceBefore=0,
    )


# ----------------------------------------------------------------------------
# Page furniture
# ----------------------------------------------------------------------------
class NumberedCanvas:
    """Not used; kept simple with footer functions."""


def on_cover(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(CREAM)
    canvas.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    canvas.setFillColor(GOLD)
    canvas.rect(0, 0, PAGE_W, 8 * mm, stroke=0, fill=1)
    canvas.setStrokeColor(GOLD_DARK)
    canvas.setLineWidth(1.4)
    canvas.line(20 * mm, 8 * mm, PAGE_W - 20 * mm, 8 * mm)
    canvas.setFillColor(GREY)
    canvas.setFont("Helvetica", 8)
    canvas.drawCentredString(PAGE_W / 2, 14 * mm, "NOVALITY STORE · DESIGN CODE NS 08 · © 2026")
    canvas.restoreState()


def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(colors.white)
    canvas.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    # top stripe
    canvas.setFillColor(SAGE)
    canvas.rect(0, PAGE_H - 5 * mm, PAGE_W, 5 * mm, stroke=0, fill=1)
    canvas.setFillColor(GOLD)
    canvas.rect(0, PAGE_H - 5.8 * mm, PAGE_W, 0.8 * mm, stroke=0, fill=1)
    # footer
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.6)
    canvas.line(20 * mm, 16 * mm, PAGE_W - 20 * mm, 16 * mm)
    canvas.setFillColor(GREY)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(20 * mm, 11 * mm, "Ember the Baby Dragon  ·  Novality Store  ·  NS08")
    canvas.drawRightString(PAGE_W - 20 * mm, 11 * mm, f"Page {doc.page}")
    canvas.restoreState()


def build_doc(path: Path):
    doc = BaseDocTemplate(
        str(path),
        pagesize=A4,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
        topMargin=18 * mm,
        bottomMargin=20 * mm,
        title="Ember the Baby Dragon - Crochet Pattern (NS08)",
        author="Novality Store / Novality Crochet Studio",
        subject="Crochet amigurumi pattern - US terms",
    )
    cover_frame = Frame(14 * mm, 12 * mm, PAGE_W - 28 * mm, PAGE_H - 26 * mm, id="cover")
    body_frame = Frame(20 * mm, 21 * mm, PAGE_W - 40 * mm, PAGE_H - 42 * mm, id="body")
    doc.addPageTemplates(
        [
            PageTemplate(id="cover", frames=[cover_frame], onPage=on_cover),
            PageTemplate(id="body", frames=[body_frame], onPage=on_page),
        ]
    )
    return doc


def kpi_row(items):
    """items: list of (value, label)."""
    cells = []
    for val, lab in items:
        inner = Table(
            [
                [Paragraph(val, styles["KPI"])],
                [Paragraph(lab, styles["KPILabel"])],
            ],
            colWidths=[54 * mm],
        )
        inner.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), PALE),
            ("BOX", (0, 0), (-1, -1), 0.8, RULE),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 5),
            ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ]))
        cells.append(inner)
    return Table([cells], colWidths=[54 * mm] * len(items))


def note_box(text, title=None):
    rows = []
    if title:
        rows.append([Paragraph(f"<b>{title}</b>", cell_style(f"<b>{title}</b>", font="Helvetica-Bold", color=SAGE_DARK, size=10))])
    rows.append([Paragraph(text, styles["NoteBox"])])
    t = Table(rows, colWidths=[PAGE_W - 40 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CREAM),
        ("BOX", (0, 0), (-1, -1), 0.8, GOLD),
        ("LINEBEFORE", (0, 0), (0, -1), 3, GOLD),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return t


def instructions_table(rows, cols=None):
    """rows: list of (rnd, instruction, count, note)."""
    headers = cols or ["Rnd", "Instruction", "Sts", "Note"]
    data = [[Paragraph(h, cell_style(h, font="Helvetica-Bold", color=colors.white, size=8.8)) for h in headers]]
    for cells in rows:
        data.append([
            Paragraph(str(cells[0]), cell_style(size=8.8)),
            Paragraph(cells[1], cell_style(size=8.8)),
            Paragraph(f"({cells[2]})", cell_style(size=8.8, align=TA_CENTER)),
            Paragraph(cells[3] if len(cells) > 3 else "", cell_style(size=8.4, color=GREY)),
        ])
    w = cols_widths = [16 * mm, (PAGE_W - 40 * mm) - 16 * mm - 16 * mm - 30 * mm, 16 * mm, 30 * mm]
    t = Table(data, colWidths=w, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), SAGE),
        ("BACKGROUND", (0, 1), (-1, -1), colors.white),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PALE]),
        ("GRID", (0, 0), (-1, -1), 0.5, RULE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return t


def numbered_steps(items):
    rows = [[Paragraph(f"<b>{i}.</b>", cell_style(font="Helvetica-Bold", color=GOLD_DARK, align=TA_CENTER, size=10)),
             Paragraph(txt, cell_style(size=9.2))] for i, txt in enumerate(items, 1)]
    t = Table(rows, colWidths=[10 * mm, (PAGE_W - 40 * mm) - 10 * mm])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t


def svg_flowable(path: Path, width_mm, height_mm=None):
    d = svg2rlg(str(path))
    scale = (width_mm * mm) / d.width
    if height_mm:
        scale = min(scale, (height_mm * mm) / d.height)
    d.width = d.width * scale
    d.height = d.height * scale
    d.scale(scale, scale)
    return d


def bullet_list(items):
    rows = [[Paragraph("•", cell_style(color=GOLD_DARK, align=TA_CENTER, size=10)),
             Paragraph(txt, cell_style(size=9.2))] for txt in items]
    t = Table(rows, colWidths=[8 * mm, (PAGE_W - 40 * mm) - 8 * mm])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 2),
        ("RIGHTPADDING", (0, 0), (-1, -1), 2),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t


# ----------------------------------------------------------------------------
# Pattern data (corrected / made consistent for publication)
# ----------------------------------------------------------------------------
HEAD = [
    (1, "6 sc in MR", 6, "start"),
    (2, "inc in each st around", 12, ""),
    (3, "[sc, inc] x 6", 18, ""),
    (4, "[2 sc, inc] x 6", 24, ""),
    (5, "[3 sc, inc] x 6", 30, ""),
    (6, "[4 sc, inc] x 6", 36, "head at full width"),
    (7, "sc in each st around", 36, "eyes at R7–R8"),
    (8, "sc in each st around", 36, ""),
    (9, "[4 sc, dec] x 6", 30, ""),
    (10, "[3 sc, dec] x 6", 24, "stuff firmly"),
    (11, "[2 sc, dec] x 6", 18, "LEAVE OPEN"),
]

SNOUT = [
    (1, "6 sc in MR", 6, ""),
    (2, "[sc, inc] x 3", 9, ""),
    (3, "[2 sc, inc] x 3", 12, ""),
    (4, "sc in each st around", 12, ""),
    (5, "sc in each st around", 12, ""),
]

BODY = [
    (1, "6 sc in MR", 6, ""),
    (2, "inc in each st around", 12, ""),
    (3, "[sc, inc] x 6", 18, ""),
    (4, "[2 sc, inc] x 6", 24, "tail attaches R4–R6"),
    (5, "[3 sc, inc] x 6", 30, "full width – check gauge"),
    (6, "sc in each st around", 30, "back legs at R6"),
    (7, "sc in each st around", 30, ""),
    (8, "sc in each st around", 30, "front legs at R8"),
    (9, "sc in each st around", 30, ""),
    (10, "[3 sc, dec] x 6", 24, "wings at R10–R11"),
    (11, "sc in each st around", 24, ""),
    (12, "[2 sc, dec] x 6", 18, "stuff firmly"),
    (13, "sc in each st around", 18, "LEAVE THE NECK OPEN"),
]

LEGS = [
    (1, "6 sc in MR", 6, "all four"),
    (2, "[sc, inc] x 3", 9, "all four"),
    (3, "sc in each st around", 9, "all four"),
    (4, "sc in each st around", 9, "all four"),
    (5, "sc in each st around", 9, "all four"),
    (6, "sc in each st around", 9, "BACK legs finish here"),
    (7, "sc in each st around", 9, "front legs only"),
    (8, "sc in each st around", 9, "front legs only"),
]

HORNS = [
    (1, "4 sc in MR", 4, ""),
    (2, "sc in each st around", 4, ""),
    (3, "[sc, inc] x 2", 6, ""),
    (4, "sc in each st around", 6, ""),
    (5, "sc in each st around", 6, ""),
]

TAIL = [
    (1, "4 sc in MR", 4, "tip"),
    (2, "sc in each st around", 4, ""),
    (3, "[sc, inc] x 2", 6, ""),
    (4, "sc in each st around", 6, ""),
    (5, "sc in each st around", 6, ""),
    (6, "[2 sc, inc] x 2", 8, ""),
    (7, "sc in each st around", 8, ""),
    (8, "sc in each st around", 8, ""),
    (9, "[3 sc, inc] x 2", 10, ""),
    (10, "sc in each st around", 10, ""),
    (11, "sc in each st around", 10, ""),
    (12, "sc in each st around", 10, "base"),
]

WINGS_ROWS = [
    ("Row 1", "from the 2nd ch: sc in 4, hdc in 3, dc in 3", 10),
    ("Row 2", "sc in 3, hdc in 3, dc in 4", 10),
    ("Row 3", "sc in 2, hdc in 4, dc in 4", 10),
    ("Row 4", "sl st in first 2, (sc, hdc, dc, hdc, sc) in next st, sl st in next 2, (sc, hdc, dc, hdc, sc) in next st, sl st in last 4", 10),
]


def build():
    story = []
    OUT.mkdir(parents=True, exist_ok=True)

    # ---------------- COVER ----------------
    cover_h = 88 * mm
    cover_w = cover_h * 2 / 3  # source is 2:3 portrait
    cover = Image(str(OUT / "cover_art.png"), width=cover_w, height=cover_h)
    story.append(Spacer(1, 2 * mm))
    story.append(cover)
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph("EMBER THE BABY DRAGON", styles["Title"]))
    story.append(Spacer(1, 2 * mm))
    story.append(Paragraph("A chunky, big-headed baby dragon with a stubby snout,<br/>scalloped wings and a ridge of spikes down her back.", styles["Subtitle"]))
    story.append(Spacer(1, 5 * mm))
    story.append(kpi_row([
        ("US Terms", "Intermediate"),
        ("4–5 hours", "Finished size ≈ 11 cm"),
        ("3.5 mm / E-4", "Worsted #4 yarn"),
    ]))
    story.append(Spacer(1, 5 * mm))
    story.append(Paragraph("Designed by <b>Novality Crochet Studio</b> · Novality Store", styles["Tiny"]))
    story.append(Spacer(1, 1 * mm))
    story.append(Paragraph("Design code <b>NS 08</b> · © 2026 Novality Store · All rights reserved", styles["Tiny"]))
    story.append(PageBreak())

    # ---------------- OVERVIEW ----------------
    story.append(Paragraph("Ember the Baby Dragon", styles["SectionHead"]))
    story.append(Paragraph("Crochet amigurumi pattern · US terminology · worked in continuous spiral with two flat sections", styles["SectionSub"]))
    story.append(note_box(
        "A chunky, big-headed baby dragon with a stubby snout, scalloped wings and a ridge of spikes down the back. "
        "She sits, with folding haunches and splayed front legs. The head is left open at 18 stitches and ladder-stitched "
        "onto a matching 18-stitch neck — this is the most important structural detail and what keeps the big head from flopping.",
        "A note on the design",
    ))
    story.append(Spacer(1, 5 * mm))
    story.append(Paragraph("Finished size", styles["H3"]))
    story.append(bullet_list([
        "<b>Height (seated):</b> about 11 cm (4.3 in) tall.",
        "<b>Wingspan:</b> about 12.5 cm (5 in).",
        "<b>Tail:</b> about 5 cm (2 in) long.",
        "A sitting dragon — her body rests on the table and her legs pose rather than lift her.",
    ]))
    story.append(PageBreak())

    # ---------------- MATERIALS ----------------
    story.append(Paragraph("Materials", styles["SectionHead"]))
    story.append(bullet_list([
        "<b>Main yarn:</b> Worsted #4, about 30 g used (buy a 50 g ball) — sage green, dusty teal, lilac or charcoal. The extra allows for tails, sewing and a second attempt.",
        "<b>Belly &amp; wings:</b> Worsted #4, about 20 g in a contrast cream or pale gold.",
        "<b>Spikes:</b> Worsted #4, about 10 g in the contrast colour (horns, spikes and wings match).",
        "<b>Hook:</b> 3.5 mm (US E/4).",
        "<b>Eyes:</b> 2 x 10 mm safety eyes — slit-pupil dragon eyes if you can get them.",
        "<b>Also needed:</b> polyester fibre fill about 10 g, tapestry needle, stitch markers, pins.",
    ]))
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph("Gauge", styles["H3"]))
    story.append(note_box(
        "About <b>4.5 mm per stitch</b> and <b>4.3 mm per round</b>. Check on the body after Rnd 5 — 30 stitches should measure "
        "about <b>43 mm across</b> when stuffed. If your stitches are wider, crochet more tightly or drop to a 3.0 mm hook, "
        "or the stuffing will show through."
    ))
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph("Abbreviations (US)", styles["H3"]))
    ab_rows = [("MR", "Magic ring"), ("ch", "Chain"), ("sc", "Single crochet"),
               ("hdc", "Half double crochet"), ("dc", "Double crochet"),
               ("inc", "Increase — 2 sc in one st"), ("dec", "Invisible decrease"),
               ("sl st", "Slip stitch"), ("FO", "Fasten off"), ("(n)", "Stitch count at round end")]
    ab_data = [[Paragraph(h, cell_style(h, font="Helvetica-Bold", color=colors.white, size=8.8)) for h in ["Abbr", "Meaning"]]]
    for a, m in ab_rows:
        ab_data.append([Paragraph(a, cell_style(size=8.8)), Paragraph(m, cell_style(size=8.8))])
    abt = Table(ab_data, colWidths=[30 * mm, (PAGE_W - 40 * mm) - 30 * mm], repeatRows=1)
    abt.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), SAGE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PALE]),
        ("GRID", (0, 0), (-1, -1), 0.5, RULE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(abt)
    story.append(Spacer(1, 4 * mm))
    story.append(note_box(
        "Work in a continuous spiral unless a row says to turn; mark the first stitch of every round. The wings and the spike strip are "
        "the exceptions — both are worked flat, in turned rows. Work every stitch through both loops unless a note says otherwise."
    ))
    story.append(PageBreak())

    # ---------------- HEAD ----------------
    story.append(Paragraph("1 · Head", styles["SectionHead"]))
    story.append(Paragraph("Main colour · make 1 · worked top-down and LEFT OPEN", styles["SectionSub"]))
    story.append(note_box(
        "Do not close the head and do not fasten off. A big head is what makes a dragon read as a baby dragon. "
        "Two straight rounds only, then the decreases. Head and neck are BOTH left open at 18 stitches, so the two edges are the same size "
        "and can be ladder-stitched together cleanly — this joint carries all the weight of the head."
    ))
    story.append(Spacer(1, 3 * mm))
    story.append(instructions_table(HEAD))
    story.append(Spacer(1, 3 * mm))
    story.append(Paragraph("Finish", styles["H3"]))
    story.append(Paragraph("Stuff the head firmly. Leave the open 18-stitch edge for sewing to the body's neck (a long tail is optional). The snout is sewn on next, then the eyes, BEFORE the head is joined.", styles["Body"]))
    story.append(PageBreak())

    # ---------------- SNOUT ----------------
    story.append(Paragraph("2 · Snout", styles["SectionHead"]))
    story.append(Paragraph("Main colour · make 1", styles["SectionSub"]))
    story.append(instructions_table(SNOUT))
    story.append(Spacer(1, 3 * mm))
    story.append(Paragraph("Finish", styles["H3"]))
    story.append(Paragraph(
        "FO with a long tail and stuff lightly. Pin centred on Rnds 8–11 of the head, just below the eye line, and sew all the way around. "
        "It must project past the curve of the head, not sit flush — a dragon without a projecting snout reads as a bear. "
        "Embroider two small nostrils at the tip.", styles["Body"]))
    story.append(PageBreak())

    # ---------------- BODY ----------------
    story.append(Paragraph("3 · Body", styles["SectionHead"]))
    story.append(Paragraph("Main colour · make 1 · worked bottom-up", styles["SectionSub"]))
    story.append(note_box(
        "The neck is left open at 18 stitches so the head can be seated on it. Pack the neck firmly before you join the head — a soft neck is what lets the head flop forward."
    ))
    story.append(Spacer(1, 3 * mm))
    story.append(instructions_table(BODY))
    story.append(Spacer(1, 3 * mm))
    story.append(Paragraph("Finish", styles["H3"]))
    story.append(Paragraph(
        "FO with a 40 cm tail; do not close. When you join the head, ladder-stitch all the way around and then make a second pass and pull it tight — this joint carries the whole head.", styles["Body"]))
    story.append(PageBreak())

    # ---------------- LEGS ----------------
    story.append(Paragraph("4 · Legs", styles["SectionHead"]))
    story.append(Paragraph("Main colour · make 4 (2 back, 2 front)", styles["SectionSub"]))
    story.append(instructions_table(LEGS))
    story.append(Spacer(1, 3 * mm))
    story.append(Paragraph("Finish &amp; placement", styles["H3"]))
    story.append(Paragraph(
        "Stuff the lower half lightly, flatten the top 3 stitches, FO with a long tail. The pairs are different lengths on purpose: "
        "back legs (6 rounds / 26 mm) attach at Rnd 6 of the body; front legs (8 rounds / 34 mm) attach at Rnd 8. A higher join needs a longer leg "
        "so all four feet reach the table. Sew each pair about 8 stitches apart; angle the back legs under as haunches and the front legs slightly forward. "
        "The body rests on the table — the legs pose, they don't lift her.", styles["Body"]))
    story.append(PageBreak())

    # ---------------- HORNS ----------------
    story.append(Paragraph("5 · Horns", styles["SectionHead"]))
    story.append(Paragraph("Contrast colour · make 2", styles["SectionSub"]))
    story.append(instructions_table(HORNS))
    story.append(Spacer(1, 3 * mm))
    story.append(Paragraph("Finish", styles["H3"]))
    story.append(Paragraph("Do not stuff; FO with a long tail. Sew to the crown of the head, 6 stitches apart, angled back.", styles["Body"]))
    story.append(PageBreak())

    # ---------------- TAIL ----------------
    story.append(Paragraph("6 · Tail", styles["SectionHead"]))
    story.append(Paragraph("Contrast colour · make 1 · worked from the tip up so it tapers naturally", styles["SectionSub"]))
    story.append(instructions_table(TAIL))
    story.append(Spacer(1, 3 * mm))
    story.append(Paragraph("Finish", styles["H3"]))
    story.append(Paragraph("Stuff lightly, FO with a long tail, flatten the open end and sew it to the back of the body at Rnds 4–6.", styles["Body"]))
    story.append(PageBreak())

    # ---------------- WINGS ----------------
    story.append(Paragraph("7 · Wings", styles["SectionHead"]))
    story.append(Paragraph("Contrast colour · make 2 · worked flat, in turned rows", styles["SectionSub"]))
    story.append(Paragraph("<b>Ch 11.</b> Work in turned rows (ch 1 and turn at each row end).", styles["Body"]))
    story.append(Spacer(1, 2 * mm))
    w_data = [[Paragraph("Row", cell_style(font="Helvetica-Bold", color=colors.white, size=8.8)),
               Paragraph("Instruction", cell_style(font="Helvetica-Bold", color=colors.white, size=8.8)),
               Paragraph("Sts", cell_style(font="Helvetica-Bold", color=colors.white, size=8.8, align=TA_CENTER))]]
    for r, inst, n in WINGS_ROWS:
        w_data.append([
            Paragraph(r, cell_style(size=8.8)),
            Paragraph(inst, cell_style(size=8.8)),
            Paragraph(f"({n})", cell_style(size=8.8, align=TA_CENTER)),
        ])
    wt = Table(w_data, colWidths=[16 * mm, (PAGE_W - 40 * mm) - 32 * mm, 16 * mm], repeatRows=1)
    wt.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), SAGE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PALE]),
        ("GRID", (0, 0), (-1, -1), 0.5, RULE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(wt)
    story.append(Spacer(1, 3 * mm))
    story.append(note_box(
        "<b>The scallop maths.</b> The slip-stitch anchors are 2 + 2 + 4 = 8 stitches; the two shells each fan from a single stitch (2 more), "
        "so all 10 stitches of Row 3 are consumed and nothing is left over. Pin the straight inner edge across Rnds 10–11 of the body and sew the "
        "WHOLE edge so the scalloped edge stays free."
    ))
    story.append(PageBreak())

    # ---------------- SPIKES ----------------
    story.append(Paragraph("8 · Spikes", styles["SectionHead"]))
    story.append(Paragraph("Contrast colour · one continuous strip · worked flat", styles["SectionSub"]))
    story.append(note_box(
        "One continuous strip sewn down the centre back from crown to tail tip. 10 units/spikes: 3 on the head, 4 on the body, 3 on the tail. "
        "Each group makes one small cone (about 10 mm tall); the last stitch of one group is where the next begins, so the spikes form one continuous ridge with no gaps. "
        "The strip is about 13.5–15 cm long — slightly under the crown-to-tail path, so it goes on slightly snug."
    ))
    story.append(Spacer(1, 3 * mm))
    story.append(Paragraph("To make", styles["H3"]))
    story.append(Paragraph(
        "<b>Ch 4.</b> Sc in the 2nd ch from the hook, then work this group <b>10 times</b>: <b>ch 4, sl st in the 2nd ch from the hook, sc in the next ch, hdc in the next ch.</b> "
        "Then sc in the next 2 and FO with a long tail.", styles["Body"]))
    story.append(Spacer(1, 3 * mm))
    story.append(Paragraph("Fitting", styles["H3"]))
    story.append(Paragraph(
        "PIN it from crown to tail tip first; if it runs short add one more spike (about 13.5 mm), if long unpick from the plain end. "
        "The spikes deliberately touch — do not add plain stitches between them.", styles["Body"]))
    story.append(PageBreak())

    # ---------------- ASSEMBLY ----------------
    story.append(Paragraph("9 · Assembly", styles["SectionHead"]))
    story.append(Paragraph("Work in this order", styles["SectionSub"]))
    steps = [
        "Snout to the head, centred on Rnds 8–11, below the eye line.",
        "Eyes between Rnds 7 and 8, 8 stitches apart, just above the snout. Fit the washers BEFORE the head is joined — once closed you cannot reach inside.",
        "Horns to the crown, 6 stitches apart, angled back.",
        "Head to body — both edges open at 18 stitches. Pack the neck firmly, seat the head and ladder-stitch around, then a second tight pass.",
        "Legs: back pair to Rnd 6, front pair to Rnd 8, angled as described.",
        "Tail to the back of the body at Rnds 4–6.",
        "Wings across Rnds 10–11, sewn along the whole straight edge.",
        "Spike strip LAST — pin from crown to tail tip before you sew a single stitch.",
    ]
    story.append(numbered_steps(steps))
    story.append(Spacer(1, 6 * mm))
    story.append(Paragraph("Troubleshooting", styles["H3"]))
    problems = [
        "<b>Head flops forward.</b> Pack the neck firmly before closing and make the second ladder-stitch pass tight. If it still moves, the edges did not match — both head and neck must be open at 18 stitches.",
        "<b>Rocks back onto haunches.</b> The legs are all the same length and they cannot be. Back legs attach 26 mm up, front 34 mm up — work the back legs 6 rounds and the front 8.",
        "<b>Will not sit.</b> Legs sewn too high, or the base is under-stuffed. Back legs on Rnd 6, front on Rnd 8; keep the lower body firm enough to sit on.",
        "<b>Wings droop.</b> Sew along the whole straight inner edge, not just the top corner.",
        "<b>Spike strip is wrong length / curves.</b> It is ten chain-4 units worked end to end (not a single 40-chain). Pin the entire strip from crown to tail before sewing; add or unpick a spike as needed.",
        "<b>Looks like a bear.</b> The snout is missing or under-stuffed — it must project past the dome of the head.",
        "<b>Stuffing shows through.</b> Gauge too loose — 30 stitches should measure 43 mm across. Crochet tighter or drop to a 3.0 mm hook.",
    ]
    story.append(bullet_list(problems))
    story.append(PageBreak())

    # ---------------- SAFETY, COLOURWAYS, TERMS ----------------
    story.append(Paragraph("Safety &amp; finishing notes", styles["SectionHead"]))
    story.append(note_box(
        "Ember uses <b>10 mm safety eyes</b>, which are a small part and a choking hazard. Lock the washers from the inside before the head is joined to the body, "
        "and pull-test each eye. She is a decorative piece, not a toy for young children, and has not been tested to ASTM F963 or EN 71. "
        "To give her to a child, embroider the eyes instead and check every seam first."
    ))
    story.append(Spacer(1, 5 * mm))
    story.append(Paragraph("Colourways", styles["H3"]))
    story.append(Paragraph("Sage green · Dusty teal · Lilac · Charcoal · Blush pink", styles["BodyCenter"]))
    story.append(Spacer(1, 6 * mm))
    story.append(Paragraph("Terms of use", styles["H3"]))
    story.append(Paragraph(
        "This crochet pattern — including all instructions, stitch counts, photography and design elements — is the original work and intellectual property of "
        "Novality Store, designed by Novality Crochet Studio. Design code NS 08. Copyright © 2026 Novality Store. All rights reserved.", styles["Body"]))
    story.append(Spacer(1, 2 * mm))
    story.append(Paragraph("You may", styles["H3"]))
    story.append(Paragraph(
        "Make as many finished Embers as you like for yourself, gifts, or charity. Sell physical finished items made from this pattern in small batches, in shops, "
        "markets and online, provided credit is given to \u201cNovality Store\u201d.", styles["Body"]))
    story.append(Spacer(1, 2 * mm))
    story.append(Paragraph("You may not", styles["H3"]))
    story.append(Paragraph(
        "Resell, share, redistribute, translate, rewrite, publish or upload this digital PDF or its contents in any form. Do not alter, copy or recolor the pattern "
        "and claim it as your own. Do not use the Novality Store name, logo or photos beyond crediting the pattern. Do not mass-produce finished items commercially "
        "without written permission.", styles["Body"]))
    story.append(Spacer(1, 3 * mm))
    story.append(Paragraph("Happy crocheting! Tag your makes with <b>#NovalityStore</b> and <b>#EmberTheBabyDragon</b>.", styles["BodyCenter"]))
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph(f"Validated with Crochet Pattern Checker · {datetime.now().strftime('%d %B %Y')}", styles["Tiny"]))

    out = OUT / "Ember_the_Baby_Dragon_NS08_NovalityStore.pdf"
    doc = build_doc(out)
    doc.build(story)
    print("Wrote", out)
    return out


if __name__ == "__main__":
    build()
