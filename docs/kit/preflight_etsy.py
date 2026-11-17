#!/usr/bin/env python3
"""Pre-flight QA for the NS-13 shop files.

Checks the two customer editions against the packaging brief:
page size, page count, bookmarks, banned strings, US spelling,
single copyright line, a true 50 mm ruler, embedded fonts and Etsy's
file-size ceiling.

    python3 docs/kit/preflight_etsy.py
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[2]
FILES = [
    ROOT / "deliverables/NS13_Christmas_Ornament_Bundle_Colour_Edition.pdf",
    ROOT / "deliverables/NS13_Christmas_Ornament_Bundle_Print_Edition.pdf",
]

BANNED = ["Corrected", "TIME UNVERIFIED", "RECORD SAMPLE", "crochet-check",
          "machine-verified", "Deterministic", "Seller notes", "remove before publishing",
          "Carry over", "TODO", "lorem"]
UK = ["colour", "colourway", "centre", "fibre", "labelling", "labelled", "jewellery"]

A4 = (595.28, 841.89)
RULER_PT = 141.732          # 50 mm
TOL = 0.6
MAX_BYTES = 20 * 1024 * 1024


def check(path: Path) -> list[str]:
    out: list[str] = []
    ok = lambda m: out.append("PASS  " + m)
    bad = lambda m: out.append("FAIL  " + m)

    if not path.exists():
        bad(f"{path.name} missing")
        return out
    doc = pymupdf.open(path)
    text = "\n".join(p.get_text() for p in doc)

    (ok if abs(doc[0].rect.width - A4[0]) < 1 and abs(doc[0].rect.height - A4[1]) < 1
     else bad)(f"page size {doc[0].rect.width:.1f} x {doc[0].rect.height:.1f} pt (A4 expected)")

    (ok if doc.page_count >= 4 else bad)(f"{doc.page_count} pages")

    toc = doc.get_toc()
    (ok if len(toc) >= 5 else bad)(f"{len(toc)} bookmarks")

    hits = [b for b in BANNED if b.lower() in text.lower()]
    (ok if not hits else bad)("no internal/verification language" +
                              ("" if not hits else " -> " + ", ".join(hits)))

    ukhits = sorted({u for u in UK if re.search(r"\b" + u, text, re.I)})
    (ok if not ukhits else bad)("US spelling only" +
                                ("" if not ukhits else " -> " + ", ".join(ukhits)))

    per_page = [p.get_text().count("\u00a9") for p in doc]
    (ok if all(n == 1 for n in per_page) else bad)(
        "one copyright line per page, in the footer -> " + str(per_page))

    found = 0
    for page in doc:
        for d in page.get_drawings():
            r = d["rect"]
            if abs(r.width - RULER_PT) < TOL:
                found += 1
    (ok if found else bad)(f"50 mm ruler found at 1:1 ({found} bar)")

    used = set()
    for page in doc:
        for b in page.get_text("dict")["blocks"]:
            for line in b.get("lines", []):
                for span in line["spans"]:
                    used.add(span["font"])
    fonts = doc.get_page_fonts(0)
    by_base = {f[3].split("+")[-1]: f for f in fonts}
    not_embedded = [n for n in sorted(used)
                    if not (by_base.get(n) and by_base[n][1] not in ("n/a", ""))]
    (ok if not not_embedded else bad)(
        "every used font embedded: " + ", ".join(sorted(used)) +
        ("" if not not_embedded else " -> missing " + ", ".join(not_embedded)))

    size = os.path.getsize(path)
    (ok if size < MAX_BYTES else bad)(
        f"{path.name} {size/1024/1024:.2f} MB (Etsy limit 20 MB)")

    return out


def main() -> int:
    fails = 0
    for f in FILES:
        print("=" * 68)
        print(f.name)
        for line in check(f):
            print("  " + line)
            fails += line.startswith("FAIL")
    print("=" * 68)
    print("PRE-FLIGHT " + ("PASSED" if not fails else f"FAILED ({fails} checks)"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
