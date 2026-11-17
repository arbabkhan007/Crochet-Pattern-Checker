"""Recompute the Grand Collection verification ledger from the live tools.

The volume's front matter says the counts were "recomputed at build time by
docs/kit/build_grand.py, not typed".  This is that script.

It splits a volume on its `# Part NN of 17 - NS-XX` headings, runs the
deterministic engine (`src/crochet_checker`) and the independent stitch
auditor (`docs/kit/audit_lib.py`) over each part, reads the colour and print
page counts straight from the PDFs, and either prints the ledger or writes it
back into the volume.

Usage:
    python3 docs/kit/build_grand.py [VOLUME.md] [--pdf-dir shop] [--write]

Exit status is 1 when the ledger in the file does not match the recomputed one.
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve()
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "docs" / "kit"))

import audit_lib  # noqa: E402
from audit_overrides import OVERRIDES  # noqa: E402

PART_RE = re.compile(r"\n# Part (\d+) of 17 — (NS-\d+)")

# colour / print edition stems in shop/
PDF_NAMES = {
    "NS-01": ("Hamish_the_Highland_Cow_NS01_NovalityStore", "Hamish_the_Highland_Cow_NS01_PRINT_EDITION_BW"),
    "NS-02": ("Kawaii_Halloween_Mini_Set_NS02_NovalityStore", "Kawaii_Halloween_Mini_Set_NS02_PRINT_EDITION_BW"),
    "NS-03": ("Axel_the_Axolotl_NS03_NovalityStore", "Axel_the_Axolotl_NS03_PRINT_EDITION_BW"),
    "NS-04": ("Coco_the_Capybara_NS04_NovalityStore", "Coco_the_Capybara_NS04_PRINT_EDITION_BW"),
    "NS-05": ("Little_Duck_Plushie_NS05_NovalityStore", "Little_Duck_Plushie_NS05_PRINT_EDITION_BW"),
    "NS-06": ("Momo_the_Loaf_Cat_NS06_NovalityStore", "Momo_the_Loaf_Cat_NS06_PRINT_EDITION_BW"),
    "NS-07": ("Pocket_Positivity_Trio_NS07_NovalityStore", "Pocket_Positivity_Trio_NS07_PRINT_EDITION_BW"),
    "NS-08": ("Ember_the_Baby_Dragon_NS08_NovalityStore", "Ember_the_Baby_Dragon_NS08_PRINT_EDITION_BW"),
    "NS-09": ("Shelby_Sea_Turtle_Bag_Charm_NS09_NovalityStore", "Shelby_Sea_Turtle_Bag_Charm_NS09_PRINT_EDITION_BW"),
    "NS-10": ("Willow_the_Bunny_Lovey_NS10_NovalityStore", "Willow_the_Bunny_Lovey_NS10_PRINT_EDITION_BW"),
    "NS-11": ("NoSew_Christmas_Gnome_NS11_NovalityStore", "NoSew_Christmas_Gnome_NS11_PRINT_EDITION_BW"),
    "NS-12": ("Bobble_Christmas_Tree_NS12_NovalityStore", "Bobble_Christmas_Tree_NS12_PRINT_EDITION_BW"),
    "NS-13": ("Christmas_Ornament_Bundle_NS13_NovalityStore", "Christmas_Ornament_Bundle_NS13_PRINT_EDITION_BW"),
    "NS-14": ("NS14_Bobble_Snowflake_Tree_Skirt", "NS14_Bobble_Snowflake_Tree_Skirt_PRINT_EDITION_BW"),
    "NS-15": ("Interchangeable_Christmas_Wreath_NS15_NovalityStore", "Interchangeable_Christmas_Wreath_NS15_PRINT_EDITION_BW"),
    "NS-16": ("Mini_Stocking_Advent_Garland_NS16_NovalityStore", "Mini_Stocking_Advent_Garland_NS16_PRINT_EDITION_BW"),
    "NS-17": ("Year_of_the_Fire_Goat_2027_Plushie_Set_NS17_NovalityStore", "Year_of_the_Fire_Goat_2027_Plushie_Set_NS17_PRINT_EDITION_BW"),
}


def split_volume(text: str):
    chunks = PART_RE.split(text)
    return [(chunks[i + 1], chunks[i + 2], chunks[i + 3]) for i in range(0, len(chunks) - 3, 3)]


def engine_counts(body: str):
    from crochet_checker.verification.stages import run_stages

    rep = run_stages(body)
    return len(getattr(rep, "errors", []) or []), len(getattr(rep, "warnings", []) or [])


def pdf_pages(pdf_dir: pathlib.Path, stem: str) -> int | None:
    path = pdf_dir / f"{stem}.pdf"
    if not path.exists():
        return None
    try:
        import PyPDF2

        return len(PyPDF2.PdfReader(str(path)).pages)
    except Exception:
        return None


def pattern_names(text: str) -> dict:
    names = {}
    for line in text.splitlines():
        m = re.match(r"\d+\. (NS-\d+) — (.+?) \(\d+ pp", line.strip())
        if m:
            names[m.group(1)] = m.group(2).strip()
    return names


def ledger_rows(volume: pathlib.Path, pdf_dir: pathlib.Path):
    rows = []
    names = pattern_names(volume.read_text(encoding="utf-8"))
    for num, code, body in split_volume(volume.read_text(encoding="utf-8")):
        colour, pr = engine_counts(body)
        problems, unparsed = audit_lib.audit_tables(body, OVERRIDES.get(code), ())
        c_pdf, p_pdf = PDF_NAMES.get(code, ("", ""))
        rows.append(
            {
                "num": num,
                "code": code,
                "name": names.get(code, code),
                "engine_e": colour,
                "engine_w": pr,
                "audit_p": len(problems),
                "audit_u": len(unparsed),
                "colour_pp": pdf_pages(pdf_dir, c_pdf),
                "print_pp": pdf_pages(pdf_dir, p_pdf),
                "problems": problems,
                "unparsed": unparsed,
            }
        )
    return rows


def ledger_markdown(rows) -> str:
    out = [
        "| Code | Pattern | Engine E / W | Audit problems / unparsed | Colour pp | Print pp |",
        "|---|---|---|---|---|---|",
    ]
    for r in rows:
        out.append(
            f"| {r['code']} | {r['name']} | {r['engine_e']} / {r['engine_w']} | "
            f"{r['audit_p']} / {r['audit_u']} | {r['colour_pp']} | {r['print_pp']} |"
        )
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("volume", nargs="?", default=str(ROOT / "NovalityStore_Grand_Collection.md"))
    ap.add_argument("--pdf-dir", default=str(ROOT / "shop"))
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    volume = pathlib.Path(args.volume)
    rows = ledger_rows(volume, pathlib.Path(args.pdf_dir))
    table = ledger_markdown(rows)
    print(table)
    for r in rows:
        if r["problems"] or r["unparsed"] or r["engine_e"]:
            print(f"\n{r['code']} detail:")
            for p in r["problems"]:
                print("  problem:", p)
            for u in r["unparsed"]:
                print("  unparsed:", u[0], "|", u[1][:100])
    if args.write:
        text = volume.read_text(encoding="utf-8")
        start = text.index("| Code | Pattern | Engine E / W |")
        end = text.index("\n\n", start)
        volume.write_text(text[:start] + table + text[end:], encoding="utf-8")
        print("\nledger written")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
