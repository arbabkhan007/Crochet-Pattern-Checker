# The store editions

Two PDFs per pattern, thirty-four files in all, written by `docs/kit/build_pdf.py`:

| File | What it is |
|---|---|
| `NSxx_<Title>_Colour_Edition.pdf` | The reading edition: cover artwork, colour, full stop-motion layout. |
| `NSxx_<Title>_Print_Edition.pdf` | Ink-saver edition: white background, no photographs, tick box on every round. |

Rebuild all of them from the corrected masters:

```bash
python3 docs/kit/build_pdf.py              # colour + print, seventeen patterns
python3 docs/kit/build_pdf.py --only print # one edition only
python3 docs/kit/build_pdf.py --check      # verify the 50 mm gauge ruler
```

Page counts in the Grand Collection ledger are read from these files, so rebuild the
volume after changing an edition:

```bash
python3 docs/kit/build_grand.py
```

These files are Novality Store patterns. They are not a checker result.
