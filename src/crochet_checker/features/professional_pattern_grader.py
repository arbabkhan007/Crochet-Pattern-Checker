"""
Professional Pattern Grader - Grade patterns like a professional
"""

class ProfessionalPatternGrader:
    def __init__(self):
        self.grading_criteria = {
            "clarity": {"weight": 25, "description": "How clear instructions are"},
            "completeness": {"weight": 20, "description": "All information included"},
            "accuracy": {"weight": 20, "description": "Technical correctness"},
            "formatting": {"weight": 15, "description": "Professional presentation"},
            "usability": {"weight": 20, "description": "Easy to follow"},
        }
    
    def grade_pattern(self, pattern_text: str, metadata: dict = None) -> dict:
        """Grade pattern professionally"""
        if metadata is None:
            metadata = {}
        
        scores = {}
        
        # Clarity score
        clarity = self._grade_clarity(pattern_text)
        scores["clarity"] = clarity
        
        # Completeness score
        completeness = self._grade_completeness(pattern_text, metadata)
        scores["completeness"] = completeness
        
        # Accuracy score
        accuracy = self._grade_accuracy(pattern_text)
        scores["accuracy"] = accuracy
        
        # Formatting score
        formatting = self._grade_formatting(pattern_text)
        scores["formatting"] = formatting
        
        # Usability score
        usability = self._grade_usability(pattern_text)
        scores["usability"] = usability
        
        # Calculate weighted total
        total_score = sum(scores[criteria] * self.grading_criteria[criteria]["weight"] / 100 
                         for criteria in scores)
        
        return {
            "scores": scores,
            "total_score": total_score,
            "grade": self._calculate_grade(total_score),
            "strengths": self._identify_strengths(scores),
            "improvements": self._identify_improvements(scores),
            "professional_rating": self._get_professional_rating(total_score)
        }
    
    def _grade_clarity(self, pattern_text: str) -> float:
        lines = pattern_text.strip().split('\n')
        score = 80
        
        if any("row" in line.lower() for line in lines):
            score += 10
        
        if len(pattern_text) > 200:
            score += 10
        
        return min(100, score)
    
    def _grade_completeness(self, pattern_text: str, metadata: dict) -> float:
        score = 60
        
        if "materials" in pattern_text.lower() or metadata.get("materials"):
            score += 15
        
        if "gauge" in pattern_text.lower() or metadata.get("gauge"):
            score += 15
        
        if "abbreviation" in pattern_text.lower():
            score += 10
        
        return min(100, score)
    
    def _grade_accuracy(self, pattern_text: str) -> float:
        score = 85
        
        lines = pattern_text.strip().split('\n')
        if len(lines) > 3:
            score += 10
        
        return min(100, score)
    
    def _grade_formatting(self, pattern_text: str) -> float:
        score = 75
        
        if "\n\n" in pattern_text:
            score += 15
        
        if len(pattern_text) > 500:
            score += 10
        
        return min(100, score)
    
    def _grade_usability(self, pattern_text: str) -> float:
        score = 80
        
        lines = pattern_text.strip().split('\n')
        if len(lines) > 5:
            score += 10
        
        return min(100, score)
    
    def _calculate_grade(self, score: float) -> str:
        if score >= 95:
            return "A+"
        elif score >= 90:
            return "A"
        elif score >= 85:
            return "B+"
        elif score >= 80:
            return "B"
        elif score >= 75:
            return "C+"
        elif score >= 70:
            return "C"
        else:
            return "D"
    
    def _identify_strengths(self, scores: dict) -> list:
        strengths = []
        for criteria, score in scores.items():
            if score >= 85:
                strengths.append(f"{criteria.capitalize()}: {score:.0f}/100")
        return strengths
    
    def _identify_improvements(self, scores: dict) -> list:
        improvements = []
        for criteria, score in scores.items():
            if score < 75:
                improvements.append(f"{criteria.capitalize()}: {score:.0f}/100 - needs improvement")
        return improvements
    
    def _get_professional_rating(self, score: float) -> str:
        if score >= 90:
            return "Publication Ready"
        elif score >= 80:
            return "Professional Quality"
        elif score >= 70:
            return "Good Quality"
        else:
            return "Needs Revision"

if __name__ == "__main__":
    print("🎓 Professional Pattern Grader")
    print("=" * 60)
    
    grader = ProfessionalPatternGrader()
    
    pattern = """Materials: Worsted weight yarn, 5mm hook
Gauge: 14 sc x 16 rows = 4 inches

Abbreviations:
sc - single crochet
ch - chain

Pattern:
Row 1: 10 sc
Row 2: ch 1, turn, 10 sc
Row 3: ch 1, turn, 10 sc"""
    
    result = grader.grade_pattern(pattern, {"materials": True, "gauge": True})
    
    print(f"\nTotal Score: {result['total_score']:.1f}/100")
    print(f"Grade: {result['grade']}")
    print(f"Professional Rating: {result['professional_rating']}")
    
    print("\nDetailed Scores:")
    for criteria, score in result['scores'].items():
        print(f"  {criteria.capitalize()}: {score:.0f}/100")
    
    if result['strengths']:
        print("\n✅ Strengths:")
        for strength in result['strengths']:
            print(f"  • {strength}")
    
    if result['improvements']:
        print("\n⚠️ Needs Improvement:")
        for improvement in result['improvements']:
            print(f"  • {improvement}")
    
    print("\n✨ Grading complete!")
