"""Does not claim a file was written."""
from pathlib import Path

class PatternExportHub:
    def __init__(self):
        self.export_formats = ["txt", "pdf", "html", "md", "json"]

    def export_pattern(self, pattern_text: str, format_type: str, filename: str = "pattern") -> dict:
        format_type = format_type.lower()
        if format_type not in self.export_formats:
            return {"error": "Format not supported", "status": "not written"}
        return {
            "status": "not written",
            "format": format_type,
            "filename": None,
            "note": "No file was written. This is not a print-shop file.",
        }

    def batch_export(self, pattern_text: str, formats: list) -> list:
        return [self.export_pattern(pattern_text, item) for item in formats]

if __name__ == "__main__":
    result = PatternExportHub().export_pattern("Row 1: sc", "txt")
    print(result["note"])
