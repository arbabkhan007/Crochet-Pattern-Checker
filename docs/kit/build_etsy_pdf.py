"""Novality Store — Etsy packaging builder (colour + printer-saver editions).

Implements the Etsy File Packaging Strategy for a single pattern:

    Page 1   retail cover: studio ribbon, title block, hero frame, 4-pill spec bar
    Page 2   materials (with colour dots) + abbreviations | gauge box + true 1:1
             50 mm ruler + techniques, safety callout across the foot
    Pages 3+ instructions as component cards (short cards never split)
    Last     numbered assembly with circular badges, troubleshooting grid,
             care / colorways / terms in a three-column footer grid, single
             copyright line in the running footer

Usage:
    python3 docs/kit/build_etsy_pdf.py --edition colour
    python3 docs/kit/build_etsy_pdf.py --edition print

The HTML/CSS pipeline in the packaging brief needs headless Chromium (Playwright)
or WeasyPrint; neither is available in this sandbox (no browser, no Pango/Cairo),
so the same page architecture is drawn directly with reportlab.  The stylesheet
in docs/kit/novality-pattern.css is kept for the HTML route.
"""
from __future__ import annotations

import argparse
import io
import os
import re
from pathlib import Path

from reportlab.lib.colors import Color, HexColor, white
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, CondPageBreak, Flowable, Frame,
                                Image as RLImage,
                                Image, KeepTogether, PageBreak, PageTemplate,
                                Paragraph, Spacer, Table, TableStyle)

ROOT = Path(__file__).resolve().parents[2]
FONTS = Path("/usr/share/fonts/truetype/dejavu")

