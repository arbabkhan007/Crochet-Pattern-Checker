#!/usr/bin/env python3
"""NS01 Hamish — market PDF v6. Fixes over v3: print-check square removed
(nothing depends on print scale), fringe trim distance corrected (~1 cm),
concept-image disclosure on every photo incl. cover, scarf cord safety
(closed loop / omit for under-3s), Option B legs R9-R12, symmetric larger
placement map, heading keep-togethers, no unembedded Helvetica reference."""
from pathlib import Path
from PIL import Image as PILImage
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, PageBreak, Table, TableStyle, Image as RLImage,
                                KeepTogether, NextPageTemplate, CondPageBreak)
from reportlab.graphics.shapes import Drawing, Circle, Ellipse, Line, String, Rect
from reportlab.pdfgen import canvas as _pdfcanvas

class EmbeddedCanvas(_pdfcanvas.Canvas):
    def __init__(self, *args, **kwargs):
        kwargs['initialFontName'] = 'DVS'  # override doc template default (Helvetica)
        kwargs.setdefault('initialFontSize', 9)
        super().__init__(*args, **kwargs)
    def setFont(self, name, size, leading=None):
        if name.startswith('Helvetica') or name.startswith('Times'):
            name = 'DVS-Bold' if 'Bold' in name else 'DVS'
        return super().setFont(name, size, leading)

ROOT = Path('/home/user/Crochet-Pattern-Checker')
OUT = ROOT / 'deliverables' / 'NS01_Hamish_Market_Pattern_v6.pdf'
PAGE_W, PAGE_H = A4

# ---------- embedded fonts ----------
FD = '/usr/share/fonts/truetype/dejavu/'
pdfmetrics.registerFont(TTFont('DVS', FD + 'DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DVS-Bold', FD + 'DejaVuSans-Bold.ttf'))
pdfmetrics.registerFont(TTFont('DVSerif', FD + 'DejaVuSerif.ttf'))
pdfmetrics.registerFontFamily('DVS', normal='DVS', bold='DVS-Bold', italic='DVS', boldItalic='DVS-Bold')

CREAM = colors.HexColor('#FAF5EC'); OAT = colors.HexColor('#EFE3CE')
GINGER = colors.HexColor('#A65A1E'); GINGER_D = colors.HexColor('#7E4212')
BROWN = colors.HexColor('#433026'); INK = colors.HexColor('#2E2620')
RUST = colors.HexColor('#9C4A1F'); LINE = colors.HexColor('#D8C6A8')
FAINT = colors.HexColor('#6B5744')

def prep(src, dst, maxw=1500):
    im = PILImage.open(ROOT / src).convert('RGB')
    im.thumbnail((maxw, maxw))
    im.save(dst, quality=88)
    return dst, im.size

COVER, COVER_SIZE = prep('assets/patterns/ns01/hamish_cover_concept.png', '/tmp/v6_cover.jpg')
HERO, HERO_SIZE = prep('docs/ns01/assets/hamish_hero.png', '/tmp/v6_hero.jpg')
MATS, MATS_SIZE = prep('assets/patterns/ns01/hamish_materials_concept.png', '/tmp/v6_mats.jpg')

def st(name, **kw):
    base = dict(fontName='DVS', fontSize=9.2, leading=13, textColor=INK)
    base.update(kw); return ParagraphStyle(name, **base)

TITLE = st('title', fontName='DVS-Bold', fontSize=14.5, leading=17, textColor=GINGER_D, spaceBefore=8, spaceAfter=4)
H2 = st('h2', fontName='DVS-Bold', fontSize=11, leading=13.5, textColor=GINGER_D, spaceBefore=8, spaceAfter=3, keepWithNext=1)
BODY = st('body', spaceAfter=4)
SMALL = st('small', fontSize=8, leading=10.5, textColor=FAINT)
NOTE_P = st('note', fontSize=8.4, leading=11.5)
ROUND_P = st('round', fontSize=9.1, leading=12.4, leftIndent=10, firstLineIndent=-10, spaceAfter=2)
BULLET = st('bullet', fontSize=9.2, leading=12.8, leftIndent=12, firstLineIndent=-8, spaceAfter=2.2)
CELL = st('cell', fontSize=8.6, leading=11.2)
CELLF = st('cellf', fontName='DVS-Bold', fontSize=8.6, leading=11.2)
CELLH = st('cellh', fontName='DVS-Bold', fontSize=8.6, leading=11.2, textColor=colors.white)
CAP = st('cap', fontSize=7.8, leading=10, textColor=FAINT, spaceBefore=2, spaceAfter=4)

def P(txt, style=BODY): return Paragraph(txt, style)
def R(label, txt): return Paragraph(f'<b>{label}</b> {txt}', ROUND_P)
def B(txt): return Paragraph(f'•&nbsp;&nbsp;{txt}', BULLET)

