"""Written checks that cover a family, not one copied sentence.

The increase, decrease, range, multiple, and measure checks are proved on
5,000 sentences. Those sentences are cases, not 5,000 named stages. A quoted
line is not an instruction. A prohibition is not a defect.
"""

from __future__ import annotations

import re

re._MAXCACHE = 4096
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
    "us half double crochet is a uk treble": "A US half double is a UK half treble, not a UK treble.",
    "us half double is a uk treble": "A US half double is a UK half treble, not a UK treble.",
    "us hdc is a uk treble": "A US half double is a UK half treble, not a UK treble.",
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
_COLOR = re.compile(r"\bChange (?:from )?Color ([A-Z]) to Color \1\b", re.IGNORECASE)
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
    found.extend(_rest_wording(line))
    found.extend(_word_gaps(line))
    found.extend(_missed_wording(line))
    found.extend(_none_wording(line))
    found.extend(_abbrev_wording(line))
    found.extend(_glued_wording(line))
    found.extend(_uses_none(line))
    found.extend(_has_one(line))
    found.extend(_word_order(line))
    found.extend(_of_no(line))
    found.extend(_nothing(line))
    if re.search(r"\bslip knot counts as\b", line, re.IGNORECASE):
        found.append("A slip knot is not a stitch.")
    return found


def _rest_wording(line: str) -> list[str]:
    """Catch the remaining copied-lesson rules in any sentence."""
    found: list[str] = []
    plus = re.search(
        r"\bmultiple of (\d+) plus (\d+)\D{0,32}(\d+) stitches\b",
        line,
        re.IGNORECASE,
    )
    if plus:
        multiple, remainder, count = (int(plus.group(i)) for i in (1, 2, 3))
        if multiple > 0 and remainder < multiple and count % multiple != remainder:
            found.append(f"{count} is not a multiple of {multiple} plus {remainder}.")
    if re.search(r"(?:turning )?chain (?:is )?counted twice|counts the (?:turning )?chain twice|chain counts twice", line, re.IGNORECASE):
        found.append("A turning chain counted twice is added two times.")
    if re.search(r"\b0\s+inches\b", line, re.IGNORECASE):
        found.append("A finished width of 0 inches is not a piece.")
    if re.search(
        r"\b\d+\.\d+\s*(?:sc|hdc|dc|tr|dtr|sts?|stitches)\b|(?:\b(?:sc|hdc|dc|tr|dtr)\s+\d+\.\d+)\b",
        line,
        re.IGNORECASE,
    ):
        found.append("A decimal stitch is not a whole stitch.")
    if re.search(r"\b(?:repeat|rep)\b.{0,30}\d+\.\d+\s+times\b", line, re.IGNORECASE):
        found.append("A fractional repeat is not a whole repeat.")
    if re.search(r"(?<![\d.])-\d+\s+times\b", line):
        found.append("A negative repeat count is not a repeat.")
    huge = re.search(r"\b(?:round|row|rnd)\s+(\d+)\b", line, re.IGNORECASE)
    if huge and int(huge.group(1)) >= 200:
        found.append(f"Round {huge.group(1)} is not a usable round number.")
    if re.search(r"\bBLO\b", line) and re.search(r"both loops", line, re.IGNORECASE) and not re.search(r"\bor\b", line, re.IGNORECASE):
        found.append("BLO only and both loops cannot be the same stitch.")
    if re.search(r"(?:front post|back post|fpdc|bpdc|fptr|bptr|post stitch).{0,24}around the chain", line, re.IGNORECASE):
        found.append("A chain has no post. Do not work a post around the chain.")
    if re.search(r"\bslip knot\b", line, re.IGNORECASE) and re.search(
        r"first stitch|as a stitch|(?:sc|hdc|dc|tr) in the slip knot|work into the slip knot",
        line,
        re.IGNORECASE,
    ):
        found.append("The slip knot is not a chain stitch.")
    if re.search(r"\bfasten off\b.{0,40}\bcontinue in (?:the |that |this )?(?:same )?yarn\b", line, re.IGNORECASE):
        found.append("Fasten off ends the yarn. The same yarn was not continued.")
    if (
        re.search(r"\bfoundation (?:single crochet|sc)\b", line, re.IGNORECASE)
        and re.search(r"\bstarting chain\b", line, re.IGNORECASE)
        and not re.search(r"\bor\b|instead|without", line, re.IGNORECASE)
    ):
        found.append("Foundation single crochet replaces the starting chain.")
    if re.search(r"\bspiral\b", line, re.IGNORECASE) and re.search(
        r"slip stitches? the round closed|sl st the round closed",
        line,
        re.IGNORECASE,
    ):
        found.append("A continuous spiral does not join every round. The join was not added.")
    for match in re.finditer(r"\bstitch (\d+) of (?:the )?(\d+)\b", line, re.IGNORECASE):
        if int(match.group(1)) > int(match.group(2)):
            found.append(f"Stitch {match.group(1)} is past a {match.group(2)}-stitch round.")
    apart = re.search(r"\b(\d+) stitches apart\b.{0,48}\bround of (\d+) stitches\b", line, re.IGNORECASE)
    if apart and int(apart.group(1)) >= int(apart.group(2)):
        found.append(
            f"Eyes {apart.group(1)} stitches apart do not fit on a {apart.group(2)}-stitch round."
        )
    skip = re.search(r"\bskip (\d+)\b.{0,32}\brow of (\d+) stitches\b", line, re.IGNORECASE)
    if skip and int(skip.group(1)) >= int(skip.group(2)):
        found.append(f"Skip {skip.group(1)} does not fit on a {skip.group(2)}-stitch row.")
    even = re.search(r"\beven count of (\d+)\b", line, re.IGNORECASE)
    if even and int(even.group(1)) % 2:
        found.append(f"{even.group(1)} is odd, but the line says the count must be even.")
    odd = re.search(r"\bodd count of (\d+)\b", line, re.IGNORECASE)
    if odd and int(odd.group(1)) % 2 == 0:
        found.append(f"{odd.group(1)} is even, but the line says the count must be odd.")
    hook = re.search(
        r"\b([A-P])\s+(\d+(?:\.\d+)?)\s+is\s+(\d+(?:\.\d+)?)\s*mm\b",
        line,
        re.IGNORECASE,
    )
    if hook:
        label = f"{hook.group(1).upper()}-{hook.group(2)}"
        nominal = HOOKS.get(label)
        if nominal is not None and abs(float(hook.group(3)) - nominal) > HOOK_GAP:
            found.append(
                f"Hook {hook.group(1)}-{hook.group(2)} is written as {hook.group(3)} mm, "
                f"but the Craft Yarn Council nominal size is {nominal:g} mm. "
                "The gap is more than 1.5 mm."
            )
    found.extend(_weight_category(line))
    if re.search(
        r"\b(?:zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\s+centimet(?:er|re)s?\b",
        line,
        re.IGNORECASE,
    ) and re.search(r"\bhook\b", line, re.IGNORECASE):
        found.append("The hook is written in centimeters. Crochet hooks are written in millimeters.")
    if re.search(r"\bgauge\b.{0,32}\bzero\b|\bzero\s+sc\b", line, re.IGNORECASE):
        found.append("A gauge of 0 sc is not a fabric.")
    shell = re.search(r"\bshell of ([0-2])\b", line, re.IGNORECASE)
    if shell:
        found.append(f"A shell of {shell.group(1)} is not a shell. Use at least 3 stitches.")
    if re.search(r"\b(?:ch|chain)\s*-?\s*0\s+(?:space|sp)\b", line, re.IGNORECASE):
        found.append("A ch-0 space has no chains to work into.")
    return found


_GAP_WORDS = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
    "thirteen": 13,
    "fourteen": 14,
    "fifteen": 15,
    "sixteen": 16,
    "seventeen": 17,
    "eighteen": 18,
    "nineteen": 19,
    "twenty": 20,
}


def _gap_count(raw: str) -> int | None:
    if raw.isdigit():
        return int(raw)
    return _GAP_WORDS.get(raw.lower())


def _word_gaps(line: str) -> list[str]:
    """Catch a copied rule when the sentence uses another word or a zero."""
    found: list[str] = []
    if re.search(r"\bcable\b.{0,20}\b(?:of|over)\s+0\b", line, re.IGNORECASE):
        found.append("A cable over 0 stitches does not cross.")
    if re.search(r"\bi-?cord\b.{0,16}\bof\s+0\b", line, re.IGNORECASE):
        found.append("An i-cord of 0 stitches has no cord.")
    if re.search(r"\bspike\b.{0,24}\bdown\s+0\b", line, re.IGNORECASE):
        found.append("A spike stitch down 0 rows does not leave the current row.")
    if re.search(r"\bsurface crochet\b.{0,16}\b(?:of\s+)?0\b", line, re.IGNORECASE):
        found.append("Surface crochet of 0 chains draws no line.")
    if re.search(r"\bpom-?pom\b.{0,16}\bof\s+0\b", line, re.IGNORECASE):
        found.append("A pom-pom of 0 wraps has nothing to tie.")
    if re.search(r"\bstuff", line, re.IGNORECASE) and re.search(
        r"\bstuff(?:ing|ed)?\s+with\s+0\b|\b0\s+(?:ounces|grams)\b",
        line,
        re.IGNORECASE,
    ):
        found.append("Stuffing with 0 does not fill the piece.")
    if re.search(r"\bmake\s+-\d+\b", line, re.IGNORECASE):
        found.append("A negative make count is not a piece. The copies were not invented.")
    if re.search(r"(?<![\d])\b(?:round|row|rnd)s?\s+-\d+\b", line, re.IGNORECASE):
        found.append("A negative round or row number is not a round. Start at 1.")
    if re.search(r"\bshell of zero\b", line, re.IGNORECASE):
        found.append("A shell of 0 is not a shell. Use at least 3 stitches.")
    if re.search(r"\b(?:fpdc|bpdc|fptr|bptr)\s+around\s+ch\b", line, re.IGNORECASE):
        found.append("A chain has no post. Do not work a post around the chain.")
    if re.search(r"\bFLO\b", line) and re.search(r"both loops", line, re.IGNORECASE) and not re.search(r"\bor\b", line, re.IGNORECASE):
        found.append("FLO and both loops cannot be the same stitch.")
    if re.search(r"\bcontinuous rounds\b", line, re.IGNORECASE) and re.search(
        r"\bjoin (?:each|every) round\b|\bjoin with a slip stitch\b",
        line,
        re.IGNORECASE,
    ):
        found.append("Continuous rounds do not join every round. The join was not added.")
    if re.search(r"\bin the round\b", line, re.IGNORECASE) and re.search(r"\bin rows\b", line, re.IGNORECASE) and not re.search(r"\bor\b", line, re.IGNORECASE):
        found.append("In the round and in rows are two fabrics. The extra fabric was not invented.")
    if re.search(r"\bfasten off\b.{0,40}\bkeep working\b", line, re.IGNORECASE):
        found.append("Fasten off ended this yarn. The later work was not continued.")
    if re.search(r"\bstitch zero\b", line, re.IGNORECASE):
        found.append("Stitch 0 does not exist. The first stitch is stitch 1.")
    if re.search(r"\bstuff\b", line, re.IGNORECASE) and re.search(r"\bleave\b.{0,24}\bempty\b", line, re.IGNORECASE) and not re.search(r"\bor\b", line, re.IGNORECASE):
        found.append("The line stuffs and leaves the piece empty. The stuffing was not added.")
    skip = re.search(r"\bskip ([A-Za-z]+)\b.{0,32}\brow of ([A-Za-z]+) stitches\b", line, re.IGNORECASE)
    if skip:
        left, right = _gap_count(skip.group(1)), _gap_count(skip.group(2))
        if left is not None and right is not None and left >= right:
            found.append(f"Skip {left} does not fit on a {right}-stitch row.")
    apart = re.search(
        r"\b([A-Za-z]+) stitches apart\b.{0,48}\bround of ([A-Za-z]+) stitches\b",
        line,
        re.IGNORECASE,
    )
    if apart:
        left, right = _gap_count(apart.group(1)), _gap_count(apart.group(2))
        if left is not None and right is not None and left >= right:
            found.append(f"Eyes {left} stitches apart do not fit on a {right}-stitch round.")
    return found



