"""Shared PDF utilities - BULLETPROOF font setup"""
import os
FONT = 'DejaVu'

def setup_unicode_font(pdf):
    """Register fonts - uses regular font for ALL styles if italic/bold missing"""
    font_locations = [
        '/usr/local/lib/python3.13/site-packages/cv2/qt/fonts/',
        '/usr/local/lib/python3.12/site-packages/cv2/qt/fonts/',
        '/usr/local/lib/python3.11/site-packages/cv2/qt/fonts/',
        '/usr/share/fonts/truetype/dejavu/',
        '/usr/share/fonts/',
    ]
    
    regular_font = None
    bold_font = None
    italic_font = None
    bold_italic_font = None
    
    # Find font files
    for font_dir in font_locations:
        if not os.path.exists(font_dir):
            continue
        for f in os.listdir(font_dir):
            fp = os.path.join(font_dir, f)
            fl = f.lower()
            if 'dejavu' in fl and 'sans' in fl and not 'condensed' in fl and not 'extra' in fl:
                if 'boldoblique' in fl or 'bolditalic' in fl:
                    bold_italic_font = fp
                elif 'bold' in fl:
                    bold_font = fp
                elif 'oblique' in fl or 'italic' in fl:
                    italic_font = fp
                elif 'regular' in fl or f == 'DejaVuSans.ttf':
                    regular_font = fp
        
        if regular_font:
            break
    
    # If no DejaVu, find ANY sans-serif TTF
    if not regular_font:
        for font_dir in font_locations:
            if not os.path.exists(font_dir):
                continue
            for f in sorted(os.listdir(font_dir)):
                if f.endswith('.ttf') and 'sans' in f.lower():
                    regular_font = os.path.join(font_dir, f)
                    break
            if regular_font:
                break
    
    # If still nothing, find ANY TTF
    if not regular_font:
        for font_dir in font_locations:
            if not os.path.exists(font_dir):
                continue
            for f in sorted(os.listdir(font_dir)):
                if f.endswith('.ttf'):
                    regular_font = os.path.join(font_dir, f)
                    break
            if regular_font:
                break
    
    if not regular_font:
        print("WARNING: No TTF fonts found!")
        return pdf
    
    # Register regular for ALL styles as fallback
    try:
        pdf.add_font('DejaVu', '', regular_font, uni=True)
    except Exception as e:
        print(f"Font error: {e}")
        return pdf
    
    # Bold - use bold font or fallback to regular
    bold_to_use = bold_font or regular_font
    try:
        pdf.add_font('DejaVu', 'B', bold_to_use, uni=True)
    except:
        pdf.add_font('DejaVu', 'B', regular_font, uni=True)
    
    # Italic - use italic font or fallback to regular
    italic_to_use = italic_font or regular_font
    try:
        pdf.add_font('DejaVu', 'I', italic_to_use, uni=True)
    except:
        pdf.add_font('DejaVu', 'I', regular_font, uni=True)
    
    # Bold Italic - use bold italic or fallback to bold or regular
    bi_to_use = bold_italic_font or bold_font or regular_font
    try:
        pdf.add_font('DejaVu', 'BI', bi_to_use, uni=True)
    except:
        pdf.add_font('DejaVu', 'BI', regular_font, uni=True)
    
    print(f"  Fonts loaded from: {os.path.dirname(regular_font)}")
    return pdf

def get_output_dir():
    for p in ['/tmp', '/home/user', os.path.expanduser('~')]:
        if os.path.exists(p) and os.access(p, os.W_OK):
            return p
    return '.'
