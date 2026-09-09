
from typing import List, Dict
from dataclasses import dataclass
import re

@dataclass
class PatternAnalytics:
    title: str
    total_rounds: int
    total_stitches: int
    stitch_distribution: Dict[str, int]
    unique_stitches: List[str]
    avg_stitches_per_round: float
    complexity_score: float
    estimated_time_minutes: int
    difficulty_factors: List[str]

class PatternAnalyticsEngine:
    def analyze(self, pattern_text: str, title: str = "Pattern") -> PatternAnalytics:
        lines = pattern_text.split('\n')
        round_pattern = r'(?:round|rnd|r)\s+(\d+)'
        rounds = re.findall(round_pattern, pattern_text, re.IGNORECASE)
        total_rounds = len(set(rounds)) if rounds else len([l for l in lines if 'round' in l.lower()])
        
        stitch_pattern = r'(\d+)\s+(sc|dc|hdc|tr|sl st|ch|inc|dec)'
        stitches = re.findall(stitch_pattern, pattern_text, re.IGNORECASE)
        
        stitch_counts = {}
        total_stitches = 0
        
        for count, stitch_type in stitches:
            count = int(count)
            stitch_type = stitch_type.lower()
            stitch_counts[stitch_type] = stitch_counts.get(stitch_type, 0) + count
            total_stitches += count
        
        avg_stitches = total_stitches / total_rounds if total_rounds > 0 else 0
        unique_stitches = list(stitch_counts.keys())
        complexity = self._calculate_complexity(stitch_counts, total_rounds)
        estimated_time = int(total_stitches * 0.1)
        difficulty_factors = self._identify_difficulty_factors(pattern_text, stitch_counts)
        
        return PatternAnalytics(
            title=title,
            total_rounds=total_rounds,
            total_stitches=total_stitches,
            stitch_distribution=stitch_counts,
            unique_stitches=unique_stitches,
            avg_stitches_per_round=round(avg_stitches, 1),
            complexity_score=complexity,
            estimated_time_minutes=estimated_time,
            difficulty_factors=difficulty_factors
        )
    
    def _calculate_complexity(self, stitch_counts: Dict[str, int], total_rounds: int) -> float:
        score = 0.0
        unique_stitches = len(stitch_counts)
        score += min(3.0, unique_stitches * 0.5)
        score += min(3.0, total_rounds * 0.05)
        complex_stitches = ['tr', 'dtr', 'trtr']
        for stitch in complex_stitches:
            if stitch in stitch_counts:
                score += 1.0
        if 'inc' in stitch_counts or 'dec' in stitch_counts:
            score += 1.0
        return min(10.0, score)
    
    def _identify_difficulty_factors(self, pattern_text: str, stitch_counts: Dict[str, int]) -> List[str]:
        factors = []
        text_lower = pattern_text.lower()
        if 'magic ring' in text_lower or 'mr' in text_lower:
            factors.append('Magic ring')
        if 'inc' in stitch_counts and 'dec' in stitch_counts:
            factors.append('Increases and decreases')
        if 'tr' in stitch_counts or 'dtr' in stitch_counts:
            factors.append('Tall stitches (treble+)')
        if 'color change' in text_lower or 'change to' in text_lower:
            factors.append('Color changes')
        if 'sew' in text_lower or 'assemble' in text_lower:
            factors.append('Assembly required')
        if len(stitch_counts) > 5:
            factors.append('Multiple stitch types')
        return factors

def format_analytics(analytics: PatternAnalytics) -> str:
    output = [
        f"📊 Pattern Analytics: {analytics.title}",
        "=" * 50,
        "",
        f"📏 Structure:",
        f"   Total Rounds: {analytics.total_rounds}",
        f"   Total Stitches: {analytics.total_stitches:,}",
        f"   Avg Stitches/Round: {analytics.avg_stitches_per_round}",
        "",
        f"🧵 Stitch Distribution:",
    ]
    for stitch, count in sorted(analytics.stitch_distribution.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / analytics.total_stitches * 100) if analytics.total_stitches > 0 else 0
        output.append(f"   {stitch.upper()}: {count:,} ({percentage:.1f}%)")
    output.extend([
        "",
        f"⏱️  Time & Difficulty:",
        f"   Estimated Time: {analytics.estimated_time_minutes} minutes ({analytics.estimated_time_minutes / 60:.1f} hours)",
        f"   Complexity Score: {analytics.complexity_score:.1f}/10",
        f"   Unique Stitches: {len(analytics.unique_stitches)}",
        "",
        f"🎯 Difficulty Factors:",
    ])
    for factor in analytics.difficulty_factors:
        output.append(f"   • {factor}")
    return "\n".join(output)

def generate_analytics_report(pattern_text: str, title: str = "Pattern") -> str:
    engine = PatternAnalyticsEngine()
    analytics = engine.analyze(pattern_text, title)
    return format_analytics(analytics)
