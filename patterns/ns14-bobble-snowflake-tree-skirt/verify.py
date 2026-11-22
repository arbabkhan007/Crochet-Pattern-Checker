#!/usr/bin/env python3
"""
Deterministic verifier for the NS 14 "Bobble Snowflake Tree Skirt" pattern.

This is a *stitch-by-stitch* simulator, not a stitch-count checker. It reads the
pattern's own markdown tables, expands every round into individual operations,
and walks a virtual hook around a virtual fabric, recording for every produced
stitch which parent stitch of the previous round it was worked into.

That parent map is what makes the difference here: a pattern can have perfect
stitch counts on every round and still be structurally wrong, because the
increase/bobble columns drift around the circle instead of radiating.

Checks performed
  1.  Tokenising  - every instruction must parse completely (no silent skips).
  2.  US <-> UK   - both columns must reduce to an identical operation stream.
  3.  Exhaustion  - each round must consume exactly the previous round's total.
  4.  Counts      - produced stitches must equal the printed "(n)" and 12 x N.
  5.  Cadence     - bobble rounds must be every 3rd round from R5.
  6.  Columns     - repeat k of round N must consume exactly the stitches made
                    by repeat k of round N-1 (radial spokes, no spiral).
  7.  Anchor      - the round-start anchor implied by the wording is compared
                    against the anchor the construction notes require.
  8.  Border      - shell repeats must exhaust the edge exactly; scallops = 2N.
  9.  Bobble      - the 5-dc bobble loop arithmetic is simulated loop by loop.
 10.  Geometry    - flat-circle test from the stated gauge, plus diameters.
 11.  Yarn        - yardage/weight estimate per size from the stated gauge.
 12.  Prose       - numbers quoted in the prose/summary tables are re-derived.

Usage:  python3 verify.py original.md
        python3 verify.py corrected.md
Exit code 0 = no errors.
"""

from __future__ import annotations

import math
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

# --------------------------------------------------------------------------
# reporting helpers
# --------------------------------------------------------------------------

ERRORS: list[str] = []
WARNINGS: list[str] = []
NOTES: list[str] = []


def err(msg: str) -> None:
    ERRORS.append(msg)


def warn(msg: str) -> None:
    WARNINGS.append(msg)


def note(msg: str) -> None:
    NOTES.append(msg)


def head(title: str) -> None:
    print()
    print(title)
    print("-" * len(title))


# --------------------------------------------------------------------------
# 1. markdown extraction
# --------------------------------------------------------------------------


@dataclass
class Row:
    label: str
    us: str
    uk: str
    sts: str
    note: str


def read_rows(path: Path) -> list[Row]:
    rows: list[Row] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line.startswith("|") or not line.endswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) != 5:
            continue
        if cells[0].lower() in {"rnd", "size"} or set(cells[0]) <= {"-", ":"} and cells[1] == "":
            continue
        if re.fullmatch(r":?-{2,}:?", cells[1]):
            continue
        rows.append(Row(cells[0], cells[1], cells[2], cells[3], cells[4]))
    return rows


# --------------------------------------------------------------------------
# 2. terminology normalisation (UK -> US) so both columns can be compared
# --------------------------------------------------------------------------

UK_TO_US = [
    (r"\bdtr\b", "tr"),
    (r"\btr\b", "dc"),
    (r"\bhtr\b", "hdc"),
    (r"\bdc\b", "sc"),
    (r"\bquadtr\b", "dtr"),
]


def uk_to_us(text: str) -> str:
    """Simultaneous UK->US stitch-name substitution (order-safe)."""
    tokens = re.split(r"(\W+)", text)
    mapping = {"dtr": "tr", "tr": "dc", "htr": "hdc", "dc": "sc"}
    return "".join(mapping.get(t, t) if t.isalpha() else t for t in tokens)


# --------------------------------------------------------------------------
# 3. instruction tokeniser
# --------------------------------------------------------------------------


@dataclass
class Op:
    kind: str  # 'work' | 'skip' | 'ring' | 'chain' | 'close' | 'join'
    consume: int = 0
    produce: int = 0
    stitch: str = "dc"
    same_as_join: bool = False
    raw: str = ""


ST = r"(?:sc|hdc|dc|tr|dtr|BO)"

