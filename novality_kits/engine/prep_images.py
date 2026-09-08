"""PNG -> JPEG copies for the PDF (keeps PDFs small). Missing slots fall back to the hero shot and are reported."""
import sys
from pathlib import Path
from PIL import Image
sys.path.insert(0, str(Path(__file__).parent))
from common import IMG_ROOT, IMG_PDF_ROOT, load_pattern


def prep(slug):
    P = load_pattern(slug); src = IMG_ROOT / slug; dst = IMG_PDF_ROOT / slug; dst.mkdir(parents=True, exist_ok=True)
    missing = []
    for key, fname in P["images"].items():
        p = src / fname
        if not p.exists():
            missing.append(key); p = src / P["images"]["hero"]
        Image.open(p).convert("RGB").save(dst / (Path(fname).stem + ".jpg"), quality=88, optimize=True)
    return missing


if __name__ == "__main__":
    for slug in sys.argv[1:]:
        m = prep(slug); print(f"{slug:10} {'ok' if not m else 'FALLBACK for ' + ', '.join(m)}")