def esc(t): return t.replace('&', '&amp;')

def callout(title, body):
    t = Table([[Paragraph(f'<b>{title}</b><br/>{body}', NOTE_P)]], colWidths=[PAGE_W - 36*mm])
    t.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), OAT), ('BOX', (0,0), (-1,-1), 0.7, LINE),
        ('LEFTPADDING', (0,0), (-1,-1), 9), ('RIGHTPADDING', (0,0), (-1,-1), 9),
        ('TOPPADDING', (0,0), (-1,-1), 7), ('BOTTOMPADDING', (0,0), (-1,-1), 7), ('ROUNDEDCORNERS', [4,4,4,4])]))
    return t

def data_table(rows, widths, header=True, first_bold=True):
    out = []
    for r, row in enumerate(rows):
        cells = []
        for c, val in enumerate(row):
            sty = CELLH if (header and r == 0) else (CELLF if (first_bold and c == 0) else CELL)
            cells.append(Paragraph(esc(val), sty))
        out.append(cells)
    t = Table(out, colWidths=widths, repeatRows=1 if header else 0)
    style = [('VALIGN', (0,0), (-1,-1), 'TOP'), ('LEFTPADDING', (0,0), (-1,-1), 6),
             ('RIGHTPADDING', (0,0), (-1,-1), 6), ('TOPPADDING', (0,0), (-1,-1), 4),
             ('BOTTOMPADDING', (0,0), (-1,-1), 4), ('GRID', (0,0), (-1,-1), 0.4, LINE),
             ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#FBF7EF')])]
    if header:
        style += [('BACKGROUND', (0,0), (-1,0), GINGER)]
    t.setStyle(TableStyle(style))
    return t

# ---------- cover ----------
BADGES = ['INTERMEDIATE', 'US TERMS', 'SIZE 14-15 CM', 'CODE NS01']
def on_cover(canv, doc):
    canv.saveState()
    canv.setFillColor(CREAM); canv.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    canv.setFillColor(RUST); canv.setFont('DVS-Bold', 10)
    canv.drawCentredString(PAGE_W/2, PAGE_H - 40, 'N O V A L I T Y   S T O R E')
    # framed portrait photo (864 px wide shown at 330 pt = ~188 ppi)
    iw = 330; ih = iw * COVER_SIZE[1] / COVER_SIZE[0]
    ix = (PAGE_W - iw) / 2; iy = PAGE_H - 58 - ih
    canv.setFillColor(GINGER); canv.roundRect(ix - 7, iy - 7, iw + 14, ih + 14, 6, stroke=0, fill=1)
    canv.setFillColor(colors.white); canv.roundRect(ix - 3.5, iy - 3.5, iw + 7, ih + 7, 4, stroke=0, fill=1)
    canv.drawImage(COVER, ix, iy, width=iw, height=ih)
    cy = iy - 44
    canv.setFillColor(BROWN); canv.setFont('DVS-Bold', 33)
    canv.drawCentredString(PAGE_W/2, cy, 'Hamish')
    cy -= 25
    canv.setFont('DVS', 15.5); canv.drawCentredString(PAGE_W/2, cy, 'the Highland Cow')
    cy -= 19
    canv.setFillColor(GINGER_D); canv.setFont('DVSerif', 10.5)
    canv.drawCentredString(PAGE_W/2, cy, 'Amigurumi Crochet Pattern — worked in pieces, sewn with confidence')
    cy -= 28
    widths = [stringWidth(b, 'DVS-Bold', 7.2) + 18 for b in BADGES]
    x = (PAGE_W - sum(widths) - 9*(len(widths)-1)) / 2
    for b, w in zip(BADGES, widths):
        canv.setStrokeColor(GINGER); canv.setFillColor(colors.white)
        canv.roundRect(x, cy - 4, w, 16, 8, stroke=1, fill=1)
        canv.setFillColor(GINGER_D); canv.setFont('DVS-Bold', 7.2)
        canv.drawCentredString(x + w/2, cy + 1.2, b)
        x += w + 9
    canv.setFillColor(FAINT); canv.setFont('DVS', 7.6)
    canv.drawCentredString(PAGE_W/2, 100, 'Concept image (AI-generated, not a photograph of a finished sample), shown for colour and character.')
    canv.drawCentredString(PAGE_W/2, 88, 'The pattern scarf is a plain solid-rust strip, and the fringe must be trimmed to clear the eyes (Section 8).')
    canv.setFont('DVS', 8.2)
    canv.drawCentredString(PAGE_W/2, 56, 'Corrected Edition v6  •  PDF pattern — this is not a finished toy')
    canv.setFont('DVS', 7.8)
    canv.drawCentredString(PAGE_W/2, 42, '© Novality Store · Design code NS01 · Please do not share or resell this file')
    canv.restoreState()

def on_page(canv, doc):
    canv.saveState()
    canv.setStrokeColor(LINE); canv.setLineWidth(0.6)
    canv.line(18*mm, PAGE_H - 13*mm, PAGE_W - 18*mm, PAGE_H - 13*mm)
    canv.setFillColor(GINGER_D); canv.setFont('DVS-Bold', 7.2)
    canv.drawString(18*mm, PAGE_H - 11*mm, 'HAMISH THE HIGHLAND COW — NS01')
    canv.setFillColor(FAINT); canv.setFont('DVS', 7.2)
    canv.drawRightString(PAGE_W - 18*mm, PAGE_H - 11*mm, 'NOVALITY STORE')
    canv.setStrokeColor(LINE); canv.line(18*mm, 13*mm, PAGE_W - 18*mm, 13*mm)
    canv.setFont('DVS', 7.2)
    canv.drawString(18*mm, 9.5*mm, '© Novality Store — personal use; finished items may be sold in small batches with credit.')
    canv.drawRightString(PAGE_W - 18*mm, 9.5*mm, f'Page {doc.page}')
    canv.restoreState()

doc = BaseDocTemplate(str(OUT), pagesize=A4, leftMargin=18*mm, rightMargin=18*mm,
                      topMargin=18*mm, bottomMargin=16*mm,
                      title='Hamish the Highland Cow — Crochet Pattern NS01 (Corrected Edition v6)',
                      author='Novality Store')
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='main')
doc.addPageTemplates([PageTemplate(id='cover', frames=[frame], onPage=on_cover),
                      PageTemplate(id='page', frames=[frame], onPage=on_page)])

