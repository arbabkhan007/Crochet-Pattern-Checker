"""
Stitch Interaction Simulator - Simulate how stitches interact with each other
"""


class StitchInteractionSimulator:
    def __init__(self):
        self.interactions = {
            ("sc", "sc"): {"compatibility": "high", "gap_risk": "low"},
            ("sc", "dc"): {"compatibility": "medium", "gap_risk": "medium"},
            ("dc", "dc"): {"compatibility": "high", "gap_risk": "low"},
            ("sc", "tr"): {"compatibility": "low", "gap_risk": "high"},
        }

    def simulate_stitch_sequence(self, stitch_sequence: list) -> dict:
        """Simulate how stitches interact in sequence"""
        interactions = []
        issues = []

        for i in range(len(stitch_sequence) - 1):
            current = stitch_sequence[i]
            next_stitch = stitch_sequence[i + 1]
            interaction = self.interactions.get(
                (current, next_stitch),
                {"compatibility": "medium", "gap_risk": "medium"},
            )
            interactions.append(interaction)

            if interaction["gap_risk"] == "high":
                issues.append(
                    f"Position {i + 1}-{i + 2}: High gap risk between {current} and {next_stitch}"
                )

        return {
            "total_interactions": len(interactions),
            "issues_found": len(issues),
            "issues": issues,
            "overall_compatibility": "good" if len(issues) == 0 else "needs_attention",
        }

    def get_recommendations(self, issues: list) -> list:
        """Get recommendations for fixing issues"""
        recommendations = []
        for issue in issues:
            if "gap risk" in issue.lower():
                recommendations.append(
                    "Add transition stitches or use intermediate height stitches"
                )
        return recommendations


if __name__ == "__main__":
    print("🔗 Stitch Interaction Simulator")
    print("=" * 60)

    simulator = StitchInteractionSimulator()

    sequence = ["sc", "sc", "dc", "dc", "sc"]
    print(f"\nTesting sequence: {sequence}")

    result = simulator.simulate_stitch_sequence(sequence)
    print(f"\nInteractions analyzed: {result['total_interactions']}")
    print(f"Issues found: {result['issues_found']}")
    print(f"Compatibility: {result['overall_compatibility']}")

    if result["issues"]:
        print("\n⚠️ Issues:")
        for issue in result["issues"]:
            print(f"  • {issue}")

    print("\n✨ Simulation complete!")
