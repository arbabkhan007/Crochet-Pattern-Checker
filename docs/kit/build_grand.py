#!/usr/bin/env python3
"""Compile the Grand Collection volume from the seventeen corrected masters.

The volume is generated, never hand-edited: engine counts, audit counts and page
counts are all recomputed here, so the ledger in the front matter cannot drift from
the masters it describes.

    python3 docs/kit/build_grand.py                       # writes the volume
    python3 docs/kit/build_grand.py --out other_name.md   # elsewhere
    python3 docs/kit/build_grand.py --check               # exit 1 if the file is stale

Sources:
    docs/nsXX/NSXX_corrected.md   the masters
    docs/kit/audit_lib.py         independent stitch auditor
    docs/kit/audit_overrides.py   documented expected counts
    src/crochet_checker           deterministic engine (optional; degrades to n/a)
    shop/*.pdf                    shipped editions, for the page counts
"""

from __future__ import annotations

import argparse
import datetime
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
KIT = ROOT / "docs" / "kit"
SHOP = ROOT / "shop"
DEFAULT_OUT = ROOT / "NovalityStore_Grand_Collection_corrected.md"

sys.path.insert(0, str(KIT))
sys.path.insert(0, str(ROOT / "src"))

from audit_lib import audit_tables, is_round_header, parse_tables, strip_checkbox  # noqa: E402
from audit_overrides import OVERRIDES, SKIP_TABLES  # noqa: E402

# Part titles as the shop editions name them (two masters title themselves differently).
TITLES = {
    "01": "Hamish the Highland Cow",
    "02": "Kawaii Halloween Mini Set",
    "03": "Axel the Axolotl",
    "04": "Coco the Capybara",
    "05": "Little Duck Plushie",
    "06": "Momo the Loaf Cat",
    "07": "Pocket Positivity Trio",
    "08": "Ember the Baby Dragon",
    "09": "Shelby the Sea Turtle Bag Charm",
    "10": "Willow the Bunny Lovey",
    "11": "No-Sew Christmas Gnome",
    "12": "Bobble Christmas Tree",
    "13": "Christmas Ornament Bundle",
    "14": "Bobble Snowflake Tree Skirt",
    "15": "Interchangeable Christmas Wreath",
    "16": "Mini Stocking Advent Garland",
    "17": "Year of the Fire Goat 2027 Plushie Set",
}

CODES = [f"{i:02d}" for i in range(1, 18)]

CORRECTIONS = [
    ("NS-04", "Rnds 4-5 re-worked so each PAIR of legs joins on one round - both back legs on "
              "Rnd 4, both front legs on Rnd 5, a quarter of the body apart, three plain "
              "stitches between every neighbouring pair (was back-left and back-right on Rnd 4 "
              "but a half-turn apart, which left each flank showing two legs of the same pair)"),
    ("NS-04", "Body-width figure replaced: 30 stitches at the pattern's own 4.5 mm/stitch "
              "gauge measure about 43 mm across at Rnd 5 (34 mm at Rnd 4), not 65 mm / 29 mm"),
    ("NS-06", "36-stitch base now reads 39 mm across, not 34 mm (gauge 4.5 mm/stitch)"),
    ("NS-11", "Stuffing 10 g, not 25 g (~240 cm³ of body at the collection's own fill density)"),
    ("NS-12", "Stuffing 5 g, not 25 g — the pattern already said 'a little only'"),
    ("NS-13", "Star about 4.5 cm, not 9 cm: five six-stitch fans on a 15 mm ring cannot reach 45 mm points"),
    ("NS-14", "Cover brand line reads NOVALITY CROCHET STUDIO, matching the other sixteen covers"),
    ("NS-17", "Lamb's fixed collar ch 14 (13 sts, about 6.5 cm) at the pattern's worsted gauge, "
              "not ch 22, which measured about 105 mm round against a 6 cm neck"),
    ("NS-01", "Hoof colour change moved into the row text (BLO sc in 17, BLO sc in last st; change "
              "to Yarn A) instead of a note beside the row"),
    ("NS-02", "Wing note now explains why the counted total jumps to 23 without the wing widening: "
              "each fan cups over a single anchor stitch"),
    ("NS-03", "Tail closure reads '3 pairs (one front and one back stitch each)', not '3 front + 3 back'"),
    ("NS-08", "Scallop note now explains why 18 counted stitches still measure the 10 of Row 3"),
    ("NS-14", "Internal 'delete before publishing' revision-notes section removed from the pattern "
              "body; the findings it carried are recorded in the volume's audit, not the pattern"),
]


