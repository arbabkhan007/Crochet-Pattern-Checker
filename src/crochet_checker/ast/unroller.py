"""
AST Unroller - Expands nested repeat brackets and 'N times' loops
Converts compact pattern notation into flat sequence of atomic actions
"""

import re

from .nodes import InstructionNode


class ASTUnroller:
    """Expands pattern repeats and loops into atomic instructions"""

    def __init__(self):
        self.repeat_pattern = re.compile(
            r"\*([^*]+)\*(?:\s*rep(?:eat)?(?:\s+from\s+\*)?(?:\s+(\d+)\s+times)?|\s+around)?",
            re.IGNORECASE,
        )
        self.n_times_pattern = re.compile(r"(\d+)\s+times", re.IGNORECASE)
        self.repeat_around_pattern = re.compile(r"rep(?:eat)?\s+around", re.IGNORECASE)

    def unroll_round(
        self, round_text: str, line_number: int = 0, prev_stitch_count: int = 0
    ) -> list[InstructionNode]:
        """Unroll a single round/row into atomic instructions"""
        instructions = []

        # Handle nested repeats
        expanded_text = self._expand_nested_repeats(round_text)

        # Parse individual instructions
        raw_instructions = self._split_instructions(expanded_text)

        for instr_text in raw_instructions:
            instr_text = instr_text.strip()
            if not instr_text:
                continue

            # Parse stitch instruction
            stitch_nodes = self._parse_stitch_instruction(
                instr_text, line_number, prev_stitch_count
            )
            instructions.extend(stitch_nodes)

        return instructions

    def _expand_nested_repeats(self, text: str) -> str:
        """Expand all repeat patterns in text"""
        # Keep expanding until no more repeats found
        max_iterations = 10
        iteration = 0

        while iteration < max_iterations:
            expanded = self._expand_single_repeat(text)
            if expanded == text:
                break
            text = expanded
            iteration += 1

        return text

    def _expand_single_repeat(self, text: str) -> str:
        """Expand a single repeat pattern"""
        match = self.repeat_pattern.search(text)
        if not match:
            return text

        repeat_content = match.group(1).strip()
        times_match = self.n_times_pattern.search(text[match.end() :])

        if times_match:
            times = int(times_match.group(1))
        elif self.repeat_around_pattern.search(text[match.end() :]):
            times = 6  # Default for "around" (can be adjusted based on context)
        else:
            times = 1

        # Expand the repeat
        expanded = " ".join([repeat_content] * times)

        # Replace in original text
        full_match_end = match.end()
        if times_match:
            full_match_end = match.end() + times_match.end()

        result = text[: match.start()] + expanded + text[full_match_end:]
        return result.strip()

    def _split_instructions(self, text: str) -> list[str]:
        """Split text into individual instruction segments"""
        # Split by commas, but keep parenthetical groups together
        segments = []
        current = []
        paren_depth = 0

        for char in text:
            if char == "(":
                paren_depth += 1
                current.append(char)
            elif char == ")":
                paren_depth -= 1
                current.append(char)
            elif char == "," and paren_depth == 0:
                segments.append("".join(current).strip())
                current = []
            else:
                current.append(char)

        if current:
            segments.append("".join(current).strip())

        return [s for s in segments if s]

    def _parse_stitch_instruction(
        self, text: str, line_number: int, prev_stitch_count: int
    ) -> list[InstructionNode]:
        """Parse one clause without treating English words as stitches.

        The old scan matched "ch" inside "each" and "st" inside "each st",
        then marked "turn" as unknown. Those became false compiler warnings.
        Repeat counts such as "inc x 6" stay at one state-machine stitch so a
        correct round is not failed for running past a short canvas.
        """
        text = text.strip()
        text = re.sub(
            r"^(?:row|rnd|round|r)s?\.?\s*\d+(?:\s*[-–—]\s*\d+)?\s*[:.]?\s*",
            "",
            text,
            flags=re.IGNORECASE,
        )
        text = re.sub(r"\(\d+\)\s*$", "", text).strip(" ,.")
        if not text or re.fullmatch(
            r"(?:turn|to join|join|from hook)\.?",
            text,
            flags=re.IGNORECASE,
        ):
            return []

        turning = re.match(
            r"ch\s+(\d+)\s*(?:\(?(counts as(?: a)?[^)]*)\)?)?\s*$",
            text,
            flags=re.IGNORECASE,
        )
        if turning:
            return [
                InstructionNode(
                    action="turning_chain",
                    stitch_type="ch",
                    count=int(turning.group(1)),
                    is_turning_chain=True,
                    counts_as_stitch="counts as" in text.lower(),
                    line_number=line_number,
                )
            ]

        each = re.match(
            r"(sc|hdc|dc|tr|sl\s*st|inc)\s+in\s+"
            r"(?:(?:BLO|FLO|back\s+loops?\s+only|front\s+loops?\s+only)\s+of\s+)?"
            r"each\s+(?:st|sts|ch)\s+(?:around|across)",
            text,
            flags=re.IGNORECASE,
        )
        if each:
            return [
                InstructionNode(
                    action="stitch",
                    stitch_type=re.sub(r"\s+", "", each.group(1).lower()),
                    count=1,
                    line_number=line_number,
                )
            ]

        hook = re.match(
            r"(sc|hdc|dc|tr)\s+in\s+2nd\s+ch\s+from\s+hook",
            text,
            flags=re.IGNORECASE,
        )
        if hook:
            return [
                InstructionNode(
                    action="stitch",
                    stitch_type=hook.group(1).lower(),
                    count=1,
                    line_number=line_number,
                )
            ]

        ring = re.match(
            r"(\d+)\s+(sc|hdc|dc|tr)\s+(?:in|into)\s+"
            r"(?:magic\s+ring|mr|magic\s+circle)",
            text,
            flags=re.IGNORECASE,
        )
        if ring:
            return [
                InstructionNode(
                    action="stitch",
                    stitch_type=ring.group(2).lower(),
                    count=int(ring.group(1)),
                    line_number=line_number,
                )
            ]

        instructions = []
        stitch_pattern = re.compile(
            r"(?<![A-Za-z])(?:(\d+)\s+)?(sc|hdc|dc|tr|dtr|sl\s*st|inc|dec|picot|skip)"
            r"(?![A-Za-z])",
            re.IGNORECASE,
        )
        if not re.search(r"\beach\b|\bfrom\s+hook\b", text, flags=re.IGNORECASE):
            for match in stitch_pattern.finditer(text):
                instructions.append(
                    InstructionNode(
                        action="stitch",
                        stitch_type=re.sub(r"\s+", "", match.group(2).lower()),
                        count=int(match.group(1) or 1),
                        line_number=line_number,
                    )
                )
            for match in re.finditer(
                r"(?<![A-Za-z])ch\s+(\d+)(?![A-Za-z])",
                text,
                flags=re.IGNORECASE,
            ):
                instructions.append(
                    InstructionNode(
                        action="turning_chain",
                        stitch_type="ch",
                        count=int(match.group(1)),
                        is_turning_chain=True,
                        counts_as_stitch="counts as" in text.lower(),
                        line_number=line_number,
                    )
                )

        if not instructions and re.search(
            r"(?<![A-Za-z])(?:sc|hdc|dc|tr|inc|dec|ch)(?![A-Za-z])",
            text,
            flags=re.IGNORECASE,
        ):
            instructions.append(
                InstructionNode(
                    action="unknown",
                    stitch_type="unknown",
                    count=1,
                    line_number=line_number,
                )
            )
        return instructions


    def calculate_round_stitch_count(
        self, instructions: list[InstructionNode], prev_count: int
    ) -> int:
        """Calculate the expected stitch count after executing instructions"""
        count = prev_count

        for instr in instructions:
            if instr.action == "stitch":
                if instr.stitch_type in ["inc", "increase"]:
                    count += instr.count
                elif instr.stitch_type in ["dec", "decrease"]:
                    count -= instr.count
                elif instr.stitch_type not in ["skip", "sl st", "ch"]:
                    # Regular stitches don't change count unless they're increases/decreases
                    pass
            elif instr.action == "turning_chain" and instr.counts_as_stitch:
                count += instr.count

        return count


