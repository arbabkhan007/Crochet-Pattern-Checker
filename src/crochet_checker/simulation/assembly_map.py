"""Draw a piece join only when the written line names two pieces.

The line is not a stitch map, not a photo, and not a measured size.
A missing piece is not invented, and a make count is not turned into a sewn count.
"""

from __future__ import annotations

import html
import re

from pydantic import BaseModel, Field

ASSEMBLY_NOTE = (
    "An assembly line is drawn only when the line names two written pieces. "
    "It is not a stitch join, not a photo, and not a measured size. "
    "A missing piece is not invented."
)

_VERB = re.compile(r"\b(?:sew|sewn|sewing|attach|attached|join|joined)\b", re.IGNORECASE)
_ROUND_LINE = re.compile(
    r"\b(?:round|row|rnd|sl\s*st|slip\s+stitch)\b",
    re.IGNORECASE,
)


class AssemblyEdge(BaseModel):
    left: str
    right: str
    sources: list[str] = Field(default_factory=list)


class AssemblyMap(BaseModel):
    pieces: list[str] = Field(default_factory=list)
    make_counts: dict[str, int | None] = Field(default_factory=dict)
    edges: list[AssemblyEdge] = Field(default_factory=list)
    unnamed: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


def written_assembly(pattern) -> AssemblyMap:
    """Read piece joins from the written lines. Do not guess a stitch."""
    pieces = []
    counts: dict[str, int | None] = {}
    for piece in getattr(pattern, "pieces", []) or []:
        name = (piece.name or "").strip()
        if not name or name in counts:
            continue
        pieces.append(name)
        counts[name] = piece.make_count
    notes = [ASSEMBLY_NOTE]
    if not pieces:
        notes.append("No piece list was written, so no assembly join was drawn.")
        return AssemblyMap(notes=notes)

    edges: dict[tuple[str, str], AssemblyEdge] = {}
    unnamed: list[str] = []
    multi = False
    for line in _candidate_lines(pattern):
        if not _VERB.search(line) or _ROUND_LINE.search(line):
            continue
        named = _named_pieces(line, pieces)
        if len(named) == 2:
            key = tuple(sorted(named))
            edge = edges.get(key)
            if edge is None:
                edge = AssemblyEdge(left=key[0], right=key[1], sources=[line])
                edges[key] = edge
            elif line not in edge.sources:
                edge.sources.append(line)
        elif len(named) == 1:
            unnamed.append(line)
        elif len(named) > 2:
            multi = True
            unnamed.append(line)
    if unnamed:
        notes.append(
            "A sew or attach line did not name two written pieces. "
            "The missing piece was not invented."
        )
    if multi:
        notes.append("A line names more than two pieces. Those joins were not guessed.")
    if any((counts.get(name) or 0) > 1 for name in pieces):
        notes.append("A make count is not a sewn count. The number was not guessed.")
    return AssemblyMap(
        pieces=pieces,
        make_counts=counts,
        edges=list(edges.values()),
        unnamed=unnamed,
        notes=notes,
    )


def assembly_map_svg(assembly: AssemblyMap, title: str = "Assembly map") -> str:
    """Boxes and lines for written piece pairs. Not a stitch diagram."""
    width, height = 760, 360
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}">',
        f'<rect width="{width}" height="{height}" fill="#ffffff"/>',
        f'<text x="24" y="32" font-family="sans-serif" font-size="18" fill="#243042">'
        f"{_xml(title)}</text>",
        f'<text x="24" y="54" font-family="sans-serif" font-size="11" fill="#5c6b7a">'
        f"{_xml(assembly.notes[0])}</text>",
    ]
    if not assembly.pieces:
        parts.append(
            '<text x="24" y="92" font-family="sans-serif" font-size="13" fill="#5c6b7a">'
            "No piece list was written.</text></svg>"
        )
        return "\n".join(parts)
    boxes = _boxes(assembly.pieces, 24, 78, width - 48, 70)
    centers = {}
    for name, (x, y, w, h) in boxes.items():
        centers[name] = (x + w / 2, y + h / 2)
    for edge in assembly.edges:
        x1, y1 = centers[edge.left]
        x2, y2 = centers[edge.right]
        parts.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="#8aa0b4" stroke-width="2"/>'
        )
    for name, (x, y, w, h) in boxes.items():
        count = assembly.make_counts.get(name)
        label = name if not count else f"{name} x {count}"
        parts.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="6" '
            f'fill="#f4f7fb" stroke="#243042"/>'
        )
        parts.append(
            f'<text x="{x + w / 2:.1f}" y="{y + h / 2 + 4:.1f}" text-anchor="middle" '
            f'font-family="sans-serif" font-size="12" fill="#243042">{_xml(label)}</text>'
        )
    y = 176
    parts.append(
        '<text x="24" y="176" font-family="sans-serif" font-size="12" fill="#243042">'
        "Written lines</text>"
    )
    y = 196
    shown = []
    for edge in assembly.edges:
        shown.extend(edge.sources)
    if not shown:
        shown.append("No line named two written pieces.")
    for line in shown[:6]:
        parts.append(
            f'<text x="24" y="{y}" font-family="sans-serif" font-size="11" fill="#243042">'
            f"{_xml(line[:90])}</text>"
        )
        y += 16
    for line in assembly.unnamed[:3]:
        parts.append(
            f'<text x="24" y="{y}" font-family="sans-serif" font-size="11" fill="#8a5a4a">'
            f"Not drawn: {_xml(line[:80])}</text>"
        )
        y += 16
    parts.append("</svg>")
    return "\n".join(parts)


def _candidate_lines(pattern) -> list[str]:
    seen = set()
    lines = []
    finishing = list(getattr(pattern, "finishing", []) or [])
    source = (getattr(pattern, "source_text", "") or "").splitlines()
    for raw in finishing + source:
        text = " ".join(raw.split())
        if not text or text in seen:
            continue
        seen.add(text)
        if text.startswith(">"):
            continue
        if re.match(r"^(?:round|row|rnd)\b", text, re.IGNORECASE):
            continue
        lines.append(text)
    return lines


def _named_pieces(line: str, pieces: list[str]) -> list[str]:
    found = []
    for name in pieces:
        if re.search(rf"\b{re.escape(name)}\b", line, re.IGNORECASE):
            found.append(name)
    return found


def _boxes(pieces: list[str], left: float, top: float, width: float, height: float):
    count = max(len(pieces), 1)
    gap = 12
    box_w = min(120, (width - gap * (count - 1)) / count)
    used = box_w * count + gap * (count - 1)
    start = left + (width - used) / 2
    boxes = {}
    for index, name in enumerate(pieces):
        boxes[name] = (start + index * (box_w + gap), top, box_w, height)
    return boxes


def _xml(text: str) -> str:
    return html.escape(text, quote=True)
