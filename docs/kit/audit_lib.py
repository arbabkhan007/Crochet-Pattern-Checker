"""Shared independent stitch-count auditor for the Novality intake queue (v2).

Parses markdown pipe tables (blank lines between rows tolerated), simulates
every round/row from its instruction text and compares the derived stitch
count with the stated (n).  Constructs covered: magic-ring starts, inc/dec
families, bracket repeats, bobble (BO) repeats, shell/cluster groups into one
stitch, slip-stitch anchors, counts-as turning chains, chain ovals (via the
Found. chain row), foundation-chain pickups and turned subset rows.  Anything
still unparsed is reported so the per-pattern auditor can add an override.
"""
import re

TBL_RE = re.compile(r"^\|(.+)\|\s*$")
_ST = r"(?:sc|dc|hdc|tr|dtr|htr)"


def parse_tables(text):
    tables, cur = [], []
    for line in text.splitlines():
        if TBL_RE.match(line.strip()):
            cells = [c.strip() for c in TBL_RE.match(line.strip()).group(1).split("|")]
            cur.append(cells)
        elif not line.strip():
            continue
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


_TOK = r"(?:\d+\s+)?(?:sl st|sc|dc|hdc|tr|dtr|htr|ch\s*\d+|picot)"
_GRP = re.compile(_TOK + r"(?:,\s*" + _TOK + r")+")


def _strip_parens(low):
    out, i = "", 0
    while i < len(low):
        ch = low[i]
        if ch == "(":
            j = i + 1
            depth = 1
            while j < len(low) and depth:
                if low[j] == "(":
                    depth += 1
                if low[j] == ")":
                    depth -= 1
                j += 1
            inner = low[i + 1:j - 1]
            keep = "counts as first" in inner or bool(_GRP.fullmatch(inner.strip()))
            if keep:
                out += low[i:j]
            i = j
        else:
            out += ch
            i += 1
    return out


def _split_ops(s):
    parts, depth, cur = [], 0, ""
    for ch in s:
        if ch in "([":
            depth += 1
        if ch in ")]":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append(cur.strip())
            cur = ""
        else:
            cur += ch
    if cur.strip():
        parts.append(cur.strip())
    return parts


def _group_count(group):
    return _count_stitches(group) + len(re.findall(r"\bsl st\b", group))


def _count_stitches(group):
    total = 0
    for cnt, _st in re.findall(r"(?:(\d+)\s+)?(" + _ST.strip("()?:") .replace("|", "|") + r")\b", group):
        total += int(cnt) if cnt else 1
    return total


