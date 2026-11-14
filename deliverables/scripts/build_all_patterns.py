#!/usr/bin/env python3
"""Build market PDFs for NS02-NS17 (NS01 already hand-built) from the
corrected Markdown sources, using the NS01 final design system:
Novality Crochet Studio as designer/publisher, Novality Store only for
seller contact, embedded fonts, wrapped tables, kept-together sections,
AI-generated concept-image captions, no printed edition/version strings.
Internal build marker lives only in PDF Subject metadata."""
import re
from pathlib import Path
from PIL import Image as PILImage
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.fonts import tt2ps
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas as _pdfcanvas
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, PageBreak, Table, TableStyle, Image as RLImage,
                                KeepTogether, NextPageTemplate, CondPageBreak)

ROOT = Path('/home/user/Crochet-Pattern-Checker')
SRC = ROOT / 'reviews' / 'user-supplied-v2'
OUTDIR = ROOT / 'deliverables'
SHOP = "Novality Store"             # the shop: where it is sold, support contact
BRAND = "Novality Crochet Studio"   # the subsidiary: designer / publisher
BUILD_TAG = 'internal build all-17 v1'

def spaced(s):
    return "  ".join(" ".join(w) for w in s.upper().split())

class EmbeddedCanvas(_pdfcanvas.Canvas):
    def __init__(self, *args, **kwargs):
        kwargs['initialFontName'] = 'DVS'
        kwargs.setdefault('initialFontSize', 9)
        super().__init__(*args, **kwargs)
    def setFont(self, name, size, leading=None):
        if name.startswith('Helvetica') or name.startswith('Times'):
            name = 'DVS-Bold' if 'Bold' in name else 'DVS'
        return super().setFont(name, size, leading)

FD = '/usr/share/fonts/truetype/dejavu/'
pdfmetrics.registerFont(TTFont('DVS', FD + 'DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DVS-Bold', FD + 'DejaVuSans-Bold.ttf'))
pdfmetrics.registerFont(TTFont('DVSerif', FD + 'DejaVuSerif.ttf'))
pdfmetrics.registerFontFamily('DVS', normal='DVS', bold='DVS-Bold', italic='DVS', boldItalic='DVS-Bold')

CREAM = colors.HexColor('#FAF5EC'); OAT = colors.HexColor('#EFE3CE')
GINGER = colors.HexColor('#A65A1E'); GINGER_D = colors.HexColor('#7E4212')
BROWN = colors.HexColor('#433026'); INK = colors.HexColor('#2E2620')
LINE = colors.HexColor('#D8C6A8'); FAINT = colors.HexColor('#6B5744')
PAGE_W, PAGE_H = A4

def st(name, **kw):
    base = dict(fontName='DVS', fontSize=9.2, leading=13, textColor=INK)
    base.update(kw); return ParagraphStyle(name, **base)

TITLE = st('title', fontName='DVS-Bold', fontSize=14.5, leading=17, textColor=GINGER_D, spaceBefore=8, spaceAfter=4)
H2 = st('h2', fontName='DVS-Bold', fontSize=11, leading=13.5, textColor=GINGER_D, spaceBefore=8, spaceAfter=3, keepWithNext=1)
H3 = st('h3', fontName='DVS-Bold', fontSize=9.8, leading=12.5, textColor=BROWN, spaceBefore=6, spaceAfter=2, keepWithNext=1)
BODY = st('body', spaceAfter=4)
NOTE = st('note', fontSize=8.8, leading=12.5, textColor=BROWN, spaceAfter=4)
BULLET = st('bullet', leftIndent=10, spaceAfter=2.5)
CAP = st('cap', fontSize=7.8, leading=10.5, textColor=FAINT, spaceBefore=2, spaceAfter=6)
SMALL = st('small', fontSize=6.8, leading=8.5, textColor=FAINT)
CELL = st('cell', fontSize=8.6, leading=11)
CELLF = st('cellf', fontName='DVS-Bold', fontSize=8.6, leading=11)
CELLH = st('cellh', fontName='DVS-Bold', fontSize=8.6, leading=11, textColor=colors.white)
CELLT = st('cellt', fontSize=7.6, leading=9.8)
CELLTH = st('cellth', fontName='DVS-Bold', fontSize=7.6, leading=9.8, textColor=colors.white)
LBL = st('lbl', fontName='DVS-Bold', fontSize=8.8, leading=11.5, textColor=BROWN)
ROW = st('row', fontSize=9.0, leading=12, textColor=INK)

