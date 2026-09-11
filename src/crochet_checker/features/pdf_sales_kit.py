"""
PDF Sales Kit Generator - Create professional pattern sale packages for Etsy, Ravelry, etc.
"""
from fpdf import FPDF
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _pdf_utils import setup_unicode_font, FONT
from typing import Dict, List, Optional
from datetime import datetime
import os


class PDFSalesKit:
    """
    Generate professional sales kits for pattern sellers
    
    Features:
    - Pattern listing images (preview PDFs)
    - Technical spec sheets
    - Pricing calculator
    - Shop banner templates
    - Terms of use pages
    - Social media promo sheets
    """
    
    PLATFORM_SPECS = {
        "etsy": {
            "image_size": "2000x2000px",
            "max_pdf_size": "20MB",
            "max_pages": 200,
            "recommended": "1-10 pages for simple patterns",
        },
        "ravelry": {
            "image_size": "No limit",
            "max_pdf_size": "50MB",
            "max_pages": 500,
            "recommended": "Detailed patterns welcome",
        },
        "love_crochet": {
            "image_size": "1500x1500px",
            "max_pdf_size": "25MB",
            "max_pages": 100,
            "recommended": "Clear photos important",
        },
        "own_website": {
            "image_size": "Any",
            "max_pdf_size": "Any",
            "max_pages": "Any",
            "recommended": "Branded PDF recommended",
        },
    }
    
    def __init__(self, shop_name: str = "", brand_color: str = "#E74C3C"):
        self.shop_name = shop_name
        self.brand_color = brand_color
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
    
    def create_listing_preview(self, pattern_title: str, 
                              description: str = "",
                              difficulty: str = "",
                              finished_size: str = "",
                              yarn_weight: str = "",
                              hook_size: str = "") -> None:
        """Create a listing preview page (what customers see)"""
        self.pdf.add_page()
        
        # Background
        r, g, b = self._hex_to_rgb(self.brand_color)
        self.pdf.set_fill_color(r, g, b)
        self.pdf.rect(0, 0, 210, 80, 'F')
        
        # Title
        self.pdf.set_text_color(255, 255, 255)
        self.pdf.set_font("DejaVu", "B", 28)
        self.pdf.set_y(15)
        self.pdf.multi_cell(0, 12, pattern_title.upper(), align='C')
        
        # Photo area
        self.pdf.set_y(90)
        self.pdf.set_draw_color(200, 200, 200)
        self.pdf.set_fill_color(245, 245, 245)
        self.pdf.rect(30, 90, 150, 100, 'DF')
        self.pdf.set_text_color(150, 150, 150)
        self.pdf.set_font("DejaVu", "I", 12)
        self.pdf.set_xy(30, 135)
        self.pdf.cell(150, 10, "[Your beautiful photo here]", align='C')
        
        # Quick info boxes
        self.pdf.set_y(200)
        boxes = [
            ("Difficulty", difficulty or "Beginner"),
            ("Size", finished_size or "One Size"),
            ("Yarn", yarn_weight or "Worsted"),
            ("Hook", hook_size or "5.5mm"),
        ]
        
        for i, (label, value) in enumerate(boxes):
            x = 20 + (i * 45)
            # Box
            r, g, b = self._hex_to_rgb(self.brand_color)
            self.pdf.set_fill_color(r, g, b)
            self.pdf.rect(x, 200, 40, 35, 'F')
            
            # Label
            self.pdf.set_text_color(255, 255, 255)
            self.pdf.set_font("DejaVu", "", 8)
            self.pdf.set_xy(x, 202)
            self.pdf.cell(40, 8, label.upper(), align='C')
            
            # Value
            self.pdf.set_font("DejaVu", "B", 10)
            self.pdf.set_xy(x, 215)
            self.pdf.cell(40, 12, value, align='C')
        
        # Description
        self.pdf.set_y(245)
        self.pdf.set_text_color(51, 51, 51)
        self.pdf.set_font("DejaVu", "", 11)
        self.pdf.set_x(20)
        if description:
            self.pdf.multi_cell(170, 7, description)
    
    def create_terms_page(self) -> None:
        """Create terms of use page"""
        self.pdf.add_page()
        
        # Header
        r, g, b = self._hex_to_rgb(self.brand_color)
        self.pdf.set_fill_color(r, g, b)
        self.pdf.rect(0, 0, 210, 20, 'F')
        self.pdf.set_text_color(255, 255, 255)
        self.pdf.set_font("DejaVu", "B", 16)
        self.pdf.set_xy(0, 5)
        self.pdf.cell(210, 10, "TERMS OF USE", align='C')
        
        # Terms content
        self.pdf.set_text_color(51, 51, 51)
        self.pdf.set_y(30)
        
        terms = [
            ("PERSONAL USE", "This pattern is for personal, non-commercial use only."),
            ("NO SHARING", "Please do not share, redistribute, or resell this pattern."),
            ("FINISHED ITEMS", "You may sell finished items made from this pattern in small quantities (up to 50). Please credit the designer."),
            ("NO MASS PRODUCTION", "Mass production of finished items is not permitted."),
            ("PATTERN RIGHTS", "The pattern design, photos, and instructions are copyright protected."),
            ("REFUNDS", "Due to the digital nature of this product, refunds are not available after download."),
            ("QUESTIONS", f"Contact {self.shop_name} with any questions."),
        ]
        
        for title, description in terms:
            self.pdf.set_font("DejaVu", "B", 12)
            r, g, b = self._hex_to_rgb(self.brand_color)
            self.pdf.set_text_color(r, g, b)
            self.pdf.set_x(20)
            self.pdf.cell(0, 8, f"- {title}")
            
            self.pdf.set_font("DejaVu", "", 10)
            self.pdf.set_text_color(51, 51, 51)
            self.pdf.set_x(25)
            self.pdf.multi_cell(160, 6, description)
            self.pdf.ln(4)
    
    def create_pricing_sheet(self, patterns: List[Dict]) -> None:
        """Create pricing calculator sheet"""
        self.pdf.add_page()
        
        r, g, b = self._hex_to_rgb(self.brand_color)
        self.pdf.set_fill_color(r, g, b)
        self.pdf.rect(0, 0, 210, 20, 'F')
        self.pdf.set_text_color(255, 255, 255)
        self.pdf.set_font("DejaVu", "B", 16)
        self.pdf.set_xy(0, 5)
        self.pdf.cell(210, 10, "PRICING GUIDE", align='C')
        
        self.pdf.set_text_color(51, 51, 51)
        self.pdf.set_y(30)
        
        # Table header
        self.pdf.set_font("DejaVu", "B", 10)
        r, g, b = self._hex_to_rgb(self.brand_color)
        self.pdf.set_fill_color(r, g, b)
        self.pdf.set_text_color(255, 255, 255)
        
        headers = [("Pattern", 60), ("Difficulty", 30), ("Pages", 20), ("Yards", 20), ("Suggested", 30)]
        for header, width in headers:
            self.pdf.cell(width, 8, header, border=1, align='C', fill=True)
        self.pdf.ln()
        
        # Table rows
        self.pdf.set_text_color(51, 51, 51)
        for i, pattern in enumerate(patterns):
            self.pdf.set_font("DejaVu", "", 9)
            
            # Alternate row colors
            if i % 2 == 0:
                self.pdf.set_fill_color(245, 245, 245)
            else:
                self.pdf.set_fill_color(255, 255, 255)
            
            self.pdf.cell(60, 7, pattern.get("title", ""), border=1, fill=True)
            self.pdf.cell(30, 7, pattern.get("difficulty", ""), border=1, align='C', fill=True)
            self.pdf.cell(20, 7, str(pattern.get("pages", "")), border=1, align='C', fill=True)
            self.pdf.cell(20, 7, str(pattern.get("yards", "")), border=1, align='C', fill=True)
            self.pdf.cell(30, 7, f"${pattern.get('price', '')}", border=1, align='C', fill=True)
            self.pdf.ln()
        
        # Pricing formula
        self.pdf.set_y(self.pdf.get_y() + 15)
        self.pdf.set_font("DejaVu", "B", 12)
        r, g, b = self._hex_to_rgb(self.brand_color)
        self.pdf.set_text_color(r, g, b)
        self.pdf.cell(0, 8, "[TIP] Pricing Formula:")
        
        self.pdf.set_font("DejaVu", "", 10)
        self.pdf.set_text_color(51, 51, 51)
        formulas = [
            "Base Price = (Pages × $0.50) + (Difficulty Bonus)",
            "Difficulty: Beginner +$0, Intermediate +$1, Advanced +$2",
            "With photo tutorial: Add $1-2",
            "Bundle 3+ patterns: 20% discount",
        ]
        for formula in formulas:
            self.pdf.set_x(25)
            self.pdf.cell(0, 7, f"- {formula}")
            self.pdf.ln(7)
    
    def create_social_media_sheet(self, patterns: List[Dict]) -> None:
        """Create social media promo templates"""
        self.pdf.add_page()
        
        r, g, b = self._hex_to_rgb(self.brand_color)
        self.pdf.set_fill_color(r, g, b)
        self.pdf.rect(0, 0, 210, 20, 'F')
        self.pdf.set_text_color(255, 255, 255)
        self.pdf.set_font("DejaVu", "B", 16)
        self.pdf.set_xy(0, 5)
        self.pdf.cell(210, 10, "SOCIAL MEDIA PROMO", align='C')
        
        self.pdf.set_text_color(51, 51, 51)
        self.pdf.set_y(30)
        
        # Instagram post template
        self.pdf.set_font("DejaVu", "B", 12)
        r, g, b = self._hex_to_rgb(self.brand_color)
        self.pdf.set_text_color(r, g, b)
        self.pdf.cell(0, 8, "[CAM] Instagram Post Template")
        
        # Square template
        self.pdf.set_draw_color(200, 200, 200)
        self.pdf.set_fill_color(250, 250, 250)
        self.pdf.rect(20, 42, 80, 80, 'DF')
        self.pdf.set_font("DejaVu", "I", 9)
        self.pdf.set_text_color(150, 150, 150)
        self.pdf.set_xy(20, 78)
        self.pdf.cell(80, 8, "1080 × 1080px", align='C')
        
        # Caption template
        self.pdf.set_xy(110, 42)
        self.pdf.set_font("DejaVu", "B", 10)
        self.pdf.set_text_color(51, 51, 51)
        self.pdf.cell(0, 7, "Caption:")
        
        self.pdf.set_font("DejaVu", "", 9)
        captions = [
            "[YARN] NEW PATTERN ALERT! [YARN]",
            "",
            "Introducing: [Pattern Name]",
            "[*] [Difficulty] level",
            "📏 Finished size: [Size]",
            "🧵 Uses: [Yarn info]",
            "",
            "Link in bio! 🔗",
            "",
            "#crochet #crochetpattern #handmade",
        ]
        
        y = 52
        for line in captions:
            self.pdf.set_xy(110, y)
            self.pdf.cell(0, 5, line)
            y += 5
        
        # Pinterest template
        self.pdf.set_y(130)
        self.pdf.set_font("DejaVu", "B", 12)
        r, g, b = self._hex_to_rgb(self.brand_color)
        self.pdf.set_text_color(r, g, b)
        self.pdf.cell(0, 8, "[PIN] Pinterest Pin Template")
        
        # Pin template
        self.pdf.set_draw_color(200, 200, 200)
        self.pdf.set_fill_color(250, 250, 250)
        self.pdf.rect(20, 142, 60, 90, 'DF')
        self.pdf.set_font("DejaVu", "I", 9)
        self.pdf.set_text_color(150, 150, 150)
        self.pdf.set_xy(20, 183)
        self.pdf.cell(60, 8, "1000 × 1500px", align='C')
        
        # Hashtag suggestions
        self.pdf.set_xy(90, 142)
        self.pdf.set_font("DejaVu", "B", 10)
        self.pdf.set_text_color(51, 51, 51)
        self.pdf.cell(0, 7, "Hashtags:")
        
        hashtags = [
            "#crochetpattern #crochetlove",
            "#freepattern #crochetdesign",
            "#handmade #yarnlove",
            "#crochetaddict #pattern",
            "#diy #craftpattern",
        ]
        
        y = 152
        for tag in hashtags:
            self.pdf.set_xy(90, y)
            self.pdf.set_font("DejaVu", "", 9)
            self.pdf.cell(0, 5, tag)
            y += 6
    
    def generate_sales_kit(self, patterns: List[Dict], 
                          output_path: str) -> str:
        """Generate complete sales kit PDF"""
        # Generate listing previews
        for pattern in patterns:
            self.create_listing_preview(
                pattern_title=pattern.get("title", "Pattern"),
                description=pattern.get("description", ""),
                difficulty=pattern.get("difficulty", ""),
                finished_size=pattern.get("finished_size", ""),
                yarn_weight=pattern.get("yarn_weight", ""),
                hook_size=pattern.get("hook_size", ""),
            )
        
        # Pricing sheet
        self.create_pricing_sheet(patterns)
        
        # Social media templates
        self.create_social_media_sheet(patterns)
        
        # Terms of use
        self.create_terms_page()
        
        # Save
        self.pdf.output(output_path)
        return output_path