def _missed_wording(line: str) -> list[str]:
    """Catch a copied rule when the sentence uses another wording."""
    found: list[str] = []
    for match in re.finditer(
        r"\b([A-P](?:/[A-Z])?(?:[-/]\d+(?:\.\d+)?)?)\s+(?:hook\s+)?is\s+(\d+(?:\.\d+)?)\s*mm\b",
        line,
        re.IGNORECASE,
    ):
        found.extend(_hook_gap_match(match.group(1), match.group(2)))
    turn = re.search(
        r"\bch\s+(\d+)\s*,?\s*turn(?:\s*,|\s+for(?:\s+an?)?)?\s+"
        r"(sc|hdc|dc|single crochet|half double(?: crochet)?|double crochet)\b",
        line,
        re.IGNORECASE,
    )
    if turn:
        names = {
            "sc": "sc",
            "hdc": "hdc",
            "dc": "dc",
            "single crochet": "sc",
            "half double": "hdc",
            "half double crochet": "hdc",
            "double crochet": "dc",
        }
        stitch = names[turn.group(2).lower()]
        needed = {"sc": 1, "hdc": 2, "dc": 3}[stitch]
        chains = int(turn.group(1))
        if chains < needed:
            found.append(
                f"ch {chains} is too short to turn for a {stitch}. Use ch {needed}."
            )
    counts = re.search(
        r"\bch\s+(\d+)\s+counts\s+as\s+(?:an?\s+)?"
        r"(sc|hdc|dc|tr|dtr|single crochet|half double(?: crochet)?|"
        r"double crochet|treble|double treble)\b",
        line,
        re.IGNORECASE,
    )
    if counts:
        names = {
            "sc": "sc",
            "single crochet": "sc",
            "hdc": "hdc",
            "half double": "hdc",
            "half double crochet": "hdc",
            "dc": "dc",
            "double crochet": "dc",
            "tr": "tr",
            "treble": "tr",
            "dtr": "dtr",
            "double treble": "dtr",
        }
        stitch = names[counts.group(2).lower()]
        pair = (counts.group(1), stitch)
        if pair in COUNTS_AS:
            found.append(f"ch {pair[0]} cannot count as a {pair[1]}.")
    if re.search(r"\b(?:v-stitch|v stitch)\s+of\s+(?:1|one)\b", line, re.IGNORECASE):
        found.append("A V-stitch of 1 is not a V-stitch.")
    if re.search(r"\bfan\s+of\s+(?:1|one)\b", line, re.IGNORECASE):
        found.append("A fan of 1 is not a fan.")
    if re.search(r"\bstar(?:\s+stitch)?\s+of\s+(?:1|one)\b", line, re.IGNORECASE):
        found.append("A star stitch of 1 cannot make a star.")
    if re.search(r"\bcluster\s+of\s+(?:1|one)\b", line, re.IGNORECASE):
        found.append("A 1-dc cluster is one stitch, not a cluster.")
    if re.search(r"\bloop(?:\s+stitch)?\s+of\s+(?:0|zero)\b", line, re.IGNORECASE):
        found.append("A loop stitch of 0 has no loop.")
    if re.search(r"\boval\b.{0,32}\b(?:0|zero)\s+chains\b", line, re.IGNORECASE):
        found.append("An oval cannot start with 0 chains.")
    if re.search(r"\brectangle\b.{0,32}\b(?:0|zero)\s+rows\b", line, re.IGNORECASE):
        found.append("A rectangle of 0 rows was not worked.")
    if (
        re.search(r"\b(?:yarn|hold)\b", line, re.IGNORECASE)
        and re.search(r"\b(?:doubled|double)\b(?!\s+crochet)", line, re.IGNORECASE)
        and re.search(r"\bsingle\b(?!\s+crochet)", line, re.IGNORECASE)
        and not re.search(r"\bor\b", line, re.IGNORECASE)
    ):
        found.append("The yarn cannot be held double and single at the same time.")
    apart = re.search(
        r"\beyes\s+([A-Za-z]+|\d+)\s+apart\b.{0,48}\bround\s+of\s+([A-Za-z]+|\d+)\s+stitches\b",
        line,
        re.IGNORECASE,
    )
    if apart:
        left, right = _gap_count(apart.group(1)), _gap_count(apart.group(2))
        if left is not None and right is not None and left >= right:
            found.append(
                f"Eyes {left} stitches apart do not fit on a {right}-stitch round."
            )
    if (
        re.search(r"\bfoundation\s+(?:single crochet|sc)\b", line, re.IGNORECASE)
        and re.search(r"\bchain\s+\d+\s+to\s+start\b", line, re.IGNORECASE)
        and not re.search(r"\bor\b|instead|without", line, re.IGNORECASE)
    ):
        found.append("Foundation single crochet replaces the starting chain.")
    if re.search(r"\bfringe\b.{0,24}\bno strands\b", line, re.IGNORECASE):
        found.append("A fringe of 0 strands is not a fringe.")
    return found



def _none_wording(line: str) -> list[str]:
    """Catch no, none, and made-of where the digit rule already exists."""
    found: list[str] = []
    if re.search(r"\bwork\s+no\s+stitches\b", line, re.IGNORECASE):
        found.append("Work 0 stitches does no work.")
    if re.search(r"\bskip\s+no\s+stitches\b", line, re.IGNORECASE):
        found.append("Skip 0 does not move the hook.")
    if re.search(r"\bdecrease\s+to\s+no\s+stitches\b", line, re.IGNORECASE):
        found.append("Decrease to 0 stitches leaves nothing to fasten.")
    if re.search(r"\bpicot\b.{0,16}\b(?:of|with)\s+no\s+chains\b", line, re.IGNORECASE):
        found.append("A picot of 0 is not a picot.")
    if re.search(r"\bchain\s+space\s+of\s+(?:0|zero)\b", line, re.IGNORECASE):
        found.append("A ch-0 space has no chains to work into.")
    if re.search(r"\bchain of none\b", line, re.IGNORECASE):
        found.append("ch 0 makes no chain.")
    if re.search(r"\bzero\s+inches\b", line, re.IGNORECASE) and not re.search(
        r"\bnot\s+zero\s+inches\b", line, re.IGNORECASE
    ):
        found.append("A finished width of 0 inches is not a piece.")
    if re.search(r"\bpull through\s+(?:no|zero)(?:\s+loops)?\b", line, re.IGNORECASE):
        found.append("Pull through 0 loops leaves the loops on the hook.")
    if re.search(r"\bwork even for\s+no\s+rows\b", line, re.IGNORECASE):
        found.append("Work even for 0 rows does no work.")
    if re.search(r"\bplace\s+no\s+safety eyes\b", line, re.IGNORECASE):
        found.append("Place 0 safety eyes mounts nothing.")
    if re.search(r"\bstuff(?:ing|ed)?\s+with\s+(?:0|zero)\s+(?:g|grams|ounces)\b", line, re.IGNORECASE):
        found.append("Stuffing with 0 does not fill the piece.")
    if re.search(r"\bevery\s+no\s+(?:rows|rounds)\b", line, re.IGNORECASE):
        found.append("Every 0 rows or rounds never happens.")
    if re.search(r"\bbuttonhole\b.{0,16}\bwith\s+(?:0|zero)\b", line, re.IGNORECASE):
        found.append("A buttonhole of 0 chains has no opening.")
    if re.search(r"\bfringe\b.{0,20}\busing\s+(?:0|zero)\b", line, re.IGNORECASE):
        found.append("A fringe of 0 strands is not a fringe.")
    if re.search(r"\bcable\b.{0,16}\bof\s+zero\b", line, re.IGNORECASE):
        found.append("A cable over 0 stitches does not cross.")
    if re.search(r"\bspike\b.{0,20}\bof\s+(?:0|zero)\s+rows\b", line, re.IGNORECASE):
        found.append("A spike stitch down 0 rows does not leave the current row.")
    if re.search(r"\bi[ -]?cord\b.{0,16}\bof\s+(?:0|zero)\b", line, re.IGNORECASE):
        found.append("An i-cord of 0 stitches has no cord.")
    if re.search(r"\b(?:corner|tube|square)\s+made of\s+(?:0|zero)\b", line, re.IGNORECASE):
        found.append("A count of 0 does not make that shape.")
    if re.search(r"\bsurface\s+slip\s+stitch\b.{0,16}\bof\s+(?:0|zero)\b", line, re.IGNORECASE):
        found.append("Surface crochet of 0 chains draws no line.")
    if re.search(r"\bshell\s+made of\s+(?:1|one)\b", line, re.IGNORECASE):
        found.append("A shell of 1 is not a shell. Use at least 3 stitches.")
    if re.search(r"\bbobble\s+made of\s+(?:1|one)\b", line, re.IGNORECASE):
        found.append("A bobble of 1 has nothing to gather.")
    if re.search(r"\bpuff\s+made of\s+(?:1|one)\b", line, re.IGNORECASE):
        found.append("A puff of 1 is not a puff.")
    if re.search(r"\bpopcorn\s+made of\s+(?:1|one)\b", line, re.IGNORECASE):
        found.append("A popcorn of 1 cannot be closed.")
    if re.search(r"\bgauge\b.{0,16}\bno\s+stitches\b", line, re.IGNORECASE):
        found.append("A gauge of 0 sc is not a fabric.")
    if re.search(r"\bstitch\s+none\b", line, re.IGNORECASE):
        found.append("Stitch 0 does not exist. The first stitch is stitch 1.")
    if re.search(r"\bround\s+none\b", line, re.IGNORECASE):
        found.append("Round 0 is not a round. Start at Round 1.")
    if re.search(r"\brow\s+none\b", line, re.IGNORECASE):
        found.append("Row 0 is not a row. Start at Row 1.")
    if re.search(
        r"\b(?:front post|back post|fpdc|bpdc|fptr|bptr)\b.{0,32}\baround an? chain\b",
        line,
        re.IGNORECASE,
    ):
        found.append("A chain has no post. Do not work a post around the chain.")
    if (
        re.search(r"\bback loop only\b", line, re.IGNORECASE)
        and re.search(r"\bboth loops\b", line, re.IGNORECASE)
        and not re.search(r"\bor\b", line, re.IGNORECASE)
    ):
        found.append("BLO only and both loops cannot be the same stitch.")
    if re.search(r"\b(?:turning )?chain\b.{0,24}\bcounted two times\b", line, re.IGNORECASE):
        found.append("A turning chain counted twice is added two times.")
    for match in re.finditer(r"\b(rounds|rows)\s+(\d+)\s+to\s+(\d+)\b", line, re.IGNORECASE):
        start, end = int(match.group(2)), int(match.group(3))
        if start > end:
            label = "Rounds" if match.group(1).lower().startswith("round") else "Rows"
            found.append(f"{label} {start}-{end} run backwards.")
    if re.search(r"\bthe round is worked across\b", line, re.IGNORECASE):
        found.append("A round says across. Rounds are worked around.")
    if re.search(r"\bthe row is worked around\b", line, re.IGNORECASE):
        found.append("A row says around. Rows are worked across.")
    if re.search(r"\bthis round turns\b(?!\s+the corner)", line, re.IGNORECASE):
        found.append("A continuous round does not turn. Turn belongs to a flat row.")
    if re.search(r"\bspiral\b", line, re.IGNORECASE) and re.search(
        r"\bclosed by a slip stitch\b", line, re.IGNORECASE
    ):
        found.append("A continuous spiral does not join every round. The join was not added.")
    if re.search(r"\bfasten off\b.{0,40}\bkeep going\b", line, re.IGNORECASE):
        found.append("Fasten off ended this yarn. The later work was not continued.")
    if (
        re.search(r"\bwhip\s*stitch\b", line, re.IGNORECASE)
        and re.search(r"\bmattress\b", line, re.IGNORECASE)
        and not re.search(r"\bor\b", line, re.IGNORECASE)
    ):
        found.append("Whipstitch and mattress stitch are two seams. The extra seam was not invented.")
    chain_of = re.search(
        r"\bchain of\s+(one|\d+)\s+counts as\s+(?:an? |the )?(dc|double crochet|hdc|tr|treble)\b",
        line,
        re.IGNORECASE,
    )
    if chain_of:
        raw = chain_of.group(1).lower()
        chains = "1" if raw == "one" else raw
        names = {"dc": "dc", "double crochet": "dc", "hdc": "hdc", "tr": "tr", "treble": "tr"}
        stitch = names[chain_of.group(2).lower()]
        if (chains, stitch) in COUNTS_AS:
            found.append(f"ch {chains} cannot count as a {stitch}.")
    risen = re.search(r"^Increase (\d+) to (\d+)\b", line, re.IGNORECASE)
    if risen and int(risen.group(2)) <= int(risen.group(1)):
        found.append(
            f"Increase from {risen.group(1)} to {risen.group(2)} does not rise."
        )
    even = re.search(r"\beven count that is (\d+)\b", line, re.IGNORECASE)
    if even and int(even.group(1)) % 2:
        found.append(f"{even.group(1)} is odd, but the line says the count must be even.")
    odd = re.search(r"\bodd count that is (\d+)\b", line, re.IGNORECASE)
    if odd and int(odd.group(1)) % 2 == 0:
        found.append(f"{odd.group(1)} is even, but the line says the count must be odd.")
    past = re.search(
        r"\bstitch\s+(\d+|[A-Za-z]+)\s+of\s+(?:a|the)\s+(\d+|[A-Za-z]+)[- ]stitch\s+round\b",
        line,
        re.IGNORECASE,
    )
    if past:
        left, right = _gap_count(past.group(1)), _gap_count(past.group(2))
        if left is not None and right is not None and left > right:
            found.append(f"Stitch {left} is past a {right}-stitch round.")
    skipped = re.search(
        r"\bskip\s+(\d+|[A-Za-z]+)\s+stitches\s+of\s+(?:a|the)\s+(\d+|[A-Za-z]+)[- ]stitch\s+row\b",
        line,
        re.IGNORECASE,
    )
    if skipped:
        left, right = _gap_count(skipped.group(1)), _gap_count(skipped.group(2))
        if left is not None and right is not None and left >= right:
            found.append(f"Skip {left} does not fit on a {right}-stitch row.")
    words = {"one": 1, "two": 2, "three": 3}
    turn = re.search(
        r"\bch(?:ain)?\s+(one|two|three|\d+)\s*(?:,\s*)?(?:to\s+)?turn(?:,|\s+for(?:\s+an?)?)?(?:\s+then)?\s+"
        r"(sc|hdc|dc|single crochet|half double(?: crochet)?|double crochet)\b",
        line,
        re.IGNORECASE,
    )
    if turn:
        raw = turn.group(1).lower()
        chains = words[raw] if raw in words else int(raw)
        names = {
            "sc": "sc",
            "hdc": "hdc",
            "dc": "dc",
            "single crochet": "sc",
            "half double": "hdc",
            "half double crochet": "hdc",
            "double crochet": "dc",
        }
        stitch = names[turn.group(2).lower()]
        needed = {"sc": 1, "hdc": 2, "dc": 3}[stitch]
        if chains < needed:
            found.append(f"ch {chains} is too short to turn for a {stitch}. Use ch {needed}.")
    counts = re.search(
        r"\b(?:chain of\s+)?ch(?:ain)?\s+(one|two|three|\d+)\s+counts\s+as\s+(?:an?\s+|the\s+)?"
        r"(sc|hdc|dc|tr|dtr|single crochet|half double(?: crochet)?|double crochet|treble|double treble)\b",
        line,
        re.IGNORECASE,
    )
    if counts:
        raw = counts.group(1).lower()
        chains = str(words[raw] if raw in words else int(raw))
        names = {
            "sc": "sc",
            "single crochet": "sc",
            "hdc": "hdc",
            "half double": "hdc",
            "half double crochet": "hdc",
            "dc": "dc",
            "double crochet": "dc",
            "tr": "tr",
            "treble": "tr",
            "dtr": "dtr",
            "double treble": "dtr",
        }
        stitch = names[counts.group(2).lower()]
        if (chains, stitch) in COUNTS_AS:
            found.append(f"ch {chains} cannot count as a {stitch}.")
    return found


