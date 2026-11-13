"""Sanity checks for the corrected user-supplied NS01-NS17 patterns.
Run: python verify.py  (from this folder or anywhere)
Checks file inventory, the corrected critical sequences, and arithmetic
of the sequences that were broken in the supplied versions.
Written audit only - not physical test-crocheting.
"""
from pathlib import Path
import re, sys

ROOT = Path(__file__).resolve().parent
errors = []

def check(cond, msg):
    if not cond:
        errors.append(msg)

files = sorted(ROOT.glob("NS??_corrected.md"))
check(len(files) == 17, f"expected 17 pattern files, found {len(files)}")
texts = {p.name: p.read_text() for p in files}
all_text = "\n".join(texts.values())

# --- arithmetic helpers: (kind, n) terms -> (consumed, produced)
def seq(terms):
    consumed = sum(n * (2 if k == "dec" else 1) for k, n in terms)
    produced = sum(n * (2 if k == "inc" else 1) for k, n in terms)
    return consumed, produced

# NS06 corrected R5 must consume 44 and produce 48 (was 36 -> 40, claimed 48)
c, p = seq([("sc",11),("inc",1),("sc",1),("inc",1),("sc",11),("inc",1),("sc",1),("inc",1),("sc",16)])
check((c, p) == (44, 48), f"NS06 R5 arithmetic {c}->{p} != 44->48")
check("11 sc, inc, sc, inc, 11 sc, inc, sc, inc, 16 sc (48)" in texts["NS06_corrected.md"], "NS06 corrected R5 missing")

# NS16 corrected Foot R2 must consume 23 and produce 20 (was 19 -> 16, claimed 20)
c, p = seq([("sc",7),("dec",1),("sc",5),("dec",1),("sc",5),("dec",1)])
check((c, p) == (23, 20), f"NS16 Foot R2 arithmetic {c}->{p} != 23->20")
check("7 sc, dec, 5 sc, dec, 5 sc, dec" in texts["NS16_corrected.md"], "NS16 corrected Foot R2 missing")
check("3 + 5 + 10 + 5 = 23" in texts["NS16_corrected.md"], "NS16 pickup total missing")

# NS04 R5 must consume 24 and produce 30, front legs clear of back legs (R4 sts 10-12)
c, p = seq([("sc",1),("inc",1)]*4 + [("sc",5),("join",3),("sc",3),("inc",1),("join",3),("inc",1)])
check((c, p) == (24, 30), f"NS04 R5 arithmetic {c}->{p} != 24->30")
check("R4 sts 14–16" in texts["NS04_corrected.md"] and "R4 sts 21–23" in texts["NS04_corrected.md"], "NS04 corrected join map missing")

# NS14 border repeat 6 sts divides all stopping counts; mini = 28 scallops
for sts, scallops in [(168,28),(288,48),(360,60),(384,64)]:
    check(sts // 6 == scallops and sts % 6 == 0, f"NS14 {sts} sts scallop math")
check("28 scallops on R13" in texts["NS14_corrected.md"], "NS14 mini scallop correction missing")
check("6.4 cm" in texts["NS14_corrected.md"], "NS14 centre opening correction missing")

# NS09 symmetry anchors + totals
plain = 3 + 4 + 3 + 5 + 3 + 1  # plain sc between the 5 fan stitches
check(plain + 5 == 24, "NS09 standard underside must consume 24 front loops")
check(plain + 4 + 4 * 3 == 35, "NS09 standard underside must produce 35 sts (head fan 4 + 4 flipper fans x3)")

# forbidden supplied-version instructions must not survive as instructions
for bad in [
    "2 sc, dec, 5 sc, dec, 5 sc, dec, 1 sc`, sl st to first sc (20)",
    "12 sc, inc, 2 sc, inc, 14 sc, inc, 2 sc, inc, 2 sc (48)",
    "Total ~16–18 m / ~6 g across all 3 pals",
    "insert 7.5 cm base disc inside now",
    "168 sts / 24 scallops",
    "preserves full 5 cm hole",
]:
    check(bad not in all_text, f"supplied-version defect still present: {bad!r}")

if errors:
    print("FAIL")
    for e in errors:
        print(" -", e)
    sys.exit(1)
print(f"OK: 17 files; NS06 R5 44->48; NS16 Foot R2 23->20; NS04 R5 24->30 with clear join map; NS14 scallops 28/48/60/64; 0 errors")
