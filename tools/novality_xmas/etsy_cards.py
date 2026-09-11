"""Compose the 15-slot Etsy image stacks for NS 14 & NS 15, plus the
11-15 extension slots for NS 11/12/13. 2400x1800, brand-styled cards over
the AI source photos in final_patterns/christmas/etsy/src14_*/src15_*.
"""
from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ETSY = Path("final_patterns/christmas/etsy")
W, H = 2400, 1800

CREAM = (251, 247, 239)
PAPER = (255, 253, 248)
CHARC = (51, 49, 59)
SAGE = (122, 139, 111)
RED = (176, 64, 55)
TERRA = (199, 123, 88)
INK = (70, 68, 80)
GOLD = (216, 163, 87)

FD = Path("/usr/share/fonts/truetype/dejavu")


def font(sz, bold=False, serif=True):
    nm = "DejaVuSerif-Bold" if bold else "DejaVuSerif"
    return ImageFont.truetype(str(FD / f"{nm}.ttf"), sz)


def font_sans(sz, bold=False):
    nm = "DejaVuSans-Bold" if bold else "DejaVuSans"
    return ImageFont.truetype(str(FD / f"{nm}.ttf"), sz)


def canvas(color=CREAM):
    im = Image.new("RGB", (W, H), color)
    return im, ImageDraw.Draw(im)


def text_center(d, y, txt, fnt, color=CHARC):
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


