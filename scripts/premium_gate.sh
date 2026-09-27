#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
export PYTHONPATH="$PWD/src"

echo "[1/8] Compile source"
python -m compileall -q src

echo "[2/8] Check whitespace"
git diff --check

echo "[3/8] Public API imports"
python - <<'PY'
from crochet_checker.parser import parse_pattern
from crochet_checker.validation import validate_pattern
from crochet_checker.pdf import generate_pdf_html
from crochet_checker.visualization import render_2d_preview
from crochet_checker.ai_providers.quality import AIQualityChecker
from crochet_checker.learning import LearningStore

print("Public APIs: PASS")
PY

echo "[4/8] AI quality layer"
python scripts/test_ai_quality.py

echo "[5/8] Architecture tests"
python test_audit_features.py

echo "[6/8] Feature tests"
python test_all_features.py

echo "[7/8] Pytest"
python -m coverage erase

python -m coverage run -m pytest -q

python -m coverage run --append test_audit_features.py
python -m coverage run --append test_new_features.py
python -m coverage run --append test_all_features.py

for file in \
  scripts/test_ai_quality.py \
  scripts/test_enterprise_certification.py \
  scripts/test_enterprise_simulation.py \
  scripts/test_enterprise_audit.py \
  scripts/test_yarn_substitution.py \
  scripts/test_gauge_calibration.py \
  scripts/test_gauge_image.py \
  scripts/test_enterprise_report.py
do
  if [ -f "$file" ]; then
    python -m coverage run --append "$file"
  fi
done

python -m coverage report \
  --show-missing \
  --fail-under=60

python -m coverage html -d test-results/htmlcov

echo "[8/8] Focused correctness lint"
ruff check src tests \
  --select F821,F601,PIE794 \
  --statistics

echo ""
echo "========================================"
echo "PREMIUM QUALITY GATE PASSED"
echo "========================================"
