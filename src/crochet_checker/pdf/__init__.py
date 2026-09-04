"""PDF generation for crochet patterns."""

# Try to import generator
try:
    from .generator import generate_pdf
    _PDF_OK = True
except Exception as e:
    print(f"Warning: PDF generator not available: {e}")
    _PDF_OK = False
    def generate_pdf(*args, **kwargs):
        raise ImportError("PDF generation not available")

# Try to import image support
try:
    from .image_support import generate_pattern_images
    _IMAGES_OK = True
except Exception as e:
    print(f"Warning: Image support not available: {e}")
    _IMAGES_OK = True  # Not critical
    def generate_pattern_images(*args, **kwargs):
        return []

__all__ = ["generate_pdf", "generate_pattern_images"]
