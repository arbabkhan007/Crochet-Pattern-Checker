"""Generate the spoken walkthrough for a pattern from its data file.

chapters(P) -> list of dicts (<= MAX_CHAPTERS, each text <= LIMIT chars, plain words for TTS):
    slug, title, text, image key,
    tables  [(heading, rows)]      rounds the video slide shows for this chapter (only the rows spoken in it)
    units   [(prefix, flat_index)] spoken sentence prefix -> row index across the slide's tables (video highlight sync)
    bullets [str] | None           for non-table chapters
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import count_words, load_pattern, speak, spoken_label, words  # noqa: E402

LIMIT = 1500          # speech tool hard limit per clip
MAX_CHAPTERS = 10     # speech tool cap per turn -> one pattern per turn


def prose(t):
    """Expand crochet shorthand and symbols so a TTS voice reads it naturally."""
    t = re.sub(r"<[^>]+>", "", str(t))
    t = t.replace("&nbsp;", " ").replace("&amp;", " and ")
    t = re.sub(r"#([A-Za-z][A-Za-z0-9]*)", lambda m: "hashtag " + re.sub(r"(?<=[a-z])(?=[A-Z])", " ", m.group(1)), t)
    t = t.replace(" · ", ", ").replace("·", ",")
    t = re.sub(r"(\d\s*(?:mm|cm)?(?:\s+\w+)?)\s+x\s+(\d)", r"\1 by \2", t)   # 70 mm wide x 67 mm / 79 x 52 mm / 4 x 30 cm
    t = re.sub(r"\b(Row \d+)\s*[-–]\s*(\d+ knots)", r"\1, \2", t)   # "Row 1 - 15 knots" is not a range
    t = re.sub(r"\bR(\d+)\s*[-–]\s*R?(\d+)\b", r"Rounds \1 to \2", t)
    t = re.sub(r"\bRnds?\s*(\d+)\s*[-–]\s*(\d+)\b", r"Rounds \1 to \2", t)
    t = re.sub(r"(\d)\s*[-–]\s*(\d)", r"\1 to \2", t)
    t = re.sub(r"\bR(\d+)\b", r"Round \1", t)
    t = re.sub(r"\bRnds\b", "Rounds", t); t = re.sub(r"\bRnd\b", "Round", t); t = re.sub(r"\brnds?\b", "rounds", t)
    t = re.sub(r"\b[Ss]l st\b", "slip stitch", t); t = re.sub(r"\bhdc\b", "half double crochet", t)
    t = re.sub(r"\bdc\b", "double crochet", t); t = re.sub(r"\bsc\b", "single crochet", t)
    t = re.sub(r"\binvdec\b", "invisible decrease", t); t = re.sub(r"\bdec\b", "decrease", t); t = re.sub(r"\binc\b", "increase", t)
    t = re.sub(r"\bsts\b", "stitches", t); t = re.sub(r"\bst\b", "stitch", t)
    t = re.sub(r"\b[Cc]h\b", "chain", t); t = re.sub(r"\bFO\b", "fasten off", t); t = re.sub(r"\bMR\b", "magic ring", t)
    t = re.sub(r"\bBLO\b", "back loops only", t); t = re.sub(r"\bFLO\b", "front loops only", t)
    t = re.sub(r"\bRS\b", "right side", t); t = re.sub(r"\bWS\b", "wrong side", t)
    t = re.sub(r"\]\s*x\s*(\d+)", r"] repeated \1 times", t); t = re.sub(r"\)\s*x\s*(\d+)", r") repeated \1 times", t)
    t = re.sub(r"(\d)\s*x\s*(\d)", r"\1 by \2", t); t = re.sub(r"\bx\s*(\d+)\b", r"\1 times", t)
    t = re.sub(r"\[(\d+)\]", r"(\1 stitches)", t); t = re.sub(r"\[(\d+ [^\]]{1,60})\]", r"(\1)", t)
    t = t.replace("[", "").replace("]", "")
    t = re.sub(r"(\d+(?:\.\d+)?)\s*mm\b", r"\1 millimetres", t); t = re.sub(r"(\d+(?:\.\d+)?)\s*cm\b", r"\1 centimetres", t)
    t = re.sub(r"(\d+(?:\.\d+)?)\s*g\b", r"\1 grams", t)
    t = re.sub(r"(\d+(?:\.\d+)?)\s*in\b(?=\s*(?:[,.;)\]]|tall|wide|long|across|high|deep|seated|standing|sitting|blanket|square|diagonal|$))", r"\1 inches", t)
    t = re.sub(r"(\d)\s*°", r"\1 degrees", t); t = t.replace("°", " degrees")
    t = t.replace("~", "about ").replace("≈", "about ").replace("→", " to ").replace("×", " by ").replace("−", " minus ")
    t = t.replace(" - ", ", ").replace(" – ", ", ").replace(" — ", ", ").replace("&", "and")
    t = t.replace("#4", "number 4").replace("#3", "number 3").replace("#2", "number 2").replace("#", "")
    t = re.sub(r"\bUS ([A-Z])/(\d+)\b", r"US \1 \2", t); t = re.sub(r"(Round \d+)\s*/\s*(Round \d+)", r"\1 and \2", t)
    t = re.sub(r"\b[Rr]epeat from \*\s*", "Repeat that ", t)
    t = re.sub(r"\s*/\s*", ", or ", t); t = t.replace("+", " plus ").replace("=", " equals ").replace("*", "")
    t = t.replace("e.g.", "for example").replace("i.e.", "that is").replace("approx.", "approximately").replace("vs.", "versus")
    t = re.sub(r"\bUS terms\b", "US crochet terms", t)
    t = re.sub(r"\s+", " ", t).strip()
    t = re.sub(r"\s+([,;.])", r"\1", t); t = re.sub(r",\s*,", ",", t); t = re.sub(r"\b(then) then\b", r"\1", t)
    if t and t[-1] not in ".!?:": t += "."
    return t[:1].upper() + t[1:] if t else t


def _sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]


def _pack(units, limit=LIMIT):
    """Pack (text, meta) units into chunks <= limit chars without splitting a unit."""
    chunks, cur, cur_meta = [], "", []
    for text, meta in units:
        if cur and len(cur) + 1 + len(text) > limit:
            chunks.append((cur, cur_meta)); cur, cur_meta = "", []
        cur = (cur + " " + text).strip(); cur_meta.append(meta)
    if cur: chunks.append((cur, cur_meta))
    return chunks


def _clean_title(t):
    return re.sub(r"^\d+\s*[·.]\s*", "", t).strip()


def round_sentence(label, instr, cnt, note):
    prefix = spoken_label(label) + ":"
    body = prose(speak(instr)).rstrip(".")
    s = f"{prefix} {body}."
    cw = count_words(cnt)
    if cw: s += " " + cw
    if note and note.strip(): s += " " + prose(note)
    return s, prefix


def _group_rows(rounds):
    """Merge consecutive identical plain rounds (same instr/count/note, labels R<n>, R<n+1>, ...) into one spoken unit."""
    groups, i = [], 0
    while i < len(rounds):
        j = i
        while (j + 1 < len(rounds) and rounds[j + 1][1] == rounds[i][1] and rounds[j + 1][2] == rounds[i][2]
               and (rounds[j + 1][3] or "") == (rounds[i][3] or "") and re.fullmatch(r"R\d+", rounds[j][0]) and re.fullmatch(r"R\d+", rounds[j + 1][0])
               and int(rounds[j + 1][0][1:]) == int(rounds[j][0][1:]) + 1):
            j += 1
        groups.append(list(range(i, j + 1))); i = j + 1
    return groups


def section_units(si, sec):
    """(text, meta) units for a section. meta = ('row', si, ti, [row indices], prefix) | ('text', si)."""
    units = []
    if sec.get("lead"): units.append((prose(sec["lead"]), ("text", si)))
    for ti, tbl in enumerate(sec.get("tables", [])):
        units.append((prose(tbl["heading"]), ("text", si)))
        for idxs in _group_rows(tbl["rounds"]):
            label, instr, cnt, note = tbl["rounds"][idxs[0]]
            if len(idxs) > 1: label = f"R{label[1:]}-{tbl['rounds'][idxs[-1]][0][1:]}"
            s, prefix = round_sentence(label, instr, cnt, note)
            units.append((s, ("row", si, ti, idxs, prefix)))
        if tbl.get("finish"): units.append((prose(tbl["finish"]), ("text", si)))
    for step in sec.get("steps", []): units.append((prose(step), ("text", si)))
    for title, text, kind in sec.get("panels", []): units.append((f"{prose(title).rstrip('.')}: {prose(text)}", ("text", si)))
    return units


GENERIC_IMAGE = {"Welcome": "hero", "Materials & gauge": "detail", "Techniques": "inhand", "Assembly & finishing": "inhand", "Troubleshooting": "colorways"}


def chapters(P, max_chapters=MAX_CHAPTERS):
    """Pack the whole walkthrough into <= max_chapters clips of <= LIMIT chars (greedy, never splits a unit)."""
    B = P["brand"]; sections = P["sections"]
    short = [_clean_title(s["title"]).split(" - ")[0].split(" · ")[0].strip() for s in sections]
    head = []
    welcome = (f"Welcome to {P['title']}, a crochet pattern from {B}. {prose(P['intro'])} "
               f"Finished size: {prose(P['size_chip'])} Skill level: {prose(P['skill']).rstrip('.')}, worked in {prose(P['terms']).rstrip('.')}; "
               f"plan for about {prose(P['time']).rstrip('.')}. In this walkthrough we will make: {', '.join(short)}, and then put everything together. "
               f"Keep the PDF open alongside: every round is written out in a table there, and I will read each round with its stitch count.")
    head.append((welcome, ("text", "Welcome")))
    mats = " ".join(f"{prose(k).rstrip('.')}: {prose(v)}" for k, v in P["materials"])
    for s in _sentences(f"Materials. You will need: {mats} Gauge: {prose(P['gauge'])}"): head.append((s, ("text", "Materials & gauge")))
    head.append(("Techniques. Here is every technique this pattern uses, in the order you will meet it.", ("text", "Techniques")))
    tech_full = [(f"Technique {words(i)}, {prose(n).rstrip('.')}. {prose(x)}", ("text", "Techniques")) for i, (n, x) in enumerate(P["techniques"], start=1)]
    tech_short = [(f"Technique {words(i)}, {prose(n).rstrip('.')}. {_sentences(prose(x))[0]}", ("text", "Techniques")) for i, (n, x) in enumerate(P["techniques"], start=1)]
    body_units = []
    for si, sec in enumerate(sections):
        body_units.append((f"{prose(_clean_title(sec['title'])).rstrip('.')}.", ("text", si)))
        body_units += section_units(si, sec)
    panel_texts = {f"{prose(title).rstrip('.')}: {prose(text)}" for sec in sections for title, text, _ in sec.get("panels", [])}
    asm = [(f"Assembly and finishing. Before you sew, lay everything out and check you have: {prose(', '.join(P['checklist']))}", ("text", "Assembly & finishing"))]
    asm += [(f"{prose(k).rstrip('.')}: {prose(v)}", ("text", "Assembly & finishing")) for k, v in P["assembly"]]
    closing = (f"That is {P['title']}, from {B}. Thank you for crocheting along, and happy making!", ("text", "Troubleshooting"))
    ts_all = [(f"{prose(q)} {prose(a)}", ("text", "Troubleshooting")) for q, a in P["troubleshooting"]]

    def assemble(n_ts, short_tech, drop_panels):
        body = [u for u in body_units if not (drop_panels and u[0] in panel_texts)]
        ts = ([("Troubleshooting.", ("text", "Troubleshooting"))] + ts_all[:n_ts]) if n_ts else []
        return head + (tech_short if short_tech else tech_full) + body + asm + ts + [closing]

    ladder = [(n, False, False) for n in range(len(ts_all), 0, -1)] + [(1, True, False), (0, True, False), (0, True, True)]
    for n_ts, short_tech, drop_panels in ladder:
        packed = _pack(assemble(n_ts, short_tech, drop_panels))
        if len(packed) <= max_chapters: break
    else:
        raise RuntimeError(f"{P['slug']}: cannot fit into {max_chapters} clips ({len(packed)})")

    ch = []
    for txt, metas in packed:
        groups = []
        for m in metas:
            if m[1] not in groups: groups.append(m[1])
        names = [short[g] if isinstance(g, int) else g for g in groups]
        title = " · ".join(dict.fromkeys(names))
        first = metas[0]
        if len(groups) == 1 and isinstance(first[1], int) and not txt.startswith(prose(_clean_title(sections[first[1]]["title"])).rstrip(".")):
            title += ", continued"
        tables, units = [], []
        for m in metas:
            if m[0] != "row": continue
            _, si, ti, idxs, prefix = m
            tbl = sections[si]["tables"][ti]; key = (si, ti)
            if not tables or tables[-1][0] != key: tables.append((key, tbl["heading"], []))
            tables[-1][2].extend(tbl["rounds"][i] for i in idxs)
            flat_index = sum(len(t[2]) for t in tables[:-1]) + len(tables[-1][2]) - 1
            units.append((prefix, flat_index))
        tables = [(h, rows) for _, h, rows in tables]
        g0 = groups[0]
        image = (sections[g0].get("image") if isinstance(g0, int) else GENERIC_IMAGE.get(g0)) or "hero"
        bullets = None
        if not tables:
            # bullets come from every group the chapter touches, slots allocated by how much of the chapter each group occupies
            def group_bullets(g):
                if g == "Welcome": return [P["size_chip"], f"{P['skill']}  ·  {P['terms']}  ·  {P['time']}"] + [f"{n} {c.replace(chr(10), ' ')}" for n, c in P["feats"]]
                if g == "Materials & gauge": return [f"{k}: {v}" for k, v in P["materials"]] + [f"Gauge: {P['gauge']}"]
                if g == "Techniques": return [f"{i}  {n}" for i, (n, _) in enumerate(P["techniques"], start=1)]
                if g == "Assembly & finishing": return [f"{k}: {v}" for k, v in P["assembly"]]
                if g == "Troubleshooting": return [q for q, _ in P["troubleshooting"]]
                return list(sections[g].get("steps", [])) or [sections[g].get("lead", "")]
            share = {g: sum(1 for m in metas if m[1] == g) for g in groups}
            total = sum(share.values()) or 1
            bullets = []
            for g in groups:
                slots = max(1, round(7 * share[g] / total))
                bullets += [b for b in group_bullets(g) if b][:slots]
            bullets = bullets[:8]
        ch.append(dict(title=title, text=txt, image=image, tables=tables, units=units, bullets=bullets))
    for i, c in enumerate(ch, start=1):
        c["slug"] = f"{i:02d}_" + re.sub(r"[^a-z0-9]+", "_", c["title"].lower()).strip("_")[:28]
        assert len(c["text"]) <= LIMIT, (c["slug"], len(c["text"]))
    return ch


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    mx = next((int(a.split("=")[1]) for a in sys.argv if a.startswith("--max=")), MAX_CHAPTERS)
    for slug in args or ["axel"]:
        P = load_pattern(slug); cs = chapters(P, max_chapters=mx)
        total = sum(len(c["text"]) for c in cs)
        print(f"== {slug}: {len(cs)} chapters, {total} chars (~{total/870:.1f} min)")
        for c in cs: print(f"   {c['slug']:34} {len(c['text']):5}  tables={len(c['tables'])}")
        if "--text" in sys.argv:
            for c in cs: print("\n---", c["title"], "\n", c["text"])
