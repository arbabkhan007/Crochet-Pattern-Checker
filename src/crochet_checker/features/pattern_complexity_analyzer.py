"""
Pattern Complexity Analyzer - Analyze pattern complexity in depth
"""


class PatternComplexityAnalyzer:
    def __init__(self):
        self.complexity_weights = {
            "sc": 1,
            "dc": 2,
            "hdc": 1.5,
            "tr": 3,
            "sl_st": 0.5,
            "inc": 2,
            "dec": 2,
            "fpdc": 3,
            "bpdc": 3,
            "magic_ring": 3,
            "bobble": 4,
            "popcorn": 4,
        }

    def analyze_complexity(self, pattern_text: str) -> dict:
        """Analyze pattern complexity"""
        lines = pattern_text.strip().split("\n")
        total_complexity = 0
        technique_count = {}

        for line in lines:
            line_lower = line.lower()
            for technique, weight in self.complexity_weights.items():
                count = line_lower.count(technique)
                if count > 0:
                    technique_count[technique] = (
                        technique_count.get(technique, 0) + count
                    )
                    total_complexity += count * weight

        avg_complexity = total_complexity / len(lines) if lines else 0

        difficulty = self._calculate_difficulty(avg_complexity, technique_count)

        return {
            "total_complexity_score": total_complexity,
            "avg_complexity_per_row": avg_complexity,
            "techniques_used": technique_count,
            "unique_techniques": len(technique_count),
            "difficulty_level": difficulty["level"],
            "difficulty_score": difficulty["score"],
            "estimated_learning_time_hours": difficulty["score"] * 0.5,
            "recommendations": self._get_recommendations(difficulty["level"]),
        }

    def _calculate_difficulty(self, avg_complexity: float, techniques: dict) -> dict:
        """Calculate difficulty level"""
        score = avg_complexity + len(techniques) * 2

        if score < 5:
            return {"level": "Beginner", "score": score}
        elif score < 15:
            return {"level": "Easy", "score": score}
        elif score < 30:
            return {"level": "Intermediate", "score": score}
        elif score < 50:
            return {"level": "Advanced", "score": score}
        else:
            return {"level": "Expert", "score": score}

    def _get_recommendations(self, difficulty: str) -> list:
        """Get recommendations based on difficulty"""
        recommendations = {
            "Beginner": [
                "Perfect for learning",
                "Take your time",
                "Practice basic stitches first",
            ],
            "Easy": [
                "Good for confident beginners",
                "Read pattern thoroughly before starting",
            ],
            "Intermediate": [
                "Some experience required",
                "Practice special stitches separately",
            ],
            "Advanced": ["Significant experience needed", "Make gauge swatch first"],
            "Expert": [
                "For experienced crocheters only",
                "Expect challenges",
                "Allow extra time",
            ],
        }
        return recommendations.get(difficulty, [])


if __name__ == "__main__":
    print("📊 Pattern Complexity Analyzer")
    print("=" * 60)

    analyzer = PatternComplexityAnalyzer()

    pattern = """Round 1: Magic ring, 6 sc
Round 2: inc in each st
Round 3: sc, inc, rep around
Round 4: fpdc in each st"""

    print("\n🔍 Analyzing complexity...")
    result = analyzer.analyze_complexity(pattern)

    print(f"\nComplexity Score: {result['total_complexity_score']}")
    print(f"Avg per Row: {result['avg_complexity_per_row']:.1f}")
    print(f"Unique Techniques: {result['unique_techniques']}")

    print(f"\nDifficulty Level: {result['difficulty_level']}")
    print(f"Difficulty Score: {result['difficulty_score']:.1f}")
    print(f"Learning Time: {result['estimated_learning_time_hours']:.1f} hours")

    print("\nTechniques used:")
    for technique, count in result["techniques_used"].items():
        print(f"  {technique}: {count}")

    print("\n💡 Recommendations:")
    for rec in result["recommendations"]:
        print(f"  • {rec}")

    print("\n✨ Analysis complete!")
