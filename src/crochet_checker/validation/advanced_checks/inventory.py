"""Conservative BOM, section-reference, and stuffing-mass cross-checks."""

from __future__ import annotations

import math
import re

from .common import AdvancedFinding

_YARN_LABEL = re.compile(r"\bYarn\s+([A-Z][A-Z0-9-]*)\b", re.IGNORECASE)
_YARN_REFERENCE = re.compile(
    r"\b(?:yarn|colou?r)\s+([A-Z][A-Z0-9-]*)\b", re.IGNORECASE
)
_SECTION_HEADING = re.compile(
    r"^\s*(?:#{1,6}\s*)?section\s+(\d+)\b(?:\s*[-–—]\s*(\d+))?",
    re.IGNORECASE,
)
_SECTION_REFERENCE = re.compile(
    r"\bsections?\s+(\d+)\b(?:\s*[-–—]\s*(\d+))?", re.IGNORECASE
)
_STUFFING_CONTEXT = re.compile(
    r"\b(?:stuff(?:ing|er|ed)?|polyester\s+fiberfill|fiber\s*fill|fibre\s*fill|polyfill)\b",
    re.IGNORECASE,
)
_MASS = re.compile(
    r"(?P<amount>\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?)\s*"
    r"(?P<unit>kgs?|kilograms?|g|grams?)\b",
    re.IGNORECASE,
)
_SIZE_LABEL = re.compile(
    r"\b(?:finished\s+(?:size|height|length)|finished\s+figure|size|height|measurements?)\b"
    r"[^\n\d]{0,24}(\d+(?:\.\d+)?)\s*cm\b",
    re.IGNORECASE,
)
_SIZE_CONTEXT = re.compile(
    r"\b(\d+(?:\.\d+)?)\s*cm\s+(?:tall|high|plush(?:ie)?|figure)\b",
    re.IGNORECASE,
)


def _canonical_yarn(value: str) -> str:
    """Compare yarns by their explicit letter/number label when available."""
    match = _YARN_REFERENCE.search(value)
    if match:
        return f"yarn {match.group(1).casefold()}"
    stripped = value.strip()
    if re.fullmatch(r"[A-Z]", stripped, re.IGNORECASE):
        return f"yarn {stripped.casefold()}"
    return re.sub(r"[^a-z0-9]+", " ", stripped.casefold()).strip()


def validate_bom_and_stuffing_sanity(
    yarns_declared: list[str],
    yarns_referenced: list[str],
    sections_declared: list[int],
    sections_referenced: list[int],
    finished_size_cm: float,
    stuffing_grams: float,
) -> list[str]:
    """Cross-check explicit materials/section references and a broad mass bound.

    The stuffing threshold is a conservative heuristic, not a verified material
    specification: ``max(150 g, finished_size_cm**3 * 0.004)``.
    """
    warnings: list[str] = []
    referenced_yarns = {_canonical_yarn(item) for item in yarns_referenced}
    for yarn in yarns_declared:
        key = _canonical_yarn(yarn)
        if key and key not in referenced_yarns:
            warnings.append(
                f"ORPHANED YARN IN BOM: '{yarn}' is listed in Materials but never used in the pattern."
            )

    declared_sections = {int(number) for number in sections_declared}
    for number in sorted({int(value) for value in sections_referenced}):
        if number not in declared_sections:
            warnings.append(
                f"DANGLING SECTION REFERENCE: Pattern references 'Section {number}', which does not exist."
            )

    if (
        math.isfinite(finished_size_cm)
        and math.isfinite(stuffing_grams)
        and finished_size_cm > 0
        and stuffing_grams > 0
    ):
        max_plausible_stuffing_g = max(150.0, finished_size_cm**3 * 0.004)
        if stuffing_grams > max_plausible_stuffing_g:
            warnings.append(
                f"IMPLAUSIBLE STUFFING MASS: {stuffing_grams:,.0f} g "
                f"({stuffing_grams / 1000:.2f} kg) is unusually high for the broad "
                f"sanity screen (~{max_plausible_stuffing_g:,.0f} g) at a "
                f"{finished_size_cm:.0f} cm figure; this is a heuristic warning, "
                "not a precise expected fill weight."
            )
    return warnings


def _is_materials_heading(line: str) -> bool:
    value = line.strip().strip("#*_ ").rstrip(": ").casefold()
    return value in {
        "materials",
        "materials list",
        "materials and supplies",
        "materials & supplies",
    }


def _materials_block(text: str) -> tuple[list[tuple[int, str]], str]:
    lines = text.splitlines()
    start = next(
        (index for index, line in enumerate(lines) if _is_materials_heading(line)),
        None,
    )
    if start is None:
        return [], text

    end = start + 1
    while end < len(lines):
        line = lines[end]
        if re.match(r"^\s*#{1,6}\s+\S", line):
            break
        if re.match(r"^\s*(?:section\s+\d+|(?:round|rnd|row)\s+\d+)\b", line, re.IGNORECASE):
            break
        end += 1

    entries = [
        (index + 1, line)
        for index, line in enumerate(lines[start + 1 : end], start=start + 1)
        if line.strip()
    ]
    body = "\n".join(
        "" if start <= index < end else line
        for index, line in enumerate(lines)
    )
    return entries, body


