"""
Yarn Dye Calculator - Calculate dye amounts for custom color mixing
"""
import colorsys
from typing import Tuple, Dict, List


class YarnDyeCalculator:
    """Calculate dye recipes for custom yarn colors"""
    
    # Base dye colors (simplified CMYK-like system)
    BASE_DYES = {
        "red": {"hex": "#FF0000", "ratio": 1.0},
        "blue": {"hex": "#0000FF", "ratio": 1.0},
        "yellow": {"hex": "#FFFF00", "ratio": 1.0},
        "black": {"hex": "#000000", "ratio": 0.5},
        "white": {"hex": "#FFFFFF", "ratio": 0.0},
    }
    
    def __init__(self):
        self.recipes = []
    
    def hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """Convert hex to RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def rgb_to_hex(self, r: int, g: int, b: int) -> str:
        """Convert RGB to hex"""
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def calculate_dye_recipe(self, target_hex: str, yarn_weight_grams: float) -> Dict:
        """
        Calculate dye amounts needed for target color
        Returns amounts in grams of each base dye
        """
        target_rgb = self.hex_to_rgb(target_hex)
        r, g, b = [x / 255.0 for x in target_rgb]
        
        # Convert to CMY (simplified dye mixing)
        c = 1 - r  # Cyan (blue component)
        m = 1 - g  # Magenta (red component)
        y = 1 - b  # Yellow
        
        # Calculate dye ratios
        total = c + m + y
        if total == 0:
            return {"white": yarn_weight_grams * 0.01, "other": {}}
        
        # Dye concentration (typically 1-3% of yarn weight)
        dye_concentration = 0.02  # 2%
        total_dye = yarn_weight_grams * dye_concentration
        
        recipe = {
            "target_color": target_hex,
            "yarn_weight_grams": yarn_weight_grams,
            "total_dye_grams": total_dye,
            "concentration_percent": dye_concentration * 100,
            "dyes": {
                "red": round(total_dye * m / total, 2),
                "blue": round(total_dye * c / total, 2),
                "yellow": round(total_dye * y / total, 2),
            },
            "water_ml": yarn_weight_grams * 0.5,  # 50ml water per 100g yarn
            "instructions": self._generate_instructions(total_dye, yarn_weight_grams),
        }
        
        # Add darker tones if needed
        k = min(c, m, y)
        if k > 0.3:
            recipe["dyes"]["black"] = round(total_dye * k * 0.3, 2)
        
        return recipe
    
    def mix_colors(self, color1_hex: str, color2_hex: str, ratio: float = 0.5) -> str:
        """Mix two colors together"""
        rgb1 = self.hex_to_rgb(color1_hex)
        rgb2 = self.hex_to_rgb(color2_hex)
        
        mixed = tuple(
            int(rgb1[i] * (1 - ratio) + rgb2[i] * ratio)
            for i in range(3)
        )
        
        return self.rgb_to_hex(*mixed)
    
    def create_gradient(self, start_hex: str, end_hex: str, steps: int = 5) -> List[str]:
        """Create color gradient between two colors"""
        gradient = []
        for i in range(steps):
            ratio = i / (steps - 1) if steps > 1 else 0
            color = self.mix_colors(start_hex, end_hex, ratio)
            gradient.append(color)
        return gradient
    
    def _generate_instructions(self, total_dye: float, yarn_weight: float) -> List[str]:
        """Generate dyeing instructions"""
        return [
            f"1. Soak {yarn_weight}g yarn in warm water for 30 minutes",
            f"2. Mix {total_dye:.1f}g dye powder with {yarn_weight * 0.5:.0f}ml warm water",
            "3. Add vinegar (1 tbsp per 100g yarn) to fix colors",
            "4. Submerge yarn in dye bath",
            "5. Heat slowly to 180°F (82°C) - do not boil",
            "6. Hold temperature for 30 minutes, stirring gently",
            "7. Let cool completely before rinsing",
            "8. Rinse in cool water until water runs clear",
            "9. Hang to dry away from direct sunlight",
        ]
    
    def save_recipe(self, recipe: Dict, name: str):
        """Save a dye recipe"""
        recipe["name"] = name
        self.recipes.append(recipe)
    
    def get_recipe_book(self) -> List[Dict]:
        """Get all saved recipes"""
        return self.recipes


if __name__ == "__main__":
    print("🎨 Yarn Dye Calculator")
    print("=" * 50)
    
    calc = YarnDyeCalculator()
    
    print("\n🎯 Calculating recipe for coral pink...")
    recipe = calc.calculate_dye_recipe("#FF7F50", 100)  # 100g yarn
    print(f"Target color: {recipe['target_color']}")
    print(f"Yarn weight: {recipe['yarn_weight_grams']}g")
    print(f"\nDye amounts:")
    for dye, amount in recipe['dyes'].items():
        print(f"  {dye:10s}: {amount:5.2f}g")
    print(f"\nWater needed: {recipe['water_ml']:.0f}ml")
    print(f"Total dye: {recipe['total_dye_grams']:.2f}g ({recipe['concentration_percent']}%)")
    
    print("\n📋 Instructions:")
    for instruction in recipe['instructions']:
        print(f"  {instruction}")
    
    print("\n🌈 Color mixing demo:")
    mixed = calc.mix_colors("#FF0000", "#0000FF", 0.5)
    print(f"  Red + Blue (50/50) = {mixed}")
    
    print("\n🎨 Gradient from purple to orange:")
    gradient = calc.create_gradient("#800080", "#FFA500", 5)
    for i, color in enumerate(gradient, 1):
        print(f"  Step {i}: {color}")
    
    print("\n✅ Yarn Dye Calculator ready!")