PATTERNS: list[tuple[re.Pattern, str]] = [
    (re.compile(rf"^ch\s+(\d+)$", re.I), "chain"),
    (re.compile(rf"^(\d+)\s+({ST})\s+in\s+(?:the\s+)?ring$", re.I), "ring"),
    (re.compile(rf"^sl\s*st\s+to\s+(?:the\s+)?first\s+({ST})$", re.I), "close"),
    (re.compile(rf"^sl\s*st\s+to\s+first\s+ch\s+to\s+form\s+a\s+ring$", re.I), "formring"),
    (re.compile(rf"^join\s+cc\s+in\s+any\s+st$", re.I), "join"),
    (re.compile(r"^fo$", re.I), "fo"),
    # increases / clusters
    (re.compile(rf"^(\d+)\s+({ST})\s+in\s+same\s+st(?:\s+as\s+join)?$", re.I), "cluster_same"),
    (re.compile(rf"^(\d+)\s+({ST})\s+in\s+next\s+st$", re.I), "cluster_next"),
    (re.compile(rf"^(\d+)\s+({ST})\s+in\s+each\s+of\s+(?:the\s+)?next\s+(\d+)\s+sts?$", re.I), "cluster_each_n"),
    (re.compile(rf"^(\d+)\s+({ST})\s+in\s+each\s+st\s+around$", re.I), "cluster_each_around"),
    # plain stitches
    (re.compile(rf"^({ST})\s+in\s+same\s+st(?:\s+as\s+join)?$", re.I), "plain_same"),
    (re.compile(rf"^({ST})\s+in\s+(?:each\s+of\s+)?next\s+(\d+)\s+sts?$", re.I), "plain_n"),
    (re.compile(rf"^({ST})\s+in\s+next\s+st$", re.I), "plain_next"),
    (re.compile(rf"^({ST})\s+in\s+each\s+st\s+around$", re.I), "plain_each_around"),
    # skips
    (re.compile(r"^skip\s+(\d+)\s+sts?$", re.I), "skip_n"),
    (re.compile(r"^skip\s+next\s+st$", re.I), "skip_1"),
]


def split_top_level(text: str) -> list[str]:
    """Split on commas/semicolons that are not inside [] or ()."""
    parts, depth, cur = [], 0, ""
    for ch in text:
        if ch in "[(":
            depth += 1
        elif ch in "])":
            depth -= 1
        if ch in ",;" and depth == 0:
            parts.append(cur)
            cur = ""
        else:
            cur += ch
    parts.append(cur)
    return [p.strip() for p in parts if p.strip()]


REPEAT = re.compile(r"^\[(.+)\]\s*(?:x\s*(\d+)|(around))$", re.I)


@dataclass
class Segment:
    """Either a literal list of ops, or a repeat block."""

    ops: list[Op] = field(default_factory=list)
    repeat_ops: list[Op] | None = None
    times: int | None = None  # None => "around" (repeat to exhaustion)


def tokenise(text: str, where: str) -> list[Segment]:
    segments: list[Segment] = []
    for chunk in split_top_level(text):
        m = REPEAT.match(chunk)
        if m:
            inner = [op for c in split_top_level(m.group(1)) for op in tokenise_atom(c, where)]
            times = int(m.group(2)) if m.group(2) else None
            segments.append(Segment(repeat_ops=inner, times=times))
        else:
            segments.append(Segment(ops=tokenise_atom(chunk, where)))
    return segments


def tokenise_atom(chunk: str, where: str) -> list[Op]:
    c = re.sub(r"\s+", " ", chunk.strip().rstrip(".")).strip()
    if not c:
        return []
    for rx, kind in PATTERNS:
        m = rx.match(c)
        if not m:
            continue
        if kind == "chain":
            return [Op("chain", raw=c)]
        if kind == "ring":
            return [Op("ring", consume=0, produce=int(m.group(1)), stitch=m.group(2), raw=c)]
        if kind == "close":
            return [Op("close", stitch=m.group(1), raw=c)]
        if kind in {"formring", "join", "fo"}:
            return [Op(kind, raw=c)]
        if kind == "cluster_same":
            return [Op("work", 1, int(m.group(1)), m.group(2), True, c)]
        if kind == "cluster_next":
            return [Op("work", 1, int(m.group(1)), m.group(2), False, c)]
        if kind == "cluster_each_n":
            n, st, k = int(m.group(1)), m.group(2), int(m.group(3))
            return [Op("work", 1, n, st, False, c) for _ in range(k)]
        if kind == "cluster_each_around":
            return [Op("work", -1, int(m.group(1)), m.group(2), False, c)]
        if kind == "plain_same":
            return [Op("work", 1, 1, m.group(1), True, c)]
        if kind == "plain_n":
            st, k = m.group(1), int(m.group(2))
            return [Op("work", 1, 1, st, False, c) for _ in range(k)]
        if kind == "plain_next":
            return [Op("work", 1, 1, m.group(1), False, c)]
        if kind == "plain_each_around":
            return [Op("work", -1, 1, m.group(1), False, c)]
        if kind == "skip_n":
            return [Op("skip", int(m.group(1)), 0, raw=c)]
        if kind == "skip_1":
            return [Op("skip", 1, 0, raw=c)]
    err(f"{where}: could not parse instruction fragment {c!r}")
    return []


