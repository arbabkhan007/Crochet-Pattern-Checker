"""
Yarn Consumption Estimator - Estimate yarn needed for patterns
"""


class YarnConsumptionEstimator:
    def __init__(self):
        self.stitch_yarn_usage = {
            "sc": 0.5,  # yards per stitch
            "dc": 1.0,
            "hdc": 0.75,
            "tr": 1.5,
            "ch": 0.2,
        }

    def estimate_yarn_needed(self, pattern_text: str) -> dict:
        """Estimate total yarn needed"""
        lines = pattern_text.strip().split("\n")
        total_yards = 0
        stitch_counts = {}

        for line in lines:
            line_lower = line.lower()
            for stitch, yards_per_stitch in self.stitch_yarn_usage.items():
                count = line_lower.count(stitch)
                if count > 0:
                    stitch_counts[stitch] = stitch_counts.get(stitch, 0) + count
                    total_yards += count * yards_per_stitch

        return {
            "total_yards": total_yards,
            "total_meters": total_yards * 0.9144,
            "stitch_breakdown": stitch_counts,
            "estimated_skeins_100g": max(1, int(total_yards / 200) + 1),
            "safety_margin_yards": total_yards * 0.1,
        }

    def estimate_cost(self, yarn_needed: dict, price_per_skein: float = 8.0) -> dict:
        """Estimate project cost"""
        skeins = yarn_needed["estimated_skeins_100g"]
        total_cost = skeins * price_per_skein

        return {
            "skeins_needed": skeins,
            "total_cost": total_cost,
            "cost_per_yard": total_cost / yarn_needed["total_yards"]
            if yarn_needed["total_yards"] > 0
            else 0,
        }


if __name__ == "__main__":
    print("🧶 Yarn Consumption Estimator")
    print("=" * 60)

    estimator = YarnConsumptionEstimator()

    pattern = """Row 1: 10 sc
Row 2: 10 dc
Row 3: 10 hdc
Row 4: 10 sc"""

    print("\n📊 Estimating yarn consumption...")
    result = estimator.estimate_yarn_needed(pattern)

    print("\nTotal yarn needed:")
    print(f"  {result['total_yards']:.1f} yards")
    print(f"  {result['total_meters']:.1f} meters")
    print(f"  {result['estimated_skeins_100g']} skeins (100g each)")
    print(f"  Safety margin: {result['safety_margin_yards']:.1f} yards")

    print("\nStitch breakdown:")
    for stitch, count in result["stitch_breakdown"].items():
        print(f"  {stitch}: {count}")

    cost = estimator.estimate_cost(result, 8.0)
    print(f"\n💰 Estimated cost: ${cost['total_cost']:.2f}")

    print("\n✨ Estimation complete!")
