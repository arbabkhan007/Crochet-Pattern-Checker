# On-demand NS01 and release-archive test inputs

The media cleanup remains in effect: the NS01 concept illustrations, generated release PDFs, and ZIP archives are **not restored as tracked checkout files**. The full-suite test flow stores source inputs under an external cache, then points the tests at that cache with `CROCHET_RELEASE_INPUT_CACHE`.

## One-command full test run

From the repository root, run:

```bash
python3 tools/run_tests_with_release_inputs.py tests/ -q --tb=short
```

On the first run it downloads 36 files (about 19.1 MB) from the immutable reviewed source commit and verifies each file's SHA-256 and exact byte size. It builds the two collection ZIPs in the external cache from those pinned PDFs plus the **current checkout's Markdown masters**, verifies ZIP CRCs and byte-identical members, then runs pytest. Later runs re-verify cached inputs without downloading them again.

The test runner does not copy or symlink images, release PDFs, or ZIPs into the Git checkout. The `ns01_pdf_model.py` image paths and the two archive tests use `CROCHET_RELEASE_INPUT_CACHE`; the archive integrity and byte-identity assertions remain active. The image QA still checks actual pixel dimensions/effective DPI and retains its human-review `HOLD` requirements.

## Cache

Default external cache:

```text
~/.cache/crochet-pattern-checker/release-test-inputs/9dbdfab5cf05e68a2136897f9739a0d81cc54114
```

Override it with `CROCHET_RELEASE_INPUT_CACHE`:

```bash
export CROCHET_RELEASE_INPUT_CACHE=/path/outside/the/checkout/cpc-release-inputs
python3 tools/run_tests_with_release_inputs.py tests/ -q --tb=short
```

The fetcher refuses a cache path inside the repository. To inspect what is missing without downloading:

```bash
python3 tools/fetch_release_test_inputs.py --group all --dry-run
```

To fetch only one group:

```bash
python3 tools/fetch_release_test_inputs.py --group ns01-images
python3 tools/fetch_release_test_inputs.py --group release-pdfs
```

The groups are two NS01 concept images (4,755,596 bytes) and 34 release PDFs (14,318,869 bytes). The files are pinned to repository commit `9dbdfab5cf05e68a2136897f9739a0d81cc54114`; no mutable branch or tag is used.

## Prepare only / run the image QA

To populate the external cache and generate both collection ZIPs without running tests:

```bash
python3 tools/run_tests_with_release_inputs.py --prepare-only
```

To run the image QA against the cached source illustrations:

```bash
export CROCHET_RELEASE_INPUT_CACHE="$HOME/.cache/crochet-pattern-checker/release-test-inputs/9dbdfab5cf05e68a2136897f9739a0d81cc54114"
python3 tools/ns01_pdf_asset_qa.py
```

The report should continue to show concept artwork below the 300-DPI target and a human-review `HOLD`; this workflow supplies genuine pinned inputs, not fabricated images or a waived review.

## CI

The `Tests` GitHub Actions workflow invokes the same explicit runner instead of plain pytest. Release PDFs are fetched into the runner's external home cache, ZIPs are created from the checked-out pattern masters, and the test process receives the cache path. No generated assets are staged or committed.
