"""Does not read an image or invent its colors."""

class ImagePatternGenerator:
    def __init__(self):
        self.color_map = {}

    def analyze_image_colors(self, image_path: str) -> dict:
        return {
            "dominant_colors": [],
            "color_count": None,
            "note": "The image was not read. No colors were invented.",
        }

    def generate_pattern_grid(self, colors: list, grid_size: tuple) -> list:
        return []

if __name__ == "__main__":
    result = ImagePatternGenerator().analyze_image_colors("test.jpg")
    print(result["note"])
