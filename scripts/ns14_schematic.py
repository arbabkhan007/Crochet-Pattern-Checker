"""Draw the NS-14 skirt exactly as the written pattern specifies.

Nothing here is invented. Every element is read off the verified pattern:

  * 32 growth rounds, round r holding 12*r stitches.
  * Bobble rounds are R5, R8, R11 ... R32 - ten of them - and each is worked
    COMPLETELY in CC, so the finished piece shows ten whole oat cream rings on
    a forest green ground, not green rings with oat flecks.
  * One BO per repeat, twelve repeats, so every bobble ring carries exactly
    twelve bobbles and they stack into twelve radial columns.
  * Twelve optional surface spokes in CC, centre ring to outer edge.
  * The scalloped border closes in 384 / 6 = 64 shells at the large size.
  * Centre opening is the relaxed ch-20 ring, about 1.6 in against a 40.7 in
    unbordered body.

The output is a flat colour schematic used as the structural reference for the
photographic cover render, so the cover cannot drift from the pattern.

Usage:  python scripts/ns14_schematic.py out.png [--size 1600]
"""

from __future__ import annotations

import argparse
import math

from PIL import Image, ImageDraw

FOREST = (30, 58, 43)
FOREST_D = (20, 42, 30)
OAT = (230, 215, 195)
OAT_D = (205, 188, 164)
BG = (248, 245, 239)

ROUNDS = 32
REPEATS = 12
FIRST_BOBBLE, BOBBLE_EVERY = 5, 3

BODY_IN = 40.7        # unbordered diameter at target gauge
OPENING_IN = 1.6      # relaxed ch-20 ring
BORDER_IN = 0.75      # 0.6-0.9 in of scallop depth


def bobble_rounds() -> list[int]:
    return [r for r in range(FIRST_BOBBLE, ROUNDS + 1, BOBBLE_EVERY)]


def draw(size: int = 1600, ss: int = 2) -> Image.Image:
    S = size * ss
    img = Image.new("RGB", (S, S), BG)
    d = ImageDraw.Draw(img)
    cx = cy = S / 2

    px_per_in = (S * 0.455) / (BODY_IN / 2)   # leave room for the border
    r_body = (BODY_IN / 2) * px_per_in
    r_hole = (OPENING_IN / 2) * px_per_in
    r_border = BORDER_IN * px_per_in
    band = (r_body - r_hole) / ROUNDS

    bobs = set(bobble_rounds())
    spoke_angles = [math.radians(90 + i * 360 / REPEATS) for i in range(REPEATS)]
    # bobble columns sit midway between the surface spokes so both read clearly
    bob_angles = [a + math.radians(180 / REPEATS) for a in spoke_angles]

    def ring(radius, width, fill):
        d.ellipse([cx - radius, cy - radius, cx + radius, cy + radius],
                  outline=fill, width=max(1, int(round(width))))

    # ---- scalloped border: 64 shells closing on the final round
    scallops = (ROUNDS * REPEATS) // 6
    for k in range(scallops):
        a = 2 * math.pi * k / scallops
        sx, sy = cx + r_body * math.cos(a), cy + r_body * math.sin(a)
        rr = r_border
        d.ellipse([sx - rr, sy - rr, sx + rr, sy + rr], fill=OAT,
                  outline=OAT_D, width=max(1, int(ss * 1.2)))

    # ---- body: one ring per growth round, coloured by the written route
    for r in range(ROUNDS, 0, -1):
        rad = r_hole + (r - 0.5) * band
        ring(rad, band * 1.06, OAT if r in bobs else FOREST)

    # faint round separations, so the 32 rounds stay countable
    for r in range(1, ROUNDS + 1):
        rad = r_hole + r * band
        ring(rad, max(1, ss * 0.7), OAT_D if r in bobs else FOREST_D)

    # ---- twelve surface spokes, centre ring to outer edge
    for a in spoke_angles:
        d.line([cx + r_hole * math.cos(a), cy + r_hole * math.sin(a),
                cx + r_body * math.cos(a), cy + r_body * math.sin(a)],
               fill=OAT, width=max(2, int(band * 0.42)))

    # ---- twelve bobbles on each of the ten bobble rings
    br = band * 0.62
    for r in bobs:
        rad = r_hole + (r - 0.5) * band
        for a in bob_angles:
            bx, by = cx + rad * math.cos(a), cy + rad * math.sin(a)
            d.ellipse([bx - br, by - br, bx + br, by + br],
                      fill=OAT, outline=OAT_D, width=max(1, int(ss * 1.4)))

    # ---- closed centre ring
    d.ellipse([cx - r_hole, cy - r_hole, cx + r_hole, cy + r_hole],
              fill=BG, outline=FOREST_D, width=max(2, int(band * 0.5)))

    return img.resize((size, size), Image.LANCZOS)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--size", type=int, default=1600)
    a = ap.parse_args()
    im = draw(a.size)
    im.save(a.out)
    b = bobble_rounds()
    print(f"wrote {a.out}  {im.size[0]}x{im.size[1]}")
    print(f"  {ROUNDS} rounds, {len(b)} oat rings at {b}")
    print(f"  {REPEATS} bobbles per ring = {REPEATS * len(b)} bobbles, "
          f"{REPEATS} spokes, {(ROUNDS * REPEATS) // 6} scallops")
