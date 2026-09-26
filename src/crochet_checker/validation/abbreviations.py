"""
Abbreviation validation - detects invalid stitch abbreviations.
"""

from ..model.stitch import ABBREVIATION_MAP, STITCH_PRODUCTION


class AbbreviationValidator:
    """Validates stitch abbreviations in pattern instructions."""

    # Known valid abbreviations (US terms)
    VALID_ABBREVIATIONS = {
        # Basic stitches
        "ch",
        "sl st",
        "sc",
        "hdc",
        "dc",
        "tr",
        "dtr",
        # Increases/decreases
        "inc",
        "dec",
        "invdec",
        "sc2tog",
        "dc2tog",
        "hdc2tog",
        # Special stitches
        "mr",
        "magic ring",
        "fp",
        "bp",
        "fphdc",
        "bphdc",
        # Multiple stitches
        "sk",
        "sp",
        "sts",
        "st",
        # Other common
        "yo",
        "yr",
        "turn",
        "beg",
        "end",
        "rep",
        "approx",
    }

    # Add all from STITCH_PRODUCTION
    VALID_ABBREVIATIONS.update(STITCH_PRODUCTION.keys())

    # Add all from ABBREVIATION_MAP
    VALID_ABBREVIATIONS.update(ABBREVIATION_MAP.get_all_abbreviations().keys())

    def __init__(self):
        self.warnings = []
        self.errors = []

    def validate_instruction_text(self, text: str, round_number: int) -> list[dict]:
        """
        Validate abbreviations in instruction text.

        Returns list of issues found.
        """
        issues = []

        # Extract potential abbreviations from text
        words = self._extract_words(text)

        for word in words:
            word_lower = word.lower().strip(".,()[]")

            # Skip numbers and common words
            if self._should_skip(word_lower):
                continue

            # Check if it's a valid abbreviation
            if not self._is_valid_abbreviation(word_lower):
                # Check for common typos
                suggestion = self._suggest_correction(word_lower)

                issue = {
                    "type": "invalid_abbreviation",
                    "round": round_number,
                    "abbreviation": word,
                    "message": f"Unknown abbreviation '{word}'",
                    "suggestion": suggestion,
                    "severity": "error" if not suggestion else "warning",
                }
                issues.append(issue)

        return issues

    def _extract_words(self, text: str) -> list[str]:
        """Extract words from instruction text."""
        import re

        # Split on spaces and punctuation
        words = re.findall(r"\b[a-zA-Z]+\b", text)
        return words

    def _should_skip(self, word: str) -> bool:
        """Check if word should be skipped (numbers, common words, etc.)."""
        # Skip numbers
        if word.isdigit():
            return True

        # Skip common English words
        skip_words = {
            "in",
            "each",
            "around",
            "next",
            "first",
            "last",
            "same",
            "skip",
            "space",
            "stitch",
            "stitches",
            "make",
            "times",
            "repeat",
            "from",
            "to",
        }
        if word in skip_words:
            return True

        return False

    def _is_valid_abbreviation(self, word: str) -> bool:
        """Check if abbreviation is valid."""
        return word.lower() in self.VALID_ABBREVIATIONS

    def _suggest_correction(self, word: str) -> str | None:
        """Suggest correction for invalid abbreviation."""
        word_lower = word.lower()

        # Common typos and their corrections
        corrections = {
            "sse": "sl st",
            "ssc": "sl st",
            "singel": "sc",
            "simgle": "sc",
            "dobule": "dc",
            "dobble": "dc",
            "halfdouble": "hdc",
            "treble": "tr",
            "doubletr": "dtr",
            "incr": "inc",
            "decr": "dec",
            "invisable": "invdec",
            "invisible": "invdec",
            "magc": "mr",
            "magi": "mr",
            "magic": "mr",
        }

        if word_lower in corrections:
            return corrections[word_lower]

        # Check for similar abbreviations (Levenshtein distance)
        for valid in self.VALID_ABBREVIATIONS:
            if self._similar(word_lower, valid):
                return valid

        return None

    def _similar(self, s1: str, s2: str, threshold: float = 0.7) -> bool:
        """Check if two strings are similar (simple similarity check)."""
        if len(s1) < 2 or len(s2) < 2:
            return False

        # Simple character overlap check
        set1 = set(s1)
        set2 = set(s2)
        overlap = len(set1 & set2)
        total = len(set1 | set2)

        if total == 0:
            return False

        similarity = overlap / total
        return similarity >= threshold


def validate_abbreviations(pattern) -> list[dict]:
    """
    Validate abbreviations in pattern instructions.

    Args:
        pattern: Pattern object to validate

    Returns:
        List of issues found
    """
    validator = AbbreviationValidator()
    all_issues = []

    items = pattern.rounds or pattern.rows
    for item in items:
        round_num = (
            item.round_number if hasattr(item, "round_number") else item.row_number
        )

        for instruction in item.instructions:
            if hasattr(instruction, "source_text"):
                issues = validator.validate_instruction_text(
                    instruction.source_text, round_num
                )
                all_issues.extend(issues)

    return all_issues
