# Crochet Pattern Collection: Technical Edit and Commercial Readiness Report

- **Review date:** 11 September 2026
- **Scope:** 15 Markdown pattern masters, Design Codes NS 01–NS 15
- **Intended channel:** Etsy digital downloads

## Release decision

| Gate | Result |
|---|---|
| Customer-facing Markdown inventory and structure | **PASS** |
| Desk-based stitch arithmetic and continuity | **PASS** |
| US/UK table parity where dual terminology is offered | **PASS** |
| Safety/care wording desk review | **PASS, subject to legal and regulatory review** |
| Sample crochet of every design and advertised option | **NOT PERFORMED — BLOCKING** |
| Independent pattern testing | **NOT PERFORMED — BLOCKING** |
| Yarn-use, size, time, wash and durability measurements | **NOT PHYSICALLY VERIFIED — BLOCKING** |
| Ownership, provenance, title and brand clearance | **NOT CLEARED — BLOCKING** |
| Market-specific legal/product-safety review | **NOT PERFORMED — BLOCKING** |
| Real sample photography and final PDF preflight | **FINAL ASSETS NOT PRESENT — BLOCKING** |
| Etsy listing compliance and disclosure review | **NOT COMPLETED — BLOCKING** |
| Overall decision | **HOLD — do not list for sale yet** |

“PASS” in this report means only that the current text passed the stated desk or automated check. It is not a claim that a crocheted object exists, that a customer can complete it without difficulty, that quantities or dimensions have been measured, or that any finished item complies with a safety standard.

## What was checked and corrected

All 15 masters were read as customer instructions rather than accepted from generator metadata. Corrections were made directly in `patterns/` for stitch arithmetic, construction order, access before closure, matched seam counts, supplies, dimensions, terminology, headings, safety language, care language and licensing consistency.

The final release gate reads the Markdown itself and currently reports:

- **15** expected files and **15** unique sequential design codes;
- **532** Markdown table rows;
- **110** side-by-side US/UK instruction rows with exact token translation;
- **507** count-bearing rows independently evaluated;
- **2,470** total assertions;
- canonical increase/decrease continuity plus explicit arithmetic for every non-canonical count-bearing construction;
- required safety, materials, gauge, abbreviations, instructions, finishing/assembly, troubleshooting, care and terms sections;
- semantic heading hierarchy, table shape, file hygiene and high-risk release safeguards.

The gate is `tools/pattern_release_audit.py`. A final desk suite passed on 11 September 2026:

- release audit: 15 files, 532 table rows, 110 dual-terminology rows, 507 count rows and 2,470 assertions;
- project Python suite: 97 tests passed, including the release gate and four mutations; two third-party FastAPI/Starlette deprecation warnings remain outside the pattern masters;
- Python compilation and Ruff static analysis: pass;
- `codespell` 2.4.1: pass after allowing only the declared crochet abbreviation `FO` and intentional Scots word `wee`;
- structural Markdownlint: 16 files (15 patterns plus this report), zero findings, with only line length, trailing heading punctuation and compact-table style disabled;
- GFM-to-HTML render: 16 files, one H1 each, 77 recognized pattern tables and balanced table tags;
- `git diff --check`: pass.

The permanent test suite also mutation-tests the gate. Four defects—an incorrect expected round count, an incorrect UK stitch translation, removal of the NS 10 load-bearing seam wording and removal of a required care section—each produce a non-zero exit and a localized finding.

### Collection-wide corrections

- Replaced misleading blanket claims such as “baby-safe”, simplistic age-label workarounds and “adult collectible” classification shortcuts. The patterns now state that embroidery or a warning removes only a particular hazard and does not prove overall compliance.
- Added market-neutral language covering intended and reasonably foreseeable use, assessment, testing, documentation, labelling and traceability.
- Added or strengthened complete-sample care testing in every pattern. A yarn ball label alone no longer supports laundering claims for an assembled and stuffed item.
- Standardized the finished-item licence: purchasers may sell small-batch finished physical items with credit, but may not redistribute the pattern itself. The wording still requires legal review before publication.
- Rebuilt heading levels so the masters can later become navigable, accessible PDFs.
- Added missing abbreviations and removed internal-review or tentative wording from customer-facing text.

### Per-pattern desk findings

