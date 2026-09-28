"""Deterministic stages the text checker can prove.

These stages read written pattern text. They do not call a vision model,
a hosted language model, or a cluster. A photo is never assigned a stitch
count here.
"""

from __future__ import annotations

import re

from .batch import batch_findings, batch_names
from .span import span_findings, span_names
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
    warnings.extend(prose_frill(text))
    errors.extend(eyes_on_frill(text))
    errors.extend(closed_join(text))
    errors.extend(chain_underside(text))
    errors.extend(dropped_body(text))
    errors.extend(front_back_post(text))
    errors.extend(eyes_before_stuff(text))
    warnings.extend(row_end_density(text))
    errors.extend(incoming_cover(text))
    errors.extend(missing_color(text))
    errors.extend(round_order(text))
    warnings.extend(every_base(text))
    errors.extend(chain_too_short(text))
    errors.extend(unclosed_repeat(text))
    errors.extend(missing_star(text))
    errors.extend(decrease_cover(text))
    errors.extend(over_double(text))
    errors.extend(written_as_mismatch(text))
    errors.extend(eye_count(text))
    errors.extend(future_round(text))
    errors.extend(make_count(text))
    errors.extend(zero_hook(text))
    errors.extend(zero_words(text))
    errors.extend(zero_repeat(text))
    batch_errors, batch_warnings = batch_findings(text)
    errors.extend(batch_errors)
    warnings.extend(batch_warnings)
    span_errors, span_warnings = span_findings(text)
    errors.extend(span_errors)
    warnings.extend(span_warnings)
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
            "prose frill",
            "eyes on a frill",
            "closed join",
            "chain underside",
            "dropped body",
            "front and back post",
            "eyes before stuffing",
            "row-end density",
            "incoming cover",
            "missing color",
            "round order",
            "every base stitch",
            "chain length",
            "unclosed repeat",
            "missing star",
            "decrease cover",
            "over-double increase",
            "written-as count",
            "eye count",
            "future round",
            "make count",
            "zero repeat",
            *batch_names(),
            *span_names(),
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


def eyes_on_frill(text: str) -> list[str]:
    """Flag safety eyes mounted on a frill. A prohibition does not fail."""
    errors = []
    for line in text.splitlines():
        if re.search(
            r"\bdo not\b|\bdon't\b|\bnot\s+on\s+the\s+frill\b|\bshould\s+not\b|\bnot\s+be\s+mounted\b",
            line,
            re.IGNORECASE,
        ):
            continue
        if not re.search(r"\b(?:safety\s+)?eyes?\b", line, re.IGNORECASE):
            continue
        if re.search(r"\bon\s+(?:the|a)\s+frill\b", line, re.IGNORECASE):
            errors.append(
                "Safety eyes are mounted on the frill. "
                "A frill has no fabric behind it for the washer. "
                "Mount them on a solid single-crochet round."
            )
    return _unique(errors)



def closed_join(text: str) -> list[str]:
    """Flag a join into a closed tentacle, or a cinched round sewn flat."""
    errors = []
    for line in text.splitlines():
        if _prohibition(line):
            continue
        if re.search(r"\bjoin\b.{0,50}\b(?:closed|sealed)\s+tentacle\b", line, re.IGNORECASE):
            errors.append(
                "A closed tentacle has no live stitches to join. "
                "Leave an open edge and state how many stitches it holds."
            )
        if re.search(r"\bcinch\b.{0,40}\bshut\b.{0,40}\bsew\b.{0,30}\bflat\b", line, re.IGNORECASE):
            errors.append(
                "A cinched round is a sealed cap. It cannot be sewn flat. Leave the last round open."
            )
    return _unique(errors)


def chain_underside(text: str) -> list[str]:
    """Flag a stated count that needs both sides of a chain when only one is written."""
    errors = []
    for line in text.splitlines():
        if re.search(r"\bunderside\b|\bboth sides\b", line, re.IGNORECASE):
            continue
        stated = _STATED.search(line.strip())
        chains = [int(item) for item in re.findall(r"\bch\s+(\d+)\b", line, re.IGNORECASE)]
        if not stated or len(chains) != 1:
            continue
        chain = chains[0]
        across = [int(item) for item in re.findall(r"\bsc\s+(\d+)\s+across\b", line, re.IGNORECASE)]
        if sum(1 for item in across if item == chain) != 1:
            continue
        singles = [int(item) for item in re.findall(r"\bsc\s+(\d+)\b", line, re.IGNORECASE)]
        if chain not in singles:
            continue
        singles.remove(chain)
        both = sum(singles) + (2 * chain)
        if int(stated.group(1)) == both:
            errors.append(
                f"Chain underside missing: ch {chain} is crossed once, "
                f"but {both} counts both sides."
            )
    return _unique(errors)


