"""
Grammar definitions for crochet pattern instructions.

Defines the expected patterns for crochet instructions using regex and
structural rules for the parser.
"""

from __future__ import annotations

import re

# Pattern: "N stitches" or "N sc" etc.
COUNT_STITCH = re.compile(
    r"(\d+)\s+(ch|sl\s*st|sc|hdc|dc|tr|dtr|inc|dec|sc2tog|dc2tog|fpdc|bpdc)"
    r"(?:\s+(in|into|around|next|each|st|sts|rem))?",
    re.IGNORECASE,
)

# Pattern: "(stuff) x N" or "(stuff) × N"
REPEAT_BLOCK = re.compile(
    r"[\(\[]([^)\]]+)[\)\]]\s*[x×]\s*(\d+)",
    re.IGNORECASE,
)

# Pattern: "sc in each st around"
EACH_AROUND = re.compile(
    r"(sc|hdc|dc|tr|sl\s*st|inc)\s+in\s+each\s+(st|sts)\s+around",
    re.IGNORECASE,
)

# Pattern: "sc in each st around (N)" or "sc around (N)"
STATED_COUNT = re.compile(
    r"\((\d+)\)\s*$",
    re.IGNORECASE,
)

# Pattern: "N sc into magic ring" or "N sc in MR"
MAGIC_RING_START = re.compile(
    r"(\d+)\s+(sc|hdc|dc|tr)\s+(?:in|into)\s+(?:magic\s+ring|MR|magic\s+circle)",
    re.IGNORECASE,
)

# Pattern: "sc in each remaining st"
REMAINING = re.compile(
    r"(sc|hdc|dc|tr|sl\s*st|inc|dec)\s+in\s+(?:each\s+)?(?:remaining|rem)\s+(?:sts?)",
    re.IGNORECASE,
)

# Pattern: "ch N" or "ch N, turn"
CHAIN_START = re.compile(
    r"ch\s+(\d+)",
    re.IGNORECASE,
)

# Pattern: "sc in next N sts"
NEXT_N = re.compile(
    r"(sc|hdc|dc|tr|sl\s*st|inc|dec)\s+in\s+(?:each\s+)?(?:next\s+)?(\d+)\s+(sts?)",
    re.IGNORECASE,
)

# Pattern: "inc in next N sts" or "2 sc in each of next N sts"
INCREASE_PATTERN = re.compile(
    r"(?:inc|2\s+sc)\s+(?:in\s+)?(?:each\s+(?:of\s+)?(?:next\s+)?)?(\d+)?\s*(?:sts?)?",
    re.IGNORECASE,
)

# Row/Round header: "Row N:" or "Round N:" or "Rnd N:"
# Also handles ranges: "Round 11-18:" or "Rows 3-5"
ROW_HEADER = re.compile(
    r"^(Row|Rnd|Round|R)s?\.?\s*(\d+)(?:\s*[-–—]\s*R?(\d+))?\s*[:\.]?\s*(.*)",
    re.IGNORECASE,
)

# Turn instruction
TURN = re.compile(r",?\s*turn\.?", re.IGNORECASE)


def extract_stated_count(text: str) -> tuple[str, int | None]:
    """
    Extract the stated stitch count from the end of an instruction.

    Returns:
        Tuple of (text without count, stated count or None)
    """
    match = STATED_COUNT.search(text.strip())
    if match:
        count = int(match.group(1))
        clean_text = text[: match.start()].strip().rstrip(",")
        return clean_text, count
    return text, None


def is_row_header(line: str) -> tuple[bool, str, int, str, int]:
    """
    Check if a line starts with a row/round header.

    Returns:
        (is_header, type, start_number, rest_of_line, end_number)
        type is "Row", "Round", or "Rnd"
        end_number is 0 if not a range
    """
    match = ROW_HEADER.match(line.strip())
    if match:
        start = int(match.group(2))
        end = int(match.group(3)) if match.group(3) else 0
        return True, match.group(1), start, match.group(4), end
    return False, "", 0, "", 0