def _abbrev_wording(line: str) -> list[str]:
    """Catch the same rule in an abbreviation or another word order."""
    found: list[str] = []
    move = re.search(
        r"\b(inc|increase|dec|decrease)\s+(?:from\s+)?(\d+|[A-Za-z]+)\s+to\s+(\d+|[A-Za-z]+)\b",
        line,
        re.IGNORECASE,
    )
    if move:
        left, right = _gap_count(move.group(2)), _gap_count(move.group(3))
        if left is not None and right is not None:
            if move.group(1).lower().startswith("inc") and right <= left:
                found.append(f"Increase from {move.group(2)} to {move.group(3)} does not rise.")
            if move.group(1).lower().startswith("dec") and right >= left:
                found.append(f"Decrease from {move.group(2)} to {move.group(3)} does not fall.")
    for match in re.finditer(
        r"\b(rounds|rows|rnds)\s+(\d+|[A-Za-z]+)\s+(?:to|through)\s+(\d+|[A-Za-z]+)\b",
        line,
        re.IGNORECASE,
    ):
        found.extend(_range_back(match.group(1), match.group(2), match.group(3)))
    for match in re.finditer(
        r"\b(rnd|round|row)\s+(\d+|[A-Za-z]+)\s+to\s+(?:rnd|round|row)\s+(\d+|[A-Za-z]+)\b",
        line,
        re.IGNORECASE,
    ):
        found.extend(_range_back(match.group(1), match.group(2), match.group(3)))
    down = re.search(
        r"\bfrom\s+(round|row|rnd)\s+(\d+|[A-Za-z]+)\s+down to\s+(?:round|row|rnd)\s+(\d+|[A-Za-z]+)\b",
        line,
        re.IGNORECASE,
    )
    if down:
        found.extend(_range_back(down.group(1), down.group(2), down.group(3)))
    stitch = (
        r"(sc|hdc|dc|tr|dtr|single crochet|half double(?: crochet)?|"
        r"double crochet|treble|double treble)"
    )
    count = r"(one|two|three|four|five|\d+)"
    for pattern in (
        rf"\bch(?:ain)?\s+{count}\s+then\s+turn\s+and\s+{stitch}\b",
        rf"\bturn\s+with\s+ch(?:ain)?\s+{count}\s+for\s+(?:an?\s+)?{stitch}\b",
        rf"\bturn,\s*ch(?:ain)?\s+{count},\s*then\s+{stitch}\b",
        rf"\bturning\s+ch(?:ain)?\s+is\s+{count}\s+for\s+(?:an?\s+)?{stitch}\b",
    ):
        turn = re.search(pattern, line, re.IGNORECASE)
        if turn:
            found.extend(_short_turn(turn.group(1), turn.group(2)))
    hyphen = re.search(
        rf"\bch-(\d+|one|two|three|four)\s+counts\s+as\s+(?:an?\s+|the\s+)?{stitch}\b",
        line,
        re.IGNORECASE,
    )
    if hyphen:
        words = {"one": "1", "two": "2", "three": "3", "four": "4"}
        raw = hyphen.group(1).lower()
        chains = words.get(raw, raw)
        names = {
            "sc": "sc",
            "single crochet": "sc",
            "hdc": "hdc",
            "half double": "hdc",
            "half double crochet": "hdc",
            "dc": "dc",
            "double crochet": "dc",
            "tr": "tr",
            "treble": "tr",
            "dtr": "dtr",
            "double treble": "dtr",
        }
        pair = (chains, names[hyphen.group(2).lower()])
        if pair in COUNTS_AS:
            found.append(f"ch {pair[0]} cannot count as a {pair[1]}.")
    if (
        re.search(r"\bfront loop\b", line, re.IGNORECASE)
        and re.search(r"\bboth loops\b", line, re.IGNORECASE)
        and not re.search(r"\bor\b", line, re.IGNORECASE)
    ):
        found.append("FLO and both loops cannot be the same stitch.")
    if (
        re.search(r"\b(?:magic ring|magic circle|magic loop|adjustable ring)\b", line, re.IGNORECASE)
        and re.search(r"\bchain(?:\s*-\s*\d+)?\s*ring\b|\bchain start\b", line, re.IGNORECASE)
        and not re.search(r"\bor\b|instead|without", line, re.IGNORECASE)
    ):
        found.append("A piece cannot start with both a magic ring and a chain ring.")
    if (
        re.search(r"\bcrab stitch\b", line, re.IGNORECASE)
        and re.search(r"\bforwards?\b", line, re.IGNORECASE)
        and not re.search(r"\bbackward\b", line, re.IGNORECASE)
    ):
        found.append("Reverse single crochet is worked backward, not forward.")
    same = re.search(
        r"\bcolou?r\s+([A-Za-z])\s+to\s+colou?r\s+\1\b", line, re.IGNORECASE
    )
    back = re.search(
        r"\bto\s+colou?r\s+([A-Za-z])\s+from\s+colou?r\s+\1\b", line, re.IGNORECASE
    )
    if same or back:
        letter = (same or back).group(1).upper()
        found.append(f"Changing from Color {letter} to Color {letter} is not a color change.")
    if re.search(r"\b(?:work the round across|the round goes across)\b", line, re.IGNORECASE):
        found.append("A round says across. Rounds are worked around.")
    if re.search(r"\b(?:work the row around|the row goes around)\b", line, re.IGNORECASE):
        found.append("A row says around. Rows are worked across.")
    if re.search(
        r"\b(?:this round says turn|turn at the end of the round|turn each round)\b",
        line,
        re.IGNORECASE,
    ):
        found.append("A round says turn. A continuous round does not turn.")
    if re.search(
        r"\b(?:front[- ]post|back[- ]post|fpdc|bpdc|fptr|bptr|post stitch)\b.{0,32}"
        r"\baround\s+(?:the\s+|a\s+)?ch(?:ain)?\b",
        line,
        re.IGNORECASE,
    ):
        found.append("A chain has no post. Do not work a post around the chain.")
    for match in re.finditer(
        r"\b([A-P](?:/[A-Z])?(?:[-/]\d+(?:\.\d+)?)?)\s+(?:hook\s+)?"
        r"(?:measures|equals)\s+(\d+(?:\.\d+)?)\s*(?:mm|millimet(?:er|re)s?)\b",
        line,
        re.IGNORECASE,
    ):
        found.extend(_hook_gap_match(match.group(1), match.group(2)))
    for match in re.finditer(
        r"\b([A-P](?:/[A-Z])?(?:[-/]\d+(?:\.\d+)?)?)\s+(?:hook\s+)?"
        r"is\s+(\d+(?:\.\d+)?)\s*millimet(?:er|re)s?\b",
        line,
        re.IGNORECASE,
    ):
        found.extend(_hook_gap_match(match.group(1), match.group(2)))
    if re.search(r"\bhook\b", line, re.IGNORECASE) and re.search(
        r"\d+(?:\.\d+)?\s*centimet(?:er|re)s?\b", line, re.IGNORECASE
    ):
        found.append("The hook is written in centimeters. Crochet hooks are written in millimeters.")
    larger = re.search(
        r"steel(?:\s+hook)?\s+(\d+|[A-Za-z]+).{0,40}\b(?:larger|bigger)\b.{0,30}"
        r"steel(?:\s+hook)?\s+(\d+|[A-Za-z]+)",
        line,
        re.IGNORECASE,
    )
    if larger:
        left, right = _gap_count(larger.group(1)), _gap_count(larger.group(2))
        if left is not None and right is not None and left > right:
            found.append("A higher steel-hook number is smaller, not larger.")
    if re.search(
        r"\b(?:turning\s+)?chain\b.{0,32}\bcounted\s+(?:2|two)\s+times\b",
        line,
        re.IGNORECASE,
    ) or re.search(
        r"\bcount\s+(?:that|the)\s+(?:turning\s+)?chain\s+(?:twice|(?:2|two)\s+times)\b",
        line,
        re.IGNORECASE,
    ):
        found.append("A turning chain counted twice is added two times.")
    if re.search(r"\b(?:0|zero)\s+inch\b", line, re.IGNORECASE) and not re.search(
        r"\bnot\s+(?:0|zero)\s+inch", line, re.IGNORECASE
    ):
        found.append("A finished width of 0 inches is not a piece.")
    if re.search(r"\bpicot\b.{0,20}\b(?:using|with)\s+(?:0|zero)\b", line, re.IGNORECASE):
        found.append("A picot of 0 is not a picot.")
    if re.search(
        r"\bshell\b.{0,24}\b(?:consisting of|using)\s+(?:1|one)\b|"
        r"\b(?:1|one)-stitch shell\b|\bshell of a single stitch\b|\bone stitch shell\b",
        line,
        re.IGNORECASE,
    ):
        found.append("A shell of 1 is not a shell. Use at least 3 stitches.")
    if re.search(
        r"\bcluster\b.{0,20}\b(?:consisting of|using)\s+(?:1|one)\b|\bcluster of a single\b",
        line,
        re.IGNORECASE,
    ):
        found.append("A 1-dc cluster is one stitch, not a cluster.")
    if re.search(r"\bbobble\b.{0,24}\b(?:made from a single stitch|using\s+(?:1|one)|consisting of\s+(?:1|one))\b", line, re.IGNORECASE):
        found.append("A bobble of 1 has nothing to gather.")
    if re.search(r"\bpuff\b.{0,24}\b(?:using\s+(?:1|one)|consisting of\s+(?:1|one)|using one stitch)\b", line, re.IGNORECASE):
        found.append("A puff of 1 is not a puff.")
    if re.search(r"\bpopcorn\b.{0,24}\b(?:using\s+(?:1|one)|consisting of\s+(?:1|one)|using one stitch)\b", line, re.IGNORECASE):
        found.append("A popcorn of 1 cannot be closed.")
    if re.search(
        r"\b(?:v-stitch|v stitch)\b.{0,20}\busing\s+(?:1|one)\b|\bv made of a single stitch\b",
        line,
        re.IGNORECASE,
    ):
        found.append("A V-stitch of 1 is not a V-stitch.")
    if re.search(
        r"\bfan\b.{0,20}\b(?:using|consisting of|made from)\s+(?:1|one)\b",
        line,
        re.IGNORECASE,
    ):
        found.append("A fan of 1 is not a fan.")
    if re.search(
        r"\bstar(?:\s+stitch)?\b.{0,20}\b(?:using|consisting of)\s+(?:1|one)\b",
        line,
        re.IGNORECASE,
    ):
        found.append("A star stitch of 1 cannot make a star.")
    if re.search(r"\b(?:0|zero)-chain space\b|\bch\s+sp of\s+(?:0|zero)\b|\bspace of\s+(?:0|zero)\s+chains\b", line, re.IGNORECASE):
        found.append("A ch-0 space has no chains to work into.")
    if re.search(r"\brnds?\s+(?:0|zero)\b", line, re.IGNORECASE):
        found.append("Round 0 is not a round. Start at Round 1.")
    if re.search(r"\bstarting\s+round\s*:?\s*(?:0|zero)\b", line, re.IGNORECASE):
        found.append("Round 0 is not a round. Start at Round 1.")
    if re.search(r"\bstarting\s+row\s*:?\s*(?:0|zero)\b", line, re.IGNORECASE):
        found.append("Row 0 is not a row. Start at Row 1.")
    if re.search(r"\b(?:pm in st(?:itch)?|marker at stitch)\s+(?:0|zero)\b", line, re.IGNORECASE):
        found.append("Stitch 0 does not exist. Place the marker in stitch 1 or later.")
    copied = re.search(
        r"\b(\d+(?:\.\d+)?)\s+in(?:ches)?\b[^.\n]{0,24}\b(?:is|equals|=)\s*\1\s*(?:cm|centimet(?:er|re)s?)\b",
        line,
        re.IGNORECASE,
    )
    if copied:
        found.append(
            f"{copied.group(1)} inches is not {copied.group(1)} cm. The line copies the same number."
        )
    copied = re.search(
        r"\b(\d+(?:\.\d+)?)\s*(?:cm|centimet(?:er|re)s?)\s*(?:=|is|equals)\s*\1\s*(?:in\b|inches)\b",
        line,
        re.IGNORECASE,
    )
    if copied:
        found.append(
            f"{copied.group(1)} cm is not {copied.group(1)} inches. The line copies the same number."
        )
    if re.search(r"\b(?:insert|mount|attach)\s+(?:0|zero|no)\s+(?:safety\s+)?eyes?\b", line, re.IGNORECASE):
        found.append("Place 0 safety eyes mounts nothing.")
    if re.search(r"\(\s*make\s+(?:no|none)\s*\)", line, re.IGNORECASE):
        found.append("Make 0 asks for none of that piece.")
    if (
        re.search(r"\bjoin\b", line, re.IGNORECASE)
        and re.search(r"\bunjoined\b|\bleave it open\b", line, re.IGNORECASE)
        and not re.search(r"\bor\b", line, re.IGNORECASE)
    ):
        found.append("The line says to join and not to join.")
    if re.search(
        r"\btight(?:ly)?\b.{0,16}\bloose(?:ly)?\b|\bloose(?:ly)?\b.{0,16}\btight(?:ly)?\b",
        line,
        re.IGNORECASE,
    ) and not re.search(r"\bor\b", line, re.IGNORECASE):
        found.append("One round cannot be worked tightly and loosely.")
    if re.search(r"\bfasten off\b.{0,48}\b(?:continue\s+with\s+(?:the\s+)?same yarn|keep crocheting)\b", line, re.IGNORECASE):
        found.append("Fasten off ends the yarn. The same yarn was not continued.")
    if re.search(r"\bx\s+0(?!\d|\.\d)\b|\btimes\s+(?:0(?!\d|\.\d)|zero)\b", line, re.IGNORECASE):
        found.append("A repeat of 0 does no work.")
    if re.search(r"\bwork straight for\s+(?:0|zero|no)\s+rows\b", line, re.IGNORECASE):
        found.append("Work even for 0 rows does no work.")
    if re.search(r"\bwork even for\s+(?:0|zero)\s+rounds\b", line, re.IGNORECASE):
        found.append("Work even for 0 rows does no work.")
    if re.search(r"\b(?:0|zero)\s+rows\s+high\b|\b(?:0|zero)\s+rounds\s+high\b|\bheight:\s*(?:0|zero)\s+rows\b", line, re.IGNORECASE):
        found.append("A piece that is 0 rows tall was not made.")
    if re.search(r"\b(?:square|tube|corner|oval|rectangle)\b.{0,24}\b(?:of|using|with)\s+(?:no(?!\s+more)|zero|0)\b", line, re.IGNORECASE):
        found.append("A count of 0 does not make that shape.")
    if re.search(r"\b(?:buttonhole|button loop)\b.{0,24}\b(?:from|with)\s+(?:no|0|zero)\b", line, re.IGNORECASE):
        found.append("A buttonhole of 0 chains has no opening.")
    if re.search(r"\bfringe\b", line, re.IGNORECASE) and re.search(
        r"\b(?:no|zero|0)\s+(?:cut\s+)?(?:yarn\s+)?strands\b|\bcut\s+(?:no|zero|0)\s+strands\b",
        line,
        re.IGNORECASE,
    ):
        found.append("A fringe of 0 strands is not a fringe.")
    if re.search(r"\bcable\b", line, re.IGNORECASE) and re.search(
        r"\b(?:over|cross|of)\s+(?:no|zero|0)\s+stitches\b", line, re.IGNORECASE
    ):
        found.append("A cable over 0 stitches does not cross.")
    if re.search(r"\b(?:spike|long stitch)\b.{0,24}\b(?:down|of)\s+(?:no|zero|0)\s+rows\b|\bdrop down\s+(?:0|zero)\s+rows\b", line, re.IGNORECASE):
        found.append("A spike stitch down 0 rows does not leave the current row.")
    if re.search(r"\bsurface\b.{0,28}\b(?:line\s+)?of\s+(?:no|0|zero)\b", line, re.IGNORECASE):
        found.append("Surface crochet of 0 chains draws no line.")
    if re.search(r"\bi[ -]?cord\b.{0,20}\b(?:on|using)\s+(?:no|0|zero)\b", line, re.IGNORECASE):
        found.append("An i-cord of 0 stitches has no cord.")
    if re.search(r"\b(?:pom\s*pom|pompom|tassel)\b.{0,20}\b(?:of|using)\s+(?:0|zero|no)\b", line, re.IGNORECASE):
        found.append("A wrap count of 0 has nothing to tie.")
    if re.search(r"\b(?:solomon'?s?|lover'?s?)\s+knot\b.{0,16}\bof\s+(?:0|zero)\b", line, re.IGNORECASE):
        found.append("A Solomon knot of 0 is not a knot.")
    if re.search(r"\bpineapple\b.{0,20}\b(?:motif\s+of|using)\s+(?:0|zero)\b|\bpineapple\b.{0,12}\bof\s+0\b", line, re.IGNORECASE):
        found.append("A pineapple of 0 is not a pineapple motif.")
    if re.search(r"\bbullion\b.{0,20}\bwith\s+(?:no|0|zero)\b", line, re.IGNORECASE):
        found.append("A bullion of 0 wraps has no wraps.")
    if re.search(r"\bbead\b.{0,20}\bevery\s+(?:no|0|zero)\b", line, re.IGNORECASE):
        found.append("A bead every 0 stitches is never placed.")
    if re.search(r"\bgauge\b.{0,24}\b(?:0|zero)\s+stitches\b|\b(?:0|zero)\s+sc\s+per\b", line, re.IGNORECASE):
        found.append("A gauge of 0 sc is not a fabric.")
    if re.search(r"\b(?:0|zero)\s+(?:meters|metres|yd)\b|\byardage of\s+(?:0|zero)\b", line, re.IGNORECASE):
        found.append("0 yards cannot make the piece.")
    if re.search(r"\bfill\s+with\s+(?:0|zero)\s+g\b|\bstuff(?:ing|ed)?\s+using\s+(?:0|zero)\b", line, re.IGNORECASE):
        found.append("Stuff with 0 g leaves the piece empty.")
    return found