def dropped_body(text: str) -> list[str]:
    """Flag body stitches taken from a larger count with no skip written."""
    errors = []
    for line in text.splitlines():
        match = re.search(
            r"\bwork(?:ed)?\s+(\d+)\b.{0,40}?\bfrom\s+(?:an?\s+)?(\d+)-stitch\b",
            line,
            re.IGNORECASE,
        )
        if not match:
            continue
        worked = int(match.group(1))
        source = int(match.group(2))
        gap = source - worked
        if gap <= 0:
            continue
        if re.search(rf"\bskip(?:ped)?\s+{gap}\b", line, re.IGNORECASE):
            continue
        errors.append(
            f"Dropped body stitches: {worked} worked from {source} leaves {gap} unwritten. "
            "Write the skip, or work the full count."
        )
    return _unique(errors)


def front_back_post(text: str) -> list[str]:
    """Flag a back post worked in the front loop. A quoted line is not an instruction."""
    errors = []
    for line in text.splitlines():
        if line.lstrip().startswith(">") or _prohibition(line):
            continue
        front = re.search(r"\b(?:flo|front loop)\b", line, re.IGNORECASE)
        back = re.search(r"\bbp(?:sc|hdc|dc|tr)\b", line, re.IGNORECASE)
        if front and back:
            errors.append(
                "A back post in the front loop turns the ridge inward. "
                "Use a front post if the ridge should show."
            )
    return _unique(errors)


def eyes_before_stuff(text: str) -> list[str]:
    """Flag safety eyes placed after the piece has been stuffed."""
    errors = []
    for name, body in _pieces(text):
        stuff_at = None
        eyes_at = None
        for index, line in enumerate(body.splitlines()):
            if stuff_at is None and re.search(r"\bstuff(?:ed)?\b", line, re.IGNORECASE):
                stuff_at = index
            if eyes_at is None and re.search(
                r"\b(?:insert|mount|place|attach)\b.{0,30}\beyes?\b",
                line,
                re.IGNORECASE,
            ):
                eyes_at = index
        if stuff_at is not None and eyes_at is not None and stuff_at < eyes_at:
            label = name or "This piece"
            errors.append(
                f"{label}: safety eyes are placed after stuffing. "
                "Insert them before the piece is stuffed."
            )
    return _unique(errors)


def row_end_density(text: str) -> list[str]:
    """Warn when more than 3 stitches are worked in each row end."""
    warnings = []
    for line in text.splitlines():
        if _quoted_or_explained(line):
            continue
        match = re.search(
            r"\b(\d+)\s+stitches\s+in\s+each\s+row[-\s]?ends?\b",
            line,
            re.IGNORECASE,
        )
        if not match:
            continue
        count = int(match.group(1))
        if count > 3:
            warnings.append(
                f"Row-end density: {count} stitches in each row end is above 3. "
                "The edge will bunch."
            )
    return _unique(warnings)


def incoming_cover(text: str) -> list[str]:
    """Flag a written repeat that does not consume the incoming count on the same line."""
    errors = []
    for line in text.splitlines():
        incoming = re.search(r"\bon\s+(\d+)\s+stitches\b", line, re.IGNORECASE)
        repeat = re.search(r"\(([^)]+)\)\s*[x×]\s*(\d+)", line, re.IGNORECASE)
        if not incoming or not repeat:
            continue
        available = int(incoming.group(1))
        used = _repeat_use(repeat.group(1), int(repeat.group(2)))
        if used is None or used == available:
            continue
        if re.search(rf"\bskip(?:ped)?\s+{abs(available - used)}\b", line, re.IGNORECASE):
            continue
        errors.append(
            f"Incoming cover: the repeat uses {used} of {available} stitches. "
            f"{abs(available - used)} are unaccounted for."
        )
    return _unique(errors)


