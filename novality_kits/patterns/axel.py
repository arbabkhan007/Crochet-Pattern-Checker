"""Axel the Axolotl - Novality NS 03. Ported unchanged from axel_kit/scripts/pattern_data.py (52 rounds, PASS);
rebranded to Novality Crochet Studio, safety block removed per studio decision."""

P = dict(
    slug="axel", title="Axel the Axolotl", design_code="NS 03", terms="US terms", skill="Advanced beginner", time="2.5 - 3 hours",
    hashtag="#AxelTheAxolotl", subtitle="An amigurumi crochet pattern",
    tagline=["A soft pink axolotl with six fluffy gills, a round head and a shell-edged paddle tail.",
             "Head, neck, body and tail are one continuous spiral - no neck seam to sew, ever."],
    intro=("A soft pink axolotl with six fluffy gills, a round head and a shell-edged paddle tail. "
           "Head, neck, body and tail are worked as one continuous spiral - no neck seam to sew."),
    size_chip="11.5 cm / 4.5 in tall",
    stats=[("11.5 cm", "TALL, SEATED"), ("10 cm", "GILL TIP TO TIP"), ("4.3 cm", "TAIL"), ("52 mm", "HEAD SPHERE")],
    feats=[("36", "stitches around\nhead and body"), ("52", "rounds across all\npieces, count-checked"), ("6", "fluffy gills,\n3 per side"), ("5", "dc scallops on\nthe tail fin")],
    palette=dict(accent="#E8A9B8", deep="#B8506F", pale="#FBEEF1", rule="#EBD7DD", hilite="#F7DCE3"),
    materials=[
        ("Main yarn", "Worsted #4, pale pink, about 15 g. Cotton or acrylic with a smooth matte finish - one 25 g ball covers the whole axolotl."),
        ("Gill yarn", "Fuzzy / eyelash / fur yarn, dark pink, about 8 g. Essential: smooth worsted will not give fluffy gills, and the gills are the whole look."),
        ("Fin yarn", "Worsted #4, dark pink, about 3 g, smooth - so the shell edging stays crisp."),
        ("Hook & eyes", "3.5 mm (US E/4) for a tight gauge so stuffing cannot show through. Two 6 mm safety eyes (9 mm reads as buggy on this head)."),
        ("Also", "Polyester filling about 8 g; tapestry needle; black embroidery floss; pink pastel or chalk; stitch marker."),
    ],
    gauge=("36 sc around measures about 52 mm across when stuffed (4.5 mm per stitch, 4.3 mm per round). "
           "Wider than 55 mm? Drop to a 3.0 mm hook; under 48 mm? Go up to 4.0 mm."),
    abbreviations=[("MR", "magic ring"), ("ch", "chain"), ("sc", "single crochet"), ("dc", "double crochet"), ("inc", "increase (2 sc in one st)"),
                   ("invdec", "invisible decrease"), ("sl st", "slip stitch"), ("st(s)", "stitch(es)"), ("FO", "fasten off"), ("(n)", "stitch count at round end")],
    techniques=[
        ("The magic ring", "Every piece begins with a magic ring. Wrap the yarn once around two fingers, insert the hook, pull up a loop and work your first round into the ring, then pull the tail to close it tight once the first round is complete."),
        ("Work in a spiral", "Do not join and do not chain 1 between rounds - just keep going round after round. Keep a stitch marker in the first stitch of every round and move it up each time; there is no join to count from."),
        ("The invisible decrease", "Insert the hook through the front loops only of the next two stitches, yarn over and pull through both, then yarn over and pull through the remaining two loops. It leaves no ridge, which matters on the head and neck where decreases are visible."),
        ("Closing through both layers", "To close a flat opening, fold the piece flat so the front and back layers lie together, then work one sc through each matched pair of stitches. Axel's 6-stitch tail tip folds into 3 pairs and closes with 3 sc."),
        ("The shell (scallop)", "Work all the stitches of the group into one stitch, then slip stitch into the next stitch to anchor it. The group fans into a cup. Working the dc loosely makes each scallop cup outward instead of lying flat."),
    ],
    sections=[
        dict(id="body", title="3 · Body - one spiral, head to tail", image="inhand", caption="Head and body are both 36 stitches around; the neck at R13 is the only waist.",
             lead=("Worked in a single spiral from the top of the head straight through to the tail tip. Head and body are both 36 stitches around; "
                   "the neck at R13 is the only waist. Three straight rounds at the head keep it spherical rather than egg-shaped."),
             tables=[
                 dict(heading="Head & neck · R1 - R13", rounds=[
                     ("R1", "6 sc in MR", 6, "start at top of head"), ("R2", "inc in each st around", 12, ""), ("R3", "[1 sc, inc] x 6", 18, ""),
                     ("R4", "[2 sc, inc] x 6", 24, ""), ("R5", "[3 sc, inc] x 6", 30, ""), ("R6", "[4 sc, inc] x 6", 36, "head at full width"),
                     ("R7", "sc in each st around", 36, "eyes between R7 / R8"), ("R8", "sc in each st around", 36, ""), ("R9", "sc in each st around", 36, "smile on R8 - R9"),
                     ("R10", "[4 sc, invdec] x 6", 30, ""), ("R11", "[3 sc, invdec] x 6", 24, "STUFF HEAD FIRMLY"), ("R12", "[2 sc, invdec] x 6", 18, ""),
                     ("R13", "sc in each st around", 18, "NECK - narrowest point")],
                      finish="Insert the safety eyes between R7 and R8 (6 stitches apart), embroider the smile across R8-R9, then stuff the head firmly at R11 - it must hold a sphere so the eyes stay level."),
                 dict(heading="Body · R14 - R26", rounds=[
                     ("R14", "[2 sc, inc] x 6", 24, "body flares out"), ("R15", "[3 sc, inc] x 6", 30, ""), ("R16", "[4 sc, inc] x 6", 36, "body at full width"),
                     ("R17", "sc in each st around", 36, "arms at R17 - R18"), ("R18", "sc in each st around", 36, ""), ("R19", "sc in each st around", 36, ""),
                     ("R20", "sc in each st around", 36, ""), ("R21", "sc in each st around", 36, ""), ("R22", "sc in each st around", 36, ""),
                     ("R23", "[4 sc, invdec] x 6", 30, ""), ("R24", "[3 sc, invdec] x 6", 24, "FEET attach at R24 - R25"), ("R25", "[2 sc, invdec] x 6", 18, "stuff body LIGHTLY"),
                     ("R26", "[1 sc, invdec] x 6", 12, "")]),
                 dict(heading="Tail · R27 - R36", rounds=[
                     ("R27", "sc in each st around", 12, "tail begins"), ("R28", "[2 sc, invdec] x 3", 9, ""), ("R29", "sc in each st around", 9, ""),
                     ("R30", "sc in each st around", 9, ""), ("R31", "sc in each st around", 9, ""), ("R32", "[1 sc, invdec] x 3", 6, "light stuffing to here"),
                     ("R33", "sc in each st around", 6, ""), ("R34", "sc in each st around", 6, ""), ("R35", "sc in each st around", 6, ""), ("R36", "sc in each st around", 6, "taper to tip")],
                      finish=("Fold the last 6 stitches flat so 3 pairs line up (3 front + 3 back), then work 1 sc through each pair - 3 sc in total - to close the tip cleanly. "
                              "FO and weave the end back through the tail tip and out along the top ridge; you will crochet the fin directly onto that ridge. "
                              "The tail runs R27-R36 - ten rounds, about 43 mm - giving the fin a long enough ridge to sit on.")),
             ]),
        dict(id="limbs", title="4 · Arms, feet & gills", image="detail", caption="Three fluffy gills fan behind each eye - upper up, middle out, lower down.",
             lead="Arms and feet are sewn on, not worked into the body - bobbles will not give you rounded limbs. Gills are worked in fuzzy yarn and sewn to the head.",
             tables=[
                 dict(heading="Arm · make 2 · do not stuff", rounds=[
                     ("R1", "6 sc in MR", 6, ""), ("R2", "sc around", 6, ""), ("R3", "sc around", 6, ""), ("R4", "sc around", 6, ""), ("R5", "sc around", 6, ""),
                     ("R6", "sc around, then FO", 6, "arms finish here")],
                      finish="FO with a long tail, do not stuff. Flatten the open end and sew it closed as you attach, so the arms hang softly."),
                 dict(heading="Foot · make 2 · stuff lightly", rounds=[
                     ("R1", "6 sc in MR", 6, ""), ("R2", "[1 sc, inc] x 3", 9, ""), ("R3", "sc around", 9, ""), ("R4", "sc around", 9, ""), ("R5", "[1 sc, invdec] x 3", 6, "feet finish here")],
                      finish="FO, cinch closed with a long tail and stuff lightly - do not flatten them, they are plump little balls; sew the cinched nub toward the body."),
                 dict(heading="Gill · make 6 · fuzzy dark pink", rounds=[
                     ("R1", "6 sc in MR", 6, ""), ("R2", "inc in each st around", 12, ""), ("R3", "sc around", 12, ""), ("R4", "sc around", 12, ""),
                     ("R5", "[1 sc, invdec] x 4", 8, "open edge sewn to head")],
                      finish=("FO with a long tail. Whip-stitch the 8-st opening flat against the head (or cinch the front loops first if you prefer a rounded lobe). "
                              "Three fluffy gills fan behind each eye - upper angled up, middle out, lower down.")),
             ],
             panels=[("Working with fuzzy yarn", "You cannot see the stitches. Hold a thin strand of matching smooth yarn together with the fur yarn so you can find the stitches, or count by feel with the hook tip and trust the round count. Small errors are invisible in the finished fluff.", "tip")]),
        dict(id="fin", title="5 · Tail fin - shell edging", image="hero", caption="Five loose dc scallops along the top ridge of the tail.",
             lead="Worked directly onto the top ridge of the tail with the smooth dark pink yarn. Five scallops over ten ridge stitches.",
             steps=["With smooth dark pink yarn, join with a sl st to the top ridge of the tail at the very tip (join into the tip end-closure corner). Working along the ridge back toward the body:",
                    "* 5 dc in the next ridge stitch, sl st in the next ridge stitch. Repeat from * a total of 5 times (5 scallops).",
                    "FO and weave in.",
                    ("Each scallop uses 2 ridge stitches, so the fin spans 10 stitches. The tail from R27 to R36 gives a ridge of about 10 workable stitches along one side, so 5 scallops fit it exactly - "
                     "start at the tip and work back toward the body, then anchor the last sl st into the body junction. Work the dc groups loosely so each scallop cups outward. "
                     "For a fuller paddle, work a second identical 5-scallop row along the underside ridge rather than stretching one row around the tip.")],
             panels=[("Fin fullness", "Five shells over ten rounds is meant to ruffle - the cupped, frilly edge is the look, not a mistake. If the scallops seem crowded, work the dc even more loosely, use half a hook size larger for the fin yarn only, or work 4 scallops on a shorter ridge.", "tip")]),
    ],
    assembly=[
        ("Eyes", "Insert the 6 mm safety eyes between R7 and R8, 6 stitches apart, centred on the front of the head. Six stitches spans about 27 mm on the 52 mm head - about half the width. Fix the washers before stuffing, and pull-test each eye once it is locked."),
        ("Smile", "With black floss, embroider a wide shallow U across R8-R9, centred between the eyes and about 5 stitches wide. Keep it shallow; a deep curve reads as a frown."),
        ("Blush", "Brush soft pink pastel or chalk in a small circle directly under each eye, just outside the eye line."),
        ("Gills", "Sew 3 lobes to each side of the head, behind the eyes, anchored at about R6 (upper), R7-R8 (middle) and R9 (lower). Angle the top lobe upward, the middle one straight out and the bottom one downward so they fan, then tease the fibres apart with a slicker brush or your fingers."),
        ("Arms", "Sew one arm to each side at R17-R18, about 6 stitches out from the centre front, angled slightly forward."),
        ("Feet", "Sew one foot to each side of the centre front at R24-R25, about 4 stitches out from centre, so Axel sits flat and upright."),
    ],
    checklist=["1 body", "2 arms", "2 feet", "6 gills", "1 fin"],
    troubleshooting=[
        ("Head firm, body soft.", "Stuff the head hard at R11 so it holds a sphere and the eyes stay level. Keep the body light so Axel stays squishy and sits down."),
        ("Neck collapsing.", "The 18-stitch neck is deliberately narrow. First pack a little more stuffing into the neck through the body opening before closing R25. For a permanently sturdier neck, work R13 as [7 sc, inc] x 2, 2 sc (20), then change R14 to [4 sc, inc] x 4 (24) so it consumes all 20 stitches; R15 onward is unchanged."),
        ("Fin runs out of tail.", "The ridge holds 10 stitches and 5 scallops need exactly 10. If you shortened the tail, work fewer scallops rather than crowding them."),
        ("Want a wider gill span?", "As written the gills give about 10 cm tip to tip. Work each gill two rounds longer - add 2 plain rounds at 12 stitches before R5 - for a span of about 12 cm."),
        ("Stuffing shows through.", "Go down to a 3.0 mm hook. Loose gauge on a 3.5 mm hook is the usual cause."),
        ("Axel will not sit.", "Move the feet one round lower and make sure the R23-R26 decreases are centred on the underside, not the back."),
    ],
    colorways=[("Classic pink", "#F2C4CF", "#B8506F"), ("White leucistic", "#F7F3EE", "#EDB7C4"), ("Melanoid black", "#2E2A2D", "#5B565A"), ("Mint", "#BFE3D6", "#3C9C93"), ("Lavender", "#CFC1E6", "#7A57A8")],
    colorways_caption="Left to right: classic pink, white leucistic, melanoid black, mint, lavender. Swap the main and gill yarns - the counts never change.",
    terms_may=("Make as many finished axolotl plushies as you like for yourself, gifts, or charity. Sell physical finished items made from this pattern in small batches, "
               "in shops, markets and online, provided credit is given to \"Novality Crochet Studio\"."),
    thanks="Tag your makes with #NovalityCrochetStudio and #AxelTheAxolotl - we love seeing your makes. Thank you for supporting an independent pattern designer.",
    images={"hero": "hero.png", "inhand": "inhand.png", "detail": "detail.png", "colorways": "colorways.png"},
)
