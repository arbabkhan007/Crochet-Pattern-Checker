"""Commercial audit rules that the stitch counter does not cover.

These checks read the pattern text. They do not change stitch math.
A passing circle stays a passing circle. A wrong stated count stays an error.
"""

from __future__ import annotations

import re

_STANDARD = {
    "ch", "sl", "st", "slst", "sc", "hdc", "dc", "tr", "dtr",
    "inc", "dec", "sc2tog", "hdc2tog", "dc2tog", "invdec",
    "mr", "blo", "flo", "fpdc", "bpdc", "fphdc", "bphdc", "fptr", "bptr",
    "fpsc", "bpsc", "yo", "sk", "sp", "sts", "tog", "rep", "cl",
    "picot", "bobble", "popcorn", "shell", "puff", "turn", "beg",
}
_STOP = {
    "in", "each", "around", "across", "next", "the", "and", "to", "of",
    "from", "hook", "magic", "ring", "into", "first", "join", "with",
    "make", "row", "round", "rnd", "rows", "rounds", "turn", "then",
    "remaining", "rem", "stitch", "stitches", "space", "skip", "same",
    "all", "end", "ends", "fasten", "off", "stuff", "sew", "attach",
}
_PLACEMENT = (
    "safety eye", "safety eyes", "eye", "eyes", "button", "buttons",
    "snap", "snaps", "bell", "squeaker", "nose", "wire", "pipe cleaner",
    "bead", "beads", "ribbon", "felt", "embroidery",
)
_UNIVERSAL = {"yarn", "hook", "scissors", "needle", "marker", "markers"}
_HEIGHT = {
    "sc": 1.0, "hdc": 1.5, "dc": 2.0, "tr": 3.0, "dtr": 4.0,
    "fpsc": 1.0, "bpsc": 1.0, "fphdc": 1.5, "bphdc": 1.5,
    "fpdc": 2.0, "bpdc": 2.0, "fptr": 3.0, "bptr": 3.0,
}
_POST = re.compile(r"\b((?:fp|bp)(?:sc|hdc|dc|tr|dtr))\b", re.IGNORECASE)
_HEADER = re.compile(
    r"^(Row|Rnd|Round|R)s?\.?\s*(\d+)(?:\s*[-–—]\s*\d+)?\s*[:.]?\s*(.*)$",
    re.IGNORECASE,
)
_PIECE = re.compile(
    r"^(?:#{2,6}\s+.+|[A-Z][A-Za-z /,&-]{0,40}\s*\(make\s+\d+\)\s*:?)\s*$"
)
_REPEAT = re.compile(
    r"^[\[(](.+)[\])]\s*(?:[x×]\s*(\d+)|(\d+)\s+times)\s*$",
    re.IGNORECASE,
)
_STATED = re.compile(r"\((\d+)\)\s*$")


def _messages(items: list[str]) -> list[str]:
    found: list[str] = []
    for item in items:
        if item not in found:
            found.append(item)
    return found


class GhostMaterialLinter:
    """Flag placement materials that the instructions never mention."""

    def lint(self, text: str) -> list[str]:
        section, body = _materials_section(text)
        if not section:
            return []
        errors = []
        for item in _material_items(section):
            if _is_universal_tool(item):
                continue
            noun = _placement_noun(item)
            if not noun:
                continue
            if noun.lower() not in body.lower():
                errors.append(
                    f"Ghost material: '{item}' is listed under Materials "
                    f"but never mentioned in the instructions."
                )
        return _messages(errors)


class GlossaryLinter:
    """Flag glossary terms that are unused, and stitch tokens that are undefined."""

    def lint(self, text: str) -> list[str]:
        defined = _glossary_terms(text)
        body = _without_glossary(text)
        errors = []
        for term in defined:
            if not re.search(rf"(?<![A-Za-z0-9-]){re.escape(term)}(?![A-Za-z0-9-])", body, re.IGNORECASE):
                errors.append(f"Glossary defines '{term}' but it is never used.")
        defined_keys = {term.lower() for term in defined}
        for token in _instruction_tokens(body):
            key = token.lower()
            if key in _STANDARD or key in defined_keys or key in _STOP:
                continue
            if not _looks_like_abbreviation(key):
                continue
            errors.append(
                f"Undefined abbreviation '{token}' is used but not defined in the glossary."
            )
        return _messages(errors)


