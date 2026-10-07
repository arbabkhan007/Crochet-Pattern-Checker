"""Does not invent a video length."""

class VideoTutorialGenerator:
    def __init__(self):
        self.video_formats = []

    def generate_script(self, pattern_text: str) -> dict:
        lines = [line for line in pattern_text.split("\n") if line.strip()]
        return {
            "intro": None,
            "steps": [{"step": index + 1, "instruction": line} for index, line in enumerate(lines)],
            "outro": None,
            "note": "No video was made. No duration was invented.",
        }

    def create_storyboard(self, script: dict) -> list:
        return [
            {"scene": step["step"], "description": step["instruction"], "duration": None}
            for step in script.get("steps", [])
        ]

if __name__ == "__main__":
    result = VideoTutorialGenerator().generate_script("Row 1: sc in 2nd ch\nRow 2: sc across")
    print(result["note"])
