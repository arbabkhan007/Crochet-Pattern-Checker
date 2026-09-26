"""
SVG-based stitch diagram generator.

Creates visual representations of crochet patterns using SVG,
showing stitch placement, round structure, and construction.
"""

from __future__ import annotations

import math
from typing import Optional

from ..model.pattern import ConstructionType, Pattern
from ..model.stitch import StitchType
from .measurements import MeasurementEngine, PatternMeasurements, StitchDimensions


# Colors for different stitch types
STITCH_COLORS = {
    StitchType.SINGLE_CROCHET: "#4A90D9",  # Blue
    StitchType.DOUBLE_CROCHET: "#7B68EE",  # Purple
    StitchType.HALF_DOUBLE_CROCHET: "#50C878",  # Green
    StitchType.TREBLE_CROCHET: "#FF8C00",  # Orange
    StitchType.CHAIN: "#999999",  # Gray
    StitchType.SLIP_STITCH: "#666666",  # Dark gray
    StitchType.INCREASE: "#2ECC71",  # Bright green
    StitchType.DECREASE: "#E74C3C",  # Red
    StitchType.MAGIC_RING: "#F39C12",  # Gold
    StitchType.SKIP: "#BDC3C7",  # Light gray
}

ERROR_COLOR = "#FF0000"
WARNING_COLOR = "#FFA500"
SUCCESS_COLOR = "#27AE60"
BACKGROUND_COLOR = "#FFFFFF"
GRID_COLOR = "#F0F0F0"


