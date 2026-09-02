"""Auto-detect pattern category from pattern structure."""
from typing import Optional
from ..model.pattern import Pattern

def detect_category(pattern: Pattern) -> str:
    if hasattr(pattern.metadata, 'category') and pattern.metadata.category:
        return pattern.metadata.category
    
    indicators = {'amigurumi': [], 'hat': [], 'scarf': [], 'blanket': []}
    
    for item in (pattern.rounds or pattern.rows):
        for inst in item.instructions:
            if 'magic ring' in inst.source_text.lower() or 'mr' in inst.source_text.lower():
                indicators['amigurumi'].append('magic_ring')
    
    if pattern.rounds:
        max_stitches = max(r.computed_stitch_count for r in pattern.rounds)
        if max_stitches < 50:
            indicators['amigurumi'].append('small')
        if max_stitches > 200:
            indicators['blanket'].append('large')
    
    text_lower = pattern.source_text.lower()
    if 'amigurumi' in text_lower or 'stuffed' in text_lower:
        indicators['amigurumi'].append('keyword')
    if 'hat' in text_lower or 'beanie' in text_lower:
        indicators['hat'].append('keyword')
    
    scores = {cat: len(ind) for cat, ind in indicators.items()}
    if scores:
        best = max(scores, key=scores.get)
        if scores[best] > 0:
            return best
    
    return 'unknown'
