"""Generate the corrected customer-facing markdown sources in patterns/.

Built from the same data that drives the audit, so the sources can never
diverge from the validated stitch math.
"""
from __future__ import annotations

from pathlib import Path

from . import PATTERNS, schema

OUT = Path("patterns")


def md_table(headers, rows):
    out = ["| " + " | ".join(headers) + " |",
           "|" + "|".join(["---"] * len(headers)) + "|"]
    for r in rows:
        out.append("| " + " | ".join(r) + " |")
    return out


def piece_md(piece):
    lines = [f"### {piece['name']}", ""]
    if piece.get("intro"):
        lines += [piece["intro"], ""]
    for sub in piece["subpieces"]:
        if sub.get("name"):
            lines += [f"**{sub['name']}**", ""]
        if sub.get("rows"):
            rows = []
            for row in sub["rows"]:
                stated = f"({row['stated']})" if row.get("stated") is not None else "-"
                note = row.get("note", "") or "-"
                rows.append([row["label"], row["text"], stated, note])
            lines += md_table(["Rnd", "Instruction", "Sts", "Note"], rows)
            lines.append("")
        for note in sub.get("notes", []):
            lines += [note, ""]
    return lines


def pattern_md(p) -> str:
    L = [f"# {p['title']}", ""]
    L.append("> **" + "  ·  ".join(p["meta"]) + f"**  —  Design Code {p['design_code']}")
    L += ["", p["tagline"], ""]
    L += ["**FINISHED SIZE**  " + "  ".join(p["finished_size"]), ""]
    L += ["---", "", "**SAFETY - READ THIS FIRST**", ""]
    for s in p["safety"]:
        L += [s, ""]
    L += ["### Materials", ""]
    for m in p["materials"]:
        L.append(f"- {m}")
    L.append("")
    L += ["**Gauge & size**", ""]
    for g in p["gauge"]:
        L += [g, ""]
    L += ["### Abbreviations (US terms)", ""]
    abbr = p["abbreviations"]
    for i in range(0, len(abbr), 2):
        pair = abbr[i:i + 2]
        L.append("  ·  ".join(pair))
    L.append("")
    if p.get("construction"):
        L += [p["construction"], ""]
    if p.get("techniques"):
        L += ["### Techniques used, in the order you will meet them", ""]
        for i, (name, body) in enumerate(p["techniques"], start=1):
            L += [f"{i}. **{name}** - {body}", ""]
    if p.get("notes"):
        L += ["### Notes", ""]
        for n in p["notes"]:
            L += [n, ""]
    L += ["### Instructions", ""]
    for piece in p["pieces"]:
        L += piece_md(piece)
    if p.get("assembly"):
        L += ["### Finishing & assembly", ""]
        for a in p["assembly"]:
            L += [a, ""]
    if p.get("troubleshooting"):
        L += ["### Troubleshooting", ""]
        for prob, fix in p["troubleshooting"]:
            L += [f"- **{prob}** {fix}"]
        L.append("")
    if p.get("colorways"):
        L += ["### Colorways", "", "  ·  ".join(p["colorways"]), ""]
    for extra in p.get("extras", []):
        L += [f"### {extra['name']}", ""]
        if extra["type"] == "table":
            L += md_table(extra["headers"], extra["rows"])
            L.append("")
            if extra.get("outro"):
                L += [extra["outro"], ""]
        else:
            for ln in extra.get("lines", []):
                L += [ln, ""]
    if p.get("designer_notes"):
        L += ["### Designer notes", ""]
        for d in p["designer_notes"]:
            L += [f"- {d}"]
        L.append("")
    L += ["## Terms of Use", ""]
    L += ["#### Copyright & ownership", ""]
    L += [p["terms"]["ownership"], "", schema.COPYRIGHT_NOTICE, ""]
    L += ["#### You may", "", p["terms"]["may"], ""]
    L += ["#### You may not", "", p["terms"]["maynot"], ""]
    L += ["#### Safety reminder", "", p["terms"]["safety"], ""]
    L += ["### Happy crocheting!", ""]
    L += [f"Tag your makes with **#NovalityStore** and **{p['hashtag']}** - "
          f"{p['closing']}", ""]
    return "\n".join(L)


def build_all():
    OUT.mkdir(exist_ok=True)
    for p in PATTERNS:
        slug = p["title"].replace(" ", "_")
        path = OUT / f"{p['number']:02d}_{slug}.md"
        path.write_text(pattern_md(p))
        print(f"wrote {path}")


if __name__ == "__main__":
    build_all()
