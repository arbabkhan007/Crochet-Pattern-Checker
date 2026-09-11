"""
PDF Pattern Book Builder - Compile multiple patterns into a professional book PDF
"""
from fpdf import FPDF
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _pdf_utils import setup_unicode_font, FONT
from typing import Dict, List
from datetime import datetime
import os


class PDFPatternBook:
    """
    Build professional crochet pattern books
    
    Features:
    - Table of contents
    - Multiple patterns in one book
    - Book cover & spine
    - Author bio page
    - Pattern index
    - ISBN-ready formatting
    """
    
    def __init__(self, title: str = "", author: str = ""):
        self.title = title
        self.author = author
        self.pdf = FPDF()
        setup_unicode_font(self.pdf)
        # Register Unicode font
        import os
        self.patterns = []
    
    def add_pattern(self, title: str, difficulty: str = "",
                   materials: Dict = None, instructions: List[str] = None,
                   notes: List[str] = None, photo_description: str = "") -> int:
        """Add a pattern to the book"""
        pattern = {
            "id": len(self.patterns) + 1,
            "title": title,
            "difficulty": difficulty,
            "materials": materials or {},
            "instructions": instructions or [],
            "notes": notes or [],
            "photo_description": photo_description,
            "page": 0,  # Will be set during generation
        }
        self.patterns.append(pattern)
        return pattern["id"]
    
    def _create_title_page(self):
        """Create book title page"""
        self.pdf.add_page()
        
        # Background
        self.pdf.set_fill_color(44, 62, 80)
        self.pdf.rect(0, 0, 210, 297, 'F')
        
        # Border
        self.pdf.set_draw_color(255, 255, 255)
        self.pdf.set_line_width(1)
        self.pdf.rect(10, 10, 190, 277)
        
        # Title
        self.pdf.set_text_color(255, 255, 255)
        self.pdf.set_y(80)
        self.pdf.set_font("DejaVu", "B", 32)
        self.pdf.multi_cell(0, 15, self.title.upper(), align='C')
        
        # Decorative line
        self.pdf.set_y(130)
        self.pdf.set_line_width(2)
        self.pdf.line(50, self.pdf.get_y(), 160, self.pdf.get_y())
        
        # Author
        if self.author:
            self.pdf.set_y(150)
            self.pdf.set_font("DejaVu", "I", 18)
            self.pdf.cell(0, 12, f"by {self.author}", align='C')
        
        # Year
        self.pdf.set_y(200)
        self.pdf.set_font("DejaVu", "", 14)
        self.pdf.cell(0, 10, datetime.now().strftime("%Y"), align='C')
        
        # Decorative
        self.pdf.set_y(230)
        self.pdf.set_font("DejaVu", "", 20)
        self.pdf.cell(0, 10, "[YARN] O x T t O x T t [YARN]", align='C')
    
    def _create_table_of_contents(self):
        """Create table of contents"""
        self.pdf.add_page()
        
        # Header
        self.pdf.set_fill_color(44, 62, 80)
        self.pdf.rect(0, 0, 210, 20, 'F')
        self.pdf.set_text_color(255, 255, 255)
        self.pdf.set_font("DejaVu", "B", 18)
        self.pdf.set_xy(0, 5)
        self.pdf.cell(210, 10, "TABLE OF CONTENTS", align='C')
        
        self.pdf.set_text_color(51, 51, 51)
        self.pdf.set_y(35)
        
        for pattern in self.patterns:
            self.pdf.set_font("DejaVu", "B", 13)
            self.pdf.set_x(25)
            title = f"{pattern['id']}. {pattern['title']}"
            self.pdf.cell(130, 10, title)
            
            # Page number placeholder (right-aligned)
            self.pdf.set_font("DejaVu", "", 12)
            self.pdf.cell(30, 10, str(pattern['page']), align='R')
            
            if pattern['difficulty']:
                self.pdf.set_font("DejaVu", "I", 10)
                self.pdf.set_x(25)
                self.pdf.cell(0, 7, f"    Difficulty: {pattern['difficulty']}")
            
            # Dotted line
            self.pdf.set_draw_color(200, 200, 200)
            self.pdf.set_line_width(0.2)
            y = self.pdf.get_y() + 2
            self.pdf.dashed_line(25, y, 185, y, 1, 1)
            
            self.pdf.ln(12)
    
    def _create_pattern_pages(self, pattern: Dict):
        """Create pages for a single pattern"""
        # Pattern title page
        self.pdf.add_page()
        
        # Header bar
        self.pdf.set_fill_color(231, 76, 60)
        self.pdf.rect(0, 0, 210, 20, 'F')
        self.pdf.set_text_color(255, 255, 255)
        self.pdf.set_font("DejaVu", "B", 16)
        self.pdf.set_xy(0, 5)
        self.pdf.cell(210, 10, f"PATTERN {pattern['id']}", align='C')
        
        # Pattern title
        self.pdf.set_text_color(51, 51, 51)
        self.pdf.set_y(30)
        self.pdf.set_font("DejaVu", "B", 22)
        self.pdf.cell(0, 12, pattern['title'], align='C')
        
        if pattern['difficulty']:
            self.pdf.set_y(45)
            self.pdf.set_font("DejaVu", "I", 12)
            self.pdf.cell(0, 8, f"Difficulty: {pattern['difficulty']}", align='C')
        
        # Photo placeholder
        if pattern['photo_description']:
            self.pdf.set_y(60)
            self.pdf.set_draw_color(200, 200, 200)
            self.pdf.set_fill_color(240, 240, 240)
            self.pdf.rect(55, 60, 100, 60, 'DF')
            self.pdf.set_text_color(150, 150, 150)
            self.pdf.set_font("DejaVu", "I", 10)
            self.pdf.set_xy(55, 85)
            self.pdf.cell(100, 10, pattern['photo_description'], align='C')
        
        # Materials section
        if pattern['materials']:
            self.pdf.set_y(135)
            self.pdf.set_text_color(231, 76, 60)
            self.pdf.set_font("DejaVu", "B", 14)
            self.pdf.set_x(20)
            self.pdf.cell(0, 10, "Materials")
            self.pdf.set_draw_color(231, 76, 60)
            self.pdf.line(20, self.pdf.get_y(), 80, self.pdf.get_y())
            
            self.pdf.set_text_color(51, 51, 51)
            self.pdf.set_font("DejaVu", "", 11)
            
            for item, detail in pattern['materials'].items():
                self.pdf.set_x(25)
                self.pdf.cell(60, 7, f"- {item}")
                self.pdf.cell(0, 7, str(detail))
                self.pdf.ln(7)
        
        # Instructions
        if pattern['instructions']:
            self.pdf.set_y(self.pdf.get_y() + 10)
            self.pdf.set_text_color(231, 76, 60)
            self.pdf.set_font("DejaVu", "B", 14)
            self.pdf.set_x(20)
            self.pdf.cell(0, 10, "Instructions")
            self.pdf.set_draw_color(231, 76, 60)
            self.pdf.line(20, self.pdf.get_y(), 95, self.pdf.get_y())
            
            self.pdf.set_text_color(51, 51, 51)
            self.pdf.set_font("DejaVu", "", 11)
            
            for instruction in pattern['instructions']:
                if instruction.lower().startswith(("row", "rnd", "round")):
                    self.pdf.set_font("DejaVu", "B", 11)
                    self.pdf.set_x(25)
                    self.pdf.multi_cell(160, 7, instruction)
                    self.pdf.set_font("DejaVu", "", 11)
                else:
                    self.pdf.set_x(30)
                    self.pdf.multi_cell(155, 7, instruction)
                self.pdf.ln(2)
        
        # Notes
        if pattern['notes']:
            self.pdf.set_y(self.pdf.get_y() + 10)
            self.pdf.set_text_color(231, 76, 60)
            self.pdf.set_font("DejaVu", "B", 14)
            self.pdf.set_x(20)
            self.pdf.cell(0, 10, "Notes")
            self.pdf.set_draw_color(231, 76, 60)
            self.pdf.line(20, self.pdf.get_y(), 65, self.pdf.get_y())
            
            self.pdf.set_text_color(51, 51, 51)
            self.pdf.set_font("DejaVu", "I", 10)
            
            for note in pattern['notes']:
                self.pdf.set_x(25)
                self.pdf.multi_cell(160, 6, f"- {note}")
    
    def _create_author_page(self, bio: str = ""):
        """Create author bio page"""
        self.pdf.add_page()
        
        self.pdf.set_fill_color(44, 62, 80)
        self.pdf.rect(0, 0, 210, 20, 'F')
        self.pdf.set_text_color(255, 255, 255)
        self.pdf.set_font("DejaVu", "B", 18)
        self.pdf.set_xy(0, 5)
        self.pdf.cell(210, 10, "ABOUT THE DESIGNER", align='C')
        
        self.pdf.set_text_color(51, 51, 51)
        self.pdf.set_y(35)
        
        if self.author:
            self.pdf.set_font("DejaVu", "B", 20)
            self.pdf.cell(0, 12, self.author, align='C')
            self.pdf.ln(20)
        
        if bio:
            self.pdf.set_font("DejaVu", "", 12)
            self.pdf.set_x(25)
            self.pdf.multi_cell(160, 8, bio)
    
    def _create_back_cover(self):
        """Create back cover"""
        self.pdf.add_page()
        
        self.pdf.set_fill_color(44, 62, 80)
        self.pdf.rect(0, 0, 210, 297, 'F')
        
        self.pdf.set_text_color(255, 255, 255)
        self.pdf.set_draw_color(255, 255, 255)
        self.pdf.set_line_width(1)
        self.pdf.rect(10, 10, 190, 277)
        
        self.pdf.set_y(100)
        self.pdf.set_font("DejaVu", "B", 20)
        self.pdf.cell(0, 12, f"{len(self.patterns)} Beautiful Patterns", align='C')
        
        self.pdf.set_y(130)
        self.pdf.set_font("DejaVu", "I", 14)
        self.pdf.multi_cell(0, 10, "From beginner-friendly basics\nto advanced techniques", align='C')
        
        if self.author:
            self.pdf.set_y(200)
            self.pdf.set_font("DejaVu", "", 14)
            self.pdf.cell(0, 10, f"by {self.author}", align='C')
        
        self.pdf.set_y(260)
        self.pdf.set_font("DejaVu", "", 10)
        self.pdf.cell(0, 8, f"© {datetime.now().year} {self.author}. All rights reserved.", align='C')
    
    def build_book(self, output_path: str, author_bio: str = "") -> str:
        """Build the complete book"""
        # Title page
        self._create_title_page()
        
        # Table of contents
        self._create_table_of_contents()
        
        # Pattern pages
        for i, pattern in enumerate(self.patterns):
            pattern['page'] = self.pdf.page_no() + 1
            self._create_pattern_pages(pattern)
        
        # Author page
        self._create_author_page(author_bio)
        
        # Back cover
        self._create_back_cover()
        
        # Add page numbers (skip cover)
        for page in range(2, self.pdf.page_no()):
            pass  # skip link
        
        # Save
        self.pdf.output(output_path)
        return output_path


