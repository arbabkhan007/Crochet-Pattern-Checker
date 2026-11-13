"""Build NovalityStore_Grand_Collection.md — all 17 corrected masters in one volume.

Numbers in the front matter are computed at build time, never typed:
  * engine errors/warnings   -> subprocess to docs/kit/engine_run.py
  * audit problems/unparsed  -> docs/kit/audit_lib.py + audit_overrides.py
  * colour / print page count -> pymupdf over each spec's out / out_bw

Usage:  .venv/bin/python docs/kit/build_grand.py
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[2]
KIT = ROOT / "docs" / "kit"
OUT = ROOT / "NovalityStore_Grand_Collection.md"
PY = str(ROOT / ".venv" / "bin" / "python")

CODES = [f"{i:02d}" for i in range(1, 18)]

TITLES = {
    "01": "Hamish the Highland Cow",
    "02": "Kawaii Halloween Mini Set",
    "03": "Axel the Axolotl",
    "04": "Coco the Capybara",
    "05": "Little Duck Plushie",
    "06": "Momo the Loaf Cat",
    "07": "Pocket Positivity Trio",
    "08": "Ember the Baby Dragon",
    "09": "Shelby Sea Turtle Bag Charm",
    "10": "Willow the Bunny Lovey",
    "11": "No-Sew Christmas Gnome",
    "12": "Bobble Christmas Tree",
    "13": "Christmas Ornament Bundle",
    "14": "Bobble Snowflake Tree Skirt",
    "15": "Interchangeable Christmas Wreath",
    "16": "Mini Stocking Advent Garland",
    "17": "Year of the Fire Goat 2027 Plushie Set",
}

# Patterns whose pattern text changed in review round 2 (7 October 2026).
ROUND2_CHANGED = ["01", "02", "04", "05", "07", "08", "09", "11", "12", "13", "14", "15", "16", "17"]

ENGINE_NOTE = {
    "14": ("2 / 3 †", "† NS-14 prints its US and UK terms side by side. The engine's dialect-scope "
                      "rule assumes one dialect per piece, so the two sections that name UK terms and "
                      "also contain a US term are flagged; §5.2 of `NS14_validation_report.md` "
                      "documents this and §2.4 machine-verifies all 36 UK rows as exact translations "
                      "of the US rows. It cannot be cleared without abandoning the dual-column format."),
}


def spec_of(code: str) -> dict:
    path = ROOT / "docs" / f"ns{code}" / "spec.py"
    ns: dict = {"__file__": str(path)}
    exec(compile(path.read_text(), str(path), "exec"), ns)
    return ns.get("SPEC", ns)


def pages(path: str) -> int:
    p = ROOT / path if not Path(path).is_absolute() else Path(path)
    with pymupdf.open(str(p)) as doc:
        return doc.page_count


def engine_counts(code: str) -> tuple[int, int]:
    md = ROOT / "docs" / f"ns{code}" / f"NS{code}_corrected.md"
    out = subprocess.run([PY, str(KIT / "engine_run.py"), str(md)],
                         capture_output=True, text=True).stdout
    e = re.search(r"^ERRORS \((\d+)\)", out, re.M)
    w = re.search(r"^WARNINGS \((\d+)\)", out, re.M)
    return int(e.group(1)) if e else -1, int(w.group(1)) if w else -1


def audit_counts(code: str) -> tuple[int, int]:
    sys.path.insert(0, str(KIT))
    import audit_lib
    from audit_overrides import OVERRIDES, SKIP_TABLES
    text = (ROOT / "docs" / f"ns{code}" / f"NS{code}_corrected.md").read_text()
    probs, unp = audit_lib.audit_tables(text, OVERRIDES.get(f"NS-{code}", {}),
                                        SKIP_TABLES.get(f"NS-{code}", ()))
    return len(probs), len(unp)


def demote(text: str) -> str:
    """Push every ATX heading one level down, leaving code fences alone."""
    out, fence = [], False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            fence = not fence
        elif not fence and re.match(r"^#{1,5}\s", line):
            line = "#" + line
        out.append(line)
    return "\n".join(out)


FRONT = """# Novality Store — The Grand Crochet Pattern Collection
### Design codes NS-01 … NS-17 · seventeen **paper-verified** amigurumi & decor masters in one volume

