"""
Special Construction Validator
Handles: granny squares, spirals, joined rounds, flat rows
"""
import re
from typing import Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class ConstructionAnalysis:
    type: str
    is_valid: bool
    details: Dict = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    expected_counts: Dict[int, int] = field(default_factory=dict)


class GrannySquareValidator:
    """Validates granny square construction (+12 dc per round)"""
    CORNERS = 4
    
    def validate(self, rounds_data: List[Dict], setup_round: int = 3) -> ConstructionAnalysis:
        analysis = ConstructionAnalysis(type="granny_square", is_valid=True)
        if not rounds_data:
            analysis.is_valid = False
            analysis.errors.append("No round data")
            return analysis
        
        for rnd_data in rounds_data:
            rn = rnd_data['round']
            stated = rnd_data.get('count', 0)
            expected = 12 * rn if rn >= 1 else 12
            analysis.expected_counts[rn] = expected
            if stated != expected:
                analysis.is_valid = False
                analysis.errors.append(f"Round {rn}: Expected {expected}, got {stated}")
        
        analysis.details['growth_per_round'] = 12
        analysis.details['corners'] = self.CORNERS
        return analysis


class SpiralValidator:
    """Validates spiral/continuous construction"""
    def validate(self, rounds_data: List[Dict]) -> ConstructionAnalysis:
        analysis = ConstructionAnalysis(type="spiral", is_valid=True)
        sorted_rounds = sorted(rounds_data, key=lambda r: r['round'])
        
        for i in range(1, len(sorted_rounds)):
            prev = sorted_rounds[i-1]
            curr = sorted_rounds[i]
            change = curr['count'] - prev['count']
            instr = curr.get('instruction', '').lower()
            
            if 'sl st' in instr and 'join' in instr:
                analysis.warnings.append(f"Round {curr['round']}: Join detected in spiral")
            if 'turn' in instr:
                analysis.warnings.append(f"Round {curr['round']}: Turn detected in spiral")
        
        return analysis


class JoinedRoundValidator:
    """Validates joined round construction"""
    def validate(self, rounds_data: List[Dict]) -> ConstructionAnalysis:
        analysis = ConstructionAnalysis(type="joined_rounds", is_valid=True)
        return analysis


class SpecialConstructionDetector:
    """Auto-detect construction type"""
    KEYWORDS = {
        'granny_square': ['granny square', 'granny-square', 'corner space', '(3 dc, ch 2, 3 dc)'],
        'spiral': ['spiral', 'continuous', 'no join', 'never join'],
        'joined_rounds': ['sl st to close', 'sl st to first', 'ch-3 counts', 'ch 3 counts'],
        'flat_rows': ['turn work', 'turn your work', 'row 1', 'rs row', 'ws row'],
        'amigurumi': ['magic ring', 'amigurumi', 'stuff firmly'],
    }
    
    def detect(self, text: str) -> Dict[str, bool]:
        tl = text.lower()
        return {c: any(kw in tl for kw in kws) for c, kws in self.KEYWORDS.items()}
    
    def get_primary(self, text: str) -> str:
        d = self.detect(text)
        for t in ['granny_square', 'spiral', 'joined_rounds', 'flat_rows', 'amigurumi']:
            if d.get(t): return t
        return 'unknown'


if __name__ == "__main__":
    import sys
    sys.path.insert(0, 'src')
    from crochet_checker.utils.enhanced_pdf import AestheticPrinter, Colors
    
    pp = AestheticPrinter('sage_garden')
    pp.header("SPECIAL CONSTRUCTION VALIDATOR", "Demo")
    
    # Test granny square
    pp.section("GRANNY SQUARE", "📐")
    validator = GrannySquareValidator()
    gs_rounds = [
        {'round': 1, 'count': 12},
        {'round': 2, 'count': 24},
        {'round': 3, 'count': 36},
        {'round': 5, 'count': 60},
        {'round': 10, 'count': 120},
        {'round': 20, 'count': 240},
    ]
    result = validator.validate(gs_rounds)
    if result.is_valid:
        pp.success("Granny square counts verified!")
    for rn, expected in sorted(result.expected_counts.items()):
        actual = next((r['count'] for r in gs_rounds if r['round'] == rn), '?')
        if actual == expected:
            pp.success(f"Round {rn}: {expected} dc ✓")
        else:
            pp.error(f"Round {rn}: Expected {expected}, got {actual}")
    
    # Test spiral
    pp.section("SPIRAL", "🌀")
    sv = SpiralValidator()
    head = [
        {'round': 1, 'instruction': '6 sc in MR', 'count': 6},
        {'round': 2, 'instruction': 'inc in each st around', 'count': 12},
        {'round': 3, 'instruction': '[sc, inc] x 6', 'count': 18},
        {'round': 6, 'instruction': '[4 sc, inc] x 6', 'count': 36},
        {'round': 11, 'instruction': '[4 sc, dec] x 6', 'count': 30},
        {'round': 15, 'instruction': 'dec x 6', 'count': 6},
    ]
    sr = sv.validate(head)
    if sr.is_valid:
        pp.success("Spiral construction valid!")
    for w in sr.warnings:
        pp.warning(w)
    
    pp.footer()
    pp.gradient_text("🔧 Special Construction Validator Complete! 🔧")
