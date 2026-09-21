"""
Premium Pattern Styler - World-class pattern styling and presentation
"""

class PremiumPatternStyler:
    def __init__(self):
        self.style_templates = {
            "magazine": {
                "font": "Helvetica",
                "layout": "grid",
                "spacing": "premium",
                "decoration": "elegant_borders"
            },
            "book": {
                "font": "Garamond",
                "layout": "traditional",
                "spacing": "comfortable",
                "decoration": "classic_ornaments"
            },
            "modern": {
                "font": "Arial",
                "layout": "minimalist",
                "spacing": "spacious",
                "decoration": "geometric"
            },
            "vintage": {
                "font": "Times New Roman",
                "layout": "ornate",
                "spacing": "detailed",
                "decoration": "floral_borders"
            }
        }
    
    def style_pattern(self, pattern_text: str, style_name: str = "magazine") -> dict:
        """Apply premium styling to pattern"""
        template = self.style_templates.get(style_name, self.style_templates["magazine"])
        
        styled_content = {
            "original": pattern_text,
            "style": style_name,
            "font": template["font"],
            "layout": template["layout"],
            "formatted_pattern": self._apply_formatting(pattern_text, template),
            "premium_elements": [
                "professional_header",
                "elegant_typography",
                "premium_spacing",
                template["decoration"]
            ]
        }
        
        return styled_content
    
    def _apply_formatting(self, pattern_text: str, template: dict) -> str:
        """Apply formatting based on template"""
        lines = pattern_text.strip().split('\n')
        formatted_lines = []
        
        for line in lines:
            if "row" in line.lower() or "round" in line.lower():
                formatted_lines.append(f"\n**{line}**\n")
            else:
                formatted_lines.append(line)
        
        return '\n'.join(formatted_lines)
    
    def get_available_styles(self) -> list:
        """Get available style templates"""
        return list(self.style_templates.keys())
    
    def preview_style(self, style_name: str) -> str:
        """Preview style characteristics"""
        template = self.style_templates.get(style_name, {})
        preview = f"Style: {style_name.title()}\n"
        preview += f"Font: {template.get('font', 'Default')}\n"
        preview += f"Layout: {template.get('layout', 'Standard')}\n"
        preview += f"Decoration: {template.get('decoration', 'None')}\n"
        return preview

if __name__ == "__main__":
    print("✨ Premium Pattern Styler")
    print("=" * 60)
    
    styler = PremiumPatternStyler()
    
    print("\n📋 Available styles:")
    for style in styler.get_available_styles():
        print(f"  • {style}")
    
    pattern = "Row 1: 10 sc\nRow 2: 10 dc\nRow 3: 10 hdc"
    
    print("\n🎨 Applying magazine style...")
    styled = styler.style_pattern(pattern, "magazine")
    print(f"Style: {styled['style']}")
    print(f"Premium elements: {len(styled['premium_elements'])}")
    
    print("\n" + styler.preview_style("vintage"))
    print("\n✨ Premium styling complete!")
