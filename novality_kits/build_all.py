"""One-shot pipeline for a set of patterns: verify -> images -> PDF -> Etsy kit -> video (video only if audio clips exist).

Usage: python build_all.py [slug ...] [--no-video] [--no-etsy]
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE / "engine"))
from common import OUT_ROOT, SLUGS, load_pattern  # noqa: E402
from narration import chapters  # noqa: E402

PY = sys.executable


def run(*args):
    print("$", " ".join(args)); subprocess.run([PY, *args], check=True, cwd=HERE)


if __name__ == "__main__":
    slugs = [a for a in sys.argv[1:] if not a.startswith("--")] or SLUGS
    run("engine/verify.py", *slugs)
    run("engine/prep_images.py", *slugs)
    run("engine/build_pdf.py", *slugs)
    if "--no-etsy" not in sys.argv: run("engine/build_etsy.py", *slugs)
    if "--no-video" not in sys.argv:
        for s in slugs:
            P = load_pattern(s)
            clips = [OUT_ROOT / s / "audio" / f"{c['slug']}.mp3" for c in chapters(P)]
            if all(c.exists() for c in clips): run("engine/build_video.py", s)
            else: print(f"[skip video] {s}: {sum(1 for c in clips if c.exists())}/{len(clips)} audio clips present")