Every pattern in this volume has been through the Novality verification pipeline:

1. **Deterministic static-analysis engine** (`src/crochet_checker`) — each corrected master is
   re-read and re-checked; the live error/warning count per pattern is in the ledger below.
2. **Independent stitch arithmetic auditor** (`docs/kit/audit_lib.py`) — every round/row table is
   re-derived from its own instruction text and compared with the count the pattern states. The
   handful of prose/continuation rows the generic grammar cannot simulate are carried as explicit
   expected counts in `docs/kit/audit_overrides.py`.
3. **Two store editions per pattern** — a colour Novality Store edition and a monochrome
   ink-friendly print edition (greyscale spread 0 on every page), compiled from the corrected
   master by `docs/kit/build_store_pdf.py` (NS-03 and NS-14 by their own compilers).

### What "verified" means here — read this before you buy or sell anything

**No sample of any pattern in this volume was crocheted, blocked, weighed, measured, washed or
safety-tested.** Everything was verified on paper: the arithmetic of every table, the internal
consistency of gauge against finished size, and the geometry implied by the stitch counts. So:

* **Stitch arithmetic is exact.** Where the audit reports 0 problems, every stated count re-derives
  from the instruction text that precedes it. That is a proof about the numbers, not about yarn.
* **Sizes, yarn quantities and times are targets.** They are computed from the patterns' own gauge
  figures at roughly 1.6 g of worsted per 100 stitches (the NS-03 yardstick) and from row heights —
  never from a finished object. Weigh and measure your first make and correct the figure.
* **Geometry findings are reasoned, not sampled.** The leg-alignment, cone-height and collar-fit
  corrections in review round 2 follow from column counts and circumferences; confirm them on a
  swatch or a first sample before repeating them in a listing.

### Corrections against the originals — what was and was not changed

Most corrections are wording, clarity, layout and derived-figure fixes: they change no stitch.
Three exceptions are recorded here rather than hidden behind a blanket claim:

* **NS-16** — the source's Row 6 lacked its `ch 1, turn`, leaving no stitches ahead of the hook for
  Row 7. The corrected turn is a real change to the instruction sequence (stitch counts unchanged).
* **NS-17** — the source's leg Rnd 13 decreased 12 → 9, which leaves an unmatched stitch in the
  flattened four-pair seam; it is corrected to 12 → 8. That is a change to a decrease schedule.
* **NS-17** — review round 2 resized the lamb's fixed collar from `ch 22` / 21 stitches to `ch 14` /
  13 stitches, because a 22-chain (about 10.5 cm) cannot fit an assembled 12-stitch neck (about
  6 cm). That is a change to a component's stitch count.

**NS-04 Rnd 5** was also re-spaced in round 2, but count-preserving: the same 24 stitches are
worked, the same 30 are made and the same six increases are used — only the columns the front legs
join over changed, from 6-8 / 16-18 to 7-9 / 19-21, which is what makes the four legs a rectangle.

Per-pattern correction tables and the round-2 findings live in each pattern's validation report.

## Review round 2 — hand review of all seventeen masters (7 October 2026)

A line-by-line hand review of the geometry, sizes and gauge, yarn quantities, front-matter claims,
leftover editorial text and branding found **no stitch-count errors** — the arithmetic stands, and
the audit still reports 0 problems on all seventeen. It did find the defects below, all now fixed in
the masters, the reports and both PDF editions of each affected pattern.

