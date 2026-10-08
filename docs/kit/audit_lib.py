"""Shared independent stitch-count auditor for the Novality intake queue.

Parses markdown pipe tables, simulates every round/row from its instruction
text and compares the derived stitch count with the stated (n).  Anything the
generic grammar cannot parse is reported as UNPARSED so the per-pattern
auditor can add an explicit override or expectation.
"""
import re

TBL_RE = re.compile(r"^\|(.+)\|\s*$")


def parse_tables(text):
    tables, cur = [], []
    for line in text.splitlines():
        if TBL_RE.match(line.strip()):
            cells = [c.strip() for c in TBL_RE.match(line.strip()).group(1).split("|")]
            cur.append(cells)
        else:
            if len(cur) >= 2:
                tables.append(cur)
            cur = []
    if len(cur) >= 2:
        tables.append(cur)
    out = []
    for t in tables:
        hdr = t[0]
        rows = [r for r in t[1:] if not all(set(c) <= set("-: ") for c in r)]
        out.append((hdr, rows))
    return out


def _ops_make_consume(instr):
    """Return (made, consumed) for comma-op style instructions, else None."""
    s = instr.lower()
    s = re.sub(r"\bblo\b|\bflo\b", " ", s)
    s = s.replace(";", ",")
    total_m = total_c = 0
    saw_op = False
    for part in s.split(","):
        part = part.strip()
        if not part:
            continue
        m = re.fullmatch(r"(\d+)?\s*(sc|dc|hdc|tr|htr|dtr|sl st|slst)?\s*(x|×)?\s*(\d+)?", part)
        # explicit op forms
        if part in ("inc",):
            total_c += 1; total_m += 2; saw_op = True; continue
        if part in ("dec", "sc2tog", "dc2tog", "invdec", "dec x 1"):
            total_c += 2; total_m += 1; saw_op = True; continue
        m = re.fullmatch(r"(inc|dec|sc2tog|dc2tog|invdec)\s*x\s*(\d+)", part)
        if m:
            n = int(m.group(2))
            if m.group(1) == "inc":
                total_c += n; total_m += 2 * n
            else:
                total_c += 2 * n; total_m += n
            saw_op = True; continue
        m = re.fullmatch(r"(\d+)\s*(sc|dc|hdc|tr)(?:\s*(?:in|across|each st around))?", part)
        if m:
            k = int(m.group(1)); total_c += k; total_m += k; saw_op = True; continue
        if part in ("sc", "dc", "hdc"):
            total_c += 1; total_m += 1; saw_op = True; continue
        m = re.fullmatch(r"(\d+)\s*(sc|dc|hdc)\s*in\s*(?:next|same|last|each|the)?\s*\w*", part)
        if m:
            k = int(m.group(1)); total_c += k; total_m += k; saw_op = True; continue
        if part.startswith("sc in") or part.startswith("dc in"):
            return None
        if "sl st" in part or part.startswith("ch"):
            continue  # chains / slip stitches handled by callers
        return None
    if not saw_op:
        return None
    return total_m, total_c