def photo(path, box_w, box_h, border=22):
    im = Image.open(path).convert("RGB")
    tw, th = box_w - border * 2, box_h - border * 2
    s = max(tw / im.width, th / im.height)
    im = im.resize((int(im.width * s + 1), int(im.height * s + 1)), Image.LANCZOS)
    im = im.crop((0, 0, tw, th)) if im.height > th else im.crop(((im.width - tw) // 2, 0, (im.width - tw) // 2 + tw, th))
    if im.width > tw or im.height > th:
        im = im.resize((tw, th), Image.LANCZOS)
    out = Image.new("RGB", (tw, th), (240, 235, 225))
    out.paste(im, ((tw - im.width) // 2, (th - im.height) // 2))
    return out


def tile(base, path, x, y, bw, bh, caption=None, cap_font=None):
    shadow = Image.new("RGB", (bw + 14, bh + 14), (214, 206, 190))
    base.paste(shadow, (x - 7, y + 8))
    inner = photo(path, bw, bh, border=20)
    base.paste(Image.new("RGB", (bw, bh), (255, 255, 255)), (x, y))
    base.paste(inner, (x + 20, y + 20))
    if caption:
        d = ImageDraw.Draw(base)
        fnt = cap_font or font_sans(30, bold=True)
        d.text((x + bw // 2, y + bh - 42), caption, font=fnt, fill=INK, anchor="mm")


def header(d, title, sub=None, color=CHARC):
    d.rectangle([0, 0, W, 250], fill=color)
    d.rectangle([0, 250, W, 266], fill=GOLD)
    text_center(d, 105 if sub else 125, title, font(76, bold=True), color=(255, 255, 255))
    if sub:
        text_center(d, 195, sub, font_sans(36), color=(233, 226, 210))


def footer(d, line="NOVALITY STORE  ·  handmade design, math-verified pattern"):
    d.rectangle([0, H - 90, W, H], fill=CHARC)
    text_center(d, H - 46, line, font_sans(30), color=(220, 214, 200))


def bullets(d, items, x, y, fnt, line_h, color=INK, max_w=1720, center=True):
    for head, rest in items:
        ln = wrap(d, head + (" - " + rest if rest else ""), fnt, max_w)
        for i, l in enumerate(ln):
            if center:
                d.text((x + max_w // 2, y), l, font=fnt, fill=color, anchor="ma")
            else:
                d.text((x, y), l, font=fnt, fill=color)
            y += line_h
        y += int(line_h * 0.35)
    return y


def chip(d, x, y, txt, fg=(255, 255, 255), bg=RED, fnt=None, pad=26):
    fnt = fnt or font_sans(30, bold=True)
    w_ = d.textlength(txt, font=fnt) + pad * 2
    d.rounded_rectangle([x, y, x + w_, y + 64], 32, fill=bg)
    d.text((x + w_ // 2, y + 32), txt, font=fnt, fill=fg, anchor="mm")
    return x + w_


def band(d, y, h, color, txt=None, fnt=None, fg=(255, 255, 255)):
    d.rectangle([0, y, W, y + h], fill=color)
    if txt:
        text_center(d, y + h // 2, txt, fnt or font(52, bold=True), color=fg)


def save(base, name):
    base.save(ETSY / name, quality=91)
    print("wrote", ETSY / name)


# ---------------------------------------------------------------- NS 14
SK = {
    "hero": ETSY / "src14_hero.jpg", "flat": ETSY / "src14_flat.jpg",
    "macro": ETSY / "src14_macro.jpg", "wip": ETSY / "src14_wip.jpg",
    "gift": ETSY / "src14_gift.jpg",
}


def ns14():
    # 01 cover
    im = photo(SK["hero"], W, H, border=0)
    base = im.copy(); d = ImageDraw.Draw(base, "RGBA")
    d.rectangle([0, 0, W, 330], fill=(51, 49, 59, 238))
    d.rectangle([0, 330, W, 344], fill=GOLD)
    text_center(d, 120, "BOBBLE SNOWFLAKE CHRISTMAS TREE SKIRT", font(84, bold=True), (255, 255, 255))
    text_center(d, 225, "Crochet Pattern  ·  Design Code NS 14  ·  US + UK terms in one file", font_sans(40), (233, 226, 210))
    d.rectangle([0, H - 210, W, H], fill=(51, 49, 59, 238))
    d.rectangle([0, H - 226, W, H - 210], fill=GOLD)
    text_center(d, H - 150, "3 sizes  ·  12-spoke bobble snowflake  ·  scalloped red & green border", font_sans(44, bold=True), (255, 255, 255))
    text_center(d, H - 78, "NOVALITY STORE", font(56, bold=True), GOLD)
    save(base, "NS14_01_cover.jpg")

    # 02 wip
    im = photo(SK["wip"], W, H, border=0)
    base = im.copy(); d = ImageDraw.Draw(base, "RGBA")
    d.rectangle([0, 0, W, 255], fill=(51, 49, 59, 235))
    d.rectangle([0, 255, W, 269], fill=GOLD)
    text_center(d, 105, "JUST A HOOK, WORSTED YARN & 3 COLORS", font(64, bold=True), (255, 255, 255))
    text_center(d, 188, "cream base  ·  red + green scallops  ·  basic stitches only: ch, sl st, sc, dc, bobbles", font_sans(36), (233, 226, 210))
    d.rectangle([0, H - 130, W, H], fill=(51, 49, 59, 235))
    text_center(d, H - 66, "worked flat in rounds from the tree trunk outward - no blocking panic, it wants to lie flat", font_sans(36), (255, 255, 255))
    save(base, "NS14_02_wip.jpg")

    # 03 three sizes (collage of 3 with labels from hero/flat crops)
    base, d = canvas(); header(d, "ONE PATTERN · THREE SIZES", "stop after R14 / R23 / R32 - the ladder does the math")
    for i, (p, cap) in enumerate([(SK["flat"], "MINI · 46-53 cm\nstop after R14"), (SK["hero"], "STANDARD · 74-84 cm\nstop after R23"), (SK["gift"], "LARGE · 97-109 cm\nstop after R32")]):
        x = 170 + i * 700
        tile(base, p, x, 430, 640, 830)
        for j, line in enumerate(cap.split("\n")):
            text_center(d, 1340 + j * 52, line, font_sans(40, bold=(j == 0)), INK) if False else d.text((x + 320, 1340 + j * 52), line, font=font_sans(40, bold=(j == 0)), fill=INK, anchor="ma")
    d.rectangle([0, 1550, W, 1640], fill=SAGE)
    text_center(d, 1595, "same 12-spoke circle grows to the size you need - 28 / 46 / 64 edge scallops", font_sans(40, bold=True), (255, 255, 255))
    footer(d)
    save(base, "NS14_03_sizes.jpg")

    # 04 detail macro
    im = photo(SK["macro"], W, H, border=0)
    base = im.copy(); d = ImageDraw.Draw(base, "RGBA")
    d.rectangle([0, H - 330, W, H], fill=(251, 247, 239, 242))
    d.rectangle([0, H - 330, W, H - 316], fill=RED)
    text_center(d, H - 235, "5-DC BOBBLES THAT POP LIKE SNOW ON A SPOTTED FIELD", font(58, bold=True), CHARC)
    text_center(d, H - 145, "bobble rounds every 3rd round  ·  surface spokes added last  ·  crisp scalloped edge, no sewing", font_sans(38), INK)
    text_center(d, H - 62, "novality store  ·  NS 14", font_sans(32, bold=True), RED)
    save(base, "NS14_04_detail.jpg")

    # 05 info / what's inside
    base, d = canvas(); header(d, "WHAT YOU GET", "instant download  ·  print-friendly")
    items = [
        ("12 pages, dual-format", "every round written in BOTH US and UK terms, side by side - one file, no separate versions"),
        ("Row-by-row sketch math", "each round is math-verified: the ladder always produces exactly 12 x N stitches"),
        ("3 size checkpoints", "stop after R14, R23 or R32; the border formula already divides"),
        ("Technique help inside", "bobbles, magic ring join, scallops, surface slip-stitch spokes - all explained"),
        ("Color recipes", "Classic Pine · Frost & Berry · Monochrome Cream palettes with yarn amounts"),
        ("Designer support", "questions welcome - I answer pattern help requests within 48 hours"),
    ]
    y = bullets(d, items, 80, 390, font_sans(40), 56)
    band(d, y + 40, 90, CHARC, "crochet level: easy-intermediate  ·  hook 5 mm  ·  worsted #4", fnt=font_sans(42, bold=True))
    footer(d)
    save(base, "NS14_05_info.jpg")

    # 06 lifestyle gift scene
    im = photo(SK["gift"], W, H, border=0)
    base = im.copy(); d = ImageDraw.Draw(base, "RGBA")
    d.rectangle([0, 0, W, 210], fill=(176, 64, 55, 235))
    text_center(d, 105, "THE TREE FINALLY LOOKS FINISHED", font(64, bold=True), (255, 255, 255))
    d.rectangle([0, H - 150, W, H], fill=(51, 49, 59, 235))
    text_center(d, H - 75, "the skirt guests notice first  ·  photographs beautifully with your tree", font_sans(38), (255, 255, 255))
    save(base, "NS14_06_lifestyle.jpg")

    # 07 size chart card
    base, d = canvas(); header(d, "SIZE CHART & TEST CHECKPOINTS", "measure twice, border once")
    rows = [("MINI", "stop after R14", "46-53 cm / 18-21 in", "168 sts · 28 scallops", "tabletop & pencil trees"),
            ("STANDARD", "stop after R23", "74-84 cm / 29-33 in", "276 sts · 46 scallops", "most 4-6 ft trees"),
            ("LARGE", "stop after R32", "97-109 cm / 38-43 in", "384 sts · 64 scallops", "7 ft+ & big trunks")]
    cols = [(170, "SIZE"), (640, "STOP AFTER"), (1150, "FINISHED ACROSS"), (1780, "BORDER MATH")]
    fy = 400
    d.rectangle([120, fy - 70, W - 120, fy], fill=SAGE)
    for cx, lab in cols:
        d.text((cx, fy - 35), lab, font=font_sans(38, bold=True), fill=(255, 255, 255), anchor="lm")
    fy += 40
    for i, (a, b, c, e, note) in enumerate(rows):
        d.rectangle([120, fy, W - 120, fy + 300], fill=(PAPER if i % 2 == 0 else (243, 238, 226)))
        d.text((170, fy + 60), a, font=font(54, bold=True), fill=RED)
        d.text((640, fy + 60), b, font=font_sans(42, bold=True), fill=CHARC)
        d.text((1150, fy + 60), c, font=font_sans(42), fill=CHARC)
        d.text((1780, fy + 60), e, font=font_sans(38), fill=INK)
        d.text((640, fy + 150), note, font=font_sans(36), fill=SAGE)
        d.text((1150, fy + 150), "(diameter is gauge-dependent; measure your swatch)", font=font_sans(28), fill=(140, 135, 125))
        fy += 320
    text_center(d, fy + 60, "tip: crochet 3 rounds, measure the center hole against YOUR tree stand before you commit", font_sans(38, bold=True), TERRA)
    footer(d)
    save(base, "NS14_07_sizechart.jpg")

    # 08 inside peek (draw sample dual rows)
    base, d = canvas()
    header(d, "PEEK INSIDE THE PATTERN", "actual dual-format round rows - US left, UK right")
    d.rectangle([120, 380, W - 120, 1450], fill=PAPER)
    d.rectangle([120, 380, W - 120, 470], fill=CHARC)
    d.text((160, 425), "Rnd", font=font_sans(34, bold=True), fill=GOLD, anchor="lm")
    d.text((330, 425), "US terms", font=font_sans(34, bold=True), fill=(255, 255, 255), anchor="lm")
    d.text((1320, 425), "UK terms", font=font_sans(34, bold=True), fill=(255, 255, 255), anchor="lm")
    d.text((2130, 425), "Sts", font=font_sans(34, bold=True), fill=GOLD, anchor="lm")
    sample = [("R4", "Ch 2, [dc in next 2 sts, 2 dc in next] x 12, sl st", "Ch 2, [tr in next 2 sts, 2 tr in next] x 12, sl st", "48"),
              ("R5", "Ch 2, [BO, dc in next 2, 2 dc in next] x 12, sl st", "Ch 2, [BO, tr in next 2, 2 tr in next] x 12, sl st", "60"),
              ("R9", "Ch 2, [dc in next 7 sts, 2 dc in next] x 12, sl st", "Ch 2, [tr in next 7 sts, 2 tr in next] x 12, sl st", "108"),
              ("R14", "Ch 2, [BO, dc in next 11, 2 dc in next] x 12, sl st", "Ch 2, [BO, tr in next 11, 2 tr in next] x 12, sl st", "168"),
              ("Border", "[sc, skip 2, 5 dc, skip 2] around, sl st, FO", "[dc, skip 2, 5 tr, skip 2] around, sl st, FO", "-")]
    fy = 560
    for i, (r, us, uk, n) in enumerate(sample):
        if r == "R9":
            d.rectangle([140, fy - 44, W - 140, fy + 118], fill=(247, 232, 229))
            d.text((150, fy + 92), "R9 verified: 12 x 9 = 108 - the pattern's stitch math is audit-checked", font=font_sans(30), fill=RED)
        d.text((160, fy), r, font=font(44, bold=True), fill=CHARC)
        d.text((330, fy), us, font=font_sans(32), fill=INK)
        d.text((1320, fy), uk, font=font_sans(32), fill=INK)
        d.text((2130, fy), f"({n})", font=font_sans(36, bold=True), fill=SAGE)
        d.line([140, fy + 66, W - 140, fy + 66], fill=(222, 215, 200), width=3)
        fy += 150
    text_center(d, 1520, "+ abbreviations key, gauge note, 3 size checkpoint pages, technique notes, troubleshooting table", font_sans(36), INK)
    footer(d)
    save(base, "NS14_08_preview.jpg")

    # 09 gift card
    base, d = canvas()
    band(d, 0, 250, RED, "MADE ONCE, HANDED DOWN", font(70, bold=True))
    d.rectangle([0, 250, W, 266], fill=GOLD)
    tile(base, SK["hero"], 140, 420, 950, 950)
    items = [
        ("A keepsake, not a decoration", "a crocheted skirt outlives plastic trees and trends"),
        ("Personalize it", "match the family palette - the math never changes"),
        ("Heirloom gift", "pair the pattern with 3 skeins of nice worsted for the perfect maker gift"),
        ("Photo-ready", "scalloped border frames every gift pile beautifully"),
    ]
    bullets(d, items, 1160, 480, font_sans(40), 56, center=False, max_w=1120)
    text_center(d, 1530, "then every December: 'I made that.'", font(52, bold=True), RED)
    footer(d)
    save(base, "NS14_09_gift.jpg")

    # 10 why card
    base, d = canvas()
    header(d, "WHY BUYERS CHOOSE NOVALITY", "independent design  ·  honest patterns")
    tiles = [(SK["flat"], "math-verified"), (SK["macro"], "clear texture"), (SK["wip"], "beginner-traced")]
    for i, (p, cap) in enumerate(tiles):
        tile(base, p, 170 + i * 700, 420, 640, 720, caption=cap)
    items = [
        ("Every round counted", "stitch math confirmed by an automated audit - not vibes"),
        ("Real support", "stuck on a bobble? message me; pattern help included"),
        ("Sell your makes", "finished skirts from this pattern may be sold with credit"),
        ("Instant download", "US + UK in one PDF - no waiting, no shipping"),
    ]
    y = bullets(d, items, 340, 1240, font_sans(38), 52)
    footer(d, "NOVALITY STORE  ·  thank you for supporting an indie designer")
    save(base, "NS14_10_why.jpg")

    # 11 pattern details card
    base, d = canvas()
    header(d, "PATTERN DETAILS", "everything at a glance")
    grid = [("DESIGN CODE", "NS 14"), ("FORMAT", "PDF · US + UK terms"), ("LEVEL", "easy-intermediate"),
            ("TIME", "3-6 evenings per size"), ("HOOK", "5 mm (US H-8)"), ("YARN", "worsted / aran #4"),
            ("AMOUNTS", "MC ~500g · red ~60g · green ~60g (large)"), ("CONSTRUCTION", "one flat circle, no seaming"),
            ("SIZES", "mini · standard · large"), ("CTC", "28-64 scallops, auto-divided"),
            ("STITCHES", "ch · sl st · sc · dc · 5-dc bobble"), ("EXTRAS", "3-color recipes + tips")]
    gx, gy = 170, 420
    for i, (k, v) in enumerate(grid):
        x = gx + (i % 2) * 1080
        y = gy + (i // 2) * 200
        d.rounded_rectangle([x, y, x + 1000, y + 160], 20, fill=PAPER, outline=(226, 219, 204), width=3)
        d.text((x + 40, y + 55), k, font=font_sans(30, bold=True), fill=RED)
        d.text((x + 40, y + 110), v, font=font_sans(38, bold=True), fill=CHARC)
    text_center(d, 1740 - 80, "worsted weight kept the ladder exact on a 5 mm hook - swatch and relax", font_sans(34, bold=True), TERRA)
    footer(d)
    save(base, "NS14_11_details.jpg")

    # 12 flat lay scene
    im = photo(SK["flat"], W, H, border=0)
    base = im.copy(); d = ImageDraw.Draw(base, "RGBA")
    d.rectangle([0, 0, W, 250], fill=(51, 49, 59, 235))
    d.rectangle([0, 250, W, 264], fill=GOLD)
    text_center(d, 105, "12 SPOKES · 12 SNOWFLAKE RAYS", font(66, bold=True), (255, 255, 255))
    text_center(d, 190, "slip-stitch surface spokes added after the border - no colorwork inside the rounds", font_sans(36), (233, 226, 210))
    d.rectangle([0, H - 120, W, H], fill=(176, 64, 55, 235))
    text_center(d, H - 60, "the circle that wants to lie flat: every round ends at exactly 12 x N stitches", font_sans(38, bold=True), (255, 255, 255))
    save(base, "NS14_12_flay.jpg")

    # 13 colorways
    base, d = canvas()
    header(d, "COLOR RECIPES", "3 tested palettes - amounts included in the pattern")
    palettes = [("CLASSIC PINE", [(246, 243, 236), (176, 64, 55), (60, 84, 56)], "cream · holly red · pine green"),
                ("FROST & BERRY", [(240, 242, 245), (120, 48, 62), (168, 178, 190)], "ice white · mulberry · silver fog"),
                ("MONOCHROME CREAM", [(246, 242, 232), (224, 214, 192), (180, 168, 145)], "three creams + oatmeal - all texture")]
    for i, (name, sw, desc) in enumerate(palettes):
        x = 170 + i * 700
        d.rounded_rectangle([x, 430, x + 640, 1240], 24, fill=PAPER, outline=(226, 219, 204), width=3)
        d.rounded_rectangle([x, 430, x + 640, 530], 24, fill=SAGE)
        d.text((x + 320, 480), name, font=font_sans(38, bold=True), fill=(255, 255, 255), anchor="mm")
        sy = 620
        for j, c in enumerate(sw):
            d.ellipse([x + 90 + j * 52, sy, x + 260 + j * 52, sy + 170], fill=c, outline=(160, 150, 135), width=4)
        yy = 860
        for l in wrap(d, desc, font_sans(36), 540):
            d.text((x + 320, yy), l, font=font_sans(36), fill=INK, anchor="ma")
            yy += 50
        d.text((x + 320, 1160), ["main + 2 contrast", "main + 2 contrast", "all one skein family"][i], font=font_sans(30, bold=True), fill=RED, anchor="ma")
    text_center(d, 1380, "skirt math never changes with color - go neutral once and re-gift forever", font_sans(40, bold=True), TERRA)
    footer(d)
    save(base, "NS14_13_colorways.jpg")

    # 14 care card
    base, d = canvas()
    header(d, "CARING FOR YOUR SKIRT", "handmade = happy decades with gentle care")
    items = [
        ("Wash", "cool hand wash or machine 'wool' cycle in a mesh bag, mild detergent"),
        ("Dry", "press water out in a towel, dry flat - it is a rug, not curtains; reshape the scallops"),
        ("Store", "roll, don't fold; tuck a lavender sachet inside the roll"),
        ("Wool caution", "if you used wool: cold only, no machine spin, dry away from radiators"),
        ("Acrylic bonus", "if you used acrylic worsted: fully machine washable on gentle"),
        ("Lifespan", "treated kindly, this skirt outlasts the tree stand you bought it for"),
    ]
    y = bullets(d, items, 340, 420, font_sans(42), 58)
    band(d, y + 40, 96, SAGE, "wash instructions also printed on the included care card", fnt=font_sans(40, bold=True))
    footer(d)
    save(base, "NS14_14_care.jpg")

    # 15 thank-you card
    base, d = canvas()
    band(d, 0, 250, CHARC, "THANK YOU FOR CROCHETING WITH NOVALITY", font(64, bold=True))
    d.rectangle([0, 250, W, 266], fill=GOLD)
    tile(base, SK["hero"], 700, 410, 1000, 760)
    text_center(d, 1300, "Share your skirt - tag #NovalityStore and #SnowflakeSkirt", font_sans(44, bold=True), CHARC)
    text_center(d, 1380, "I read every message; pattern help is always included", font_sans(40), INK)
    text_center(d, 1490, "5% to knitting-for-warmth charities each December", font_sans(36), SAGE)
    footer(d, "© 2026 Novality Store · pattern for personal use, small-batch selling welcome with credit")
    save(base, "NS14_15_thanks.jpg")


# ---------------------------------------------------------------- NS 15
WR = {
    "door": ETSY / "src15_door.jpg", "variants": ETSY / "src15_variants.jpg",
    "fire": ETSY / "src15_fireplace.jpg", "macro": ETSY / "src15_macro.jpg",
    "wip": ETSY / "src15_wip.jpg",
}


def ns15():
    # 01 cover
    im = photo(WR["door"], W, H, border=0)
    base = im.copy(); d = ImageDraw.Draw(base, "RGBA")
    d.rectangle([0, 0, W, 330], fill=(51, 49, 59, 240))
    d.rectangle([0, 330, W, 344], fill=GOLD)
    text_center(d, 115, "THE 3-IN-1 CHRISTMAS WREATH", font(88, bold=True), (255, 255, 255))
    text_center(d, 225, "Crochet Pattern  ·  Design Code NS 15  ·  US + UK terms in one file", font_sans(40), (233, 226, 210))
    d.rectangle([0, H - 210, W, H], fill=(51, 49, 59, 240))
    d.rectangle([0, H - 226, W, H - 210], fill=GOLD)
    text_center(d, H - 150, "one stuffed tube wreath  ·  3 swappable decorations  ·  poinsettia · snowflake · bow", font_sans(40, bold=True), (255, 255, 255))
    text_center(d, H - 78, "NOVALITY STORE", font(56, bold=True), GOLD)
    save(base, "NS15_01_cover.jpg")

    # 02 variants on linen - the key interchangeability image
    im = photo(WR["variants"], W, H, border=0)
    base = im.copy(); d = ImageDraw.Draw(base, "RGBA")
    d.rectangle([0, 0, W, 250], fill=(176, 64, 55, 240))
    text_center(d, 105, "1 WREATH · 3 LOOKS · 1 PATTERN", font(70, bold=True), (255, 255, 255))
    text_center(d, 190, "swap the centerpiece in 10 seconds - each decoration is a finished ornament too", font_sans(38), (255, 255, 255))
    d.rectangle([0, H - 120, W, H], fill=(51, 49, 59, 240))
    text_center(d, H - 60, "loop tie-ons + optional safety-pin backs mean you restyle all season", font_sans(38), (255, 255, 255))
    save(base, "NS15_02_looks.jpg")

    # 03 macro texture
    im = photo(WR["macro"], W, H, border=0)
    base = im.copy(); d = ImageDraw.Draw(base, "RGBA")
    d.rectangle([0, H - 330, W, H], fill=(251, 247, 239, 243))
    d.rectangle([0, H - 330, W, H - 316], fill=SAGE)
    text_center(d, H - 235, "A THICK, PLUSH TUBE - NO WIRE FRAME NEEDED", font(58, bold=True), CHARC)
    text_center(d, H - 145, "constant 12-stitch spiral  ·  stuff as you go  ·  squishy enough to mail to grandma", font_sans(38), INK)
    text_center(d, H - 62, "novality store  ·  NS 15", font_sans(32, bold=True), SAGE)
    save(base, "NS15_03_detail.jpg")

    # 04 fireplace lifestyle
    im = photo(WR["fire"], W, H, border=0)
    base = im.copy(); d = ImageDraw.Draw(base, "RGBA")
    d.rectangle([0, 0, W, 210], fill=(51, 49, 59, 238))
    text_center(d, 105, "WINTER MODE: SNOWFLAKE CENTERPIECE", font(62, bold=True), (255, 255, 255))
    d.rectangle([0, H - 150, W, H], fill=(176, 64, 55, 238))
    text_center(d, H - 75, "the same wreath, one week later - poinsettia coming back for party night", font_sans(38), (255, 255, 255))
    save(base, "NS15_04_lifestyle.jpg")

    # 05 info card
    base, d = canvas(); header(d, "WHAT YOU GET", "instant download  ·  print-friendly")
    items = [
        ("Dual-format rounds", "US and UK terms side by side for every row - one file for everyone"),
        ("Wreath + 3 decorations", "tube, poinsettia, snowflake, holiday bow - plus a mini hanging-wreath bonus"),
        ("Loop tie-on system", "decorations attach and detach in 10 seconds; safety-pin backs optional"),
        ("Mini wreath bonus", "tiny 16-19 cm version for doors, garlands, table settings"),
        ("Exact size table", "tube lengths for 10 / 12 / 14 inch wreaths - the math is done for you"),
        ("Support included", "pattern help answered within 48 hours"),
    ]
    y = bullets(d, items, 80, 390, font_sans(40), 56)
    band(d, y + 40, 90, CHARC, "crochet level: confident beginner  ·  hook 4 mm  ·  DK or worsted", fnt=font_sans(42, bold=True))
    footer(d)
    save(base, "NS15_05_info.jpg")

    # 06 sizes
    base, d = canvas(); header(d, "SIZE CHART", "the tube does the sizing - three standard wreaths")
    rows = [("MINI", "chain 20 base", "16-19 cm / 6-7.5 in across", "doors, garlands, tree ornaments"),
            ("STANDARD", "chain 25 base", "25-30 cm / 10-12 in across", "the classic front-door wreath"),
            ("STATEMENT", "chain 30 base", "35-42 cm / 14-16 in across", "oversized mantel drama")]
    cols = [(170, "SIZE"), (640, "START CHAIN"), (1180, "FINISHED ACROSS")]
    fy = 420
    d.rectangle([120, fy - 70, W - 120, fy], fill=SAGE)
    for cx, lab in cols:
        d.text((cx, fy - 35), lab, font=font_sans(38, bold=True), fill=(255, 255, 255), anchor="lm")
    fy += 60
    for i, (a, b, c, note) in enumerate(rows):
        d.rectangle([120, fy, W - 120, fy + 260], fill=(PAPER if i % 2 == 0 else (243, 238, 226)))
        d.text((170, fy + 70), a, font=font(56, bold=True), fill=RED)
        d.text((640, fy + 70), b, font=font_sans(44, bold=True), fill=CHARC)
        d.text((1180, fy + 70), c, font=font_sans(42), fill=CHARC)
        d.text((640, fy + 170), note, font=font_sans(36), fill=SAGE)
        fy += 300
    text_center(d, fy + 40, "size comes from your start chain + tube length - both spelled out in the pattern", font_sans(38, bold=True), TERRA)
    footer(d)
    save(base, "NS15_06_sizes.jpg")

    # 07 peek inside
    base, d = canvas(); header(d, "PEEK INSIDE THE PATTERN", "actual dual-format rows - US left, UK right")
    d.rectangle([120, 380, W - 120, 1450], fill=PAPER)
    d.rectangle([120, 380, W - 120, 470], fill=CHARC)
    d.text((160, 425), "Part", font=font_sans(34, bold=True), fill=GOLD, anchor="lm")
    d.text((360, 425), "US terms", font=font_sans(34, bold=True), fill=(255, 255, 255), anchor="lm")
    d.text((1330, 425), "UK terms", font=font_sans(34, bold=True), fill=(255, 255, 255), anchor="lm")
    d.text((2140, 425), "Sts", font=font_sans(34, bold=True), fill=GOLD, anchor="lm")
    sample = [("Tube", "MR 6 sc; inc around (12); sc in spiral 140-160 rnds, stuff as you go", "MR 6 dc; inc around (12); dc in spiral 140-160 rnds, stuff as you go", "12/rd"),
              ("Skirt R1", "ch 1, 2 sc in each st around, sl st (24)", "ch 1, 2 dc in each st around, sl st (24)", "24"),
              ("Petal", "[ch 4, 3 tr, ch 4, sl st] in same st; repeat in each of 6 centre sts", "[ch 4, 3 dtr, ch 4, sl st] in same st; repeat x6", "6 petals"),
              ("Bow tail", "ch 15, sc in 2nd ch from hook and across (14)", "ch 15, dc in 2nd ch from hook and across (14)", "14"),
              ("Snowflake", "ch 5, sl st in next st around into ch-5 spaces: 6 spaces", "ch 5, sl st in next st around into ch-5 spaces: 6 spaces", "6 spaces")]
    fy = 560
    for i, (r, us, uk, n) in enumerate(sample):
        if r == "Petal":
            d.rectangle([140, fy - 44, W - 140, fy + 118], fill=(247, 232, 229))
            d.text((150, fy + 92), "Petals: 6 petals = all 6 centre stitches - fully counted and verified", font=font_sans(30), fill=RED)
        d.text((160, fy), r, font=font(42, bold=True), fill=CHARC)
        for l in (wrap(d, us, font_sans(29), 940)[:2]):
            d.text((360, fy), l, font=font_sans(29), fill=INK); fy_l = fy
        d.text((1330, fy), uk, font=font_sans(29), fill=INK) if False else None
        for l in (wrap(d, uk, font_sans(29), 780)[:2]):
            d.text((1330, fy), l, font=font_sans(29), fill=INK)
        d.text((2140, fy), n, font=font_sans(32, bold=True), fill=SAGE)
        d.line([140, fy + 66, W - 140, fy + 66], fill=(222, 215, 200), width=3)
        fy += 150
    text_center(d, 1520, "+ 5 decoration sub-pieces, size table, assembly walk-through, troubleshooting, 2 colorway ideas", font_sans(36), INK)
    footer(d)
    save(base, "NS15_07_preview.jpg")

    # 08 gift
    base, d = canvas()
    band(d, 0, 250, RED, "A WREATH THEY CAN RESTYLE ALL SEASON", font(66, bold=True))
    d.rectangle([0, 250, W, 266], fill=GOLD)
    tile(base, WR["door"], 140, 420, 950, 950)
    items = [
        ("Three gifts in one", "wreath + poinsettia + snowflake + bow - box it as a set"),
        ("Ships flat", "the stuffed tube squishes; it springs back after the journey"),
        ("Boutique-worthy", "sell finished wreaths with credit - perfect market stock"),
        ("Season-proof", "swap decorations in December, January nicknames, cozy bow in February"),
    ]
    bullets(d, items, 1160, 480, font_sans(40), 56, center=False, max_w=1120)
    text_center(d, 1530, "'did you BUY that?' - best question in crochet", font(50, bold=True), RED)
    footer(d)
    save(base, "NS15_08_gift.jpg")

    # 09 why
    base, d = canvas(); header(d, "WHY BUYERS CHOOSE NOVALITY", "independent design  ·  honest patterns")
    tiles = [(WR["variants"], "one pattern, three looks"), (WR["macro"], "plush hand-made tube"), (WR["door"], "porch-ready result")]
    for i, (p, cap) in enumerate(tiles):
        tile(base, p, 170 + i * 700, 420, 640, 720, caption=cap)
    items = [
        ("Counted to the stitch", "every consumption & stitch tally re-derived by an automated audit"),
        ("Photos that match", "the listing images mirror the actual pattern pieces - no stock illusions"),
        ("Real support", "pattern questions answered fast; I test everything I sell"),
        ("Sell your makes", "small-batch friendly with designer credit"),
    ]
    y = bullets(d, items, 340, 1240, font_sans(38), 52)
    footer(d, "NOVALITY STORE  ·  thank you for supporting an indie designer")
    save(base, "NS15_09_why.jpg")

    # 10 wip/crafting scene
    im = photo(WR["wip"], W, H, border=0)
    base = im.copy(); d = ImageDraw.Draw(base, "RGBA")
    d.rectangle([0, 0, W, 250], fill=(51, 49, 59, 238))
    d.rectangle([0, 250, W, 264], fill=GOLD)
    text_center(d, 105, "STUFF AS YOU GO - THE SQUISH IS THE POINT", font(62, bold=True), (255, 255, 255))
    text_center(d, 190, "the tube is one long spiral; the decorations are finished in under an hour each", font_sans(36), (233, 226, 210))
    d.rectangle([0, H - 120, W, H], fill=(176, 64, 55, 238))
    text_center(d, H - 60, "confidence list: magic ring, increase, spiral rounds, chains, simple loops", font_sans(38, bold=True), (255, 255, 255))
    save(base, "NS15_10_wip.jpg")

    # 11 details grid
    base, d = canvas(); header(d, "PATTERN DETAILS", "everything at a glance")
    grid = [("DESIGN CODE", "NS 15"), ("FORMAT", "PDF · US + UK terms"),
            ("LEVEL", "confident beginner"), ("TIME", "wreath 1 wknd · decos 1 hr"),
            ("HOOK", "4 mm (US G-6)"), ("YARN", "DK or light worsted"),
            ("AMOUNTS", "green ~80g · red ~25g · white ~15g"), ("CONSTRUCTION", "spiral tube + 4 flat pieces"),
            ("SIZES", "mini · standard · statement"), ("ATTACH", "loop tie-on or safety pin"),
            ("BONUS", "mini wreath for doors/garlands"), ("STITCHES", "ch · sl st · sc · dc · tr · puff leaves")]
    gx, gy = 170, 420
    for i, (k, v) in enumerate(grid):
        x = gx + (i % 2) * 1080
        y = gy + (i // 2) * 200
        d.rounded_rectangle([x, y, x + 1000, y + 160], 20, fill=PAPER, outline=(226, 219, 204), width=3)
        d.text((x + 40, y + 55), k, font=font_sans(30, bold=True), fill=RED)
        d.text((x + 40, y + 110), v, font=font_sans(38, bold=True), fill=CHARC)
    text_center(d, 1740 - 80, "designed so the tube size shifts YOUR row count, never the pattern", font_sans(34, bold=True), TERRA)
    footer(d)
    save(base, "NS15_11_details.jpg")

    # 12 colorways
    base, d = canvas(); header(d, "COLOR RECIPES", "2 tested palettes")
    palettes = [("TRADITIONAL", [(52, 84, 56), (176, 64, 55), (246, 243, 236)], "pine green · holly red · creamy white"),
                ("WINTER WONDERLAND", [(168, 178, 190), (246, 243, 236), (120, 48, 62)], "silver fog · snow white · mulberry")]
    for i, (name, sw, desc) in enumerate(palettes):
        x = 300 + i * 950
        d.rounded_rectangle([x, 470, x + 760, 1180], 24, fill=PAPER, outline=(226, 219, 204), width=3)
        d.rounded_rectangle([x, 470, x + 760, 580], 24, fill=SAGE)
        d.text((x + 380, 525), name, font=font_sans(42, bold=True), fill=(255, 255, 255), anchor="mm")
        sy = 700
        for j, c in enumerate(sw):
            d.ellipse([x + 120 + j * 60, sy, x + 320 + j * 60, sy + 200], fill=c, outline=(160, 150, 135), width=4)
        yy = 980
        for l in wrap(d, desc, font_sans(38), 620):
            d.text((x + 380, yy), l, font=font_sans(38), fill=INK, anchor="ma")
            yy += 54
    text_center(d, 1360, "swap one color, get a new tradition - the tube math never changes", font_sans(40, bold=True), TERRA)
    footer(d)
    save(base, "NS15_12_colorways.jpg")

    # 13 care
    base, d = canvas(); header(d, "CARING FOR YOUR WREATH", "a decade of Decembers")
    items = [
        ("Dust", "a 10-second blow with cool hair-dryer air revives it every year"),
        ("Spot clean", "damp cloth + cool water; the aromatized yarn oils hate hot washes"),
        ("Store", "hang it or roll it; never crush under heavy boxes - the tube dents"),
        ("Decos", "detach before storing; wrap the snowflake in tissue"),
        ("Moisture", "indoor or sheltered-door use; rain will stretch wet wool"),
        ("Revive", "gently steam (hover iron, no touch) to puff flattened bobbles"),
    ]
    y = bullets(d, items, 340, 420, font_sans(42), 58)
    band(d, y + 40, 96, SAGE, "care notes also included in the pattern PDF", fnt=font_sans(40, bold=True))
    footer(d)
    save(base, "NS15_13_care.jpg")

    # 14 mini bonus
    base, d = canvas()
    band(d, 0, 250, SAGE, "BONUS: THE MINI WREATH", font(70, bold=True))
    d.rectangle([0, 250, W, 266], fill=GOLD)
    tile(base, WR["variants"], 140, 420, 950, 950)
    items = [
        ("Same tube, tiny scale", "constant 8-stitch spiral, 20-24 cm of tube, 16-19 cm finished"),
        ("Ornament-engineered", "a ch 14 hanging loop is built into the last round"),
        ("Advent idea", "make 4 in 4 colorways - one per December week"),
        ("Bundle-seller secret", "mini wreaths sell out fast at 8-12 dollars a piece"),
    ]
    bullets(d, items, 1160, 480, font_sans(40), 56, center=False, max_w=1120)
    text_center(d, 1530, "included free in the NS 15 pattern - no separate listing needed", font_sans(40, bold=True), RED)
    footer(d)
    save(base, "NS15_14_mini.jpg")

    # 15 thanks
    base, d = canvas()
    band(d, 0, 250, CHARC, "THANK YOU FOR CROCHETING WITH NOVALITY", font(64, bold=True))
    d.rectangle([0, 250, W, 266], fill=GOLD)
    tile(base, WR["door"], 700, 410, 1000, 760)
    text_center(d, 1300, "Share your wreath - tag #NovalityStore and #3in1Wreath", font_sans(44, bold=True), CHARC)
    text_center(d, 1380, "I read every message; pattern help is always included", font_sans(40), INK)
    text_center(d, 1490, "5% to knitting-for-warmth charities each December", font_sans(36), SAGE)
    footer(d, "© 2026 Novality Store · pattern for personal use, small-batch selling welcome with credit")
    save(base, "NS15_15_thanks.jpg")


# ------------------------------------------------------------ extensions
EXT = {
    "11x": (None, None, None, ["NS11_01_cover.jpg", "NS11_02_wip.jpg", "NS11_06_lifestyle.jpg"],
           [("11_pattern", "PATTERN DETAILS", [("DESIGN CODE", "NS 11"), ("FORMAT", "PDF · US + UK terms"), ("LEVEL", "beginner+"), ("TIME", "1.5-2.5 hrs"), ("HOOK", "4 mm (US G-6)"), ("YARN", "DK / light worsted"), ("SIZE", "15 cm / 6 in tall"), ("CONSTRUCTION", "one piece, NO SEWING"), ("STITCHES", "ch · sl st · sc · inc · dec"), ("EXTRAS", "3 hat color recipes")]),
            ("11_process", "HOW IT'S MADE", None),
            ("13_care", "CARING FOR YOUR GNOME", None),
            ("15_thanks", "THANK YOU FOR CROCHETING WITH NOVALITY", None)]),
    "12": ("Bobble Christmas Tree", "NS12", ["NS12_01_cover.jpg", "NS12_02_wip.jpg", "NS12_06_lifestyle.jpg"],
           [("11_pattern", "PATTERN DETAILS", [("DESIGN CODE", "NS 12"), ("FORMAT", "PDF · US + UK terms"), ("LEVEL", "easy"), ("TIME", "2-3 hrs"), ("HOOK", "4 mm (US G-6)"), ("YARN", "DK / light worsted"), ("SIZE", "18 cm / 7 in tall"), ("CONSTRUCTION", "spiral cone + bobble garland"), ("STITCHES", "ch · sl st · sc · dc · bobble"), ("EXTRAS", "2 colorways + stump option")]),
            ("11_process", "HOW IT'S MADE", None),
            ("13_care", "CARING FOR YOUR TREE", None),
            ("15_thanks", "THANK YOU FOR CROCHETING WITH NOVALITY", None)]),
    "13": ("Christmas Ornament Bundle", "NS13", ["NS13_01_cover.jpg", "NS13_02_wip.jpg", "NS13_06_lifestyle.jpg"],
           [("11_pattern", "PATTERN DETAILS", [("DESIGN CODE", "NS 13"), ("FORMAT", "PDF · US + UK terms"), ("LEVEL", "confident beginner"), ("TIME", "45-75 min each"), ("HOOK", "3.5 mm (US E-4)"), ("YARN", "fingering / sport"), ("SET", "bauble · star · snowflake"), ("SIZE", "8-10 cm each"), ("STITCHES", "ch · sl st · sc · dc · tr · puff"), ("EXTRAS", "bonus gift-tag notes")]),
            ("11_process", "HOW IT'S MADE", None),
            ("13_care", "CARE NOTES", None),
            ("15_thanks", "THANK YOU FOR CROCHETING WITH NOVALITY", None)]),
}


def ext_slot_details(code, title, key, rows):
    base, d = canvas(); header(d, title, "everything at a glance")
    gx, gy = 170, 420
    for i, (k, v) in enumerate(rows):
        x = gx + (i % 2) * 1080
        y = gy + (i // 2) * 200
        d.rounded_rectangle([x, y, x + 1000, y + 160], 20, fill=PAPER, outline=(226, 219, 204), width=3)
        d.text((x + 40, y + 55), k, font=font_sans(30, bold=True), fill=RED)
        d.text((x + 40, y + 110), v, font=font_sans(38, bold=True), fill=CHARC)
    text_center(d, 1740 - 80, "full row-by-row tables in both US and UK terms inside the PDF", font_sans(34, bold=True), TERRA)
    footer(d)
    save(base, f"{code}_{key}_card.jpg")


def ext_process(code, tiles, title_txt, steps):
    base, d = canvas(); header(d, title_txt, "from ball of yarn to holiday hero")
    for i, p in enumerate(tiles):
        tile(base, ETSY / p, 170 + i * 700, 420, 640, 720)
    y = bullets(d, steps, 340, 1240, font_sans(38), 52)
    footer(d)
    save(base, f"{code}_11_process.jpg")


def ext_care(code, thank_note):
    base, d = canvas(); header(d, thank_note[0], thank_note[1])
    y = bullets(d, thank_note[2], 340, 420, font_sans(42), 58)
    band(d, y + 40, 96, SAGE, thank_note[3], fnt=font_sans(40, bold=True))
    footer(d)
    save(base, f"{code}_13_care.jpg")


def ext_thanks(code, img, tag_h):
    base, d = canvas()
    band(d, 0, 250, CHARC, "THANK YOU FOR CROCHETING WITH NOVALITY", font(64, bold=True))
    d.rectangle([0, 250, W, 266], fill=GOLD)
    tile(base, ETSY / img, 700, 410, 1000, 760)
    text_center(d, 1300, f"Share yours - tag #NovalityStore and {tag_h}", font_sans(44, bold=True), CHARC)
    text_center(d, 1380, "pattern help is always included - I answer within 48 hrs", font_sans(40), INK)
    text_center(d, 1490, "small-batch selling welcome with designer credit", font_sans(36), SAGE)
    footer(d, "© 2026 Novality Store · thank you,")
    save(base, f"{code}_15_thanks.jpg")


def extensions():
    packs = {
        "11": ("NS11", "NS11_01_cover.jpg",
               [(("the gnome who never grew a seam", "one tube, 3 color changes, a popcorn nose - done")),
                (("no tapestry needle gymnastics", "the beard, face, and hat are built into the rounds")),
                (("fast stash-buster", "about 40 g of yarn - the perfect craft-fair pot-boiler"))],
               ("CARING FOR YOUR GNOME", "keep him plump for years",
                [("Dust", "gentle blow with cool hair-dryer air or a soft brush"),
                 ("Spot clean", "damp cloth, cool water - never soak the nose"),
                 ("Wool only", "if you upgraded to wool: cold hand wash, dry flat"),
                 ("Store", "in a box with space - his hat likes its peak"),
                 ("Revive", "a fingertip of steam plumps flattened beard bobbles")],
                "care card also included in the PDF"),
               "#NoSewGnome",
               [("DESIGN CODE", "NS 11"), ("FORMAT", "PDF · US + UK terms"), ("LEVEL", "beginner+"), ("TIME", "1.5-2.5 hrs"), ("HOOK", "4 mm (US G-6)"), ("YARN", "DK / light worsted"), ("SIZE", "15 cm / 6 in tall"), ("CONSTRUCTION", "ONE piece - zero sewing"), ("STITCHES", "ch · sl st · sc · inc · dec"), ("BONUS", "3 hat color recipes")]),
        "12": ("NS12", "NS12_01_cover.jpg",
               [(("social-media famous texture", "bobble rows form the classic pine silhouette")),
                (("single spiral, no seaming", "cone → trunk → bobbles in one continuous build")),
                (("two sizes, one recipe", "scale by rounds; pattern flags the pivot rows"))],
               ("CARING FOR YOUR TREE", "keep the bobbles bouncy",
                [("Dust", "cool hair-dryer puff, 10 seconds"),
                 ("Spot clean", "damp cloth, cool water; no twisting"),
                 ("Store", "nestle in tissue - bobbles don't like boxes stacked on them"),
                 ("Steam revive", "hover-iron steam perks up squashed bobbles"),
                 ("Embellish-safe", "mini ornaments hook right onto the bobble rows")],
                "care notes also printed in the PDF"),
               "#BobbleTree",
               [("DESIGN CODE", "NS 12"), ("FORMAT", "PDF · US + UK terms"), ("LEVEL", "easy"), ("TIME", "2-3 hrs"), ("HOOK", "4 mm (US G-6)"), ("YARN", "DK / light worsted"), ("SIZE", "18 cm / 7 in tall"), ("CONSTRUCTION", "spiral cone + bobble garland"), ("STITCHES", "ch · sl st · sc · dc · bobble"), ("BONUS", "2 colorways + stump option")]),
        "13": ("NS13", "NS13_01_cover.jpg",
               [(("three ornaments, one sitting", "bauble, star, and snowflake share a build philosophy")),
                (("true scrap-busters", "each uses under 12 g - smash your leftover sport yarn")),
                (("gift-tag ready", "pattern prints tiny versions you can tuck into presents"))],
               ("CARE NOTES", "tiny things, long life",
                [("Store", "wrap the snowflake in tissue; star and bauble in a divided box"),
                 ("Spot clean", "cool damp cloth only; puffs dislike soap soak"),
                 ("Steam revive", "hover-steam lifts flattened snowflake arms"),
                 ("Hanger check", "re-tighten the hanging loop each season"),
                 ("Sunlight", "keep white snowflakes out of direct brown-sun fade")],
                "care notes also printed in the PDF"),
               "#NS13Bundle",
               [("DESIGN CODE", "NS 13"), ("FORMAT", "PDF · US + UK terms"), ("LEVEL", "confident beginner"), ("TIME", "45-75 min each"), ("HOOK", "3.5 mm (US E-4)"), ("YARN", "fingering / sport"), ("SET", "bauble · star · snowflake"), ("SIZE", "8-10 cm each"), ("STITCHES", "ch · sl st · sc · dc · tr · puff"), ("BONUS", "gift-tag notes")]),
    }
    for key, (code, hero, steps, care, tag, details) in packs.items():
        ext_process(code, [f"{code}_02_wip.jpg", f"{code}_04_detail.jpg", f"{code}_09_gift.jpg"],
                    "HOW IT'S MADE", [(h, t) for h, t in steps])
        ext_slot_details(code, "PATTERN DETAILS", "11_pattern", details)
        ext_care(code, care)
        ext_thanks(code, hero, tag)


def main():
    ns14()
    ns15()
    extensions()


if __name__ == "__main__":
    main()