| # | Pattern | Defect | Correction |
|---|---|---|---|
| 1 | NS-04 | Front legs joined over columns 6-8 / 16-18 against back legs at 1-3 / 13-15 → leg gaps 5/7/3/9 columns: not a rectangle, and the text's "centres each front leg" claim was false | Rnd 5 re-spaced to `[sc, inc] x 3, join FL1: 3 sc, [sc, inc] x 3, 3 sc, join FL2: 3 sc, 3 sc` → joins at columns 7-9 / 19-21, gaps 3/3/3/3; 24 worked → 30 made, six increases, counts unchanged |
| 2 | NS-04 | "About 65 mm across" footprint not derivable — 30 stitches at ~3.5 mm give ~34 mm across the body | Derived body width stated (~34 mm) plus an instruction to measure the splayed footprint |
| 3 | NS-07 | Materials said #4 worsted on 3.5 mm but the gauge (3.5 mm/st, 3.2 mm/row), the ~8 m yarn use and the "1.3×" bigger-trio comparison are all the DK-on-2.5 mm figures; as written the trio would be 3.9/4.9/3.5 cm, not 3.0/3.8/2.7 cm | Materials changed to DK cotton (#3) on a 2.5 mm hook; gauge, counts and finished sizes unchanged; escape hooks 4 mm → 3 mm and 3 mm → 2.25 mm |
| 4 | NS-11 | 12 cm height counted the flat base rounds R1-R5, which add width only | ~8 cm (walls R6-R15 ≈ 4.6 cm + hat taper ≈ 3.2 cm); mini 8-9 cm → 6-6.5 cm; large 15 cm → 11-12 cm |
| 5 | NS-12 | 12 cm height counted the flat base rounds R1-R9 | ~7 cm cone; chunky 15.5 cm → 9.5 cm; three-size set 9-16 cm → 5.5-9.5 cm |
| 6 | NS-11, NS-12, NS-13, NS-15, NS-08, NS-04, NS-09 | Yarn quantities inflated against the patterns' own stitch counts (NS-11 67 g for ~530 sts; NS-12 70 g for ~700 sts; NS-13 21 g for ~177 sts; NS-15 one 175 g figure for three tube lengths and no stuffing; NS-08 30 g + 20 g; NS-04 30 g + 5 g; NS-09 materials 2 g vs header 3 g) | Re-derived at ~1.6 g per 100 sts: NS-11 9 g / 2 g / 1 g / 10 g stuffing; NS-12 15 g; NS-13 3 g / 2 g / 2 g; NS-15 12 g / 40 g / 55 g by tube length plus 2 g / 8 g / 12 g stuffing; NS-08 12 g / 5 g; NS-04 16 g / 2 g; NS-09 shell 2 g — all labelled paper estimates |
| 7 | Front matter | Claimed no stitch count, repeat multiplier or decrease schedule was ever changed, while NS-16 has a corrected Row-6 turn and NS-17 a corrected leg Rnd 13 (12 → 8) | Rewritten above: the three genuine changes are listed explicitly |
| 8 | NS-14, NS-16, NS-17 | "Verified" read as tested, though each file states no sample was crocheted | Reframed as **paper-verified** throughout this volume, in every report, and on every PDF cover (*5-AXIOM MATH VERIFIED ON PAPER* chip + "Paper-verified: no sample crocheted" card) |
| 9 | NS-14 | The internal "Revision notes — delete before publishing" section was still in the published volume; "Read before making" carried amigurumi-template wording (weave tails "while the centre opening is still open") contradicting its own Finishing section | Section deleted from the master (its substance stays in the report); the sentence now gives the real order and cross-references Finishing step 3 |
| 10 | NS-01 | Muzzle lower edge pinned at head Rnds 15-16 — the closing nub that assembly step 5 tucks inside the neck seam, with the seam itself at Rnd 14 | Lower edge now falls at Rnd 13; rim span reworded six rounds → four |
| 11 | NS-01 | Short-front option pinned the legs at 25° while assembly step 7 uses 55° | Option now starts at 55° with a 45-65° window |
| 12 | NS-02 | 20 brim stitches at 3.5 mm/st ≈ 22 mm across, not the stated 24 mm | Corrected to ~22 mm |
| 13 | NS-05 | Troubleshooting said "DK on 3.0 mm" against the size table's DK row (2.5-2.75 mm, 7.5-8.5 cm); a 12-stitch wing at ~8 mm/st flattens to ~45-50 mm, not 30 mm | Both corrected |
| 14 | NS-11 | "The nose sits on the round before the hat-colour change" — the nose is Rnd 14, the change is Rnd 16 | Both rounds now named |
| 15 | NS-16 | 5 heel pickups over ~10 row ends ≈ 1 per 2 rows, which can pucker | Ratio stated; the same five pickups may be spread over a longer edge span and recorded — count unchanged, flagged for testing |
| 16 | NS-17 | Lamb collar `ch 22` (~10.5 cm) on an assembled 12-stitch neck (~6 cm) | `ch 14` (~6.5 cm), Row 1 = 13 sts, Row 2 = 13 sts; collar yarn 9 m → 6 m |
| 17 | NS-17 | Smithsonian citation URL could not be resolved from the build environment | Citation removed; the reference now states only the checkable calendar facts (6 February 2027; Fire Goat / Ding Wei in the sixty-year sexagenary cycle) — both confirmed correct |
| 18 | NS-14, NS-16, NS-17 | Branding split: "Novality Crochet Studio" used for copyright, finished-item credit and hashtag, against "Novality Store" in NS-01-13 and NS-15 | Unified: copyright, credit and hashtag are Novality Store (#NovalityStore), with the designer credit "designed by Novality Crochet Studio" matching the other fourteen; NS-14's PDF compilers, which hard-coded the old credit, were patched and both editions recompiled |

NS-03, NS-06 and NS-10 raised no defect and their pattern text is unchanged; their PDFs were
recompiled only so all seventeen editions carry the same cover framing.

## Contents
"""


def main() -> None:
    rows, parts = [], []
    for i, code in enumerate(CODES, 1):
        spec = spec_of(code)
        md = (ROOT / "docs" / f"ns{code}" / f"NS{code}_corrected.md").read_text()
        e, w = engine_counts(code)
        ap, au = audit_counts(code)
        cp, bp = pages(spec["out"]), pages(spec["out_bw"])
        title = TITLES[code]
        ew = f"{e} / {w}" + (f" †" if code in ENGINE_NOTE else "")
        rows.append(f"| NS-{code} | {title} | {ew} | {ap} / {au} | {cp} | {bp} |")

        verdict = (f"*Paper-verified master — no sample crocheted · engine {e} error"
                   f"{'s' if e != 1 else ''} / {w} warning{'s' if w != 1 else ''} · independent audit "
                   f"{ap} problem{'s' if ap != 1 else ''} / {au} unparsed · colour edition {cp} pp · "
                   f"print edition {bp} pp · report: `docs/ns{code}/NS{code}_validation_report.md`*")
        round2 = ("*Review round 2 (7 October 2026): corrections applied — see this pattern's report.*"
                  if code in ROUND2_CHANGED else
                  "*Review round 2 (7 October 2026): no defect raised; text unchanged, PDFs recompiled "
                  "for cover framing only.*")
        parts.append("\n---\n\n"
                     f"# Part {i:02d} of 17 — NS-{code} · {title}\n\n"
                     f"{verdict}\n\n{round2}\n\n{demote(md).strip()}\n")

    ledger = ("## Verification ledger\n\n"
              "Counts below were recomputed at build time by `docs/kit/build_grand.py`, not typed.\n\n"
              "| Code | Pattern | Engine E / W | Audit problems / unparsed | Colour pp | Print pp |\n"
              "|---|---|---|---|---|---|\n" + "\n".join(rows) + "\n")
    notes = "\n\n".join(v for _, v in ENGINE_NOTE.values())
    if notes:
        ledger += "\n" + notes + "\n"
    ledger += ("\n*Cover artwork in the PDF editions is an illustrative render of the written design, "
               "not a\nphotograph of a sample; each cover says so. Etsy-style listings must carry the "
               "matching\nAI-disclosure sentence.*\n")

    contents = "## Contents\n\n" + "\n".join(
        f"{i:02d}. NS-{c} — {TITLES[c]} ({pages(spec_of(c)['out'])} pp colour / "
        f"{pages(spec_of(c)['out_bw'])} pp print)" for i, c in enumerate(CODES, 1)) + "\n"

    head = FRONT.split("## Contents\n")[0]
    OUT.write_text(head + contents + "\n" + ledger + "".join(parts) +
                   "\n---\n\n*End of the Grand Collection — Novality Store · seventeen patterns, "
                   "one paper-verified volume.*\n")
    print(f"wrote {OUT} ({OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
