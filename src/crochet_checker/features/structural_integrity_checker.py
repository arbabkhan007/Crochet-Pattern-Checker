"""
Structural Integrity Checker - Check if pattern will hold together
"""


class StructuralIntegrityChecker:
    def __init__(self):
        self.strength_factors = {
            "sc": 0.9,
            "dc": 0.7,
            "hdc": 0.8,
            "tr": 0.6,
            "inc": 0.8,
            "dec": 0.9,
            "sl_st": 0.5,
        }

    def check_integrity(self, pattern_text: str) -> dict:
        """Check structural integrity"""
        lines = pattern_text.strip().split("\n")
        total_strength = 0
        weak_points = []

        for i, line in enumerate(lines, 1):
            line_lower = line.lower()
            row_strength = 0
            stitch_count = 0

            for stitch, strength in self.strength_factors.items():
                count = line_lower.count(stitch)
                if count > 0:
                    row_strength += strength * count
                    stitch_count += count

            avg_strength = row_strength / stitch_count if stitch_count > 0 else 0.7
            total_strength += avg_strength

            if avg_strength < 0.6:
                weak_points.append(
                    {
                        "row": i,
                        "strength": avg_strength,
                        "issue": "Low structural strength",
                    }
                )

        avg_integrity = total_strength / len(lines) if lines else 0

        return {
            "integrity_score": avg_integrity,
            "integrity_rating": self._get_rating(avg_integrity),
            "weak_points": weak_points,
            "overall_strength": "high"
            if avg_integrity > 0.8
            else "medium"
            if avg_integrity > 0.6
            else "low",
            "recommendations": self._get_recommendations(avg_integrity, weak_points),
        }

    def _get_rating(self, score: float) -> str:
        if score >= 0.85:
            return "Excellent"
        elif score >= 0.7:
            return "Good"
        elif score >= 0.5:
            return "Fair"
        else:
            return "Poor"

    def _get_recommendations(self, score: float, weak_points: list) -> list:
        recommendations = []

        if score < 0.7:
            recommendations.append("Consider using stronger stitches (sc, hdc)")
            recommendations.append("Add reinforcement at stress points")

        if weak_points:
            recommendations.append(
                f"{len(weak_points)} weak rows detected - reinforce these areas"
            )

        return recommendations


if __name__ == "__main__":
    print("🏗️ Structural Integrity Checker")
    print("=" * 60)

    checker = StructuralIntegrityChecker()

    pattern = """Row 1: 10 sc
Row 2: 10 dc
Row 3: 10 tr"""

    result = checker.check_integrity(pattern)

    print(f"\nIntegrity Score: {result['integrity_score']:.2f}")
    print(f"Rating: {result['integrity_rating']}")
    print(f"Overall Strength: {result['overall_strength']}")

    if result["weak_points"]:
        print(f"\n⚠️ {len(result['weak_points'])} weak points detected")

    if result["recommendations"]:
        print("\n💡 Recommendations:")
        for rec in result["recommendations"]:
            print(f"  • {rec}")

    print("\n✨ Check complete!")
