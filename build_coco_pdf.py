#!/usr/bin/env python3
"""Build a high-fidelity PDF for NS 04 'Coco the Capybara'."""
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    HRFlowable, KeepTogether, ListFlowable, ListItem
)

OUT = Path(__file__).resolve().parent / "output" / "pdf" / "Coco_the_Capybara_NS04.pdf"

OUT.parent.mkdir(parents=True, exist_ok=True)

# ---------- palette ----------
BROWN = colors.HexColor("#8B5E3C")
DARK = colors.HexColor("#2C3E50")
MUTED = colors.HexColor("#7F8C8D")
LIGHT = colors.HexColor("#F5F0EB")
GREEN = colors.HexColor("#27AE60")
AMBER = colors.HexColor("#F39C12")
BORDER = colors.HexColor("#DCD3C9")

# ---------- styles ----------
styles = getSampleStyleSheet()
body = ParagraphStyle("body", parent=styles["Normal"], fontName="Helvetica",
                      fontSize=9.6, leading=14, textColor=DARK, spaceAfter=4)
body_indent = ParagraphStyle("body_indent", parent=body, leftIndent=14, spaceAfter=3)
h1 = ParagraphStyle("h1", parent=styles["Title"], fontName="Helvetica-Bold",
                    fontSize=30, leading=34, textColor=BROWN, spaceAfter=6, alignment=TA_CENTER)
h2 = ParagraphStyle("h2", parent=styles["Heading2"], fontName="Helvetica-Bold",
                    fontSize=16, leading=20, textColor=BROWN, spaceBefore=12, spaceAfter=6)
h3 = ParagraphStyle("h3", parent=styles["Heading3"], fontName="Helvetica-Bold",
                    fontSize=11.5, leading=15, textColor=DARK, spaceBefore=8, spaceAfter=3)
sub = ParagraphStyle("sub", parent=body, fontSize=10.5, leading=16, textColor=MUTED, alignment=TA_CENTER)
small = ParagraphStyle("small", parent=body, fontSize=8.2, leading=11, textColor=MUTED)
note = ParagraphStyle("note", parent=body, fontSize=9.4, leading=14, textColor=DARK, spaceBefore=4, spaceAfter=6)
box = ParagraphStyle("box", parent=body, fontSize=9.4, leading=14, textColor=DARK, paddingTop=6, paddingBottom=6)
th = ParagraphStyle("th", parent=body, fontName="Helvetica-Bold", fontSize=9.2, textColor=colors.white)
td = ParagraphStyle("td", parent=body, fontSize=9.2, leading=12.5, textColor=DARK)
tdc = ParagraphStyle("tdc", parent=td, alignment=TA_CENTER)

# ---------- helpers ----------
def P(text, style=body):
    return Paragraph(text, style)


def heading(text, style=h2):
    return [Paragraph(text, style), HRFlowable(width="100%", thickness=0.8, color=BORDER, spaceAfter=8)]


