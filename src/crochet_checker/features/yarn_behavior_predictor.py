"""
Yarn Behavior Predictor - Predict how yarn will behave in patterns
"""


class YarnBehaviorPredictor:
    def __init__(self):
        self.yarn_properties = {
            "wool": {"stretch": 0.15, "memory": 0.9, "warmth": 0.95, "durability": 0.7},
            "cotton": {
                "stretch": 0.05,
                "memory": 0.3,
                "warmth": 0.3,
                "durability": 0.9,
            },
            "acrylic": {
                "stretch": 0.10,
                "memory": 0.5,
                "warmth": 0.6,
                "durability": 0.8,
            },
            "alpaca": {
                "stretch": 0.20,
                "memory": 0.7,
                "warmth": 0.98,
                "durability": 0.6,
            },
            "bamboo": {
                "stretch": 0.08,
                "memory": 0.4,
                "warmth": 0.4,
                "durability": 0.7,
            },
        }

    def predict_behavior(self, yarn_type: str, pattern_type: str) -> dict:
        """Predict yarn behavior in specific pattern"""
        props = self.yarn_properties.get(
            yarn_type.lower(), self.yarn_properties["acrylic"]
        )

        behavior = {
            "yarn_type": yarn_type,
            "pattern_type": pattern_type,
            "stretch_factor": props["stretch"],
            "memory_retention": props["memory"],
            "warmth_rating": props["warmth"],
            "durability_rating": props["durability"],
            "predicted_behavior": self._analyze_behavior(props, pattern_type),
            "best_for": self._recommend_use(props),
            "care_instructions": self._get_care_instructions(yarn_type),
        }

        return behavior

    def _analyze_behavior(self, props: dict, pattern_type: str) -> str:
        """Analyze how yarn will behave"""
        if pattern_type == "garment":
            if props["stretch"] > 0.15:
                return "May stretch significantly - consider lining"
            elif props["warmth"] > 0.8:
                return "Excellent for warm garments"
            else:
                return "Good drape and structure"
        elif pattern_type == "amigurumi":
            if props["memory"] > 0.7:
                return "Will hold shape well"
            else:
                return "May lose shape over time"
        else:
            return "Suitable for general use"

    def _recommend_use(self, props: dict) -> str:
        """Recommend best use for yarn"""
        if props["warmth"] > 0.8:
            return "Winter garments, blankets, scarves"
        elif props["durability"] > 0.8:
            return "Bags, hats, items requiring durability"
        elif props["stretch"] < 0.1:
            return "Summer garments, dishcloths, structured items"
        else:
            return "General purpose items"

    def _get_care_instructions(self, yarn_type: str) -> list:
        """Get care instructions"""
        care = {
            "wool": ["Hand wash cold", "Lay flat to dry", "Do not wring"],
            "cotton": ["Machine wash warm", "Tumble dry low", "Can iron"],
            "acrylic": ["Machine wash warm", "Tumble dry low", "Do not iron"],
            "alpaca": ["Hand wash cold", "Lay flat to dry", "Dry clean recommended"],
        }
        return care.get(yarn_type.lower(), ["Follow yarn label instructions"])


if __name__ == "__main__":
    print("🧶 Yarn Behavior Predictor")
    print("=" * 60)

    predictor = YarnBehaviorPredictor()

    print("\n📊 Predicting wool behavior in garment...")
    result = predictor.predict_behavior("wool", "garment")

    print(f"\nYarn: {result['yarn_type']}")
    print(f"Pattern: {result['pattern_type']}")
    print("\nProperties:")
    print(f"  Stretch: {result['stretch_factor']:.0%}")
    print(f"  Memory: {result['memory_retention']:.0%}")
    print(f"  Warmth: {result['warmth_rating']:.0%}")
    print(f"  Durability: {result['durability_rating']:.0%}")

    print(f"\nPredicted behavior: {result['predicted_behavior']}")
    print(f"Best for: {result['best_for']}")

    print("\nCare instructions:")
    for instruction in result["care_instructions"]:
        print(f"  • {instruction}")

    print("\n✨ Prediction complete!")
