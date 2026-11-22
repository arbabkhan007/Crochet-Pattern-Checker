"""Brand-styled technical figures for Novality Store pattern PDFs.

Every figure here is drawn from the verified stitch counts, not from the
checker's visualisation module. That module was audited for NS-14 and found to
emit, for this pattern:

  * a sphere mesh for a flat circular skirt (each round is given a rising z),
  * sc symbols for a double-crochet pattern, with no bobble symbol at all,
  * a stitch-count chart whose round 2 reads 2 instead of 24,
  * a composite preview carrying the NeckJumpChecker false-positive banner.

So these are redrawn. The arithmetic below is the published arithmetic: round r
holds 12*r stitches, one repeat of round r is r stitches, and a bobble round
swaps the first plain dc of each repeat for a BO.

Output is vector (ReportLab Drawing), so it stays crisp at any zoom and adds
almost nothing to the file size.
"""

from __future__ import annotations

import math

from reportlab.graphics.shapes import (
    Circle,
    Drawing,
    Group,
    Line,
    PolyLine,
    Rect,
    String,
)
from reportlab.lib import colors

FOREST = colors.HexColor("#1E3A2B")
FOREST_LT = colors.HexColor("#2E5440")
OAT = colors.HexColor("#E6D7C3")
OAT_LT = colors.HexColor("#F3EADF")
GOLD = colors.HexColor("#D4AF37")
SAGE = colors.HexColor("#E8F0EC")
INK = colors.HexColor("#1A1A1A")
MUTED = colors.HexColor("#5F6B64")
RULE = colors.HexColor("#D8DEDA")
PANEL = colors.HexColor("#F8F9FA")

# The host renderer registers DejaVu under its own face names, so it injects
# them here. Defaults keep this module runnable standalone.
BODY = "Helvetica"
BOLD = "Helvetica-Bold"


def use_fonts(body: str, bold: str) -> None:
    """Adopt the caller's registered face names."""
    global BODY, BOLD
    BODY, BOLD = body, bold

TOTAL_ROUNDS = 32
PER_ROUND = 12          # 12 repeats, so round r gains 12 stitches
FIRST_BOBBLE = 5
BOBBLE_EVERY = 3
STOPS = {14: "MINI", 23: "STANDARD", 32: "LARGE"}


def counts() -> list[int]:
    """Published stitch count for every round: 12, 24, ... 384."""
    return [PER_ROUND * r for r in range(1, TOTAL_ROUNDS + 1)]


def is_bobble(r: int) -> bool:
    """R5, R8, R11 ... every third round from 5."""
    return r >= FIRST_BOBBLE and (r - FIRST_BOBBLE) % BOBBLE_EVERY == 0


def _panel(d: Drawing, w: float, h: float, fill=PANEL) -> None:
    d.add(Rect(0, 0, w, h, fillColor=fill, strokeColor=RULE,
               strokeWidth=0.6, rx=5, ry=5))


def _text(g, x, y, s, size=7.0, col=MUTED, font=None, anchor="start"):
    g.add(String(x, y, s, fontName=font or BODY, fontSize=size, fillColor=col,
                 textAnchor=anchor))


# ---------------------------------------------------------------- colour route

