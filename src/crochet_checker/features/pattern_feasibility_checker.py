"""
Pattern Feasibility Checker - Check if pattern is feasible
"""

class PatternFeasibilityChecker:
    def __init__(self):
        self.feasibility_rules = {
            "max_stitches_per_row": 200,
            "max_rows": 500,
            "min_stitches_per_row": 3,
        }
    
    def check_feasibility(self, pattern_text: str) -> dict:
        """Check if pattern is feasible to make"""
        lines = pattern_text.strip().split('\n')
        issues = []
        
        if len(lines) > self.feasibility_rules["max_rows"]:
            issues.append(f"Too many rows ({len(lines)} > {self.feasibility_rules['max_rows']})")
        
        for i, line in enumerate(lines, 1):
            stitch_count = line.lower().count("sc") + line.lower().count("dc") + line.lower().count("hdc")
            
            if stitch_count > self.feasibility_rules["max_stitches_per_row"]:
                issues.append(f"Row {i}: Too many stitches ({stitch_count})")
            
            if stitch_count < self.feasibility_rules["min_stitches_per_row"] and stitch_count > 0:
                issues.append(f"Row {i}: Too few stitches ({stitch_count})")
        
        return {
            "feasible": len(issues) == 0,
            "issues": issues,
            "total_rows": len(lines),
            "estimated_time_hours": len(lines) * 0.5,
            "recommendation": "Pattern is feasible" if len(issues) == 0 else "Review issues"
        }

if __name__ == "__main__":
    print("✅ Pattern Feasibility Checker")
    print("=" * 60)
    
    checker = PatternFeasibilityChecker()
    
    pattern = """Row 1: 10 sc
Row 2: 15 sc
Row 3: 20 sc"""
    
    print("\n🔍 Checking feasibility...")
    result = checker.check_feasibility(pattern)
    
    print(f"\nFeasible: {result['feasible']}")
    print(f"Total rows: {result['total_rows']}")
    print(f"Estimated time: {result['estimated_time_hours']:.1f} hours")
    
    if result['issues']:
        print("\n⚠️ Issues:")
        for issue in result['issues']:
            print(f"  • {issue}")
    
    print(f"\n💡 {result['recommendation']}")
    print("\n✨ Check complete!")
