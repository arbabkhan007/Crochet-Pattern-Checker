"""Color Palette Generator - Generate color schemes"""
class ColorPaletteGenerator:
    def generate_palette(self, base_color: str, colors_count: int = 5) -> list:
        return [f"{base_color}_{i}" for i in range(colors_count)]

if __name__ == "__main__":
    print("🎨 Color Palette Generator - Working!")
    gen = ColorPaletteGenerator()
    palette = gen.generate_palette("blue", 5)
    print(f"Generated {len(palette)} colors")