class ModuloDriftChecker:
    """Warn when a decrease repeat does not tile the previous stitch count."""

    def check(self, text: str) -> list[str]:
        warnings = []
        for label, previous, body in _round_bodies(text):
            if previous is None:
                continue
            match = _REPEAT.match(body.strip())
            if not match:
                continue
            unit = match.group(1)
            if re.search(r"\binc\b", unit, re.IGNORECASE):
                continue
            consumed = _unit_consumption(unit)
            if not consumed or previous % consumed == 0:
                continue
            leftover = previous % consumed
            warnings.append(
                f"Non-modulo consumption: {label} has {previous} incoming stitches, "
                f"but the repeat consumes {consumed}. {leftover} stitch"
                f"{'' if leftover == 1 else 'es'} would be left unworked."
            )
        return _messages(warnings)


class PostStitchFoundationValidator:
    """Post stitches need a previous row at least as tall as hdc."""

    def validate(self, text: str) -> list[str]:
        errors = []
        previous_height = None
        for line in text.splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            if _PIECE.match(stripped) or re.match(r"^#{2,6}\s+\S", stripped):
                previous_height = None
                continue
            header = _HEADER.match(stripped)
            if not header:
                continue
            body = header.group(3)
            posts = [item.lower() for item in _POST.findall(body)]
            if posts and (previous_height is None or previous_height < 1.5):
                target = "no previous row" if previous_height is None else "a short sc row"
                shown = ", ".join(sorted(set(posts)))
                errors.append(
                    f"Post stitch {shown} is worked into {target}. "
                    f"Post stitches need a foundation of hdc or taller."
                )
            height = _line_height(body)
            if height is not None:
                previous_height = height
        return _messages(errors)


class SpatialFitChecker:
    """A tab must not be wider than the skipped-chain socket it enters."""

    def check(self, text: str) -> list[str]:
        sockets = [int(n) for n in re.findall(
            r"skip(?:ped)?\s+(\d+)\s+ch(?:ains?)?", text, re.IGNORECASE
        )]
        tabs = _tab_widths(text)
        if not sockets or not tabs:
            return []
        errors = []
        if len(sockets) == 1:
            pairs = [(name, width, sockets[0]) for name, width in tabs]
        else:
            pairs = [
                (name, width, socket)
                for (name, width), socket in zip(tabs, sockets)
            ]
        for name, width, socket in pairs:
            if width > socket:
                errors.append(
                    f"Spatial fit: {name} insertion is {width} stitches, "
                    f"wider than the {socket}-chain socket."
                )
        return _messages(errors)


class ShortRowPerimeterChecker:
    """Short-row turns create vertical sites the horizontal count does not see."""

    def check(self, text: str) -> list[str]:
        has_short = re.search(
            r"\b(?:row|round|rnd)s?\s+\d+[a-z]\b", text, re.IGNORECASE
        )
        has_turn = re.search(r"\bturn\b", text, re.IGNORECASE)
        has_count = re.search(
            r"row[-\s]?ends?\s*(?:\(|:)?\s*\d+", text, re.IGNORECASE
        )
        if has_short and has_turn and not has_count:
            return [
                "Short-row turns create vertical row-end sites, "
                "but no row-end stitch count is stated."
            ]
        return []


def audit_findings(text: str) -> tuple[list[str], list[str]]:
    """Return (errors, warnings) for the commercial audit rules."""
    errors: list[str] = []
    warnings: list[str] = []
    errors.extend(GhostMaterialLinter().lint(text))
    errors.extend(GlossaryLinter().lint(text))
    errors.extend(PostStitchFoundationValidator().validate(text))
    errors.extend(SpatialFitChecker().check(text))
    warnings.extend(ModuloDriftChecker().check(text))
    warnings.extend(ShortRowPerimeterChecker().check(text))
    return _messages(errors), _messages(warnings)


