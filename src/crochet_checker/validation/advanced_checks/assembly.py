"""Construction-mode classification and complete numbered assembly ingestion."""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum

from .common import AdvancedFinding, split_sections


class ConstructionMode(str, Enum):
    UNKNOWN = "UNKNOWN"
    INLINE_COLORWORK = "INLINE_COLORWORK"
    DIRECT_SURFACE_JOIN = "DIRECT_SURFACE_JOIN"
    JAYG_ATTACHED = "JAYG_ATTACHED"
    SEPARATE_SEW_ON = "SEPARATE_SEW_ON"


@dataclass(frozen=True)
class AssemblyStep:
    number: int
    piece_name: str | None
    target_parent: str | None
    target_round_min: int | None
    target_round_max: int | None
    source: str
    line_number: int


@dataclass(frozen=True)
class PieceConstruction:
    name: str
    mode: ConstructionMode
    body: str
    line_number: int


def _clean_name(name: str) -> str:
    value = re.sub(r"\(\s*make\s+\d+\s*\)", "", name, flags=re.IGNORECASE)
    value = re.sub(r"\s*\(.*?\)\s*$", "", value)
    return value.strip(" :#\t")


def classify_construction_mode(name: str, body: str) -> ConstructionMode:
    """Classify only construction modes supported by explicit written wording."""
    scope = f"{name}\n{body}"
    if re.search(
        r"\b(?:inline\s+colorwork|tapestry\s+(?:panel|colorwork)|worked\s+inline|worked\s+as\s+part\s+of)\b",
        scope,
        re.IGNORECASE,
    ) or (
        re.search(r"\btapestry\b", scope, re.IGNORECASE)
        and re.search(
            r"\b(?:inside|within|part\s+of)\s+(?:the\s+)?(?:torso|body|main\s+piece)\b",
            body,
            re.IGNORECASE,
        )
    ):
        return ConstructionMode.INLINE_COLORWORK
    if re.search(r"\b(?:JAYG|join\s+as\s+you\s+go)\b", scope, re.IGNORECASE):
        return ConstructionMode.JAYG_ATTACHED
    if re.search(
        r"\b(?:sl\s*st|slip\s+stitch)\b[^.\n]{0,55}\b(?:directly\s+)?(?:to|into|onto)\s+(?:the\s+)?(?:torso|body|head|piece)\b|\bjoined\s+directly\s+(?:to|into)\b",
        scope,
        re.IGNORECASE,
    ):
        return ConstructionMode.DIRECT_SURFACE_JOIN
    if re.search(
        r"\b(?:make|made|crochet(?:ed)?|work(?:ed)?)\s+separately\b|"
        r"\bseparate(?:ly)?\s+piece\b|\bmade\s+as\s+a\s+separate\s+piece\b",
        scope,
        re.IGNORECASE,
    ):
        return ConstructionMode.SEPARATE_SEW_ON
    return ConstructionMode.UNKNOWN


def _piece_sections(text: str) -> list[PieceConstruction]:
    result: list[PieceConstruction] = []
    for heading, body, line in split_sections(text):
        if not heading or re.search(
            r"\b(?:materials|gauge|glossary|notes?|final\s+assembly|assembly|finishing|instructions)\b",
            heading,
            re.IGNORECASE,
        ):
            continue
        name = _clean_name(heading)
        if not name:
            continue
        # Keep heading annotations such as "(make separately)" for classification.
        mode = classify_construction_mode(heading, body)
        result.append(PieceConstruction(name, mode, body, line))
    return result


def _is_assembly_heading(line: str) -> bool:
    value = re.sub(r"^\s*#{1,6}\s*", "", line)
    value = re.sub(r"\s*#*\s*$", "", value).strip(" :\t")
    return bool(
        re.fullmatch(
            r"(?:final\s+)?assembly(?:\s+(?:steps|instructions))?",
            value,
            re.IGNORECASE,
        )
    )


def _has_assembly_section(text: str) -> bool:
    return any(_is_assembly_heading(line) for line in text.splitlines())


def _name_pattern(name: str) -> re.Pattern[str]:
    words = [re.escape(word) for word in name.split() if word]
    return re.compile(r"(?<!\w)" + r"\s+".join(words) + r"(?!\w)", re.IGNORECASE)


