"""2D preview renderer."""
from __future__ import annotations
from ..model.pattern import Pattern
from .stitch_diagram import generate_circle_diagram, generate_stitch_count_chart, _esc

def render_2d_preview(pattern, validation_report=None):
    el = []
    total_h = 1100
    el.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 {total_h}" width="800" height="{total_h}">')
    el.append(f'<rect width="800" height="{total_h}" fill="white"/>')
    title = pattern.metadata.title or "Crochet Pattern Preview"
    el.append(f'<text x="400" y="30" text-anchor="middle" font-family="Arial" font-size="20" font-weight="bold" fill="#2C3E50">{_esc(title)}</text>')
    el.append(f'<text x="400" y="50" text-anchor="middle" font-family="Arial" font-size="12" fill="#7F8C8D">Construction: {pattern.construction.value}</text>')
    if validation_report:
        status = validation_report.overall_status; score = validation_report.score
        c = {"PASS":"#27AE60","PASS_WITH_WARNINGS":"#F39C12","ERROR":"#E74C3C"}.get(status,"#95A5A6")
        el.append(f'<rect x="30" y="65" width="200" height="30" rx="5" fill="{c}" opacity="0.15" stroke="{c}"/>')
        el.append(f'<text x="130" y="85" text-anchor="middle" font-size="12" font-weight="bold" fill="{c}" font-family="Arial">{status} | Score: {score}/100</text>')
    items = pattern.rounds or pattern.rows
    ty = 640
    el.append(f'<text x="30" y="{ty}" font-family="Arial" font-size="14" font-weight="bold" fill="#2C3E50">Pattern Instructions</text>')
    ty += 20
    for i, r in enumerate(items[:20]):
        num = r.round_number if hasattr(r,"round_number") else r.row_number
        label = "Round" if hasattr(r,"round_number") else "Row"
        el.append(f'<text x="50" y="{ty}" font-family="monospace" font-size="10" fill="#444">{label} {num}: {_esc(r.source_text[:80])}</text>')
        ty += 16
    el.append("</svg>")
    return chr(10).join(el)
