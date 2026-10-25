"""Little Duck Plushie - Novality NS 05. Chenille one-piece duck; no safety eyes (embroidered). Stuffing call moved to R10
so the body is filled before the waist closes. All counts verified."""

P = dict(
    slug="duck", title="Little Duck Plushie", design_code="NS 05", terms="US terms", skill="Confident beginner", time="1.5 - 2 hours",
    hashtag="#LittleDuckPlushie",
    tagline=["A squashy chenille duck worked in ONE piece from tail to crown - the waist is the neck,",
             "so there is nothing to line up and only a beak and two wings to sew."],
    intro=("A squashy chenille duck worked in one continuous piece from the tail up to the crown. The body narrows to an 18-stitch waist that becomes the neck, "
           "then widens again for the head - so there is no head-to-body seam at all. A flat beak and two little wings are the only sewing."),
    size_chip="16 cm / 6.25 in tall",
    stats=[("16 cm", "TALL"), ("7.5 cm", "WIDE"), ("23", "ROUNDS, ONE PIECE"), ("0", "SAFETY EYES")],
    feats=[("1", "seamless piece,\ntail to crown"), ("30", "stitches around\nbody and head"), ("18", "stitch waist =\nthe neck"), ("3", "pieces to sew:\n2 wings, 1 beak")],
    palette=dict(accent="#F2CF6B", deep="#B58A1E", pale="#FCF6E4", rule="#EFE3C2", hilite="#F8ECC6"),
    materials=[
        ("Body yarn", "Chenille / velvet yarn, super bulky (#6), yellow, about 60 g. Chenille hides stitches and gives the squash."),
        ("Details", "Worsted #4 orange, a few metres, for the beak. Black embroidery floss for the eyes."),
        ("Hook", "5.0 mm (US H/8) for the chenille body; 3.5 mm for the worsted beak."),
        ("Stuffing & notions", "Polyester fibre filling about 40 g; a long yarn needle; stitch marker (essential - chenille hides the rounds)."),
    ],
    gauge=("30 sc around in chenille on a 5.0 mm hook measures about 75 mm across when stuffed (about 8 mm per stitch, 7 mm per round). "
           "Chenille is forgiving: if your duck comes out a little bigger or smaller it will still be a duck. Just keep the fabric tight enough that no stuffing shows."),
    abbreviations=[("MR", "magic ring"), ("ch", "chain"), ("sc", "single crochet"), ("inc", "increase (2 sc in one st)"), ("invdec", "invisible decrease"), ("sl st", "slip stitch"),
                   ("FO", "fasten off"), ("st(s)", "stitch(es)"), ("(n)", "stitch count at round end")],
    techniques=[
        ("Magic ring in chenille", "Chenille is slippery: wrap the ring twice round your finger and pull the tail firmly once R1 is done, then knot the tail inside before you go on. A chenille ring that opens later cannot be closed."),
        ("Spiral with a marker", "You cannot see chenille stitches, so the marker is your only count. Move it up every single round and count the stitches of each round as you work them."),
        ("Invisible decrease", "Front loops only of the next two stitches, yarn over, pull through both, yarn over, pull through two. In chenille the front loops are found by feel - insert the hook under the top 'V' from the front."),
        ("Stuff early", "Chenille closes over a narrow waist quickly. Start stuffing at R10 and keep the body firm before the waist round; you cannot push stuffing down through an 18-stitch neck afterwards."),
        ("Finding stitches for sewing", "Part the pile with your fingers to find the round you want before you sew a wing or the beak; pin first, then stitch."),
    ],
    sections=[
        dict(id="body", title="3 · Body & head - one piece", image="hero", caption="Tail to crown in one spiral; R13 is the waist that becomes the neck.",
             lead="Start at the tail end. The body reaches 30 stitches, narrows to an 18-stitch waist at R13 (the neck), widens again to 30 for the head, then closes at the crown.",
             tables=[dict(heading="Body & head · R1 - R23", rounds=[
                 ("R1", "6 sc in MR", 6, "tail end - knot the tail"), ("R2", "inc in each st around", 12, ""), ("R3", "[1 sc, inc] x 6", 18, ""), ("R4", "[2 sc, inc] x 6", 24, ""),
                 ("R5", "[3 sc, inc] x 6", 30, "body at full width"), ("R6", "sc in each st around", 30, ""), ("R7", "sc in each st around", 30, ""),
                 ("R8", "sc in each st around", 30, "wings at R7 - R9"), ("R9", "sc in each st around", 30, ""), ("R10", "sc in each st around", 30, "START STUFFING NOW - firmly"),
                 ("R11", "[3 sc, invdec] x 6", 24, ""), ("R12", "[2 sc, invdec] x 6", 18, "top up the body"), ("R13", "sc in each st around", 18, "WAIST = the neck"),
                 ("R14", "[2 sc, inc] x 6", 24, "head begins"), ("R15", "[3 sc, inc] x 6", 30, "head at full width"), ("R16", "sc in each st around", 30, ""),
                 ("R17", "sc in each st around", 30, "eyes at R17 - R18, 6 sts apart"), ("R18", "sc in each st around", 30, "beak over R17 - R19"), ("R19", "sc in each st around", 30, ""),
                 ("R20", "[3 sc, invdec] x 6", 24, "stuff the head firmly"), ("R21", "[2 sc, invdec] x 6", 18, ""), ("R22", "[1 sc, invdec] x 6", 12, "top up"), ("R23", "invdec x 6", 6, "crown")],
                 finish="Cinch the 6 stitches closed and bury the tail. Roll the duck between your palms to even out the stuffing. About 16 cm tall and 7.5 cm wide.")],
             panels=[("Why the waist works", "18 stitches at R13 is 60% of the 30-stitch body. That is narrow enough to read as a neck but wide enough for the head to be stuffed firmly through it from above - stuff the head as you go, R15-R20.", "tip")]),
        dict(id="parts", title="4 · Wings & beak", image="inhand", caption="Two flat wings and one flat beak - the only sewing on the duck.",
             lead="Wings are flat teardrops in chenille; the beak is a small flat oval in worsted orange on the smaller hook.",
             tables=[dict(heading="Wing · make 2 · chenille, 5.0 mm", rounds=[
                         ("R1", "6 sc in MR", 6, ""), ("R2", "[1 sc, inc] x 3", 9, ""), ("R3", "[2 sc, inc] x 3", 12, ""), ("R4", "sc in each st around", 12, ""),
                         ("R5", "sc in each st around", 12, ""), ("R6", "[2 sc, invdec] x 3", 9, "")],
                         finish="FO with a long tail; do not stuff. Flatten with the R1 point down and sew the 9-stitch opening to the body sides at R7-R9, opposite each other, tips pointing back and down."),
                     dict(heading="Beak · worsted orange, 3.5 mm · oval", rounds=[
                         ("Found.", "ch 5", "chain", ""),
                         ("R1", "sc in 2nd ch, sc in next 2, 3 sc in last ch, other side: sc in next 2, 2 sc in last ch", 10, ""),
                         ("R2", "inc, 2 sc, inc x 3, 2 sc, inc x 2", 16, "")],
                         finish="FO with a long tail. Fold the 16-stitch oval in half lengthways; sew the fold line to the face over R17-R19, centred between the eyes, with the free edge pointing forward - a soft, slightly open bill.")],
             steps=["Eyes - with black floss, embroider two small horizontal ovals (4-5 wraps each) at R17-R18, 6 stitches apart, just above the beak. Part the pile first so the floss sits on the fabric, not in the fluff.",
                    "Optional cheeks - two pink blush stitches under the eyes, or a brushed dab of pink pastel."]),
    ],
    assembly=[
        ("Wings", "Flatten each wing and sew the 9-stitch edge to the body at R7-R9, one each side, tips angled back and slightly down. Part the chenille pile to find the round first."),
        ("Beak", "Fold the orange oval and sew the fold to the face over R17-R19, centred. Two or three stitches along the underside keep it tilted slightly up."),
        ("Eyes", "Embroidered black ovals at R17-R18, 6 stitches apart, just above and outside the beak corners. No safety eyes anywhere on this duck."),
        ("Final shaping", "Squeeze the neck gently to define the waist, then roll the body and head between your palms so both are round and the duck stands on its flat tail end."),
    ],
    checklist=["1 body & head (one piece, closed at the crown)", "2 wings", "1 beak", "black floss for the eyes"],
    troubleshooting=[
        ("The body is soft and the head is fine.", "You started stuffing after the waist. Stuff firmly from R10 and top up at R12; the 18-stitch neck will not let stuffing back down afterwards."),
        ("The neck looks too thin or floppy.", "Keep the neck round (R13) tight and stuffed - push a little extra filling into the waist from above before R15. Do not add an extra plain round at 18."),
        ("Lost count in the chenille.", "Stop, find the marker, and count the current round by feel from the marker. If in doubt, work to the marker and treat that as the end of the round - chenille forgives a stitch either way."),
        ("Wings sit too high or low.", "R7-R9 is roughly the middle of the body. Part the pile, pin both wings, and check they are level from the front before sewing."),
        ("The beak looks flat and wide.", "Fold the oval lengthways and sew the FOLD to the face; the free edge should stand forward about 12 mm."),
        ("Stuffing shows.", "Chenille on 5.0 mm should be dense; if it gapes, go down to a 4.5 mm hook or stuff a little less firmly."),
    ],
    colorways=[("Duckling yellow", "#F5D96B", "#E8923A"), ("Cream", "#F5EFE0", "#E8A867"), ("Mint", "#BFE0D0", "#E8923A"), ("Blush", "#F3C9CF", "#E8923A"), ("Sky", "#BFD7EA", "#E8923A")],
    colorways_caption="Left to right: duckling yellow, cream, mint, blush, sky. Keep the beak orange for all of them - it is what makes a duck a duck.",
    terms_may=("Make as many finished ducks as you like for yourself, gifts, or charity. Sell physical finished items made from this pattern in small batches, "
               "in shops, markets and online, provided credit is given to \"Novality Crochet Studio\"."),
    thanks="Tag your makes with #NovalityCrochetStudio and #LittleDuckPlushie - we love seeing your ducks. Thank you for supporting an independent pattern designer.",
    images={"hero": "hero.png", "inhand": "inhand.png", "detail": "detail.png", "colorways": "colorways.png"},
    image_prompts={
        "hero": "Product photograph of a handmade crocheted duck plush toy in fluffy yellow chenille yarn, round squashy body and round head in one piece with a soft waist, small flat orange crocheted beak, embroidered black eyes, two small flat wings, about sixteen centimetres tall, on a soft cream linen surface, pastel backdrop, soft natural window light, shallow depth of field, clean etsy product photo",
        "inhand": "A handmade crocheted yellow chenille duck plush toy held in two open adult hands to show scale, about sixteen centimetres tall, small orange beak and embroidered eyes, soft cream background, natural light, shallow depth of field, product photo",
        "detail": "Close-up macro photograph of a handmade crocheted yellow chenille duck plush face showing the small folded orange crocheted beak, embroidered black oval eyes and the soft velvet pile texture, soft light, shallow depth of field",
        "colorways": "Five handmade crocheted chenille duck plush toys in a row, identical shape, in yellow, cream, mint, blush pink and sky blue velvet yarn, each with an orange beak, on a cream linen surface, pastel backdrop, soft natural light, product photo",
    },
)
