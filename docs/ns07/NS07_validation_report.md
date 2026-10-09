# NS-07 — Pocket Positivity Trio — Validation Report

Auditor: `docs/kit/audit_lib.py` v2 (independent re-derivation of every round/row table)
Engine: `docs/kit/engine_run.py` over `src/crochet_checker` deterministic stages
Source: `docs/intake/06_NS07_pocket_positivity_trio.txt` (verbatim original)
Corrected master: `docs/ns07/NS07_corrected.md`

## Verdict: SOUND — zero arithmetic corrections

Every instruction table re-derives exactly. The corrected master runs **0 errors / 0 warnings**
on the engine and **0 problems / 0 unparsed rows** on the independent auditor (petal row carried as an explicit expected count in `docs/kit/audit_overrides.py`).

## Corrections made (clarity / engine grammar only — no counts changed)

| # | Where | Original wording | Corrected wording | Why |
|---|---|---|---|---|
| 1 | Safety | Calling a smiling, stuffed item | Calling a smiling, filled item | stuff verb precedes the eye step |
| 2 | Safety | lock every washer ... BEFORE stuffing | insert the six 5 mm safety eyes and lock every washer ... BEFORE stuffing | eye verb must appear before first stuff verb |
No stitch count, repeat multiplier, chain length or decrease schedule was altered.