# Demo
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  PDF SALES KIT GENERATOR - DEMO")
    print("=" * 60)
    
    kit = PDFSalesKit(
        shop_name="Cozy Stitches Studio",
        brand_color="#E74C3C",
    )
    
    patterns = [
        {
            "title": "Cozy Scarf",
            "description": "A beginner-friendly scarf perfect for winter!",
            "difficulty": "Beginner",
            "finished_size": "8\" × 60\"",
            "yarn_weight": "Worsted",
            "hook_size": "5.5mm",
            "pages": 3,
            "yards": 400,
            "price": "4.99",
        },
        {
            "title": "Granny Square Blanket",
            "description": "Classic granny square blanket with modern colors.",
            "difficulty": "Intermediate",
            "finished_size": "50\" × 60\"",
            "yarn_weight": "Worsted",
            "hook_size": "5.5mm",
            "pages": 8,
            "yards": 1500,
            "price": "7.99",
        },
        {
            "title": "Amigurumi Bunny",
            "description": "Adorable stuffed bunny for all ages.",
            "difficulty": "Intermediate",
            "finished_size": "10\" tall",
            "yarn_weight": "Worsted",
            "hook_size": "3.5mm",
            "pages": 6,
            "yards": 200,
            "price": "5.99",
        },
    ]
    
    output = "/home/user/demo_sales_kit.pdf"
    result = kit.generate_sales_kit(patterns, output)
    
    print(f"\n[OK] Sales Kit Generated: {result}")
    print(f"   Shop: {kit.shop_name}")
    print(f"   Patterns: {len(patterns)}")
    print(f"   Includes: Listing previews, pricing, social media, terms")
    print(f"   File size: {os.path.getsize(result)} bytes")
    
    print(f"\n  PDF Sales Kit Complete! [$$][*]")
