"""
CornerSequenceValidator
Matches repeat blocks sequentially against corner-space queues to detect mismatches
in asymmetric or non-uniform shapes (e.g., expecting ch-2 when encountering ch-3).
"""

import re
from dataclasses import dataclass


@dataclass
class CornerSpace:
    """Represents a corner space in the pattern"""

    space_id: str
    round_number: int
    corner_index: int
    chain_count: int  # e.g., ch-2, ch-3
    position: int


@dataclass
class RepeatBlock:
    """Represents a repeat block expecting a corner"""

    block_id: str
    expected_chain_count: int
    corner_index: int
    line_number: int


class CornerMismatchError(Exception):
    """Raised when corner sequence doesn't match expectations"""


class CornerSequenceValidator:
    """
    Validates that repeat blocks match corner-space sequences correctly.
    Detects mismatches in asymmetric patterns.
    """

    def __init__(self):
        self.corner_spaces: list[CornerSpace] = []
        self.repeat_blocks: list[RepeatBlock] = []
        self.space_counter: int = 0
        self.block_counter: int = 0

    def add_corner_space(
        self, round_number: int, corner_index: int, chain_count: int, position: int
    ) -> CornerSpace:
        """Add a corner space"""
        space = CornerSpace(
            space_id=f"r{round_number}_c{corner_index}_{self.space_counter}",
            round_number=round_number,
            corner_index=corner_index,
            chain_count=chain_count,
            position=position,
        )
        self.corner_spaces.append(space)
        self.space_counter += 1
        return space

    def add_repeat_block(
        self, expected_chain_count: int, corner_index: int, line_number: int
    ) -> RepeatBlock:
        """Add a repeat block that expects a corner"""
        block = RepeatBlock(
            block_id=f"block_{self.block_counter}",
            expected_chain_count=expected_chain_count,
            corner_index=corner_index,
            line_number=line_number,
        )
        self.repeat_blocks.append(block)
        self.block_counter += 1
        return block

    def parse_corner_from_instruction(self, instruction: str) -> int | None:
        """Extract chain count from instruction like 'ch-2 sp' or 'ch 3 space'"""
        match = re.search(
            r"ch[\s-]*(\d+)[\s-]*(?:sp|space)", instruction, re.IGNORECASE
        )
        if match:
            return int(match.group(1))
        return None

    def validate_sequence(self, round_number: int) -> list[str]:
        """
        Validate that repeat blocks match corner spaces in sequence.
        Returns list of mismatch errors.
        """
        errors = []

        # Get spaces and blocks for this round
        round_spaces = [s for s in self.corner_spaces if s.round_number == round_number]
        round_blocks = [b for b in self.repeat_blocks]

        # Sort by position/corner_index
        round_spaces.sort(key=lambda s: (s.corner_index, s.position))
        round_blocks.sort(key=lambda b: b.corner_index)

        # Match blocks to spaces sequentially
        for block in round_blocks:
            matching_space = None

            # Find the space at this corner index
            for space in round_spaces:
                if space.corner_index == block.corner_index:
                    matching_space = space
                    break

            if not matching_space:
                errors.append(
                    f"Line {block.line_number}: Repeat block expects corner {block.corner_index}, "
                    f"but no corner space found at that position"
                )
                continue

            # Check chain count match
            if block.expected_chain_count != matching_space.chain_count:
                raise CornerMismatchError(
                    f"Line {block.line_number}: Repeat block expects ch-{block.expected_chain_count}, "
                    f"but corner space is ch-{matching_space.chain_count}"
                )

        return errors

    def validate_asymmetric_pattern(self, round_number: int) -> dict:
        """
        Validate an asymmetric pattern with varying corner sizes.
        Returns validation report.
        """
        round_spaces = [s for s in self.corner_spaces if s.round_number == round_number]

        # Group by corner index
        corners_by_index = {}
        for space in round_spaces:
            if space.corner_index not in corners_by_index:
                corners_by_index[space.corner_index] = []
            corners_by_index[space.corner_index].append(space)

        # Check for inconsistencies
        inconsistencies = []
        for corner_idx, spaces in corners_by_index.items():
            chain_counts = [s.chain_count for s in spaces]
            if len(set(chain_counts)) > 1:
                inconsistencies.append(
                    {
                        "corner": corner_idx,
                        "chain_counts": chain_counts,
                        "message": f"Corner {corner_idx} has inconsistent chain counts: {chain_counts}",
                    }
                )

        return {
            "round": round_number,
            "total_corners": len(corners_by_index),
            "total_spaces": len(round_spaces),
            "inconsistencies": inconsistencies,
            "is_valid": len(inconsistencies) == 0,
        }

    def get_corner_summary(self, round_number: int) -> dict:
        """Get summary of corners in a round"""
        round_spaces = [s for s in self.corner_spaces if s.round_number == round_number]

        corners_by_index = {}
        for space in round_spaces:
            if space.corner_index not in corners_by_index:
                corners_by_index[space.corner_index] = []
            corners_by_index[space.corner_index].append(space.chain_count)

        return {
            "round": round_number,
            "corners": {
                idx: {"count": len(counts), "chain_counts": counts}
                for idx, counts in corners_by_index.items()
            },
        }

    def reset(self) -> None:
        """Reset the validator"""
        self.corner_spaces.clear()
        self.repeat_blocks.clear()
        self.space_counter = 0
        self.block_counter = 0


# Example usage
if __name__ == "__main__":
    validator = CornerSequenceValidator()

    # Simulate a square pattern with 4 corners
    print("Creating square pattern with ch-2 corners")
    for i in range(4):
        validator.add_corner_space(1, i, 2, i * 5)

    # Add repeat blocks expecting ch-2
    for i in range(4):
        validator.add_repeat_block(2, i, line_number=10 + i)

    # Validate
    try:
        errors = validator.validate_sequence(1)
        if errors:
            print(f"❌ Validation errors: {errors}")
        else:
            print("✅ All corners match correctly")
    except CornerMismatchError as e:
        print(f"❌ {e}")

    # Test mismatch case
    print("\nTesting mismatch: expecting ch-3 but corner is ch-2")
    validator.reset()

    validator.add_corner_space(1, 0, 2, 0)
    validator.add_repeat_block(3, 0, line_number=10)

    try:
        errors = validator.validate_sequence(1)
        print("✅ Validation passed")
    except CornerMismatchError as e:
        print(f"❌ {e}")

    # Test asymmetric pattern
    print("\nTesting asymmetric pattern")
    validator.reset()

    # Asymmetric corners
    validator.add_corner_space(1, 0, 2, 0)
    validator.add_corner_space(1, 1, 3, 5)
    validator.add_corner_space(1, 1, 2, 10)  # Inconsistent!

    report = validator.validate_asymmetric_pattern(1)
    print(f"Valid: {report['is_valid']}")
    if report["inconsistencies"]:
        for inc in report["inconsistencies"]:
            print(f"  - {inc['message']}")

    print(f"\nCorner summary: {validator.get_corner_summary(1)}")
