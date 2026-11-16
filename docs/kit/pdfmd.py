"""Small Markdown reader for the store PDF compiler.

Only the constructs the seventeen masters and the compiled volume actually use
are supported, and every one of them is: headings 1-4, paragraphs, bullet and
numbered lists, pipe tables with an alignment row, block quotes, horizontal
rules and inline **bold** / `code`. Single-asterisk emphasis never appears in
the masters, so it is deliberately not treated as markup (a stray asterisk in
an instruction line must not italicise the rest of a round).

The output is a list of `Block` records; the renderer in build_pdf.py turns
them into ReportLab flowables. Parsing is side-effect free, so the same reader
serves a single pattern and the compiled collection.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

HEADING = re.compile(r"^(#{1,4})\s+(.+?)\s*$")
BULLET = re.compile(r"^[-*]\s+(.+)$")
NUMBERED = re.compile(r"^(\d+)\.\s+(.+)$")
SEP_ROW = re.compile(r"^\|(?:\s*:?-{2,}:?\s*\|)+$")
HR = re.compile(r"^(?:-{3,}|\*{3,}|_{3,})$")


@dataclass
class Block:
    kind: str                      # h1 h2 h3 h4 p ul ol table quote hr
    text: str = ""
    level: int = 0
    items: list[str] = field(default_factory=list)      # ul / ol item texts
    header: list[str] = field(default_factory=list)     # table header cells
    rows: list[list[str]] = field(default_factory=list)  # table body rows
    aligns: list[str] = field(default_factory=list)


def _cells(line: str) -> list[str]:
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|"):
        body = body[:-1]
    return [c.strip() for c in body.split("|")]


def parse(md: str) -> list[Block]:
    """Turn Markdown into blocks. Blank lines separate everything."""
    lines = md.replace("\r\n", "\n").split("\n")
    blocks: list[Block] = []
    i = 0
    while i < len(lines):
        raw = lines[i]
        line = raw.rstrip()
        if not line.strip():
            i += 1
            continue

        m = HEADING.match(line)
        if m:
            blocks.append(Block(kind=f"h{len(m.group(1))}", text=m.group(2).strip(),
                                level=len(m.group(1))))
            i += 1
            continue

        if HR.match(line.strip()):
            blocks.append(Block(kind="hr"))
            i += 1
            continue

        if line.lstrip().startswith(">"):
            buf = []
            while i < len(lines) and lines[i].lstrip().startswith(">"):
                buf.append(lines[i].lstrip()[1:].strip())
                i += 1
            blocks.append(Block(kind="quote", text=" ".join(x for x in buf if x)))
            continue

        if line.lstrip().startswith("|"):
            header = _cells(line)
            table_lines = [line]
            i += 1
            # the masters space their printer-saver tables with blank lines
            # between rows, so a blank line does not end a table here: the next
            # pipe row with the same width does, and anything else ends it.
            while i < len(lines):
                if lines[i].lstrip().startswith("|"):
                    row_cells = _cells(lines[i])
                    if len(row_cells) != len(header):
                        break
                    table_lines.append(lines[i].rstrip())
                    i += 1
                    continue
                if not lines[i].strip():
                    j = i
                    while j < len(lines) and not lines[j].strip():
                        j += 1
                    if j < len(lines) and lines[j].lstrip().startswith("|") \
                            and len(_cells(lines[j])) == len(header):
                        i = j
                        continue
                break
            rows: list[list[str]] = []
            aligns: list[str] = []
            body_start = 1
            if len(table_lines) > 1 and SEP_ROW.match(table_lines[1].strip()):
                for cell in _cells(table_lines[1]):
                    cell = cell.strip()
                    if cell.startswith(":") and cell.endswith(":"):
                        aligns.append("center")
                    elif cell.endswith(":"):
                        aligns.append("right")
                    else:
                        aligns.append("left")
                body_start = 2
            for tline in table_lines[body_start:]:
                cells = _cells(tline)
                # pad short rows so a dropped trailing cell cannot shift columns
                while len(cells) < len(header):
                    cells.append("")
                rows.append(cells[:len(header)] if len(cells) > len(header) else cells)
            blocks.append(Block(kind="table", header=header, rows=rows,
                                aligns=aligns or ["left"] * len(header)))
            continue

        if BULLET.match(line.strip()):
            items: list[str] = []
            while i < len(lines):
                cand = lines[i].rstrip()
                mb = BULLET.match(cand.strip())
                if not mb:
                    break
                items.append(mb.group(1).strip())
                i += 1
            blocks.append(Block(kind="ul", items=items))
            continue

        if NUMBERED.match(line.strip()):
            items = []
            while i < len(lines):
                cand = lines[i].rstrip()
                mn = NUMBERED.match(cand.strip())
                if not mn:
                    break
                items.append(mn.group(2).strip())
                i += 1
            blocks.append(Block(kind="ol", items=items))
            continue

        # paragraph: collect until a blank line or the start of another block
        buf = [line.strip()]
        i += 1
        while i < len(lines):
            nxt = lines[i].rstrip()
            if not nxt.strip():
                break
            if (HEADING.match(nxt) or HR.match(nxt.strip()) or BULLET.match(nxt.strip())
                    or NUMBERED.match(nxt.strip()) or nxt.lstrip().startswith(("|", ">"))):
                break
            buf.append(nxt.strip())
            i += 1
        blocks.append(Block(kind="p", text=" ".join(buf)))
    return blocks


def inline(text: str) -> str:
    """Markdown inline markup -> ReportLab mini-markup, entity-safe."""
    out = (text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
    out = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", out)
    out = re.sub(r"`([^`]+)`", r'<font face="DD-M">\1</font>', out)
    return out


def plain(text: str) -> str:
    """Strip inline markup - used for headings, outline entries and QA."""
    text = text.replace("**", "").replace("`", "")
    return re.sub(r"\s+", " ", text).strip()


def table_is_stitch(header: list[str]) -> bool:
    """A stitch table is one whose first header cell labels rounds or rows."""
    first = plain(header[0]).strip().lower() if header else ""
    return first in ("rnd", "rnds", "round", "rounds", "row", "rows", "rnd / row")


def stitch_kind(header: list[str]) -> str:
    """'4' or '5' - the two stitch-table families the collection uses."""
    joined = " ".join(plain(h).lower() for h in header[1:])
    if "uk" in joined:
        return "5"
    return "4"


CRITICAL = ("pause", "start stuffing", "lock", "leave open")


def critical_row(cells: list[str]) -> bool:
    lowered = " ".join(cells).lower()
    return any(word in lowered for word in CRITICAL)
