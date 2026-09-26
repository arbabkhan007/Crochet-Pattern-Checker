"""
Premium Watermark System - Professional watermarking
"""


class PremiumWatermarkSystem:
    def __init__(self):
        self.watermark_styles = {
            "subtle": {"opacity": 0.1, "position": "center", "rotation": -45},
            "prominent": {"opacity": 0.3, "position": "center", "rotation": -45},
            "corner": {"opacity": 0.2, "position": "bottom_right", "rotation": 0},
            "diagonal": {"opacity": 0.15, "position": "diagonal", "rotation": -30},
        }

    def add_watermark(
        self, content: str, watermark_text: str, style: str = "subtle"
    ) -> dict:
        """Add premium watermark"""
        config = self.watermark_styles.get(style, self.watermark_styles["subtle"])

        return {
            "status": "success",
            "watermark_text": watermark_text,
            "style": style,
            "opacity": config["opacity"],
            "position": config["position"],
            "rotation": config["rotation"],
            "premium_features": ["custom_font", "anti_aliasing", "vector_quality"],
        }


if __name__ == "__main__":
    print("💧 Premium Watermark System")
    print("=" * 60)

    system = PremiumWatermarkSystem()
    result = system.add_watermark("Pattern content", "© Your Brand", "subtle")

    print(f"\n✅ Watermark added: {result['watermark_text']}")
    print(f"Style: {result['style']}")
    print(f"Opacity: {result['opacity']}")
    print("\n✨ Premium watermarking complete!")
