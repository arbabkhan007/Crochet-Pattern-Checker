"""Stitch-conservation checks for explicit piece joins."""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class JoinInterface:
    parent_piece: str
    child_piece: str
    skipped_parent_sts: int
    leftover_child_sts: int


def validate_join_interface(interface: JoinInterface) -> list[str]:
    """A join closes only when skipped parent stitches equal unjoined child stitches."""
    if interface.skipped_parent_sts != interface.leftover_child_sts:
        return [
            (
                f"Join imbalance between {interface.parent_piece} and "
                f"{interface.child_piece}: parent skipped "
                f"{interface.skipped_parent_sts} stitches, but child left "
                f"{interface.leftover_child_sts} unjoined stitches."
            )
        ]
    return []


_SKIP = re.compile(r"skip(?:ped)?\s+(\d+)\s+st", re.IGNORECASE)
_OTHER = re.compile(
    r"(?:join(?:ed)?|sew(?:n|ed)?|attach(?:ed)?|leav(?:e|ing)|left(?:over)?)\s+"
    r"(\d+)\s+(?:unjoined\s+)?st",
    re.IGNORECASE,
)
_NAME = re.compile(r"\b([A-Z][a-z]+|[A-Z]{2,})\b")
_SKIP_NAMES = {"Join", "Sew", "Attach", "Skip", "Leave", "Leaving", "The", "And"}


def find_join_interfaces(text: str) -> list[JoinInterface]:
    found: list[JoinInterface] = []
    for line in text.splitlines():
        skipped = _SKIP.search(line)
        other = _OTHER.search(line)
        if not skipped or not other:
            continue
        names = [name for name in _NAME.findall(line) if name not in _SKIP_NAMES]
        parent = names[0] if names else "parent"
        child = names[1] if len(names) > 1 else "child"
        found.append(
            JoinInterface(parent, child, int(skipped.group(1)), int(other.group(1)))
        )
    return found


def join_interface_errors(text: str) -> list[str]:
    errors: list[str] = []
    for interface in find_join_interfaces(text):
        errors.extend(validate_join_interface(interface))
    return errors
