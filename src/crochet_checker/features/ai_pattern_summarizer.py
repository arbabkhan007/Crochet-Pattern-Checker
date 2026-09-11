"""
AI Pattern Summarizer - Summarize and extract key info from long patterns
"""
import re
from typing import Dict, List, Optional


class AIPatternSummarizer:
    """
    Summarize crochet patterns intelligently
    
    Features:
    - Extract key measurements
    - Identify stitch patterns
    - Summarize instructions
    - Extract materials
    - Generate quick reference
    """
    
    def summarize_pattern(self, pattern_text: str) -> Dict:
        """
        Summarize a pattern
        
        Args:
            pattern_text: Full pattern text
        
        Returns:
            Dict with summary
        """
        if not pattern_text or len(pattern_text) < 50:
            return {"error": "Pattern too short to summarize"}
        
        # Extract sections
        summary = {
            "total_lines": len(pattern_text.split("\n")),
            "word_count": len(pattern_text.split()),
            "sections": self._extract_sections(pattern_text),
            "measurements": self._extract_measurements(pattern_text),
            "materials": self._extract_materials(pattern_text),
            "stitches": self._extract_stitches(pattern_text),
            "difficulty_estimate": self._estimate_difficulty(pattern_text),
            "quick_reference": self._generate_quick_ref(pattern_text),
            "summary": self._generate_summary(pattern_text),
        }
        
        return summary
    
    def _extract_sections(self, text: str) -> List[str]:
        """Extract section headings"""
        sections = []
        keywords = ["Materials", "Gauge", "Instructions", "Pattern", "Notes", 
                   "Abbreviations", "Finished Size", "Special Stitches"]
        
        for keyword in keywords:
            if keyword.lower() in text.lower():
                sections.append(keyword)
        
        return sections if sections else ["No clear sections identified"]
    
    def _extract_measurements(self, text: str) -> Dict[str, str]:
        """Extract measurements"""
        measurements = {}
        
        # Look for patterns like "8 inches", "20 cm", etc.
        inch_matches = re.findall(r'(\d+(?:\.\d+)?)\s*(?:inch|in|"|cm)', text, re.IGNORECASE)
        if inch_matches:
            measurements["dimensions"] = f"{', '.join(inch_matches[:3])} inches"
        
        # Look for gauge
        gauge_match = re.search(r'gauge[:\s]+([\d\s\w=]+)', text, re.IGNORECASE)
        if gauge_match:
            measurements["gauge"] = gauge_match.group(1).strip()
        
        return measurements if measurements else {"note": "No measurements found"}
    
    def _extract_materials(self, text: str) -> Dict:
        """Extract materials list"""
        materials = {}
        
        # Look for yarn mentions
        yarn_patterns = [
            r'(\w+)\s+(?:weight\s+)?yarn',
            r'(\d+)\s+yards?',
            r'(\d+)\s+(?:g|grams)',
        ]
        
        for pattern in yarn_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                materials["yarn_mentions"] = len(matches)
                break
        
        # Look for hook size
        hook_match = re.search(r'hook\s+(?:size\s+)?[\(\s]*([\d\.]+\s*mm|[\d\.\-]+\s*[A-Z])', text, re.IGNORECASE)
        if hook_match:
            materials["hook"] = hook_match.group(1).strip()
        
        return materials if materials else {"note": "Materials not clearly specified"}
    
    def _extract_stitches(self, text: str) -> List[str]:
        """Extract stitch abbreviations"""
        stitches = set()
        stitch_patterns = [r'\b(sc|dc|hdc|tr|sl st|ch|fpdc|bpdc)\b']
        
        for pattern in stitch_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            stitches.update([m.lower() for m in matches])
        
        return sorted(list(stitches)) if stitches else ["No stitches identified"]
    
    def _estimate_difficulty(self, text: str) -> str:
        """Estimate pattern difficulty"""
        text_lower = text.lower()
        
        # Beginner indicators
        beginner_words = ["beginner", "easy", "simple", "basic", "sc", "dc"]
        beginner_score = sum(1 for word in beginner_words if word in text_lower)
        
        # Advanced indicators
        advanced_words = ["cable", "lace", "filet", "overlay", "entrelac", 
                         "colorwork", "intarsia", "tunisian"]
        advanced_score = sum(1 for word in advanced_words if word in text_lower)
        
        # Length complexity
        line_count = len(text.split("\n"))
        length_score = min(3, line_count // 50)
        
        total_score = beginner_score - advanced_score + length_score
        
        if total_score >= 3:
            return "Beginner"
        elif total_score >= 1:
            return "Intermediate"
        else:
            return "Advanced"
    
    def _generate_quick_ref(self, text: str) -> str:
        """Generate quick reference card"""
        lines = text.split("\n")
        
        # Get first few meaningful lines
        meaningful = [line.strip() for line in lines if len(line.strip()) > 10][:5]
        
        quick_ref = "QUICK REFERENCE\n"
        quick_ref += "=" * 40 + "\n"
        for line in meaningful:
            quick_ref += f"• {line}\n"
        
        return quick_ref
    
    def _generate_summary(self, text: str) -> str:
        """Generate text summary"""
        word_count = len(text.split())
        line_count = len(text.split("\n"))
        
        summary = f"This is a {line_count}-line crochet pattern with approximately {word_count} words. "
        
        # Add difficulty
        difficulty = self._estimate_difficulty(text)
        summary += f"Estimated difficulty: {difficulty}. "
        
        # Add stitch info
        stitches = self._extract_stitches(text)
        if stitches and stitches[0] != "No stitches identified":
            summary += f"Uses {len(stitches)} different stitches. "
        
        summary += "Review the full pattern for complete instructions."
        
        return summary
    
    def extract_pattern_stats(self, pattern_text: str) -> Dict:
        """Extract pattern statistics"""
        return {
            "word_count": len(pattern_text.split()),
            "line_count": len(pattern_text.split("\n")),
            "estimated_time_minutes": len(pattern_text.split("\n")) * 5,
            "complexity": self._estimate_difficulty(pattern_text),
        }


# Demo
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  AI PATTERN SUMMARIZER - DEMONSTRATION")
    print("=" * 60)
    
    summarizer = AIPatternSummarizer()
    
    # Test pattern
    test_pattern = """
    COZY SCARF PATTERN
    
    Materials:
    - 400 yards worsted weight yarn
    - 5.5mm (I-9) hook
    - Scissors
    - Tapestry needle
    
    Gauge:
    14 sc = 4 inches, 16 rows = 4 inches
    
    Finished Size:
    8 inches wide by 60 inches long
    
    Abbreviations:
    ch = chain, sc = single crochet, dc = double crochet
    
    Instructions:
    Ch 32.
    Row 1: Sc in 2nd ch from hook and each ch across. (31 sc)
    Row 2-240: Ch 1, turn, sc in each st across. (31 sc)
    
    Fasten off. Weave in ends.
    
    Notes:
    This is a beginner-friendly pattern using basic stitches.
    Perfect for practicing consistent tension.
    """
    
    print("\n📝 Summarizing pattern...")
    summary = summarizer.summarize_pattern(test_pattern)
    
    print(f"\n  Lines: {summary['total_lines']}")
    print(f"  Words: {summary['word_count']}")
    print(f"  Difficulty: {summary['difficulty_estimate']}")
    
    print(f"\n  Sections found:")
    for section in summary['sections']:
        print(f"    • {section}")
    
    print(f"\n  Stitches used: {', '.join(summary['stitches'])}")
    
    print(f"\n  Measurements: {summary['measurements']}")
    
    print(f"\n  Materials: {summary['materials']}")
    
    print(f"\n  Summary: {summary['summary']}")
    
    print(f"\n  Quick Reference:")
    print(summary['quick_reference'])
    
    # Stats
    print(f"\n📊 Pattern Stats:")
    stats = summarizer.extract_pattern_stats(test_pattern)
    print(f"  Time estimate: {stats['estimated_time_minutes']} minutes")
    print(f"  Complexity: {stats['complexity']}")
    
    print(f"\n  AI Pattern Summarizer Complete! 📋")
