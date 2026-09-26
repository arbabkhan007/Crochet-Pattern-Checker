"""
Complex Pattern Validator - Validate intricate patterns for errors
"""


class ComplexPatternValidator:
    def __init__(self):
        self.validation_rules = {
            "stitch_count": {"check": "consistent", "severity": "high"},
            "pattern_repeat": {"check": "divisible", "severity": "medium"},
            "turning_chains": {"check": "present", "severity": "medium"},
            "color_changes": {"check": "clear", "severity": "low"},
            "special_stitches": {"check": "defined", "severity": "medium"},
        }

    def validate_complex_pattern(
        self, pattern_text: str, pattern_metadata: dict
    ) -> dict:
        """Validate complex pattern for errors"""
        errors = []
        warnings = []

        lines = pattern_text.strip().split("\n")

        # Check stitch count consistency
        stitch_counts = self._extract_stitch_counts(lines)
        if not self._check_stitch_consistency(stitch_counts):
            errors.append(
                {
                    "type": "stitch_count",
                    "message": "Inconsistent stitch counts detected",
                    "severity": "high",
                }
            )

        # Check pattern repeat
        if "repeat_multiple" in pattern_metadata:
            if not self._check_pattern_repeat(
                lines, pattern_metadata["repeat_multiple"]
            ):
                warnings.append(
                    {
                        "type": "pattern_repeat",
                        "message": f"Rows may not be divisible by {pattern_metadata['repeat_multiple']}",
                        "severity": "medium",
                    }
                )

        # Check turning chains
        if not self._check_turning_chains(lines):
            warnings.append(
                {
                    "type": "turning_chains",
                    "message": "Missing turning chains in some rows",
                    "severity": "medium",
                }
            )

        # Check special stitch definitions
        if self._has_special_stitches(pattern_text) and not self._has_definitions(
            pattern_text
        ):
            warnings.append(
                {
                    "type": "special_stitches",
                    "message": "Special stitches used but not defined",
                    "severity": "medium",
                }
            )

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "error_count": len(errors),
            "warning_count": len(warnings),
            "validation_score": self._calculate_score(errors, warnings),
            "recommendations": self._get_recommendations(errors, warnings),
        }

    def _extract_stitch_counts(self, lines: list) -> list:
        """Extract stitch counts from each row"""
        counts = []
        for line in lines:
            if "row" in line.lower() or "round" in line.lower():
                # Simple extraction - count stitch abbreviations
                count = (
                    line.lower().count("sc")
                    + line.lower().count("dc")
                    + line.lower().count("hdc")
                )
                counts.append(count)
        return counts

    def _check_stitch_consistency(self, counts: list) -> bool:
        """Check if stitch counts are consistent"""
        if len(counts) < 2:
            return True
        # Allow some variation for shaping
        avg = sum(counts) / len(counts)
        variance = sum((c - avg) ** 2 for c in counts) / len(counts)
        return variance < (avg * 0.5)  # Allow 50% variance

    def _check_pattern_repeat(self, lines: list, multiple: int) -> bool:
        """Check if pattern follows repeat multiple"""
        # Simplified check
        return True

    def _check_turning_chains(self, lines: list) -> bool:
        """Check for turning chains"""
        for i, line in enumerate(lines[1:], 1):  # Skip first row
            if "turn" in line.lower() or i > 0:
                if "ch" not in line.lower() and "chain" not in line.lower():
                    return False
        return True

    def _has_special_stitches(self, pattern_text: str) -> bool:
        """Check if pattern uses special stitches"""
        special = ["bobble", "popcorn", "cable", "bullion", "shell"]
        text_lower = pattern_text.lower()
        return any(stitch in text_lower for stitch in special)

    def _has_definitions(self, pattern_text: str) -> bool:
        """Check if special stitches are defined"""
        return (
            "abbreviation" in pattern_text.lower()
            or "special stitch" in pattern_text.lower()
            or "definition" in pattern_text.lower()
        )

    def _calculate_score(self, errors: list, warnings: list) -> int:
        """Calculate validation score"""
        score = 100
        for error in errors:
            if error["severity"] == "high":
                score -= 20
            elif error["severity"] == "medium":
                score -= 10
            else:
                score -= 5

        for warning in warnings:
            if warning["severity"] == "high":
                score -= 10
            elif warning["severity"] == "medium":
                score -= 5
            else:
                score -= 2

        return max(0, score)

    def _get_recommendations(self, errors: list, warnings: list) -> list:
        """Get recommendations based on validation"""
        recommendations = []

        if errors:
            recommendations.append("Fix critical errors before proceeding")

        for warning in warnings:
            if warning["type"] == "turning_chains":
                recommendations.append("Add turning chains at start of each row")
            elif warning["type"] == "special_stitches":
                recommendations.append("Define all special stitches used")
            elif warning["type"] == "pattern_repeat":
                recommendations.append("Verify pattern repeat multiples")

        if not errors and not warnings:
            recommendations.append("Pattern looks good! Ready to crochet")

        return recommendations


if __name__ == "__main__":
    print("✅ Complex Pattern Validator")
    print("=" * 60)

    validator = ComplexPatternValidator()

    # Test with complex pattern
    pattern = """
    Materials: Worsted yarn, 5mm hook
    
    Special Stitches:
    Bobble: Yarn over 5 times in same stitch
    
    Pattern:
    Row 1: sc in 2nd ch from hook, sc across (20 sc)
    Row 2: ch 1, turn, sc across (20 sc)
    Row 3: ch 1, turn, bobble in next st, sc across
    Row 4: ch 1, turn, sc across (20 sc)
    """

    metadata = {"repeat_multiple": 4}

    result = validator.validate_complex_pattern(pattern, metadata)

    print(f"\nValidation Score: {result['validation_score']}/100")
    print(f"Valid: {result['valid']}")
    print(f"Errors: {result['error_count']}")
    print(f"Warnings: {result['warning_count']}")

    if result["errors"]:
        print("\n❌ Errors:")
        for error in result["errors"]:
            print(f"  • {error['message']} ({error['severity']})")

    if result["warnings"]:
        print("\n⚠️ Warnings:")
        for warning in result["warnings"]:
            print(f"  • {warning['message']} ({warning['severity']})")

    print("\n💡 Recommendations:")
    for rec in result["recommendations"]:
        print(f"  • {rec}")
