"""
Pattern Dependency Analyzer - Analyze dependencies
"""

class PatternDependencyAnalyzer:
    def __init__(self):
        self.dependencies = {
            "stitches": ["sc", "dc", "hdc", "tr"],
            "techniques": ["inc", "dec", "magic ring"],
            "tools": ["hook", "yarn", "scissors"],
        }
    
    def analyze_dependencies(self, pattern_text: str) -> dict:
        found_stitches = []
        found_techniques = []
        pattern_lower = pattern_text.lower()
        
        for stitch in self.dependencies["stitches"]:
            if stitch.lower() in pattern_lower:
                found_stitches.append(stitch)
        
        for technique in self.dependencies["techniques"]:
            if technique.lower() in pattern_lower:
                found_techniques.append(technique)
        
        return {
            "stitches_required": found_stitches,
            "techniques_required": found_techniques,
            "tools_needed": self.dependencies["tools"],
            "total_dependencies": len(found_stitches) + len(found_techniques) + len(self.dependencies["tools"]),
        }
    
    def get_skill_level(self, dependencies: dict) -> str:
        total = dependencies["total_dependencies"]
        if total <= 5:
            return "Beginner"
        elif total <= 10:
            return "Intermediate"
        else:
            return "Advanced"

if __name__ == "__main__":
    print("🔗 Pattern Dependency Analyzer")
    print("=" * 60)
    analyzer = PatternDependencyAnalyzer()
    deps = analyzer.analyze_dependencies("sc dc inc")
    skill = analyzer.get_skill_level(deps)
    print(f"\nSkill Level: {skill}")
    print(f"Total Dependencies: {deps['total_dependencies']}")
    print("\n✨ Pattern Dependency Analyzer complete!")
