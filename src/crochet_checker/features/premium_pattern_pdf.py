"""
Premium Pattern PDF Generator - Create beautiful, professional crochet pattern PDFs
"""
from fpdf import FPDF
from typing import Dict, List, Optional
from datetime import datetime
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _pdf_utils import setup_unicode_font, FONT


class PremiumPatternPDF:
    """Generate premium-quality crochet pattern PDFs"""
    
    THEMES = {
        "elegant": {"primary": "#2C3E50", "secondary": "#E74C3C", "accent": "#3498DB", "bg": "#FFFFFF", "text": "#333333"},
        "boho": {"primary": "#8B6914", "secondary": "#D4A574", "accent": "#C17817", "bg": "#FFF8F0", "text": "#4A3728"},
        "modern": {"primary": "#1A1A2E", "secondary": "#16213E", "accent": "#E94560", "bg": "#F5F5F5", "text": "#1A1A2E"},
        "pastel": {"primary": "#FFB7C5", "secondary": "#FFDAB9", "accent": "#98FB98", "bg": "#FFFAF0", "text": "#4A4A4A"},
        "dark": {"primary": "#1A1A2E", "secondary": "#16213E", "accent": "#0F3460", "bg": "#FFFFFF", "text": "#1A1A2E"},
    }
    
    def __init__(self, theme: str = "elegant"):
        self.theme = self.THEMES.get(theme, self.THEMES["elegant"])
        self.pdf = FPDF()
        setup_unicode_font(self.pdf)
    
    def _hex_to_rgb(self, hex_color: str) -> tuple:
        h = hex_color.lstrip('#')
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    
    def _set_colors(self, text_color: str = None, fill_color: str = None):
        if text_color:
            r, g, b = self._hex_to_rgb(text_color)
            self.pdf.set_text_color(r, g, b)
        if fill_color:
            r, g, b = self._hex_to_rgb(fill_color)
            self.pdf.set_fill_color(r, g, b)
    
    def create_cover_page(self, title: str, subtitle: str = "", designer: str = ""):
        self.pdf.add_page()
        r, g, b = self._hex_to_rgb(self.theme["primary"])
        self.pdf.set_fill_color(r, g, b)
        self.pdf.rect(0, 0, 210, 297, 'F')
        
        self._set_colors(text_color="#FFFFFF")
        self.pdf.set_draw_color(255, 255, 255)
        self.pdf.set_line_width(0.5)
        self.pdf.rect(10, 10, 190, 277)
        self.pdf.rect(15, 15, 180, 267)
        
        self.pdf.set_y(60)
        self.pdf.set_font(FONT, "B", 36)
        self.pdf.multi_cell(0, 15, title.upper(), align='C')
        
        self.pdf.set_y(110)
        self.pdf.set_draw_color(255, 255, 255)
        self.pdf.set_line_width(1)
        self.pdf.line(60, self.pdf.get_y(), 150, self.pdf.get_y())
        
        if subtitle:
            self.pdf.set_y(125)
            self.pdf.set_font(FONT, "I", 18)
            self.pdf.multi_cell(0, 10, subtitle, align='C')
        
        if designer:
            self.pdf.set_y(200)
            self.pdf.set_font(FONT, "", 14)
            self.pdf.cell(0, 10, f"Designed by {designer}", align='C')
        
        self.pdf.set_y(220)
        self.pdf.set_font(FONT, "", 12)
        self.pdf.cell(0, 10, datetime.now().strftime("%B %Y"), align='C')
        
        self.pdf.set_y(240)
        self.pdf.set_font(FONT, "", 20)
        self.pdf.cell(0, 10, "~  O  X  T  ~", align='C')
    
    def create_materials_page(self, materials: Dict, gauge: str = ""):
        self.pdf.add_page()
        self._page_header("Materials & Supplies")
        
        self.pdf.set_y(45)
        self._section("Materials")
        self.pdf.set_font(FONT, "", 12)
        self._set_colors(text_color=self.theme["text"])
        
        y_pos = self.pdf.get_y() + 5
        for item, details in materials.items():
            self.pdf.set_xy(25, y_pos)
            self.pdf.set_font(FONT, "B", 11)
            self.pdf.cell(60, 8, f"> {item}")
            self.pdf.set_font(FONT, "", 11)
            self.pdf.cell(0, 8, str(details))
            y_pos += 10
        
        if gauge:
            self.pdf.set_y(y_pos + 15)
            self._section("Gauge")
            self.pdf.set_font(FONT, "", 12)
            self.pdf.set_x(25)
            self.pdf.multi_cell(160, 8, gauge)
    
    def create_instructions_page(self, instructions: List[str], section_title: str = "Instructions"):
        self.pdf.add_page()
        self._page_header(section_title)
        self.pdf.set_y(45)
        self._set_colors(text_color=self.theme["text"])
        
        for instruction in instructions:
            if instruction.lower().startswith(("row", "rnd", "round")):
                self.pdf.set_font(FONT, "B", 12)
                r, g, b = self._hex_to_rgb(self.theme["secondary"])
                self.pdf.set_text_color(r, g, b)
                self.pdf.set_x(20)
                self.pdf.multi_cell(170, 8, instruction)
                self._set_colors(text_color=self.theme["text"])
            else:
                self.pdf.set_font(FONT, "", 11)
                self.pdf.set_x(25)
                self.pdf.multi_cell(160, 7, f"  {instruction}")
            self.pdf.ln(2)
    
    def create_notes_page(self, notes: List[str], tips: List[str] = None):
        self.pdf.add_page()
        self._page_header("Notes & Tips")
        self.pdf.set_y(45)
        self._section("Designer Notes")
        self.pdf.set_font(FONT, "I", 11)
        self._set_colors(text_color=self.theme["text"])
        
        for note in notes:
            self.pdf.set_x(30)
            self.pdf.multi_cell(150, 7, f"> {note}")
            self.pdf.ln(2)
        
        if tips:
            self.pdf.set_y(self.pdf.get_y() + 10)
            self._section("Helpful Tips")
            for tip in tips:
                self.pdf.set_x(35)
                self.pdf.set_font(FONT, "", 10)
                self.pdf.cell(0, 7, f"[OK] {tip}")
                self.pdf.ln(7)
    
    def create_back_page(self, designer: str = "", website: str = "", copyright_text: str = ""):
        self.pdf.add_page()
        r, g, b = self._hex_to_rgb(self.theme["primary"])
        self.pdf.set_fill_color(r, g, b)
        self.pdf.rect(0, 0, 210, 297, 'F')
        
        self._set_colors(text_color="#FFFFFF")
        self.pdf.set_draw_color(255, 255, 255)
        self.pdf.set_line_width(0.5)
        self.pdf.rect(10, 10, 190, 277)
        
        self.pdf.set_y(100)
        self.pdf.set_font(FONT, "B", 24)
        self.pdf.cell(0, 15, "Thank You!", align='C')
        
        self.pdf.set_y(125)
        self.pdf.set_font(FONT, "I", 14)
        self.pdf.multi_cell(0, 10, "Happy Crocheting!", align='C')
        
        if designer:
            self.pdf.set_y(170)
            self.pdf.set_font(FONT, "", 14)
            self.pdf.cell(0, 10, f"Designed by {designer}", align='C')
        
        if website:
            self.pdf.set_y(190)
            self.pdf.set_font(FONT, "", 12)
            self.pdf.cell(0, 10, website, align='C')
        
        if copyright_text:
            self.pdf.set_y(250)
            self.pdf.set_font(FONT, "", 10)
            self.pdf.cell(0, 8, copyright_text, align='C')
    
    def _page_header(self, title: str):
        r, g, b = self._hex_to_rgb(self.theme["primary"])
        self.pdf.set_fill_color(r, g, b)
        self.pdf.rect(0, 0, 210, 25, 'F')
        self._set_colors(text_color="#FFFFFF")
        self.pdf.set_font(FONT, "B", 18)
        self.pdf.set_xy(20, 8)
        self.pdf.cell(170, 10, title, align='C')
        r2, g2, b2 = self._hex_to_rgb(self.theme["secondary"])
        self.pdf.set_draw_color(r2, g2, b2)
        self.pdf.set_line_width(1)
        self.pdf.line(20, 26, 190, 26)
        self._set_colors(text_color=self.theme["text"])
    
    def _section(self, title: str):
        self.pdf.set_font(FONT, "B", 14)
        r, g, b = self._hex_to_rgb(self.theme["secondary"])
        self.pdf.set_text_color(r, g, b)
        self.pdf.set_x(20)
        self.pdf.cell(170, 10, title)
        self.pdf.set_draw_color(r, g, b)
        self.pdf.set_line_width(0.5)
        y = self.pdf.get_y() + 2
        self.pdf.line(20, y, 100, y)
        self.pdf.ln(5)
        self._set_colors(text_color=self.theme["text"])
    
    def generate_full_pattern_pdf(self, pattern_data: Dict, output_path: str) -> str:
        self.create_cover_page(
            title=pattern_data.get("title", "Crochet Pattern"),
            subtitle=pattern_data.get("subtitle", ""),
            designer=pattern_data.get("designer", ""),
        )
        if pattern_data.get("materials"):
            self.create_materials_page(materials=pattern_data["materials"], gauge=pattern_data.get("gauge", ""))
        if pattern_data.get("instructions"):
            self.create_instructions_page(instructions=pattern_data["instructions"])
        if pattern_data.get("notes") or pattern_data.get("tips"):
            self.create_notes_page(notes=pattern_data.get("notes", []), tips=pattern_data.get("tips", []))
        self.create_back_page(
            designer=pattern_data.get("designer", ""),
            website=pattern_data.get("website", ""),
            copyright_text=pattern_data.get("copyright", ""),
        )
        self.pdf.output(output_path)
        return output_path


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  PREMIUM PATTERN PDF GENERATOR - DEMO")
    print("=" * 60)
    
    pdf_gen = PremiumPatternPDF(theme="elegant")
    
    pattern = {
        "title": "Cozy Winter Scarf",
        "subtitle": "A Beginner-Friendly Pattern",
        "designer": "Your Name",
        "materials": {"Yarn": "400 yards worsted weight", "Hook": "5.5mm (I-9)", "Extras": "Scissors, tapestry needle"},
        "gauge": "14 sc = 4 inches, 16 rows = 4 inches",
        "instructions": [
            "Ch 32.",
            "Row 1: Sc in 2nd ch from hook and each ch across. (31 sc) Turn.",
            "Row 2-240: Ch 1, sc in each st across. (31 sc) Turn.",
            "Fasten off. Weave in ends.",
        ],
        "notes": ["This pattern uses basic stitches only.", "Adjust hook size to match gauge."],
        "tips": ["Use stitch markers every 10 stitches", "Count your stitches every few rows"],
        "website": "www.yourwebsite.com",
        "copyright": f"(c) {datetime.now().year} Your Name. All rights reserved.",
    }
    
    output = "/home/user/demo_pattern.pdf"
    result = pdf_gen.generate_full_pattern_pdf(pattern, output)
    
    print(f"\n  PDF Generated: {result}")
    print(f"  File size: {os.path.getsize(result)} bytes")
    print(f"  Pages: 5 (Cover + Materials + Instructions + Notes + Back)")
    
    print(f"\n  Themes available: {', '.join(PremiumPatternPDF.THEMES.keys())}")
    print(f"\n  Premium Pattern PDF Complete!")
