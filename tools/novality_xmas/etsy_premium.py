"""Premium Etsy stacks - 15 slots per Christmas pattern, regenerated.
Full-bleed editorial photos + airy ivory cards, one muted brand palette.
Output: final_patterns/christmas/etsy_premium/<CODE>/NSxx_01..15.jpg
"""
from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path("final_patterns/christmas/etsy_premium")
SRC = ROOT / "src"
W, H = 2400, 1800

# palette -----------------------------------------------------------------
IVORY = (250, 247, 240)
PAPER = (255, 254, 249)
INK = (47, 45, 54)
EVERGREEN = (46, 75, 63)
CRANBERRY = (168, 63, 55)
GOLD = (187, 146, 79)
MIST = (236, 231, 219)
SOFT = (96, 92, 104)

FD = Path("/usr/share/fonts/truetype/dejavu")


def serif(sz, bold=True):
    return ImageFont.truetype(str(FD / (("DejaVuSerif-Bold" if bold else "DejaVuSerif") + ".ttf")), sz)


def sans(sz, bold=False):
    return ImageFont.truetype(str(FD / (("DejaVuSans-Bold" if bold else "DejaVuSans") + ".ttf")), sz)


def spaced(txt):  # small-caps feel
    return " ".join(list(txt)) if len(txt) < 42 else txt


# primitives ---------------------------------------------------------------
def fit(path, tw, th):
    im = Image.open(path).convert("RGB")
    s = max(tw / im.width, th / im.height)
    im = im.resize((int(im.width * s + 1), int(im.height * s + 1)), Image.LANCZOS)
    x = (im.width - tw) // 2
    y = (im.height - th) // 2
    return im.crop((x, y, x + tw, y + th))


def card():
    im = Image.new("RGB", (W, H), IVORY)
    return im, ImageDraw.Draw(im)


def rule(d, x0, y, x1, color=GOLD, width=4):
    d.line([x0, y, x1, y], fill=color, width=width)


def center(d, y, txt, fnt, color=INK):
    d.text((W // 2, y), txt, font=fnt, fill=color, anchor="mm")


def wrap(d, txt, fnt, width):
    words, lines, cur = txt.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=fnt) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def soft_shadow(base, x, y, w, h, r=26, blur=26, alpha=42):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    ld.rounded_rectangle([x + 8, y + 16, x + w + 8, y + h + 16], r, fill=(40, 34, 30, alpha))
    lay = lay.filter(ImageFilter.GaussianBlur(blur))
    base.paste(Image.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 0)), lay).convert("RGB"), (0, 0), lay)


def tile(base, path, x, y, tw, th, r=26, mat=18):
    soft_shadow(base, x, y, tw + mat * 2, th + mat * 2, r=r + 18)
    plate = Image.new("RGB", (tw + mat * 2, th + mat * 2), PAPER)
    ph = fit(path, tw, th)
    plate.paste(ph, (mat, mat))
    base.paste(plate, (x, y))


