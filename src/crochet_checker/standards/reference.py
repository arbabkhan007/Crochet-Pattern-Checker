"""Published crochet standards used as a reference, not as a guess.

Source: Craft Yarn Council's www.YarnStandards.com
Pages read on 2026-09-28:
- https://www.craftyarncouncil.com/standards/yarn-weight-system
- https://www.craftyarncouncil.com/standards/hooks-and-needles
- https://www.craftyarncouncil.com/standards/steel-crochet-hook-crochet-thread-sizes
- https://www.craftyarncouncil.com/standards/crochet-abbreviations
- https://www.craftyarncouncil.com/standards/crochet-chart-symbols
- https://www.craftyarncouncil.com/standards/how-measure-wraps-inch-wpi
- https://www.craftyarncouncil.com/standards/project-levels
- https://www.craftyarncouncil.com/standards/body-sizing
- https://www.craftyarncouncil.com/standards/yarn-label-information
- https://www.craftyarncouncil.com/standards/care-symbols

The Council asks for this credit when its standard is used:
Source: Craft Yarn Council's www.YarnStandards.com

A Size 8 yarn band was announced on the weight page, with downloadable
resources still coming. No Size 8 gauge or hook range is published there,
so none is stored here. Steel hook numbers are not one millimeter each:
the Council prints more than one millimeter for the same number.
"""

from __future__ import annotations

CREDIT = "Source: Craft Yarn Council's www.YarnStandards.com"
INCH_TO_CM = 2.54

# number, name, yarn types, crochet gauge low/high, gauge stitch,
# hook mm low/high, hook note, US hook note, needle mm low/high, US needle,
# wraps per inch. Lace crochet gauge is double crochet, and the Council
# says a lace range is hard to determine.
YARN_WEIGHTS: tuple[dict, ...] = (
    {
        "number": 0,
        "name": "Lace",
        "types": ("fingering", "10-count crochet thread"),
        "knit_gauge": (33, 40),
        "crochet_gauge": (32, 42),
        "crochet_gauge_stitch": "double crochet",
        "hook_mm": None,
        "steel_hook_mm": (1.4, 1.6),
        "regular_hook_mm": 2.25,
        "hook_note": "Steel 1.6-1.4 mm, or a regular hook of 2.25 mm.",
        "hook_us": "Steel 6, 7, 8, or regular hook B-1.",
        "needle_mm": (1.5, 2.25),
        "needle_us": "000-1",
        "wpi": "30-40+",
        "banded": False,
    },
    {
        "number": 1,
        "name": "Super Fine",
        "types": ("sock", "fingering", "baby"),
        "knit_gauge": (27, 32),
        "crochet_gauge": (21, 32),
        "crochet_gauge_stitch": "single crochet",
        "hook_mm": (2.25, 3.5),
        "hook_note": "2.25-3.5 mm.",
        "hook_us": "B-1 to E-4.",
        "needle_mm": (2.25, 3.25),
        "needle_us": "1 to 3",
        "wpi": "14-30",
        "banded": True,
    },
    {
        "number": 2,
        "name": "Fine",
        "types": ("sport", "baby"),
        "knit_gauge": (23, 26),
        "crochet_gauge": (16, 20),
        "crochet_gauge_stitch": "single crochet",
        "hook_mm": (3.5, 4.5),
        "hook_note": "3.5-4.5 mm.",
        "hook_us": "E-4 to 7.",
        "needle_mm": (3.25, 3.75),
        "needle_us": "3 to 5",
        "wpi": "12-18",
        "banded": True,
    },
    {
        "number": 3,
        "name": "Light",
        "types": ("dk", "light worsted"),
        "knit_gauge": (21, 24),
        "crochet_gauge": (12, 17),
        "crochet_gauge_stitch": "single crochet",
        "hook_mm": (4.5, 5.5),
        "hook_note": "4.5-5.5 mm.",
        "hook_us": "7 to I-9.",
        "needle_mm": (3.75, 4.5),
        "needle_us": "5 to 7",
        "wpi": "11-15",
        "banded": True,
    },
    {
        "number": 4,
        "name": "Medium",
        "types": ("worsted", "afghan", "aran"),
        "knit_gauge": (16, 20),
        "crochet_gauge": (11, 14),
        "crochet_gauge_stitch": "single crochet",
        "hook_mm": (5.5, 6.5),
        "hook_note": "5.5-6.5 mm.",
        "hook_us": "I-9 to K-10 1/2.",
        "needle_mm": (4.5, 5.5),
        "needle_us": "7 to 9",
        "wpi": "9-12",
        "banded": True,
    },
    {
        "number": 5,
        "name": "Bulky",
        "types": ("chunky", "craft", "rug"),
        "knit_gauge": (12, 15),
        "crochet_gauge": (8, 11),
        "crochet_gauge_stitch": "single crochet",
        "hook_mm": (6.5, 9),
        "hook_note": "6.5-9 mm.",
        "hook_us": "K-10 1/2 to M-13.",
        "needle_mm": (5.5, 8),
        "needle_us": "9 to 11",
        "wpi": "6-9",
        "banded": True,
    },
    {
        "number": 6,
        "name": "Super Bulky",
        "types": ("super bulky", "roving"),
        "knit_gauge": (7, 11),
        "crochet_gauge": (7, 9),
        "crochet_gauge_stitch": "single crochet",
        "hook_mm": (9, 15),
        "hook_note": "9-15 mm.",
        "hook_us": "M-13 to Q.",
        "needle_mm": (8, 12.75),
        "needle_us": "11 to 17",
        "wpi": "5-6",
        "banded": True,
    },
    {
        "number": 7,
        "name": "Jumbo",
        "types": ("jumbo", "roving"),
        "knit_gauge": (None, 6),
        "crochet_gauge": (None, 6),
        "crochet_gauge_stitch": "single crochet",
        "hook_mm": (15, None),
        "hook_note": "15 mm and larger.",
        "hook_us": "Q and larger.",
        "needle_mm": (12.75, None),
        "needle_us": "17 and larger",
        "wpi": "1-4",
        "banded": True,
    },
)