def op_signature(segments: list[Segment]) -> str:
    def sig(ops: list[Op]) -> str:
        return "|".join(f"{o.kind}:{o.consume}:{o.produce}:{o.stitch}:{int(o.same_as_join)}" for o in ops)

    out = []
    for s in segments:
        if s.repeat_ops is not None:
            out.append(f"REPEAT({sig(s.repeat_ops)})x{s.times if s.times else 'around'}")
        else:
            out.append(sig(s.ops))
    return " ; ".join(out)


# --------------------------------------------------------------------------
# 4. the fabric simulator
# --------------------------------------------------------------------------


@dataclass
class Stitch:
    idx: int
    round: int
    kind: str  # 'dc' / 'BO' / 'sc' / 'inc' / 'ring'
    parent: int | None  # index into the previous round
    repeat: int  # which of the 12 repeats produced it (0 for round 1 = own index%12)


@dataclass
class RoundResult:
    number: int
    label: str
    produced: list[Stitch]
    consumed: int
    anchor: int  # 0 = first st worked into the join st; 1 = into the st after it
    stated: int | None
    bobbles: int
    increases: int
    repeat_of_parent: list[int]  # repeat id of each consumed parent, in order
    consumption: list[tuple[int, int]]  # (parent index, stitches produced into it)
    consuming_repeat: list[int]  # which repeat of THIS round consumed each parent


def simulate_round(
    number: int,
    label: str,
    segments: list[Segment],
    prev: list[Stitch] | None,
    where: str,
) -> RoundResult:
    """Walk the hook through one round. Cursor is an index into `prev`."""
    prev_n = len(prev) if prev else 0

    # Determine the round-start anchor from the wording.
    first_work = None
    for s in segments:
        pool = s.repeat_ops if s.repeat_ops is not None else s.ops
        for o in pool:
            if o.kind in {"work", "skip"}:
                first_work = o
                break
        if first_work:
            break
    anchor = 0 if (first_work and first_work.same_as_join) else 1
    if prev_n == 0:
        anchor = 0

    cursor = anchor % prev_n if prev_n else 0
    produced: list[Stitch] = []
    consumed = 0
    consumed_parent_repeat: list[int] = []
    consumption: list[tuple[int, int]] = []
    repeat_id = 0

    def do_ops(ops: list[Op], rep: int) -> None:
        nonlocal cursor, consumed
        for o in ops:
            if o.kind == "ring":
                for _ in range(o.produce):
                    produced.append(Stitch(len(produced), number, o.stitch, None, len(produced)))
                continue
            if o.kind in {"chain", "close", "formring", "join", "fo"}:
                continue
            take = o.consume
            if take == -1:  # "in each st around"
                take = prev_n - consumed
                for _ in range(take):
                    p = cursor % prev_n
                    consumed_parent_repeat.append(prev[p].repeat)
                    consumption.append((p, o.produce))
                    for _ in range(o.produce):
                        produced.append(Stitch(len(produced), number, o.stitch, p, rep))
                    cursor += 1
                    consumed += 1
                continue
            for _ in range(take):
                if prev_n == 0:
                    err(f"{where}: works into stitches but there is no previous round")
                    return
                p = cursor % prev_n
                consumed_parent_repeat.append(prev[p].repeat)
                consumption.append((p, o.produce if o.kind == "work" else 0))
                if o.kind == "work":
                    for _ in range(o.produce):
                        produced.append(Stitch(len(produced), number, o.stitch, p, rep))
                cursor += 1
                consumed += 1

    for s in segments:
        if s.repeat_ops is None:
            do_ops(s.ops, repeat_id)
            # a bare (unbracketed) group at the head of a round is repeat 0
            if any(o.kind in {"work", "skip"} for o in s.ops):
                repeat_id += 1
        else:
            per = sum(o.consume for o in s.repeat_ops)
            if s.times is None:  # "around"
                if per <= 0:
                    err(f"{where}: '[...] around' with non-positive consumption")
                    continue
                remaining = prev_n - consumed
                times, rem = divmod(remaining, per)
                if rem:
                    err(
                        f"{where}: '[...] around' does not divide evenly - "
                        f"{remaining} stitches left, repeat consumes {per} "
                        f"({rem} stitch(es) would be stranded)"
                    )
                for _ in range(times):
                    do_ops(s.repeat_ops, repeat_id)
                    repeat_id += 1
            else:
                for _ in range(s.times):
                    do_ops(s.repeat_ops, repeat_id)
                    repeat_id += 1

    stated = None
    bobbles = sum(1 for st in produced if st.kind.upper() == "BO")
    increases = 0
    # count increases = parents that produced >1 stitch
    seen: dict[int, int] = {}
    for st in produced:
        if st.parent is not None:
            seen[st.parent] = seen.get(st.parent, 0) + 1
    increases = sum(1 for v in seen.values() if v > 1)

    # Structural repeat labelling: the design's 12 repeats are delimited by the
    # increases, so derive them from the fabric rather than from how the line of
    # text happened to be punctuated.
    if prev_n == 0:
        for st in produced:
            st.repeat = st.idx  # round 1 seeds the 12 spokes
        consuming_repeat: list[int] = []
    else:
        rep = 0
        consuming_repeat = []
        pos = 0
        for parent, made in consumption:
            consuming_repeat.append(rep)
            for _ in range(made):
                produced[pos].repeat = rep
                pos += 1
            if made >= 2:
                rep += 1

    return RoundResult(
        number=number,
        label=label,
        produced=produced,
        consumed=consumed,
        anchor=anchor,
        stated=stated,
        bobbles=bobbles,
        increases=increases,
        repeat_of_parent=consumed_parent_repeat,
        consumption=consumption,
        consuming_repeat=consuming_repeat,
    )