pdfmetrics.registerFont(TTFont("Sans", FONTS / "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("Sans-B", FONTS / "DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Serif", FONTS / "DejaVuSerif.ttf"))
pdfmetrics.registerFont(TTFont("Serif-B", FONTS / "DejaVuSerif-Bold.ttf"))
registerFontFamily("Sans", normal="Sans", bold="Sans-B", italic="Sans", boldItalic="Sans-B")
registerFontFamily("Serif", normal="Serif", bold="Serif-B", italic="Serif", boldItalic="Serif-B")

W, H = A4
M_TOP, M_SIDE, M_BOT = 16 * mm, 15 * mm, 18 * mm
CW = W - 2 * M_SIDE

COLOUR = dict(
    page="#FAF7F2", card="#FFFFFF", head="#4A3728", head_text="#FFFFFF",
    alt="#F6F1EA", pause="#FFF4E5", pause_border="#D97706", text="#231F1C",
    muted="#655B53", accent="#8C4A27", soft="#EFE6DC", border="#DFD5C8",
)
PRINT = dict(
    page="#FFFFFF", card="#FFFFFF", head="#F2F2F2", head_text="#111111",
    alt="#FAFAFA", pause="#F5F5F5", pause_border="#111111", text="#000000",
    muted="#333333", accent="#000000", soft="#F0F0F0", border="#999999",
)

SPEC = dict(
    code="NS-13",
    title="Christmas Ornament Bundle",
    pitch="Bauble, star and snowflake: three quick hanging ornaments from leftover DK.",
    md="docs/ns13/NS13_corrected.md",
    hero="docs/ns13/assets/ornament_hero.png",
    hero_bw="docs/ns13/assets/ornament_hero.bw.png",
    skill="Beginner",
    active="15-40 min per piece",
    size="2.6 cm bauble · 6 cm star · 6 cm flake",
    yarn="DK #3 · 3.5 mm (US E/4)",
    swatches=[("RED", "#B33A3A"), ("WHITE", "#FFFFFF"), ("GREEN", "#2F6B4F"),
              ("GOLD", "#D9A441"), ("BLUE", "#7FA8C9"), ("SILVER", "#C0C0C8")],
)

P = COLOUR  # replaced per edition at build time

PRINT_GREY = {"RED": "#333333", "WHITE": "#D8D8D8", "GREEN": "#555555",
              "GOLD": "#8A8A8A", "BLUE": "#A6A6A6", "SILVER": "#C4C4C4"}


def swatch_colour(name, hexv):
    """Ink-saving greys for the print edition, real shades for the colour one."""
    return hexv if P is COLOUR else PRINT_GREY.get(name, "#777777")


def c(key):
    return HexColor(P[key])


# ---------------------------------------------------------------- markdown
def parse_md(text):
    """Return [(kind, payload)] with kind in h2/h3/p/bullet/num/table."""
    blocks, tbl = [], []

    def flush():
        nonlocal tbl
        rows = [r for r in tbl if not all(set(x) <= set("-: ") for x in r)]
        if len(rows) >= 2:
            blocks.append(("table", rows))
        tbl = []

    for raw in text.splitlines():
        s = raw.strip()
        if s.startswith("|"):
            tbl.append([x.strip() for x in s.strip("|").split("|")])
            continue
        if not s:
            continue
        flush()
        if s.startswith("# "):
            continue
        if s.startswith("### "):
            blocks.append(("h3", s[4:]))
        elif s.startswith("## "):
            blocks.append(("h2", s[3:]))
        elif s.startswith("> "):
            continue
        elif re.match(r"^[-*]\s+", s):
            blocks.append(("bullet", re.sub(r"^[-*]\s+", "", s)))
        elif re.match(r"^\d+\.\s+", s):
            m = re.match(r"^(\d+)\.\s+(.*)$", s)
            blocks.append(("num", (m.group(1), m.group(2))))
        else:
            blocks.append(("p", s))
    flush()
    return blocks


def sections(blocks):
    out, cur = {}, None
    for kind, payload in blocks:
        if kind == "h2":
            cur = payload
            out[cur] = []
        elif cur:
            out[cur].append((kind, payload))
    return out


def md(s):
    """Minimal inline markdown -> reportlab markup."""
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    s = s.replace(" - ", " \u2013 ")
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<i>\1</i>", s)
    return s


# ---------------------------------------------------------------- styles
def styles():
    return {
        "ribbon": ParagraphStyle("ribbon", fontName="Sans-B", fontSize=7.6, leading=10,
                                 textColor=c("muted")),
        "h1": ParagraphStyle("h1", fontName="Serif-B", fontSize=28, leading=32,
                             textColor=c("text"), spaceAfter=4),
        "pitch": ParagraphStyle("pitch", fontName="Sans", fontSize=11, leading=15,
                                textColor=c("muted")),
        "h2": ParagraphStyle("h2", fontName="Serif-B", fontSize=13, leading=16,
                             textColor=c("text"), spaceBefore=2, spaceAfter=4),
        "h3": ParagraphStyle("h3", fontName="Sans-B", fontSize=10.5, leading=13,
                             textColor=c("accent"), spaceBefore=2, spaceAfter=3),
        "body": ParagraphStyle("body", fontName="Sans", fontSize=9.2, leading=12.6,
                               textColor=c("text")),
        "small": ParagraphStyle("small", fontName="Sans", fontSize=7.8, leading=10.4,
                                textColor=c("muted")),
        "bullet": ParagraphStyle("bullet", fontName="Sans", fontSize=9.0, leading=12.2,
                                 textColor=c("text"), leftIndent=10, bulletIndent=0),
        "cell": ParagraphStyle("cell", fontName="Sans", fontSize=8.4, leading=11.0,
                               textColor=c("text")),
        "cellb": ParagraphStyle("cellb", fontName="Sans-B", fontSize=8.4, leading=11.0,
                                textColor=c("text")),
        "cellc": ParagraphStyle("cellc", fontName="Sans-B", fontSize=8.4, leading=11.0,
                                textColor=c("text"), alignment=TA_CENTER),
        "head": ParagraphStyle("head", fontName="Sans-B", fontSize=7.8, leading=10,
                               textColor=c("head_text")),
        "headc": ParagraphStyle("headc", fontName="Sans-B", fontSize=7.8, leading=10,
                                textColor=c("head_text"), alignment=TA_CENTER),
    }


# ---------------------------------------------------------------- flowables
class Rule(Flowable):
    def __init__(self, width, thickness=1.5, colour=None, space=4):
        super().__init__()
        self.width, self.thickness, self.space = width, thickness, space
        self.colour = colour or c("accent")
        self.height = thickness + space

    def draw(self):
        self.canv.setStrokeColor(self.colour)
        self.canv.setLineWidth(self.thickness)
        self.canv.line(0, self.space, self.width, self.space)


class RoundedImage(Flowable):
    """Aspect-locked photo in a rounded frame (the cover hero)."""

    def __init__(self, path, width, ratio=4 / 3, radius=12):
        super().__init__()
        self.path, self.width, self.radius = path, width, radius
        self.height = width / ratio

    def draw(self):
        from PIL import Image as PILImage, ImageOps

        im = PILImage.open(self.path).convert("RGB")
        target = 4 / 3
        w, h = im.size
        if w / h > target:                       # too wide -> crop sides
            new_w = int(h * target)
            im = im.crop(((w - new_w) // 2, 0, (w + new_w) // 2, h))
        elif w / h < target:                     # too tall -> crop top/bottom
            new_h = int(w / target)
            im = im.crop((0, (h - new_h) // 2, w, (h + new_h) // 2))
        buf = io.BytesIO()
        im.save(buf, format="PNG")
        buf.seek(0)
        p = self.canv.beginPath()
        p.roundRect(0, 0, self.width, self.height, self.radius)
        self.canv.saveState()
        self.canv.clipPath(p, stroke=0, fill=0)
        RLImage(buf, width=self.width, height=self.height).drawOn(self.canv, 0, 0)
        self.canv.restoreState()
        self.canv.setStrokeColor(c("border"))
        self.canv.setLineWidth(1)
        self.canv.roundRect(0, 0, self.width, self.height, self.radius, stroke=1, fill=0)


class TickBox(Flowable):
    def __init__(self, size=8):
        super().__init__()
        self.width = self.height = size

    def draw(self):
        self.canv.setStrokeColor(c("muted"))
        self.canv.setLineWidth(1.0)
        self.canv.roundRect(0, 0, self.width, self.height, 1.5, stroke=1, fill=0)


class GaugeRuler(Flowable):
    """True 1:1 50 mm bar, printed at actual size."""

    def __init__(self):
        super().__init__()
        self.width = 50 * mm
        self.height = 26

    def draw(self):
        cv = self.canv
        cv.setStrokeColor(c("text"))
        cv.setFillColor(white)
        cv.setLineWidth(1.4)
        cv.rect(0, 8, self.width, 14, stroke=1, fill=1)
        cv.setFillColor(c("text"))
        cv.setFont("Sans-B", 6.5)
        for i in range(0, 51, 5):
            x = i * mm
            h = 7 if i % 10 == 0 else 4
            cv.setLineWidth(0.8)
            cv.line(x, 8, x, 8 + h)
            if i % 10 == 0:
                cv.drawCentredString(x, 0, str(i // 10))
        cv.setFont("Sans", 6.5)
        cv.setFillColor(c("muted"))
        cv.drawRightString(self.width, 0, "cm")


class Badge(Flowable):
    """Circular numbered step badge."""

    def __init__(self, n, d=13):
        super().__init__()
        self.n, self.width, self.height = n, d, d

    def draw(self):
        cv = self.canv
        cv.setFillColor(c("accent"))
        cv.setStrokeColor(c("accent"))
        cv.circle(self.width / 2, self.height / 2, self.width / 2 - 0.5, stroke=0, fill=1)
        cv.setFillColor(white)
        cv.setFont("Sans-B", 7.5)
        cv.drawCentredString(self.width / 2, self.height / 2 - 2.6, str(self.n))


# ---------------------------------------------------------------- tables
def stitch_table(rows, S, tick=False):
    hdr = rows[0]
    body = rows[1:]
    hdr = [h for h in hdr]
    if tick:
        hdr = ["✓"] + hdr
    ncol = len(hdr)
    if ncol >= 6:                                    # check | Rnd | US | UK | Sts | Note
        widths = [0.05, 0.09, 0.30, 0.30, 0.09, 0.17]
    elif ncol == 5:                                  # Rnd | US | UK | Sts | Note
        widths = [0.10, 0.32, 0.32, 0.09, 0.17]
    else:                                            # Rnd | Instruction | Sts | Note
        widths = [0.12, 0.52, 0.10, 0.26]
    if tick and ncol == 5:
        widths = [0.05, 0.10, 0.29, 0.29, 0.09, 0.18]
    widths = [w * CW for w in widths]

    data = [[Paragraph(md(h), S["headc"] if (tick and i == 0) or h.lower() == "sts" else S["head"])
             for i, h in enumerate(hdr)]]
    style = [("BACKGROUND", (0, 0), (-1, 0), c("head")),
             ("GRID", (0, 0), (-1, -1), 0.5, c("border")),
             ("VALIGN", (0, 0), (-1, -1), "TOP"),
             ("TOPPADDING", (0, 0), (-1, -1), 2.6),
             ("BOTTOMPADDING", (0, 0), (-1, -1), 2.6),
             ("LEFTPADDING", (0, 0), (-1, -1), 4),
             ("RIGHTPADDING", (0, 0), (-1, -1), 4)]
    for i, r in enumerate(body, start=1):
        r = [x for x in r]
        note = r[-1].lower() if r else ""
        critical = any(k in note for k in ("start stuffing", "stuff firm", "pause", "leave open", "lock"))
        cells = []
        if tick:
            cells.append(TickBox())
        cells.append(Paragraph(md(r[0]), S["cellb"]))
        cells.append(Paragraph(md(r[1]), S["cell"]))
        if ncol - len(cells) > 1:
            cells.append(Paragraph(md(r[2]), S["cell"]))
        cells.append(Paragraph(md(r[-2]), S["cellc"]))
        cells.append(Paragraph(md(r[-1]), S["cell"]))
        cells = cells[:ncol]
        data.append(cells)
        if critical:
            style.append(("BACKGROUND", (0, i), (-1, i), c("pause")))
            style.append(("LINEBEFORE", (0, i), (0, i), 2.5, c("pause_border")))
        elif i % 2 == 0:
            style.append(("BACKGROUND", (0, i), (-1, i), c("alt")))
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle(style))
    return t


def kv_table(rows, S, widths, header=("Item", "Detail")):
    data = [[Paragraph(md(header[0]), S["head"]), Paragraph(md(header[1]), S["head"])]]
    style = [("BACKGROUND", (0, 0), (-1, 0), c("head")),
             ("GRID", (0, 0), (-1, -1), 0.5, c("border")),
             ("VALIGN", (0, 0), (-1, -1), "TOP"),
             ("TOPPADDING", (0, 0), (-1, -1), 3),
             ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]
    for i, (a, b, *rest) in enumerate(rows, start=1):
        dot = rest[0] if rest else None
        if dot is True:                                  # pre-rendered markup cell
            left, right = Paragraph(a, S["cellb"]), Paragraph(b, S["cell"])
        elif dot:
            left = Paragraph(f'<font color="{dot}">&#9632;</font>&nbsp; {md(a)}', S["cellb"])
            right = Paragraph(md(b), S["cell"])
        else:
            left, right = Paragraph(md(a), S["cellb"]), Paragraph(md(b), S["cell"])
        data.append([left, right])
        if i % 2 == 0:
            style.append(("BACKGROUND", (0, i), (-1, i), c("alt")))
    t = Table(data, colWidths=widths)
    t.setStyle(TableStyle(style))
    return t


def card(content, pad=8):
    t = Table([[content]], colWidths=[CW])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), c("card")),
                           ("BOX", (0, 0), (-1, -1), 0.7, c("border")),
                           ("LEFTPADDING", (0, 0), (-1, -1), pad),
                           ("RIGHTPADDING", (0, 0), (-1, -1), pad),
                           ("TOPPADDING", (0, 0), (-1, -1), pad),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), pad)]))
    return t