S = [Spacer(1, PAGE_H - 40*mm), NextPageTemplate('page'), PageBreak()]

# ---------- page 2 ----------
S.append(P('Meet Hamish', TITLE))
hw = doc.width - 37; hh = hw * HERO_SIZE[1] / HERO_SIZE[0]
hero_img = RLImage(HERO, width=hw, height=hh); hero_img.hAlign = 'CENTER'
S.append(hero_img)
S.append(P('Concept image (AI-generated, not a photograph of a finished sample): the plaid scarf, fabric bandana and added coat fringe are styling only. The pattern makes the forehead fringe and a plain solid-rust scarf, with a ribbon option; hooves are chocolate (Yarn C).', CAP))
S.append(P('A shaggy, sturdy Highland cow with a flattened brow, a wide cream muzzle and a rustic fringe. '
           'Hamish is worked in pieces — head, body, ears, horns, legs, muzzle and belly patch — so every proportion can be pinned and checked before sewing.', BODY))
S.append(P('At a glance', H2))
S.append(data_table([
    ['Skill level', 'Intermediate — comfortable with spiral amigurumi, invisible decreases and sewing pieces'],
    ['Finished size', 'Approx. 14–15 cm (5.5–6 in) seated at stated gauge — confirm on your sample'],
    ['Gauge', '11 sc × 12 rnds = 5 cm (2 in) in spiral single crochet'],
    ['Hook', '3.5 mm (US E-4) — smaller than the ball band so stuffing cannot show'],
    ['Terminology', 'US crochet terms throughout'],
    ['Time', 'Approx. 6–8 hours'],
], [34*mm, doc.width - 34*mm], header=False))
S.append(Spacer(1, 5))
S.append(callout('Safety — read first.',
    'Hamish uses two 12&nbsp;mm plastic safety eyes. Lock each washer firmly from inside the head <b>before</b> stuffing and joining, then check the eye and fabric by hand. '
    'Sew every seam twice, weave ends in at least 5&nbsp;cm, and secure every knot in the fringe and tail. If an eye, washer or stitch fails, a small part can be released: '
    'not suitable for children under 3. The optional scarf or ribbon is a <b>loose cord</b>: for children under 3, leave it off entirely, or use the short closed Collar loop (Section 9b) sewn flat all the way round with no free ends (many markets cap free cord length at about 20 cm — check your local rules first). '
    'Embroidered eyes remove the plastic-eye hazard but do not by themselves make a toy compliant — sellers must meet the toy-safety rules of their market.'))
S.append(P('How this pattern is written', H2))
S.append(B('Work in a <b>continuous spiral</b> unless told otherwise; use a stitch marker in the first stitch of each round.'))
S.append(B('<b>R1, R2 …</b> means Round 1, Round 2. The number in brackets at the end of each round, e.g. (48), is the <b>stitch count</b> — count often, especially after increase and decrease rounds.'))
S.append(B('<b>Stuff as you go</b> where instructed; the head and body are joined through their matched 24-stitch openings.'))
S.append(B('Rounds are written top-down for the head and bottom-up for the body — follow the section headings.'))

