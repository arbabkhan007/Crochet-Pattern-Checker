"""Shared constants, palette handling, number/instruction speech helpers for all Novality kits."""
from __future__ import annotations

import importlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent          # novality_kits/
FONTS = ROOT / "assets" / "fonts"
IMG_ROOT = ROOT / "assets" / "img"
IMG_PDF_ROOT = ROOT / "assets" / "img_pdf"
OUT_ROOT = ROOT / "out"

BRAND = "Novality Crochet Studio"
BRAND_TAG = "#NovalityCrochetStudio"
YEAR = "2026"
SAFETY_BLOCK = False      # user decision (2026-09): no safety panels in customer-facing PDFs. Flip to restore.

DEFAULT_PALETTE = dict(accent="#E8A9B8", deep="#B8506F", pale="#FBEEF1", cream="#FFFBF7",
                       ink="#3B2F33", ink_soft="#7A6A70", mint="#8FCFC0", rule="#EBD7DD", hilite="#F7DCE3")

SLUGS = ["axel", "coco", "ember", "hamish", "halloween", "duck", "momo", "trio", "shelby", "willow"]


def load_pattern(slug):
    sys.path.insert(0, str(ROOT / "patterns"))
    mod = importlib.import_module(slug)
    P = dict(mod.P)
    pal = dict(DEFAULT_PALETTE); pal.update(P.get("palette", {}))
    P["palette"] = pal
    P.setdefault("subtitle", "An amigurumi crochet pattern")
    P.setdefault("hashtags", [BRAND_TAG, P["hashtag"]])
    P.setdefault("file_stem", re.sub(r"[^A-Za-z0-9]+", "_", P["title"]).strip("_"))
    P.setdefault("brand", BRAND); P.setdefault("year", YEAR)
    P.setdefault("images", {"hero": "hero.png", "inhand": "inhand.png", "detail": "detail.png", "colorways": "colorways.png"})
    return P


def hex_rgb(h):
    h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def mix(c1, c2, t):
    a, b = hex_rgb(c1), hex_rgb(c2)
    return "#%02x%02x%02x" % tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


# ------------------------------------------------------------------ numbers -> words
_ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve",
         "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
_TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]


def words(n):
    n = int(n)
    if n < 20: return _ONES[n]
    if n < 100: return _TENS[n // 10] + ("" if n % 10 == 0 else "-" + _ONES[n % 10])
    return str(n)


def label_start(label):
    """'R4' -> 4, 'R4-6' -> 4, 'Row 2' -> 2, 'Found.' -> None."""
    m = re.match(r"(?:R|Row\s*|Rnd\s*)(\d+)", label)
    return int(m.group(1)) if m else None


def spoken_label(label):
    m = re.match(r"R(\d+)-(\d+)$", label)
    if m: return f"Rounds {words(m.group(1))} to {words(m.group(2))}"
    m = re.match(r"R(\d+)$", label)
    if m: return f"Round {words(m.group(1))}"
    m = re.match(r"Row\s*(\d+)$", label)
    if m: return f"Row {words(m.group(1))}"
    if label.lower().startswith("found"): return "Foundation"
    return label


_STITCH = {"sc": "single crochet", "hdc": "half double crochet", "dc": "double crochet", "sl st": "slip stitch",
           "inc": "increase", "dec": "invisible decrease", "invdec": "invisible decrease", "ch": "chain", "picot": "picot"}


def _say_unit(u):
    u = u.strip()
    m = re.fullmatch(r"(\d+)\s*(sc|hdc|dc|sl st|ch)(\*)?", u)
    if m: return f"{words(m.group(1))} {_STITCH[m.group(2)]}" + (" through the leg and body" if m.group(3) else "")
    m = re.fullmatch(r"(sc|hdc|dc|sl st)\s*(\d+)", u)
    if m: return f"{words(m.group(2))} {_STITCH[m.group(1)]}"
    m = re.fullmatch(r"(sc|hdc|dc|sl st) in (?:the )?(next|first|last)\s*(\d+)", u)
    if m: return f"{_STITCH[m.group(1)]} in the {m.group(2)} {words(m.group(3))}"
    m = re.fullmatch(r"(inc|dec|invdec)\s*x\s*(\d+)", u)
    if m: return f"{_STITCH[m.group(1)]} {words(m.group(2))} times"
    m = re.fullmatch(r"(\d+)\s*sc in (?:the )?last( ch| loop)?", u)
    if m: return f"{words(m.group(1))} single crochet in the last chain"
    m = re.fullmatch(r"\((.*)\) (?:all )?in (?:the )?next(?: st)?", u)
    if m: return "a group of " + ", ".join(_STITCH.get(x.strip(), x.strip()) for x in m.group(1).split(",")) + " all in the next stitch"
    if u in _STITCH: return ("one " if u in ("sc", "hdc", "dc") else "") + _STITCH[u]
    if u == "sc in 2nd ch": return "single crochet in the second chain from the hook"
    if u == "sl st in next st": return "slip stitch in the next stitch"
    m = re.fullmatch(r"other side:\s*(.*)", u)
    if m: return "then along the other side of the chain, " + _say_unit(m.group(1))
    return u


def _split_top(s, seps=",;"):
    out, depth, cur = [], 0, ""
    for ch in s:
        if ch in "[(": depth += 1
        if ch in "])": depth -= 1
        if ch in seps and depth == 0: out.append(cur); cur = ""
        else: cur += ch
    out.append(cur)
    return [x.strip() for x in out if x.strip()]


def speak(instr):
    """Turn a table instruction into natural speech. Falls back to reading it as written."""
    s = instr.strip()
    s = re.sub(r"\s*\(\d+ rnds?\)", "", s)
    if s.lower().startswith("blo"):
        return "in back loops only, " + speak(s[3:].lstrip(": ").strip())
    if s.lower().startswith("flo"):
        return "in front loops only, " + speak(s[3:].lstrip(": ").strip())
    m = re.fullmatch(r"(\d+) sc in MR", s)
    if m: return f"{words(m.group(1))} single crochet into a magic ring"
    m = re.match(r"(join [^,]+?), then\s*(.*)$", s, re.I)
    if m: return f"{m.group(1)}, then {speak(m.group(2))}"
    if re.fullmatch(r"inc in each st around", s): return "increase in each stitch around"
    if re.fullmatch(r"sc in each st around|sc around", s): return "single crochet in each stitch around"
    if s == "sc around, then FO": return "single crochet in each stitch around, then fasten off"
    parts = []
    for seg in _split_top(s):
        m = re.fullmatch(r"\[(.*)\]\s*x\s*(\d+)", seg)
        if m:
            inner = _split_top(m.group(1), ",")
            parts.append(", ".join(_say_unit(x) for x in inner) + f", repeated {words(m.group(2))} times")
        else:
            parts.append(_say_unit(seg))
    return "; then ".join(parts) if len(parts) > 3 else ", then ".join(parts)


def count_words(cnt):
    if cnt is None or isinstance(cnt, str): return ""
    return f"{words(cnt).capitalize()} stitches."
