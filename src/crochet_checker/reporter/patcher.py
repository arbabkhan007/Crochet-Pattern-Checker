"""
DiffPatchGenerator
Automatically suggests minimal pattern rewrites for failing rounds
(like correcting an extra treble in a starting chain or realigning a corner sequence).
"""

import difflib
import re
from dataclasses import dataclass, field


@dataclass
class Patch:
    """Represents a suggested pattern fix"""

    round_number: int
    line_number: int
    original_text: str
    corrected_text: str
    issue_type: str
    description: str
    confidence: float  # 0.0 to 1.0

    def to_diff(self) -> str:
        """Generate a unified diff of this patch"""
        diff = list(
            difflib.unified_diff(
                [self.original_text],
                [self.corrected_text],
                fromfile=f"round_{self.round_number}_original",
                tofile=f"round_{self.round_number}_corrected",
                lineterm="",
            )
        )
        return "\n".join(diff)


@dataclass
class PatchReport:
    """Complete patch report for a pattern"""

    patches: list[Patch] = field(default_factory=list)
    total_issues: int = 0
    fixable_issues: int = 0

    def add_patch(self, patch: Patch):
        self.patches.append(patch)
        self.total_issues += 1
        if patch.confidence > 0.5:
            self.fixable_issues += 1


class DiffPatchGenerator:
    """
    Generates minimal pattern rewrites for failing rounds.
    """

    def __init__(self):
        self.stitch_definitions = {
            "ch": 0,  # Chains don't count as base stitches
            "sl st": 0,
            "sc": 1,
            "hdc": 1,
            "dc": 1,
            "tr": 1,
            "dtr": 1,
        }

        self.turning_chain_heights = {
            "sc": 1,
            "hdc": 2,
            "dc": 3,
            "tr": 4,
            "dtr": 5,
        }

    def analyze_round(
        self,
        round_number: int,
        instructions: list[str],
        expected_count: int,
        line_numbers: list[int] = None,
    ) -> PatchReport:
        """
        Analyze a round and generate patches for issues.

        Args:
            round_number: The round number
            instructions: List of instruction strings
            expected_count: Expected stitch count for the round
            line_numbers: Optional list of line numbers corresponding to instructions

        Returns:
            PatchReport with suggested patches
        """
        report = PatchReport()

        if line_numbers is None:
            line_numbers = list(range(1, len(instructions) + 1))

        # Calculate actual stitch count
        actual_count, counted_instructions = self._count_stitches(instructions)

        # Check for count mismatch
        if actual_count != expected_count:
            patch = self._generate_count_fix_patch(
                round_number,
                line_numbers[0] if line_numbers else 1,
                instructions[0] if instructions else "",
                actual_count,
                expected_count,
            )
            if patch:
                report.add_patch(patch)

        # Check for turning chain issues
        for i, instruction in enumerate(instructions):
            turning_patch = self._check_turning_chain(
                round_number,
                instruction,
                line_numbers[i] if i < len(line_numbers) else i + 1,
            )
            if turning_patch:
                report.add_patch(turning_patch)

        # Check for corner sequence issues
        corner_patch = self._check_corner_sequence(
            round_number, instructions, line_numbers
        )
        if corner_patch:
            report.add_patch(corner_patch)

        return report

    def _count_stitches(self, instructions: list[str]) -> tuple[int, list[dict]]:
        """Count stitches in instructions without double-counting."""
        total = 0
        counted = []

        for instruction in instructions:
            count = 0
            stitch_type = None

            # Match "N stitch" patterns
            for match in re.finditer(
                r"(\d+)\s+(sc|dc|hdc|tr|dtr)", instruction, re.IGNORECASE
            ):
                n = int(match.group(1))
                total += n
                count += n
                stitch_type = match.group(2).lower()

            # Match "stitch N" patterns
            for match in re.finditer(
                r"(sc|dc|hdc|tr|dtr)\s+(\d+)", instruction, re.IGNORECASE
            ):
                n = int(match.group(2))
                total += n
                count += n
                stitch_type = match.group(1).lower()

            # Match single stitches, excluding those already part of counted groups
            residue = re.sub(
                r"\d+\s+(?:sc|dc|hdc|tr|dtr)", " ", instruction, flags=re.IGNORECASE
            )
            residue = re.sub(
                r"(?:sc|dc|hdc|tr|dtr)\s+\d+", " ", residue, flags=re.IGNORECASE
            )
            single_stitches = re.findall(
                r"\b(sc|dc|hdc|tr|dtr)\b", residue, re.IGNORECASE
            )
            for s in single_stitches:
                total += 1
                count += 1
                stitch_type = s.lower()

            counted.append(
                {"instruction": instruction, "count": count, "stitch_type": stitch_type}
            )

        return total, counted

    def _generate_count_fix_patch(
        self,
        round_number: int,
        line_number: int,
        instruction: str,
        actual: int,
        expected: int,
    ) -> Patch | None:
        """Generate a patch to fix count mismatch"""
        difference = expected - actual

        if difference == 0:
            return None

        # Generate corrected instruction
        if difference > 0:
            # Need to add stitches
            correction_type = "add"
            suggestion = self._suggest_add_stitches(instruction, difference)
        else:
            # Need to remove stitches
            correction_type = "remove"
            suggestion = self._suggest_remove_stitches(instruction, abs(difference))

        if not suggestion:
            return None

        # Calculate confidence based on how clear the fix is
        confidence = min(0.9, 0.5 + abs(difference) * 0.1)

        patch = Patch(
            round_number=round_number,
            line_number=line_number,
            original_text=instruction,
            corrected_text=suggestion,
            issue_type=f"stitch_count_{correction_type}",
            description=(
                f"Stitch count mismatch: pattern has {actual}, expected {expected}. "
                f"Need to {correction_type} {abs(difference)} stitch(es)."
            ),
            confidence=confidence,
        )

        return patch

    def _suggest_add_stitches(self, instruction: str, count: int) -> str | None:
        """Suggest adding stitches to instruction"""
        # Find last stitch count to modify
        match = re.search(r"(\d+)\s+(sc|dc|hdc|tr|dtr)", instruction, re.IGNORECASE)
        if match:
            new_count = int(match.group(1)) + count
            return (
                instruction[: match.start(1)]
                + str(new_count)
                + instruction[match.end(1) :]
            )

        # If no count found, add "count sc" at the end
        if instruction.strip().endswith("."):
            instruction = instruction.rstrip(".")
        return f"{instruction}, {count} sc"

    def _suggest_remove_stitches(self, instruction: str, count: int) -> str | None:
        """Suggest removing stitches from instruction"""
        # Find last stitch count to modify
        match = re.search(r"(\d+)\s+(sc|dc|hdc|tr|dtr)", instruction, re.IGNORECASE)
        if match:
            new_count = max(0, int(match.group(1)) - count)
            if new_count == 0:
                # Remove the whole instruction
                return instruction[: match.start()].rstrip(", ")
            return (
                instruction[: match.start(1)]
                + str(new_count)
                + instruction[match.end(1) :]
            )

        return None

    def _check_turning_chain(
        self, round_number: int, instruction: str, line_number: int
    ) -> Patch | None:
        """Check for turning chain issues"""
        # Find turning chain
        match = re.search(r"ch\s+(\d+)", instruction, re.IGNORECASE)
        if not match:
            return None

        chain_count = int(match.group(1))

        # Check if chain count matches stitch type used
        stitch_match = re.search(r"\b(sc|hdc|dc|tr|dtr)\b", instruction, re.IGNORECASE)
        if not stitch_match:
            return None

        stitch_type = stitch_match.group(1).lower()
        expected_chain = self.turning_chain_heights.get(stitch_type)

        if expected_chain and chain_count != expected_chain:
            # Correct the chain count
            corrected = (
                instruction[: match.start(1)]
                + str(expected_chain)
                + instruction[match.end(1) :]
            )

            patch = Patch(
                round_number=round_number,
                line_number=line_number,
                original_text=instruction,
                corrected_text=corrected,
                issue_type="turning_chain_mismatch",
                description=(
                    f"Turning chain ch-{chain_count} doesn't match {stitch_type} stitch height. "
                    f"Should be ch-{expected_chain}."
                ),
                confidence=0.8,
            )

            return patch

        return None

    def _check_corner_sequence(
        self, round_number: int, instructions: list[str], line_numbers: list[int]
    ) -> Patch | None:
        """Check for corner sequence issues"""
        # Find corner chain counts
        corner_counts = []
        corner_positions = []

        for i, instruction in enumerate(instructions):
            matches = re.findall(r"ch[\s-](\d+)", instruction, re.IGNORECASE)
            if matches and (
                "corner" in instruction.lower()
                or "sp" in instruction.lower()
                or "space" in instruction.lower()
            ):
                corner_counts.extend(int(m) for m in matches)
                corner_positions.append(i)

        # Check for inconsistent corner counts
        if len(set(corner_counts)) > 1:
            # Most common count is likely correct
            from collections import Counter

            most_common = Counter(corner_counts).most_common(1)[0][0]

            # Fix the inconsistent ones
            fixed_instruction = instructions[corner_positions[0]]
            for count in corner_counts:
                if count != most_common:
                    fixed_instruction = re.sub(
                        r"ch[\s-]" + str(count), f"ch-{most_common}", fixed_instruction
                    )

            patch = Patch(
                round_number=round_number,
                line_number=line_numbers[corner_positions[0]]
                if corner_positions
                else 1,
                original_text=instructions[corner_positions[0]]
                if corner_positions
                else "",
                corrected_text=fixed_instruction,
                issue_type="corner_sequence_mismatch",
                description=(
                    f"Inconsistent corner chain counts: {corner_counts}. "
                    f"Most corners use ch-{most_common}."
                ),
                confidence=0.7,
            )

            return patch

        return None

    def generate_full_patch_report(self, pattern_text: str) -> dict:
        """
        Generate a full patch report for an entire pattern.

        Args:
            pattern_text: Complete pattern text

        Returns:
            Dictionary with patch summary
        """
        lines = pattern_text.split("\n")
        rounds = {}

        current_round = None
        for i, line in enumerate(lines):
            round_match = re.search(r"(?i)\b(round|row)\s+(\d+)", line)
            if round_match:
                current_round = int(round_match.group(2))
                rounds[current_round] = {"instructions": [], "line_numbers": []}
                # The remainder of the header line is itself an instruction
                rest = line[round_match.end() :].strip(" :.-")
                if rest:
                    rounds[current_round]["instructions"].append(rest)
                    rounds[current_round]["line_numbers"].append(i + 1)
            elif current_round is not None and line.strip():
                rounds[current_round]["instructions"].append(line.strip())
                rounds[current_round]["line_numbers"].append(i + 1)

        all_patches = []
        for round_num, round_data in rounds.items():
            # Extract expected count
            expected = None
            for instruction in round_data["instructions"]:
                match = re.search(r"\((\d+)\s*(?:sts?|stitches?)?\)", instruction)
                if match:
                    expected = int(match.group(1))
                    break

            if expected is not None:
                report = self.analyze_round(
                    round_num,
                    round_data["instructions"],
                    expected,
                    round_data["line_numbers"],
                )
                all_patches.extend(report.patches)

        return {
            "total_patches": len(all_patches),
            "patches": [
                {
                    "round": p.round_number,
                    "line": p.line_number,
                    "issue": p.issue_type,
                    "description": p.description,
                    "confidence": p.confidence,
                    "diff": p.to_diff(),
                }
                for p in all_patches
            ],
        }

    def reset(self) -> None:
        """Reset the generator"""


