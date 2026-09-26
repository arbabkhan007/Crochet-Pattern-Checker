"""
Round by Round Simulator - Detailed round-by-round simulation
"""


class RoundByRoundSimulator:
    def __init__(self):
        self.rounds = []
        self.total_stitches = 0

    def simulate_round(self, round_num: int, instruction: str) -> dict:
        """Simulate a single round in detail"""
        stitches_in_round = 0
        operations = []

        instruction_lower = instruction.lower()

        # Parse operations
        if "sc" in instruction_lower:
            operations.append("single crochet")
            stitches_in_round += 1
        if "dc" in instruction_lower:
            operations.append("double crochet")
            stitches_in_round += 1
        if "inc" in instruction_lower:
            operations.append("increase")
            stitches_in_round += 2
        if "dec" in instruction_lower:
            operations.append("decrease")
            stitches_in_round -= 1
        if "ch" in instruction_lower:
            operations.append("chain")

        self.total_stitches += stitches_in_round

        round_data = {
            "round": round_num,
            "instruction": instruction,
            "operations": operations,
            "stitches_added": stitches_in_round,
            "total_stitches": self.total_stitches,
            "cumulative_height_cm": self.total_stitches * 0.1,
        }

        self.rounds.append(round_data)
        return round_data

    def get_detailed_report(self) -> str:
        """Generate detailed simulation report"""
        report = "ROUND-BY-ROUND SIMULATION\n" + "=" * 60 + "\n\n"

        for round_data in self.rounds:
            report += f"Round {round_data['round']}:\n"
            report += f"  Instruction: {round_data['instruction']}\n"
            report += f"  Operations: {', '.join(round_data['operations'])}\n"
            report += f"  Stitches added: {round_data['stitches_added']}\n"
            report += f"  Total stitches: {round_data['total_stitches']}\n"
            report += (
                f"  Cumulative height: {round_data['cumulative_height_cm']:.1f} cm\n\n"
            )

        return report


if __name__ == "__main__":
    print("🔄 Round by Round Simulator")
    print("=" * 60)

    simulator = RoundByRoundSimulator()

    pattern = [
        "6 sc in magic ring",
        "inc in each st around",
        "sc, inc, rep 5 times",
        "sc in each st around",
    ]

    print("\n📊 Simulating round by round...")
    for i, instruction in enumerate(pattern, 1):
        result = simulator.simulate_round(i, instruction)
        print(
            f"Round {i}: {result['stitches_added']} stitches (Total: {result['total_stitches']})"
        )

    print("\n" + simulator.get_detailed_report())
    print("✨ Simulation complete!")