def missing_color(text: str) -> list[str]:
    """Flag a Color letter used when a yarn list names other colors but not this one."""
    listed = set()
    used = []
    for line in text.splitlines():
        if line.lstrip().startswith(">"):
            continue
        defined = set(re.findall(r"\bColor\s+([A-Z])\s*:", line))
        if re.match(r"^\s*(?:[-*]\s*)?(?:yarn|materials)\b", line, re.IGNORECASE):
            defined.update(re.findall(r"\bColor\s+([A-Z])\b", line))
        if defined:
            listed.update(defined)
            continue
        used.extend(re.findall(r"\bColor\s+([A-Z])\b", line))
    if not listed:
        return []
    return _unique(
        [
            f"Color {color} is used but the yarn line never lists it."
            for color in used
            if color not in listed
        ]
    )


def round_order(text: str) -> list[str]:
    """Flag a round number that repeats or goes backwards inside one piece."""
    errors = []
    seen: set[int] = set()
    last = None
    for line in text.splitlines():
        if _is_piece_line(line):
            seen = set()
            last = None
            continue
        header = _HEADER.match(line.strip())
        if not header:
            continue
        start = int(header.group(2))
        end_match = re.search(r"\d+\s*[-–—]\s*(\d+)", line)
        end = int(end_match.group(1)) if end_match else start
        numbers = range(start, end + 1)
        if any(number in seen or (last is not None and number < last) for number in numbers):
            errors.append(
                f"Round {start} repeats or goes backwards. Number the rounds in order."
            )
        seen.update(numbers)
        last = end
    return _unique(errors)


def every_base(text: str) -> list[str]:
    """Warn when more than 2.5 stitches are worked into every base stitch."""
    warnings = []
    for line in text.splitlines():
        if _quoted_or_explained(line):
            continue
        match = re.search(
            r"\b(\d+(?:\.\d+)?)\s+stitches\s+worked\s+into\s+every\s+base\b",
            line,
            re.IGNORECASE,
        )
        if not match:
            continue
        count = float(match.group(1))
        if count > 2.5:
            warnings.append(
                f"Every base stitch is worked {count:g} times. Above 2.5x the fabric bunches."
            )
    return _unique(warnings)


def _prohibition(line: str) -> bool:
    return bool(re.search(r"\bdo not\b|\bdon't\b|\bshould\s+not\b", line, re.IGNORECASE))


def _quoted_or_explained(line: str) -> bool:
    if line.lstrip().startswith(">") or _prohibition(line):
        return True
    return bool(re.search(r"\binstead of\b|\bcreates\b|\bexcessive\b|\bstated\b", line, re.IGNORECASE))


def _repeat_use(unit: str, times: int) -> int | None:
    used = 0
    found = False
    for part in unit.split(","):
        part = part.strip()
        counted = re.search(
            r"(\d+)\s+(sc|hdc|dc|tr|inc|dec|sc2tog)\b",
            part,
            re.IGNORECASE,
        )
        bare = re.search(r"\b(sc|hdc|dc|tr|inc|dec|sc2tog)\b", part, re.IGNORECASE)
        if counted:
            count = int(counted.group(1))
            name = counted.group(2).lower()
        elif bare:
            count = 1
            name = bare.group(1).lower()
        else:
            continue
        found = True
        used += count * (2 if name in {"dec", "sc2tog"} else 1)
    if not found:
        return None
    return used * times



def chain_too_short(text: str) -> list[str]:
    """Flag a foundation chain that is shorter than the stitches worked into it."""
    errors = []
    for line in text.splitlines():
        if not re.search(r"\b2nd\s+ch\b|\beach\s+ch\b", line, re.IGNORECASE):
            continue
        chain = re.search(r"\bch\s+(\d+)\b", line, re.IGNORECASE)
        stated = _STATED.search(line.strip())
        if not chain or not stated:
            continue
        length = int(chain.group(1))
        count = int(stated.group(1))
        limit = length - 1 if re.search(r"\b2nd\s+ch\b", line, re.IGNORECASE) else length
        if count > limit:
            errors.append(
                f"Chain of {length} cannot hold {count} stitches. "
                f"The most this line can hold is {limit}."
            )
    return _unique(errors)


