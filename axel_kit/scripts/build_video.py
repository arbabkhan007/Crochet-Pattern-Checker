"""Build the narrated Axel tutorial video (1920x1080, H.264 + AAC) from the chapter audio.

Each chapter = one designed slide. Slides that walk through rounds highlight the rows
progressively across the chapter's duration; slides also carry a subtitle strip built
from the narration sentences and a global progress bar.

Usage: python build_video.py           -> ../video/Axel_the_Axolotl_Tutorial.mp4
       python build_video.py --preview -> only renders the still frames to /tmp/frames
"""
from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from pathlib import Path

import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.path.insert(0, str(Path(__file__).parent))
import narration as N  # noqa: E402
import pattern_data as P  # noqa: E402

KIT = Path(__file__).resolve().parent.parent
IMG = KIT / "assets" / "img"
FONTS = KIT / "assets" / "fonts"
AUDIO = KIT / "audio"
OUT_DIR = KIT / "video"
OUT = OUT_DIR / "Axel_the_Axolotl_Tutorial.mp4"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

W, H = 1920, 1080
FPS = 12  # slideshow - low fps keeps the file small; audio is untouched

# palette (RGB)
CREAM = (255, 251, 247); PINK = (232, 169, 184); PINK_DEEP = (184, 80, 111); PINK_PALE = (251, 238, 241)
INK = (59, 47, 51); INK_SOFT = (122, 106, 112); RULE = (235, 215, 221); WHITE = (255, 255, 255)
HILITE = (247, 220, 227); MINT = (60, 156, 147)

IMAGES = {"hero": "hero_axel.png", "flatlay": "flatlay_materials.png", "wip": "wip_hands.png", "gills": "detail_gills.png",
          "tail": "detail_tail.png", "inhand": "in_hand_scale.png", "colorways": "colorways.png"}


def font(name, size):
    files = {"display": "FredokaOne-Regular.ttf", "sans": "SourceSansPro-Regular.ttf", "semi": "SourceSansPro-Semibold.ttf",
             "bold": "SourceSansPro-Bold.ttf", "it": "SourceSansPro-It.ttf", "serif_it": "Caladea-Italic.ttf"}
    return ImageFont.truetype(str(FONTS / files[name]), size)


F_TITLE = font("display", 58); F_KICK = font("semi", 26); F_BODY = font("sans", 30); F_SMALL = font("sans", 24)
F_ROW = font("sans", 28); F_ROW_B = font("semi", 28); F_CNT = font("display", 28); F_NOTE = font("it", 22)
F_SUB = font("semi", 34); F_BIG = font("display", 96); F_CHAP = font("semi", 24)


# ------------------------------------------------------------------ slide content
def rows_for(slug):
    """Which rounds table (if any) a chapter shows."""
    if slug == "04_head": return [("Head & neck  ·  R1 - R13", P.BODY_ROUNDS[:13])]
    if slug == "05_body": return [("Body  ·  R14 - R26", P.BODY_ROUNDS[13:26])]
    if slug == "06_tail": return [("Tail  ·  R27 - R36", P.BODY_ROUNDS[26:])]
    if slug == "07_arms_feet": return [("Arms - make 2", P.ARM_ROUNDS), ("Feet - make 2", P.FEET_ROUNDS)]
    if slug == "08_gills": return [("Gills - make 6", P.GILL_ROUNDS)]
    return []


