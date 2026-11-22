#!/usr/bin/env python3
"""Self-contained HTML editions of the whole Novality line (NS 01-10).

Reuses the exact validated spec data that drives the PDFs, so HTML and PDF
can never drift apart. Output: deliverables/html/<pattern>.html (one per
pattern, images inlined as base64, print-friendly) + a catalog index.
"""
from __future__ import annotations

import base64
import io
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from content_ns0103 import HAMISH, KAWAII, AXEL  # noqa: E402
from content_ns0406 import COCO, DUCK, MOMO  # noqa: E402
from content_ns0709 import TRIO, EMBER, SHELBY  # noqa: E402

OUT = ROOT / "deliverables" / "html"


def cover_b64(cover: str, width=880, ratio=2.35, quality=82):
    img = Image.open(ROOT / cover).convert("RGB")
    W, H = img.size
    tgt_h = int(W / ratio)
    top = int((H - tgt_h) * 0.42)
    img = img.crop((0, top, W, top + tgt_h)).resize((width, int(width / ratio)))
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=quality)
    return base64.b64encode(buf.getvalue()).decode()


def thumb_b64(cover: str, width=420, quality=74):
    img = Image.open(ROOT / cover).convert("RGB")
    img.thumbnail((width, width))
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=quality)
    return base64.b64encode(buf.getvalue()).decode()


