"""
TurningChainRulesEngine
Evaluates turning chain directives (counts as st vs does not count as st)
and allocates +1 or +0 to the active round's output count accordingly.
"""

import re
from dataclasses import dataclass


@dataclass
class TurningChain:
    """Represents a turning chain"""

    chain_count: int
    counts_as_stitch: bool
    round_number: int
    line_number: int
    stitch_type: str | None = None  # What it counts as (e.g., "dc")


@dataclass
class ChainAllocation:
    """Result of chain allocation"""

    chain: TurningChain
    stitch_count_addition: int
    reason: str


class TurningChainRulesEngine:
    """
    Evaluates turning chain directives and allocates stitch counts.
    """

    def __init__(self):
        self.turning_chains: list[TurningChain] = []
        self.allocations: list[ChainAllocation] = []

        # Default chain counts that count as stitches
        self.default_counts_as = {1: "sc", 2: "hdc", 3: "dc", 4: "tr", 5: "dtr"}

    def parse_turning_chain(
        self, instruction: str, round_number: int, line_number: int
    ) -> TurningChain | None:
        """
        Parse a turning chain from instruction.
        Examples:
        - "ch 3 (counts as dc)" -> counts_as_stitch=True, stitch_type="dc"
        - "ch 1 (does not count as st)" -> counts_as_stitch=False
        - "ch 3" -> defaults based on count
        """
        # Match chain instruction
        match = re.match(r"ch\s+(\d+)", instruction, re.IGNORECASE)
        if not match:
            return None

        chain_count = int(match.group(1))

        # NOTE: check "does not count" BEFORE "counts as" — the phrase
        # "does not count as st" contains "count as st" as a substring.
        if re.search(r"does\s+not\s+count", instruction, re.IGNORECASE):
            counts_as_stitch = False
            stitch_type = None
        # Check if it explicitly says "counts as"
        elif re.search(r"counts?\s+as\s+(\w+)", instruction, re.IGNORECASE):
            counts_match = re.search(
                r"counts?\s+as\s+(\w+)", instruction, re.IGNORECASE
            )
            counts_as_stitch = True
            stitch_type = counts_match.group(1).lower()
        # Default behavior
        else:
            counts_as_stitch = chain_count >= 2  # ch-1 doesn't count, ch-2+ do
            stitch_type = self.default_counts_as.get(chain_count)

        chain = TurningChain(
            chain_count=chain_count,
            counts_as_stitch=counts_as_stitch,
            stitch_type=stitch_type,
            round_number=round_number,
            line_number=line_number,
        )

        self.turning_chains.append(chain)
        return chain

    def allocate_chain(self, chain: TurningChain) -> ChainAllocation:
        """
        Allocate stitch count for a turning chain.
        Returns +1 if counts as stitch, +0 otherwise.
        """
        if chain.counts_as_stitch:
            addition = 1
            reason = f"ch-{chain.chain_count} counts as {chain.stitch_type}"
        else:
            addition = 0
            reason = f"ch-{chain.chain_count} does not count as stitch"

        allocation = ChainAllocation(
            chain=chain, stitch_count_addition=addition, reason=reason
        )

        self.allocations.append(allocation)
        return allocation

    def calculate_round_stitch_count(self, round_number: int, base_count: int) -> dict:
        """
        Calculate total stitch count for a round including turning chains.

        Args:
            round_number: The round number
            base_count: Stitch count from instructions (excluding turning chain)

        Returns:
            Dictionary with breakdown of stitch count
        """
        round_chains = [
            c for c in self.turning_chains if c.round_number == round_number
        ]

        total_addition = 0
        allocations = []

        for chain in round_chains:
            allocation = self.allocate_chain(chain)
            allocations.append(allocation)
            total_addition += allocation.stitch_count_addition

        return {
            "round": round_number,
            "base_count": base_count,
            "turning_chain_addition": total_addition,
            "total_count": base_count + total_addition,
            "allocations": [
                {
                    "chain_count": a.chain.chain_count,
                    "addition": a.stitch_count_addition,
                    "reason": a.reason,
                }
                for a in allocations
            ],
        }

    def validate_turning_chains(self, round_number: int) -> list[str]:
        """
        Validate turning chains for a round.
        Returns list of warnings/errors.
        """
        warnings = []
        round_chains = [
            c for c in self.turning_chains if c.round_number == round_number
        ]

        for chain in round_chains:
            # Check if chain count matches stitch type
            if chain.counts_as_stitch and chain.stitch_type:
                expected_count = {"sc": 1, "hdc": 2, "dc": 3, "tr": 4, "dtr": 5}.get(
                    chain.stitch_type
                )

                if expected_count and chain.chain_count != expected_count:
                    warnings.append(
                        f"Line {chain.line_number}: ch-{chain.chain_count} typically counts as "
                        f"{self.default_counts_as.get(chain.chain_count, '?')}, not {chain.stitch_type}"
                    )

        return warnings

    def get_chain_summary(self, round_number: int) -> dict:
        """Get summary of turning chains in a round"""
        round_chains = [
            c for c in self.turning_chains if c.round_number == round_number
        ]

        return {
            "round": round_number,
            "total_chains": len(round_chains),
            "chains": [
                {
                    "count": c.chain_count,
                    "counts_as_stitch": c.counts_as_stitch,
                    "stitch_type": c.stitch_type,
                }
                for c in round_chains
            ],
        }

    def reset(self) -> None:
        """Reset the engine"""
        self.turning_chains.clear()
        self.allocations.clear()


# Example usage
if __name__ == "__main__":
    engine = TurningChainRulesEngine()

    # Test 1: ch-3 counts as dc
    print("Test 1: ch-3 counts as dc")
    chain1 = engine.parse_turning_chain("ch 3 (counts as dc)", 1, 5)
    result1 = engine.calculate_round_stitch_count(1, 10)
    print(
        f"Base: {result1['base_count']}, Addition: {result1['turning_chain_addition']}, Total: {result1['total_count']}"
    )
    print(f"Allocation: {result1['allocations'][0]['reason']}")

    # Test 2: ch-1 does not count
    print("\nTest 2: ch-1 does not count as stitch")
    engine.reset()
    chain2 = engine.parse_turning_chain("ch 1 (does not count as st)", 2, 10)
    result2 = engine.calculate_round_stitch_count(2, 12)
    print(
        f"Base: {result2['base_count']}, Addition: {result2['turning_chain_addition']}, Total: {result2['total_count']}"
    )
    print(f"Allocation: {result2['allocations'][0]['reason']}")

    # Test 3: Default behavior
    print("\nTest 3: Default behavior (ch-3 automatically counts as dc)")
    engine.reset()
    chain3 = engine.parse_turning_chain("ch 3", 3, 15)
    result3 = engine.calculate_round_stitch_count(3, 15)
    print(f"Total: {result3['total_count']} (ch-3 counts as dc by default)")

    # Test 4: Validate mismatched chain
    print("\nTest 4: Validation - ch-2 claiming to count as dc")
    engine.reset()
    chain4 = engine.parse_turning_chain("ch 2 (counts as dc)", 4, 20)
    warnings = engine.validate_turning_chains(4)
    if warnings:
        print(f"⚠️ Warning: {warnings[0]}")
    else:
        print("✅ No warnings")

    print(f"\nChain summary: {engine.get_chain_summary(1)}")
