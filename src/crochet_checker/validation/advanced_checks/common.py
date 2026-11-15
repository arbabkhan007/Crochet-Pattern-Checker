"""Shared types/helpers for conservative advanced validation checks."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

SeverityName = Literal["error", "warning", "info"]


@dataclass(frozen=True)
class AdvancedFinding:
    """A deterministic finding supported by explicit written evidence."""

    code: str
    message: str
    severity: SeverityName = "warning"
    line_number: int = 0


ROUND_HEADER = re.compile(
    r"^\s*(?:round|rnd|r)\.?\s*(\d+)\b(?:\s*[-–—]\s*\d+)?\s*[:.)-]?\s*(.*)$",
    re.IGNORECASE,
)
ROW_HEADER = re.compile(
    r"^\s*row\.?\s*(\d+)\b(?:\s*[-–—]\s*\d+)?\s*(?:\((?:RS|WS)\)\s*)?[:.)-]?\s*(.*)$",
    re.IGNORECASE,
)
STATED_COUNT = re.compile(r"\((\d+)\)\s*$")


def split_sections(text: str) -> list[tuple[str, str, int]]:
    """Split at Markdown headings while retaining each section's first line."""
    sections: list[tuple[str, str, int]] = []
    heading = ""
    start_line = 1
    body: list[str] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        match = re.match(r"^\s*#{1,6}\s+(.+?)\s*#*\s*$", line)
        if match:
            if heading or body:
                sections.append((heading, "\n".join(body), start_line))
            heading = match.group(1).strip()
            start_line = line_number
            body = []
        else:
            body.append(line)
    if heading or body:
        sections.append((heading, "\n".join(body), start_line))
    return sections


def meaningful_lines(text: str):
    """Yield (1-based line number, line) while ignoring quotations and fences."""
    fence_marker: str | None = None
    for line_number, raw in enumerate(text.splitlines(), start=1):
        stripped = raw.strip()
        if stripped.startswith(("```", "~~~")):
            marker = stripped[:3]
            if fence_marker is None:
                fence_marker = marker
            elif marker == fence_marker:
                fence_marker = None
            continue
        if fence_marker is not None or not stripped or stripped.startswith(">"):
            continue
        yield line_number, raw


def meaningful_text(text: str) -> str:
    """Blank quoted and fenced example lines without shifting source locations."""
    keep = {line_number for line_number, _line in meaningful_lines(text)}
    return "\n".join(
        line if line_number in keep else ""
        for line_number, line in enumerate(text.splitlines(), start=1)
    )


def unique_findings(items: list[AdvancedFinding]) -> list[AdvancedFinding]:
    result: list[AdvancedFinding] = []
    seen: set[tuple[str, str, int]] = set()
    for item in items:
        key = (item.code, item.message, item.line_number)
        if key not in seen:
            result.append(item)
            seen.add(key)
    return result


def number_or_none(value: str | None) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None
