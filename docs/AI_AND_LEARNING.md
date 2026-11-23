# AI and Safe Learning

## Validation authority

The deterministic compiler is authoritative for:

- Stitch counts
- Repeat expansion
- Round boundaries
- Turning chains
- Multi-piece state
- Assembly checks

The standard CLI and deterministic API checks do not call hosted models. The separate `/consensus` workflow can call hosted providers only when their IDs, model names, and credentials are explicitly configured and a user submits a pattern. It reports actual participation and failures; the deterministic compiler remains authoritative for the rules it checks.

## AI modes

- `offline`: compiler only
- `cloud`: the legacy `AIQualityChecker` path remains a no-call placeholder
- `consensus`: the legacy `AIQualityChecker` path is not the hosted multi-provider orchestrator
- `rule_based`: deterministic wording only

The optional `ConsensusRunner` assigns specialist roles, runs selected providers concurrently for independent reviews, then cross-examines and adversarially reviews findings. No providers are selected by default. Its structured report does not turn model agreement into deterministic proof or physical verification.

## Safe learning

The learning store records:

- Pattern hash
- Compiler result
- Errors and warnings
- Optional corrected pattern
- User confirmation

The validator never changes itself automatically.

A case becomes a trusted regression case only after:

1. A human reviews the compiler result.
2. The correction is confirmed.
3. The case is exported to `tests/regression`.

## Privacy

Do not commit:

- API keys
- `.env` files
- `.crochet_learning`
- `.crochet_cache`
- `.crochet_consensus/history.sqlite3`
- Private customer patterns