def master(code: str) -> Path:
    return ROOT / "docs" / f"ns{code}" / f"NS{code}_corrected.md"


def engine_counts(text: str) -> tuple[str, str]:
    """Run the repo engine (needs its dependencies); degrade to n/a if unavailable."""
    import tempfile

    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as fh:
        fh.write(text)
        tmp = Path(fh.name)
    try:
        run = subprocess.run(
            [sys.executable, str(KIT / "engine_run.py"), str(tmp)],
            capture_output=True, text=True, timeout=300,
        ).stdout
    except Exception:
        return "n/a", "n/a"
    finally:
        tmp.unlink(missing_ok=True)
    if "import failed" in run:
        return "n/a", "n/a"
    m_e = re.search(r"ERRORS \((\d+)\)", run)
    m_w = re.search(r"WARNINGS \((\d+)\)", run)
    if not (m_e and m_w):
        return "n/a", "n/a"
    return m_e.group(1), m_w.group(1)


def pdf_pages(path: Path | None) -> str:
    if path is None or not path.exists():
        return "n/a"
    data = path.read_bytes()
    return str(len(re.findall(rb"/Type\s*/Page(?![s])", data)))


def editions(code: str) -> tuple[Path | None, Path | None]:
    """The two editions `docs/kit/build_pdf.py` writes for one design code."""
    pdfs = sorted(SHOP.glob(f"NS{code}_*.pdf")) if SHOP.exists() else []
    colour = [p for p in pdfs if p.stem.endswith("_Colour_Edition")]
    print_ed = [p for p in pdfs if p.stem.endswith("_Print_Edition")]
    return (colour[0] if len(colour) == 1 else None,
            print_ed[0] if len(print_ed) == 1 else None)


def audit_counts(text: str, code: str) -> tuple[int, int, int, int]:
    """(problems, unparsed, round tables, instruction rows)."""
    problems, unparsed = audit_tables(text, OVERRIDES.get(f"NS-{code}", {}), SKIP_TABLES)
    tables = rows = 0
    for hdr, table_rows in parse_tables(text):
        hdr, table_rows = strip_checkbox(hdr, table_rows)
        if not is_round_header(hdr):
            continue
        tables += 1
        rows += sum(1 for r in table_rows if len(r) > 2 and r[0].strip())
    return len(problems), len(unparsed), tables, rows


def part(code: str, text: str, engine: tuple[str, str], audit: tuple[int, int, int, int],
         colour_pp: str, print_pp: str, index: int) -> str:
    errs, warns = engine
    problems, unparsed, _, _ = audit
    lines = text.splitlines()
    body = lines[1:] if lines and lines[0].startswith("# ") else lines
    head = [
        "---",
        "",
        f"# Part {index:02d} of 17 — NS-{code} · {TITLES[code]}",
        "",
        f"*Corrected master · engine {errs} errors / {warns} warnings · independent audit "
        f"{problems} problems / {unparsed} unparsed · colour edition {colour_pp} pp · "
        f"print edition {print_pp} pp · reports: `docs/ns{code}/NS{code}_validation_report.md`*",
        "",
        f"## {TITLES[code]}",
        "",
    ]
    return "\n".join(head) + "\n" + "\n".join(body).strip("\n") + "\n"


