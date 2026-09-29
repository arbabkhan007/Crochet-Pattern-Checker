"""PDF generation package for crochet patterns."""

from .generator import TEMPLATES, PDFConfig, PDFGenerator, generate_pdf_html


def generate_pdf(pattern, output_path: str, format: str = "modern") -> str:
    """
    Backward-compatible PDF generation entry point.

    The current generator writes PDF-ready HTML or a PDF depending on the
    configured backend. The output path is returned for legacy callers.
    """
    template = format if format in TEMPLATES else "minimal"
    PDFGenerator(PDFConfig(template=template)).save(output_path, pattern)
    return output_path


__all__ = [
    "TEMPLATES",
    "PDFConfig",
    "PDFGenerator",
    "generate_pdf",
    "generate_pdf_html",
]
