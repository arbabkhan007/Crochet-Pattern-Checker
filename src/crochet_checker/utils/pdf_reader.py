"""PDF text extraction utility for reading crochet patterns from PDF files."""

from pathlib import Path


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text content from a PDF file."""
    pdf_file = Path(pdf_path)
    
    if not pdf_file.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    if not pdf_file.suffix.lower() == '.pdf':
        raise ValueError(f"File is not a PDF: {pdf_path}")
    
    try:
        import PyPDF2
        
        with open(pdf_file, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            
            if reader.is_encrypted:
                raise ValueError("PDF is encrypted and cannot be read")
            
            text_parts = []
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
            
            full_text = '\n\n'.join(text_parts)
            
            if not full_text.strip():
                raise ValueError("No text could be extracted from PDF")
            
            return full_text
            
    except ImportError:
        raise ImportError("PyPDF2 is required. Install with: pip install PyPDF2")
    except Exception as e:
        raise ValueError(f"Error reading PDF: {str(e)}")


def is_pdf_file(file_path: str) -> bool:
    """Check if a file is a PDF."""
    return Path(file_path).suffix.lower() == '.pdf'


def read_pattern_file(file_path: str) -> str:
    """Read a pattern file, automatically detecting if it's PDF or text."""
    if is_pdf_file(file_path):
        return extract_text_from_pdf(file_path)
    else:
        return Path(file_path).read_text()
