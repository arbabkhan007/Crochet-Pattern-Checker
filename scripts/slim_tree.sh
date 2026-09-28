#!/usr/bin/env bash
# Move unused product claims out of the package. Safe to run twice.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p experimental/not_the_product
for name in features agents marketplace ai_enhanced generator library pricing; do
  src="src/crochet_checker/$name"
  dest="experimental/not_the_product/$name"
  if [ -d "$src" ]; then
    rm -rf "$dest"
    mv "$src" "$dest"
    echo "moved $src"
  fi
done
for name in \
  pytest-errors.txt remaining-errors.txt collection-errors.txt \
  collaboration.json crochet_analytics.json crochet_budget.json notifications.json \
  generated_sphere_small.json crochet_3d_viewer.html crochet_dashboard.html \
  watermark_preview.html ADD_3_FEATURES_TO_REPO.sh NEW_FEATURES_COMPLETE.md \
  TEST_CAPABILITY_PROMPT.md PROJECT_CONTEXT.md push_pdf_features.sh \
  test_bunny.sh workaround_helper.sh test.md test_all_features.py \
  test_new_features.py test_blender.py crochet-architecture.bundle
 do
  if [ -e "$name" ]; then
    mkdir -p experimental/not_the_product/root_junk
    mv "$name" experimental/not_the_product/root_junk/
    echo "moved $name"
  fi
done

for name in \
  src/crochet_checker/__init__.py.backup \
  src/crochet_checker/cli.py.backup \
  src/crochet_checker/crochet-architecture.bundle \
  src/crochet_checker/new_features.tar.gz \
  install_premium_features.py \
  run_ai_agents.py \
  test_audit_features.py
 do
  if [ -e "$name" ]; then
    mkdir -p experimental/not_the_product/root_junk
    mv "$name" experimental/not_the_product/root_junk/
    echo "moved $name"
  fi
done

echo "Tree slimmed. The checker remains in src/crochet_checker."
