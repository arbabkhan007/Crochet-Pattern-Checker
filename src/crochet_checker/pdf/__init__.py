"""PDF generation for crochet patterns."""
from .generator import PDFConfig, PDFGenerator, generate_pdf_html, generate_pdf

# Optional image support (best-effort)
try:
    from .image_support import generate_pattern_images
except Exception:
    def generate_pattern_images(*_args, **_kwargs):  # type: ignore
        return []

__all__ = [
    "PDFConfig",
    "PDFGenerator",
    "generate_pdf_html",
    "generate_pdf",
    "generate_pattern_images",
]
