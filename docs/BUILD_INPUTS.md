# External build inputs

This branch intentionally omits large source-media inputs and generated deliverables. The PDF/Etsy build commands fetch only their required source inputs into an external cache and verify each file's byte size and SHA-256 before using it. Downloads are pinned to the immutable base commit `49d69daeb8d7a2462d5e5bef5394a4ff5d170a3b`; no branch name or moving URL is used.

## Cache behavior

The default cache is:

```text
~/.cache/crochet-pattern-checker/49d69daeb8d7a2462d5e5bef5394a4ff5d170a3b/
```

Set `CROCHET_BUILD_CACHE` to use a different location. Keep it outside the repository so downloaded inputs and regenerated outputs do not reappear as Git changes.

The manifest is `tools/build-inputs-manifest.json`; it records the pinned source commit, expected path, byte length, and SHA-256 for each input. The fetcher refuses to overwrite an existing cache file with a different hash. To repair a corrupt cache entry, remove that one file from the cache and rerun the fetch command.

## Commands

Preview missing files without downloading:

```bash
python tools/fetch_build_inputs.py --group novality --dry-run
python tools/fetch_build_inputs.py --group publish --dry-run
```

Fetch the inputs directly:

```bash
python tools/fetch_build_inputs.py --group novality
python tools/fetch_build_inputs.py --group publish
```

The Novality kit pipeline (`cd novality_kits && python build_all.py`) automatically fetches the `novality` group before building. It writes intermediates and outputs under the external cache. The crochet-checker publishing entry point (`python -m crochet_checker.publish.build`) automatically fetches the `publish` fonts before rendering PDFs.

The `novality` group includes 40 source images and 9 font files. Its derived JPEGs and generated kit outputs are also written to the cache. The `publish` group includes 8 DejaVu font files; the PDF publisher writes generated PDFs to `<cache>/src/crochet_checker/publish/output/` by default. An explicit `--out` can override that destination. The build-input cache is separate from `novality_kits/external-media-manifest.json`, which records already-published output binaries and their mirror URLs.

## Offline use

A clean environment needs network access the first time it builds. After the expected inputs are present in the cache, subsequent runs verify their hashes locally and can build offline. If GitHub is unavailable during first use, the build fails with the input path and download error instead of producing a partial or falsely complete PDF.
