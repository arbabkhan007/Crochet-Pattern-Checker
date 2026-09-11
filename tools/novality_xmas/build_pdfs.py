"""Build the Christmas Collection PDFs.

One PDF per pattern, written in ONE flow: every round shows the US-terms
instruction and the exact UK equivalent side by side; stitch counts once.

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
        out, pages = build_pdfs.build_dual_rows(p, uk, f"christmas/{SLUGS[p['id']]}")
        results.append((out.name, pages))
        print(f"built {out} ({pages} pages, dual US|UK rows)")
    return results


if __name__ == "__main__":
    build_all()