def unclosed_repeat(text: str) -> list[str]:
    """Flag a round whose parentheses do not balance."""
    errors = []
    for line in text.splitlines():
        header = _HEADER.match(line.strip())
        if not header:
            continue
        body = header.group(3)
        if body.count("(") != body.count(")"):
            kind = header.group(1).title()
            errors.append(
                f"{kind} {header.group(2)} has an unclosed parenthesis. Close the repeat."
            )
    return _unique(errors)


def missing_star(text: str) -> list[str]:
    """Flag rep from * when the line never opens the star."""
    errors = []
    for line in text.splitlines():
        if line.lstrip().startswith(">") or _prohibition(line):
            continue
        if not re.search(r"\brep(?:eat)?\s+from\s+\*", line, re.IGNORECASE):
            continue
        if line.count("*") < 2:
            errors.append("Rep from * has no opening star. Mark the start of the repeat with *.")
    return _unique(errors)


def decrease_cover(text: str) -> list[str]:
    """Flag a decrease repeat that does not consume the count written on the same line."""
    errors = []
    for line in text.splitlines():
        match = re.search(
            r"\bdec(?:rease)?\s*[x×]\s*(\d+)\s+on\s+(\d+)\s+stitches\b",
            line,
            re.IGNORECASE,
        )
        if not match:
            continue
        times = int(match.group(1))
        incoming = int(match.group(2))
        used = times * 2
        if used == incoming:
            continue
        errors.append(
            f"Decrease cover: dec x {times} uses {used} stitches, not {incoming}."
        )
    return _unique(errors)


def over_double(text: str) -> list[str]:
    """Flag a stated count that more than doubles the previous round."""
    errors = []
    previous = None
    for line in text.splitlines():
        if _is_piece_line(line) or line.startswith("## "):
            previous = None
            continue
        header = _HEADER.match(line.strip())
        stated = _STATED.search(line.strip()) if header else None
        if not header or not stated:
            continue
        produced = int(stated.group(1))
        if previous is not None and produced > previous * 2:
            errors.append(
                f"Round {header.group(2)} jumps from {previous} to {produced}. "
                "More than doubling in one round skips a size."
            )
        previous = produced
    return _unique(errors)


def written_as_mismatch(text: str) -> list[str]:
    """Flag an N-stitch edge that the same line writes as a different count."""
    errors = []
    for line in text.splitlines():
        if line.lstrip().startswith(">"):
            continue
        match = re.search(
            r"\b(\d+)-stitch\b.{0,80}?\bwritten\s+as\s+(\d+)\b",
            line,
            re.IGNORECASE,
        )
        if not match:
            continue
        left = int(match.group(1))
        right = int(match.group(2))
        if left != right:
            errors.append(
                f"Written count {right} does not match the {left}-stitch edge."
            )
    return _unique(errors)


def eye_count(text: str) -> list[str]:
    """Flag a mount count that disagrees with the materials count in the same section."""
    errors = []
    for section in _sections(text):
        listed = re.findall(r"safety\s+eyes?\s*\(x\s*(\d+)\)", section, re.IGNORECASE)
        mounted = re.findall(
            r"\b(?:mount|insert|place)\s+(\d+)\s+safety\s+eyes?\b",
            section,
            re.IGNORECASE,
        )
        if not listed or not mounted:
            continue
        if int(listed[0]) != int(mounted[0]):
            errors.append(
                f"Eye count: materials list {listed[0]} safety eyes, "
                f"but the instructions place {mounted[0]}."
            )
    return _unique(errors)


def future_round(text: str) -> list[str]:
    """Flag a round that works into a later round number."""
    errors = []
    for line in text.splitlines():
        header = _HEADER.match(line.strip())
        if not header:
            continue
        current = int(header.group(2))
        for match in re.finditer(r"\b(?:round|rnd)\s+(\d+)\b", header.group(3), re.IGNORECASE):
            target = int(match.group(1))
            if target > current:
                errors.append(
                    f"Round {current} works into Round {target}, which has not been made yet."
                )
    return _unique(errors)


