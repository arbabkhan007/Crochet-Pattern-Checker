"""Fifty written-phrase checks.

Each rule matches one impossible or contradictory sentence. A quoted line
is not an instruction. A prohibition is not a defect, except the rule that
looks for join and do-not-join on the same line.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class PhraseRule:
    slug: str
    title: str
    how: str
    what: str
    wrong: str
    corrected: str
    pattern: str
    message: str
    needle: str
    allow_prohibition: bool = False


RULES: tuple[PhraseRule, ...] = (
    PhraseRule(
        "hook_zero", "Zero hook",
        "a hook of 0 mm cannot pull up a loop.",
        "the corrected file uses a 5 mm hook.",
        "Hook: 0 mm.\n", "Hook: 5 mm.\n",
        r"Hook:\s*0\s*mm",
        "A hook of 0 mm cannot make a stitch.",
        "0 mm cannot",
    ),
    PhraseRule(
        "hook_huge", "Huge hook",
        "a 40 mm hook is past even jumbo crochet. This warns.",
        "the corrected file uses a 6 mm hook.",
        "Hook: 40 mm.\n", "Hook: 6 mm.\n",
        r"Hook:\s*(?:[3-9]\d|\d{3,})\s*mm",
        "A hook of 40 mm or more is past normal crochet. This is a warning.",
        "past normal crochet",
    ),
    PhraseRule(
        "hook_cm", "Hook in centimeters",
        "a hook written as 5 cm is 50 mm. Crochet hooks are written in millimeters.",
        "the corrected file says 5 mm.",
        "Hook: 5 cm.\n", "Hook: 5 mm.\n",
        r"Hook:\s*\d+(?:\.\d+)?\s*cm\b",
        "The hook is written in centimeters. Crochet hooks are written in millimeters.",
        "written in centimeters",
    ),
    PhraseRule(
        "chain_zero", "Zero chain",
        "ch 0 makes no chain to work into.",
        "the corrected file chains 4.",
        "ch 0, then sc in the next stitch.\n", "ch 4, then sc in the next stitch.\n",
        r"\bch\s+0\b",
        "ch 0 makes no chain.",
        "no chain",
    ),
    PhraseRule(
        "work_zero", "Work zero",
        "work 0 stitches is an instruction that does nothing.",
        "the corrected file works 6 stitches.",
        "Work 0 stitches.\n", "Work 6 stitches.\n",
        r"\bwork\s+0\s+stitches\b",
        "Work 0 stitches does no work.",
        "does no work",
    ),
    PhraseRule(
        "skip_zero", "Skip zero",
        "skip 0 does not move the hook.",
        "the corrected file skips 2.",
        "Skip 0 stitches.\n", "Skip 2 stitches.\n",
        r"\bskip\s+0\b",
        "Skip 0 does not move the hook.",
        "does not move",
    ),
    PhraseRule(
        "decrease_to_zero", "Decrease to zero",
        "decreasing to 0 stitches leaves nothing to fasten or sew.",
        "the corrected file decreases to 6 stitches.",
        "Decrease to 0 stitches.\n", "Decrease to 6 stitches.\n",
        r"\bdecrease\s+to\s+0\s+stitches\b",
        "Decrease to 0 stitches leaves nothing to fasten.",
        "nothing to fasten",
    ),
    PhraseRule(
        "until_zero", "Until zero",
        "repeat until 0 stitches is not a workable stop. A digit of 0 still counts as written, so the termination rule does not catch it.",
        "the corrected file stops at 6 stitches.",
        "Repeat until 0 stitches.\n", "Repeat until 6 stitches.\n",
        r"\buntil\s+0\s+stitches\b",
        "Repeat until 0 stitches is not a workable stop.",
        "not a workable stop",
    ),
    PhraseRule(
        "round_zero", "Round zero",
        "rounds are numbered from 1. Round 0 is not a round.",
        "the corrected file starts at Round 1.",
        "The piece starts at Round 0.\n", "The piece starts at Round 1.\n",
        r"\bRound\s+0\b",
        "Round 0 is not a round. Start at Round 1.",
        "not a round",
    ),
    PhraseRule(
        "marker_zero", "Marker at zero",
        "stitch 0 does not exist. The first stitch is stitch 1.",
        "the corrected file places the marker in stitch 1.",
        "Place the marker in stitch 0.\n", "Place the marker in stitch 1.\n",
        r"\bmarker in stitch 0\b",
        "Stitch 0 does not exist. Place the marker in stitch 1 or later.",
        "Stitch 0 does not exist",
    ),
    PhraseRule(
        "gauge_zero", "Zero gauge",
        "a gauge of 0 sc per 4 inches is not a fabric.",
        "the corrected file uses 12 sc per 4 inches.",
        "Gauge: 0 sc = 4 inches.\n", "Gauge: 12 sc = 4 inches.\n",
        r"Gauge:\s*0\s+sc\b",
        "A gauge of 0 sc is not a fabric.",
        "not a fabric",
    ),
    PhraseRule(
        "zero_inches", "Zero inches",
        "a finished width of 0 inches is not a piece.",
        "the corrected file is 4 inches wide.",
        "Finished width: 0 inches wide.\n", "Finished width: 4 inches wide.\n",
        r"\b0\s+inches\s+wide\b",
        "A finished width of 0 inches is not a piece.",
        "0 inches is not",
    ),
    PhraseRule(
        "picot_zero", "Picot of zero",
        "a picot of 0 chains is not a picot.",
        "the corrected file uses a picot of 3.",
        "Work a picot of 0.\n", "Work a picot of 3.\n",
        r"\bpicot of 0\b",
        "A picot of 0 is not a picot.",
        "not a picot",
    ),
    PhraseRule(
        "ch0_space", "Chain-zero space",
        "a ch-0 space has no chains to work into.",
        "the corrected file uses a ch-2 space.",
        "sc in the ch-0 sp.\n", "sc in the ch-2 sp.\n",
        r"\bch-0\s+sp\b",
        "A ch-0 space has no chains to work into.",
        "no chains to work into",
    ),
    PhraseRule(
        "shell_one", "Shell of one",
        "a shell needs at least 3 stitches. A shell of 1 is a single stitch.",
        "the corrected file uses a shell of 5.",
        "Work a shell of 1.\n", "Work a shell of 5.\n",
        r"\bshell of 1\b",
        "A shell of 1 is not a shell. Use at least 3 stitches.",
        "not a shell",
    ),
    PhraseRule(
        "cluster_one", "Cluster of one",
        "a 1-dc cluster is one double crochet, not a cluster.",
        "the corrected file uses a 3-dc cluster.",
        "Work a 1-dc cluster.\n", "Work a 3-dc cluster.\n",
        r"\b1-dc cluster\b",
        "A 1-dc cluster is one stitch, not a cluster.",
        "not a cluster",
    ),
    PhraseRule(
        "bobble_one", "Bobble of one",
        "a bobble of 1 has no stitches to gather.",
        "the corrected file uses a bobble of 5.",
        "Work a bobble of 1.\n", "Work a bobble of 5.\n",
        r"\bbobble of 1\b",
        "A bobble of 1 has nothing to gather.",
        "nothing to gather",
    ),
    PhraseRule(
        "puff_one", "Puff of one",
        "a puff of 1 is one yarn over, not a puff.",
        "the corrected file uses a puff of 5.",
        "Work a puff of 1.\n", "Work a puff of 5.\n",
        r"\bpuff of 1\b",
        "A puff of 1 is not a puff.",
        "not a puff",
    ),
    PhraseRule(
        "popcorn_one", "Popcorn of one",
        "a popcorn of 1 cannot be folded closed.",
        "the corrected file uses a popcorn of 5.",
        "Work a popcorn of 1.\n", "Work a popcorn of 5.\n",
        r"\bpopcorn of 1\b",
        "A popcorn of 1 cannot be closed.",
        "cannot be closed",
    ),
    PhraseRule(
        "yarn_over_zero", "Zero yarn over",
        "yo 0 does not put yarn on the hook.",
        "the corrected file uses yo 2.",
        "yo 0, then pull through.\n", "yo 2, then pull through.\n",
        r"\byo\s+0\b",
        "yo 0 does not put yarn on the hook.",
        "does not put yarn",
    ),
    PhraseRule(
        "pull_zero", "Pull through zero",
        "pull through 0 loops leaves the loops on the hook.",
        "the corrected file pulls through 2 loops.",
        "Pull through 0 loops.\n", "Pull through 2 loops.\n",
        r"\bpull through 0 loops\b",
        "Pull through 0 loops leaves the loops on the hook.",
        "leaves the loops",
    ),
    PhraseRule(
        "decimal_stitch", "Decimal stitch",
        "6.5 sc is not a whole stitch. The hook cannot make half a single crochet.",
        "the corrected file works 6 sc.",
        "Work 6.5 sc.\n", "Work 6 sc.\n",
        r"\b6\.5\s+sc\b",
        "6.5 sc is not a whole stitch.",
        "not a whole stitch",
    ),
    PhraseRule(
        "fraction_repeat", "Fractional repeat",
        "x 2.5 asks for half of a repeat. Repeats are whole numbers.",
        "the corrected file repeats 3 times.",
        "Repeat the shell x 2.5.\n", "Repeat the shell x 3.\n",
        r"\bx\s+2\.5\b",
        "x 2.5 is not a whole repeat.",
        "not a whole repeat",
    ),
    PhraseRule(
        "negative_repeat", "Negative repeat",
        "x -1 is not a repeat count.",
        "the corrected file repeats 4 times.",
        "Repeat x -1.\n", "Repeat x 4.\n",
        r"\bx\s+-\d+\b",
        "A negative repeat count is not a repeat.",
        "negative repeat",
    ),
    PhraseRule(
        "round_huge", "Round 9000",
        "Round 9000 is not a usable round number in this pattern.",
        "the corrected file says Round 9.",
        "The note points at Round 9000.\n", "The note points at Round 9.\n",
        r"\bRound\s+9000\b",
        "Round 9000 is not a usable round number.",
        "not a usable round",
    ),
    PhraseRule(
        "join_contradiction", "Join contradiction",
        "the same line says to join and not to join.",
        "the corrected file joins with a slip stitch.",
        "Join with a sl st and do not join.\n", "Join with a sl st.\n",
        r"\bjoin\b.*\b(?:do not|don\'t) join\b",
        "The line says to join and not to join.",
        "join and not to join",
        True,
    ),
    PhraseRule(
        "spiral_and_join", "Spiral and join",
        "a continuous spiral does not join every round. The two instructions disagree.",
        "the corrected file keeps the spiral and says not to join.",
        "Work in a continuous spiral and join every round.\n",
        "Work in a continuous spiral and do not join.\n",
        r"continuous spiral and join every round",
        "A continuous spiral cannot also join every round.",
        "cannot also join",
    ),
    PhraseRule(
        "blo_and_both", "Both loop claims",
        "BLO only and both loops cannot be the same stitch.",
        "the corrected file keeps BLO only.",
        "Work BLO only and both loops of the same stitch.\n", "Work BLO only.\n",
        r"BLO only and both loops",
        "BLO only and both loops cannot be the same stitch.",
        "cannot be the same stitch",
    ),
    PhraseRule(
        "inc_and_dec", "Increase and decrease",
        "inc and dec in each stitch cancel, and the line does not say which one.",
        "the corrected file increases in each stitch.",
        "Work inc and dec in each st.\n", "Work inc in each st.\n",
        r"inc and dec in each st",
        "inc and dec in each stitch contradict each other.",
        "contradict each other",
    ),
    PhraseRule(
        "both_directions", "Both directions",
        "left to right and right to left, with no or, gives two directions.",
        "the corrected file works left to right.",
        "Work left to right and right to left.\n", "Work left to right.\n",
        r"left to right and right to left",
        "The line gives both directions and does not say or.",
        "both directions",
    ),
    PhraseRule(
        "two_joins", "Two joins",
        "an invisible join and a slip-stitch join are two finishes. The line requires both.",
        "the corrected file uses the invisible join.",
        "Finish with an invisible join and sl st to join.\n",
        "Finish with an invisible join.\n",
        r"invisible join and sl st to join",
        "An invisible join and a slip-stitch join cannot both finish the round.",
        "cannot both finish",
    ),
    PhraseRule(
        "both_sides_facing", "Both sides facing",
        "the right side and the wrong side cannot both face the worker.",
        "the corrected file keeps the right side facing.",
        "With the right side facing and the wrong side facing.\n",
        "With the right side facing.\n",
        r"right side facing and the wrong side facing",
        "The right side and the wrong side cannot both face the worker.",
        "cannot both face",
    ),
    PhraseRule(
        "yarn_double_single", "Double and single",
        "the yarn cannot be held double and single at the same time.",
        "the corrected file holds the yarn double.",
        "Hold the yarn double and hold it single.\n", "Hold the yarn double.\n",
        r"hold the yarn double and hold it single",
        "The yarn cannot be held double and single at the same time.",
        "double and single",
    ),
    PhraseRule(
        "inside_and_out", "Inside and out",
        "turning inside out and keeping the right side out disagree.",
        "the corrected file turns inside out.",
        "Turn inside out and keep the right side out.\n", "Turn inside out.\n",
        r"inside out and keep the right side out",
        "Inside out and right side out disagree.",
        "disagree",
    ),
    PhraseRule(
        "tight_and_loose", "Tight and loose",
        "one round cannot be worked tightly and loosely.",
        "the corrected file works the round tightly.",
        "Work this round tightly and loosely.\n", "Work this round tightly.\n",
        r"tightly and loosely",
        "One round cannot be worked tightly and loosely.",
        "tightly and loosely",
    ),
    PhraseRule(
        "same_color", "Same color change",
        "changing from Color A to Color A is not a color change.",
        "the corrected file changes to Color B.",
        "Change from Color A to Color A.\n", "Change from Color A to Color B.\n",
        r"Change from Color A to Color A",
        "Changing from Color A to Color A is not a color change.",
        "not a color change",
    ),
    PhraseRule(
        "increase_same", "Increase to the same count",
        "an increase from 12 to 12 does not increase.",
        "the corrected file increases from 12 to 18.",
        "Increase from 12 to 12.\n", "Increase from 12 to 18.\n",
        r"Increase from 12 to 12",
        "An increase from 12 to 12 does not increase.",
        "does not increase",
    ),
    PhraseRule(
        "increase_down", "Increase that shrinks",
        "an increase from 12 to 6 is a decrease. The word and the numbers disagree.",
        "the corrected file increases from 6 to 12.",
        "Increase from 12 to 6.\n", "Increase from 6 to 12.\n",
        r"Increase from 12 to 6",
        "An increase from 12 to 6 shrinks. Call it a decrease, or reverse the numbers.",
        "shrinks",
    ),
    PhraseRule(
        "decrease_up", "Decrease that grows",
        "a decrease from 6 to 12 grows. The word and the numbers disagree.",
        "the corrected file decreases from 12 to 6.",
        "Decrease from 6 to 12.\n", "Decrease from 12 to 6.\n",
        r"Decrease from 6 to 12",
        "A decrease from 6 to 12 grows. Call it an increase, or reverse the numbers.",
        "grows",
    ),
    PhraseRule(
        "chain_counts_twice", "Chain counted twice",
        "a turning chain counted twice is added to the stitch count two times.",
        "the corrected file counts the turning chain once.",
        "The turning chain counts twice.\n", "The turning chain counts once.\n",
        r"turning chain counts twice",
        "A turning chain counted twice is added two times.",
        "added two times",
    ),
    PhraseRule(
        "post_around_chain", "Post around a chain",
        "a chain has no post. fpdc cannot go around the chain.",
        "the corrected file works the post around the dc.",
        "fpdc around the chain.\n", "fpdc around the dc.\n",
        r"fpdc around the chain",
        "A chain has no post. Do not work fpdc around the chain.",
        "no post",
    ),
    PhraseRule(
        "slip_knot_stitch", "Slip knot as a stitch",
        "the slip knot is not a chain stitch. Do not work into it.",
        "the corrected file works into the second chain.",
        "sc in the slip knot.\n", "sc in the 2nd ch from the hook.\n",
        r"sc in the slip knot",
        "The slip knot is not a chain stitch.",
        "not a chain stitch",
    ),
    PhraseRule(
        "short_turning_chain", "Short turning chain",
        "ch 1 is the turning chain for sc, not for dc. A dc turn needs ch 3.",
        "the corrected file uses ch 3 before the dc.",
        "ch 1, turn, dc in the next stitch.\n", "ch 3, turn, dc in the next stitch.\n",
        r"ch 1, turn, dc",
        "ch 1 is too short to turn for a dc. Use ch 3.",
        "too short to turn",
    ),
    PhraseRule(
        "round_uses_across", "Round says across",
        "a round is worked around. Across is the flat-row word.",
        "the corrected file says around.",
        "The round says sc in each st across.\n", "The round says sc in each st around.\n",
        r"The round says sc in each st across",
        "A round says across. Rounds are worked around.",
        "says across",
    ),
    PhraseRule(
        "row_uses_around", "Row says around",
        "a flat row is worked across. Around is the round word.",
        "the corrected file says across.",
        "The row says sc in each st around.\n", "The row says sc in each st across.\n",
        r"The row says sc in each st around",
        "A row says around. Rows are worked across.",
        "says around",
    ),
    PhraseRule(
        "round_says_turn", "Round says turn",
        "a continuous round does not turn. Turn belongs to a flat row.",
        "the corrected file does not turn.",
        "The round says turn before the stitches.\n", "The round is worked without a turn.\n",
        r"The round says turn",
        "A round says turn. A continuous round does not turn.",
        "says turn",
    ),
    PhraseRule(
        "backward_range", "Backward range",
        "Rounds 8-5 run backwards. A range has to climb.",
        "the corrected file uses Rounds 5-8.",
        "The range is Rounds 8-5.\n", "The range is Rounds 5-8.\n",
        r"Rounds 8-5",
        "Rounds 8-5 run backwards. Write the lower number first.",
        "run backwards",
    ),
    PhraseRule(
        "not_multiple", "Not a multiple",
        "a multiple of 3 cannot be 10 stitches. 10 is not divisible by 3.",
        "the corrected file uses 12 stitches.",
        "Multiple of 3, 10 stitches.\n", "Multiple of 3, 12 stitches.\n",
        r"Multiple of 3, 10 stitches",
        "10 is not a multiple of 3.",
        "not a multiple of 3",
    ),
    PhraseRule(
        "odd_when_even", "Odd when even",
        "a count that must be even cannot be 7.",
        "the corrected file uses 8.",
        "The count must be even (7 stitches).\n", "The count must be even (8 stitches).\n",
        r"must be even \(7 stitches\)",
        "7 is odd, but the line says the count must be even.",
        "7 is odd",
    ),
    PhraseRule(
        "eyes_too_far", "Eyes too far apart",
        "eyes 8 stitches apart cannot sit on a 6-stitch round.",
        "the corrected file places them 4 stitches apart.",
        "Place the eyes 8 stitches apart on a 6-stitch round.\n",
        "Place the eyes 4 stitches apart on a 6-stitch round.\n",
        r"8 stitches apart on a 6-stitch round",
        "Eyes 8 stitches apart do not fit on a 6-stitch round.",
        "do not fit",
    ),
)


def batch_names() -> list[str]:
    return [rule.title.lower() for rule in RULES]


def batch_findings(text: str) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    for rule in RULES:
        if _hit(text, rule):
            if rule.slug == "hook_huge":
                warnings.append(rule.message)
            else:
                errors.append(rule.message)
    return _unique(errors), _unique(warnings)


def _hit(text: str, rule: PhraseRule) -> bool:
    compiled = re.compile(rule.pattern, re.IGNORECASE)
    for line in text.splitlines():
        if line.lstrip().startswith(">"):
            continue
        if not rule.allow_prohibition and re.search(
            r"\bdo not\b|\bdon't\b|\bshould\s+not\b", line, re.IGNORECASE
        ):
            continue
        if compiled.search(line):
            return True
    return False


def _unique(items: list[str]) -> list[str]:
    found: list[str] = []
    for item in items:
        if item not in found:
            found.append(item)
    return found
