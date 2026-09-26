"""
AST Lexer & Frontmatter Isolation
Strips formatting, isolates Frontmatter/Glossary/Instructions
"""

import re
from dataclasses import dataclass


@dataclass
class Section:
    """Represents a section of the pattern"""

    section_type: str  # 'glossary', 'notes', 'instructions', 'frontmatter'
    content: str
    line_number: int


class Lexer:
    """Tokenizes and isolates pattern sections"""

    def __init__(self):
        self.section_patterns = {
            "glossary": re.compile(
                r"^(glossary|abbreviations|terms|stitch definitions)", re.IGNORECASE
            ),
            "notes": re.compile(
                r"^(notes?|instructions?|special instructions)", re.IGNORECASE
            ),
            "instructions": re.compile(r"^(round|row|instructions)", re.IGNORECASE),
        }
        self.markdown_pattern = re.compile(r"[*_#`]|^\s*[-*+]\s+")
        self.round_pattern = re.compile(r"(round|row)\s+(\d+)", re.IGNORECASE)

    def tokenize(self, markdown_text: str) -> list[Section]:
        """Tokenize markdown into discrete sections"""
        sections = []
        lines = markdown_text.split("\n")
        current_section = None
        current_content = []
        line_num = 0

        for line in lines:
            line_num += 1
            stripped = line.strip()

            # Check for section header
            section_type = self._detect_section_type(stripped)

            if section_type:
                # Save previous section
                if current_section and current_content:
                    sections.append(
                        Section(
                            section_type=current_section,
                            content="\n".join(current_content),
                            line_number=line_num - len(current_content),
                        )
                    )

                # Start new section
                current_section = section_type
                current_content = [stripped]
            elif current_section:
                current_content.append(line)

        # Save last section
        if current_section and current_content:
            sections.append(
                Section(
                    section_type=current_section,
                    content="\n".join(current_content),
                    line_number=line_num - len(current_content) + 1,
                )
            )

        return sections

    def _detect_section_type(self, line: str) -> str | None:
        """Detect section type from line"""
        cleaned = self.strip_markdown(line)

        for section_type, pattern in self.section_patterns.items():
            if pattern.search(cleaned):
                return section_type

        return None

    def strip_markdown(self, text: str) -> str:
        """Strip markdown formatting"""
        return self.markdown_pattern.sub("", text).strip()

    def extract_round_number(self, line: str) -> int | None:
        """Extract round/row number from line"""
        match = self.round_pattern.search(line)
        if match:
            return int(match.group(2))
        return None

    def isolate_glossary(self, sections: list[Section]) -> dict[str, str]:
        """Extract glossary definitions from sections"""
        glossary = {}

        for section in sections:
            if section.section_type == "glossary":
                lines = section.content.split("\n")
                for line in lines:
                    # Parse "abbreviation: definition" or "abbreviation - definition"
                    match = re.match(r"^\s*([^:]+?)\s*[:\-]\s*(.+?)\s*$", line)
                    if match:
                        abbrev = self.strip_markdown(match.group(1)).strip()
                        definition = match.group(2).strip()
                        if abbrev and not abbrev.lower().startswith(
                            ("round", "row", "note")
                        ):
                            glossary[abbrev] = definition

        return glossary

    def isolate_instructions(self, sections: list[Section]) -> list[tuple[int, str]]:
        """Extract instruction lines with line numbers"""
        instructions = []

        for section in sections:
            if section.section_type == "instructions":
                lines = section.content.split("\n")
                for i, line in enumerate(lines):
                    round_num = self.extract_round_number(line)
                    if round_num:
                        instructions.append((section.line_number + i, line))

        return instructions


if __name__ == "__main__":
    print("🔤 Lexer Test")
    lexer = Lexer()

    test_pattern = """
# Test Pattern

## Glossary
sc: single crochet
dc: double crochet
3-tr-cl: 3 Treble Cluster

## Notes
Work in continuous rounds

## Instructions
Round 1: 6 sc in magic ring
Round 2: 2 sc in each st around
"""

    sections = lexer.tokenize(test_pattern)
    print(f"Found {len(sections)} sections")

    glossary = lexer.isolate_glossary(sections)
    print(f"Glossary: {glossary}")

    instructions = lexer.isolate_instructions(sections)
    print(f"Instructions: {len(instructions)} rounds")