def P(txt, style=BODY): return Paragraph(txt, style)
def B(txt): return Paragraph('&bull;&nbsp;&nbsp;' + txt, BULLET)

def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def md_inline(t):
    t = esc(t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'`([^`]+)`', r'\1', t)
    t = re.sub(r'(?<![\w*])\*([^*\n]+?)\*(?![\w*])', r'<i>\1</i>', t)
    return t

def data_table(rows, widths, header=True, first_bold=True, small=False, raw_html=False):
    cs, chs = (CELLT, CELLTH) if small else (CELL, CELLH)
    out = []
    for r, row in enumerate(rows):
        cells = []
        for c, val in enumerate(row):
            sty = chs if (header and r == 0) else (CELLF if (first_bold and c == 0 and not small) else cs)
            cells.append(Paragraph(str(val) if raw_html else md_inline(str(val)), sty))
        out.append(cells)
    t = Table(out, colWidths=widths, repeatRows=1 if header else 0)
    lr = 4 if small else 6
    style = [('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LEFTPADDING', (0, 0), (-1, -1), lr),
             ('RIGHTPADDING', (0, 0), (-1, -1), lr), ('TOPPADDING', (0, 0), (-1, -1), 4),
             ('BOTTOMPADDING', (0, 0), (-1, -1), 4), ('GRID', (0, 0), (-1, -1), 0.4, LINE),
             ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#FBF7EF')])]
    if header:
        style += [('BACKGROUND', (0, 0), (-1, 0), GINGER)]
    t.setStyle(TableStyle(style))
    return t

def round_row(label, text):
    t = Table([[Paragraph(md_inline(label), LBL), Paragraph(md_inline(text), ROW)]],
              colWidths=[21 * mm, None])
    t.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'),
                           ('LEFTPADDING', (0, 0), (-1, -1), 0), ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                           ('TOPPADDING', (0, 0), (-1, -1), 1.2), ('BOTTOMPADDING', (0, 0), (-1, -1), 1.2)]))
    return t

def callout(title, body):
    inner = [[Paragraph(f'<b>{title}</b>', st('ct', fontName='DVS-Bold', fontSize=9.2, leading=12, textColor=GINGER_D))],
             [Paragraph(body, st('cb', fontSize=8.8, leading=12.2, textColor=BROWN))]]
    t = Table(inner, colWidths=[None])
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), OAT), ('BOX', (0, 0), (-1, -1), 0.7, GINGER),
                           ('LEFTPADDING', (0, 0), (-1, -1), 8), ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                           ('TOPPADDING', (0, 0), (-1, -1), 6), ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                           ('ROUNDEDCORNERS', [3, 3, 3, 3])]))
    return t

def prep(src, dst, maxw=1400):
    im = PILImage.open(src).convert('RGB')
    im.thumbnail((maxw, maxw))
    im.save(dst, quality=88)
    return dst, im.size

# ---------------- Markdown -> flowables ----------------

