#!/usr/bin/env python3
"""Build and postflight the NS 02–NS 15 full-colour and printer-saver PDFs.

Every full-colour edition uses the approved Novality Crochet Studio visual system,
selectable named original-colour swatches, one clearly labelled illustrative cover
visual, one clearly labelled maker-map visual, bookmarks, repeated table headers,
and printable progress boxes. Every companion edition is raster-free, grayscale,
and black on white for economical home printing.

The visuals are illustrations, not photographs of physically tested samples. Physical
testing, real photography, title/provenance review, safety review, accessibility review,
and Etsy listing/disclosure compliance remain owner responsibilities.
"""

from __future__ import annotations

import argparse
import math
import random
import re
import zipfile
from dataclasses import dataclass
from hashlib import sha256
from html import unescape
from pathlib import Path
from typing import Iterable, Sequence

from PIL import Image as PILImage
from PIL import ImageDraw, ImageFilter
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import (
    BaseDocTemplate,
    CondPageBreak,
    Flowable,
    Frame,
    HRFlowable,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.platypus.tableofcontents import TableOfContents
from pypdf import PdfReader
from pypdf.generic import ContentStream, IndirectObject

try:  # Direct script execution: python tools/build_remaining_pattern_pdfs.py
    from build_ns01_etsy_pdf import (
        Block,
        Fonts,
        HeadingParagraph,
        image_for_width,
        inline_markup,
        make_printer_styles,
        make_styles,
        parse_markdown,
        pil_font,
        register_fonts,
        wrap_words,
    )
except ModuleNotFoundError:  # Module execution/import from the repository root.
    from tools.build_ns01_etsy_pdf import (
        Block,
        Fonts,
        HeadingParagraph,
        image_for_width,
        inline_markup,
        make_printer_styles,
        make_styles,
        parse_markdown,
        pil_font,
        register_fonts,
        wrap_words,
    )


ROOT = Path(__file__).resolve().parents[1]
PATTERN_DIR = ROOT / "patterns"
ASSET_ROOT = ROOT / "assets/patterns"
RELEASE_DIR = ROOT / "release"
BUNDLE_OUTPUT = RELEASE_DIR / "Novality_Crochet_Studio_NS02-NS15_PDF_Collection.zip"

PAGE_WIDTH, PAGE_HEIGHT = A4
BRAND = "Novality Crochet Studio"
FOREST = HexColor("#31473B")
FOREST_DARK = HexColor("#213229")
GINGER = HexColor("#B9652B")
GINGER_LIGHT = HexColor("#D08A4B")
PARCHMENT = HexColor("#F7F1E7")
PAPER = HexColor("#FFFDF8")
INK = HexColor("#28231F")
MUTED = HexColor("#6F665E")
LINE = HexColor("#D8CDBE")
PALE_GREEN = HexColor("#E7ECE7")
PALE_GINGER = HexColor("#F3E1D2")
WARNING_BG = HexColor("#F5E5D7")


@dataclass(frozen=True)
class PaletteEntry:
    name: str
    use: str
    colour: str


@dataclass(frozen=True)
class PatternSpec:
    number: int
    source_name: str
    cover_lines: tuple[str, ...]
    subtitle: str
    tagline: str
    identity: str
    skill: str
    time: str
    size: str
    yarn_hook: str
    palette: tuple[PaletteEntry, ...]
    critical: str
    hero_name: str
    motif: str = "photo"

    @property
    def code(self) -> str:
        return f"NS {self.number:02d}"

    @property
    def compact_code(self) -> str:
        return f"NS{self.number:02d}"

    @property
    def source(self) -> Path:
        return PATTERN_DIR / self.source_name

    @property
    def slug(self) -> str:
        return Path(self.source_name).stem.split("_", 1)[1]

    @property
    def hero(self) -> Path:
        return ASSET_ROOT / f"ns{self.number:02d}" / self.hero_name

    @property
    def maker_map(self) -> Path:
        return ASSET_ROOT / f"ns{self.number:02d}" / f"{self.compact_code.lower()}_maker_map.png"

    @property
    def main_output(self) -> Path:
        return RELEASE_DIR / f"{self.compact_code}_{self.slug}_Crochet_Pattern.pdf"

    @property
    def printer_output(self) -> Path:
        return RELEASE_DIR / f"{self.compact_code}_{self.slug}_PRINTER_SAVER.pdf"

    @property
    def title(self) -> str:
        first_line = self.source.read_text(encoding="utf-8").splitlines()[0]
        return re.sub(r"^#\s+", "", first_line).strip()

    @property
    def palette_summary(self) -> str:
        return " · ".join(entry.name for entry in self.palette)


SPECS: tuple[PatternSpec, ...] = (
    PatternSpec(
        2,
        "02_Kawaii_Halloween_Mini_Set.md",
        ("KAWAII", "HALLOWEEN"),
        "Mini Set",
        "Three pocket-sized spookies: Boo, Pip and Bramble.",
        "3 PATTERNS",
        "INTERMEDIATE",
        "45–60 MIN EACH",
        "ABOUT 5 CM EACH",
        "DK COTTON · 2.5 MM HOOK",
        (
            PaletteEntry("CREAM", "Boo body · about 8 g", "#E8DFCE"),
            PaletteEntry("PASTEL ORANGE", "Pip body · about 10 g", "#D98555"),
            PaletteEntry("LAVENDER", "Bramble body · about 9 g", "#9B83B7"),
            PaletteEntry("SAGE GREEN", "stem, tendril + leaf · about 4 g", "#82917A"),
            PaletteEntry("PALE PINK", "bat ear linings · about 2 g", "#DCA2AD"),
        ),
        "LOCK BOO + BRAMBLE EYES BEFORE CLOSING · EMBROIDER PIP BEFORE STUFFING",
        "halloween_mini_set_cover.jpg",
    ),
    PatternSpec(
        3,
        "03_Axel_the_Axolotl.md",
        ("AXEL",),
        "the Axolotl",
        "A soft pink axolotl with six fluffy gills and a paddle tail.",
        "US TERMS",
        "ADVANCED BEGINNER",
        "2.5–3 HOURS",
        "ABOUT 11.5 CM",
        "WORSTED · 3.5 MM HOOK",
        (
            PaletteEntry("PALE PINK", "head, body, limbs + tail · about 15 g", "#E5A4B4"),
            PaletteEntry("DARK PINK · FUZZY", "six fluffy gills · about 8 g", "#BE5D76"),
            PaletteEntry("DARK PINK · SMOOTH", "tail fin · about 3 g", "#A94061"),
        ),
        "LOCK EYES + EMBROIDER FACE AFTER RND 9 · BEFORE STUFFING",
        "axel_axolotl_cover.jpg",
    ),
    PatternSpec(
        4,
        "04_Coco_the_Capybara.md",
        ("COCO",),
        "the Capybara",
        "A low, calm capybara with a sleeping embroidered face.",
        "NO PLASTIC EYES",
        "INTERMEDIATE",
        "2.5–3 HOURS",
        "ABOUT 10.3 CM",
        "WORSTED · 3.0 MM HOOK",
        (
            PaletteEntry("WARM BROWN", "body, legs, ears + muzzle · about 30 g", "#986A4B"),
            PaletteEntry("DARK BROWN", "embroidered face · about 5 g", "#4A3027"),
        ),
        "EMBROIDER FACE AFTER BODY RND 15 · BEFORE DECREASES",
        "coco_capybara_cover.jpg",
    ),
    PatternSpec(
        5,
        "05_Little_Duck_Plushie.md",
        ("LITTLE DUCK",),
        "Plushie",
        "A round, squashy chenille duckling with embroidered eyes.",
        "EMBROIDERED EYES",
        "CONFIDENT BEGINNER",
        "1.5–2 HOURS",
        "ABOUT 16 CM",
        "CHENILLE #6 · 4.5 MM HOOK",
        (
            PaletteEntry("SUNSHINE YELLOW", "body + wings · about 25–35 g", "#EFC84D"),
            PaletteEntry("TANGERINE", "flat beak · small amount", "#E97934"),
            PaletteEntry("BLACK", "embroidered eyes", "#292525"),
        ),
        "SEW WINGS AFTER RND 9 · FACE + BEAK AFTER RND 19",
        "little_duck_cover.jpg",
    ),
    PatternSpec(
        6,
        "06_Momo_the_Loaf_Cat.md",
        ("MOMO",),
        "the Loaf Cat",
        "One low, wide loaf with worked-on ears and tail.",
        "NO-SEW BODY",
        "ADVANCED BEGINNER",
        "2–2.5 HOURS",
        "ABOUT 7.9 CM LONG",
        "WORSTED · 3.5 MM HOOK",
        (
            PaletteEntry("SOFT GREY", "main loaf · about 10 g", "#929593"),
            PaletteEntry("CREAM", "chest + tucked paws", "#EEE9DD"),
            PaletteEntry("PALE PINK", "nose + inner ears", "#DDA4AA"),
            PaletteEntry("BLACK", "eyes + whisker details", "#2D2C2B"),
        ),
        "LOCK EYES + EMBROIDER ALL DETAILS AFTER RND 9",
        "momo_loaf_cat_cover.jpg",
    ),
    PatternSpec(
        7,
        "07_Pocket_Positivity_Trio.md",
        ("POCKET", "POSITIVITY"),
        "Trio",
        "Sunny, Waddle and Spud: three tiny pocket companions.",
        "3 MINI PATTERNS",
        "EASY / BEGINNER",
        "20–35 MIN EACH",
        "ABOUT 2.7–3.8 CM",
        "WORSTED · 3.5 MM HOOK",
        (
            PaletteEntry("GOLDEN YELLOW", "Sunny petals + Waddle beak", "#D5A32E"),
            PaletteEntry("CHOCOLATE", "Sunny centre", "#5A3827"),
            PaletteEntry("BLACK", "Waddle body + faces", "#292929"),
            PaletteEntry("CREAM", "Waddle chest", "#EEE5D2"),
            PaletteEntry("WARM TAN", "Spud body", "#B78A5E"),
        ),
        "LOCK OR EMBROIDER EVERY FACE BEFORE DECREASES AND CLOSURE",
        "pocket_positivity_trio_cover.jpg",
    ),
    PatternSpec(
        8,
        "08_Ember_the_Baby_Dragon.md",
        ("EMBER",),
        "the Baby Dragon",
        "A chunky seated dragon with scalloped wings and back spikes.",
        "US TERMS",
        "INTERMEDIATE",
        "4–5 HOURS",
        "ABOUT 10.5 CM",
        "WORSTED · 3.5 MM HOOK",
        (
            PaletteEntry("SAGE GREEN", "body, snout, legs + tail · about 30 g", "#7C9274"),
            PaletteEntry("PALE GOLD", "wings, horns + spikes · about 20 g", "#DEC58A"),
            PaletteEntry("DARK BROWN", "embroidered nostrils", "#40342F"),
        ),
        "LOCK EYES AFTER RND 8 · MATCH THE 18-TO-18 NECK JOIN",
        "ember_baby_dragon_cover.jpg",
    ),
    PatternSpec(
        9,
        "09_Shelby_the_Sea_Turtle_Bag_Charm.md",
        ("SHELBY",),
        "the Sea Turtle Bag Charm",
        "A tiny flat sea turtle worked directly into its underside.",
        "BAG CHARM",
        "EASY",
        "ABOUT 30 MIN",
        "ABOUT 3.7 CM",
        "DK COTTON · 2.5 MM HOOK",
        (
            PaletteEntry("SAGE GREEN", "shell · about 1 g", "#788D72"),
            PaletteEntry("CREAM", "underside, head + flippers · about 1 g", "#E9DFCB"),
            PaletteEntry("DARK SAGE", "embroidered shell markings", "#4F6650"),
            PaletteEntry("BLACK", "French-knot eyes", "#282828"),
        ),
        "JOIN 24 SHELL STS TO 24 EXPOSED LOOPS · SECURE KEYRING BEFORE CLOSING",
        "shelby_turtle_cover_graphic.png",
        "turtle",
    ),
    PatternSpec(
        10,
        "10_Willow_the_Bunny_Lovey.md",
        ("WILLOW",),
        "the Bunny Lovey",
        "A firmly joined bunny head above a drapey granny square.",
        "EMBROIDERED FACE",
        "ADVANCED BEGINNER",
        "ABOUT 4–6 HOURS",
        "26 CM SQUARE",
        "DK COTTON · 3.5 MM HOOK",
        (
            PaletteEntry("CREAM", "head, ears + blanket · about 60 g", "#E9DFCC"),
            PaletteEntry("DARK BROWN", "embroidered face", "#4C382F"),
        ),
        "FACE AFTER HEAD RND 10 · SEW ALL 18 MARKED STS TWICE",
        "willow_lovey_cover_graphic.png",
        "lovey",
    ),
    PatternSpec(
        11,
        "11_No-Sew_Christmas_Gnome.md",
        ("NO-SEW",),
        "Christmas Gnome",
        "Body, beard, face and hat worked as one continuous piece.",
        "US + UK TERMS",
        "BEGINNER",
        "1–2 HOURS",
        "ABOUT 11–12.5 CM",
        "WORSTED · 3.5 MM HOOK",
        (
            PaletteEntry("SANTA RED", "body + hat · about 40–50 g", "#B6433A"),
            PaletteEntry("SNOW WHITE", "beard · about 10–15 g", "#F0ECE2"),
            PaletteEntry("SKIN TONE", "face + bobble nose · about 10 g", "#D9A17F"),
            PaletteEntry("DARK BROWN", "optional embroidered eyes", "#3A302C"),
        ),
        "ADD EYES AFTER RND 15 · BEFORE STUFFING AT RND 16",
        "no_sew_gnome_cover_graphic.png",
        "gnome",
    ),
    PatternSpec(
        12,
        "12_Bobble_Christmas_Tree.md",
        ("BOBBLE",),
        "Christmas Tree",
        "A one-piece standing fir with tiered bobbles and baubles.",
        "US + UK TERMS",
        "EASY–INTERMEDIATE",
        "2–3 HOURS",
        "ABOUT 12 CM",
        "WORSTED · 4.0 MM HOOK",
        (
            PaletteEntry("FIR GREEN", "one-piece tree · about 60–80 g", "#446447"),
            PaletteEntry("CRIMSON", "optional contrast bobbles", "#B8453C"),
            PaletteEntry("GOLD", "optional contrast bobbles", "#C99A32"),
            PaletteEntry("CREAM", "optional contrast bobbles", "#EEE4CD"),
        ),
        "CHANGE TO CONTRAST BEFORE EACH BOBBLE · BASE DISC AFTER RND 9",
        "bobble_tree_cover_graphic.png",
        "tree",
    ),
    PatternSpec(
        13,
        "13_Christmas_Ornament_Bundle.md",
        ("CHRISTMAS",),
        "Ornament Bundle",
        "A bauble, five-point star and six-arm snowflake from scraps.",
        "US + UK TERMS",
        "BEGINNER",
        "15–40 MIN EACH",
        "THREE ORNAMENTS",
        "DK / WORSTED · 3–4 MM",
        (
            PaletteEntry("CLASSIC RED", "round bauble", "#B6403C"),
            PaletteEntry("SNOW WHITE", "snowflake + accents", "#F2EEE4"),
            PaletteEntry("GOLD", "star + metallic details", "#C79A35"),
            PaletteEntry("EVERGREEN", "optional coordinated accents", "#3F6348"),
            PaletteEntry("SILVER", "metallic stripe or loop option", "#A7AAA8"),
        ),
        "COUNT EACH REPEAT · BLOCK THE STAR AND SNOWFLAKE TO SHAPE",
        "ornament_bundle_cover_graphic.png",
        "ornaments",
    ),
    PatternSpec(
        14,
        "14_Bobble_Snowflake_Tree_Skirt.md",
        ("BOBBLE", "SNOWFLAKE"),
        "Tree Skirt",
        "A twelve-spoke circle with bobble snowflakes and three sizes.",
        "US + UK TERMS",
        "EASY–INTERMEDIATE",
        "GROWS BY SIZE",
        "46–109 CM",
        "WORSTED · 5–5.5 MM HOOK",
        (
            PaletteEntry("FOREST GREEN", "main twelve-spoke field", "#3D6245"),
            PaletteEntry("OAT CREAM", "bobble snowflake contrast", "#E8DEC6"),
        ),
        "ROUND N CONSUMES N-1 STS · KEEP ALL 12 COLUMNS ALIGNED",
        "tree_skirt_cover_graphic.png",
        "skirt",
    ),
    PatternSpec(
        15,
        "15_Interchangeable_Christmas_Wreath.md",
        ("INTERCHANGEABLE",),
        "Christmas Wreath",
        "A measured stuffed ring with three removable decorations.",
        "US + UK TERMS",
        "BEGINNER",
        "GROWS BY LENGTH",
        "MINI TO LARGE DOOR",
        "WORSTED · 4.0 MM HOOK",
        (
            PaletteEntry("WREATH GREEN", "stuffed tube base · 150–200 g", "#426947"),
            PaletteEntry("POINSETTIA RED", "removable flower", "#B53F39"),
            PaletteEntry("SNOW WHITE", "removable snowflake", "#F1EDE3"),
            PaletteEntry("GOLD", "flower centre + bow accent", "#C9A03A"),
        ),
        "MEASURE THE TUBE · KEEP OPENINGS ROUND · JOIN 12 PAIRS",
        "wreath_cover_graphic.png",
        "wreath",
    ),
)


def normalize_branding(text: str) -> str:
    """Apply the approved customer brand and collection spelling."""

    return (
        text.replace("Novality Store", BRAND)
        .replace("#NovalityStore", "#NovalityCrochetStudio")
        .replace("## Colorways", "## Colourways")
        .replace(
            "including all instructions, stitch counts, photography and design elements",
            "including all instructions, stitch counts, editorial layout and design elements",
        )
    )


def hex_rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[index : index + 2], 16) for index in (0, 2, 4))  # type: ignore[return-value]


