"""Does not claim a PDF was protected."""
from pathlib import Path

class PDFSecurityManager:
    def __init__(self):
        self.security_levels = {}

    def add_watermark(self, pdf_path: str, watermark_text: str) -> dict:
        return {
            "status": "not written",
            "watermark": None,
            "output": None,
            "note": "No watermark was written. The PDF was not changed.",
        }

    def add_password(self, pdf_path: str, password: str) -> dict:
        return {
            "status": "not written",
            "password_protected": False,
            "note": "No password was added. The PDF was not changed.",
        }

if __name__ == "__main__":
    result = PDFSecurityManager().add_watermark("pattern.pdf", "name")
    print(result["note"])