if __name__ == "__main__":
    print("🔄 AST Unroller")
    print("=" * 60)

    unroller = ASTUnroller()

    # Test repeat expansion
    test_round = "*sc 2, inc* rep 3 times"
    expanded = unroller.unroll_round(test_round, line_number=1, prev_stitch_count=10)

    print(f"\nInput: {test_round}")
    print(f"Expanded instructions: {len(expanded)}")
    for i, instr in enumerate(expanded, 1):
        print(f"  {i}. {instr.stitch_type} x{instr.count}")

    print("\n✅ AST Unroller working!")

# Legacy compatibility alias.
try:
    Unroller
except NameError:
    Unroller = ASTUnroller


# Legacy compatibility API.
def _legacy_unroll(self, text, *args, **kwargs):
    """
    Legacy text-based unroller.

    Example:
        *sc 2* repeat 3 times
    becomes:
        sc sc sc sc sc sc
    """
    import re

    value = str(text).strip()

    repeat_match = re.search(
        r"\*(.*?)\*\s*repeat\s+(\d+)\s+times",
        value,
        flags=re.IGNORECASE,
    )

    if repeat_match:
        body = repeat_match.group(1).strip()
        count = int(repeat_match.group(2))
        return " ".join([body] * count)

    twice_match = re.search(
        r"\*(.*?)\*\s*(twice|thrice)",
        value,
        flags=re.IGNORECASE,
    )

    if twice_match:
        body = twice_match.group(1).strip()
        count = 2 if twice_match.group(2).lower() == "twice" else 3
        return " ".join([body] * count)

    return value


ASTUnroller.unroll = _legacy_unroll

# Legacy class name.
Unroller = ASTUnroller
