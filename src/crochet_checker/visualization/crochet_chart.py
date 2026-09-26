"""
Crochet chart generator.

Creates traditional crochet symbol charts showing stitch symbols
arranged in the pattern layout, similar to what appears in
commercial crochet patterns.
"""

from __future__ import annotations

import math
from typing import Optional

from ..model.pattern import Pattern
from ..model.stitch import StitchType
from .stitch_diagram import _escape_xml


# SVG symbol paths for each stitch type (simplified representations)
STITCH_SYMBOLS = {
    StitchType.CHAIN: {"symbol": "○", "color": "#999", "desc": "Chain"},
    StitchType.SINGLE_CROCHET: {"symbol": "✕", "color": "#4A90D9", "desc": "Single Crochet"},
    StitchType.HALF_DOUBLE_CROCHET: {"symbol": "T", "color": "#50C878", "desc": "Half Double Crochet"},
    StitchType.DOUBLE_CROCHET: {"symbol": "T̄", "color": "#7B68EE", "desc": "Double Crochet"},
    StitchType.TREBLE_CROCHET: {"symbol": "T̈", "color": "#FF8C00", "desc": "Treble Crochet"},
    StitchType.SLIP_STITCH: {"symbol": "•", "color": "#666", "desc": "Slip Stitch"},
    StitchType.INCREASE: {"symbol": "V", "color": "#2ECC71", "desc": "Increase"},
    StitchType.DECREASE: {"symbol": "Λ", "color": "#E74C3C", "desc": "Decrease"},
}


def generate_crochet_chart(pattern: Pattern, width: int = 600, height: int = 500) -> str:
    """
    Generate a traditional crochet symbol chart as SVG.

    Shows stitch symbols arranged in circles (for rounds) or
    rows (for flat work), similar to commercial pattern charts.
    """
    elements = []

    elements.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {width} {height}" width="{width}" height="{height}">'
    )
    elements.append(f'<rect width="{width}" height="{height}" fill="#FEFEFE"/>')

    # Title
    title = pattern.metadata.title or "Crochet Chart"
    elements.append(
        f'<text x="{width/2}" y="25" text-anchor="middle" '
        f'font-family="Arial" font-size="16" font-weight="bold" '
        f'fill="#2C3E50">{_escape_xml(title)}</text>'
    )
    elements.append(
        f'<text x="{width/2}" y="42" text-anchor="middle" '
        f'font-family="Arial" font-size="10" fill="#7F8C8D">'
        f'Symbol Chart</text>'
    )

    cx = width / 2
    cy = height / 2 + 20

    if pattern.rounds:
        _draw_chart_rounds(elements, pattern, cx, cy, width, height)
    elif pattern.rows:
        _draw_chart_rows(elements, pattern, width, height)

    # Legend
    _draw_chart_legend(elements, width, height)

    elements.append("</svg>")
    return "\n".join(elements)


def _draw_chart_rounds(
    elements: list[str], pattern: Pattern, cx: float, cy: float,
    width: int, height: int
) -> None:
    """Draw a circular crochet chart with stitch symbols."""
    max_r = min(width, height) / 2 - 70
    num_rounds = len(pattern.rounds)

    if num_rounds == 0:
        return

    # Center marker
    elements.append(
        f'<circle cx="{cx}" cy="{cy}" r="6" fill="#F39C12" '
        f'stroke="#333" stroke-width="1"/>'
    )

    for i, rnd in enumerate(pattern.rounds):
        radius = ((i + 1) / num_rounds) * max_r + 25

        # Get stitch count
        sc = rnd.computed_stitch_count
        if sc == 0:
            prev = 0
            if i > 0:
                prev = pattern.rounds[i-1].computed_stitch_count
            sc = rnd.compute_stitch_count_with_context(prev)

        if sc == 0:
            continue

        # Draw round guide circle (dashed)
        elements.append(
            f'<circle cx="{cx}" cy="{cy}" r="{radius:.1f}" '
            f'fill="none" stroke="#E0E0E0" stroke-width="0.5" '
            f'stroke-dasharray="3,3"/>'
        )

        # Draw stitch symbols
        # Limit displayed symbols for readability
        display_count = min(sc, 72)
        symbol_size = max(8, min(16, 400 / display_count))

        for j in range(display_count):
            angle = (2 * math.pi * j / display_count) - math.pi / 2
            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle)

            # Determine stitch symbol from operations
            symbol_info = _get_stitch_symbol(rnd, j, display_count)

            # Draw the symbol
            elements.append(
                f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="middle" '
                f'dominant-baseline="central" font-size="{symbol_size}" '
                f'fill="{symbol_info["color"]}" '
                f'font-family="Arial">{symbol_info["symbol"]}</text>'
            )

        # Round number
        label_angle = -math.pi / 4  # Top-right
        lx = cx + (radius + 15) * math.cos(label_angle)
        ly = cy + (radius + 15) * math.sin(label_angle)
        elements.append(
            f'<text x="{lx:.1f}" y="{ly:.1f}" font-family="Arial" font-size="9" '
            f'fill="#888" text-anchor="middle">{rnd.round_number}</text>'
        )


