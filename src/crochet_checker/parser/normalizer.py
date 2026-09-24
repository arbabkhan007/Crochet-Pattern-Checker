"""
Normalizer for crochet pattern text.

Handles variations in how crochet patterns are written:
- Different abbreviation styles
- US vs UK terminology
- Formatting inconsistencies
- Common shorthand variations
"""

from __future__ import annotations

import re
from typing import Optional


class TerminologyDialect(str):
    """Supported terminology dialects."""

    US = "us"
    UK = "uk"


# US to UK terminology mapping
US_TO_UK: dict[str, str] = {
    "sc": "dc",
    "hdc": "tr",
    "dc": "tr",  # Note: ambiguity - US dc = UK tr
    "tr": "dtr",
    "sl st": "sl st",
    "ch": "ch",
    "single crochet": "double crochet",
    "half double crochet": "treble crochet",
    "double crochet": "treble crochet",  # Ambiguous
    "treble crochet": "double treble crochet",
}

# UK to US terminology mapping
UK_TO_US: dict[str, str] = {
    "dc": "sc",
    "tr": "hdc",
    "dtr": "tr",
    "double crochet": "single crochet",
    "treble crochet": "half double crochet",
    "double treble crochet": "treble crochet",
}


class PatternNormalizer:
    """Normalizes crochet pattern text for consistent parsing."""

    def __init__(self, source_dialect: str = TerminologyDialect.US) -> None:
        self.source_dialect = source_dialect
        self._normalizations_applied: list[str] = []

    def normalize(self, text: str) -> str:
        """
        Normalize pattern text for consistent parsing.

        Does NOT modify the original - returns a new normalized string.
        """
        self._normalizations_applied = []

        result = text

        # Normalize whitespace
        result = self._normalize_whitespace(result)

        # Normalize common symbols
        result = self._normalize_symbols(result)

        # Normalize abbreviations
        result = self._normalize_abbreviations(result)

        # Normalize case for abbreviations
        result = self._normalize_case(result)

        return result

    def _normalize_whitespace(self, text: str) -> str:
        """Normalize whitespace."""
        # Replace tabs with spaces
        result = text.replace("\t", " ")
        # Collapse multiple spaces
        result = re.sub(r"  +", " ", result)
        # Normalize line endings
        result = result.replace("\r\n", "\n").replace("\r", "\n")
        # Strip trailing whitespace per line
        lines = [line.rstrip() for line in result.split("\n")]
        result = "\n".join(lines)
        return result

    def _normalize_symbols(self, text: str) -> str:
        """Normalize special symbols."""
        result = text
        # Normalize multiplication signs
        result = result.replace("×", "x")
        # Normalize dashes
        result = result.replace("–", "-")
        result = result.replace("—", "-")
        # Normalize quotes
        result = result.replace(""", '"').replace(""", '"')
        result = result.replace("'", "'").replace("'", "'")
        return result

    def _normalize_abbreviations(self, text: str) -> str:
        """Normalize common abbreviation variations."""
        result = text

        # "2 sc in next st" -> "inc in next st" (for amigurumi style)
        # Actually keep both forms - just ensure consistency
        # "2sc" -> "inc"
        result = re.sub(r"2sc\b", "inc", result, flags=re.IGNORECASE)

        # "sc2tog" -> "dec" (single crochet two together)
        # Keep both forms, they're valid

        # "ss" or "ss" -> "sl st"
        result = re.sub(r"\bss\b", "sl st", result, flags=re.IGNORECASE)

        # "m.r." or "M.R." -> "MR"
        result = re.sub(r"\bm\.?r\.?\b", "MR", result, flags=re.IGNORECASE)

        return result

    def _normalize_case(self, text: str) -> str:
        """Normalize case - keep abbreviations lowercase."""
        # Keep the text as-is for case; the parser handles case-insensitive matching
        return text

    def detect_dialect(self, text: str) -> str:
        """
        Attempt to detect whether a pattern uses US or UK terminology.

        This is heuristic-based and may not be 100% accurate.
        """
        us_indicators = ["single crochet", "hdc", "sc2tog"]
        uk_indicators = ["double crochet", "treble crochet"]

        lower = text.lower()

        us_score = sum(1 for ind in us_indicators if ind in lower)
        uk_score = sum(1 for ind in uk_indicators if ind in lower)

        # Abbreviation-based detection
        # "sc" is US, UK uses "dc" for the same stitch
        # This is ambiguous since both are valid abbreviations
        if "single crochet" in lower:
            us_score += 3
        if "double crochet" in lower:
            uk_score += 2  # Could be either, slight UK lean

        if uk_score > us_score:
            return TerminologyDialect.UK
        return TerminologyDialect.US

    def get_normalizations(self) -> list[str]:
        """Return a list of normalizations that were applied."""
        return list(self._normalizations_applied)


def normalize_pattern(text: str, dialect: str = TerminologyDialect.US) -> str:
    """Convenience function to normalize pattern text."""
    normalizer = PatternNormalizer(source_dialect=dialect)
    return normalizer.normalize(text)
