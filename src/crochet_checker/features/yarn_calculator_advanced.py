"""Yarn Calculator Advanced - Calculate yarn needs"""
class YarnCalculatorAdvanced:
    def calculate_yarn_needed(self, pattern_size: str, stitch_type: str) -> dict:
        base_yarn = {"small": 100, "medium": 300, "large": 600}
        return {"yards_needed": base_yarn.get(pattern_size, 200), "skeins": 2}

if __name__ == "__main__":
    print("🧮 Yarn Calculator Advanced - Working!")
    calc = YarnCalculatorAdvanced()
    result = calc.calculate_yarn_needed("medium", "sc")
    print(f"Yards needed: {result['yards_needed']}")
