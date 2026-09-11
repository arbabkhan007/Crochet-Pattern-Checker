"""Build the Christmas Collection PDFs.

One PDF per pattern; each PDF contains the COMPLETE pattern twice:
first in US terms, then in UK terms (own cover divider with a UK-terms badge).

Outputs (3 PDFs) under final_patterns/christmas/:
  NS11_No-Sew_Christmas_Gnome.pdf
  NS12_Bobble_Christmas_Tree.pdf
  NS13_Christmas_Ornament_Bundle.pdf
"""
from __future__ import annotations

from tools.novality import build_pdfs
from tools.novality_xmas import PATTERNS
from tools.novality_xmas.uk_terms import to_uk

SLUGS = {
    "gnome": "NS11_No-Sew_Christmas_Gnome",
    "tree": "NS12_Bobble_Christmas_Tree",
    "bundle": "NS13_Christmas_Ornament_Bundle",
}


def build_all():
    results = []
    for p in PATTERNS:
        uk = to_uk(p)
        out, pages = build_pdfs.build_dual(p, uk, f"christmas/{SLUGS[p['id']]}")
        results.append((out.name, pages))
        print(f"built {out} ({pages} pages, US + UK combined)")
    return results


if __name__ == "__main__":
    build_all()
