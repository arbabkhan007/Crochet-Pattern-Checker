"""Shared PDF utilities - Unicode font setup"""
import os

def setup_unicode_font(pdf):
    """Add Unicode fonts to an FPDF instance"""
    font_dir = '/usr/local/lib/python3.13/site-packages/cv2/qt/fonts/'
    regular = os.path.join(font_dir, 'DejaVuSans.ttf')
    bold = os.path.join(font_dir, 'DejaVuSans-Bold.ttf')
    oblique = os.path.join(font_dir, 'DejaVuSans-Oblique.ttf')
    
    if os.path.exists(regular):
        pdf.add_font('DejaVu', '', regular, uni=True)
    if os.path.exists(bold):
        pdf.add_font('DejaVu', 'B', bold, uni=True)
    if os.path.exists(oblique):
        pdf.add_font('DejaVu', 'I', oblique, uni=True)
    
    # Also add bold italic if available
    bold_oblique = os.path.join(font_dir, 'DejaVuSans-BoldOblique.ttf')
    if os.path.exists(bold_oblique):
        pdf.add_font('DejaVu', 'BI', bold_oblique, uni=True)
    
    return pdf

FONT = 'DejaVu'
