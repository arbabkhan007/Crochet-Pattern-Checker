"""
Color Pattern Simulator - Simulate colorwork patterns
"""

class ColorPatternSimulator:
    def __init__(self):
        self.color_map = {
            "A": "#FF0000",  # Red
            "B": "#0000FF",  # Blue
            "C": "#00FF00",  # Green
            "D": "#FFFF00",  # Yellow
        }
    
    def simulate_color_pattern(self, pattern_grid: list) -> dict:
        """Simulate color pattern"""
        color_changes = 0
        color_usage = {}
        
        for row in pattern_grid:
            prev_color = None
            for color in row:
                color_usage[color] = color_usage.get(color, 0) + 1
                if prev_color and color != prev_color:
                    color_changes += 1
                prev_color = color
        
        return {
            "total_stitches": sum(len(row) for row in pattern_grid),
            "color_changes": color_changes,
            "colors_used": list(color_usage.keys()),
            "color_distribution": color_usage,
            "complexity": "simple" if color_changes < 10 else "moderate" if color_changes < 30 else "complex"
        }
    
    def generate_visual_preview(self, pattern_grid: list) -> str:
        """Generate ASCII visual preview"""
        preview = "COLOR PATTERN PREVIEW\n" + "=" * 40 + "\n"
        for row in pattern_grid:
            preview += " ".join(row) + "\n"
        return preview

if __name__ == "__main__":
    print("🎨 Color Pattern Simulator")
    print("=" * 60)
    
    simulator = ColorPatternSimulator()
    
    pattern_grid = [
        ["A", "A", "B", "B", "A", "A"],
        ["A", "B", "B", "A", "A", "B"],
        ["B", "B", "A", "A", "B", "B"],
        ["B", "A", "A", "B", "B", "A"],
    ]
    
    print("\n📊 Simulating color pattern...")
    result = simulator.simulate_color_pattern(pattern_grid)
    
    print(f"\nTotal stitches: {result['total_stitches']}")
    print(f"Color changes: {result['color_changes']}")
    print(f"Colors used: {result['colors_used']}")
    print(f"Complexity: {result['complexity']}")
    
    print("\nColor distribution:")
    for color, count in result['color_distribution'].items():
        print(f"  Color {color}: {count} stitches")
    
    print("\n" + simulator.generate_visual_preview(pattern_grid))
    print("✨ Simulation complete!")