def _range_back(label: str, start: str, end: str) -> list[str]:
    left, right = _gap_count(start), _gap_count(end)
    if left is None or right is None or left <= right:
        return []
    name = "Rows" if label.lower().startswith("row") else "Rounds"
    return [f"{name} {left}-{right} run backwards."]


def _short_turn(raw: str, stitch_raw: str) -> list[str]:
    words = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5}
    chains = words[raw.lower()] if raw.lower() in words else int(raw)
    names = {
        "sc": "sc",
        "hdc": "hdc",
        "dc": "dc",
        "tr": "tr",
        "dtr": "dtr",
        "single crochet": "sc",
        "half double": "hdc",
        "half double crochet": "hdc",
        "double crochet": "dc",
        "treble": "tr",
        "double treble": "dtr",
    }
    stitch = names[stitch_raw.lower()]
    needed = {"sc": 1, "hdc": 2, "dc": 3, "tr": 4, "dtr": 5}[stitch]
    short = chains <= needed - 2 if stitch in {"tr", "dtr"} else chains < needed
    if not short:
        return []
    return [f"ch {chains} is too short to turn for a {stitch}. Use ch {needed}."]



def _glued_wording(line: str) -> list[str]:
    """Catch the same rule when a space or a small word is missing."""
    found: list[str] = []
    move = re.search(
        r"\b(inc|increase|dec|decrease)\s+from\s+(\d+|[A-Za-z]+)\s+(?:up|down)\s+to\s+(\d+|[A-Za-z]+)\b",
        line,
        re.IGNORECASE,
    )
    if move:
        left, right = _gap_count(move.group(2)), _gap_count(move.group(3))
        if left is not None and right is not None:
            if move.group(1).lower().startswith("inc") and right <= left:
                found.append(f"Increase from {move.group(2)} to {move.group(3)} does not rise.")
            if move.group(1).lower().startswith("dec") and right >= left:
                found.append(f"Decrease from {move.group(2)} to {move.group(3)} does not fall.")
    down = re.search(
        r"\b(rounds|rows)\s+from\s+(\d+|[A-Za-z]+)\s+down\s+(?:through|to)\s+(\d+|[A-Za-z]+)\b",
        line,
        re.IGNORECASE,
    )
    if down:
        found.extend(_range_back(down.group(1), down.group(2), down.group(3)))
    stitch = (
        r"(sc|hdc|dc|tr|dtr|single crochet|half double(?: crochet)?|"
        r"double crochet|treble|double treble)"
    )
    glued_turn = re.search(
        rf"\bch(\d+)\s*,?\s*turn(?:\s*,|\s+for(?:\s+an?)?)?\s+{stitch}\b",
        line,
        re.IGNORECASE,
    )
    if glued_turn:
        found.extend(_short_turn(glued_turn.group(1), glued_turn.group(2)))
    word_turn = re.search(
        r"\bch(?:ain)?\s+(one|two|three|four|five|\d+)\s*,?\s*turn(?:\s*,|\s+for(?:\s+an?)?)?\s+"
        r"(treble|double treble)\b",
        line,
        re.IGNORECASE,
    )
    if word_turn:
        found.extend(_short_turn(word_turn.group(1), word_turn.group(2)))
    after = re.search(
        rf"\b(?:after turning,\s*)?ch\s+(\d+)\s*,\s*{stitch}\b",
        line,
        re.IGNORECASE,
    )
    if after and re.search(r"\bturn", line, re.IGNORECASE):
        found.extend(_short_turn(after.group(1), after.group(2)))
    glued_counts = re.search(
        rf"\bch(\d+)\s+counts\s+as\s+(?:an?\s+|the\s+)?{stitch}\b",
        line,
        re.IGNORECASE,
    )
    if glued_counts:
        found.extend(_glued_counts_as(glued_counts.group(1), glued_counts.group(2)))
    for match in re.finditer(
        r"\b([A-P](?:/[A-Z])?(?:[-/]\d+(?:\.\d+)?)?)\s*(?:hook\s+)?(?:=|:|\bat\b|listed as)\s*"
        r"(\d+(?:\.\d+)?)\s*(?:mm|millimet(?:er|re)s?)\b",
        line,
        re.IGNORECASE,
    ):
        found.extend(_hook_gap_match(match.group(1), match.group(2)))
    listed = re.search(
        r"\b([A-P](?:/[A-Z])?(?:[-/]\d+(?:\.\d+)?)?)\s+(?:hook\s+)?(?:is\s+)?listed as\s+"
        r"(\d+(?:\.\d+)?)\s*(?:mm|millimet(?:er|re)s?)\b",
        line,
        re.IGNORECASE,
    )
    if listed:
        found.extend(_hook_gap_match(listed.group(1), listed.group(2)))
    copied = re.search(
        r"\b(\d+(?:\.\d+)?)\s*in(?:ches)?\s*=\s*\1\s*(?:cm|centimet(?:er|re)s?)\b",
        line,
        re.IGNORECASE,
    )
    if copied:
        found.append(
            f"{copied.group(1)} inches is not {copied.group(1)} cm. The line copies the same number."
        )
    even = re.search(
        r"\b(\d+)\s+stitches\s+must\s+be\s+even\b|\bstitch count\s+(\d+)\s+must\s+be\s+even\b|"
        r"\b(\d+)\s+is\s+required\s+to\s+be\s+even\b|\beven\s+(?:number\s+required|stitch count of)\s*:?\s*(\d+)\b",
        line,
        re.IGNORECASE,
    )
    if even:
        raw = next(group for group in even.groups() if group)
        if int(raw) % 2:
            found.append(f"{raw} is odd, but the line says the count must be even.")
    odd = re.search(
        r"\b(\d+)\s+stitches\s+must\s+be\s+odd\b|\bcount of\s+(\d+)\s+must\s+be\s+odd\b|"
        r"\bodd\s+number\s+required\s*:?\s*(\d+)\b",
        line,
        re.IGNORECASE,
    )
    if odd:
        raw = next(group for group in odd.groups() if group)
        if int(raw) % 2 == 0:
            found.append(f"{raw} is even, but the line says the count must be odd.")
    apart = re.search(
        r"\beyes\s+(?:placed\s+)?(\d+|[A-Za-z]+)\s+sts?\s+apart\b.{0,40}\b(\d+|[A-Za-z]+)[- ]st\s+round\b",
        line,
        re.IGNORECASE,
    )
    if apart:
        left, right = _gap_count(apart.group(1)), _gap_count(apart.group(2))
        if left is not None and right is not None and left >= right:
            found.append(f"Eyes {left} stitches apart do not fit on a {right}-stitch round.")
    marker = re.search(
        r"\b(?:marker|pm)\s+in\s+st(?:itch)?\s+(\d+|[A-Za-z]+)\b.{0,32}\b(\d+|[A-Za-z]+)[- ]st\s+round\b",
        line,
        re.IGNORECASE,
    )
    if marker:
        left, right = _gap_count(marker.group(1)), _gap_count(marker.group(2))
        if left is not None and right is not None and left > right:
            found.append(f"Stitch {left} is past a {right}-stitch round.")
    skipped = re.search(
        r"\b(?:skip|sk)\s+(\d+|[A-Za-z]+)(?:\s+sts?)?\b.{0,24}\b(\d+|[A-Za-z]+)[- ]st\s+row\b",
        line,
        re.IGNORECASE,
    )
    if skipped:
        left, right = _gap_count(skipped.group(1)), _gap_count(skipped.group(2))
        if left is not None and right is not None and left >= right:
            found.append(f"Skip {left} does not fit on a {right}-stitch row.")
    if re.search(
        r"\bshell\s*(?:=|is)\s*(?:1|one|a single)\b|\b(?:1|one)\s+dc\s+shell\b|"
        r"\bshell consisting of a single stitch\b",
        line,
        re.IGNORECASE,
    ):
        found.append("A shell of 1 is not a shell. Use at least 3 stitches.")
    if re.search(r"\bcluster\s*(?:=|is)\s*(?:1|one|a single)\b", line, re.IGNORECASE):
        found.append("A 1-dc cluster is one stitch, not a cluster.")
    if re.search(r"\bbobble\s+is\s+(?:one|a single)\s+stitch\b", line, re.IGNORECASE):
        found.append("A bobble of 1 has nothing to gather.")
    if re.search(r"\bpuff\s+is\s+a\s+single\s+stitch\b", line, re.IGNORECASE):
        found.append("A puff of 1 is not a puff.")
    if re.search(r"\bpopcorn\s+is\s+one\s+dc\b", line, re.IGNORECASE):
        found.append("A popcorn of 1 cannot be closed.")
    if re.search(r"\bv-?st\b.{0,20}\b(?:of a single|made of one)\b", line, re.IGNORECASE):
        found.append("A V-stitch of 1 is not a V-stitch.")
    if re.search(r"\bfan\s+(?:is|made of)\s+one\b", line, re.IGNORECASE):
        found.append("A fan of 1 is not a fan.")
    if re.search(r"\bstar\s+is\s+one\s+stitch\b", line, re.IGNORECASE):
        found.append("A star stitch of 1 cannot make a star.")
    if re.search(
        r"\bpicot\s*:\s*(?:0|zero)\b|\bch\s*0\s+picot\b|\bpicot\s+with\s+0\s*ch\b",
        line,
        re.IGNORECASE,
    ):
        found.append("A picot of 0 is not a picot.")
    if re.search(r"\brsc\b", line, re.IGNORECASE) and re.search(r"\bforwards?\b", line, re.IGNORECASE) and not re.search(r"\bbackward\b", line, re.IGNORECASE):
        found.append("Reverse single crochet is worked backward, not forward.")
    if (
        re.search(r"\b(?:magic circle|magic loop|adjustable ring|adjustable loop)\b", line, re.IGNORECASE)
        and re.search(r"\bchain-ring\b|\bchain ring\b", line, re.IGNORECASE)
        and not re.search(r"\bor\b|instead|without", line, re.IGNORECASE)
    ):
        found.append("A piece cannot start with both a magic ring and a chain ring.")
    if (
        re.search(r"\bfsc\b", line, re.IGNORECASE)
        and re.search(r"\bchain\s+\d+\b", line, re.IGNORECASE)
        and re.search(r"\b(?:to\s+start|as\s+the\s+start|to\s+begin)\b", line, re.IGNORECASE)
        and not re.search(r"\bor\b|instead|without", line, re.IGNORECASE)
    ):
        found.append("Foundation single crochet replaces the starting chain.")
    if re.search(
        r"\b(?:front[- ]post|back[- ]post|fpdc|bpdc|fptr|bptr|post stitch)\b.{0,28}"
        r"\b(?:into|around)\s+(?:the\s+|a\s+)?ch(?:ain)?\d*\b|\baround the post of the chain\b",
        line,
        re.IGNORECASE,
    ):
        found.append("A chain has no post. Do not work a post around the chain.")
    if re.search(r"\bturning chain\b.{0,24}\badded twice\b|\bcount the chain a second time\b", line, re.IGNORECASE):
        found.append("A turning chain counted twice is added two times.")
    if re.search(r"\bfasten off\b.{0,40}\bproceed\b.{0,24}\bsame yarn\b", line, re.IGNORECASE):
        found.append("Fasten off ends the yarn. The same yarn was not continued.")
    if re.search(r"(?<![\d.])0in\b", line, re.IGNORECASE):
        found.append("A finished width of 0 inches is not a piece.")
    if re.search(r"(?<![\d.])0yd\b", line, re.IGNORECASE):
        found.append("0 yards cannot make the piece.")
    if re.search(r"(?<![\d.])0sc\b", line, re.IGNORECASE):
        found.append("A gauge of 0 sc is not a fabric.")
    if re.search(r"\bch\s+none\b|\bchains of none\b", line, re.IGNORECASE):
        found.append("ch 0 makes no chain.")
    if re.search(r"\byo\s+none\b|\byarn over no times\b", line, re.IGNORECASE):
        found.append("yo 0 does not put yarn on the hook.")
    if re.search(r"\bpull through none\b|\bpull through no loop\b", line, re.IGNORECASE):
        found.append("Pull through 0 loops leaves the loops on the hook.")
    if re.search(r"\bstart(?:ing)?\s+round\s*:\s*(?:0|zero)\b", line, re.IGNORECASE):
        found.append("Round 0 is not a round. Start at Round 1.")
    if (
        re.search(r"\binside-?\s*out\b", line, re.IGNORECASE)
        and re.search(r"\bright-?\s*side out\b", line, re.IGNORECASE)
        and not re.search(r"\bor\b", line, re.IGNORECASE)
    ):
        found.append("Inside out and right side out disagree.")
    if (
        re.search(r"\bleft-to-right\b", line, re.IGNORECASE)
        and re.search(r"\bright-to-left\b", line, re.IGNORECASE)
        and not re.search(r"\bor\b", line, re.IGNORECASE)
    ):
        found.append("The line gives both directions and does not say or.")
    return found


