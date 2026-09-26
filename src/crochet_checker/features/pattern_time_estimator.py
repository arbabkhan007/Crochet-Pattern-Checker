"""
Pattern Time Estimator - Estimate time to complete pattern
"""


class PatternTimeEstimator:
    def __init__(self):
        self.stitch_time = {
            "sc": 3,  # seconds per stitch
            "dc": 4,
            "hdc": 3.5,
            "tr": 5,
            "ch": 1,
            "sl_st": 2,
        }
        self.skill_multiplier = {
            "beginner": 1.5,
            "intermediate": 1.0,
            "advanced": 0.8,
        }

    def estimate_time(
        self, pattern_text: str, skill_level: str = "intermediate"
    ) -> dict:
        """Estimate time to complete pattern"""
        lines = pattern_text.strip().split("\n")
        total_seconds = 0
        stitch_counts = {}

        multiplier = self.skill_multiplier.get(skill_level, 1.0)

        for line in lines:
            line_lower = line.lower()
            for stitch, time_per_stitch in self.stitch_time.items():
                count = line_lower.count(stitch)
                if count > 0:
                    stitch_counts[stitch] = stitch_counts.get(stitch, 0) + count
                    total_seconds += count * time_per_stitch

        total_seconds *= multiplier

        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)

        return {
            "total_seconds": total_seconds,
            "total_minutes": total_seconds / 60,
            "total_hours": total_seconds / 3600,
            "formatted_time": f"{hours}h {minutes}m",
            "stitch_breakdown": stitch_counts,
            "skill_level": skill_level,
        }


if __name__ == "__main__":
    print("⏱️ Pattern Time Estimator")
    print("=" * 60)

    estimator = PatternTimeEstimator()

    pattern = """Row 1: 20 sc
Row 2: 20 dc
Row 3: 20 hdc
Row 4: 20 sc"""

    print("\n📊 Estimating time...")
    result = estimator.estimate_time(pattern, "intermediate")

    print(f"\nEstimated time: {result['formatted_time']}")
    print(f"Total minutes: {result['total_minutes']:.0f}")
    print(f"Total hours: {result['total_hours']:.1f}")
    print(f"Skill level: {result['skill_level']}")

    print("\nStitch breakdown:")
    for stitch, count in result["stitch_breakdown"].items():
        print(f"  {stitch}: {count}")

    print("\n✨ Estimation complete!")
