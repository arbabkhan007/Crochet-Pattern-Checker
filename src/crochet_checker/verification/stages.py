"""Deterministic stages the text checker can prove.

These stages read written pattern text. They do not call a vision model,
a hosted language model, or a cluster. A photo is never assigned a stitch
count here.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field


# Craft Yarn Council crochet single-crochet ranges per 4 inches.
# Source: https://www.craftyarncouncil.com/standards/yarn-weight-system
# A tight amigurumi gauge is common, so only a count outside half to
# double that published band warns. Lace is not banded: the Council says
# a lace range is hard to determine.
_WEIGHTS = (
    ("super bulky", (7, 9)),
    ("super fine", (21, 32)),
    ("light worsted", (12, 17)),
    ("fingering", (21, 32)),
    ("sport", (16, 20)),
    ("worsted", (11, 14)),
    ("chunky", (8, 11)),
    ("bulky", (8, 11)),
    ("jumbo", (1, 6)),
    ("sock", (21, 32)),
    ("aran", (11, 14)),
    ("dk", (12, 17)),
)
_NO_BAND = ("lace", "thread", "cobweb")

_HEADER = re.compile(
    r"^(Row|Rnd|Round|R)s?\.?\s*(\d+)(?:\s*[-–—]\s*\d+)?\s*[:.]?\s*(.*)$",
    re.IGNORECASE,
)
_STATED = re.compile(r"\((\d+)\)\s*$")
_META = {
    "materials", "glossary", "gauge", "yarn", "hook", "assembly",
    "note", "notes", "terms", "difficulty", "category", "pattern",
    "edging", "seam", "finishing", "introduction", "instructions",
    "abbreviations", "stitch", "stitches", "title",
}
_NOT_A_PIECE = {
    "stitch", "stitches", "round", "row", "edge", "end", "side", "top",
    "bottom", "front", "back", "loop", "inch", "span", "same", "first",
    "next", "last", "other", "following", "remaining", "hook", "yarn",
}
_US_ONLY = ("sc", "hdc")
_UK_ONLY = ("htr", "trtr")
_DEFAULT_SYMBOLS = {
    "X": "sc",
    "+": "sc",
    "V": "dc",
    "T": "hdc",
    "O": "chain",
    "•": "sl st",
}
_CHAIN = {"ch", "chain", "chains"}
_SKIPPED = (
    "chart image detector",
    "photo stitch classifier",
    "hosted language model",
    "vision training set",
    "process cluster",
)


@dataclass
class StageReport:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    engines_ran: list[str] = field(default_factory=list)
    engines_skipped: list[str] = field(default_factory=list)

    @property
    def status(self) -> str:
        if self.errors:
            return "ERROR"
        if self.warnings:
            return "PASS_WITH_WARNINGS"
        return "PASS"


def stage_findings(text: str) -> tuple[list[str], list[str]]:
    """Return errors and warnings from the written-text stages."""
    report = run_stages(text)
    return report.errors, report.warnings


def run_stages(text: str) -> StageReport:
    """Run every written-text stage in order. External engines are not called."""
    errors: list[str] = []
    warnings: list[str] = []
    errors.extend(dialect_scope(text))
    errors.extend(termination(text))
    errors.extend(reachability(text))
    errors.extend(references(text))
    errors.extend(chart_text(text))
    errors.extend(short_row_gap(text))
    warnings.extend(ambiguity(text))
    warnings.extend(gauge_band(text))
    return StageReport(
        errors=_unique(errors),
        warnings=_unique(warnings),
        engines_ran=[
            "dialect scope",
            "termination",
            "stitch reachability",
            "references",
            "chart text",
            "short-row gap",
            "ambiguity",
            "gauge band",
        ],
        engines_skipped=list(_SKIPPED),
    )


def dialect_scope(text: str) -> list[str]:
    """Flag a US/UK mix inside one piece. Pieces may declare different dialects."""
    errors = []
    pieces = _pieces(text)
    preamble = next((body for name, body in pieces if not name), "")
    default = _declared_dialect(preamble)
    for name, body in pieces:
        declared = _declared_dialect(body) or default
        us = _terms(body, _US_ONLY)
        uk = _terms(body, _UK_ONLY)
        if not us and not uk:
            continue
        label = name or "This pattern"
        if declared == "US" and uk:
            errors.append(
                f"{label} is marked US, but it uses the UK term '{uk[0]}'."
            )
        elif declared == "UK" and us:
            errors.append(
                f"{label} is marked UK, but it uses the US term '{us[0]}'."
            )
        elif declared is None and us and uk:
            errors.append(
                f"{label} mixes the US term '{us[0]}' with the UK term '{uk[0]}'."
            )
    return _unique(errors)


def termination(text: str) -> list[str]:
    """Flag a repeat that has no stitch, round, or inch stop."""
    errors = []
    for line in text.splitlines():
        if re.search(r"\bdo not\b|\bdon't\b", line, re.IGNORECASE):
            continue
        match = re.search(
            r"\b(?:repeat|continue|rep)\b(.{0,40}?)\buntil\b(.*)$",
            line,
            re.IGNORECASE,
        )
        forever = re.search(
            r"\b(?:repeat|continue|rep)\b.{0,20}\b(?:forever|indefinitely)\b",
            line,
            re.IGNORECASE,
        )
        if forever:
            errors.append("This repeat does not terminate. Give it a stitch, round, or inch stop.")
            continue
        if not match:
            continue
        clause = match.group(2)
        if re.search(r"\d|one|two|three|four|five|six|seven|eight|nine|ten|twelve", clause, re.IGNORECASE):
            continue
        errors.append(
            "This repeat does not terminate. "
            "Say the stitch count, the round count, or the length."
        )
    return _unique(errors)


def reachability(text: str) -> list[str]:
    """Flag a stitch index, skip, or leftover loop the previous round cannot reach."""
    errors = []
    previous = None
    loops: dict[int, set[str]] = {}
    for line in text.splitlines():
        stripped = line.strip()
        if _is_piece_line(stripped):
            previous = None
            loops = {}
            continue
        header = _HEADER.match(stripped)
        scope = header.group(3) if header else stripped
        number = int(header.group(2)) if header else None
        if previous is not None:
            ordinal = re.search(
                r"\b(\d+)(?:st|nd|rd|th)\s+st(?:itch)?\b",
                scope,
                re.IGNORECASE,
            )
            if ordinal and int(ordinal.group(1)) > previous:
                errors.append(
                    f"Stitch {ordinal.group(1)} is not reachable. "
                    f"The previous round has {previous} stitches."
                )
            skipped = re.search(r"\b(?:sk|skip)\s+(\d+)\b", scope, re.IGNORECASE)
            if skipped and int(skipped.group(1)) > previous:
                errors.append(
                    f"Skip of {skipped.group(1)} stitches goes past the "
                    f"{previous} stitches still live."
                )
        for match in re.finditer(
            r"\b(?:unused|free|remaining)\s+loops?\s+of\s+(?:round|rnd)\s+(\d+)\b",
            scope,
            re.IGNORECASE,
        ):
            target = int(match.group(1))
            left = loops.get(target)
            if left is not None and not left:
                errors.append(
                    f"The unused loop of Round {target} is not reachable. "
                    "That round already worked both loops."
                )
        if number is not None and previous is not None:
            loops[number - 1] = loops.get(number - 1, set())
        if header and _STATED.search(stripped):
            previous = int(_STATED.search(stripped).group(1))
            if re.search(r"\b(?:blo|flo|back loop|front loop)\b", scope, re.IGNORECASE):
                loops[number] = {"other"}
            else:
                loops[number] = set()
        elif header and previous is not None:
            loops[number] = set()
    return _unique(errors)


def references(text: str) -> list[str]:
    """Flag a named piece or round the pattern never starts."""
    errors = []
    known_rounds = {
        int(match.group(2))
        for line in text.splitlines()
        if (match := _HEADER.match(line.strip()))
    }
    known_pieces = {name.lower() for name in _piece_names(text)}
    for line in text.splitlines():
        if re.search(r"\bdo not\b|\bdon't\b", line, re.IGNORECASE):
            continue
        for match in re.finditer(
            r"\b(?:join|sew|attach|graft|see)\s+to\s+(?:round|rnd)\s+(\d+)\b",
            line,
            re.IGNORECASE,
        ):
            number = int(match.group(1))
            if number not in known_rounds:
                errors.append(f"Round {number} is named but this pattern never starts it.")
        for match in re.finditer(
            r"(?i:\b(?:sew|attach|graft)\b)[^.!\n]{0,80}?\bthe\s+([A-Z][a-z]+)\b",
            line,
        ):
            name = match.group(1)
            if name.lower() in _NOT_A_PIECE or name.lower() in known_pieces:
                continue
            errors.append(f"Piece '{name}' is named in assembly but never started.")
    return _unique(errors)


def short_row_gap(text: str) -> list[str]:
    """Flag a short-row span whose missing row-ends are not written."""
    if not re.search(r"\bshort rows?\b", text, re.IGNORECASE):
        return []
    match = re.search(
        r"\b(?:works?|worked)\s+(\d+)\s+of\s+(\d+)\b",
        text,
        re.IGNORECASE,
    )
    if not match:
        return []
    worked = int(match.group(1))
    perimeter = int(match.group(2))
    gap = perimeter - worked
    if gap <= 0:
        return []
    stated = []
    for left, right in re.findall(
        r"\b(\d+)\s+row-?ends?\b|\brow-?ends?\s*(?:\(|:)?\s*(\d+)",
        text,
        re.IGNORECASE,
    ):
        stated.append(int(left or right))
    if gap in stated or sum(stated) == gap:
        return []
    return [
        f"Short-row gap: {worked} of {perimeter} leaves {gap} row-ends unstated."
    ]


def chart_text(text: str) -> list[str]:

    """Count written chart symbols. This does not read a chart image."""
    legend = dict(_DEFAULT_SYMBOLS)
    errors = []
    for line in text.splitlines():
        if re.search(r"\blegend\b|\bsymbols\b", line, re.IGNORECASE):
            for symbol, meaning in re.findall(
                r"([A-Za-z+•])\s*=\s*([A-Za-z]+(?:\s+[A-Za-z]+)?)",
                line,
            ):
                legend[symbol] = meaning.strip().lower()
        if not re.match(r"^(?:#{1,6}\s+)?chart\b", line.strip(), re.IGNORECASE):
            continue
        if re.search(r"\blegend\b|\bsymbols\b", line, re.IGNORECASE):
            continue
        stated = _STATED.search(line.strip())
        body = re.sub(
            r"^(?:#{1,6}\s+)?chart\s+(?:row|round|rnd)?\s*\d*\s*[:.]?\s*",
            "",
            line.strip(),
            flags=re.IGNORECASE,
        )
        body = _STATED.sub("", body).strip()
        count = 0
        for token in body.split():
            meaning = legend.get(token)
            if meaning is None:
                errors.append(f"Chart symbol '{token}' is not in the legend.")
                continue
            if meaning not in _CHAIN:
                count += 1
        if stated and count != int(stated.group(1)):
            errors.append(
                f"Chart row states {stated.group(1)} stitches "
                f"but the symbols produce {count}."
            )
    return _unique(errors)


def ambiguity(text: str) -> list[str]:
    """Warn when a round names a stitch but not how many."""
    warnings = []
    for line in text.splitlines():
        header = _HEADER.match(line.strip())
        if not header:
            continue
        body = _STATED.sub("", header.group(3)).strip()
        if not body or re.search(r"\bdo not\b|\bdon't\b", body, re.IGNORECASE):
            continue
        if re.search(r"\d|\beach\b|\baround\b|\bacross\b|\bremaining\b|\bx\b|×|\btimes\b", body, re.IGNORECASE):
            continue
        if re.search(r"\b(?:sc|hdc|dc|tr|htr|inc|dec|sl\s*st)\b|\bwork even\b", body, re.IGNORECASE):
            kind = header.group(1).title()
            warnings.append(
                f"{kind} {header.group(2)} does not say how many stitches to work."
            )
    return _unique(warnings)


def gauge_band(text: str) -> list[str]:
    """Warn when a stated gauge is far outside the published crochet band."""
    weight = _weight(text)
    if weight is None:
        return []
    name, low, high = weight
    warnings = []
    for line in text.splitlines():
        match = re.search(
            r"\bgauge\b\s*:?\s*(\d+(?:\.\d+)?)\s*(?:sc|hdc|dc|tr|sts?|stitches)\b"
            r"[^.\n]{0,48}?(?:=|per)\s*4\s*(?:inches|in)\b",
            line,
            re.IGNORECASE,
        )
        if not match:
            continue
        stitches = float(match.group(1))
        if low * 0.5 <= stitches <= high * 2:
            continue
        warnings.append(
            f"Gauge {stitches:g} stitches per 4 inches is outside the "
            f"Craft Yarn Council crochet band for {name} ({low}-{high}). "
            "This is a published-range check, not a trained model."
        )
    return _unique(warnings)


def inspect_photo(
    path: str | None = None,
    confirmed_stitches: int | None = None,
    confirmed_rows: int | None = None,
) -> dict:
    """Record confirmed counts. The path is not opened and no count is invented."""
    del path
    if confirmed_stitches is None or confirmed_rows is None:
        return {
            "automatic_detection": False,
            "counts": None,
            "message": "A photo is not classified. A person must confirm the stitch and row counts.",
        }
    return {
        "automatic_detection": False,
        "counts": {"stitches": confirmed_stitches, "rows": confirmed_rows},
        "message": "Confirmed counts were recorded. The photo was not read for stitch type.",
    }


def read_chart_image() -> dict:
    """A chart picture is not detected. Written symbols are the chart stage."""
    return {
        "read": False,
        "message": "A chart image is not detected. Write the row, such as Chart row 1: X V X V (4).",
    }


def _pieces(text: str) -> list[tuple[str, str]]:
    pieces: list[tuple[str, list[str]]] = [("", [])]
    for line in text.splitlines():
        name = _piece_name(line)
        if name:
            pieces.append((name, []))
            continue
        pieces[-1][1].append(line)
    return [(name, "\n".join(lines)) for name, lines in pieces if name or any(line.strip() for line in lines)]


def _piece_names(text: str) -> list[str]:
    return [name for name in (_piece_name(line) for line in text.splitlines()) if name]


def _piece_name(line: str) -> str | None:
    stripped = re.sub(r"^#{1,6}\s+", "", line.strip())
    match = re.match(
        r"^([A-Za-z][A-Za-z0-9]*(?:\s+[A-Za-z][A-Za-z0-9]*){0,3})"
        r"(?:\s*\(make\s+\d+\))?\s*:?\s*$",
        stripped,
    )
    if not match:
        return None
    name = match.group(1).strip()
    if name.lower() in _META or name.lower() in {"round", "row", "rnd"}:
        return None
    return name


def _is_piece_line(line: str) -> bool:
    return _piece_name(line) is not None


def _declared_dialect(body: str) -> str | None:
    if re.search(r"\b(?:terms?\s*:\s*UK|UK\s+terms?|UK\s+terminology)\b", body, re.IGNORECASE):
        return "UK"
    if re.search(r"\b(?:terms?\s*:\s*US|US\s+terms?|US\s+terminology)\b", body, re.IGNORECASE):
        return "US"
    return None


def _terms(body: str, words: tuple[str, ...]) -> list[str]:
    found = []
    for line in body.splitlines():
        if re.search(r"\bdo not\b|\bdon't\b", line, re.IGNORECASE):
            continue
        if re.match(r"^[A-Za-z0-9-]+:\s+\S", line.strip()) and not _HEADER.match(line.strip()):
            continue
        for word in words:
            if re.search(rf"\b{word}\b", line, re.IGNORECASE) and word not in found:
                found.append(word)
    return found


def _weight(text: str):
    low = text.lower()
    if any(re.search(rf"\b{name}\b", low) for name in _NO_BAND) and not any(
        name in low for name, _band in _WEIGHTS
    ):
        return None
    found = []
    for name, band in _WEIGHTS:
        start = 0
        while True:
            at = low.find(name, start)
            if at < 0:
                break
            found.append((at, len(name), name, band))
            start = at + 1
    if not found:
        return None
    found.sort(key=lambda item: (-item[1], item[0]))
    chosen = []
    for at, length, name, band in found:
        if any(pos <= at and at + length <= pos + span for pos, span, _name, _band in chosen):
            continue
        chosen.append((at, length, name, band))
    chosen.sort()
    name, band = chosen[0][2], chosen[0][3]
    return name, band[0], band[1]


def _unique(items: list[str]) -> list[str]:
    found = []
    for item in items:
        if item not in found:
            found.append(item)
    return found
