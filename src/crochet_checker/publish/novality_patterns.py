"""Customer-facing content for the ten Novality Store patterns.

The stitch instructions themselves come from the validated source patterns in
``examples/`` (see ``source``). Everything else here — titles, overviews,
materials, sizes, finishing and tips — is publisher copy written for sale on
Etsy. Materials and sizes marked in the validation report as publisher-supplied
where the original source pattern did not state them.
"""

BRAND = "Novality Store"
BRAND_SMALLCAPS = "NOVALITY STORE"
YEAR = 2026

COPYRIGHT = (
    "\u00a9 2026 Novality Store. All rights reserved.\n\n"
    "This pattern is for personal use only. You may sell finished items made "
    "from this pattern, but you may not copy, redistribute, resell, share, "
    "translate, reproduce, or claim this pattern as your own. The pattern "
    "itself may not be uploaded, reproduced, or distributed in digital or "
    "printed form without permission from Novality Store."
)

FOOTER_COPY = "\u00a9 2026 Novality Store \u00b7 Personal use only"

# Standard abbreviation definitions; each pattern lists only the ones it uses.
ABBREVIATIONS = {
    "ch": "chain",
    "st(s)": "stitch(es)",
    "sc": "single crochet",
    "hdc": "half double crochet",
    "dc": "double crochet",
    "tr": "treble",
    "sl st": "slip stitch",
    "inc": "increase \u2014 work 2 sc into the same stitch",
    "dec": "decrease \u2014 work 2 stitches together as one (sc2tog)",
    "MR": "magic ring",
    "rep": "repeat",
}