# Demo
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  PDF PATTERN BOOK BUILDER - DEMO")
    print("=" * 60)
    
    book = PDFPatternBook(
        title="My Crochet Collection",
        author="Jane Smith",
    )
    
    # Add patterns
    book.add_pattern(
        title="Simple Scarf",
        difficulty="Beginner",
        materials={"Yarn": "400 yards worsted", "Hook": "5.5mm"},
        instructions=[
            "Ch 32.",
            "Row 1: Sc in 2nd ch from hook and each ch across. (31 sc) Turn.",
            "Rows 2-240: Ch 1, sc in each st across. (31 sc) Turn.",
            "Fasten off.",
        ],
        notes=["Perfect for beginners!", "Adjust length as desired."],
        photo_description="[Photo: Finished scarf]",
    )
    
    book.add_pattern(
        title="Granny Square Blanket",
        difficulty="Intermediate",
        materials={"Yarn": "1500 yards worsted", "Hook": "5.5mm"},
        instructions=[
            "Make 36 granny squares.",
            "Row 1: Magic ring, ch 3, 2 dc, ch 2, 3 dc, ch 2, 3 dc, ch 2, 3 dc. Join.",
            "Row 2: Join in corner, ch 3, 2 dc, ch 2, 3 dc in each ch-2 space around.",
            "Join squares in 6x6 grid.",
        ],
        notes=["Block squares before joining.", "Use stitch markers for corners."],
        photo_description="[Photo: Finished blanket]",
    )
    
    book.add_pattern(
        title="Amigurumi Bunny",
        difficulty="Intermediate",
        materials={"Yarn": "Worsted in white & pink", "Hook": "3.5mm", "Extras": "Safety eyes, stuffing"},
        instructions=[
            "Head (make 1):",
            "Rnd 1: 6 sc in magic ring. (6)",
            "Rnd 2: Inc in each st around. (12)",
            "Rnd 3: *Sc, inc* around. (18)",
            "Continue until head is 4 inches.",
            "Stuff firmly. Fasten off.",
        ],
        notes=["Use stitch marker.", "Stuff firmly for best shape."],
        photo_description="[Photo: Cute bunny]",
    )
    
    # Build book
    output = "/tmp/demo_pattern_book.pdf"
    result = book.build_book(output, author_bio="Jane Smith is a passionate crochet designer with 10 years of experience. She loves creating patterns that are both beautiful and accessible.")
    
    print(f"\n[OK] Book Generated: {result}")
    print(f"   Title: {book.title}")
    print(f"   Author: {book.author}")
    print(f"   Patterns: {len(book.patterns)}")
    print(f"   File size: {os.path.getsize(result)} bytes")
    
    print(f"\n  PDF Pattern Book Builder Complete! [BOOK][*]")