BULLETS = {
    "01_welcome": ["11.5 cm / 4.5 in tall seated  ·  10 cm gill tip to tip", "US terms  ·  Advanced beginner  ·  2.5 - 3 hours",
                   "Head, neck, body & tail: one continuous spiral", "6 fluffy gills  ·  5-scallop shell fin  ·  2 arms  ·  2 feet"],
    "02_safety_materials": ["Main yarn: worsted #4 pale pink, ~15 g (smooth, matte)", "Gill yarn: fuzzy / eyelash fur, dark pink, ~8 g",
                            "Fin yarn: worsted #4 dark pink, ~3 g, smooth", "Hook 3.5 mm (US E/4)  ·  two 6 mm safety eyes",
                            "Filling ~8 g  ·  tapestry needle  ·  black floss  ·  pink pastel  ·  stitch marker",
                            "Gauge: 36 sc around = ~52 mm across when stuffed", "Under 3 years: embroider the eyes instead"],
    "03_techniques": ["1  Magic ring - every piece starts here", "2  Spiral - no join, no ch 1, move the marker each round",
                      "3  Invisible decrease - front loops only, no ridge", "4  Close through both layers - 6 sts fold to 3 pairs, 3 sc",
                      "5  Shell / scallop - 5 dc in one st, sl st to anchor"],
    "09_fin": ["Join dark pink with sl st at the very tail tip", "* 5 dc in next ridge st, sl st in next ridge st", "Repeat from * 5 times = 5 scallops, FO",
               "2 ridge sts per scallop -> 10 sts = 10 tail rounds", "Work the dc loosely - the ruffle is the look"],
    "10_assembly": ["Check: 1 body · 2 arms · 2 feet · 6 gills · 1 fin", "Eyes: between R7 / R8, 6 sts apart  ·  pull-test",
                    "Smile: shallow U across R8 - R9, ~5 sts wide  ·  Blush under eyes", "Gills: 3 per side at R6 (up), R7-8 (out), R9 (down)",
                    "Arms: R17 - R18, 6 sts from centre front", "Feet: R24 - R25, 4 sts from centre - so Axel sits"],
}


def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]


_NUM_WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
              "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17,
              "eighteen": 18, "nineteen": 19, "twenty": 20, "thirty": 30}


def _spoken_round(sentence):
    """Return the round number a narration sentence starts with ("Round twenty-four: ..."), else None."""
    m = re.match(r"\s*Rounds?\s+([a-z\-]+)", sentence, re.IGNORECASE)
    if not m: return None
    parts = m.group(1).lower().split("-")
    n = 0
    for w_ in parts:
        if w_ not in _NUM_WORDS: return None
        n += _NUM_WORDS[w_]
    return n


# ------------------------------------------------------------------ drawing helpers
def rounded(draw, box, r, fill):
    draw.rounded_rectangle(box, radius=r, fill=fill)


def fit_image(path, box_w, box_h):
    im = Image.open(path).convert("RGB")
    scale = max(box_w / im.width, box_h / im.height)
    im = im.resize((int(im.width * scale) + 1, int(im.height * scale) + 1), Image.LANCZOS)
    x = (im.width - box_w) // 2; y = (im.height - box_h) // 2
    return im.crop((x, y, x + box_w, y + box_h))


def round_mask(w, h, r):
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=r, fill=255); return m


def wrap(draw, text, fnt, max_w):
    words = text.split(); lines = []; cur = ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if draw.textlength(t, font=fnt) <= max_w: cur = t
        else: lines.append(cur); cur = w_
    if cur: lines.append(cur)
    return lines


def base_frame(idx, total, title, image_key, progress):
    """Background, header, photo and chapter chrome. Returns (image, draw, content_box)."""
    im = Image.new("RGB", (W, H), CREAM); d = ImageDraw.Draw(im)
    # soft blobs
    blob = Image.new("RGB", (W, H), CREAM); bd = ImageDraw.Draw(blob)
    bd.ellipse((W - 420, -260, W + 200, 300), fill=PINK_PALE); bd.ellipse((-260, H - 300, 260, H + 200), fill=PINK_PALE)
    im.paste(blob.filter(ImageFilter.GaussianBlur(40)))
    d = ImageDraw.Draw(im)
    # header
    d.text((80, 44), P.TITLE, font=font("display", 30), fill=PINK_DEEP)
    d.text((W - 80, 52), f"{P.DESIGNER}  ·  Design {P.DESIGN_CODE}  ·  {P.TERMS}", font=F_CHAP, fill=INK_SOFT, anchor="ra")
    d.line((80, 96, W - 80, 96), fill=RULE, width=2)
    # chapter kicker + title
    d.text((80, 122), f"CHAPTER {idx} OF {total}", font=F_KICK, fill=PINK_DEEP)
    d.text((80, 152), title, font=F_TITLE, fill=INK)
    # photo, right column
    pw, ph = 640, 640
    px, py = W - 80 - pw, 236
    photo = fit_image(IMG / IMAGES[image_key], pw, ph)
    shadow = Image.new("RGBA", (pw + 60, ph + 60), (0, 0, 0, 0)); sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle((30, 40, pw + 30, ph + 40), radius=36, fill=(184, 80, 111, 70))
    shadow = shadow.filter(ImageFilter.GaussianBlur(24))
    im.paste(shadow, (px - 30, py - 30), shadow)
    im.paste(photo, (px, py), round_mask(pw, ph, 36))
    # progress bar + subtitle strip drawn later per-frame
    return im, (80, 236, px - 60, H - 200)


