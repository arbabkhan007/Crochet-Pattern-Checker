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
    return notes