def darker(rgb: tuple[int, int, int], factor: float = 0.72) -> tuple[int, int, int]:
    return tuple(max(0, round(channel * factor)) for channel in rgb)  # type: ignore[return-value]


def contrasting_pdf_colour(value: str):  # noqa: ANN201
    """Choose the higher-contrast near-black or white text colour."""

    channels = []
    for channel in hex_rgb(value):
        normalized = channel / 255
        channels.append(normalized / 12.92 if normalized <= 0.04045 else ((normalized + 0.055) / 1.055) ** 2.4)
    luminance = 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]
    return colors.white if luminance < 0.179 else INK


def shape_layer(
    canvas: PILImage.Image,
    mask: PILImage.Image,
    fill: tuple[int, int, int],
    *,
    spacing: int = 34,
    seed: int = 1,
) -> None:
    """Fill a masked shape and add restrained crochet-like stitch marks."""

    colour_layer = PILImage.new("RGB", canvas.size, fill)
    canvas.paste(colour_layer, mask=mask)
    stitches = PILImage.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(stitches)
    rng = random.Random(seed)
    mark = (*darker(fill, 0.75), 105)
    bbox = mask.getbbox()
    if not bbox:
        return
    left, top, right, bottom = bbox
    for y in range(top + spacing // 2, bottom, spacing):
        offset = spacing // 2 if (y // spacing) % 2 else 0
        for x in range(left + offset, right, spacing):
            if mask.getpixel((min(x, canvas.width - 1), min(y, canvas.height - 1))) > 0:
                width = max(8, spacing // 2 + rng.randint(-3, 3))
                draw.arc((x - width, y - 6, x + width, y + 10), 205, 335, fill=mark, width=2)
    clipped = PILImage.composite(stitches, PILImage.new("RGBA", canvas.size), mask)
    canvas.paste(clipped, mask=clipped.getchannel("A"))


def mask_image(size: tuple[int, int]) -> tuple[PILImage.Image, ImageDraw.ImageDraw]:
    mask = PILImage.new("L", size, 0)
    return mask, ImageDraw.Draw(mask)


def polygon_star(cx: int, cy: int, outer: int, inner: int, points: int = 5) -> list[tuple[float, float]]:
    result = []
    for index in range(points * 2):
        radius = outer if index % 2 == 0 else inner
        angle = -math.pi / 2 + index * math.pi / points
        result.append((cx + radius * math.cos(angle), cy + radius * math.sin(angle)))
    return result


def create_graphic_cover(spec: PatternSpec) -> None:
    """Create a deterministic editorial crochet motif when no generated hero exists."""

    path = spec.hero
    path.parent.mkdir(parents=True, exist_ok=True)
    size = (1400, 1800)
    rng = random.Random(spec.number)
    canvas = PILImage.new("RGB", size, "#F3EBDD")
    draw = ImageDraw.Draw(canvas)
    for _ in range(420):
        y = rng.randrange(0, size[1])
        shade = rng.choice(("#EFE5D6", "#F7F1E7", "#EDE2D2"))
        draw.line((0, y, size[0], y + rng.choice((-2, -1, 1, 2))), fill=shade, width=1)
    draw.rounded_rectangle((82, 82, 1318, 1718), radius=52, fill="#FFFDF8", outline="#D8CDBE", width=4)
    draw.ellipse((250, 1375, 1150, 1515), fill="#E5DDD1")

    colours = [hex_rgb(entry.colour) for entry in spec.palette]
    main = colours[0]
    second = colours[1] if len(colours) > 1 else darker(main)
    third = colours[2] if len(colours) > 2 else (70, 70, 70)
    outline = darker(main, 0.58)

    def ellipse(box, colour, seed):  # noqa: ANN001
        mask, md = mask_image(size)
        md.ellipse(box, fill=255)
        shape_layer(canvas, mask, colour, seed=seed)
        draw.ellipse(box, outline=darker(colour, 0.58), width=5)

    def polygon(points, colour, seed):  # noqa: ANN001
        mask, md = mask_image(size)
        md.polygon(points, fill=255)
        shape_layer(canvas, mask, colour, seed=seed)
        draw.line([*points, points[0]], fill=darker(colour, 0.58), width=5, joint="curve")

    if spec.motif == "turtle":
        ellipse((510, 760, 900, 1080), second, 91)
        polygon([(515, 850), (390, 765), (420, 930), (530, 950)], second, 92)
        polygon([(860, 850), (1010, 770), (980, 940), (870, 955)], second, 93)
        polygon([(530, 1010), (410, 1115), (575, 1110), (625, 1040)], second, 94)
        polygon([(840, 1010), (965, 1115), (800, 1110), (755, 1040)], second, 95)
        ellipse((610, 585, 795, 790), second, 96)
        ellipse((430, 690, 975, 1100), main, 97)
        draw.ellipse((430, 690, 975, 1100), outline=outline, width=8)
        for x, y in ((570, 820), (700, 760), (830, 830), (620, 950), (780, 960)):
            draw.line((x - 28, y - 20, x, y + 8, x + 28, y - 20), fill=darker(main, 0.58), width=8)
        draw.ellipse((645, 660, 658, 673), fill="#222222")
        draw.ellipse((747, 660, 760, 673), fill="#222222")
        draw.arc((920, 545, 1150, 775), 25, 330, fill="#777777", width=20)
        draw.arc((955, 580, 1115, 740), 25, 330, fill="#FFFDF8", width=18)
        draw.line((950, 740, 880, 820), fill="#777777", width=18)
    elif spec.motif == "lovey":
        blanket = [(700, 730), (1110, 1120), (700, 1510), (290, 1120)]
        polygon(blanket, main, 101)
        for inset in (85, 165, 245):
            pts = [(700, 730 + inset), (1110 - inset, 1120), (700, 1510 - inset), (290 + inset, 1120)]
            draw.line([*pts, pts[0]], fill=darker(main, 0.76), width=7, joint="curve")
        ellipse((515, 470, 885, 830), main, 102)
        ellipse((485, 235, 625, 600), main, 103)
        ellipse((775, 235, 915, 600), main, 104)
        draw.ellipse((555, 300, 590, 520), fill=second)
        draw.ellipse((810, 300, 845, 520), fill=second)
        draw.arc((590, 570, 670, 650), 195, 345, fill=third, width=8)
        draw.arc((730, 570, 810, 650), 195, 345, fill=third, width=8)
        draw.polygon([(700, 650), (675, 680), (725, 680)], fill=third)
    elif spec.motif == "gnome":
        ellipse((430, 720, 970, 1390), main, 111)
        polygon([(700, 230), (395, 870), (1005, 870)], main, 112)
        draw.ellipse((420, 795, 980, 915), fill=main, outline=outline, width=6)
        beard_mask, beard_draw = mask_image(size)
        beard_draw.polygon([(465, 825), (935, 825), (850, 1375), (700, 1510), (550, 1375)], fill=255)
        for x in range(500, 920, 90):
            beard_draw.ellipse((x - 60, 780, x + 70, 1030), fill=255)
        shape_layer(canvas, beard_mask, second, seed=113)
        draw.ellipse((620, 760, 780, 920), fill=third, outline=darker(third), width=5)
        draw.arc((500, 800, 900, 1040), 0, 180, fill=darker(second), width=5)
    elif spec.motif == "tree":
        polygon([(700, 250), (365, 790), (1035, 790)], main, 121)
        polygon([(700, 520), (285, 1120), (1115, 1120)], main, 122)
        polygon([(700, 790), (210, 1415), (1190, 1415)], main, 123)
        draw.rectangle((625, 1390, 775, 1510), fill=darker(main, 0.55))
        bobble_colours = colours[1:] or [second]
        for index, (x, y) in enumerate(((610, 550), (785, 670), (515, 860), (720, 930), (925, 980), (395, 1190), (635, 1250), (900, 1270))):
            colour = bobble_colours[index % len(bobble_colours)]
            draw.ellipse((x - 36, y - 36, x + 36, y + 36), fill=colour, outline=darker(colour), width=4)
    elif spec.motif == "ornaments":
        ellipse((245, 650, 645, 1050), main, 131)
        draw.rectangle((385, 580, 505, 680), fill=third, outline=darker(third), width=4)
        draw.arc((350, 455, 540, 660), 195, 345, fill="#806C53", width=12)
        polygon(polygon_star(925, 820, 245, 105), third, 132)
        snow = second
        center = (700, 1290)
        for angle in range(0, 360, 60):
            rad = math.radians(angle)
            x2 = center[0] + 280 * math.cos(rad)
            y2 = center[1] + 280 * math.sin(rad)
            draw.line((*center, x2, y2), fill=darker(snow, 0.72), width=15)
            for distance in (155, 220):
                bx = center[0] + distance * math.cos(rad)
                by = center[1] + distance * math.sin(rad)
                for delta in (-35, 35):
                    branch = math.radians(angle + 180 + delta)
                    draw.line((bx, by, bx + 70 * math.cos(branch), by + 70 * math.sin(branch)), fill=darker(snow, 0.72), width=11)
        draw.ellipse((675, 1265, 725, 1315), fill=snow)
    elif spec.motif == "skirt":
        center = (700, 930)
        radii = (520, 420, 320, 215)
        for index, radius in enumerate(radii):
            colour = main if index % 2 == 0 else second
            ellipse((700 - radius, 930 - radius, 700 + radius, 930 + radius), colour, 140 + index)
        draw.ellipse((555, 785, 845, 1075), fill="#FFFDF8", outline=outline, width=7)
        for angle in range(0, 360, 30):
            rad = math.radians(angle)
            draw.line((700 + 150 * math.cos(rad), 930 + 150 * math.sin(rad), 700 + 520 * math.cos(rad), 930 + 520 * math.sin(rad)), fill=darker(main, 0.68), width=5)
            bx = 700 + 365 * math.cos(rad)
            by = 930 + 365 * math.sin(rad)
            draw.ellipse((bx - 22, by - 22, bx + 22, by + 22), fill=second, outline=darker(second), width=3)
    elif spec.motif == "wreath":
        mask, md = mask_image(size)
        md.ellipse((225, 390, 1175, 1340), fill=255)
        md.ellipse((505, 670, 895, 1060), fill=0)
        shape_layer(canvas, mask, main, spacing=38, seed=151)
        draw.ellipse((225, 390, 1175, 1340), outline=outline, width=8)
        draw.ellipse((505, 670, 895, 1060), outline=outline, width=8)
        cx, cy = 980, 570
        for index in range(6):
            angle = index * math.pi / 3
            px = cx + 95 * math.cos(angle)
            py = cy + 95 * math.sin(angle)
            polygon(polygon_star(round(px), round(py), 100, 38, 5), second, 152 + index)
        draw.ellipse((945, 535, 1015, 605), fill=third)
        sx, sy = 390, 1080
        for angle in range(0, 360, 60):
            rad = math.radians(angle)
            draw.line((sx, sy, sx + 145 * math.cos(rad), sy + 145 * math.sin(rad)), fill=darker(third, 0.65), width=12)
        polygon([(660, 1280), (540, 1390), (690, 1425), (700, 1335)], third, 160)
        polygon([(740, 1280), (860, 1390), (710, 1425), (700, 1335)], third, 161)
        draw.rounded_rectangle((625, 1200, 775, 1340), radius=34, fill=third, outline=darker(third), width=5)

    draw.rounded_rectangle((160, 1540, 1240, 1618), radius=30, fill="#E7ECE7", outline="#76836A", width=3)
    label = "ILLUSTRATIVE CROCHET MOTIF · WRITTEN DIRECTIONS CONTROL"
    font = pil_font(26, bold=True)
    bbox = draw.textbbox((0, 0), label, font=font)
    draw.text(((1400 - (bbox[2] - bbox[0])) / 2, 1564), label, font=font, fill="#31473B")
    canvas = canvas.filter(ImageFilter.UnsharpMask(radius=1.2, percent=90, threshold=3))
    canvas.save(path, optimize=True)


def clean_heading(value: str) -> str:
    value = re.sub(r"\*+|`", "", value)
    return unescape(value).strip()


def component_headings(text: str) -> list[str]:
    match = re.search(r"^## Instructions\s*$\n(.*?)(?=^## |\Z)", text, re.MULTILINE | re.DOTALL)
    if not match:
        return []
    return [clean_heading(value) for value in re.findall(r"^###\s+(.+)$", match.group(1), re.MULTILINE)]


def create_maker_map(spec: PatternSpec) -> None:
    """Create a concise visual route through the source's component sections."""

    spec.maker_map.parent.mkdir(parents=True, exist_ok=True)
    source_text = normalize_branding(spec.source.read_text(encoding="utf-8"))
    headings = component_headings(source_text)
    cards = headings[:9]
    if len(cards) < 4:
        cards.extend(
            [
                "COUNT · Confirm every stated stitch total",
                "SHAPE · Measure and pin before committing",
                "FINISH · Follow the written finishing order",
            ][: 4 - len(cards)]
        )

    width, height = 1800, 1120
    canvas = PILImage.new("RGB", (width, height), "#F7F1E7")
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((40, 40, 1760, 1080), radius=38, fill="#FFFDF8", outline="#D8CDBE", width=3)
    draw.text((105, 82), "MAKER MAP", font=pil_font(53, bold=True, serif=True), fill="#28231F")
    draw.text(
        (108, 154),
        f"{spec.code} · Use this route for orientation; the numbered written directions control.",
        font=pil_font(25),
        fill="#6F665E",
    )

    columns = 3
    rows = math.ceil(len(cards) / columns)
    card_w = 500
    x0, gap_x = 105, 45
    top, bottom = 230, 930
    gap_y = 30
    card_h = (bottom - top - gap_y * (rows - 1)) // rows
    for index, title in enumerate(cards):
        row, column = divmod(index, columns)
        x = x0 + column * (card_w + gap_x)
        y = top + row * (card_h + gap_y)
        fill = "#F3E1D2" if index == 0 else "#F3F5F1"
        outline = "#B9652B" if index == 0 else "#D8CDBE"
        draw.rounded_rectangle((x, y, x + card_w, y + card_h), radius=22, fill=fill, outline=outline, width=3)
        draw.ellipse((x + 24, y + 24, x + 98, y + 98), fill="#31473B")
        number = f"{index + 1:02d}"
        number_box = draw.textbbox((0, 0), number, font=pil_font(23, bold=True))
        draw.text((x + 61 - (number_box[2] - number_box[0]) / 2, y + 44), number, font=pil_font(23, bold=True), fill="#FFFDF8")
        title = re.sub(r"^\d+[.]\s*|^[A-Z][.]\s*", "", title)
        wrapped = wrap_words(title, 34)
        draw.multiline_text((x + 118, y + 27), wrapped, font=pil_font(22, bold=True), fill="#28231F", spacing=8)

    draw.rounded_rectangle((105, 970, 1695, 1040), radius=18, fill="#31473B")
    critical = wrap_words(spec.critical, 92)
    bbox = draw.multiline_textbbox((0, 0), critical, font=pil_font(23, bold=True), spacing=3)
    text_w = bbox[2] - bbox[0]
    draw.multiline_text(((1800 - text_w) / 2, 988), critical, font=pil_font(23, bold=True), fill="#FFFDF8", spacing=3, align="center")
    canvas.save(spec.maker_map, optimize=True)


def ensure_visual_assets(spec: PatternSpec) -> None:
    if spec.motif != "photo":
        create_graphic_cover(spec)
    if not spec.hero.exists():
        raise FileNotFoundError(f"Missing cover visual for {spec.code}: {spec.hero}")
    create_maker_map(spec)


def draw_fitted_text(canvas, font_name: str, text: str, x: float, y: float, max_width: float, start: float, minimum: float) -> float:  # noqa: ANN001
    size = start
    while size > minimum and pdfmetrics.stringWidth(text, font_name, size) > max_width:
        size -= 0.5
    canvas.setFont(font_name, size)
    canvas.drawString(x, y, text)
    return size


class CollectionCover(Flowable):
    """Approved editorial cover adapted to one collection spec."""

    def __init__(self, spec: PatternSpec, fonts: Fonts):
        super().__init__()
        self.spec = spec
        self.fonts = fonts
        self.width = PAGE_WIDTH
        self.height = PAGE_HEIGHT - 0.2 * mm

    def wrap(self, available_width, available_height):  # noqa: ANN001
        return self.width, min(self.height, available_height)

    def draw(self) -> None:
        canvas = self.canv
        spec = self.spec
        canvas.saveState()
        canvas.setFillColor(PARCHMENT)
        canvas.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, stroke=0, fill=1)
        canvas.setFillColor(FOREST_DARK)
        canvas.rect(0, PAGE_HEIGHT - 18 * mm, PAGE_WIDTH, 18 * mm, stroke=0, fill=1)
        canvas.setFillColor(colors.white)
        canvas.setFont(self.fonts.sans_bold, 9)
        canvas.drawString(15 * mm, PAGE_HEIGHT - 11.2 * mm, BRAND.upper())
        canvas.setFont(self.fonts.sans, 7.5)
        canvas.drawRightString(PAGE_WIDTH - 15 * mm, PAGE_HEIGHT - 11.2 * mm, "ORIGINAL CROCHET PATTERN")

        image_x, image_y = 89 * mm, 76 * mm
        image_w, image_h = 106 * mm, 142 * mm
        canvas.setFillColor(PAPER)
        canvas.roundRect(image_x - 3 * mm, image_y - 3 * mm, image_w + 6 * mm, image_h + 6 * mm, 5 * mm, stroke=0, fill=1)
        canvas.drawImage(str(spec.hero), image_x, image_y, width=image_w, height=image_h, preserveAspectRatio=True, anchor="c", mask="auto")

        accent = HexColor(spec.palette[0].colour)
        canvas.setFillColor(accent)
        canvas.roundRect(14 * mm, 224 * mm, 54 * mm, 11 * mm, 5.5 * mm, stroke=0, fill=1)
        canvas.setFillColor(contrasting_pdf_colour(spec.palette[0].colour))
        canvas.setFont(self.fonts.sans_bold, 9.2)
        canvas.drawCentredString(41 * mm, 227.7 * mm, f"DESIGN CODE  {spec.code}")

        canvas.setFillColor(FOREST_DARK)
        title_y = 204 * mm
        for line in spec.cover_lines:
            draw_fitted_text(canvas, self.fonts.serif_bold, line, 14 * mm, title_y, 66 * mm, 27, 14)
            title_y -= 12 * mm
        draw_fitted_text(canvas, self.fonts.serif, spec.subtitle, 14 * mm, title_y, 67 * mm, 16, 10)
        line_y = title_y - 9 * mm
        canvas.setStrokeColor(accent)
        canvas.setLineWidth(2)
        canvas.line(14 * mm, line_y, 70 * mm, line_y)

        canvas.setFillColor(MUTED)
        canvas.setFont(self.fonts.sans, 8.1)
        description_y = line_y - 10 * mm
        for line in wrap_words(spec.tagline, 37).splitlines()[:4]:
            canvas.drawString(14 * mm, description_y, line)
            description_y -= 5.7 * mm

        stats = ((spec.identity, 132), (spec.skill, 121), (spec.time, 110), (spec.size, 99))
        for label, y in stats:
            canvas.setFillColor(FOREST)
            canvas.circle(17 * mm, y * mm + 1.4 * mm, 1.6 * mm, stroke=0, fill=1)
            canvas.setFillColor(INK)
            draw_fitted_text(canvas, self.fonts.sans_bold, label, 23 * mm, y * mm, 53 * mm, 8.0, 6.2)

        canvas.setFillColor(PALE_GINGER)
        canvas.roundRect(14 * mm, 62 * mm, 62 * mm, 27 * mm, 3 * mm, stroke=0, fill=1)
        canvas.setFillColor(INK)
        canvas.setFont(self.fonts.sans_bold, 7.3)
        canvas.drawString(19 * mm, 81 * mm, "ORIGINAL COLOURWAY")
        canvas.setFont(self.fonts.sans, 6.8)
        palette_lines = wrap_words(spec.palette_summary, 36).splitlines()[:2]
        y = 74.5 * mm
        for line in palette_lines:
            canvas.drawString(19 * mm, y, line)
            y -= 5 * mm
        draw_fitted_text(canvas, self.fonts.sans, spec.yarn_hook, 19 * mm, 65.5 * mm, 52 * mm, 6.6, 5.4)

        canvas.setStrokeColor(LINE)
        canvas.setLineWidth(0.7)
        canvas.line(14 * mm, 42 * mm, PAGE_WIDTH - 14 * mm, 42 * mm)
        canvas.setFillColor(MUTED)
        canvas.setFont(self.fonts.sans, 6.8)
        canvas.drawString(14 * mm, 34.5 * mm, "FIRST EDITION · 2026")
        canvas.drawRightString(PAGE_WIDTH - 14 * mm, 34.5 * mm, "DIGITAL CROCHET PATTERN")
        canvas.setFont(self.fonts.sans, 6.2)
        canvas.drawString(14 * mm, 27 * mm, "ILLUSTRATIVE COVER ART · NAMED ORIGINAL COLOURS · WRITTEN INSTRUCTIONS CONTROL")
        canvas.setFillColor(FOREST_DARK)
        canvas.rect(0, 0, PAGE_WIDTH, 14 * mm, stroke=0, fill=1)
        canvas.setFillColor(colors.white)
        canvas.setFont(self.fonts.sans_bold, 7.2)
        canvas.drawCentredString(PAGE_WIDTH / 2, 5.1 * mm, "NOVALITY CROCHET STUDIO  ·  ORIGINAL PATTERN")
        canvas.restoreState()


class CollectionClosingPanel(Flowable):
    """Light interior-style closing panel."""

    def __init__(self, spec: PatternSpec, width: float, fonts: Fonts):
        super().__init__()
        self.spec = spec
        self.fonts = fonts
        self.width = width
        self.height = 172 * mm

    def wrap(self, available_width, available_height):  # noqa: ANN001
        return min(self.width, available_width), min(self.height, available_height)

    def draw(self) -> None:
        canvas = self.canv
        canvas.saveState()
        canvas.setFillColor(PALE_GREEN)
        canvas.setStrokeColor(HexColor("#76836A"))
        canvas.setLineWidth(0.8)
        canvas.roundRect(0, 19 * mm, self.width, 144 * mm, 5 * mm, stroke=1, fill=1)
        center = self.width / 2
        canvas.setFillColor(HexColor(self.spec.palette[0].colour))
        canvas.circle(center, 139 * mm, 14 * mm, stroke=0, fill=1)
        canvas.setFillColor(contrasting_pdf_colour(self.spec.palette[0].colour))
        canvas.setFont(self.fonts.sans_bold, 12)
        canvas.drawCentredString(center, 136.4 * mm, self.spec.code)
        canvas.setFillColor(FOREST_DARK)
        canvas.setFont(self.fonts.serif_bold, 25)
        canvas.drawCentredString(center, 111 * mm, "HAPPY CROCHETING")
        canvas.setFont(self.fonts.serif, 11.5)
        canvas.drawCentredString(center, 99 * mm, "Make it slowly. Check every count. Make it yours.")
        canvas.setStrokeColor(GINGER_LIGHT)
        canvas.setLineWidth(1.2)
        canvas.line(36 * mm, 88 * mm, self.width - 36 * mm, 88 * mm)
        canvas.setFillColor(INK)
        canvas.setFont(self.fonts.sans_bold, 8.2)
        canvas.drawCentredString(center, 76 * mm, "SHARE YOUR FINISHED PROJECT")
        hashtag = "#" + re.sub(r"[^A-Za-z0-9]", "", self.spec.title)
        canvas.setFont(self.fonts.sans, 7.8)
        canvas.drawCentredString(center, 67 * mm, f"#NovalityCrochetStudio   ·   {hashtag}")
        canvas.setFillColor(MUTED)
        canvas.setFont(self.fonts.sans, 7.3)
        canvas.drawCentredString(center, 50 * mm, "Keep this design code with support questions and pattern revisions.")
        canvas.setFillColor(FOREST_DARK)
        canvas.setFont(self.fonts.sans_bold, 8)
        canvas.drawCentredString(center, 39 * mm, BRAND.upper())
        canvas.setFont(self.fonts.sans, 7)
        canvas.drawCentredString(center, 29 * mm, f"© 2026 {BRAND} · ALL RIGHTS RESERVED · {self.spec.code}")
        canvas.restoreState()


class PrinterCover(Flowable):
    """Black-on-white collection cover for a printer-saver companion."""

    def __init__(self, spec: PatternSpec, fonts: Fonts):
        super().__init__()
        self.spec = spec
        self.fonts = fonts
        self.width = PAGE_WIDTH
        self.height = PAGE_HEIGHT - 0.2 * mm

    def wrap(self, available_width, available_height):  # noqa: ANN001
        return self.width, min(self.height, available_height)

    def draw(self) -> None:
        canvas = self.canv
        spec = self.spec
        canvas.saveState()
        canvas.setFillColor(colors.white)
        canvas.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, stroke=0, fill=1)
        canvas.setStrokeColor(colors.black)
        canvas.setLineWidth(0.8)
        canvas.rect(14 * mm, 14 * mm, PAGE_WIDTH - 28 * mm, PAGE_HEIGHT - 28 * mm, stroke=1, fill=0)
        canvas.setFillColor(colors.black)
        canvas.setFont(self.fonts.sans_bold, 9)
        canvas.drawString(20 * mm, PAGE_HEIGHT - 25 * mm, BRAND.upper())
        canvas.setFont(self.fonts.sans, 8)
        canvas.drawRightString(PAGE_WIDTH - 20 * mm, PAGE_HEIGHT - 25 * mm, "PRINTER-SAVER EDITION")
        canvas.line(20 * mm, PAGE_HEIGHT - 31 * mm, PAGE_WIDTH - 20 * mm, PAGE_HEIGHT - 31 * mm)
        canvas.setFont(self.fonts.sans_bold, 11)
        canvas.drawString(20 * mm, 235 * mm, f"DESIGN CODE {spec.code}")
        y = 213 * mm
        for line in spec.cover_lines:
            draw_fitted_text(canvas, self.fonts.serif_bold, line, 20 * mm, y, 165 * mm, 31, 18)
            y -= 14 * mm
        draw_fitted_text(canvas, self.fonts.serif, spec.subtitle, 20 * mm, y, 165 * mm, 19, 12)
        canvas.line(20 * mm, y - 10 * mm, 100 * mm, y - 10 * mm)
        canvas.setFont(self.fonts.sans_bold, 9.5)
        canvas.drawString(20 * mm, 150 * mm, "BLACK + WHITE · WHITE BACKGROUNDS · PROGRESS BOXES")
        canvas.setFont(self.fonts.sans, 8.5)
        canvas.drawString(20 * mm, 139 * mm, f"{spec.identity} · {spec.skill} · {spec.time} · {spec.size}")
        canvas.drawString(20 * mm, 131 * mm, spec.yarn_hook)
        canvas.rect(20 * mm, 91 * mm, PAGE_WIDTH - 40 * mm, 27 * mm, stroke=1, fill=0)
        canvas.setFont(self.fonts.sans_bold, 8.3)
        canvas.drawString(25 * mm, 109 * mm, "NAMED ORIGINAL COLOURWAY")
        canvas.setFont(self.fonts.sans, 7.6)
        for index, line in enumerate(wrap_words(spec.palette_summary, 95).splitlines()[:2]):
            canvas.drawString(25 * mm, (100 - index * 6) * mm, line)
        canvas.setFont(self.fonts.sans_bold, 8.3)
        canvas.drawString(20 * mm, 72 * mm, "ABOUT THIS COMPANION FILE")
        canvas.setFont(self.fonts.sans, 8)
        canvas.drawString(20 * mm, 62 * mm, "Designed for economical home printing and progress tracking.")
        canvas.drawString(20 * mm, 54 * mm, "Large artwork is omitted; the written directions match the full-colour edition.")
        canvas.line(20 * mm, 42 * mm, PAGE_WIDTH - 20 * mm, 42 * mm)
        canvas.setFont(self.fonts.sans, 7)
        canvas.drawString(20 * mm, 33 * mm, f"© 2026 {BRAND} · All rights reserved")
        canvas.drawRightString(PAGE_WIDTH - 20 * mm, 33 * mm, "PERSONAL LICENSE · SEE TERMS")
        canvas.setFont(self.fonts.sans_bold, 7)
        canvas.drawCentredString(PAGE_WIDTH / 2, 23 * mm, f"{spec.code} · PRINTER-SAVER CROCHET PATTERN")
        canvas.restoreState()


class PrinterNotesPanel(Flowable):
    """Low-ink project checklist and ruled notes area."""

    def __init__(self, spec: PatternSpec, width: float, fonts: Fonts):
        super().__init__()
        self.spec = spec
        self.fonts = fonts
        self.width = width
        self.height = 228 * mm

    def wrap(self, available_width, available_height):  # noqa: ANN001
        return min(self.width, available_width), min(self.height, available_height)

    def draw(self) -> None:
        canvas = self.canv
        canvas.saveState()
        canvas.setFillColor(colors.black)
        canvas.setFont(self.fonts.serif_bold, 22)
        canvas.drawString(0, 211 * mm, "Finish checklist & notes")
        canvas.setFont(self.fonts.sans, 8.5)
        checks = (
            "[ ] Every row count checked before moving on",
            "[ ] Gauge, dimensions and selected version confirmed",
            "[ ] Face and internal ends completed before closure",
            "[ ] Components counted and pinned before attachment",
            "[ ] Structural seams and hanging points checked twice",
            "[ ] All yarn ends, knots and attachments inspected",
        )
        y = 196 * mm
        for check in checks:
            canvas.drawString(2 * mm, y, check)
            y -= 9 * mm
        canvas.setFont(self.fonts.sans_bold, 9)
        canvas.drawString(0, 132 * mm, "PROJECT NOTES")
        canvas.setStrokeColor(HexColor("#777777"))
        canvas.setLineWidth(0.45)
        for index in range(12):
            line_y = (122 - index * 9) * mm
            canvas.line(0, line_y, self.width, line_y)
        canvas.setFont(self.fonts.sans, 7)
        canvas.setFillColor(colors.black)
        canvas.drawString(0, 7 * mm, f"{BRAND} · {self.spec.code} · printer-saver companion")
        canvas.drawRightString(self.width, 7 * mm, "Keep this page with your project notes")
        canvas.restoreState()


class CollectionDocument(BaseDocTemplate):
    """A4 template with collection identity, bookmarks, and metadata."""

    def __init__(self, filename: Path, spec: PatternSpec, fonts: Fonts, *, printer_saver: bool = False):
        subject = "Printer-saver crochet pattern" if printer_saver else "Branded crochet pattern"
        super().__init__(
            str(filename),
            pagesize=A4,
            leftMargin=18 * mm,
            rightMargin=18 * mm,
            topMargin=22 * mm,
            bottomMargin=18 * mm,
            title=f"{spec.code} — {spec.title}",
            author=BRAND,
            subject=f"{subject} · {spec.code}",
            creator=BRAND,
        )
        self.spec = spec
        self.fonts = fonts
        self.printer_saver = printer_saver
        cover_frame = Frame(0, 0, PAGE_WIDTH, PAGE_HEIGHT, id="cover", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        content_frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="content", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates(
            [
                PageTemplate(id="Cover", frames=[cover_frame], onPage=self.draw_cover_meta),
                PageTemplate(id="Content", frames=[content_frame], onPage=self.draw_content_page),
            ]
        )

    def set_metadata(self, canvas) -> None:  # noqa: ANN001
        subject = "Printer-saver crochet pattern" if self.printer_saver else "Branded crochet pattern"
        canvas.setTitle(f"{self.spec.code} — {self.spec.title}")
        canvas.setAuthor(BRAND)
        canvas.setSubject(f"{subject} · {self.spec.code}")
        canvas.setCreator(BRAND)
        canvas.setKeywords(f"crochet, pattern, {self.spec.code}, {self.spec.title}, {BRAND}")

    def draw_cover_meta(self, canvas, doc) -> None:  # noqa: ANN001
        self.set_metadata(canvas)

    def draw_content_page(self, canvas, doc) -> None:  # noqa: ANN001
        self.set_metadata(canvas)
        canvas.saveState()
        y = PAGE_HEIGHT - 13 * mm
        line_colour = HexColor("#777777") if self.printer_saver else LINE
        primary = colors.black if self.printer_saver else FOREST_DARK
        accent = colors.black if self.printer_saver else GINGER
        canvas.setStrokeColor(line_colour)
        canvas.setLineWidth(0.5)
        canvas.line(18 * mm, y - 3.2 * mm, PAGE_WIDTH - 18 * mm, y - 3.2 * mm)
        canvas.setFillColor(primary)
        canvas.setFont(self.fonts.sans_bold, 7.2)
        canvas.drawString(18 * mm, y, BRAND.upper())
        canvas.setFillColor(accent)
        edition = " · PRINTER SAVER" if self.printer_saver else ""
        canvas.drawRightString(PAGE_WIDTH - 18 * mm, y, f"DESIGN CODE {self.spec.code}{edition}")
        canvas.setStrokeColor(line_colour)
        canvas.line(18 * mm, 12.5 * mm, PAGE_WIDTH - 18 * mm, 12.5 * mm)
        canvas.setFillColor(HexColor("#444444") if self.printer_saver else MUTED)
        canvas.setFont(self.fonts.sans, 6.6)
        canvas.drawString(18 * mm, 7.2 * mm, f"© 2026 {BRAND} · All rights reserved")
        canvas.drawCentredString(PAGE_WIDTH / 2, 7.2 * mm, "PERSONAL LICENSE · SEE TERMS")
        canvas.setFont(self.fonts.sans_bold, 7)
        canvas.drawRightString(PAGE_WIDTH - 18 * mm, 7.2 * mm, f"{self.spec.code}   ·   {doc.page}")
        canvas.restoreState()

    def afterFlowable(self, flowable: Flowable) -> None:
        if isinstance(flowable, HeadingParagraph):
            self.canv.bookmarkPage(flowable.bookmark_key)
            self.canv.addOutlineEntry(
                flowable.plain_heading,
                flowable.bookmark_key,
                level=flowable.outline_level,
                closed=False,
            )
            if flowable.outline_level == 0:
                self.notify(
                    "TOCEntry",
                    (
                        flowable.outline_level,
                        flowable.plain_heading,
                        self.page,
                        flowable.bookmark_key,
                    ),
                )


def palette_table(
    spec: PatternSpec,
    styles: dict[str, ParagraphStyle],
    available_width: float,
    *,
    printer_saver: bool,
) -> Table:
    count = len(spec.palette)
    width = available_width / count
    font_size = 6.5 if count >= 5 else 7.1
    label_style = ParagraphStyle(
        f"Palette-{spec.number}-{'print' if printer_saver else 'colour'}",
        parent=styles["small"],
        fontSize=font_size,
        leading=font_size + 2.4,
        textColor=colors.black if printer_saver else MUTED,
    )
    cells = [Paragraph(f"<b>{entry.name}</b><br/>{entry.use}", label_style) for entry in spec.palette]
    if printer_saver:
        table = Table([cells], colWidths=[width] * count)
        table.setStyle(
            TableStyle(
                [
                    ("BOX", (0, 0), (-1, -1), 0.7, HexColor("#777777")),
                    ("INNERGRID", (0, 0), (-1, -1), 0.45, HexColor("#777777")),
                    ("BACKGROUND", (0, 0), (-1, -1), colors.white),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 6),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                    ("TOPPADDING", (0, 0), (-1, -1), 7),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ]
            )
        )
        return table

    table = Table([["" for _ in spec.palette], cells], colWidths=[width] * count, rowHeights=[12 * mm, None])
    commands: list[tuple] = [
        ("BOX", (0, 0), (-1, -1), 0.7, LINE),
        ("INNERGRID", (0, 0), (-1, -1), 0.45, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 1), (-1, 1), HexColor("#FAF6EF")),
        ("LEFTPADDING", (0, 1), (-1, -1), 6),
        ("RIGHTPADDING", (0, 1), (-1, -1), 6),
        ("TOPPADDING", (0, 1), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 7),
    ]
    for index, entry in enumerate(spec.palette):
        commands.append(("BACKGROUND", (index, 0), (index, 0), HexColor(entry.colour)))
    table.setStyle(TableStyle(commands))
    return table


def facts_table(spec: PatternSpec, styles: dict[str, ParagraphStyle], *, printer_saver: bool) -> Table:
    values = (
        ("FORMAT", spec.identity),
        ("SKILL LEVEL", spec.skill),
        ("ACTIVE TIME", spec.time),
        ("FINISHED SIZE", spec.size),
    )
    data = [[Paragraph(f"<b>{label}</b><br/>{value}", styles["body_compact"]) for label, value in values]]
    table = Table(data, colWidths=[42.5 * mm] * 4)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.white if printer_saver else PALE_GREEN),
                ("BOX", (0, 0), (-1, -1), 0.7, HexColor("#777777") if printer_saver else HexColor("#76836A")),
                ("INNERGRID", (0, 0), (-1, -1), 0.4, HexColor("#777777") if printer_saver else colors.white),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    return table


def profile_story(
    spec: PatternSpec,
    styles: dict[str, ParagraphStyle],
    available_width: float,
    *,
    printer_saver: bool,
) -> list[Flowable]:
    story: list[Flowable] = [
        Paragraph("Pattern profile", styles["front_title"]),
        Paragraph(
            f"<b>{spec.code}</b> is the permanent identity of this pattern. Keep it with every revision, tester note, photograph and support message.",
            styles["front_body"],
        ),
        Spacer(1, 2 * mm),
        facts_table(spec, styles, printer_saver=printer_saver),
        Spacer(1, 4 * mm),
        Paragraph("Named original colourway", styles["h3"]),
        palette_table(spec, styles, available_width, printer_saver=printer_saver),
        Paragraph(
            "Use the written colour names and material roles when selecting yarn; screen and printer appearance varies.",
            styles["caption"],
        ),
    ]
    if printer_saver:
        story.extend(
            [
                Paragraph("Progress tracking", styles["h2"]),
                Paragraph(
                    "Every construction-table row begins with a printable [ ] box. Tick it only after completing the row and confirming the stated count.",
                    styles["front_body"],
                ),
            ]
        )
    else:
        maker_map = image_for_width(spec.maker_map, 164 * mm, 74 * mm)
        maker_map.hAlign = "CENTER"
        story.extend(
            [
                maker_map,
                Paragraph(
                    f"FIGURE 1 · Illustrative maker map for {spec.code}. It supports navigation only; the written directions and counts control.",
                    styles["caption"],
                ),
            ]
        )
    story.extend(
        [
            Paragraph("Read before making", styles["h2"]),
            Paragraph(
                "Read every component and finishing note before beginning. Mark completed rows, confirm the count at each row end, and stop immediately if your count differs. Complete internal eyes, embroidery, knots and joins while the relevant opening remains accessible.",
                styles["front_body"],
            ),
            Paragraph(
                "<b>Safety:</b> this PDF does not claim that a finished item meets any toy or consumer-product standard. Follow the full Safety section and obtain every assessment required for the finished item's intended market and use.",
                styles["callout"],
            ),
            Paragraph(
                f"<b>Copyright notice</b><br/>© 2026 {BRAND}. All rights reserved. Licensed to the purchaser under the Terms of Use in this document. Visuals are illustrative; the written materials, counts and construction directions control.",
                styles["quote"],
            ),
        ]
    )
    return story


def toc_story(styles: dict[str, ParagraphStyle], fonts: Fonts, *, printer_saver: bool) -> list[Flowable]:
    primary = colors.black if printer_saver else FOREST_DARK
    secondary = colors.black if printer_saver else INK
    muted = HexColor("#444444") if printer_saver else MUTED
    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle("CollectionTOC1", fontName=fonts.serif_bold, fontSize=10, leading=15, textColor=primary, leftIndent=0, firstLineIndent=0, spaceBefore=4),
        ParagraphStyle("CollectionTOC2", fontName=fonts.sans, fontSize=8.4, leading=12, textColor=secondary, leftIndent=10, firstLineIndent=0),
        ParagraphStyle("CollectionTOC3", fontName=fonts.sans, fontSize=7.8, leading=11, textColor=muted, leftIndent=20, firstLineIndent=0),
    ]
    return [
        Paragraph("Contents", styles["front_title"]),
        Paragraph(
            "Major sections are listed below; all component headings are bookmarked. Table headers repeat after page breaks, and the design code appears on every page.",
            styles["front_body"],
        ),
        Spacer(1, 4 * mm),
        toc,
        Spacer(1, 7 * mm),
        HRFlowable(width="100%", thickness=0.8, color=HexColor("#777777") if printer_saver else LINE),
        Spacer(1, 5 * mm),
        Paragraph("How to use this pattern", styles["h2"]),
        Paragraph(
            "Read the complete component before beginning it. Move the marker at the start of every crochet round unless the master says otherwise. Diagrams and illustrations support orientation only; the numbered written directions control construction.",
            styles["callout"],
        ),
    ]


def progress_table(rows: Sequence[Sequence[str]]) -> bool:
    if not rows:
        return False
    first = rows[0][0].strip().lower()
    headers = {cell.strip().lower() for cell in rows[0]}
    return first in {"rnd", "round", "row"} and ("sts" in headers or "stitches" in headers)


def table_widths(rows: Sequence[Sequence[str]], available: float) -> list[float]:
    header = [cell.strip().lower() for cell in rows[0]]
    columns = len(header)
    if columns == 5 and "us terms" in header and "uk terms" in header:
        return [available * 0.10, available * 0.30, available * 0.30, available * 0.10, available * 0.20]
    if columns == 5 and header[0] == "size":
        return [available * 0.15, available * 0.20, available * 0.15, available * 0.18, available * 0.32]
    if columns == 4 and "instruction" in header:
        return [available * 0.14, available * 0.49, available * 0.11, available * 0.26]
    if columns == 4 and header[0] == "piece":
        return [available * 0.25, available * 0.14, available * 0.28, available * 0.33]
    if columns == 4:
        return [available * 0.25, available * 0.36, available * 0.17, available * 0.22]
    if columns == 3:
        return [available * 0.18, available * 0.63, available * 0.19]
    if columns == 2:
        return [available * 0.55, available * 0.45]
    return [available / columns] * columns


def make_table(
    spec: PatternSpec,
    rows: Sequence[Sequence[str]],
    styles: dict[str, ParagraphStyle],
    available: float,
    *,
    printer_saver: bool,
) -> Table:
    dense = len(rows[0]) >= 5
    body_style = ParagraphStyle(
        f"TableCell-{spec.number}-{'dense' if dense else 'normal'}-{'print' if printer_saver else 'colour'}",
        parent=styles["table_cell"],
        fontSize=6.35 if dense else 7.25,
        leading=8.15 if dense else 9.5,
        textColor=colors.black if printer_saver else INK,
    )
    first_style = ParagraphStyle(
        f"TableFirst-{spec.number}-{'dense' if dense else 'normal'}-{'print' if printer_saver else 'colour'}",
        parent=body_style,
        fontName=styles["table_cell_bold"].fontName,
    )
    header_style = ParagraphStyle(
        f"TableHead-{spec.number}-{'dense' if dense else 'normal'}-{'print' if printer_saver else 'colour'}",
        parent=styles["table_header"],
        fontSize=6.25 if dense else 7.1,
        leading=7.9 if dense else 9,
        textColor=colors.black if printer_saver else colors.white,
        alignment=TA_LEFT,
    )
    track = progress_table(rows)
    formatted: list[list[Paragraph]] = []
    for row_index, row in enumerate(rows):
        formatted_row = []
        for column_index, cell in enumerate(row):
            display = f"[ ] {cell}" if track and row_index > 0 and column_index == 0 else cell
            style = header_style if row_index == 0 else first_style if column_index == 0 else body_style
            formatted_row.append(Paragraph(inline_markup(display), style))
        formatted.append(formatted_row)

    header_fill = colors.white if printer_saver else FOREST
    header_text = colors.black if printer_saver else colors.white
    grid = HexColor("#777777") if printer_saver else LINE
    row_fills = [colors.white] if printer_saver else [PAPER, HexColor("#F8F3EB")]
    table = Table(formatted, colWidths=table_widths(rows, available), repeatRows=1, hAlign="LEFT", splitByRow=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), header_fill),
                ("TEXTCOLOR", (0, 0), (-1, 0), header_text),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("GRID", (0, 0), (-1, -1), 0.35, grid),
                ("LEFTPADDING", (0, 0), (-1, -1), 4.0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4.0),
                ("TOPPADDING", (0, 0), (-1, -1), 3.7 if dense else 4.1),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3.7 if dense else 4.1),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), row_fills),
                ("LINEBELOW", (0, 0), (-1, 0), 1.0, colors.black if printer_saver else FOREST_DARK),
            ]
        )
    )
    return table


def blocks_to_story(
    spec: PatternSpec,
    blocks: Iterable[Block],
    styles: dict[str, ParagraphStyle],
    available_width: float,
    *,
    printer_saver: bool,
) -> list[Flowable]:
    story: list[Flowable] = []
    current_h2 = ""
    heading_count = 0
    for block in blocks:
        if block.kind == "heading":
            text = str(block.value)
            if text == "Happy crocheting!":
                break
            if block.level == 1:
                continue
            if block.level == 2:
                current_h2 = text
                story.append(CondPageBreak(42 * mm))
            style_key = f"h{min(block.level, 4)}"
            level = max(0, block.level - 2)
            key = f"ns{spec.number:02d}-section-{heading_count}"
            heading_count += 1
            story.append(HeadingParagraph(inline_markup(text), styles[style_key], level, key))
            if text == "Colourways":
                story.extend(
                    [
                        palette_table(spec, styles, available_width, printer_saver=printer_saver),
                        Paragraph(
                            f"NAMED ORIGINAL COLOURWAY · {spec.palette_summary}.",
                            styles["caption"],
                        ),
                    ]
                )
            continue
        if block.kind == "rule":
            rule = HexColor("#777777") if printer_saver else LINE
            story.extend([Spacer(1, 2 * mm), HRFlowable(width="100%", thickness=0.8, color=rule), Spacer(1, 3 * mm)])
            continue
        if block.kind == "quote":
            story.append(Paragraph(inline_markup(str(block.value)), styles["quote"]))
            continue
        if block.kind == "table":
            story.extend(
                [
                    Spacer(1, 2 * mm),
                    make_table(spec, block.value, styles, available_width, printer_saver=printer_saver),
                    Spacer(1, 4 * mm),
                ]
            )
            continue
        if block.kind == "bullet":
            story.append(Paragraph(inline_markup(str(block.value)), styles["bullet"], bulletText="•"))
            continue
        if block.kind == "ordered":
            story.append(Paragraph(inline_markup(str(block.value)), styles["number"], bulletText=f"{block.level}."))
            continue
        if block.kind == "paragraph":
            style = styles["callout"] if current_h2.startswith("Safety") else styles["body"]
            value = str(block.value)
            if current_h2 == "Colourways":
                value = f"<b>Colourway notes:</b> {inline_markup(value)}"
                story.append(Paragraph(value, style))
            else:
                story.append(Paragraph(inline_markup(value), style))
    return story


def expected_progress_rows(blocks: Iterable[Block]) -> int:
    return sum(len(block.value) - 1 for block in blocks if block.kind == "table" and progress_table(block.value))


def expected_outline_titles(blocks: Iterable[Block]) -> list[str]:
    titles = []
    for block in blocks:
        if block.kind != "heading":
            continue
        text = clean_heading(str(block.value))
        if text == "Happy crocheting!":
            break
        if block.level > 1:
            titles.append(text)
    return titles


def build_one(spec: PatternSpec, fonts: Fonts, *, printer_saver: bool) -> tuple[Path, list[Block]]:
    output = spec.printer_output if printer_saver else spec.main_output
    output.parent.mkdir(parents=True, exist_ok=True)
    source_text = normalize_branding(spec.source.read_text(encoding="utf-8"))
    blocks = parse_markdown(source_text)
    styles = make_printer_styles(fonts) if printer_saver else make_styles(fonts)
    document = CollectionDocument(output, spec, fonts, printer_saver=printer_saver)
    story: list[Flowable] = [
        PrinterCover(spec, fonts) if printer_saver else CollectionCover(spec, fonts),
        NextPageTemplate("Content"),
        PageBreak(),
        *profile_story(spec, styles, document.width, printer_saver=printer_saver),
        PageBreak(),
        *toc_story(styles, fonts, printer_saver=printer_saver),
        PageBreak(),
        *blocks_to_story(spec, blocks, styles, document.width, printer_saver=printer_saver),
        PageBreak(),
        PrinterNotesPanel(spec, document.width, fonts)
        if printer_saver
        else CollectionClosingPanel(spec, document.width, fonts),
    ]
    document.multiBuild(story)
    return output, blocks


def flatten_outline(items: Sequence[object]) -> list[str]:
    result: list[str] = []
    for item in items:
        if isinstance(item, list):
            result.extend(flatten_outline(item))
        else:
            result.append(str(getattr(item, "title", item)))
    return result


def image_inventory(reader: PdfReader) -> tuple[set[str], int]:
    hashes: set[str] = set()
    placements = 0
    for page in reader.pages:
        resources = page.get("/Resources")
        if isinstance(resources, IndirectObject):
            resources = resources.get_object()
        xobjects = resources.get("/XObject") if resources else None
        if isinstance(xobjects, IndirectObject):
            xobjects = xobjects.get_object()
        for image in (xobjects or {}).values():
            image = image.get_object()
            if image.get("/Subtype") == "/Image":
                placements += 1
                hashes.add(sha256(image.get_data()).hexdigest())
    return hashes, placements


def canonical_text(value: str) -> str:
    value = unescape(value)
    value = re.sub(r"<[^>]+>", " ", value)
    value = re.sub(r"\*+|`", "", value)
    value = value.replace("×", "x").replace("–", "-").replace("—", "-")
    value = value.replace("’", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", value).strip().casefold()


def block_sentinels(blocks: Iterable[Block]) -> list[str]:
    sentinels: list[str] = []
    for block in blocks:
        if block.kind == "heading":
            value = clean_heading(str(block.value))
            if value == "Happy crocheting!":
                break
            if block.level == 1:
                continue
            sentinels.append(canonical_text(value))
            continue
        values: list[str] = []
        if block.kind == "table":
            for row in block.value[1:]:
                values.extend(str(cell) for cell in row if len(str(cell).strip()) >= 4)
        elif block.kind in {"paragraph", "quote", "bullet", "ordered"}:
            values.append(str(block.value))
        for value in values:
            normalized = canonical_text(value)
            words = normalized.split()
            if not words:
                continue
            if len(words) <= 12:
                sentinels.append(normalized)
            else:
                sentinels.append(" ".join(words[:9]))
                sentinels.append(" ".join(words[-9:]))
    return sentinels


def check_grayscale_vectors(reader: PdfReader, spec: PatternSpec) -> None:
    for page_number, page in enumerate(reader.pages, 1):
        content = ContentStream(page.get_contents(), reader)
        for operands, operator in content.operations:
            if operator in (b"rg", b"RG"):
                channels = [float(value) for value in operands]
                if max(channels) - min(channels) > 0.0001:
                    raise ValueError(f"{spec.code} printer page {page_number} contains colour")
            if operator in (b"k", b"K"):
                cyan, magenta, yellow, _black = [float(value) for value in operands]
                if max(cyan, magenta, yellow) > 0.0001:
                    raise ValueError(f"{spec.code} printer page {page_number} contains CMYK colour")


def postflight(spec: PatternSpec, output: Path, blocks: list[Block], *, printer_saver: bool) -> dict[str, int | float]:
    reader = PdfReader(output, strict=True)
    edition = "printer-saver" if printer_saver else "full-colour"
    if reader.is_encrypted:
        raise ValueError(f"{spec.code} {edition} PDF is encrypted")
    if not 7 <= len(reader.pages) <= 36:
        raise ValueError(f"{spec.code} {edition}: unexpected {len(reader.pages)}-page length")
    limit = 5 * 1024 * 1024 if printer_saver else 20 * 1024 * 1024
    if output.stat().st_size >= limit:
        raise ValueError(f"{spec.code} {edition} PDF exceeds its size gate")
    if reader.metadata.title != f"{spec.code} — {spec.title}":
        raise ValueError(f"{spec.code} {edition}: incorrect title metadata")
    if reader.metadata.author != BRAND:
        raise ValueError(f"{spec.code} {edition}: incorrect author metadata")
    subject = (reader.metadata.subject or "").lower()
    if printer_saver and "printer-saver" not in subject:
        raise ValueError(f"{spec.code}: printer-saver metadata label missing")

    expected_titles = expected_outline_titles(blocks)
    outline_titles = flatten_outline(reader.outline)
    if outline_titles != expected_titles:
        raise ValueError(
            f"{spec.code} {edition}: bookmark mismatch "
            f"({len(outline_titles)} rendered vs {len(expected_titles)} expected)"
        )
    if any("&amp;" in title for title in outline_titles):
        raise ValueError(f"{spec.code} {edition}: escaped entity in bookmarks")

    page_texts = [page.extract_text() or "" for page in reader.pages]
    for page_number, (page, text) in enumerate(zip(reader.pages, page_texts, strict=True), 1):
        if len(text) < 220:
            raise ValueError(f"{spec.code} {edition}: page {page_number} is unexpectedly empty")
        if spec.code.casefold() not in text.casefold():
            raise ValueError(f"{spec.code} {edition}: page {page_number} lacks design code")
        if BRAND.casefold() not in text.casefold():
            raise ValueError(f"{spec.code} {edition}: page {page_number} lacks brand")
        if abs(float(page.mediabox.width) - 595.28) >= 1 or abs(float(page.mediabox.height) - 841.89) >= 1:
            raise ValueError(f"{spec.code} {edition}: page {page_number} is not A4")

    all_text = "\n".join(page_texts)
    normalized_pdf = canonical_text(all_text)
    if "novality store" in normalized_pdf:
        raise ValueError(f"{spec.code} {edition}: legacy brand remains")
    if "**" in all_text or "|---" in all_text:
        raise ValueError(f"{spec.code} {edition}: raw Markdown leaked")
    for marker in ("confirmation proof", "not for retail", "do not distribute"):
        if marker in normalized_pdf:
            raise ValueError(f"{spec.code} {edition}: proof-only marker remains")
    for entry in spec.palette:
        if canonical_text(entry.name) not in normalized_pdf:
            raise ValueError(f"{spec.code} {edition}: colour name missing: {entry.name}")
    for sentinel in block_sentinels(blocks):
        if sentinel and sentinel not in normalized_pdf:
            raise ValueError(f"{spec.code} {edition}: source content sentinel missing: {sentinel!r}")

    expected_boxes = expected_progress_rows(blocks)
    actual_boxes = all_text.count("[ ]")
    expected_actual = expected_boxes + (7 if printer_saver else 0)
    if actual_boxes != expected_actual:
        raise ValueError(
            f"{spec.code} {edition}: progress boxes {actual_boxes}, expected {expected_actual}"
        )

    image_hashes, placements = image_inventory(reader)
    if printer_saver:
        if image_hashes or placements:
            raise ValueError(f"{spec.code}: printer-saver contains raster images")
        check_grayscale_vectors(reader, spec)
    elif len(image_hashes) != 2 or placements != 2:
        raise ValueError(
            f"{spec.code}: expected exactly 2 distinct raster visuals / placements, "
            f"found {len(image_hashes)} / {placements}"
        )

    result: dict[str, int | float] = {
        "pages": len(reader.pages),
        "bytes": output.stat().st_size,
        "boxes": actual_boxes,
        "bookmarks": len(outline_titles),
        "images": len(image_hashes),
    }
    print(
        f"{spec.code} {edition} postflight: PASS — {result['pages']} A4 pages, "
        f"{result['bytes'] / 1024 / 1024:.2f} MiB, {result['boxes']} progress boxes, "
        f"{result['bookmarks']} bookmarks, {result['images']} raster images"
    )
    return result


def create_bundle(specs: Sequence[PatternSpec]) -> Path:
    BUNDLE_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(BUNDLE_OUTPUT, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for spec in specs:
            archive.write(spec.main_output, arcname=spec.main_output.name)
            archive.write(spec.printer_output, arcname=spec.printer_output.name)
    with zipfile.ZipFile(BUNDLE_OUTPUT) as archive:
        expected = {path.name for spec in specs for path in (spec.main_output, spec.printer_output)}
        if set(archive.namelist()) != expected:
            raise ValueError("Collection ZIP inventory mismatch")
        bad = archive.testzip()
        if bad:
            raise ValueError(f"Collection ZIP CRC failure: {bad}")
    if BUNDLE_OUTPUT.stat().st_size >= 20 * 1024 * 1024:
        raise ValueError("Collection ZIP exceeds 20 MiB")
    print(
        f"Bundle postflight: PASS — {len(specs) * 2} PDFs, "
        f"{BUNDLE_OUTPUT.stat().st_size / 1024 / 1024:.2f} MiB"
    )
    return BUNDLE_OUTPUT


def selected_specs(value: str) -> tuple[PatternSpec, ...]:
    wanted: set[int] = set()
    for part in value.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start, end = (int(item) for item in part.split("-", 1))
            wanted.update(range(start, end + 1))
        else:
            wanted.add(int(part))
    available = {spec.number: spec for spec in SPECS}
    unknown = wanted - available.keys()
    if unknown:
        raise ValueError(f"Unsupported design codes: {sorted(unknown)}")
    return tuple(available[number] for number in sorted(wanted))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--codes",
        default="2-15",
        help="Comma-separated numbers/ranges to build (default: 2-15)",
    )
    parser.add_argument("--skip-printer-savers", action="store_true")
    parser.add_argument("--skip-bundle", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    specs = selected_specs(args.codes)
    fonts = register_fonts()
    for spec in specs:
        if not spec.source.exists():
            raise FileNotFoundError(f"Missing audited master: {spec.source}")
        ensure_visual_assets(spec)
        main_output, blocks = build_one(spec, fonts, printer_saver=False)
        postflight(spec, main_output, blocks, printer_saver=False)
        if not args.skip_printer_savers:
            printer_output, printer_blocks = build_one(spec, fonts, printer_saver=True)
            postflight(spec, printer_output, printer_blocks, printer_saver=True)
    if not args.skip_bundle and not args.skip_printer_savers and len(specs) == len(SPECS):
        print(create_bundle(specs))
    for spec in specs:
        print(spec.main_output)
        if not args.skip_printer_savers:
            print(spec.printer_output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
