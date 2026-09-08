"""Narrated tutorial video (1920x1080 H.264 + AAC) for any pattern, from the chapter audio in out/<slug>/audio/.

Each chapter = one designed slide. Round tables highlight the row being spoken (synced through the chapter's
narration units), other chapters step through bullets; every frame carries a subtitle strip and a progress bar.
Also writes <file_stem>_Full_Walkthrough.mp3 (all chapters joined) and chapters.txt (timestamps).

Usage: python engine/build_video.py <slug> [...] [--preview]     (--preview renders frames only, to /tmp/frames_<slug>)
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
from common import FONTS, IMG_ROOT, OUT_ROOT, hex_rgb, load_pattern  # noqa: E402
from narration import chapters  # noqa: E402

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
W, H = 1920, 1080
FPS = 12
WHITE = (255, 255, 255)
LEAD_IN, LEAD_OUT = 3.0, 6.0


def font(name, size):
    files = {"display": "FredokaOne-Regular.ttf", "sans": "SourceSansPro-Regular.ttf", "semi": "SourceSansPro-Semibold.ttf",
             "bold": "SourceSansPro-Bold.ttf", "it": "SourceSansPro-It.ttf", "serif_it": "Caladea-Italic.ttf"}
    return ImageFont.truetype(str(FONTS / files[name]), size)


F_TITLE = font("display", 54); F_KICK = font("semi", 26); F_BODY = font("sans", 30); F_SUB = font("semi", 34)
F_BIG = font("display", 96); F_CHAP = font("semi", 24)


def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]


def fit_image(path, bw, bh):
    im = Image.open(path).convert("RGB"); sc = max(bw / im.width, bh / im.height)
    im = im.resize((int(im.width * sc) + 1, int(im.height * sc) + 1), Image.LANCZOS)
    x = (im.width - bw) // 2; y = (im.height - bh) // 2
    return im.crop((x, y, x + bw, y + bh))


def round_mask(w, h, r):
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=r, fill=255); return m


def wrap(d, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=fnt) <= max_w: cur = t
        else: lines.append(cur); cur = w_
    if cur: lines.append(cur)
    return lines


def shrink(d, text, name, size, max_w, min_size=18):
    f = font(name, size)
    while d.textlength(text, font=f) > max_w and f.size > min_size: f = font(name, f.size - 2)
    if d.textlength(text, font=f) > max_w:
        while text and d.textlength(text + "…", font=f) > max_w: text = text[:-1]
        text += "…"
    return text, f


def audio_duration(path):
    out = subprocess.run([FFMPEG, "-i", str(path)], capture_output=True, text=True).stderr
    m = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", out)
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))


class Video:
    def __init__(self, slug):
        self.P = P = load_pattern(slug); self.slug = slug
        pal = P["palette"]
        self.ACC, self.DEEP, self.PALE, self.HIL = hex_rgb(pal["accent"]), hex_rgb(pal["deep"]), hex_rgb(pal["pale"]), hex_rgb(pal["hilite"])
        self.CREAM, self.INK, self.SOFT, self.RULE = hex_rgb(pal["cream"]), hex_rgb(pal["ink"]), hex_rgb(pal["ink_soft"]), hex_rgb(pal["rule"])
        self.DIM = tuple(int(c * 0.35 + 255 * 0.65) for c in self.INK)
        self.img = IMG_ROOT / slug
        self.out_dir = OUT_ROOT / slug; self.audio = self.out_dir / "audio"
        self.out = self.out_dir / f"{P['file_stem']}_Tutorial.mp4"
        self.chapters = chapters(P)
        self._photo = {}; self._bg = None
        self.PW = 560; self.PX = W - 80 - self.PW; self.PY = 236
        self.box = (80, 236, self.PX - 60, H - 200)

    def photo_path(self, key):
        p = self.img / self.P["images"].get(key, "hero.png")
        return p if p.exists() else self.img / self.P["images"]["hero"]

    def photo(self, key):
        if key not in self._photo:
            pw = self.PW
            ph = fit_image(self.photo_path(key), pw, pw)
            self._photo[key] = ph
        return self._photo[key]

    def background(self):
        if self._bg is None:
            im = Image.new("RGB", (W, H), self.CREAM)
            blob = Image.new("RGB", (W, H), self.CREAM); bd = ImageDraw.Draw(blob)
            bd.ellipse((W - 420, -260, W + 200, 300), fill=self.PALE); bd.ellipse((-260, H - 300, 260, H + 200), fill=self.PALE)
            im.paste(blob.filter(ImageFilter.GaussianBlur(40)))
            d = ImageDraw.Draw(im)
            d.text((80, 44), self.P["title"], font=font("display", 30), fill=self.DEEP)
            d.text((W - 80, 52), f"{self.P['brand']}  ·  Design {self.P['design_code']}  ·  {self.P['terms']}", font=F_CHAP, fill=self.SOFT, anchor="ra")
            d.line((80, 96, W - 80, 96), fill=self.RULE, width=2)
            pw = self.PW
            shadow = Image.new("RGBA", (pw + 60, pw + 60), (0, 0, 0, 0)); sd = ImageDraw.Draw(shadow)
            sd.rounded_rectangle((30, 40, pw + 30, pw + 40), radius=36, fill=(*self.DEEP, 70))
            shadow = shadow.filter(ImageFilter.GaussianBlur(24))
            im.paste(shadow, (self.PX - 30, self.PY - 30), shadow)
            self._bg = im
        return self._bg.copy()

    def base_frame(self, idx, total, title, image_key):
        im = self.background(); d = ImageDraw.Draw(im)
        d.text((80, 122), f"CHAPTER {idx} OF {total}", font=F_KICK, fill=self.DEEP)
        t, f = shrink(d, title, "display", 54, self.PX - 140, 30)
        d.text((80, 150), t, font=f, fill=self.INK)
        im.paste(self.photo(image_key), (self.PX, self.PY), round_mask(self.PW, self.PW, 36))
        return im, d

    # ------------------------------------------------------------- tables
    def table_lines(self, tables):
        lines, flat = [], 0
        for heading, rows in tables:
            lines.append(("heading", heading)); lines.append(("header",))
            for r in rows: lines.append(("row", r, flat)); flat += 1
        return lines

    def draw_tables(self, d, tables, lo, hi):
        """Draw the chapter's tables; rows lo..hi (flat indices, inclusive) are 'active', rows < lo are done, rows > hi dimmed."""
        x0, y0, x1, y1 = self.box
        lines = self.table_lines(tables)
        n_rows = sum(len(r) for _, r in tables)
        compact = len(tables) > 1 or n_rows > 12
        hh, hd, rh = (44, 40, 36) if compact else (52, 46, 44)
        heights = [hh if l[0] == "heading" else hd if l[0] == "header" else rh for l in lines]
        avail = y1 - y0
        if sum(heights) > avail:  # sliding window keeping the active row visible
            act = next((i for i, l in enumerate(lines) if l[0] == "row" and l[2] == max(hi, 0)), 0)
            cap = max(3, int(avail // rh) - 2)
            start = max(0, act - cap // 2)
            while start > 0 and sum(heights[start:act + 1]) + rh * 2 < avail and lines[start - 1][0] != "heading": start -= 1
            if start > 0 and lines[start][0] == "header": start += 1
            window = []; used = 0
            for l, hgt in zip(lines[start:], heights[start:]):
                if used + hgt > avail - (rh if start > 0 else 0): break
                window.append(l); used += hgt
            hidden_before = sum(1 for l in lines[:start] if l[0] == "row")
            hidden_after = n_rows - hidden_before - sum(1 for l in window if l[0] == "row")
        else:
            window, hidden_before, hidden_after = lines, 0, 0
        f_row, f_lab, f_cnt, f_note = font("sans", 26 if compact else 28), font("semi", 26 if compact else 28), font("display", 26 if compact else 28), font("it", 21 if compact else 22)
        c_lab, c_ins, c_cnt, c_note = x0, x0 + 104, x0 + 700, x0 + 796
        y = y0
        if hidden_before:
            d.text((x0, y), f"… {hidden_before} earlier round{'s' if hidden_before > 1 else ''} above", font=font("it", 22), fill=self.SOFT); y += rh
        for l in window:
            if l[0] == "heading":
                t, f = shrink(d, l[1], "display", 30 if compact else 34, x1 - x0, 22)
                d.text((x0, y + 4), t, font=f, fill=self.DEEP); y += hh
            elif l[0] == "header":
                d.rounded_rectangle((x0 - 10, y - 2, x1, y + 34), radius=8, fill=self.PALE)
                for cx, lab in ((c_lab, "Rnd"), (c_ins, "Instruction"), (c_cnt, "Sts"), (c_note, "Note")):
                    d.text((cx, y + 3), lab, font=F_KICK, fill=self.DEEP)
                y += hd
            else:
                (label, instr, cnt, note), k = l[1], l[2]
                active = lo <= k <= hi; done = k < lo
                if active: d.rounded_rectangle((x0 - 10, y - 5, x1, y + rh - 7), radius=8, fill=self.HIL)
                col = self.INK if (done or active) else self.DIM
                d.text((c_lab, y), str(label), font=f_lab, fill=self.DEEP if active else col)
                t, f = shrink(d, str(instr), "sans", f_row.size, c_cnt - c_ins - 14, 20)
                d.text((c_ins, y + (f_row.size - f.size) // 2), t, font=f, fill=col)
                ct = f"({cnt})" if isinstance(cnt, int) else str(cnt or "")
                d.text((c_cnt, y), ct, font=f_cnt, fill=self.DEEP if (done or active) else self.ACC)
                if note:
                    t, f = shrink(d, str(note), "it", f_note.size, x1 - c_note, 18)
                    d.text((c_note, y + 3), t, font=f, fill=self.SOFT if (done or active) else self.DIM)
                if active: d.polygon([(x0 - 34, y + 8), (x0 - 34, y + 26), (x0 - 20, y + 17)], fill=self.DEEP)
                y += rh
        if hidden_after:
            d.text((x0, y), f"… {hidden_after} more round{'s' if hidden_after > 1 else ''} below", font=font("it", 22), fill=self.SOFT)

    def draw_bullets(self, d, items, active):
        x0, y0, x1, y1 = self.box; y = y0
        for k, t in enumerate(items):
            lines = wrap(d, t, F_BODY, x1 - x0 - 50)
            if len(lines) > 2:
                lines = lines[:2]
                while d.textlength(lines[1] + "…", font=F_BODY) > x1 - x0 - 50: lines[1] = lines[1][:-1]
                lines[1] += "…"
            hgt = 36 * len(lines) + 22
            if y + hgt > y1 + 10: break
            act = k == active; done = k < active
            if act: d.rounded_rectangle((x0 - 10, y - 8, x1, y + hgt - 14), radius=10, fill=self.HIL)
            d.ellipse((x0, y + 12, x0 + 16, y + 28), fill=self.DEEP if (done or act) else self.RULE)
            for i, line in enumerate(lines): d.text((x0 + 36, y + i * 36), line, font=F_BODY, fill=self.INK if (done or act) else self.DIM)
            y += hgt

    def draw_footer(self, d, subtitle, progress):
        d.rounded_rectangle((80, H - 170, W - 80, H - 70), radius=22, fill=WHITE, outline=self.RULE, width=2)
        f = F_SUB
        while len(wrap(d, subtitle, f, W - 240)) > 2 and f.size > 24: f = font("semi", f.size - 2)
        lines = wrap(d, subtitle, f, W - 240)
        if len(lines) > 2:
            lines = lines[:2]
            while d.textlength(lines[1] + "…", font=f) > W - 240: lines[1] = lines[1][:-1]
            lines[1] += "…"
        y = H - 150 + (0 if len(lines) == 2 else 20) + (34 - f.size) // 2
        for i, line in enumerate(lines): d.text((W // 2, y + i * (f.size + 8)), line, font=f, fill=self.INK, anchor="ma")
        d.rounded_rectangle((80, H - 44, W - 80, H - 34), radius=5, fill=self.RULE)
        d.rounded_rectangle((80, H - 44, 80 + int((W - 160) * progress), H - 34), radius=5, fill=self.ACC)
        d.text((80, H - 30), "progress", font=font("it", 18), fill=self.SOFT)
        d.text((W - 80, H - 30), f"{int(progress * 100)}%", font=font("semi", 18), fill=self.SOFT, anchor="ra")

    # ------------------------------------------------------------- frames
    def chapter_frames(self, idx, total, ch, duration, t_offset, total_dur, frame_dir):
        sents = sentences(ch["text"]); total_chars = sum(len(s) for s in sents)
        tables, units, bullets = ch["tables"], ch["units"], ch["bullets"]
        frames = []; t = 0.0; lo, hi = -1, -1; prev_hi = -1
        for si, sent in enumerate(sents):
            dur = duration * len(sent) / total_chars
            if tables:
                hit = next((fi for prefix, fi in units if sent.startswith(prefix)), None)
                if hit is not None:
                    lo, hi = prev_hi + 1, hit; prev_hi = hit
            im, d = self.base_frame(idx, total, ch["title"], ch["image"])
            if tables: self.draw_tables(d, tables, lo if lo >= 0 else 0, hi)
            elif bullets:
                u = min(len(bullets) - 1, int(((t + dur / 2) / duration) * len(bullets)))
                self.draw_bullets(d, bullets, u)
            self.draw_footer(d, sent, (t_offset + t) / total_dur)
            p = frame_dir / f"{ch['slug']}_{si:03d}.png"; im.save(p, compress_level=1)
            frames.append((p, dur)); t += dur
        return frames

    def title_card(self, frame_dir):
        P = self.P
        hero = fit_image(self.photo_path("hero"), W, H).filter(ImageFilter.GaussianBlur(6))
        im = Image.blend(hero, Image.new("RGB", (W, H), self.DEEP), 0.55); d = ImageDraw.Draw(im)
        t, f = shrink(d, P["title"], "display", 96, W - 200, 48)
        d.text((W // 2, 380), t, font=f, fill=WHITE, anchor="mm")
        d.text((W // 2, 470), "Narrated pattern walkthrough", font=font("serif_it", 44), fill=WHITE, anchor="mm")
        d.text((W // 2, 560), f"{P['brand']}  ·  {P['terms']}  ·  {P['skill']}  ·  {P['time']}", font=font("semi", 28), fill=self.PALE, anchor="mm")
        d.text((W // 2, H - 90), "Have the PDF pattern open alongside this video.", font=font("it", 26), fill=self.PALE, anchor="mm")
        p = frame_dir / "000_title.png"; im.save(p); return p

    def end_card(self, frame_dir):
        P = self.P; im = Image.new("RGB", (W, H), self.CREAM); d = ImageDraw.Draw(im)
        im.paste(fit_image(self.photo_path("colorways"), 1200, 560), ((W - 1200) // 2, 120), round_mask(1200, 560, 36))
        d.text((W // 2, 760), "Happy crocheting!", font=F_BIG, fill=self.DEEP, anchor="mm")
        d.text((W // 2, 850), "  ".join(P["hashtags"]), font=font("semi", 36), fill=self.INK, anchor="mm")
        d.text((W // 2, 920), f"© {P['year']} {P['brand']}  ·  Design Code {P['design_code']}", font=font("sans", 24), fill=self.SOFT, anchor="mm")
        p = frame_dir / "999_end.png"; im.save(p); return p

    # ------------------------------------------------------------- assemble
    def clips(self):
        return [self.audio / f"{c['slug']}.mp3" for c in self.chapters]

    def build_full_audio(self):
        clips = self.clips(); n = len(clips)
        out = self.out_dir / f"{self.P['file_stem']}_Full_Walkthrough.mp3"
        cmd = [FFMPEG, "-y", "-loglevel", "error"]
        for c in clips: cmd += ["-i", str(c)]
        fc = "".join(f"[{i}:a]apad=pad_dur=0.8[a{i}];" for i in range(n)) + "".join(f"[a{i}]" for i in range(n)) + f"concat=n={n}:v=0:a=1[out]"
        cmd += ["-filter_complex", fc, "-map", "[out]", "-c:a", "libmp3lame", "-b:a", "96k", str(out)]
        subprocess.run(cmd, check=True); return out

    def build(self, preview=False):
        missing = [c for c in self.clips() if not c.exists()]
        if missing: raise SystemExit(f"{self.slug}: missing audio clips: {[m.name for m in missing]}")
        frame_dir = Path(f"/tmp/frames_{self.slug}") if preview else Path(tempfile.mkdtemp(prefix=f"{self.slug}_frames_"))
        frame_dir.mkdir(parents=True, exist_ok=True)
        durations = [audio_duration(c) for c in self.clips()]
        total = LEAD_IN + sum(durations) + LEAD_OUT
        concat = [(self.title_card(frame_dir), LEAD_IN)]; t_offset = LEAD_IN
        for i, (ch, dur) in enumerate(zip(self.chapters, durations), start=1):
            print(f"  chapter {i:02d} {ch['slug']:34} {dur:6.1f}s")
            concat += self.chapter_frames(i, len(self.chapters), ch, dur, t_offset, total, frame_dir); t_offset += dur
        concat.append((self.end_card(frame_dir), LEAD_OUT))
        if preview: print("preview frames in", frame_dir); return
        lst = frame_dir / "frames.txt"
        with open(lst, "w") as f:
            for p, dsec in concat: f.write(f"file '{p}'\nduration {dsec:.3f}\n")
            f.write(f"file '{concat[-1][0]}'\n")
        alist = frame_dir / "audio.txt"
        with open(alist, "w") as f:
            for c in self.clips(): f.write(f"file '{c.resolve()}'\n")
        ms = int(LEAD_IN * 1000)
        cmd = [FFMPEG, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-f", "concat", "-safe", "0", "-i", str(alist),
               "-filter_complex", f"[1:a]adelay={ms}|{ms},apad=pad_dur={LEAD_OUT}[a]", "-map", "0:v", "-map", "[a]",
               "-vf", f"fps={FPS},format=yuv420p,scale={W}:{H}", "-c:v", "libx264", "-preset", "fast", "-crf", "23", "-tune", "stillimage",
               "-c:a", "aac", "-b:a", "112k", "-shortest", "-movflags", "+faststart", str(self.out)]
        subprocess.run(cmd, check=True)
        print("wrote", self.out, self.out.stat().st_size // (1024 * 1024), "MB", f"({total / 60:.1f} min)")
        marks = []; t = LEAD_IN
        for ch, dur in zip(self.chapters, durations):
            marks.append(f"{int(t // 60):02d}:{int(t % 60):02d}  {ch['title']}"); t += dur
        (self.out_dir / "chapters.txt").write_text("\n".join(marks) + "\n")
        full = self.build_full_audio(); print("wrote", full, full.stat().st_size // 1024, "KB")
        for p in frame_dir.glob("*.png"): p.unlink()


if __name__ == "__main__":
    for slug in [a for a in sys.argv[1:] if not a.startswith("--")]:
        Video(slug).build(preview="--preview" in sys.argv)
