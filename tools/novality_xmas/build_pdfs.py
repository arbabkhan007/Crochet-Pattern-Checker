"""Build the Christmas Collection PDFs: each pattern in US and UK terms.

Outputs (6 PDFs) under final_patterns/christmas/:
  X01_No-Sew_Christmas_Gnome_US.pdf   X01_No-Sew_Christmas_Gnome_UK.pdf
  X02_Bobble_Christmas_Tree_US.pdf    X02_Bobble_Christmas_Tree_UK.pdf
  X03_Christmas_Ornament_Bundle_US.pdf X03_Christmas_Ornament_Bundle_UK.pdf
"""
from __future__ import annotations

from tools.novality import build_pdfs
from tools.novality_xmas import PATTERNS
from tools.novality_xmas.uk_terms import to_uk

SLUGS = {
    "gnome": "X01_No-Sew_Christmas_Gnome",
    "tree": "X02_Bobble_Christmas_Tree",
    "bundle": "X03_Christmas_Ornament_Bundle",
}


def build_all():
    results = []
    for p in PATTERNS:
        for suffix, patt in (("US", p), ("UK", to_uk(p))):
            q = dict(patt)
            q["file_slug"] = f"christmas/{SLUGS[p['id']]}_{suffix}"
            out, pages = build_pdfs.build(q)
            results.append((out.name, pages))
            print(f"built {out} ({pages} pages)")
    return results


if __name__ == "__main__":
    build_all()
