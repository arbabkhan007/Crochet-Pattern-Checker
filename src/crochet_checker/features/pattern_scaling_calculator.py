"""Pattern Scaling Calculator - Resize patterns"""
class PatternScalingCalculator:
    def calculate_scaling(self, original_size: float, target_size: float) -> dict:
        ratio = target_size / original_size
        return {"ratio": ratio, "new_stitch_count": int(100 * ratio)}

if __name__ == "__main__":
    print("📏 Pattern Scaling Calculator - Working!")
    calc = PatternScalingCalculator()
    result = calc.calculate_scaling(10.0, 15.0)
    print(f"Scaling ratio: {result['ratio']}")
