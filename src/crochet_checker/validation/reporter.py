"""
Reporter - Generates structured CLI / JSON output with line-by-line feedback
"""

import json
from datetime import datetime

from .validator import ValidationError, ValidationResult


class PatternReporter:
    """Generates reports from validation results"""

    def __init__(self):
        self.output_formats = ["text", "json", "markdown"]

    def generate_report(self, result: ValidationResult, format: str = "text") -> str:
        """Generate a report in the specified format.

        Accepts a ValidationResult, or a raw pattern string (legacy callers) —
        in the latter case the pattern is validated first.
        """
        if isinstance(result, str):
            from .validator import PatternValidator

            result = PatternValidator().validate(result)
        if format == "json":
            return self._generate_json_report(result)
        elif format == "markdown":
            return self._generate_markdown_report(result)
        else:
            return self._generate_text_report(result)

    def _generate_text_report(self, result: ValidationResult) -> str:
        """Generate human-readable text report"""
        lines = []

        lines.append("=" * 70)
        lines.append("CROCHET PATTERN VALIDATION REPORT")
        lines.append("=" * 70)
        lines.append("")

        # Summary
        lines.append("SUMMARY")
        lines.append("-" * 70)
        lines.append(f"Status: {'✅ VALID' if result.is_valid else '❌ INVALID'}")
        lines.append(f"Total Pieces: {result.piece_count}")
        lines.append(f"Total Stitches: {result.total_stitches}")
        lines.append(f"Errors: {len(result.errors)}")
        lines.append(f"Warnings: {len(result.warnings)}")
        lines.append(f"Execution Time: {result.execution_time:.3f}s")
        lines.append("")

        # Stitch counts
        if result.stitch_counts:
            lines.append("STITCH COUNTS BY ROUND")
            lines.append("-" * 70)
            for (piece, round_num), count in sorted(result.stitch_counts.items()):
                lines.append(f"  {piece} - Round {round_num}: {count} stitches")
            lines.append("")

        # Errors
        if result.errors:
            lines.append("ERRORS")
            lines.append("-" * 70)
            for error in result.errors:
                location = self._format_location(error)
                lines.append(f"  ❌ {location}")
                lines.append(f"     {error.message}")
                lines.append("")

        # Warnings
        if result.warnings:
            lines.append("WARNINGS")
            lines.append("-" * 70)
            for warning in result.warnings:
                location = self._format_location(warning)
                lines.append(f"  ⚠️  {location}")
                lines.append(f"     {warning.message}")
                lines.append("")

        # Footer
        lines.append("=" * 70)
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("=" * 70)

        return "\n".join(lines)

    def _generate_json_report(self, result: ValidationResult) -> str:
        """Generate JSON report"""
        report = {
            "validation": {
                "status": "valid" if result.is_valid else "invalid",
                "timestamp": datetime.now().isoformat(),
                "execution_time": result.execution_time,
            },
            "summary": {
                "total_pieces": result.piece_count,
                "total_stitches": result.total_stitches,
                "error_count": len(result.errors),
                "warning_count": len(result.warnings),
            },
            "stitch_counts": {
                f"{piece}_round_{round_num}": count
                for (piece, round_num), count in result.stitch_counts.items()
            },
            "errors": [
                {
                    "line": error.line_number,
                    "message": error.message,
                    "piece": error.piece_name,
                    "round": error.round_number,
                    "severity": error.severity,
                }
                for error in result.errors
            ],
            "warnings": [
                {
                    "line": warning.line_number,
                    "message": warning.message,
                    "piece": warning.piece_name,
                    "round": warning.round_number,
                    "severity": warning.severity,
                }
                for warning in result.warnings
            ],
        }

        return json.dumps(report, indent=2)

    def _generate_markdown_report(self, result: ValidationResult) -> str:
        """Generate Markdown report"""
        lines = []

        lines.append("# Crochet Pattern Validation Report")
        lines.append("")
        lines.append(f"**Status:** {'✅ Valid' if result.is_valid else '❌ Invalid'}")
        lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")

        # Summary
        lines.append("## Summary")
        lines.append("")
        lines.append(f"- **Total Pieces:** {result.piece_count}")
        lines.append(f"- **Total Stitches:** {result.total_stitches}")
        lines.append(f"- **Errors:** {len(result.errors)}")
        lines.append(f"- **Warnings:** {len(result.warnings)}")
        lines.append(f"- **Execution Time:** {result.execution_time:.3f}s")
        lines.append("")

        # Stitch counts
        if result.stitch_counts:
            lines.append("## Stitch Counts")
            lines.append("")
            lines.append("| Piece | Round | Stitch Count |")
            lines.append("|-------|-------|--------------|")
            for (piece, round_num), count in sorted(result.stitch_counts.items()):
                lines.append(f"| {piece} | {round_num} | {count} |")
            lines.append("")

        # Errors
        if result.errors:
            lines.append("## Errors")
            lines.append("")
            for error in result.errors:
                location = self._format_location(error)
                lines.append(f"### ❌ {location}")
                lines.append("")
                lines.append(f"{error.message}")
                lines.append("")

        # Warnings
        if result.warnings:
            lines.append("## Warnings")
            lines.append("")
            for warning in result.warnings:
                location = self._format_location(warning)
                lines.append(f"### ⚠️ {location}")
                lines.append("")
                lines.append(f"{warning.message}")
                lines.append("")

        return "\n".join(lines)

    def _format_location(self, error: ValidationError) -> str:
        """Format error location"""
        parts = []

        if error.piece_name:
            parts.append(f"Piece: {error.piece_name}")

        if error.round_number > 0:
            parts.append(f"Round {error.round_number}")

        if error.line_number > 0:
            parts.append(f"Line {error.line_number}")

        return " | ".join(parts) if parts else "Unknown location"

    def print_report(self, result: ValidationResult, format: str = "text"):
        """Print report to console"""
        print(self.generate_report(result, format))

    def save_report(
        self, result: ValidationResult, filename: str, format: str = "text"
    ):
        """Save report to file"""
        report = self.generate_report(result, format)

        with open(filename, "w", encoding="utf-8") as f:
            f.write(report)


if __name__ == "__main__":
    print("📊 Pattern Reporter")
    print("=" * 60)

    from .validator import PatternValidator

    # Create a test pattern
    test_pattern = """
# Test Pattern

## Piece 1 (worked in rounds)
Round 1: 6 sc in magic ring (6)
Round 2: inc in each st around (12)
Round 3: *sc 1, inc* rep around (18)
"""

    # Validate
    validator = PatternValidator()
    result = validator.validate(test_pattern)

    # Generate reports
    reporter = PatternReporter()

    print("\n📄 Text Report:")
    print(reporter.generate_report(result, "text"))

    print("\n📋 JSON Report (first 500 chars):")
    json_report = reporter.generate_report(result, "json")
    print(json_report[:500] + "...")

    print("\n📝 Markdown Report (first 500 chars):")
    md_report = reporter.generate_report(result, "markdown")
    print(md_report[:500] + "...")

    print("\n✅ Pattern Reporter working!")