PATTERNS = [
    # ------------------------------------------------------------------ 01
    dict(
        slug="classic-amigurumi-ball",
        number="01",
        title="Classic Amigurumi Ball",
        tagline="A simple sphere to practice your first amigurumi.",
        source="examples/amigurumi.txt",
        difficulty="Beginner",
        time="2\u20133 hours",
        overview=(
            "Make a smooth little ball, worked in continuous rounds. "
            "This is a perfect first amigurumi project, and it works as a "
            "practice ball, a toy ball, or a base for a small creature."
        ),
        materials=[
            ("Yarn", "Worsted weight (medium, category 5), about 100 g in one colour"),
            ("Hook", "4.0 mm"),
            ("Also", "Yarn needle, polyester stuffing (optional)"),
        ],
        finished_size="About 7 cm (2.75 in) across",
        gauge="Not critical. Work a little tightly so no gaps show.",
        abbreviations=["MR", "sc", "inc", "dec", "st(s)"],
        notes=[
            "Worked in continuous rounds \u2014 there is no turning.",
            "Keep a stitch marker in the first stitch of each round.",
        ],
        finishing=[
            "Fasten off, leaving a long tail.",
            "Pull the tail through the last 6 stitches and pull tight to close the ball.",
            "Sew the top closed. Weave in all ends.",
        ],
        tips=[
            "Check your stitch count at the end of every round.",
            "Even, relaxed tension keeps the ball smooth.",
        ],
    ),
    # ------------------------------------------------------------------ 02
    dict(
        slug="amigurumi-bunny",
        number="02",
        title="Amigurumi Bunny",
        tagline="A sweet little bunny with long ears.",
        source="examples/amigurumi_bunny.txt",
        difficulty="Intermediate",
        time="5\u20137 hours",
        overview=(
            "A cuddly stuffed bunny with a round head and body and two long "
            "ears. Every piece is worked in continuous rounds, then sewn "
            "together. Follow the pieces in the order shown: head, body, "
            "ears, arms and legs."
        ),
        materials=[
            ("Yarn", "DK weight \u2014 white for the body, pink for the ears"),
            ("Hook", "3.5 mm"),
            ("Also", "2 safety eyes, polyester stuffing, embroidery thread, yarn needle"),
        ],
        finished_size="About 18\u201320 cm (7\u20138 in) tall, depending on stuffing",
        gauge="Not critical. Work tightly \u2014 stuffing will push the fabric out.",
        abbreviations=["MR", "sc", "inc", "dec", "st(s)"],
        notes=[
            "Worked in continuous rounds \u2014 there is no turning.",
            "Stuff the head and body firmly as you close them.",
            "Attach the ears at the top of the head, spaced apart.",
        ],
        finishing=[
            "Stuff the head and body firmly.",
            "Sew the head to the body.",
            "Attach the ears to the top of the head.",
            "Sew the arms to the sides of the body.",
            "Attach the legs to the bottom.",
            "Sew on the safety eyes and embroider a small nose.",
            "Weave in all ends.",
        ],
        tips=[
            "Keep a stitch marker in the first stitch of every round.",
            "Pin or baste each piece in position before sewing it on for good.",
        ],
    ),
    # ------------------------------------------------------------------ 03
    dict(
        slug="baby-booties",
        number="03",
        title="Baby Booties",
        tagline="Tiny booties for a newborn\u2019s feet.",
        source="examples/baby_booties.txt",
        difficulty="Beginner",
        time="1\u20132 hours each",
        overview=(
            "Make a pair of soft booties worked from the toe up in continuous "
            "rounds. The decreases in rounds 8 and 9 shape the opening for "
            "the foot."
        ),
        materials=[
            ("Yarn", "DK weight, about 50 g in one soft colour"),
            ("Hook", "3.5 mm"),
            ("Also", "Light stuffing (optional), yarn needle"),
        ],
        finished_size="Foot opening about 6\u20137 cm (2.5 in) around \u2014 newborn (0\u20133 months)",
        gauge="Not critical. Work evenly so the opening stays round.",
        abbreviations=["MR", "sc", "dec", "st(s)"],
        notes=[
            "Make 2 \u2014 one for each foot.",
            "Worked in continuous rounds \u2014 there is no turning.",
            "Keep a stitch marker in the first stitch of each round.",
        ],
        finishing=[
            "Fasten off and weave in the ends.",
            "Lightly stuff the foot if you like a fuller shape.",
            "Repeat for the second bootie.",
        ],
        tips=[
            "You should have 15 stitches at the end of round 8 and 11 at the end of round 9.",
            "Work the decreases in one area \u2014 that is where the foot opening forms.",
        ],
    ),
    # ------------------------------------------------------------------ 04
    dict(
        slug="simple-round-basket",
        number="04",
        title="Simple Round Basket",
        tagline="A sturdy round basket in 12 rounds.",
        source="examples/basket.txt",
        difficulty="Beginner",
        time="3\u20134 hours",
        overview=(
            "A round basket made of firm single crochet. The base grows in the "
            "first seven rounds, then the walls continue straight for five "
            "more rounds."
        ),
        materials=[
            ("Yarn", "Worsted weight (medium, category 5), about 200 g \u2014 cotton or a cotton blend works best"),
            ("Hook", "4.0 mm"),
            ("Also", "Yarn needle"),
        ],
        finished_size="About 8 cm (3.5 in) across, about 6 cm (2.5 in) deep",
        gauge="Work firmly \u2014 a tight stitch makes the basket stand on its own.",
        abbreviations=["MR", "sc", "inc", "st(s)"],
        notes=[
            "Worked in continuous rounds \u2014 there is no turning.",
            "Keep a stitch marker in the first stitch of each round.",
        ],
        finishing=[
            "Fasten off and weave in the ends.",
            "Optional: fold down the last 3 rounds for a neat rim.",
        ],
        tips=[
            "Keep your tension even, or the base will curl.",
            "The basket can be made bigger by adding more straight rounds.",
        ],
    ),
    # ------------------------------------------------------------------ 05
    dict(
        slug="simple-round-coaster",
        number="05",
        title="Simple Round Coaster",
        tagline="A quick round coaster in 8 rounds.",
        source="examples/flat_coaster.txt",
        difficulty="Beginner",
        time="1 hour",
        overview=(
            "A small flat circle in single crochet. Quick to finish, great for "
            "practising even rounds, and useful on the table."
        ),
        materials=[
            ("Yarn", "Worsted weight yarn or cotton, about 30 g in one colour"),
            ("Hook", "4.0 mm"),
            ("Also", "Yarn needle"),
        ],
        finished_size="About 9 cm (3.5 in) across",
        gauge="Work evenly so the coaster lies flat.",
        abbreviations=["MR", "sc", "inc", "st(s)"],
        notes=[
            "Worked in continuous rounds \u2014 there is no turning.",
            "Keep a stitch marker in the first stitch of each round.",
        ],
        finishing=[
            "Fasten off and weave in the ends.",
            "Optional: crochet a second identical circle and sew them together for a sturdier coaster.",
        ],
        tips=[
            "Cotton makes the best table coaster.",
            "Check your count at the end of each round \u2014 it doubles every round.",
        ],
    ),
    # ------------------------------------------------------------------ 06
    dict(
        slug="crochet-bowl",
        number="06",
        title="Crochet Bowl",
        tagline="A smooth, gently sloping bowl in 10 rounds.",
        source="examples/gradual_bowl.txt",
        difficulty="Beginner",
        time="2\u20133 hours",
        overview=(
            "A flat circle that grows a little every round. The steady "
            "increases keep the sides smooth and gentle, so the finished "
            "piece curves up like a small bowl."
        ),
        materials=[
            ("Yarn", "Worsted weight (medium, category 5), about 100 g in one colour"),
            ("Hook", "4.0 mm"),
            ("Also", "Yarn needle"),
        ],
        finished_size="About 12 cm (4.5 in) across",
        gauge="Work evenly \u2014 keep the rounds as flat as you can.",
        abbreviations=["MR", "sc", "inc", "st(s)"],
        notes=[
            "Worked in continuous rounds \u2014 there is no turning.",
            "Keep a stitch marker in the first stitch of each round.",
        ],
        finishing=[
            "Fasten off and weave in the ends.",
            "Optional: stuff the centre lightly so it holds its bowl shape.",
        ],
        tips=[
            "The increases are spread evenly, which is what keeps the sides smooth.",
            "A firm cotton yarn gives the best shape.",
        ],
    ),
    # ------------------------------------------------------------------ 07
    dict(
        slug="mini-amigurumi-ball",
        number="07",
        title="Mini Amigurumi Ball",
        tagline="A little ball for tiny projects.",
        source="examples/mini_sphere.txt",
        difficulty="Beginner",
        time="1\u20132 hours",
        overview=(
            "A small sphere worked in continuous rounds. Use it as a toy, a "
            "button-style detail, a doll\u2019s ball, or the body of a tiny creature."
        ),
        materials=[
            ("Yarn", "Worsted weight or DK, about 40 g in one colour"),
            ("Hook", "4.0 mm (or 3.5 mm for DK)"),
            ("Also", "Yarn needle, a little polyester stuffing"),
        ],
        finished_size="About 5\u20136 cm (2\u20132.5 in) across",
        gauge="Work tightly \u2014 the ball is small, so gaps show easily.",
        abbreviations=["MR", "sc", "inc", "dec", "st(s)"],
        notes=[
            "Worked in continuous rounds \u2014 there is no turning.",
            "Keep a stitch marker in the first stitch of each round.",
        ],
        finishing=[
            "Stuff the ball while you close it, so it stays round.",
            "Pull the tail through the last 6 stitches and pull tight.",
            "Sew the top closed and weave in all ends.",
        ],
        tips=[
            "A pencil or a small stitch holder helps you stuff as you close.",
            "Check your count at the end of every round.",
        ],
    ),
    # ------------------------------------------------------------------ 08
    dict(
        slug="beginner-scarf",
        number="08",
        title="Beginner Scarf",
        tagline="Your first scarf \u2014 just chains and single crochet.",
        source="examples/scarf.txt",
        difficulty="Beginner",
        time="2\u20134 hours",
        overview=(
            "This scarf uses only chains and single crochet. Work the first "
            "row once, then repeat rows 2\u20135 until your scarf is as long "
            "as you want it to be."
        ),
        materials=[
            ("Yarn", "Worsted weight (medium, category 5), about 200\u2013400 g depending on the length you want"),
            ("Hook", "4.0 mm"),
            ("Also", "Yarn needle"),
        ],
        finished_size="About 11 cm (4.5 in) wide \u2014 length is up to you",
        gauge="10 sc \u00d7 5 rows = 6 \u00d7 6 cm (2.5 \u00d7 2.5 in) in single crochet",
        abbreviations=["ch", "sc", "st(s)"],
        notes=[
            "Worked in rows \u2014 you will turn at the end of every row.",
            "The chain at the start of a row only lifts your work. It does not count as a stitch.",
        ],
        finishing=[
            "Fasten off and weave in the ends.",
            "Optional: add fringe to both short ends.",
        ],
        tips=[
            "Count your stitches after the first row \u2014 you should have 19.",
            "Even tension gives the neatest edge.",
        ],
    ),
    # ------------------------------------------------------------------ 09
    dict(
        slug="everyday-beanie",
        number="09",
        title="Everyday Beanie",
        tagline="A cozy beanie with a soft crown.",
        source="examples/simple_hat.txt",
        difficulty="Beginner",
        time="4\u20136 hours",
        overview=(
            "A classic beanie worked from the brim up in continuous rounds. "
            "The crown closes with gentle, even decreases, so it sits flat "
            "on the head with no point."
        ),
        materials=[
            ("Yarn", "Worsted weight (medium, category 5), about 150 g in one colour"),
            ("Hook", "4.0 mm"),
            ("Also", "Yarn needle"),
        ],
        finished_size="Fits a 35\u201338 cm (14\u201315 in) head, crown depth about 16 cm (6.5 in)",
        gauge="Work loosely for a slouchy fit, more firmly for a snug fit.",
        abbreviations=["MR", "sc", "inc", "dec", "st(s)"],
        notes=[
            "Worked in continuous rounds \u2014 there is no turning.",
            "Keep a stitch marker in the first stitch of each round.",
        ],
        finishing=[
            "Fasten off, leaving a long tail.",
            "Pull the tail through the last 6 stitches and pull tight.",
            "Sew the top closed and weave in all ends.",
            "Fold up the brim if you like.",
        ],
        tips=[
            "Try the hat on as you work the straight rounds \u2014 stop when it fits.",
            "Work the decreases evenly so the crown stays flat.",
        ],
    ),
    # ------------------------------------------------------------------ 10
    dict(
        slug="simple-round-cowl",
        number="10",
        title="Simple Round Cowl",
        tagline="A quick neck warmer in 12 rounds.",
        source="examples/tube_cowl.txt",
        difficulty="Beginner",
        time="1\u20132 hours",
        overview=(
            "A simple round cowl with no shaping at all. Join a chain into a "
            "ring, then work even single crochet rounds around and around."
        ),
        materials=[
            ("Yarn", "Worsted weight (medium, category 5), about 100 g in one colour"),
            ("Hook", "4.0 mm"),
            ("Also", "Yarn needle"),
        ],
        finished_size="About 24 cm (9.5 in) around, about 7 cm (3 in) tall",
        gauge="Work evenly so the tube stays the same width all the way round.",
        abbreviations=["ch", "sl st", "sc", "st(s)"],
        notes=[
            "Worked in continuous rounds \u2014 there is no turning.",
            "Keep a stitch marker in the first stitch of each round.",
        ],
        finishing=[
            "Fasten off and weave in the ends.",
            "The cowl can be worn straight, folded, or twisted.",
        ],
        tips=[
            "Try it on around round 8 \u2014 stop early if it is too tight for your neck.",
            "A soft wool blend makes the cosiest cowl.",
        ],
    ),
]


def get(slug):
    for p in PATTERNS:
        if p["slug"] == slug:
            return p
    raise KeyError(slug)
