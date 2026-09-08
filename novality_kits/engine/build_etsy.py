"""Etsy listing kit for any pattern: 10 listing images (2000x2000) + SEO copy (LISTING_COPY.md, listing.json).

Usage: python engine/build_etsy.py <slug> [...]   -> out/<slug>/etsy/
Run after build_pdf.py (page previews). Audio/video durations are read from out/<slug>/audio if present.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pymupdf
from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.path.insert(0, str(Path(__file__).parent))
from common import FONTS, IMG_ROOT, OUT_ROOT, hex_rgb, load_pattern  # noqa: E402
from narration import chapters  # noqa: E402

S = 2000
WHITE = (255, 255, 255)

# title <= 140 chars, 13 tags each <= 20 chars (asserted at build time)
SEO = {
    "axel": ("Axolotl Crochet Pattern PDF, Amigurumi Axolotl Plush with Video & Audio Tutorial, Fluffy Gills Toy, Advanced Beginner, Axel the Axolotl",
             ["axolotl crochet", "amigurumi axolotl", "crochet axolotl toy", "axolotl pattern pdf", "crochet pattern pdf", "amigurumi pattern",
              "crochet toy pattern", "beginner crochet toy", "video tutorial", "kawaii crochet", "crochet plushie", "fluffy gills axolotl", "instant download pdf"]),
    "coco": ("Capybara Crochet Pattern PDF, Amigurumi Capybara Plush with Video & Audio Tutorial, No-Sew Legs, Sleepy Face Toy, Coco the Capybara",
             ["capybara crochet", "amigurumi capybara", "capybara plush toy", "capybara pattern pdf", "crochet pattern pdf", "amigurumi pattern",
              "crochet toy pattern", "video tutorial", "kawaii crochet", "crochet plushie", "capybara plushie", "instant download pdf", "intermediate crochet"]),
    "ember": ("Baby Dragon Crochet Pattern PDF, Amigurumi Dragon Plush with Wings & Spikes, Video & Audio Tutorial, Intermediate, Ember the Dragon",
              ["dragon crochet", "amigurumi dragon", "crochet dragon plush", "baby dragon pattern", "crochet pattern pdf", "amigurumi pattern",
               "crochet toy pattern", "video tutorial", "fantasy crochet", "crochet plushie", "dragon plushie pdf", "instant download pdf", "intermediate crochet"]),
    "hamish": ("Highland Cow Crochet Pattern PDF, Amigurumi Highland Cow Plush with Fringe & Scarf, Video & Audio Tutorial, 3 Sizes, Hamish the Cow",
               ["highland cow crochet", "amigurumi cow", "crochet cow plush", "highland cow pattern", "crochet pattern pdf", "amigurumi pattern",
                "crochet toy pattern", "video tutorial", "scottish cow plush", "crochet plushie", "hairy coo crochet", "instant download pdf", "intermediate crochet"]),
    "halloween": ("Halloween Crochet Pattern Set PDF, 3 Mini Amigurumi: Ghost, Pumpkin & Bat, Kawaii Ornaments with Video & Audio Tutorial, Instant Download",
                  ["halloween crochet", "crochet ghost", "crochet pumpkin", "crochet bat pattern", "amigurumi halloween", "mini amigurumi",
                   "crochet pattern pdf", "kawaii crochet", "halloween ornament", "video tutorial", "crochet pattern set", "instant download pdf", "spooky cute crochet"]),
    "duck": ("Duck Crochet Pattern PDF, Chunky Chenille Duck Plushie, One-Piece Seamless Amigurumi with Video & Audio Tutorial, Beginner Friendly",
             ["duck crochet pattern", "amigurumi duck", "crochet duck plush", "chenille crochet", "crochet pattern pdf", "amigurumi pattern",
              "beginner crochet toy", "video tutorial", "kawaii crochet", "crochet plushie", "duckling plushie", "instant download pdf", "no sew amigurumi"]),
    "momo": ("Loaf Cat Crochet Pattern PDF, Amigurumi Cat Loaf Plush, No-Sew Ears & Tail, Video & Audio Tutorial, Advanced Beginner, Momo the Cat",
             ["cat crochet pattern", "amigurumi cat", "crochet cat loaf", "cat loaf plush", "crochet pattern pdf", "amigurumi pattern",
              "crochet toy pattern", "video tutorial", "kawaii crochet cat", "crochet plushie", "chonky cat crochet", "instant download pdf", "beginner amigurumi"]),
    "trio": ("Mini Amigurumi Crochet Pattern Set PDF, Sunflower, Penguin & Potato Pocket Pals, Beginner Friendly with Video & Audio Tutorial",
             ["mini amigurumi", "crochet sunflower", "crochet penguin", "crochet potato", "pocket hug crochet", "crochet pattern pdf",
              "amigurumi set", "beginner crochet", "video tutorial", "kawaii crochet", "crochet keychain", "instant download pdf", "positivity gift"]),
    "shelby": ("Sea Turtle Keychain Crochet Pattern PDF, Amigurumi Turtle Bag Charm in 2 Sizes, 30-Minute Make with Video & Audio Tutorial, Easy",
               ["turtle crochet", "amigurumi turtle", "crochet keychain", "crochet bag charm", "sea turtle crochet", "crochet pattern pdf",
                "mini amigurumi", "easy crochet pattern", "video tutorial", "kawaii crochet", "crochet keyring pdf", "instant download pdf", "quick crochet gift"]),
    "willow": ("Bunny Lovey Crochet Pattern PDF, Granny Square Security Blanket with Bunny Head, Baby Comforter with Video & Audio Tutorial",
               ["bunny lovey crochet", "crochet lovey", "security blanket", "granny square lovey", "crochet baby blanket", "crochet pattern pdf",
                "amigurumi bunny", "baby shower gift", "video tutorial", "crochet comforter", "bunny blanket pdf", "instant download pdf", "beginner crochet"]),
}


def font(name, size):
    files = {"display": "FredokaOne-Regular.ttf", "sans": "SourceSansPro-Regular.ttf", "semi": "SourceSansPro-Semibold.ttf",
             "bold": "SourceSansPro-Bold.ttf", "it": "SourceSansPro-It.ttf", "serif_it": "Caladea-Italic.ttf"}
    return ImageFont.truetype(str(FONTS / files[name]), size)


def fit(path, w, h):
    im = Image.open(path).convert("RGB"); sc = max(w / im.width, h / im.height)
    im = im.resize((int(im.width * sc) + 1, int(im.height * sc) + 1), Image.LANCZOS)
    x = (im.width - w) // 2; y = (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))


def rmask(w, h, r):
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=r, fill=255); return m


def wrap(d, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=fnt) <= max_w: cur = t
        else: lines.append(cur); cur = w_
    if cur: lines.append(cur)
    return lines


def text_block(d, xy, text, fnt, fill, max_w, lh=None, max_lines=None):
    x, y = xy; lh = lh or int(fnt.size * 1.25)
    lines = wrap(d, text, fnt, max_w)
    if max_lines: lines = lines[:max_lines]
    for ln in lines: d.text((x, y), ln, font=fnt, fill=fill); y += lh
    return y


def mp3_duration(path):
    import imageio_ffmpeg
    out = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-i", str(path)], capture_output=True, text=True).stderr
    m = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", out)
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3)) if m else 0


def short_name(title):
    return title.split(" the ")[0] if " the " in title else title


class Kit:
    def __init__(self, slug):
        self.P = P = load_pattern(slug); self.slug = slug
        pal = P["palette"]
        self.ACC, self.DEEP, self.PALE = hex_rgb(pal["accent"]), hex_rgb(pal["deep"]), hex_rgb(pal["pale"])
        self.CREAM, self.INK, self.SOFT, self.RULE = hex_rgb(pal["cream"]), hex_rgb(pal["ink"]), hex_rgb(pal["ink_soft"]), hex_rgb(pal["rule"])
        self.img = IMG_ROOT / slug
        self.out_dir = OUT_ROOT / slug; self.out = self.out_dir / "etsy"; self.out.mkdir(parents=True, exist_ok=True)
        self.pdf = self.out_dir / f"{P['file_stem']}_Pattern.pdf"
        self.pages = len(pymupdf.open(str(self.pdf))) if self.pdf.exists() else 12
        self.chapters = chapters(P)
        audio = self.out_dir / "audio"
        clips = [audio / f"{c['slug']}.mp3" for c in self.chapters]
        if all(c.exists() for c in clips): secs = sum(mp3_duration(c) for c in clips)
        else: secs = sum(len(c["text"]) for c in self.chapters) / 870 * 60
        self.minutes = max(1, round(secs / 60))
        self.rounds = sum(1 for s in P["sections"] for t in s.get("tables", []) for r in t["rounds"] if isinstance(r[2], int) and not t["heading"].startswith("Total dc"))
        self.title, self.tags = SEO[slug]
        assert len(self.title) <= 140, (slug, len(self.title))
        bad = [t for t in self.tags if len(t) > 20]
        assert len(self.tags) == 13 and not bad, (slug, bad)

    def photo(self, key):
        p = self.img / self.P["images"][key]
        return p if p.exists() else self.img / self.P["images"]["hero"]

    def canvas(self):
        im = Image.new("RGB", (S, S), self.CREAM)
        blob = Image.new("RGB", (S, S), self.CREAM); bd = ImageDraw.Draw(blob)
        bd.ellipse((S - 700, -500, S + 300, 500), fill=self.PALE); bd.ellipse((-400, S - 500, 400, S + 300), fill=self.PALE)
        im.paste(blob.filter(ImageFilter.GaussianBlur(70)))
        return im

    def chip(self, d, xy, text, fnt, fill=None, fg=WHITE, pad=(28, 14)):
        x, y = xy; w = d.textlength(text, font=fnt) + pad[0] * 2; h = fnt.size + pad[1] * 2
        d.rounded_rectangle((x, y, x + w, y + h), radius=h // 2, fill=fill or self.DEEP)
        d.text((x + pad[0], y + pad[1] - 2), text, font=fnt, fill=fg)
        return w

    def shadow_paste(self, base, im, xy, radius=48, blur=40, alpha=80):
        w, h = im.size
        sh = Image.new("RGBA", (w + blur * 3, h + blur * 3), (0, 0, 0, 0))
        ImageDraw.Draw(sh).rounded_rectangle((blur, blur + 20, w + blur, h + blur + 20), radius=radius, fill=(*self.DEEP, alpha))
        sh = sh.filter(ImageFilter.GaussianBlur(blur // 2))
        base.paste(sh, (xy[0] - blur, xy[1] - blur), sh); base.paste(im, xy, rmask(w, h, radius))

    def footer(self, d):
        d.text((S // 2, S - 70), f"{self.P['brand']}  ·  Design {self.P['design_code']}  ·  PDF pattern, {self.P['terms']}", font=font("semi", 30), fill=self.SOFT, anchor="mm")

    def heading(self, d, title, sub, y=150):
        size = 110
        while d.textlength(title, font=font("display", size)) > S - 200: size -= 4
        d.text((S // 2, y), title, font=font("display", size), fill=self.DEEP, anchor="mm")
        if sub:
            f = font("serif_it", 44)
            while d.textlength(sub, font=f) > S - 200: f = font("serif_it", f.size - 2)
            d.text((S // 2, y + 100), sub, font=f, fill=self.SOFT, anchor="mm")

    # ------------------------------------------------------------- images
    def img01(self):
        """Thumbnail-first: full-bleed hero with a compact badge - must read at 200 px."""
        P = self.P; im = fit(self.photo("hero"), S, S); d = ImageDraw.Draw(im, "RGBA")
        for y in range(S - 620, S):
            a = int(230 * ((y - (S - 620)) / 620) ** 1.4); d.line((0, y, S, y), fill=(*self.DEEP, a))
        d = ImageDraw.Draw(im); size = 150
        while d.textlength(P["title"], font=font("display", size)) > S - 200: size -= 6
        d.text((100, S - 470), P["title"], font=font("display", size), fill=WHITE)
        d.text((104, S - 300), f"{P['subtitle']}  ·  PDF", font=font("serif_it", 62), fill=WHITE)
        x = 104
        for c in (P["terms"], P["skill"], P["size_chip"]): x += self.chip(d, (x, S - 200), c, font("semi", 38), fill=WHITE, fg=self.DEEP) + 20
        d.ellipse((S - 420, 80, S - 80, 420), fill=WHITE)
        d.text((S - 250, 210), "PDF", font=font("display", 96), fill=self.DEEP, anchor="mm")
        d.text((S - 250, 300), "instant download", font=font("semi", 32), fill=self.SOFT, anchor="mm")
        return im

    def img02(self):
        """What's included."""
        P = self.P; im = self.canvas(); d = ImageDraw.Draw(im)
        self.heading(d, "What's included", f"Everything you need to make {short_name(P['title'])} - delivered instantly")
        self.shadow_paste(im, fit(self.photo("inhand"), 820, 820), (1080, 380))
        items = [(f"{self.pages}-page designed PDF", "cover, materials, techniques, every round in a table"),
                 ("Full narrated audio", f"~{self.minutes} min walkthrough in {len(self.chapters)} chapters - listen while you crochet"),
                 ("Tutorial video", "1080p round-by-round slides with captions and chapter markers"),
                 (f"{self.rounds} verified rounds", "every stitch count machine-checked, 0 errors"),
                 (f"{len(P['colorways'])} colourway ideas", ", ".join(c[0] for c in P["colorways"][:4]).lower() + ("..." if len(P["colorways"]) > 4 else "")),
                 ("Troubleshooting guide", f"{len(P['troubleshooting'])} common snags and their fixes")]
        y = 400
        for title, sub in items:
            d.ellipse((120, y + 14, 168, y + 62), fill=self.DEEP); d.text((144, y + 38), "✓", font=font("bold", 34), fill=WHITE, anchor="mm")
            d.text((200, y), title, font=font("semi", 46), fill=self.INK)
            d.text((200, y + 58), sub[:60], font=font("sans", 32), fill=self.SOFT); y += 150
        self.footer(d); return im

    def img03(self):
        """Size & key numbers."""
        P = self.P; im = self.canvas(); d = ImageDraw.Draw(im)
        self.shadow_paste(im, fit(self.photo("hero"), 1100, 1100), (450, 120))
        self.heading(d, "Finished size", None, y=1330)
        d.text((S // 2, 1420), P["size_chip"], font=font("serif_it", 52), fill=self.SOFT, anchor="mm")
        cw = 420; x0 = (S - (cw * 4 + 60)) // 2
        for i, (num, lab) in enumerate(P["stats"]):
            x = x0 + i * (cw + 20)
            d.rounded_rectangle((x, 1500, x + cw, 1760), radius=36, fill=WHITE, outline=self.RULE, width=3)
            f = font("display", 84)
            while d.textlength(num, font=f) > cw - 40: f = font("display", f.size - 4)
            d.text((x + cw // 2, 1600), num, font=f, fill=self.DEEP, anchor="mm")
            d.text((x + cw // 2, 1690), lab.title(), font=font("semi", 28), fill=self.SOFT, anchor="mm")
        self.footer(d); return im

    def img04(self):
        """Materials & gauge."""
        P = self.P; im = self.canvas(); d = ImageDraw.Draw(im)
        self.shadow_paste(im, fit(self.photo("detail"), 900, 900), (60, 520))
        d.text((100, 120), "Materials", font=font("display", 110), fill=self.DEEP)
        d.text((104, 250), P["materials"][0][1].split(",")[0][:60], font=font("serif_it", 44), fill=self.SOFT)
        y = 480
        for k, v in P["materials"]:
            d.text((1030, y), k.upper(), font=font("semi", 28), fill=self.DEEP); y += 38
            y = text_block(d, (1030, y), v, font("sans", 33), self.INK, 900, lh=42, max_lines=3) + 24
            if y > 1520: break
        d.rounded_rectangle((1030, 1580, 1940, 1760), radius=30, fill=self.PALE)
        d.text((1060, 1605), "GAUGE", font=font("semi", 28), fill=self.DEEP)
        text_block(d, (1060, 1645), P["gauge"], font("sans", 30), self.INK, 850, lh=38, max_lines=3)
        self.footer(d); return im

    def img05(self):
        """Real pages from the PDF."""
        im = self.canvas(); d = ImageDraw.Draw(im)
        self.heading(d, "Inside the PDF", f"{self.pages} designed pages - clear tables, photos, and notes exactly where you need them", y=140)
        doc = pymupdf.open(str(self.pdf)); n = len(doc)
        pages = [0, min(4, n - 1), min(6, n - 1), max(0, n - 4)]
        pw = 560; ph = int(pw * 1.414); xs = [70, 550, 1030, 1510]
        for k, (pi, x) in enumerate(zip(pages, xs)):
            pix = doc[pi].get_pixmap(dpi=110)
            pg = Image.frombytes("RGB", (pix.width, pix.height), pix.samples).resize((pw, ph), Image.LANCZOS)
            self.shadow_paste(im, pg, (x, 380 + (0 if k % 2 == 0 else 120)), radius=18, blur=30, alpha=70)
        d.rounded_rectangle((280, 1420, 1720, 1560), radius=40, fill=WHITE, outline=self.RULE, width=3)
        d.text((S // 2, 1490), "Every round in a table  ·  stitch counts on every row  ·  notes for eyes, stuffing and joins", font=font("semi", 34), fill=self.INK, anchor="mm")
        d.text((S // 2, 1700), "Prints beautifully on A4 or Letter  ·  reads perfectly on a phone or tablet", font=font("sans", 36), fill=self.SOFT, anchor="mm")
        self.footer(d); return im

    def img06(self):
        """Video + audio."""
        im = self.canvas(); d = ImageDraw.Draw(im)
        self.heading(d, "Watch it. Hear it. Make it.", "A narrated tutorial video and a chaptered audio walkthrough come with the pattern", y=140)
        frame = fit(self.photo("hero"), 1400, 788).filter(ImageFilter.GaussianBlur(3))
        frame = Image.blend(frame, Image.new("RGB", frame.size, self.DEEP), 0.45); fd = ImageDraw.Draw(frame)
        fd.ellipse((620, 314, 780, 474), fill=WHITE); fd.polygon([(680, 354), (680, 434), (750, 394)], fill=self.DEEP)
        fd.text((700, 560), f"Round-by-round tutorial  ·  {self.minutes} min  ·  1080p  ·  captions", font=font("semi", 36), fill=WHITE, anchor="mm")
        fd.rounded_rectangle((60, 720, 1340, 736), radius=8, fill=WHITE); fd.rounded_rectangle((60, 720, 520, 736), radius=8, fill=self.ACC)
        self.shadow_paste(im, frame, (300, 330), radius=36)
        d.rounded_rectangle((300, 1190, 1700, 1760), radius=40, fill=WHITE, outline=self.RULE, width=3)
        d.text((360, 1230), "AUDIO CHAPTERS", font=font("semi", 30), fill=self.DEEP)
        chs = [f"{i:02d} {c['title']}" for i, c in enumerate(self.chapters, start=1)][:10]
        for i, c in enumerate(chs):
            col = i % 2; row = i // 2; x = 360 + col * 680; y = 1290 + row * 88
            d.ellipse((x, y + 8, x + 40, y + 48), fill=self.PALE); d.polygon([(x + 14, y + 17), (x + 14, y + 39), (x + 30, y + 28)], fill=self.DEEP)
            f = font("sans", 34); txt = c
            while d.textlength(txt, font=f) > 600: txt = txt[:-2]
            d.text((x + 60, y + 6), txt, font=f, fill=self.INK)
        d.text((S // 2, 1830), "Listen while your hands are busy - every round is read out with its stitch count.", font=font("serif_it", 38), fill=self.SOFT, anchor="mm")
        self.footer(d); return im

    def img07(self):
        """Design details."""
        P = self.P; im = self.canvas(); d = ImageDraw.Draw(im)
        self.heading(d, f"The details that make {short_name(P['title'])}", None, y=140)
        self.shadow_paste(im, fit(self.photo("detail"), 900, 900), (80, 260)); self.shadow_paste(im, fit(self.photo("inhand"), 900, 900), (1020, 260))
        cw = 430; x0 = (S - (cw * 4 + 60)) // 2
        for i, (num, lab) in enumerate(P["feats"]):
            x = x0 + i * (cw + 20)
            d.rounded_rectangle((x, 1240, x + cw, 1560), radius=36, fill=WHITE, outline=self.RULE, width=3)
            f = font("display", 96)
            while d.textlength(num, font=f) > cw - 40: f = font("display", f.size - 4)
            d.text((x + cw // 2, 1330), num, font=f, fill=self.DEEP, anchor="mm")
            for j, ln in enumerate(wrap(d, lab.replace("\n", " "), font("semi", 30), cw - 40)[:3]):
                d.text((x + cw // 2, 1410 + j * 38), ln, font=font("semi", 30), fill=self.INK, anchor="mm")
        for j, line in enumerate(P["tagline"]):
            f = font("serif_it", 38)
            while d.textlength(line, font=f) > S - 200: f = font("serif_it", f.size - 2)
            d.text((S // 2, 1680 + j * 55), line, font=f, fill=self.SOFT, anchor="mm")
        self.footer(d); return im

    def img08(self):
        """Colourways."""
        P = self.P; im = self.canvas(); d = ImageDraw.Draw(im)
        self.heading(d, "Make it yours", P["colorways_caption"].split(". ")[0][:90], y=140)
        self.shadow_paste(im, fit(self.photo("colorways"), 1800, 900), (100, 320))
        cw = P["colorways"]; n = len(cw); gap = 1800 // n
        for i, (name, c1, c2) in enumerate(cw):
            cx = 100 + gap * i + gap // 2
            d.ellipse((cx - 90, 1320, cx + 90, 1500), fill=hex_rgb(c1), outline=WHITE, width=6)
            d.ellipse((cx + 30, 1440, cx + 130, 1540), fill=hex_rgb(c2), outline=WHITE, width=6)
            d.text((cx, 1600), name, font=font("semi", 30), fill=self.INK, anchor="mm")
        d.text((S // 2, 1740), "Same pattern, same counts - just swap the yarn colours.", font=font("serif_it", 38), fill=self.SOFT, anchor="mm")
        self.footer(d); return im

    def img09(self):
        """Skill level & techniques."""
        P = self.P; im = self.canvas(); d = ImageDraw.Draw(im)
        self.heading(d, "Skill level", f"{P['skill']}  ·  {P['terms']}  ·  {P['time']}", y=140)
        self.shadow_paste(im, fit(self.photo("inhand"), 820, 820), (1080, 340))
        d.text((120, 360), "YOU WILL USE", font=font("semi", 30), fill=self.DEEP)
        y = 420
        for i, (name, _) in enumerate(P["techniques"], start=1):
            d.ellipse((120, y + 6, 176, y + 62), fill=self.PALE); d.text((148, y + 34), str(i), font=font("display", 32), fill=self.DEEP, anchor="mm")
            d.text((200, y + 8), name, font=font("semi", 42), fill=self.INK); y += 96
            if y > 1150: break
        d.rounded_rectangle((120, 1300, 1880, 1560), radius=40, fill=WHITE, outline=self.RULE, width=3)
        d.text((160, 1340), "EVERY TECHNIQUE IS EXPLAINED", font=font("semi", 30), fill=self.DEEP)
        text_block(d, (160, 1390), "Step-by-step in the PDF, read aloud in the audio, and shown on the video slides. " + P["techniques"][0][1], font("sans", 34), self.INK, 1680, lh=44, max_lines=3)
        d.text((S // 2, 1700), ("Troubleshooting covers: " + "; ".join(q.rstrip("?.") for q, _ in P["troubleshooting"][:3]))[:110], font=font("sans", 32), fill=self.SOFT, anchor="mm")
        self.footer(d); return im

    def img10(self):
        """Good to know - digital file, terms."""
        P = self.P; im = self.canvas(); d = ImageDraw.Draw(im)
        self.shadow_paste(im, fit(self.photo("hero"), 760, 760), (1160, 160))
        d.text((100, 130), "Good to know", font=font("display", 100), fill=self.DEEP)
        blocks = [("THIS IS A DIGITAL PATTERN", "You are buying the PDF + audio + video files, not the finished item. Files are available to download immediately after purchase - nothing will be shipped."),
                  ("YOU MAY", f"Make as many as you like for yourself, gifts or charity, and sell finished items in small batches with credit to {P['brand']}."),
                  ("YOU MAY NOT", "Resell, share or redistribute the files, or claim the design as your own."),
                  ("NEED HELP?", "Message us any time - every round is count-checked, and we love helping makers finish.")]
        y = 300
        for k, v in blocks:
            d.text((100, y), k, font=font("semi", 32), fill=self.DEEP); y += 46
            y = text_block(d, (100, y), v, font("sans", 38), self.INK, 980, lh=48) + 46
        d.rounded_rectangle((100, 1560, 1900, 1760), radius=40, fill=self.DEEP)
        d.text((S // 2, 1630), f"Design Code {P['design_code']}  ·  © {P['year']} {P['brand']}", font=font("semi", 40), fill=WHITE, anchor="mm")
        d.text((S // 2, 1700), "  ".join(P["hashtags"]), font=font("sans", 34), fill=self.PALE, anchor="mm")
        self.footer(d); return im

    # ------------------------------------------------------------- copy
    def copy(self):
        P = self.P; B = P["brand"]; name = P["title"]
        mats = "\n".join(f"• {k}: {v}" for k, v in P["materials"])
        techs = ", ".join(n.lower() for n, _ in P["techniques"])
        cws = " · ".join(c[0] for c in P["colorways"])
        pieces = "\n".join(f"• {re.sub(r'^[0-9]+ [·.] ', '', s['title'])}" + (f" - {s['lead']}" if s.get("lead") else "") for s in P["sections"])
        desc = f"""🧶 {name.upper()} - crochet pattern (PDF + audio + video)

{P['intro']}

Finished size: {P['size_chip']}. {P['gauge']}

✨ WHAT YOU GET (instant download)
• {self.pages}-page designed PDF pattern - every round in a clear table with stitch counts, photos and notes exactly where you need them
• Narrated audio walkthrough (~{self.minutes} min, {len(self.chapters)} chapters) - every round read aloud so you can crochet without looking at the page
• Tutorial video (1080p, ~{self.minutes} min) - round-by-round slides that highlight the row being spoken, with captions and chapter markers
• Techniques explained step by step: {techs}
• Assembly guide with exact placement for every piece
• Troubleshooting page ({len(P['troubleshooting'])} common snags) and {len(P['colorways'])} colourway ideas

🧩 WHAT YOU WILL MAKE
{pieces}

✅ EVERY STITCH COUNT VERIFIED
All {self.rounds} rounds were machine-checked with a deterministic pattern validator: zero errors. The maths adds up, so you can trust the counts.

🧶 YOU WILL NEED
{mats}

📏 SKILL LEVEL
{P['skill']} - {P['terms']}. About {P['time']} from start to finish.

🎨 COLOURWAYS
{cws} - {P['colorways_caption']}

📄 THIS IS A DIGITAL FILE
No physical item will be shipped. Files are available in your Etsy account under Purchases immediately after payment. Because this is an instant download, refunds cannot be offered - but message us any time and we will help you finish.

📜 TERMS OF USE
{P['terms_may']} Please do not resell, share, translate or redistribute the files, or claim the design as your own.

Design Code {P['design_code']} · © {P['year']} {B}.
Tag your makes with {P['hashtags'][0]} and {P['hashtags'][1]} - we love seeing them!
"""
        faq = [("Is this a physical item?", f"No - this listing is for the digital pattern (PDF + audio + video). You make {short_name(name)} yourself."),
               ("What terms does the pattern use?", f"{P['terms']}. " + ", ".join(f"{a} = {b}" for a, b in P["abbreviations"][:4]) + "."),
               ("How long does it take?", f"About {P['time']} for a {P['skill'].lower()} crocheter."),
               ("Can I sell what I make?", f"Yes - small-batch sales are welcome with credit to {B}. Mass production needs written permission."),
               ("Can I get a refund?", "Digital downloads cannot be refunded once delivered, but message us with any problem and we will help you finish."),
               (P["troubleshooting"][0][0], P["troubleshooting"][0][1])]
        listing = {"title": self.title, "tags": self.tags, "category": "Craft Supplies & Tools > Patterns & How To > Patterns & Blueprints > Crochet Patterns",
                   "type": "Digital download", "who_made": "I did", "what_is_it": "A supply or tool to make things", "when_made": "Made to order",
                   "materials_field": "PDF, MP3 audio, MP4 video",
                   "files": [f"{P['file_stem']}_Pattern.pdf ({self.pages} pages)", f"{P['file_stem']}_Full_Walkthrough.mp3 (~{self.minutes} min) + {len(self.chapters)} chapter MP3s",
                             f"{P['file_stem']}_Tutorial.mp4 (1080p, ~{self.minutes} min) - if it exceeds Etsy's 20 MB per-file limit, host it on an unlisted video link and include the link in the PDF or a 'links' PDF"],
                   "description": desc, "faq": faq,
                   "shop_announcement": f"New: {name} 🧶 - {P['tagline'][0].rstrip(',.')}. Narrated audio walkthrough + round-by-round video, every stitch count verified. {P['skill']}, {P['terms']}, {P['time']}.",
                   "message_to_buyer": f"""Thank you so much for buying {name}! 🧶

Your files are ready under Purchases and Reviews > Download Files:
• {P['file_stem']}_Pattern.pdf - the full {self.pages}-page pattern
• {P['file_stem']}_Full_Walkthrough.mp3 - the narrated audio walkthrough (plus {len(self.chapters)} chapter files)
• Tutorial video - see the last page of the PDF for the link and chapter markers

A quick tip before you start: check your gauge - {P['gauge'].split('.')[0]}.

If anything is unclear, just reply to this message. Tag your finished make with {P['hashtags'][0]} {P['hashtags'][1]} - we would love to see it!

Happy crocheting,
{B}
"""}
        return listing

    def build(self):
        fns = [("01_cover.jpg", self.img01), ("02_whats_included.jpg", self.img02), ("03_size.jpg", self.img03), ("04_materials.jpg", self.img04),
               ("05_pdf_preview.jpg", self.img05), ("06_video_audio.jpg", self.img06), ("07_details.jpg", self.img07), ("08_colorways.jpg", self.img08),
               ("09_skill_level.jpg", self.img09), ("10_good_to_know.jpg", self.img10)]
        for name, fn in fns:
            fn().save(self.out / name, quality=90, optimize=True, progressive=True)
        L = self.copy()
        (self.out / "listing.json").write_text(json.dumps(L, indent=2, ensure_ascii=False))
        md = [f"# Etsy listing kit - {self.P['title']}", "", "## Title (140 chars max)", "", L["title"], f"\n_{len(L['title'])} characters_", "", "## Tags (13, each <= 20 chars)", ""]
        md += [f"- `{t}` ({len(t)})" for t in L["tags"]]
        md += ["", "## Listing settings", "", f"- Category: {L['category']}", f"- Type: {L['type']}", f"- Who made it / What is it / When: {L['who_made']} / {L['what_is_it']} / {L['when_made']}",
               f"- Materials field: {L['materials_field']}", "", "## Files to upload", ""] + [f"- {f}" for f in L["files"]]
        md += ["", "## Images (upload in this order)", ""] + [f"{i+1}. `{n}` - {fn.__doc__.strip()}" for i, (n, fn) in enumerate(fns)]
        md += ["", "## Description", "", "```", L["description"], "```", "", "## FAQ", ""] + [f"**{q}**  \n{a}\n" for q, a in L["faq"]]
        md += ["## Shop announcement", "", L["shop_announcement"], "", "## Automatic message to buyers", "", "```", L["message_to_buyer"], "```"]
        (self.out / "LISTING_COPY.md").write_text("\n".join(md))
        return self.out


if __name__ == "__main__":
    for slug in sys.argv[1:]:
        print("wrote", Kit(slug).build())