def colour_route_map(width: float) -> Drawing:
    """Concentric colour map: which rounds are MC and which are CC.

    One ring per growth round, coloured by the pattern's written colour route,
    with the twelve increase columns and the three size stop-points marked.
    """
    h = width * 0.86
    d = Drawing(width, h)
    _panel(d, width, h, colors.white)

    cx, cy = width * 0.40, h * 0.50
    outer = min(width * 0.355, h * 0.43)
    hole = outer * 0.085
    band = (outer - hole) / TOTAL_ROUNDS

    g = Group()
    # growth rounds, inner to outer
    for r in range(1, TOTAL_ROUNDS + 1):
        rad = hole + (r - 0.5) * band
        col = OAT if is_bobble(r) else FOREST
        g.add(Circle(cx, cy, rad, fillColor=None, strokeColor=col,
                     strokeWidth=band * 0.92))

    # the twelve increase columns
    for i in range(PER_ROUND):
        a = math.radians(90 + i * 360 / PER_ROUND)
        g.add(Line(cx + hole * math.cos(a), cy + hole * math.sin(a),
                   cx + outer * math.cos(a), cy + outer * math.sin(a),
                   strokeColor=GOLD, strokeWidth=0.8, strokeOpacity=0.85))

    # size stop-points
    for r, label in STOPS.items():
        rad = hole + r * band
        # white under-stroke so the dashes stay legible over the dark bands
        g.add(Circle(cx, cy, rad, fillColor=None, strokeColor=colors.white,
                     strokeWidth=2.8))
        g.add(Circle(cx, cy, rad, fillColor=None, strokeColor=GOLD,
                     strokeWidth=1.8, strokeDashArray=[3.2, 2.6]))
        a = math.radians(38)
        lx, ly = cx + rad * math.cos(a), cy + rad * math.sin(a)
        g.add(Circle(lx, ly, 1.9, fillColor=GOLD, strokeColor=colors.white,
                     strokeWidth=0.6))

    # closed centre ring
    g.add(Circle(cx, cy, hole, fillColor=colors.white, strokeColor=FOREST,
                 strokeWidth=1.1))
    d.add(g)

    # ---- legend
    lx = width * 0.775
    ly = h * 0.80
    _text(d, lx, ly + 16, "Colour route", 8.6, FOREST, BOLD)

    rows = [
        (FOREST, "MC forest green",
         ["R1-R4 and every", "non-bobble round"]),
        (OAT, "CC oat cream",
         ["every bobble round,", "R5 then every 3rd"]),
        (GOLD, "Increase column",
         ["12 of them, R2 on"]),
    ]
    yy = ly
    for col, name, sub in rows:
        d.add(Rect(lx, yy, 9, 9, fillColor=col, strokeColor=FOREST_LT,
                   strokeWidth=0.5, rx=1.5, ry=1.5))
        _text(d, lx + 14, yy + 3.2, name, 7.2, INK, BOLD)
        for j, line in enumerate(sub):
            _text(d, lx + 14, yy - 5.0 - j * 7.6, line, 6.3, MUTED)
        yy -= 15 + 7.6 * len(sub)

    ly = yy - 6
    _text(d, lx, ly, "Stop-points", 8.0, FOREST, BOLD)
    for i, (r, label) in enumerate(sorted(STOPS.items())):
        yy = ly - 14 - i * 13
        d.add(Circle(lx + 4, yy + 2.4, 2.4, fillColor=GOLD,
                     strokeColor=colors.white, strokeWidth=0.5))
        _text(d, lx + 14, yy, f"R{r}  {label}  ({PER_ROUND * r})", 6.8, INK)

    for j, line in enumerate(("Ring order is the written",
                              "colour route. Ring width is",
                              "not a measured size.")):
        _text(d, lx, ly - 62 - j * 8.4, line, 6.2, MUTED)
    return d


# ---------------------------------------------------------------- growth chart

def growth_chart(width: float) -> Drawing:
    """Stitch count per round, 12 to 384, with the three stop-points marked."""
    h = width * 0.52
    d = Drawing(width, h)
    _panel(d, width, h)

    ml, mr, mb, mt = 32.0, 12.0, 26.0, 34.0
    pw, ph = width - ml - mr, h - mb - mt
    ymax = 384.0
    cs = counts()

    # gridlines
    for v in (0, 96, 192, 288, 384):
        y = mb + ph * v / ymax
        d.add(Line(ml, y, ml + pw, y, strokeColor=RULE, strokeWidth=0.5))
        _text(d, ml - 5, y - 2.4, str(v), 6.4, MUTED, anchor="end")

    slot = pw / TOTAL_ROUNDS
    bw = slot * 0.66
    for i, c in enumerate(cs):
        r = i + 1
        x = ml + i * slot + (slot - bw) / 2
        bh = ph * c / ymax
        col = GOLD if r in STOPS else (OAT if is_bobble(r) else FOREST)
        d.add(Rect(x, mb, bw, bh, fillColor=col,
                   strokeColor=FOREST_LT if col is OAT else None,
                   strokeWidth=0.4))
        if r in STOPS or r in (1, 10, 20, 30):
            _text(d, x + bw / 2, mb + bh + 3, str(c), 5.8,
                  FOREST, BOLD, anchor="middle")
        if r % 4 == 0 or r == 1:
            _text(d, x + bw / 2, mb - 9, str(r), 5.8, MUTED, anchor="middle")

    d.add(Line(ml, mb, ml + pw, mb, strokeColor=FOREST, strokeWidth=0.9))
    _text(d, ml + pw / 2, 4, "Round", 7.0, MUTED, anchor="middle")
    _text(d, ml, h - 12, "Stitch count per round", 8.6, FOREST, BOLD)

    # stop-point pills, top right
    px = ml + pw
    for r, label in sorted(STOPS.items(), reverse=True):
        tw = len(label) * 4.0 + 10
        px -= tw + 5
        d.add(Rect(px, h - 15, tw, 10, fillColor=GOLD, strokeColor=None,
                   rx=5, ry=5))
        _text(d, px + tw / 2, h - 12, label, 5.9, FOREST, BOLD,
              anchor="middle")
    return d


# ---------------------------------------------------------------- symbol chart

