"""Build the Etsy listing kit: 10 listing images (2000x2000, Etsy's recommended square) + a
thumbnail-safe cover, plus SEO copy (title, tags, description, FAQ) as Markdown/JSON.

Usage: python build_etsy.py  -> ../etsy/
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.path.insert(0, str(Path(__file__).parent))
import pattern_data as P  # noqa: E402

KIT = Path(__file__).resolve().parent.parent
IMG = KIT / "assets" / "img"
FONTS = KIT / "assets" / "fonts"
OUT = KIT / "etsy"
OUT.mkdir(exist_ok=True)

S = 2000  # Etsy square
CREAM = (255, 251, 247); PINK = (232, 169, 184); PINK_DEEP = (184, 80, 111); PINK_PALE = (251, 238, 241)
INK = (59, 47, 51); INK_SOFT = (122, 106, 112); RULE = (235, 215, 221); WHITE = (255, 255, 255); MINT = (60, 156, 147)


def font(name, size):
    files = {"display": "FredokaOne-Regular.ttf", "sans": "SourceSansPro-Regular.ttf", "semi": "SourceSansPro-Semibold.ttf",
             "bold": "SourceSansPro-Bold.ttf", "it": "SourceSansPro-It.ttf", "serif_it": "Caladea-Italic.ttf"}
    return ImageFont.truetype(str(FONTS / files[name]), size)


def fit(path, w, h):
    im = Image.open(path).convert("RGB")
    sc = max(w / im.width, h / im.height)
    im = im.resize((int(im.width * sc) + 1, int(im.height * sc) + 1), Image.LANCZOS)
    x = (im.width - w) // 2; y = (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))


def rmask(w, h, r):
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=r, fill=255); return m


def wrap(d, text, fnt, max_w):
    words = text.split(); lines = []; cur = ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=fnt) <= max_w: cur = t
        else: lines.append(cur); cur = w_
    if cur: lines.append(cur)
    return lines


def chip(d, xy, text, fnt, fill=PINK_DEEP, fg=WHITE, pad=(28, 14)):
    x, y = xy
    w = d.textlength(text, font=fnt) + pad[0] * 2
    h = fnt.size + pad[1] * 2
    d.rounded_rectangle((x, y, x + w, y + h), radius=h // 2, fill=fill)
    d.text((x + pad[0], y + pad[1] - 2), text, font=fnt, fill=fg)
    return w


def shadow_paste(base, im, xy, radius=48, blur=40, alpha=80):
    w, h = im.size
    sh = Image.new("RGBA", (w + blur * 3, h + blur * 3), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((blur, blur + 20, w + blur, h + blur + 20), radius=radius, fill=(120, 40, 70, alpha))
    sh = sh.filter(ImageFilter.GaussianBlur(blur // 2))
    base.paste(sh, (xy[0] - blur, xy[1] - blur), sh)
    base.paste(im, xy, rmask(w, h, radius))


def canvas():
    im = Image.new("RGB", (S, S), CREAM)
    blob = Image.new("RGB", (S, S), CREAM); bd = ImageDraw.Draw(blob)
    bd.ellipse((S - 700, -500, S + 300, 500), fill=PINK_PALE); bd.ellipse((-400, S - 500, 400, S + 300), fill=PINK_PALE)
    im.paste(blob.filter(ImageFilter.GaussianBlur(70)))
    return im


def brand_footer(d, text=None):
    d.text((S // 2, S - 70), text or f"{P.DESIGNER}  ·  Design {P.DESIGN_CODE}  ·  PDF pattern, {P.TERMS}", font=font("semi", 30), fill=INK_SOFT, anchor="mm")


# ------------------------------------------------------------------ the ten images
def img01_cover():
    """Thumbnail-first: full-bleed hero with a compact badge - must read at 200 px."""
    im = fit(IMG / "hero_axel.png", S, S)
    d = ImageDraw.Draw(im, "RGBA")
    # bottom gradient
    for y in range(S - 620, S):
        a = int(230 * ((y - (S - 620)) / 620) ** 1.4)
        d.line((0, y, S, y), fill=(184, 80, 111, a))
    d = ImageDraw.Draw(im)
    d.text((100, S - 470), "Axel the Axolotl", font=font("display", 150), fill=WHITE)
    d.text((104, S - 300), "Amigurumi crochet pattern  ·  PDF", font=font("serif_it", 62), fill=WHITE)
    x = 104
    for c in ("US terms", "Advanced beginner", "11.5 cm / 4.5 in"):
        x += chip(d, (x, S - 200), c, font("semi", 38), fill=(255, 255, 255), fg=PINK_DEEP) + 20
    # corner badge
    d.ellipse((S - 420, 80, S - 80, 420), fill=WHITE)
    d.text((S - 250, 210), "PDF", font=font("display", 96), fill=PINK_DEEP, anchor="mm")
    d.text((S - 250, 300), "instant download", font=font("semi", 32), fill=INK_SOFT, anchor="mm")
    return im


def img02_whats_included():
    im = canvas(); d = ImageDraw.Draw(im)
    d.text((S // 2, 150), "What's included", font=font("display", 110), fill=PINK_DEEP, anchor="mm")
    d.text((S // 2, 250), "Everything you need to make Axel - delivered instantly", font=font("serif_it", 46), fill=INK_SOFT, anchor="mm")
    photo = fit(IMG / "in_hand_scale.png", 820, 820)
    shadow_paste(im, photo, (1080, 380))
    items = [("12-page designed PDF", "cover, materials, 5 techniques, every round in tables"),
             ("Full narrated audio", "~12 min walkthrough, chaptered - listen while you crochet"),
             ("Tutorial video", "1080p round-by-round slides with captions and chapter markers"),
             ("52 verified rounds", "every stitch count machine-checked, 0 errors"),
             ("5 colourway ideas", "classic pink, leucistic, melanoid, mint, lavender"),
             ("Troubleshooting guide", "neck, fin, gauge, sitting - fixes for every common snag")]
    y = 400
    for title, sub in items:
        d.ellipse((120, y + 14, 168, y + 62), fill=PINK_DEEP)
        d.text((144, y + 38), "✓", font=font("bold", 34), fill=WHITE, anchor="mm")
        d.text((200, y), title, font=font("semi", 46), fill=INK)
        d.text((200, y + 58), sub, font=font("sans", 32), fill=INK_SOFT)
        y += 150
    brand_footer(d)
    return im


def img03_size():
    im = canvas(); d = ImageDraw.Draw(im)
    photo = fit(IMG / "hero_axel.png", 1240, 1240)
    shadow_paste(im, photo, (380, 160))
    # dimension lines
    d.line((300, 200, 300, 1360), fill=PINK_DEEP, width=6); d.line((270, 200, 330, 200), fill=PINK_DEEP, width=6); d.line((270, 1360, 330, 1360), fill=PINK_DEEP, width=6)
    txt = Image.new("RGBA", (500, 90), (0, 0, 0, 0)); ImageDraw.Draw(txt).text((250, 45), "11.5 cm  /  4.5 in tall", font=font("semi", 44), fill=PINK_DEEP, anchor="mm")
    im.paste(txt.rotate(90, expand=True), (140, 560), txt.rotate(90, expand=True))
    d.line((420, 1440, 1580, 1440), fill=PINK_DEEP, width=6); d.line((420, 1410, 420, 1470), fill=PINK_DEEP, width=6); d.line((1580, 1410, 1580, 1470), fill=PINK_DEEP, width=6)
    d.text((1000, 1500), "10 cm  /  4 in  gill tip to gill tip", font=font("semi", 44), fill=PINK_DEEP, anchor="mm")
    d.text((S // 2, 1660), "Palm-sized & huggable", font=font("display", 96), fill=PINK_DEEP, anchor="mm")
    d.text((S // 2, 1760), "Worsted #4 yarn  ·  3.5 mm hook  ·  head is a true 52 mm sphere  ·  4.3 cm shell-edged tail", font=font("sans", 36), fill=INK_SOFT, anchor="mm")
    brand_footer(d)
    return im


def img04_materials():
    im = canvas(); d = ImageDraw.Draw(im)
    photo = fit(IMG / "flatlay_materials.png", 1100, 1100)
    shadow_paste(im, photo, (60, 460))
    d.text((100, 120), "Materials", font=font("display", 110), fill=PINK_DEEP)
    d.text((104, 250), "One 25 g ball of pale pink covers the whole toy", font=font("serif_it", 44), fill=INK_SOFT)
    lines = [("Main yarn", "Worsted #4 pale pink, ~15 g"), ("Gill yarn", "Fuzzy / eyelash fur, dark pink, ~8 g"), ("Fin yarn", "Worsted #4 dark pink, ~3 g"),
             ("Hook", "3.5 mm (US E/4)"), ("Eyes", "Two 6 mm safety eyes"), ("Also", "Filling ~8 g, needle, black floss,\npink pastel, stitch marker")]
    y = 480
    for k, v in lines:
        d.text((1230, y), k.upper(), font=font("semi", 30), fill=PINK_DEEP)
        for i, ln in enumerate(v.split("\n")):
            d.text((1230, y + 40 + i * 44), ln, font=font("sans", 38), fill=INK)
        y += 150 + (44 if "\n" in v else 0)
    d.rounded_rectangle((1200, 1560, 1940, 1740), radius=30, fill=PINK_PALE)
    d.text((1570, 1610), "GAUGE", font=font("semi", 30), fill=PINK_DEEP, anchor="mm")
    d.text((1570, 1670), "36 sc around = ~52 mm when stuffed", font=font("sans", 34), fill=INK, anchor="mm")
    brand_footer(d)
    return im


def img05_pdf_preview():
    """Show real pages from the PDF."""
    import pymupdf
    im = canvas(); d = ImageDraw.Draw(im)
    d.text((S // 2, 140), "Inside the PDF", font=font("display", 110), fill=PINK_DEEP, anchor="mm")
    d.text((S // 2, 240), "12 designed pages - clear tables, photos, and notes exactly where you need them", font=font("serif_it", 42), fill=INK_SOFT, anchor="mm")
    doc = pymupdf.open(str(KIT / "Axel_the_Axolotl_Pattern.pdf"))
    pages = [0, 4, 6, 7]
    pw = 560; ph = int(pw * 1.414)
    xs = [70, 550, 1030, 1510]
    for k, (pi, x) in enumerate(zip(pages, xs)):
        pix = doc[pi].get_pixmap(dpi=110)
        pg = Image.frombytes("RGB", (pix.width, pix.height), pix.samples).resize((pw, ph), Image.LANCZOS)
        y = 380 + (0 if k % 2 == 0 else 120)
        pg_im = Image.new("RGB", (pw, ph), WHITE); pg_im.paste(pg)
        shadow_paste(im, pg_im, (x, y), radius=18, blur=30, alpha=70)
    d.rounded_rectangle((280, 1420, 1720, 1560), radius=40, fill=WHITE, outline=RULE, width=3)
    d.text((S // 2, 1490), "Every round in a table  ·  stitch counts on every row  ·  notes for eyes, stuffing and limbs", font=font("semi", 36), fill=INK, anchor="mm")
    d.text((S // 2, 1700), "Prints beautifully on A4 or Letter  ·  reads perfectly on a phone or tablet", font=font("sans", 36), fill=INK_SOFT, anchor="mm")
    brand_footer(d)
    return im


def img06_video_audio():
    im = canvas(); d = ImageDraw.Draw(im)
    d.text((S // 2, 140), "Watch it. Hear it. Make it.", font=font("display", 104), fill=PINK_DEEP, anchor="mm")
    d.text((S // 2, 240), "A narrated tutorial video and a chaptered audio walkthrough come with the pattern", font=font("serif_it", 40), fill=INK_SOFT, anchor="mm")
    # fake video frame using the real title card render
    frame = fit(IMG / "hero_axel.png", 1400, 788).filter(ImageFilter.GaussianBlur(3))
    frame = Image.blend(frame, Image.new("RGB", frame.size, PINK_DEEP), 0.45)
    fd = ImageDraw.Draw(frame)
    fd.ellipse((620, 314, 780, 474), fill=WHITE); fd.polygon([(680, 354), (680, 434), (750, 394)], fill=PINK_DEEP)
    fd.text((700, 560), "Round-by-round tutorial  ·  12 min  ·  1080p  ·  captions", font=font("semi", 36), fill=WHITE, anchor="mm")
    fd.rounded_rectangle((60, 720, 1340, 736), radius=8, fill=(255, 255, 255, 120)); fd.rounded_rectangle((60, 720, 520, 736), radius=8, fill=WHITE)
    shadow_paste(im, frame, (300, 330), radius=36)
    # audio chapters
    d.rounded_rectangle((300, 1190, 1700, 1760), radius=40, fill=WHITE, outline=RULE, width=3)
    d.text((360, 1230), "AUDIO CHAPTERS", font=font("semi", 30), fill=PINK_DEEP)
    chapters = ["01 Welcome", "02 Safety & materials", "03 Five techniques", "04 Head R1-R13", "05 Body R14-R26",
                "06 Tail R27-R36", "07 Arms & feet", "08 Gills x6", "09 Tail fin", "10 Assembly"]
    for i, c in enumerate(chapters):
        col = i % 2; row = i // 2
        x = 360 + col * 680; y = 1290 + row * 88
        d.ellipse((x, y + 8, x + 40, y + 48), fill=PINK_PALE); d.polygon([(x + 14, y + 17), (x + 14, y + 39), (x + 30, y + 28)], fill=PINK_DEEP)
        d.text((x + 60, y + 6), c, font=font("sans", 36), fill=INK)
    d.text((S // 2, 1830), "Listen while your hands are busy - every round is read out with its stitch count.", font=font("serif_it", 38), fill=INK_SOFT, anchor="mm")
    brand_footer(d)
    return im


def img07_details():
    im = canvas(); d = ImageDraw.Draw(im)
    a = fit(IMG / "detail_gills.png", 900, 900); b = fit(IMG / "detail_tail.png", 900, 900)
    shadow_paste(im, a, (80, 260)); shadow_paste(im, b, (1020, 260))
    d.text((S // 2, 140), "The details that make Axel", font=font("display", 100), fill=PINK_DEEP, anchor="mm")
    for x, t, s_ in ((530, "Six fluffy fur-yarn gills", "3 per side, fanned up / out / down"), (1470, "Shell-edged paddle tail", "5 loose dc scallops, fits the ridge exactly")):
        d.rounded_rectangle((x - 400, 1200, x + 400, 1370), radius=30, fill=WHITE, outline=RULE, width=3)
        d.text((x, 1250), t, font=font("semi", 44), fill=INK, anchor="mm")
        d.text((x, 1315), s_, font=font("sans", 32), fill=INK_SOFT, anchor="mm")
    feats = ["Round head - 3 straight rounds keep it a true sphere", "No neck seam - head, neck, body & tail in one spiral",
             "Invisible decreases - no ridges where it shows", "Sits upright on its own - plump ball feet"]
    y = 1440
    for f in feats:
        d.ellipse((360, y + 10, 392, y + 42), fill=PINK_DEEP); d.text((420, y), f, font=font("sans", 38), fill=INK); y += 78
    brand_footer(d)
    return im


def img08_colorways():
    im = canvas(); d = ImageDraw.Draw(im)
    photo = fit(IMG / "colorways.png", 1840, 1100)
    shadow_paste(im, photo, (80, 330))
    d.text((S // 2, 150), "Five colourways, one pattern", font=font("display", 100), fill=PINK_DEEP, anchor="mm")
    d.text((S // 2, 250), "Swap the main and gill yarns - the stitch counts never change", font=font("serif_it", 42), fill=INK_SOFT, anchor="mm")
    names = [n for n, *_ in P.COLORWAYS]
    x0 = 130; step = 1740 / 5
    for i, (n, m, g) in enumerate(P.COLORWAYS):
        cx = int(x0 + step * i + step / 2)
        d.ellipse((cx - 60, 1500, cx + 60, 1620), fill=m, outline=RULE, width=3)
        d.ellipse((cx - 20, 1545, cx + 20, 1585), fill=g)
        d.text((cx, 1680), n, font=font("semi", 34), fill=INK, anchor="mm")
    d.text((S // 2, 1800), "Classic pink  ·  White leucistic  ·  Melanoid black  ·  Mint  ·  Lavender", font=font("sans", 34), fill=INK_SOFT, anchor="mm")
    brand_footer(d)
    return im


def img09_skill():
    im = canvas(); d = ImageDraw.Draw(im)
    photo = fit(IMG / "wip_hands.png", 1000, 1000)
    shadow_paste(im, photo, (940, 420))
    d.text((100, 130), "Advanced beginner", font=font("display", 100), fill=PINK_DEEP)
    d.text((104, 250), "If you can sc, inc and dec in a spiral, you can make Axel", font=font("serif_it", 42), fill=INK_SOFT)
    steps = [("Magic ring", "you already know it"), ("Spiral rounds", "just move the marker"), ("Invisible decrease", "explained step by step"),
             ("Close through both layers", "3 stitches, done"), ("The shell / scallop", "5 dc, sl st - that's the fin")]
    y = 430
    for i, (t, s_) in enumerate(steps, 1):
        d.ellipse((100, y, 190, y + 90), fill=PINK_PALE); d.text((145, y + 45), str(i), font=font("display", 50), fill=PINK_DEEP, anchor="mm")
        d.text((220, y + 4), t, font=font("semi", 44), fill=INK); d.text((220, y + 56), s_, font=font("sans", 32), fill=INK_SOFT)
        y += 150
    d.rounded_rectangle((100, 1230, 860, 1420), radius=30, fill=WHITE, outline=RULE, width=3)
    d.text((480, 1280), "TIME", font=font("semi", 30), fill=PINK_DEEP, anchor="mm")
    d.text((480, 1350), "2.5 - 3 hours start to finish", font=font("semi", 40), fill=INK, anchor="mm")
    d.text((S // 2, 1600), "Every one of the 52 rounds was machine-verified - the counts add up, guaranteed.", font=font("serif_it", 40), fill=INK_SOFT, anchor="mm")
    d.text((S // 2, 1680), "Includes a troubleshooting page: neck, gauge, fin fit, sitting, gill span.", font=font("sans", 36), fill=INK_SOFT, anchor="mm")
    brand_footer(d)
    return im


def img10_terms():
    im = canvas(); d = ImageDraw.Draw(im)
    photo = fit(IMG / "hero_axel.png", 760, 760)
    shadow_paste(im, photo, (1160, 160))
    d.text((100, 130), "Good to know", font=font("display", 100), fill=PINK_DEEP)
    blocks = [("THIS IS A DIGITAL PATTERN", "You are buying the PDF + audio + video files, not the finished toy. Files are available to download immediately after purchase - nothing will be shipped."),
              ("YOU MAY", "Make as many Axels as you like for yourself, gifts or charity, and sell finished toys in small batches with credit to Novality Store."),
              ("YOU MAY NOT", "Resell, share or redistribute the files, or claim the design as your own."),
              ("SAFETY", "Uses 6 mm safety eyes (small parts). Embroider the eyes for children under 3. Not certified to ASTM F963 / EN 71.")]
    y = 300
    for k, v in blocks:
        d.text((100, y), k, font=font("semi", 32), fill=PINK_DEEP); y += 46
        for ln in wrap(d, v, font("sans", 38), 980):
            d.text((100, y), ln, font=font("sans", 38), fill=INK); y += 48
        y += 46
    d.rounded_rectangle((100, 1560, 1900, 1760), radius=40, fill=PINK_DEEP)
    d.text((S // 2, 1630), "Questions? Message us any time - we love helping makers finish.", font=font("semi", 40), fill=WHITE, anchor="mm")
    d.text((S // 2, 1700), "  ".join(P.HASHTAGS), font=font("sans", 34), fill=(255, 230, 236), anchor="mm")
    brand_footer(d)
    return im


IMAGES = [("01_cover.jpg", img01_cover), ("02_whats_included.jpg", img02_whats_included), ("03_size.jpg", img03_size),
          ("04_materials.jpg", img04_materials), ("05_pdf_preview.jpg", img05_pdf_preview), ("06_video_audio.jpg", img06_video_audio),
          ("07_details.jpg", img07_details), ("08_colorways.jpg", img08_colorways), ("09_skill_level.jpg", img09_skill), ("10_good_to_know.jpg", img10_terms)]


# ------------------------------------------------------------------ copy
LISTING = {
    "title": "Axolotl Crochet Pattern PDF, Amigurumi Axolotl Plush Pattern with Video & Audio Tutorial, Beginner Friendly Fluffy Gills Toy, Axel the Axolotl",
    "tags": ["axolotl crochet pattern", "amigurumi axolotl", "crochet axolotl plush", "axolotl amigurumi pdf", "crochet pattern pdf",
             "amigurumi pattern", "crochet toy pattern", "beginner crochet toy", "video crochet tutorial", "kawaii crochet",
             "crochet plushie pattern", "fluffy gills axolotl", "instant download pdf"],
    "category": "Craft Supplies & Tools > Patterns & How To > Patterns & Blueprints > Crochet Patterns",
    "type": "Digital download",
    "who_made": "I did", "what_is_it": "A supply or tool to make things", "when_made": "Made to order",
    "price_suggestion_usd": "5.50 - 7.50 (comparable multi-format amigurumi patterns with video list at 6-9 USD)",
    "materials_field": "PDF, MP3 audio, MP4 video",
    "files": ["Axel_the_Axolotl_Pattern.pdf (12 pages, 1.8 MB)", "Axel_the_Axolotl_Full_Walkthrough.mp3 (12 min) + 10 chapter MP3s",
              "Axel_the_Axolotl_Tutorial.mp4 (1080p, 12 min, 22 MB) - upload to a private/unlisted video link and include it in the PDF or a 'links' PDF if Etsy's 20 MB per-file limit blocks a direct upload"],
}

DESCRIPTION = f"""🩷 AXEL THE AXOLOTL - amigurumi crochet pattern (PDF + audio + video)

