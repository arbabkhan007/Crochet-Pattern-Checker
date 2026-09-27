#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
export PYTHONPATH="$PWD/src"

exec python -m uvicorn \
  crochet_checker.enterprise.api:app \
  --host 0.0.0.0 \
  --port "${PORT:-8000}"
