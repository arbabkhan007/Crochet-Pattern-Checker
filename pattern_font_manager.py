"""Names fonts. It does not score them."""

class PatternFontManager:
    def __init__(self):
        self.recommended_fonts = [
            {"name": "Arial", "type": "sans-serif"},
            {"name": "Courier New", "type": "monospace"},
            {"name": "Times New Roman", "type": "serif"},
        ]

    def get_font_recommendations(self, pattern_type: str = "standard") -> list:
        return self.recommended_fonts

    def generate_font_preview(self, font_name: str) -> str:
        return f"Font: {font_name}. No readability score was invented."

if __name__ == "__main__":
    print(PatternFontManager().generate_font_preview("Arial"))