WILLOW = dict(
    slug="willow", code="NS 10", file_stem="Willow_the_Bunny_Lovey_Crochet_Pattern_NS10",
    title="Willow the Bunny Lovey",
    subtitle="A bunny comforter — a soft, firmly stuffed head above a light, drapey granny-square blanket; long floppy ears to hold and an embroidered face with no small parts",
    cover="assets/willow_cover.png",
    badges=["No small parts", "Advanced beginner", "2–3 hours"],
    size_line="Blanket about 26 cm (10 in) square after 20 rounds (≈ 37 cm corner to corner)  •  head ≈ 4.9 cm across, 5.7 cm tall  •  ≈ 25 cm ear tips to corner",
    materials_line="DK #3 100% cotton ~60 g / 140–150 m  •  3.5 mm hook (3.0 mm head if loose)  •  embroidered face, no safety eyes  •  ~8 g fibre fill",
    terms_name="loveys", tags="#WillowTheBunnyLovey",
    theme=dict(dark=(58, 92, 64), accent=(122, 154, 122), soft=(233, 239, 231),
               box_bg=(247, 236, 239), box_edge=(196, 126, 140)),
    safety=dict(title="SAFETY — A BABY ITEM, READ THIS", lines=[
        ("No safety eyes, buttons, beads or removable parts. The face is fully embroidered and every floss "
         "end is knotted inside the head.", True),
        "Willow is not a tested toy (ASTM F963 / EN 71). Never list or describe her as “baby-safe”.",
        "Comforters are not recommended in the cot for babies under 12 months — use with supervision, and "
        "say so in your listing.",
        ("Sew every seam twice. Weave every end in at least 5 cm (2 in).", True),
    ]),
    materials=[
        ("Yarn:", "DK (#3) 100% cotton (or a baby-safe certified blend), about 60 g / 140–150 m — cream, "
         "sage, dusty pink or pale grey, plus a scrap of contrast cotton for embroidery. Buy two 50 g balls "
         "so you never run short. Only the head is stuffed."),
        ("Hook:", "3.5 mm (US E/4) for the blanket; 3.0 mm for the head if your tension is loose."),
        ("Face:", "dark brown or charcoal cotton floss. No safety eyes."),
        ("Also:", "about 8 g fibre fill, tapestry needle, stitch marker."),
    ],
    gauge=[("1 dc ≈ 4.3 mm wide and 1 round ≈ 3.8 mm deep. After blanket Rnd 4, 9 dc along an edge should "
            "measure ≈ 39 mm (1.5 in).", True),
           "Narrower? Go up a hook size — or keep the hook and add rounds (22 rounds ≈ 28 cm)."],
    abbrev="MR magic ring  •  ch chain  •  sl st slip stitch  •  sc single crochet (UK dc)  •  dc double crochet "
           "(UK tr)  •  inc increase — 2 sc in the same stitch  •  dec decrease — sc2tog over 2 sts  •  Rnd round  •  "
           "( ) stitch count at round end. On head and ears chains are never counted; on the blanket the "
           "beginning ch-3 counts as one dc.",
    construction=[
        ("Spiral pieces.", "the head and ears are worked in a continuous spiral — no joins, marker in the "
         "first stitch of every round, never turn."),
        ("The blanket.", "worked in joined rounds — each round closes with a slip stitch and the next begins "
         "with a ch-3 that counts as your first dc. Never turn."),
        ("Loops.", "work every stitch through both loops unless noted."),
    ],
    techniques=[
        ("Magic ring & spiral", "the head and each ear begin with a magic ring; pull the tail tight after "
         "round one."),
        ("The granny-square corner", "every blanket corner is (3 dc, ch 2, 3 dc) into one corner space. Those "
         "four corners make the piece square instead of round. Miss one corner group and the whole square "
         "pulls out of true — check all four at the end of every round."),
        ("The border round", "a final round of single crochet around the edge, with 3 sc into each corner "
         "space, squares the edge and stops the blanket curling. Do not skip it."),
    ],
    sizing_tables=[dict(
        title="Sizing the blanket",
        headers=["Rounds", "Approx. size (square)", "Use"],
        rows=[["18 rounds", "≈ 23 cm (9 in)", "small comforter / preemie gift"],
              ["20 rounds", "≈ 26 cm (10 in)", "the classic Willow (this pattern)"],
              ["22 rounds", "≈ 28 cm (11 in)", "bigger lovey, same recipe"]],
        aligns=["C", "L", "L"],
        note="The square grows ≈ 1.3 cm per side per round — add rounds two at a time.")],
    pieces=[
        dict(title="1 · Head — make 1",
             note="Continuous spiral, no joins. Marker in the first stitch of every round.",
             table=dict(headers=["Rnd", "Instruction", "Sts", "Notes"],
                        rows=[["1", "6 sc in MR", "6", "pull ring tight"],
                              ["2", "inc in each st around", "12", ""],
                              ["3", "[sc, inc] × 6", "18", ""],
                              ["4", "[2 sc, inc] × 6", "24", "ears attach at Rnds 4–6"],
                              ["5", "[3 sc, inc] × 6", "30", ""],
                              ["6", "[4 sc, inc] × 6", "36", "full width"],
                              ["7", "sc in each st around", "36", ""],
                              ["8", "sc in each st around", "36", "face on Rnds 8–9"],
                              ["9", "sc in each st around", "36", ""],
                              ["10", "sc in each st around", "36", ""],
                              ["11", "[4 sc, dec] × 6", "30", "begin stuffing firmly"],
                              ["12", "[3 sc, dec] × 6", "24", ""],
                              ["13", "[2 sc, dec] × 6", "18", "top up stuffing"],
                              ["14", "[sc, dec] × 6", "12", ""],
                              ["15", "dec × 6", "6", "fasten off, close the hole"]]),
             boxes=[dict(lines=[
                 ("The decrease ladder must step 36 → 30 → 24 → 18 → 12 → 6 — that is why the head has 15 "
                  "rounds.", False),
                 ("Stuff FIRMLY — a soft head collapses when gripped and the face distorts. Finished head ≈ "
                  "4.9 cm across and 5.7 cm tall.", True)])]),
        dict(title="2 · Ears — make 2 (do not stuff)",
             table=dict(headers=["Rnd", "Instruction", "Sts", "Notes"],
                        rows=[["1", "6 sc in MR", "6", ""],
                              ["2", "[sc, inc] × 3", "9", ""],
                              ["3", "[2 sc, inc] × 3", "12", "widest point"],
                              ["4–8", "sc in each st around (5 rnds)", "12", "the long, floppy part"],
                              ["9", "[2 sc, dec] × 3", "9", ""],
                              ["10", "sc in each st around", "9", "taper to the base"],
                              ["11", "[sc, dec] × 3", "6", "flatten, fasten off long tail"]]),
             paras=["Pinch each ear base flat and fasten off with a long tail. Sew the ears to Rnds 4–6 of the "
                    "head, about 10 stitches apart, pinching each base so the ear flops forward."]),
        dict(title="3 · Granny-square blanket — joined rounds, 3.5 mm hook",
             paras=["Foundation: ch 4 and sl st to the first ch to form a ring.",
                    "Rnd 1: ch 3 (counts as first dc), 2 dc in the ring, [ch 2, 3 dc in the ring] × 3, ch 2, "
                    "sl st to the top of the ch-3.  [12 dc, 4 corner spaces]",
                    "Rnd 2: sl st into the next corner space; ch 3, 2 dc in that space, ch 2, 3 dc in the same "
                    "space (first corner); then (3 dc, ch 2, 3 dc) into each remaining corner space; sl st to "
                    "close.  [24 dc]",
                    "Rnd 3 (setup): sl st into the next corner space; ch 3, (2 dc, ch 2, 3 dc) in the same "
                    "space; *3 dc in the next side space, (3 dc, ch 2, 3 dc) in the next corner space*; repeat "
                    "from * around; sl st to close.  [36 dc]",
                    "Rnds 4–20: as Rnd 3 — 3 dc into every side space and (3 dc, ch 2, 3 dc) into every corner "
                    "space. Each round adds one 3-dc group to every side (+12 dc per round)."],
             boxes=[dict(title="COUNT CHECK — before you close any round", lines=[
                 "Four crisp (3 dc, ch 2, 3 dc) corners — every time. Then total double crochets:",
                 ("Rnd 3 = 36   |   Rnd 5 = 60   |   Rnd 10 = 120   |   Rnd 15 = 180   |   Rnd 20 = 240   "
                  "(60 dc per edge ≈ 26 cm)", True)]),
                    dict(title="Border — do not skip", lines=[
                 "Work one final round of sc all the way around: 1 sc into each dc and 3 sc into each corner "
                 "space, then sl st and fasten off. At Rnd 20 that is 240 sc + 12 corner sc = 252 sc."])]),
    ],
    assembly=dict(
        title="4 · Face & assembly",
        bullets=[
            ("Eyes:", "two small embroidered ovals, about 8 stitches apart, across Rnds 8–9 of the head."),
            ("Nose:", "a small inverted triangle centred between and just below the eyes."),
            ("Mouth:", "a shallow Y from the base of the nose. Knot every floss end inside the head and bury "
             "the tails before closing. Skip blush — chalk rubs off on bedding and is not washable."),
            ("Joining:", "centre the head over one corner of the square, overlapping the blanket by about "
             "3 cm. Sew all the way around the base of the head — then sew it a second time. This is the only "
             "structural seam and it will be pulled, chewed and washed. Weave every end in at least 5 cm."),
        ],
        checklist=["1 head (stuffed, 15 rounds)  •  2 ears  •  1 granny square (20 rounds + border).",
                   "Why two passes? The head-to-blanket seam carries the whole toy — two passes survive "
                   "chewing and machine washing."],
        listing=[("Materials:", "100% cotton, embroidered face, no safety eyes, no buttons, beads or "
                  "removable parts."),
                 ("Care:", "machine wash cool on a gentle cycle inside a mesh bag; reshape while damp and dry "
                  "flat. Do not tumble dry — cotton can shrink and the stuffing may clump."),
                 ("Supervision:", "comforters are not recommended in the cot for babies under 12 months; use "
                  "with supervision. Copy this into your listing."),
                 ("Colorways:", "cream, sage, dusty pink, pale grey and butter yellow — neutrals outsell "
                  "brights in the baby category.")]),
    troubleshooting=[
        ("Blanket curls / not square?", "you skipped the sc border, or missed a (3 dc, ch 2, 3 dc) corner. "
         "Check all four corners at the end of every round."),
        ("Came out too small / head flops?", "gauge tighter than 4.3 mm per dc — go up a hook size or add "
         "rounds (22 rounds ≈ 28 cm). Stuff the head firmly and sew the base seam twice."),
    ],
    colorways=[("Cream", (240, 232, 214)), ("Sage", (154, 166, 138)),
               ("Dusty pink", (214, 164, 170)), ("Pale grey", (196, 198, 198)),
               ("Butter yellow", (232, 208, 140))],
    checks=[
        ["Head Rnds 1–15: count chain 6 → 36 → 6 (ladder 36→30→24→18→12→6)", "✓ verified"],
        ["Ear Rnds 1–11: count chain 6 → 12 → 6", "✓ verified"],
        ["Granny square: +12 dc per round, 12 → 240 over 20 rnds", "✓ verified"],
        ["Border: 240 dc + 4 × 3 corner sc = 252 sc", "✓ verified"],
        ["Sizes vs. gauge: 18/20/22 rounds ≈ 23/26/28 cm", "✓ verified"],
        ["Gauge probe: 9 dc ≈ 39 mm (measurable from Rnd 4)", "✓ verified"],
        ["Head size: 36 sts ≈ 4.9 cm across; 15 rnds ≈ 5.7 cm tall", "✓ verified"],
    ],
    safety_reminder="Willow has NO safety eyes, buttons, beads or removable parts — the face is embroidered "
                    "and floss ends are knotted inside the head. Even so she is not a tested toy "
                    "(ASTM F963 / EN 71): do not claim “baby-safe”. Comforters are not recommended in a cot "
                    "for babies under 12 months and should be used with supervision; sew every seam twice and "
                    "weave ends in at least 5 cm.",
)

