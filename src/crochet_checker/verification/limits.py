"""What a passing result does not mean.

These notes are not errors. A cinch with no stitch count, and a lowercase
sew line, stay unread on purpose. A photo and a chart image are not opened.
"""

from __future__ import annotations

import re

SKIPPED = (
    "chart image detector",
    "photo stitch classifier",
    "hosted language model",
    "vision training set",
    "process cluster",
)


def skipped_line() -> str:
    return (
        "Not run: a chart image, a photo stitch count, a hosted model, "
        "a vision training set, and a process cluster."
    )


def unread_notes(text: str) -> list[str]:
    cinch = False
    sew = False
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith(">"):
            continue
        if re.search(r"\bdo not\b|\bdon't\b|\bshould\s+not\b", line, re.IGNORECASE):
            continue
        if re.search(r"\bcinch", line, re.IGNORECASE) and not re.search(r"\d", line):
            cinch = True
        if re.search(r"(?<![A-Za-z])sew\s+[a-z]+\s+to\s+[a-z]+\b", line):
            sew = True
    notes = []
    if cinch:
        notes.append("A cinch with no stitch count is not checked.")
    if sew:
        notes.append("A lowercase sew line is not read as a piece name.")
    notes.extend(unread_instruction_lines(text))
    return notes

_INSTRUCTION = re.compile(
    r"^(?:row|rnd|round|r)s?\.?\s*\d+"
    r"|\b(?:sc|hdc|dc|tr|dtr|inc|dec|sc2tog)\b"
    r"|\bsl\s*st\b"
    r"|\bmagic\s+ring\b"
    r"|\bch\s+\d+"
    r"|\b(?:single|double|half\s+double)\s+crochet\b"
    r"|\b(?:increase|decrease)\b",
    re.IGNORECASE,
)
_CINCH = re.compile(r"\bcinch", re.IGNORECASE)
_SEW = re.compile(r"(?<![A-Za-z])sew\s+[a-z]+\s+to\s+[a-z]+\b")
_PROHIBITION = re.compile(r"\bdo not\b|\bdon't\b|\bshould\s+not\b", re.IGNORECASE)


def _plain(line: str) -> str:
    line = re.sub(r"[*_`]", "", line)
    line = line.replace("–", "-").replace("—", "-").replace("−", "-")
    return re.sub(r"\s+", " ", line).strip().casefold()


def _consumed_lines(text: str) -> set[str] | None:
    """Lines the parser attached to a round or row.

    None means the parser could not be asked. That is not evidence that
    every line was unread.
    """
    try:
        from ..parser.parser import parse_pattern

        parsed = parse_pattern(text)
    except Exception:
        return None
    items = list(getattr(parsed, "rounds", None) or [])
    items.extend(getattr(parsed, "rows", None) or [])
    for piece in getattr(parsed, "pieces", None) or []:
        items.extend(getattr(piece, "rounds", None) or [])
        items.extend(getattr(piece, "rows", None) or [])
    found: set[str] = set()
    for item in items:
        source = str(getattr(item, "source_text", None) or "")
        for raw in source.splitlines():
            stripped = raw.strip()
            if not stripped:
                continue
            found.add(_plain(stripped))
    return found


def unread_instruction_lines(text: str) -> list[str]:
    """Name stitch lines the parser did not count.

    These are not errors. A quoted line, a prohibition, a cinch with no
    count, and a lowercase sew line keep their own rules.
    """
    consumed = _consumed_lines(text)
    if consumed is None:
        return []
    notes: list[str] = []
    hidden = 0
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith(">") or line.startswith("#"):
            continue
        if _PROHIBITION.search(line):
            continue
        plain = _plain(line)
        if not plain or not _INSTRUCTION.search(plain):
            continue
        if _CINCH.search(line) and not re.search(r"\d", line):
            continue
        if _SEW.search(line):
            continue
        if plain in consumed:
            continue
        if len(notes) >= 8:
            hidden += 1
            continue
        shown = plain if len(plain) <= 90 else plain[:87] + "..."
        notes.append(f"Not counted: {shown}")
    if hidden:
        notes.append(f"{hidden} more instruction lines were not counted.")
    return notes
