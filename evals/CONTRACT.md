# Evaluation contract

## 1. Scope and threat model

The target is the Solver's ability to identify well-grounded defects in frozen crochet-pattern text. Verifier quality is diagnostic; it does not repair or inflate the primary Solver score. The benchmark does not certify a pattern as craft-correct or a model as generally reliable.

The rubric, expected recomputations, private notes, and holdout results are answer-bearing. Solver and Verifier must never receive them. The orchestrator may compute a rubric hash, but must not put the rubric or its contents in either model context. Tuner receives only development-set aggregates, never holdout data, item IDs, defect locations, expected values, or raw responses.

## 2. Fixture curation and immutability

- A human curator freezes source files, their SHA-256, the exact canonical text delivered to models, and the canonicalizer/version. Store both source and canonical-text hashes privately.
- Pin page/line/round anchors and a source-derived proof for every rubric item. Independently review the expected interpretation, especially any claimed implication between rounds. Do not assume a later count alone disproves an earlier one unless the written operations establish that implication.
- Use opaque IDs. Do not include issue names, answers, or rubric categories in filenames or IDs visible to Solver/Verifier.
- Split fixtures before tuning into `development` and sealed `holdout`. Tuning, prompt selection, model selection, and feedback use development fixtures only. A holdout result used to choose a change consumes that holdout; create a new version for a later final test.
- Two fixtures are a smoke-test/pilot set, not enough evidence for broad claims. Prefer multiple independent patterns and pattern families, with hidden holdout families not used in development.
- Never silently edit a fixture or rubric. Version it, re-hash it, and retain prior versions for comparability.

## 3. Run identity and API controls

For every response, record privately: campaign/batch/fixture/replicate IDs; source and canonical-input hashes; prompt and client-profile hashes; provider label; requested and returned model identifiers; pinned route/profile; timestamp; temperature, top-p, output-token cap, seed and whether the endpoint honors seeds; request ID; usage; finish reason; JSON/schema validation result; and any transport retry. Do not record API secrets.

Use temperature 0 for baseline and final runs. A seed is useful only if the endpoint documents and honors it; temperature 0 does not guarantee bit-identical outputs across provider revisions or runs. If the returned model differs from the pinned model, mark the call invalid and do not score it. Check the provider's content-retention policy before sending any pattern.

Set an output-token cap based on measured canonical input and required response size. `max_tokens >= 4000` is not a universal guarantee. Treat `finish_reason=length`, refusal, empty content, or schema-invalid JSON as a format/run failure—not a partial success. Prefer provider-enforced JSON Schema output when supported. For a Solver format failure, create a zero-score private record with `python3 evals/score.py --rubric <private-rubric.json> --format-failure`; do not pass a partial response to the adjudicator.

### Retry policy

- A transient transport error may be retried once with the exact same request, settings, and seed, and must be logged.
- Do not send answer-changing “format reminders.” If structured output is unavailable and the first model response is invalid/truncated, record that replicate as a format failure and score it 0 for the Solver. Do not silently drop it or select a later response. A separate diagnostic retry may be logged but cannot replace the primary response.
- Distinguish provider/transport failure from model refusal or malformed output. Only the former may use the fixed transport retry. If both transport attempts fail before a model response exists, mark the scheduled call/batch incomplete and do not create a zero-scored model response; complete it only under a documented technical recovery with the same frozen request. A provider failure is not a Solver format failure and cannot support a final PASS.

## 4. Phases

### Phase 0 — Freeze

Freeze fixtures, splits, rubric version, prompts, settings, model/profile, parser/canonicalizer, replicate IDs, thresholds, and retry policy. Hash all inputs. Verify endpoint reachability and actual model identity without exposing private material.

### Phase 1 — Baseline on development

For each development fixture and each predeclared replicate, call Solver at temperature 0 with the same pinned profile and exact prompt. Store raw response and metadata privately. Never choose the best seed.

### Phase 2 — Independent verification

Give Verifier the original canonical pattern and Solver JSON only. Prefer a different model family; if unavailable, record that limitation. Verifier independently recomputes every claim and performs a separate sweep. It does not see the rubric. Keep additions separate from the Solver report.

### Phase 3 — Adjudication and scoring

The Grader proposes a mapping of each Solver claim to one private rubric item (or no item), with evidence and an adjudication. A human checks the mapping. Set `human_approved=true` only after review. `score.py` then computes arithmetic deterministically. Verifier-only additions are reported separately and receive no points in the Solver's primary score. A separate, explicitly named end-to-end pipeline metric may be added later, but must not be confused with Solver score.

### Phase 4 — Tuning on development only

