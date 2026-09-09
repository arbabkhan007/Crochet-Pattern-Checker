"""Yarn Consumption Calculator"""

from dataclasses import dataclass
from typing import Dict

@dataclass
class YarnEstimate:
    total_yards: float
    total_grams: float
    total_ounces: float
    skeins_needed: int
    skein_size_yards: int
    confidence: str
    breakdown: Dict[str, float]

STITCH_YARN_USAGE = {
    'sc': 0.10, 'dc': 0.20, 'hdc': 0.15, 'tr': 0.25,
    'ch': 0.05, 'sl st': 0.03,
}

def count_stitches(pattern_text: str) -> Dict[str, int]:
    import re
    stitch_counts = {}
    stitch_pattern = r'(\d+)\s+(sc|dc|hdc|tr|sl st|ch)\b'
    
    for match in re.finditer(stitch_pattern, pattern_text.lower()):
        count = int(match.group(1))
        stitch_type = match.group(2)
        stitch_counts[stitch_type] = stitch_counts.get(stitch_type, 0) + count
    
    return stitch_counts

def estimate_yarn(pattern_text: str, yarn_weight: str = 'worsted', skein_size: int = 200) -> YarnEstimate:
    stitch_counts = count_stitches(pattern_text)
    total_yards = sum(count * STITCH_YARN_USAGE.get(stitch, 0.10) for stitch, count in stitch_counts.items())
    total_yards *= 1.10
    
    yards_per_gram = {'worsted': 1.9, 'dk': 2.5, 'bulky': 1.3}.get(yarn_weight, 1.9)
    total_grams = total_yards / yards_per_gram
    total_ounces = total_grams / 28.35
    skeins_needed = int(total_yards / skein_size) + 1
    confidence = 'high' if len(stitch_counts) > 5 else 'medium' if len(stitch_counts) > 2 else 'low'
    
    return YarnEstimate(
        total_yards=round(total_yards, 1),
        total_grams=round(total_grams, 1),
        total_ounces=round(total_ounces, 2),
        skeins_needed=skeins_needed,
        skein_size_yards=skein_size,
        confidence=confidence,
        breakdown=stitch_counts
    )

def format_yarn_estimate(estimate: YarnEstimate) -> str:
    return f"""🧶 Yarn Consumption Estimate
{'=' * 40}
Total Yards: {estimate.total_yards} yards
Total Grams: {estimate.total_grams} g
Total Ounces: {estimate.total_ounces} oz
Skeins Needed: {estimate.skeins_needed} (assuming {estimate.skein_size_yards} yard skeins)
Confidence: {estimate.confidence.upper()}"""
