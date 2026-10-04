"""Compare written stitch counts. Not a measured shape."""

from __future__ import annotations

from .parser import CrochetParser


def written_counts(text: str) -> list[tuple[str, int, int]]:
    """Return piece, number, and the count the checker would print."""
    pattern = CrochetParser().parse(text)
    found: list[tuple[str, int, int]] = []
    sections = []
    if pattern.pieces:
        for piece in pattern.pieces:
            sections.append((piece.name, piece.rounds or piece.rows))
    else:
        sections.append(("", pattern.rounds or pattern.rows))
    for name, items in sections:
        previous = 0
        for index, item in enumerate(items):
            number = item.round_number if hasattr(item, "round_number") else item.row_number
            counted = (
                item.computed_stitch_count
                if index == 0
                else item.compute_stitch_count_with_context(previous)
            )
            shown = counted
            for inst in item.instructions:
                if inst.stated_stitch_count is not None:
                    shown = inst.stated_stitch_count
                    break
            label = f"{name} {number}".strip() if name else str(number)
            found.append((label, number, shown))
            previous = shown
    return found


def diff_counts(left: str, right: str) -> tuple[list[str], bool]:
    """Name written count changes. A match is not a measured shape."""
    old = {label: count for label, _number, count in written_counts(left)}
    new = {label: count for label, _number, count in written_counts(right)}
    lines = [
        "Written stitch counts only. This is not a measured shape, not a cone, and not a disk."
    ]
    changed = False
    for label in list(old) + [label for label in new if label not in old]:
        if label not in old:
            lines.append(f"{label}: not in the first file, {new[label]} in the second.")
            changed = True
        elif label not in new:
            lines.append(f"{label}: {old[label]} in the first file, not in the second.")
            changed = True
        elif old[label] != new[label]:
            lines.append(f"{label}: {old[label]} to {new[label]}.")
            changed = True
    if not changed:
        lines.append("The written counts match.")
    return lines, changed