def draw_table(d, box, heading, rows, active_upto, y, compact=False):
    rh = 38 if compact else 44
    x0, _, x1, _ = box
    d.text((x0, y), heading, font=font("display", 30 if compact else 34), fill=PINK_DEEP); y += (44 if compact else 52)
    col_r, col_i, col_c, col_n = x0, x0 + 110, x0 + 640, x0 + 740
    rounded(d, (x0 - 10, y - 4, x1, y + 36), 8, PINK_PALE)
    for cx, lab in ((col_r, "Rnd"), (col_i, "Instruction"), (col_c, "Sts"), (col_n, "Note")):
        d.text((cx, y + 2), lab, font=F_KICK, fill=PINK_DEEP)
    y += 46
    for k, (rn, instr, cnt, note) in enumerate(rows):
        active = k == active_upto; done = k < active_upto
        if active: rounded(d, (x0 - 10, y - 6, x1, y + 38), 8, HILITE)
        col = INK if (done or active) else (170, 158, 162)
        d.text((col_r, y), f"R{rn}", font=F_ROW_B, fill=PINK_DEEP if active else col)
        d.text((col_i, y), instr, font=F_ROW, fill=col)
        d.text((col_c, y), f"({cnt})", font=F_CNT, fill=PINK_DEEP if (done or active) else (214, 170, 184))
        if note: d.text((col_n, y), note, font=F_NOTE, fill=INK_SOFT if (done or active) else (190, 180, 184))
        if active:
            d.polygon([(x0 - 34, y + 8), (x0 - 34, y + 26), (x0 - 20, y + 17)], fill=PINK_DEEP)
        y += rh
    return y + (8 if compact else 18)


def draw_bullets(d, box, items, active_upto, y):
    x0, _, x1, _ = box
    for k, t in enumerate(items):
        active = k == active_upto; done = k < active_upto
        if active: rounded(d, (x0 - 10, y - 8, x1, y + 48), 10, HILITE)
        d.ellipse((x0, y + 12, x0 + 16, y + 28), fill=PINK_DEEP if (done or active) else RULE)
        for i, line in enumerate(wrap(d, t, F_BODY, x1 - x0 - 50)):
            d.text((x0 + 36, y + i * 36), line, font=F_BODY, fill=INK if (done or active) else (170, 158, 162))
        y += 36 * max(1, len(wrap(d, t, F_BODY, x1 - x0 - 50))) + 22
    return y


def draw_footer(d, im, subtitle, progress, chapter_progress):
    # subtitle strip
    rounded(d, (80, H - 170, W - 80, H - 70), 22, (255, 255, 255))
    d.rounded_rectangle((80, H - 170, W - 80, H - 70), radius=22, outline=RULE, width=2)
    lines = wrap(d, subtitle, F_SUB, W - 240)[:2]
    for i, line in enumerate(lines):
        d.text((W // 2, H - 150 + i * 42), line, font=F_SUB, fill=INK, anchor="ma")
    # global progress
    d.rounded_rectangle((80, H - 44, W - 80, H - 34), radius=5, fill=RULE)
    d.rounded_rectangle((80, H - 44, 80 + int((W - 160) * progress), H - 34), radius=5, fill=PINK)
    # chapter progress ticks
    d.text((80, H - 30), "progress", font=font("it", 18), fill=INK_SOFT)
    d.text((W - 80, H - 30), f"{int(progress * 100)}%", font=font("semi", 18), fill=INK_SOFT, anchor="ra")


# ------------------------------------------------------------------ frames per chapter
def audio_duration(path):
    out = subprocess.run([FFMPEG, "-i", str(path)], capture_output=True, text=True).stderr
    m = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", out)
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))


