#!/usr/bin/env python3
"""
Independent second opinion on the NS 14 pattern.

Deliberately shares NO code with verify.py and uses a different method:

  * repeats are expanded TEXTUALLY (the "[...] x 11" is literally rewritten into
    11 copies of the text) before anything is interpreted, so a bug in the
    segment/repeat machinery in verify.py cannot be reproduced here;
  * the column test is by ANCESTRY, not by repeat labels: every stitch's parent
    chain is followed all the way back to round 1, and the 12 increase points of
    every round must descend from the same 12 round-1 stitches. If the columns
    drift, the ancestor set changes from round to round.

Usage: python3 crosscheck.py corrected.md
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

FAILURES: list[str] = []


def check(cond: bool, msg: str) -> None:
    if not cond:
        FAILURES.append(msg)


# ---------------------------------------------------------------- extraction
def rows(md: str) -> list[list[str]]:
    out = []
    for line in md.splitlines():
        line = line.strip()
        if line.startswith("|") and line.endswith("|"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) == 5 and not re.fullmatch(r":?-{2,}:?", cells[1]):
                out.append(cells)
    return out


# ---------------------------------------------------------------- expansion
def expand(text: str, total_available: int | None = None) -> list[str]:
    """Textually blow the instruction out into one phrase per operation."""
    def repl(m: re.Match) -> str:
        body, times = m.group(1), int(m.group(2))
        return ", ".join([body] * times)

    text = re.sub(r"\[([^\]]+)\]\s*x\s*(\d+)", repl, text)

    # "[...] around" -> repeat until the stitches run out
    m = re.search(r"\[([^\]]+)\]\s*around", text)
    if m:
        body = m.group(1)
        before = text[: m.start()]
        consumed_before = sum(max(cost(p)[0], 0) for p in phrases(before))
        per = sum(cost(p)[0] for p in phrases(body))
        assert total_available is not None and per > 0
        remaining = total_available - consumed_before
        times, rem = divmod(remaining, per)
        check(rem == 0, f"'around' repeat leaves {rem} stitch(es) stranded")
        text = text[: m.start()] + ", ".join([body] * times) + text[m.end():]

    return phrases(text)


def phrases(text: str) -> list[str]:
    return [p.strip() for p in re.split(r"[,;]", text) if p.strip()]


# ---------------------------------------------------------------- costing
def cost(phrase: str) -> tuple[int, int, str]:
    """-> (stitches consumed, stitches produced, kind). Independent matcher."""
    p = phrase.strip().rstrip(".")
    low = p.lower()

    if re.fullmatch(r"ch \d+", low):
        return 0, 0, "chain"
    if re.fullmatch(r"fo", low):
        return 0, 0, "fo"
    if low.startswith("sl st to first"):
        return 0, 0, "close"
    if low.startswith("join cc in any st"):
        return 0, 0, "join"
    if "form a ring" in low:
        return 0, 0, "ring"

    m = re.fullmatch(r"(\d+) (dc|tr|sc|bo) in ring", low)
    if m:
        return 0, int(m.group(1)), "ringrow"

    m = re.fullmatch(r"skip (\d+) sts?", low)
    if m:
        return int(m.group(1)), 0, "skip"

    m = re.fullmatch(r"(\d+) (dc|tr|sc|bo) in each st around", low)
    if m:
        return -1, int(m.group(1)), "each_around"

    m = re.fullmatch(r"(dc|tr|sc|bo) in each st around", low)
    if m:
        return -1, 1, "each_around"

    m = re.fullmatch(r"(\d+) (dc|tr|sc|bo) in each of next (\d+) sts?", low)
    if m:
        return int(m.group(3)), int(m.group(1)) * int(m.group(3)), "multi"

    m = re.fullmatch(r"(\d+) (dc|tr|sc|bo) in (same st as join|same st|next st)", low)
    if m:
        return 1, int(m.group(1)), "inc"

    m = re.fullmatch(r"(dc|tr|sc|bo) in next (\d+) sts?", low)
    if m:
        return int(m.group(2)), int(m.group(2)), m.group(1)

    m = re.fullmatch(r"(dc|tr|sc|bo) in (same st as join|same st|next st)", low)
    if m:
        return 1, 1, m.group(1)

    FAILURES.append(f"cross-check cannot cost phrase {p!r}")
    return 0, 0, "?"


# ---------------------------------------------------------------- main
def main(path: Path) -> int:
    md = path.read_text(encoding="utf-8")
    table = rows(md)

    growth: dict[int, tuple[str, str, int]] = {}
    border_us = None
    for c in table:
        if re.fullmatch(r"R\d+", c[0], re.I):
            n = int(c[0][1:])
            stated = int(re.sub(r"\D", "", c[3]))
            growth[n] = (c[1], c[2], stated)
        elif c[1].lower().startswith("join cc in any st"):
            border_us = c[1]

    print(f"cross-check of {path.name}: {len(growth)} growth rounds\n")

    # parent[i] for round N = index into round N-1
    prev_parents: list[int | None] = []
    ancestry: dict[int, list[int]] = {}  # round -> root round-1 index per stitch
    inc_roots_by_round: dict[int, tuple[int, ...]] = {}
    bo_roots_by_round: dict[int, tuple[int, ...]] = {}
    prev_count = 0
    prev_inc_tail: list[bool] = []
    column_slip: dict[int, int] = {}

    for n in sorted(growth):
        us, uk, stated = growth[n]

        # ---- independent US/UK equivalence: normalise UK then compare costs
        uk_us = re.sub(r"\btr\b", "@DC@", uk)
        uk_us = re.sub(r"\bdc\b", "sc", uk_us).replace("@DC@", "dc")
        check(
            [cost(p) for p in expand(us)] == [cost(p) for p in expand(uk_us)],
            f"R{n}: UK column does not cost out identically to the US column",
        )

        ops = expand(us)
        anchor_same = any(
            re.search(r"in same st", o, re.I) for o in ops[:3]
        )
        cursor = 0 if (anchor_same or prev_count == 0) else 1

        parents: list[int | None] = []
        kinds: list[str] = []
        consumed = 0
        for o in ops:
            c, prod, kind = cost(o)
            if kind in {"chain", "fo", "close", "join", "ring"}:
                continue
            if kind == "ringrow":
                parents.extend([None] * prod)
                kinds.extend(["dc"] * prod)
                continue
            if kind == "each_around":
                c = prev_count - consumed
                per = prod          # prod is per-parent here
            else:
                per = (prod // c) if c > 0 else 0
            for _ in range(c):
                src = cursor % prev_count if prev_count else 0
                if kind != "skip":
                    for _ in range(per):
                        parents.append(src)
                        kinds.append(kind)
                cursor += 1
                consumed += 1

        made = len(parents)
        check(made == stated, f"R{n}: made {made}, printed ({stated})")
        check(made == 12 * n, f"R{n}: made {made}, ladder needs {12 * n}")
        if prev_count:
            check(consumed == prev_count,
                  f"R{n}: consumed {consumed} of {prev_count} available")

        # ---- ancestry back to round 1
        if n == 1:
            roots = list(range(made))
        else:
            prevroots = ancestry[n - 1]
            if any(p is not None and p >= len(prevroots) for p in parents):
                FAILURES.append(f"R{n}: works into stitches that do not exist")
                break
            roots = [prevroots[p] for p in parents]  # type: ignore[index]
        ancestry[n] = roots

        # ---- COLUMN CONTINUITY (the sharp test)
        # For the spokes to stack, the increase of each repeat must be worked
        # INTO the stitch the previous round's increase produced, and each
        # bobble must sit on the stitch immediately after one.
        # (The ancestor-set test below is rotation-invariant and therefore
        # cannot see a one-stitch slip - it is kept only as a sanity check.)
        tally: dict[int, int] = {}
        for p in parents:
            if p is not None:
                tally[p] = tally.get(p, 0) + 1
        inc_parents = sorted(p for p, v in tally.items() if v > 1)
        if n > 1:
            check(len(inc_parents) == 12, f"R{n}: {len(inc_parents)} increases, need 12")
            inc_roots_by_round[n] = tuple(sorted(ancestry[n - 1][p] for p in inc_parents))
        bo_idx = [i for i, k in enumerate(kinds) if k == "bo"]
        if bo_idx:
            check(len(bo_idx) == 12, f"R{n}: {len(bo_idx)} bobbles, need 12")
            bo_roots_by_round[n] = tuple(sorted(roots[i] for i in bo_idx))

        # flag the LAST stitch produced by any parent that received >1
        is_inc_tail = [False] * made
        run_parent, run_start = None, 0
        for i, par in enumerate(parents + [object()]):  # sentinel
            if par != run_parent:
                if run_parent is not None and (i - run_start) > 1:
                    is_inc_tail[i - 1] = True
                run_parent, run_start = par, i

        if n >= 3 and prev_inc_tail:
            off_inc = sum(1 for q in inc_parents if not prev_inc_tail[q])
            check(off_inc == 0,
                  f"R{n}: {off_inc} of 12 increases are NOT worked into the "
                  f"previous round's increase - the column has slipped")
            if bo_idx:
                bo_parents = sorted({parents[i] for i in bo_idx})
                off_bo = sum(
                    1 for q in bo_parents
                    if not prev_inc_tail[(q - 1) % prev_count]
                )
                check(off_bo == 0,
                      f"R{n}: {off_bo} of 12 bobbles are NOT on the stitch "
                      f"following an increase - the bobble column has slipped")
            column_slip[n] = off_inc

        prev_inc_tail = is_inc_tail
        prev_count = made
        prev_parents = parents

    # ---- the sharp column test
    slipped = sorted(n for n, v in column_slip.items() if v)
    print("Column continuity - is each round's increase worked into the stitch")
    print("the previous round's increase made?\n")
    print(f"   rounds tested            : {len(column_slip)}")
    print(f"   rounds with a slipped col: {len(slipped)}"
          + (f"  -> R{slipped[0]}-R{slipped[-1]}" if slipped else "  -> none"))
    if slipped:
        print(f"   increases off-column     : {sum(column_slip.values())} "
              f"of {12 * len(column_slip)}")
    print()

    # ---- the ancestry test (weak: rotation-invariant, kept as a sanity check)
    print("Increase-column ancestry (which round-1 stitches each round's 12")
    print("increases descend from). A necessary but NOT sufficient check.\n")
    sets = set(inc_roots_by_round.values())
    for n in sorted(inc_roots_by_round)[:4] + sorted(inc_roots_by_round)[-2:]:
        print(f"   R{n:<3} {inc_roots_by_round[n]}")
    print(f"\n   distinct ancestor sets across R2-R32: {len(sets)}")
    check(len(sets) == 1,
          f"increase columns drift: {len(sets)} distinct ancestor sets across the rounds")
    if len(sets) == 1:
        only = next(iter(sets))
        check(len(set(only)) == 12,
              f"the 12 increases share ancestors: {sorted(set(only))}")
        print(f"   all rounds share one set of {len(set(only))} distinct ancestors -> radial")

    bsets = set(bo_roots_by_round.values())
    print(f"\n   distinct bobble ancestor sets across the 10 bobble rounds: {len(bsets)}")
    check(len(bsets) == 1, f"bobble columns drift: {len(bsets)} distinct ancestor sets")

    # ---- border, independently
    print("\nBorder (independent expansion):")
    for name, n in (("Mini", 14), ("Standard", 23), ("Large", 32)):
        edge = 12 * n
        ops = expand(border_us, total_available=edge)
        consumed = sum(cost(o)[0] for o in ops)
        produced = sum(cost(o)[1] for o in ops)
        shells = sum(1 for o in ops if re.fullmatch(r"5 (dc|tr) in next st", o.strip(), re.I))
        check(consumed == edge, f"border/{name}: consumed {consumed} of {edge}")
        check(shells == 2 * n, f"border/{name}: {shells} scallops, need {2 * n}")
        print(f"   {name:<9} edge {edge:>3} -> consumed {consumed:>3}, "
              f"{shells:>2} scallops, {produced:>3} sts made")

    # ---- totals
    total = sum(12 * n for n in range(1, 33))
    check(total == 6336, f"total stitch count {total}")
    print(f"\nTotal body stitches R1-R32: {total} (closed form 6*32*33 = {6 * 32 * 33})")

    print()
    if FAILURES:
        print(f"CROSS-CHECK FAILED - {len(FAILURES)} issue(s):")
        for i, f in enumerate(FAILURES, 1):
            print(f"  {i}. {f}")
        return 1
    print("CROSS-CHECK PASSED - independent method agrees with verify.py")
    return 0


if __name__ == "__main__":
    target = Path(sys.argv[1] if len(sys.argv) > 1 else "corrected.md")
    if not target.is_absolute():
        target = Path(__file__).parent / target
    sys.exit(main(target))
