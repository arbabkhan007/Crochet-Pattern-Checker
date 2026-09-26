"""
Complex Gauge Calculator - Calculate gauge for intricate patterns
"""


class ComplexGaugeCalculator:
    def __init__(self):
        self.pattern_types = {
            "lace": {"stretch_factor": 1.3, "blocking_effect": "significant"},
            "cable": {"stretch_factor": 0.8, "blocking_effect": "minimal"},
            "texture": {"stretch_factor": 1.1, "blocking_effect": "moderate"},
            "colorwork": {"stretch_factor": 1.0, "blocking_effect": "minimal"},
        }

    def calculate_complex_gauge(
        self, swatch_measurements: dict, pattern_type: str
    ) -> dict:
        """Calculate gauge for complex patterns"""
        pattern_info = self.pattern_types.get(
            pattern_type, self.pattern_types["texture"]
        )

        raw_gauge = {
            "stitches_per_4in": swatch_measurements.get("stitches", 20) / 4,
            "rows_per_4in": swatch_measurements.get("rows", 24) / 4,
        }

        # Apply pattern-specific adjustments
        adjusted_gauge = {
            "stitches_per_4in": raw_gauge["stitches_per_4in"]
            * pattern_info["stretch_factor"],
            "rows_per_4in": raw_gauge["rows_per_4in"] * pattern_info["stretch_factor"],
        }

        return {
            "pattern_type": pattern_type,
            "raw_gauge": raw_gauge,
            "adjusted_gauge": adjusted_gauge,
            "stretch_factor": pattern_info["stretch_factor"],
            "blocking_effect": pattern_info["blocking_effect"],
            "recommendations": self._get_recommendations(pattern_type, adjusted_gauge),
            "swatch_size_recommendation": self._recommend_swatch_size(pattern_type),
        }

    def calculate_project_dimensions(
        self, gauge: dict, stitch_count: int, row_count: int
    ) -> dict:
        """Calculate final project dimensions"""
        width = (stitch_count / gauge["stitches_per_4in"]) * 4
        height = (row_count / gauge["rows_per_4in"]) * 4

        return {
            "width_inches": width,
            "height_inches": height,
            "width_cm": width * 2.54,
            "height_cm": height * 2.54,
            "total_stitches": stitch_count,
            "total_rows": row_count,
        }

    def _get_recommendations(self, pattern_type: str, gauge: dict) -> list:
        recommendations = []

        if pattern_type == "lace":
            recommendations.append("Block swatch before measuring")
            recommendations.append("Measure after blocking for accurate gauge")
        elif pattern_type == "cable":
            recommendations.append("Don't stretch when measuring")
            recommendations.append("Cables pull in - account for width reduction")
        elif pattern_type == "colorwork":
            recommendations.append("Keep tension consistent")
            recommendations.append("Floats affect gauge - don't pull too tight")

        recommendations.append("Make swatch at least 6x6 inches")
        recommendations.append("Wash and block swatch like finished project")

        return recommendations

    def _recommend_swatch_size(self, pattern_type: str) -> str:
        sizes = {
            "lace": "8x8 inches minimum - lace opens up significantly",
            "cable": "6x6 inches - cables need space to form",
            "texture": "6x6 inches - texture needs room",
            "colorwork": "6x6 inches - include pattern repeat",
        }
        return sizes.get(pattern_type, "6x6 inches")


if __name__ == "__main__":
    print("📏 Complex Gauge Calculator")
    print("=" * 60)

    calculator = ComplexGaugeCalculator()

    # Test with lace pattern
    swatch = {"stitches": 24, "rows": 32}
    result = calculator.calculate_complex_gauge(swatch, "lace")

    print(f"\nPattern Type: {result['pattern_type']}")
    print(
        f"Raw Gauge: {result['raw_gauge']['stitches_per_4in']:.1f} sts x {result['raw_gauge']['rows_per_4in']:.1f} rows"
    )
    print(
        f"Adjusted Gauge: {result['adjusted_gauge']['stitches_per_4in']:.1f} sts x {result['adjusted_gauge']['rows_per_4in']:.1f} rows"
    )
    print(f"Stretch Factor: {result['stretch_factor']}")
    print(f"Blocking Effect: {result['blocking_effect']}")

    print("\nRecommendations:")
    for rec in result["recommendations"]:
        print(f"  • {rec}")

    print(f"\nSwatch Size: {result['swatch_size_recommendation']}")

    # Calculate project dimensions
    dimensions = calculator.calculate_project_dimensions(
        result["adjusted_gauge"], 100, 120
    )
    print("\nProject Dimensions (100 sts x 120 rows):")
    print(
        f"  Width: {dimensions['width_inches']:.1f} inches ({dimensions['width_cm']:.1f} cm)"
    )
    print(
        f"  Height: {dimensions['height_inches']:.1f} inches ({dimensions['height_cm']:.1f} cm)"
    )