| Code | Pattern | Principal corrected or verified points | Mandatory physical focus |
|---|---|---|---|
| NS 01 | Hamish the Highland Cow | Restored fully completed nested ears; corrected muzzle access, eye-lock timing, fringe arithmetic, yarn allowance and the 18-to-18 head/body join. | Neck rigidity and two-pass seam; nested-ear thickness; fringe security; seated balance; actual yarn use and size. |
| NS 02 | Kawaii Halloween Mini Set | Corrected Boo’s open base, Pip’s sculpting/face order and tendril, Bramble’s wing arithmetic, optional-hat inventory and nine-mini garland quantities/components. | Make all three minis plus every advertised base/hat/garland option; verify standing, sculpting, wing symmetry and hanging system. |
| NS 03 | Axel the Axolotl | Corrected face access, dorsal anchors, closure wording and fin placement; round ladder rechecked. | Gill shedding/matting, neck posture, fin crowding, limb placement and both advertised adjustment options. |
| NS 04 | Coco the Capybara | Repaired component tables and face timing; leg joins now pass through both flattened leg layers and the body stitch. | Three-layer joins, four-leg alignment, sitting/standing stability, muzzle and ear seams. |
| NS 05 | Little Duck Plushie | Corrected beak construction, component order, closure, gauge/supply assumptions and embroidered-face access. | Chenille shedding, gauge spread by brand, beak shape, waist/neck shape, wing seams, stuffing and every advertised yarn-size result. |
| NS 06 | Momo the Loaf Cat | Corrected oval-base arithmetic, face access, surface-worked ear anchoring, tail order and “no-sew” marketing wording. | Ear/tail anchors, oval shape, top closure, stuffing distribution and actual one-piece appearance. |
| NS 07 | Pocket Positivity Trio | Corrected Sunny’s 18-anchor/36-stitch petal round, Waddle component timing, Spud closure and safety-eye access. | Make all three; check tiny-eye/fabric interaction, petal lay, sewn chest/beak/wings and the four-stitch Spud closure. |
| NS 08 | Ember the Baby Dragon | Rebuilt the spine to use exactly 33 anchors, retained an 18-to-18 open neck join, corrected face access, supplies and leg closure. | Heavy-head support, spine length, seated balance, four legs, wing/horn seams and whether a belly piece was intended. |
| NS 09 | Shelby the Sea Turtle Bag Charm | Reworked shell/underside construction to preserve 24 exposed loops for a 24-to-24 seam; enlarged version preserves 42. Plastic eyes were removed from the tiny head fan. | Make both sizes; check seam shape, French-knot placement, stuffing, keyring abrasion and attachment durability. |
| NS 10 | Willow the Bunny Lovey | Restored head/ear arithmetic, 240 + 12 = 252 border, gauge and diagonal calculations; the head is sewn twice around all 18 marked Head Rnd-12 stitches rather than carried by the six-stitch closure. | Highest-priority destructive seam and laundering test; blanket drape, border corners, shrinkage, infant-sleep wording and 4–6 hour estimate. |
| NS 11 | No-Sew Christmas Gnome | Verified colour-band shaping and component counts; clarified eye/face access and “no assembly seams” versus nose/beard tacking. | Colour joins, nose/beard anchors, hat tip, stuffing and optional-eye version. |
| NS 12 | Bobble Christmas Tree | Corrected contrast-bobble colour sequence and insert sizing/timing; full decrease ladder verified. | Base-disc fit, upright stability, bobble columns, three advertised yarn weights and cardboard non-washability. |
| NS 13 | Christmas Ornament Bundle | Verified the star’s 35 counted stitches plus five uncounted ch-2 spaces and clarified fibre-appropriate blocking and loops. | Make bauble, star and snowflake; blocking repeatability, hanging balance, loop security and storage recovery. |
| NS 14 | Bobble Snowflake Tree Skirt | Verified the 12-column progression and all three size endings; strengthened measurement, heat and care cautions. | Crochet every advertised size or obtain equivalent tester samples; measure opening/diameter, yarn use, drape, flatness and wash change. |
| NS 15 | Interchangeable Christmas Wreath | Corrected circumference/diameter relationships, round tube ends, full-tube join, two-ended decoration ties and whole-tube hanger. | Build every advertised size; long-term roundness, door exposure, tube seam, decoration ties and complete hanging system under real use. |

## Mandatory sample-crochet and tester gate

At least **21 core objects** are required to cover the 15 files at their primary size: NS 02 contains three designs, NS 07 contains three and NS 13 contains three. That minimum does **not** cover advertised alternate sizes, yarn weights or optional modules. Every option retained in the final product description must either be physically made and checked or be removed until tested.

For each design and retained option:

1. **Freeze a test draft.** Give testers the exact PDF candidate, not an editable document and not verbal corrections.
2. **Record materials.** Brand, line, fibre, colour, lot, stated metres per gram, hook, eye/washer supplier, stuffing and every notion.
3. **Measure before and after.** Swatch gauge; component width/height/depth; finished dimensions; mass; yarn mass by colour; stuffing mass; and elapsed active time.
4. **Photograph construction checkpoints.** Open-access face stage, every unusual join, pre-stuff shape, completed assembly and post-care condition.
5. **Test the proposed care method on the whole item.** Fully dry it, remeasure, and inspect dye transfer, shrinkage, fibre shedding/matting, stuffing migration, corrosion, embroidery, seams and shape.
6. **Exercise intended use.** Sit, hang, carry or drape the piece as marketed. Treat in-house tugging or hanging as developmental checks only, not as compliance evidence; use the forces, conditioning and methods required by the applicable standard and qualified adviser.
7. **Use independent testers.** At least two per core design is recommended: one at the stated skill level and one more experienced tester. Each bundle component must be made. Testers should first work without live help and log every question, assumption, count discrepancy, yarn shortage and measured result.
8. **Close every finding.** Revise the master, increment a version/date, regenerate the PDF, and have the affected step retested. A release candidate should have no unresolved blocker, no silent correction communicated only in chat and no quantity or dimension based solely on calculation.

Extra samples are specifically required for NS 09’s enlarged Shelby, NS 12’s three yarn-weight presentation, NS 14’s three sizes and NS 15’s three sizes. The same rule applies to any NS 02 hat/base/garland, NS 03 adjustment or NS 05 scale that will be advertised.

## Product-safety and legal gate

The Markdown now avoids claiming certification, but wording cannot replace legal review or testing. Obtain market-specific advice before sale, especially because the licence expressly permits purchasers to make finished items.