# ---------- materials (flows on) ----------
S.append(P('Materials &amp; Tools', TITLE))
mw = doc.width; mh = mw * MATS_SIZE[1] / MATS_SIZE[0]
S.append(RLImage(MATS, width=mw, height=mh))
S.append(P('Your kit (concept image, AI-generated): Yarns A–C, 3.5 mm hook, safety eyes with washers, needle, pins, stitch marker, scissors, stuffing and optional ribbon.', CAP))
S.append(data_table([
    ['Item', 'Details'],
    ['Yarn A — Ginger', 'Worsted / aran (#4), approx. 35 g including fringe. Caramel, toffee or ginger gold.'],
    ['Yarn B — Oat cream', 'Worsted / aran (#4), approx. 12 g — muzzle, horns, inner ears, optional belly patch.'],
    ['Yarn C — Dark chocolate', 'Worsted / aran (#4), approx. 5 g — hooves and nostril embroidery.'],
    ['Yarn D — Rust (optional)', 'Worsted / aran (#4), approx. 6 g for the scarf or collar — or a generous 40 cm ribbon, fitted on the finished cow.'],
    ['Hook', '3.5 mm (US E-4)'],
    ['Eyes', 'Two 12 mm black safety eyes — or black embroidery floss for an embroidered-eye version.'],
    ['Notions', 'Polyester fiberfill (approx. 35 g), stitch markers, scrap contrast yarn, tapestry needle, pins, scissors.'],
], [40*mm, doc.width - 40*mm]))
S.append(P('Gauge — check before you start', H2))
S.append(P('Work <b>Rounds 1–6 of the Head</b> (Section 1) as your swatch: the flat disc should measure <b>about 5 cm across</b>. '
           'If it is larger, try a smaller hook; if smaller, a larger hook. Keep tension firm — stuffing should never show through.', BODY))
S.append(P('<i>Printing note: nothing in this pattern is measured from the page — all sizes come from your stitch counts and swatch. <b>A4: print at 100%. US Letter: choose “Fit to Page”</b> (printing Letter at 100% cuts off the bottom line of each page).</i>', BODY))
abbr = [P('Abbreviations (US terms)', H2), data_table([
    ['MR', 'magic ring', 'inc', '2 sc in the same stitch'],
    ['ch', 'chain', 'dec', 'invisible decrease (front loops of next 2 sts together)'],
    ['sl st', 'slip stitch', 'BLO', 'back loop only'],
    ['sc', 'single crochet', 'FO', 'fasten off'],
    ['hdc', 'half double crochet', 'R / rnd', 'round (R1 = Round 1)'],
    ['st(s)', 'stitch(es)', 'lark’s-head knot', 'fold a strand in half; pull the folded loop through the stitch, then pull the loose ends through the loop and tighten'],
], [20*mm, doc.width/2 - 20*mm, 24*mm, doc.width/2 - 24*mm], header=False)]
S.append(KeepTogether(abbr))
S.append(Spacer(1, 4))
S.append(callout('Before you start.',
    'Read the Assembly section (near the end) once through. The head and body both finish at <b>24 stitches</b> and stay open; the legs keep their top openings for sewing; the muzzle, ears and horns are sewn onto the head <b>before</b> the head is joined to the body.'))

# ---------- pattern ----------
S.append(Spacer(1, 6))
S.append(P('Pattern', TITLE))
S.append(CondPageBreak(120))
S.append(P('1 &nbsp; Head — Yarn A (top-down, continuous spiral)', H2))
for lab, txt in [
    ('R1', '6 sc in MR <b>(6)</b>'), ('R2', 'inc in each st around <b>(12)</b>'),
    ('R3', '[sc, inc] × 6 <b>(18)</b>'), ('R4', '[2 sc, inc] × 6 <b>(24)</b>'),
    ('R5', '[3 sc, inc] × 6 <b>(30)</b>'), ('R6', '[4 sc, inc] × 6 <b>(36)</b>'),
    ('R7', '[5 sc, inc] × 6 <b>(42)</b>'), ('R8', '[6 sc, inc] × 6 <b>(48)</b>'),
    ('R9–R15', 'sc in each st around (7 rnds) <b>(48)</b>')]:
    S.append(R(lab, txt))
S.append(P('<i>Insert the 12 mm safety eyes between <b>R10 and R11</b>, 7 stitches apart centre-to-centre. Mark the stitch midway between the eyes as your <b>front-centre line</b> — thread a short length of scrap contrast yarn through it so the mark survives stuffing. Horn, ear and fringe positions are counted from it. Lock the washers firmly inside.</i>', BODY))
for lab, txt in [
    ('R16', '[6 sc, dec] × 6 <b>(42)</b>'), ('R17', '[5 sc, dec] × 6 <b>(36)</b>'),
    ('R18', '[4 sc, dec] × 6 <b>(30)</b>'), ('R19', '[3 sc, dec] × 6 <b>(24)</b>')]:
    S.append(R(lab, txt))