def table(header, rows, col_widths, header_bg=BROWN):
    data = [[Paragraph(h, th) for h in header]]
    for r in rows:
        data.append([Paragraph(c, tdc if i else td) for i, c in enumerate(r)])
    t = Table(data, colWidths=col_widths, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), header_bg),
        ("GRID", (0, 0), (-1, -1), 0.35, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t


def callout(lines, bg="#F9EFE3", border=BROWN):
    """A light callout box."""
    content = [[P(x, box)] for x in lines]
    t = Table(content, colWidths=[17 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor(bg)),
        ("BOX", (0, 0), (-1, -1), 1, border),
        ("LINEBEFORE", (0, 0), (0, -1), 2.5, border),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return t


def bullets(items, style=body_indent):
    return ListFlowable(
        [ListItem(P(x, style), leftIndent=14) for x in items],
        bulletType="bullet", start="•", bulletFontSize=7, leftIndent=12
    )


def page_decor(canvas, doc):
    canvas.saveState()
    # header
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(2 * cm, A4[1] - 1.1 * cm, "Design Code NS 04")
    canvas.drawRightString(A4[0] - 2 * cm, A4[1] - 1.1 * cm, "Coco the Capybara · Novality Store")
    canvas.setStrokeColor(BORDER)
    canvas.line(2 * cm, A4[1] - 1.25 * cm, A4[0] - 2 * cm, A4[1] - 1.25 * cm)
    # footer
    canvas.line(2 * cm, 1.25 * cm, A4[0] - 2 * cm, 1.25 * cm)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(2 * cm, 0.9 * cm, "© 2026 Novality Store · For personal use & small-batch finished sales")
    canvas.drawRightString(A4[0] - 2 * cm, 0.9 * cm, f"Page {doc.page}")
    canvas.restoreState()


def build_story():
    story = []

    # ---------------- COVER ----------------
    story.append(Spacer(1, 2.2 * cm))
    story.append(P("Novality Crochet Studio", sub))
    story.append(Spacer(1, 0.6 * cm))
    story.append(P("COCO<br/>the Capybara", h1))
    story.append(Spacer(1, 0.2 * cm))
    story.append(P("Design Code <b>NS 04</b>", sub))
    story.append(Spacer(1, 0.4 * cm))
    story.append(P("No plastic eyes · Intermediate · 2.5 – 3 hours", sub))
    story.append(Spacer(1, 0.6 * cm))
    story.append(P("A low, round, bottom-heavy capybara with a blunt sewn-on muzzle, plump stuffed legs and a calm embroidered sleeping face.", body))
    story.append(Spacer(1, 0.5 * cm))
    story.append(HRFlowable(width="45%", thickness=1, color=BROWN, spaceAfter=10, hAlign="CENTER"))

    cover_grid = Table([
        [P("<b>Finished size</b>", tdc), P("<b>Yarn</b>", tdc), P("<b>Hook</b>", tdc)],
        [P("About 10.3 cm (4 in) tall<br/>5 cm (2 in) wide", tdc),
         P("Worsted weight (#4)<br/>Warm brown, ~30 g", tdc),
         P("3.0 mm<br/>(US C-2 / D-3)", tdc)],
    ], colWidths=[5.7 * cm, 5.7 * cm, 5.7 * cm], hAlign="CENTER")
    cover_grid.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F9EFE3")),
        ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#E6D1BB")),
        ("SPAN", (0, 0), (0, -1)),
        ("SPAN", (1, 0), (1, -1)),
        ("SPAN", (2, 0), (2, -1)),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
    ]))
    story.append(cover_grid)
    story.append(Spacer(1, 1.0 * cm))
    story.append(P("Copyright © 2026 Novality Store. All rights reserved.", small))
    story.append(PageBreak())

    # ---------------- SAFETY ----------------
    story += heading("Safety — embroidered face, no plastic parts")
    story.append(callout([
        "Coco has <b>no safety eyes</b> and <b>no small plastic parts</b>, which makes the face safer than a safety-eyed toy.",
        "That does <b>not</b> make the finished toy suitable for babies: Coco is a stuffed toy with a sewn-on muzzle and sewn-on ears, and it has <b>not been tested</b> to a toy-safety standard such as ASTM F963 or EN 71.",
        "Intended as a decorative item, or a gift for a child old enough not to chew it. Check every seam — especially the muzzle and ears — before giving Coco to a young child."
    ]))

    # ---------------- MATERIALS ----------------
    story += heading("Materials")
    story.append(bullets([
        "<b>Main yarn</b> — Worsted weight (#4), warm brown, about 30 g. A smooth matte yarn shows the stitch texture best.",
        "<b>Face yarn</b> — Worsted weight (#4), dark brown, about 5 g, for the closed eyes, nose and mouth. Use the same weight as the main yarn.",
        "<b>Hook</b> — 3.0 mm (US C-2 or D-3). The gauge is written for this hook.",
        "<b>Eyes</b> — None. The sleeping face is embroidered — no safety eyes.",
        "<b>Also needed</b> — Polyester fiber filling about 5–8 g; yarn needle; stitch marker; pins. Pins matter: the muzzle and ears are pinned before sewing."
    ]))

    # ---------------- GAUGE ----------------
    story += heading("Gauge & finished size")
    story.append(callout([
        "<b>Gauge:</b> 36 sc around measures about <b>52 mm</b> in diameter when stuffed (4.5 mm per stitch, 4.3 mm per round).",
        "Check it on the body <b>after Rnd 6</b> — a stuffed tube, not a flat swatch. If your 36 sts measure wider than 52 mm, crochet more tightly or go down a hook size; a loose gauge will show stuffing.",
        "<b>Finished size:</b> about 10.3 cm (4 in) tall, 5 cm (2 in) wide."
    ]))

    # ---------------- ABBREVIATIONS ----------------
    story += heading("Abbreviations")
    story.append(table(
        ["Abbr", "Meaning", "Abbr", "Meaning"],
        [
            ["MR", "magic ring", "sl st", "slip stitch"],
            ["ch", "chain", "st(s)", "stitch(es)"],
            ["sc", "single crochet", "Rnd(s)", "round(s)"],
            ["inc", "increase (2 sc in one st)", "FO", "fasten off"],
            ["invdec", "invisible decrease", "(n)", "stitch count at round end"],
        ],
        [2.4 * cm, 6.1 * cm, 2.4 * cm, 6.1 * cm]
    ))
    story.append(Spacer(1, 0.4 * cm))
    story.append(P("Work in a <b>continuous spiral</b> — do not join and do not chain 1 between rounds. Keep a marker in the first stitch of every round. Work every stitch through both loops unless a note says otherwise.", body))

    # ---------------- TECHNIQUES ----------------
    story += heading("Techniques")
    story.append(P("<b>1 · The magic ring</b> — Every piece begins with a magic ring. Pull the tail tight once the first round is complete.", note))
    story.append(P("<b>2 · Working in a spiral</b> — Keep a stitch marker in the first stitch of every round and move it up. There is no seam and no join to count from.", note))
    story.append(P("<b>3 · The two-layer leg join</b> — This is the only fiddly step — worth practicing once on a scrap magic ring. Hold a finished leg against the body with the pinched-flat top of the leg lying against the outside of the body. Insert the hook through <b>BOTH</b> the leg and the body stitch and work one single crochet; the leg edge and body stitch are treated as one stitch. They still count as one stitch each, so every count in the body table stays correct. Pinch the leg top flat first — a round, un-pinched top will not lie against the curved body and the join will pucker.", note))

    story.append(Spacer(1, 0.3 * cm))
    story.append(P("<b>Pinching the leg top</b> — A 9-stitch leg top flattens to about 5 stitches across — pinch it down to a strip about 3 stitches wide and hold it while you join. The stitches you don’t join bunch up inside, and that bunch makes the leg look plump rather than tubular. Don’t keep the top flat and wide.", note))

    # ---------------- HOW HEIGHT ADDS UP ----------------
    story += heading("How the height adds up")
    story.append(table(
        ["Part", "Calculation", "Result"],
        [
            ["Body, Rnd 1–20", "20 rnd × 4.3 mm", "86 mm"],
            ["Legs lift the body off the table", "short 8/9-round legs", "17 mm"],
            ["<b>Total standing height</b>", "86 + 17", "<b>103 mm = 10.3 cm</b>"],
        ],
        [7.0 * cm, 5.0 * cm, 5.0 * cm]
    ))

    # ---------------- LEGS ----------------
    story.append(PageBreak())
    story += heading("Part 1 · Legs")
    story.append(P("Make <b>2 back legs (8 rounds)</b> and <b>2 front legs (9 rounds)</b>. Stuff the lower half of each leg lightly, leaving the top loose. Back legs stop after Rnd 8; front legs work Rnd 9 too — they join one round higher and need to be one round longer so all four feet reach the table level.", note))
    story.append(table(
        ["Rnd", "Instruction", "Sts", "Note"],
        [
            ["R1", "6 sc in MR", "(6)", "all four"],
            ["R2", "[1 sc, inc] x 3", "(9)", "all four"],
            ["R3", "sc in each st around", "(9)", "all four"],
            ["R4", "sc in each st around", "(9)", "all four"],
            ["R5", "sc in each st around", "(9)", "all four"],
            ["R6", "sc in each st around", "(9)", "all four"],
            ["R7", "sc in each st around", "(9)", "all four"],
            ["R8", "sc in each st around", "(9)", "BACK legs finish here"],
            ["R9", "sc in each st around", "(9)", "FRONT legs only"],
        ],
        [1.4 * cm, 6.2 * cm, 1.6 * cm, 8.8 * cm]
    ))
    story.append(Spacer(1, 0.3 * cm))
    story.append(callout([
        "<b>Finish:</b> FO with a long tail for sewing. Before joining, pinch the whole 9-stitch top flat into a narrow strip about 3 stitches wide (see technique 3)."
    ]))

    # ---------------- EAR & MUZZLE ----------------
    story.append(PageBreak())
    story += heading("Part 1 · Ear and Muzzle")
    story.append(Spacer(1, 0.1 * cm))

    story.append(P("<b>EAR — make 2 (do not stuff)</b>", h3))
    story.append(table(
        ["Rnd", "Instruction", "Sts"],
        [
            ["R1", "6 sc in MR", "(6)"],
            ["R2", "[1 sc, inc] x 3", "(9)"],
            ["R3", "sc in each st around", "(9)"],
        ],
        [1.6 * cm, 8.0 * cm, 2.0 * cm]
    ))
    story.append(P("FO with a long tail, do not stuff — a shallow cup.", note))

    story.append(Spacer(1, 0.5 * cm))
    story.append(P("<b>MUZZLE — make 1 (stuff lightly)</b>", h3))
    story.append(table(
        ["Rnd", "Instruction", "Sts"],
        [
            ["R1", "6 sc in MR", "(6)"],
            ["R2", "[1 sc, inc] x 3", "(9)"],
            ["R3", "[2 sc, inc] x 3", "(12)"],
            ["R4", "sc in each st around", "(12)"],
            ["R5", "sc in each st around", "(12)"],
        ],
        [1.6 * cm, 8.0 * cm, 2.0 * cm]
    ))
    story.append(P("FO with a long tail and stuff lightly, just enough to hold a dome; it should sit proud of the head when sewn on.", note))

    # ---------------- BODY & HEAD ----------------
    story.append(PageBreak())
    story += heading("Part 2 · Body and Head")
    story.append(P("Both are 36 stitches around with only a shallow waist between them — that is what makes Coco read as one round blob rather than a snowman. The legs are joined low at Rnd 4–5.", note))
    story.append(table(
        ["Rnd", "Instruction", "Sts", "Note"],
        [
            ["R1", "6 sc in MR", "(6)", ""],
            ["R2", "inc in each st around", "(12)", ""],
            ["R3", "[1 sc, inc] x 6", "(18)", ""],
            ["R4", "3 sc, [1 sc, inc] x 3, 3 sc, [1 sc, inc] x 3", "(24)", "join the BACK legs"],
            ["R5", "[3 sc, inc] x 6", "(30)", "join the FRONT legs"],
            ["R6", "[4 sc, inc] x 6", "(36)", "full width — check gauge"],
            ["R7", "sc in each st around", "(36)", ""],
            ["R8", "sc in each st around", "(36)", ""],
            ["R9", "sc in each st around", "(36)", "stuff the body FIRMLY"],
            ["R10", "[7 sc, invdec] x 4", "(32)", "shallow waist"],
            ["R11", "[7 sc, inc] x 4", "(36)", "head begins"],
            ["R12", "sc in each st around", "(36)", "muzzle over R12–14"],
            ["R13", "sc in each st around", "(36)", ""],
            ["R14", "sc in each st around", "(36)", "eyes at R14–15"],
            ["R15", "sc in each st around", "(36)", "ears at R15"],
            ["R16", "[4 sc, invdec] x 6", "(30)", ""],
            ["R17", "[3 sc, invdec] x 6", "(24)", "stuff the head firmly"],
            ["R18", "[2 sc, invdec] x 6", "(18)", ""],
            ["R19", "[1 sc, invdec] x 6", "(12)", "top up stuffing"],
            ["R20", "invdec x 6", "(6)", ""],
        ],
        [1.4 * cm, 6.8 * cm, 1.6 * cm, 8.2 * cm]
    ))
    story.append(Spacer(1, 0.3 * cm))
    story.append(callout([
        "<b>Finish.</b> Cinch the remaining 6 stitches closed and weave the tail inside the body. <b>Do not decrease the Rnd 10 waist further</b> — a narrow neck cannot hold the head upright on this shape."
    ]))

    # ---------------- JOINING THE LEGS ----------------
    story.append(PageBreak())
    story += heading("Part 2 · Joining the Legs")
    story.append(P("Work Rnd 4 and Rnd 5 as the plain increase rounds in the body table, but as you reach each leg position, hold a pinched-flat leg against the body and work the next 3 sc through <b>BOTH</b> the leg and the body together (technique 3). Those 3 sc still count as 3 stitches of the round, so the stitch totals do not change — Rnd 4 ends at 24, Rnd 5 at 30.", note))

    story.append(Spacer(1, 0.2 * cm))
    story.append(P("<b>Rnd 4 — the BACK legs (total 24 stitches)</b>", h3))
    story.append(bullets([
        "1. Work the first 3 sc through a leg and the body together, then [1 sc, inc] x 3.",
        "2. Work the next 3 sc through the second leg and the body together, then [1 sc, inc] x 3 to the end of the round."
    ]))

    story.append(Spacer(1, 0.2 * cm))
    story.append(P("<b>Rnd 5 — the FRONT legs (total 30 stitches)</b>", h3))
    story.append(callout([
        "Work Rnd 5 as the increase round <b>[3 sc, inc] x 6</b>, keeping all 6 increases.",
        "Position the leg joins within that round: <b>work 7 stitches · join a leg over the next 3 stitches · work 10 stitches · join a leg over the next 3 stitches · work 7 stitches</b> to the end.",
        "That is 7 + 3 + 10 + 3 + 7 = 30 stitches. The 6 increases are worked inside the 7 / 10 / 7 sections and are <b>counted in those totals</b> — do not add them separately. Rnd 4’s 24 stitches are used exactly.",
        "The 7-10-7 spacing centres each front leg between the two back legs. <b>Work the numbers exactly.</b> If the front legs line up directly behind the back legs instead of between them, the footprint narrows and Coco tips. Hold the piece upside down and check all four legs sit square before you stuff the body."
    ]))

    # ---------------- WHY LEGS JOIN LOW ----------------
    story += heading("Part 3 · Why the legs join so low")
    story.append(P("The legs join low (Rnd 4–5) so every foot hangs <b>about 17 mm below the body</b> and Coco stands on her feet, not her belly.", note))
    story.append(callout([
        "<b>Why the legs join so low.</b> Back legs (8 rnd, ~34 mm) join at Rnd 4, only 17 mm above the base; front legs (9 rnd, ~39 mm) join at Rnd 5, 21 mm up. Different lengths, same result: every foot hangs about 17 mm below the body so all four land level. This is the most common failure on round-bodied animals."
    ]))

    # ---------------- FACE & ASSEMBLY ----------------
    story.append(PageBreak())
    story += heading("Part 4 · Face and Assembly")
    story.append(P("<b>Muzzle</b> — Stuff lightly and pin it to the front of the head over Rnd 12–14, centered, then sew all the way around with matching brown. It should sit proud of the head, not flush. Centering matters — the eyes go 6 stitches apart and a muzzle pinned even slightly off-center crowds one eye.", note))
    story.append(P("<b>Eyes</b> — Embroider — do not use safety eyes. With dark brown, work a shallow downward arc about 3 stitches wide on each side, at Rnd 14–15, 6 stitches apart, with a tiny tick angled down at each outer end. This closed-eye curve is what makes Coco look asleep.", note))
    story.append(P("<b>Nose & mouth</b> — Embroider <b>AFTER</b> the muzzle is sewn on, so the stitches sit on the finished curve. On the muzzle, work a small dark triangle at top center, a short vertical line down from it, and a soft curved mouth to one side.", note))
    story.append(P("<b>Ears</b> — Pinch the base of each ear so it cups forward, then sew at Rnd 15, about 5 stitches apart, angled slightly outward. Rnd 15 is a full 36-st round, so this puts the ears on top of the head where a capybara’s belong.", note))
    story.append(P("<b>Legs</b> — The legs were joined during Rnd 4–5 — there is nothing to sew. Just check each pinched 3-stitch strip is caught fully in the round.", note))
    story.append(P("<b>Final shaping</b> — Roll the finished piece gently between your palms to settle the stuffing into a round, bottom-heavy shape.", note))

    story.append(Spacer(1, 0.3 * cm))
    story.append(P("<b>Before you sew</b> — lay every component out and check:", h3))
    story.append(bullets([
        "4 legs (2 back of 8 rounds, 2 front of 9) · 2 ears · 1 muzzle · 1 body & head, closed at the crown.",
        "The sleeping face is all embroidery — closed-eye arcs, a small triangle nose and a soft curved mouth."
    ]))

    # ---------------- TROUBLESHOOTING ----------------
    story.append(PageBreak())
    story += heading("Troubleshooting")
    story.append(bullets([
        "<b>Coco looks too tall.</b> Almost always too many plain rounds. Rnd 12–15 is the straight head section the face is positioned on; adding \u201cjust one more\u201d round turns the shape into a tower and moves the face.",
        "<b>Coco will not stand.</b> Check the join height, not the leg spacing. The legs belong on Rnd 4 and Rnd 5; joined any higher, they cannot clear the underside of the body and the belly rests on the table.",
        "<b>Coco tips forward or backward.</b> Most often the front legs are lined up behind the back legs instead of between them — the Rnd 5 spacing must be 7 sc, 10 sc, 7 sc. If still tipping, stuff the lower body more firmly and settle weight back over all four feet.",
        "<b>Rocks back, front feet in the air.</b> All four legs are the same length and they cannot be. Front legs join at Rnd 5 (21 mm up), back at Rnd 4 (17 mm up); work the front legs 9 rounds and the back legs 8.",
        "<b>The head flops back.</b> The Rnd 10 waist is deliberately shallow at 32 stitches — do not decrease it further. A narrow neck cannot hold the head upright.",
        "<b>Small hole where a leg meets the body.</b> You joined a flat, wide leg top instead of a pinched one. Flatten the whole 9-stitch top into a strip about 3 stitches wide before joining, so the un-joined stitches bunch up inside.",
        "<b>Muzzle looks flat / stuffing shows.</b> Stuff the muzzle just enough to hold a dome. If stuffing shows through the body, your gauge is too loose — 36 sts should measure 52 mm; crochet tighter or go down a hook size."
    ]))

    # ---------------- COLORWAYS ----------------
    story += heading("Colorways")
    story.append(P("Classic warm brown · Soft grey · Sandy beige · Cocoa", body))

    # ---------------- DESIGNER NOTES ----------------
    story += heading("Designer Notes")
    story.append(P("<b>Bottom-heavy by design.</b> Stuff the lower body firmly and keep the shape squat. Coco is meant to be one continuous curve from base to crown — she stands on her feet, not her belly.", note))

    # ---------------- TERMS OF USE ----------------
    story.append(PageBreak())
    story += heading("Terms of Use")
    story.append(P("<b>Copyright & ownership</b>", h3))
    story.append(P("This crochet pattern — including all instructions, stitch counts, photography and design elements — is the original work and intellectual property of <b>Novality Store</b>, designed by <b>Novality Crochet Studio</b>. Design Code NS 04. Copyright © 2026 Novality Store. All rights reserved.", note))

    story.append(P("<b>You may</b>", h3))
    story.append(bullets([
        "Make as many finished Coco plushies as you like for yourself, gifts, or charity.",
        "Sell physical finished items made from this pattern in small batches, in shops, markets and online, provided credit is given to \u201cNovality Store\u201d (a link or tag is always appreciated)."
    ]))

    story.append(P("<b>You may not</b>", h3))
    story.append(bullets([
        "Resell, share, redistribute, translate, rewrite, publish or upload this digital PDF or its contents in any form.",
        "Alter, copy or recolor the pattern and claim it as your own.",
        "Use the Novality Store name, logo or photos in your own listings beyond crediting the pattern.",
        "Mass-produce finished items commercially without written permission."
    ]))

    story.append(P("<b>Safety reminder</b>", h3))
    story.append(P("This pattern has not been tested to a toy-safety standard (ASTM F963 / EN 71). Although Coco has no plastic parts, finished items made for sale must be assessed by the seller against local toy-safety laws. Reinforce all sewn-on parts before giving to a young child.", note))

    story.append(Spacer(1, 0.5 * cm))
    story.append(HRFlowable(width="100%", thickness=0.8, color=BORDER, spaceAfter=8))
    story.append(P("<b>Happy crocheting!</b>", h3))
    story.append(P("Tag your makes with <b>#NovalityStore</b> and <b>#CocoTheCapybara</b> — we love seeing your Cocos. Thank you for supporting an independent pattern designer.", body))

    return story


def main():
    doc = SimpleDocTemplate(
        str(OUT), pagesize=A4,
        rightMargin=2 * cm, leftMargin=2 * cm,
        topMargin=1.8 * cm, bottomMargin=1.8 * cm,
        title="Coco the Capybara — Design Code NS 04",
        author="Novality Store",
        subject="Crochet pattern — Coco the Capybara"
    )
    doc.build(build_story(), onFirstPage=page_decor, onLaterPages=page_decor)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