def _draw_chart_rows(
    elements: list[str], pattern: Pattern, width: int, height: int
) -> None:
    """Draw a flat crochet chart with stitch symbols."""
    max_stitches = max(r.computed_stitch_count for r in pattern.rows) if pattern.rows else 1
    if max_stitches == 0:
        max_stitches = 1

    row_h = 25
    stitch_w = min(20, (width - 100) / max_stitches)
    start_y = 60
    start_x = 60

    for i, row in enumerate(pattern.rows):
        y = start_y + i * row_h
        sc = row.computed_stitch_count

        # Row background
        elements.append(
            f'<rect x="{start_x - 2}" y="{y - row_h/2 + 2}" '
            f'width="{sc * stitch_w + 4}" height="{row_h - 4}" '
            f'fill="#F8F9FA" stroke="#EEE" rx="3"/>'
        )

        # Draw stitch symbols
        for j in range(min(sc, 40)):  # Limit visual markers
            x = start_x + j * stitch_w + stitch_w / 2
            symbol = "✕"  # Default to sc symbol

            # Check if row has increases/decreases
            has_inc = any(
                op.stitch_type == StitchType.INCREASE
                for inst in row.instructions for op in inst.operations
            )
            has_dec = any(
                op.stitch_type == StitchType.DECREASE
                for inst in row.instructions for op in inst.operations
            )

            if has_inc:
                color = "#2ECC71"
            elif has_dec:
                color = "#E74C3C"
            else:
                color = "#4A90D9"

            elements.append(
                f'<text x="{x:.1f}" y="{y + 2}" text-anchor="middle" '
                f'dominant-baseline="central" font-size="12" '
                f'fill="{color}" font-family="Arial">{symbol}</text>'
            )

        # Row number
        elements.append(
            f'<text x="{start_x - 10}" y="{y + 2}" text-anchor="end" '
            f'dominant-baseline="central" font-family="Arial" font-size="10" '
            f'fill="#888">{row.row_number}</text>'
        )

        # Stitch count
        elements.append(
            f'<text x="{start_x + sc * stitch_w + 10}" y="{y + 2}" '
            f'dominant-baseline="central" font-family="Arial" font-size="9" '
            f'fill="#AAA">({sc})</text>'
        )


def _get_stitch_symbol(rnd, position: int, total: int) -> dict:
    """Get the symbol for a stitch position in a round."""
    default = {"symbol": "✕", "color": "#4A90D9"}

    if not rnd.instructions:
        return default

    # Determine what type of stitch is at this position
    pos_in_round = position % total
    cumulative = 0

    for inst in rnd.instructions:
        if inst.is_repeat_block and inst.repeat_unit and inst.repeat_count:
            unit_size = len(inst.repeat_unit)
            total_in_block = unit_size * inst.repeat_count
            if pos_in_round < cumulative + total_in_block:
                local_pos = (pos_in_round - cumulative) % unit_size
                op = inst.repeat_unit[local_pos]
                return STITCH_SYMBOLS.get(op.stitch_type, default)
            cumulative += total_in_block
        else:
            for op in inst.operations:
                if pos_in_round < cumulative + op.count:
                    return STITCH_SYMBOLS.get(op.stitch_type, default)
                cumulative += op.count

    return default


def _draw_chart_legend(elements: list[str], width: int, height: int) -> None:
    """Draw a legend for the chart symbols."""
    y = height - 30
    x = 20

    items = [
        ("✕", "sc", "#4A90D9"),
        ("V", "inc", "#2ECC71"),
        ("Λ", "dec", "#E74C3C"),
        ("○", "ch", "#999"),
    ]

    for symbol, label, color in items:
        elements.append(
            f'<text x="{x}" y="{y}" font-size="14" fill="{color}" '
            f'font-family="Arial">{symbol}</text>'
        )
        elements.append(
            f'<text x="{x + 18}" y="{y}" font-size="9" fill="#666" '
            f'font-family="Arial" dominant-baseline="central">{label}</text>'
        )
        x += 70