S.append(P('Stuff the head firmly. FO after R19 with a 45 cm sewing tail. <b>Leave the 24-stitch neck opening unclosed.</b>', BODY))

S.append(CondPageBreak(120))
muzzle = [P('2 &nbsp; Muzzle — Yarn B', H2)] + [R(l, t) for l, t in [
    ('R1', '6 sc in MR <b>(6)</b>'), ('R2', 'inc in each st around <b>(12)</b>'),
    ('R3', '[sc, inc] × 6 <b>(18)</b>'), ('R4', '[2 sc, inc] × 6 <b>(24)</b>'),
    ('R5–R6', 'sc in each st around (2 rnds) <b>(24)</b>'), ('R7', '[2 sc, dec] × 6 <b>(18)</b>')]]
muzzle.append(P('FO with a 35 cm tail. Embroider two diagonal nostrils (Yarn C) on the upper front and secure the tails inside. '
           'Lightly stuff, flatten into a wide horizontal oval, and sew centred on the front-centre line below the eyes over <b>Head R13–R16</b> — see Assembly step 1.', BODY))
S.append(KeepTogether(muzzle))

S.append(CondPageBreak(120))
body_first = [P('3 &nbsp; Body — Yarn A (bottom-up, continuous spiral)', H2)] + [R(l, t) for l, t in [
    ('R1', '6 sc in MR <b>(6)</b>'), ('R2', 'inc in each st around <b>(12)</b>'),
    ('R3', '[sc, inc] × 6 <b>(18)</b>'), ('R4', '[2 sc, inc] × 6 <b>(24)</b>'),
    ('R5', '[3 sc, inc] × 6 <b>(30)</b>')]]
S.append(KeepTogether(body_first))
for lab, txt in [
    ('R6', '[4 sc, inc] × 6 <b>(36)</b>'),
    ('R7', '[5 sc, inc] × 6 <b>(42)</b>'), ('R8', '[6 sc, inc] × 6 <b>(48)</b>'),
    ('R9', 'BLO sc in each st around — flat sitting base edge <b>(48)</b>'),
    ('R10–R16', 'sc in each st around (7 rnds) <b>(48)</b>'),
    ('R17', '[6 sc, dec] × 6 <b>(42)</b>'), ('R18', 'sc in each st around <b>(42)</b>'),
    ('R19', '[5 sc, dec] × 6 <b>(36)</b>'), ('R20', '[4 sc, dec] × 6 <b>(30)</b>'),
    ('R21', '[3 sc, dec] × 6 <b>(24)</b>')]:
    S.append(R(lab, txt))
S.append(P('Stuff firmly, packing the flat base so Hamish sits level. FO with a 45 cm tail; <b>leave the 24-stitch neck open</b>.', BODY))

S.append(CondPageBreak(120))
belly = [P('4 &nbsp; Belly Patch — Yarn B (optional)', H2),
    R('Ch', '6.'),
    R('R1', 'sc in 2nd ch from hook, 3 sc, 3 sc in last ch; along opposite side of chain: 3 sc, 2 sc in first working ch (the same chain your first sc went into) <b>(12)</b>'),
    R('R2', 'inc, 3 sc, inc × 3, 3 sc, inc × 2 <b>(18)</b>'),
    R('R3', 'sc, inc, 3 sc, [sc, inc] × 3, 3 sc, [sc, inc] × 2, sl st to first sc <b>(24)</b>'),
    P('FO with a 30 cm tail. Sew vertically, long axis upright, to the centre front of the body over <b>R10–R16</b>, so the patch ends just below the first decrease round (R17).', BODY)]
S.append(KeepTogether(belly))
S.append(Spacer(1, 6))

S.append(CondPageBreak(120))
S.append(P('5 &nbsp; Legs — start Yarn C, change to Yarn A', H2))
S.append(P('Choose <b>Option A</b> — four splayed Standard Legs — or <b>Option B</b> — upright sit: 2 Standard Legs (back) + 2 Shortened Front Legs. '
           'Standard legs sew over the lowest body rounds <b>R9–R11</b> (just above the flat base); the wider 12-stitch Option B shortened fronts sew over <b>R9–R12</b> — see Assembly.', BODY))
S.append(P('<b>Standard Legs</b> (make 4 for Option A; 2 for Option B backs)', BODY))
for lab, txt in [
    ('R1 (C)', '6 sc in MR <b>(6)</b>'), ('R2', 'inc in each st around <b>(12)</b>'),
    ('R3', '[sc, inc] × 6 <b>(18)</b>'), ('R4', 'BLO sc in each st around — flat hoof sole <b>(18)</b>'),
    ('R5', 'sc in each st around <b>(18)</b>'),
    ('R6', 'sc in each st around; change to <b>Yarn A</b> on the last pull-through <b>(18)</b>'),
    ('R7 (A)', 'BLO sc in each st around — colour-transition ridge <b>(18)</b>'),
    ('R8', '[sc, dec] × 6 <b>(12)</b> — stuff the hoof firmly'),
    ('R9–R13', 'sc in each st around (5 rnds) <b>(12)</b>'),
    ('R14', '[2 sc, dec] × 3 <b>(9)</b> — stuff the upper leg lightly'),
    ('R15–R16', 'sc in each st around (2 rnds) <b>(9)</b>')]:
    S.append(R(lab, txt))
