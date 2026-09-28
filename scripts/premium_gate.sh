#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
export PYTHONPATH="$PWD/src"

echo "[1/4] Compile checker"
python -m compileall -q src/crochet_checker/parser src/crochet_checker/validation src/crochet_checker/verification src/crochet_checker/cli.py

echo "[2/4] Whitespace"
git diff --check

echo "[3/4] Checker tests and consensus"
python -m pytest -q tests/test_contract.py tests/test_stages.py tests/test_verdict.py tests/test_span.py tests/validation
python scripts/check_consensus.py

echo "[4/4] Undefined names in the checker"
python -m ruff check src/crochet_checker/parser src/crochet_checker/validation src/crochet_checker/verification src/crochet_checker/cli.py tests/test_contract.py tests/test_stages.py tests/test_verdict.py tests/test_span.py --select F821,F601 --statistics

echo "PREMIUM QUALITY GATE PASSED"