def page_title(d, kicker, title, sub=None):
    """Ivory-card header block, ~400px tall."""
    center(d, 120, spaced(kicker).upper(), sans(34, bold=True), GOLD)
    center(d, 218, title, serif(86), INK)
    rule(d, W // 2 - 130, 300, W // 2 + 130)
    if sub:
        center(d, 366, sub, sans(40), SOFT)
        return 470
    return 430


def brand_footer(d, note="NOVALITY STORE"):
    rule(d, 140, H - 150, W - 140, color=(205, 194, 170), width=3)
    center(d, H - 88, spaced(note), sans(30, bold=True), GOLD)
    d.text((140, H - 88), "© 2026 Novality Store", font=sans(24), fill=SOFT, anchor="lm")
    d.text((W - 140, H - 88), "instant download · us + uk terms", font=sans(24), fill=SOFT, anchor="rm")


def fullbleed(path):
    return fit(path, W, H)


def band(im, y0, y1, color, alpha=232):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    ld.rectangle([0, y0, W, y1], fill=color + (alpha,))
    im.paste(im.convert("RGBA").composite(im) if False else im, (0, 0))
    return Image.alpha_composite(im.convert("RGBA"), lay).convert("RGB")


# ---------------------------------------------------------------- generic slots
def s_cover(p, src):
    im = fullbleed(src["hero"])
    im = band(im, 0, 300, INK, 222)
    d = ImageDraw.Draw(im)
    center(d, 96, spaced(p["kicker"]).upper(), sans(34, bold=True), (233, 224, 200))
    center(d, 190, p["name"].upper(), serif(74), (255, 253, 246))
    rule(d, W // 2 - 120, 268, W // 2 + 120, GOLD)
    im = band(im, H - 290, H, EVERGREEN, 228)
    d = ImageDraw.Draw(im)
    center(d, H - 186, p["cover_line"], sans(42, bold=True), (255, 253, 246))
    center(d, H - 108, spaced("NOVALITY STORE"), serif(44), GOLD)
    return im


def s_scene(p, key, slotfile, heading, caption, top=True, color=None):
    im = fullbleed(p["src"][key])
    col = color or (INK if top else EVERGREEN)
    if top:
        im = band(im, 0, 230, col, 222)
    else:
        im = band(im, H - 230, H, col, 226)
    d = ImageDraw.Draw(im)
    yy = 96 if top else H - 134
    center(d, yy, heading, serif(62), (255, 253, 246))
    if caption:
        for i, ln in enumerate(wrap(d, caption, sans(34), W - 520)[:2]):
            center(d, yy + 78 + i * 48, ln, sans(34), (233, 224, 200))
    return im


def s_trio(p, slotfile, title, items, note, kicker="(STYLED）"):
    im, d = card()
    y0 = page_title(d, p["kicker"], title, note)
    for i, (key, cap, sub) in enumerate(items):
        x = 170 + i * 700
        tile(im, p["src"][key], x, y0 + 60, 640, 760)
        center(d, y0 + 940, cap, serif(44), INK) if False else d.text((x + 338, y0 + 940), cap, font=serif(44), fill=INK, anchor="ma")
        d.text((x + 338, y0 + 1010), sub, font=sans(32), fill=SOFT, anchor="ma")
    brand_footer(d)
    return im


def s_info(p, slotfile, bullets_):
    im, d = card()
    y0 = page_title(d, p["kicker"], "What's inside", "one PDF · us and uk terms side by side in every round")
    f = sans(38)
    xx = 250
    y = y0 + 30
    d.ellipse([xx - 38, y + 8, xx - 14, y + 32], fill=GOLD)
    for head, rest in bullets_:
        lines = wrap(d, rest, f, W - 700)
        d.text((xx, y), head, font=sans(40, bold=True), fill=EVERGREEN)
        y += 62
        for ln in lines:
            d.text((xx + 40, y), ln, font=f, fill=INK)
            y += 52
        y += 34
        d.ellipse([xx - 38, y - 26, xx - 14, y - 2], fill=GOLD)
    brand_footer(d)
    return im


def s_sizes(p, slotfile, title, cols, rows, note):
    im, d = card()
    y0 = page_title(d, p["kicker"], title, note[0] if isinstance(note, tuple) else None)
    fy = y0 + 30
    d.rounded_rectangle([140, fy, W - 140, fy + 96], 18, fill=EVERGREEN)
    for cx, lab in cols:
        d.text((cx, fy + 48), lab, font=sans(34, bold=True), fill=(255, 253, 246), anchor="lm")
    fy += 128
    for i, row in enumerate(rows):
        d.rounded_rectangle([140, fy, W - 140, fy + 200], 18,
                            fill=(PAPER if i % 2 == 0 else MIST))
        vals, sub = row
        for (cx, _), v in zip(cols, vals):
            d.text((cx, fy + 62), v, font=(serif(48) if cx == cols[0][0] else sans(40)), fill=(CRANBERRY if cx == cols[0][0] else INK))
        if sub:
            d.text((cols[1][0], fy + 140), sub, font=sans(30), fill=SOFT)
        fy += 224
    txt = note[1] if isinstance(note, tuple) else note
    for i, ln in enumerate(wrap(d, txt, sans(34, bold=True), W - 640)[:2]):
        center(d, fy + 46 + i * 52, ln, sans(34, bold=True), CRANBERRY)
    brand_footer(d)
    return im


def s_peek(p, slotfile, rows, note):
    im, d = card()
    y0 = page_title(d, p["kicker"], "Peek inside", "actual dual-format rounds - us left, uk right")
    x0, x1 = 150, W - 150
    fy = y0 + 20
    d.rounded_rectangle([x0, fy, x1, fy + 96], 18, fill=INK)
    for cx, lab, c in [(190, "Rnd", GOLD), (360, "US TERMS", (255, 253, 246)), (1370, "UK TERMS", (255, 253, 246)), (2140, "STS", GOLD)]:
        d.text((cx, fy + 48), lab, font=sans(32, bold=True), fill=c, anchor="lm")
    fy += 130
    for i, (r, us, uk, n) in enumerate(rows):
        if i % 2 == 0:
            d.rounded_rectangle([x0, fy - 16, x1, fy + 118], 14, fill=PAPER)
        d.text((190, fy + 20), r, font=serif(40), fill=CRANBERRY)
        d.text((360, fy + 20), us, font=sans(31), fill=INK)
        d.text((1370, fy + 20), uk, font=sans(31), fill=INK)
        d.text((2140, fy + 24), f"({n})", font=sans(34, bold=True), fill=EVERGREEN)
        fy += 168
    for i, ln in enumerate(wrap(d, note, sans(34), W - 640)[:2]):
        center(d, fy + 44 + i * 52, ln, sans(34), SOFT)
    brand_footer(d)
    return im


def s_grid(p, slotfile, items, title="Pattern details", sub="everything at a glance"):
    im, d = card()
    y0 = page_title(d, p["kicker"], title, sub)
    gx, gy = 180, y0 + 40
    cw, ch_, gap = (W - 360 - 60) // 2, 172, 34
    for i, (k, v) in enumerate(items[:12]):
        x = gx + (i % 2) * (cw + 44)
        y = gy + (i // 2) * (ch_ + gap)
        d.rounded_rectangle([x, y, x + cw, y + ch_], 20, fill=PAPER, outline=(224, 217, 202), width=3)
        d.text((x + 36, y + 50), spaced(k).upper(), font=sans(26, bold=True), fill=GOLD)
        d.text((x + 36, y + 108), v, font=sans(36, bold=True), fill=INK)
    brand_footer(d)
    return im


def s_palette(p, slotfile, sets, note):
    im, d = card()
    y0 = page_title(d, p["kicker"], "Colour recipes", "amounts for every recipe are in the pattern")
    n = len(sets)
    tw = 620 if n == 3 else 720
    gap = (W - 280 - n * tw) // (n - 1)
    for i, (name, sw, desc) in enumerate(sets):
        x = 140 + i * (tw + gap)
        y0_ = y0 + 30
        d.rounded_rectangle([x, y0_, x + tw, y0_ + 700], 24, fill=PAPER, outline=(224, 217, 202), width=3)
        d.rounded_rectangle([x, y0_, x + tw, y0_ + 96], 24, fill=EVERGREEN)
        d.text((x + tw // 2, y0_ + 48), name, font=sans(36, bold=True), fill=(255, 253, 246), anchor="mm")
        sy = y0_ + 190
        off = (tw - (60 + 3 * 170 + 2 * 26)) // 2
        for j, c in enumerate(sw):
            d.ellipse([x + off + j * 196, sy, x + off + 170 + j * 196, sy + 170], fill=c, outline=(170, 162, 148), width=4)
        yy = y0_ + 430
        for ln in wrap(d, desc, sans(34), tw - 120):
            d.text((x + tw // 2, yy), ln, font=sans(34), fill=INK, anchor="ma")
            yy += 48
    yy2 = y0 + 800
    if p["src"].get("macro"):
        center(d, yy2, note, sans(36, bold=True), CRANBERRY)
    else:
        center(d, yy2, note, sans(36, bold=True), CRANBERRY)
    brand_footer(d)
    return im


def s_care(p, slotfile, items, extra):
    im, d = card()
    y0 = page_title(d, p["kicker"], "Caring for it", "handmade pieces earn decades of gentle care")
    f = sans(38)
    y = y0 + 10
    for head, rest in items:
        d.text((240, y), head, font=sans(40, bold=True), fill=EVERGREEN)
        for j, ln in enumerate(wrap(d, rest, f, W - 940)):
            d.text((560, y + (0 if j == 0 else 44) + 0), ln, font=f, fill=INK)
            if j:
                y += 44
        y += 96
    center(d, y + 30, extra, sans(34, bold=True), GOLD)
    brand_footer(d)
    return im


def s_faq(p, slotfile, qa):
    im, d = card()
    y0 = page_title(d, p["kicker"], "Quick answers", "asked before you press buy")
    y = y0 - 10
    for q, a in qa:
        d.rounded_rectangle([160, y, W - 160, y + 172], 18, fill=PAPER, outline=(224, 217, 202), width=3)
        d.text((200, y + 56), q, font=sans(34, bold=True), fill=CRANBERRY)
        for j, ln in enumerate(wrap(d, a, sans(30), W - 520)[:2]):
            d.text((200, y + 104 + j * 42), ln, font=sans(30), fill=INK)
        y += 196
    brand_footer(d, "pattern help answered within 48 hours")
    return im


def s_thanks(p, slotfile, tag):
    im, d = card()
    page_title(d, p["kicker"], "Thank you", "for crocheting with novality")
    tile(im, p["src"]["hero"], 700, 470, 1000, 700)
    center(d, 1350, f"Share your make - tag #NovalityStore and {tag}", sans(40, bold=True), INK)
    center(d, 1432, "every question you send is answered by a real person - by me.", sans(34), SOFT)
    brand_footer(d)
    return im


def s_why(p, slotfile, tiles3, items):
    im, d = card()
    y0 = page_title(d, p["kicker"], "Why Novality", "independent design · honest patterns")
    for i, (key, cap) in enumerate(tiles3):
        x = 170 + i * 700
        tile(im, p["src"][key], x, y0 + 30, 640, 560)
        d.text((x + 338, y0 + 700), cap, font=serif(36), fill=INK, anchor="ma")
    y = y0 + 810
    for head, rest in items:
        d.ellipse([240, y + 12, 264, y + 36], fill=GOLD)
        d.text((300, y), head, font=sans(38, bold=True), fill=EVERGREEN)
        for ln in wrap(d, rest, sans(34), W - 880)[:2]:
            d.text((560, y + 44), ln, font=sans(34), fill=INK)
            y += 44
        y += 96
    brand_footer(d)
    return im


def gift_card(p, slotfile, heading, items, strip_line):
    im, d = card()
    y0 = page_title(d, p["kicker"], heading, None)
    tile(im, p["src"]["life"], 140, y0 + 40, 920, 880)
    y = y0 + 90
    for head, rest in items:
        d.text((1160, y), head, font=sans(40, bold=True), fill=CRANBERRY)
        y += 58
        for ln in wrap(d, rest, sans(36), W - 1280):
            d.text((1160, y), ln, font=sans(36), fill=INK)
            y += 50
        y += 36
    d.text((1160, y + 20), strip_line, font=serif(44), fill=EVERGREEN)
    brand_footer(d)
    return im


# ----------------------------------------------------------------- data
P: dict[str, dict] = {}


# ============================================================== NS 14
def build_ns14(p):
    peek_rows = [
        ("R4", "ch 2, [dc 2, 2 dc] x 12, sl st", "ch 2, [tr 2, 2 tr] x 12, sl st", "48"),
        ("R5", "ch 2, [BO, dc 2, 2 dc] x 12, sl st", "ch 2, [BO, tr 2, 2 tr] x 12, sl st", "60"),
        ("R9", "ch 2, [dc 7, 2 dc] x 12, sl st", "ch 2, [tr 7, 2 tr] x 12, sl st", "108"),
        ("R14", "ch 2, [BO, dc 11, 2 dc] x 12, sl st", "ch 2, [BO, tr 11, 2 tr] x 12, sl st", "168"),
        ("Border", "[dc, skip 2, 5 dc, skip 2] around", "[tr, skip 2, 5 tr, skip 2] around", "-"),
    ]
    jobs = [
        ("01", "cover", s_cover(p, p["src"])),
        ("02", "wip", s_scene(p, "wip", None, "JUST THREE COLOURS & ONE HOOK",
                              "cream, cranberry and forest green - classic heritage palette", top=True)),
        ("03", "sizes", s_trio(p, None, "Three sizes, one pattern",
            [("flat", "MINI", "46-53 cm across · stop after R14"),
             ("hero", "STANDARD", "74-84 cm across · stop after R23"),
             ("gift", "GRAND", "97-109 cm across · stop after R32")],
            "one 12-spoke ladder grows to each; the border math already divides")),
        ("04", "detail", s_scene(p, "macro", None, "FIRM, RAISED SNOWFLAKES",
                                 "5-dc bobble texture on a crisp dc field - the spokes are surface slip-stitch lines added at the end", top=False, color=CRANBERRY)),
        ("05", "info", s_info(p, None, [
            ("Instant download, dual formats", "every round written in both US and UK terms, side by side in one column - no second printout needed"),
            ("Stitch-mapped rounds", "each ladder round ends at exactly 12 x N stitches; the pattern prints consumed and produced counts so you can verify your tension as you grow"),
            ("Three measured checkpoints", "stop after R14, R23 or R32 and go straight to the border - the scallop repeat always sits on a multiple of 6"),
            ("Technique notes inside", "magic-ring join, 5-dc bobbles, scalloped edge and surface slip-stitch spokes each get a step-by-step explanation"),
            ("Three colour recipes", "Classic Pine, Frost & Berry and Monochrome Cream, each with generous yardage for all sizes"),
            ("Real support", "pattern questions answered personally, within 48 hours"),
        ])),
        ("06", "lifestyle", s_scene(p, "gift", None, "INSPIRE THE ROOM BEFORE THE TREE DOES",
                                     "the standard skirt under a modest fir holds the whole scene together", top=True, color=EVERGREEN)),
        ("07", "sizechart", s_sizes(p, None, "Measurements", 
            [(210, "SIZE"), (740, "STOP AFTER"), (1290, "FINISHED ACROSS")],
            [(["MINI", "ROUND 14", "46-53 cm / 18-21 in"], "168 stitches · 28 border scallops · tabletop and pencil trees"),
             (["STANDARD", "ROUND 23", "74-84 cm / 29-33 in"], "276 stitches · 46 border scallops · most 4-6 ft trees"),
             (["GRAND", "ROUND 32", "97-109 cm / 38-43 in"], "384 stitches · 64 border scallops · 7 ft+ showpiece trees")],
            ("gauge varies; check your treble/dc tension early", "always measure the centre hole against your own tree stand after 3 rounds")),
        ),
        ("08", "preview", s_peek(p, None, peek_rows,
            "+ abbreviations key, gauge note, three checkpoint guides, technique notes and troubleshooting")),
        ("09", "gift", gift_card(p, None, "Gift this & the tree wins", [
            ("Heirloom with logic", "the ladder guarantees a flat, full circle - buyers never guess which row to add"),
            ("Instant-download present", "gift the pattern with three skeins of luxury worsted for a maker's favourite box"),
            ("Market-ready finish", "sell the final skirt small-batch with the 'pattern by Novality Store' credit"),
        ], "the gift that keeps the tree company")),
        ("10", "why", s_why(p, None,
            [("hero", "proven stitch math"), ("macro", "tactile, honest texture"), ("wip", "beginner-traceable rounds")],
            [("Audited against the machine", "every ladder round re-derived - 12 x N, no exceptions - before publication"),
             ("Pictures you can trust", "the listing photos mirror what actually exits the rounds, not stocks"),
             ("Small-batch friendly", "finished skirts may be sold with credit to Novality Store"),
             ("Instant download", "us + uk terms in one PDF, printable on A4 or letter"),
            ])),
        ("11", "details", s_grid(p, None, [
            ("design code", "NS 14"), ("format", "PDF · us + uk terms"),
            ("level", "easy-intermediate"), ("time", "3-6 evenings"),
            ("hook", "5 mm (US H-8)"), ("yarn", "worsted / aran (#4)"),
            ("yardage", "3 skeins + 2 contrast"), ("construction", "one flat circle, zero seams"),
            ("sizes", "mini · standard · grand"), ("stitches", "ch · sl st · sc · dc · bobble"),
            ("repeat", "12-spoke ladder"), ("extras", "3 colour recipes + tips"),
        ])),
        ("12", "flat", s_scene(p, "flat", None, "THE FLORAL MANDALA THAT MAKES GIFTS LOOK BETTER",
                                "top edge to border lies perfectly flat when the counts are right - and they are", top=True)),
        ("13", "colourways", s_palette(p, None, [
            ("CLASSIC PINE", [(248, 246, 240), (168, 63, 55), (46, 75, 63)], "cream · cranberry · forest green - heritage red and green done softly"),
            ("FROST & BERRY", [(242, 240, 236), (138, 96, 118), (168, 178, 190)], "ice white with mulberry and silver fog - cooler, modern holiday"),
            ("MONOCHROME CREAM", [(247, 243, 233), (214, 202, 178), (168, 155, 133)], "three creams + oatmeal - all texture, goes with every tree"),
        ], "stitch counts never move with colour - swap the story without reading the pattern again")),
        ("14", "care", s_care(p, None, [
            ("Wash", "cool hand wash or gentle machine cycle in a mesh garment bag, mild wool-safe detergent"),
            ("Dry", "press water out in a towel, dry flat - reshape the scallops while damp"),
            ("Store", "roll around a cardboard tube rather than fold; tuck a lavender sachet inside"),
            ("Wool yarn", "cold hand wash only, keep away from radiators, reshape damp"),
            ("Revive", "hover a steam iron 2 cm above flattened bobbles watching them spring back"),
        ], "treated kindly, this skirt outlasts the tree stand")),
        ("15", "thanks", s_thanks(p, None, "#SnowflakeSkirt")),
    ]
    return jobs


_add = None


def add(code, name, kicker, srcnames, **kw):
    base = SRC / code.lower()
    src = {k: base / f"{code.lower()}_{srcnames[k]}.jpg" for k in srcnames}
    if "gift" in src and "life" not in src:
        src["life"] = src["gift"]
    p = {"code": code, "name": name, "kicker": kicker, "src": src, **kw}
    base.mkdir(parents=True, exist_ok=True)
    P[code] = p
    return p


# ============================================================== NS 15
def build_ns15(p):
    peek_rows = [
        ("Tube", "MR 6 sc; inc (12); sc spiral ~150 rnds", "MR 6 dc; inc (12); dc spiral ~150 rnds", "12/rd"),
        ("Skirt R1", "ch 1, 2 sc in each st, sl st", "ch 1, 2 dc in each st, sl st", "24"),
        ("Petal", "[ch 4, 3 tr, ch 4, sl st] same st, then x5", "[ch 4, 3 dtr, ch 4, sl st] same st, then x5", "6"),
        ("Bow tail", "ch 15, sc in 2nd ch from hook, across", "ch 15, dc in 2nd ch from hook, across", "14"),
        ("Snowflake", "into 6 ch-5 spaces: 6 arms", "into 6 ch-5 spaces: 6 arms", "6"),
    ]
    jobs = [
        ("01", "cover", s_cover(p, p["src"])),
        ("02", "looks", s_scene(p, "variants", None, "ONE WREATH, THREE MOODS",
                                "poinsettia for december · snowflake for january · bow for whenever the mood wins", top=True, color=CRANBERRY)),
        ("03", "detail", s_scene(p, "macro", None, "A TUBE THAT FORGIVES",
                                 "stuff as you go - the plush 12-stitch spiral needs no wire frame", top=False)),
        ("04", "lifestyle", s_scene(p, "fire", None, "JANUARY MODE",
                                    "the same wreath, snowflake swapped in - 10 seconds of loop ties", top=True, color=EVERGREEN)),
        ("05", "info", s_info(p, None, [
            ("One pattern, three looks", "one stuffed tube wreath plus poinsettia, snowflake and holiday bow centerpieces - swapable in seconds"),
            ("Dual-format rounds", "us and uk terms in one column for every row; one shared stitch count"),
            ("Five sub-pieces counted", "tube, skirt, poinsettia, snowflake, bow - every piece stitch-counted and cross-checked before release"),
            ("10-second swap system", "built-in loop ties plus optional safety-pin backs - restyle for every week of winter"),
            ("Bonus mini wreath", "16-19 cm door-and-garland version with its hanging loop printed free inside"),
            ("Size table included", "tube lengths for 10, 12 and 14 inch wreaths - the geometry is done for you"),
        ])),
        ("06", "wip", s_scene(p, "wip", None, "STUFF AS YOU GO",
                              "one long spiral of single crochet; the tube fills itself with shape", top=True)),
        ("07", "sizechart", s_sizes(p, None, "Three standard wreaths",
            [(210, "SIZE"), (740, "FINISHED ACROSS"), (1380, "TUBE LENGTH")],
            [(["MINI", "16-19 cm", "~35-40 cm tube"], "doors, garlands, table settings"),
             (["STANDARD", "25-30 cm", "~80-95 cm tube"], "the classic front-door wreath"),
             (["STATEMENT", "35-42 cm", "~110-130 cm tube"], "mantel drama and shop windows")],
            ("size is controlled by your tube length, not the pattern", "the pattern prints finished diameter per round at gauge - choose your length before you join")),
        ),
        ("08", "preview", s_peek(p, None, peek_rows,
            "+ full size table, assembly walk-through, care notes and troubleshooting")),
        ("09", "gift", gift_card(p, None, "The wreath that keeps giving", [
            ("Three gifts in one box", "wreath + poinsettia + snowflake + bow - beautifully giftable"),
            ("Ships flat", "the stuffed tube squishes for postage then springs right back"),
            ("Sell the set", "boutique small-batch runs welcome with designer credit"),
        ], "restyled all season - a piece worth keeping out")),
        ("10", "why", s_why(p, None,
            [("variants", "one pattern, three looks"), ("macro", "plush hand-made tube"), ("hero", "porch-ready result")],
            [("Counted before christmas", "consumption and production checks across all five sub-pieces"),
             ("Photos that mirror", "the listing images show what comes out of the actual rounds"),
             ("Questions answered fast", "pattern help within 48 hours - real person, no bots"),
             ("Small-batch friendly", "sell finished wreaths with credit to Novality Store"),
            ])),
        ("11", "details", s_grid(p, None, [
            ("design code", "NS 15"), ("format", "PDF · us + uk terms"),
            ("level", "confident beginner"), ("time", "weekend + 3 evenings"),
            ("hook", "4 mm (US G-6)"), ("yarn", "DK / light worsted"),
            ("yardage", "green 80 g · red 25 g · white 15 g"), ("construction", "spiral tube + 4 flat pieces"),
            ("sizes", "mini · standard · statement"), ("attach", "loop tie-on or safety pin"),
            ("bonus", "mini wreath included"), ("stitches", "ch · sl st · sc · dc · tr · puff"),
        ])),
        ("12", "flat", s_scene(p, "variants", None, "THE WHOLE SYMPHONY AT ONCE",
                                "wreath + poinsettia + snowflake + bow - everything the pattern covers, laid in formation", top=False, color=CRANBERRY)),
        ("13", "colourways", s_palette(p, None, [
            ("TRADITIONAL", [(46, 75, 63), (168, 63, 55), (248, 246, 240)], "forest green · holly red · creamy white - the front-door classic"),
            ("WINTER FOG", [(168, 178, 190), (248, 246, 240), (138, 96, 118)], "silver fog · snow white · mulberry - quiet scandi winter"),
        ], "any palette works - the tube geometry never changes")),
        ("14", "care", s_care(p, None, [
            ("Dust", "a 10-second blast of cool hair-dryer air each year"),
            ("Spot clean", "damp cloth, cool water only - hot water felts wool"),
            ("Store", "hang or roll; never crush under boxes - the tube dents"),
            ("Decorations", "detach and tissue-wrap the snowflake for storage"),
            ("Revive", "hover-steam puffs flattened bobbles back to shape"),
        ], "a decade of decembers with gentle care")),
        ("15", "thanks", s_thanks(p, None, "#3in1Wreath")),
    ]
    return jobs


add("NS14", "Bobble Snowflake Christmas Tree Skirt", "crochet pattern · NS 14",
    {"hero": "hero", "flat": "flat", "macro": "macro", "wip": "wip", "gift": "gift"},
    cover_line="3 sizes in one ladder · scalloped red & green border · 12-spoke snowflake",
    build=build_ns14)


# ============================================================== NS 11
def build_ns11(p):
    peek_rows = [
        ("R1-4", "MR 6 sc; inc ladders to 24", "MR 6 dc; inc ladders to 24", "24"),
        ("R5", "14 sc, 4 hdc, 6 sc - face zone", "14 dc, 4 htr, 6 dc - face zone", "24"),
        ("Nose", "5-dc bobble between face sts", "5-tr bobble between face sts", "24"),
        ("Beard", "ch 8 loop into fn-sts, x12", "ch 8 loop into fn-sts, x12", "-"),
        ("Hat", "sc rnds + 3 inc kinks, 12 slouch rnds", "dc rnds + 3 inc kinks, 12 slouch rnds", "-"),
    ]
    jobs = [
        ("01", "cover", s_cover(p, p["src"])),
        ("02", "wip", s_scene(p, "wip", None, "NO INSTRUCTION LEFT TO GUESS",
                              "every colour change is counted; the beard loop is engineered, not draped", top=True)),
        ("03", "trio", s_trio(p, None, "Three colours, one gnome",
            [("trio", "HOLLY RED", "classic nordic - the bestseller"),
             ("life", "FOREST PINE", "deep woodland tones"),
             ("hero", "IVORY GOLD", "quiet luxury for mantle whites")],
            "yardage for all three recipes is in the pattern")),
        ("04", "detail", s_scene(p, "macro", None, "TEXTURE YOU CAN FEEL THROUGH THE SCREEN",
                                 "dense amigurumi fabric plus a looped beard - zero sewing, all attitude", top=False, color=CRANBERRY)),
        ("05", "info", s_info(p, None, [
            ("Genuinely no-sew", "body, beard, face, nose and hat grow from one continuous tube - one yarn end to hide"),
            ("Dual-format rounds", "us and uk terms side by side in one column; one shared stitch count"),
            ("Stitch-checked ladders", "each increase/decrease round is re-derived and printed; your stitch count always checks out"),
            ("Nose engineered in", "a 5-dc bobble placed on the face round - no assembly, no wobble"),
            ("Three colour recipes", "holly red, forest pine, ivory gold - all with exact yardage"),
            ("Real support", "questions answered personally within 48 hours"),
        ])),
        ("06", "lifestyle", s_scene(p, "life", None, "EVERY MANTEL NEEDS ONE",
                                    "fifteen centimetres of pure holiday attitude that sells itself at markets", top=True, color=EVERGREEN)),
        ("07", "sizechart", s_sizes(p, None, "Built to fill a shelf",
            [(210, "VARIANT"), (740, "FINISHED HEIGHT"), (1380, "YARN LOAD")],
            [(["STANDARD", "15 cm / 6 in", "~40 g total"], "the pattern size - DK or light worsted"),
             (["MINI", "11-12 cm", "~25 g"], "worsted with 3.5 mm hook - tote-friendly"),
             (["UPGRADE", "18-20 cm", "~70 g"], "a wreath-sized showpiece in chunky yarn")],
            ("size scales with yarn and hook, not the pattern", "the 24-stitch body round is the same - change the yarn, change the height")),
        ),
        ("08", "preview", s_peek(p, None, peek_rows,
            "+ beard loop engineering, nose placement round, hat slouch section and troubleshooting")),
        ("09", "gift", gift_card(p, None, "The safest handmade gift", [
            ("Sews itself", "nothing to hide - one continuous build means no visible seams to worry about"),
            ("Cute at both sizes", "mini for stockings, standard for mantels"),
            ("Sell at markets", "gnomes move fast on stall tables - small-batch credit included"),
        ], "the gnomes sell themselves")),
        ("10", "why", s_why(p, None,
            [("hero", "no-sew, engineered in"), ("macro", "dense, tactile fabric"), ("trio", "three moods, one build")],
            [("Really no sewing", "the gloves-off spirit is real - the whole guy is one tube"),
             ("Rounds you can audit", "ladder math printed next to every round - tension and count both tamed"),
             ("Support by the maker", "48-hour pattern questions answered by a human"),
             ("Instant download", "us + uk terms, one PDF"),
            ])),
        ("11", "details", s_grid(p, None, [
            ("design code", "NS 11"), ("format", "PDF · us + uk terms"),
            ("level", "beginner+"), ("time", "1.5-2.5 hours"),
            ("hook", "4 mm (US G-6)"), ("yarn", "DK / light worsted"),
            ("yardage", "≈ 40 g total"), ("construction", "ONE piece - zero sewing"),
            ("height", "15 cm standard"), ("stitches", "ch · sl st · sc · inc · dec · bobble"),
            ("finish", "set washer eyes optional"), ("bonus", "3 hat colour recipes"),
        ])),
        ("12", "hero2", s_scene(p, "hero", None, "THE NO-SEW GNOME THAT LIVES ON EVERYONE'S MANTEL",
                                "body, beard, face, hat - one continuous spiral from base to pom", top=True)),
        ("13", "colourways", s_palette(p, None, [
            ("HOLLY RED", [(168, 63, 55), (244, 238, 226), (240, 220, 190)], "cranberry hat · cream beard · warm earth nose - the classic"),
            ("FOREST PINE", [(46, 75, 63), (234, 232, 222), (176, 150, 106)], "deep green hat · frost beard · tan nose - the calm nordic"),
            ("IVORY GOLD", [(198, 172, 120), (248, 247, 242), (140, 130, 110)], "antique gold hat · ivory beard · slate nose - quiet luxury"),
        ], "same pattern, any mood - the colour-change rounds stay exactly where they are")),
        ("14", "care", s_care(p, None, [
            ("Display", "indoors only - sunshine will eventually fade the hat"),
            ("Dust", "cool hair-dryer air or a soft brush, gentle over the beard loops"),
            ("Spot clean", "damp cloth and cool water; never soak the nose area"),
            ("Store", "in a box with space - the beard likes its shape"),
            ("Revive", "a fingertip of steam (never touch) fluffs flattened beard loops"),
        ], "takes seconds to dust, lasts years")),
        ("15", "thanks", s_thanks(p, None, "#NoSewGnome")),
    ]
    return jobs


# ============================================================== NS 12
def build_ns12(p):
    peek_rows = [
        ("R1-6", "tip spiral: 6 → 48 by 7 tiers", "tip spiral: 6 → 48 by 7 tiers", "48"),
        ("R7", "bobble row every few sc", "bobble row every few tr", "48"),
        ("R8-26", "dec to plateau, repeat 7 bobble tiers", "dec to plateau, repeat 7 bobble tiers", "48"),
        ("Trunk", "last 6 rnds straight, stuff", "last 6 rnds straight, stuff", "18"),
        ("Finish", "ch-amber loop at crown", "ch-amber loop at crown", "-"),
    ]
    jobs = [
        ("01", "cover", s_cover(p, p["src"])),
        ("02", "wip", s_scene(p, "wip", None, "BOBBLES THAT ACTUALLY BUBBLE",
                              "unfinished bobbles pass the crochet hook test: firm, even, satisfying", top=True)),
        ("03", "trio", s_trio(p, None, "Two heights, two moods",
            [("trio", "GRAND FIR", "28 cm bobble statement"),
             ("hero", "CLASSIC PINE", "18 cm table topper"),
             ("life", "PLACE SETTING", "fiction-scaled for the table")],
            "scaled by round count: the pattern flags the pivot rounds")),
        ("04", "detail", s_scene(p, "macro", None, "IT'S NOT STUFFED - IT'S STITCHED",
                                 "dense bobble rows hold the cone sonically solid; stiffness comes from structure", top=False, color=EVERGREEN)),
        ("05", "info", s_info(p, None, [
            ("One stimulus-cone build", "tip to trunk in one continuous spiral - no seaming, no finishing seamstress work"),
            ("Bobble rounds taught", "the 4-dc incomplete-bobble technique with the hook-count trick"),
            ("Stitch-checked tiers", "every tier's consumption and production printed beside the round - scale anxiety gone"),
            ("Two heights included", "classic 18 cm table tree plus pivot markers for the 28 cm grand statement"),
            ("Dual-format PDF", "us and uk terms in one column, single stitch count"),
            ("Real support", "pattern questions answered personally within 48 hours"),
        ])),
        ("06", "lifestyle", s_scene(p, "life", None, "CENTREPIECE, NO WRAPPING REQUIRED",
                                    "two trees, two heights and dinner flowers itself", top=True, color=EVERGREEN)),
        ("07", "sizechart", s_sizes(p, None, "Two heights, one ladder",
            [(210, "HEIGHT"), (740, "FINAL ROUND"), (1380, "APPROX LOAD")],
            [(["CLASSIC", "stop after tier 7", "≈100-120 g"], "18 cm - the place-setting classic"),
             (["GRAND", "continue to tier 9", "≈180-220 g"], "28 cm - the mantel statement"),
             (["ORNAMENT", "stop at tier 4", "≈35-45 g"], "10 cm - tree-topper-sized minis")],
            ("both sizes share every ladder count", "the pattern prints the tier table - choose your station, stop counting where it says STOP")),
        ),
        ("08", "preview", s_peek(p, None, peek_rows,
            "+ bobble technique card, tier pivot table, stuffing guide and troubleshooting")),
        ("09", "gift", gift_card(p, None, "A tree people keep out", [
            ("Never wilts", "unlike the spruce outside, this one stays perfect all year"),
            ("Market favourite", "bobbles sell - small-batch runs welcome with credit"),
            ("Gift once, use for decades", "premium wool and structure make it heirloom grade"),
        ], "greenery that outlives the season")),
        ("10", "why", s_why(p, None,
            [("hero", "self-standing, no wires"), ("macro", "bobblefic texture"), ("trio", "two heights, one ladder")],
            [("Cone, not cone-shaped compromise", "the flat ladder gives a true conical profile"),
             ("Audited ladder", "tier-by-tier math re-derived before publication"),
             ("Real human support", "48-hour answers, maker's knowledge"),
             ("Instant download", "us + uk terms in one PDF"),
            ])),
        ("11", "details", s_grid(p, None, [
            ("design code", "NS 12"), ("format", "PDF · us + uk terms"),
            ("level", "easy"), ("time", "2-3 hours"),
            ("hook", "4 mm (US G-6)"), ("yarn", "DK / light worsted"),
            ("yardage", "≈100-120 g"), ("construction", "one continuous spiral"),
            ("heights", "classic 18 · grand 28 cm"), ("stitches", "ch · sl st · sc · dec · bobble"),
            ("finish", "no seaming"), ("bonus", "tier pivot table"),
        ])),
        ("12", "hero2", s_scene(p, "hero", None, "THE TREE WHOSE BOBBLES MAKE OTHER TREES JEALOUS",
                                "spiral tip, seven tiers of bobble-weight, straight-trunk finish", top=True)),
        ("13", "colourways", s_palette(p, None, [
            ("FOREST PINE", [(46, 75, 63), (58, 94, 76), (34, 56, 47)], "deep forest greens, lighter tips - woodsy classic"),
            ("WINTER FOG", [(188, 194, 200), (238, 240, 242), (160, 148, 168)], "silver fog with white tips - scandi minimal"),
            ("GOLDEN HOUR", [(188, 146, 92), (214, 180, 126), (244, 232, 204)], "warm amber and honey - the hostess gift"),
        ], "the tier table doesn't move with colour - just swap the skein")),
        ("14", "care", s_care(p, None, [
            ("Dust", "cool hair-dryer puff, then reshape any flattened bobbles by hand"),
            ("Spot clean", "damp cloth with cold water, minimal soap, don't twist"),
            ("Store", "away from heaters; wrap loosely in tissue, never stack"),
            ("Revive", "hover a steam iron over tired bobbles - they puff right back"),
            ("Storage tip", "store standing upright in a box with the tip free"),
        ], "the bobbles last decades with simple care")),
        ("15", "thanks", s_thanks(p, None, "#BobbleTree")),
    ]
    return jobs


add("NS15", "Interchangeable Christmas Wreath", "crochet pattern · NS 15",
    {"hero": "hero", "variants": "variants", "fire": "fire", "macro": "macro",
     "wip": "wip", "gift": "hero", "life": "variants", "three": "variants"},
    cover_line="one plush wreath · three swappable centrepieces · bonus mini",
    build=build_ns15)


# ============================================================== NS 13
def build_ns13(p):
    peek_rows = [
        ("Bauble R1-5", "MR 6 sc, inc ladder to 30", "MR 6 dc, inc ladder to 30", "30"),
        ("Bauble R12", "dec x6 ladder to 6, stuff", "dec x6 ladder to 6, stuff", "6"),
        ("Star", "centre ring + 5 fan points, 2 rnds", "centre ring + 5 fan points, 2 rnds", "-"),
        ("Snowflake", "12 anchors → 6 ch-5 spaces → 6 arms", "12 anchors → 6 ch-5 spaces → 6 arms", "6"),
        ("Hanger", "ch 14 loop, join, FO", "ch 14 loop, join, FO", "-"),
    ]
    jobs = [
        ("01", "cover", s_cover(p, p["src"])),
        ("02", "wip", s_scene(p, "wip", None, "SCRAP-BUSTERS WITH STRUCTURE",
                              "five to fifteen grams each - your leftover sport yarn is about to pay its way", top=True)),
        ("03", "trio", s_trio(p, None, "Three ornaments, one ladder",
            [("trio", "BAUBLE + STAR + SNOWFLAKE", "the full set in one PDF"),
             ("hero", "TREE-READY", "thin ribbon loops built in"),
             ("macro", "BLOCKED CRISP", "picot points that stay stiff")],
            "each ornament is independent - start with the bauble, branch out")),
        ("04", "detail", s_scene(p, "macro", None, "LACE THAT HOLDS ITS POINTS",
                                 "the snowflake arms are anchored twice and blocked once - no floppy corners", top=False, color=CRANBERRY)),
        ("05", "info", s_info(p, None, [
            ("Three patterns in one PDF", "round bauble, flat five-point star, lace six-armed snowflake"),
            ("Closet-scale yarn use", "5-15 g per ornament; the set is your leftover-yarn win"),
            ("Stitch ladders shown", "every increase/decrease round with produced counts - tension-friendly"),
            ("Blocking walk-through", "post-wash pinning for the star and snowflake, step by step"),
            ("Dual-format rounds", "us and uk terms side by side in one column, one shared count"),
            ("Real support", "pattern questions answered personally within 48 hours"),
        ])),
        ("06", "lifestyle", s_scene(p, "life", None, "ELEGANT ON THE BRANCH",
                                    "the white stars catch the fairy lights; the reds warm them up", top=True, color=EVERGREEN)),
        ("07", "sizechart", s_sizes(p, None, "Finished dimensions",
            [(210, "ORNAMENT"), (740, "FINISHED SIZE"), (1380, "YARN LOAD")],
            [(["BAUBLE", "≈3.5-4 cm across", "≈8-12 g"], "stuffed sphere, 30→6 ladder"),
             (["STAR", "≈9 cm wide", "≈5-8 g"], "flat, two rounds, five fans"),
             (["SNOWFLAKE", "≈10 cm wide", "≈5-7 g"], "lace, six anchor points, six arms")],
            ("scale freely with hook size", "larger yarn + hook grows them proportionally - count stays the same")),
        ),
        ("08", "preview", s_peek(p, None, peek_rows,
            "+ blocking board walk-through and troubleshooting for every ornament")),
        ("09", "gift", gift_card(p, None, "Hangable, giftable, sellable", [
            ("Gift tags included", "print-ready minis for tucking ornaments into packages"),
            ("Great stocking filler", "small size, instant delight"),
            ("Fast sellers", "bundle sets perform at holiday markets - credit included"),
        ], "the set that decorates a dozen trees")),
        ("10", "why", s_why(p, None,
            [("hero", "three types, one purchase"), ("macro", "lace that behaves"), ("trio", "set, styled and counted")],
            [("Counted before christmas", "bauble ladder, star fan math and snowflake 12→6 derivation all reconciled"),
             ("Pictures you can trust", "the listing shows what the pattern actually outputs"),
             ("Real human support", "48-hour answers from the maker"),
             ("Instant download", "us + uk terms, one PDF"),
            ])),
        ("11", "details", s_grid(p, None, [
            ("design code", "NS 13"), ("format", "PDF · us + uk terms"),
            ("level", "beginner"), ("time", "45-75 min each"),
            ("hook", "3 mm (us C-2)"), ("yarn", "sport / fingering"),
            ("yardage", "5-15 g each"), ("set", "bauble · star · snowflake"),
            ("sizes", "3.5-10 cm"), ("stitches", "ch · sl st · sc · inc · dec · fans"),
            ("finish", "loop hanger built in"), ("bonus", "printable gift tags"),
        ])),
        ("12", "hero2", s_scene(p, "hero", None, "THE ORNAMENT SET YOUR TREE WAS MISSING",
                                "bauble, star, snowflake - balanced, elegant, and quick", top=True)),
        ("13", "colourways", s_palette(p, None, [
            ("HERITAGE", [(168, 63, 55), (244, 238, 226), (46, 75, 63)], "holly red · cream · pine green - the classic trio"),
            ("FROST", [(188, 194, 200), (244, 246, 248), (120, 148, 160)], "silver fog · white · dusty blue - winter pastels"),
            ("GOLDEN HOUR", [(188, 146, 92), (244, 238, 226), (140, 110, 70)], "amber, cream, copper - warm handmade luxe"),
        ], "grab any palette - the counts are identical")),
        ("14", "care", s_care(p, None, [
            ("Wash", "hand wash cool, mild detergent - only the bauble can take a dip"),
            ("Dry flat", "lay on a towel; reshape the star and snowflake points while damp"),
            ("Store", "flat in a box with tissue; the snowflake likes a divider card"),
            ("Block yearly", "re-pin the lace points each season for crisp arms"),
            ("Handle loops", "hang by the loop, never by the lace arms"),
        ], "gentle care keeps the lace crisp for decades")),
        ("15", "thanks", s_thanks(p, None, "#NovalityOrnaments")),
    ]
    return jobs


add("NS11", "No-Sew Christmas Gnome", "crochet pattern · NS 11",
    {"hero": "hero", "trio": "trio", "macro": "macro", "life": "life", "wip": "wip",
     "gift": "life", "flat": "trio", "three": "trio"},
    cover_line="body · beard · face · hat in one piece · zero sewing",
    build=build_ns11)


add("NS12", "Bobble Christmas Tree", "crochet pattern · NS 12",
    {"hero": "hero", "trio": "trio", "macro": "macro", "life": "life", "wip": "wip",
     "gift": "life", "flat": "trio", "three": "trio"},
    cover_line="bobble-stitch tiers · self-standing · two heights included",
    build=build_ns12)


add("NS13", "Christmas Ornament Bundle", "crochet pattern · NS 13",
    {"hero": "hero", "trio": "trio", "macro": "macro", "life": "life", "wip": "wip",
     "gift": "life", "flat": "trio", "three": "trio"},
    cover_line="bauble · star · snowflake - three lace-weight ornaments in one PDF",
    build=build_ns13)


OUTNAME = "{code}_{nn}_{label}.jpg"


def build(code):
    p = P[code]
    outdir = ROOT / code
    outdir.mkdir(parents=True, exist_ok=True)
    jobs = p["build"](p)
    for nn, label, im in jobs:
        f = outdir / OUTNAME.format(code=code, nn=nn, label=label)
        im.save(f, quality=92, subsampling=0)
        print("wrote", f)


def main(*codes):
    for c in (codes or P):
        build(c)


if __name__ == "__main__":
    import sys
    main(*sys.argv[1:])