S.append(P('FO with a 35 cm sewing tail; leave the 9-stitch top open.', BODY))
S.append(P('<b>Shortened Front Legs</b> (Option B only, make 2): work R1–R8 of the Standard Leg, then R9–R10 sc in each st around (12). Stuff the hoof firmly and the top lightly. FO with a 35 cm tail; leave the 12-stitch top open.', BODY))

S.append(CondPageBreak(120))
ears_sec = [P('6 &nbsp; Flat Layered Ears — 2 Outer (Yarn A) + 2 Inner (Yarn B)', H2)]
ears_sec += [R(l, t) for l, t in [('R1', '6 sc in MR <b>(6)</b>'), ('R2', 'inc in each st around <b>(12)</b>'), ('R3', '[sc, inc] × 6 <b>(18)</b>')]]
ears_sec.append(P('<b>Inner ear (B):</b> FO and weave in ends. <b>Outer ear (A):</b> do not FO. Mark the first stitch of each layer; place inner and outer <b>wrong sides together</b> (cream facing front), markers aligned, and work <b>18 sc in Yarn A</b> through corresponding stitches of both layers. '
           'FO with a 30 cm tail. Pinch 3 bottom stitches together and tack closed to cup the ear. <b>Placement:</b> sew to <b>Head R8–R10</b> with the centre of each ear base about <b>10 stitches from the front-centre line</b>; pin both ears and mirror-check before sewing.', BODY))
S.append(KeepTogether(ears_sec))

S.append(CondPageBreak(120))
horns = [P('7 &nbsp; Horns — Yarn B (make 2)', H2)] + [R(l, t) for l, t in [
    ('R1', '4 sc in MR <b>(4)</b>'), ('R2', '[sc, inc] × 2 <b>(6)</b>'),
    ('R3–R4', 'sc in each st around (2 rnds) <b>(6)</b>'), ('R5', '[2 sc, inc] × 2 <b>(8)</b>'),
    ('R6–R7', 'sc in each st around (2 rnds) <b>(8)</b>')]]
horns.append(P('FO with a 30 cm tail. Stuff the tip lightly. For a gentle upward curve, pinch R4 to R5 on the inner side with one tiny hidden stitch. '
           '<b>Placement:</b> sew all 8 base stitches to <b>Head R6–R8</b>, centred about <b>7 stitches from the front-centre line</b> and slightly toward the face from the ears; pin and mirror-check first.', BODY))
S.append(KeepTogether(horns))

S.append(CondPageBreak(120))
tail_sec = [P('8 &nbsp; Tail &amp; Fringe — Yarn A', H2),
    P('<b>Tail:</b> cut 6 strands of Yarn A, 22 cm each. Attach with lark’s-head knots into 2 adjacent stitches at the centre back on <b>Body R10</b>, clear of the back legs. '
           'Divide the 12 hanging ends into <b>3 groups of 4</b> and braid for 4 cm. Tie an overhand knot and trim the tassel to 1.5 cm.', BODY),
    P('<b>Fringe:</b> cut 36–40 strands of Yarn A, 14 cm each (you will trim most of the length away; 8 cm strands reduce waste). '
           'Attach with lark’s-head knots in a horseshoe across the forehead on <b>Head R6, R7 and R8</b>, between the horns. The horseshoe has roughly 30 stitch positions, so some stitches take two strands. Comb the strands down, then trim: centre strands should end <b>just above the eye line</b> — at this gauge the eyes sit only about 1 cm below R8 — in a shallow V, and side strands shorter still, so the fringe <b>clears the eyes</b>. Never leave it hanging over the eyes or down to the muzzle.', BODY)]
S.append(KeepTogether(tail_sec))

S.append(CondPageBreak(120))
scarf = [P('9 &nbsp; Scarf — Yarn D (optional)', H2),
    R('Ch', '92.'),
    R('Row 1', 'hdc in 3rd ch from hook and in each ch across; ch 2 (does not count), turn <b>(90)</b>'),
    R('Row 2', 'hdc in each st across; FO and weave in ends <b>(90)</b>'),
    P('Try the scarf on the finished cow and add rows for a longer drape — or tie on a 40 cm ribbon. <b>Cord safety:</b> for babies and toddlers, skip the scarf and ribbon and make the Collar loop (9b) instead, or leave the neck bare. Never leave long free ends: many markets cap free cord length at about 20 cm — check your local toy rules.', BODY)]
