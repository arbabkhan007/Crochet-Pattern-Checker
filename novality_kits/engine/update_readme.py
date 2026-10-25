"""Refresh the Audio / Video cells of the Downloads table in novality_kits/README.md
from what actually exists in out/<slug>/.  Run from novality_kits/:  python engine/update_readme.py
"""
import re, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from common import load_pattern, SLUGS, OUT_ROOT
from narration import chapters

ROOT = pathlib.Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
RAW = "https://github.com/arbabkhan007/Crochet-Pattern-Checker/raw/arena/01a079c8-crochet-pattern-checker/novality_kits/out"

def cells(slug):
    P = load_pattern(slug)
    stem = P["file_stem"]
    out = pathlib.Path(OUT_ROOT) / slug
    n_ch = len(chapters(P))
    have = len(list((out / "audio").glob("*.mp3"))) if (out / "audio").exists() else 0
    mp3 = out / f"{stem}_Full_Walkthrough.mp3"
    mp4 = out / f"{stem}_Tutorial.mp4"
    audio = f"[MP3]({RAW}/{slug}/{mp3.name}) ({mp3.stat().st_size // 1024 // 1024} MB)" if mp3.exists() else f"— ({have}/{n_ch} ch.)"
    video = f"[MP4]({RAW}/{slug}/{mp4.name}) ({mp4.stat().st_size // 1024 // 1024} MB)" if mp4.exists() else "—"
    return P["title"], audio, video

def main():
    text = README.read_text()
    lines = text.split("\n")
    names = {}
    for slug in SLUGS:
        name, audio, video = cells(slug)
        names[name] = (audio, video)
    out_lines = []
    for ln in lines:
        m = re.match(r"^\| (.+?) \| NS \d\d \| ", ln)
        if m and m.group(1) in names:
            parts = ln.split(" | ")
            # columns: Pattern | Code | Rounds | PDF | Etsy kit | Audio | Video |
            audio, video = names[m.group(1)]
            parts[5] = audio
            parts[6] = video + " |"
            ln = " | ".join(parts)
        out_lines.append(ln)
    new = "\n".join(out_lines)
    pending = [n for n, (a, v) in names.items() if a.startswith("—") or v == "—"]
    note = "Audio/video marked — are still being rendered (10 speech clips per session)."
    if not pending and note in new:
        new = new.replace(note, "All ten kits are complete.")
    README.write_text(new)
    print("README updated; pending:", pending or "none")

if __name__ == "__main__":
    main()
