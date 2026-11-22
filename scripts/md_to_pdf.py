#!/usr/bin/env python3
"""Render the corrected NS 14 markdown to a printable PDF with ReportLab.

Pure-Python: no WeasyPrint, no system libraries. Handles the subset of markdown
used by the pattern document - headings, tables, blockquotes, fenced code,
bullet/ordered lists, horizontal rules, and inline bold/italic/code.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    CondPageBreak,
    Frame,
    HRFlowable,
    KeepTogether,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
INK = colors.HexColor("#111111")
MUTED = colors.HexColor("#5b5b5b")
RULE = colors.HexColor("#c8c8c8")
BAND = colors.HexColor("#f0f0f0")
NOTE_BG = colors.HexColor("#f7f7f7")
ACCENT = colors.HexColor("#1f5130")


def register_fonts() -> tuple[str, str, str]:
    """Register DejaVu face by face.

    Registration is per-file on purpose: this box ships DejaVuSans.ttf,
    DejaVuSans-Bold.ttf and DejaVuSansMono.ttf but no Oblique. Registering the
    set as one try/except meant a single missing file silently downgraded the
    whole document to Helvetica, which has no U+2610 ballot box and rendered
    every progress checkbox as a filled .notdef block. Italic falls back to the
    regular face rather than taking the document down with it.
    """

    def reg(name: str, filename: str) -> bool:
        path = FONT_DIR / filename
        if not path.is_file():
            return False
        try:
            pdfmetrics.registerFont(TTFont(name, str(path)))
            return True
        except Exception:  # pragma: no cover - unreadable font file
            return False

    if not reg("DejaVu", "DejaVuSans.ttf"):
        return "Helvetica", "Helvetica-Bold", "Courier"

    bold = "DejaVu-Bold" if reg("DejaVu-Bold", "DejaVuSans-Bold.ttf") else "DejaVu"
    mono = "DejaVuMono" if reg("DejaVuMono", "DejaVuSansMono.ttf") else "DejaVu"
    italic = "DejaVu-Oblique" if reg("DejaVu-Oblique", "DejaVuSans-Oblique.ttf") else "DejaVu"

    # registerFontFamily alone leaves ps2tt("DejaVu") == ("dejavu", 1, 1), i.e. the
    # base face is treated as already bold+italic, so <b> resolves back to the
    # regular face and every bold run renders at normal weight. addMapping writes
    # both direction maps, and the (0, 0) call must come last: each call also sets
    # _ps2tt_map[psname], so a later alias for the same file would clobber it.
    from reportlab.lib.fonts import addMapping

    addMapping("DejaVu", 1, 1, bold)
    addMapping("DejaVu", 0, 1, italic)
    addMapping("DejaVu", 1, 0, bold)
    addMapping("DejaVu", 0, 0, "DejaVu")
    return "DejaVu", bold, mono


BODY, BOLD, MONO = register_fonts()


def inline(text: str) -> str:
    """Convert inline markdown to ReportLab markup."""
    out = escape(text)
    out = re.sub(r"`([^`]+)`", rf'<font face="{MONO}" size="8.5">\1</font>', out)
    out = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", out)
    out = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<i>\1</i>", out)
    out = out.replace("\u2610", f'<font face="{BODY}" size="10.5">&#9744;</font>')
    return out


def styles() -> dict[str, ParagraphStyle]:
    def mk(**kw):
        kw.setdefault("fontName", BODY)
        kw.setdefault("textColor", INK)
        return ParagraphStyle(**kw)

    return {
        "title": mk(name="t", fontName=BOLD, fontSize=23, leading=27,
                    spaceAfter=2, textColor=ACCENT),
        "sub": mk(name="s", fontSize=9.5, leading=13, textColor=MUTED, spaceAfter=10),
        "h1": mk(name="h1", fontName=BOLD, fontSize=15.5, leading=19, spaceBefore=16,
                 spaceAfter=6, textColor=ACCENT),
        "h2": mk(name="h2", fontName=BOLD, fontSize=12, leading=15, spaceBefore=11, spaceAfter=5),
        "h3": mk(name="h3", fontName=BOLD, fontSize=10.3, leading=13, spaceBefore=9, spaceAfter=4),
        "p": mk(name="p", fontSize=9.2, leading=13.2, spaceAfter=5, alignment=TA_LEFT),
        "li": mk(name="li", fontSize=9.2, leading=13.2, spaceAfter=2.5, leftIndent=11,
                 bulletIndent=2),
        "note": mk(name="n", fontSize=8.8, leading=12.6, spaceAfter=4),
        "code": mk(name="c", fontName=MONO, fontSize=7.9, leading=10.2, textColor=INK),
        "cell": mk(name="cell", fontSize=8.0, leading=10.6),
        "cellb": mk(name="cellb", fontName=BOLD, fontSize=8.0, leading=10.6),
    }


S = styles()


def split_row(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def is_sep(line: str) -> bool:
    return bool(re.fullmatch(r"\|[\s:\-|]+\|", line.strip()))


def build_table(rows: list[list[str]], width: float) -> Table:
    head, body = rows[0], rows[1:]
    ncols = len(head)
    data = [[Paragraph(inline(c), S["cellb"]) for c in head]]
    for r in body:
        r = (r + [""] * ncols)[:ncols]
        data.append([Paragraph(inline(c), S["cell"]) for c in r])

    # Weight columns by content length so instruction columns get the room.
    weights = []
    for i in range(ncols):
        longest = max((len(r[i]) if i < len(r) else 0) for r in rows)
        weights.append(max(longest, 6) ** 0.72)
    total = sum(weights)
    widths = [max(width * w / total, 13 * mm) for w in weights]
    if sum(widths) > width:  # rescale back down after the minimum clamp
        k = width / sum(widths)
        widths = [w * k for w in widths]

    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), BAND),
                ("LINEBELOW", (0, 0), (-1, 0), 0.7, RULE),
                ("GRID", (0, 0), (-1, -1), 0.3, RULE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 3.2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3.2),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#fafafa")]),
            ]
        )
    )
    return t


def parse(md: str, width: float) -> list:
    lines = md.split("\n")
    flow: list = []
    i = 0
    first_h1 = True

    while i < len(lines):
        ln = lines[i]
        st = ln.strip()

        if not st:
            i += 1
            continue

        # fenced code
        if st.startswith("```"):
            i += 1
            buf = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1
            txt = "<br/>".join(escape(b) or "&nbsp;" for b in buf)
            box = Table([[Paragraph(txt, S["code"])]], colWidths=[width], hAlign="LEFT")
            box.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, -1), NOTE_BG),
                        ("BOX", (0, 0), (-1, -1), 0.4, RULE),
                        ("LEFTPADDING", (0, 0), (-1, -1), 7),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                        ("TOPPADDING", (0, 0), (-1, -1), 6),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                    ]
                )
            )
            flow += [Spacer(1, 3), box, Spacer(1, 7)]
            continue

        # table
        if st.startswith("|") and i + 1 < len(lines) and is_sep(lines[i + 1]):
            rows = [split_row(st)]
            i += 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(split_row(lines[i]))
                i += 1
            flow += [Spacer(1, 3), build_table(rows, width), Spacer(1, 8)]
            continue

        # blockquote (callout)
        if st.startswith(">"):
            buf = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                buf.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            inner = parse("\n".join(buf), width - 14 * mm)
            box = Table([[inner]], colWidths=[width], hAlign="LEFT")
            box.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, -1), NOTE_BG),
                        ("LINEBEFORE", (0, 0), (0, -1), 2.4, ACCENT),
                        ("LEFTPADDING", (0, 0), (-1, -1), 9),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                        ("TOPPADDING", (0, 0), (-1, -1), 7),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                    ]
                )
            )
            flow += [Spacer(1, 4), box, Spacer(1, 9)]
            continue

        # horizontal rule
        if re.fullmatch(r"-{3,}|\*{3,}", st):
            flow += [Spacer(1, 5), HRFlowable(width="100%", thickness=0.5, color=RULE),
                     Spacer(1, 5)]
            i += 1
            continue

        # headings
        m = re.match(r"^(#{1,6})\s+(.*)$", st)
        if m:
            lvl, txt = len(m.group(1)), m.group(2)
            if lvl == 1 and first_h1:
                flow.append(Paragraph(inline(txt), S["title"]))
                first_h1 = False
            elif lvl == 1:
                flow += [CondPageBreak(42 * mm), Paragraph(inline(txt), S["h1"])]
            elif lvl == 2:
                flow += [CondPageBreak(34 * mm), Paragraph(inline(txt), S["h2"])]
            else:
                flow += [CondPageBreak(26 * mm), Paragraph(inline(txt), S["h3"])]
            i += 1
            continue

        # lists
        if re.match(r"^\s*([-*+]|\d+\.)\s+", ln):
            items = []
            while i < len(lines) and re.match(r"^\s*([-*+]|\d+\.)\s+", lines[i]):
                mm_ = re.match(r"^\s*([-*+]|\d+\.)\s+(.*)$", lines[i])
                marker, txt = mm_.group(1), mm_.group(2)
                i += 1
                # absorb wrapped continuation lines
                while (
                    i < len(lines)
                    and lines[i].strip()
                    and not re.match(r"^\s*([-*+]|\d+\.)\s+", lines[i])
                    and not lines[i].strip().startswith(("#", "|", ">", "```"))
                    and not re.fullmatch(r"-{3,}", lines[i].strip())
                ):
                    txt += " " + lines[i].strip()
                    i += 1
                bullet = marker if marker[0].isdigit() else "\u2022"
                items.append(Paragraph(inline(txt), S["li"], bulletText=bullet))
            flow += [Spacer(1, 2), *items, Spacer(1, 6)]
            continue

        # paragraph
        buf = [st]
        i += 1
        while (
            i < len(lines)
            and lines[i].strip()
            and not lines[i].strip().startswith(("#", "|", ">", "```", "- ", "* "))
            and not re.fullmatch(r"-{3,}", lines[i].strip())
            and not re.match(r"^\s*\d+\.\s", lines[i])
        ):
            buf.append(lines[i].strip())
            i += 1
        para = " ".join(buf)
        sty = S["sub"] if (len(flow) == 1 and not first_h1) else S["p"]
        flow.append(Paragraph(inline(para), sty))

    return flow


def render(md_path: Path, pdf_path: Path, header: str = "", footer: str = "") -> None:
    md = md_path.read_text(encoding="utf-8")
    page = A4
    lm = rm = 16 * mm
    tm = 21 * mm if header else 15 * mm
    bm = 16 * mm
    fw = page[0] - lm - rm

    doc = BaseDocTemplate(
        str(pdf_path),
        pagesize=page,
        leftMargin=lm,
        rightMargin=rm,
        topMargin=tm,
        bottomMargin=bm,
        title="Bobble Snowflake Tree Skirt - NS-14 (Corrected Edition)",
        author=header.split("|")[0].strip() or "Novality Store",
        subject="Crochet pattern, corrected edition",
    )
    frame = Frame(lm, bm, fw, page[1] - tm - bm, id="body",
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)

    def furniture(canvas, _doc):
        canvas.saveState()
        canvas.setStrokeColor(RULE)
        canvas.setLineWidth(0.4)

        if header:
            hy = page[1] - tm + 5.5 * mm
            canvas.setFont(BOLD, 7.4)
            canvas.setFillColor(ACCENT)
            canvas.drawString(lm, hy, header)
            canvas.line(lm, hy - 2.6 * mm, page[0] - rm, hy - 2.6 * mm)

        canvas.setFont(BODY, 7.0)
        canvas.setFillColor(MUTED)
        canvas.drawString(lm, bm - 8.5 * mm, footer)
        canvas.drawRightString(page[0] - rm, bm - 8.5 * mm, f"Page {canvas.getPageNumber()}")
        canvas.line(lm, bm - 5.5 * mm, page[0] - rm, bm - 5.5 * mm)
        canvas.restoreState()

    doc.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=furniture)])
    doc.build(parse(md, fw))


DEFAULT_HEADER = "Novality Store  |  Design Code NS-14  |  Corrected Edition"
DEFAULT_FOOTER = (
    "\u00a9 2026 Novality Store. All rights reserved. "
    "5-Axiom Mathematically Verified Pattern."
)


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description="Render a pattern markdown file to PDF.")
    ap.add_argument("source")
    ap.add_argument("dest")
    ap.add_argument("--header", default=DEFAULT_HEADER, help="running header text")
    ap.add_argument("--footer", default=DEFAULT_FOOTER, help="running footer text")
    ap.add_argument("--no-header", action="store_true", help="omit the running header")
    a = ap.parse_args()

    dst = Path(a.dest)
    dst.parent.mkdir(parents=True, exist_ok=True)
    render(Path(a.source), dst, "" if a.no_header else a.header, a.footer)
    print(f"wrote {dst}  ({dst.stat().st_size:,} bytes)")

