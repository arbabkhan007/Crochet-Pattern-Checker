#!/usr/bin/env python3
"""Generate retail + print PDFs for the whole Novality line (NS 01-09, plus
Willow NS 10 which has its own generator)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from pattern_pdf_lib import build  # noqa: E402
from content_ns0103 import HAMISH, KAWAII, AXEL  # noqa: E402
from content_ns0406 import COCO, DUCK, MOMO  # noqa: E402
from content_ns0709 import TRIO, EMBER, SHELBY  # noqa: E402

SPECS = [HAMISH, KAWAII, AXEL, COCO, DUCK, MOMO, TRIO, EMBER, SHELBY]


def main():
    only = sys.argv[1:] or None
    for spec in SPECS:
        if only and spec["slug"] not in only:
            continue
        build(spec, "retail")
        build(spec, "print")


if __name__ == "__main__":
    main()
