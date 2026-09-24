"""Pattern Optimization Engine"""
from typing import List
from dataclasses import dataclass

@dataclass
class Optimization:
    category: str
    description: str
    impact: str
    effort: str
    suggestion: str = ""

class PatternOptimizer:
    def optimize(self, pattern_text: str) -> List[Optimization]:
        optimizations = []
        if 'ch 1' in pattern_text.lower() and 'sc' in pattern_text.lower():
            optimizations.append(Optimization('efficiency', 'Potential redundant turning chains', 'low', 'easy', 'Review turning chains for sc rows'))
        if pattern_text.lower().count('sc') > 5 and '*' not in pattern_text:
            optimizations.append(Optimization('clarity', 'Long stitch sequence could use repeat notation', 'medium', 'easy', 'Consider using *...* repeat notation'))
        return optimizations
