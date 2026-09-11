"""Generate the markdown master documents for the Christmas patterns
(NS 11 - NS 15), matching the style of patterns/01-10 and using the dual
US|UK round tables.  Output: patterns/11_*.md .. patterns/15_*.md
"""
from __future__ import annotations

from pathlib import Path

from tools.novality.build_pdfs import merge_dual, _merge_abbr
from tools.novality import schema
from tools.novality_xmas import X01, X02, X03, X04, X05
from tools.novality_xmas.uk_terms import to_uk

OUT = Path("patterns")

FILES = {
    "gnome": "11_No-Sew_Christmas_Gnome.md",
    "tree": "12_Bobble_Christmas_Tree.md",
    "bundle": "13_Christmas_Ornament_Bundle.md",
    "treeskirt": "14_Bobble_Snowflake_Tree_Skirt.md",
    "wreath": "15_Interchangeable_Christmas_Wreath.md",
}


def build(p):
    uk = to_uk(p)
    m = merge_dual(p, uk)
    B = []
    B.append(f"# {p['title']}\n")
    meta = p.get("meta", [])
    badges = "  ·  ".join(["US + UK terms", *meta[1:]])
    B.append(f"> **{badges}**  —  Design Code {p['design_code']}\n")
    B.append(p["tagline"] + "\n")
    fs = "  ".join(p["finished_size"])
    B.append(f"**FINISHED SIZE**  {fs}\n")
    B.append("---\n")
    B.append("**SAFETY - READ THIS FIRST**\n")
    for s in p["safety"]:
        B.append(s + "\n")
    B.append("### Materials\n")
    for mat in p["materials"]:
        B.append(f"- {mat}")
    B.append("")
    B.append("**Gauge & size**\n")
    for g in p["gauge"]:
        B.append(g + "\n")
    B.append("### Abbreviations (US + UK)\n")
    abbr = _merge_abbr(p["abbreviations"], uk["abbreviations"])
    half = (len(abbr) + 1) // 2
    for i in range(half):
        left = abbr[i]
        right = abbr[i + half] if i + half < len(abbr) else ""
        B.append(left + ("  ·  " + right if right else ""))
    B.append("")
    if m.get("notes"):
        B.append(m["notes"][0] + "\n")  # dual-reading note first
    if p.get("construction") or p.get("techniques"):
        B.append("### Construction & techniques\n")
        if p.get("construction"):
            B.append(p["construction"] + "\n")
        for i, (name, txt) in enumerate(p.get("techniques", []), start=1):
            B.append(f"{i}. **{name}** - {txt}\n")
    B.append("### Instructions\n")
    # map uk pieces in parallel
    uk_pieces = uk["pieces"]
    for pi, piece in enumerate(p["pieces"]):
        B.append(f"### {piece['name']}\n")
        if piece.get("intro"):
            B.append(piece["intro"] + "\n")
        for si, sub in enumerate(piece["subpieces"]):
            if sub.get("name"):
                B.append(f"#### {sub['name']}\n")
            if sub.get("rows"):
                uks = uk_pieces[pi]["subpieces"][si].get("rows", [])
                B.append("| Rnd | US terms | UK terms | Sts | Note |")
                B.append("|---|---|---|---|---|")
                for ri, r in enumerate(sub["rows"]):
                    uk_txt = uks[ri]["text"] if ri < len(uks) else ""
                    sts = f"({r['stated']})" if r.get("stated") is not None else "-"
                    note = r.get("note") or "-"
                    label = r["label"] or "-"
                    B.append(f"| {label} | {r['text']} | {uk_txt} | {sts} | {note} |")
                B.append("")
            for note in sub.get("notes", []):
                B.append(note + "\n")
    for n in m.get("notes", [])[1:]:
        B.append(n + "\n")
    if p.get("assembly"):
        B.append("## Finishing & assembly\n")
        for a in p["assembly"]:
            B.append(f"- {a}")
        B.append("")
    if p.get("troubleshooting"):
        B.append("## Troubleshooting\n")
        for prob, fix in p["troubleshooting"]:
            B.append(f"- **{prob}** {fix}")
        B.append("")
    if p.get("colorways"):
        B.append("## Colorways\n")
        B.append("  ·  ".join(p["colorways"]) + "\n")
    tips = p.get("extras") or p.get("designer_notes")
    if tips:
        B.append("## Helpful tips\n")
        for extra in p.get("extras", []):
            B.append(f"#### {extra['name']}\n")
            if extra["type"] == "table":
                B.append("| " + " | ".join(extra["headers"]) + " |")
                B.append("|" + "---|" * len(extra["headers"]))
                for row in extra["rows"]:
                    B.append("| " + " | ".join(row) + " |")
                B.append("")
                if extra.get("outro"):
                    B.append(extra["outro"] + "\n")
            else:
                for ln in extra.get("lines", []):
                    B.append(ln + "\n")
        for dnote in p.get("designer_notes", []):
            B.append(f"- {dnote}")
        B.append("")
    B.append("## Terms of Use\n")
    B.append("#### Copyright & ownership\n")
    B.append(p["terms"]["ownership"] + "\n")
    B.append(schema.COPYRIGHT_NOTICE + "\n")
    B.append("#### You may\n")
    B.append(p["terms"]["may"] + "\n")
    B.append("#### You may not\n")
    B.append(p["terms"]["maynot"] + "\n")
    B.append("#### Safety reminder\n")
    B.append(p["terms"]["safety"] + "\n")
    B.append("### Happy crocheting!\n")
    B.append(f"Tag your makes with **#NovalityStore** and **{p['hashtag']}** - "
             f"{p['closing']}. Thank you for supporting an independent "
             f"pattern designer.\n")
    return "\n".join(B)


def build_all():
    OUT.mkdir(exist_ok=True)
    for p in (X01, X02, X03, X04, X05):
        out = OUT / FILES[p["id"]]
        out.write_text(build(p))
        print("wrote", out)


if __name__ == "__main__":
    build_all()