SIZE_8_NOTE = (
    "The Craft Yarn Council page says a Size 8, Blocking, and Plus update "
    "is coming. The published table still ends at 7. No Size 8 numbers are stored."
)

# Millimeter, then the U.S. label printed by the Council. A blank label is None.
# The Council says letter sizes vary by maker, so the millimeter is the measurement.
CROCHET_HOOKS: tuple[tuple[float, str | None], ...] = (
    (2.25, "B-1"),
    (2.50, None),
    (2.75, "C-2"),
    (3.125, "D"),
    (3.25, "D-3"),
    (3.50, "E-4"),
    (3.75, "F-5"),
    (4.0, "G-6"),
    (4.25, "G"),
    (4.50, "7"),
    (5.0, "H-8"),
    (5.25, "I"),
    (5.50, "I-9"),
    (5.75, "J"),
    (6.0, "J-10"),
    (6.50, "K-10 1/2"),
    (7.0, None),
    (8.0, "L-11"),
    (9.0, "M/N-13"),
    (10.0, "N/P-15"),
    (11.50, "P-16"),
    (12.0, None),
    (15.0, "P/Q"),
    (15.75, "Q"),
    (16.0, "Q"),
    (19.0, "S"),
    (25.0, "T/U/X"),
    (30.0, "T/X"),
)

