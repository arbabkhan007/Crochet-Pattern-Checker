"""
Pattern Error Detector - Detect common pattern errors
"""


class PatternErrorDetector:
    def __init__(self):
        self.error_rules = {
            "missing_turning_chain": {
                "severity": "medium",
                "fix": "Add turning chain at start of row",
            },
            "stitch_count_mismatch": {
                "severity": "high",
                "fix": "Check stitch count at end of each row",
            },
            "inconsistent_abbreviations": {
                "severity": "low",
                "fix": "Use consistent abbreviations",
            },
            "missing_repeat_instructions": {
                "severity": "medium",
                "fix": "Add clear repeat instructions",
            },
        }

    def detect_errors(self, pattern_text: str) -> dict:
        """Detect errors in pattern"""
        lines = pattern_text.strip().split("\n")
        errors = []
        warnings = []

        for i, line in enumerate(lines, 1):
            line_lower = line.lower()

            # Check for turning chains
            if i > 1 and "turn" in line_lower:
                if "ch" not in line_lower and "chain" not in line_lower:
                    errors.append(
                        {
                            "line": i,
                            "type": "missing_turning_chain",
                            "severity": "medium",
                            "message": "Missing turning chain after turn",
                        }
                    )

            # Check for unclear repeats
            if "rep" in line_lower or "repeat" in line_lower:
                if "times" not in line_lower and "around" not in line_lower:
                    warnings.append(
                        {
                            "line": i,
                            "type": "unclear_repeat",
                            "severity": "low",
                            "message": "Unclear repeat instruction",
                        }
                    )

        return {
            "errors": errors,
            "warnings": warnings,
            "total_issues": len(errors) + len(warnings),
            "pattern_quality": "good" if len(errors) == 0 else "needs_fixes",
        }

    def get_fixes(self, errors: list) -> list:
        """Get recommended fixes"""
        fixes = []
        for error in errors:
            rule = self.error_rules.get(error["type"], {})
            fixes.append(
                {
                    "line": error["line"],
                    "issue": error["message"],
                    "fix": rule.get("fix", "Review pattern instructions"),
                }
            )
        return fixes


if __name__ == "__main__":
    print("🔍 Pattern Error Detector")
    print("=" * 60)

    detector = PatternErrorDetector()

    pattern = """Row 1: sc in 2nd ch from hook
Row 2: turn, sc across
Row 3: turn, sc across"""

    print("\n🔍 Detecting errors...")
    result = detector.detect_errors(pattern)

    print(f"\nTotal issues: {result['total_issues']}")
    print(f"Pattern quality: {result['pattern_quality']}")

    if result["errors"]:
        print("\n❌ Errors found:")
        for error in result["errors"]:
            print(f"  Line {error['line']}: {error['message']}")

    if result["warnings"]:
        print("\n⚠️ Warnings:")
        for warning in result["warnings"]:
            print(f"  Line {warning['line']}: {warning['message']}")

    fixes = detector.get_fixes(result["errors"])
    if fixes:
        print("\n💡 Recommended fixes:")
        for fix in fixes:
            print(f"  Line {fix['line']}: {fix['fix']}")

    print("\n✨ Detection complete!")
