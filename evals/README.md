# Nightmare Pattern Verifier evaluation kit

This directory contains **public, non-secret evaluation machinery**: role prompts, JSON schemas, a deterministic arithmetic scorer, and a batch aggregator. It contains no real crochet-pattern fixtures, answer keys, rubrics, API credentials, raw model responses, or live API client.

The evaluation measures a model's defect-finding performance on a versioned adversarial crochet-pattern set. It is a narrow proxy for reasoning and instruction-following—not a general LLM benchmark, independent craft certification, or replacement for the repository's unit, consensus, archive-integrity, NS01 image-QA, or byte-identity checks.

## Security boundary

Keep source fixtures, canonicalized inputs, the item-level rubric, adjudications, raw responses, and per-fixture scores in a private directory **outside this repository**. This repository is public; putting the sealed rubric or holdout fixtures here would expose the answers and contaminate the benchmark. Commit only non-sensitive schemas and hashes for public inputs; keep holdout/rubric hashes in private manifests unless their disclosure has been reviewed. Never put API keys in prompts, manifests, shell history, logs, or reports. Before sending a fixture to a hosted endpoint, confirm that its content may be processed by that provider.

A suitable private layout is:

```text
$NIGHTMARE_EVAL_PRIVATE_ROOT/
  fixtures/development/<opaque-id>/source.*
  fixtures/holdout/<opaque-id>/source.*
  rubrics/<opaque-id>.json
  runs/<campaign>/<batch>/<opaque-id>/<replicate>/
```

Use opaque fixture IDs; don't encode a defect, expected answer, or pattern name in an ID exposed to Solver or Verifier. Keep the private root out of Git and redact fixture-level data from any PR/chat report.

## Roles

- **Fixture Curator (human, one-time per version):** freeze lawful source files, canonicalization procedure, source/evidence anchors, item-level rubric, and development/holdout split. Independently review every expected defect. Never edit a fixture in place; issue a new version and retain the old hash.
- **Orchestrator:** follow `CONTRACT.md` and pass only each role's permitted inputs. It may record hashes through the harness but must not send rubric content or keys to Solver/Verifier.
- **Solver:** sees one canonical pattern and `prompts/solver.md` only.
- **Verifier:** sees that pattern and the Solver response, never the rubric.
- **Grader/Adjudicator:** may see the private rubric and all evidence; proposes item mappings. A human reviews its adjudication before scoring.
- **Scorer and Regression Agent:** `score.py` and `aggregate.py` are deterministic local tools, not LLM agents. The numerical score is computed from the approved adjudication and private rubric.
- **Tuner:** sees only development-set aggregate metrics and a sanitized failure taxonomy. It never sees holdout results, expected answers, rubric item IDs, or raw pattern text.

## Use

1. Read `CONTRACT.md`; prepare fixtures, canonical inputs, and rubrics privately. Do not run a benchmark until the holdout is genuinely separated from tuning.
2. Pin the model/profile and freeze the exact system prompts and settings. Verify that the API's returned model matches the requested model. Record the prompt, fixture, and canonical-input hashes in a private run manifest conforming to `schemas/run-manifest.schema.json`.
3. Capture each raw response privately and validate it against its role schema. Reject truncation and invalid JSON; don't repair answer content with repeated reminders. Install the optional validator dependency with `python3 -m pip install -r evals/requirements.txt`, then run, for example:

   ```bash
   python3 evals/validate.py --schema evals/schemas/solver.schema.json --input "$NIGHTMARE_EVAL_PRIVATE_ROOT/runs/<run>/solver.json"
   ```

   See the retry policy in `CONTRACT.md`. For a refusal, truncation, or schema-invalid response, create its zero-score record without grading a partial answer:

   ```bash
   python3 evals/score.py --rubric "$NIGHTMARE_EVAL_PRIVATE_ROOT/rubrics/<opaque-id>.json" --format-failure
   ```

4. Have an adjudicator produce a JSON instance conforming to `schemas/adjudication.schema.json`, with `human_approved` set to `false`. A human must review it and explicitly approve it before scoring. The grader prompt is in `prompts/grader.md`; validate the approved instance before scoring.
5. Score one Solver response with:

   ```bash
   python3 evals/score.py \
     --rubric "$NIGHTMARE_EVAL_PRIVATE_ROOT/rubrics/<opaque-id>.json" \
     --solver "$NIGHTMARE_EVAL_PRIVATE_ROOT/runs/<run>/solver.json" \
     --adjudication "$NIGHTMARE_EVAL_PRIVATE_ROOT/runs/<run>/adjudication.json"
   ```

   The output includes rubric item IDs and is private. Do not paste it publicly.
6. Aggregate complete, predeclared batches with `aggregate.py` according to `CONTRACT.md`. Validate the private input against `schemas/aggregate-input.schema.json` first. For development tuning, compare a candidate input with the current best summary using `--baseline`. Only development results may inform tuning. Run the sealed holdout after the configuration is frozen. Aggregator outputs contain fixture IDs and scores; keep them private.

   ```bash
   python3 evals/validate.py --schema evals/schemas/aggregate-input.schema.json --input "$NIGHTMARE_EVAL_PRIVATE_ROOT/aggregate-input.json"
   python3 evals/aggregate.py "$NIGHTMARE_EVAL_PRIVATE_ROOT/aggregate-input.json"
   python3 evals/aggregate.py "$NIGHTMARE_EVAL_PRIVATE_ROOT/candidate-input.json" --baseline "$NIGHTMARE_EVAL_PRIVATE_ROOT/best-development-summary.json"
   ```

There is deliberately no network client or example answer key here. Supply a provider adapter in your controlled environment, using a secret manager or environment injection; verify privacy, routing, schema mode, finish reason, token usage, and actual served model before treating a run as valid.

## Local checks

```bash
python3 -m pip install -r evals/requirements.txt
python3 -m unittest discover -s evals/tests -v
for schema in evals/schemas/*.json; do python3 -m json.tool "$schema" >/dev/null; done
```
