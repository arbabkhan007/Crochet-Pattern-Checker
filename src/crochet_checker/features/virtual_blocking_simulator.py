"""
Virtual Blocking Simulator - Simulate blocking results
"""


class VirtualBlockingSimulator:
    def __init__(self):
        self.fabric_properties = {
            "wool": {"stretch": 0.15, "shape_retention": "high"},
            "cotton": {"stretch": 0.05, "shape_retention": "medium"},
            "acrylic": {"stretch": 0.10, "shape_retention": "low"},
        }

    def simulate_blocking(
        self, current_size: dict, target_size: dict, yarn_type: str = "wool"
    ) -> dict:
        """Simulate blocking process"""
        yarn_props = self.fabric_properties.get(
            yarn_type, self.fabric_properties["wool"]
        )

        width_change = target_size["width"] - current_size["width"]
        height_change = target_size["height"] - current_size["height"]

        max_stretch = yarn_props["stretch"] * 100

        can_achieve = (
            abs(width_change) <= max_stretch and abs(height_change) <= max_stretch
        )

        return {
            "can_achieve_target": can_achieve,
            "width_change_cm": width_change,
            "height_change_cm": height_change,
            "max_possible_stretch_percent": max_stretch,
            "shape_retention": yarn_props["shape_retention"],
            "recommendation": "Blocking will work"
            if can_achieve
            else "Target size not achievable",
        }


if __name__ == "__main__":
    print("🧵 Virtual Blocking Simulator")
    print("=" * 60)

    simulator = VirtualBlockingSimulator()

    current = {"width": 20, "height": 25}
    target = {"width": 22, "height": 27}

    print(f"\nCurrent size: {current['width']}x{current['height']} cm")
    print(f"Target size: {target['width']}x{target['height']} cm")

    result = simulator.simulate_blocking(current, target, "wool")

    print(f"\nCan achieve target: {result['can_achieve_target']}")
    print(f"Width change: {result['width_change_cm']:+.1f} cm")
    print(f"Height change: {result['height_change_cm']:+.1f} cm")
    print(f"Shape retention: {result['shape_retention']}")
    print(f"💡 {result['recommendation']}")

    print("\n✨ Simulation complete!")
