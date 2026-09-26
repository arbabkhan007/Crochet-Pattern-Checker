#!/usr/bin/env python3
"""
Draws the 12 increase columns and the bobble placements for both readings of
the round-start instruction, straight from the simulator's geometry.

  left  : "[dc in next N-2 sts, 2 dc in next st] x 12"  (original wording)
          the round begins one stitch past the join -> the columns spiral
  right : "dc in same st as join, ... x 11"             (corrected wording)
          the round begins in the join -> the columns radiate

Output: spoke-comparison.svg
"""

from __future__ import annotations

import math
from pathlib import Path

LAST = 32
ST_WIDTH_CM = 10.0 / 12
ROW_H_CM = 10.0 / 6
HOLE_R_CM = (12 * ST_WIDTH_CM / math.pi) / 2


def is_bobble(n: int) -> bool:
    return n >= 5 and (n - 5) % 3 == 0


def phases(anchor: int) -> dict[int, float]:
    """Fraction-of-a-turn offset of each round's first stitch."""
    phi = {1: 0.0}
    for n in range(2, LAST + 1):
        phi[n] = phi[n - 1] + anchor / (12 * (n - 1))
    return phi


def point(n: int, idx: int, phi: dict[int, float], cx: float, cy: float, scale: float):
    ang = 2 * math.pi * (phi[n] + idx / (12 * n)) - math.pi / 2
    r = (HOLE_R_CM + n * ROW_H_CM) * scale
    return cx + r * math.cos(ang), cy + r * math.sin(ang)


def panel(anchor: int, cx: float, cy: float, scale: float, title: str, subtitle: str,
          colour: str) -> str:
    phi = phases(anchor)
    out: list[str] = []

    # faint round outlines
    for n in range(1, LAST + 1):
        r = (HOLE_R_CM + n * ROW_H_CM) * scale
        out.append(
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="none" '
            f'stroke="#e8e4dd" stroke-width="0.7"/>'
        )

    # the 12 increase columns
    for k in range(1, 13):
        pts = []
        for n in range(2, LAST + 1):
            pts.append(point(n, k * n - 1, phi, cx, cy, scale))
        d = " ".join(f"{'M' if i == 0 else 'L'}{x:.2f},{y:.2f}" for i, (x, y) in enumerate(pts))
        out.append(f'<path d="{d}" fill="none" stroke="{colour}" stroke-width="2.1" '
                   f'stroke-linecap="round" stroke-linejoin="round" opacity="0.95"/>')

    # bobbles
    for n in range(5, LAST + 1):
        if not is_bobble(n):
            continue
        for k in range(1, 13):
            x, y = point(n, (k - 1) * n, phi, cx, cy, scale)
            out.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="2.6" fill="#b4432f" '
                       f'stroke="#ffffff" stroke-width="0.6"/>')

    out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{HOLE_R_CM * scale:.1f}" '
               f'fill="#ffffff" stroke="#c9c2b6" stroke-width="1.2"/>')
    out.append(f'<text x="{cx:.0f}" y="{cy - 245:.0f}" text-anchor="middle" '
               f'font-family="Georgia,serif" font-size="19" fill="#2b2b2b">{title}</text>')
    out.append(f'<text x="{cx:.0f}" y="{cy - 224:.0f}" text-anchor="middle" '
               f'font-family="Georgia,serif" font-size="12.5" fill="#6b6b6b">{subtitle}</text>')
    return "\n".join(out)


def main() -> None:
    scale = 3.7
    w, h = 1080, 580
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}">',
        f'<rect width="{w}" height="{h}" fill="#fbf9f5"/>',
        '<text x="540" y="38" text-anchor="middle" font-family="Georgia,serif" '
        'font-size="21" fill="#2b2b2b">NS 14 Bobble Snowflake Tree Skirt - simulated '
        'spoke geometry, R1 to R32</text>',
        panel(1, 285, 310, scale,
              "As written: &#8220;dc in next st&#8221;",
              "columns wind 120.8&#176; - a spiral, not a snowflake", "#9a6fb0"),
        panel(0, 795, 310, scale,
              "Corrected: &#8220;dc in same st as join&#8221;",
              "columns hold 0.0&#176; - 12 straight spokes", "#2f7d5c"),
        '<text x="540" y="560" text-anchor="middle" font-family="Georgia,serif" '
        'font-size="12.5" fill="#6b6b6b">Both versions produce identical stitch counts '
        '(12 x N every round) - only a stitch-level simulation separates them. '
        'Dots = bobbles.</text>',
        '</svg>',
    ]
    out = Path(__file__).parent / "spoke-comparison.svg"
    out.write_text("\n".join(svg), encoding="utf-8")

    # numeric summary
    for anchor, name in ((1, "as written"), (0, "corrected")):
        phi = phases(anchor)
        print(f"{name:<12}: total column rotation R1->R{LAST} = "
              f"{phi[LAST] * 360:.1f} degrees")
    print(f"wrote {out.name}")


if __name__ == "__main__":
    main()
