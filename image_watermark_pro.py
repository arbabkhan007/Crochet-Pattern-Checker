"""Does not claim an image was watermarked."""
from pathlib import Path

class ImageWatermarkPro:
    def __init__(self):
        self.watermark_styles = {}

    def apply_watermark(self, image_path: str, watermark_text: str, style: str = "text") -> dict:
        return {
            "status": "not written",
            "watermark_text": None,
            "style": None,
            "output": None,
            "note": "No watermark was written. The image was not changed.",
        }

    def batch_watermark(self, image_paths: list, watermark_text: str) -> dict:
        return {
            "status": "not written",
            "total_images": 0,
            "note": "No images were watermarked.",
        }

if __name__ == "__main__":
    result = ImageWatermarkPro().apply_watermark("pattern.jpg", "name")
    print(result["note"])