def chapter_frames(idx, total, slug, title, text, image_key, duration, t_offset, total_dur, frame_dir):
    """Render keyframes for one chapter; return list of (png_path, seconds)."""
    sents = sentences(text)
    n_sent = len(sents)
    tables = rows_for(slug); bullets = BULLETS.get(slug)
    # narrated units to sync: rows (for tables) or bullets - spread evenly across the chapter
    if tables:
        units = sum(len(r) for _, r in tables)
    elif bullets:
        units = len(bullets)
    else:
        units = 1
    # per-sentence timing (weighted by char count) drives subtitles; unit highlight follows the same clock
    total_chars = sum(len(s) for s in sents)
    # flat list of round numbers across the slide's tables, in display order
    flat_rounds = [rn for _, rows in tables for (rn, *_r) in rows] if tables else []
    # for multi-table slides (arms then feet) the second table restarts at R1: resolve by walking forward
    frames = []
    t = 0.0
    u_prev = -1; cursor = 0
    for si, sent in enumerate(sents):
        dur = duration * len(sent) / total_chars
        prog_start = t / duration
        if tables:
            rn = _spoken_round(sent)
            if rn is not None:
                # find next occurrence of rn at or after the cursor (handles "Rounds two to six" -> row R2)
                for j in range(cursor, len(flat_rounds)):
                    if flat_rounds[j] == rn: cursor = j; break
                u_prev = cursor
                # a range like "Rounds seventeen through twenty-two" / "Rounds two to six" highlights up to the end round
                m2 = re.match(r"\s*Rounds\s+[a-z\-]+(?:,\s*[a-z\-]+)*(?:\s+(?:and|to|through)\s+([a-z\-]+))", sent, re.IGNORECASE)
                if m2:
                    end_rn = _spoken_round("Round " + m2.group(1))
                    if end_rn is not None:
                        for j in range(cursor, len(flat_rounds)):
                            if flat_rounds[j] == end_rn: cursor = j; break
            elif si == 0:
                u_prev = -1
            u = u_prev if u_prev >= 0 else -1
        else:
            # unit index at the middle of this sentence
            u = min(units - 1, int(((t + dur / 2) / duration) * units))
        im, box = base_frame(idx, total, title, image_key, (t_offset + t) / total_dur)
        d = ImageDraw.Draw(im)
        y = box[1]
        if tables:
            offset = 0
            for heading, rows in tables:
                local = (u - offset) if u >= 0 else -1
                y = draw_table(d, box, heading, rows, local if 0 <= local < len(rows) else (len(rows) if local >= len(rows) else -1), y, compact=len(tables) > 1)
                offset += len(rows)
        elif bullets:
            y = draw_bullets(d, box, bullets, u, y)
        draw_footer(d, im, sent, (t_offset + t) / total_dur, prog_start)
        p = frame_dir / f"{slug}_{si:03d}.png"; im.save(p)
        frames.append((p, dur))
        t += dur
    return frames