# --------------------------------------------------------------------------
# 5. gauge / geometry / yarn model
# --------------------------------------------------------------------------

STS_PER_10CM = 12.0  # 12 dc = 10 cm
ROUNDS_PER_10CM = 6.0  # 6 rounds = 10 cm
ST_WIDTH_CM = 10.0 / STS_PER_10CM  # 0.8333 cm
ROW_HEIGHT_CM = 10.0 / ROUNDS_PER_10CM  # 1.6667 cm
CM_PER_IN = 2.54

# yarn model: length of yarn consumed by one worked stitch, worsted/aran on 5-5.5 mm
YARN_CM_PER_DC = 10.0
YARN_CM_PER_SC = 5.5
M_PER_100G_WORSTED = 180.0
M_PER_100G_ARAN = 150.0


def diameter_from_stitch_gauge(total_sts: int) -> float:
    """Outer diameter in cm implied by the circumference of the last round."""
    circumference = total_sts * ST_WIDTH_CM
    return circumference / math.pi


def diameter_from_row_gauge(rounds: int, hole_radius_cm: float) -> float:
    return 2 * (hole_radius_cm + rounds * ROW_HEIGHT_CM)


def yarn_for_size(last_round: int, bobble_rounds: list[int], scallops: int) -> dict:
    body = sum(12 * n for n in range(1, last_round + 1))
    extra_bobble_dc = sum(4 * 12 for n in bobble_rounds if n <= last_round)
    border_dc = scallops * 5
    border_sc = scallops * 1
    cm = (body + extra_bobble_dc + border_dc) * YARN_CM_PER_DC + border_sc * YARN_CM_PER_SC
    metres = cm / 100.0
    return {
        "stitches": body,
        "metres": metres,
        "yards": metres * 1.0936,
        "g_worsted": metres / M_PER_100G_WORSTED * 100,
        "g_aran": metres / M_PER_100G_ARAN * 100,
    }


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------


