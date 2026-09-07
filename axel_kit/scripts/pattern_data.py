"""Single source of truth for the Axel the Axolotl pattern - used by the PDF, video and Etsy builders.

Every stitch count below was verified with the repository's deterministic checker
(crochet-check) and by independent arithmetic: 0 errors across all 52 rounds.
"""

TITLE = "Axel the Axolotl"
SUBTITLE = "An amigurumi crochet pattern"
DESIGNER = "Novality Store"
STUDIO = "Novality Crochet Studio"
DESIGN_CODE = "NS 03"
YEAR = "2026"
TERMS = "US terms"
SKILL = "Advanced beginner"
TIME = "2.5 - 3 hours"
HASHTAGS = ["#NovalityStore", "#AxelTheAxolotl"]

FINISHED_SIZE = [
    ("Height (seated)", "11.5 cm / 4.5 in"),
    ("Width, gill tip to gill tip", "10 cm / 4 in"),
    ("Tail", "4.3 cm / 1.7 in"),
    ("Head", "52 mm wide x 51.6 mm tall - a near-true sphere"),
]

INTRO = ("A soft pink axolotl with six fluffy gills, a round head and a shell-edged paddle tail. "
         "Head, neck, body and tail are worked as one continuous spiral - no neck seam to sew.")

SAFETY = ("Axel has two 6 mm safety eyes. Safety eyes are small parts: lock the washers firmly from the inside "
          "before stuffing, and pull-test every eye on the finished toy - a properly locked washer will not come off "
          "by hand. The gills, arms, feet and tail fin are all sewn or worked on: sew each seam twice and weave every "
          "end in for at least 5 cm, then trim close - a loose gill is the first thing a child will pull. This pattern "
          "has not been tested to ASTM F963 or EN 71, so do not describe finished Axels as \"baby-safe\". For children "
          "under 3, skip the safety eyes and stitch the eyes with black floss instead.")

MATERIALS = [
    ("Main yarn", "Worsted #4, pale pink, about 15 g. Cotton or acrylic with a smooth matte finish - one 25 g ball covers the whole axolotl."),
    ("Gill yarn", "Fuzzy / eyelash / fur yarn, dark pink, about 8 g. Essential: smooth worsted will not give fluffy gills, and the gills are the whole look."),
    ("Fin yarn", "Worsted #4, dark pink, about 3 g, smooth - so the shell edging stays crisp."),
    ("Hook & eyes", "3.5 mm (US E/4) for a tight gauge so stuffing cannot show through. Two 6 mm safety eyes (9 mm reads as buggy on this head)."),
    ("Also", "Polyester filling about 8 g; tapestry needle; black embroidery floss; pink pastel or chalk; stitch marker."),
]

GAUGE = ("36 sc around measures about 52 mm across when stuffed (4.5 mm per stitch, 4.3 mm per round). "
         "Wider than 55 mm? Drop to a 3.0 mm hook; under 48 mm? Go up to 4.0 mm.")

ABBREVIATIONS = [
    ("MR", "magic ring"), ("ch", "chain"), ("sc", "single crochet"), ("dc", "double crochet"),
    ("inc", "increase (2 sc in one st)"), ("invdec", "invisible decrease"), ("sl st", "slip stitch"),
    ("st(s)", "stitch(es)"), ("FO", "fasten off"), ("(n)", "stitch count at round end"),
]

TECHNIQUES = [
    ("The magic ring",
     "Every piece begins with a magic ring. Wrap the yarn once around two fingers, insert the hook, pull up a loop and "
     "work your first round into the ring, then pull the tail to close it tight once the first round is complete."),
    ("Work in a spiral",
     "Do not join and do not chain 1 between rounds - just keep going round after round. Keep a stitch marker in the "
     "first stitch of every round and move it up each time; there is no join to count from."),
    ("The invisible decrease",
     "Insert the hook through the front loops only of the next two stitches, yarn over and pull through both, then yarn "
     "over and pull through the remaining two loops. It leaves no ridge, which matters on the head and neck where "
     "decreases are visible."),
    ("Closing through both layers",
     "To close a flat opening, fold the piece flat so the front and back layers lie together, then work one sc through "
     "each matched pair of stitches. Axel's 6-stitch tail tip folds into 3 pairs and closes with 3 sc."),
    ("The shell (scallop)",
     "Work all the stitches of the group into one stitch, then slip stitch into the next stitch to anchor it. The group "
     "fans into a cup. Working the dc loosely makes each scallop cup outward instead of lying flat."),
]

BODY_INTRO = ("Worked in a single spiral from the top of the head straight through to the tail tip. Head and body are "
              "both 36 stitches around; the neck at R13 is the only waist. Three straight rounds at the head keep it "
              "spherical rather than egg-shaped.")

