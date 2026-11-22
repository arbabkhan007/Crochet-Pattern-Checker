"""Refresh the Audio / Video cells in novality_kits/README.md.

Published files are sourced from external-media-manifest.json, not from a
local build directory, so deleting local generated outputs does not break the
published links. Outputs built locally but absent from the manifest are not
linked because the pinned mirror has no verified copy of them.

Run from novality_kits/: python engine/update_readme.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import OUT_ROOT, SLUGS, load_pattern  # noqa: E402
from narration import chapters  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
MANIFEST_PATH = ROOT / "external-media-manifest.json"
MANIFEST = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
RAW = MANIFEST["canonical_remote"]["raw_base"].rstrip("/")
PUBLISHED = {item["path"]: item for item in MANIFEST["files"]}


def published_cell(path: Path, label: str) -> str | None:
    """Return a pinned download link only when the manifest verifies a copy."""
    relative = f"out/{path.relative_to(Path(OUT_ROOT)).as_posix()}"
    item = PUBLISHED.get(relative)
    if item is None:
        return None
    out_relative = relative.removeprefix("out/")
    size_mb = int(item["bytes"]) // 1024 // 1024
    return f"[{label}]({RAW}/{out_relative}) ({size_mb} MB)"


def cells(slug: str) -> tuple[str, str, str]:
    pattern = load_pattern(slug)
    stem = pattern["file_stem"]
    out = Path(OUT_ROOT) / slug
    n_chapters = len(chapters(pattern))
    audio_dir = out / "audio"
    have = len(list(audio_dir.glob("*.mp3"))) if audio_dir.exists() else 0
    mp3 = out / f"{stem}_Full_Walkthrough.mp3"
    mp4 = out / f"{stem}_Tutorial.mp4"

    audio = published_cell(mp3, "MP3")
    if audio is None:
        audio = "— (local build; not published)" if mp3.exists() else f"— ({have}/{n_chapters} ch.)"
    video = published_cell(mp4, "MP4")
    if video is None:
        video = "— (local build; not published)" if mp4.exists() else "—"
    return pattern["title"], audio, video


def main() -> None:
    text = README.read_text(encoding="utf-8")
    names = {load_pattern(slug)["title"]: cells(slug)[1:] for slug in SLUGS}
    out_lines = []
    for line in text.split("\n"):
        match = re.match(r"^\| (.+?) \| NS \d\d \| ", line)
        if match and match.group(1) in names:
            parts = line.split(" | ")
            # columns: Pattern | Code | Rounds | PDF | Etsy kit | Audio | Video |
            audio, video = names[match.group(1)]
            parts[5] = audio
            parts[6] = video + " |"
            line = " | ".join(parts)
        out_lines.append(line)

    updated = "\n".join(out_lines)
    pending = [name for name, (audio, video) in names.items() if audio.startswith("—") or video.startswith("—")]
    old_note = "Audio/video marked — are still being rendered (10 speech clips per session)."
    new_note = "Audio/video marked — are not published yet; chapter counts show render progress."
    if old_note in updated:
        updated = updated.replace(old_note, new_note)
    README.write_text(updated, encoding="utf-8")
    print("README updated; unpublished:", pending or "none")


if __name__ == "__main__":
    main()
