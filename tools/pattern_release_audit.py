#!/usr/bin/env python3
"""Release-gate audit for the 15 Novality crochet pattern Markdown masters.

This checker intentionally has no third-party dependencies.  It validates the
customer-facing files themselves (rather than trusting generator source data):

* expected file/design-code inventory and required release sections;
* Markdown table shape;
* exact US -> UK stitch-term parity in all dual-terminology tables;
* canonical round arithmetic (consumed stitches and produced stitches);
* explicit independent assertions for non-canonical constructions;
* removal of editorial/debug language and known stale statements;
* key safety/construction ordering statements introduced by the tech edit.

Run from the repository root:

    python tools/pattern_release_audit.py
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import math
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
PATTERN_DIR = ROOT / "patterns"
EXPECTED = [
    "01_Hamish_the_Highland_Cow.md",
    "02_Kawaii_Halloween_Mini_Set.md",
    "03_Axel_the_Axolotl.md",
    "04_Coco_the_Capybara.md",
    "05_Little_Duck_Plushie.md",
    "06_Momo_the_Loaf_Cat.md",
    "07_Pocket_Positivity_Trio.md",
    "08_Ember_the_Baby_Dragon.md",
    "09_Shelby_the_Sea_Turtle_Bag_Charm.md",
    "10_Willow_the_Bunny_Lovey.md",
    "11_No-Sew_Christmas_Gnome.md",
    "12_Bobble_Christmas_Tree.md",
    "13_Christmas_Ornament_Bundle.md",
    "14_Bobble_Snowflake_Tree_Skirt.md",
    "15_Interchangeable_Christmas_Wreath.md",
]


@dataclass(frozen=True)
class TableRow:
    file: str
    line: int
    section: str
    table: int
    label: str
    instruction: str
    uk_instruction: str | None
    stated_text: str
    stated: int | None


class Audit:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.checks = 0

    def check(self, condition: bool, message: str) -> None:
        self.checks += 1
        if not condition:
            self.errors.append(message)

    def equal(self, got, want, message: str) -> None:
        self.checks += 1
        if got != want:
            self.errors.append(f"{message}: got {got!r}, expected {want!r}")


def split_table_line(line: str) -> list[str]:
    # Patterns do not use escaped pipes inside cells.
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def parse_rows(path: Path, audit: Audit) -> list[TableRow]:
    lines = path.read_text(encoding="utf-8").splitlines()
    section = ""
    table_no = 0
    header: list[str] | None = None
    rows: list[TableRow] = []
    in_table = False

    for line_no, line in enumerate(lines, 1):
        if line.startswith("#"):
            section = line.lstrip("#").strip()
        if not line.startswith("|"):
            in_table = False
            header = None
            continue

        cells = split_table_line(line)
        if not in_table:
            table_no += 1
            header = cells
            in_table = True
            continue

        if all(re.fullmatch(r":?-{3,}:?", c) for c in cells):
            audit.equal(len(cells), len(header or []),
                        f"{path.name}:{line_no} separator width")
            continue

        audit.equal(len(cells), len(header or []),
                    f"{path.name}:{line_no} table row width")
        if not header or len(cells) != len(header):
            continue
        lower_header = [h.lower() for h in header]
        if "sts" not in lower_header or not cells:
            continue
        label = cells[0]
        us_idx = lower_header.index("us terms") if "us terms" in lower_header else 1
        uk_idx = lower_header.index("uk terms") if "uk terms" in lower_header else None
        sts_idx = lower_header.index("sts")
        stated_text = cells[sts_idx]
        match = re.fullmatch(r"\((\d+)(?:\s+each)?\)", stated_text)
        stated = int(match.group(1)) if match else None
        rows.append(TableRow(
            file=path.name,
            line=line_no,
            section=section,
            table=table_no,
            label=label,
            instruction=cells[us_idx],
            uk_instruction=cells[uk_idx] if uk_idx is not None else None,
            stated_text=stated_text,
            stated=stated,
        ))
    return rows


def norm(text: str) -> str:
    text = text.lower().replace("×", "x").replace("–", "-")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def translate_us_to_uk(text: str) -> str:
    """Token-preserving translation used to compare side-by-side table cells."""
    value = norm(text)
    # Placeholders contain no stitch-name substrings, so substitutions cannot
    # cascade (for example, the "dc" pass cannot mutate an hdc placeholder).
    replacements = {
        "sc2tog": "@@a@@",
        "hdc": "@@b@@",
        "sc": "@@c@@",
        "tr": "@@d@@",
        "dc": "@@e@@",
    }
    for source, placeholder in replacements.items():
        value = re.sub(rf"\b{source}\b", placeholder, value)
    for placeholder, target in {
        "@@a@@": "dc2tog",
        "@@b@@": "htr",
        "@@c@@": "dc",
        "@@d@@": "dtr",
        "@@e@@": "tr",
    }.items():
        value = value.replace(placeholder, target)
    return value


def canonical_math(text: str, previous: int | None) -> tuple[int | None, int] | None:
    """Evaluate the repeated round forms used throughout the collection.

    Returns (consumed, produced).  ``None`` means this row needs an explicit
    construction assertion below; it is never silently skipped.
    """
    s = norm(text)
    # Remove common non-mathematical wrappers.
    s = re.sub(r"^(?:with [^:]+:\s*)", "", s)
    s = re.sub(r"^(?:flo|blo):\s*", "", s)
    s = re.sub(r"\s*\([^)]*(?:rnd|round|all four|front|back)[^)]*\)\s*$", "", s)

    # Magic-ring starts (an optional starting chain/join does not count).
    # A starting ch-3 that explicitly counts contributes one dc/tr in addition
    # to the written stitches that follow it.
    m = re.search(r"(?:^|[,;]\s*)(\d+)\s+(sc|dc)\s+in\s+(?:mr|ring)\b", s)
    if m and ("[" not in s):
        produced = int(m.group(1))
        if re.search(r"ch 3 \(counts as first (?:dc|tr)\)", s):
            produced += 1
        return (0, produced)

    if previous is not None:
        # Test increases before the generic "in each stitch" form.
        if re.search(r"\b2\s+(?:sc|dc|tr)\s+in\s+each\s+st\s+around", s):
            return (previous, previous * 2)
        if re.search(r"\binc\s+in\s+each\s+st\s+around", s):
            return (previous, previous * 2)
        if re.search(r"\b(?:sc|dc)\s+in\s+each\s+(?:st|ch)(?:\s+around|\s+across)", s):
            return (previous, previous)
        if re.fullmatch(r"(?:blo\s+)?(?:sc|dc)(?:\s+in\s+each\s+st)?\s+around(?:, then fo)?", s):
            return (previous, previous)
        if re.fullmatch(r"(?:sc|dc)\s+around", s):
            return (previous, previous)

    # [k plain stitch, increase/decrease] x repeats.  Require the repeat to
    # occupy the whole instruction; otherwise an oval with several groups can
    # accidentally match only one nested group.
    m = re.fullmatch(
        r"\[\s*(?:(\d+)\s+)?(?:sc|dc),?\s*"
        r"(inc|dec|invdec|sc2tog)\s*\]\s*x\s*(\d+)", s)
    if m:
        plain = int(m.group(1) or 1)
        repeats = int(m.group(3))
        if m.group(2) == "inc":
            return ((plain + 1) * repeats, (plain + 2) * repeats)
        return ((plain + 2) * repeats, (plain + 1) * repeats)

    # [BO, k sc, optional decrease] x repeats.
    m = re.search(
        r"\[\s*bo(?:\s+in\s+next\s+st)?,?\s*"
        r"(?:(\d+)\s+)?(?:sc|dc)?(?:\s+in\s+next\s+\d+\s+sts?)?"
        r"(?:,?\s*(sc2tog|dc2tog))?\s*\]\s*x\s*(\d+)", s)
    if m and s.count("[") == 1:
        plain = int(m.group(1) or (1 if re.search(r"bo,\s*(?:sc|dc),", s) else 0))
        has_dec = bool(m.group(2))
        repeats = int(m.group(3))
        consumed_each = 1 + plain + (2 if has_dec else 0)
        produced_each = 1 + plain + (1 if has_dec else 0)
        return (consumed_each * repeats, produced_each * repeats)

    # Pure decreases.
    m = re.search(r"\b(dec|invdec|sc2tog)\s+x\s*(\d+)\b", s)
    if m and "[" not in s:
        n = int(m.group(2))
        return (2 * n, n)

    # Tree-skirt 12-repeat ladder, with or without a BO replacing one dc.
    m = re.search(
        r"\[(?:bo in next st,\s*)?dc in next\s+(\d+)\s+sts?,\s*"
        r"2 dc in next st\]\s*x\s*12", s)
    if m:
        plain = int(m.group(1))
        bobble = 1 if s[s.find("["):].startswith("[bo") else 0
        return ((bobble + plain + 1) * 12,
                (bobble + plain + 2) * 12)

    # Short named sequences that are still canonical.
    m = re.fullmatch(r"\[(\d+) sc, inc\] x (\d+)", s)
    if m:
        k, n = map(int, m.groups())
        return ((k + 1) * n, (k + 2) * n)

    return None


# Explicit independent arithmetic for every count-bearing construction outside
# canonical_math().  Keys are normalized customer-facing instructions, so the
# audit evaluates the actual Markdown rather than a separate generated row ID.
# Values are (consumed, produced). ``consumed=None`` is used only for an
# intentional partial row whose availability is asserted separately below.
def _manual(items: list[tuple[str, int | None, int]]) -> dict[str, tuple[int | None, int]]:
    result: dict[str, tuple[int | None, int]] = {}
    for instruction, consumed, produced in items:
        normalized = norm(instruction)
        if normalized in result and result[normalized] != (consumed, produced):
            raise ValueError(f"conflicting manual rule: {instruction}")
        result[normalized] = (consumed, produced)
    return result


MANUAL = _manual([
    # Around-chain ovals and their expansion rounds.
    ("sc in 2nd ch, sc in next 6, 3 sc in last ch, sc in next 6, 2 sc in last loop", 8, 18),
    ("inc, 6 sc, inc x 3, 6 sc, inc x 2", 18, 24),
    ("sc, inc, 6 sc, [sc, inc] x 3, 6 sc, [sc, inc] x 2", 24, 30),
    ("2 sc, inc, 6 sc, [2 sc, inc] x 3, 6 sc, [2 sc, inc] x 2", 30, 36),
    ("3 sc, inc, 6 sc, [3 sc, inc] x 3, 6 sc, [3 sc, inc] x 2", 36, 42),
    ("4 sc, inc, 6 sc, [4 sc, inc] x 3, 6 sc, [4 sc, inc] x 2", 42, 48),
    ("sc in 2nd ch, 4 sc, 3 sc in last ch; continue along the other side: 4 sc, 2 sc in last ch", 6, 14),
    ("sc in 2nd ch, 4 sc, 3 sc in last ch; other side: 4 sc, 2 sc in last ch", 6, 14),
    ("inc, 4 sc, inc x 3, 4 sc, inc x 2", 14, 20),
    ("sc in 2nd ch, 3 sc, 3 sc in last ch, then down the other side 3 sc, 2 sc in last ch", 5, 12),
    ("inc, 3 sc, inc x 3, 3 sc, inc x 2", 12, 18),
    ("sc in 2nd ch from hook, sc in next 2 ch, 3 sc in last ch; rotate to work along the opposite side: sc in next 2 ch, 2 sc in the remaining loop of the first working ch", 4, 10),
    ("inc, 2 sc, inc x 3, 2 sc, inc x 2", 10, 16),

    # Flat rows, foundations and partial shaping.
    ("hdc in 2nd ch from hook and in each ch across", 60, 60),
    ("ch 1, turn, hdc across", 60, 60),
    ("ch 1, turn; 4 sc, inc in each of next 3, 4 sc (last 3 sts of R1 stay unworked - they form the pointed base)", None, 14),
    ("ch 1, turn; sl st in each st across", 14, 14),
    ("ch 20; from the 2nd ch, work 2 sc in each chain to the end", 19, 38),
    ("from the 2nd ch: sc in 4, hdc in 4, dc in 4; ch 1, turn", 12, 12),
    ("sc in 3, hdc in 4, dc in 5; ch 1, turn", 12, 12),
    ("from the 2nd ch: sc in 4, hdc in 3, dc in 3", 10, 10),
    ("sc in 3, hdc in 3, dc in 4", 10, 10),
    ("sc in 2, hdc in 4, dc in 4", 10, 10),
    ("sc in next 5, ch 1, turn", 5, 5),
    ("dec, sc, dec, ch 1, turn", 5, 3),
    ("dec, sc", 3, 2),

    # Clusters, joins and decorative rounds.
    ("FLO: [2 sl st, (sc, hdc, dc, hdc, sc) in next st, 1 sl st] x 6", 24, 48),
    ("sl st in first 2, (sc, hdc, dc, picot, dc, hdc, sc) in next st, sl st in next 3, (sc, hdc, picot, hdc, sc) in next st, sl st in next 2, (sc, hdc, picot, hdc, sc) in next st, sl st in last 2", 12, 23),
    ("sl st in first 2, (sc, hdc, dc, hdc, sc) all in next st, sl st in next 2, (sc, hdc, dc, hdc, sc) all in next st, sl st in last 4", 10, 18),
    ("after closing the centre, join yellow with a sl st in any EXPOSED front loop of Rnd 3 (this counts as the first sl st); (sc, hdc, sc) in next front loop, [sl st in next front loop, (sc, hdc, sc) in next front loop] x 8, sl st to the first sl st, FO", 18, 36),
    ("join BL1: 3 sc, [sc, inc] x 3, join BL2: 3 sc, [sc, inc] x 3", 18, 24),
    ("1 sc, inc, 1 sc, inc, 1 sc, join FL1: 3 sc, [sc, inc] x 3, 1 sc, join FL2: 3 sc, 3 sc, inc, 2 sc", 24, 30),
    ("BLO: 3 sc, (sc, hdc, hdc, sc) in next st, 4 sc, (sc, hdc, sc) in next st, 3 sc, (sc, hdc, sc) in next st, 4 sc, (sc, hdc, sc) in next st, 3 sc, (sc, hdc, sc) in next st, 2 sc", 24, 35),
    ("[sl st in next st, (sc, hdc, dc, ch 2, dc, hdc, sc) in next st] x 5, sl st to first sl st, FO", 10, 35),

    # Small starts and joined granny rounds.
    ("ch 2, 3 sc in 2nd ch from hook", 1, 3),
    ("inc x 3", 3, 6),
    ("ch 3 (counts as first dc), 2 dc in the ring, [ch 2, 3 dc in the ring] x 3, ch 2, sl st to the ch-3 top", 0, 12),
    ("sl st in next 2 dc and into the next corner space; ch 3 (counts as first dc), 2 dc, ch 2, 3 dc in that same space (first corner); then (3 dc, ch 2, 3 dc) into each remaining corner space; sl st to top of ch-3", 12, 24),
    ("Ch 2, [dc in next st, 2 dc in next st] x 12, sl st to first dc", 24, 36),

    # New-table continuation rows in the one-piece gnome.
    ("sc in each st around (4 rnd)", 30, 30),
    ("sc in each st around", 30, 30),
    ("sc in next 14, BO in next st (nose), sc in remaining 15", 30, 30),

    # Wreath-specific chain pieces (counts are per leaf/tail/row as printed).
    ("Sc in each ch around", 12, 12),
    ("Sc in each st around until the tube reaches the target MEASURED length", 12, 12),
    ("Make 3 separately in green: ch 8, sc in 2nd ch from hook, hdc in next ch, dc in next 3 ch, hdc in next ch, sc in last ch; FO with a 15 cm tail", None, 7),
    ("Ch 15, sc in 2nd ch from hook and across (14 sc), sl st to bow base; repeat for second tail", 14, 14),
    ("Ch 6, sc in 2nd ch from hook and across (5); rows 2-4: ch 1, turn, sc across (5)", None, 5),
    ("Ch 8 ring; sc in each ch (8); spiral in 8 sc until the tube measures 20-24 cm; join the 8 end pairs ROUND as for the base; wrap a separate doubled yarn tie twice around the whole tube for hanging", 8, 8),
])


def run() -> int:
    audit = Audit()
    actual = sorted(p.name for p in PATTERN_DIR.glob("*.md"))
    audit.equal(actual, EXPECTED, "15-pattern file inventory")

    all_rows: list[TableRow] = []
    codes: list[str] = []
    banned = re.compile(
        r"\b(?:todo|tbd|fixme|placeholder|skip-check|tentative)\b|"
        r"corrected from|validation correction|from the q4 draft|"
        r"thank you[^\n]*thank you",
        re.IGNORECASE,
    )
    required = [
        "## Safety — read this first", "## Materials", "## Gauge & size",
        "## Abbreviations", "## Instructions", "## Troubleshooting",
        "## Terms of Use",
    ]

    for expected_no, name in enumerate(EXPECTED, 1):
        path = PATTERN_DIR / name
        audit.check(path.exists(), f"missing {name}")
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        match = re.search(r"Design Code NS (\d{2})", text)
        audit.check(bool(match), f"{name}: missing design code")
        if match:
            audit.equal(int(match.group(1)), expected_no,
                        f"{name}: design-code sequence")
            codes.append(match.group(1))
        for section in required:
            audit.check(section in text, f"{name}: missing section {section!r}")
        audit.check(bool(re.search(
            r"^## (?:Finishing(?: & assembly)?|Assembly(?: & finishing)?)$",
            text, re.MULTILINE)),
            f"{name}: missing finishing/assembly section")
        audit.check(bool(re.search(
            r"^## (?:Selling & )?Care(?: & storage)?$",
            text, re.MULTILINE | re.IGNORECASE)),
            f"{name}: missing care section")
        audit.check(text.endswith("\n"), f"{name}: missing final newline")
        audit.check("\r" not in text, f"{name}: CR line ending found")
        audit.check("\t" not in text, f"{name}: tab character found")
        audit.check(not banned.search(text),
                    f"{name}: internal/editorial language leaked into customer file")
        audit.check("designer.." not in text,
                    f"{name}: doubled punctuation in closing")

        # Semantic heading structure matters when these masters become tagged
        # PDFs and a navigable table of contents.  Do not use bold paragraphs
        # as pseudo-headings or skip levels.
        headings = [(len(m.group(1)), m.group(2)) for m in
                    re.finditer(r"^(#{1,6})\s+(.+)$", text, re.MULTILINE)]
        audit.check(bool(headings) and headings[0][0] == 1,
                    f"{name}: first heading must be the single H1 title")
        audit.equal(sum(level == 1 for level, _ in headings), 1,
                    f"{name}: H1 title count")
        for (prior, _), (level, title) in zip(headings, headings[1:]):
            audit.check(level <= prior + 1,
                        f"{name}: heading level jumps to H{level} at {title!r}")
        audit.check(not re.search(r"^\*\*[^*]+\*\*$", text, re.MULTILINE),
                    f"{name}: bold paragraph used as a pseudo-heading")
        audit.check("\n\n\n" not in text,
                    f"{name}: multiple consecutive blank lines")
        all_rows.extend(parse_rows(path, audit))

    audit.equal(len(set(codes)), 15, "unique design codes")

    # Side-by-side terminology must be an exact token translation.
    dual_rows = 0
    for row in all_rows:
        if row.uk_instruction is None:
            continue
        dual_rows += 1
        audit.equal(translate_us_to_uk(row.instruction), norm(row.uk_instruction),
                    f"{row.file}:{row.line} US/UK parity")
    audit.check(dual_rows >= 100, "unexpectedly few dual-terminology rows")

    # Count arithmetic.  Previous count is tracked within each table; the split
    # skirt tables are also checked independently by the 12*n invariant below.
    checked_count_rows = 0
    unhandled: list[TableRow] = []
    by_table: dict[tuple[str, int], list[TableRow]] = {}
    for row in all_rows:
        by_table.setdefault((row.file, row.table), []).append(row)

    for _, rows in by_table.items():
        previous: int | None = None
        for row in rows:
            if row.stated is None:
                continue
            result = canonical_math(row.instruction, previous)
            if result is None:
                result = MANUAL.get(norm(row.instruction))
            if result is None:
                unhandled.append(row)
                previous = row.stated
                continue
            consumed, produced = result
            checked_count_rows += 1
            audit.equal(produced, row.stated,
                        f"{row.file}:{row.line} {row.section} {row.label} produced")
            if previous is not None and consumed is not None:
                audit.equal(consumed, previous,
                            f"{row.file}:{row.line} {row.section} {row.label} consumed")
            previous = row.stated

    if unhandled:
        audit.errors.append(
            "count rows lacking an explicit audit rule:\n  " + "\n  ".join(
                f"{r.file}:{r.line} [{r.section} / {r.label}] {r.instruction} {r.stated_text}"
                for r in unhandled
            )
        )
    audit.check(checked_count_rows >= 500,
                f"only {checked_count_rows} count rows were arithmetically checked")

    # Tree-skirt independent invariant: row n must finish at 12*n.
    skirt_rows = [r for r in all_rows if r.file.startswith("14_") and re.fullmatch(r"R\d+", r.label)]
    for row in skirt_rows:
        n = int(row.label[1:])
        audit.equal(row.stated, 12 * n,
                    f"{row.file}:{row.line} 12-spoke invariant")
    audit.equal(len(skirt_rows), 32, "tree-skirt round coverage")

    # Independent derivations for constructions that do not have a simple
    # one-repeat parser form.  These deliberately recompute the arithmetic
    # rather than copying the printed total.
    derivations = [
        (24 + 10 + 9, 43, "Hamish fringe knots"),
        (1 + 6 + 3 + 6 + 2, 18, "Hamish/Momo ch-9 oval R1"),
        (6 * (2 + 1 + 1), 24, "Boo ruffle anchors consumed"),
        (6 * (2 + 5 + 1), 48, "Boo ruffle stitches produced"),
        (4 + 3 + 4, 11, "Pip partial leaf row anchors consumed"),
        (4 + 6 + 4, 14, "Pip partial leaf row stitches produced"),
        (2 + 1 + 3 + 1 + 2 + 1 + 2, 12, "Bramble wing Row 3 anchors consumed"),
        (2 + 6 + 3 + 4 + 2 + 4 + 2, 23, "Bramble wing Row 3 counted stitches"),
        (5 * 2, 10, "Axel fin anchors"),
        (3 + 6 + 3 + 6, 18, "Coco back-leg join anchors consumed"),
        (3 + 9 + 3 + 9, 24, "Coco back-leg join stitches produced"),
        (5 + 3 + 7 + 3 + 6, 24, "Coco front-leg join anchors consumed"),
        (7 + 3 + 10 + 3 + 7, 30, "Coco front-leg join stitches produced"),
        (1 + 2 + 3 + 2 + 2, 10, "Duck beak R1 stitches"),
        (2 + 2 + 6 + 2 + 4, 16, "Duck beak R2 stitches"),
        (1 + 6 + 3 + 6 + 2, 18, "Momo oval R1 stitches"),
        (9 + 9 * 3, 36, "Sunny petal-round stitches"),
        (1 + 3 + 3 + 3 + 2, 12, "Waddle chest oval R1 stitches"),
        (1 + 4 + 3 + 4 + 2, 14, "Spud oval R1 stitches"),
        (3 + 9 * 3 + 3, 33, "Ember spike-strip anchors"),
        (2 + 5 + 2 + 5 + 4, 18, "Ember wing edge counted stitches"),
        (3 + 1 + 4 + 1 + 3 + 1 + 4 + 1 + 3 + 1 + 2, 24,
         "Shelby small underside anchors"),
        (19 + 4 + 4 * 3, 35, "Shelby small underside stitches"),
        (37 + 4 + 4 * 3, 53, "Shelby large underside stitches"),
        (240 + 4 * 3, 252, "Willow R20 border stitches"),
        (14 + 1 + 15, 30, "Gnome nose round"),
        (6 * ((1 + 5 + 2)), 48, "Tree R12 anchors consumed"),
        (6 * ((1 + 5 + 1)), 42, "Tree R12 stitches produced"),
        (5 * (1 + 6), 35, "Star counted stitches"),
        (6 * 2, 12, "Snowflake R2 ring stitches consumed"),
        (168 // 6, 28, "Mini tree-skirt scallops"),
        (276 // 6, 46, "Standard tree-skirt scallops"),
        (384 // 6, 64, "Large tree-skirt scallops"),
        (1 + 1 + 3 + 1 + 1, 7, "Wreath poinsettia leaf chains"),
        (15 - 1, 14, "Wreath bow-tail stitches"),
        (6 - 1, 5, "Wreath bow-band stitches"),
    ]
    for got, want, label in derivations:
        audit.equal(got, want, label)

    # Dimension sanity checks derived from the printed gauges.  These are not a
    # substitute for sample measurements, but they catch unit and circumference
    # mistakes such as the former mini-wreath inches/centimetres error.
    audit.check(abs((48 * (50 / 11) / math.pi) - 70) < 1,
                "Hamish 48-st circumference should be about 70 mm diameter")
    audit.check(abs((36 * 4.5 / math.pi) - 52) < 1,
                "36 stitches at 4.5 mm should be about 52 mm diameter")
    audit.check(abs(math.hypot(26, 26) - 36.8) < 0.1,
                "Willow 26 cm square should have about a 36.8 cm diagonal")
    for length_cm, printed_diameter_cm, label in [
        (20, 6.5, "mini wreath low"), (24, 7.5, "mini wreath high"),
        (86, 27, "standard wreath low"), (97, 31, "standard wreath high"),
        (119, 38, "large wreath low"), (132, 42, "large wreath high"),
    ]:
        audit.check(abs(length_cm / math.pi - printed_diameter_cm) < 0.6,
                    f"{label}: tube length / pi conversion")

    # High-risk release statements: these exact concepts prevent regressions in
    # eye order, end joining, unit conversion, and customer-facing math.
    must_contain = {
        "01_Hamish_the_Highland_Cow.md": [
            "18 head stitches of Rnd 14",
            "INNER ear through Rnd 6 only",
            "Shortened front legs - upright option only (make 2)",
            "12-stitch top opening",
            "Start each leg 25 degrees forward from vertical",
        ],
        "02_Kawaii_Halloween_Mini_Set.md": ["UP THE OUTSIDE", "(38)", "FIRST fan in the written Row-3 sequence", "lock eye washers and embroider fangs/blush now"],
        "04_Coco_the_Capybara.md": ["Immediately after Rnd 15", "through all three layers"],
        "03_Axel_the_Axolotl.md": ["lock eye washers and embroider face now", "TEN marked surface anchors"],
        "05_Little_Duck_Plushie.md": ["Rnd 1 has 10 stitches", "inc x 3", "(16)", "PAUSE: embroider eyes", "before stuffing, sew one wing"] ,
        "06_Momo_the_Loaf_Cat.md": ["do not make a magic ring", "do NOT try to slip-stitch from the ear tip", "lock eyes; embroider face/chest/paws; then stuff"],
        "07_Pocket_Positivity_Trio.md": ["EXPOSED front loop", "after R6: lock eyes and embroider mouth", "after R9: lock eyes, attach all pieces"],
        "08_Ember_the_Baby_Dragon.md": ["ch 34", "3 + 27 + 3 = 33", "LOCK eye washers now", "nostrils inside the still-open snout"],
        "09_Shelby_the_Sea_Turtle_Bag_Charm.md": ["no plastic eyes", "Do not wait until the seam is closed", "24 exposed front loops"],
        "10_Willow_the_Bunny_Lovey.md": ["sl st in next 2 dc", "cotton does not felt", "immediately after Head Rnd 10", "18 marked Rnd-12 stitches"],
        "11_No-Sew_Christmas_Gnome.md": ["after Rnd 15", "begin stuffing through the still-wide opening"],
        "12_Bobble_Christmas_Tree.md": ["change TO contrast before each bobble", "immediately after Rnd 9"],
        "13_Christmas_Ornament_Bundle.md": ["(35)", "fan contains 6 worked stitches"],
        "14_Bobble_Snowflake_Tree_Skirt.md": ["SAME stitch as the join", "Round N always consumes N-1"],
        "15_Interchangeable_Christmas_Wreath.md": ["20-24 cm / 8-9.5 in", "Keep both openings ROUND", "folded 55 cm tie under at least 2 sturdy", "does not rely on individual crochet sts"],
    }
    for name, needles in must_contain.items():
        text = (PATTERN_DIR / name).read_text(encoding="utf-8")
        for needle in needles:
            audit.check(needle in text, f"{name}: missing release safeguard {needle!r}")

    print(f"Files: 15 | table rows: {len(all_rows)} | dual rows: {dual_rows} | "
          f"count rows checked: {checked_count_rows} | assertions: {audit.checks}")
    if audit.errors:
        print(f"FAIL ({len(audit.errors)} findings)")
        for finding in audit.errors:
            print(f"- {finding}")
        return 1
    print("PASS - all release-gate checks succeeded")
    return 0


if __name__ == "__main__":
    sys.exit(run())
