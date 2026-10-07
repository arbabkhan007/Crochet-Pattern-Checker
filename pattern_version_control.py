"""Does not invent a difference between versions."""
from datetime import datetime

class PatternVersionControl:
    def __init__(self):
        self.versions = []

    def create_version(self, pattern_text: str, version_name: str, change_notes: str = "") -> dict:
        version = {
            "version_name": version_name,
            "timestamp": datetime.now().isoformat(),
            "line_count": len(pattern_text.split("\n")),
            "change_notes": change_notes,
        }
        self.versions.append(version)
        return version

    def get_version_history(self) -> list:
        return self.versions

    def compare_versions(self, version1: str, version2: str) -> dict:
        return {
            "line_difference": None,
            "note": "The two versions were not compared. No count was invented.",
        }

if __name__ == "__main__":
    result = PatternVersionControl().compare_versions("v1.0", "v1.1")
    print(result["note"])
