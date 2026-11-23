# Provisional golden findings

`manifest.json` locks four small checker outputs, the exact fixture text hashes, the public `CPC-RULESET-1` identifier, and SHA-256 hashes of the parser/validation source files that determine these outputs. `tests/test_golden_fixtures.py` fails when a finding is missing, an unexpected finding appears, a source location changes, or a fixture/ruleset source hash drifts.

The set is deliberately small and **provisional**. The literal stitch arithmetic and expected review severity were checked, but independent human craft review and broader real-pattern review are still pending. The 12-to-24 fixture is a warning example, not an assertion that its shaping is wrong. None of these cases certifies fit or target shape.

To update intentionally:

1. Review the rule and fixture change; do not update hashes just to silence a failure.
2. Re-run the golden test and inspect the complete finding records.
3. Update expected findings and the matching fixture/source SHA-256 values in `manifest.json`.
4. Keep `ruleset_id` stable for compatible rule changes only when reviewers approve; otherwise bump `RULESET_ID` and the manifest together.
5. Leave `review_status` provisional until a human reviewer records approval and provenance.