def callout(title, body, S, accent=None):
    accent = accent or c("pause_border")
    inner = [Paragraph(f"<b>{md(title)}</b>", S["h3"]), Paragraph(md(body), S["small"])]
    t = Table([[inner]], colWidths=[CW])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), c("soft")),
                           ("LINEBEFORE", (0, 0), (0, -1), 3.2, accent),
                           ("LEFTPADDING", (0, 0), (-1, -1), 9),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                           ("TOPPADDING", (0, 0), (-1, -1), 7),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 7)]))
    return t


def pills(S):
    items = [("SKILL LEVEL", SPEC["skill"]), ("ACTIVE TIME", SPEC["active"]),
             ("FINISHED SIZE", SPEC["size"]), ("YARN & HOOK", SPEC["yarn"])]
    cells = []
    for k, v in items:
        cells.append([Paragraph(k, ParagraphStyle("pk", fontName="Sans-B", fontSize=6.4,
                                                  leading=8.4, textColor=c("muted"))),
                      Paragraph(md(v), ParagraphStyle("pv", fontName="Sans-B", fontSize=8.6,
                                                      leading=11, textColor=c("text")))])
    t = Table([cells], colWidths=[CW / 4] * 4)
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                           ("BACKGROUND", (0, 0), (-1, -1), c("card")),
                           ("BOX", (0, 0), (-1, -1), 0.7, c("border")),
                           ("INNERGRID", (0, 0), (-1, -1), 0.7, c("border")),
                           ("LEFTPADDING", (0, 0), (-1, -1), 7),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                           ("TOPPADDING", (0, 0), (-1, -1), 6),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    return t