KNITTING_NEEDLES: tuple[tuple[float, str | None], ...] = (
    (1.50, "000"),
    (1.75, "00"),
    (2.0, "0"),
    (2.25, "1"),
    (2.75, "2"),
    (3.0, None),
    (3.125, "3"),
    (3.25, "3"),
    (3.50, "4"),
    (3.75, "5"),
    (4.0, "6"),
    (4.25, "6"),
    (4.50, "7"),
    (5.0, "8"),
    (5.25, "9"),
    (5.50, "9"),
    (5.75, "10"),
    (6.0, "10"),
    (6.50, "10 1/2"),
    (7.0, None),
    (8.0, "11"),
    (9.0, "13"),
    (10.0, "15"),
    (12.50, "17"),
    (12.75, "17"),
    (15.0, "19"),
    (19.0, "35"),
    (25.0, "50"),
    (35.0, "70"),
)

# Every steel pair the Council prints. The same number is not one size.
STEEL_HOOKS: tuple[tuple[float, str], ...] = (
    (3.50, "00"),
    (3.25, "0"),
    (2.75, "1"),
    (2.70, "00"),
    (2.55, "0"),
    (2.35, "1"),
    (2.25, "2"),
    (2.20, "2"),
    (2.10, "3"),
    (2.0, "4"),
    (1.90, "5"),
    (1.80, "6"),
    (1.75, "4/0"),
    (1.70, "5"),
    (1.65, "7"),
    (1.60, "6"),
    (1.50, "8/7/2"),
    (1.40, "9/8"),
    (1.30, "10"),
    (1.25, "9/4"),
    (1.15, "10"),
    (1.10, "11"),
    (1.05, "11"),
    (1.0, "12/6"),
    (0.95, "13"),
    (0.90, "14/8"),
    (0.85, "13"),
    (0.75, "14/10"),
    (0.60, "12"),
)

STEEL_NOTE = (
    "A higher steel-hook number is smaller. The Council's chart gives more "
    "than one millimeter for the same number, so a steel number is not stored "
    "as one millimeter."
)

THREAD_NOTE = (
    "Crochet thread sizes run the other way from steel hooks: a smaller thread "
    "number is thicker. Common sizes are 3, 5, 10, 20, and 30. Size 100 is the finest."
)

ABBREVIATIONS: dict[str, str] = {
    "alt": "alternate",
    "approx": "approximately",
    "beg": "begin/beginning",
    "bet": "between",
    "BL": "back loop",
    "BLO": "back loop only",
    "bo": "bobble",
    "BP": "back post",
    "BPdc": "back post double crochet",
    "BPdtr": "back post double treble crochet",
    "BPhdc": "back post half double crochet",
    "BPsc": "back post single crochet",
    "BPtr": "back post treble crochet",
    "CC": "contrasting color",
    "ch": "chain stitch",
    "ch-": "refer to chain or space previously made, e.g., ch-1 space",
    "ch-sp": "chain space",
    "CL": "cluster",
    "cont": "continue",
    "dc": "double crochet",
    "dc2tog": "double crochet 2 stitches together",
    "dec": "decrease",
    "dtr": "double treble crochet",
    "edc": "extended double crochet",
    "ehdc": "extended half double crochet",
    "esc": "extended single crochet",
    "etr": "extended treble crochet",
    "FL": "front loop",
    "FLO": "front loop only",
    "foll": "following",
    "FP": "front post",
    "FPdc": "front post double crochet",
    "FPdtr": "front post double treble crochet",
    "FPhdc": "front post half double crochet",
    "FPsc": "front post single crochet",
    "FPtr": "front post treble crochet",
    "hdc": "half double crochet",
    "hdc2tog": "half double crochet 2 stitches together",
    "inc": "increase",
    "lp": "loop",
    "m": "marker",
    "MC": "main color",
    "pat": "pattern",
    "patt": "pattern",
    "pc": "popcorn stitch",
    "pm": "place marker",
    "prev": "previous",
    "ps": "puff stitch",
    "puff": "puff stitch",
    "rem": "remaining",
    "rep": "repeat",
    "rnd": "round",
    "RS": "right side",
    "sc": "single crochet",
    "sc2tog": "single crochet 2 stitches together",
    "sh": "shell",
    "sk": "skip",
    "sl st": "slip stitch",
    "sl m": "slip marker",
    "sm": "slip marker",
    "sp": "space",
    "st": "stitch",
    "tbl": "through back loop",
    "t-ch": "turning chain",
    "tch": "turning chain",
    "tog": "together",
    "tr": "treble crochet",
    "tr2tog": "treble crochet 2 stitches together",
    "trtr": "triple treble crochet",
    "WS": "wrong side",
    "yo": "yarn over",
    "yoh": "yarn over hook",
}