def _dc(g, cx, cy, ang, r0, r1, col=FOREST, bobble=False, lw=1.1):
    """One US dc / UK tr symbol drawn radially: stem, top bar, one slash."""
    ca, sa = math.cos(ang), math.sin(ang)
    px, py = -sa, ca  # perpendicular
    x0, y0 = cx + r0 * ca, cy + r0 * sa
    x1, y1 = cx + r1 * ca, cy + r1 * sa

    if bobble:
        mx, my = cx + (r0 + r1) / 2 * ca, cy + (r0 + r1) / 2 * sa
        rr = (r1 - r0) * 0.32
        g.add(Circle(mx, my, rr, fillColor=OAT, strokeColor=FOREST,
                     strokeWidth=0.9))
        g.add(Line(x0, y0, mx - rr * ca, my - rr * sa,
                   strokeColor=col, strokeWidth=lw))
        return

    g.add(Line(x0, y0, x1, y1, strokeColor=col, strokeWidth=lw))
    bar = (r1 - r0) * 0.22
    g.add(Line(x1 - bar * px, y1 - bar * py, x1 + bar * px, y1 + bar * py,
               strokeColor=col, strokeWidth=lw))
    # the single diagonal slash that distinguishes dc from hdc
    mr = (r0 + r1) / 2
    sx, sy = cx + mr * ca, cy + mr * sa
    s = (r1 - r0) * 0.17
    g.add(Line(sx - s * px - s * ca, sy - s * py - s * sa,
               sx + s * px + s * ca, sy + s * py + s * sa,
               strokeColor=col, strokeWidth=lw))


def symbol_chart(width: float, rounds: int = 8) -> Drawing:
    """One of the twelve repeats, rounds 1-N, in true crochet symbols."""
    h = width * 0.52
    d = Drawing(width, h)
    _panel(d, width, h, colors.white)

    cx, cy = width * 0.31, h * 0.055
    outer = min(width * 0.415, h * 0.80)
    hole = outer * 0.075
    band = (outer - hole) / rounds
    half = 90.0 / 2 / 1.0  # the wedge opens 90 deg for legibility

    g = Group()
    # guide arcs
    for r in range(rounds + 1):
        rad = hole + r * band
        pts = []
        for k in range(29):
            a = math.radians(45 + 90 * k / 28)
            pts += [cx + rad * math.cos(a), cy + rad * math.sin(a)]
        g.add(PolyLine(pts, strokeColor=RULE, strokeWidth=0.45))

    for r in range(1, rounds + 1):
        r0 = hole + (r - 1) * band + band * 0.14
        r1 = hole + r * band - band * 0.14
        n = r                     # one repeat of round r holds r stitches
        bob = is_bobble(r)
        # layout: [BO?] plain... then the increase pair in the last slot
        for k in range(n):
            frac = (k + 0.5) / n
            a = math.radians(45 + 90 * frac)
            last = (k == n - 1)
            if last and r >= 2:
                # increase: two stems from a shared base
                off = math.radians(90 / n * 0.20)
                _dc(g, cx, cy, a - off, r0, r1, FOREST_LT)
                _dc(g, cx, cy, a + off, r0, r1, FOREST_LT)
            else:
                _dc(g, cx, cy, a, r0, r1, FOREST, bobble=(bob and k == 0))

        lab_a = math.radians(45) - math.radians(5)
        lr = hole + (r - 0.5) * band
        _text(g, cx + lr * math.cos(lab_a) - 2, cy + lr * math.sin(lab_a),
              f"R{r}", 5.4, MUTED, anchor="end")

    g.add(Circle(cx, cy, hole, fillColor=colors.white, strokeColor=FOREST,
                 strokeWidth=1.0))
    d.add(g)

    # ---- legend
    lx = width * 0.70
    ly = h - 26
    _text(d, lx, ly + 16, "Symbols", 8.6, FOREST, BOLD)
    gl = Group()
    _dc(gl, lx + 6, ly - 4, math.radians(90), 0, 13, FOREST)
    d.add(gl)
    _text(d, lx + 18, ly + 2, "dc  (US)  /  tr  (UK)", 7.0, INK, BOLD)
    _text(d, lx + 18, ly - 6, "one plain stitch", 6.2, MUTED)

    g2 = Group()
    _dc(g2, lx + 6, ly - 34, math.radians(90), 0, 13, FOREST, bobble=True)
    d.add(g2)
    _text(d, lx + 18, ly - 28, "BO  bobble", 7.0, INK, BOLD)
    _text(d, lx + 18, ly - 36, "5 legs, 6 loops, counts as 1", 6.2, MUTED)

    g3 = Group()
    _dc(g3, lx + 3, ly - 64, math.radians(97), 0, 13, FOREST_LT)
    _dc(g3, lx + 9, ly - 64, math.radians(83), 0, 13, FOREST_LT)
    d.add(g3)
    _text(d, lx + 18, ly - 58, "increase", 7.0, INK, BOLD)
    _text(d, lx + 18, ly - 66, "2 sts worked into 1", 6.2, MUTED)

    _text(d, lx, ly - 92, "One repeat of twelve.", 6.4, MUTED)
    _text(d, lx, ly - 101, "Round r holds r stitches", 6.4, MUTED)
    _text(d, lx, ly - 110, "per repeat, so 12r in all.", 6.4, MUTED)
    _text(d, lx, ly - 123, "Ch 2 at the round start is", 6.2, MUTED)
    _text(d, lx, ly - 132, "never counted and is not", 6.2, MUTED)
    _text(d, lx, ly - 141, "drawn.", 6.2, MUTED)

    _text(d, 10, h - 13, "Stitch chart - one repeat", 8.6, FOREST, BOLD)
    return d


FIGURES = {
    "colour_route": colour_route_map,
    "growth_chart": growth_chart,
    "symbol_chart": symbol_chart,
}
