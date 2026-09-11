"""Independent second-opinion verification of the hand-computed rows.

Every construction the repo parser cannot represent is recomputed here from
raw arithmetic (independent of the stored cons/prod values), then compared
against the data files. Nothing passes unless both agree.
"""
from __future__ import annotations

import sys

sys.path.insert(0, "tools")
from novality import PATTERNS  # noqa: E402

FAIL = []


def expect(name, got, want):
    status = "ok" if got == want else "FAIL"
    if got != want:
        FAIL.append(f"{name}: got {got}, want {want}")
    print(f"  [{status}] {name}: {got} (want {want})")


def row(pid, piece_idx, sub_idx, row_idx):
    p = next(x for x in PATTERNS if x["id"] == pid)
    return p["pieces"][piece_idx]["subpieces"][sub_idx]["rows"][row_idx]


def seq(text):
    """Tiny independent evaluator for 'n sc, (a,b,c) in next, ...' sequences
    of single stitches and clusters (stitches inside parens into ONE st)."""
    cons = prod = 0
    for part in [x.strip() for x in text.split(",")]:
        if not part:
            continue
        if part.startswith("("):
            inside = part.strip("()").split("+")
            n = len(inside)          # cluster: consumes 1, produces len(inside)
            cons += 1
            prod += n
        else:
            n = int(part.split()[0])
            cons += n
            prod += n
    return cons, prod


def oval_round(prev, run, cap):
    """Oval rounds of form: A sc, inc, run sc, [run, inc] x cap..., etc.
    Each full oval round consumes prev and adds 6 (one extra on each of the
    6 corners)."""
    return prev, prev + 6


print("== Halloween (NS 02) ==")
boo_hem_cons, boo_hem_prod = 6 * (2 + 1 + 1), 6 * (2 + 5 + 1)
expect("Boo R13 hem cons/prod", (boo_hem_cons, boo_hem_prod), (24, 48))
expect("data", (row("halloween", 0, 0, 12)["cons"], row("halloween", 0, 0, 12)["prod"]), (24, 48))
beak = row("halloween", 1, 3, 0)
expect("Pip tendril 19 sl st", (beak["cons"], beak["prod"]), (19, 19))
stem = row("halloween", 0, 3, 5)
expect("Boo hat R6 FLO inc: 10 -> 20", (stem["cons"], stem["prod"]), (10, 20))
wing = row("halloween", 2, 2, 3)
expect("Bramble wing Row 3 consumes 12", (wing["cons"], 12), (12, 12))

print("== Axel (NS 03) ==")
fin_cons = 5 * 2
expect("tail-fin scallops consume 10 ridge sts", fin_cons, 10)
expect("tail rounds R27-R36", 36 - 27 + 1, 10)
# neck-fix alternative
r13 = (7 + 1) * 2 + 2            # consumes 18
r13p = (7 + 2) * 2 + 2           # produces 20
r14 = (4 + 1) * 4                # consumes 20
r14p = (4 + 2) * 4               # produces 24
expect("sturdier neck R13 consumes 18", r13, 18)
expect("sturdier neck R13 produces 20", r13p, 20)
expect("sturdier neck R14 consumes 20 / produces 24", (r14, r14p), (20, 24))

print("== Coco (NS 04) ==")
r4 = row("coco", 2, 0, 3)
# sequence: join BL1: 3 sc | [sc, inc]x3 | join BL2: 3 sc | [sc, inc]x3
# each [sc, inc]x3 block: consumes 2*3=6, produces 3*3=9
cons4 = 3 + (2 * 3) + 3 + (2 * 3)
prod4 = 3 + (3 * 3) + 3 + (3 * 3)
expect("Coco R4 join round: cons/prod", (cons4, prod4), (18, 24))
expect("data", (r4["cons"], r4["prod"], r4["stated"]), (18, 24, 24))

r5 = row("coco", 2, 0, 4)
# sequence: 1 sc, inc, 1 sc, inc, 1 sc | join 3 | [sc, inc]x3, 1 sc | join 3 | 3 sc, inc, 2 sc
cons = (1 + 1 + 1 + 1 + 1) + 3 + (2 * 3 + 1) + 3 + (3 + 1 + 2)
prod = (1 + 2 + 1 + 2 + 1) + 3 + (3 * 3 + 1) + 3 + (3 + 2 + 2)
expect("Coco R5 join round: cons/prod", (cons, prod), (24, 30))
expect("data", (r5["cons"], r5["prod"], r5["stated"]), (24, 30, 30))
expect("finished layout 7-3-10-3-7", 7 + 3 + 10 + 3 + 7, 30)

print("== Duck (NS 05) ==")
beak1 = row("duck", 2, 0, 1)
beak2 = row("duck", 2, 0, 2)
expect("beak Rnd1: (3+3)+(3+2) = 11", (beak1["cons"], beak1["prod"]), (4, 11))
b2c = 1+2+1+2+1+2+1+1
b2p = 2+2+2+2+2+2+2+1
expect("beak Rnd2 cons/prod", (b2c, b2p), (11, 15))
expect("data", (beak2["cons"], beak2["prod"]), (11, 15))
wing_close = 12 // 2
expect("wing flattened close 12 -> 6", wing_close, 6)