def _materials_section(text: str) -> tuple[str, str]:
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if re.match(r"^#{0,3}\s*materials\s*:?\s*$", line.strip(), re.IGNORECASE):
            start = index
            break
    if start is None:
        return "", text
    collected = []
    end = start + 1
    for line in lines[start + 1:]:
        if _HEADER.match(line.strip()) or re.match(r"^#{1,6}\s+\S", line.strip()):
            break
        if line.strip() == "" and collected:
            break
        collected.append(line)
        end += 1
    body = "\n".join(lines[:start] + lines[end:])
    return "\n".join(collected), body


def _material_items(section: str) -> list[str]:
    items = []
    for raw in section.splitlines():
        line = raw.strip().lstrip("-*").strip()
        if not line:
            continue
        line = re.sub(r"^\d+\s*(?:x|mm|cm)?\s*", "", line, flags=re.IGNORECASE).strip()
        if line:
            items.append(line)
    return items


def _is_universal_tool(item: str) -> bool:
    words = {word.lower() for word in re.findall(r"[A-Za-z]+", item)}
    return bool(words) and words <= (_UNIVERSAL | {"weight", "mm", "size", "for", "and", "the", "a"})


def _placement_noun(item: str) -> str | None:
    low = item.lower()
    for noun in sorted(_PLACEMENT, key=len, reverse=True):
        if noun in low:
            return noun
    return None


def _glossary_terms(text: str) -> list[str]:
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if re.match(r"^#{0,3}\s*glossary\s*:?\s*$", line.strip(), re.IGNORECASE):
            start = index
            break
    if start is None:
        return []
    terms = []
    for line in lines[start + 1:]:
        stripped = line.strip()
        if not stripped:
            if terms:
                break
            continue
        if _HEADER.match(stripped) or re.match(r"^#{1,6}\s+\S", stripped):
            break
        match = re.match(r"^([A-Za-z0-9]+(?:-[A-Za-z0-9]+)*)\s*:\s+\S", stripped)
        if match:
            terms.append(match.group(1))
    return terms


def _without_glossary(text: str) -> str:
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if re.match(r"^#{0,3}\s*glossary\s*:?\s*$", line.strip(), re.IGNORECASE):
            start = index
            break
    if start is None:
        return text
    end = start + 1
    for line in lines[start + 1:]:
        stripped = line.strip()
        if not stripped and end > start + 1:
            break
        if _HEADER.match(stripped) or re.match(r"^#{1,6}\s+\S", stripped):
            break
        end += 1
    return "\n".join(lines[:start] + lines[end:])


def _instruction_tokens(text: str) -> list[str]:
    tokens = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or not _HEADER.match(stripped):
            continue
        body = _HEADER.match(stripped).group(3)
        for match in re.finditer(r"\d+-[A-Za-z0-9-]+", body):
            tokens.append(match.group(0))
        for match in re.finditer(r"[A-Za-z][A-Za-z0-9]*(?:-[A-Za-z0-9]+)*", body):
            if match.start() > 0 and body[match.start() - 1] in "-0123456789":
                continue
            if match.group(0).lower() in {"nd", "rd", "st", "th"}:
                continue
            tokens.append(match.group(0))
    return tokens


def _looks_like_abbreviation(token: str) -> bool:
    if "-" in token:
        return True
    if token in _STOP or token in _STANDARD:
        return False
    return 2 <= len(token) <= 8 and token.isalpha() and token not in _STOP


