"""Complexity Analyzer"""
from dataclasses import dataclass

@dataclass
class ComplexityScore:
    overall_score: float
    difficulty_level: str

class ComplexityAnalyzer:
    def analyze(self, pattern_text: str) -> ComplexityScore:
        text_lower = pattern_text.lower()
        score = 0
        if 'cluster' in text_lower or 'bobble' in text_lower: score += 30
        if '*' in text_lower: score += 20
        if len(text_lower.split('\n')) > 30: score += 25
        level = 'beginner' if score < 30 else 'intermediate' if score < 60 else 'advanced' if score < 80 else 'expert'
        return ComplexityScore(overall_score=min(100, score), difficulty_level=level)
