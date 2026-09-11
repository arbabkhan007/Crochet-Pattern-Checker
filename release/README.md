# Customer pattern PDFs

## NS 01 — Hamish the Highland Cow

The composed A4 customer PDF for Design Code **NS 01** is:

`NS01_Hamish_the_Highland_Cow_Crochet_Pattern.pdf`

It uses **Novality Crochet Studio** branding, named original-colour swatches,
a materials visual, an assembly map, bookmarks, repeated table headers,
selectable text, copyright notices and a light interior-style closing page.

The cover and materials visuals are illustrative rather than physical test
evidence. Before an Etsy listing goes live, the owner must complete the
outstanding sample/test, title/provenance, product-safety and listing-disclosure
gates recorded in `reports/commercial_readiness.md`. In particular, review
Etsy's current disclosure requirement for seller-prompted AI artwork.

## Rebuild and postflight

```bash
python -m venv /tmp/novality-pdf
/tmp/novality-pdf/bin/pip install -r requirements-release-pdf.txt
/tmp/novality-pdf/bin/python tools/build_ns01_etsy_pdf.py
```

The builder rejects missing branding, design codes, bookmarks, required
sections, critical construction phrases, raw Markdown, proof-only labels,
non-A4 pages, incorrect image counts and files at or above Etsy's 20 MB limit.
