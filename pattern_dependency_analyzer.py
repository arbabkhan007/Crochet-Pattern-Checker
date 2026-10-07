"""Names words that are written. It does not assign a skill grade."""

class PatternDependencyAnalyzer:
    def __init__(self):
        self.dependencies = {
            "stitches": ["sc", "dc", "hdc", "tr"],
            "techniques": ["inc", "dec", "magic ring"],
            "tools": ["hook", "yarn", "scissors"],
        }

    def analyze_dependencies(self, pattern_text: str) -> dict:
        low = pattern_text.lower()
        stitches = [item for item in self.dependencies["stitches"] if item in low]
        techniques = [item for item in self.dependencies["techniques"] if item in low]
        tools = [item for item in self.dependencies["tools"] if item in low]
        return {
            "stitches_required": stitches,
            "techniques_required": techniques,
            "tools_needed": tools,
            "note": "Only written words were named. No skill grade was invented.",
        }

    def get_skill_level(self, dependencies: dict) -> str:
        return "No skill grade was invented."

if __name__ == "__main__":
    result = PatternDependencyAnalyzer().analyze_dependencies("sc dc inc")
    print(result["note"])