SPECS = [HAMISH, KAWAII, AXEL, COCO, DUCK, MOMO, TRIO, EMBER, SHELBY, WILLOW]


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


CSS = """
:root{--dark:%(dark)s;--accent:%(accent)s;--soft:%(soft)s;--boxbg:%(boxbg)s;--edge:%(edge)s;}
*{box-sizing:border-box}
body{margin:0;font-family:-apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;color:#383634;
     background:#faf8f4;line-height:1.55}
main{max-width:860px;margin:0 auto;padding:0 20px 60px}
.hero img{width:100%%;display:block;border-radius:0 0 14px 14px}
.hero .bar{height:6px;background:var(--dark)}
h1{font-family:Georgia,'Times New Roman',serif;font-size:2.1rem;margin:.6em 0 .1em;text-align:center}
.sub{text-align:center;color:#5c5854;margin:0 0 .4em}
.code{text-align:center;color:#767269;font-size:.9rem;margin-bottom:1em}
.badges{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin:14px 0 18px}
.badge{background:var(--soft);color:var(--dark);font-weight:600;font-size:.82rem;
       padding:5px 13px;border-radius:999px}
.badge.first{background:var(--boxbg);color:var(--edge)}
.meta{text-align:center;color:#6e6a66;font-size:.92rem;max-width:680px;margin:0 auto 6px}
section{background:#fff;border:1px solid #e6e3dc;border-radius:12px;padding:22px 24px;margin:18px 0}
h2{font-family:Georgia,serif;color:var(--dark);font-size:1.25rem;margin:0 0 10px;
   border-bottom:2px solid var(--soft);padding-bottom:6px}
h3{color:var(--dark);margin:18px 0 8px;font-size:1.02rem}
.safety{border:1.5px solid var(--edge);background:var(--boxbg)}
.safety h2{color:var(--edge);border-color:transparent}
.safety strong{color:var(--edge)}
table{width:100%%;border-collapse:collapse;margin:10px 0 6px;font-size:.92rem}
th{background:var(--dark);color:#fff;text-align:left;padding:7px 9px;font-weight:600}
td{padding:6px 9px;border:1px solid #e3e0d8;vertical-align:top}
tbody tr:nth-child(odd){background:var(--soft)}
td.c,th.c{text-align:center}
ul{margin:8px 0;padding-left:0;list-style:none}
ul li{padding-left:18px;position:relative;margin:7px 0}
ul li:before{content:'';position:absolute;left:2px;top:.55em;width:6px;height:6px;border-radius:50%%;
             background:var(--edge)}
.callout{background:var(--soft);border-left:4px solid var(--dark);border-radius:8px;
         padding:12px 16px;margin:12px 0;font-size:.93rem}
.check{background:var(--soft);border-left:4px solid var(--dark)}
.chips{display:flex;flex-wrap:wrap;gap:14px;margin:8px 0 2px}
.chip{display:flex;align-items:center;gap:7px;font-size:.9rem}
.dot{width:16px;height:16px;border-radius:50%%;border:1px solid rgba(0,0,0,.15)}
.foot{background:#f3efe6;border-radius:12px;padding:18px 24px;margin-top:20px;text-align:center;color:#6e6a66}
.foot b{font-family:Georgia,serif;color:var(--dark);letter-spacing:.08em}
.vt td:last-child{text-align:center;white-space:nowrap}
@media print{body{background:#fff}section{border:none;padding:8px 0;break-inside:avoid-page}
.hero img{border-radius:0}}
"""