def _subject_piece_names(source: str, names: list[str]) -> list[str]:
    """Return named pieces before the first explicit attachment target phrase."""
    action = re.search(
        r"\b(?:sew|attach|join|graft|stitch|fasten|connect|secure|place|add)\w*\b",
        source,
        re.IGNORECASE,
    )
    if not action:
        return []
    target = re.search(
        r"\b(?:to|onto|into|on|around|with|together)\b",
        source[action.end() :],
        re.IGNORECASE,
    )
    end = action.end() + target.start() if target else len(source)
    mentions: list[tuple[int, str]] = []
    for name in names:
        for match in _name_pattern(name).finditer(source, action.end(), end):
            mentions.append((match.start(), name))
    result: list[str] = []
    seen_positions: set[int] = set()
    for position, name in sorted(mentions, key=lambda item: (item[0], -len(item[1]))):
        if position in seen_positions:
            continue
        seen_positions.add(position)
        if name.casefold() not in {item.casefold() for item in result}:
            result.append(name)
    return result


def parse_numbered_assembly_steps(text: str) -> list[AssemblyStep]:
    """Read every numbered item in Markdown or plain-text assembly sections."""
    pieces = _piece_sections(text)
    names = sorted((piece.name for piece in pieces), key=len, reverse=True)
    round_range = re.compile(
        r"\b(?:rounds?|rnds?|r)\s*(\d+)\s*(?:[-–—]|to|through|and)\s*(?:r\s*)?(\d+)\b",
        re.IGNORECASE,
    )
    round_single = re.compile(r"\b(?:round|rnd|r)\s*(\d+)\b", re.IGNORECASE)
    target_pattern = re.compile(
        r"\b(?:to|onto|into|on|around)\s+(?:the\s+)?([A-Za-z][A-Za-z -]{0,30}?)"
        r"(?=\s+(?:at|between|round|rnd|and|with)\b|[,.;]|$)",
        re.IGNORECASE,
    )

    steps: list[AssemblyStep] = []
    active = False
    assembly_level: int | None = None
    for line_number, line in enumerate(text.splitlines(), start=1):
        markdown_heading = re.match(r"^\s*(#{1,6})\s*", line)
        if markdown_heading:
            level = len(markdown_heading.group(1))
            if _is_assembly_heading(line):
                active = True
                assembly_level = level
            elif (
                active
                and assembly_level is not None
                and assembly_level > 0
                and level > assembly_level
            ):
                # Keep nested headings inside the current assembly section.
                pass
            else:
                active = False
                assembly_level = None
            continue
        if _is_assembly_heading(line):
            active = True
            assembly_level = 0
            continue
        if not active:
            continue
        numbered = re.match(r"^\s*(\d+)\s*[.)]\s+(.+)$", line)
        if not numbered:
            continue
        number = int(numbered.group(1))
        source = numbered.group(2).strip()
        subject_names = _subject_piece_names(source, names)
        target_match = target_pattern.search(source)
        target_parent = target_match.group(1).strip() if target_match else None
        range_match = round_range.search(source)
        if range_match:
            r0, r1 = sorted((int(range_match.group(1)), int(range_match.group(2))))
        else:
            single = round_single.search(source)
            r0 = r1 = int(single.group(1)) if single else None
        steps.append(
            AssemblyStep(
                number,
                subject_names[0] if subject_names else None,
                target_parent,
                r0,
                r1,
                source,
                line_number,
            )
        )
    return steps


_LOCAL_ATTACHMENT = re.compile(
    r"\b(?:sew|attach|graft|stitch|join)\w*\b[^.\n]{0,80}?"
    r"\b(?:to|onto|into|on)\s+(?:the\s+)?"
    r"(?:body|torso|head|face|chest|back|main\s+piece|"
    r"(?:side|top|bottom|front|back)\s+of\s+(?:the\s+)?(?:body|torso))\b",
    re.IGNORECASE,
)


def assembly_findings(text: str) -> list[AdvancedFinding]:
    """Warn when an explicitly separate piece lacks a placement instruction."""
    if not _has_assembly_section(text):
        return []
    pieces = _piece_sections(text)
    steps = parse_numbered_assembly_steps(text)
    names = [piece.name for piece in pieces]
    attached_by_steps = {
        name.casefold()
        for step in steps
        for name in _subject_piece_names(step.source, names)
    }

    findings: list[AdvancedFinding] = []
    for piece in pieces:
        if piece.mode != ConstructionMode.SEPARATE_SEW_ON:
            continue
        if (
            _LOCAL_ATTACHMENT.search(piece.body)
            or piece.name.casefold() in attached_by_steps
        ):
            continue
        findings.append(
            AdvancedFinding(
                "MissingSeparatePieceAssemblyStep",
                f"'{piece.name}' is explicitly made separately but no sewing/placement instruction for it was found in its section or numbered Final Assembly steps.",
                "warning",
                piece.line_number,
            )
        )
    return findings
