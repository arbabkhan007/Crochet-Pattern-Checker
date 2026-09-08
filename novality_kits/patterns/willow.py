"""Willow the Bunny Lovey - Novality NS 10. Corrections applied: missing head rounds R3/R5/R10 and ear rounds R3/R10
reconstructed and verified; blanket diagonal corrected to ~43 cm (26 cm square x 1.41); granny corners specified.
All counts verified."""

P = dict(
    slug="willow", title="Willow the Bunny Lovey", design_code="NS 10", terms="US terms", skill="Advanced beginner", time="2 - 3 hours",
    hashtag="#WillowTheBunnyLovey", subtitle="A bunny comforter crochet pattern",
    tagline=["A bunny comforter: a soft, firmly stuffed head above a light, drapey granny-square blanket.",
             "Long floppy ears to hold, an embroidered face with no small parts, and a blanket that grows evenly from the centre out."],
    intro=("A bunny comforter: a soft, firmly stuffed head above a light, drapey granny-square blanket. Long floppy ears to hold, an embroidered face with no small parts, "
           "and a blanket that grows evenly from the centre out."),
    size_chip="26 cm / 10 in blanket",
    stats=[("26 cm", "BLANKET, SQUARE"), ("4.9 cm", "HEAD, ACROSS"), ("20", "GRANNY ROUNDS"), ("0", "SMALL PARTS")],
    feats=[("20", "granny rounds,\n+12 dc each"), ("240", "dc around the\nfinished edge"), ("36", "stitches around\nthe head"), ("2", "seams - and the\nbase sewn twice")],
    palette=dict(accent="#A8C4B0", deep="#4F7A5E", pale="#EEF4EF", rule="#D6E3D9", hilite="#DEEBE1"),
    materials=[
        ("Yarn", "DK (#3) 100% cotton (or a baby-safe certified blend), about 60 g - cream, sage, dusty pink or pale grey. Only the head is stuffed."),
        ("Hook", "3.5 mm (US E/4) for the blanket; use 3.0 mm for the head if your tension is loose."),
        ("Eyes / floss", "None - the face is embroidered in dark brown or charcoal cotton floss, ends knotted inside."),
        ("Also", "About 8 g fibre fill, tapestry needle, stitch marker."),
    ],
    gauge=("About 4.5 mm per stitch and 4.3 mm per round on the head. Check on the blanket after Rnd 3: 9 dc along an edge should measure about 39 mm; narrower and the blanket comes out small. "
           "The square grows about 1.3 cm per side per round: 18 rounds = 23 cm, 20 rounds = 26 cm, 22 rounds = 28 cm."),
    abbreviations=[("MR", "magic ring"), ("ch", "chain"), ("sc", "single crochet"), ("dc", "double crochet"), ("inc", "2 sc in one st"), ("dec", "invisible decrease"),
                   ("sl st", "slip stitch"), ("sp", "space"), ("FO", "fasten off"), ("(n)", "stitch count")],
    techniques=[
        ("Magic ring & spiral", "The head and each ear begin with a magic ring and are worked in a continuous spiral (no joins, marker in the first stitch); pull the tail tight after round one."),
        ("Joined rounds", "The BLANKET is worked in JOINED rounds: each round closes with a slip stitch and the next begins with a ch 3 (counting as the first dc) - a different rhythm that lets the square grow out evenly."),
        ("The granny-square corner", "Every blanket corner is (3 dc, ch 2, 3 dc) into one corner space. Those four corners make the piece square instead of round. Miss one corner group and the whole square pulls out of true - check all four at the end of every round."),
        ("The border round", "One final round of single crochet around the edge with 3 sc into each corner space squares the edge and stops the blanket curling. Do not skip it."),
    ],
    sections=[
        dict(id="head", title="3 · Head", image="hero", caption="A 36-stitch sphere with three straight rounds for the face; the ears are long, flat and floppy.",
             lead="A 36-stitch sphere with three straight rounds for the face. The finished head is about 4.9 cm across and 5.3 cm tall.",
             tables=[dict(heading="Head · R1 - R14", rounds=[
                         ("R1", "6 sc in MR", 6, ""), ("R2", "inc in each st around", 12, ""), ("R3", "[1 sc, inc] x 6", 18, ""), ("R4", "[2 sc, inc] x 6", 24, ""),
                         ("R5", "[3 sc, inc] x 6", 30, ""), ("R6", "[4 sc, inc] x 6", 36, "full width"), ("R7", "sc in each st around", 36, ""),
                         ("R8", "sc in each st around", 36, "face on R8 - R9"), ("R9", "sc in each st around", 36, ""), ("R10", "[4 sc, dec] x 6", 30, ""),
                         ("R11", "[3 sc, dec] x 6", 24, "stuff firmly"), ("R12", "[2 sc, dec] x 6", 18, ""), ("R13", "[1 sc, dec] x 6", 12, "top up stuffing"),
                         ("R14", "dec x 6", 6, "close")],
                         finish="FO and close with the tail. Stuff FIRMLY - a soft head collapses when gripped and the face distorts."),
                     dict(heading="Ear · make 2 · long and floppy, do not stuff", rounds=[
                         ("R1", "6 sc in MR", 6, ""), ("R2", "[1 sc, inc] x 3", 9, ""), ("R3", "[2 sc, inc] x 3", 12, ""), ("R4-8", "sc in each st around (5 rnds)", 12, ""),
                         ("R9", "[2 sc, dec] x 3", 9, ""), ("R10", "sc in each st around", 9, ""), ("R11", "[1 sc, dec] x 3", 6, "flatten, FO")],
                         finish="Flatten and FO with a long tail. Sew to Rnds 4-6 of the head, about 10 stitches apart, pinching each base so it flops forward.")],
             steps=["Face - with dark brown floss: two small sleeping arcs on R8-R9, 6 stitches apart, and a small Y-shaped nose and mouth centred one round below. Knot every end inside the head before closing R14.",
                    "Cheeks - two small pink stitches, or leave plain for a very calm face."]),
        dict(id="blanket", title="4 · Granny-square blanket", image="inhand", caption="Each round adds one 3-dc group to every side and one to each corner: +12 dc per round.",
             lead="Worked in joined rounds from a chain ring. Every round adds one 3-dc group to every side.",
             tables=[dict(heading="Total dc per round", rounds=[
                 ("R3", "36 dc", 36, ""), ("R5", "60 dc", 60, ""), ("R10", "120 dc", 120, ""), ("R15", "180 dc", 180, ""), ("R20", "240 dc", 240, "60 dc per edge + 26 cm square")])],
             steps=["Ch 4 and sl st to the first ch to form a ring.",
                    "Rnd 1: ch 3 (counts as first dc), 2 dc in the ring, [ch 2, 3 dc in the ring] x 3, ch 2, sl st to the ch-3 top. [12 dc, 4 corner spaces]",
                    "Rnd 2: sl st into the next corner space; ch 3, 2 dc in that space, ch 2, 3 dc in the same space (first corner); then (3 dc, ch 2, 3 dc) into each remaining corner space; sl st to close. [24 dc]",
                    "Rnds 3-20: into every corner space work (3 dc, ch 2, 3 dc), and into every space along a side work 3 dc. Each round adds one 3-dc group to every side (+12 dc per round).",
                    "Border: work one final round of sc all the way around - 1 sc into each dc and 3 sc into each corner space - then sl st and FO. Rnd 20 has 240 dc: 4 corners x 3 sc + 240 sc = 252 sc. This firms the edge and stops the square curling.",
                    "Size check: about 1.3 cm per side per round. 20 rounds gives a 26 cm square; the diagonal corner to corner is about 37 cm before the border and about 43 cm with it stretched flat - a good size to hold and drag.",
                    "Fewer rounds for a smaller lovey (18 rounds = 23 cm) or more for a larger one (22 rounds = 28 cm) - the counts simply continue by +12 per round."],
             panels=[("Counting a granny round", "Rnd n has 12 x n dc. If you are unsure which round you are on, count the 3-dc groups along one side: on Rnd n there are n groups on each side including the two corner halves.", "tip")]),
    ],
    assembly=[
        ("Ears", "Sew the flattened base of each ear to Rnds 4-6 of the head, about 10 stitches apart. Pinch the base so the ear folds forward and flops. Sew round twice."),
        ("Head to blanket", "Place the head at the CENTRE of the blanket (over the ch-4 ring), face toward one corner. Sew the head's closed base (R12-R14) to the centre 3-dc groups with a doubled strand, going round twice - this is the seam a baby drags the lovey by."),
        ("Face", "Sleeping arcs on R8-R9, 6 apart, Y nose below. Everything embroidered; no safety eyes or buttons on a comforter."),
        ("Ends", "Every floss end knotted inside the head; every yarn end woven in at least 5 cm and trimmed."),
        ("Wash test", "Cotton loveys are washed a lot: wash once before gifting and check the head seam and ears afterwards."),
    ],
    checklist=["1 head (closed, firmly stuffed)", "2 ears (flat)", "1 granny square, 20 rounds + border", "face embroidered, ends knotted inside"],
    troubleshooting=[
        ("The blanket is round, not square.", "You are missing corner groups. Every corner must be (3 dc, ch 2, 3 dc) into the ch-2 space, all four, every round. Count corners before you join each round."),
        ("The edge ripples or curls.", "Ripples: too many groups on a side - each round adds exactly one per side. Curls: you skipped the sc border round, or worked it too tight - 3 sc in each corner space."),
    ],
    colorways=[("Cream", "#F1E9DA", "#8B6A4E"), ("Sage", "#A8C4B0", "#F1E9DA"), ("Dusty pink", "#E4B8BE", "#F1E9DA"), ("Pale grey", "#CFCBC6", "#F1E9DA"), ("Butter yellow", "#F3DFA0", "#F1E9DA")],
    colorways_caption="Left to right: cream, sage, dusty pink, pale grey, butter yellow. One colour throughout is calmest; a contrast border round is the easiest way to add a second.",
    terms_may=("Make as many finished loveys as you like for yourself, gifts, or charity. Sell physical finished items made from this pattern in small batches, "
               "in shops, markets and online, provided credit is given to \"Novality Crochet Studio\"."),
    thanks="Tag your makes with #NovalityCrochetStudio and #WillowTheBunnyLovey - we love seeing your bunnies. Thank you for supporting an independent pattern designer.",
    images={"hero": "hero.png", "inhand": "inhand.png", "detail": "detail.png", "colorways": "colorways.png"},
    image_prompts={
        "hero": "Product photograph of a handmade crocheted bunny lovey comforter, a small round cream cotton bunny head with long floppy ears and an embroidered face sewn onto the centre of a light open granny-square blanket in cream DK cotton, blanket draped softly, on a soft cream linen surface, pastel backdrop, soft natural window light, shallow depth of field, clean etsy product photo",
        "inhand": "A handmade crocheted cream cotton bunny lovey comforter held up by one ear in an adult hand so the granny-square blanket hangs down, showing its size of about twenty-six centimetres, soft cream background, natural light, shallow depth of field, product photo",
        "detail": "Close-up macro photograph of a handmade crocheted cream cotton bunny lovey head showing the embroidered sleeping-eye arcs and small Y nose in brown floss, two long flat floppy ears, and the open granny-square double crochet clusters of the blanket beneath, soft light, shallow depth of field",
        "colorways": "Five handmade crocheted bunny lovey comforters laid out in a row, identical design of a small bunny head on a granny-square blanket, in cream, sage green, dusty pink, pale grey and butter yellow cotton yarn, on a cream linen surface, soft natural light, product photo",
    },
)
