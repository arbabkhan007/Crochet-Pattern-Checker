"""
MarkdownFrontmatterSanitizer
Strips introductory text, notes, and bullet points so non-instructional markdown
isn't parsed as extra rounds (e.g., preventing "1 round, computed count 40" or ghost rounds).
"""

import re


class MarkdownFrontmatterSanitizer:
    """Sanitizes markdown by removing non-instructional content"""

    def __init__(self):
        self.frontmatter_patterns = [
            r"^#.*$",  # Headers
            r"^\s*[-*+]\s+",  # Bullet points
            r"^\s*\d+\.\s+",  # Numbered lists
            r"^\s*>",  # Blockquotes
            r"^\s*```",  # Code blocks
            r"^\s*\[.*\]\(.*\)",  # Links
            r"^\s*!\[.*\]\(.*\)",  # Images
        ]

        self.note_patterns = [
            r"(?i)\b(notes?|important|warning|tip|note:)\b",
            r"(?i)\b(make sure|remember|be careful)\b",
        ]

    def sanitize(self, markdown_text: str) -> tuple[str, list[str]]:
        """
        Sanitize markdown text by removing frontmatter and notes

        Returns:
            Tuple of (sanitized_text, removed_sections)
        """
        lines = markdown_text.split("\n")
        sanitized_lines = []
        removed_sections = []
        in_code_block = False
        current_section = []

        for line in lines:
            # Track code blocks
            if line.strip().startswith("```"):
                in_code_block = not in_code_block
                if in_code_block:
                    current_section.append(line)
                else:
                    current_section.append(line)
                    removed_sections.append("\n".join(current_section))
                    current_section = []
                continue

            # Skip content in code blocks
            if in_code_block:
                current_section.append(line)
                continue

            # Check if line is frontmatter
            is_frontmatter = False
            for pattern in self.frontmatter_patterns:
                if re.match(pattern, line):
                    is_frontmatter = True
                    break

            # Check if line is a note
            is_note = False
            for pattern in self.note_patterns:
                if re.search(pattern, line):
                    is_note = True
                    break

            if is_frontmatter or is_note:
                removed_sections.append(line)
            else:
                # Keep the line if it contains actual instructions
                if self._contains_instructions(line):
                    sanitized_lines.append(line)

        return "\n".join(sanitized_lines), removed_sections

    def _contains_instructions(self, line: str) -> bool:
        """Check if line contains actual crochet instructions"""
        instruction_patterns = [
            r"\b(ch|sc|dc|hdc|tr|sl\s*st|sp|st|rep|round|row)\b",
            r"\d+\s*(sc|dc|hdc|tr)",
            r"\*\s*.*\*",  # Repeat patterns
            r"\(\s*\d+\s*\)",  # Stitch counts
        ]

        for pattern in instruction_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                return True

        return False

    def extract_round_markers(self, text: str) -> list[tuple[int, str]]:
        """Extract round/row markers with their positions"""
        markers = []
        lines = text.split("\n")

        for i, line in enumerate(lines):
            match = re.search(r"(?i)(round|row)\s+(\d+)", line)
            if match:
                markers.append((i, line.strip()))

        return markers


# Example usage
if __name__ == "__main__":
    sanitizer = MarkdownFrontmatterSanitizer()

    test_text = """
# My Pattern

This is a beautiful pattern made with love.

## Materials
- Yarn: 100g wool
- Hook: 5mm

## Notes
Make sure to keep your tension even!

Round 1: Ch 4, sl st to join
Round 2: Ch 3, 11 dc in ring

Remember to count your stitches!
"""

    sanitized, removed = sanitizer.sanitize(test_text)
    print("Sanitized:")
    print(sanitized)
    print("\nRemoved sections:")
    for section in removed:
        print(f"  - {section[:50]}...")