def glance_block(sec, S):
    """Time / yarn table from the master's 'Bundle at a glance' table."""
    tips = sec.get("Helpful tips", [])
    g = next((pl for k, pl in tips if k == "table"), None)
    if not g:
        return []
    rows = [[Paragraph("<b>%s</b>" % md(x), S["cell"])
             for x in g[0]]]
    for r in g[1:]:
        rows.append([Paragraph("<b>%s</b>" % md(r[0]), S["cellb"])] +
                    [Paragraph(md(x), S["cell"]) for x in r[1:]])
    widths = [CW * 0.22, CW * 0.20, CW * 0.20, CW * 0.38]
    t = Table(rows, colWidths=widths[:len(rows[0])], repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), c("soft")),
                           ("BOX", (0, 0), (-1, -1), 0.7, c("border")),
                           ("INNERGRID", (0, 0), (-1, -1), 0.4, c("border")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("TOPPADDING", (0, 0), (-1, -1), 4),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                           ("LEFTPADDING", (0, 0), (-1, -1), 6),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 6)]))
    return [Paragraph("Bundle at a glance", S["h2"]), t,
            Paragraph("Times are working time per piece and exclude blocking, which dries "
                      "overnight. All three string neatly on one length of yarn \u2014 a matching "
                      "garland is just all three patterns on repeat.", S["small"]), Spacer(1, 10)]

FRAME_H = 745.5


def flex(story, start, width, tail, frame_h=FRAME_H, gap=12):
    """Spacer that pins the tail block to the foot of the page."""
    def h(f):
        try:
            return f.wrap(width, frame_h)[1]
        except Exception:
            return 0.0
    used = sum(h(f) for f in story[start:])
    tail_h = sum(h(f) for f in tail)
    return Spacer(1, max(6, frame_h - used - tail_h - gap))