def _ops_make_consume(instr):
    """(made, consumed) for comma-op instructions, else None."""
    s = instr.lower()
    s = re.sub(r"\bblo\b|\bflo\b", " ", s)
    s = s.replace(";", ",")
    s = s.replace(":", ",")
    s = re.sub(r",?\s*\bthen\b\s*", ", ", s)
    total_m = total_c = 0
    saw_op = False
    for part in _split_ops(s):
        part = part.strip()
        if not part:
            continue
        if part == "inc":
            total_c += 1; total_m += 2; saw_op = True; continue
        m = re.fullmatch(r"join (?:bl|fl)\s*\d\s+(\d+) sc", part)
        if m:
            k = int(m.group(1)); total_c += k; total_m += k; saw_op = True; continue
        m = re.fullmatch(r"inc in each of next (\d+)", part)
        if m:
            k = int(m.group(1)); total_c += k; total_m += 2 * k; saw_op = True; continue
        m = re.fullmatch(_ST + r"\s+in\s+(?:remaining|the remaining)?\s*(\d+)", part)
        if m:
            k = int(m.group(1)); total_c += k; total_m += k; saw_op = True; continue
        m = re.fullmatch(_ST + r"\s+in\s+(\d+)", part)
        if m:
            k = int(m.group(1)); total_c += k; total_m += k; saw_op = True; continue
        if part in ("dec", "sc2tog", "dc2tog", "invdec"):
            total_c += 2; total_m += 1; saw_op = True; continue
        if part in ("bo", "bo in next st"):
            total_c += 1; total_m += 1; saw_op = True; continue
        m = re.fullmatch(r"(inc|dec|sc2tog|dc2tog|invdec|bo)\s*(?:in next st)?\s*x\s*(\d+)", part)
        if m:
            n = int(m.group(2))
            if m.group(1) == "inc":
                total_c += n; total_m += 2 * n
            elif m.group(1) == "bo":
                total_c += n; total_m += n
            else:
                total_c += 2 * n; total_m += n
            saw_op = True; continue
        m = re.fullmatch(r"\[([^\]]+)\]\s*x\s*(\d+)", part)
        if m:
            inner = _ops_make_consume(m.group(1))
            if inner is None:
                return None
            total_m += inner[0] * int(m.group(2))
            total_c += inner[1] * int(m.group(2))
            saw_op = True; continue
        m = re.fullmatch(r"\(([^)]+)\)\s*(?:all )?in (?:next|same|the next) st", part)
        if m:
            total_c += 1; total_m += _group_count(m.group(1)); saw_op = True; continue
        m = re.fullmatch(r"\(([^)]+)\)\s+in each of (?:the )?(\d+)\s+[a-z0-9-]+ spaces?", part)
        if m:
            k = int(m.group(2))
            total_m += _group_count(m.group(1)) * k; saw_op = True; continue
        m = re.fullmatch(r"(\d+)\s*sl st\b.*", part) or re.fullmatch(
            r"sl st in (?:next|first|last) (\d+).*", part)
        if m:
            k = int(m.group(1))
            total_c += k; total_m += k; saw_op = True; continue
        if re.match(r"sl st (?:to|in) (?:the )?(?:top|base|beginning)(?!\s*\d)", part) \
                or re.match(r"sl st (?:to|in) first (?!\d)", part) \
                or re.match(r"sl st in next \d+ dc and into", part) \
                or "to form a ring" in part or "and into the next corner" in part:
            continue
        if part.startswith("sl st") and " in " in part:
            total_c += 1; total_m += 1; saw_op = True; continue
        if part.startswith("sl st to") or part in ("sl st", "sl st, fo", "fo", "fo.",
                                                   "fasten off"):
            continue
        if part in ("mr", "magic ring", "do not turn", "do not turn.") or \
                part.startswith("do not "):
            continue
        m = re.fullmatch(r"sc in 2nd ch and next (\d+) ch", part)
        if m:
            total_m += int(m.group(1)) + 1; saw_op = True; continue
        if part.startswith("ch") and "counts as" not in part:
            continue
        if "skip next" in part or part.startswith("skip"):
            continue
        m = re.fullmatch(r"(\d+)\s*" + _ST + r"(?:\s*(?:in|across|around|each st around|"
                         r"in the ring|in next st|in same st|in last ch|in next ch))?", part)
        if m:
            k = int(m.group(1)); total_c += k; total_m += k; saw_op = True; continue
        if re.fullmatch(_ST, part):
            total_c += 1; total_m += 1; saw_op = True; continue
        m = re.fullmatch(r"(\d+)\s*" + _ST + r"\s+in\s+[^,]+", part)
        if m:
            k = int(m.group(1)); total_c += k; total_m += k; saw_op = True; continue
        m = re.fullmatch(r"(\d+)\s+(?:side|instep|heel-centre|heel-center)\s+sc", part)
        if m:
            total_m += int(m.group(1)); saw_op = True; continue
        if re.search(r"(?:side|instep|heel-centre)\s+sc", part):
            m2 = re.search(r"(\d+)\s*(?:side|instep|heel-centre)\s+sc", part)
            if m2:
                total_m += int(m2.group(1)); saw_op = True; continue
        return None
    if not saw_op:
        return None
    return total_m, total_c


