"""
Complex Pattern Analyzer - Analyze highly intricate crochet patterns
"""

class ComplexPatternAnalyzer:
    def __init__(self):
        self.complexity_metrics = {
            "stitch_variety": 0,
            "color_changes": 0,
            "shape_complexity": 0,
            "technique_advanced": 0
        }
    
    def analyze_complexity(self, pattern_text: str) -> dict:
        """Analyze pattern complexity level"""
        lines = pattern_text.strip().split('\n')
        
        # Count unique stitches
        stitches = set()
        for line in lines:
            for stitch in ['sc', 'dc', 'hdc', 'tr', 'dtr', 'fpdc', 'bpdc', 'bobble', 'popcorn']:
                if stitch in line.lower():
                    stitches.add(stitch)
        
        # Count color changes
        color_changes = pattern_text.lower().count('color') + pattern_text.lower().count('change yarn')
        
        # Detect advanced techniques
        advanced_techniques = []
        if 'tapestry' in pattern_text.lower():
            advanced_techniques.append('tapestry crochet')
        if 'intarsia' in pattern_text.lower():
            advanced_techniques.append('intarsia')
        if 'fair isle' in pattern_text.lower():
            advanced_techniques.append('Fair Isle')
        if 'hairpin' in pattern_text.lower():
            advanced_techniques.append('hairpin lace')
        if 'tusisian' in pattern_text.lower() or 'afghan' in pattern_text.lower():
            advanced_techniques.append('Tunisian crochet')
        
        complexity_score = len(stitches) * 10 + color_changes * 5 + len(advanced_techniques) * 20
        
        return {
            'complexity_score': complexity_score,
            'unique_stitches': len(stitches),
            'color_changes': color_changes,
            'advanced_techniques': advanced_techniques,
            'difficulty_level': self._get_difficulty(complexity_score),
            'estimated_time_hours': complexity_score * 0.5
        }
    
    def _get_difficulty(self, score: int) -> str:
        if score < 50:
            return "Intermediate"
        elif score < 100:
            return "Advanced"
        elif score < 200:
            return "Expert"
        else:
            return "Master"

if __name__ == "__main__":
    print("🔍 Complex Pattern Analyzer")
    print("=" * 60)
    
    analyzer = ComplexPatternAnalyzer()
    
    # Test with complex pattern
    complex_pattern = """
    Round 1: sc in magic ring, change to red
    Round 2: fpdc, bpdc, tapestry crochet technique
    Round 3: bobble stitch, popcorn stitch
    Round 4: intarsia colorwork, Fair Isle pattern
    Round 5: hairpin lace, tusisian stitch
    """
    
    result = analyzer.analyze_complexity(complex_pattern)
    print(f"\nComplexity Score: {result['complexity_score']}")
    print(f"Difficulty: {result['difficulty_level']}")
    print(f"Unique Stitches: {result['unique_stitches']}")
    print(f"Advanced Techniques: {', '.join(result['advanced_techniques'])}")
    print(f"Estimated Time: {result['estimated_time_hours']} hours")
