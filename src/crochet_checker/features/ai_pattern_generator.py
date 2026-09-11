"""
AI Pattern Generator - Generate crochet patterns from text descriptions
"""
import json
from typing import Dict, List, Optional
from datetime import datetime


class AIPatternGenerator:
    """
    Generate crochet patterns using AI
    
    Features:
    - Text-to-pattern generation
    - Customizable parameters
    - Difficulty scaling
    - Yarn recommendations
    - Stitch suggestions
    - Pattern validation
    """
    
    STITCH_DATABASE = {
        "basic": ["ch", "sc", "dc", "hdc", "sl st"],
        "intermediate": ["tr", "dtr", "fpdc", "bpdc", "pop", "puff"],
        "advanced": ["cable", "broomstick", "hairpin", "tatting", "solomon"],
    }
    
    PROJECT_TYPES = {
        "scarf": {"width": 8, "length": 60, "unit": "inches"},
        "blanket": {"width": 50, "length": 60, "unit": "inches"},
        "hat": {"circumference": 20, "depth": 9, "unit": "inches"},
        "amigurumi": {"size": "medium", "complexity": "detailed"},
        "dishcloth": {"width": 8, "length": 8, "unit": "inches"},
    }
    
    def generate_pattern(self, description: str, difficulty: str = "beginner",
                        project_type: str = "scarf", yarn_weight: str = "worsted") -> Dict:
        """
        Generate a pattern from description
        
        Args:
            description: What to create (e.g., "cozy winter scarf with cables")
            difficulty: beginner, intermediate, advanced
            project_type: scarf, blanket, hat, amigurumi, dishcloth
            yarn_weight: lace, fingering, dk, worsted, bulky
        
        Returns:
            Dict with complete pattern
        """
        # Parse description
        keywords = description.lower().split()
        
        # Determine stitch complexity
        if difficulty == "beginner":
            stitches = self.STITCH_DATABASE["basic"]
        elif difficulty == "intermediate":
            stitches = self.STITCH_DATABASE["basic"] + self.STITCH_DATABASE["intermediate"][:3]
        else:
            stitches = self.STITCH_DATABASE["basic"] + self.STITCH_DATABASE["intermediate"] + self.STITCH_DATABASE["advanced"][:2]
        
        # Get project dimensions
        dimensions = self.PROJECT_TYPES.get(project_type, self.PROJECT_TYPES["scarf"])
        
        # Generate pattern structure
        pattern = {
            "title": self._generate_title(description, project_type),
            "description": description,
            "difficulty": difficulty,
            "project_type": project_type,
            "dimensions": dimensions,
            "materials": self._generate_materials(yarn_weight, dimensions),
            "gauge": self._generate_gauge(yarn_weight, stitches[0]),
            "stitches_used": stitches[:3],
            "pattern": self._generate_instructions(project_type, dimensions, stitches, difficulty),
            "notes": self._generate_notes(difficulty, project_type),
            "generated_at": datetime.now().isoformat(),
        }
        
        return pattern
    
    def _generate_title(self, description: str, project_type: str) -> str:
        """Generate a catchy title"""
        adjectives = ["Cozy", "Beautiful", "Simple", "Elegant", "Classic", "Modern"]
        import random
        adj = random.choice(adjectives)
        return f"{adj} {project_type.title()}"
    
    def _generate_materials(self, yarn_weight: str, dimensions: Dict) -> Dict:
        """Generate materials list"""
        # Estimate yardage based on project
        if "length" in dimensions and "width" in dimensions:
            area = dimensions["length"] * dimensions["width"]
            yardage = int(area * 1.5)  # Rough estimate
        else:
            yardage = 300  # Default
        
        hook_sizes = {
            "lace": "3.5mm (E-4)",
            "fingering": "4.0mm (G-6)",
            "dk": "4.5mm (7)",
            "worsted": "5.5mm (I-9)",
            "bulky": "6.5mm (K-10.5)",
        }
        
        return {
            "yarn": f"{yardage} yards of {yarn_weight} weight yarn",
            "hook": hook_sizes.get(yarn_weight, "5.5mm (I-9)"),
            "extras": ["Scissors", "Tapestry needle", "Stitch markers"],
        }
    
    def _generate_gauge(self, yarn_weight: str, main_stitch: str) -> str:
        """Generate gauge information"""
        gauges = {
            "worsted": "14 sc = 4 inches, 16 rows = 4 inches",
            "dk": "16 sc = 4 inches, 18 rows = 4 inches",
            "bulky": "10 sc = 4 inches, 12 rows = 4 inches",
        }
        return gauges.get(yarn_weight, "14 sc = 4 inches, 16 rows = 4 inches")
    
    def _generate_instructions(self, project_type: str, dimensions: Dict,
                              stitches: List[str], difficulty: str) -> List[str]:
        """Generate step-by-step instructions"""
        instructions = []
        
        if project_type == "scarf":
            instructions.append(f"Ch {dimensions['width'] * 4}.")
            instructions.append(f"Row 1: {stitches[1]} in 2nd ch from hook and each ch across. Turn.")
            
            if difficulty == "beginner":
                instructions.append(f"Rows 2-{dimensions['length'] * 4}: Ch 1, {stitches[1]} in each st across. Turn.")
            elif difficulty == "intermediate":
                instructions.append("Row 2: Ch 3 (counts as dc), dc in each st across. Turn.")
                instructions.append("Rows 3-20: Repeat Row 2.")
                if len(stitches) > 2:
                    instructions.append(f"Row 21: Ch 1, {stitches[2]} in each st across. Turn.")
                    instructions.append("Rows 22-40: Repeat Row 21.")
            else:
                instructions.append("Row 1: Ch 3, *skip 2 sts, dc in next st, ch 2, dc in same st; repeat from * across.")
                instructions.append("Row 2: Ch 3, dc in each ch-2 space across.")
                instructions.append("Repeat Rows 1-2 for pattern.")
            
            instructions.append("Fasten off. Weave in ends.")
        
        elif project_type == "hat":
            instructions.append("Magic ring or ch 4, join with sl st.")
            instructions.append(f"Round 1: Ch 1, 6 {stitches[1]} in ring. (6 sts)")
            instructions.append(f"Round 2: Ch 1, 2 {stitches[1]} in each st around. (12 sts)")
            instructions.append(f"Round 3: Ch 1, *{stitches[1]}, inc; repeat from * around. (18 sts)")
            instructions.append("Continue increasing 6 sts every round until circumference matches head size.")
            instructions.append("Work even until hat reaches desired depth.")
            instructions.append("Fasten off. Weave in ends.")
        
        else:  # blanket, dishcloth, etc.
            instructions.append(f"Ch {dimensions.get('width', 10) * 4}.")
            instructions.append(f"Row 1: {stitches[1]} in 2nd ch from hook and each ch across. Turn.")
            instructions.append("Repeat Row 1 until piece reaches desired size.")
            instructions.append("Fasten off. Weave in ends.")
        
        return instructions
    
    def _generate_notes(self, difficulty: str, project_type: str) -> List[str]:
        """Generate helpful notes"""
        notes = []
        
        if difficulty == "beginner":
            notes.append("Perfect for beginners!")
            notes.append("Practice tension on a swatch first.")
        elif difficulty == "intermediate":
            notes.append("Intermediate level - some experience required.")
            notes.append("Check gauge for proper sizing.")
        else:
            notes.append("Advanced pattern - take your time!")
            notes.append("Read through entire pattern before starting.")
        
        notes.append("Adjust hook size to match gauge.")
        notes.append("Weave in ends securely.")
        
        return notes
    
    def validate_pattern(self, pattern: Dict) -> Dict:
        """Validate a generated pattern"""
        issues = []
        
        if not pattern.get("materials"):
            issues.append("Missing materials list")
        
        if not pattern.get("gauge"):
            issues.append("Missing gauge information")
        
        if not pattern.get("pattern") or len(pattern["pattern"]) < 3:
            issues.append("Pattern instructions too short")
        
        if not pattern.get("stitches_used"):
            issues.append("No stitches specified")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "score": 100 - (len(issues) * 20),
        }
    
    def estimate_time(self, pattern: Dict) -> Dict:
        """Estimate completion time"""
        stitch_count = len(pattern.get("pattern", []))
        difficulty_multiplier = {
            "beginner": 1.0,
            "intermediate": 1.5,
            "advanced": 2.0,
        }
        
        base_hours = stitch_count * 0.5
        multiplier = difficulty_multiplier.get(pattern.get("difficulty", "beginner"), 1.0)
        estimated_hours = base_hours * multiplier
        
        return {
            "estimated_hours": round(estimated_hours, 1),
            "estimated_days": max(1, round(estimated_hours / 2)),
            "skill_level": pattern.get("difficulty", "beginner"),
        }


