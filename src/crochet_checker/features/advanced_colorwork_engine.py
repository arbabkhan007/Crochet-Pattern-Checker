"""
Advanced Colorwork Engine - Handle complex color patterns (tapestry, intarsia, Fair Isle)
"""


class AdvancedColorworkEngine:
    def __init__(self):
        self.colorwork_types = {
            "tapestry": {"yarn_management": "carry", "complexity": "high"},
            "intarsia": {"yarn_management": "separate_bobbins", "complexity": "expert"},
            "fair_isle": {"yarn_management": "stranded", "complexity": "advanced"},
        }

    def analyze_colorwork(self, pattern_text: str, color_chart: list) -> dict:
        """Analyze complex colorwork pattern"""
        colors_used = set()
        color_changes = 0

        # Parse pattern for colors
        for line in pattern_text.split("\n"):
            if "color" in line.lower() or any(c in line for c in ["A", "B", "C", "D"]):
                color_changes += 1
                colors_used.add(line.strip())

        # Determine colorwork type
        colorwork_type = self._detect_colorwork_type(pattern_text, color_chart)

        return {
            "colorwork_type": colorwork_type,
            "colors_used": len(colors_used),
            "color_changes": color_changes,
            "yarn_management": self.colorwork_types[colorwork_type]["yarn_management"],
            "tension_tips": self._get_tension_tips(colorwork_type),
            "float_management": self._get_float_management(colorwork_type),
        }

    def _detect_colorwork_type(self, pattern_text: str, chart: list) -> str:
        text_lower = pattern_text.lower()
        if "tapestry" in text_lower:
            return "tapestry"
        elif "intarsia" in text_lower:
            return "intarsia"
        elif "fair isle" in text_lower or "stranded" in text_lower:
            return "fair_isle"
        else:
            return "tapestry"  # default

    def _get_tension_tips(self, colorwork_type: str) -> list:
        tips = {
            "tapestry": [
                "Keep carried yarn loose",
                "Don't pull working yarn too tight",
            ],
            "intarsia": [
                "Twist yarns at color changes",
                "Use separate bobbins for each color",
            ],
            "fair_isle": [
                "Catch floats every 3-4 stitches",
                "Keep floats uniform length",
            ],
        }
        return tips.get(colorwork_type, [])

    def _get_float_management(self, colorwork_type: str) -> str:
        management = {
            "tapestry": "Enclose carried yarn within stitches",
            "intarsia": "No floats - twist at each color change",
            "fair_isle": "Catch floats on wrong side every 3-4 stitches",
        }
        return management.get(colorwork_type, "Standard float management")

    def generate_color_chart_visualization(self, chart: list) -> str:
        """Generate visual representation of color chart"""
        viz = "🎨 COLOR CHART\n" + "=" * 60 + "\n\n"
        for i, row in enumerate(chart, 1):
            viz += f"Row {i:2d}: " + " ".join(row) + "\n"
        return viz


if __name__ == "__main__":
    print("🎨 Advanced Colorwork Engine")
    print("=" * 60)

    engine = AdvancedColorworkEngine()

    # Test with colorwork pattern
    pattern = """
    Row 1: sc 5 in color A, sc 5 in color B (tapestry crochet)
    Row 2: sc 5 in color B, sc 5 in color A
    Row 3: intarsia technique - separate bobbins
    """

    color_chart = [
        ["A", "A", "B", "B", "A"],
        ["B", "A", "A", "B", "B"],
        ["A", "B", "B", "A", "A"],
    ]

    result = engine.analyze_colorwork(pattern, color_chart)
    print(f"\nColorwork Type: {result['colorwork_type']}")
    print(f"Colors Used: {result['colors_used']}")
    print(f"Yarn Management: {result['yarn_management']}")
    print(f"Float Management: {result['float_management']}")

    print("\nTension Tips:")
    for tip in result["tension_tips"]:
        print(f"  • {tip}")

    print("\n" + engine.generate_color_chart_visualization(color_chart))