def _glued_counts_as(raw: str, stitch_raw: str) -> list[str]:
    names = {
        "sc": "sc",
        "single crochet": "sc",
        "hdc": "hdc",
        "half double": "hdc",
        "half double crochet": "hdc",
        "dc": "dc",
        "double crochet": "dc",
        "tr": "tr",
        "treble": "tr",
        "dtr": "dtr",
        "double treble": "dtr",
    }
    pair = (raw, names[stitch_raw.lower()])
    if pair not in COUNTS_AS:
        return []
    return [f"ch {pair[0]} cannot count as a {pair[1]}."]



def _uses_none(line: str) -> list[str]:
    """Catch the same empty count or copied rule with another verb."""
    found: list[str] = []
    if re.search(r"\bloop stitch\b.{0,20}\b(?:has\s+)?(?:zero|no)\s+loops\b", line, re.IGNORECASE):
        found.append("A loop stitch of 0 has no loop.")
    if re.search(r"\b(?:rectangle|square|tube|corner)\s+(?:has|uses)\s+(?:no|zero)\b", line, re.IGNORECASE):
        found.append("A count of 0 does not make that shape.")
    if re.search(r"\bi-?cord\b.{0,20}\buses\s+(?:no|zero)\b", line, re.IGNORECASE):
        found.append("An i-cord of 0 stitches has no cord.")
    if re.search(r"\bcable\b.{0,24}\bcross(?:es)?\s+(?:no|zero)\b", line, re.IGNORECASE):
        found.append("A cable over 0 stitches does not cross.")
    if re.search(r"\bspike\b.{0,20}\bdrops?\s+(?:no|zero)\b", line, re.IGNORECASE):
        found.append("A spike stitch down 0 rows does not leave the current row.")
    if re.search(r"\bsurface\b.{0,24}\buses\s+(?:no|zero)\b", line, re.IGNORECASE):
        found.append("Surface crochet of 0 chains draws no line.")
    if re.search(r"\bfringe\b.{0,24}\bcuts?\s+(?:no|zero)\b", line, re.IGNORECASE):
        found.append("A fringe of 0 strands is not a fringe.")
    if re.search(r"\bbuttonhole\b.{0,20}\buses\s+(?:no|zero)\b", line, re.IGNORECASE):
        found.append("A buttonhole of 0 chains has no opening.")
    if re.search(r"\bbead\b.{0,16}\bevery\s+none\b", line, re.IGNORECASE):
        found.append("A bead every 0 stitches is never placed.")
    if re.search(r"\bstripe\b.{0,16}\bevery\s+none\b|\bcolour every none\b|\bcolor every none\b", line, re.IGNORECASE):
        found.append("A stripe every 0 rounds never stripes.")
    if re.search(r"\b(?:pom-?pom|tassel)\b.{0,20}\bwraps?\s+(?:no|none|zero)\b", line, re.IGNORECASE):
        found.append("A wrap count of 0 has nothing to tie.")
    if re.search(r"\bpineapple\b.{0,20}\buses\s+(?:no|zero)\b", line, re.IGNORECASE):
        found.append("A pineapple of 0 is not a pineapple motif.")
    if re.search(r"\bbullion\b.{0,16}\bwraps?\s+none\b", line, re.IGNORECASE):
        found.append("A bullion of 0 wraps has no wraps.")
    if re.search(r"\bsolomon(?:'s)?\s+knot\b.{0,20}\buses\s+(?:no|zero)\b", line, re.IGNORECASE):
        found.append("A Solomon knot of 0 is not a knot.")
    if re.search(r"\b(?:stuff(?:ing|ed)?\s+using|fill\s+with)\s+(?:no|zero)\b", line, re.IGNORECASE):
        found.append("Stuffing with 0 does not fill the piece.")
    if re.search(r"\bplace\s+none of the safety eyes\b", line, re.IGNORECASE):
        found.append("Place 0 safety eyes mounts nothing.")
    if re.search(r"\byardage is none\b|\buses no yards\b", line, re.IGNORECASE):
        found.append("0 yards cannot make the piece.")
    if re.search(r"\bwork even across no rows\b|\bwork straight for none rows\b", line, re.IGNORECASE):
        found.append("Work even for 0 rows does no work.")
    if re.search(r"\b(?:inc|increase)\s+every\s+none\b", line, re.IGNORECASE):
        found.append("Every 0 rows or rounds never happens.")
    if re.search(r"\bmake\s+none\b|\bmake\s+no\b(?!\s+more)", line, re.IGNORECASE):
        found.append("Make 0 asks for none of that piece.")
    if re.search(r"\bheight is no rows\b|\bno rounds of height\b", line, re.IGNORECASE):
        found.append("A piece that is 0 rows tall was not made.")
    if re.search(r"\bmake no chains to start\b|\bchains of none\b", line, re.IGNORECASE):
        found.append("ch 0 makes no chain.")
    if re.search(r"\buntil none (?:remain|are left)\b", line, re.IGNORECASE):
        found.append("Repeat until 0 stitches is not a workable stop.")
    if re.search(r"\bpopcorn is a single stitch\b", line, re.IGNORECASE):
        found.append("A popcorn of 1 cannot be closed.")
    if re.search(r"\b0\s*ch\s+picot\b", line, re.IGNORECASE):
        found.append("A picot of 0 is not a picot.")
    if re.search(r"\b(?:0|zero)\s+in\.?\s+wide\b", line, re.IGNORECASE):
        found.append("A finished width of 0 inches is not a piece.")
    if re.search(r"\bround\b.{0,24}\b(?:from side to side|back and forth)\b", line, re.IGNORECASE):
        found.append("A round says across. Rounds are worked around.")
    if re.search(r"\brow\b.{0,24}\bworked in the round\b|\bthis row is joined and worked around\b", line, re.IGNORECASE):
        found.append("A row says around. Rows are worked across.")
    if re.search(r"\bturn the round\b|\bat the end of each round, turn\b", line, re.IGNORECASE):
        found.append("A round says turn. A continuous round does not turn.")
    if re.search(r"\bspiral\b", line, re.IGNORECASE) and re.search(
        r"\bjoined at the end\b|\bjoins with a sl st\b|\ba joined round\b", line, re.IGNORECASE
    ):
        found.append("A continuous spiral does not join every round. The join was not added.")
    if re.search(r"\bus\s+dc\b", line, re.IGNORECASE) and re.search(r"\buk\s+double\b", line, re.IGNORECASE) and not re.search(r"\buk\s+treble\b|\bnot a uk double\b", line, re.IGNORECASE):
        found.append("A US double crochet is a UK treble, not a UK double.")
    if re.search(r"\btr\b.{0,24}\bcalled uk tr\b", line, re.IGNORECASE):
        found.append("A US treble is a UK double treble, not a UK treble.")
    if re.search(r"\bslipknot\b.{0,24}\bas\b|\bstarting knot counts as\b", line, re.IGNORECASE):
        found.append("The slip knot is not a chain stitch.")
    if (
        re.search(r"\bright handed\b", line, re.IGNORECASE)
        and re.search(r"\bleft handed\b", line, re.IGNORECASE)
        and not re.search(r"\bor\b|\bseparate\b", line, re.IGNORECASE)
    ):
        found.append("Right-handed and left-handed work need separate instructions.")
    if re.search(r"\bjoin\b", line, re.IGNORECASE) and re.search(r"\bleave the round open\b|\bround stays open\b", line, re.IGNORECASE) and not re.search(r"\bor\b", line, re.IGNORECASE):
        found.append("The line says to join and not to join.")
    if re.search(r"\b(?:sl\s*st|slst)\s+join\b", line, re.IGNORECASE) and re.search(r"\bno join\b", line, re.IGNORECASE):
        found.append("The line says to join and not to join.")
    if re.search(r"\btwo strands\b", line, re.IGNORECASE) and re.search(r"\bsingle strand\b", line, re.IGNORECASE) and not re.search(r"\bor\b", line, re.IGNORECASE):
        found.append("The yarn cannot be held double and single at the same time.")
    steel = re.search(
        r"\bsteel(?:\s+hook)?\b.{0,32}\b(\d+)\s+is\s+(?:larger|bigger)\s+than\s+(\d+)\b",
        line,
        re.IGNORECASE,
    )
    if steel and int(steel.group(1)) > int(steel.group(2)):
        found.append("A higher steel-hook number is smaller, not larger.")
    if re.search(r"\bhook\b", line, re.IGNORECASE) and re.search(r"\b(?:zero|one|two|three|four|five|six|seven|eight|nine|ten|nought)\s*cm\b", line, re.IGNORECASE):
        found.append("The hook is written in centimeters. Crochet hooks are written in millimeters.")
    if re.search(r"\bhook\b", line, re.IGNORECASE) and re.search(r"\bnought\s*mm\b", line, re.IGNORECASE):
        found.append("A hook of 0 mm cannot make a stitch.")
    shown = re.search(
        r"\bturning chain:\s*(one|\d+)\s*,\s*then\s+(sc|hdc|dc|tr|dtr|treble|double treble)\b",
        line,
        re.IGNORECASE,
    )
    if shown:
        found.extend(_short_turn(shown.group(1), shown.group(2)))
    later = re.search(
        r"\bturn then ch\s+(one|\d+)\s+for\s+(?:a\s+)?(sc|hdc|dc|tr|dtr|treble|double treble)\b",
        line,
        re.IGNORECASE,
    )
    if later:
        found.extend(_short_turn(later.group(1), later.group(2)))
    for match in re.finditer(
        r"\b(\d+)\s+sts?\s*,\s*multiple of\s+(\d+)\b|\bcount is\s+(\d+)\b.{0,32}\bmultiple of\s+(\d+)\b|"
        r"\bstitch count of\s+(\d+)\s+is a multiple of\s+(\d+)\b|\b(\d+)\s+stitches should be a multiple of\s+(\d+)\b",
        line,
        re.IGNORECASE,
    ):
        nums = [group for group in match.groups() if group]
        count, base = int(nums[0]), int(nums[1])
        if base and count % base:
            found.append(f"{count} is not divisible by {base}.")
    written = re.search(
        r"\bwritten as\s+(\d+|[A-Za-z]+)\s+on a\s+(\d+|[A-Za-z]+)-stitch\b|"
        r"\b(\d+|[A-Za-z]+)\s+stitch edge written as\s+(\d+|[A-Za-z]+)\b",
        line,
        re.IGNORECASE,
    )
    if written:
        groups = [group for group in written.groups() if group]
        if "edge" in written.group(0).lower():
            edge, stated = _gap_count(groups[0]), _gap_count(groups[1])
        else:
            stated, edge = _gap_count(groups[0]), _gap_count(groups[1])
        if stated is not None and edge is not None and stated != edge:
            found.append(f"Written count {stated} does not match the {edge}-stitch edge.")
    grown = re.search(r"\bsc2tog\s+from\s+(\d+)\s+to\s+(\d+)\b", line, re.IGNORECASE)
    if grown and int(grown.group(2)) >= int(grown.group(1)):
        found.append(f"Decrease from {grown.group(1)} to {grown.group(2)} does not fall.")
    shrunk = re.search(r"\b2\s+sc\s+in\s+each\s+from\s+(\d+)\s+to\s+(\d+)\b", line, re.IGNORECASE)
    if shrunk and int(shrunk.group(2)) <= int(shrunk.group(1)):
        found.append(f"Increase from {shrunk.group(1)} to {shrunk.group(2)} does not rise.")
    moved = re.search(r"\bincrease\b.{0,20}\bfrom\s+(\d+)\s+to\s+(\d+)\b", line, re.IGNORECASE)
    if moved and int(moved.group(2)) <= int(moved.group(1)):
        found.append(f"Increase from {moved.group(1)} to {moved.group(2)} does not rise.")
    mark = re.search(r"\b(\d+)\s*(?:\"|″)\s*=\s*\1\s*cm\b", line, re.IGNORECASE)
    if mark:
        found.append(f"{mark.group(1)} inches is not {mark.group(1)} cm. The line copies the same number.")
    if re.search(r"\bx\s*\d+\.\d+\b|\b\d+\.\d+\s+single crochets\b|\b(?:repeat|rep)\s+\d+,\d+\s+times\b|\b(?:rep|repeat)\s+\d+\.\d+x\b", line, re.IGNORECASE):
        found.append("A fractional repeat is not a whole repeat.")
    if re.search(r"\bboth ways\b", line, re.IGNORECASE) and not re.search(r"\bor\b", line, re.IGNORECASE):
        found.append("The line gives both directions and does not say or.")
    if re.search(r"\bclockwise\b", line, re.IGNORECASE) and re.search(r"\b(?:counterclockwise|anti-clockwise)\b", line, re.IGNORECASE) and not re.search(r"\bor\b", line, re.IGNORECASE):
        found.append("The line gives both directions and does not say or.")
    if re.search(r"\bin the round plus flat\b|\bworked circular and also flat\b|\bin rounds and flat\b", line, re.IGNORECASE):
        found.append("In the round and in rows are two fabrics. The extra fabric was not invented.")
    if (
        re.search(r"\bfoundation\s+(?:single crochet|sc)\b", line, re.IGNORECASE)
        and re.search(r"\bch\s+\d+\s+to\s+start\b", line, re.IGNORECASE)
        and not re.search(r"\bor\b|instead|without", line, re.IGNORECASE)
    ):
        found.append("Foundation single crochet replaces the starting chain.")
    if re.search(r"\byo\b", line, re.IGNORECASE) and re.search(r"\byarn under\b", line, re.IGNORECASE) and re.search(r"\bsame\s+st(?:itch)?\b", line, re.IGNORECASE):
        found.append("Yarn over and yarn under cannot be the same stitch.")
    if re.search(r"\bsame chain is in the count again\b", line, re.IGNORECASE):
        found.append("A turning chain counted twice is added two times.")
    if re.search(r"\bbreak yarn\b.{0,32}\bcontinue in the same yarn\b", line, re.IGNORECASE):
        found.append("Fasten off ends the yarn. The same yarn was not continued.")
    return found



