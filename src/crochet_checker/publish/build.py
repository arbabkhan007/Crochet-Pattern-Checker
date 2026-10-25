"""Build all Novality Store pattern PDFs into final_patterns/.

Usage:
    python -m crochet_checker.publish.build [--slug SLUG] [--out DIR]
"""
import argparse
from pathlib import Path

from .novality_pdf import build_all


def main():
    ap = argparse.ArgumentParser(description="Build Novality Store pattern PDFs")
    ap.add_argument("--slug", default=None, help="build a single pattern")
    ap.add_argument("--out", default="final_patterns", help="output directory")
    args = ap.parse_args()
    root = Path(__file__).resolve().parents[3]
    out_dir = root / args.out
    paths = build_all(root, out_dir, slug=args.slug)
    for p in paths:
        print(f"built: {p}")


if __name__ == "__main__":
    main()