def _round_bodies(text: str):
    """Yield label, previous produced count, and the instruction body."""
    try:
        from ..parser.parser import parse_pattern
        from .validator import _produced_with_context
    except Exception:
        return
    parsed = parse_pattern(text)
    if parsed.pieces and len(parsed.pieces) > 1:
        groups = [piece.rounds or piece.rows for piece in parsed.pieces if piece.rounds or piece.rows]
    else:
        groups = [parsed.rounds or parsed.rows]
    for group in groups:
        previous = None
        for item in group:
            raw = getattr(item, "source_text", "") or ""
            header = _HEADER.match(raw.strip())
            body = header.group(3) if header else raw.strip()
            body = _STATED.sub("", body).strip()
            number = getattr(item, "round_number", getattr(item, "row_number", "?"))
            kind = "Round" if hasattr(item, "round_number") else "Row"
            yield f"{kind} {number}", previous, body
            total = 0
            available = previous
            for instruction in item.instructions:
                total += _produced_with_context(instruction, available)
                if any(
                    getattr(op, "into_stitch", None) in ("each_stitch_around", "each_stitch_across", "remaining")
                    for op in instruction.operations
                ):
                    available = 0
                elif available is not None:
                    available -= instruction.total_stitches_consumed
            previous = total


def _unit_consumption(unit: str) -> int | None:
    flat = unit
    previous = None
    while previous != flat:
        previous = flat
        flat = re.sub(
            r"[\[(]([^\[\]()]+)[\])]\s*[x×]\s*(\d+)",
            lambda match: ", ".join([match.group(1)] * int(match.group(2))),
            flat,
            flags=re.IGNORECASE,
        )
    stitch = (
        r"sc2tog|hdc2tog|dc2tog|fpdc|bpdc|fphdc|bphdc|fptr|bptr|fpsc|bpsc|"
        r"hdc|dtr|inc|dec|sc|dc|tr|ch|sl\s*st"
    )
    total = 0
    found = False
    for part in flat.split(","):
        part = part.strip()
        if not part:
            continue
        count = 1
        name = None
        counted = re.search(rf"(\d+)\s+({stitch})\b", part, re.IGNORECASE)
        named = re.search(rf"\b({stitch})\s+(\d+)", part, re.IGNORECASE)
        bare = re.search(rf"\b({stitch})\b", part, re.IGNORECASE)
        if counted:
            count = int(counted.group(1))
            name = counted.group(2)
        elif named:
            name = named.group(1)
            count = int(named.group(2))
        elif bare:
            name = bare.group(1)
        if not name:
            continue
        found = True
        key = re.sub(r"\s+", "", name.lower())
        if key in {"dec", "sc2tog", "hdc2tog", "dc2tog"}:
            total += 2 * count
        elif key == "ch":
            total += 0
        else:
            total += count
    if not found or total <= 0:
        return None
    return total


def _line_height(body: str) -> float | None:
    found = []
    for match in re.finditer(
        r"\b(fpdc|bpdc|fphdc|bphdc|fptr|bptr|fpsc|bpsc|hdc|dtr|sc|dc|tr)\b",
        body,
        re.IGNORECASE,
    ):
        found.append(_HEIGHT[match.group(1).lower()])
    if not found:
        return None
    return max(found)


def _tab_widths(text: str) -> list[tuple[str, int]]:
    lines = text.splitlines()
    tabs = []
    for index, line in enumerate(lines):
        if not re.search(r"\b(tab|insertion)\b", line, re.IGNORECASE):
            continue
        if _HEADER.match(line.strip()):
            continue
        for nxt in lines[index + 1:index + 8]:
            if not nxt.strip():
                continue
            stated = _STATED.search(nxt.strip())
            counted = re.search(r"\b(\d+)\s+(?:sc|hdc|dc|tr)\b", nxt, re.IGNORECASE)
            if stated:
                tabs.append((_piece_name(line), int(stated.group(1))))
                break
            if counted:
                tabs.append((_piece_name(line), int(counted.group(1))))
                break
    return tabs


def _piece_name(line: str) -> str:
    name = re.sub(r"^#+\s*", "", line.strip())
    name = re.sub(r"\s*\(make\s+\d+\)\s*:?\s*$", "", name, flags=re.IGNORECASE)
    return name.strip() or "Tab"
