"""
Glossary Extractor - Builds stitch definition tables
Extracts and processes stitch glossaries and abbreviations
"""

import re
from dataclasses import dataclass


@dataclass
class StitchDefinition:
    """Definition of a stitch technique"""

    abbreviation: str
    full_name: str
    instructions: str
    loop_count_in: int = 1  # Loops consumed
    loop_count_out: int = 1  # Loops produced
    height: int = 1  # Height in rows
    is_decrease: bool = False
    is_increase: bool = False


class GlossaryExtractor:
    """Extracts and manages stitch glossaries"""

    def __init__(self):
        self.stitch_definitions = self._build_default_glossary()

    def _build_default_glossary(self) -> dict[str, StitchDefinition]:
        """Build default stitch glossary"""
        definitions = {}

        # Basic stitches
        definitions["ch"] = StitchDefinition(
            abbreviation="ch",
            full_name="chain",
            instructions="Yarn over, pull through loop",
            loop_count_in=1,
            loop_count_out=1,
            height=0,
        )

        definitions["sl st"] = StitchDefinition(
            abbreviation="sl st",
            full_name="slip stitch",
            instructions="Insert hook, yarn over, pull through both loops",
            loop_count_in=1,
            loop_count_out=1,
            height=0,
        )

        definitions["sc"] = StitchDefinition(
            abbreviation="sc",
            full_name="single crochet",
            instructions="Insert hook, yarn over, pull up loop, yarn over, pull through 2 loops",
            loop_count_in=1,
            loop_count_out=1,
            height=1,
        )

        definitions["hdc"] = StitchDefinition(
            abbreviation="hdc",
            full_name="half double crochet",
            instructions="Yarn over, insert hook, yarn over, pull up loop, yarn over, pull through 3 loops",
            loop_count_in=1,
            loop_count_out=1,
            height=2,
        )

        definitions["dc"] = StitchDefinition(
            abbreviation="dc",
            full_name="double crochet",
            instructions="Yarn over, insert hook, yarn over, pull up loop, yarn over, pull through 2, yarn over, pull through 2",
            loop_count_in=1,
            loop_count_out=1,
            height=3,
        )

        definitions["tr"] = StitchDefinition(
            abbreviation="tr",
            full_name="treble crochet",
            instructions="Yarn over twice, insert hook, yarn over, pull up loop, *yarn over, pull through 2* repeat 3 times",
            loop_count_in=1,
            loop_count_out=1,
            height=4,
        )

        # Special stitches
        definitions["inc"] = StitchDefinition(
            abbreviation="inc",
            full_name="increase",
            instructions="Work 2 stitches into 1 stitch",
            loop_count_in=1,
            loop_count_out=2,
            height=1,
            is_increase=True,
        )

        definitions["dec"] = StitchDefinition(
            abbreviation="dec",
            full_name="decrease",
            instructions="Work 2 stitches together",
            loop_count_in=2,
            loop_count_out=1,
            height=1,
            is_decrease=True,
        )

        definitions["magic ring"] = StitchDefinition(
            abbreviation="magic ring",
            full_name="magic ring",
            instructions="Create adjustable ring, work stitches into ring, pull tail to close",
            loop_count_in=0,
            loop_count_out=0,
            height=1,
        )

        return definitions

    def extract_from_text(self, text: str) -> dict[str, StitchDefinition]:
        """Extract glossary definitions from pattern text"""
        extracted = {}
        lines = text.split("\n")

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Parse "abbreviation - definition" or "abbreviation: definition"
            match = re.match(r"^([a-z\s\-]+?)\s*[-:]\s*(.+)$", line, re.IGNORECASE)
            if match:
                abbrev = match.group(1).strip().lower()
                definition = match.group(2).strip()

                # Skip non-stitch definitions
                if any(
                    skip in abbrev
                    for skip in ["approx", "mm", "inch", "yards", "meters"]
                ):
                    continue

                # Create or update definition
                if abbrev in self.stitch_definitions:
                    # Update existing definition with custom text
                    defn = self.stitch_definitions[abbrev]
                    extracted[abbrev] = StitchDefinition(
                        abbreviation=defn.abbreviation,
                        full_name=definition if not defn.full_name else defn.full_name,
                        instructions=definition,
                        loop_count_in=defn.loop_count_in,
                        loop_count_out=defn.loop_count_out,
                        height=defn.height,
                        is_decrease=defn.is_decrease,
                        is_increase=defn.is_increase,
                    )
                else:
                    # Create new definition
                    extracted[abbrev] = StitchDefinition(
                        abbreviation=abbrev,
                        full_name=definition,
                        instructions=definition,
                        loop_count_in=1,
                        loop_count_out=1,
                        height=1,
                    )

        return extracted

    def get_definition(self, abbreviation: str) -> StitchDefinition:
        """Get stitch definition by abbreviation"""
        abbrev = abbreviation.lower().strip()
        return self.stitch_definitions.get(abbrev)

    def add_definition(self, definition: StitchDefinition):
        """Add or update a stitch definition"""
        self.stitch_definitions[definition.abbreviation.lower()] = definition

    def get_all_definitions(self) -> dict[str, StitchDefinition]:
        """Get all stitch definitions"""
        return self.stitch_definitions.copy()

    def validate_abbreviations(self, pattern_text: str) -> list[str]:
        """Validate that all abbreviations in pattern are defined"""
        undefined = []
        words = re.findall(r"\b[a-z]+\b", pattern_text.lower())

        for word in words:
            if word not in self.stitch_definitions:
                # Check if it's a common English word
                if word not in [
                    "round",
                    "row",
                    "st",
                    "sts",
                    "rep",
                    "around",
                    "next",
                    "each",
                    "in",
                    "into",
                    "skip",
                    "space",
                ]:
                    undefined.append(word)

        return list(set(undefined))


if __name__ == "__main__":
    print("📖 Glossary Extractor")
    print("=" * 60)

    extractor = GlossaryExtractor()

    # Test extraction
    test_text = """
    sc - single crochet
    dc - double crochet
    inc - increase (2 sc in same st)
    dec - decrease (sc 2 together)
    """

    extracted = extractor.extract_from_text(test_text)

    print(f"\nExtracted {len(extracted)} definitions:")
    for abbrev, defn in extracted.items():
        print(f"  {abbrev}: {defn.full_name}")

    # Test default glossary
    print(f"\nDefault glossary has {len(extractor.get_all_definitions())} definitions")

    sc_def = extractor.get_definition("sc")
    print("\nSC Definition:")
    print(f"  Full Name: {sc_def.full_name}")
    print(f"  Instructions: {sc_def.instructions}")
    print(f"  Loops In: {sc_def.loop_count_in}, Out: {sc_def.loop_count_out}")

    print("\n✅ Glossary Extractor working!")


# Legacy compatibility alias.
GlossaryExtractor.extract_glossary = GlossaryExtractor.extract_from_text