Meet Axel: a soft pink axolotl with six fluffy gills, a perfectly round head and a frilly shell-edged paddle tail. Head, neck, body and tail are worked as ONE continuous spiral - so there is no neck seam to sew, ever.

Finished size: about 11.5 cm / 4.5 in tall seated, 10 cm / 4 in gill tip to gill tip. Palm-sized and very huggable.

✨ WHAT YOU GET (instant download)
• 12-page designed PDF pattern - every round in a clear table with stitch counts, photos and notes exactly where you need them
• Narrated audio walkthrough (~12 min, 10 chapters) - every round read aloud so you can crochet without looking at the page
• Tutorial video (1080p, ~12 min) - round-by-round slides that highlight the row being spoken, with captions and chapter markers
• Five techniques explained step by step: magic ring, spiral rounds, invisible decrease, closing through both layers, the shell/scallop
• Assembly guide with exact eye, smile, gill, arm and foot placement
• Troubleshooting page (neck collapsing, fin fit, gauge, sitting, wider gills) and 5 colourway ideas

✅ EVERY STITCH COUNT VERIFIED
All 52 rounds were machine-checked with a deterministic pattern validator: zero errors. The maths adds up, so you can trust the counts.

🧶 YOU WILL NEED
• Worsted #4 pale pink yarn, ~15 g (one 25 g ball covers the whole toy)
• Fuzzy / eyelash fur yarn, dark pink, ~8 g (for the gills)
• Worsted #4 dark pink, ~3 g (for the fin)
• 3.5 mm (US E/4) hook · two 6 mm safety eyes · ~8 g fibrefill
• Tapestry needle, black embroidery floss, pink pastel for blush, stitch marker

