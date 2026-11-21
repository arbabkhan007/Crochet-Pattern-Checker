# NS 01 PDF asset preflight and human photo QA

This checklist is specific to the current NS 01 PDF layout. The render pipeline measures image pixels at their actual placed size and checks the generated PDF's page count and page bounds. It does **not** infer yarn identity, hook engraving, construction consistency, physical testing, or toy-safety compliance from an image.

## Current canonical pattern facts

The authoritative pattern text is `patterns/01_Hamish_the_Highland_Cow.md`. PDF data and placement labels are compiled from that file on each build; this document and the JSON Schema are not a second copy of its instructions.

The current master specifies about 15 cm finished size, a 3.5 mm / US E-4 hook, an 11 sc × 12 rounds per 5 cm gauge, a closed head ending at R16 with 6 stitches, and an open 18-stitch body neck at R19. The assembly joins the 18 body R19 stitches to 18 head R14 stitches. The eyes go between R9 and R10, 7 stitches apart. These values differ from the supplied draft's 24-stitch open head/body openings and different round placements, so the draft values are not used here.

The leg instructions use Yarn C through R5 and change to Yarn A at R6. Do not change this to a six-round hoof color block without revising and revalidating the canonical pattern.

## One-sided insert-size threshold

The compiled model records the canonical 12 mm safety-eye diameter. `tools/ns01_pdf_model.py` exposes `insert_exceeds_crochet_threshold(insert_diameter_mm, crochet_diameter_mm)`, which flags only when `insert_diameter > 1.15 × crochet_diameter`; both inputs must use the same units. There is no lower threshold and no 0.85–1.15 fit band. The Markdown master does not state a measured crochet-opening diameter, so the PDF build does not calculate or claim an NS01 eye-fit result. This numerical check is not a physical fit test or a safety certification.

## Current asset-resolution report

Run:

```text
python tools/ns01_pdf_asset_qa.py
```

The checker measures the current files against the actual image boxes used by `tools/build_ns01_etsy_pdf.py` (contain-fit, not an assumed full-page crop). The checked-in files are named as concept illustrations and currently fall below the 300 effective-DPI target. A layout PDF can still be built, but these assets are not automatically cleared for a final print release. `--strict` fails until both the resolution checks and the human checklist are complete.

## Human review — complete every item before final photo release

- [ ] Confirm the visible leg color split matches the master: Yarn C through Rnd 5, with the change to Yarn A on Rnd 6.
- [ ] Compare each named yarn and its stated role with the cover and materials visuals; record any color or role that is not shown clearly.
- [ ] Record each asset's creator/source, provenance, usage rights, and required attribution; retain evidence with the release record.
- [ ] Inspect any visible hook, ruler, or yarn-label marking at 200%; confirm a visible hook is marked 3.5 mm or remove/obscure any conflicting marking.
- [ ] Confirm the cover and materials visuals are construction-consistent with the written low, seated pose; identify concept art as illustrative rather than a photograph of a finished sample.
- [ ] Replace concept assets with images meeting the 300 effective-DPI target at their actual placed sizes, or document and approve a different print-resolution target.
- [ ] Confirm the visuals do not imply physical prototyping, product testing, or toy-standard certification that has not occurred.

## Automated PDF regression

`tools/build_ns01_etsy_pdf.py` postflight checks the generated A4 page range, required source text, metadata, bookmarks, vector/raster policy for each edition, and that extracted text remains within each page's physical bounds. The existing generator uses ReportLab and its expected page range; this is not the separate four-page HTML proposal. The text-bounds check is page-level and does not claim to inspect HTML table-cell bounding boxes.

Use temporary output paths so release PDFs are not replaced during review:

```text
python tools/build_ns01_etsy_pdf.py \
  --output /tmp/NS01-review.pdf \
  --printer-output /tmp/NS01-printer-review.pdf
```

The vector placement figure is schematic and explicitly not to scale. Follow the written instructions for construction and placement. No loop-to-loop join map is generated.
