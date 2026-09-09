"""
Pattern Difficulty Analyzer - Analyze and rate crochet pattern complexity
"""
from typing import Dict, List, Optional
import re


class PatternDifficultyAnalyzer:
    """
    Analyze crochet patterns and rate their difficulty
    
    Features:
    - Stitch complexity scoring
    - Technique detection
    - Pattern length analysis
    - Special stitch detection
    - Overall difficulty rating
    - Skill requirements
    """
    
    STITCH_DIFFICULTY = {
        # Beginner stitches
        "ch": 1, "sl st": 1, "sc": 1,
        # Easy stitches
        "hdc": 2, "dc": 2, "tr": 2,
        # Intermediate stitches
        "dtr": 3, "ttr": 3, "fpdc": 3, "bpdc": 3,
        "fpsc": 3, "bpsc": 3, "pop": 3, "puff": 3,
        # Advanced stitches
        "cable": 4, "xst": 4, "bullion": 4, "solomon": 4,
        "hairpin": 4, "tatting": 4, "broomstick": 4,
        "tunisian": 4, "entrelac": 4,
        # Expert stitches
        "irish": 5, "filet": 5, "overlay": 5,
        "tapestry": 5, "mosaic": 5,
    }
    
    TECHNIQUE_DIFFICULTY = {
        "magic ring": 2,
        "gauge swatch": 2,
        "blocking": 2,
        "seaming": 2,
        "color change": 2,
        "working in rounds": 2,
        "increases": 1,
        "decreases": 2,
        "shape": 2,
        "amigurumi": 3,
        "colorwork": 4,
        "intarsia": 4,
        "fair isle": 4,
        "cables": 4,
        "lace": 4,
        "freeform": 5,
        "design": 5,
    }
    
    COMPLEXITY_INDICATORS = [
        (r"\(.*?\)", 0.5),  # Repeats
        (r"\*", 0.5),  # Pattern repeats
        (r"\[.*?\]", 0.3),  # Brackets
        (r"turn", 1),  # Turning work
        (r"join", 1),  # Joining
        (r"sew", 1.5),  # Assembly
        (r"assemble", 1.5),
        (r"block", 1),
        (r"weave in ends", 0.5),
        (r"gauge", 1.5),
        (r"multiple of", 1),
        (r"chart", 2),
        (r"symbol", 2),
    ]
    
    def analyze_pattern(self, pattern_text: str) -> Dict:
        """Analyze a pattern and calculate difficulty"""
        if not pattern_text or len(pattern_text) < 50:
            return {"error": "Pattern too short to analyze"}
        
        # Convert to lowercase for analysis
        text = pattern_text.lower()
        
        # Score stitches
        stitch_score = 0
        stitches_found = []
        for stitch, difficulty in self.STITCH_DIFFICULTY.items():
            count = len(re.findall(rf'\b{stitch}\b', text))
            if count > 0:
                stitch_score += difficulty * count
                stitches_found.append({"stitch": stitch, "count": count, "difficulty": difficulty})
        
        # Score techniques
        technique_score = 0
        techniques_found = []
        for technique, difficulty in self.TECHNIQUE_DIFFICULTY.items():
            if technique in text:
                technique_score += difficulty * 2
                techniques_found.append({"technique": technique, "difficulty": difficulty})
        
        # Complexity indicators
        complexity_score = 0
        for pattern, weight in self.COMPLEXITY_INDICATORS:
            matches = len(re.findall(pattern, text))
            complexity_score += matches * weight
        
        # Pattern length (longer = more complex)
        word_count = len(text.split())
        length_score = min(5, word_count / 200)
        
        # Total score
        total_score = (stitch_score + technique_score + complexity_score + length_score)
        
        # Normalize to 1-5 scale
        normalized = min(5, max(1, total_score / 10))
        
        # Determine level
        level, emoji = self._get_level(normalized)
        
        # Estimate time
        time_estimate = self._estimate_time(word_count, normalized)
        
        return {
            "difficulty_score": round(normalized, 1),
            "level": level,
            "emoji": emoji,
            "estimated_time": time_estimate,
            "word_count": word_count,
            "stitches_found": sorted(stitches_found, key=lambda x: -x["difficulty"]),
            "techniques_required": sorted(techniques_found, key=lambda x: -x["difficulty"]),
            "complexity_factors": {
                "stitch_complexity": round(stitch_score, 1),
                "technique_complexity": round(technique_score, 1),
                "pattern_complexity": round(complexity_score, 1),
                "length_factor": round(length_score, 1),
            },
            "recommendations": self._get_recommendations(normalized, techniques_found),
        }
    
    def _get_level(self, score: float) -> tuple:
        """Get difficulty level from score"""
        if score < 1.5:
            return "Beginner", "🌱"
        elif score < 2.5:
            return "Easy", "🌿"
        elif score < 3.5:
            return "Intermediate", "🌳"
        elif score < 4.5:
            return "Advanced", "🏆"
        else:
            return "Expert", "👑"
    
    def _estimate_time(self, words: int, difficulty: float) -> str:
        """Estimate completion time"""
        base_hours = words / 50  # Rough estimate
        adjusted = base_hours * (0.5 + difficulty / 5)
        
        if adjusted < 2:
            return f"{int(adjusted * 60)} minutes"
        elif adjusted < 10:
            return f"{adjusted:.1f} hours"
        else:
            return f"{adjusted:.0f} hours"
    
    def _get_recommendations(self, score: float, techniques: List[Dict]) -> List[str]:
        """Get recommendations based on analysis"""
        recs = []
        
        if score < 2:
            recs.append("Great for beginners! Simple stitches and clear instructions.")
        elif score < 3:
            recs.append("Comfortable for confident beginners. Some new techniques to learn.")
        elif score < 4:
            recs.append("Intermediate project. Practice new stitches on scrap yarn first.")
        else:
            recs.append("Advanced project. Take your time and enjoy the challenge!")
        
        # Technique-specific recommendations
        for tech in techniques:
            if tech["difficulty"] >= 4:
                recs.append(f"• Practice {tech['technique']} separately before starting")
        
        if score >= 3.5:
            recs.append("• Make a gauge swatch to ensure proper sizing")
        
        return recs
    
    def compare_patterns(self, pattern1: str, pattern2: str) -> Dict:
        """Compare two patterns"""
        analysis1 = self.analyze_pattern(pattern1)
        analysis2 = self.analyze_pattern(pattern2)
        
        if "error" in analysis1 or "error" in analysis2:
            return {"error": "Could not analyze one or both patterns"}
        
        diff = analysis1["difficulty_score"] - analysis2["difficulty_score"]
        
        return {
            "pattern_1": analysis1,
            "pattern_2": analysis2,
            "difference": round(abs(diff), 1),
            "easier": "Pattern 1" if diff > 0 else "Pattern 2",
            "comparison": f"Pattern {'1' if diff > 0 else '2'} is easier",
        }