def parse_pattern(md_text):
    lines = md_text.split('\n')
    title_line = next(l for l in lines if l.startswith('# '))[2:].strip()
    title_line = re.sub(r'\s*\(Corrected\)\s*$', '', title_line)
    m = re.match(r'^(.*?)\s*—\s*(NS\d+)$', title_line)
    name, code = (m.group(1).strip(), m.group(2)) if m else (title_line, '')
    flow = []          # body flowables after meta
    meta = []          # (label, value_html_parts)
    in_meta = True
    para_buf = []

    def flush_para():
        if para_buf:
            flow.append(P(md_inline(' '.join(para_buf)), BODY))
            para_buf.clear()

    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        i += 1
        if line.startswith('# '):
            continue
        if re.match(r'^---+$', line.strip()):
            flush_para()
            if in_meta:
                in_meta = False
            flow.append(Spacer(1, 3))
            continue
        if line.startswith('>'):
            flush_para()
            q = [line.lstrip('> ').strip()]
            while i < len(lines) and lines[i].startswith('>'):
                q.append(lines[i].lstrip('> ').strip()); i += 1
            txt = ' '.join(q)
            if re.match(r'\*\*Corrections?\b', txt):
                continue  # internal audit note — not buyer content
            txt = re.sub(r'^\*\*Safety:\*\*\s*', '', txt)
            flow.append(callout('Safety — read first.', md_inline(txt)))
            flow.append(Spacer(1, 4))
            in_meta = False
            continue
        if line.startswith('|') and '|' in line[1:]:
            flush_para()
            rows = []
            while i - 1 < len(lines) and lines[i - 1].startswith('|'):
                cells = [c.strip() for c in lines[i - 1].strip().strip('|').split('|')]
                if not all(re.match(r'^:?-{2,}:?$', c) for c in cells if c != ''):
                    rows.append(cells)
                if i < len(lines) and lines[i].startswith('|'):
                    i += 1
                else:
                    break
            if rows:
                ncol = max(len(r) for r in rows)
                rows = [r + [''] * (ncol - len(r)) for r in rows]
                weights = []
                for c in range(ncol):
                    weights.append(min(60, max(8, max(len(r[c]) for r in rows))))
                total = sum(weights)
                docw = 174 * mm
                widths = [max(docw * w / total, 15 * mm) for w in weights]
                scale = docw / sum(widths)
                widths = [w * scale for w in widths]
                flow.append(data_table(rows, widths, header=True, first_bold=False, small=(ncol >= 4)))
                flow.append(Spacer(1, 4))
            in_meta = False
            continue
        hm = re.match(r'^(#{2,4})\s+(.+)$', line)
        if hm:
            flush_para()
            in_meta = False
            level, txt = len(hm.group(1)), md_inline(hm.group(2))
            if level <= 3:
                flow.append(CondPageBreak(90))
                flow.append(P(txt, H2))
            else:
                flow.append(P(txt, H3))
            continue
        bm = re.match(r'^(\s*)\*\s+(.+)$', line)
        if bm:
            indent, content = len(bm.group(1)), bm.group(2)
            if in_meta:
                mm_ = re.match(r'^\*\*(.+?):\*\*\s*(.*)$', content)
                if mm_ and indent == 0:
                    meta.append([mm_.group(1), [mm_.group(2)]])
                elif meta:
                    meta[-1][1].append(content)
                continue
            flush_para()
            lm = re.match(r'^\*\*(.+?):\*\*\s*(.*)$', content)
            full_it = re.match(r'^\*([^*].*)\*$', content)
            if lm and len(lm.group(1)) <= 34:
                flow.append(round_row(lm.group(1) + ':', lm.group(2)))
            elif full_it:
                flow.append(P(md_inline(content), NOTE))
            else:
                sty = ParagraphStyle('sub', parent=BULLET, leftIndent=22) if indent else BULLET
                flow.append(Paragraph('&bull;&nbsp;&nbsp;' + md_inline(content), sty))
            continue
        nm = re.match(r'^(\d+)\.\s+(.+)$', line)
        if nm:
            flush_para()
            in_meta = False
            flow.append(KeepTogether(Paragraph(f'<b>{nm.group(1)}.</b>&nbsp;&nbsp;' + md_inline(nm.group(2)), BULLET)))
            continue
        if line.strip() == '':
            flush_para()
            continue
        in_meta = False if para_buf or flow else in_meta
        para_buf.append(line.strip())
    flush_para()
    return name, code, meta, flow

def meta_value(meta, key_start):
    for label, parts in meta:
        if label.lower().startswith(key_start):
            return ' '.join(parts)
    return ''

