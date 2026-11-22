"""What a passing result does not mean.

These notes are not errors. A photo and a chart image are not opened.
A cinch with no number, and a lowercase sew line, are read by the written
checks. They are not listed here.
"""

from __future__ import annotations

import re

def has_unparsed_repeat_suffix(body: str) -> bool:
    """Detect a parsed-looking flat repeat followed by ignored alternative text."""
    candidate = body.strip().rstrip(".").strip()
    stated = re.search(r"\s*\(\d+\)\s*$", candidate)
    if stated:
        candidate = candidate[: stated.start()].rstrip()

    flat = re.match(
        r"[\(\[][^()\[\]]+[\)\]]\s*[x×]\s*\d+",
        candidate,
        flags=re.IGNORECASE,
    )
    if flat and candidate[flat.end() :].strip():
        return True

    star = re.match(
        r"\*[^*]+\*\s*(?:rep(?:eat)?\s+)?"
        r"(?:\d+\s+times|[x×]\s*\d+)",
        candidate,
        flags=re.IGNORECASE,
    )
    return bool(star and candidate[star.end() :].strip())


def parser_coverage_notes(text: str) -> list[str]:
    """Audit only recognized Row/Round headers for empty or partly parsed bodies."""
    from ..parser.grammar import is_row_header
    from ..parser.normalizer import sanitize_pattern_text
    from ..parser.parser import CrochetParser

    parser = CrochetParser()
    notes: list[str] = []
    for line_number, raw in enumerate(sanitize_pattern_text(text).splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith(">") or line.startswith("```"):
            continue
        candidate = line
        for marker in ("- ", "* ", "+ "):
            if candidate.startswith(marker):
                candidate = candidate[len(marker) :].strip()
                break
        is_header, _, _, body, _ = is_row_header(candidate)
        if not is_header:
            continue
        if not body.strip():
            notes.append(
                f"Line {line_number}: row/round header has no instruction body to verify."
            )
            continue
        try:
            instructions = parser._parse_instruction_text(body.strip(), line)
        except Exception:
            instructions = []
        not_fully_parsed = not instructions or any(
            instruction.is_ambiguous or bool(instruction.parse_warnings)
            for instruction in instructions
        )
        # A tail after a repeat is review-worthy only when the parser also
        # signals incomplete coverage; valid repeat-plus-clause lines are read.
        if has_unparsed_repeat_suffix(body) and not_fully_parsed:
            notes.append(
                f"Line {line_number}: text after the repeat may be unparsed; "
                f"review manually: {line}"
            )
        elif not_fully_parsed:
            notes.append(
                f"Line {line_number}: parser could not fully interpret this "
                f"instruction; review manually: {line}"
            )
    return notes


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
    """Return parser-coverage and existing prose/assembly notes without duplication."""
    items = parser_coverage_notes(text) + unread_instruction_lines(text) + assembly_gaps(text)
    return list(dict.fromkeys(items))


def purchase_blockers() -> list[str]:
    """Facts a text checker cannot supply. These do not change a status."""
    return [
        "A photo was not opened.",
        "The piece was not made.",
        "A gauge swatch was not measured.",
        "This result is not a purchase check.",
    ]


def assembly_gaps(text: str) -> list[str]:
    """Read sew and flatten lines that do not give a comparable count.

    The count is not guessed. A missing number is named, not passed.
    """
    notes = []
    made = {}
    for line in text.splitlines():
        if line.lstrip().startswith(">") or _PROHIBITION.search(line):
            continue
        match = re.search(
            r"\b([A-Za-z][A-Za-z]+)\s*(?:\(make\s+(\d+)\)|[—–-]\s*make\s+(\d+)\b)",
            line,
            re.IGNORECASE,
        )
        if match:
            count = int(match.group(2) or match.group(3))
            made[match.group(1).lower()] = count
    named = set()
    flatten = False
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith(">") or line.startswith("#") or _PROHIBITION.search(line):
            continue
        if re.search(r"\bflatten\b", line, re.IGNORECASE) and len(re.findall(r"\d+", line)) < 2:
            flatten = True
        if re.search(r"\d", line):
            continue
        if not re.search(r"\b(?:sew|attach)\b", line, re.IGNORECASE):
            continue
        for name, count in made.items():
            if name in named:
                continue
            if re.search(rf"\b{name}s?\b", line, re.IGNORECASE):
                named.add(name)
                notes.append(
                    f"{name} is made {count} times, but the sew line does not say how many. "
                    "The count was not guessed."
                )
    if flatten:
        notes.append(
            "A flatten line does not give two stitch counts, so the seam was not compared."
        )
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

    These are not errors. A quoted line and a prohibition are not
    instructions. A cinch and a lowercase sew line have their own checks.
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