# Demo
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  PATTERN DIFFICULTY ANALYZER - DEMONSTRATION")
    print("=" * 60)
    
    analyzer = PatternDifficultyAnalyzer()
    
    # Test patterns
    pattern1 = """
    Beginner Scarf
    Ch 20. Row 1: Sc in second ch from hook and each ch across. (19 sts)
    Rows 2-50: Ch 1, turn, sc in each st across. (19 sts)
    Fasten off. Weave in ends.
    """
    
    pattern2 = """
    Intermediate Sweater
    Make gauge swatch first. Magic ring.
    Body: Ch 80, join. Work in rounds.
    Round 1: Sc in each ch around. (80 sts)
    Round 2-10: Fpdc in next st, bpdc in next st around.
    Shape armholes: Skip 10 sts, sc across, ch 10, join.
    Sleeves: Work in rounds with increases every 4 rounds.
    Colorwork section: Follow chart A for yoke pattern.
    Seam shoulders. Block to measurements.
    """
    
    pattern3 = """
    Expert Lace Shawl
    Work from chart. Irish lace technique.
    Make foundation chain of 200.
    Row 1: Dtr, ch 5, skip 5, dtr (shell made).
    Repeat shell pattern following lace chart.
    Picot edging: Ch 3, sl st in first ch, repeat across.
    Block aggressively to open lace pattern.
    Freeform elements: Add random surface crochet flourishes.
    """
    
    print(f"\n📊 Pattern 1: Beginner Scarf")
    result1 = analyzer.analyze_pattern(pattern1)
    print(f"  {result1['emoji']} {result1['level']} ({result1['difficulty_score']}/5)")
    print(f"  Time: {result1['estimated_time']}")
    print(f"  Stitches: {', '.join(s['stitch'] for s in result1['stitches_found'][:3])}")
    
    print(f"\n📊 Pattern 2: Intermediate Sweater")
    result2 = analyzer.analyze_pattern(pattern2)
    print(f"  {result2['emoji']} {result2['level']} ({result2['difficulty_score']}/5)")
    print(f"  Time: {result2['estimated_time']}")
    print(f"  Techniques: {', '.join(t['technique'] for t in result2['techniques_required'][:3])}")
    
    print(f"\n📊 Pattern 3: Expert Lace Shawl")
    result3 = analyzer.analyze_pattern(pattern3)
    print(f"  {result3['emoji']} {result3['level']} ({result3['difficulty_score']}/5)")
    print(f"  Time: {result3['estimated_time']}")
    print(f"  Complexity: {result3['complexity_factors']}")
    
    # Compare
    print(f"\n🔄 Comparing Patterns:")
    comp = analyzer.compare_patterns(pattern1, pattern2)
    if "error" not in comp:
        print(f"  {comp['comparison']}")
        print(f"  Difference: {comp['difference']} points")
    
    # Recommendations
    print(f"\n💡 Recommendations for Pattern 2:")
    for rec in result2["recommendations"]:
        print(f"  {rec}")
    
    print(f"\n  Pattern Difficulty Analyzer Complete! 📊")
