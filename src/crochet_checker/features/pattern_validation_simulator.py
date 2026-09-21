"""
Pattern Validation Simulator - Validate patterns through simulation
"""

class PatternValidationSimulator:
    def __init__(self):
        self.validation_rules = {
            "stitch_count_consistency": True,
            "turning_chains": True,
            "increase_decrease_balance": True,
        }
    
    def validate_pattern(self, pattern_text: str) -> dict:
        """Validate pattern through simulation"""
        lines = pattern_text.strip().split('\n')
        errors = []
        warnings = []
        
        prev_stitch_count = 0
        
        for i, line in enumerate(lines, 1):
            line_lower = line.lower()
            
            # Check for turning chains
            if i > 1 and "turn" in line_lower and "ch" not in line_lower:
                warnings.append(f"Row {i}: Missing turning chain")
            
            # Simulate stitch count
            current_stitches = self._count_stitches(line)
            
            # Check for drastic changes
            if prev_stitch_count > 0:
                change = abs(current_stitches - prev_stitch_count)
                if change > prev_stitch_count * 0.5:
                    warnings.append(f"Row {i}: Large stitch count change ({change} stitches)")
            
            prev_stitch_count = current_stitches
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "score": 100 - len(errors) * 10 - len(warnings) * 5,
            "recommendation": "Pattern is valid" if len(errors) == 0 else "Fix errors before testing"
        }
    
    def _count_stitches(self, instruction: str) -> int:
        """Count stitches in instruction"""
        import re
        count = 0
        for stitch in ["sc", "dc", "hdc", "tr"]:
            matches = re.findall(r'(\d+)?\s*' + stitch, instruction.lower())
            for match in matches:
                count += int(match) if match else 1
        return count

if __name__ == "__main__":
    print("✅ Pattern Validation Simulator")
    print("=" * 60)
    
    validator = PatternValidationSimulator()
    
    pattern = """Row 1: sc in 2nd ch from hook
Row 2: ch 1, turn, sc across
Row 3: ch 1, turn, sc across"""
    
    print("\n🔍 Validating pattern...")
    result = validator.validate_pattern(pattern)
    
    print(f"\nValid: {result['valid']}")
    print(f"Score: {result['score']}/100")
    
    if result['errors']:
        print("\n❌ Errors:")
        for error in result['errors']:
            print(f"  • {error}")
    
    if result['warnings']:
        print("\n⚠️ Warnings:")
        for warning in result['warnings']:
            print(f"  • {warning}")
    
    print(f"\n💡 {result['recommendation']}")
    print("\n✨ Validation complete!")