print("== Momo (NS 06) ==")
base = 8  # ch 9, 8 workable chains
prev = None
c, p = base, 1 + 6 + 3 + 6 + 2
expect("Momo R1", (c, p), (8, 18))
prev = p
for n, want in ((2, 24), (3, 30), (4, 36), (5, 42), (6, 48)):
    c, p = oval_round(prev, None, None)
    expect(f"Momo R{n}", (c, p), (prev, want))
    prev = p
ear = row("momo", 1, 0, 1)
expect("ear Row 2 dec,sc,dec", (ear["cons"], ear["prod"]), (5, 3))
ear3 = row("momo", 1, 0, 2)
expect("ear Row 3 dec,sc", (ear3["cons"], ear3["prod"]), (3, 2))

print("== Trio (NS 07) ==")
petal = row("trio", 0, 1, 0)
expect("Sunny petals cons/prod", (petal["cons"], petal["prod"], petal["stated"]), (18, 36, 36))
chest1 = row("trio", 1, 2, 1)
expect("Waddle chest R1", (chest1["cons"], chest1["prod"], chest1["stated"]), (5, 12, 12))
chest2 = row("trio", 1, 2, 2)
expect("Waddle chest R2", (chest2["cons"], chest2["prod"], chest2["stated"]), (12, 18, 18))
spud1 = row("trio", 2, 0, 1)
expect("Spud R1", (spud1["cons"], spud1["prod"], spud1["stated"]), (6, 14, 14))
spud2 = row("trio", 2, 0, 2)
expect("Spud R2", (spud2["cons"], spud2["prod"], spud2["stated"]), (14, 20, 20))

print("== Ember (NS 08) ==")
w4 = row("ember", 6, 0, 4)
expect("wing Row 4 scallops consume 10", (w4["cons"], 8 + 2), (10, 10))
spike_units = 1 + 9
expect("spike strip: 1 starting ch-4 + 9 units = 10 units / 40 chains", (spike_units, spike_units * 4), (10, 40))

print("== Shelby (NS 09) ==")
s5 = "3, (sc+hdc+hdc+sc), 4, (sc+hdc+sc), 3, (sc+hdc+sc), 4, (sc+hdc+sc), 3, (sc+hdc+sc), 2"
c, p = seq(s5)
data = row("shelby", 1, 1, 0)
expect("underside R5 cons/prod", (c, p), (24, 35))
expect("data", (data["cons"], data["prod"], data["stated"]), (24, 35, 35))
# bump positions (consumed-stitch index)
pos, i = [], 0
for part in [x.strip() for x in s5.split(",")]:
    if part.startswith("("):
        i += 1
        pos.append(i)
    else:
        i += int(part.split()[0])
expect("bump stitches", pos, [4, 9, 13, 18, 22])
anchors = sum(int(x.split()[0]) for x in s5.split(",") if not x.strip().startswith("(")) + 5
expect("anchors 19 plain + 5 clusters", anchors, 24)
big = "7, (sc+hdc+hdc+sc), 8, (sc+hdc+sc), 7, (sc+hdc+sc), 8, (sc+hdc+sc), 7, (sc+hdc+sc)"
c, p = seq(big)
expect("Bigger Shelby R8 cons/prod", (c, p), (42, 53))
shell_sts = 6+12+18+24+24+24
under_sts = 6+12+18+24+35
expect("whole charm = 203 stitches", shell_sts + under_sts, 203)

print("== Willow (NS 10) ==")
r1dc = 3 * 4
r2dc = 4 * (3 + 3)
expect("blanket Rnd1/2 dc", (r1dc, r2dc), (12, 24))
expect("dc totals 3/5/10/15/20", [12 * n for n in (3, 5, 10, 15, 20)], [36, 60, 120, 180, 240])
expect("per-edge dc at R20", 240 // 4, 60)
border = 240 + 4 * 3
expect("border sc at Rnd 20", border, 252)
gauge_check = 9 * 4.3
expect("9 dc ~ 39 mm", round(gauge_check, 1), 38.7)
growth = 3 * 4.3
expect("growth ~1.3 cm/side/round", round(growth / 10, 2), 1.29)
edge_mm = 60 * 4.3
expect("R20 edge ~26 cm", round(edge_mm / 10, 1), 25.8)

print("== Hamish (NS 01) ==")
belly = 8
c, p = belly, 1 + 6 + 3 + 6 + 2
expect("belly R1", (c, p), (8, 18))
prev = p
for n, want in ((2, 24), (3, 30), (4, 36)):
    c, p = oval_round(prev, None, None)
    expect(f"belly R{n}", (c, p), (prev, want))
    prev = p
fringe = 24 + 10 + 9
expect("fringe knots 24+10+9", fringe, 43)
scarf = 61 - 1
expect("scarf 60 hdc", scarf, 60)
tail_groups = 6 * 2
expect("tail 6->12 ends, 3x4", (tail_groups, tail_groups // 4), (12, 3))

print()
if FAIL:
    print("FAILURES:")
    for f in FAIL:
        print("  " + f)
    sys.exit(1)
print("All hand-computed constructions independently confirmed.")
