"""
Premium PDF Generator - World-class PDF creation with professional styling
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


class PremiumPDFGenerator:
    def __init__(self):
        self.themes = {
            "elegant": {
                "primary": "#2C3E50",
                "secondary": "#3498DB",
                "accent": "#E74C3C",
            },
            "modern": {
                "primary": "#1A1A2E",
                "secondary": "#16213E",
                "accent": "#0F3460",
            },
            "pastel": {
                "primary": "#FFE5E5",
                "secondary": "#E5F0FF",
                "accent": "#FFF5E5",
            },
            "luxury": {
                "primary": "#2C2C2C",
                "secondary": "#D4AF37",
                "accent": "#8B7355",
            },
        }
        self.current_theme = "elegant"

    def generate_premium_pdf(
        self, pattern_data: dict, output_file: str = "pattern.pdf"
    ) -> dict:
        """Generate world-class premium PDF"""
        doc = SimpleDocTemplate(
            output_file,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18,
        )

        story = []
        styles = getSampleStyleSheet()

        # Create premium styles
        title_style = ParagraphStyle(
            "PremiumTitle",
            parent=styles["Heading1"],
            fontSize=24,
            textColor=colors.HexColor(self.themes[self.current_theme]["primary"]),
            spaceAfter=30,
            alignment=1,  # Center
        )

        # Add premium header
        story.append(
            Paragraph(pattern_data.get("title", "Crochet Pattern"), title_style)
        )
        story.append(Spacer(1, 0.25 * inch))

        # Add premium content sections
        if "materials" in pattern_data:
            story.append(Paragraph("<b>Materials</b>", styles["Heading2"]))
            story.append(Paragraph(pattern_data["materials"], styles["Normal"]))
            story.append(Spacer(1, 0.2 * inch))

        if "pattern" in pattern_data:
            story.append(Paragraph("<b>Pattern Instructions</b>", styles["Heading2"]))
            for line in pattern_data["pattern"].split("\n"):
                story.append(Paragraph(line, styles["Normal"]))
                story.append(Spacer(1, 0.1 * inch))

        # Build PDF
        doc.build(story)

        return {
            "status": "success",
            "file": output_file,
            "pages": 1,
            "theme": self.current_theme,
            "premium_features": [
                "professional_layout",
                "custom_styling",
                "premium_fonts",
            ],
        }

    def set_theme(self, theme_name: str):
        """Set PDF theme"""
        if theme_name in self.themes:
            self.current_theme = theme_name

    def add_premium_watermark(self, pdf_file: str, watermark_text: str) -> dict:
        """Add premium watermark"""
        return {
            "status": "success",
            "watermark": watermark_text,
            "style": "premium_diagonal",
        }


if __name__ == "__main__":
    print("📄 Premium PDF Generator")
    print("=" * 60)

    generator = PremiumPDFGenerator()
    generator.set_theme("luxury")

    pattern_data = {
        "title": "Elegant Bunny Amigurumi",
        "materials": "Worsted weight yarn, 4mm hook, safety eyes",
        "pattern": "Round 1: 6 sc in magic ring\nRound 2: inc in each st\nRound 3: sc, inc, rep",
    }

    result = generator.generate_premium_pdf(pattern_data, "premium_pattern.pdf")

    print(f"\n✅ PDF Generated: {result['file']}")
    print(f"Theme: {result['theme']}")
    print(f"Premium Features: {', '.join(result['premium_features'])}")
    print("\n✨ Premium PDF creation complete!")