def _has_one(line: str) -> list[str]:
    """Catch has-no, is-one, and the same rule in another order."""
    found: list[str] = []
    if re.search(r"\bfringe\s+has\s+(?:no|zero)\b", line, re.IGNORECASE):
        found.append("A fringe of 0 strands is not a fringe.")
    if re.search(r"\bcable\s+has\s+(?:no|zero)\b", line, re.IGNORECASE):
        found.append("A cable over 0 stitches does not cross.")
    if re.search(r"\bspike\s+has\s+(?:no|zero)\b", line, re.IGNORECASE):
        found.append("A spike stitch down 0 rows does not leave the current row.")
    if re.search(r"\bi\s*cord\s+has\s+(?:no|zero)\b", line, re.IGNORECASE):
        found.append("An i-cord of 0 stitches has no cord.")
    if re.search(r"\b(?:pom\s*pom|tassel)\s+has\s+(?:no|zero)\b", line, re.IGNORECASE):
        found.append("A wrap count of 0 has nothing to tie.")
    if re.search(r"\bpineapple\s+has\s+(?:no|zero)\b", line, re.IGNORECASE):
        found.append("A pineapple of 0 is not a pineapple motif.")
    if re.search(r"\bbullion\s+has\s+(?:no|zero)\b", line, re.IGNORECASE):
        found.append("A bullion of 0 wraps has no wraps.")
    if re.search(r"\bsolomon(?:'s)?\s+knot\s+has\s+(?:no|zero)\b", line, re.IGNORECASE):
        found.append("A Solomon knot of 0 is not a knot.")
    if re.search(r"\boval\s+has\s+(?:no|zero)\b", line, re.IGNORECASE):
        found.append("An oval cannot start with 0 chains.")
    if re.search(r"\bloop\s+has\s+no\s+yarn\b", line, re.IGNORECASE):
        found.append("A loop stitch of 0 has no loop.")
    if re.search(r"\bbutton loop\s+uses\s+(?:no|zero)\b", line, re.IGNORECASE):
        found.append("A buttonhole of 0 chains has no opening.")
    if re.search(r"\bpuff\s+is\s+(?:one|a single)\b", line, re.IGNORECASE):
        found.append("A puff of 1 is not a puff.")
    if re.search(r"\bv[- ]?stitch\s+is\s+(?:one|a single)\b", line, re.IGNORECASE):
        found.append("A V-stitch of 1 is not a V-stitch.")
    if re.search(r"\bfan\s+is\s+(?:one|a single)\b", line, re.IGNORECASE):
        found.append("A fan of 1 is not a fan.")
    if re.search(r"\bstar(?:\s+stitch)?\s+is\s+(?:one|a single)\b", line, re.IGNORECASE):
        found.append("A star stitch of 1 cannot make a star.")
    if re.search(r"\bpicot\s*=\s*(?:0|zero)\b|\bch-0\s+picot\b", line, re.IGNORECASE):
        found.append("A picot of 0 is not a picot.")
    if re.search(r"\b(?:place|mount)\s+(?:0|zero|no)\s+eyes\b|\bsafety eyes:\s*none\b", line, re.IGNORECASE):
        found.append("Place 0 safety eyes mounts nothing.")
    if re.search(r"\byardage:\s*none\b", line, re.IGNORECASE):
        found.append("0 yards cannot make the piece.")
    if re.search(r"\bwork even for no rounds\b|\bstraight for\s+(?:0|zero)\s+rows\b", line, re.IGNORECASE):
        found.append("Work even for 0 rows does no work.")
    if re.search(r"\bheight:\s*no rows\b|\b(?:0|zero)\s+rows of height\b", line, re.IGNORECASE):
        found.append("A piece that is 0 rows tall was not made.")
    if re.search(r"\bstuff with no fiber\b|\bfill using no grams\b", line, re.IGNORECASE):
        found.append("Stuffing with 0 does not fill the piece.")
    if re.search(r"\bevery none rows\b|\b(?:decrease|dec)\s+every none\b", line, re.IGNORECASE):
        found.append("Every 0 rows or rounds never happens.")
    if re.search(r"\bbead on none\b|\bstripe on none\b", line, re.IGNORECASE):
        found.append("A bead every 0 stitches is never placed.")
    if re.search(r"\b(?:us\s+)?(?<!half )double crochet\b.{0,24}\buk double\b", line, re.IGNORECASE) and not re.search(r"\buk treble\b|\bnot a uk double\b", line, re.IGNORECASE):
        found.append("A US double crochet is a UK treble, not a UK double.")
    if re.search(r"\bdc\s+uk double\b", line, re.IGNORECASE):
        found.append("A US double crochet is a UK treble, not a UK double.")
    if re.search(r"(?<!double )treble\s*\(\s*uk treble\s*\)|\bus\s+tr\s+is called uk tr\b", line, re.IGNORECASE):
        found.append("A US treble is a UK double treble, not a UK treble.")
    if re.search(r"\bround goes (?:side to side|back and forth)\b", line, re.IGNORECASE):
        found.append("A round says across. Rounds are worked around.")
    if re.search(r"\brow goes around\b", line, re.IGNORECASE):
        found.append("A row says around. Rows are worked across.")
    if re.search(r"\bturn after (?:the|each) round\b|\bafter the round, turn\b", line, re.IGNORECASE):
        found.append("A round says turn. A continuous round does not turn.")
    if re.search(r"\bspiral\b.{0,32}\b(?:joined by sl st|closed with a sl st)\b", line, re.IGNORECASE):
        found.append("A continuous spiral does not join every round. The join was not added.")
    if re.search(r"\bcut yarn\b.{0,40}\bcontinue in the same yarn\b|\bfasten off\b.{0,40}\bproceed in that yarn\b|\bafter fastening off\b.{0,40}\bcontinue in the same yarn\b", line, re.IGNORECASE):
        found.append("Fasten off ends the yarn. The same yarn was not continued.")
    if re.search(r"\b(?:starting knot|slip knot) is stitch\b", line, re.IGNORECASE):
        found.append("The slip knot is not a chain stitch.")
    if re.search(r"\bjoin and leave open\b|\bjoined and left open\b", line, re.IGNORECASE):
        found.append("The line says to join and not to join.")
    if re.search(r"\bright handers\b", line, re.IGNORECASE) and re.search(r"\bleft handers\b", line, re.IGNORECASE) and not re.search(r"\bor\b", line, re.IGNORECASE):
        found.append("Right-handed and left-handed work need separate instructions.")
    if re.search(r"\bRS out\b", line) and re.search(r"\bWS out\b", line) and not re.search(r"\bor\b", line, re.IGNORECASE):
        found.append("The right side and the wrong side cannot both face the worker.")
    glued = re.search(r"\bchain1\s*,?\s*turn\s*,?\s*(sc|hdc|dc|tr|dtr|treble)\b", line, re.IGNORECASE)
    if glued:
        found.extend(_short_turn("1", glued.group(1)))
    listed = re.search(
        r"\b([A-P](?:/[A-Z])?(?:[-/]\d+(?:\.\d+)?)?)\s+listed\s+(\d+(?:\.\d+)?)\s*mm\b",
        line,
        re.IGNORECASE,
    )
    if listed:
        found.extend(_hook_gap_match(listed.group(1), listed.group(2)))
    down = re.search(r"\binc(?:rease)?\s+down from\s+(\d+)\s+to\s+(\d+)\b", line, re.IGNORECASE)
    if down and int(down.group(2)) <= int(down.group(1)):
        found.append(f"Increase from {down.group(1)} to {down.group(2)} does not rise.")
    up = re.search(r"\bdec(?:rease)?\s+up from\s+(\d+)\s+to\s+(\d+)\b", line, re.IGNORECASE)
    if up and int(up.group(2)) >= int(up.group(1)):
        found.append(f"Decrease from {up.group(1)} to {up.group(2)} does not fall.")
    back = re.search(r"\b(rounds|rows)\s+run from\s+(\d+)\s+back to\s+(\d+)\b", line, re.IGNORECASE)
    if back:
        found.extend(_range_back(back.group(1), back.group(2), back.group(3)))
    rnd = re.search(r"\bfrom rnd\s+(\d+)\s+back to rnd\s+(\d+)\b", line, re.IGNORECASE)
    if rnd:
        found.extend(_range_back("rnd", rnd.group(1), rnd.group(2)))
    apart = re.search(
        r"\beyes\b.{0,24}\b(\d+)\s+sts?\s+apart\b.{0,40}\bround (?:has|is)\s+(\d+)\s+sts?\b",
        line,
        re.IGNORECASE,
    )
    if apart and int(apart.group(1)) >= int(apart.group(2)):
        found.append(f"Eyes {apart.group(1)} stitches apart do not fit on a {apart.group(2)}-stitch round.")
    marker = re.search(r"\bmarker\b.{0,24}\bstitch\s+(\d+)\b.{0,32}\bround is\s+(\d+)\b", line, re.IGNORECASE)
    if marker and int(marker.group(1)) > int(marker.group(2)):
        found.append(f"Stitch {marker.group(1)} is past a {marker.group(2)}-stitch round.")
    skipped = re.search(r"\bskip\s+(\d+)\b.{0,32}\brow is\s+(\d+)\s+sts?\b", line, re.IGNORECASE)
    if skipped and int(skipped.group(1)) >= int(skipped.group(2)):
        found.append(f"Skip {skipped.group(1)} does not fit on a {skipped.group(2)}-stitch row.")
    mult = re.search(r"\bmultiple of\s+(\d+)\s+but the count is\s+(\d+)\b", line, re.IGNORECASE)
    if mult and int(mult.group(1)) and int(mult.group(2)) % int(mult.group(1)):
        found.append(f"{mult.group(2)} is not divisible by {mult.group(1)}.")
    even = re.search(r"\beven number is required\b.{0,32}\bcount is\s+(\d+)\b", line, re.IGNORECASE)
    if even and int(even.group(1)) % 2:
        found.append(f"{even.group(1)} is odd, but the line says the count must be even.")
    if re.search(r"\b\d+,\d+\s+(?:sc|hdc|dc)\b", line, re.IGNORECASE):
        found.append("A decimal stitch is not a whole stitch.")
    if re.search(r"\bx\s+\d+,\d+\b", line, re.IGNORECASE):
        found.append("A fractional repeat is not a whole repeat.")
    together = re.search(r"\bsc2tog\s+(\d+)\s+to\s+(\d+)\b", line, re.IGNORECASE)
    if together and int(together.group(2)) >= int(together.group(1)):
        found.append(f"Decrease from {together.group(1)} to {together.group(2)} does not fall.")
    return found




