"""
Complex Amigurumi Shaper - Advanced 3D shaping for amigurumi
"""


class ComplexAmigurumiShaper:
    def __init__(self):
        self.shaping_techniques = {
            "increases": {"method": "inc", "effect": "expand"},
            "decreases": {"method": "dec", "effect": "contract"},
            "3d_shaping": {"method": "strategic_inc_dec", "effect": "complex_curves"},
            "surface_crochet": {"method": "added_detail", "effect": "texture"},
        }

    def design_complex_shape(self, shape_type: str, dimensions: dict) -> dict:
        """Design complex 3D amigurumi shape"""
        if shape_type == "sphere":
            rounds = self._generate_sphere_rounds(dimensions.get("diameter", 10))
        elif shape_type == "oval":
            rounds = self._generate_oval_rounds(
                dimensions.get("length", 12), dimensions.get("width", 8)
            )
        elif shape_type == "complex":
            rounds = self._generate_complex_rounds(dimensions)
        else:
            rounds = self._generate_basic_rounds()

        return {
            "shape_type": shape_type,
            "rounds": rounds,
            "total_rounds": len(rounds),
            "final_stitch_count": rounds[-1]["count"] if rounds else 0,
            "stuffing_guide": self._get_stuffing_guide(len(rounds)),
            "assembly_notes": self._get_assembly_notes(shape_type),
        }

    def _generate_sphere_rounds(self, diameter: int) -> list:
        rounds = []
        max_count = diameter * 5

        # Increase to max
        for i in range(1, 7):
            count = 6 * i
            rounds.append(
                {
                    "round": len(rounds) + 1,
                    "instruction": "inc in each stitch around",
                    "count": count,
                }
            )

        # Work even
        for i in range(4):
            rounds.append(
                {
                    "round": len(rounds) + 1,
                    "instruction": "sc in each stitch around",
                    "count": max_count,
                }
            )

        # Decrease to close
        for i in range(6, 0, -1):
            count = 6 * i
            rounds.append(
                {
                    "round": len(rounds) + 1,
                    "instruction": "dec evenly around",
                    "count": count,
                }
            )

        return rounds

    def _generate_oval_rounds(self, length: int, width: int) -> list:
        rounds = []
        rounds.append(
            {
                "round": 1,
                "instruction": f"ch {length}, sc in 2nd ch from hook, sc across, 3 sc in last ch, rotate - sc in remaining ch, 2 sc in first ch",
                "count": length * 2 + 2,
            }
        )

        for i in range(2, 6):
            rounds.append(
                {
                    "round": i,
                    "instruction": "inc at each end, sc around",
                    "count": rounds[-1]["count"] + 4,
                }
            )

        return rounds

    def _generate_complex_rounds(self, dimensions: dict) -> list:
        # Generate complex multi-part shape
        rounds = []
        rounds.append({"round": 1, "instruction": "magic ring, 6 sc", "count": 6})
        rounds.append({"round": 2, "instruction": "inc in each around", "count": 12})
        rounds.append({"round": 3, "instruction": "*sc 2, inc* around", "count": 18})
        rounds.append(
            {
                "round": 4,
                "instruction": "sc around, add surface crochet details",
                "count": 18,
            }
        )
        return rounds

    def _get_stuffing_guide(self, total_rounds: int) -> str:
        if total_rounds < 10:
            return "Light stuffing - maintain shape"
        elif total_rounds < 20:
            return "Medium stuffing - firm but flexible"
        else:
            return "Firm stuffing - stuff as you go"

    def _get_assembly_notes(self, shape_type: str) -> list:
        notes = {
            "sphere": [
                "Stuff firmly before closing",
                "Use stitch markers for symmetry",
            ],
            "oval": ["Stuff ends first", "Shape while stuffing"],
            "complex": [
                "Stuff in sections",
                "Add features before assembly",
                "Use pins to hold parts",
            ],
        }
        return notes.get(shape_type, ["Standard assembly"])


if __name__ == "__main__":
    print("🧸 Complex Amigurumi Shaper")
    print("=" * 60)

    shaper = ComplexAmigurumiShaper()

    # Test sphere
    result = shaper.design_complex_shape("sphere", {"diameter": 10})
    print(f"\nShape: {result['shape_type']}")
    print(f"Total Rounds: {result['total_rounds']}")
    print(f"Final Stitch Count: {result['final_stitch_count']}")
    print(f"Stuffing: {result['stuffing_guide']}")

    print("\nFirst 5 rounds:")
    for r in result["rounds"][:5]:
        print(f"  Round {r['round']}: {r['instruction']} (count: {r['count']})")

    print("\nAssembly Notes:")
    for note in result["assembly_notes"]:
        print(f"  • {note}")
