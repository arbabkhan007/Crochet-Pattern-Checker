"""
Pattern Simulation Engine - Simulate crochet patterns round by round
"""


class PatternSimulationEngine:
    def __init__(self):
        self.rounds = []
        self.stitch_count = 0
        self.simulation_log = []

    def simulate_pattern(self, pattern_text: str) -> dict:
        """Simulate entire pattern round by round"""
        lines = pattern_text.strip().split("\n")

        for round_num, line in enumerate(lines, 1):
            round_result = self._simulate_round(round_num, line)
            self.rounds.append(round_result)
            self.simulation_log.append(
                f"Round {round_num}: {round_result['stitches_added']} stitches - {round_result['status']}"
            )

        return {
            "total_rounds": len(self.rounds),
            "final_stitch_count": self.stitch_count,
            "simulation_log": self.simulation_log,
            "status": "success"
            if all(r["status"] == "valid" for r in self.rounds)
            else "errors_found",
        }

    def _simulate_round(self, round_num: int, instruction: str) -> dict:
        """Simulate a single round"""
        stitches_added = 0
        status = "valid"
        errors = []

        # Parse instruction
        instruction_lower = instruction.lower()

        # Count stitches
        if "sc" in instruction_lower:
            count = self._extract_number(instruction, "sc")
            stitches_added += count if count else 1
        if "dc" in instruction_lower:
            count = self._extract_number(instruction, "dc")
            stitches_added += count if count else 1
        if "inc" in instruction_lower:
            stitches_added += 2
        if "dec" in instruction_lower:
            stitches_added -= 1

        # Check for common errors
        if "inc" in instruction_lower and "dec" in instruction_lower and round_num < 3:
            errors.append("Warning: Increases and decreases in early rounds")

        self.stitch_count += stitches_added

        return {
            "round": round_num,
            "instruction": instruction,
            "stitches_added": stitches_added,
            "total_stitches": self.stitch_count,
            "status": status,
            "errors": errors,
        }

    def _extract_number(self, instruction: str, stitch: str) -> int:
        """Extract number from instruction"""
        import re

        match = re.search(r"(\d+)\s*" + stitch, instruction)
        return int(match.group(1)) if match else 0

    def get_simulation_report(self) -> str:
        """Generate simulation report"""
        report = "PATTERN SIMULATION REPORT\n" + "=" * 60 + "\n\n"
        for log in self.simulation_log:
            report += f"{log}\n"
        report += f"\nFinal Stitch Count: {self.stitch_count}\n"
        report += f"Total Rounds: {len(self.rounds)}\n"
        return report


if __name__ == "__main__":
    print("🔬 Pattern Simulation Engine")
    print("=" * 60)

    engine = PatternSimulationEngine()

    pattern = """Round 1: 6 sc in magic ring
Round 2: inc in each st around
Round 3: sc, inc, rep 5 times
Round 4: sc in each st around"""

    print("\n📊 Simulating pattern...")
    result = engine.simulate_pattern(pattern)

    print(f"\nSimulation Status: {result['status']}")
    print(f"Total Rounds: {result['total_rounds']}")
    print(f"Final Stitch Count: {result['final_stitch_count']}")

    print("\n📋 Simulation Log:")
    for log in result["simulation_log"]:
        print(f"  {log}")

    print("\n" + engine.get_simulation_report())
    print("\n✨ Simulation complete!")