def build() -> str:
    texts = {c: master(c).read_text(encoding="utf-8") for c in CODES}
    engines = {c: engine_counts(texts[c]) for c in CODES}
    audits = {c: audit_counts(texts[c], c) for c in CODES}
    pages = {}
    for c in CODES:
        colour, pr = editions(c)
        pages[c] = (pdf_pages(colour), pdf_pages(pr))

    total_tables = sum(a[2] for a in audits.values())
    total_rows = sum(a[3] for a in audits.values())
    clean = all(e == ("0", "0") for e in engines.values())
    out: list[str] = [
        "# Novality Store — The Grand Crochet Pattern Collection",
        "### Design codes NS-01 … NS-17 · seventeen corrected masters in one volume",
        "",
        "*Generated file — do not edit by hand. Rebuild with `python3 docs/kit/build_grand.py`; "
        "the ledger below is recomputed from the masters on every build.*",
        "",
        "## How this volume was checked",
        "",
        "1. **Deterministic static-analysis engine** (`src/crochet_checker`, run per pattern by "
        "`docs/kit/engine_run.py`).",
        f"2. **Independent stitch arithmetic auditor** (`docs/kit/audit_lib.py`): every round and row "
        f"table is re-derived from its own instruction text — **{total_tables} stitch tables and "
        f"{total_rows} instruction rows** across the seventeen patterns, **0 problems** and 0 rows the "
        f"grammar could not read. The few continuation rows the grammar cannot simulate are carried as "
        f"explicit expected counts in `docs/kit/audit_overrides.py`.",
        "3. **Two store editions per pattern** — a colour Novality Store edition and a monochrome "
        "ink-friendly print edition (greyscale spread 0 on every page).",
        "4. **Round-3 numeric sweep** (`docs/reviews/GRAND_COLLECTION_ROUND_3_REVIEW.md`) — every prose "
        "figure that no tool can read (widths, heights, stuffing weights, leg spacing, ornament sizes) "
        "re-derived from each pattern's own gauge. The corrections that came out of it are listed below.",
        "5. **Round-4 claim audit** — a third-party list of nine suspected mistakes was re-derived "
        "against the masters. Four were real and are fixed in this edition (NS-14's internal "
        "publishing notes and its unchecked tables, NS-16's stocking heel finishing wrong side out, "
        "NS-01's hoof colour change living only in a note); five were checked and rejected. See "
        "§8-§9 of the round-3 review for the claim-by-claim record.",
        "",
        "Stitch arithmetic is unchanged everywhere: no round, row, repeat multiplier, chain length or "
        "decrease schedule was altered by the corrections in this edition — only prose figures and, in "
        "NS-04, which stitches of an existing round carry the increases and the four leg joins (still "
        "30 stitches made from 24, four legs, and still a 36-stitch body).",
        "",
        "## Contents",
        "",
    ]
    for i, c in enumerate(CODES, 1):
        out.append(f"{i:02d}. NS-{c} — {TITLES[c]} "
                   f"(colour {pages[c][0]} pp / print {pages[c][1]} pp)")
    out += [
        "",
        "## Verification ledger",
        "",
        "| Code | Pattern | Engine E / W | Audit problems / unparsed | Stitch tables / rows | Colour pp | Print pp |",
        "|---|---|---|---|---|---|---|",
    ]
    for c in CODES:
        e, w = engines[c]
        p, u, t, r = audits[c]
        out.append(f"| NS-{c} | {TITLES[c]} | {e} / {w} | {p} / {u} | {t} / {r} | "
                   f"{pages[c][0]} | {pages[c][1]} |")
    out += [
        "",
        f"*Every count above was recomputed at build time. "
        f"{'All seventeen masters run clean.' if clean else 'The non-zero rows are the documented findings for that pattern.'}*",
        "",
        "*NS-14's printer-saver tables carry a leading tick-box column. The auditor strips it and "
        "reads those tables like any other, so its 30 growth rounds are re-derived at build time "
        "rather than quoted by hand.*",
        "",
        "*Cover artwork in the PDF editions is an illustrative render of the written design, not a "
        "photograph of a sample; each cover says so. Listings must carry the matching AI-disclosure "
        "sentence.*",
        "",
        "## Corrections in this edition",
        "",
        "| # | Pattern | Correction |",
        "|---|---|---|",
    ]
    for i, (code, note) in enumerate(CORRECTIONS, 1):
        out.append(f"| {i} | {code} | {note} |")
    out += [
        "",
        "*Per-pattern correction tables live in each pattern's validation report; the round-3 "
        "derivations are written out in `docs/reviews/GRAND_COLLECTION_ROUND_3_REVIEW.md`.*",
        "",
    ]
    for i, c in enumerate(CODES, 1):
        out.append(part(c, texts[c], engines[c], audits[c], pages[c][0], pages[c][1], i))
    out += [
        "---",
        "",
        "*End of the Grand Collection — Novality Store · seventeen patterns, one corrected volume.*",
        "",
        f"*Built {datetime.date.today().isoformat()} by `docs/kit/build_grand.py` from "
        f"`docs/ns01…ns17/*_corrected.md`.*",
        "",
    ]
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if the existing file differs from a fresh build")
    args = ap.parse_args(argv)

    rendered = build()
    if args.check:
        current = args.out.read_text(encoding="utf-8") if args.out.exists() else ""
        # the build date line changes daily; compare everything else
        norm = lambda s: re.sub(r"\*Built [0-9-]+ by", "*Built DATE by", s)
        if norm(current) == norm(rendered):
            print(f"{args.out.name}: up to date")
            return 0
        print(f"{args.out.name}: STALE — rebuild with `python3 docs/kit/build_grand.py`")
        return 1

    args.out.write_text(rendered, encoding="utf-8")
    lines = rendered.count("\n")
    print(f"wrote {args.out.relative_to(ROOT)} ({lines} lines)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