class SVGDiagram:
    """Generates SVG diagrams for crochet patterns."""

    def __init__(
        self,
        width: int = 600,
        height: int = 600,
        stitch_dims: Optional[StitchDimensions] = None,
    ) -> None:
        self.width = width
        self.height = height
        self.dims = stitch_dims or StitchDimensions.for_worsted()
        self.elements: list[str] = []
        self.cx = width / 2
        self.cy = height / 2

    def generate_circle_diagram(self, pattern: Pattern) -> str:
        """
        Generate a top-down circular diagram of a pattern worked in rounds.

        Shows each round as a concentric circle with stitch markers.
        """
        self.elements = []

        # Header
        self.elements.append(
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'viewBox="0 0 {self.width} {self.height}" '
            f'width="{self.width}" height="{self.height}">'
        )

        # Background
        self.elements.append(
            f'<rect width="{self.width}" height="{self.height}" fill="{BACKGROUND_COLOR}"/>'
        )

        # Title
        title = "Crochet Pattern Diagram"
        if pattern.metadata.title:
            title = pattern.metadata.title
        self.elements.append(
            f'<text x="{self.cx}" y="30" text-anchor="middle" '
            f'font-family="Arial, sans-serif" font-size="18" font-weight="bold" '
            f'fill="#333333">{_escape_xml(title)}</text>'
        )

        if pattern.rounds:
            self._draw_rounds_circular(pattern)
        elif pattern.rows:
            self._draw_rows_flat(pattern)

        # Legend
        self._draw_legend()

        # Footer
        self.elements.append("</svg>")
        return "\n".join(self.elements)

    def _draw_rounds_circular(self, pattern: Pattern) -> None:
        """Draw concentric circles representing rounds."""
        max_radius_px = min(self.width, self.height) / 2 - 60  # Leave margin
        num_rounds = len(pattern.rounds)

        if num_rounds == 0:
            return

        # Calculate max stitch count for scaling
        max_stitches = max(
            r.computed_stitch_count for r in pattern.rounds
        )
        if max_stitches == 0:
            # Try context-aware
            prev = 0
            for r in pattern.rounds:
                sc = r.compute_stitch_count_with_context(prev)
                if sc > max_stitches:
                    max_stitches = sc
                prev = sc if sc > 0 else prev

        if max_stitches == 0:
            max_stitches = 1  # Avoid division by zero

        # Draw each round
        for i, rnd in enumerate(pattern.rounds):
            # Radius for this round (proportional to round number)
            radius = ((i + 1) / num_rounds) * max_radius_px + 20

            # Get stitch count
            sc = rnd.computed_stitch_count
            if sc == 0:
                prev_count = 0
                if i > 0:
                    prev_count = pattern.rounds[i - 1].computed_stitch_count
                    if prev_count == 0 and i > 1:
                        prev_count = pattern.rounds[i - 2].computed_stitch_count
                sc = rnd.compute_stitch_count_with_context(prev_count)

            # Determine stitch color based on operations
            color = self._get_round_color(rnd)

            # Draw the round circle
            self.elements.append(
                f'<circle cx="{self.cx}" cy="{self.cy}" r="{radius:.1f}" '
                f'fill="none" stroke="{color}" stroke-width="2" opacity="0.8"/>'
            )

            # Draw stitch markers around the circle
            if sc > 0 and sc <= 120:  # Only draw markers for reasonable counts
                self._draw_stitch_markers(rnd, radius, sc, i)

            # Round number label
            label_x = self.cx + radius + 5
            label_y = self.cy - 3
            self.elements.append(
                f'<text x="{label_x:.1f}" y="{label_y:.1f}" '
                f'font-family="Arial" font-size="10" fill="#666" '
                f'dominant-baseline="middle">R{rnd.round_number}</text>'
            )

        # Center dot (magic ring)
        self.elements.append(
            f'<circle cx="{self.cx}" cy="{self.cy}" r="5" '
            f'fill="{STITCH_COLORS[StitchType.MAGIC_RING]}" stroke="#333" stroke-width="1"/>'
        )
        self.elements.append(
            f'<text x="{self.cx}" y="{self.cy + 18}" text-anchor="middle" '
            f'font-family="Arial" font-size="9" fill="#666">MR</text>'
        )

    def _draw_stitch_markers(
        self, rnd, radius: float, stitch_count: int, round_index: int
    ) -> None:
        """Draw small markers for each stitch position."""
        for j in range(stitch_count):
            angle = (2 * math.pi * j / stitch_count) - math.pi / 2
            x = self.cx + radius * math.cos(angle)
            y = self.cy + radius * math.sin(angle)

            # Small dot for each stitch
            marker_size = max(1.5, min(4, 200 / stitch_count))
            self.elements.append(
                f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{marker_size:.1f}" '
                f'fill="#555" opacity="0.5"/>'
            )

    def _draw_rows_flat(self, pattern: Pattern) -> None:
        """Draw a flat diagram for row-based patterns."""
        max_width = max(r.computed_stitch_count for r in pattern.rows) if pattern.rows else 1
        if max_width == 0:
            max_width = 1

        row_height_px = 20
        stitch_width_px = min(15, (self.width - 100) / max_width)
        start_y = 60
        start_x = 50

        for i, row in enumerate(pattern.rows):
            y = start_y + i * row_height_px
            sc = row.computed_stitch_count

            # Row background
            row_width = sc * stitch_width_px
            self.elements.append(
                f'<rect x="{start_x}" y="{y}" width="{row_width}" '
                f'height="{row_height_px - 2}" fill="{GRID_COLOR}" '
                f'stroke="#DDD" stroke-width="0.5" rx="2"/>'
            )

            # Stitch markers
            for j in range(min(sc, 60)):  # Limit visual markers
                x = start_x + j * stitch_width_px + stitch_width_px / 2
                self.elements.append(
                    f'<circle cx="{x:.1f}" cy="{y + row_height_px / 2:.1f}" '
                    f'r="3" fill="#4A90D9" opacity="0.7"/>'
                )

            # Row label
            self.elements.append(
                f'<text x="{start_x - 5}" y="{y + row_height_px / 2:.1f}" '
                f'text-anchor="end" font-family="Arial" font-size="10" '
                f'fill="#666" dominant-baseline="middle">{row.row_number}</text>'
            )

            # Stitch count
            self.elements.append(
                f'<text x="{start_x + row_width + 5}" y="{y + row_height_px / 2:.1f}" '
                f'font-family="Arial" font-size="10" fill="#999" '
                f'dominant-baseline="middle">({sc})</text>'
            )

    def _get_round_color(self, rnd) -> str:
        """Determine the color for a round based on its operations."""
        for inst in rnd.instructions:
            for op in inst.operations:
                if op.stitch_type == StitchType.INCREASE:
                    return STITCH_COLORS[StitchType.INCREASE]
                if op.stitch_type == StitchType.DECREASE:
                    return STITCH_COLORS[StitchType.DECREASE]
                if op.stitch_type in STITCH_COLORS:
                    return STITCH_COLORS[op.stitch_type]
        return "#4A90D9"

    def _draw_legend(self) -> None:
        """Draw a color legend at the bottom."""
        y = self.height - 40
        items = [
            ("Increase", STITCH_COLORS[StitchType.INCREASE]),
            ("Decrease", STITCH_COLORS[StitchType.DECREASE]),
            ("Single Crochet", STITCH_COLORS[StitchType.SINGLE_CROCHET]),
            ("Magic Ring", STITCH_COLORS[StitchType.MAGIC_RING]),
        ]

        x = 20
        for label, color in items:
            self.elements.append(
                f'<circle cx="{x + 6}" cy="{y}" r="5" fill="{color}"/>'
            )
            self.elements.append(
                f'<text x="{x + 15}" y="{y}" font-family="Arial" font-size="10" '
                f'fill="#555" dominant-baseline="middle">{label}</text>'
            )
            x += len(label) * 7 + 30