def sim_round(instr, prev):
    """(made, required_prev); either may be None.  prev=None means the row
    starts a table fragment, so prev-dependent rules report unknown."""
    s = " ".join(instr.split())
    low = s.lower()
    low = re.sub(r"^(with|in|using)\b[^:\n]*:\s*", "", low)
    low = re.sub(r"^(with|in|using)\s+[a-z0-9&#/ -]+,\s*", "", low)
    low = _strip_parens(low)
    low = low.replace(";", ",")
    low = re.sub(r"\bblo\b|\bflo\b", " ", low)
    low = re.sub(r"^flo\s*:\s*|^\blo\s*:\s*", "", low)
    low = low.replace(":", " ")
    unworked = 0
    mu = re.search(r"leave (?:final|the final) (\d+)?\s*(?:sts?|st)?\s*unworked", low)
    if mu:
        unworked = int(mu.group(1)) if mu.group(1) else 1
        low = re.sub(r";?\s*leave (?:final|the final) \d*\s*(?:sts?|st)?\s*unworked", "", low)
    counts_as = 0
    if re.search(r"ch \d+ \(counts as first", low):
        counts_as = 1
        low = re.sub(r"ch \d+ \(counts as first [a-z]+\),?\s*", "", low)
    low = re.sub(r",?\s*(?:;|,)\s*(?:change|switch)\b.*$", "", low)
    low = re.sub(r",?\s*(?:;|,)\s*stop here$", "", low)
    low = re.sub(r",?\s*ch [12], turn$", "", low)
    low = re.sub(r"^ch [12], turn,?\s*", "", low)
    low = re.sub(r"^from the 2nd ch:\s*", "", low)
    low = re.sub(r"\(\d+ rnd\)$", "", low)
    low = re.sub(r"sc in same st as join and next (\d+) sts", lambda m: f"{int(m.group(1))+1} sc", low)
    low = re.sub(r"sc in next (\d+)", r"\1 sc", low)
    low = " ".join(low.split())

    m = re.fullmatch(r"(\d+) sc in mr", low)
    if m:
        return int(m.group(1)), None
    if low in ("inc in each st around", "inc in each st around."):
        return (2 * prev, prev) if prev is not None else (None, None)
    if re.fullmatch(r"sc in each st around until .+", low):
        return (prev, prev) if prev is not None else (None, None)
    m = re.fullmatch(r"ch (\d+), sc in 2nd ch from hook and across.*", low)
    if m:
        return int(m.group(1)) - 1, None
    m = re.fullmatch(r"ch (\d+) ring; sc in each ch.*", low)
    if m:
        return int(m.group(1)), None
    if low in ("sc in each st around", "sc in each st around, then fo", "sc in each st around.",
               "blo sc around", "blo sc in each st around", "blo: sc in each st around",
               "sc in each st across", "blo sc in each st across", "sc in each st across, turn",
               "sc in each st around -", "dc in each st around", "sc around",
               "sl st in each st across", "sl st in each st around",
               "hdc across", "dc across", "sc across", "hdc in each st across",
               "dc in each st across"):
        return (prev, prev) if prev is not None else (None, None)
    m = re.fullmatch(r"\[(\d+) sc, (inc|dec|sc2tog|dc2tog|invdec)\] x (\d+)", low)
    if m:
        k, n = int(m.group(1)), int(m.group(3))
        if m.group(2) == "inc":
            return n * (k + 2), n * (k + 1)
        return n * (k + 1), n * (k + 2)
    m = re.fullmatch(r"\[sc, (inc|dec|sc2tog|dc2tog|invdec)\] x (\d+)", low)
    if m:
        n = int(m.group(2))
        return (3 * n, 2 * n) if m.group(1) == "inc" else (2 * n, 3 * n)
    m = re.fullmatch(r"(dec|sc2tog|dc2tog|invdec) x (\d+)", low)
    if m:
        return int(m.group(2)), 2 * int(m.group(2))
    m = re.fullmatch(r"inc x (\d+)", low)
    if m:
        return 2 * int(m.group(1)), int(m.group(1))
    m = re.search(r"ch (\d+)", low)
    if m and ("2nd ch" in low) and ("other side" in low or "opposite side" in low
                                   or "along the opposite" in low):
        return 2 * int(m.group(1)), None
    if "2nd ch" in low or "in the ring" in low or "in ring" in low or "corner space" in low \
            or "ch-5 space" in low or "side sc" in low or "instep sc" in low \
            or "heel-centre sc" in low:
        res = _ops_make_consume(low)
        if res:
            return res[0] + counts_as, None
        return None, None
    m = re.fullmatch(r"sc in each of (\d+) foundation chains around", low)
    if m:
        return int(m.group(1)), None
    m = re.fullmatch(r"sc in 2nd ch and next (\d+) ch", low)
    if m:
        return int(m.group(1)) + 1, None
    res = _ops_make_consume(low)
    if res:
        made, consumed = res
        return made + counts_as, (consumed + unworked) if consumed else None
    return None, None


