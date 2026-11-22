from pathlib import Path
ROOT = Path(__file__).resolve().parent
SPEC = {
    "code": "NS-01",
    "title": "Hamish the Highland Cow",
    "subtitle": "One spiral head, one spiral body · wide cream muzzle · weather-beaten fringe · seated 15 cm",
    "tagline": "CROCHET PATTERN · US TERMS · INTERMEDIATE · 6 - 8 HOURS · INK-FRIENDLY PRINT LAYOUT",
    "md": str(ROOT / "NS01_corrected.md"),
    "hero": str(ROOT / "assets" / "hamish_hero.png"),
    "out": str(ROOT.parents[1] / "shop" / "Hamish_the_Highland_Cow_NS01_NovalityStore.pdf"),
    "out_bw": str(ROOT.parents[1] / "shop" / "Hamish_the_Highland_Cow_NS01_PRINT_EDITION_BW.pdf"),
    "chips": ["16 ROUNDS", "9 PIECES", "12 MM EYES", "WORSTED #4"],
    "swatches": [("GINGER - MAIN", "#B4713A"), ("OAT CREAM - MUZZLE", "#E9DCBF")],
    "cards": [
        ("WHAT YOU GET", ["One-piece spiral head and body",
                          "Muzzle, belly patch, legs, ears, horns",
                          "Fringe, tail and optional tartan scarf"]),
        ("VERIFICATION", ["✓ 5-axiom mathematical audit",
                          "All round counts re-derived exactly",
                          "Deterministic static analysis engine"]),
        ("PRINT NOTES", ["US Letter, no full-bleed colour",
                         "Tables sized for home printers",
                         "Checklist and record pages included"]),
    ],
    "cover_note_title": "Worked in pieces so every proportion can be pinned and checked",
    "cover_note": "head, body, muzzle, belly patch, four legs, four ear layers and two horns are "
                  "made separately, then sewn in the numbered assembly order; the fringe and tail "
                  "are knotted yarn secured twice.",
    "components": [("1  Head", "16 rnd\nclose to 6"),
                   ("2  Muzzle", "8 rnd\nsew R10-R16"),
                   ("3  Body", "19 rnd\nneck open 18"),
                   ("4  Legs x4", "16 rnd\nor 10 front"),
                   ("5  Ears x4", "inner +\nouter layer"),
                   ("6  Horns x2", "7 rnd\ntip stuffed")],
    "assembly_note": "Assembly order: muzzle and face first, then horns, ears, fringe, head to "
                     "body over the 18-stitch neck, legs, belly patch, tail and scarf last.",
    "main_section": "3. body",
    "zones": (7, 8),
    "colophon": "Assembly map, count chart, 36-row ladder equivalents and the 5-axiom table are "
                "computed from the corrected master at compile time; no sampled results.",
}
