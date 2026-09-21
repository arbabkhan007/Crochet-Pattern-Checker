"""
Virtual Swatch Generator - Generate virtual swatches to test patterns
"""

class VirtualSwatchGenerator:
    def __init__(self):
        self.swatch_data = {}
    
    def generate_swatch(self, pattern_text: str, size: tuple = (10, 10)) -> dict:
        """Generate a virtual swatch"""
        lines = pattern_text.strip().split('\n')
        
        swatch = {
            "width_stitches": size[0],
            "height_rows": size[1],
            "total_stitches": size[0] * size[1],
            "estimated_size_cm": {"width": size[0] * 0.5, "height": size[1] * 0.5},
            "pattern_used": lines[0][:50],
            "gauge_check": "pass" if len(lines) >= 2 else "insufficient_data"
        }
        
        self.swatch_data = swatch
        return swatch
    
    def check_gauge(self, swatch: dict, target_gauge: dict) -> dict:
        """Check if swatch matches target gauge"""
        actual_width = swatch["estimated_size_cm"]["width"]
        actual_height = swatch["estimated_size_cm"]["height"]
        target_width = target_gauge.get("width", 10)
        target_height = target_gauge.get("height", 10)
        
        width_diff = abs(actual_width - target_width)
        height_diff = abs(actual_height - target_height)
        
        return {
            "gauge_match": width_diff < 1 and height_diff < 1,
            "width_difference_cm": width_diff,
            "height_difference_cm": height_diff,
            "recommendation": "Adjust hook size" if width_diff > 1 or height_diff > 1 else "Gauge is correct"
        }
    
    def generate_swatch_visualization(self, swatch: dict) -> str:
        """Generate ASCII visualization of swatch"""
        width = min(swatch["width_stitches"], 20)
        height = min(swatch["height_rows"], 10)
        
        viz = "VIRTUAL SWATCH\n" + "=" * 40 + "\n"
        for row in range(height):
            viz += "• " * width + "\n"
        viz += f"\nSize: {width} x {height} stitches"
        
        return viz

if __name__ == "__main__":
    print("🧪 Virtual Swatch Generator")
    print("=" * 60)
    
    generator = VirtualSwatchGenerator()
    
    pattern = "Row 1: sc in each st across\nRow 2: ch 1, turn, sc across"
    
    print("\n📐 Generating swatch...")
    swatch = generator.generate_swatch(pattern, (10, 10))
    print(f"  Size: {swatch['estimated_size_cm']['width']} x {swatch['estimated_size_cm']['height']} cm")
    print(f"  Total stitches: {swatch['total_stitches']}")
    
    print("\n📏 Checking gauge...")
    gauge_check = generator.check_gauge(swatch, {"width": 5, "height": 5})
    print(f"  Gauge match: {gauge_check['gauge_match']}")
    print(f"  Recommendation: {gauge_check['recommendation']}")
    
    print("\n" + generator.generate_swatch_visualization(swatch))
    print("\n✨ Swatch generation complete!")