def render_table(t):
    aligns = t.get("aligns") or ["L"] * len(t["headers"])
    head = "".join(f'<th class="{"c" if a == "C" else ""}">{esc(str(h))}</th>'
                   for h, a in zip(t["headers"], aligns))
    body = ""
    for row in t["rows"]:
        cells = "".join(f'<td class="{"c" if a == "C" else ""}">{esc(str(c))}</td>'
                        for c, a in zip(row, aligns))
        body += f"<tr>{cells}</tr>"
    return f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>"


def render_lines(lines):
    out = []
    for ln in lines:
        if isinstance(ln, str):
            out.append(esc(ln))
        else:
            text, bold = ln[0], ln[1]
            out.append(f"<strong>{esc(text)}</strong>" if bold else esc(text))
    return " ".join(out)


def render_piece(p):
    h = [f"<h2>{esc(p['title'])}</h2>"]
    if p.get("note"):
        h.append(f"<p><em>{esc(p['note'])}</em></p>")
    if p.get("table"):
        h.append(render_table(p["table"]))
    for txt in p.get("paras", []):
        h.append(f"<p>{esc(txt)}</p>")
    if p.get("finish"):
        h.append("<ul>" + "".join(
            f"<li><strong>{esc(lead)}</strong> {esc(t)}</li>" for lead, t in p["finish"]) + "</ul>")
    for bx in p.get("boxes", []):
        cls = "callout check" if bx.get("title", "").startswith("COUNT") else "callout"
        inner = f"<h3>{esc(bx['title'])}</h3>" if bx.get("title") else ""
        h.append(f'<div class="{cls}">{inner}{render_lines(bx["lines"])}</div>')
    for sub in p.get("extra_tables", []):
        if sub.get("title"):
            h.append(f"<h3>{esc(sub['title'])}</h3>")
        h.append(render_table(sub))
        for txt in sub.get("paras", []):
            h.append(f"<p>{esc(txt)}</p>")
    return f"<section>{''.join(h)}</section>"