TUNISIAN: dict[str, str] = {
    "etss": "extended Tunisian simple stitch",
    "FwP": "forward pass",
    "RetP": "return pass",
    "tdc": "Tunisian double crochet",
    "tfs": "Tunisian full stitch",
    "thdc": "Tunisian half double crochet",
    "tks": "Tunisian knit stitch",
    "tps": "Tunisian purl stitch",
    "trs": "Tunisian reverse stitch",
    "tsc": "Tunisian single crochet",
    "tss": "Tunisian simple stitch",
    "tslst": "Tunisian slip stitch",
    "ttr": "Tunisian treble crochet",
    "ttw": "Tunisian twisted",
}

# U.S. and Canada term, then the U.K. term for the same stitch.
US_UK: tuple[tuple[str, str], ...] = (
    ("slip stitch (sl st)", "slip stitch (ss)"),
    ("single crochet (sc)", "double crochet (dc)"),
    ("half double crochet (hdc)", "half treble (htr)"),
    ("double crochet (dc)", "treble (tr)"),
    ("treble (tr)", "double treble (dtr)"),
    ("double treble (dtr)", "triple treble (trtr)"),
)

TERM_DIFFERENCES: tuple[tuple[str, str], ...] = (
    ("gauge", "tension"),
    ("yarn over (yo)", "yarn over hook (yoh)"),
)

MEASUREMENTS: dict[str, str] = {
    "in": "inch",
    "cm": "centimeter",
    "g": "gram",
    "m": "meter",
    "mm": "millimeter",
    "oz": "ounce",
    "yd": "yard",
}

CHART_SYMBOLS: tuple[str, ...] = (
    "chain (ch)",
    "slip stitch (sl st)",
    "single crochet (sc)",
    "half double crochet (hdc)",
    "double crochet (dc)",
    "treble crochet (tr)",
    "double treble crochet (dtr)",
    "sc2tog",
    "sc3tog",
    "dc2tog",
    "dc3tog",
    "3-dc cluster",
    "3-hdc cluster/puff st/bobble",
    "5-dc popcorn",
    "5-dc shell",
    "ch-3 picot",
    "front post dc (FPdc)",
    "back post dc (BPdc)",
    "worked in back loop only",
    "worked in front loop only",
)

SKILL_LEVELS: tuple[tuple[str, str], ...] = (
    ("Basic", "Projects using basic stitches. May include basic increases and decreases."),
    ("Easy", "Projects may include simple stitch patterns, color work, and/or shaping."),
    ("Intermediate", "Projects may include involved stitch patterns, color work, and/or shaping."),
    ("Complex", "Projects may include complex stitch patterns, color work, and or/shaping using a variety of techniques and stitches simultaneously."),
)

# The Complex sentence is stored as the page prints it, including "and or/shaping".

EASE: tuple[tuple[str, str], ...] = (
    ("Very close fitting", "About 2 to 4 inches (5 to 10 cm) less than the bust or chest."),
    ("Close fitting", "The actual bust or chest measurement. Zero ease."),
    ("Classic fit", "About 2 to 4 inches (5 to 10 cm) more than the bust or chest."),
    ("Loose fit", "About 4 to 6 inches (10 to 15 cm) more than the bust or chest."),
    ("Oversized", "About 6 inches (15 cm) or more than the bust or chest."),
)