def make_count(text: str) -> list[str]:
    """Flag sewing a different number of a piece than its make count."""
    errors = []
    for section in _sections(text):
        made = {}
        for line in section.splitlines():
            match = re.search(
                r"\b([A-Za-z][A-Za-z]+)\s*\(make\s+(\d+)\)",
                line,
                re.IGNORECASE,
            )
            if match:
                made[match.group(1).lower()] = int(match.group(2))
        for line in section.splitlines():
            if line.lstrip().startswith(">"):
                continue
            for name, count in made.items():
                found = re.search(rf"\b(\d+)\s+{name}s?\b", line, re.IGNORECASE)
                if found and int(found.group(1)) != count:
                    errors.append(
                        f"Make count: {name} is made {count} times, "
                        f"but the line uses {found.group(1)}."
                    )
    return _unique(errors)


def zero_hook(text: str) -> list[str]:
    """Flag a hook size of 0 mm in any sentence, not only "Hook: 0 mm"."""
    zero = re.compile(
        r"\bhook\b[^.\n]{0,48}?(?<![\d.])0(?:\.0+)?\s*mm\b"
        r"|(?<![\d.])0(?:\.0+)?\s*mm\b[^.\n]{0,48}?\bhook\b",
        re.IGNORECASE,
    )
    errors = []
    for line in text.splitlines():
        if line.lstrip().startswith(">") or _prohibition(line):
            continue
        if zero.search(line):
            errors.append("A hook of 0 mm cannot make a stitch.")
    return _unique(errors)



def zero_words(text: str) -> list[str]:
    """Flag zero-work and centimeter-hook lines that are not the lesson sentence."""
    chain = re.compile(r"\bch(?:ains?)?\s+(?:of\s+)?0\b", re.IGNORECASE)
    work = re.compile(r"\bwork\s+(?:0|zero)\s+stitches\b", re.IGNORECASE)
    skip = re.compile(r"\bskip\s+(?:0|zero)\b", re.IGNORECASE)
    hook_cm = re.compile(
        r"\bhook\b[^.\n]{0,24}?(?<![\d.])\d+(?:\.\d+)?\s*cm\b"
        r"|(?<![\d.])\d+(?:\.\d+)?\s*cm\s+hook\b",
        re.IGNORECASE,
    )
    errors = []
    for line in text.splitlines():
        if line.lstrip().startswith(">") or _prohibition(line):
            continue
        if chain.search(line):
            errors.append("ch 0 makes no chain.")
        if work.search(line):
            errors.append("Work 0 stitches does no work.")
        if skip.search(line):
            errors.append("Skip 0 does not move the hook.")
        if hook_cm.search(line):
            errors.append(
                "The hook is written in centimeters. "
                "Crochet hooks are written in millimeters."
            )
    return _unique(errors)


def zero_repeat(text: str) -> list[str]:
    """Flag a repeat of zero. It does no work."""
    errors = []
    for line in text.splitlines():
        if line.lstrip().startswith(">") or _prohibition(line):
            continue
        if re.search(r"\b(?:repeat|rep)\b[^.\n]{0,20}?[x×]\s*0\b|\b0\s+times\b|\bzero\s+times\b", line, re.IGNORECASE):
            errors.append("A repeat of zero does no work. Give the repeat a count above zero.")
    return _unique(errors)


def _sections(text: str) -> list[str]:
    parts = re.split(r"(?=^## )", text, flags=re.MULTILINE)
    return [part for part in parts if part.strip()]


def prose_frill(text: str) -> list[str]:

    """Warn when prose says one edge is worked more than 2.5 times full."""
    warnings = []
    for line in text.splitlines():
        if re.search(r"\bdo not\b|\bdon't\b", line, re.IGNORECASE):
            continue
        worked = re.search(
            r"\b(\d+)\s+stitches\s+worked\s+into\s+(\d+)\s+base\b",
            line,
            re.IGNORECASE,
        )
        if worked:
            made = int(worked.group(1))
            base = int(worked.group(2))
            if base > 0 and made / base > 2.5:
                warnings.append(
                    f"Prose frill: {made} stitches worked into {base} base stitches "
                    f"is {made / base:.1f}x full. Above 2.5x the edge bunches."
                )
        times = re.search(
            r"\b(\d+(?:\.\d+)?)\s+times\s+full\b",
            line,
            re.IGNORECASE,
        )
        if times and float(times.group(1)) > 2.5 and re.search(r"\bfrill\b", line, re.IGNORECASE):
            warnings.append(
                f"Prose frill: {float(times.group(1)):g} times full is above 2.5x. "
                "The edge will bunch."
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