def render_spec(spec):
    th = spec["theme"]
    rgb = lambda c: f"rgb({c[0]},{c[1]},{c[2]})"
    css = CSS % dict(dark=rgb(th["dark"]), accent=rgb(th["accent"]), soft=rgb(th["soft"]),
                     boxbg=rgb(th["box_bg"]), edge=rgb(th["box_edge"]))
    badges = "".join(
        f'<span class="badge{" first" if i == 0 else ""}">{esc(b)}</span>'
        for i, b in enumerate(spec["badges"] + ["Stitch counts verified"]))

    parts = [f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
             f'<meta name="viewport" content="width=device-width,initial-scale=1">'
             f'<title>{esc(spec["title"])} — Crochet Pattern {esc(spec["code"])}</title>'
             f'<style>{css}</style></head><body>']

    img = cover_b64(spec["cover"])
    parts.append(f'<div class="hero"><img src="data:image/jpeg;base64,{img}" '
                 f'alt="{esc(spec["title"])}"><div class="bar"></div></div><main>')
    parts.append(f'<h1>{esc(spec["title"])}</h1>'
                 f'<p class="sub">{esc(spec["subtitle"])}</p>'
                 f'<p class="code">Design Code {esc(spec["code"])} — Novality Store</p>'
                 f'<div class="badges">{badges}</div>'
                 f'<p class="meta">{esc(spec["size_line"])}</p>'
                 f'<p class="meta">{esc(spec["materials_line"])}</p>')

    s = spec["safety"]
    parts.append('<section class="safety">' + render_lines(
        [s["title"]] and []) )
    parts.append(f'<h2>{esc(s["title"])}</h2>' + render_lines(s["lines"]) + "</section>")

    parts.append("<section><h2>Materials</h2><ul>" + "".join(
        f'<li><strong>{esc(lead)}</strong> {esc(t)}</li>' for lead, t in spec["materials"]) + "</ul>")
    if spec.get("gauge"):
        parts.append('<div class="callout check"><h3>Gauge &amp; size check</h3>' +
                     render_lines(spec["gauge"]) + "</div>")
    if spec.get("abbrev"):
        parts.append(f"<h3>Abbreviations — US terms</h3><p>{esc(spec['abbrev'])}</p>")
    parts.append("</section>")

    if spec.get("construction") or spec.get("techniques"):
        parts.append("<section>")
        if spec.get("construction"):
            parts.append("<h2>Before you begin</h2><ul>" + "".join(
                f'<li><strong>{esc(lead)}</strong> {esc(t)}</li>'
                for lead, t in spec["construction"]) + "</ul>")
        if spec.get("techniques"):
            parts.append(f'<h2>{esc(spec.get("techniques_title", "Techniques used"))}</h2><ul>' +
                         "".join(f'<li><strong>{esc(lead)}</strong> — {esc(t)}</li>'
                                 for lead, t in spec["techniques"]) + "</ul>")
        for bx in spec.get("technique_boxes", []):
            parts.append(f'<div class="callout"><h3>{esc(bx.get("title", ""))}</h3>' +
                         render_lines(bx["lines"]) + "</div>")
        for t in spec.get("sizing_tables", []):
            parts.append(f"<h3>{esc(t.get('title', 'Sizing'))}</h3>" + render_table(t))
            if t.get("note"):
                parts.append(f"<p><em>{esc(t['note'])}</em></p>")
        parts.append("</section>")

    for p in spec["pieces"]:
        parts.append(render_piece(p))

    a = spec.get("assembly")
    if a:
        parts.append(f'<section><h2>{esc(a.get("title", "Assembly"))}</h2>')
        if a.get("intro"):
            parts.append(f"<p>{esc(a['intro'])}</p>")
        if a.get("bullets"):
            parts.append("<ul>" + "".join(
                f'<li><strong>{esc(lead)}</strong> {esc(t)}</li>' for lead, t in a["bullets"]) + "</ul>")
        for bx in a.get("boxes", []):
            parts.append(f'<div class="callout"><h3>{esc(bx.get("title", ""))}</h3>' +
                         render_lines(bx["lines"]) + "</div>")
        if a.get("checklist"):
            parts.append('<div class="callout check"><h3>Before you sew — lay every component out and check</h3>'
                         + "".join(f"<p>{esc(c)}</p>" for c in a["checklist"]) + "</div>")
        if a.get("listing"):
            parts.append("<h3>For your Etsy listing</h3><ul>" + "".join(
                f'<li><strong>{esc(lead)}</strong> {esc(t)}</li>' for lead, t in a["listing"]) + "</ul>")
        if a.get("care"):
            parts.append(f"<h3>Care</h3><p>{esc(a['care'])}</p>")
        parts.append("</section>")

    if spec.get("troubleshooting"):
        parts.append("<section><h2>Troubleshooting</h2><ul>" + "".join(
            f'<li><strong>{esc(lead)}</strong> {esc(t)}</li>'
            for lead, t in spec["troubleshooting"]) + "</ul></section>")

    parts.append('<section><h2>Why this pattern works — validation summary</h2>'
                 '<p>Every stitch count was checked with deterministic math (Crochet Pattern Checker): '
                 'round-by-round production vs. consumption, stated counts, and every size claim against '
                 'the stated gauge.</p>'
                 '<table class="vt"><thead><tr><th>Check</th><th class="c">Result</th></tr></thead><tbody>'
                 + "".join(f"<tr><td>{esc(c)}</td><td>{esc(r)}</td></tr>" for c, r in spec["checks"])
                 + "</tbody></table></section>")

    chips = "".join(f'<span class="chip"><span class="dot" style="background:rgb{rgb}"></span>{esc(n)}</span>'
                    for n, rgb in spec.get("colorways", []))
    if chips:
        parts.append(f'<section><h2>Colorways</h2><div class="chips">{chips}</div></section>')

    parts.append('<section><h2>Terms of use</h2>'
                 f'<h3>Copyright &amp; ownership</h3><p>This crochet pattern — including all instructions, '
                 f'stitch counts, photography and design elements — is the original work and intellectual '
                 f'property of Novality Store, designed by Novality Crochet Studio. Design Code '
                 f'{esc(spec["code"])}. © 2026 Novality Store. All rights reserved.</p>'
                 f'<h3>You may</h3><p>Make as many finished {esc(spec.get("terms_name", "items"))} as you like '
                 f'for yourself, gifts, or charity. Sell physical finished items made from this pattern in '
                 f'small batches, in shops, markets and online, provided credit is given to “Novality '
                 f'Store”.</p>'
                 '<h3>You may not</h3><p>Resell, share, redistribute, translate, rewrite, publish or upload '
                 'this digital pattern or its contents in any form. Do not alter, copy or recolor the pattern '
                 'and claim it as your own. Do not use the Novality Store name, logo or photos beyond '
                 'crediting the pattern. Do not mass-produce finished items commercially without written '
                 'permission.</p>'
                 '<div class="callout safety" style="border-radius:8px"><strong>SAFETY REMINDER — </strong>'
                 + esc(spec["safety_reminder"]) + "</div></section>")

    parts.append(f'<div class="foot"><b>NOVALITY STORE</b><br>Happy crocheting! Tag your makes with '
                 f'#NovalityStore and {esc(spec["tags"])}<br><small>Design Code {esc(spec["code"])}  •  '
                 f'US terms  •  stitch counts independently verified</small></div></main></body></html>')
    return "".join(parts)


