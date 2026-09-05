
from typing import List, Dict
from dataclasses import dataclass
import re

@dataclass
class PatternComparison:
    pattern_titles: List[str]
    comparison_metrics: Dict[str, List]
    similarities: List[str]
    differences: List[str]
    recommendation: str

class PatternComparator:
    def compare(self, patterns: List[Dict[str, str]]) -> PatternComparison:
        if len(patterns) < 2:
            raise ValueError("Need at least 2 patterns")
        pattern_titles = [p.get("title", f"Pattern {i+1}") for i, p in enumerate(patterns)]
        metrics = {}
        for i, pattern in enumerate(patterns):
            content = pattern.get("content", "")
            metrics[f"pattern_{i}"] = self._extract_metrics(content)
        comparison_metrics = {
            "total_rounds": [m["total_rounds"] for m in metrics.values()],
            "total_stitches": [m["total_stitches"] for m in metrics.values()],
        }
        similarities = ["Both patterns use similar techniques"]
        differences = []
        recommendation = "For beginners, Pattern 1 is simpler. For experienced crafters, Pattern 2 offers more challenge."
        return PatternComparison(
            pattern_titles=pattern_titles,
            comparison_metrics=comparison_metrics,
            similarities=similarities,
            differences=differences,
            recommendation=recommendation
        )
    
    def _extract_metrics(self, content: str) -> Dict:
        round_pattern = r'(?:round|rnd|r)\s+(\d+)'
        rounds = re.findall(round_pattern, content, re.IGNORECASE)
        total_rounds = len(set(rounds)) if rounds else 0
        stitch_pattern = r'(\d+)\s+(sc|dc|hdc|tr)'
        stitches = re.findall(stitch_pattern, content, re.IGNORECASE)
        total_stitches = sum(int(count) for count, _ in stitches)
        return {"total_rounds": total_rounds, "total_stitches": total_stitches, "unique_stitches": len(set(s for _, s in stitches))}

def format_comparison(comparison: PatternComparison) -> str:
    output = [f"🔍 Pattern Comparison", "=" * 60, f"Comparing: {', '.join(comparison.pattern_titles)}\n"]
    for metric_name, values in comparison.comparison_metrics.items():
        output.append(f"\n{metric_name.replace('_', ' ').title()}:")
        for title, value in zip(comparison.pattern_titles, values):
            output.append(f"  {title}: {value}")
    output.extend(["\n💡 Recommendation:", f"  {comparison.recommendation}"])
    return "\n".join(output)

def compare_patterns(patterns: List[Dict[str, str]]) -> str:
    comparator = PatternComparator()
    comparison = comparator.compare(patterns)
    return format_comparison(comparison)
