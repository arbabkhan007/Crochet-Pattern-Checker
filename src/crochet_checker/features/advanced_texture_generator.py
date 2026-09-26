"""
Advanced Texture Generator - Create complex surface textures
"""


class AdvancedTextureGenerator:
    def __init__(self):
        self.texture_types = {
            "cable": {"complexity": "advanced", "technique": "cross_stitches"},
            "bobble": {
                "complexity": "intermediate",
                "technique": "multiple_stitches_one",
            },
            "popcorn": {"complexity": "intermediate", "technique": "cluster_work"},
            "puff": {"complexity": "intermediate", "technique": "yarn_overs"},
            "ripple": {
                "complexity": "advanced",
                "technique": "increase_decrease_pattern",
            },
            "waffle": {"complexity": "advanced", "technique": "fpdc_bpdc_pattern"},
            "basketweave": {
                "complexity": "advanced",
                "technique": "alternating_fpdc_bpdc",
            },
        }

    def generate_texture_pattern(self, texture_type: str, dimensions: dict) -> dict:
        """Generate complex texture pattern"""
        texture_info = self.texture_types.get(texture_type, self.texture_types["cable"])

        if texture_type == "cable":
            pattern = self._generate_cable_pattern(dimensions)
        elif texture_type == "bobble":
            pattern = self._generate_bobble_pattern(dimensions)
        elif texture_type == "waffle":
            pattern = self._generate_waffle_pattern(dimensions)
        else:
            pattern = self._generate_basic_texture(texture_type, dimensions)

        return {
            "texture_type": texture_type,
            "pattern": pattern,
            "complexity": texture_info["complexity"],
            "technique": texture_info["technique"],
            "hook_size_recommendation": self._recommend_hook(texture_type),
            "yarn_recommendation": self._recommend_yarn(texture_type),
        }

    def _generate_cable_pattern(self, dimensions: dict) -> list:
        width = dimensions.get("width", 20)
        pattern = []
        pattern.append(f"Ch {width + 5}")
        pattern.append("Row 1: dc in 4th ch from hook, dc across")
        pattern.append(
            "Row 2: ch 3, *skip 2, dc in next 2, dc in each of skipped 2 (cross), dc across, repeat from *"
        )
        pattern.append("Row 3: ch 3, dc across")
        pattern.append("Row 4: ch 3, dc across")
        pattern.append("Repeat rows 2-4 for cable pattern")
        return pattern

    def _generate_bobble_pattern(self, dimensions: dict) -> list:
        pattern = []
        pattern.append("Ch multiple of 6 + 3")
        pattern.append("Row 1: sc in 2nd ch from hook, sc across")
        pattern.append(
            "Row 2: ch 1, *sc 3, bobble (yo, insert hook, yo, pull up loop) 5 times in next st, yo, pull through all 6 loops, sc 3, repeat from * across"
        )
        pattern.append("Row 3: ch 1, sc across, working bobble in sc below")
        pattern.append("Repeat rows 2-3")
        return pattern

    def _generate_waffle_pattern(self, dimensions: dict) -> list:
        pattern = []
        pattern.append("Ch multiple of 3 + 2")
        pattern.append("Row 1: dc in 3rd ch from hook, dc across")
        pattern.append("Row 2: ch 2, *fpdc 2, bpdc 1, repeat from * across, turn")
        pattern.append("Row 3: ch 2, *bpdc 1, fpdc 2, repeat from * across, turn")
        pattern.append("Repeat rows 2-3 for waffle texture")
        return pattern

    def _generate_basic_texture(self, texture_type: str, dimensions: dict) -> list:
        pattern = []
        pattern.append("Ch multiple of 4 + 2")
        pattern.append("Row 1: sc in 2nd ch from hook, sc across")

        if texture_type == "popcorn":
            pattern.append(
                "Row 2: ch 1, *sc 2, popcorn (5 dc in next st, remove hook, insert in 1st dc, pull loop through), sc 2, repeat from *"
            )
        elif texture_type == "puff":
            pattern.append(
                "Row 2: ch 1, *puff (yo, insert hook, yo, pull up loop) 3 times in same st, yo, pull through all loops, ch 1, repeat from *"
            )

        return pattern

    def _recommend_hook(self, texture_type: str) -> str:
        recommendations = {
            "cable": "One size smaller than normal for defined cables",
            "bobble": "Same size or slightly larger for loose bobbles",
            "waffle": "Standard size for even texture",
            "ripple": "Standard size for smooth curves",
        }
        return recommendations.get(texture_type, "Standard hook size")

    def _recommend_yarn(self, texture_type: str) -> str:
        recommendations = {
            "cable": "Worsted weight with good stitch definition",
            "bobble": "Soft yarn that shows texture",
            "waffle": "Medium weight yarn, solid colors work best",
            "ripple": "Drapey yarn for soft waves",
        }
        return recommendations.get(texture_type, "Medium weight yarn")


if __name__ == "__main__":
    print("🎭 Advanced Texture Generator")
    print("=" * 60)

    generator = AdvancedTextureGenerator()

    # Test cable texture
    result = generator.generate_texture_pattern("cable", {"width": 20})
    print(f"\nTexture: {result['texture_type']}")
    print(f"Complexity: {result['complexity']}")
    print(f"Technique: {result['technique']}")

    print("\nPattern:")
    for row in result["pattern"]:
        print(f"  {row}")

    print(f"\nHook: {result['hook_size_recommendation']}")
    print(f"Yarn: {result['yarn_recommendation']}")