def generate_circle_diagram(
    pattern: Pattern,
    width: int = 600,
    height: int = 600,
) -> str:
    """Generate an SVG circle diagram for a pattern."""
    diagram = SVGDiagram(width=width, height=height)
    return diagram.generate_circle_diagram(pattern)


def generate_stitch_count_chart(pattern: Pattern, width: int = 500, height: int = 300) -> str:
    """Generate an SVG chart showing stitch counts per round."""
    elements = []
    elements.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {width} {height}" width="{width}" height="{height}">'
    )
    elements.append(f'<rect width="{width}" height="{height}" fill="white"/>')

    # Title
    elements.append(
        f'<text x="{width/2}" y="25" text-anchor="middle" '
        f'font-family="Arial" font-size="14" font-weight="bold" '
        f'fill="#333">Stitch Count Per Round</text>'
    )

    # Get stitch counts
    items = pattern.rounds or pattern.rows
    if not items:
        elements.append("</svg>")
        return "\n".join(elements)

    counts = []
    prev = 0
    for i, r in enumerate(items):
        sc = r.computed_stitch_count
        if sc == 0:
            sc = r.compute_stitch_count_with_context(prev)
        num = r.round_number if hasattr(r, 'round_number') else r.row_number
        counts.append((num, sc))
        prev = sc if sc > 0 else prev

    if not counts:
        elements.append("</svg>")
        return "\n".join(elements)

    # Chart area
    margin_left = 60
    margin_right = 30
    margin_top = 45
    margin_bottom = 40
    chart_w = width - margin_left - margin_right
    chart_h = height - margin_top - margin_bottom

    max_count = max(c[1] for c in counts) if counts else 1
    num_items = len(counts)

    # Axes
    elements.append(
        f'<line x1="{margin_left}" y1="{margin_top}" '
        f'x2="{margin_left}" y2="{margin_top + chart_h}" '
        f'stroke="#333" stroke-width="1"/>'
    )
    elements.append(
        f'<line x1="{margin_left}" y1="{margin_top + chart_h}" '
        f'x2="{margin_left + chart_w}" y2="{margin_top + chart_h}" '
        f'stroke="#333" stroke-width="1"/>'
    )

    # Y-axis labels
    for i in range(5):
        val = int(max_count * i / 4)
        y = margin_top + chart_h - (chart_h * i / 4)
        elements.append(
            f'<text x="{margin_left - 5}" y="{y}" text-anchor="end" '
            f'font-family="Arial" font-size="9" fill="#666" '
            f'dominant-baseline="middle">{val}</text>'
        )
        elements.append(
            f'<line x1="{margin_left}" y1="{y}" x2="{margin_left + chart_w}" y2="{y}" '
            f'stroke="#EEE" stroke-width="0.5"/>'
        )

    # Bars
    bar_width = max(8, min(30, chart_w / num_items - 4))
    gap = (chart_w - bar_width * num_items) / (num_items + 1)

    for i, (num, count) in enumerate(counts):
        x = margin_left + gap + i * (bar_width + gap)
        bar_h = (count / max_count) * chart_h if max_count > 0 else 0
        y = margin_top + chart_h - bar_h

        # Determine color
        if i > 0:
            prev_count = counts[i - 1][1]
            if count > prev_count:
                color = STITCH_COLORS[StitchType.INCREASE]
            elif count < prev_count:
                color = STITCH_COLORS[StitchType.DECREASE]
            else:
                color = STITCH_COLORS[StitchType.SINGLE_CROCHET]
        else:
            color = STITCH_COLORS[StitchType.MAGIC_RING]

        elements.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_width}" '
            f'height="{bar_h:.1f}" fill="{color}" opacity="0.8" rx="2"/>'
        )

        # Value on top
        elements.append(
            f'<text x="{x + bar_width/2:.1f}" y="{y - 3:.1f}" text-anchor="middle" '
            f'font-family="Arial" font-size="8" fill="#555">{count}</text>'
        )

        # Round number below
        elements.append(
            f'<text x="{x + bar_width/2:.1f}" y="{margin_top + chart_h + 12}" '
            f'text-anchor="middle" font-family="Arial" font-size="8" fill="#666">{num}</text>'
        )

    # Axis labels
    elements.append(
        f'<text x="{width/2}" y="{height - 5}" text-anchor="middle" '
        f'font-family="Arial" font-size="10" fill="#555">Round</text>'
    )
    elements.append(
        f'<text x="15" y="{height/2}" text-anchor="middle" '
        f'font-family="Arial" font-size="10" fill="#555" '
        f'transform="rotate(-90, 15, {height/2})">Stitches</text>'
    )

    elements.append("</svg>")
    return "\n".join(elements)


def _escape_xml(text: str) -> str:
    """Escape special XML characters."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )
