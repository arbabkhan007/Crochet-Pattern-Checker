"""SVG-based stitch diagram generator."""
from __future__ import annotations
import math
from typing import Optional
from ..model.pattern import Pattern
from ..model.stitch import StitchType
from .measurements import StitchDimensions

STITCH_COLORS = {
    StitchType.SINGLE_CROCHET: "#4A90D9", StitchType.DOUBLE_CROCHET: "#7B68EE",
    StitchType.HALF_DOUBLE_CROCHET: "#50C878", StitchType.INCREASE: "#2ECC71",
    StitchType.DECREASE: "#E74C3C", StitchType.MAGIC_RING: "#F39C12",
    StitchType.CHAIN: "#999999",
}

def _esc(t):
    return t.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace(chr(34),"&quot;")

class SVGDiagram:
    def __init__(self, width=600, height=600):
        self.width = width; self.height = height; self.elements = []
        self.cx = width/2; self.cy = height/2
    def generate_circle_diagram(self, pattern):
        self.elements = []
        self.elements.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.width} {self.height}" width="{self.width}" height="{self.height}">')
        self.elements.append(f'<rect width="{self.width}" height="{self.height}" fill="white"/>')
        title = pattern.metadata.title or "Crochet Pattern Diagram"
        self.elements.append(f'<text x="{self.cx}" y="30" text-anchor="middle" font-family="Arial" font-size="18" font-weight="bold" fill="#333">{_esc(title)}</text>')
        if pattern.rounds: self._draw_rounds(pattern)
        self.elements.append(f'<circle cx="{self.cx}" cy="{self.cy}" r="5" fill="#F39C12" stroke="#333"/>')
        self.elements.append(f'<text x="{self.cx}" y="{self.cy+18}" text-anchor="middle" font-size="9" fill="#666" font-family="Arial">MR</text>')
        self.elements.append("</svg>")
        return chr(10).join(self.elements)
    def _draw_rounds(self, pattern):
        max_r = min(self.width, self.height)/2 - 60
        n = len(pattern.rounds)
        if n == 0: return
        for i, rnd in enumerate(pattern.rounds):
            radius = ((i+1)/n)*max_r + 20
            sc = rnd.computed_stitch_count
            if sc == 0:
                prev = pattern.rounds[i-1].computed_stitch_count if i > 0 else 0
                sc = rnd.compute_stitch_count_with_context(prev)
            color = self._color(rnd)
            self.elements.append(f'<circle cx="{self.cx}" cy="{self.cy}" r="{radius:.1f}" fill="none" stroke="{color}" stroke-width="2" opacity="0.8"/>')
            if 0 < sc <= 120:
                for j in range(sc):
                    angle = (2*math.pi*j/sc) - math.pi/2
                    x = self.cx + radius*math.cos(angle); y = self.cy + radius*math.sin(angle)
                    ms = max(1.5, min(4, 200/sc))
                    self.elements.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{ms:.1f}" fill="#555" opacity="0.5"/>')
            lx = self.cx + radius + 5; ly = self.cy - 3
            self.elements.append(f'<text x="{lx:.1f}" y="{ly:.1f}" font-family="Arial" font-size="10" fill="#666" dominant-baseline="middle">R{rnd.round_number}</text>')
    def _color(self, rnd):
        for inst in rnd.instructions:
            for op in inst.operations:
                if op.stitch_type in STITCH_COLORS: return STITCH_COLORS[op.stitch_type]
        return "#4A90D9"

def generate_circle_diagram(pattern, width=600, height=600):
    return SVGDiagram(width, height).generate_circle_diagram(pattern)

def generate_stitch_count_chart(pattern, width=500, height=300):
    el = []
    el.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    el.append(f'<rect width="{width}" height="{height}" fill="white"/>')
    el.append(f'<text x="{width/2}" y="25" text-anchor="middle" font-family="Arial" font-size="14" font-weight="bold" fill="#333">Stitch Count Per Round</text>')
    items = pattern.rounds or pattern.rows
    if not items: el.append("</svg>"); return chr(10).join(el)
    counts = []; prev = 0
    for i, r in enumerate(items):
        sc = r.computed_stitch_count
        if sc == 0: sc = r.compute_stitch_count_with_context(prev)
        num = r.round_number if hasattr(r, "round_number") else r.row_number
        counts.append((num, sc)); prev = sc if sc > 0 else prev
    ml, mt, mb = 60, 45, 40; cw = width-ml-30; ch = height-mt-mb
    mc = max(c[1] for c in counts) if counts else 1
    el.append(f'<line x1="{ml}" y1="{mt}" x2="{ml}" y2="{mt+ch}" stroke="#333"/>')
    el.append(f'<line x1="{ml}" y1="{mt+ch}" x2="{ml+cw}" y2="{mt+ch}" stroke="#333"/>')
    bw = max(8, min(30, cw/len(counts)-4)); gap = (cw - bw*len(counts))/(len(counts)+1)
    for i, (num, count) in enumerate(counts):
        x = ml + gap + i*(bw+gap); bh = (count/mc)*ch if mc > 0 else 0; y = mt+ch-bh
        color = "#2ECC71" if i > 0 and count > counts[i-1][1] else "#E74C3C" if i > 0 and count < counts[i-1][1] else "#4A90D9"
        el.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw}" height="{bh:.1f}" fill="{color}" opacity="0.8" rx="2"/>')
        el.append(f'<text x="{x+bw/2:.1f}" y="{y-3:.1f}" text-anchor="middle" font-size="8" fill="#555" font-family="Arial">{count}</text>')
        el.append(f'<text x="{x+bw/2:.1f}" y="{mt+ch+12}" text-anchor="middle" font-size="8" fill="#666" font-family="Arial">{num}</text>')
    el.append("</svg>")
    return chr(10).join(el)