def build(code):
    md = (SRC / f'{code}_corrected.md').read_text()
    name, pcode, meta, flow = parse_pattern(md)
    code = pcode or code
    low = code.lower()
    adir = ROOT / 'assets' / 'patterns' / low
    cover_file = next(p for p in sorted(adir.iterdir()) if 'cover' in p.name and p.suffix.lower() in ('.png', '.jpg', '.jpeg'))
    map_file = next((p for p in sorted(adir.iterdir()) if 'maker_map' in p.name), None)
    cover_jpg, cover_size = prep(cover_file, f'/tmp/{low}_cover.jpg')
    main = name
    sub = ''
    if '(' in name:
        main, sub = name.split('(', 1)
        main = main.strip(); sub = sub.rstrip(')').strip()
    terms_raw = meta_value(meta, 'terminology')
    terms_badge = 'DUAL US & UK' if 'dual' in terms_raw.lower() else 'US TERMS'
    terms_line = 'Dual US & UK terms' if 'dual' in terms_raw.lower() else 'US terms'
    skill = meta_value(meta, 'skill')
    skill_badge = re.split(r'\s+\(|\s+—', skill)[0].strip().upper() or 'CROCHET'
    badges = [skill_badge, terms_badge, f'CODE {code}']
    slug = re.sub(r'[^A-Za-z0-9]+', '_', main).strip('_')
    out_path = OUTDIR / f'{code}_{slug}_Pattern.pdf'

    def on_cover(canv, doc):
        canv.saveState()
        canv.setFillColor(CREAM); canv.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
        canv.setFillColor(GINGER_D); canv.setFont('DVS-Bold', 10)
        canv.drawCentredString(PAGE_W / 2, PAGE_H - 40, spaced(BRAND))
        iw_px, ih_px = cover_size
        box_w, box_h = 430, 430
        w = box_w; h = w * ih_px / iw_px
        if h > box_h:
            h = box_h; w = h * iw_px / ih_px
        ix = (PAGE_W - w) / 2; iy = PAGE_H - 58 - h
        canv.setFillColor(GINGER); canv.roundRect(ix - 7, iy - 7, w + 14, h + 14, 6, stroke=0, fill=1)
        canv.setFillColor(colors.white); canv.roundRect(ix - 3.5, iy - 3.5, w + 7, h + 7, 4, stroke=0, fill=1)
        canv.drawImage(cover_jpg, ix, iy, width=w, height=h)
        cy = iy - 42
        size = 27
        while stringWidth(main, 'DVS-Bold', size) > 500 and size > 14:
            size -= 1.5
        canv.setFillColor(BROWN); canv.setFont('DVS-Bold', size)
        canv.drawCentredString(PAGE_W / 2, cy, main)
        if sub:
            cy -= 22
            canv.setFont('DVS', 13); canv.drawCentredString(PAGE_W / 2, cy, f'({sub})')
        cy -= 20
        canv.setFillColor(GINGER_D); canv.setFont('DVSerif', 10.5)
        canv.drawCentredString(PAGE_W / 2, cy, 'Crochet Pattern')
        cy -= 26
        widths = [stringWidth(b, 'DVS-Bold', 7.2) + 18 for b in badges]
        x = (PAGE_W - sum(widths) - 9 * (len(widths) - 1)) / 2
        for btext, bw in zip(badges, widths):
            canv.setStrokeColor(GINGER); canv.setFillColor(colors.white)
            canv.roundRect(x, cy - 4, bw, 16, 8, stroke=1, fill=1)
            canv.setFillColor(GINGER_D); canv.setFont('DVS-Bold', 7.2)
            canv.drawCentredString(x + bw / 2, cy + 1.2, btext)
            x += bw + 9
        canv.setFillColor(FAINT); canv.setFont('DVS', 7.6)
        canv.drawCentredString(PAGE_W / 2, 100, 'Concept image (AI-generated, not a photograph of a finished sample), shown for colour and character.')
        canv.drawCentredString(PAGE_W / 2, 88, 'Follow the written instructions where they differ from the image.')
        canv.setFont('DVS', 8.2)
        canv.drawCentredString(PAGE_W / 2, 56, 'PDF pattern — this is not a finished toy')
        canv.setFont('DVS', 7.8)
        canv.drawCentredString(PAGE_W / 2, 42, f'© {BRAND}, a {SHOP} brand · Design code {code} · Please do not share or resell this file')
        canv.restoreState()

    def on_page(canv, doc):
        canv.saveState()
        canv.setStrokeColor(LINE); canv.setLineWidth(0.6)
        canv.line(18 * mm, PAGE_H - 13 * mm, PAGE_W - 18 * mm, PAGE_H - 13 * mm)
        canv.setFillColor(GINGER_D); canv.setFont('DVS-Bold', 7.2)
        canv.drawString(18 * mm, PAGE_H - 11 * mm, f'{main.upper()} — {code}')
        canv.setFillColor(FAINT); canv.setFont('DVS', 7.2)
        canv.drawRightString(PAGE_W - 18 * mm, PAGE_H - 11 * mm, BRAND.upper())
        canv.setStrokeColor(LINE); canv.line(18 * mm, 13 * mm, PAGE_W - 18 * mm, 13 * mm)
        canv.setFont('DVS', 7.2)
        canv.drawString(18 * mm, 9.5 * mm, f'© {BRAND} — personal use; finished items may be sold in small batches with credit.')
        canv.drawRightString(PAGE_W - 18 * mm, 9.5 * mm, f'Page {doc.page}')
        canv.restoreState()

    doc = BaseDocTemplate(str(out_path), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm,
                          topMargin=18 * mm, bottomMargin=16 * mm,
                          title=f'{name} — Crochet Pattern {code}', author=BRAND, subject=BUILD_TAG)
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='main')
    doc.addPageTemplates([PageTemplate(id='cover', frames=[frame], onPage=on_cover),
                          PageTemplate(id='page', frames=[frame], onPage=on_page)])

    S = [Spacer(1, PAGE_H - 40 * mm), NextPageTemplate('page'), PageBreak()]
    S.append(P(main + (f' ({sub})' if sub else ''), TITLE))
    S.append(P('At a glance', H2))
    glance_rows = [[label, '<br/>'.join(md_inline(p) for p in parts if p)] for label, parts in meta]
    S.append(data_table(glance_rows, [38 * mm, doc.width - 38 * mm], header=False, raw_html=True))
    S.append(Spacer(1, 4))
    S.extend(flow)
    if map_file:
        map_jpg, map_size = prep(map_file, f'/tmp/{low}_map.jpg')
        mw = doc.width; mh = mw * map_size[1] / map_size[0]
        if mh > 155 * mm:
            mh = 155 * mm; mw = mh * map_size[0] / map_size[1]
        img = RLImage(map_jpg, width=mw, height=mh); img.hAlign = 'CENTER'
        S.append(CondPageBreak(120))
        S.append(P('Maker map', H2))
        S.append(img)
        S.append(P('Maker map (concept graphic, AI-generated) — use it for orientation; the written instructions in this pattern control.', CAP))
    S.append(Spacer(1, 6))
    closing = [callout('Thank you for making ' + main.split(' the ')[0] + '!',
        f'Finished-item photos may be shared with credit to <b>{BRAND}</b>. This PDF is for personal use — please do not copy, share or resell the file. '
        f'You may sell finished items made from this pattern in small batches, crediting “Pattern by {BRAND}”.<br/><br/>'
        f'Stuck on a round, or think you have found an error? Message <b>{SHOP}</b> — the shop where you bought this pattern (for example via Etsy Messages) — quoting the section and round number. Corrections are issued as free updates to this file.'),
        Spacer(1, 8),
        P(f'© {BRAND}, a {SHOP} brand · {main} · {code} · {terms_line} · A4 file — on US Letter, print with “Fit to Page”.', SMALL)]
    S.append(KeepTogether(closing))
    doc.build(S, canvasmaker=EmbeddedCanvas)
    return out_path

if __name__ == '__main__':
    import sys
    codes = sys.argv[1:] or [f'NS{i:02d}' for i in range(2, 18)]
    for c in codes:
        p = build(c)
        print('built', p.name, p.stat().st_size, 'bytes')
