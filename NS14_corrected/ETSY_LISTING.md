# Novality Store — shop assets & listing copy

Design Code NS-14 · Bobble Snowflake Tree Skirt · Corrected Edition

Copy below is written to be **defensible**: every claim maps to a check that was actually run and
whose result is published in Appendix B of the pattern. Claims that could not be substantiated were
rewritten rather than dropped — the substantiated version is usually the stronger sell, because it
names a specific number instead of a vague superlative.

See **Claims that were changed** at the end for what was altered and why.

---

## 1. Shop tagline

> **Novality Store | Mathematically Audited Crochet Patterns**

Alternates, same footing:

- *Novality Store | Every Stitch Count Audited Before Release*
- *Novality Store | 5-Axiom Verified Crochet Patterns*

---

## 2. Shop bio

> Welcome to Novality Store.
>
> We engineer high-precision digital crochet patterns. Every pattern is audited against five stated
> axioms before release — count closure, stated-count parity, repeat and closure divisibility,
> dialect parity, and geometric consistency — and the result of each is published inside the
> pattern, pass or fail.
>
> That last part matters. Our NS-14 tree skirt shipped as a Corrected Edition because the audit
> caught a 4.7% gauge inconsistency that would have made the circle cup. We publish the finding and
> the fix rather than quietly reprinting.
>
> Written in side-by-side US and UK terms, with a machine-checkable round list in every appendix so
> you can verify the stitch mathematics yourself.

---

## 3. Listing bullet points

**100% of stitch counts audited.** All 32 growth rounds, all three size stop-points and all three
border closures reconcile exactly — 0 mismatches. Each round consumes precisely the total the
previous round produced, so nothing is left unworked.

**Published verification record, including what failed.** Appendix B lists all five audit axioms
with their results. Axiom 5 failed on the source edition at 4.7% and is corrected here. You see the
audit, not just a badge.

**Dual terminology, verified line by line.** Side-by-side US and UK columns on every round and the
border, checked to describe the same operations in the same order with identical counts. No
translating on the fly.

**Radial gauge that actually closes.** Round gauge is derived from the increase rate the shape
requires — `12 ÷ 3 ÷ 2π = 0.637 in` of radius per round — so matching both gauge measures produces a
flat circle instead of cupping or ruffling.

**Yarn estimates split by colour.** Calculated per size and split between main and contrast, because
the contrast carries every bobble round, all twelve spokes and the whole border — roughly 45% of the
total. Calculated from stitch counts, not weighed; weigh a sample before buying for production.

**Machine-checkable appendix.** The full 32-round stitch ladder in a form a stitch-count checker
parses directly, so the arithmetic is independently reproducible.

**Three sizes in one file.** Mini / tabletop (R14, 168 sts, 28 scallops), Standard (R23, 276, 46),
Large (R32, 384, 64).

---

## 4. PDF header & footer standard

Applied to `scripts/md_to_pdf.py` as the default, overridable with `--header` / `--footer`:

```
Header:  Novality Store  |  Design Code NS-14  |  Corrected Edition
Footer:  © 2026 Novality Store. All rights reserved. 5-Axiom Mathematically Verified Pattern.
```

```bash
python scripts/md_to_pdf.py pattern.md pattern.pdf \
  --header "Novality Store  |  Design Code NS-15  |  First Edition" \
  --footer "© 2026 Novality Store. All rights reserved. 5-Axiom Mathematically Verified Pattern."
```

### Two renderers, one source file

Both read the same `*_CORRECTED.md`, so the content can never drift between them.

| Script | Output | Use it for |
|:--|:--|:--|
| `scripts/md_to_pdf.py` | `*_CORRECTED.pdf` | Print edition. Low-ink, greyscale-safe. The one to send to a buyer who prints at home. |
| `scripts/novality_pdf.py` | `*_FULLCOLOR.pdf` | Shop edition. The full-colour house layout — this is the file to list. |

The full-colour renderer carries the brand design system and is reusable from NS-15 onward:

```bash
python scripts/novality_pdf.py pattern.md pattern_FULLCOLOR.pdf \
  --title "Pattern Name" --code NS-15 --edition "First Edition" \
  --difficulty "Intermediate" --colourway "Navy + Silver Grey"
```

What it applies automatically:

- **Cover banner** — forest-green card, `N STORE` logo badge, title, imprint line, and tag pills for design code, difficulty and colourway.
- **Section bars** — every `##` becomes a forest bar with a gold end cap and white text.
- **Instruction tables** — green header with gold rule, alternating `#F8F9FA`/white rows, the `Sts` column auto-detected and filled oat so counts pop, and a gold vertical divider between the US and UK columns.
- **Size pills** — `**MINI**`, `**STANDARD**`, `**LARGE**` anywhere in the text render as filled badges.
- **Callouts** — any markdown blockquote becomes a rounded box. A title containing *safety*, *warning* or *disregard* turns amber with ⚠; anything else turns sage with ❖.
- **Code blocks** — grey panel with a forest left bar, used for Appendix A.
- **5-Axiom badge** — on page 1, and as a full end card on the last page.
- **`Page X of Y`** — the page furniture is drawn at save time, so the total is real.

