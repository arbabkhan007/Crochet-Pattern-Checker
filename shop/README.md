# Novality Store — shop editions

34 PDFs: for each of the seventeen design codes NS-01 … NS-17 there is a **colour store edition**
(`*_NSnn_NovalityStore.pdf`) and a **monochrome print edition** (`*_NSnn_PRINT_EDITION_BW.pdf`,
greyscale spread 0 on every page, sized for home inkjet/laser printers).

These are compiled pattern documents, not checker output. Each is built from the corrected master in
`docs/nsNN/NSNN_corrected.md` by `docs/kit/build_store_pdf.py` (NS-03 by `docs/ns03/build_ns03*.py`,
NS-14 by `docs/ns14/build_pdf_v2.py` and `build_pdf_bw.py`). Rebuild one with:

```
.venv/bin/python docs/kit/build_store_pdf.py docs/ns05/spec.py          # colour
.venv/bin/python docs/kit/build_store_pdf.py docs/ns05/spec.py --bw     # print
```

**Every edition is paper-verified, not sample-verified.** The cover chip reads *5-AXIOM MATH
VERIFIED ON PAPER* and the cover states that no sample was crocheted, blocked, weighed or measured:
the stitch arithmetic is proved from the instruction text, while sizes, yarn quantities and times
are derived targets. Cover artwork is an illustrative render of the written design, not a photograph
of a sample — listings must carry the matching AI-disclosure sentence.

Branding is uniform across all seventeen: copyright and finished-item credit are **Novality Store**,
the designer credit is *designed by Novality Crochet Studio*, and the project hashtag is
**#NovalityStore**.
