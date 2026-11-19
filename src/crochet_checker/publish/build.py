"""Build Novality Store PDFs into the external cache by default.

Usage:
    python -m crochet_checker.publish.build [--slug SLUG] [--out DIR]
"""
import argparse
import os
import subprocess
import sys
from pathlib import Path



def main():
    ap = argparse.ArgumentParser(description="Build Novality Store pattern PDFs")
    ap.add_argument("--slug", default=None, help="build a single pattern")
    ap.add_argument("--out", default=None, help="output directory (default: external build cache)")
    args = ap.parse_args()
    root = Path(__file__).resolve().parents[3]
    fetcher = root / "tools" / "fetch_build_inputs.py"
    subprocess.run([sys.executable, str(fetcher), "--group", "publish"], check=True, cwd=root)
    from .novality_pdf import build_all

    if args.out is None:
        cache_root = Path(os.environ.get(
            "CROCHET_BUILD_CACHE",
            Path.home() / ".cache" / "crochet-pattern-checker" / "49d69daeb8d7a2462d5e5bef5394a4ff5d170a3b",
        )).expanduser().resolve()
        out_dir = cache_root / "src" / "crochet_checker" / "publish" / "output"
    else:
        out_dir = Path(args.out)
        if not out_dir.is_absolute():
            out_dir = root / out_dir
    paths = build_all(root, out_dir, slug=args.slug)
    for p in paths:
        print(f"built: {p}")


if __name__ == "__main__":
    main()
