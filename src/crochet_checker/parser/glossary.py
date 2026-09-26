"""
GlossaryPrePassExtractor
Extracts abbreviation definitions (like `3-tr-cl: 3 Treble Cluster`) into a local
symbol table before instruction parsing, preventing definition lines from being
tallied as executable stitches.
"""

import re
from dataclasses import dataclass


@dataclass
class GlossaryEntry:
    """Represents a glossary entry"""

    abbreviation: str
    definition: str
    stitch_count: int = 0
    line_number: int = 0
    is_complex: bool = False


class GlossaryPrePassExtractor:
    """Extracts and manages glossary definitions before pattern parsing"""

    def __init__(self):
        self.symbol_table: dict[str, GlossaryEntry] = {}
        self.complex_patterns = [
            r"\d+-[a-z]+-cl",  # e.g., 3-tr-cl
            r"\d+-[a-z]+-tog",  # e.g., 3-dc-tog
            r"[A-Z][a-z]+",  # CamelCase stitches like BPtr, FPtr
        ]

    def extract(self, text: str) -> dict[str, GlossaryEntry]:
        """
        Extract glossary definitions from text

        Returns:
            Dictionary mapping abbreviations to GlossaryEntry objects
        """
        self.symbol_table = {}
        lines = text.split("\n")

        for line_num, line in enumerate(lines, 1):
            # Look for glossary sections
            if self._is_glossary_section(line):
                # Extract definitions from following lines
                i = line_num
                while i < len(lines):
                    entry = self._parse_definition(lines[i], i + 1)
                    if entry:
                        self.symbol_table[entry.abbreviation] = entry
                    elif lines[i].strip() and not lines[i].strip().startswith("#"):
                        # Stop if we hit a non-definition line
                        break
                    i += 1

        return self.symbol_table

    def _is_glossary_section(self, line: str) -> bool:
        """Check if line starts a glossary section"""
        glossary_headers = [
            r"(?i)^(#*\s*)?(glossary|abbreviations|terms|stitch definitions)",
            r"(?i)^(#*\s*)?special\s+stitches",
        ]

        for pattern in glossary_headers:
            if re.match(pattern, line):
                return True
        return False

    def _parse_definition(self, line: str, line_num: int) -> GlossaryEntry:
        """Parse a single glossary definition line"""
        line = line.strip()
        if not line:
            return None

        # Pattern 1: "abbreviation: definition" (colon separator, safe for hyphenated abbrevs)
        match = re.match(r"^([a-zA-Z0-9\-\s]+?)\s*:\s*(.+)$", line)
        if not match:
            # Pattern 2: "abbreviation - definition" (dash must be surrounded by spaces)
            match = re.match(r"^(.+?)\s+-\s+(.+)$", line)

        if match:
            abbrev = match.group(1).strip()
            definition = match.group(2).strip()

            # Calculate stitch count from definition
            stitch_count = self._calculate_stitch_count(definition)

            # Check if it's a complex pattern
            is_complex = any(
                re.search(pattern, abbrev) for pattern in self.complex_patterns
            )

            return GlossaryEntry(
                abbreviation=abbrev,
                definition=definition,
                stitch_count=stitch_count,
                line_number=line_num,
                is_complex=is_complex,
            )

        return None

    def _calculate_stitch_count(self, definition: str) -> int:
        """Calculate the number of stitches in a definition"""
        count = 0

        # Count individual stitches
        stitch_patterns = [
            r"\b(sc|dc|hdc|tr|sl\s*st|ch)\b",
            r"\b(\d+)\s*(sc|dc|hdc|tr)",
        ]

        for pattern in stitch_patterns:
            matches = re.finditer(pattern, definition, re.IGNORECASE)
            for match in matches:
                if match.lastindex == 2:
                    # Pattern with count like "3 dc"
                    count += int(match.group(1))
                else:
                    # Single stitch
                    count += 1

        return count

    def lookup(self, abbreviation: str) -> GlossaryEntry:
        """Look up an abbreviation in the symbol table"""
        return self.symbol_table.get(abbreviation)

    def is_defined(self, abbreviation: str) -> bool:
        """Check if an abbreviation is defined"""
        return abbreviation in self.symbol_table

    def get_complex_stitches(self) -> list[GlossaryEntry]:
        """Get all complex stitch definitions"""
        return [entry for entry in self.symbol_table.values() if entry.is_complex]

    def validate_pattern_references(self, pattern_text: str) -> list[str]:
        """
        Validate that all abbreviations used in pattern are defined

        Returns:
            List of undefined abbreviations
        """
        undefined = []

        # Find all potential abbreviations in pattern
        abbrev_pattern = r"\b([a-zA-Z0-9\-]+)\b"
        matches = re.finditer(abbrev_pattern, pattern_text)

        for match in matches:
            abbrev = match.group(1)
            # Skip common words and numbers
            if not self._is_common_word(abbrev) and not self.is_defined(abbrev):
                # Check if it looks like a stitch abbreviation
                if self._looks_like_stitch_abbrev(abbrev):
                    undefined.append(abbrev)

        return list(set(undefined))

    def _is_common_word(self, word: str) -> bool:
        """Check if word is a common English word (not a stitch)"""
        common_words = {
            "in",
            "next",
            "st",
            "sts",
            "each",
            "around",
            "rep",
            "from",
            "to",
            "and",
            "the",
            "a",
            "an",
            "of",
            "into",
            "skip",
            "space",
            "round",
            "row",
            "ch",
            "sp",
            "turn",
            "work",
            "working",
        }
        return word.lower() in common_words or word.isdigit()

    def _looks_like_stitch_abbrev(self, word: str) -> bool:
        """Check if word looks like a stitch abbreviation"""
        # Stitch abbreviations are typically short, may contain hyphens,
        # and may have numbers
        if len(word) > 10:
            return False

        # Check for common stitch patterns
        stitch_patterns = [
            r"^[a-z]+$",  # Simple: sc, dc, hdc
            r"^\d+-[a-z]+",  # Numbered: 3-tr-cl
            r"^[A-Z][a-z]+",  # CamelCase: BPtr, FPtr
        ]

        return any(re.match(pattern, word) for pattern in stitch_patterns)


# Example usage
if __name__ == "__main__":
    extractor = GlossaryPrePassExtractor()

    test_text = """
## Glossary
sc: single crochet
dc: double crochet
3-tr-cl: 3 Treble Cluster (yarn over 3 times, insert hook, pull up loop, yarn over, pull through 4 loops) 3 times
BPtr: Back Post Treble
FPtr: Front Post Treble

Round 1: Ch 4, sl st to join
"""

    glossary = extractor.extract(test_text)

    print("Extracted Glossary:")
    for abbrev, entry in glossary.items():
        print(f"  {abbrev}: {entry.definition}")
        print(f"    Stitch count: {entry.stitch_count}, Complex: {entry.is_complex}")

    print("\nComplex stitches:")
    for entry in extractor.get_complex_stitches():
        print(f"  {entry.abbreviation}: {entry.definition}")