def _yarn_records(entries: list[tuple[int, str]]) -> list[tuple[int, str, str, str]]:
    """Return line, display label, comparison key, and optional color name."""
    records: list[tuple[int, str, str, str]] = []
    for line_number, raw in entries:
        line = raw.strip().strip("| ").lstrip("-* ").strip()
        matches = list(_YARN_LABEL.finditer(line))
        for index, match in enumerate(matches):
            label = f"Yarn {match.group(1).upper()}"
            tail_end = matches[index + 1].start() if index + 1 < len(matches) else len(line)
            description = line[match.end() : tail_end].strip(" \t|,:;—–-()[]*")
            description = re.sub(
                r"^\d+(?:,\d{3})*(?:\.\d+)?\s*(?:kgs?|kilograms?|g|grams?)\s*",
                "",
                description,
                flags=re.IGNORECASE,
            )
            description = re.sub(
                r"\s*,?\s*\d+(?:,\d{3})*(?:\.\d+)?\s*(?:kgs?|kilograms?|g|grams?)\b.*$",
                "",
                description,
                flags=re.IGNORECASE,
            ).strip(" \t|,:;—–-()[]*")
            records.append((line_number, label, _canonical_yarn(label), description))
    return records


def _description_referenced(description: str, body: str) -> bool:
    words = re.findall(r"[A-Za-z][A-Za-z'-]*", description)
    if len(words) < 2:
        return False
    phrase = r"\b" + r"\s+".join(re.escape(word) for word in words) + r"\b"
    return bool(re.search(phrase, body, re.IGNORECASE))


def _section_sets(text: str) -> tuple[list[int], list[tuple[int, int]]]:
    declared: set[int] = set()
    referenced: list[tuple[int, int]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        heading = _SECTION_HEADING.match(line)
        if heading:
            first = int(heading.group(1))
            last = int(heading.group(2) or first)
            if last >= first and last - first <= 500:
                declared.update(range(first, last + 1))
            continue
        for match in _SECTION_REFERENCE.finditer(line):
            first = int(match.group(1))
            last = int(match.group(2) or first)
            if last >= first and last - first <= 500:
                referenced.extend((number, line_number) for number in range(first, last + 1))
    return sorted(declared), referenced


def _finished_size_cm(text: str) -> float | None:
    for pattern in (_SIZE_LABEL, _SIZE_CONTEXT):
        match = pattern.search(text)
        if match:
            size = float(match.group(1))
            if math.isfinite(size) and size > 0:
                return size
    return None


def _mass_grams(text: str) -> tuple[float, int] | None:
    for line_number, line in enumerate(text.splitlines(), start=1):
        if not _STUFFING_CONTEXT.search(line):
            continue
        match = _MASS.search(line)
        if not match:
            continue
        amount = float(match.group("amount").replace(",", ""))
        unit = match.group("unit").casefold()
        grams = amount * 1000 if unit.startswith(("kg", "kilogram")) else amount
        if math.isfinite(grams) and grams > 0:
            return grams, line_number
    return None


def inventory_findings(text: str) -> list[AdvancedFinding]:
    """Find explicit orphan yarns, dangling section refs, and extreme fill mass."""
    entries, body = _materials_block(text)
    records = _yarn_records(entries)
    referenced_yarns = {
        f"yarn {match.group(1).casefold()}"
        for match in _YARN_REFERENCE.finditer(body)
    }
    findings: list[AdvancedFinding] = []
    for line_number, label, key, description in records:
        if key in referenced_yarns or _description_referenced(description, body):
            continue
        findings.append(
            AdvancedFinding(
                "OrphanedYarn",
                f"ORPHANED YARN IN BOM: '{label}' is listed in Materials but never used in the pattern.",
                "warning",
                line_number,
            )
        )

    declared_sections, referenced_sections = _section_sets(text)
    declared_set = set(declared_sections)
    seen_missing: set[int] = set()
    for section, line_number in referenced_sections:
        if section in declared_set or section in seen_missing:
            continue
        seen_missing.add(section)
        findings.append(
            AdvancedFinding(
                "DanglingSectionReference",
                f"DANGLING SECTION REFERENCE: Pattern references 'Section {section}', which does not exist.",
                "warning",
                line_number,
            )
        )

    size = _finished_size_cm(text)
    mass = _mass_grams(text)
    if size is not None and mass is not None:
        message = validate_bom_and_stuffing_sanity([], [], declared_sections, [], size, mass[0])
        findings.extend(
            AdvancedFinding("ImplausibleStuffingMass", item, "warning", mass[1])
            for item in message
            if item.startswith("IMPLAUSIBLE STUFFING MASS:")
        )
    return findings