def build_catalog(cards):
    rgb = lambda c: f"rgb({c[0]},{c[1]},{c[2]})"
    css = CSS % dict(dark=rgb((58, 92, 64)), accent=rgb((122, 154, 122)),
                     soft=rgb((233, 239, 231)), boxbg=rgb((247, 236, 239)),
                     edge=rgb((196, 126, 140)))
    items = ""
    for spec in specs_all:
        t = thumb_b64(spec["cover"], width=420)
        items += (f'<a class="card" href="{esc(spec["slug"])}.html">'
                  f'<img src="data:image/jpeg;base64,{t}" alt="{esc(spec["title"])}">'
                  f'<div class="pad"><b>{esc(spec["title"])}</b>'
                  f'<span>{esc(spec["code"])}  •  {" • ".join(esc(b) for b in spec["badges"])}</span></div></a>')
    return ('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>Novality Crochet Pattern Collection</title><style>' + css +
            '.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:16px}'
            '.card{background:#fff;border:1px solid #e6e3dc;border-radius:12px;overflow:hidden;'
            'text-decoration:none;color:#383634;display:block}'
            '.card img{width:100%;display:block;aspect-ratio:1/1;object-fit:cover}'
            '.card .pad{padding:10px 14px 14px;display:flex;flex-direction:column;gap:4px}'
            '.card b{font-family:Georgia,serif;color:#3a5c40}'
            '.card span{font-size:.78rem;color:#767269}'
            '.dl{display:inline-block;background:#3a5c40;color:#fff;font-weight:600;padding:10px 22px;'
            'border-radius:999px;text-decoration:none;margin:6px 0 22px}'
            '</style></head><body><main>'
            '<h1>Novality Crochet Pattern Collection</h1>'
            '<p class="sub">10 validated patterns — stitch counts independently verified</p>'
            '<p style="text-align:center"><a class="dl" href="../Novality_Crochet_Patterns_Bundle.zip">'
            '⬇ Download the full bundle (PDF + HTML)</a></p>'
            f'<div class="grid">{items}</div>'
            '<div class="foot"><b>NOVALITY STORE</b><br>© 2026 Novality Store — patterns for personal and '
            'small-batch commercial use as stated in each pattern’s terms.</div>'
            '</main></body></html>')


specs_all = SPECS


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for spec in SPECS:
        html = render_spec(spec)
        out = OUT / f"{spec['slug']}.html"
        out.write_text(html)
        print(f"{out.name:22s} {out.stat().st_size/1024:6.0f} KB")
    (OUT / "index.html").write_text(build_catalog(SPECS))
    print("index.html (catalog) written")


if __name__ == "__main__":
    main()