- **United States:** CPSC states that ASTM F963 is mandatory for children’s toys through 16 CFR part 1250 and describes testing, certification and tracking-label duties. Small-batch status does not remove the duty to comply or issue the required certificate where applicable: [CPSC Toy Safety Business Guidance](https://www.cpsc.gov/Business--Manufacturing/Business-Education/Toy-Safety), [ASTM F963 requirements chart](https://www.cpsc.gov/Business--Manufacturing/Business-Education/Toy-Safety/ASTM-F-963-Chart), and [Small Batch guidance](https://www.cpsc.gov/Business--Manufacturing/Small-Business-Resources/Small-Batch-Manufacturers-and-Third-Party-).
- **Great Britain:** official guidance requires toys to meet essential safety requirements and addresses safety assessment, conformity assessment, technical records, manufacturer identification, warnings and markings: [Toys (Safety) Regulations 2011 guidance](https://www.gov.uk/government/publications/toys-safety-regulations-2011/toys-safety-regulations-2011-great-britain).
- **European Union:** determine which rules and transition dates apply when the product is placed on the market. Official sources describe safety assessment, technical documentation and CE responsibilities: [Directive 2009/48/EC](https://eur-lex.europa.eu/eli/dir/2009/48/oj/eng) and [Regulation (EU) 2025/2509](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX%3A32025R2509).

A cute stuffed object may be classified by intended and reasonably foreseeable play, not just by calling it “decor”, “bag charm” or “adult collectible”. Likewise, an embroidered face removes plastic eye components but does not address flammability, chemistry, seam strength, fibre release, cords, hygiene, labelling or traceability. Have a qualified product-safety professional or accredited laboratory define the actual test plan; do not invent pass forces or apply a compliance mark without the complete required basis.

The owner should also have counsel review the finished-item licence, copyright notice, warranty/disclaimer strategy, privacy/contact information, consumer digital-content terms, tax treatment and target-country listing obligations. This report is technical QA, not legal advice.

## Ownership, originality, title and brand gate

### Provenance

Every master currently says that it is original Novality Store work designed by Novality Crochet Studio. The repository does not contain enough evidence to verify that claim. Before release, preserve and review:

- original dated sketches, swatches, drafts and revision history;
- the identity and written assignment/licence of every contributing designer, editor, photographer and illustrator;
- source/licence records for fonts, templates, diagrams and other assets;
- proof that final sample and process photographs belong to the seller;
- an originality comparison where an existing product has the same character name and concept.

Etsy’s current Creativity Standards require digital downloads to be sellers’ original designs and require disclosure for seller-prompted AI creations: [Etsy Creativity Standards](https://www.etsy.com/legal/handmade). These masters have received AI-assisted technical editing in this workspace. Record that history and obtain a current Etsy-policy determination on the listing disclosure; a conservative accurate disclosure is preferable to representing the work as wholly unassisted. Etsy also states that sellers are responsible for having the necessary rights to their content: [Etsy Intellectual Property Policy](https://etsy.com/legal/ip/).

### Marketplace name collisions found

This was a limited marketplace/web screen, **not** a trademark search or legal clearance. A result does not by itself prove infringement, and no result proves availability. Nevertheless, the following names should not be launched unchanged without an owner decision and qualified clearance. Sources were checked on 11 September 2026.

| Code | Current name | Screen result | Action |
|---|---|---|---|
| NS 01 | Hamish the Highland Cow | Multiple earlier crochet patterns use the exact title, including a 2017 Ravelry entry and active Etsy listings: [Ravelry](https://www.ravelry.com/patterns/library/hamish-the-highland-cow), [Etsy listing 759679967](https://www.etsy.com/listing/759679967/pattern-hamish-the-highland-cow-crochet), [Etsy listing 710698860](https://www.etsy.com/listing/710698860/hamish-the-highland-cow-coo-cattle). | Rename and clear, or obtain a reasoned legal clearance before listing. Review visual/construction provenance as well as the title. |
| NS 03 | Axel the Axolotl | The exact title is used by several paid/free patterns: [The Blue Elephants](https://www.theblueelephants.com/axel-free-axolotl-crochet-pattern/), [Ribblr](https://ribblr.com/pattern/axel-the-axolotl-Crochet-2/), [Ravelry](https://www.ravelry.com/patterns/library/axel-the-axolotl-3), and [Etsy listing 1737029892](https://www.etsy.com/listing/1737029892/axel-the-axolotl-no-sew-crochet-pattern). | Treat as a high-priority rename/provenance review. |
| NS 04 | Coco the Capybara | Exact-name crochet products and patterns exist, including [A Little Ripple’s kit](https://alittleripple.com/products/coco-the-capybara-crochet-kit) and a [2025 Ribblr tester call](https://meet.ribblr.com/t/tester-call-for-crochet-coco-the-capybara-yuzu/635378) for an exact-name pattern. | Rename and clear; compare source history before asserting uniqueness. |
| NS 06 | Momo the Loaf Cat | A 2023 “MoMo the Cat” crochet pattern is documented by a [Scribd index entry](https://www.scribd.com/document/896062055/Bigbebez-MoMothecat-F-2). The full title is not identical, but the character name/category is close and loaf-cat patterns are crowded. | Owner/counsel review; a more distinctive cleared name is advisable. |
| NS 07 | Sunny the Sunflower | Exact paid pattern title: [The Weaving Witch](https://www.theweavingwitch.com/shop/p/crochet-pattern-sunny-the-sunflower-amigurumi). | Rename and clear all three component characters, not just the bundle title. |
| NS 07 | Waddle the Penguin | Exact paid PDF title: [Etsy listing 1108283996](https://www.etsy.com/listing/1108283996/waddle-the-penguin-amigurumi-crochet-pdf). | Rename and clear. |
| NS 07 | Spud the Potato | Exact paid PDF title: [Etsy listing 1135809719](https://www.etsy.com/listing/1135809719/spud-the-potato-crochet-pattern-pattern). | Rename and clear. |
| NS 08 | Ember the Baby Dragon | Exact and very close crochet products exist, including an [Etsy market result](https://www.etsy.com/market/ember_dragon) using “Crochet Pattern Ember the Baby Dragon”, “Baby Ember the Dragon” at [Knottypod](https://knottypod.com/product-details/product/670550f743d93c85f93ee420), and a paid 2014 [Ember the Dragon pattern](https://www.ravelry.com/patterns/library/ember-the-dragon). | Highest-priority rename and provenance comparison before sale. |
| NS 09 | Shelby the Sea Turtle Bag Charm | “Shelby the Sea Turtle” is a paid pattern published in April 2019: [Ravelry](https://www.ravelry.com/patterns/library/shelby-the-sea-turtle). “Bag Charm” does not eliminate the shared character title. | Rename and clear. |
| NS 10 | Willow the Bunny Lovey | Exact-title free and paid pattern with the same general bunny-lovey concept: [free pattern](https://www.theblueelephants.com/willow-the-bunny-lovey-free-crochet-pattern/), [shop](https://shop.theblueelephants.com/products/willow-the-bunny-lovey-crochet-pattern), [Etsy listing 1041281046](https://www.etsy.com/listing/1041281046/crochet-pattern-willow-the-bunny-lovey). | Highest-priority rename and originality/provenance comparison before sale. |

NS 11 (“No-Sew Christmas Gnome”) and NS 12 (“Bobble Christmas Tree”) also use extremely crowded descriptive marketplace wording; exact or near-exact phrases appear throughout Etsy’s [crochet-gnome results](https://www.etsy.com/market/crochet_gnome_pattern) and [bobble-tree results](https://www.etsy.com/market/bobble_tree). That is not the same as a distinctive character-name collision, but unique cleared product names would reduce confusion and improve branding. NS 02, NS 05 and NS 13–NS 15 did not produce the same level of distinctive-title concern in this limited screen; they still require normal clearance.

Do not silently invent replacement names and call them cleared. The owner should select a coherent naming system, then search relevant trademark registers, Etsy, Ravelry, search engines, social handles and domains in all target markets. Clear “Novality Store”, “Novality Crochet Studio” and the proposed hashtags at the same time.

### Owner decisions still required

1. **NS 05 design code:** its recovered source described “NS 05” as tentative. Confirm the code and studio attribution in writing.
2. **NS 08 design intent:** an earlier materials description referred to a belly although no belly construction existed. The corrected master assumes there is no separate belly piece. The designer must confirm that decision.
3. **Authorship/assignment:** confirm that Novality Store owns or is licensed to publish every design, text contribution and future image.
4. **AI disclosure:** decide and document the accurate Etsy disclosure after reviewing current policy.

## Photography and PDF production gate

The repository contains Markdown masters and one branded NS 01 confirmation proof, `proofs/NS01_Hamish_the_Highland_Cow_CONFIRMATION_PROOF.pdf`; it does not contain photographed, sale-ready PDFs. The proof is explicitly marked “not for retail” and labels its generated cover artwork as concept imagery. It tests the proposed visual system only and does not satisfy the sample-photography gate. Do not use a generated or borrowed image as evidence that a pattern was physically made.

After sample testing is complete:

- photograph the actual finished sample, all components and critical construction stages;
- include close-ups for NS 01’s nested ears/neck join, NS 04’s three-layer leg joins, NS 08’s spine/neck, NS 09’s 24-to-24 seam/keyring and NS 10’s full 18-stitch head seam;
- identify clearly that the Etsy product is a **digital PDF pattern, not a finished item**;
- state the exact terminology offered: NS 01–NS 10 are US-term patterns; NS 11–NS 15 include side-by-side US/UK instructions;
- state tested skill level, tested materials, measured yarn use, measured finished dimensions and realistic active time;
- generate selectable text rather than page images; embed fonts; create bookmarks; preserve heading hierarchy and reading order; tag tables; add meaningful alt text where supported; and maintain readable contrast and font size;
- preflight both on screen and printed at 100%: no clipped content, split rows, missing repeated table headers, blank pages, tiny tables, orphan headings or hidden text;
- check links, page numbers, revision/version, design code, contact/support route, copyright/licence and accessibility with the final file—not only the Markdown;
- give every downloadable file a final customer-facing filename. Etsy currently permits up to five files per digital listing, at up to 20 MB each, and exposes the uploaded names to buyers: [Etsy digital listing guidance](https://help.etsy.com/hc/en-us/articles/115015628347-How-to-Manage-Your-Digital-Listings).

## Final release checklist

The collection may move from **HOLD** only when all applicable boxes are evidenced:

- [ ] Owner confirms all authorship, assignments, source licences, brand rights and photo rights.
- [ ] Marketplace/trademark review is complete and affected titles are renamed or formally cleared.
- [ ] NS 05’s code/studio attribution and NS 08’s no-belly design intent are signed off.
- [ ] Every core design and every advertised size/option has a completed sample record.
- [ ] Actual yarn use, stuffing, dimensions and active time have replaced unmeasured estimates where needed.
- [ ] Proposed care methods pass complete-sample testing.
- [ ] Structural and intended-use checks pass, including NS 10’s high-risk head seam and NS 15’s entire hanging system.
- [ ] Independent testers complete the frozen release candidate and all findings are closed.
- [ ] A qualified adviser defines applicable product classification, safety, documentation, warning and traceability obligations.
- [ ] Real sample photography and accessible final PDFs are complete and preflighted.
- [ ] Etsy originality, AI disclosure, listing, filename and digital-product requirements are checked against the policy in force on launch day.
- [ ] The final PDFs are compared back to the approved masters and the release audit, spelling, lint, render and file-preflight suites all pass.

Until then, the corrected Markdown is a strong **desk-validated production draft**, not a sale-ready product.