BODY_MEASURES: tuple[str, ...] = (
    "chest/bust",
    "center back neck-to-wrist",
    "back waist length",
    "cross back",
    "arm length",
    "upper arm",
    "armhole depth",
    "waist",
    "hip",
    "head circumference",
    "foot circumference",
    "sock height",
    "total foot length",
    "hand circumference",
    "wrist circumference",
    "hand length",
)

CARE_CATEGORIES: tuple[str, ...] = (
    "washing",
    "bleaching",
    "drying",
    "ironing",
    "professional textile care",
)

REPEAT_MARKS: tuple[tuple[str, str], ...] = (
    ("*", "repeat the instructions following the single asterisk as directed"),
    ("**", "repeat instructions between asterisks as many times as directed or repeat at specified locations"),
    ("{}", "work instructions within brackets as many times as directed"),
    ("[]", "work instructions within brackets as many times as directed"),
    ("()", "work instructions within parentheses as many times as directed or work a group of stitches all in the same stitch or space"),
)

LENGTHS: tuple[tuple[str, str], ...] = (
    ("Child hip length", "2 inches / 5 cm down from the waist"),
    ("Child tunic length", "6 inches / 15 cm down from the waist"),
    ("Woman hip length", "6 inches / 15 cm down from the waist"),
    ("Woman tunic length", "11 inches / 28 cm down from the waist"),
    ("Men", "Usually 1-2 inches / 2.5-5 cm from the back hip length"),
)

HAND_NOTE = (
    "The HAND symbol is for gauge on yarns that do not use a hook or a needle, "
    "including loop yarns and arm or hand knitting and crocheting. It can also "
    "mark a pattern that needs no tools."
)

CARE_NOTE = (
    "A large X through a care symbol means do not. International wash symbols "
    "use Celsius. North American yarn labels may list both Celsius and Fahrenheit. "
    "The symbol pictures are on the Council page and are not copied here."
)


def _band(pair: tuple, stitch: str) -> str:
    low, high = pair
    if low is None:
        return f"{high} {stitch} and fewer"
    return f"{low}-{high} {stitch}"


def yarn_by_number(number: int) -> dict | None:
    for item in YARN_WEIGHTS:
        if item["number"] == number:
            return item
    return None


def yarn_by_name(name: str) -> dict | None:
    key = name.strip().lower()
    for item in YARN_WEIGHTS:
        names = {item["name"].lower(), *item["types"]}
        if key in names:
            return item
    return None


def hook_label(mm: float) -> str | None:
    for size, label in CROCHET_HOOKS:
        if size == mm:
            return label
    return None


def steel_rows_for_label(label: str) -> tuple[tuple[float, str], ...]:
    """Printed rows whose U.S. cell is exactly this label.

    A slash cell such as 8/7/2 is one printed label, not three sizes.
    This is not a unique number-to-millimeter map.
    """
    return tuple(row for row in STEEL_HOOKS if row[1] == label)