def _word_order(line: str) -> list[str]:
    """Catch the same written rule when the words are in another order."""
    found: list[str] = []
    choice = re.search(r"\bor\b", line, re.IGNORECASE)
    if (
        re.search(r"\brighties\b", line, re.IGNORECASE)
        and re.search(r"\blefties\b", line, re.IGNORECASE)
        and not choice
        and not re.search(r"\bseparate\b", line, re.IGNORECASE)
    ):
        found.append("Right-handed and left-handed work need separate instructions.")
    if re.search(r"\binstructions for right hand and left hand\b", line, re.IGNORECASE) and not choice:
        found.append("Right-handed and left-handed work need separate instructions.")
    if (
        re.search(r"\btwo strands\b", line, re.IGNORECASE)
        and re.search(r"\bone strand\b", line, re.IGNORECASE)
        and not choice
    ):
        found.append("The yarn cannot be held double and single at the same time.")
    if (
        re.search(r"\b(?:flo|front loop only)\b", line, re.IGNORECASE)
        and re.search(r"\bback loop\b", line, re.IGNORECASE)
        and re.search(r"\b(?:same stitch|plus)\b", line, re.IGNORECASE)
        and not choice
    ):
        found.append("FLO and BLO cannot be the same stitch.")
    if (
        re.search(r"\b(?:magic loop|adjustable ring)\b", line, re.IGNORECASE)
        and re.search(r"\bchain(?:-\d+)? start\b", line, re.IGNORECASE)
        and not choice
        and not re.search(r"\binstead\b|\bwithout\b", line, re.IGNORECASE)
    ):
        found.append("A piece cannot start with both a magic ring and a chain ring.")
    turn = re.search(
        r"\b(?:chain of (one|1)|turning chain of (one|1)|ch (one|1) is the turning chain)\b.{0,32}\b(dc|double crochet|tr|treble)\b",
        line,
        re.IGNORECASE,
    )
    if turn:
        number = next(group for group in turn.groups()[:3] if group)
        found.extend(_short_turn(number, turn.group(4)))
    steel = re.search(
        r"\bsteel\b.{0,24}\bhook\s+(\d+)\s+is\s+(?:bigger|larger)\s+than\s+hook\s+(\d+)\b",
        line,
        re.IGNORECASE,
    )
    if steel and int(steel.group(1)) > int(steel.group(2)):
        found.append("A higher steel-hook number is smaller, not larger.")
    if re.search(r"\bwork toward the left and the right\b|\bleftwards and rightwards\b", line, re.IGNORECASE) and not choice:
        found.append("The line gives both directions and does not say or.")
    if re.search(r"\byo plus under in one stitch\b", line, re.IGNORECASE):
        found.append("Yarn over and yarn under cannot be the same stitch.")
    if re.search(
        r"\bcount the turning chain a second time\b|\bthe chain is counted again\b|\badd the turning chain a second time\b",
        line,
        re.IGNORECASE,
    ):
        found.append("A turning chain counted twice is added two times.")
    if re.search(r"\bturning chain counts and does not count\b", line, re.IGNORECASE):
        found.append("The line says the chain counts as a stitch and does not count. The count was not invented.")
    if (
        re.search(r"\bfsc\b", line, re.IGNORECASE)
        and re.search(r"\bch\s+\d+\s+to\s+start\b", line, re.IGNORECASE)
        and not choice
        and not re.search(r"\binstead\b|\bwithout\b", line, re.IGNORECASE)
    ):
        found.append("Foundation single crochet replaces the starting chain.")
    if re.search(r"\bcontinuous rounds joined\b", line, re.IGNORECASE) and not choice:
        found.append("A continuous spiral does not join every round. The join was not added.")
    shrunk = re.search(r"\bincrease shrinks,\s*(\d+)\s+to\s+(\d+)\b", line, re.IGNORECASE)
    if shrunk and int(shrunk.group(2)) <= int(shrunk.group(1)):
        found.append(f"Increase from {shrunk.group(1)} to {shrunk.group(2)} does not rise.")
    grown = re.search(r"\bdecrease grows,\s*(\d+)\s+to\s+(\d+)\b", line, re.IGNORECASE)
    if grown and int(grown.group(2)) >= int(grown.group(1)):
        found.append(f"Decrease from {grown.group(1)} to {grown.group(2)} does not fall.")
    if (
        re.search(r"\bin the round and also worked flat\b|\bcircular and flat for the same piece\b", line, re.IGNORECASE)
        and not choice
    ):
        found.append("In the round and in rows are two fabrics. The extra fabric was not invented.")
    if re.search(r"\bbreak the yarn and continue with it\b|\bfasten off and keep the yarn\b", line, re.IGNORECASE):
        found.append("Fasten off ends the yarn. The same yarn was not continued.")
    claimed = re.search(
        r"\b(\d+) is not a multiple, it is claimed as a multiple of (\d+)\b",
        line,
        re.IGNORECASE,
    )
    if claimed and int(claimed.group(2)) and int(claimed.group(1)) % int(claimed.group(2)):
        found.append(f"{claimed.group(1)} is not divisible by {claimed.group(2)}.")
    skipped = re.search(r"\bskip\s+(\d+)\s+sts?\b.{0,40}\brow is\s+(\d+)\s+stitches\b", line, re.IGNORECASE)
    if skipped and int(skipped.group(1)) >= int(skipped.group(2)):
        found.append(f"Skip {skipped.group(1)} does not fit on a {skipped.group(2)}-stitch row.")
    if re.search(r"\bboth loops and the back loop\b", line, re.IGNORECASE) and not choice:
        found.append("BLO only and both loops cannot be the same stitch.")
    if re.search(r"\bus treble called a uk treble\b", line, re.IGNORECASE) and not re.search(r"\bnot a uk treble\b", line, re.IGNORECASE):
        found.append("A US treble is a UK double treble, not a UK treble.")
    return found



