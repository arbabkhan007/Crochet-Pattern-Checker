# Consensus lessons

These are the only benchmark repairs both corrected files agree on and this checker can prove.

Each folder has:

- `wrong.txt` must not pass cleanly.
- `corrected.txt` must pass with no errors and no warnings.
- `lesson.txt` says how the defect works and what the consensus repair is.

Write them in the checker's dialect. Use `(sc, inc) x 6`, not `[sc 1, inc] 6 times`.

Do not add a lesson for a disagreement. Wyvern 24 versus 30, a 35-stitch fan versus a 42-stitch fan, and a rebuilt 64-stitch hub stay in the viewpoint files.

Run:

```bash
PYTHONPATH=src python3 scripts/check_consensus.py
```

`CONSENSUS_OK` means every lesson proved, and `docs/consensus.md` was rewritten from that run.