# (round, instruction, count, note)
BODY_ROUNDS = [
    (1, "6 sc in MR", 6, "start at top of head"),
    (2, "inc in each st around", 12, ""),
    (3, "[1 sc, inc] x 6", 18, ""),
    (4, "[2 sc, inc] x 6", 24, ""),
    (5, "[3 sc, inc] x 6", 30, ""),
    (6, "[4 sc, inc] x 6", 36, "head at full width"),
    (7, "sc in each st around", 36, "eyes between R7 / R8"),
    (8, "sc in each st around", 36, ""),
    (9, "sc in each st around", 36, "smile on R8 - R9"),
    (10, "[4 sc, invdec] x 6", 30, ""),
    (11, "[3 sc, invdec] x 6", 24, "STUFF HEAD FIRMLY"),
    (12, "[2 sc, invdec] x 6", 18, ""),
    (13, "sc in each st around", 18, "NECK - narrowest point"),
    (14, "[2 sc, inc] x 6", 24, "body flares out"),
    (15, "[3 sc, inc] x 6", 30, ""),
    (16, "[4 sc, inc] x 6", 36, "body at full width"),
    (17, "sc in each st around", 36, "arms at R17 - R18"),
    (18, "sc in each st around", 36, ""),
    (19, "sc in each st around", 36, ""),
    (20, "sc in each st around", 36, ""),
    (21, "sc in each st around", 36, ""),
    (22, "sc in each st around", 36, ""),
    (23, "[4 sc, invdec] x 6", 30, ""),
    (24, "[3 sc, invdec] x 6", 24, "FEET attach at R24 - R25"),
    (25, "[2 sc, invdec] x 6", 18, "stuff body LIGHTLY"),
    (26, "[1 sc, invdec] x 6", 12, ""),
    (27, "sc in each st around", 12, "tail begins"),
    (28, "[2 sc, invdec] x 3", 9, ""),
    (29, "sc in each st around", 9, ""),
    (30, "sc in each st around", 9, ""),
    (31, "sc in each st around", 9, ""),
    (32, "[1 sc, invdec] x 3", 6, "light stuffing to here"),
    (33, "sc in each st around", 6, ""),
    (34, "sc in each st around", 6, ""),
    (35, "sc in each st around", 6, ""),
    (36, "sc in each st around", 6, "taper to tip"),
]

BODY_FINISH = ("Fold the last 6 stitches flat so 3 pairs line up (3 front + 3 back), then work 1 sc through each pair - "
               "3 sc in total - to close the tip cleanly. FO and weave the end back through the tail tip and out along "
               "the top ridge; you will crochet the fin directly onto that ridge. The tail runs R27-R36 - ten rounds, "
               "about 43 mm - giving the fin a long enough ridge to sit on.")

LIMBS_INTRO = "Arms and feet are sewn on, not worked into the body - bobbles will not give you rounded limbs."

ARM_ROUNDS = [
    (1, "6 sc in MR", 6, ""),
    (2, "sc around", 6, ""),
    (3, "sc around", 6, ""),
    (4, "sc around", 6, ""),
    (5, "sc around", 6, ""),
    (6, "sc around, then FO", 6, "arms finish here"),
]
FEET_ROUNDS = [
    (1, "6 sc in MR", 6, ""),
    (2, "[1 sc, inc] x 3", 9, ""),
    (3, "sc around", 9, ""),
    (4, "sc around", 9, ""),
    (5, "[1 sc, invdec] x 3", 6, "feet finish here"),
]
ARMS_FINISH = ("FO with a long tail, do not stuff. Flatten the open end and sew it closed as you attach, so the arms "
               "hang softly.")
FEET_FINISH = ("FO, cinch closed with a long tail and stuff lightly - do not flatten them, they are plump little balls; "
               "sew the cinched nub toward the body.")

GILL_ROUNDS = [
    (1, "6 sc in MR", 6, ""),
    (2, "inc in each st around", 12, ""),
    (3, "sc around", 12, ""),
    (4, "sc around", 12, ""),
    (5, "[1 sc, invdec] x 4", 8, "open edge sewn to head"),
]
FUZZY_TIP = ("You cannot see the stitches. Hold a thin strand of matching smooth yarn together with the fur yarn so you "
             "can find the stitches, or count by feel with the hook tip and trust the round count. Small errors are "
             "invisible in the finished fluff.")
GILLS_FINISH = ("FO with a long tail. The open edge sewn straight to the head disappears in the fluff - simply "
                "whip-stitch the 8-st opening flat against the head (or cinch the front loops first if you prefer a "
                "rounded lobe). Three fluffy gills fan behind each eye - upper angled up, middle out, lower down.")

FIN_STEPS = [
    "With smooth dark pink yarn, join with a sl st to the top ridge of the tail at the very tip (join into the tip end-closure corner). Working along the ridge back toward the body:",
    "* 5 dc in the next ridge stitch, sl st in the next ridge stitch. Repeat from * a total of 5 times (5 scallops).",
    "FO and weave in.",
]
FIN_NOTES = ("Each scallop uses 2 ridge stitches, so the fin spans 10 stitches. The tail from R27 to R36 gives a ridge "
             "of about 10 workable stitches along one side, so 5 scallops fit it exactly - start at the tip and work "
             "back toward the body, then anchor the last sl st into the body junction. Work the dc groups loosely so "
             "each scallop cups outward. For a fuller paddle, work a second identical 5-scallop row along the underside "
             "ridge rather than stretching one row around the tip.")