# ---------------------------------------------------------------- document
class Doc(BaseDocTemplate):
    def __init__(self, target, edition, **kw):
        super().__init__(str(target), pagesize=A4,
                         leftMargin=M_SIDE, rightMargin=M_SIDE,
                         topMargin=M_TOP, bottomMargin=M_BOT,
                         title=f"{SPEC['code']} {SPEC['title']}",
                         author="Novality Store",
                         subject="Crochet pattern",
                         creator="Novality Store build pipeline", **kw)
        self.edition = edition
        self.total_pages = 0
        frame = Frame(M_SIDE, M_BOT, CW, H - M_TOP - M_BOT, id="main",
                      leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates([PageTemplate(id="page", frames=[frame],
                                            onPage=self.furniture)])

    def furniture(self, cv, doc):
        pg = doc.page
        cv.saveState()
        if pg > 1:
            cv.setFont("Sans-B", 7.4)
            cv.setFillColor(c("muted"))
            cv.drawString(M_SIDE, H - 26, f"{SPEC['code']}  ·  {SPEC['title'].upper()}")
            cv.setFont("Sans-B", 7.4)
            cv.drawRightString(W - M_SIDE, H - 26, "NOVALITY STORE")
            cv.setStrokeColor(c("border"))
            cv.setLineWidth(0.6)
            cv.line(M_SIDE, H - 30, W - M_SIDE, H - 30)
        cv.setStrokeColor(c("border"))
        cv.setLineWidth(0.6)
        cv.line(M_SIDE, 30, W - M_SIDE, 30)
        cv.setFont("Sans", 7)
        cv.setFillColor(c("muted"))
        cv.drawString(M_SIDE, 19, "© 2026 Novality Store · Personal & small-batch handmade license")
        cv.setFont("Sans-B", 8)
        cv.setFillColor(c("text"))
        cv.drawRightString(W - M_SIDE, 19, f"Page {pg} of {doc.total_pages}")
        cv.restoreState()

    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph):
            style = flowable.style.name
            if style in ("h2", "h3"):
                key = f"bm{self.page}_{id(flowable)}"
                self.canv.bookmarkPage(key)
                level = 0 if style == "h2" else 1
                text = re.sub(r"<[^>]+>", "", flowable.getPlainText())
                self.canv.addOutlineEntry(text, key, level=level, closed=False)


def retoc(path):
    """Curated bookmark tree (headings nested in table cells are not seen by afterFlowable)."""
    import pymupdf
    want = [("Cover", None),
            ("Materials, gauge & abbreviations", "Materials & tools"),
            ("Instructions", "Instructions"),
            ("Finishing & assembly", "Finishing & assembly"),
            ("Troubleshooting", "Troubleshooting"),
            ("Care, colorways & terms", "Care & washing")]
    d = pymupdf.open(str(path))
    toc = []
    for title, anchor in want:
        page = 1
        if anchor:
            page = next((i + 1 for i, pg in enumerate(d) if anchor in pg.get_text()), 1)
        toc.append([1, title, page])
    d.set_toc(toc)
    tmp = path.with_suffix(".retoc.pdf")
    d.save(str(tmp), garbage=3, deflate=True)
    d.close()
    tmp.replace(path)