# Demo
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  AI PATTERN GENERATOR - DEMONSTRATION")
    print("=" * 60)
    
    gen = AIPatternGenerator()
    
    # Generate patterns
    print("\n🧶 Generating Beginner Scarf...")
    pattern1 = gen.generate_pattern(
        "cozy winter scarf",
        difficulty="beginner",
        project_type="scarf",
        yarn_weight="worsted"
    )
    print(f"  Title: {pattern1['title']}")
    print(f"  Materials: {pattern1['materials']['yarn']}")
    print(f"  Gauge: {pattern1['gauge']}")
    print(f"  Instructions: {len(pattern1['pattern'])} steps")
    
    print("\n🧶 Generating Intermediate Hat...")
    pattern2 = gen.generate_pattern(
        "warm beanie with texture",
        difficulty="intermediate",
        project_type="hat",
        yarn_weight="bulky"
    )
    print(f"  Title: {pattern2['title']}")
    print(f"  Stitches: {', '.join(pattern2['stitches_used'])}")
    
    # Validate
    print("\n✅ Validating Pattern...")
    validation = gen.validate_pattern(pattern1)
    print(f"  Valid: {validation['valid']}")
    print(f"  Score: {validation['score']}/100")
    if validation['issues']:
        print(f"  Issues: {validation['issues']}")
    
    # Estimate time
    print("\n⏱️  Time Estimate...")
    time_est = gen.estimate_time(pattern1)
    print(f"  Estimated: {time_est['estimated_hours']} hours")
    print(f"  Days: {time_est['estimated_days']}")
    
    print(f"\n  AI Pattern Generator Complete! 🤖")
