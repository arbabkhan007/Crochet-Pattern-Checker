"""
2D Preview renderer for crochet patterns.

Creates a detailed visual preview showing:
- Stitch-by-stitch layout
- Color coding for stitch types
- Error highlighting
- Round/row labels
"""

from __future__ import annotations

import math
from typing import Optional

from ..model.pattern import ConstructionType, Pattern
from ..model.stitch import StitchType
from .stitch_diagram import STITCH_COLORS, _escape_xml, generate_circle_diagram, generate_stitch_count_chart


class Render2D:
    """Renders a 2D visual preview of a crochet pattern."""

    def __init__(self, width: int = 800, height: int = 800) -> None:
        self.width = width
        self.height = height

    def render(self, pattern: Pattern, validation_report=None) -> str:
        """
        Render a complete 2D preview as SVG.

        Includes:
        - Circle diagram
        - Stitch count chart
        - Pattern summary
        - Error highlights (if validation report provided)
        """
        elements = []

        # Main container
        total_height = self.height + 350
        elements.append(
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'viewBox="0 0 {self.width} {total_height}" '
            f'width="{self.width}" height="{total_height}">'
        )
        elements.append(f'<rect width="{self.width}" height="{total_height}" fill="white"/>')

        # Title
        title = pattern.metadata.title or "Crochet Pattern Preview"
        elements.append(
            f'<text x="{self.width/2}" y="30" text-anchor="middle" '
            f'font-family="Arial" font-size="20" font-weight="bold" '
            f'fill="#2C3E50">{_escape_xml(title)}</text>'
        )

        # Construction type
        elements.append(
            f'<text x="{self.width/2}" y="50" text-anchor="middle" '
            f'font-family="Arial" font-size="12" fill="#7F8C8D">'
            f'Construction: {pattern.construction.value}</text>'
        )

        # Circle diagram (top half)
        diagram_svg = generate_circle_diagram(pattern, width=self.width, height=self.height - 60)
        # Extract inner SVG content (skip the outer svg tags)
        inner = "\n".join(diagram_svg.split("\n")[2:-1])  # Skip svg open/close
        elements.append(f'<g transform="translate(0, 60)">')
        elements.append(inner)
        elements.append('</g>')

        # Stitch count chart (bottom)
        chart_y = self.height + 20
        chart_svg = generate_stitch_count_chart(pattern, width=self.width - 40, height=250)
        inner_chart = "\n".join(chart_svg.split("\n")[2:-1])
        elements.append(f'<g transform="translate(20, {chart_y})">')
        elements.append(inner_chart)
        elements.append('</g>')

        # Validation summary (if available)
        if validation_report:
            summary_y = chart_y + 270
            elements.append(self._render_validation_summary(validation_report, summary_y))

        # Pattern text listing
        text_y = (chart_y + 270 + 80) if validation_report else (chart_y + 270)
        elements.append(self._render_pattern_text(pattern, text_y))

        elements.append("</svg>")
        return "\n".join(elements)

    def _render_validation_summary(self, report, y: int) -> str:
        """Render validation summary section."""
        lines = []
        lines.append(
            f'<text x="30" y="{y}" font-family="Arial" font-size="14" '
            f'font-weight="bold" fill="#2C3E50">Validation Summary</text>'
        )

        status = report.overall_status
        score = report.score
        color = {
            "PASS": "#27AE60",
            "PASS_WITH_WARNINGS": "#F39C12",
            "NEEDS_REVIEW": "#E67E22",
            "ERROR": "#E74C3C",
        }.get(status, "#95A5A6")

        lines.append(
            f'<rect x="30" y="{y+10}" width="200" height="30" rx="5" '
            f'fill="{color}" opacity="0.15" stroke="{color}" stroke-width="1"/>'
        )
        lines.append(
            f'<text x="130" y="{y+30}" text-anchor="middle" font-family="Arial" '
            f'font-size="12" font-weight="bold" fill="{color}">'
            f'{status} | Score: {score}/100</text>'
        )

        # Error/warning counts
        ex = 260
        lines.append(
            f'<text x="{ex}" y="{y+30}" font-family="Arial" font-size="11" fill="#555">'
            f'Errors: {len(report.errors)} | Warnings: {len(report.warnings)}</text>'
        )

        # List first few errors
        ey = y + 50
        for f in report.errors[:3]:
            lines.append(
                f'<text x="50" y="{ey}" font-family="Arial" font-size="10" fill="#E74C3C">'
                f'✗ [{f.location}] {_escape_xml(f.message[:70])}</text>'
            )
            ey += 15

        return "\n".join(lines)

    def _render_pattern_text(self, pattern: Pattern, y: int) -> str:
        """Render the pattern text listing."""
        lines = []
        lines.append(
            f'<text x="30" y="{y}" font-family="Arial" font-size="14" '
            f'font-weight="bold" fill="#2C3E50">Pattern Instructions</text>'
        )

        items = pattern.rounds or pattern.rows
        ty = y + 20
        for i, r in enumerate(items[:20]):  # Limit to 20 rounds for display
            num = r.round_number if hasattr(r, 'round_number') else r.row_number
            label = "Round" if hasattr(r, 'round_number') else "Row"
            text = _escape_xml(r.source_text[:80])
            lines.append(
                f'<text x="50" y="{ty}" font-family="monospace" font-size="10" fill="#444">'
                f'{label} {num}: {text}</text>'
            )
            ty += 16

        if len(items) > 20:
            lines.append(
                f'<text x="50" y="{ty}" font-family="Arial" font-size="10" fill="#999">'
                f'... and {len(items) - 20} more rounds</text>'
            )

        return "\n".join(lines)


def render_2d_preview(pattern: Pattern, validation_report=None) -> str:
    """Generate a complete 2D preview SVG."""
    renderer = Render2D()
    return renderer.render(pattern, validation_report)
