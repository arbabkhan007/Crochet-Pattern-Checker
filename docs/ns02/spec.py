from pathlib import Path
ROOT = Path(__file__).resolve().parent
SPEC = {
    "code": "NS-02",
    "title": "Kawaii Halloween Mini Set",
    "subtitle": "Boo the Ghost · Pip the Pumpkin · Bramble the Bat · three 5 cm minis, one DK hook",
    "tagline": "CROCHET PATTERN · US TERMS · INTERMEDIATE · 2 - 3 HOURS PER MINI · INK-FRIENDLY PRINT LAYOUT",
    "md": str(ROOT / "NS02_corrected.md"),
    "hero": str(ROOT / "assets" / "halloween_trio_hero.png"),
    "out": str(ROOT.parents[1] / "shop" / "Kawaii_Halloween_Mini_Set_NS02_NovalityStore.pdf"),
    "out_bw": str(ROOT.parents[1] / "shop" / "Kawaii_Halloween_Mini_Set_NS02_PRINT_EDITION_BW.pdf"),
    "chips": ["3 MINIS", "16 ROUNDS MAX", "PICOT WINGS", "DK #3"],
    "swatches": [("CREAM - BOO", "#F3EBDD"), ("PASTEL ORANGE - PIP", "#F2A65A"),
                 ("LAVENDER - BRAMBLE", "#B79ED4")],
    "cards": [
        ("WHAT YOU GET", ["Boo: open bell with ruffled hem",
                          "Pip: needle-sculpted six-rib body",
                          "Bramble: picot wings and fang stitches"]),
        ("VERIFICATION", ["✓ 5-axiom mathematical audit",
                          "All round counts re-derived exactly",
                          "Deterministic static analysis engine"]),
        ("PRINT NOTES", ["US Letter, no full-bleed colour",
                         "Tables sized for home printers",
                         "Checklist and record pages included"]),
    ],
    "cover_note_title": "Three pocket-size minis that share one hook, one gauge and one sitting",
    "cover_note": "each mini is worked top-down in one piece plus small sewn parts; Boo stays "
                  "hollow and stands on his ruffled hem, Pip is overstuffed then sculpted with "
                  "six rib passes, Bramble closes over light stuffing with picot-edged wings.",
    "components": [("1  Boo body", "13 rnd\nopen bell"),
                   ("2  Boo arms x2", "2 rnd\nno stuffing"),
                   ("3  Pip body", "14 rnd\n6-rib sculpt"),
                   ("4  Stem + leaf", "cone 4 rnd\nflat leaf"),
                   ("5  Bramble body", "16 rnd\ncloses 6"),
                   ("6  Wings x2", "rows 1-3\npicot edge")],
    "assembly_note": "Assembly order: faces first (Boo and Bramble eyes, Pip embroidery), then "
                     "Pip stem, leaf and tendril, Bramble ears and wings, Boo arms and optional "
                     "base; the optional garland threads all nine minis on cord with felt balls.",
    "main_section": "bramble body",
    "zones": (8, 12),
    "colophon": "Assembly map, count chart, ladder equivalents and the 5-axiom table are computed "
                "from the corrected master at compile time; no sampled results.",
}