S.append(KeepTogether(scarf))

collar = [P('9b &nbsp; Collar loop — Yarn D (the under-3 option)', H2),
    R('Ch', '26.'),
    R('Row 1', 'hdc in 3rd ch from hook and in each ch across; ch 2 (does not count), turn <b>(24)</b>'),
    R('Row 2', 'hdc in each st across; FO, leaving a 40 cm tail <b>(24)</b>'),
    P('Wrap the strip snugly around the neck join, ends butted, and whipstitch the two short ends together into a closed band. Sew both long edges flat to the neck, all the way round, so the band cannot be pulled off or lifted. Weave in all ends at least 5 cm.', BODY),
    P('<i>Fit:</i> 24 hdc is about 11–12 cm. If it is too tight or loose, add or remove 2 stitches at a time (chain count = stitches + 2). <b>This sizing has not been test-made: try the band on your finished cow and adjust before sewing it flat.</b>', BODY)]
S.append(CondPageBreak(120))
S.append(KeepTogether(collar))

# ---------- placement map ----------
def placement_map():
    d = Drawing(doc.width, 160)
    txt = colors.HexColor('#433026')
    def num(x, y, n):
        d.add(Circle(x, y, 7, strokeColor=GINGER, fillColor=colors.white, strokeWidth=1))
        d.add(String(x, y - 2.8, str(n), fontName='DVS-Bold', fontSize=7.5, fillColor=GINGER_D, textAnchor='middle'))
    # head (left)
    hx, hy, hr = 80, 92, 48
    d.add(Circle(hx, hy, hr, strokeColor=GINGER, fillColor=colors.white, strokeWidth=1.2))
    d.add(Ellipse(hx, hy - 18, 26, 13.5, strokeColor=GINGER, fillColor=OAT, strokeWidth=1))
    d.add(Circle(hx - 12, hy + 10, 4, strokeColor=None, fillColor=txt))
    d.add(Circle(hx + 12, hy + 10, 4, strokeColor=None, fillColor=txt))
    for i in range(-4, 5):
        x = hx + i * 7.5
        d.add(Line(x, hy + hr - 3, x, hy + 22, strokeColor=GINGER, strokeWidth=1.3))
    d.add(String(hx, 28, 'HEAD - front', fontName='DVS-Bold', fontSize=8, fillColor=GINGER_D, textAnchor='middle'))
    num(hx - 30, hy + 36, 1); num(hx + 30, hy + 36, 1)   # horns, both sides
    num(hx - 47, hy + 12, 2); num(hx + 47, hy + 12, 2)   # ears, both sides
    num(hx - 27, hy + 21, 3); num(hx + 27, hy + 21, 3)   # eyes
    num(hx, hy + 34, 4)        # fringe
    num(hx + 18, hy - 18, 5)   # muzzle
    # body (right)
    bx, by = 330, 96
    d.add(Ellipse(bx, by, 44, 50, strokeColor=GINGER, fillColor=colors.white, strokeWidth=1.2))
    d.add(Ellipse(bx, by - 2, 19, 27, strokeColor=GINGER, fillColor=OAT, strokeWidth=1))
    d.add(Circle(bx - 26, by - 58, 11, strokeColor=GINGER, fillColor=OAT, strokeWidth=1))
    d.add(Circle(bx + 26, by - 58, 11, strokeColor=GINGER, fillColor=OAT, strokeWidth=1))
    d.add(String(bx, 10, 'BODY - front', fontName='DVS-Bold', fontSize=8, fillColor=GINGER_D, textAnchor='middle'))
    num(bx + 16, by + 6, 6)    # belly patch
    num(bx - 26, by - 58, 7); num(bx + 26, by - 58, 7)   # front legs, both
    return d