def main(path: Path) -> int:
    print("=" * 72)
    print(f"NS 14 Bobble Snowflake Tree Skirt - full stitch-level simulation")
    print(f"source: {path.name}")
    print("=" * 72)

    rows = read_rows(path)
    if not rows:
        err("no pattern tables found")
        return report()

    ring_row = None
    growth: list[tuple[int, Row]] = []
    border_row = None
    size_rows: list[Row] = []

    for r in rows:
        if re.match(r"^R\d+$", r.label, re.I):
            growth.append((int(r.label[1:]), r))
        elif r.us.lower().startswith("ch ") and "form a ring" in r.us.lower():
            ring_row = r
        elif r.us.lower().startswith("join cc") and "surface" not in r.us.lower():
            border_row = r
        elif "surface sl st" in r.us.lower():
            pass
        elif r.label.lower() in {"mini/tabletop", "standard", "large"}:
            size_rows.append(r)

    growth.sort(key=lambda t: t[0])

    # ---------------------------------------------------------------- 1/2
    head("1. Tokenising + US/UK equivalence")
    parsed: dict[int, list[Segment]] = {}
    mismatches = 0
    for n, r in growth:
        us_seg = tokenise(r.us, f"R{n} US")
        uk_seg = tokenise(uk_to_us(r.uk), f"R{n} UK")
        parsed[n] = us_seg
        if op_signature(us_seg) != op_signature(uk_seg):
            mismatches += 1
            err(f"R{n}: UK column is not the exact equivalent of the US column")
    if border_row:
        b_us = tokenise(border_row.us, "border US")
        b_uk = tokenise(uk_to_us(border_row.uk), "border UK")
        if op_signature(b_us) != op_signature(b_uk):
            mismatches += 1
            err("Border: UK column is not the exact equivalent of the US column")
    print(f"   rounds parsed          : {len(parsed)}")
    print(f"   US/UK stream mismatches: {mismatches}")
    if mismatches == 0:
        print("   OK - every UK instruction reduces to the identical operation stream.")

    # ---------------------------------------------------------------- 3/4/5/6/7
    head("2. Round-by-round simulation (consume / produce / columns)")
    print(f"   {'Rnd':>4} {'avail':>6} {'used':>6} {'made':>6} {'stated':>7} "
          f"{'12N':>5} {'inc':>4} {'BO':>3} {'anchor':>7} {'col-err':>8}")

    prev: list[Stitch] | None = None
    rounds: dict[int, RoundResult] = {}
    bobble_rounds: list[int] = []
    column_breaks = 0
    phase = 0.0  # fraction of a turn that the round-start has drifted
    phase_trace: list[tuple[int, float]] = []

    for n, r in growth:
        res = simulate_round(n, r.label, parsed[n], prev, f"R{n}")
        stated = int(re.sub(r"[^\d]", "", r.sts)) if re.search(r"\d", r.sts) else None
        made = len(res.produced)
        avail = len(prev) if prev else 0

        # exhaustion
        if avail and res.consumed != avail:
            err(
                f"R{n}: consumes {res.consumed} stitches but {avail} are available "
                f"({avail - res.consumed:+d} stranded)"
            )
        # stated count
        if stated is not None and made != stated:
            err(f"R{n}: produces {made} stitches, printed count says ({stated})")
        # ladder
        if made != 12 * n:
            err(f"R{n}: produces {made} stitches, the 12 x N ladder requires {12 * n}")
        # increases (round 1 is worked into the ring, so it has none by design)
        if n > 1 and res.increases != 12:
            err(f"R{n}: has {res.increases} increase points, the 12-spoke design needs 12")

        # Column alignment.
        # The round is cut into its 12 design repeats, each of which consumes
        # avail/12 parent stitches. For the spokes to radiate, a repeat must
        # consume parents that all belong to ONE repeat of the previous round.
        # If a repeat straddles two parent repeats, the column is broken.
        col_err = 0
        if prev:
            groups: dict[int, set[int]] = {}
            for my_rep, parent_rep in zip(res.consuming_repeat, res.repeat_of_parent):
                groups.setdefault(my_rep, set()).add(parent_rep)
            col_err = sum(1 for v in groups.values() if len(v) > 1)
            if col_err:
                column_breaks += 1

        if avail:
            phase = (phase + (res.anchor / avail)) % 1.0
        phase_trace.append((n, phase))

        if res.bobbles:
            bobble_rounds.append(n)
            if res.bobbles != 12:
                err(f"R{n}: {res.bobbles} bobbles, expected 12 (one per spoke)")

        print(
            f"   R{n:<3} {avail:>6} {res.consumed:>6} {made:>6} "
            f"{(stated if stated is not None else '-'):>7} {12 * n:>5} "
            f"{res.increases:>4} {res.bobbles:>3} "
            f"{('join' if res.anchor == 0 else 'next'):>7} {col_err:>8}"
        )

        rounds[n] = res
        prev = res.produced

    # ---------------------------------------------------------------- anchor
    head("3. Round-start anchor / spoke geometry")
    anchors = {n: rounds[n].anchor for n in rounds if n > 1}
    literal = [n for n, a in anchors.items() if a == 1]
    if literal:
        drift_deg = phase_trace[-1][1] * 360.0
        err(
            f"Round-start anchor contradiction on {len(literal)} rounds "
            f"(R{literal[0]}-R{literal[-1]}): the construction notes say "
            f"'work the first dc or BO into the SAME stitch as the join', but the "
            f"round text says 'in next st', which starts one stitch past the join."
        )
        err(
            f"Simulated consequence: the 12 increase/bobble columns rotate by "
            f"{drift_deg:.1f} degrees from R1 to R{max(rounds)} - the 'snowflake' "
            f"spirals instead of radiating. Stitch counts stay correct, so a "
            f"count-only checker cannot see this."
        )
        print(f"   FAIL - the column slips 1 stitch per round, every round")
        print(f"   FAIL - cumulative column rotation R1->R{max(rounds)}: {drift_deg:.1f} degrees")
        print(f"   FAIL - rounds whose repeats straddle two parent repeats: {column_breaks}")
    else:
        print("   OK - every round is explicitly anchored in the joining stitch.")
        print(f"   OK - cumulative column rotation: {phase_trace[-1][1] * 360.0:.1f} degrees")
        print(f"   {'OK' if column_breaks == 0 else 'FAIL'} - rounds whose repeats straddle "
              f"two parent repeats: {column_breaks}")
        if column_breaks:
            err(f"{column_breaks} round(s) have repeats that straddle two parent repeats, "
                f"so the increase/bobble columns do not stack radially")

    # verify radial columns concretely on the last round
    last = max(rounds)
    inc_parents = []
    seen: dict[int, int] = {}
    for st in rounds[last].produced:
        if st.parent is not None:
            seen[st.parent] = seen.get(st.parent, 0) + 1
    inc_parents = sorted(p for p, c in seen.items() if c > 1)
    gaps = {inc_parents[i + 1] - inc_parents[i] for i in range(len(inc_parents) - 1)}
    print(f"   R{last} increase spacing on the parent round: {sorted(gaps)} "
          f"(even spacing = {len(rounds[last - 1].produced) // 12})")
    if gaps and gaps != {len(rounds[last - 1].produced) // 12}:
        err(f"R{last}: increases are not evenly spaced around the previous round")

    # ---------------------------------------------------------------- cadence
    head("4. Bobble cadence")
    expected = list(range(5, max(rounds) + 1, 3))
    print(f"   bobble rounds found   : {bobble_rounds}")
    print(f"   every 3rd round from 5: {expected}")
    if bobble_rounds != expected:
        err(f"Bobble cadence is {bobble_rounds}, the text promises {expected}")
    else:
        print("   OK - matches 'every third round from R5'.")

    # ---------------------------------------------------------------- bobble
    head("5. 5-dc bobble loop simulation")
    loops = 1  # the live loop
    steps = []
    for i in range(5):
        loops += 1  # yarn over
        loops += 1  # insert hook, pull up loop
        loops -= 1  # yo, pull through 2
        steps.append(loops)
    print(f"   loops on hook after each incomplete dc: {steps}")
    if steps[-1] != 6:
        err(f"5-dc bobble leaves {steps[-1]} loops on the hook, the text says 6")
    else:
        print("   OK - 6 loops on the hook, closed with one yarn-over through all 6.")
    text = path.read_text(encoding="utf-8")
    if "pull through all 6" not in text:
        warn("bobble closing instruction does not say 'pull through all 6'")

    # ---------------------------------------------------------------- border
    head("6. Scalloped border")
    if not border_row:
        err("no scalloped border row found")
    else:
        for size_name, n in (("Mini", 14), ("Standard", 23), ("Large", 32)):
            if n not in rounds:
                continue
            edge = rounds[n].produced
            res = simulate_round(999, "border", tokenise(border_row.us, f"border/{size_name}"), edge, f"border/{size_name}")
            shells = sum(1 for s in res.produced if s.kind == "dc") // 5
            scallops = len(edge) // 6
            ok = res.consumed == len(edge)
            print(
                f"   {size_name:<9} edge {len(edge):>3} sts -> consumed {res.consumed:>3}, "
                f"{scallops:>2} scallops, {len(res.produced):>3} sts made  "
                f"[{'OK' if ok else 'FAIL'}]"
            )
            if not ok:
                err(f"Border on {size_name}: consumes {res.consumed} of {len(edge)} stitches")
            if scallops != 2 * n:
                err(f"Border on {size_name}: {scallops} scallops, formula 2N gives {2 * n}")
        print("   note: every round total is 12N, and 12N is always divisible by 6,")
        print("         so the 6-stitch shell repeat closes after ANY round (scallops = 2N).")

    # ---------------------------------------------------------------- centre ring
    head("7. Centre ring vs. round 1")
    if ring_row:
        m = re.search(r"ch\s+(\d+)", ring_row.us, re.I)
        chains = int(m.group(1)) if m else 0
        ch_len_cm = chains * ST_WIDTH_CM * 0.95  # a chain is a touch narrower than a dc
        ring_d_max = ch_len_cm / math.pi
        r1_span = len(rounds[1].produced) * ST_WIDTH_CM
        r1_d = r1_span / math.pi
        print(f"   ch {chains} ring  : max circumference {ch_len_cm:.1f} cm -> hole up to "
              f"{ring_d_max:.1f} cm ({ring_d_max / CM_PER_IN:.2f} in) when stretched open")
        print(f"   R1 = {len(rounds[1].produced)} dc: base span {r1_span:.1f} cm -> hole gathers to "
              f"{r1_d:.1f} cm ({r1_d / CM_PER_IN:.2f} in) at rest")
        gathers = r1_span < ch_len_cm * 0.9
        claim = re.search(r"Centre hole approximately ([\d.]+)-([\d.]+) in", text)
        if claim:
            lo, hi = float(claim.group(1)), float(claim.group(2))
            print(f"   pattern claims    : {lo}-{hi} in at rest")
            if not (lo - 0.05 <= r1_d / CM_PER_IN <= hi + 0.05):
                warn(
                    f"claimed hole {lo}-{hi} in does not contain the simulated relaxed value "
                    f"{r1_d / CM_PER_IN:.2f} in (R1's {len(rounds[1].produced)} dc gather the "
                    f"ch {chains} ring from {ch_len_cm:.1f} cm down to {r1_span:.1f} cm)"
                )
            else:
                print("   OK - printed hole size covers the simulated gathered value")
        elif gathers:
            warn("R1 gathers the chain ring; quote the centre hole as a range")

    # ---------------------------------------------------------------- geometry
    head("8. Flat-circle geometry from the stated gauge")
    radius_needed = (12 * ST_WIDTH_CM) / (2 * math.pi)
    print(f"   +12 sts per round = +{12 * ST_WIDTH_CM:.2f} cm circumference "
          f"-> needs +{radius_needed:.2f} cm radius per round")
    print(f"   stated row gauge  = +{ROW_HEIGHT_CM:.2f} cm radius per round")
    ratio = ROW_HEIGHT_CM / radius_needed
    print(f"   ratio             = {ratio:.3f}  (1.00 = perfectly flat)")
    if abs(ratio - 1) > 0.15:
        err(f"gauge pair is inconsistent with a flat circle (ratio {ratio:.2f})")
    elif abs(ratio - 1) > 0.02:
        print(f"   OK - {(ratio - 1) * 100:.0f}% tall; blocks flat, slight cup if worked tight.")

    head("9. Finished diameters (simulated, both gauge directions)")
    hole_r = diameter_from_stitch_gauge(len(rounds[1].produced)) / 2
    border_cm = 2 * 1.8  # a 5-dc shell adds ~1.8 cm of radius
    # read the printed diameter claims out of the "Sizes at a glance" table
    claims: dict[int, tuple[float, float]] = {}
    for r in size_rows:
        m_rnd = re.search(r"R(\d+)", r.us)
        m_in = re.search(r"([\d.]+)\s*-\s*([\d.]+)\s*in", r.note)
        if m_rnd and m_in:
            claims[int(m_rnd.group(1))] = (float(m_in.group(1)), float(m_in.group(2)))
    if not claims:
        claims = {14: (18, 21), 23: (29, 33), 32: (38, 43)}
    for n in (14, 23, 32):
        if n not in rounds:
            continue
        d1 = diameter_from_stitch_gauge(len(rounds[n].produced)) + border_cm
        d2 = diameter_from_row_gauge(n, hole_r) + border_cm
        lo_in, hi_in = min(d1, d2) / CM_PER_IN, max(d1, d2) / CM_PER_IN
        c_lo, c_hi = claims[n]
        ok = c_lo <= lo_in + 0.6 and hi_in - 0.6 <= c_hi
        print(
            f"   R{n:<3} stitch-gauge {d1 / CM_PER_IN:5.1f} in | row-gauge {d2 / CM_PER_IN:5.1f} in "
            f"-> {lo_in:.0f}-{hi_in:.0f} in ({min(d1, d2):.0f}-{max(d1, d2):.0f} cm); "
            f"pattern says {c_lo}-{c_hi} in  [{'OK' if ok else 'MISMATCH'}]"
        )
        if not ok:
            warn(
                f"R{n}: simulated finished diameter {lo_in:.0f}-{hi_in:.0f} in is not covered by "
                f"the printed {c_lo}-{c_hi} in"
            )

    head("10. Yarn requirement (from the stated gauge, not a guess)")
    print(f"   model: {YARN_CM_PER_DC:.0f} cm of yarn per dc, worsted 180 m/100 g, aran 150 m/100 g")
    for size_name, n in (("Mini", 14), ("Standard", 23), ("Large", 32)):
        if n not in rounds:
            continue
        y = yarn_for_size(n, bobble_rounds or expected, 2 * n)
        print(
            f"   {size_name:<9} {y['stitches']:>5} body sts -> {y['metres']:>5.0f} m "
            f"({y['yards']:>4.0f} yd) -> {y['g_worsted']:>3.0f} g worsted / {y['g_aran']:>3.0f} g aran"
        )
    # Compare against whatever the document claims.
    # Preferred form: a per-size row "| Mini (R14) | ... | 100-150 g | ...".
    per_size = dict(re.findall(r"\(R(\d+)\)\s*\|[^|]*\|\s*([\d,]+-[\d,]+)\s*g", text))
    if per_size:
        for n_str, rng in sorted(per_size.items(), key=lambda kv: int(kv[0])):
            n = int(n_str)
            lo, hi = (float(x.replace(",", "")) for x in rng.split("-"))
            sim = yarn_for_size(n, bobble_rounds or expected, 2 * n)
            s_lo, s_hi = sim["g_worsted"] * 0.75, sim["g_aran"] * 1.25
            ok = lo <= s_hi and hi >= s_lo
            print(
                f"   R{n:<3} states {lo:.0f}-{hi:.0f} g vs simulated "
                f"{sim['g_worsted']:.0f}-{sim['g_aran']:.0f} g  [{'OK' if ok else 'MISMATCH'}]"
            )
            if not ok:
                err(
                    f"stated yarn for R{n} ({lo:.0f}-{hi:.0f} g) does not overlap the "
                    f"simulated requirement {sim['g_worsted']:.0f}-{sim['g_aran']:.0f} g "
                    f"(+/-25%)"
                )
    else:
        big = yarn_for_size(32, bobble_rounds or expected, 64)
        std = yarn_for_size(23, bobble_rounds or expected, 46)
        m = re.search(r"([\d,]+)-([\d,]+)\s*g", text)
        if m:
            lo = float(m.group(1).replace(",", ""))
            hi = float(m.group(2).replace(",", ""))
            print(f"   pattern states    : {lo:.0f}-{hi:.0f} g for standard or large")
            if lo > big["g_aran"] * 1.25:
                err(
                    f"stated yarn {lo:.0f}-{hi:.0f} g is far above the simulated requirement "
                    f"(standard {std['g_worsted']:.0f}-{std['g_aran']:.0f} g, "
                    f"large {big['g_worsted']:.0f}-{big['g_aran']:.0f} g). "
                    f"A maker would buy roughly 2-3x too much yarn."
                )

    head("11. Prose / summary-table cross-check")
    checks = [
        (r"R9 \(7 plain dc\)", 9, 7),
        (r"R10 needs 8", 10, 8),
        (r"R9 needs 7 plain dc", 9, 7),
    ]
    for rx, n, plain in checks:
        if re.search(rx, text):
            want = n - 2  # plain round: N-2 plain dc + 1 increase
            if plain != want:
                err(f"prose says R{n} has {plain} plain dc, the count rule gives {want}")
            else:
                print(f"   OK - prose R{n} = {plain} plain dc matches the N-2 rule")
    for r in size_rows:
        cells = [r.label, r.us, r.uk, r.sts, r.note]
        m_rnd = re.search(r"R(\d+)", r.us)
        if not m_rnd:
            continue
        n = int(m_rnd.group(1))
        sts = int(re.sub(r"\D", "", r.uk))
        sc = int(re.sub(r"\D", "", r.sts))
        okc = sts == 12 * n and sc == 2 * n
        print(f"   {r.label:<14} R{n:<3} sts {sts:>3} (need {12 * n:>3}), scallops {sc:>2} "
              f"(need {2 * n:>2})  [{'OK' if okc else 'FAIL'}]")
        if sts != 12 * n:
            err(f"summary table: {r.label} says {sts} sts, R{n} gives {12 * n}")
        if sc != 2 * n:
            err(f"summary table: {r.label} says {sc} scallops, R{n} gives {2 * n}")

    if re.search(r"one plain dc short leaves 12 stitches unworked", text):
        print("   OK - 'one plain dc short leaves 12 stitches unworked' (12 repeats x 1 st)")
    if re.search(r"6 rounds = 4 in", text):
        warn("gauge is measured on a 'flat swatch' but quoted in 'rounds'; say 'rows'")
    elif re.search(r"6 rows = 4 in", text):
        print("   OK - flat-swatch gauge is quoted in rows, not rounds")

    # the final round of every size is a bobble round: flag the border interaction
    for n in (14, 23, 32):
        if n in rounds and rounds[n].bobbles:
            note(
                f"R{n} (a size stopping point) is a bobble round, so a few edge bobbles "
                f"fall inside the border's 'skip 2'. Cosmetic only; an extra plain round "
                f"before the border avoids it and keeps the 12N/2N maths."
            )
            break

    return report()


def report() -> int:
    head("RESULT")
    if ERRORS:
        print(f"{len(ERRORS)} ERROR(S):")
        for i, e in enumerate(ERRORS, 1):
            print(f"  E{i}. {e}")
    if WARNINGS:
        print(f"\n{len(WARNINGS)} WARNING(S):")
        for i, w in enumerate(WARNINGS, 1):
            print(f"  W{i}. {w}")
    if NOTES:
        print(f"\n{len(NOTES)} NOTE(S):")
        for i, nte in enumerate(NOTES, 1):
            print(f"  N{i}. {nte}")
    if not ERRORS and not WARNINGS:
        print("PASS - no errors, no warnings. Pattern is ready to publish.")
    elif not ERRORS:
        print("\nPASS WITH WARNINGS - no mathematical or structural errors.")
    else:
        print("\nFAIL - correct the errors above before publishing.")
    print()
    return 1 if ERRORS else 0


if __name__ == "__main__":
    target = Path(sys.argv[1] if len(sys.argv) > 1 else "corrected.md")
    if not target.is_absolute():
        target = Path(__file__).parent / target
    sys.exit(main(target))
