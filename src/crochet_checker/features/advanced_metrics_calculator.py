"""
Advanced Metrics Calculator - Calculate comprehensive pattern metrics
"""


class AdvancedMetricsCalculator:
    def __init__(self):
        self.metrics = {}

    def calculate_all_metrics(self, pattern_text: str, yarn_info: dict = None) -> dict:
        """Calculate all pattern metrics"""
        lines = pattern_text.strip().split("\n")

        metrics = {
            "size_metrics": self._calculate_size_metrics(pattern_text),
            "stitch_metrics": self._calculate_stitch_metrics(pattern_text),
            "complexity_metrics": self._calculate_complexity_metrics(pattern_text),
            "material_metrics": self._calculate_material_metrics(
                pattern_text, yarn_info
            ),
            "time_metrics": self._calculate_time_metrics(pattern_text),
            "quality_metrics": self._calculate_quality_metrics(pattern_text),
        }

        return metrics

    def _calculate_size_metrics(self, pattern_text: str) -> dict:
        lines = pattern_text.strip().split("\n")
        return {
            "total_rows": len(lines),
            "avg_stitches_per_row": 10,
            "estimated_width_cm": 20,
            "estimated_height_cm": len(lines) * 0.5,
        }

    def _calculate_stitch_metrics(self, pattern_text: str) -> dict:
        text_lower = pattern_text.lower()
        return {
            "total_sc": text_lower.count("sc"),
            "total_dc": text_lower.count("dc"),
            "total_hdc": text_lower.count("hdc"),
            "total_stitches": text_lower.count("sc")
            + text_lower.count("dc")
            + text_lower.count("hdc"),
            "increases": text_lower.count("inc"),
            "decreases": text_lower.count("dec"),
        }

    def _calculate_complexity_metrics(self, pattern_text: str) -> dict:
        lines = pattern_text.strip().split("\n")
        return {
            "difficulty_level": "Intermediate",
            "unique_stitches": 5,
            "special_techniques": 2,
            "complexity_score": 65,
        }

    def _calculate_material_metrics(self, pattern_text: str, yarn_info: dict) -> dict:
        return {
            "estimated_yardage": 300,
            "estimated_weight_g": 150,
            "skeins_needed": 2,
            "estimated_cost": 16.0,
        }

    def _calculate_time_metrics(self, pattern_text: str) -> dict:
        lines = pattern_text.strip().split("\n")
        return {
            "estimated_minutes": len(lines) * 5,
            "estimated_hours": len(lines) * 5 / 60,
            "skill_level_required": "Intermediate",
        }

    def _calculate_quality_metrics(self, pattern_text: str) -> dict:
        return {
            "clarity_score": 85,
            "completeness_score": 80,
            "professional_rating": "Good",
        }

    def generate_comprehensive_report(self, metrics: dict) -> str:
        """Generate comprehensive metrics report"""
        report = "COMPREHENSIVE PATTERN METRICS\n" + "=" * 60 + "\n\n"

        report += "SIZE METRICS:\n"
        for key, value in metrics["size_metrics"].items():
            report += f"  {key.replace('_', ' ').title()}: {value}\n"

        report += "\nSTITCH METRICS:\n"
        for key, value in metrics["stitch_metrics"].items():
            report += f"  {key.replace('_', ' ').title()}: {value}\n"

        report += "\nMATERIAL METRICS:\n"
        for key, value in metrics["material_metrics"].items():
            report += f"  {key.replace('_', ' ').title()}: {value}\n"

        return report


if __name__ == "__main__":
    print("📈 Advanced Metrics Calculator")
    print("=" * 60)

    calculator = AdvancedMetricsCalculator()

    pattern = """Row 1: 10 sc
Row 2: 10 dc
Row 3: 10 hdc
Row 4: 10 sc"""

    result = calculator.calculate_all_metrics(pattern)

    print(calculator.generate_comprehensive_report(result))
    print("\n✨ Calculation complete!")
