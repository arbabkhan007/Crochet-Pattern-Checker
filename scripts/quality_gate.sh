#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

export PYTHONPATH="$ROOT/src"

echo "========================================"
echo " CROCHET PATTERN CHECKER QUALITY GATE"
echo "========================================"

echo "[1/7] Compile source"
python -m compileall -q src

echo "[2/7] Import public APIs"
python - <<'PY'
from crochet_checker.parser import (
    CrochetParser,
    parse_pattern,
    MarkdownFrontmatterSanitizer,
    GlossaryPrePassExtractor,
    MultiPieceASTBuilder,
    RecursiveLoopUnroller,
)
from crochet_checker.engine import (
    CanvasQueue,
    GlobalAnchorGraph,
    StitchConsumer,
    PostVsHeadLoopTracker,
)
from crochet_checker.validation import (
    validate_pattern,
    PatternValidator,
    ValidationReport,
)
from crochet_checker.pdf import (
    PDFConfig,
    PDFGenerator,
    generate_pdf,
    generate_pdf_html,
)
from crochet_checker.visualization import (
    generate_circle_diagram,
    generate_stitch_count_chart,
    generate_crochet_chart,
    render_2d_preview,
    measure_pattern,
)

print("Public API imports passed")
PY

echo "[3/7] Parse and validate smoke pattern"
python - <<'PY'
from crochet_checker.parser.parser import parse_pattern
from crochet_checker.validation import validate_pattern

text = """\
Round 1: 6 sc into magic ring (6)
Round 2: (sc, inc) x 6 (18)
Round 3: (2 sc, inc) x 6 (24)
"""

pattern = parse_pattern(text)
report = validate_pattern(pattern)

assert pattern.rounds
assert len(pattern.rounds) == 3
assert report.score >= 50
assert report.to_dict()

print("Parser and validator smoke test passed")
PY

echo "[4/7] Architecture tests"
python test_audit_features.py

echo "[5/7] Feature tests"
python test_all_features.py

echo "[6/7] Pytest suite"
python -m pytest -q

echo "[7/7] Repository status"
git diff --check
git status --short

echo ""
echo "QUALITY GATE PASSED"
