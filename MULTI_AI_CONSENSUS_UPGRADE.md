# Multi-AI Consensus Upgrade

This ZIP is a source-file overlay for the `multi-ai-consensus` checkout based on commit `3922dab`. Extract it at the repository root. It adds an optional, server-side multi-provider written-pattern review while keeping the existing parser and deterministic validator in place.

## Files in this upgrade

- `src/crochet_checker/ai_providers/settings.py` — bounded review, participation, and draft policy.
- `src/crochet_checker/ai_providers/provider_adapters.py` — explicit provider catalog, native API-family adapters, retries, timeouts, safe error handling, and telemetry.
- `src/crochet_checker/ai_providers/review.py` — structured response validation, source-evidence grounding, and prompt construction.
- `src/crochet_checker/ai_providers/orchestrator.py` — deterministic validation plus independent, anonymized cross-examination, adversarial review, evidence aggregation, and fail-closed gate.
- `src/crochet_checker/ai_providers/history.py` — SQLite run, report, progress, and revision history.
- `src/crochet_checker/ai_providers/service.py` — run lifecycle and separate, reasoned, revalidated draft revisions.
- `src/crochet_checker/ai_providers/__init__.py` — package exports.
- `src/crochet_checker/web/app.py` and `src/crochet_checker/web/consensus_dashboard.py` — JSON API and inline, dependency-free dashboard at `/consensus`.
- `tests/ai_providers/test_*_upgrade.py` and `tests/web/test_consensus_api_upgrade.py` — isolated mocked adapter, orchestration, persistence, API, and policy tests.

Two existing files are replacements/merges and should be reviewed before overwriting local edits: `src/crochet_checker/ai_providers/__init__.py` and `src/crochet_checker/web/app.py`. All other listed implementation/test paths are new on the stated base commit. No core checker, parser, standards, examples, workflows, or existing tests are removed.

## Configure providers explicitly

No provider is selected by default. Set `CROCHET_CONSENSUS_PROVIDERS` to a comma-separated list of provider IDs, and set an explicit model ID and credential for each selected provider. No model ID or live availability is guessed.

| Provider ID | Model environment variable | Credential environment variable | Default API base |
|---|---|---|---|
| `openai` | `OPENAI_MODEL` | `OPENAI_API_KEY` | `OPENAI_BASE_URL` (optional; default `https://api.openai.com/v1`) |
| `anthropic` | `ANTHROPIC_MODEL` | `ANTHROPIC_API_KEY` | `ANTHROPIC_BASE_URL` (optional; default `https://api.anthropic.com`) |
| `google` | `GOOGLE_MODEL` or `GEMINI_MODEL` | `GOOGLE_API_KEY` or `GEMINI_API_KEY` | `GOOGLE_BASE_URL` (optional; default `https://generativelanguage.googleapis.com/v1beta`) |
| `xai` | `XAI_MODEL` | `XAI_API_KEY` | `XAI_BASE_URL` (optional; default `https://api.x.ai/v1`) |
| `deepseek` | `DEEPSEEK_MODEL` | `DEEPSEEK_API_KEY` | `DEEPSEEK_BASE_URL` (optional; default `https://api.deepseek.com`) |
| `mistral` | `MISTRAL_MODEL` | `MISTRAL_API_KEY` | `MISTRAL_BASE_URL` (optional; default `https://api.mistral.ai/v1`) |
| `meta_llama` | `LLAMA_MODEL` | `LLAMA_API_KEY` (optional for an unauthenticated trusted endpoint) | Must set `LLAMA_BASE_URL` |
| `qwen` | `QWEN_MODEL` | `QWEN_API_KEY` (optional for an unauthenticated trusted endpoint) | Must set `QWEN_BASE_URL` |
| `openai_compatible` | `CROCHET_COMPAT_MODEL` | `CROCHET_COMPAT_API_KEY` (optional) | Must set `CROCHET_COMPAT_BASE_URL` |

The `meta_llama`, `qwen`, and generic-compatible IDs use the OpenAI-compatible chat-completions wire format at the caller-supplied endpoint; they are not separate vendor-specific protocol implementations. API models, permissions, pricing, quotas, and account availability change over time. The dashboard's `ready` flag means only that local configuration values exist; the application deliberately does not probe a provider until a review is submitted.

Provider API references for checking current endpoint/model details:

- [OpenAI API reference](https://platform.openai.com/docs/api-reference/chat/create)
- [Anthropic Messages API](https://docs.anthropic.com/en/api/messages)
- [Google Gemini REST quickstart](https://ai.google.dev/gemini-api/docs/quickstart)
- [xAI chat completions](https://docs.x.ai/developers/model-capabilities/legacy/chat-completions)
- [DeepSeek API quickstart](https://api-docs.deepseek.com/)
- [Mistral migration and compatibility notes](https://docs.mistral.ai/resources/migration-guides)

Set secrets through the server's environment or secret manager. Do not put credentials in a frontend bundle, report, database, committed `.env` file, test fixture intended for production, or log. Pattern text is sent to each selected provider when a run starts, so only send text whose disclosure to those providers is acceptable.

### Example configuration (no credentials included)

```text
CROCHET_CONSENSUS_PROVIDERS=openai,anthropic
CROCHET_REQUIRED_PROVIDERS=openai,anthropic
OPENAI_MODEL=<explicit-model-id-from-your-account>
ANTHROPIC_MODEL=<explicit-model-id-from-your-account>
```

Credential values are intentionally not shown. A keyless or unselected provider is not represented as having been consulted. A failed call remains a failed call in the report. A configured fallback runs when the primary provider's independent review fails. If it succeeds through all required phases, the fallback is named as the participant that fulfilled the required slot; the failed primary remains visible as failed. A later cross-examination or adversarial failure is not silently replaced and keeps the gate closed.

Optional settings:

- `CROCHET_CONSENSUS_MIN_MODELS` (default `2`) and `CROCHET_CONSENSUS_MIN_PARTICIPATION_RATIO` (default `1.0`) set participation targets.
- `CROCHET_CONSENSUS_THRESHOLD` (default `0.67`) sets the grounded independent-agreement threshold. Model confidence is not a vote weight.
- `CROCHET_FALLBACK_MAP` uses explicit pairs such as `openai=deepseek` (comma-separate multiple pairs); configure each fallback's model, endpoint, and credential too.
- `CROCHET_PROVIDER_TIMEOUT_SECONDS` (default `45`), `CROCHET_PROVIDER_MAX_RETRIES` (default `2`), `CROCHET_PROVIDER_MAX_TOKENS` (default `1800`), and `CROCHET_CONSENSUS_MAX_CONCURRENCY` (default `8`) bound calls.
- `CROCHET_PROVIDER_TEMPERATURE` is omitted from provider requests unless explicitly configured, avoiding an assumed model-specific setting.
- `<PREFIX>_INPUT_COST_PER_1M` and `<PREFIX>_OUTPUT_COST_PER_1M` allow estimates only when the user supplies current rates; prefixes are `OPENAI`, `ANTHROPIC`, `GOOGLE`, `XAI`, `DEEPSEEK`, `MISTRAL`, `LLAMA`, `QWEN`, or `CROCHET_COMPAT`. Unknown rates stay unknown.
- `CROCHET_ROLE_<PROVIDER_ID>` may assign a configured reviewer role. `CROCHET_REQUIRED_REVIEW_ROLES` may add roles, but the required `stitch_arithmetic` and `construction_assembly` roles cannot be removed.
- `CROCHET_CONSENSUS_CROSS_EXAMINATION=false` or `CROCHET_CONSENSUS_ADVERSARIAL_REVIEW=false` can be used to suppress those calls, but a run cannot be approved if either required review phase is disabled.
- Strict participation is a hard safety gate and cannot be disabled. A false `CROCHET_CONSENSUS_STRICT_PARTICIPATION` setting is rejected.
- `CROCHET_CONSENSUS_MAX_REVISIONS` (default `3`, maximum `10`) limits child-draft depth.
- `CROCHET_CONSENSUS_DATABASE` sets the SQLite file path. The default is `.crochet_consensus/history.sqlite3` relative to the server working directory. History stores submitted pattern text and reports; protect it accordingly.

## Run the API and dashboard

Start the existing FastAPI application from the repository checkout using the deployment's Python environment. For a local background run from an open `+` terminal:

```text
nohup uvicorn crochet_checker.web.app:app --host 0.0.0.0 --port 8000 </dev/null >/tmp/crochet-consensus.log 2>&1 &
```

Open `http://127.0.0.1:8000/consensus` locally. Do not expose the service publicly without adding suitable authentication, network restrictions, and a privacy review: these endpoints return locally stored pattern reports.

### API routes

- `GET /api/consensus/providers` — local configuration readiness and safe settings only; never returns keys and does not probe live availability.
- `POST /api/consensus/runs` — queues a run and returns a run ID (`202`).
- `GET /api/consensus/runs/{run_id}` — detailed report or current progress/failure.
- `GET /api/consensus/runs?limit=50` — recent history summary.
- `POST /api/consensus/runs/{run_id}/drafts` — creates a separate child run from exact, single-match replacements with a required reason; queues full validation again.
- `POST /api/consensus/check` — runs a full review synchronously and returns the report.

The existing `POST /api/check` remains the deterministic checker only. The legacy `AIConsensusChecker` helper is not retroactively made a hosted client; hosted calls and their reports are only performed by the new `/api/consensus/...` service after explicit provider configuration and a run request.

## Approval and interpretation

The existing deterministic text checker remains authoritative for arithmetic it checks; model opinions cannot override it. Each model call must return structured JSON with source-grounded review coverage. Findings and peer assessments must cite text present in the submitted pattern. One independent finding contribution per provider forms an issue cluster; reviewer counts and confidence scores do not establish truth.

A run returns `NOT APPROVED – HUMAN REVIEW REQUIRED` if deterministic validation fails, required providers/roles/participants or review phases are missing, source evidence is ungrounded, a review leaves questions/disagreements, an actionable finding remains, or a written construction step is not parsed/verified. A successful gate is labelled `APPROVED FOR WRITTEN-TEXT CHECKS ONLY`; it is not a claim of physical construction, gauge, fit, safety, durability, commercial readiness, or zero false positives. The gap scanner reports known unparsed/unverified items; an empty list means no known gap was flagged, not proof every written instruction was interpreted. The report leaves `written_steps_all_parsed` unknown.

Corrections appear as proposals only. Creating a draft requires an explicit, exact source excerpt, replacement text, and justification; the original run and text stay unchanged. The child draft is run through deterministic checks and every configured review phase again.

## Tests

The added tests use injected fake adapters and `httpx.MockTransport`. They do not call hosted AI APIs, do not require credentials, and must not be described as live-provider validation. From the repository root:

```text
python -m pytest -q
ruff check src/crochet_checker/ai_providers src/crochet_checker/web/app.py src/crochet_checker/web/consensus_dashboard.py tests/ai_providers tests/web/test_consensus_api_upgrade.py
```

A real provider call has not been verified as part of this ZIP build. Live use requires the operator to configure current model IDs, credentials, provider terms, and any required consent/privacy controls.