def sim_round(instr, prev):
    """Derive (made, required_prev) from one instruction string.

    made == derived stitch count after the round; required_prev == the count
    the previous round must have had (None when unconstrained).
    """
    s = " ".join(instr.split())
    low = s.lower()
    low = re.sub(r"^(with|in|using)\b[^,]*?,\s*", "", low)
    low = re.sub(r"\s*\(.*?\)", "", low)
    low = low.replace(";", ",")
    low = re.sub(r"\bblo\b|\bflo\b", " ", low)
    low = re.sub(r"\(\d+ rnd\)$", "", low)
    low = re.sub(r"sc in same st as join and next (\d+) sts", lambda m: f"{int(m.group(1))+1} sc", low)
    low = re.sub(r"sc in next (\d+)", r"\1 sc", low)
    low = " ".join(low.split())
    unworked = 0
    mu = re.search(r"leave (?:final|the final) (\d+)?\s*(?:sts?|st)?\s*unworked", low)
    if mu:
        unworked = int(mu.group(1)) if mu.group(1) else 1
        low = re.sub(r";?\s*leave (?:final|the final) \d*\s*(?:sts?|st)?\s*unworked", "", low)
        low = " ".join(low.split())
    mch = re.fullmatch(r"sc in 2nd ch and next (\d+) ch", low)
    if mch:
        return int(mch.group(1)) + 1, None

    m = re.fullmatch(r"(\d+) sc in mr", low)
    if m:
        return int(m.group(1)), None
    m = re.fullmatch(r"(\d+) sc in mr \(yarn [a-z]\)", low)
    if m:
        return int(m.group(1)), None
    if low in ("inc in each st around", "inc in each st around.", "flo: inc in each st around"):
        return 2 * prev, prev
    if low in ("sc in each st around", "sc in each st around, then fo", "sc in each st around.",
               "blo sc around", "blo sc in each st around", "sc in each st around (3 rnd)",
               "blo: sc in each st around", "sc in each st around -", "dc in each st around"):
        return prev, prev
    m = re.fullmatch(r"\[(\d+) sc, (inc|dec|sc2tog|dc2tog|invdec)\] x (\d+)", low)
    if m:
        k, n = int(m.group(1)), int(m.group(3))
        if m.group(2) == "inc":
            return n * (k + 2), n * (k + 1)
        return n * (k + 1), n * (k + 2)
    m = re.fullmatch(r"\[sc, (inc|dec|sc2tog|dc2tog|invdec)\] x (\d+)", low)
    if m:
        n = int(m.group(2))
        if m.group(1) == "inc":
            return 3 * n, 2 * n
        return 2 * n, 3 * n
    m = re.fullmatch(r"(dec|sc2tog|dc2tog|invdec) x (\d+)", low)
    if m:
        n = int(m.group(2))
        return n, 2 * n
    m = re.fullmatch(r"inc x (\d+)", low)
    if m:
        n = int(m.group(1))
        return 2 * n, n
    # oval around a chain:  sc in 2nd ch ... other side ...  -> made = 2 * chain
    m = re.search(r"ch (\d+)", low)
    if m and ("2nd ch" in low) and ("other side" in low or "opposite side" in low or "along the opposite" in low):
        return 2 * int(m.group(1)), None
    res = _ops_make_consume(low)
    if res:
        made, consumed = res
        req = (consumed + unworked) if consumed else None
        return made, req
    return None, None


def stated_count(cell):
    m = re.search(r"\((\d+)\)", cell)
    return int(m.group(1)) if m else None


def audit_tables(text, overrides=None, skip_tables=()):
    """Return (problems, unparsed).  overrides: {(piece_hint, label): expected}"""
    overrides = overrides or {}
    problems, unparsed = [], []
    for hdr, rows in parse_tables(text):
        low_hdr = [h.lower() for h in hdr]
        if not any("rnd" in h or "row" in h for h in low_hdr[:2]):
            continue
        if any(k in " ".join(low_hdr) for k in skip_tables):
            continue
        i_sts = next((i for i, h in enumerate(low_hdr) if h.strip() in ("sts", "stitch count", "sts |")), None)
        i_ins = next((i for i, h in enumerate(low_hdr) if "instruction" in h or "us terms" in h or "exact instruction" in h), None)
        if i_sts is None or i_ins is None:
            continue
        prev = None
        for r in rows:
            if len(r) <= max(i_sts, i_ins):
                continue
            label, instr, sts_cell = r[0], r[i_ins], r[i_sts]
            stated = stated_count(sts_cell)
            key = label.strip().lower()
            if key in overrides:
                exp = overrides[key]
                if stated is not None and stated != exp:
                    problems.append(f"{label}: stated {stated} != expected {exp}")
                if exp is not None:
                    prev = exp
                continue
            made, req = sim_round(instr, prev if prev is not None else 0)
            if made is None:
                unparsed.append((label, instr, stated))
                if stated is not None:
                    prev = stated
                continue
            if req is not None and prev is not None and req != prev:
                problems.append(f"{label}: needs prev {req} but previous round made {prev} ({instr})")
            if stated is not None and stated != made:
                problems.append(f"{label}: stated ({stated}) != derived {made} ({instr})")
            if stated is not None:
                prev = stated
            elif made is not None:
                prev = made
    return problems, unparsed
