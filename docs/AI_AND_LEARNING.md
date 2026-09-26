# AI and Safe Learning

## Validation authority

The deterministic compiler is authoritative for:

- Stitch counts
- Repeat expansion
- Round boundaries
- Turning chains
- Multi-piece state
- Assembly checks

ChatGPT and Gemini are advisory providers only.

## AI modes

- `offline`: compiler only
- `cloud`: configured provider responses
- `consensus`: compare ChatGPT and Gemini
- `rule_based`: deterministic fallback

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
- Private customer patterns