📏 SKILL LEVEL
Advanced beginner - US terms. If you can single crochet, increase and decrease in a spiral, you can make Axel. About 2.5-3 hours from start to finish.

🎨 COLOURWAYS
Classic pink · White leucistic · Melanoid black · Mint · Lavender - just swap the main and gill yarns.

⚠️ SAFETY
Axel uses 6 mm safety eyes (small parts). For children under 3, embroider the eyes instead. This pattern has not been tested to ASTM F963 / EN 71 - please do not describe finished toys as "baby-safe".

📄 THIS IS A DIGITAL FILE
No physical item will be shipped. Files are available in your Etsy account under Purchases immediately after payment. Because this is an instant download, refunds cannot be offered - but message us any time and we will help you finish.

📜 TERMS OF USE
You may make as many Axels as you like for yourself, gifts or charity, and sell finished toys in small batches (shops, markets, online) with credit to "Novality Store". Please do not resell, share, translate or redistribute the files, or claim the design as your own.

Design Code {P.DESIGN_CODE} · © {P.YEAR} Novality Store, designed by Novality Crochet Studio.
Tag your makes with {P.HASHTAGS[0]} and {P.HASHTAGS[1]} - we love seeing them!
"""

FAQ = [
    ("Is this a physical toy?", "No - this listing is for the digital pattern (PDF + audio + video). You make Axel yourself."),
    ("What terms does the pattern use?", "US crochet terms. sc = single crochet, dc = double crochet, inc = 2 sc in one stitch, invdec = invisible decrease."),
    ("How long does it take?", "About 2.5-3 hours for an advanced beginner."),
    ("Can I sell the toys I make?", "Yes - small-batch sales are welcome with credit to Novality Store. Mass production needs written permission."),
    ("Is it safe for babies?", "The pattern uses 6 mm safety eyes (small parts). For under-3s embroider the eyes. It is not certified to a toy-safety standard."),
    ("Can I get a refund?", "Digital downloads cannot be refunded once delivered, but message us with any problem and we will help you finish."),
    ("I can't see the stitches in the fur yarn!", "Nobody can - hold a thin strand of smooth yarn with it, or count by feel and trust the round count. Errors vanish in the fluff."),
]

SHOP_ANNOUNCEMENT = ("New: Axel the Axolotl 🩷 - a no-neck-seam amigurumi pattern with a narrated audio walkthrough and a round-by-round "
                     "video tutorial. Every stitch count verified. Advanced beginner, US terms, 2.5-3 hours.")

MESSAGE_TO_BUYER = f"""Thank you so much for buying Axel the Axolotl! 🩷