Each iteration changes exactly one lever: generic Solver protocol addition; defined two-pass mode; temperature only if the campaign's final-temperature rule permits it; pinned model/profile; or output-token cap. A two-pass mode means: pass 1 produces a draft; pass 2 receives only the same pattern and that draft, without Verifier output, rubric, or keys; pass 2 is the scored response. Record both calls and the total token budget.

Compare candidate and current-best configurations on the same predeclared development fixture/replicate matrix. Accept a change only if the macro-average improves by at least the predeclared margin (default 1 point) and no development fixture drops more than 5 points. This iteration rule applies even while the score is below the final pass threshold. Otherwise revert. Tuner receives aggregate category counts and score deltas only; do not provide fixture-specific claims or answer-bearing feedback.

### Phase 5 — Final sealed regression gate

After tuning ends, freeze the chosen configuration. Run three complete holdout batches without examining results between batches. Each batch must contain every holdout fixture at every predeclared replicate. The final PASS gate is:

- equal-weight macro-average across fixture means is at least 92/100;
- no fixture mean is below 85/100; and
- there are zero rubric-adjudicated refuted Solver claims in each of the three final batches.

If any holdout result is used to tune, select, or rewrite a prompt, the holdout is consumed and cannot support a final PASS for that configuration. Keep all three batch results, including failures. If the endpoint cannot provide meaningful independent replicates, state that the repeated batches are stability checks, not independent statistical evidence.

### Phase 6 — Report

Publish only a redacted report: campaign/version, pinned model/profile and settings, prompt hashes, aggregate scores and deltas, fixture-level pseudonyms if safe, failure-taxonomy counts, invalid-response counts, and PASS/FAIL/INCOMPLETE. Do not expose patterns, rubric items, expected counts, claim-level adjudications, API request payloads, or private paths.

## 5. Scoring contract

The hidden rubric has four categories whose item maxima sum to the configured category weights, default math 40, coherence 35, finishing 15, and absurdity 10. The 10-point anchor, if independently proven by the source text, is included inside math's 40 points—not added on top. If it is not logically forced by the text, remove or rewrite it.

For each response, the adjudicator maps each Solver defect ID to at most one rubric item, or to `null` for a non-rubric claim. A rubric item cannot be credited twice. `full` awards the item's full points; `partial` awards a named, rubric-defined partial value; `refuted` awards zero and counts toward the false-positive penalty; `unverifiable` awards zero and is reported for human review. Missing rubric items receive zero. Duplicate claims must be adjudicated as duplicates/refuted or left unmapped; they must never earn double credit.

```text
raw_points = sum(item points awarded)
penalty = min(per_refuted_claim × refuted_claim_count, configured_penalty_cap)
score = clamp(raw_points - penalty, 0, 100)
```

The private rubric must define exact acceptable variants, evidence needed, partial-credit keys, and a method for ambiguous/underivable cases. “Underivable, because …” can earn full credit only where the rubric explicitly permits it. Matching by location and type alone is insufficient. The adjudicator's proposed mappings are not treated as ground truth until a human approves them.

For an aggregate, compute each fixture's arithmetic mean across all predeclared replicates and batches, then average fixture means equally. Do not weight by response count, choose best-of-N, or omit failed model responses. Each invalid Solver response is a zero for that replicate; transport failures are handled only under the fixed retry policy.

`aggregate.py` consumes a private JSON object with `split`, `fixtures`, `replicates_per_fixture`, and `batches`. Each batch has an `id` and exactly one run for every fixture × replicate pair; each run contains `fixture`, `replicate`, `score` (0–100), `refuted_count`, and `failure_taxonomy`. The taxonomy counts undercredited expected items by math/coherence/finishing/absurdity; `format` is 1 for an invalid Solver response and 0 otherwise. A format-failure run must score 0 and has no adjudicated refuted claims. False positives are counted separately in `refuted_count`. Validate input against `schemas/aggregate-input.schema.json`. Development input returns `DEVELOPMENT_SCORED`; holdout with fewer than three complete batches returns `INCOMPLETE`; a completed final gate returns `PASS` or `FAIL`. For development tuning, pass the current best development summary with `--baseline`; it accepts only the configured macro gain and per-fixture regression rule. Aggregator input and output are private because they contain fixture IDs and scores.

## 6. Conflicts resolved from the draft workflow

- The tuning acceptance gate is separate from the final `>=92` gate, so incremental improvements can be accepted.
- Solver-only score is primary; Verifier additions are diagnostic, not borrowed Solver recall.
- Final holdout is not replayed after every tuning change. Development fixtures serve regression; holdout is sealed until configuration freeze.
- “Three runs” means three complete fixture-by-replicate batches, not three individual calls.
- “Deterministic grader” means deterministic score calculation after human-approved adjudication, not an LLM at temperature 0.
- If final temperature 0 is mandatory, a nonzero-temperature proposal is disabled unless the campaign acceptance policy is formally changed before evaluation.