# Example usage
if __name__ == "__main__":
    generator = DiffPatchGenerator()

    # Test 1: Stitch count mismatch
    print("Test 1: Stitch count mismatch")
    instructions = ["ch 3, 10 dc in ring"]
    report = generator.analyze_round(1, instructions, 12, [5])

    for patch in report.patches:
        print(f"\nIssue: {patch.issue_type}")
        print(f"Description: {patch.description}")
        print(f"Confidence: {patch.confidence:.1%}")
        print(f"Diff:\n{patch.to_diff()}")

    # Test 2: Turning chain mismatch
    print("\n\nTest 2: Turning chain mismatch")
    instructions = ["ch 2, dc in each st around"]
    report = generator.analyze_round(2, instructions, 20, [10])

    for patch in report.patches:
        print(f"\nIssue: {patch.issue_type}")
        print(f"Description: {patch.description}")
        print(f"Diff:\n{patch.to_diff()}")

    # Test 3: Full pattern analysis
    print("\n\nTest 3: Full pattern analysis")
    test_pattern = """
Round 1: ch 4, sl st to join
Round 2: ch 3, 10 dc in ring (12 sts)
Round 3: ch 2, 2 dc in each st around (24 sts)
Round 4: ch 3, dc in next st, 2 dc in next st (30 sts)
"""

    full_report = generator.generate_full_patch_report(test_pattern)
    print(f"Total patches: {full_report['total_patches']}")
    for patch in full_report["patches"][:3]:
        print(f"  Round {patch['round']}: {patch['description'][:60]}...")
