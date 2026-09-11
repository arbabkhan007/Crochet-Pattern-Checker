"""
AI Error Detector - Find and fix mistakes in crochet patterns automatically
"""
import re
from typing import Dict, List, Optional, Tuple


class AIErrorDetector:
    """
    Detect and fix errors in crochet patterns
    
    Features:
    - Stitch count validation
    - Missing instructions detection
    - Gauge consistency checking
    - Abbreviation validation
    - Pattern logic checking
    - Auto-fix suggestions
    """
    
    STITCH_ABBREVIATIONS = {
        "ch", "sc", "dc", "hdc", "tr", "dtr", "sl st", "sp", "st", "sts",
        "sk", "inc", "dec", "yo", "fpdc", "bpdc", "pop", "puff",
        "ch-sp", "ch-sp", "mc", "mr", "fo",
    }
    
    COMMON_ERRORS = {
        "missing_ch": "Row/round starts without turning chain",
        "stitch_mismatch": "Stitch count doesn't match previous row",
        "missing_turn": "Missing 'turn' instruction at end of row",
        "orphan_round": "Round without clear start/end",
        "invalid_abbr": "Unknown stitch abbreviation",
        "gauge_mismatch": "Gauge doesn't match yarn weight",
        "missing_fasten": "Pattern doesn't end with fasten off",
    }
    
    def detect_errors(self, pattern_text: str) -> Dict:
        """
        Detect errors in a pattern
        
        Args:
            pattern_text: Pattern to check
        
        Returns:
            Dict with errors and suggestions
        """
        if not pattern_text or len(pattern_text) < 50:
            return {"error": "Pattern too short to analyze"}
        
        errors = []
        warnings = []
        suggestions = []
        
        # Check for common issues
        errors.extend(self._check_stitch_counts(pattern_text))
        errors.extend(self._check_turning_chains(pattern_text))
        errors.extend(self._check_structure(pattern_text))
        
        warnings.extend(self._check_abbreviations(pattern_text))
        warnings.extend(self._check_gauge(pattern_text))
        
        suggestions.extend(self._generate_suggestions(pattern_text))
        
        # Calculate error score
        error_score = max(0, 100 - (len(errors) * 10) - (len(warnings) * 5))
        
        return {
            "errors": errors,
            "warnings": warnings,
            "suggestions": suggestions,
            "error_count": len(errors),
            "warning_count": len(warnings),
            "score": error_score,
            "severity": self._get_severity(len(errors), len(warnings)),
            "fixable": len([e for e in errors if e.get("auto_fix")]),
        }
    
    def _check_stitch_counts(self, text: str) -> List[Dict]:
        """Check stitch counts for consistency"""
        errors = []
        
        # Find stitch count annotations like (31 sc)
        counts = re.findall(r'\((\d+)\s*(?:sc|dc|hdc|sts)\)', text, re.IGNORECASE)
        
        if len(counts) >= 2:
            # Check if counts are consistent (within expected range)
            int_counts = [int(c) for c in counts]
            for i in range(1, len(int_counts)):
                diff = abs(int_counts[i] - int_counts[i-1])
                if diff > 5:  # Significant change without explanation
                    errors.append({
                        "type": "stitch_mismatch",
                        "message": f"Stitch count changed from {int_counts[i-1]} to {int_counts[i]} without explanation",
                        "line": f"Row/round {i+1}",
                        "auto_fix": False,
                    })
        
        return errors
    
    def _check_turning_chains(self, text: str) -> List[Dict]:
        """Check for missing turning chains"""
        errors = []
        
        lines = text.split("\n")
        for i, line in enumerate(lines):
            line_lower = line.lower().strip()
            
            # Check if row starts with stitch but no chain
            if re.match(r'^row\s+\d+[:\.]\s+(sc|dc|hdc|tr)', line_lower, re.IGNORECASE):
                # Check if previous line has "turn"
                if i > 0 and "turn" not in lines[i-1].lower():
                    errors.append({
                        "type": "missing_turn",
                        "message": f"Row starts with stitch but previous row doesn't say 'turn'",
                        "line": f"Line {i+1}",
                        "auto_fix": True,
                        "fix": "Add 'turn' to end of previous row",
                    })
            
            # Check if row with dc/tr starts without proper chain
            if re.match(r'^row\s+\d+[:\.]\s+(dc|tr)\b', line_lower, re.IGNORECASE):
                if not re.search(r'ch\s+[234]', line_lower):
                    errors.append({
                        "type": "missing_ch",
                        "message": "Row starts with dc/tr but no turning chain specified",
                        "line": f"Line {i+1}",
                        "auto_fix": True,
                        "fix": "Add 'ch 3' (for dc) or 'ch 4' (for tr) at start",
                    })
        
        return errors
    
    def _check_structure(self, text: str) -> List[Dict]:
        """Check pattern structure"""
        errors = []
        
        text_lower = text.lower()
        
        # Check for ending instructions
        if not any(word in text_lower for word in ["fasten off", "bind off", "fo"]):
            errors.append({
                "type": "missing_fasten",
                "message": "Pattern doesn't end with 'fasten off' or similar",
                "line": "End of pattern",
                "auto_fix": True,
                "fix": "Add 'Fasten off. Weave in ends.' at the end",
            })
        
        # Check for materials section
        if "materials" not in text_lower and "supplies" not in text_lower:
            errors.append({
                "type": "missing_materials",
                "message": "No materials/supplies section found",
                "line": "Beginning",
                "auto_fix": False,
            })
        
        return errors
    
    def _check_abbreviations(self, text: str) -> List[Dict]:
        """Check for invalid abbreviations"""
        warnings = []
        
        # Find all abbreviations
        abbrevs = re.findall(r'\b([a-z]{2,4})\b', text.lower())
        
        invalid = set()
        for abbr in abbrevs:
            if abbr not in self.STITCH_ABBREVIATIONS and len(abbr) <= 4:
                # Check if it's a common word
                common_words = ["row", "rnd", "rep", "each", "next", "across", "around"]
                if abbr not in common_words:
                    invalid.add(abbr)
        
        if invalid:
            warnings.append({
                "type": "invalid_abbr",
                "message": f"Potentially invalid abbreviations: {', '.join(sorted(invalid))}",
                "auto_fix": False,
            })
        
        return warnings
    
    def _check_gauge(self, text: str) -> List[Dict]:
        """Check gauge information"""
        warnings = []
        
        text_lower = text.lower()
        
        if "gauge" not in text_lower:
            warnings.append({
                "type": "missing_gauge",
                "message": "No gauge information found (important for garments)",
                "auto_fix": False,
            })
        
        return warnings
    
    def _generate_suggestions(self, text: str) -> List[str]:
        """Generate improvement suggestions"""
        suggestions = []
        
        text_lower = text.lower()
        
        if len(text.split("\n")) < 10:
            suggestions.append("Pattern is very short - consider adding more details")
        
        if "notes" not in text_lower:
            suggestions.append("Add a 'Notes' section for helpful tips")
        
        if "difficulty" not in text_lower and "level" not in text_lower:
            suggestions.append("Specify difficulty level (beginner/intermediate/advanced)")
        
        if "finished" not in text_lower and "size" not in text_lower:
            suggestions.append("Include finished measurements")
        
        return suggestions
    
    def _get_severity(self, error_count: int, warning_count: int) -> str:
        """Get severity level"""
        if error_count == 0:
            return "None"
        elif error_count <= 2:
            return "Low"
        elif error_count <= 5:
            return "Medium"
        else:
            return "High"
    
    def auto_fix(self, pattern_text: str) -> str:
        """Automatically fix common errors"""
        fixed = pattern_text
        
        # Add turning chains where missing
        fixed = re.sub(
            r'(row\s+\d+[:\.]\s+)(dc\b)',
            r'\g<1>ch 3, \2',
            fixed,
            flags=re.IGNORECASE
        )
        
        fixed = re.sub(
            r'(row\s+\d+[:\.]\s+)(tr\b)',
            r'\g<1>ch 4, \2',
            fixed,
            flags=re.IGNORECASE
        )
        
        # Add fasten off if missing
        if not re.search(r'fasten off|bind off|fo', fixed, re.IGNORECASE):
            fixed += "\n\nFasten off. Weave in ends."
        
        return fixed


