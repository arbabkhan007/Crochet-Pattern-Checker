"""Coco the Capybara - Novality NS 04. Corrections applied: R4/R5 leg layout rewritten so the two pairs sit opposite
each other (back legs a quarter-turn apart at R4, front pair directly opposite at R5). All counts verified."""

P = dict(
    slug="coco", title="Coco the Capybara", design_code="NS 04", terms="US terms", skill="Intermediate", time="2.5 - 3 hours",
    hashtag="#CocoTheCapybara",
    tagline=["A low, round, bottom-heavy capybara with a blunt sewn-on muzzle, plump legs",
             "and a calm embroidered sleeping face - no plastic eyes, no small plastic parts."],
    intro=("A low, round, bottom-heavy capybara with a blunt sewn-on muzzle, plump stuffed legs and a calm embroidered sleeping face. "
           "The legs are crocheted straight into the body as you go, so Coco stands on her feet, not her belly."),
    size_chip="10.3 cm / 4 in tall",
    stats=[("10.3 cm", "TALL, STANDING"), ("5 cm", "WIDE AT THE BODY"), ("36 sts", "AROUND THE BODY"), ("17 mm", "FEET BELOW THE BODY")],
    feats=[("36", "stitches around\nbody and head"), ("20", "body rounds, all\ncount-checked"), ("4", "legs joined in,\nnothing to sew"), ("0", "plastic parts -\nembroidered face")],
    palette=dict(accent="#C99A6B", deep="#8A5A32", pale="#F6ECE1", rule="#E8D9C8", hilite="#F1DFC9"),
    materials=[
        ("Main yarn", "Worsted weight (#4), warm brown, about 30 g. A smooth matte yarn shows the stitch texture best."),
        ("Face yarn", "Worsted weight (#4), dark brown, about 5 g - for the closed eyes, nose and mouth. Use the same weight as the main yarn."),
        ("Hook", "3.0 mm (US C-2 or D-3). The gauge is written for this hook."),
        ("Eyes", "None. The sleeping face is embroidered."),
        ("Also needed", "Polyester fibre filling about 5-8 g; yarn needle; stitch marker; pins. Pins matter: the muzzle and ears are pinned before sewing."),
    ],
    gauge=("36 sc around measures about 52 mm in diameter when stuffed (4.5 mm per stitch, 4.3 mm per round). Check it on the body after R6 - a stuffed tube, not a flat swatch. "
           "If your 36 stitches measure wider than 52 mm, crochet more tightly or go down a hook size; a loose gauge will show stuffing."),
    abbreviations=[("MR", "magic ring"), ("sc", "single crochet"), ("inc", "increase (2 sc in one st)"), ("invdec", "invisible decrease"), ("sc*", "sc worked through leg AND body together"),
                   ("st(s)", "stitch(es)"), ("FO", "fasten off"), ("(n)", "stitch count at round end")],
    techniques=[
        ("The magic ring", "Every piece begins with a magic ring. Pull the tail tight once the first round is complete."),
        ("Working in a spiral", "Keep a stitch marker in the first stitch of every round and move it up. There is no seam and no join to count from. Do not chain 1 between rounds."),
        ("The two-layer leg join", "The only fiddly step - worth practising once on a scrap magic ring. Hold a finished leg against the body with the pinched-flat top of the leg lying against the outside of the body. Insert the hook through BOTH the leg and the body stitch and work one single crochet; leg edge and body stitch are treated as one stitch. Every count in the body table stays correct. Pinch the leg top flat first - a round, un-pinched top will not lie against the curved body and the join will pucker."),
        ("Pinching the leg top", "A 9-stitch leg top flattens to about 5 stitches across - pinch it down to a strip about 3 stitches wide and hold it while you join. The stitches you don't join bunch up inside, and that bunch makes the leg look plump rather than tubular."),
    ],
    height_note=[("Legs below the body", "4 rounds x 4.3 mm", "17 mm"), ("Body + head, R1 - R20", "20 rounds x 4.3 mm", "86 mm"), ("Total standing height", "17 + 86", "103 mm (10.3 cm)")],
    sections=[
        dict(id="legs", title="3 · Legs - make 4", image="hero", caption="Back legs stop at R8, front legs work R9 - all four feet then reach the table.",
             lead=("Stuff the lower half of each leg lightly, leaving the top loose. Back legs stop after Rnd 8; front legs work Rnd 9 too - they join one round higher "
                   "and need to be one round longer so all four feet reach the table level."),
             tables=[dict(heading="Leg · make 4", rounds=[
                 ("R1", "6 sc in MR", 6, "all four"), ("R2", "[1 sc, inc] x 3", 9, "all four"), ("R3", "sc in each st around", 9, "all four"),
                 ("R4", "sc in each st around", 9, "all four"), ("R5", "sc in each st around", 9, "all four"), ("R6", "sc in each st around", 9, "all four"),
                 ("R7", "sc in each st around", 9, "all four"), ("R8", "sc in each st around", 9, "BACK legs finish here"), ("R9", "sc in each st around", 9, "FRONT legs only")],
                 finish="FO with a long tail. Before joining, pinch the whole 9-stitch top flat into a narrow strip about 3 stitches wide (technique 3).")]),
        dict(id="ears", title="4 · Ears & muzzle", image=None,
             lead="Ears are shallow cups and are not stuffed. The muzzle is stuffed just enough to hold a dome; it should sit proud of the head when sewn on.",
             tables=[dict(heading="Ear · make 2 · do not stuff", rounds=[
                         ("R1", "6 sc in MR", 6, ""), ("R2", "[1 sc, inc] x 3", 9, ""), ("R3", "sc in each st around", 9, "")],
                         finish="FO with a long tail; do not stuff - a shallow cup."),
                     dict(heading="Muzzle · make 1 · stuff lightly", rounds=[
                         ("R1", "6 sc in MR", 6, ""), ("R2", "[1 sc, inc] x 3", 9, ""), ("R3", "[2 sc, inc] x 3", 12, ""),
                         ("R4", "sc in each st around", 12, ""), ("R5", "sc in each st around", 12, "")],
                         finish="FO with a long tail and stuff lightly, just enough to hold a dome.")]),
        dict(id="body", title="5 · Body & head - one piece", image="inhand", caption="Body and head are both 36 stitches around; the R10 waist is deliberately shallow.",
             lead=("Both are 36 stitches around with only a shallow waist between them - that is what makes Coco read as one round blob rather than a snowman. "
                   "The legs are joined low at R4-R5 as you work those rounds: every stitch marked sc* is worked through a pinched leg top AND the body stitch together (technique 3). "
                   "Those stitches still count, so the totals do not change."),
             tables=[dict(heading="Body & head · R1 - R20", rounds=[
                 ("R1", "6 sc in MR", 6, ""), ("R2", "inc in each st around", 12, ""), ("R3", "[1 sc, inc] x 6", 18, ""),
                 ("R4", "3 sc*, 1 sc, inc, 3 sc*, [1 sc, inc] x 5", 24, "join the BACK legs"),
                 ("R5", "[2 sc, inc] x 4, 3 sc*, 1 sc, inc, 1 sc, 3 sc*, 1 sc, inc, 1 sc", 30, "join the FRONT legs"),
                 ("R6", "[4 sc, inc] x 6", 36, "full width - check gauge"), ("R7", "sc in each st around", 36, ""), ("R8", "sc in each st around", 36, ""),
                 ("R9", "sc in each st around", 36, "stuff the body FIRMLY"), ("R10", "[7 sc, invdec] x 4", 32, "shallow waist"),
                 ("R11", "[7 sc, inc] x 4", 36, "head begins"), ("R12", "sc in each st around", 36, "muzzle over R12 - R14"),
                 ("R13", "sc in each st around", 36, ""), ("R14", "sc in each st around", 36, "eyes at R14 - R15"), ("R15", "sc in each st around", 36, "ears at R15"),
                 ("R16", "[4 sc, invdec] x 6", 30, ""), ("R17", "[3 sc, invdec] x 6", 24, "stuff the head firmly"), ("R18", "[2 sc, invdec] x 6", 18, ""),
                 ("R19", "[1 sc, invdec] x 6", 12, "top up stuffing"), ("R20", "invdec x 6", 6, "")],
                 finish="Cinch the remaining 6 stitches closed and weave the tail inside the body. Do not decrease the R10 waist further - a narrow neck cannot hold the head upright on this shape.")],
             steps=["Joining the legs in R4 and R5: R4, BACK legs (24). Work the first 3 sc through a pinched leg and the body together, 1 sc, inc, then the next 3 sc through the second leg and the body together, then [1 sc, inc] x 5 to the end. The two back legs sit a quarter-turn apart.",
                    "R5, FRONT legs (30). [2 sc, inc] x 4, then 3 sc through a leg, 1 sc, inc, 1 sc, 3 sc through the other leg, 1 sc, inc, 1 sc. This puts the front pair directly opposite the back pair, each pair about a quarter-turn wide - a roughly square footprint of about 30 mm a side.",
                    "Hold the piece upside down and check all four legs sit square before you stuff the body. The side with the front legs is the front of the toy - centre the muzzle and eyes over it."]),
    ],
    assembly=[
        ("Muzzle", "Stuff lightly and pin it to the front of the head over R12-R14, centred, then sew all the way around with matching brown. It should sit proud of the head, not flush. Centring matters - the eyes go 6 stitches apart and a muzzle pinned even slightly off-centre crowds one eye."),
        ("Eyes", "Embroider. With dark brown, work a shallow downward arc about 3 stitches wide on each side, at R14-R15, 6 stitches apart, with a tiny tick angled down at each outer end. This closed-eye curve is what makes Coco look asleep."),
        ("Nose & mouth", "Embroider AFTER the muzzle is sewn on, so the stitches sit on the finished curve. On the muzzle, work a small dark triangle at top centre, a short vertical line down from it, and a soft curved mouth to one side."),
        ("Ears", "Pinch the base of each ear so it cups forward, then sew at R15, about 5 stitches apart, angled slightly outward. R15 is a full 36-stitch round, so this puts the ears on top of the head where a capybara's belong."),
        ("Legs", "The legs were joined during R4-R5 - there is nothing to sew. Just check each pinched 3-stitch strip is caught fully in the round."),
        ("Final shaping", "Roll the finished piece gently between your palms to settle the stuffing into a round, bottom-heavy shape."),
    ],
    checklist=["4 legs (2 back of 8 rounds, 2 front of 9)", "2 ears", "1 muzzle", "1 body & head, closed at the crown"],
    troubleshooting=[
        ("Coco looks too tall.", "Almost always too many plain rounds. R12-R15 is the straight head section the face is positioned on; adding 'just one more' round turns the shape into a tower and moves the face."),
        ("Coco will not stand.", "Check the join height, not the leg spacing. The legs belong on R4 and R5; joined any higher, they cannot clear the underside of the body and the belly rests on the table."),
        ("Coco tips forward or backward.", "The two pairs must sit opposite each other: back legs on the R4 stitches given, front legs on the R5 stitches given. Turn the piece upside down before stuffing and check the four feet make a square. If still tipping, stuff the lower body more firmly."),
        ("Rocks back, front feet in the air.", "All four legs are the same length and they cannot be. Front legs join at R5 (21 mm up), back at R4 (17 mm up); work the front legs 9 rounds and the back legs 8."),
        ("The head flops back.", "The R10 waist is deliberately shallow at 32 stitches - do not decrease it further. A narrow neck cannot hold the head upright."),
        ("Small hole where a leg meets the body.", "You joined a flat, wide leg top instead of a pinched one. Flatten the whole 9-stitch top into a strip about 3 stitches wide before joining, so the un-joined stitches bunch up inside."),
        ("Muzzle looks flat, or stuffing shows.", "Stuff the muzzle just enough to hold a dome. If stuffing shows through the body, your gauge is too loose - 36 stitches should measure 52 mm; crochet tighter or go down a hook size."),
    ],
    colorways=[("Classic warm brown", "#A9713F", "#5B3A21"), ("Soft grey", "#B9B4AE", "#5E5954"), ("Sandy beige", "#D8BE96", "#8A6A45"), ("Cocoa", "#6B4429", "#3A2314")],
    colorways_caption="Left to right: classic warm brown, soft grey, sandy beige, cocoa. Swap the main yarn - the sleeping face stays dark brown or charcoal.",
    terms_may=("Make as many finished Cocos as you like for yourself, gifts, or charity. Sell physical finished items made from this pattern in small batches, "
               "in shops, markets and online, provided credit is given to \"Novality Crochet Studio\"."),
    thanks="Tag your makes with #NovalityCrochetStudio and #CocoTheCapybara - we love seeing your Cocos. Thank you for supporting an independent pattern designer.",
    images={"hero": "hero.png", "inhand": "inhand.png", "detail": "detail.png", "colorways": "colorways.png"},
    image_prompts={
        "hero": "Product photograph of a small handmade crocheted amigurumi capybara plush toy, warm brown worsted yarn, squat round bottom-heavy body, four short plump legs, blunt sewn-on muzzle, embroidered closed sleeping eyes, tiny ears on top of head, standing on all four legs on a soft cream linen surface, pastel peach backdrop, soft natural window light, shallow depth of field, clean etsy product photo",
        "inhand": "A small handmade crocheted amigurumi capybara plush toy in warm brown yarn held in an open adult palm to show scale, about ten centimetres tall, embroidered sleeping face, standing on four short legs, soft cream and peach background, natural light, shallow depth of field, product photo",
        "detail": "Close-up macro photograph of a handmade crocheted amigurumi capybara toy showing the embroidered closed sleeping eyes, dark brown embroidered nose on a round sewn-on muzzle and tiny ears, visible single crochet stitch texture in warm brown worsted yarn, soft light, shallow depth of field",
        "colorways": "Four small handmade crocheted amigurumi capybara plush toys in a row, identical shape, in warm brown, soft grey, sandy beige and dark cocoa yarn, each with an embroidered sleeping face, on a cream linen surface, pastel backdrop, soft natural light, product photo",
    },
)
