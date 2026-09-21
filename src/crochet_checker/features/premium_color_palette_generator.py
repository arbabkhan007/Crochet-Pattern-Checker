"""
Premium Color Palette Generator - World-class color schemes
"""
import colorsys

class PremiumColorPaletteGenerator:
    def __init__(self):
        self.premium_palettes = {
            "luxury_neutrals": ["#2C2C2C", "#8B7355", "#D4AF37", "#F5F5DC", "#FFFFFF"],
            "ocean_breeze": ["#006994", "#0099CC", "#66CCCC", "#99CCCC", "#CCEEEE"],
            "sunset_glow": ["#FF6B6B", "#FF8E53", "#FED766", "#FEC260", "#FFA07A"],
            "forest_mist": ["#2D5016", "#4A7C2C", "#6B9B37", "#8FB55C", "#B8D68C"],
            "royal_elegance": ["#4B0082", "#6A0DAD", "#9B30FF", "#BA55D3", "#DDA0DD"],
            "scandinavian": ["#F7F9FC", "#E8EEF2", "#B8C5D0", "#6B7C8F", "#2C3E50"],
        }
    
    def generate_palette(self, base_color: str, palette_type: str = "analogous") -> list:
        """Generate premium color palette from base color"""
        rgb = self._hex_to_rgb(base_color)
        h, l, s = colorsys.rgb_to_hls(rgb[0]/255, rgb[1]/255, rgb[2]/255)
        
        palette = []
        
        if palette_type == "analogous":
            for i in range(5):
                new_h = (h + i * 0.05) % 1.0
                r, g, b = colorsys.hls_to_rgb(new_h, l, s)
                palette.append(self._rgb_to_hex(int(r*255), int(g*255), int(b*255)))
        
        elif palette_type == "complementary":
            palette.append(base_color)
            comp_h = (h + 0.5) % 1.0
            r, g, b = colorsys.hls_to_rgb(comp_h, l, s)
            palette.append(self._rgb_to_hex(int(r*255), int(g*255), int(b*255)))
            # Add variations
            for i in range(3):
                r, g, b = colorsys.hls_to_rgb(h, l * (0.8 + i * 0.1), s)
                palette.append(self._rgb_to_hex(int(r*255), int(g*255), int(b*255)))
        
        elif palette_type == "triadic":
            for i in range(3):
                new_h = (h + i * 0.33) % 1.0
                r, g, b = colorsys.hls_to_rgb(new_h, l, s)
                palette.append(self._rgb_to_hex(int(r*255), int(g*255), int(b*255)))
            palette.extend(palette[:2])
        
        return palette[:5]
    
    def get_premium_palette(self, palette_name: str) -> list:
        """Get pre-made premium palette"""
        return self.premium_palettes.get(palette_name, self.premium_palettes["luxury_neutrals"])
    
    def _hex_to_rgb(self, hex_color: str) -> tuple:
        """Convert hex to RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def _rgb_to_hex(self, r: int, g: int, b: int) -> str:
        """Convert RGB to hex"""
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def generate_color_scheme_report(self, palette: list) -> str:
        """Generate color scheme report"""
        report = "PREMIUM COLOR PALETTE\n" + "=" * 60 + "\n\n"
        for i, color in enumerate(palette, 1):
            report += f"Color {i}: {color}\n"
        report += "\n✨ Premium palette generated!"
        return report

if __name__ == "__main__":
    print("🎨 Premium Color Palette Generator")
    print("=" * 60)
    
    generator = PremiumColorPaletteGenerator()
    
    print("\n📊 Generating luxury palette...")
    palette = generator.get_premium_palette("luxury_neutrals")
    print(generator.generate_color_scheme_report(palette))
    
    print("\n🎨 Creating custom palette from #3498DB...")
    custom = generator.generate_palette("#3498DB", "analogous")
    print(f"Generated: {custom}")
    
    print("\n✨ Premium palette generation complete!")
