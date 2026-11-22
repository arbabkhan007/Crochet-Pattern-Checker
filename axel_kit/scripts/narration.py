"""Narration script for the Axel the Axolotl audio walkthrough and tutorial video.

Each chapter is (slug, on-screen title, spoken text, image key for the video slide).
Spoken text is kept under 1500 characters per chapter (the speech engine's per-call limit).
"""

CHAPTERS = [
    ("01_welcome", "Welcome to Axel",
     "Welcome to Axel the Axolotl, an amigurumi crochet pattern from Novality Store. "
     "Axel is a soft pink axolotl with six fluffy gills, a perfectly round head, and a shell-edged paddle tail. "
     "The head, neck, body and tail are worked as one continuous spiral, so there is no neck seam to sew. "
     "Finished, Axel sits about eleven and a half centimetres tall, that is four and a half inches, "
     "and measures about ten centimetres from gill tip to gill tip. "
     "The pattern uses US terms, is rated advanced beginner, and takes around two and a half to three hours. "
     "In this walkthrough I will take you through the materials, the five techniques you will use, "
     "and then every round of every piece, followed by assembly. Grab your hook, and let's begin.",
     "hero"),

    ("02_safety_materials", "Safety & materials",
     "First, a word on safety. Axel has two six millimetre safety eyes, which are small parts. "
     "Lock the washers firmly from the inside before stuffing, and pull-test every eye on the finished toy. "
     "For children under three, skip the safety eyes and embroider them with black floss instead. "
     "This pattern has not been tested to a toy-safety standard, so please do not describe finished Axels as baby-safe. "
     "Now, materials. You need about fifteen grams of pale pink worsted weight yarn, number four, "
     "in cotton or acrylic with a smooth matte finish. One twenty-five gram ball covers the whole axolotl. "
     "For the gills, about eight grams of fuzzy, eyelash or fur yarn in dark pink. This is essential: "
     "smooth yarn will not give you fluffy gills, and the gills are the whole look. "
     "For the fin, about three grams of smooth dark pink worsted, so the shell edging stays crisp. "
     "You will also need a three and a half millimetre hook, that is a US E four, two six millimetre safety eyes, "
     "about eight grams of polyester filling, a tapestry needle, black embroidery floss, a little pink pastel or chalk for blush, "
     "and a stitch marker. "
     "Gauge: thirty-six single crochet around should measure about fifty-two millimetres across when stuffed. "
     "If yours is wider than fifty-five, drop to a three millimetre hook. Under forty-eight? Go up to four millimetres.",
     "flatlay"),

    ("03_techniques", "Five techniques",
     "Axel uses five techniques, and here they are in the order you will meet them. "
     "One, the magic ring. Every piece begins with one. Wrap the yarn once around two fingers, insert the hook, pull up a loop, "
     "work your first round into the ring, then pull the tail to close it tight. "
     "Two, working in a spiral. Do not join and do not chain one between rounds. Just keep going round after round. "
     "Keep a stitch marker in the first stitch of every round and move it up each time. "
     "Three, the invisible decrease. Insert your hook through the front loops only of the next two stitches, "
     "yarn over and pull through both, then yarn over and pull through the remaining two loops. "
     "It leaves no ridge, which matters on the head and neck where decreases are visible. "
     "Four, closing through both layers. Fold the piece flat so the front and back layers lie together, "
     "then work one single crochet through each matched pair of stitches. Axel's six-stitch tail tip folds into three pairs "
     "and closes with three single crochet. "
     "Five, the shell, or scallop. Work all the stitches of the group into one stitch, then slip stitch into the next stitch to anchor it. "
     "Working the double crochets loosely makes each scallop cup outward instead of lying flat.",
     "wip"),

    ("04_head", "Body part 1: the head, R1 to R13",
     "Let's start the body. This is one spiral from the top of the head all the way to the tail tip. "
     "Round one: six single crochet into a magic ring. Six stitches. "
     "Round two: increase in each stitch around. Twelve. "
     "Round three: one single crochet, then increase, repeated six times. Eighteen. "
     "Round four: two single crochet, increase, six times. Twenty-four. "
     "Round five: three single crochet, increase, six times. Thirty. "
     "Round six: four single crochet, increase, six times. Thirty-six. The head is now at full width. "
     "Rounds seven, eight and nine: single crochet in each stitch around. Thirty-six stitches on each of these three rounds. "
     "These three straight rounds are what keep the head spherical rather than egg-shaped. "
     "The eyes go between rounds seven and eight, six stitches apart, and the smile sits across rounds eight and nine. "
     "Round ten: four single crochet, invisible decrease, six times. Thirty. "
     "Round eleven: three single crochet, invisible decrease, six times. Twenty-four. Now stuff the head firmly. "
     "It needs to hold a sphere so the eyes stay level. "
     "Round twelve: two single crochet, invisible decrease, six times. Eighteen. "
     "Round thirteen: single crochet in each stitch around. Eighteen. This is the neck, the narrowest point of the whole toy.",
     "gills"),

    ("05_body", "Body part 2: the body, R14 to R26",
     "Now the body flares out from the neck. "
     "Round fourteen: two single crochet, increase, six times. Twenty-four. "
     "Round fifteen: three single crochet, increase, six times. Thirty. "
     "Round sixteen: four single crochet, increase, six times. Thirty-six. The body is at full width. "
     "Rounds seventeen through twenty-two: single crochet in each stitch around. That is six straight rounds of thirty-six. "
     "The arms will attach at rounds seventeen and eighteen. "
     "Round twenty-three: four single crochet, invisible decrease, six times. Thirty. "
     "Round twenty-four: three single crochet, invisible decrease, six times. Twenty-four. The feet attach at rounds twenty-four and twenty-five. "
     "Round twenty-five: two single crochet, invisible decrease, six times. Eighteen. Stuff the body lightly now. "
     "Keep it soft so Axel stays squishy and sits down nicely. If the neck feels floppy, pack a little extra stuffing up into the neck through this opening. "
     "Round twenty-six: one single crochet, invisible decrease, six times. Twelve.",
     "hero"),

    ("06_tail", "Body part 3: the tail, R27 to R36",
     "From here the spiral becomes the tail. "
     "Round twenty-seven: single crochet in each stitch around. Twelve. The tail begins. "
     "Round twenty-eight: two single crochet, invisible decrease, three times. Nine. "
     "Rounds twenty-nine, thirty and thirty-one: single crochet in each stitch around. Nine stitches each. "
     "Round thirty-two: one single crochet, invisible decrease, three times. Six. Add light stuffing up to here, then stop. "
     "Rounds thirty-three, thirty-four, thirty-five and thirty-six: single crochet in each stitch around. Six stitches each, tapering to the tip. "
     "To finish, fold the last six stitches flat so three pairs line up, then work one single crochet through each pair. "
     "Three single crochet in total closes the tip cleanly. Fasten off and weave the end back through the tail tip and out along the top ridge. "
     "You will crochet the fin directly onto that ridge later. The tail runs ten rounds, about forty-three millimetres, "
     "which gives the fin a long enough ridge to sit on.",
     "tail"),

    ("07_arms_feet", "Arms and feet",
     "Arms and feet are sewn on, not worked into the body. Bobbles will not give you rounded limbs. "
     "Make two arms. Round one: six single crochet into a magic ring. "
     "Rounds two to six: single crochet around, six stitches every round. Fasten off with a long tail after round six. "
     "Do not stuff the arms. Flatten the open end and sew it closed as you attach it, so the arms hang softly. "
     "Now make two feet. Round one: six single crochet into a magic ring. "
     "Round two: one single crochet, increase, three times. Nine. "
     "Rounds three and four: single crochet around. Nine stitches each. "
     "Round five: one single crochet, invisible decrease, three times. Six. "
     "Fasten off, cinch closed with a long tail, and stuff lightly. Do not flatten the feet. They are plump little balls, "
     "and you will sew the cinched nub toward the body.",
     "inhand"),

    ("08_gills", "Gills, make six",
     "Now the gills, and this is where Axel comes to life. Make six, three per side, in the fuzzy dark pink yarn. "
     "Round one: six single crochet into a magic ring. "
     "Round two: increase in each stitch around. Twelve. "
     "Rounds three and four: single crochet around. Twelve stitches each. "
     "Round five: one single crochet, invisible decrease, four times. Eight. This open edge is what you sew to the head. "
     "A tip for fuzzy yarn: you cannot see the stitches. Hold a thin strand of matching smooth yarn together with the fur yarn "
     "so you can find them, or count by feel with the hook tip and trust the round count. Small errors are invisible in the finished fluff. "
     "Fasten off with a long tail. Whip-stitch the eight-stitch opening flat against the head, or cinch the front loops first if you prefer a rounded lobe. "
     "Three fluffy gills fan behind each eye: the upper one angled up, the middle one straight out, and the lower one down.",
     "gills"),

    ("09_fin", "The tail fin",
     "Time for the shell-edged fin. With the smooth dark pink yarn, join with a slip stitch to the top ridge of the tail at the very tip, "
     "right into the corner of the end closure. Now work along the ridge back toward the body. "
     "Five double crochet in the next ridge stitch, then slip stitch in the next ridge stitch. "
     "Repeat that a total of five times, for five scallops. Fasten off and weave in. "
     "Each scallop uses two ridge stitches, so the fin spans ten stitches. The ten-round tail gives you a ridge of about ten workable stitches, "
     "so five scallops fit it exactly. Anchor the last slip stitch into the body junction. "
     "Work the double crochets loosely so each scallop cups outward. For a fuller paddle, work a second identical row along the underside ridge. "
     "And remember: five shells over ten rounds is meant to ruffle. The cupped, frilly edge is the look, not a mistake. "
     "If it seems crowded, work the double crochets even more loosely, or use half a hook size larger for the fin yarn only.",
     "tail"),

    ("10_assembly", "Assembly and finishing",
     "Before you sew anything, lay every component out and check: one body, two arms, two feet, six gills, and one fin. "
     "Eyes: insert the six millimetre safety eyes between rounds seven and eight, six stitches apart, centred on the front of the head. "
     "That spans about twenty-seven millimetres, roughly half the head. Fix the washers before stuffing and pull-test each one. "
     "Smile: with black floss, embroider a wide, shallow U across rounds eight and nine, about five stitches wide. Keep it shallow; a deep curve reads as a frown. "
     "Blush: brush soft pink pastel in a small circle just under each eye. "
     "Gills: sew three lobes to each side of the head behind the eyes, anchored at about round six for the upper, rounds seven to eight for the middle, "
     "and round nine for the lower. Angle them so they fan, then tease the fibres apart. "
     "Arms: sew one to each side at rounds seventeen and eighteen, about six stitches out from the centre front, angled slightly forward. "
     "Feet: sew one to each side of the centre front at rounds twenty-four and twenty-five, about four stitches out from centre, so Axel sits flat and upright. "
     "If Axel will not sit, move the feet one round lower and make sure the tail decreases are centred underneath, not at the back. "
     "And that is Axel. Try the other colourways too: white leucistic, melanoid black, mint, or lavender. "
     "Tag your makes with hashtag Novality Store and hashtag Axel the Axolotl. Thank you for supporting an independent pattern designer, and happy crocheting.",
     "colorways"),
]

for _slug, _title, _text, _img in CHAPTERS:
    assert len(_text) <= 1500, (_slug, len(_text))