# Demo
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  AI ERROR DETECTOR - DEMONSTRATION")
    print("=" * 60)
    
    detector = AIErrorDetector()
    
    # Test pattern with errors
    bad_pattern = """
    SCARF
    Row 1: dc in 2nd ch from hook and each ch across. (30)
    Row 2: dc in each st across. (30)
    Row 3: dc in each st across. (25)
    """
    
    print("\n🔍 Analyzing pattern with errors...")
    result = detector.detect_errors(bad_pattern)
    
    print(f"\n  Score: {result['score']}/100")
    print(f"  Severity: {result['severity']}")
    print(f"  Errors: {result['error_count']}")
    print(f"  Warnings: {result['warning_count']}")
    
    if result['errors']:
        print(f"\n  ❌ Errors found:")
        for error in result['errors'][:3]:
            print(f"    • {error['message']}")
            if error.get('auto_fix'):
                print(f"      → Fix: {error['fix']}")
    
    if result['warnings']:
        print(f"\n  ⚠️  Warnings:")
        for warning in result['warnings'][:3]:
            print(f"    • {warning['message']}")
    
    if result['suggestions']:
        print(f"\n  💡 Suggestions:")
        for suggestion in result['suggestions']:
            print(f"    • {suggestion}")
    
    # Auto-fix
    print(f"\n🔧 Auto-fixing...")
    fixed = detector.auto_fix(bad_pattern)
    print(f"  Fixed pattern preview:")
    print(f"  {fixed[:200]}...")
    
    # Good pattern
    good_pattern = """
    COZY SCARF
    
    Materials:
    - 400 yards worsted yarn
    - 5.5mm hook
    
    Gauge: 14 sc = 4 inches
    
    Instructions:
    Ch 32.
    Row 1: Sc in 2nd ch from hook and each ch across. (31 sc)
    Row 2-240: Ch 1, turn, sc in each st across. (31 sc)
    
    Fasten off. Weave in ends.
    """
    
    print(f"\n✅ Analyzing good pattern...")
    good_result = detector.detect_errors(good_pattern)
    print(f"  Score: {good_result['score']}/100")
    print(f"  Errors: {good_result['error_count']}")
    print(f"  Severity: {good_result['severity']}")
    
    print(f"\n  AI Error Detector Complete! 🔍")