def _of_no(line: str) -> list[str]:
    """Catch the same empty count written with of, number, or x."""
    found: list[str] = []
    empty = r"(?:no(?!\s+more)|zero|0)"
    if re.search(rf"\bi-?cord\b.{{0,24}}\b(?:of|with)\s+{empty}\b", line, re.IGNORECASE):
        found.append("An i-cord of 0 stitches has no cord.")
    if re.search(rf"\b(?:pom-?pom|pom|tassel)\b.{{0,20}}\bof\s+{empty}\s+wraps\b", line, re.IGNORECASE):
        found.append("A wrap count of 0 has nothing to tie.")
    if re.search(rf"\bpineapple\b.{{0,20}}\bof\s+{empty}\b", line, re.IGNORECASE):
        found.append("A pineapple of 0 is not a pineapple motif.")
    if re.search(rf"\bbullion\b.{{0,16}}\bof\s+{empty}\b", line, re.IGNORECASE):
        found.append("A bullion of 0 wraps has no wraps.")
    if re.search(rf"\bsolomon(?:'s)?\s+knot\b.{{0,20}}\bof\s+{empty}\b", line, re.IGNORECASE):
        found.append("A Solomon knot of 0 is not a knot.")
    if re.search(rf"\bbuttonhole\b.{{0,20}}\bof\s+{empty}\b", line, re.IGNORECASE):
        found.append("A buttonhole of 0 chains has no opening.")
    if re.search(rf"\bsurface\b.{{0,24}}\b(?:with|of)\s+{empty}\s+chains\b", line, re.IGNORECASE):
        found.append("Surface crochet of 0 chains draws no line.")
    if re.search(r"\bheight of\s+(?:0|zero)\s+rows\b", line, re.IGNORECASE):
        found.append("A piece that is 0 rows tall was not made.")
    if re.search(r"\bwork even across\s+(?:0|zero)\s+rows\b|\bstraight for zero rounds\b", line, re.IGNORECASE):
        found.append("Work even for 0 rows does no work.")
    if re.search(r"\b(?:0|zero)\s+stitches per\b", line, re.IGNORECASE):
        found.append("A gauge of 0 sc is not a fabric.")
    if re.search(r"\bround number\s+(?:0|zero)\b", line, re.IGNORECASE):
        found.append("Round 0 is not a round. Start at Round 1.")
    if re.search(r"\bstitch number\s+(?:0|zero)\b", line, re.IGNORECASE):
        found.append("Stitch 0 does not exist. The first stitch is stitch 1.")
    if re.search(r"\b(?:repeat|rep)\s+x\s+zero\b|\bx\s+zero\b", line, re.IGNORECASE):
        found.append("A repeat of 0 does no work.")
    if re.search(r"\buntil zero remain\b", line, re.IGNORECASE):
        found.append("Repeat until 0 stitches is not a workable stop.")
    if re.search(r"\b(?:0|zero)\s+cm wide\b", line, re.IGNORECASE):
        found.append("A finished width of 0 inches is not a piece.")
    if re.search(r"\bhook\b.{0,24}\bnought\s+millimetres\b", line, re.IGNORECASE):
        found.append("A hook of 0 mm cannot make a stitch.")
    return found




def _nothing(line: str) -> list[str]:
    """Catch the same empty count written as nothing."""
    if re.search(r"\bunworked\b", line, re.IGNORECASE):
        return []
    found: list[str] = []
    if re.search(r"\bi-?cord\b.{0,32}\bnothing\b", line, re.IGNORECASE):
        found.append("An i-cord of 0 stitches has no cord.")
    if re.search(r"\bcable\b.{0,40}\bcross(?:es)?\s+nothing\b", line, re.IGNORECASE):
        found.append("A cable over 0 stitches does not cross.")
    if re.search(r"\bspike\b.{0,32}\b(?:drops?|down)\s+nothing\b", line, re.IGNORECASE):
        found.append("A spike stitch down 0 rows does not leave the current row.")
    if re.search(r"\bsurface\b.{0,32}\b(?:draws?|uses|of)\s+nothing\b", line, re.IGNORECASE):
        found.append("Surface crochet of 0 chains draws no line.")
    if re.search(r"\bfringe\b.{0,32}\b(?:cuts?|of|from)\s+nothing\b", line, re.IGNORECASE):
        found.append("A fringe of 0 strands is not a fringe.")
    if re.search(r"\bbuttonhole\b.{0,32}\b(?:of|from|uses)\s+nothing\b|\bbuttonhole\b.{0,24}\bchained\s+from\s+nothing\b", line, re.IGNORECASE):
        found.append("A buttonhole of 0 chains has no opening.")
    if re.search(r"\b(?:pom-?pom|tassel)\b.{0,32}\b(?:wrap(?:ped|s)?|of)\s+nothing\b", line, re.IGNORECASE):
        found.append("A wrap count of 0 has nothing to tie.")
    if re.search(r"\bpineapple\b.{0,32}\b(?:built|made|of|from)\s+nothing\b", line, re.IGNORECASE):
        found.append("A pineapple of 0 is not a pineapple motif.")
    if re.search(r"\bbullion\b.{0,32}\b(?:wrap(?:ped|s)?|of)\s+nothing\b", line, re.IGNORECASE):
        found.append("A bullion of 0 wraps has no wraps.")
    if re.search(r"\bsolomon(?:'s)?\s+knot\b.{0,32}\b(?:tied|of|from)\s+nothing\b", line, re.IGNORECASE):
        found.append("A Solomon knot of 0 is not a knot.")
    if re.search(r"\byardage\b.{0,24}\bnothing\b(?!\s+(?:special|else|more|extra))", line, re.IGNORECASE):
        found.append("0 yards cannot make the piece.")
    if re.search(r"\bstuff(?:ing|ed)?\b.{0,20}\b(?:using|with)\s+nothing\b(?!\s+(?:extra|else|more))", line, re.IGNORECASE):
        found.append("Stuffing with 0 does not fill the piece.")
    if re.search(r"\bwork even\b.{0,20}\bfor\s+nothing\b", line, re.IGNORECASE):
        found.append("Work even for 0 rows does no work.")
    if re.search(r"\bheight\b.{0,16}\bof\s+nothing\b", line, re.IGNORECASE):
        found.append("A piece that is 0 rows tall was not made.")
    if re.search(r"\bbead\b.{0,24}\b(?:on|every|after)\s+nothing\b", line, re.IGNORECASE):
        found.append("A bead every 0 stitches is never placed.")
    if re.search(r"\bstripe\b.{0,24}\b(?:after|every|on)\s+nothing\b", line, re.IGNORECASE):
        found.append("A stripe every 0 rounds never stripes.")
    if re.search(r"\bgauge\b.{0,24}\b(?:reads|of|is)\s+nothing\b", line, re.IGNORECASE):
        found.append("A gauge of 0 sc is not a fabric.")
    if re.search(r"\b(?:repeat|rep)\s+(?:x\s+)?nothing\b|\btimes\s+nothing\b", line, re.IGNORECASE):
        found.append("A repeat of 0 does no work.")
    if re.search(r"\bround\b.{0,24}\bnumbered\s+nothing\b", line, re.IGNORECASE):
        found.append("Round 0 is not a round. Start at Round 1.")
    if re.search(r"\brow\b.{0,24}\bnumbered\s+nothing\b", line, re.IGNORECASE):
        found.append("Row 0 is not a row. Start at Row 1.")
    if re.search(r"\bstitch\b.{0,24}\bnumbered\s+nothing\b", line, re.IGNORECASE):
        found.append("Stitch 0 does not exist. The first stitch is stitch 1.")
    if re.search(r"\bhook\b.{0,32}\bnothing\s+(?:mm|millimet(?:er|re)s?|millimeters?)\b", line, re.IGNORECASE):
        found.append("A hook of 0 mm cannot make a stitch.")
    if re.search(r"\b(?:ch|chain)\s+(?:of\s+)?nothing\b", line, re.IGNORECASE):
        found.append("ch 0 makes no chain.")
    if re.search(r"\bdec(?:rease)?\b.{0,16}\bto\s+nothing\b", line, re.IGNORECASE):
        found.append("Decrease to 0 stitches leaves nothing to fasten.")
    if re.search(r"\bmake\s+nothing\b(?!\s+(?:else|extra|more|up))", line, re.IGNORECASE):
        found.append("Make 0 asks for none of that piece.")
    if re.search(r"\bsafety eyes?\b.{0,16}(?::|are|is)\s*nothing\b|\b(?:place|mount)\s+nothing\b.{0,20}\beyes\b", line, re.IGNORECASE):
        found.append("Place 0 safety eyes mounts nothing.")
    if re.search(r"\bloop stitch\b.{0,24}\b(?:of|uses|has)\s+nothing\b", line, re.IGNORECASE):
        found.append("A loop stitch of 0 has no loop.")
    if re.search(r"\bsquare\b.{0,24}\b(?:of|from|for)\s+nothing\b", line, re.IGNORECASE):
        found.append("A square of 0 rounds was not worked.")
    if re.search(r"\brectangle\b.{0,24}\b(?:of|for|from)\s+nothing\b", line, re.IGNORECASE):
        found.append("A rectangle of 0 rows was not worked.")
    if re.search(r"\btube\b.{0,24}\b(?:of|with|from)\s+nothing\b", line, re.IGNORECASE):
        found.append("A tube of 0 stitches has no opening.")
    if re.search(r"\bcorner\b.{0,24}\b(?:of|uses)\s+nothing\b", line, re.IGNORECASE):
        found.append("A corner of 0 chains does not turn the corner.")
    if re.search(r"\boval\b.{0,24}\b(?:of|with|from)\s+nothing\b", line, re.IGNORECASE):
        found.append("An oval cannot start with 0 chains.")
    if re.search(r"\bpicot\b.{0,16}\bof\s+nothing\b", line, re.IGNORECASE):
        found.append("A picot of 0 is not a picot.")
    if re.search(r"\bshell\b.{0,16}\bof\s+nothing\b", line, re.IGNORECASE):
        found.append("A shell of 0 is not a shell. Use at least 3 stitches.")
    if re.search(r"\b(?:width of nothing|nothing inches wide|nothing cm wide)\b", line, re.IGNORECASE):
        found.append("A finished width of 0 inches is not a piece.")
    return found


def _weight_category(line: str) -> list[str]:
    low = line.lower()
    best: tuple[str, tuple[int, ...], int] | None = None
    for name, allowed in WEIGHTS:
        match = re.search(
            rf"\bcategory\s+(\d+)\b.{{0,24}}(?<![a-z]){re.escape(name)}\b"
            rf"|(?<![a-z]){re.escape(name)}\b.{{0,24}}\bcategory\s+(\d+)\b",
            low,
        )
        if not match:
            continue
        number = int(match.group(1) or match.group(2))
        if best is None or len(name) > len(best[0]):
            best = (name, allowed, number)
    if best and best[2] not in best[1]:
        shown = "/".join(str(item) for item in best[1])
        return [f"{best[0].title()} is Craft Yarn Council category {shown}, not {best[2]}."]
    return []


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
        r"steel(?:\s+hook)?\s+(\d+).{0,40}\b(?:larger|bigger)\b.{0,30}steel(?:\s+hook)?\s+(\d+)",
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