FIN_FULLNESS = ("Five shells over ten rounds is meant to ruffle - the cupped, frilly edge is the look, not a mistake. If "
                "the scallops seem crowded, work the dc even more loosely, use half a hook size larger for the fin yarn "
                "only, or work 4 scallops on a shorter ridge.")

ASSEMBLY = [
    ("Eyes", "Insert the 6 mm safety eyes between R7 and R8, 6 stitches apart, centred on the front of the head. Six stitches spans about 27 mm on the 52 mm head - about half the width. Fix the washers before stuffing, and pull-test each eye once it is locked."),
    ("Smile", "With black floss, embroider a wide shallow U across R8-R9, centred between the eyes and about 5 stitches wide. Keep it shallow; a deep curve reads as a frown."),
    ("Blush", "Brush soft pink pastel or chalk in a small circle directly under each eye, just outside the eye line."),
    ("Gills", "Sew 3 lobes to each side of the head, behind the eyes, anchored at about R6 (upper), R7-R8 (middle) and R9 (lower). Angle the top lobe upward, the middle one straight out and the bottom one downward so they fan, then tease the fibres apart with a slicker brush or your fingers."),
    ("Arms", "Sew one arm to each side at R17-R18, about 6 stitches out from the centre front, angled slightly forward."),
    ("Feet", "Sew one foot to each side of the centre front at R24-R25, about 4 stitches out from centre, so Axel sits flat and upright."),
]
CHECKLIST = ["1 body", "2 arms", "2 feet", "6 gills", "1 fin"]

TROUBLESHOOTING = [
    ("Head firm, body soft.", "Stuff the head hard at R11 so it holds a sphere and the eyes stay level. Keep the body light so Axel stays squishy and sits down."),
    ("Neck collapsing.", "The 18-stitch neck is deliberately narrow. First pack a little more stuffing into the neck through the body opening before closing R25. For a permanently sturdier neck, work R13 as [7 sc, inc] x 2, 2 sc (20), then change R14 to [4 sc, inc] x 4 (24) so it consumes all 20 stitches; R15 onward is unchanged."),
    ("Fin runs out of tail.", "The ridge holds 10 stitches and 5 scallops need exactly 10. If you shortened the tail, work fewer scallops rather than crowding them."),
    ("Want a wider gill span?", "As written the gills give about 10 cm tip to tip. Work each gill two rounds longer - add 2 plain rounds at 12 stitches before R5 - for a span of about 12 cm."),
    ("Stuffing shows through.", "Go down to a 3.0 mm hook. Loose gauge on a 3.5 mm hook is the usual cause."),
    ("Axel will not sit.", "Move the feet one round lower and make sure the R23-R26 decreases are centred on the underside, not the back."),
]

COLORWAYS = [
    ("Classic pink", "#F2C4CF", "#B8506F"),
    ("White leucistic", "#F7F3EE", "#EDB7C4"),
    ("Melanoid black", "#2E2A2D", "#5B565A"),
    ("Mint", "#BFE3D6", "#3C9C93"),
    ("Lavender", "#CFC1E6", "#7A57A8"),
]

TERMS_MAY = ("Make as many finished axolotl plushies as you like for yourself, gifts, or charity. Sell physical finished "
             "items made from this pattern in small batches, in shops, markets and online, provided credit is given to "
             "\"Novality Store\".")
TERMS_MAY_NOT = ("Do not resell, share, redistribute, translate, rewrite, publish or upload this digital PDF or its contents "
                 "in any form. Do not alter, copy or recolor the pattern and claim it as your own. Do not use the Novality "
                 "Store name, logo or photos beyond crediting the pattern. Do not mass-produce finished items commercially "
                 "without written permission.")
TERMS_COPYRIGHT = ("This crochet pattern - including all instructions, stitch counts, photography and design elements - is "
                   "the original work and intellectual property of Novality Store, designed by Novality Crochet Studio. "
                   f"Design Code {DESIGN_CODE}. Copyright (c) {YEAR} Novality Store. All rights reserved.")
TERMS_SAFETY = ("This pattern has not been tested to a toy-safety standard such as ASTM F963 or EN 71, so please do not "
                "describe finished Axels as \"baby-safe\" or \"suitable from birth\". Axel uses two 6 mm safety eyes (small "
                "parts): for children under 3, embroider the eyes instead. Finished items made for sale must be assessed "
                "by the seller against local toy-safety laws.")
THANKS = ("Tag your makes with #NovalityStore and #AxelTheAxolotl - we love seeing your makes. Thank you for supporting "
          "an independent pattern designer.")