# ---------- assembly ----------
S.append(Spacer(1, 8))
S.append(P('Assembly', TITLE))
S.append(P('Placement map (schematic)', H2))
S.append(placement_map())
S.append(P('<b>Key:</b> 1 Horns R6–R8 · 2 Ears R8–R10 · 3 Eyes R10/11 · 4 Fringe R6–R8 · 5 Muzzle R13–R16 · 6 Belly patch R10–R16 · 7 Front legs R9–R11 (Option B fronts R9–R12). Back legs sit on the rear flanks; the tail goes at centre back on R10. Positions count from the front-centre line: horns ~7 sts out, ears ~10 sts out, eyes 7 sts apart, and 8 body stitches sit between the front legs’ inner edges.', BODY))
steps = [
    '<b>Face first (head still open).</b> Sew the <b>muzzle</b> centred on the front-centre line over Head R13–R16. Then pin the <b>ears</b> (R8–R10, ~10 sts from centre) and <b>horns</b> (R6–R8, ~7 sts from centre, slightly toward the face); check the pairs mirror each other, then sew. Attach the <b>fringe</b> last and trim it clear of the eyes.',
    '<b>Head to body.</b> Align the 24 open stitches of Head R19 with the 24 of Body R21, face forward. Whipstitch all 24 matched pairs <b>twice</b> — head tail for one pass, body tail for the second — topping up neck stuffing before the final 3 pairs.',
    '<b>Front legs (lowest body rounds, just above the flat base).</b> Pin Standard fronts over <b>R9–R11</b> and the wider Option B shortened fronts over <b>R9–R12</b>, leaving <b>8 body stitches between the inner edges</b>. Angle forward so the hooves rest flat. Sew around the whole open rim twice — all <b>9 rim stitches</b> on Standard Legs, all <b>12</b> on Option B shortened fronts.',
    '<b>Back legs and tail.</b> Pin the back legs on the rear flanks at R9–R11, angled outward. In <b>Option A</b> (all legs equal) angle them so the back hooves sit wider than the front hooves; in <b>Option B</b> the longer back legs give the upright sit. Keep the centre-back stitch column free, then attach the <b>tail at centre back on Body R10</b> (Section 8) and braid it in 3 groups of 4.',
    '<b>Belly patch (optional).</b> Sew vertically to the centre front over Body <b>R10–R16</b>.',
    '<b>Scarf, ribbon or collar (optional).</b> Scarf or ribbon: tie on and adjust the fit. For any cow that may go to a child under 3, use only the Collar loop (9b) sewn flat on both edges, or nothing at all. Stitching a scarf at the neck alone still leaves dangling ends.',
]
for i, s in enumerate(steps, 1):
    S.append(KeepTogether(Paragraph(f'<b>{i}.</b>&nbsp;&nbsp;{s}', BULLET)))
S.append(P('Finishing checklist', H2))
for t in [
    'Every seam sewn <b>twice</b>; all ends woven in at least 5 cm and trimmed.',
    'Safety-eye washers locked and checked by hand (skip if embroidered).',
    'Fringe trimmed <b>clear of the eyes</b>; fringe and tail knots secure.',
    'No loose cords on under-3 makes: Collar loop (9b) sewn flat on both edges, or nothing.',
    'Hamish sits level, face centred, hooves flat.',
    'Brush the fringe gently with your fingers to separate the strands.',
]:
    S.append(B(t))
S.append(P('Care', H2))
S.append(P('Spot-clean with a damp cloth and reshape while drying. If washing is unavoidable, hand-wash cool, press water out in a towel, reshape and dry flat. Re-check all seams and eyes after washing.', BODY))
miy = [P('Make it yours', H2), B('<b>Colourways:</b> classic ginger, soft grey, cream or chocolate Highland — keep the muzzle and inner ears in a pale contrast.')]
miy.append(B('<b>Eyes:</b> embroidered sleeping eyes give a baby-gift look (and remove the plastic-eye hazard).'))
miy.append(B('<b>Finish:</b> crochet scarf or plaid ribbon (older children and display pieces only), or a tiny fabric bandana as in the concept images. For any cow that may go to a child under 3, use only the Collar loop (9b) sewn flat on both edges, or leave the neck bare.'))
S.append(KeepTogether(miy))
notes = Table([[''] for _ in range(4)], colWidths=[doc.width], rowHeights=[20]*4)
notes.setStyle(TableStyle([('LINEBELOW', (0,0), (-1,-2), 0.5, LINE), ('LEFTPADDING', (0,0), (-1,-1), 0), ('RIGHTPADDING', (0,0), (-1,-1), 0)]))
S.append(P('Your notes', H2))
S.append(notes)
S.append(Spacer(1, 6))
S.append(callout('Thank you for making Hamish!',
    'This is the <b>Corrected Edition (v6)</b> of design NS01: stitch counts, component openings, placements and print layout have been re-audited. <b>v6:</b> safety wording aligned, front-centre marking, layout fixes.<br/><br/>'
    'Finished-item photos may be shared with credit to <b>Novality Store</b>. This PDF is for personal use — please do not copy, share or resell the file. '
    'You may sell finished cows made from this pattern in small batches, crediting “Pattern by Novality Store”.<br/><br/>'
    'Stuck on a round, or think you have found an error? Message <b>Novality Store through the shop where you bought this pattern</b> (for example Etsy shop Messages), quoting the section and round number — corrections are issued as free updates to this file.'))
S.append(Spacer(1, 8))
S.append(P('© Novality Store · Hamish the Highland Cow · NS01 · Corrected Edition v6 · US terms · A4 file — on US Letter, print with “Fit to Page”.', SMALL))

doc.build(S, canvasmaker=EmbeddedCanvas)
print('built', OUT, OUT.stat().st_size, 'bytes')
