"""
PDF Branding Studio - Create custom branded PDFs with logos, colors, watermarks
"""
from fpdf import FPDF
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _pdf_utils import setup_unicode_font, FONT
from typing import Dict, List, Optional
from datetime import datetime
import os


class PDFBrandingStudio:
    """
    Create branded PDFs with custom design elements
    
    Features:
    - Custom color schemes
    - Logo placement
    - Watermarks
    - Header/footer templates
    - Font selection
    - Brand guidelines PDF
    """
    
    BRAND_TEMPLATES = {
        "minimalist": {
            "primary": "#2C3E50",
            "secondary": "#BDC3C7",
            "accent": "#E74C3C",
            "bg": "#FFFFFF",
            "font_title": "DejaVu",
            "font_body": "DejaVu",
            "style": "clean",
        },
        "bohemian": {
            "primary": "#8B6914",
            "secondary": "#D4A574",
            "accent": "#C17817",
            "bg": "#FFF8F0",
            "font_title": "DejaVu",
            "font_body": "DejaVu",
            "style": "warm",
        },
        "modern_bold": {
            "primary": "#1A1A2E",
            "secondary": "#E94560",
            "accent": "#0F3460",
            "bg": "#F5F5F5",
            "font_title": "DejaVu",
            "font_body": "DejaVu",
            "style": "bold",
        },
        "pastel_dream": {
            "primary": "#FFB7C5",
            "secondary": "#FFDAB9",
            "accent": "#98FB98",
            "bg": "#FFFAF0",
            "font_title": "DejaVu",
            "font_body": "DejaVu",
            "style": "soft",
        },
        "dark_luxe": {
            "primary": "#0D0D0D",
            "secondary": "#333333",
            "accent": "#FFD700",
            "bg": "#FFFFFF",
            "font_title": "DejaVu",
            "font_body": "DejaVu",
            "style": "luxury",
        },
    }
    
    def __init__(self, brand_name: str = "", template: str = "minimalist"):
        self.brand_name = brand_name
        self.brand = self.BRAND_TEMPLATES.get(template, self.BRAND_TEMPLATES["minimalist"])
        self.pdf = FPDF()
        setup_unicode_font(self.pdf)
        # Register Unicode font
        import os
        font_path = '/usr/local/lib/python3.13/site-packages/cv2/qt/fonts/DejaVuSans.ttf'
        font_bold = '/usr/local/lib/python3.13/site-packages/cv2/qt/fonts/DejaVuSans-Bold.ttf'
        if os.path.exists(font_path):
            self.pdf.add_font('DejaVu', '', font_path, uni=True)
        if os.path.exists(font_bold):
            self.pdf.add_font('DejaVu', 'B', font_bold, uni=True)
    
    def _hex_to_rgb(self, hex_color: str) -> tuple:
        h = hex_color.lstrip('#')
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    
    def create_brand_guide_pdf(self, output_path: str) -> str:
        """Create a brand guidelines PDF"""
        # Cover page
        self.pdf.add_page()
        r, g, b = self._hex_to_rgb(self.brand["primary"])
        self.pdf.set_fill_color(r, g, b)
        self.pdf.rect(0, 0, 210, 297, 'F')
        
        self.pdf.set_text_color(255, 255, 255)
        self.pdf.set_y(80)
        self.pdf.set_font("DejaVu", "B", 36)
        self.pdf.cell(0, 15, "BRAND GUIDE", align='C')
        
        self.pdf.set_y(110)
        self.pdf.set_font("DejaVu", "", 18)
        self.pdf.cell(0, 12, self.brand_name, align='C')
        
        # Color palette page
        self.pdf.add_page()
        self._create_section_header("Color Palette")
        
        colors = [
            ("Primary", self.brand["primary"]),
            ("Secondary", self.brand["secondary"]),
            ("Accent", self.brand["accent"]),
            ("Background", self.brand["bg"]),
        ]
        
        y = 50
        for name, hex_color in colors:
            r, g, b = self._hex_to_rgb(hex_color)
            self.pdf.set_fill_color(r, g, b)
            self.pdf.rect(25, y, 40, 40, 'F')
            
            # Border
            self.pdf.set_draw_color(200, 200, 200)
            self.pdf.rect(25, y, 40, 40)
            
            # Info
            self.pdf.set_text_color(51, 51, 51)
            self.pdf.set_font("DejaVu", "B", 12)
            self.pdf.set_xy(75, y + 5)
            self.pdf.cell(0, 8, name)
            
            self.pdf.set_font("DejaVu", "", 10)
            self.pdf.set_xy(75, y + 15)
            self.pdf.cell(0, 7, f"HEX: {hex_color}")
            
            self.pdf.set_xy(75, y + 25)
            self.pdf.cell(0, 7, f"RGB: {r}, {g}, {b}")
            
            y += 50
        
        # Typography page
        self.pdf.add_page()
        self._create_section_header("Typography")
        
        self.pdf.set_y(50)
        self.pdf.set_text_color(51, 51, 51)
        
        # Title font
        self.pdf.set_font("DejaVu", "B", 24)
        self.pdf.cell(0, 12, "Title Font")
        
        self.pdf.set_font("DejaVu", "", 12)
        self.pdf.cell(0, 8, f"Font: {self.brand['font_title']}")
        self.pdf.ln(15)
        
        self.pdf.set_font("DejaVu", "", 14)
        self.pdf.cell(0, 10, "ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        self.pdf.ln(8)
        self.pdf.cell(0, 10, "abcdefghijklmnopqrstuvwxyz")
        self.pdf.ln(8)
        self.pdf.cell(0, 10, "0123456789")
        
        # Body font
        self.pdf.ln(20)
        self.pdf.set_font("DejaVu", "B", 24)
        self.pdf.cell(0, 12, "Body Font")
        
        self.pdf.set_font("DejaVu", "", 12)
        self.pdf.cell(0, 8, f"Font: {self.brand['font_body']}")
        self.pdf.ln(15)
        
        self.pdf.set_font("DejaVu", "", 12)
        sample = "The quick brown fox jumps over the lazy dog. This is how your body text will look in patterns and documents."
        self.pdf.multi_cell(0, 7, sample)
        
        # Logo placement page
        self.pdf.add_page()
        self._create_section_header("Logo Placement")
        
        self.pdf.set_y(50)
        self.pdf.set_text_color(51, 51, 51)
        self.pdf.set_font("DejaVu", "", 11)
        
        placements = [
            ("Top Left", "Use on letterheads and documents"),
            ("Center", "Use on covers and title pages"),
            ("Bottom Right", "Use as watermark on patterns"),
            ("Header", "Use on every page for brand recognition"),
        ]
        
        for position, usage in placements:
            self.pdf.set_font("DejaVu", "B", 12)
            r, g, b = self._hex_to_rgb(self.brand["accent"])
            self.pdf.set_text_color(r, g, b)
            self.pdf.cell(0, 8, f"- {position}")
            
            self.pdf.set_font("DejaVu", "", 10)
            self.pdf.set_text_color(51, 51, 51)
            self.pdf.set_x(30)
            self.pdf.cell(0, 7, usage)
            self.pdf.ln(10)
        
        # Save
        self.pdf.output(output_path)
        return output_path
    
    def _create_section_header(self, title: str):
        """Create section header"""
        r, g, b = self._hex_to_rgb(self.brand["primary"])
        self.pdf.set_fill_color(r, g, b)
        self.pdf.rect(0, 0, 210, 25, 'F')
        
        self.pdf.set_text_color(255, 255, 255)
        self.pdf.set_font("DejaVu", "B", 18)
        self.pdf.set_xy(20, 7)
        self.pdf.cell(170, 10, title, align='C')
    
    def create_watermarked_pdf(self, content_text: str, 
                              watermark_text: str = "",
                              output_path: str = "") -> str:
        """Create PDF with watermark"""
        if not watermark_text:
            watermark_text = self.brand_name
        
        self.pdf.add_page()
        
        # Content
        self.pdf.set_text_color(51, 51, 51)
        self.pdf.set_font("DejaVu", "", 12)
        self.pdf.set_xy(20, 20)
        self.pdf.multi_cell(170, 7, content_text)
        
        # Watermark (diagonal text across page)
        self.pdf.set_text_color(200, 200, 200)
        self.pdf.set_font("DejaVu", "B", 40)
        
        # Add watermark at multiple positions
        positions = [(50, 100), (30, 150), (70, 200)]
        for x, y in positions:
            self.pdf.set_xy(x, y)
            self.pdf.cell(0, 20, watermark_text.upper(), align='C')
        
        # Save
        if output_path:
            self.pdf.output(output_path)
            return output_path
    
    def create_letterhead(self, output_path: str) -> str:
        """Create branded letterhead"""
        self.pdf.add_page()
        
        # Header
        r, g, b = self._hex_to_rgb(self.brand["primary"])
        self.pdf.set_fill_color(r, g, b)
        self.pdf.rect(0, 0, 210, 30, 'F')
        
        # Brand name
        self.pdf.set_text_color(255, 255, 255)
        self.pdf.set_font("DejaVu", "B", 20)
        self.pdf.set_xy(15, 8)
        self.pdf.cell(100, 12, self.brand_name)
        
        # Logo placeholder
        self.pdf.set_draw_color(255, 255, 255)
        self.pdf.rect(160, 5, 35, 20)
        self.pdf.set_font("DejaVu", "I", 8)
        self.pdf.set_xy(160, 12)
        self.pdf.cell(35, 8, "LOGO", align='C')
        
        # Footer
        self.pdf.set_fill_color(r, g, b)
        self.pdf.rect(0, 280, 210, 17, 'F')
        
        self.pdf.set_text_color(255, 255, 255)
        self.pdf.set_font("DejaVu", "", 8)
        self.pdf.set_xy(15, 283)
        self.pdf.cell(180, 5, f"© {datetime.now().year} {self.brand_name} | www.yourwebsite.com | email@yourwebsite.com", align='C')
        
        # Content area
        self.pdf.set_text_color(51, 51, 51)
        self.pdf.set_xy(20, 40)
        self.pdf.set_font("DejaVu", "", 11)
        self.pdf.cell(0, 8, "Date: _______________")
        self.pdf.ln(15)
        self.pdf.cell(0, 8, "To: _______________")
        self.pdf.ln(20)
        
        self.pdf.multi_cell(170, 7, "Dear ________,\n\n[Your letter content goes here. This branded letterhead template can be used for business correspondence, customer communications, and official documents.]")
        
        # Save
        self.pdf.output(output_path)
        return output_path
    
    def create_pattern_header_footer(self) -> Dict:
        """Get header/footer specifications for patterns"""
        return {
            "header": {
                "height": 20,
                "background": self.brand["primary"],
                "text_color": "#FFFFFF",
                "font": "DejaVu",
                "size": 14,
                "content": self.brand_name,
                "align": "center",
            },
            "footer": {
                "height": 15,
                "background": self.brand["primary"],
                "text_color": "#FFFFFF",
                "font": "DejaVu",
                "size": 8,
                "content": f"© {datetime.now().year} {self.brand_name}",
                "align": "center",
            },
        }


# Demo
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  PDF BRANDING STUDIO - DEMO")
    print("=" * 60)
    
    # Create brand guide
    studio = PDFBrandingStudio(
        brand_name="Cozy Stitches Studio",
        template="bohemian",
    )
    
    output = "/home/user/demo_brand_guide.pdf"
    result = studio.create_brand_guide_pdf(output)
    
    print(f"\n[OK] Brand Guide Generated: {result}")
    print(f"   Brand: {studio.brand_name}")
    print(f"   Template: bohemian")
    print(f"   Includes: Colors, Typography, Logo placement")
    print(f"   File size: {os.path.getsize(result)} bytes")
    
    # Show color palette
    print(f"\n[COLOR] Color Palette:")
    for name, hex_color in [
        ("Primary", studio.brand["primary"]),
        ("Secondary", studio.brand["secondary"]),
        ("Accent", studio.brand["accent"]),
    ]:
        print(f"  {name}: {hex_color}")
    
    # Letterhead
    letterhead = "/home/user/demo_letterhead.pdf"
    studio2 = PDFBrandingStudio(brand_name="Cozy Stitches Studio", template="bohemian")
    studio2.create_letterhead(letterhead)
    print(f"\n[OK] Letterhead Generated: {letterhead}")
    
    # Available templates
    print(f"\n[LIST] Available Templates:")
    for template in PDFBrandingStudio.BRAND_TEMPLATES:
        print(f"  - {template}")
    
    print(f"\n  PDF Branding Studio Complete! [COLOR][*]")
