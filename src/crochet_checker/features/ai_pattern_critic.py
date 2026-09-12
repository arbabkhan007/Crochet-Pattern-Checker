"""
AI Pattern Critic - Review patterns and suggest improvements using AI analysis
"""
from typing import Dict, List


class AIPatternCritic:
    """AI-powered pattern review and improvement suggestions"""
    
    def __init__(self):
        self.criteria = {
            "clarity": "Are instructions clear and unambiguous?",
            "completeness": "Are all steps included?",
            "consistency": "Are stitch counts consistent?",
            "terminology": "Is terminology standard and consistent?",
            "formatting": "Is the pattern well-formatted?",
        }
    
    def review_pattern(self, pattern_text: str) -> Dict:
        """Review a pattern and provide feedback"""
        issues = []
        suggestions = []
        scores = {}
        
        lines = pattern_text.strip().split('\n')
        
        # Check clarity
        clarity_score = 10
        if any("do stuff" in line.lower() or "make it" in line.lower() for line in lines):
            issues.append("Vague instructions found - be more specific")
            clarity_score -= 3
        scores["clarity"] = clarity_score
        
        # Check completeness
        completeness_score = 10
        if not any("materials" in line.lower() or "supplies" in line.lower() for line in lines):
            issues.append("No materials list found")
            completeness_score -= 2
        if not any("gauge" in line.lower() for line in lines):
            suggestions.append("Consider adding gauge information")
            completeness_score -= 1
        scores["completeness"] = completeness_score
        
        # Check consistency (stitch counts)
        consistency_score = 10
        stitch_counts = []
        for line in lines:
            if "(" in line and ")" in line:
                try:
                    count = int(line.split("(")[1].split(")")[0].split()[0])
                    stitch_counts.append(count)
                except:
                    pass
        
        if len(stitch_counts) > 1:
            if stitch_counts[0] != stitch_counts[-1] and len(set(stitch_counts)) > 2:
                issues.append("Stitch counts vary without explanation")
                consistency_score -= 3
        scores["consistency"] = consistency_score
        
        # Check terminology
        terminology_score = 10
        abbreviations = set()
        for line in lines:
            words = line.split()
            for word in words:
                if len(word) <= 4 and word.isalpha() and word.islower():
                    if word not in ["ch", "sc", "dc", "hdc", "tr", "sl", "st", "sts", "rep", "inc", "dec"]:
                        abbreviations.add(word)
        
        if abbreviations:
            suggestions.append(f"Define abbreviations: {', '.join(list(abbreviations)[:3])}")
        scores["terminology"] = terminology_score
        
        # Check formatting
        formatting_score = 10
        if len(lines) > 10:
            if not any(line.strip().startswith(("Row", "Round", "Materials", "Instructions")) for line in lines):
                suggestions.append("Add clear section headers (Materials, Instructions, etc.)")
                formatting_score -= 2
        scores["formatting"] = formatting_score
        
        # Calculate overall score
        overall = sum(scores.values()) / len(scores)
        
        return {
            "overall_score": round(overall, 1),
            "scores": scores,
            "issues": issues,
            "suggestions": suggestions,
            "grade": self._calculate_grade(overall),
        }
    
    def _calculate_grade(self, score: float) -> str:
        """Convert score to letter grade"""
        if score >= 9:
            return "A+"
        elif score >= 8:
            return "A"
        elif score >= 7:
            return "B"
        elif score >= 6:
            return "C"
        elif score >= 5:
            return "D"
        else:
            return "F"
    
    def generate_improvement_plan(self, review: Dict) -> str:
        """Generate a plan to improve the pattern"""
        plan = f"""
╔══════════════════════════════════════════════════════════╗
║         📝 PATTERN IMPROVEMENT PLAN                       ║
║         Overall Grade: {review['grade']} ({review['overall_score']}/10)                      ║
╚══════════════════════════════════════════════════════════╝

📊 SCORE BREAKDOWN
═══════════════════════════════════════════════════════════
  Clarity:       {review['scores']['clarity']}/10
  Completeness:  {review['scores']['completeness']}/10
  Consistency:   {review['scores']['consistency']}/10
  Terminology:   {review['scores']['terminology']}/10
  Formatting:    {review['scores']['formatting']}/10
"""
        
        if review["issues"]:
            plan += "\n❌ ISSUES TO FIX\n"
            plan += "═" * 59 + "\n"
            for issue in review["issues"]:
                plan += f"  • {issue}\n"
        
        if review["suggestions"]:
            plan += "\n💡 SUGGESTIONS\n"
            plan += "═" * 59 + "\n"
            for suggestion in review["suggestions"]:
                plan += f"  • {suggestion}\n"
        
        if not review["issues"] and not review["suggestions"]:
            plan += "\n✅ Pattern looks great! No major issues found.\n"
        
        return plan


if __name__ == "__main__":
    print("🤖 AI Pattern Critic")
    print("=" * 50)
    
    critic = AIPatternCritic()
    
    # Sample pattern to review
    pattern = """
    Cozy Scarf Pattern
    
    Materials:
    - 400 yards worsted yarn
    - 5.0mm hook
    
    Gauge: 14 sc = 4 inches
    
    Instructions:
    Row 1: Ch 30, sc in 2nd ch from hook and each ch across (29)
    Row 2: Ch 1, turn, sc in each st across (29)
    Row 3-50: Repeat Row 2
    Fasten off
    """
    
    print("\n🔍 Reviewing pattern...")
    review = critic.review_pattern(pattern)
    
    print(f"\n📊 Scores:")
    for category, score in review["scores"].items():
        print(f"  {category:12s}: {score}/10")
    
    print(f"\n🎯 Overall: {review['overall_score']}/10 (Grade: {review['grade']})")
    
    if review["issues"]:
        print(f"\n❌ Issues:")
        for issue in review["issues"]:
            print(f"  • {issue}")
    
    if review["suggestions"]:
        print(f"\n💡 Suggestions:")
        for suggestion in review["suggestions"]:
            print(f"  • {suggestion}")
    
    print("\n📋 Improvement Plan:")
    print(critic.generate_improvement_plan(review))
    
    print("\n✅ AI Pattern Critic ready!")
