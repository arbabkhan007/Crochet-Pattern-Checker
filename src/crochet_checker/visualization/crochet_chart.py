"""Crochet symbol chart generator."""
from __future__ import annotations
import math
from ..model.pattern import Pattern
from ..model.stitch import StitchType

def _esc(t): return t.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def generate_crochet_chart(pattern, width=600, height=500):
    el = []
    el.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    el.append(f'<rect width="{width}" height="{height}" fill="#FEFEFE"/>')
    title = pattern.metadata.title or "Crochet Chart"
    el.append(f'<text x="{width/2}" y="25" text-anchor="middle" font-family="Arial" font-size="16" font-weight="bold" fill="#2C3E50">{_esc(title)}</text>')
    el.append(f'<text x="{width/2}" y="42" text-anchor="middle" font-family="Arial" font-size="10" fill="#7F8C8D">Symbol Chart</text>')
    cx, cy = width/2, height/2+20
    if pattern.rounds:
        max_r = min(width,height)/2-70; n = len(pattern.rounds)
        el.append(f'<circle cx="{cx}" cy="{cy}" r="6" fill="#F39C12" stroke="#333"/>')
        for i, rnd in enumerate(pattern.rounds):
            radius = ((i+1)/n)*max_r+25
            sc = rnd.computed_stitch_count
            if sc == 0:
                prev = pattern.rounds[i-1].computed_stitch_count if i > 0 else 0
                sc = rnd.compute_stitch_count_with_context(prev)
            if sc == 0: continue
            el.append(f'<circle cx="{cx}" cy="{cy}" r="{radius:.1f}" fill="none" stroke="#E0E0E0" stroke-dasharray="3,3"/>')
            dc = min(sc, 72); ss = max(8, min(16, 400/dc))
            has_inc = any(op.stitch_type==StitchType.INCREASE for inst in rnd.instructions for op in inst.operations)
            has_dec = any(op.stitch_type==StitchType.DECREASE for inst in rnd.instructions for op in inst.operations)
            color = "#2ECC71" if has_inc else "#E74C3C" if has_dec else "#4A90D9"
            sym = "V" if has_inc else chr(923) if has_dec else chr(10006)
            for j in range(dc):
                angle = (2*math.pi*j/dc)-math.pi/2
                x = cx+radius*math.cos(angle); y = cy+radius*math.sin(angle)
                el.append(f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="middle" dominant-baseline="central" font-size="{ss}" fill="{color}" font-family="Arial">{sym}</text>')
    y = height-30; x = 20
    for sym, lbl, c in [("X","sc","#4A90D9"),("V","inc","#2ECC71"),(chr(923),"dec","#E74C3C")]:
        el.append(f'<text x="{x}" y="{y}" font-size="14" fill="{c}" font-family="Arial">{sym}</text>')
        el.append(f'<text x="{x+18}" y="{y}" font-size="9" fill="#666" font-family="Arial" dominant-baseline="central">{lbl}</text>')
        x += 70
    el.append("</svg>")
    return chr(10).join(el)