### Palette

| Role | Hex |
|:--|:--|
| Primary — headers, bars, borders | `#1E3A2B` Deep Forest Green |
| Primary light — subheads | `#2E5440` |
| Accent — rules, pills, badge | `#D4AF37` Gold |
| Secondary — stitch-count fill | `#E6D7C3` Oat Cream → `#F3EADF` at text size |
| Info callout | `#E8F0EC` Soft Muted Sage |
| Warning callout | `#FFF8E7` Pale Amber, edge `#E0B84C` |
| Body text | `#1A1A1A` on white |
| Table alternate row | `#F8F9FA` |

---

## 5. The five axioms — reusable boilerplate

Drop this into any listing or pattern front matter:

> **The 5-Axiom Verification System.** An axiom is a property decidable from the written pattern by
> arithmetic alone — not an opinion, and not a physical test.
>
> 1. **Count closure** — each round consumes exactly the total the previous round produced.
> 2. **Stated-count parity** — each printed count equals the count its own operations produce.
> 3. **Repeat & closure divisibility** — repeats divide their round evenly; the final count divides
>    evenly by the border repeat.
> 4. **Dialect parity** — US and UK columns resolve to identical operations and counts.
> 5. **Geometric consistency** — stated gauge agrees with the increase rate the shape requires.
>
> Results are published per pattern, pass or fail. Axioms are written checks only. They do not
> certify safety, fit, finished size, yarn quantity or care behaviour — those require a physical
> sample.

---

## 6. Claims that were changed, and why

| Original wording | Status | Replacement |
|:--|:--|:--|
| "Zero-Defect" / "guaranteeing zero error assembly" | **Removed** | "100% of stitch counts audited" |
| "5-Axiom Verification System" (undefined) | **Defined** | Five named axioms, each mapped to a check, results published |
| "exact join parity" | **Removed** | "dialect parity", which is a check that ran |
| "domain-isolated loop logic" | **Removed** | — |
| "precise yarn estimates" | **Softened** | "calculated from stitch counts, not weighed" |
| "100% verified stitch mathematics" | **Kept** | Accurate — 32/32 rounds, 0 mismatches |

**Why "zero-defect" had to go.** Three independent reasons:

1. **It is contradicted by this very pattern.** The audit found four defects and corrected them. A
   zero-defect claim on a Corrected Edition invites exactly the question you do not want asked.
2. **A written audit cannot support it.** No skirt was crocheted, no gauge swatch measured, no stand
   fitted. Stitch arithmetic being sound does not guarantee error-free assembly by a human with
   different yarn, hook and tension.
3. **It breaches the pattern's own licence.** The Terms of Use permit selling finished items only
   where the listing *"does not claim unverified safety, testing, size, yarn quantity, fit or care
   results."* "Guaranteeing zero error assembly" and "precise yarn estimates" are exactly that. A
   buyer could hold the listing to a standard the file disclaims three pages later.

The replacement copy is narrower but *checkable*, which is the more durable position for a shop
selling precision as the product.

---

## 7. Brand architecture — resolved

**Novality Store** is the business. **Novality Crochet Studio** is its crochet pattern line. This is
a parent-and-imprint structure, the same way a publisher issues books under an imprint, and it is
worth keeping: it lets the crochet patterns carry a craft-specific identity while the spreadsheets
and any future product line sit under the same business.

The rule applied throughout:

| Element | Name used | Why |
|:--|:--|:--|
| Copyright holder | **Novality Store** | One owner across every product line, crochet and non-crochet. A single © holder is what makes the Terms enforceable. |
| Running header | **Novality Store** | Identifies the business on every page. |
| Imprint on the pattern | **Novality Crochet Studio** | This is a crochet product, so it carries the crochet line's name on the cover and sign-off. |
| Credit buyers must give | **"Pattern by Novality Crochet Studio · Design Code NS-14"** | Buyers credit the line they actually bought from. |
| Hashtags | `#NovalityCrochetStudio` · `#NovalityTreeSkirt` | Unchanged — the craft audience follows the craft line. |

The relationship is now stated twice in the pattern so neither name looks like a typo: once as a
colophon under the title, once in the Terms of Use.

> *Novality Crochet Studio is the crochet pattern line of Novality Store.*

The previous conflict — the running footer reading "© 2026 Novality Store" directly above a Terms
section reading "© 2026 Novality Crochet Studio" — is gone. Copyright now reads **Novality Store**
in both places.

**Design code normalised to `NS-14`** (hyphenated) in every file, matching the header standard.

### If you ever register a company

Should Novality Store become a registered entity, the © line should become the registered name —
for example *"© 2026 Novality Store Ltd"* — with the imprint line unchanged. That is a one-line edit
in the markdown and a rebuild.
