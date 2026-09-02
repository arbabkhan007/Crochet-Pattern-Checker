from pathlib import Path

def extract_text_from_pdf(pdf_path: str) -> str:
    pdf_file = Path(pdf_path)
    if not pdf_file.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    try:
        import PyPDF2
        with open(pdf_file, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            if reader.is_encrypted:
                raise ValueError("PDF is encrypted")
            text_parts = []
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
            return '\n\n'.join(text_parts)
    except ImportError:
        raise ImportError("Install PyPDF2: pip install PyPDF2")

def is_pdf_file(file_path: str) -> bool:
    return Path(file_path).suffix.lower() == '.pdf'

def read_pattern_file(file_path: str) -> str:
    if is_pdf_file(file_path):
        return extract_text_from_pdf(file_path)
    return Path(file_path).read_text()
