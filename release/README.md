# Customer pattern PDFs

## NS 01 — Hamish the Highland Cow

The A4 customer set for Design Code **NS 01** contains two files:

- `NS01_Hamish_the_Highland_Cow_Crochet_Pattern.pdf` — the full-colour
  customer edition;
- `NS01_Hamish_the_Highland_Cow_PRINTER_SAVER.pdf` — a black-on-white,
  image-free companion for economical home printing.

Both editions use **Novality Crochet Studio** branding, named original colours,
selectable text, bookmarks, repeated table headers, copyright notices and
printable `[ ]` progress boxes on every construction-table row. Both also
contain the explicit 10-round shortened-front-leg table and placement method.

The full-colour edition adds a materials visual, an assembly map and a light
interior-style closing page. The printer-saver edition contains no raster image
objects, uses white page backgrounds and ends with a project checklist and
ruled notes page.

The Head Rnd 11 instruction is `[5 sc, dec] x 6`, reducing 42 stitches to 36.
It must not be replaced by `sc in each st around`, because that would leave 42
stitches and contradict the stated count.

The cover, materials and assembly visuals are illustrative rather than physical
test evidence. No real NS 01 process photographs were supplied, so real ear,
fringe and leg progress photographs are deferred rather than fabricated or
borrowed. When rights-cleared photographs of the tested sample are available,
replace the assembly map with one high-contrast three-panel progress plate to
keep the full-colour edition within its three-image limit.

Before an Etsy listing goes live, the owner must complete the outstanding
sample/test, title/provenance, product-safety and listing-disclosure gates in
`reports/commercial_readiness.md`. In particular, review Etsy's current
disclosure requirement for seller-prompted AI artwork.

## Rebuild and postflight

```bash
python -m venv /tmp/novality-pdf
/tmp/novality-pdf/bin/pip install -r requirements-release-pdf.txt
/tmp/novality-pdf/bin/python tools/build_ns01_etsy_pdf.py
```

The default build produces and postflights both PDFs. The full-colour gate
checks for exactly three raster visuals. The printer-saver gate rejects every
raster object and checks its edition metadata, progress boxes and critical
instructions. Both gates reject missing identity, sections or bookmarks; raw
Markdown; proof-only labels; non-A4 pages; and oversized output.