def stated_count(cell):
    m = re.search(r"\((\d+)\)", cell)
    return int(m.group(1)) if m else None


def is_round_header(hdr):
    low = [h.lower() for h in hdr]
    return bool(low) and any("rnd" in h or "row" in h for h in low[:2])


def audit_tables(text, overrides=None, skip_tables=()):
    overrides = overrides or {}
    problems, unparsed = [], []
    for hdr, rows in parse_tables(text):
        if not is_round_header(hdr):
            continue
        low_hdr = [h.lower() for h in hdr]
        if any(k in " ".join(low_hdr) for k in skip_tables):
            continue
        i_sts = next((i for i, h in enumerate(low_hdr) if h.strip() in ("sts", "stitch count")), None)
        i_ins = next((i for i, h in enumerate(low_hdr)
                      if "instruction" in h or "us terms" in h or "exact instruction" in h), None)
        if i_sts is None or i_ins is None:
            continue
        prev = None
        last_chain = None
        for r in rows:
            if len(r) <= max(i_sts, i_ins):
                continue
            label, instr, sts_cell = r[0], r[i_ins], r[i_sts]
            if label.strip().lower().startswith("[ ]") or label.strip().lower().startswith("[x]"):
                continue
            stated = stated_count(sts_cell)
            key = label.strip().lower()
            il0 = instr.strip().lower()
            mch = re.fullmatch(r"ch (\d+)", il0) or \
                re.search(r"^ch (\d+), sl st to first ch to form a ring", il0)
            if mch:
                last_chain = int(mch.group(1))
                continue
            mcf = re.search(r"^ch (\d+);\s*from the 2nd ch, work (\d+) sc in each chain", il0)
            if mcf:
                made = int(mcf.group(2)) * (int(mcf.group(1)) - 1)
                if stated is not None and stated != made:
                    problems.append(f"{label}: {mcf.group(2)} sc in each of ch "
                                    f"{int(mcf.group(1))-1} should make {made}, stated {stated}")
                prev = stated if stated is not None else made
                continue
            if key in overrides:
                exp = overrides[key]
                if exp is None:
                    prev = stated
                    continue
                if stated is not None and stated != exp:
                    problems.append(f"{label}: stated {stated} != expected {exp}")
                prev = exp
                continue
            if last_chain and re.search(r"2nd ch", instr.lower()) and stated is not None:
                around = re.search(r"other side|opposite side|along the other|rotate|last loop|last ch",
                                   instr.lower())
                expect = 2 * last_chain if around else last_chain - 1
                if stated != expect:
                    problems.append(f"{label}: {'oval' if around else 'flat row'} around "
                                    f"ch {last_chain} should make {expect}, stated {stated}")
                prev = stated
                last_chain = None
                continue
            il = instr.strip().lower()
            mce = re.search(r"(\d+) sc in each chain", il) if last_chain else None
            if last_chain and mce:
                made = int(mce.group(1)) * (last_chain - 1)
                if stated is not None and stated != made:
                    problems.append(f"{label}: {mce.group(1)} sc in each of ch "
                                    f"{last_chain}-1 should make {made}, stated {stated}")
                prev = stated if stated is not None else made
                last_chain = None
                continue
            if last_chain and re.fullmatch(r"sc in each ch around", il):
                if stated is not None and stated != last_chain:
                    problems.append(f"{label}: ring of ch {last_chain} should make "
                                    f"{last_chain}, stated {stated}")
                prev = stated if stated is not None else last_chain
                last_chain = None
                continue
            made, req = sim_round(instr, prev)
            if made is None:
                unparsed.append((label, instr, stated))
                if stated is not None:
                    prev = stated
                continue
            if req is not None and prev is not None and req != prev:
                subset = ("turn" in instr.lower()) or req < prev
                if not subset or req > prev:
                    problems.append(f"{label}: needs prev {req} but previous round made "
                                    f"{prev} ({instr})")
            if stated is not None and stated != made:
                problems.append(f"{label}: stated ({stated}) != derived {made} ({instr})")
            prev = stated if stated is not None else made
    return problems, unparsed
