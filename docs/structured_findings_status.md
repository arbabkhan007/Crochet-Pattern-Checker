# Structured finding coverage

`ValidationReport.to_dict()` and `verify_pattern().to_dict()` keep the existing human-readable `errors` and `warnings` arrays, add a machine-readable `findings` array, and include `ruleset_id: CPC-RULESET-1`. Each finding record contains `rule_id`, `severity`, `message`, `location`, `source_line`, and `expected`/`actual` counts when known.

Stable IDs currently cover:

- `CPC.STITCH.REPEAT_OVERCONSUMPTION` — a confidently parsed simple repeat consumes more than the preceding verified count.
- `CPC.STITCH.LARGE_INCREASE_REVIEW` — a greater-than-2x stated increase; warning only, not a proof of an error.
- `CPC.STITCH.STATED_COUNT_MISMATCH` — stated versus computed stitches.
- `CPC.SHAPE.LARGE_STEP_REVIEW` — the current 12-to-24 step heuristic; warning only, not proof that a shaping step is wrong.
- `CPC.PARSER.ROW_UNPARSED`, `CPC.PARSER.EMPTY_ROW_BODY`, `CPC.PARSER.REPEAT_SUFFIX_UNPARSED`, and `CPC.PARSER.COVERAGE_AUDIT_FAILED` — coverage/review findings.

Legacy findings that are not yet mapped use `CPC.LEGACY.UNCLASSIFIED`. Do not treat that fallback as a stable rule-specific ID. The `not_checked` list remains alongside the structured findings for compatibility.

A small provisional set under `tests/golden_fixtures/` now pins `CPC-RULESET-1`, source-file hashes, fixture hashes, expected statuses, and exact finding IDs/severity/source locations. The broader `learning_pairs/` and `consensus_lessons/` collections do not yet have this manifest contract. The provisional set is not independently human-reviewed; provenance and review state remain open before calling the full benchmark golden.
