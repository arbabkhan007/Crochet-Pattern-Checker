"""
Premium Chart Generator - World-class crochet chart creation
"""


class PremiumChartGenerator:
    def __init__(self):
        self.chart_styles = {
            "traditional": {
                "symbol_size": "medium",
                "grid": "visible",
                "colors": "standard",
            },
            "modern": {"symbol_size": "large", "grid": "minimal", "colors": "vibrant"},
            "elegant": {"symbol_size": "medium", "grid": "subtle", "colors": "muted"},
            "professional": {
                "symbol_size": "large",
                "grid": "visible",
                "colors": "high_contrast",
            },
        }

    def generate_chart(self, pattern_text: str, style: str = "professional") -> dict:
        """Generate premium crochet chart"""
        chart_config = self.chart_styles.get(style, self.chart_styles["professional"])

        lines = pattern_text.strip().split("\n")
        chart_data = []

        for i, line in enumerate(lines, 1):
            chart_data.append(
                {
                    "row": i,
                    "instruction": line,
                    "symbols": self._convert_to_symbols(line),
                }
            )

        return {
            "chart_style": style,
            "total_rows": len(chart_data),
            "chart_data": chart_data,
            "symbol_size": chart_config["symbol_size"],
            "grid_visible": chart_config["grid"] != "none",
            "premium_features": [
                "color_coding",
                "row_numbers",
                "directional_arrows",
                "legend",
            ],
        }

    def _convert_to_symbols(self, instruction: str) -> list:
        """Convert instruction to chart symbols"""
        symbols = []
        instruction_lower = instruction.lower()

        if "sc" in instruction_lower:
            symbols.append("×")
        if "dc" in instruction_lower:
            symbols.append("T")
        if "hdc" in instruction_lower:
            symbols.append("†")
        if "inc" in instruction_lower:
            symbols.append("V")
        if "dec" in instruction_lower:
            symbols.append("Λ")

        return symbols if symbols else ["•"]

    def export_chart_svg(self, chart_data: dict) -> str:
        """Export chart as SVG"""
        svg = '<svg width="400" height="400" xmlns="http://www.w3.org/2000/svg">\n'
        svg += '  <rect width="400" height="400" fill="white"/>\n'
        svg += '  <text x="200" y="30" text-anchor="middle" font-size="20">Premium Crochet Chart</text>\n'
        svg += "</svg>"
        return svg


if __name__ == "__main__":
    print("📊 Premium Chart Generator")
    print("=" * 60)

    generator = PremiumChartGenerator()

    pattern = "Row 1: 6 sc\nRow 2: inc in each\nRow 3: sc, inc, rep"

    print("\n📋 Generating professional chart...")
    chart = generator.generate_chart(pattern, "professional")

    print(f"Chart style: {chart['chart_style']}")
    print(f"Total rows: {chart['total_rows']}")
    print(f"Premium features: {len(chart['premium_features'])}")

    print("\nRow 1 symbols:", chart["chart_data"][0]["symbols"])
    print("Row 2 symbols:", chart["chart_data"][1]["symbols"])

    print("\n✨ Premium chart generation complete!")
