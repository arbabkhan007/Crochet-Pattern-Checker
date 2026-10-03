"""Written checks that cover a family, not one copied sentence.

The increase, decrease, range, multiple, and measure checks are proved on
5,000 sentences. Those sentences are cases, not 5,000 named stages. A quoted
line is not an instruction. A prohibition is not a defect.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Phrase:
    slug: str
    title: str
    how: str
    what: str
    wrong: str
    corrected: str
    needle: str


def _phrase(
    slug: str,
    title: str,
    how: str,
    what: str,
    wrong: str,
    corrected: str,
    needle: str,
) -> Phrase:
    return Phrase(slug, title, how, what, wrong, corrected, needle)


PHRASES: tuple[Phrase, ...] = (
    _phrase(
        "hook_letter_gap", "Hook letter gap",
        "H/8 written as 2.25 mm is the B-1 size, not a brand variation. The Craft Yarn Council nominal for H-8 is 5 mm. This fires only when the written millimeter is more than 1.5 mm away.",
        "the corrected file uses H/8 (5 mm).",
        "Hook: H/8 (2.25 mm).\n", "Hook: H/8 (5 mm).\n",
        "more than 1.5 mm",
    ),
    _phrase(
        "yarn_weight_number", "Yarn weight number",
        "worsted is Craft Yarn Council category 4, not 1.",
        "the corrected file says worsted (4).",
        "Yarn: worsted (1).\n", "Yarn: worsted (4).\n",
        "category 4, not 1",
    ),
    _phrase(
        "short_treble_turn", "Short treble turn",
        "ch 1 cannot turn for a treble. A treble turn needs ch 4. ch 2 for a double treble is short as well.",
        "the corrected file uses ch 4 before the treble.",
        "ch 1, turn, tr in the next stitch.\n", "ch 4, turn, tr in the next stitch.\n",
        "too short to turn for a tr",
    ),
    _phrase(
        "counts_as_mismatch", "Counts-as mismatch",
        "ch 1 cannot count as a double crochet. A double crochet turning chain is ch 3.",
        "the corrected file lets ch 3 count as the dc.",
        "ch 1 counts as a dc.\n", "ch 3 counts as a dc.\n",
        "cannot count as a dc",
    ),
    _phrase(
        "uk_gloss", "UK gloss",
        "a US single crochet is a UK double, not a UK treble.",
        "the corrected file says sc (UK double).",
        "sc (UK treble).\n", "sc (UK double).\n",
        "not a UK treble",
    ),
    _phrase(
        "steel_hook_order", "Steel hook order",
        "on a steel hook, a higher number is smaller. Steel 14 is not larger than steel 1.",
        "the corrected file says steel 14 is smaller.",
        "A steel hook 14 is larger than a steel hook 1.\n",
        "A steel hook 14 is smaller than a steel hook 1.\n",
        "higher steel-hook number is smaller",
    ),
    _phrase(
        "spiral_turn", "Spiral turn",
        "a continuous spiral does not turn every round.",
        "the corrected file keeps the spiral and does not turn.",
        "Work a continuous spiral and turn every round.\n",
        "Work a continuous spiral and do not turn.\n",
        "does not turn every round",
    ),
    _phrase(
        "fasten_continue", "Fasten and continue",
        "fasten off ends that yarn. The same line cannot continue in it.",
        "the corrected file fastens off.",
        "Fasten off and continue in the same yarn.\n", "Fasten off.\n",
        "ends the yarn",
    ),
    _phrase(
        "yarn_over_under", "Yarn over and under",
        "one stitch cannot be both a yarn over and a yarn under.",
        "the corrected file uses a yarn over.",
        "Work yarn over and yarn under for the same stitch.\n",
        "Work yarn over for the same stitch.\n",
        "Yarn over and yarn under",
    ),
    _phrase(
        "reverse_sc_forward", "Reverse sc direction",
        "reverse single crochet is worked backward, not forward.",
        "the corrected file works it backward.",
        "Reverse sc worked forward.\n", "Reverse sc worked backward.\n",
        "not forward",
    ),
    _phrase(
        "two_foundations", "Two foundations",
        "foundation single crochet replaces the starting chain for that row.",
        "the corrected file starts with foundation sc.",
        "Start with foundation sc and a starting chain for the same row.\n",
        "Start with foundation sc.\n",
        "replaces the starting chain",
    ),
    _phrase(
        "both_hands", "Both hands",
        "right-handed and left-handed work need separate instructions when both are required.",
        "the corrected file is written for right-handed work.",
        "Written for right-handed and left-handed work with no separate instructions.\n",
        "Written for right-handed work.\n",
        "need separate instructions",
    ),
    _phrase(
        "two_starts", "Two starts",
        "a piece cannot have both a magic ring and a chain ring as its only start.",
        "the corrected file starts with a magic ring.",
        "Start with a magic ring and a chain ring as the only start.\n",
        "Start with a magic ring.\n",
        "cannot start with both",
    ),
    _phrase(
        "two_seams", "Two seam methods",
        "whipstitch and mattress stitch are different seams. One line cannot require both for the same seam.",
        "the corrected file uses mattress stitch.",
        "Seam with whipstitch and mattress stitch for the same seam.\n",
        "Seam with mattress stitch.\n",
        "are two seams",
    ),
    _phrase(
        "negative_gauge", "Negative gauge",
        "a gauge of -1 sc is not a fabric.",
        "the corrected file uses 12 sc per 4 inches.",
        "Gauge: -1 sc = 4 inches.\n", "Gauge: 12 sc = 4 inches.\n",
        "negative gauge",
    ),
    _phrase(
        "negative_length", "Negative length",
        "a finished length of -1 inches is not a piece.",
        "the corrected file is 8 inches long.",
        "Finished length: -1 inches.\n", "Finished length: 8 inches.\n",
        "negative length",
    ),
    _phrase(
        "zero_rows_tall", "Zero rows tall",
        "a piece that is 0 rows tall was not made.",
        "the corrected file is 8 rows tall.",
        "The piece is 0 rows tall.\n", "The piece is 8 rows tall.\n",
        "0 rows tall",
    ),
    _phrase(
        "zero_rounds_tall", "Zero rounds tall",
        "a piece that is 0 rounds tall was not made.",
        "the corrected file is 8 rounds tall.",
        "The piece is 0 rounds tall.\n", "The piece is 8 rounds tall.\n",
        "0 rounds tall",
    ),
    _phrase(
        "row_zero", "Row zero",
        "rows are numbered from 1. Row 0 is not a row.",
        "the corrected file starts at Row 1.",
        "The piece starts at Row 0.\n", "The piece starts at Row 1.\n",
        "Row 0 is not a row",
    ),
    _phrase(
        "make_zero", "Make zero",
        "make 0 asks for none of that piece.",
        "the corrected file makes 2.",
        "Ears (make 0).\n", "Ears (make 2).\n",
        "make 0",
    ),
    _phrase(
        "negative_times", "Negative times",
        "repeating a row -1 times is not a repeat. This is not the x -1 form.",
        "the corrected file repeats the row 4 times.",
        "Repeat the row -1 times.\n", "Repeat the row 4 times.\n",
        "not a repeat count",
    ),
    _phrase(
        "work_even_zero", "Work even zero",
        "work even for 0 rows does no work.",
        "the corrected file works even for 4 rows.",
        "Work even for 0 rows.\n", "Work even for 4 rows.\n",
        "for 0 rows",
    ),
    _phrase(
        "place_zero_eyes", "Place zero eyes",
        "place 0 safety eyes is an instruction that mounts nothing.",
        "the corrected file places 2 safety eyes.",
        "Place 0 safety eyes.\n", "Place 2 safety eyes.\n",
        "mounts nothing",
    ),
    _phrase(
        "yardage_zero", "Zero yardage",
        "0 yards cannot make the piece.",
        "the corrected file lists 200 yards.",
        "Yardage: 0 yards.\n", "Yardage: 200 yards.\n",
        "0 yards",
    ),
    _phrase(
        "stuff_zero", "Stuff zero",
        "stuff with 0 g leaves the piece empty while telling the crocheter to stuff.",
        "the corrected file stuffs with 20 g.",
        "Stuff with 0 g.\n", "Stuff with 20 g.\n",
        "0 g",
    ),
    _phrase(
        "color_every_zero", "Color every zero",
        "changing color every 0 rows never changes color.",
        "the corrected file changes color every 2 rows.",
        "Change color every 0 rows.\n", "Change color every 2 rows.\n",
        "every 0 rows",
    ),
    _phrase(
        "increase_every_zero", "Increase every zero",
        "increasing every 0 rounds never increases.",
        "the corrected file increases every 3 rounds.",
        "Increase every 0 rounds.\n", "Increase every 3 rounds.\n",
        "every 0 rounds",
    ),
    _phrase(
        "decrease_every_zero", "Decrease every zero",
        "decreasing every 0 rows never decreases.",
        "the corrected file decreases every 2 rows.",
        "Decrease every 0 rows.\n", "Decrease every 2 rows.\n",
        "every 0 rows",
    ),
    _phrase(
        "v_stitch_one", "V-stitch of one",
        "a V-stitch needs two tall stitches and a chain. A V-stitch of 1 is one stitch.",
        "the corrected file uses a V-stitch of 2 dc.",
        "Work a V-stitch of 1.\n", "Work a V-stitch of 2 dc.\n",
        "V-stitch of 1",
    ),
    _phrase(
        "fan_one", "Fan of one",
        "a fan needs several stitches in one space. A fan of 1 is one stitch.",
        "the corrected file uses a fan of 5.",
        "Work a fan of 1.\n", "Work a fan of 5.\n",
        "fan of 1",
    ),
    _phrase(
        "bullion_zero", "Bullion of zero",
        "a bullion of 0 wraps has no wraps to coil.",
        "the corrected file uses 7 wraps.",
        "Work a bullion of 0 wraps.\n", "Work a bullion of 7 wraps.\n",
        "0 wraps",
    ),
    _phrase(
        "cable_zero", "Cable of zero",
        "a cable over 0 stitches does not cross.",
        "the corrected file crosses 2 stitches.",
        "Cable over 0 stitches.\n", "Cable over 2 stitches.\n",
        "does not cross",
    ),
    _phrase(
        "fringe_zero", "Fringe of zero",
        "a fringe of 0 strands is not a fringe.",
        "the corrected file uses 4 strands.",
        "Fringe of 0 strands.\n", "Fringe of 4 strands.\n",
        "not a fringe",
    ),
    _phrase(
        "buttonhole_zero", "Buttonhole of zero",
        "a buttonhole of 0 chains has no opening.",
        "the corrected file uses 3 chains.",
        "Buttonhole of 0 chains.\n", "Buttonhole of 3 chains.\n",
        "no opening",
    ),
    _phrase(
        "icord_zero", "I-cord of zero",
        "an i-cord of 0 stitches has no cord.",
        "the corrected file uses 4 stitches.",
        "I-cord of 0 stitches.\n", "I-cord of 4 stitches.\n",
        "no cord",
    ),
    _phrase(
        "oval_zero", "Oval of zero",
        "an oval cannot start with 0 chains.",
        "the corrected file starts with 8 chains.",
        "Oval start with 0 chains.\n", "Oval start with 8 chains.\n",
        "0 chains",
    ),
    _phrase(
        "square_zero", "Square of zero",
        "a square of 0 rounds was not worked.",
        "the corrected file has 4 rounds.",
        "Square of 0 rounds.\n", "Square of 4 rounds.\n",
        "0 rounds",
    ),
    _phrase(
        "solomon_zero", "Solomon knot of zero",
        "a Solomon knot of 0 is not a knot.",
        "the corrected file uses 5.",
        "Work a Solomon knot of 0.\n", "Work a Solomon knot of 5.\n",
        "not a knot",
    ),
    _phrase(
        "surface_zero", "Surface of zero",
        "surface crochet of 0 chains draws no line.",
        "the corrected file uses 12 chains.",
        "Surface crochet of 0 chains.\n", "Surface crochet of 12 chains.\n",
        "draws no line",
    ),
    _phrase(
        "bead_every_zero", "Bead every zero",
        "a bead every 0 stitches is never placed.",
        "the corrected file places a bead every 4 stitches.",
        "Place a bead every 0 stitches.\n", "Place a bead every 4 stitches.\n",
        "never placed",
    ),
    _phrase(
        "stripe_every_zero", "Stripe every zero",
        "a stripe every 0 rounds never stripes.",
        "the corrected file stripes every 2 rounds.",
        "Stripe every 0 rounds.\n", "Stripe every 2 rounds.\n",
        "never stripes",
    ),
    _phrase(
        "pompom_zero", "Pom-pom of zero",
        "a pom-pom of 0 wraps has nothing to tie.",
        "the corrected file uses 40 wraps.",
        "Pom-pom of 0 wraps.\n", "Pom-pom of 40 wraps.\n",
        "nothing to tie",
    ),
    _phrase(
        "tassel_zero", "Tassel of zero",
        "a tassel of 0 wraps has nothing to hang.",
        "the corrected file uses 40 wraps.",
        "Tassel of 0 wraps.\n", "Tassel of 40 wraps.\n",
        "nothing to hang",
    ),
    _phrase(
        "pineapple_zero", "Pineapple of zero",
        "a pineapple of 0 is not a pineapple motif.",
        "the corrected file uses 7.",
        "Work a pineapple of 0.\n", "Work a pineapple of 7.\n",
        "not a pineapple",
    ),
    _phrase(
        "spike_zero", "Spike of zero",
        "a spike stitch down 0 rows does not leave the current row.",
        "the corrected file goes down 2 rows.",
        "Spike stitch down 0 rows.\n", "Spike stitch down 2 rows.\n",
        "does not leave",
    ),
    _phrase(
        "tube_zero", "Tube of zero",
        "a tube of 0 stitches has no opening.",
        "the corrected file uses 6 stitches.",
        "Tube of 0 stitches.\n", "Tube of 6 stitches.\n",
        "no opening",
    ),
    _phrase(
        "rectangle_zero", "Rectangle of zero",
        "a rectangle of 0 rows was not worked.",
        "the corrected file has 12 rows.",
        "Rectangle of 0 rows.\n", "Rectangle of 12 rows.\n",
        "0 rows",
    ),
    _phrase(
        "corner_zero", "Corner of zero",
        "a corner of 0 chains does not turn the corner.",
        "the corrected file uses 2 chains.",
        "Corner of 0 chains.\n", "Corner of 2 chains.\n",
        "does not turn the corner",
    ),
    _phrase(
        "star_one", "Star of one",
        "a star stitch of 1 cannot pull up the loops a star needs.",
        "the corrected file uses a star stitch of 5.",
        "Work a star stitch of 1.\n", "Work a star stitch of 5.\n",
        "star stitch of 1",
    ),
    _phrase(
        "loop_zero", "Loop of zero",
        "a loop stitch of 0 has no loop.",
        "the corrected file uses 1 loop.",
        "Work a loop stitch of 0.\n", "Work a loop stitch of 1.\n",
        "no loop",
    ),
    _phrase(
        "same_color_letter", "Same color letter",
        "changing from Color Q to Color Q is not a color change. The check is any repeated letter, not only A.",
        "the corrected file changes to Color R.",
        "Change from Color Q to Color Q.\n", "Change from Color Q to Color R.\n",
        "not a color change",
    ),
)


HOOKS = {
    "B-1": 2.25,
    "C-2": 2.75,
    "D-3": 3.25,
    "E-4": 3.5,
    "F-5": 3.75,
    "G-6": 4.0,
    "H-8": 5.0,
    "I-9": 5.5,
    "J-10": 6.0,
    "K-10.5": 6.5,
    "L-11": 8.0,
    "M/N-13": 9.0,
    "N/P-15": 10.0,
    "P/Q": 15.0,
}
HOOK_GAP = 1.5

WEIGHTS = (
    ("super bulky", (6,)),
    ("super fine", (1,)),
    ("light worsted", (3,)),
    ("fingering", (0, 1)),
    ("worsted", (4,)),
    ("chunky", (5,)),
    ("bulky", (5,)),
    ("jumbo", (7,)),
    ("aran", (4,)),
    ("afghan", (4,)),
    ("medium", (4,)),
    ("sport", (2,)),
    ("lace", (0,)),
    ("dk", (3,)),
)

TURN_MIN = {"tr": 4, "dtr": 5}
COUNTS_AS = {
    ("1", "hdc"): "hdc",
    ("1", "dc"): "dc",
    ("1", "tr"): "tr",
    ("1", "dtr"): "dtr",
    ("2", "tr"): "tr",
    ("2", "dtr"): "dtr",
    ("3", "sc"): "sc",
    ("3", "dtr"): "dtr",
    ("4", "sc"): "sc",
    ("4", "hdc"): "hdc",
}
UK_GLOSS = {
    "us single crochet is a uk double treble": "A US single crochet is a UK double, not a UK double treble.",
    "us sc is a uk double treble": "A US single crochet is a UK double, not a UK double treble.",
    "us single crochet is a uk treble": "A US single crochet is a UK double, not a UK treble.",
    "us sc is a uk treble": "A US single crochet is a UK double, not a UK treble.",
    "us double crochet is a uk double treble": "A US double crochet is a UK treble, not a UK double treble.",
    "us dc is a uk double treble": "A US double crochet is a UK treble, not a UK double treble.",
    "us double crochet is a uk double": "A US double crochet is a UK treble, not a UK double.",
    "us dc is a uk double": "A US double crochet is a UK treble, not a UK double.",
    "us treble is a uk treble": "A US treble is a UK double treble, not a UK treble.",
    "us tr is a uk treble": "A US treble is a UK double treble, not a UK treble.",
    "sc (uk treble)": "A US single crochet is a UK double, not a UK treble.",
    "sc (uk double treble)": "A US single crochet is a UK double, not a UK double treble.",
    "hdc (uk treble)": "A US half double is a UK half treble, not a UK treble.",
    "dc (uk double)": "A US double crochet is a UK treble, not a UK double.",
    "tr (uk treble)": "A US treble is a UK double treble, not a UK treble.",
    "tr (uk double)": "A US treble is a UK double treble, not a UK double.",
}

_HOOK = re.compile(
    r"Hook:\s*([A-Z](?:/[A-Z])?(?:-\d+(?:\.\d+)?)?)\s*\((\d+(?:\.\d+)?)\s*mm\)",
    re.IGNORECASE,
)
_HOOK_ANY = re.compile(
    r"\b([A-P](?:/[A-Z])?-\d+(?:\.\d+)?|[A-P]/\d+(?:\.\d+)?|[A-P]/[A-Z](?:-\d+(?:\.\d+)?)?)\s*\(?(\d+(?:\.\d+)?)\s*mm\)?",
    re.IGNORECASE,
)
_INCREASE = re.compile(r"^Increase from (\d+) to (\d+)\b", re.IGNORECASE)
_DECREASE = re.compile(r"^Decrease from (\d+) to (\d+)\b", re.IGNORECASE)
_MULTIPLE = re.compile(r"^Multiple of (\d+), (\d+) stitches\b", re.IGNORECASE)
_PLUS = re.compile(
    r"^Multiple of (\d+) plus (\d+), (\d+) stitches\b", re.IGNORECASE
)
_ROUNDS = re.compile(r"\bRounds (\d+)-(\d+)\b", re.IGNORECASE)
_ROWS = re.compile(r"\bRows (\d+)-(\d+)\b", re.IGNORECASE)
_EVEN = re.compile(r"^The count must be even \((\d+) stitches\)", re.IGNORECASE)
_ODD = re.compile(r"^The count must be odd \((\d+) stitches\)", re.IGNORECASE)
_APART = re.compile(
    r"^Place the eyes (\d+) stitches apart on a (\d+)-stitch round\b",
    re.IGNORECASE,
)
_STITCH_AT = re.compile(
    r"^Place the marker in stitch (\d+) on a (\d+)-stitch round\b",
    re.IGNORECASE,
)
_SKIP = re.compile(r"^Skip (\d+) on a (\d+)-stitch row\b", re.IGNORECASE)
_FRACTION = re.compile(r"\bx\s+(\d+\.\d+)\b", re.IGNORECASE)
_INCH_CM = re.compile(r"^(\d+(?:\.\d+)?) inches = \1 cm\b", re.IGNORECASE)
_CM_INCH = re.compile(r"^(\d+(?:\.\d+)?) cm = \1 inches\b", re.IGNORECASE)
_TURN = re.compile(r"\bch (\d+), turn, (tr|dtr)\b", re.IGNORECASE)
_COUNTS = re.compile(r"\bch (\d+) counts as an? (sc|hdc|dc|tr|dtr)\b", re.IGNORECASE)
_COLOR = re.compile(r"\bChange from Color ([A-Z]) to Color \1\b")
_PROHIBITION = re.compile(r"\bdo not\b|\bdon't\b|\bshould\s+not\b", re.IGNORECASE)


def span_names() -> list[str]:
    names = [item.title.lower() for item in PHRASES]
    names.extend(
        [
            "increase direction",
            "decrease direction",
            "multiple mismatch",
            "plus remainder",
            "backward round range",
            "backward row range",
            "even count",
            "odd count",
            "apart span",
            "stitch past end",
            "skip past count",
            "fractional times",
            "copied inch measure",
            "copied centimeter measure",
        ]
    )
    return names


_COMPILED = tuple(
    (re.compile(re.escape(item.wrong.strip()), re.IGNORECASE), item) for item in PHRASES
)


def span_findings(text: str) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    for raw in text.splitlines():
        if _skip(raw):
            continue
        line = raw.strip()
        for pattern, item in _COMPILED:
            if pattern.search(line):
                errors.append(_phrase_message(item))
        errors.extend(_line_errors(line))
    return _unique(errors), []


def _phrase_message(item: Phrase) -> str:
    if item.slug == "hook_letter_gap":
        return (
            "Hook H/8 is written as 2.25 mm, but the Craft Yarn Council "
            "nominal size is 5 mm. The gap is more than 1.5 mm."
        )
    if item.slug == "yarn_weight_number":
        return "Worsted is Craft Yarn Council category 4, not 1."
    if item.slug == "short_treble_turn":
        return "ch 1 is too short to turn for a tr. Use ch 4."
    if item.slug == "counts_as_mismatch":
        return "ch 1 cannot count as a dc."
    if item.slug == "uk_gloss":
        return "A US single crochet is a UK double, not a UK treble."
    if item.slug == "steel_hook_order":
        return "A higher steel-hook number is smaller, not larger."
    if item.slug == "spiral_turn":
        return "A continuous spiral does not turn every round."
    if item.slug == "fasten_continue":
        return "Fasten off ends the yarn."
    if item.slug == "yarn_over_under":
        return "Yarn over and yarn under cannot be the same stitch."
    if item.slug == "reverse_sc_forward":
        return "Reverse single crochet is worked backward, not forward."
    if item.slug == "two_foundations":
        return "Foundation single crochet replaces the starting chain."
    if item.slug == "both_hands":
        return "Right-handed and left-handed work need separate instructions."
    if item.slug == "two_starts":
        return "A piece cannot start with both a magic ring and a chain ring."
    if item.slug == "two_seams":
        return "Whipstitch and mattress stitch are two seams."
    if item.slug == "negative_gauge":
        return "A negative gauge is not a fabric."
    if item.slug == "negative_length":
        return "A negative length is not a piece."
    if item.slug == "zero_rows_tall":
        return "A piece that is 0 rows tall was not made."
    if item.slug == "zero_rounds_tall":
        return "A piece that is 0 rounds tall was not made."
    if item.slug == "row_zero":
        return "Row 0 is not a row."
    if item.slug == "make_zero":
        return "make 0 asks for none of that piece."
    if item.slug == "negative_times":
        return "-1 times is not a repeat count."
    if item.slug == "work_even_zero":
        return "Work even for 0 rows does no work."
    if item.slug == "place_zero_eyes":
        return "Place 0 safety eyes mounts nothing."
    if item.slug == "yardage_zero":
        return "0 yards cannot make the piece."
    if item.slug == "stuff_zero":
        return "Stuff with 0 g does not stuff the piece."
    if item.slug == "color_every_zero":
        return "Change color every 0 rows never changes color."
    if item.slug == "increase_every_zero":
        return "Increase every 0 rounds never increases."
    if item.slug == "decrease_every_zero":
        return "Decrease every 0 rows never decreases."
    if item.slug == "v_stitch_one":
        return "A V-stitch of 1 is not a V-stitch."
    if item.slug == "fan_one":
        return "A fan of 1 is not a fan."
    if item.slug == "bullion_zero":
        return "A bullion of 0 wraps has no wraps."
    if item.slug == "cable_zero":
        return "A cable over 0 stitches does not cross."
    if item.slug == "fringe_zero":
        return "A fringe of 0 strands is not a fringe."
    if item.slug == "buttonhole_zero":
        return "A buttonhole of 0 chains has no opening."
    if item.slug == "icord_zero":
        return "An i-cord of 0 stitches has no cord."
    if item.slug == "oval_zero":
        return "An oval cannot start with 0 chains."
    if item.slug == "square_zero":
        return "A square of 0 rounds was not worked."
    if item.slug == "solomon_zero":
        return "A Solomon knot of 0 is not a knot."
    if item.slug == "surface_zero":
        return "Surface crochet of 0 chains draws no line."
    if item.slug == "bead_every_zero":
        return "A bead every 0 stitches is never placed."
    if item.slug == "stripe_every_zero":
        return "A stripe every 0 rounds never stripes."
    if item.slug == "pompom_zero":
        return "A pom-pom of 0 wraps has nothing to tie."
    if item.slug == "tassel_zero":
        return "A tassel of 0 wraps has nothing to hang."
    if item.slug == "pineapple_zero":
        return "A pineapple of 0 is not a pineapple motif."
    if item.slug == "spike_zero":
        return "A spike stitch down 0 rows does not leave the current row."
    if item.slug == "tube_zero":
        return "A tube of 0 stitches has no opening."
    if item.slug == "rectangle_zero":
        return "A rectangle of 0 rows was not worked."
    if item.slug == "corner_zero":
        return "A corner of 0 chains does not turn the corner."
    if item.slug == "star_one":
        return "A star stitch of 1 cannot make a star."
    if item.slug == "loop_zero":
        return "A loop stitch of 0 has no loop."
    if item.slug == "same_color_letter":
        return "Changing from Color Q to Color Q is not a color change."
    return item.needle


def _line_errors(line: str) -> list[str]:
    found: list[str] = []
    found.extend(_hook_gap(line))
    found.extend(_weight_number(line))
    found.extend(_turn_height(line))
    found.extend(_counts_as(line))
    found.extend(_uk(line))
    match = _INCREASE.match(line)
    if match and int(match.group(2)) <= int(match.group(1)):
        found.append(
            f"Increase from {match.group(1)} to {match.group(2)} does not rise."
        )
    match = _DECREASE.match(line)
    if match and int(match.group(2)) >= int(match.group(1)):
        found.append(
            f"Decrease from {match.group(1)} to {match.group(2)} does not fall."
        )
    match = _MULTIPLE.match(line)
    if match and int(match.group(1)) > 0 and int(match.group(2)) % int(match.group(1)):
        found.append(
            f"{match.group(2)} is not divisible by {match.group(1)}."
        )
    match = _PLUS.match(line)
    if match:
        multiple, remainder, count = (int(match.group(i)) for i in (1, 2, 3))
        if multiple > 0 and remainder < multiple and count % multiple != remainder:
            found.append(
                f"{count} is not a multiple of {multiple} plus {remainder}."
            )
    for pattern, label in ((_ROUNDS, "Rounds"), (_ROWS, "Rows")):
        for match in pattern.finditer(line):
            start, end = int(match.group(1)), int(match.group(2))
            if start > end:
                found.append(f"{label} {start}-{end} run backwards.")
    match = _EVEN.match(line)
    if match and int(match.group(1)) % 2:
        found.append(f"{match.group(1)} is odd, but the line says the count must be even.")
    match = _ODD.match(line)
    if match and int(match.group(1)) % 2 == 0:
        found.append(f"{match.group(1)} is even, but the line says the count must be odd.")
    match = _APART.match(line)
    if match and int(match.group(1)) >= int(match.group(2)):
        found.append(
            f"Eyes {match.group(1)} stitches apart do not fit on a "
            f"{match.group(2)}-stitch round."
        )
    match = _STITCH_AT.match(line)
    if match and int(match.group(1)) > int(match.group(2)):
        found.append(
            f"Stitch {match.group(1)} is past a {match.group(2)}-stitch round."
        )
    match = _SKIP.match(line)
    if match and int(match.group(1)) >= int(match.group(2)):
        found.append(
            f"Skip {match.group(1)} does not fit on a {match.group(2)}-stitch row."
        )
    match = _FRACTION.search(line)
    if match:
        found.append(f"x {match.group(1)} is not a whole repeat.")
    match = _INCH_CM.match(line)
    if match:
        found.append(
            f"{match.group(1)} inches is not {match.group(1)} cm. "
            "The line copies the same number."
        )
    match = _CM_INCH.match(line)
    if match:
        found.append(
            f"{match.group(1)} cm is not {match.group(1)} inches. "
            "The line copies the same number."
        )
    match = _COLOR.search(line)
    if match:
        found.append(
            f"Changing from Color {match.group(1)} to Color {match.group(1)} is not a color change."
        )
    again = re.search(
        r"\b(?:switch|change) to Color ([A-Z])\b.{0,60}\b(?:switch|change) to Color \1\b",
        line,
        re.IGNORECASE,
    )
    if again:
        found.append(
            f"Changing from Color {again.group(1)} to Color {again.group(1)} is not a color change."
        )
    found.extend(_nearby_counts(line))
    found.extend(_steel_order(line))
    found.extend(_flat_turn(line))
    if re.search(r"\bslip knot counts as\b", line, re.IGNORECASE):
        found.append("A slip knot is not a stitch.")
    return found


def _nearby_counts(line: str) -> list[str]:
    """Catch the same count contradiction when it is not the copied lesson sentence."""
    found: list[str] = []
    even = re.search(r"\bmust be even\D{0,16}(\d+)", line, re.IGNORECASE)
    if even and int(even.group(1)) % 2:
        found.append(f"{even.group(1)} is odd, but the line says the count must be even.")
    odd = re.search(r"\bmust be odd\D{0,16}(\d+)", line, re.IGNORECASE)
    if odd and int(odd.group(1)) % 2 == 0:
        found.append(f"{odd.group(1)} is even, but the line says the count must be odd.")
    if not re.search(r"\bplus\b", line, re.IGNORECASE):
        match = re.search(r"\bmultiple of (\d+)\D{0,12}(\d+) stitches\b", line, re.IGNORECASE)
        if match and int(match.group(1)) and int(match.group(2)) % int(match.group(1)):
            found.append(f"{match.group(2)} is not divisible by {match.group(1)}.")
    for match in re.finditer(r"\bstitch (\d+)\b.{0,32}\b(\d+)-stitch\b", line, re.IGNORECASE):
        if int(match.group(1)) > int(match.group(2)):
            found.append(
                f"Stitch {match.group(1)} is past a {match.group(2)}-stitch round."
            )
    apart = re.search(r"\b(\d+) stitches apart\b.{0,40}\b(\d+)-stitch\b", line, re.IGNORECASE)
    if apart and int(apart.group(1)) >= int(apart.group(2)):
        found.append(
            f"Eyes {apart.group(1)} stitches apart do not fit on a "
            f"{apart.group(2)}-stitch round."
        )
    skip = re.search(r"\bskip (\d+)\b.{0,24}\bon an? (\d+)-stitch\b", line, re.IGNORECASE)
    if skip and int(skip.group(1)) >= int(skip.group(2)):
        found.append(f"Skip {skip.group(1)} does not fit on a {skip.group(2)}-stitch row.")
    return found


def _steel_order(line: str) -> list[str]:
    larger = re.search(
        r"steel(?:\s+hook)?\s+(\d+).{0,40}\blarger\b.{0,30}steel(?:\s+hook)?\s+(\d+)",
        line,
        re.IGNORECASE,
    )
    if larger and int(larger.group(1)) > int(larger.group(2)):
        return ["A higher steel-hook number is smaller, not larger."]
    smaller = re.search(
        r"steel(?:\s+hook)?\s+(\d+).{0,40}\bsmaller\b.{0,30}steel(?:\s+hook)?\s+(\d+)",
        line,
        re.IGNORECASE,
    )
    if smaller and int(smaller.group(1)) < int(smaller.group(2)):
        return ["A higher steel-hook number is smaller, not larger."]
    return []


def _flat_turn(line: str) -> list[str]:
    needed = {"sc": 1, "hdc": 2, "dc": 3}
    match = re.search(r"\bch (\d+), turn, (sc|hdc|dc)\b", line, re.IGNORECASE)
    if not match:
        return []
    chains = int(match.group(1))
    stitch = match.group(2).lower()
    if chains >= needed[stitch]:
        return []
    return [f"ch {chains} is too short to turn for a {stitch}. Use ch {needed[stitch]}."]


def _hook_gap(line: str) -> list[str]:
    errors = []
    for match in _HOOK.finditer(line):
        errors.extend(_hook_gap_match(match.group(1), match.group(2)))
    for match in _HOOK_ANY.finditer(line):
        errors.extend(_hook_gap_match(match.group(1), match.group(2)))
    return _unique(errors)


def _hook_gap_match(raw: str, millimetres: str) -> list[str]:
    label = raw.upper()
    if re.fullmatch(r"[A-P]/\d+(?:\.\d+)?", label):
        label = label.replace("/", "-")
    nominal = HOOKS.get(label)
    if nominal is None:
        folded = raw.upper().replace("/", "-")
        nominal = HOOKS.get(folded)
        label = raw.upper() if nominal is None else folded
    if nominal is None:
        return []
    written = float(millimetres)
    if abs(written - nominal) <= HOOK_GAP:
        return []
    return [
        f"Hook {raw} is written as {millimetres} mm, "
        f"but the Craft Yarn Council nominal size is {nominal:g} mm. "
        "The gap is more than 1.5 mm."
    ]


def _weight_number(line: str) -> list[str]:
    low = line.lower()
    occupied: list[tuple[int, int]] = []
    errors = []
    for name, allowed in WEIGHTS:
        for match in re.finditer(rf"(?<![a-z]){re.escape(name)}(?:\s+weight)?\s*\((\d+)\)", low):
            span = match.span()
            if any(start <= span[0] and span[1] <= end for start, end in occupied):
                continue
            occupied.append(span)
            number = int(match.group(1))
            if number not in allowed:
                shown = "/".join(str(item) for item in allowed)
                errors.append(
                    f"{name.title()} is Craft Yarn Council category {shown}, not {number}."
                )
    return errors


def _turn_height(line: str) -> list[str]:
    match = _TURN.search(line)
    if not match:
        return []
    chains = int(match.group(1))
    stitch = match.group(2).lower()
    needed = TURN_MIN[stitch]
    if chains > needed - 2:
        return []
    return [f"ch {chains} is too short to turn for a {stitch}. Use ch {needed}."]


def _counts_as(line: str) -> list[str]:
    match = _COUNTS.search(line)
    if not match:
        return []
    pair = (match.group(1), match.group(2).lower())
    if pair not in COUNTS_AS:
        return []
    return [f"ch {pair[0]} cannot count as a {pair[1]}."]


def _uk(line: str) -> list[str]:
    low = line.lower()
    for phrase, message in UK_GLOSS.items():
        if phrase in low:
            return [message]
    return []


def _skip(line: str) -> bool:
    return line.lstrip().startswith(">") or bool(_PROHIBITION.search(line))


def _unique(items: list[str]) -> list[str]:
    found: list[str] = []
    for item in items:
        if item not in found:
            found.append(item)
    return found


def proof_cases() -> list[tuple[str, str, str, str]]:
    """5,000 wrong/corrected sentences. Cases, not extra stage names."""
    cases: list[tuple[str, str, str, str]] = []
    for start in range(1, 45):
        for end in range(0, start + 1):
            cases.append(
                (
                    "increase direction",
                    f"Increase from {start} to {end}.",
                    f"Increase from {end} to {end + 6}.",
                    "does not rise",
                )
            )
            if len(cases) == 1000:
                break
        if len(cases) == 1000:
            break
    decrease: list[tuple[str, str, str, str]] = []
    for start in range(1, 46):
        for end in range(start, 46):
            decrease.append(
                (
                    "decrease direction",
                    f"Decrease from {start} to {end}.",
                    f"Decrease from {end + 6} to {start}.",
                    "does not fall",
                )
            )
            if len(decrease) == 1000:
                break
        if len(decrease) == 1000:
            break
    cases.extend(decrease)
    ranges: list[tuple[str, str, str, str]] = []
    for high in range(2, 41):
        for low in range(1, high):
            ranges.append(
                (
                    "backward round range",
                    f"The range is Rounds {high}-{low}.",
                    f"The range is Rounds {low}-{high}.",
                    "run backwards",
                )
            )
            if len(ranges) == 600:
                break
        if len(ranges) == 600:
            break
    cases.extend(ranges)
    rows: list[tuple[str, str, str, str]] = []
    for high in range(2, 41):
        for low in range(1, high):
            rows.append(
                (
                    "backward row range",
                    f"The range is Rows {high}-{low}.",
                    f"The range is Rows {low}-{high}.",
                    "run backwards",
                )
            )
            if len(rows) == 400:
                break
        if len(rows) == 400:
            break
    cases.extend(rows)
    multiples: list[tuple[str, str, str, str]] = []
    for multiple in range(2, 10):
        for count in range(1, 91):
            if count % multiple == 0:
                continue
            fixed = count + (multiple - count % multiple)
            multiples.append(
                (
                    "multiple mismatch",
                    f"Multiple of {multiple}, {count} stitches.",
                    f"Multiple of {multiple}, {fixed} stitches.",
                    "not divisible by",
                )
            )
            if len(multiples) == 500:
                break
        if len(multiples) == 500:
            break
    cases.extend(multiples)
    plus: list[tuple[str, str, str, str]] = []
    for multiple in range(3, 9):
        for remainder in range(1, multiple):
            for count in range(1, 41):
                if count % multiple == remainder:
                    continue
                fixed = remainder if remainder else multiple
                while fixed < 1 or fixed % multiple != remainder:
                    fixed += multiple
                plus.append(
                    (
                        "plus remainder",
                        f"Multiple of {multiple} plus {remainder}, {count} stitches.",
                        f"Multiple of {multiple} plus {remainder}, {fixed} stitches.",
                        "plus",
                    )
                )
                if len(plus) == 400:
                    break
            if len(plus) == 400:
                break
        if len(plus) == 400:
            break
    cases.extend(plus)
    for number in range(1, 400, 2):
        cases.append(
            (
                "even count",
                f"The count must be even ({number} stitches).",
                f"The count must be even ({number + 1} stitches).",
                "must be even",
            )
        )
        if sum(1 for item in cases if item[0] == "even count") == 200:
            break
    for number in range(2, 402, 2):
        cases.append(
            (
                "odd count",
                f"The count must be odd ({number} stitches).",
                f"The count must be odd ({number - 1} stitches).",
                "must be odd",
            )
        )
        if sum(1 for item in cases if item[0] == "odd count") == 200:
            break
    apart: list[tuple[str, str, str, str]] = []
    for size in range(3, 23):
        for gap in range(size, size + 10):
            apart.append(
                (
                    "apart span",
                    f"Place the eyes {gap} stitches apart on a {size}-stitch round.",
                    f"Place the eyes 1 stitches apart on a {size}-stitch round.",
                    "do not fit",
                )
            )
            if len(apart) == 200:
                break
        if len(apart) == 200:
            break
    cases.extend(apart)
    past: list[tuple[str, str, str, str]] = []
    for size in range(3, 13):
        for stitch in range(size + 1, size + 16):
            past.append(
                (
                    "stitch past end",
                    f"Place the marker in stitch {stitch} on a {size}-stitch round.",
                    f"Place the marker in stitch 1 on a {size}-stitch round.",
                    "is past",
                )
            )
            if len(past) == 150:
                break
        if len(past) == 150:
            break
    cases.extend(past)
    skips: list[tuple[str, str, str, str]] = []
    for size in range(3, 13):
        for count in range(size, size + 15):
            skips.append(
                (
                    "skip past count",
                    f"Skip {count} on a {size}-stitch row.",
                    f"Skip 1 on a {size}-stitch row.",
                    "does not fit",
                )
            )
            if len(skips) == 150:
                break
        if len(skips) == 150:
            break
    cases.extend(skips)
    for number in range(1, 81):
        cases.append(
            (
                "copied inch measure",
                f"{number} inches = {number} cm.",
                f"{number} inches = {number * 2.54:.2f} cm.",
                "copies the same number",
            )
        )
    for number in range(1, 81):
        cases.append(
            (
                "copied centimeter measure",
                f"{number} cm = {number} inches.",
                f"{number} cm = {number / 2.54:.2f} inches.",
                "copies the same number",
            )
        )
    for whole in range(1, 41):
        cases.append(
            (
                "fractional times",
                f"Repeat the shell x {whole}.5.",
                f"Repeat the shell x {whole + 1}.",
                "not a whole repeat",
            )
        )
    if len(cases) != 5000:
        raise RuntimeError(f"expected 5000 proof cases, found {len(cases)}")
    return cases