def build(edition: str, out: Path) -> int:
    global P
    P = COLOUR if edition == "colour" else PRINT
    S = styles()
    tick = edition == "print"
    text = (ROOT / SPEC["md"]).read_text(encoding="utf-8")
    blocks = parse_md(text)
    sec = sections(blocks)

    def paras(items):
        out = []
        for kind, payload in items:
            if kind == "p":
                out.append(Paragraph(md(payload), S["body"]))
                out.append(Spacer(1, 4))
            elif kind == "bullet":
                out.append(Paragraph("•&nbsp; " + md(payload), S["bullet"]))
                out.append(Spacer(1, 3))
            elif kind == "num":
                n, t = payload
                out.append(Paragraph(f"<b>{n}.</b>&nbsp; {md(t)}", S["bullet"]))
                out.append(Spacer(1, 3))
            elif kind == "table":
                out.append(stitch_table(payload, S, tick))
                out.append(Spacer(1, 5))
        return out

    story = []

    # ---------------- page 1: cover
    tag = ParagraphStyle("tag", parent=S["ribbon"], fontSize=7.4, textColor=c("accent"))
    head = [Paragraph(f"NOVALITY STORE &nbsp;·&nbsp; STUDIO EDITION &nbsp;·&nbsp; "
                      f"DESIGN CODE {SPEC['code']}", S["ribbon"]),
            Spacer(1, 8),
            Rule(CW, 1.5, c("accent"), 2),
            Spacer(1, 12),
            Paragraph(md(SPEC["title"]), S["h1"]),
            Paragraph(md("Bauble, star and snowflake · three quick hanging ornaments"), S["pitch"]),
            Spacer(1, 4),
            Paragraph("CROCHET PATTERN · US + UK TERMS · INK-FRIENDLY PRINT LAYOUT", tag),
            Spacer(1, 10)]

    body = []
    if True:
        path = ROOT / (SPEC["hero"] if edition == "colour" else SPEC.get("hero_bw", SPEC["hero"]))
        body.append(RoundedImage(path, CW, ratio=4 / 3, radius=12))
        body.append(Spacer(1, 6))
        body.append(Paragraph(
            ("Illustrative render of the finished design \u2014 not a photograph of a sample. It "
             "shows the optional metallic stripe on the bauble.") if edition == "colour" else
            "Illustrative render of the finished design \u2014 not a photograph of a sample. "
            "Reproduced in greyscale for ink-saving prints.",
            ParagraphStyle("cap", parent=S["small"], fontSize=7)))
    body.append(Spacer(1, 8))
    body.append(pills(S))

    inside_cells = []
    for ttl, txt in (("MATERIALS &amp; GAUGE", "yarn, hook and fill, with a true 50 mm print check"),
                     ("ALL THREE PIECES", "stitch tables with US and UK terms side by side"),
                     ("FINISHING", "assembly, blocking, troubleshooting and care")):
        inside_cells.append([Paragraph(ttl, ParagraphStyle(
            "ins", parent=S["ribbon"], fontSize=7, textColor=c("accent"))),
            Spacer(1, 2), Paragraph(txt, S["small"])])
    inside = Table([inside_cells], colWidths=[CW / 3] * 3)
    inside.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                                ("BACKGROUND", (0, 0), (-1, -1), c("card")),
                                ("LINEABOVE", (0, 0), (-1, 0), 0.8, c("border")),
                                ("LINEBELOW", (0, 0), (-1, -1), 0.8, c("border")),
                                ("LEFTPADDING", (0, 0), (0, 0), 0),
                                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                                ("TOPPADDING", (0, 0), (-1, -1), 7),
                                ("BOTTOMPADDING", (0, 0), (-1, -1), 7)]))
    body.append(Spacer(1, 14))
    body.append(inside)

    sw = []
    for name, hexv in SPEC["swatches"]:
        sw.append(Paragraph(f'<font color="{swatch_colour(name, hexv)}">&#9632;</font>&nbsp;{name}',
                            S["small"]))
    swt = Table([sw], colWidths=[CW / len(sw)] * len(sw))
    swt.setStyle(TableStyle([("LEFTPADDING", (0, 0), (-1, -1), 0)]))
    tail = [Rule(CW, 0.6, c("border"), 2), Spacer(1, 6),
            Paragraph(md(SPEC["pitch"]), S["body"]), Spacer(1, 8), swt]

    def blk_h(items):
        return sum(f.wrap(CW, FRAME_H)[1] for f in items)

    slack = FRAME_H - blk_h(head) - blk_h(body) - blk_h(tail) - 20
    story.extend(head)
    story.append(Spacer(1, max(8, slack * 0.45)))
    story.extend(body)
    story.append(Spacer(1, max(8, slack * 0.55)))
    story.extend(tail)
    story.append(PageBreak())

    # ---------------- page 2: materials / gauge / abbreviations / safety
    p2 = len(story)
    mat = sec.get("Materials", [])
    gauge = sec.get("Gauge & size", [])
    abbr = sec.get("Abbreviations (US + UK)", [])
    tech = sec.get("Construction & techniques", [])
    safety = sec.get("Safety — read this first", [])

    LW = CW * 0.52 - 12
    RW = CW * 0.48 - 6
    dots = " ".join(f'<font color="{swatch_colour(n, h)}">&#9632;</font>'
                    for n, h in SPEC["swatches"])
    yarn_rows = [
        ("Yarn", "DK / light worsted (#3), cotton or acrylic, in red, white, green, gold, "
                 "blue and silver: scraps are enough for the set."),
        ("Shades", dots, True),
        ("Hook", "3.5 mm (US E/4)"),
        ("Fill", "about 1 g polyester fiberfill, bauble only"),
        ("Notions", "tapestry needle, scissors, pin board for blocking"),
    ]
    left = [Paragraph("Materials &amp; tools", S["h2"]),
            kv_table(yarn_rows, S, [LW * 0.40, LW * 0.60], ("Item", "Detail")),
            Spacer(1, 8),
            Paragraph("Abbreviations (US + UK)", S["h2"])]
    ab_rows = []
    for kind, payload in abbr:
        if kind != "p":
            continue
        if payload.lower().startswith(("how to read", "this dual pattern")):
            continue                 # prose note, not an abbreviation entry
        for part in [x.strip() for x in payload.split("·")]:
            if " - " in part:
                a, b = part.split(" - ", 1)
                ab_rows.append((a.strip(), b.strip()))
            else:
                ab_rows.append(("", part.strip()))
    ab = Table([[Paragraph(md(a), S["cellb"]), Paragraph(md(b), S["cell"])] for a, b in ab_rows],
               colWidths=[LW * 0.30, LW * 0.70])
    ab.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, c("border")),
                            ("VALIGN", (0, 0), (-1, -1), "TOP"),
                            ("TOPPADDING", (0, 0), (-1, -1), 2.5),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5)]))
    left.append(ab)
    left.append(Spacer(1, 6))
    left.append(Paragraph(
        "How to read the tables: every round appears twice, side by side \u2014 US terms on the "
        "left, UK terms on the right. Stitch counts are identical for both terminologies; the "
        "counts in this booklet follow US terms.", S["small"]))

    right = [Paragraph("Gauge &amp; size", S["h2"]),
             Paragraph(
                 "Gauge sets the finished size: at 3.4 mm per stitch and 3.0 mm per round the "
                 "bauble comes out 2.6 cm across, the star 6 cm point to point and the snowflake "
                 "6 cm across. Work tightly enough that the bauble holds its fill and the star "
                 "blocks flat. Sizes are calculated from the stitch counts at that gauge; measure "
                 "your first piece and change hook if you want the set larger or smaller.",
                 S["small"]),
             Spacer(1, 4)]
    right.append(Spacer(1, 2))
    right.append(Paragraph("Print check — 50 mm at 100%", S["h3"]))
    rw = Table([[GaugeRuler()], [Paragraph("This bar must measure 50 mm (2 in). If it does not, "
                                           "set your printer to Actual Size / 100%.", S["small"])]],
               colWidths=[min(RW, 60 * mm)])
    rw.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.7, c("border")),
                            ("BACKGROUND", (0, 0), (-1, -1), c("card")),
                            ("LEFTPADDING", (0, 0), (-1, -1), 7),
                            ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                            ("TOPPADDING", (0, 0), (-1, -1), 6),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    right.append(rw)
    right.append(Spacer(1, 8))
    right.append(Paragraph("Techniques, in the order you meet them", S["h3"]))
    for kind, payload in tech:
        if kind == "num":
            n, t = payload
            right.append(Paragraph(f"<b>{n}.</b>&nbsp; {md(t)}", S["small"]))
            right.append(Spacer(1, 3))

    grid = Table([[left, right]], colWidths=[CW * 0.52, CW * 0.48])
    grid.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                              ("LEFTPADDING", (0, 0), (0, 0), 0),
                              ("RIGHTPADDING", (0, 0), (0, 0), 10),
                              ("LEFTPADDING", (1, 0), (1, 0), 6),
                              ("RIGHTPADDING", (1, 0), (1, 0), 0)]))
    if os.environ.get('NOV_DEBUG'):
        print('left', sum(f.wrap(LW, 999)[1] for f in left), 'right', sum(f.wrap(RW, 999)[1] for f in right))
        print('grid', grid.wrap(CW, 999)[1])
    story.append(grid)
    story.append(Spacer(1, 12))
    story.extend(glance_block(sec, S))
    safety_text = " ".join(payload for kind, payload in safety if kind == "p")
    story.append(Spacer(1, 10))
    story.append(callout("Safety — read this first", safety_text, S, c("pause_border")))
    story.append(PageBreak())

    # ---------------- instructions
    story.append(Paragraph("Instructions", S["h2"]))
    story.append(Spacer(1, 2))
    inst = sec.get("Instructions", [])
    cards, cur = [], None
    for kind, payload in inst:
        if kind == "h3":
            if cur:
                cards.append(cur)
            cur = {"h3": payload, "items": []}
        elif cur is not None:
            cur["items"].append((kind, payload))
    if cur:
        cards.append(cur)

    for carddef in cards:
        inner = [Paragraph(md(carddef["h3"]), S["h3"])]
        ntables = sum(1 for k, _ in carddef["items"] if k == "table")
        rows = max((len(p) for k, p in carddef["items"] if k == "table"), default=0)
        for kind, payload in carddef["items"]:
            if kind == "table":
                inner.append(stitch_table(payload, S, tick))
                inner.append(Spacer(1, 5))
            elif kind == "p":
                inner.append(Paragraph(md(payload), S["body"]))
                inner.append(Spacer(1, 4))
        box = card(inner)
        if rows and rows <= 16:
            story.append(KeepTogether([box, Spacer(1, 7)]))
        else:
            story.append(box)
            story.append(Spacer(1, 7))
    story.append(Spacer(1, 4))

    # ---------------- final page: finishing, troubleshooting, care/terms
    story.append(CondPageBreak(2.6 * inch))
    story.append(Paragraph("Finishing &amp; assembly", S["h2"]))
    fin = sec.get("Finishing & assembly", [])
    steps = [(p[0], p[1]) for k, p in fin if k == "num"]
    rows = []
    for n, t in steps:
        rows.append([Badge(int(n)), Paragraph(md(t), S["body"])])
    ft = Table(rows, colWidths=[20, CW - 20])
    ft.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                            ("LEFTPADDING", (0, 0), (-1, -1), 0),
                            ("RIGHTPADDING", (0, 0), (0, -1), 6),
                            ("TOPPADDING", (0, 0), (-1, -1), 3),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    story.append(ft)
    story.append(Spacer(1, 12))

    story.append(Paragraph("Troubleshooting", S["h2"]))
    tb = [(k, p) for k, p in sec.get("Troubleshooting", []) if k == "bullet"]
    rows = [[Paragraph("<b>If this happens</b>", S["cell"]), Paragraph("<b>Do this</b>", S["cell"])]]
    for item in tb:
        m = re.match(r"\*\*(.+?)\*\*\s*(.*)", item[1])
        head, body = (m.group(1), m.group(2)) if m else ("Note", item[1])
        rows.append([Paragraph(md(head), S["cellb"]), Paragraph(md(body), S["small"])])
    grid2 = Table(rows, colWidths=[CW * 0.28, CW * 0.72], repeatRows=1)
    grid2.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), c("soft")),
        ("BOX", (0, 0), (-1, -1), 0.7, c("border")),
        ("INNERGRID", (0, 0), (-1, -1), 0.4, c("border")),
        ("BACKGROUND", (0, 1), (-1, -1), c("card")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
    story.append(grid2)
    story.append(Spacer(1, 12))

    # three-column footer grid: care | colorways | terms
    care = sec.get("Care & storage", [])
    col = sec.get("Colorways", [])
    terms = sec.get("Terms of Use", [])
    care_txt = " ".join(p for k, p in care if k == "p")
    cw_items = []
    for k, p in col:
        if k == "table":
            for r in p[1:]:
                if len(r) >= 5:
                    cw_items.append("<b>%s</b><br/>%s / %s / %s / %s" % (r[0], r[1], r[2], r[3], r[4]))
                else:
                    cw_items.append("<b>%s</b><br/>%s" % (r[0], " / ".join(r[1:])))
        elif k == "p":
            cw_items.append(md(p))
    cw_legend = ('<font size="6.6">columns: bauble R1-R4 / R5-R6 / R7-R9 / star + '
                 'snowflake</font><br/><br/>')
    term_parts, skip = [], False
    for k, p in terms:
        if k == "h3":
            skip = "safety" in p.lower()          # already covered by the page-2 callout
            if not skip:
                term_parts.append(("h", p))
        elif k == "p" and not skip:
            if p.startswith("\u00a9") or p.startswith("(c)"):
                continue                           # copyright appears once, in the footer
            term_parts.append(("p", p))

    two = []
    for title, body, raw in (("Care &amp; washing", care_txt, False),
                             ("Colorways", cw_legend + "<br/><br/>".join(cw_items), True)):
        two.append([Paragraph(title, S["h3"]),
                    Paragraph(body if raw else md(body), ParagraphStyle(
                        "colbody", parent=S["body"], fontSize=8.8, leading=12.4))])
    gt = Table([two], colWidths=[CW * 0.42, CW * 0.58])
    gt.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                            ("BOX", (0, 0), (-1, -1), 0.7, c("border")),
                            ("INNERGRID", (0, 0), (-1, -1), 0.5, c("border")),
                            ("BACKGROUND", (0, 0), (-1, -1), c("card")),
                            ("LEFTPADDING", (0, 0), (-1, -1), 10),
                            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                            ("TOPPADDING", (0, 0), (-1, -1), 10),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), 12)]))
    cells_terms = [Paragraph("Terms of use", S["h3"])]
    body_style = ParagraphStyle("tbody", parent=S["body"], fontSize=8.8, leading=12.4)
    for kind, payload in term_parts:
        if kind == "h":
            cells_terms.append(Paragraph("<b>%s</b>" % md(payload), body_style))
        else:
            cells_terms.append(Paragraph(md(payload), body_style))
            cells_terms.append(Spacer(1, 4))
    tt = Table([[c] for c in cells_terms], colWidths=[CW])
    tt.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.7, c("border")),
                            ("BACKGROUND", (0, 0), (-1, -1), c("card")),
                            ("LEFTPADDING", (0, 0), (-1, -1), 10),
                            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                            ("TOPPADDING", (0, 0), (-1, -1), 3),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                            ("TOPPADDING", (0, 0), (0, 0), 10),
                            ("BOTTOMPADDING", (0, -1), (0, -1), 10)]))
    story.append(CondPageBreak(3.4 * inch))
    story.append(gt)
    story.append(Spacer(1, 8))
    story.append(tt)
    story.append(Spacer(1, 16))
    story.append(Rule(CW, 0.6, c("border"), 2))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Happy crocheting!", ParagraphStyle(
        "close", parent=S["h2"], fontSize=11, alignment=TA_CENTER, spaceBefore=0)))
    story.append(Paragraph("Tag your makes <b>#NovalityStore</b> and <b>#NovalityOrnaments</b> \u2014 "
                           "tag us in your trees and tables. Thank you for supporting an independent "
                           "pattern designer.",
                           ParagraphStyle("close2", parent=S["small"], alignment=TA_CENTER)))

    # two-pass for page totals (probe file outside the repo, then the real build)
    import pymupdf
    probe_path = Path("/tmp/novality_probe.pdf")
    probe = Doc(probe_path, edition)
    probe.total_pages = 99
    probe.build(list(story))
    pages = pymupdf.open(str(probe_path)).page_count
    doc = Doc(out, edition)
    doc.total_pages = pages
    doc.build(list(story))
    retoc(out)
    tmp_pages = pages
    print(f"wrote {out} pages: {tmp_pages}")
    return tmp_pages


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--edition", choices=["colour", "print"], default="colour")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    name = "NS13_Christmas_Ornament_Bundle_%s_Edition.pdf" % a.edition.title()
    out = Path(a.out) if a.out else ROOT / "deliverables" / name
    build(a.edition, out)


if __name__ == "__main__":
    main()