def title_card(frame_dir):
    im = Image.new("RGB", (W, H), PINK_DEEP)
    hero = fit_image(IMG / "hero_axel.png", W, H).filter(ImageFilter.GaussianBlur(6))
    im = Image.blend(hero, Image.new("RGB", (W, H), PINK_DEEP), 0.55)
    d = ImageDraw.Draw(im)
    d.text((W // 2, 380), P.TITLE, font=F_BIG, fill=WHITE, anchor="mm")
    d.text((W // 2, 470), "Narrated pattern walkthrough", font=font("serif_it", 44), fill=WHITE, anchor="mm")
    d.text((W // 2, 560), f"{P.DESIGNER}  ·  {P.TERMS}  ·  {P.SKILL}  ·  {P.TIME}", font=font("semi", 28), fill=(255, 230, 236), anchor="mm")
    d.text((W // 2, H - 90), "Have the PDF pattern open alongside this video.", font=font("it", 26), fill=(255, 230, 236), anchor="mm")
    p = frame_dir / "000_title.png"; im.save(p); return p


def end_card(frame_dir):
    im = Image.new("RGB", (W, H), CREAM); d = ImageDraw.Draw(im)
    photo = fit_image(IMG / "colorways.png", 1200, 560)
    im.paste(photo, ((W - 1200) // 2, 120), round_mask(1200, 560, 36))
    d.text((W // 2, 760), "Happy crocheting!", font=F_BIG, fill=PINK_DEEP, anchor="mm")
    d.text((W // 2, 850), "  ".join(P.HASHTAGS), font=font("semi", 36), fill=INK, anchor="mm")
    d.text((W // 2, 920), f"© {P.YEAR} {P.DESIGNER} · designed by {P.STUDIO} · Design Code {P.DESIGN_CODE}", font=font("sans", 24), fill=INK_SOFT, anchor="mm")
    p = frame_dir / "999_end.png"; im.save(p); return p


# ------------------------------------------------------------------ assemble
def build(preview=False):
    OUT_DIR.mkdir(exist_ok=True)
    frame_dir = Path(tempfile.mkdtemp(prefix="axel_frames_")) if not preview else Path("/tmp/frames")
    frame_dir.mkdir(exist_ok=True, parents=True)
    chapters = N.CHAPTERS
    durations = [audio_duration(AUDIO / f"{slug}.mp3") for slug, *_ in chapters]
    lead_in, lead_out = 3.0, 6.0
    total = lead_in + sum(durations) + lead_out
    concat_lines = []
    tp = title_card(frame_dir); concat_lines.append((tp, lead_in))
    t_offset = lead_in
    for i, ((slug, title, text, key), dur) in enumerate(zip(chapters, durations), start=1):
        print(f"  chapter {i:02d} {slug:22} {dur:6.1f}s")
        frames = chapter_frames(i, len(chapters), slug, title, text, key, dur, t_offset, total, frame_dir)
        concat_lines += frames
        t_offset += dur
    ep = end_card(frame_dir); concat_lines.append((ep, lead_out))
    if preview:
        print("preview frames in", frame_dir); return
    # concat demuxer list
    lst = frame_dir / "frames.txt"
    with open(lst, "w") as f:
        for p, dsec in concat_lines:
            f.write(f"file '{p}'\nduration {dsec:.3f}\n")
        f.write(f"file '{concat_lines[-1][0]}'\n")  # concat quirk: repeat last frame
    # audio: 3 s silence + chapters + 6 s silence
    alist = frame_dir / "audio.txt"
    with open(alist, "w") as f:
        for slug, *_ in chapters:
            f.write(f"file '{AUDIO / (slug + '.mp3')}'\n")
    cmd = [FFMPEG, "-y", "-loglevel", "error",
           "-f", "concat", "-safe", "0", "-i", str(lst),
           "-f", "concat", "-safe", "0", "-i", str(alist),
           "-filter_complex", f"[1:a]adelay={int(lead_in*1000)}|{int(lead_in*1000)},apad=pad_dur={lead_out}[a]",
           "-map", "0:v", "-map", "[a]",
           "-vf", f"fps={FPS},format=yuv420p,scale={W}:{H}",
           "-c:v", "libx264", "-preset", "medium", "-crf", "22", "-tune", "stillimage",
           "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", str(OUT)]
    subprocess.run(cmd, check=True)
    print("wrote", OUT, OUT.stat().st_size // (1024 * 1024), "MB", f"({total/60:.1f} min)")
    # chapter markers for YouTube / description
    marks = []; t = lead_in
    for (slug, title, *_), dur in zip(chapters, durations):
        marks.append(f"{int(t//60):02d}:{int(t%60):02d}  {title}"); t += dur
    (OUT_DIR / "chapters.txt").write_text("\n".join(marks) + "\n")
    print("\n".join(marks))


if __name__ == "__main__":
    build(preview="--preview" in sys.argv)