Your files are ready under Purchases and Reviews > Download Files:
• Axel_the_Axolotl_Pattern.pdf - the full 12-page pattern
• Axel_the_Axolotl_Full_Walkthrough.mp3 - the narrated audio walkthrough (plus 10 chapter files)
• Tutorial video - link and chapter markers are on the last page of the PDF

A quick tip before you start: check your gauge - 36 sc around should measure about 52 mm across when stuffed. And do stuff the head firmly at R11; it keeps the eyes level.

If anything is unclear, just reply to this message. Tag your finished Axel with {P.HASHTAGS[0]} {P.HASHTAGS[1]} - we would love to see it!

Happy crocheting,
Novality Store
"""


def build():
    for name, fn in IMAGES:
        im = fn()
        im.save(OUT / name, quality=92, optimize=True, progressive=True)
        print("  ", name, im.size, (OUT / name).stat().st_size // 1024, "KB")
    (OUT / "listing.json").write_text(json.dumps({**LISTING, "description": DESCRIPTION, "faq": FAQ, "shop_announcement": SHOP_ANNOUNCEMENT, "message_to_buyer": MESSAGE_TO_BUYER}, indent=2, ensure_ascii=False))
    md = [f"# Etsy listing kit - {P.TITLE}", "", "## Title (140 chars max)", "", LISTING["title"], f"\n_{len(LISTING['title'])} characters_", "",
          "## Tags (13, each <= 20 chars)", ""]
    md += [f"- `{t}` ({len(t)})" for t in LISTING["tags"]]
    md += ["", "## Listing settings", "", f"- Category: {LISTING['category']}", f"- Type: {LISTING['type']}", f"- Who made it / What is it / When: {LISTING['who_made']} / {LISTING['what_is_it']} / {LISTING['when_made']}",
           f"- Materials field: {LISTING['materials_field']}", f"- Suggested price: {LISTING['price_suggestion_usd']}", "", "## Files to upload", ""]
    md += [f"- {f}" for f in LISTING["files"]]
    md += ["", "## Images (upload in this order)", ""]
    md += [f"{i+1}. `{n}` - {fn.__doc__.strip() if fn.__doc__ else fn.__name__[6:].replace('_', ' ')}" for i, (n, fn) in enumerate(IMAGES)]
    md += ["", "## Description", "", "```", DESCRIPTION, "```", "", "## FAQ (Etsy 'Frequently asked questions' section)", ""]
    md += [f"**{q}**  \n{a}\n" for q, a in FAQ]
    md += ["## Shop announcement", "", SHOP_ANNOUNCEMENT, "", "## Automatic message to buyers", "", "```", MESSAGE_TO_BUYER, "```"]
    (OUT / "LISTING_COPY.md").write_text("\n".join(md))
    print("wrote", OUT / "LISTING_COPY.md", "and listing.json")


if __name__ == "__main__":
    build()