def render_markdown() -> str:
    lines = [
        "# Crochet standards reference",
        "",
        CREDIT,
        "",
        "This page stores the published tables. It does not count the stitches in a pattern, and it does not change a check result. It does not list every commercial yarn brand. There is no such published list.",
        "",
        SIZE_8_NOTE,
        "",
        "## Yarn weights 0 to 7",
        "",
        "Guidelines only. Always follow the gauge in the pattern. Lace is not given a single-crochet band: the Council prints 32-42 double crochets and says a lace range is hard to determine.",
        "",
        "| Number | Name | Also called | Knit gauge / 4 inches | Crochet gauge / 4 inches | Hook range | Wraps per inch |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in YARN_WEIGHTS:
        lines.append(
            "| {number} | {name} | {types} | {knit} | {crochet} | {hook} | {wpi} |".format(
                number=item["number"],
                name=item["name"],
                types=", ".join(item["types"]),
                knit=_band(item["knit_gauge"], "stockinette"),
                crochet=_band(item["crochet_gauge"], item["crochet_gauge_stitch"]),
                hook=item["hook_note"],
                wpi=item["wpi"],
            )
        )
    lines.extend(["", "## Crochet hooks", "", "The millimeter is the measurement. A blank U.S. label means the Council printed no letter for that millimeter.", "", "| mm | U.S. label |", "| --- | --- |"])
    for mm, label in CROCHET_HOOKS:
        lines.append(f"| {mm:g} | {label or ''} |")
    lines.extend(["", "## Knitting needles", "", "Stored so a needle size is not mistaken for a crochet hook letter. A knitting needle is not a crochet hook.", "", "| mm | U.S. label |", "| --- | --- |"])
    for mm, label in KNITTING_NEEDLES:
        lines.append(f"| {mm:g} | {label or ''} |")
    lines.extend(["", "## Steel hooks and thread", "", STEEL_NOTE, "", THREAD_NOTE, "", "A slash label such as 8/7/2 is one printed cell, not three sizes.", "", "| mm | Printed U.S. label |", "| --- | --- |"])
    for mm, label in STEEL_HOOKS:
        lines.append(f"| {mm:g} | {label} |")
    lines.extend(["", HAND_NOTE, "", "## Repeat marks", "", "The Council page uses the word brackets for both the brace row and the bracket row. That wording is kept.", ""])
    for mark, text in REPEAT_MARKS:
        lines.append(f"- `{mark}`: {text}")
    lines.extend(["", "## Garment length guides", "", "These are the length guides printed as text. The numbered body-size charts are pictures on the Council page and are not copied here.", ""])
    for name, text in LENGTHS:
        lines.append(f"- {name}: {text}")
    lines.extend(["", "## U.S. abbreviations", "", "Designers may define more abbreviations in a pattern. Those extras are not errors in this list.", ""])
    for key in sorted(ABBREVIATIONS, key=str.lower):
        lines.append(f"- `{key}`: {ABBREVIATIONS[key]}")
    lines.extend(["", "## Tunisian abbreviations", ""])
    for key, value in TUNISIAN.items():
        lines.append(f"- `{key}`: {value}")
    lines.extend(["", "## U.S. and U.K. terms", "", "Canada follows the U.S. stitch names on the Council chart. Gauge is tension in the U.K. and Canada. Yarn over is yarn over hook there.", ""])
    for left, right in US_UK:
        lines.append(f"- {left} is {right}")
    lines.extend(["", "## Chart symbol names", "", "The pictures stay on the Council page. The names are:", ""])
    for name in CHART_SYMBOLS:
        lines.append(f"- {name}")
    lines.extend(["", "## Skill, ease, and measuring", ""])
    for name, text in SKILL_LEVELS:
        lines.append(f"- {name}: {text}")
    lines.append("")
    for name, text in EASE:
        lines.append(f"- {name}: {text}")
    lines.extend(["", "Body measurements named by the Council: " + ", ".join(BODY_MEASURES) + ".", "", "## Care", "", CARE_NOTE, ""])
    for name in CARE_CATEGORIES:
        lines.append(f"- {name}")
    lines.extend(["", f"One inch is {INCH_TO_CM} cm. A line that copies the same number for both is not a conversion.", ""])
    return "\n".join(lines) + "\n"


def summary() -> str:
    return (
        f"{CREDIT}\n"
        f"Yarn weights stored: 0-7. Size 8 numbers are not published.\n"
        f"Crochet hook rows: {len(CROCHET_HOOKS)}. Knitting needle rows: {len(KNITTING_NEEDLES)}.\n"
        f"Steel pairs stored: {len(STEEL_HOOKS)}. They are not one number to one millimeter.\n"
        f"U.S. abbreviations: {len(ABBREVIATIONS)}. Tunisian: {len(TUNISIAN)}.\n"
        "The written page is docs/standards.md.\n"
    )
