"""Shared schema + constants for the Novality Store pattern audit pipeline.

A pattern is a dict:

    {
      "id":            str,          # slug, e.g. "hamish"
      "number":        int,          # sales-line number 1..10
      "design_code":   str,          # e.g. "NS 01"
      "title":         str,
      "tagline":       str,          # short intro paragraph
      "meta":          [str, ...],   # cover badges: terms / skill / time
      "finished_size": [str, ...],   # bullet lines
      "safety":        [str, ...],   # safety paragraphs
      "materials":     [str, ...],   # bullet lines
      "gauge":         [str, ...],   # paragraph lines
      "abbreviations": [str, ...],   # "abbr - meaning" lines
      "construction":  str,          # general working note (optional "")
      "techniques":    [(name, body), ...],   # numbered technique box
      "notes":         [str, ...],   # extra pattern notes (optional)
      "pieces":        [ piece, ... ],
      "assembly":      [...],        # finishing / assembly lines
      "troubleshooting": [(problem, fix), ...],
      "colorways":     [str, ...],
      "extras":        [...],        # pattern specific extra sections
      "terms":         {...},        # terms of use text blocks
      "closing":       str,          # happy crocheting text
    }

piece = {
    "name":   str,            # e.g. "Head (Cream)"
    "intro":  str,            # lead-in paragraph (optional "")
    "kind":   "table"|"text", # table of rounds/rows vs free text
    "subpieces": [ subpiece, ... ]  # optional named variants
}

subpiece = {
    "name":   str,            # e.g. "INNER ear - Yarn B (make 2)" or ""
    "rows":   [ row, ... ],
    "notes":  [str, ...],     # trailing notes for the sub piece
}

row = {
    "label":   "R1",          # Rnd/Row label (may be "R4-6" span)
    "text":    "6 sc in MR",  # instruction as printed in the customer pattern
    "stated":  18 or None,    # stated stitch count, None if not stated
    "cons":    18 or None,    # stitches consumed entering this row (hand-computed)
    "prod":    18 or None,    # stitches produced leaving this row (hand-computed)
    "check":   "sc in ...",   # optional normalized string the repo parser handles
    "note":    "",            # note column
    "skip_check": False,      # decorative/informational rows
}

cons/prod are computed twice: by hand (stored here) and, where "check"
is present, by the repository's own parser.  The audit refuses a pattern
if the two disagree or if cons != previous prod or stated != prod.
"""

BRAND = "Novality Store"
COPYRIGHT_NOTICE = (
    "\u00a9 2026 Novality Store. All rights reserved.\n\n"
    "This pattern is for personal use only. You may sell finished items made from "
    "this pattern, but you may not copy, redistribute, resell, share, translate, "
    "reproduce, or claim this pattern as your own. The pattern itself may not be "
    "uploaded, reproduced, or distributed in digital or printed form without "
    "permission from Novality Store."
)

FOOTER_LINE = "\u00a9 2026 Novality Store - personal use only"
