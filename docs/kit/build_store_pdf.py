"""Generic Novality Store edition PDF compiler (colour + ink-saver BW).

Reads a corrected master markdown file plus a small SPEC and produces the
store-edition PDF with the standing furniture: white ink-friendly cover with
framed illustrative render + disclosure chip, a linked contents page and PDF
bookmarks, a fail-closed verification badge, running page stamps, copyright,
and appendices with an assembly map, count chart, count ladder and live checks.

Usage:  python build_store_pdf.py <spec.py> [--bw]
"""
import hashlib
import importlib.util
import io
import math
import os
import re
import shutil
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path, PurePosixPath
from xml.sax.saxutils import escape

from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, PageBreak, CondPageBreak,
                                KeepTogether, Flowable)
from reportlab.platypus.tableofcontents import TableOfContents

KIT = Path(__file__).resolve().parent
sys.path.insert(0, str(KIT))
sys.path.insert(0, str(KIT.parents[1] / "src"))
import audit_lib  # noqa: E402

pdfmetrics.registerFont(TTFont("DJ", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DJ-B", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DS", "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"))
pdfmetrics.registerFont(TTFont("DS-B", "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"))
registerFontFamily("DJ", normal="DJ", bold="DJ-B", italic="DJ", boldItalic="DJ-B")

W, H = letter
M = 0.6 * inch
CW = W - 2 * M

ASSET_BUNDLE_URL = (
    "https://github.com/arbabkhan007/Crochet-Pattern-Checker/releases/download/"
    "novality-pattern-assets-v1/novality-pattern-hero-assets-v1.zip"
)
ASSET_BUNDLE_SHA256_URL = (
    "https://github.com/arbabkhan007/Crochet-Pattern-Checker/releases/download/"
    "novality-pattern-assets-v1/novality-pattern-hero-assets-v1.sha256"
)
ASSET_CACHE_DEFAULT = Path.home() / ".cache" / "novality-pattern-assets-v1"
ASSET_PATH_RE = re.compile(r"docs/ns[0-9]{2}/assets/[^/]+\.png")


def resolve_hero_asset(asset_path):
    """Resolve a hero image from the checkout, an override, or the release ZIP."""
    requested_text = os.fspath(asset_path)
    if not isinstance(requested_text, str) or "\\" in requested_text or "\0" in requested_text:
        raise ValueError(f"Hero path must be a safe relative path: {asset_path}")
    requested = Path(requested_text)
    if ".." in requested.parts:
        raise ValueError(f"Hero path must not traverse parent directories: {asset_path}")
    repo_root = KIT.parents[1].resolve()
    if requested.is_absolute():
        try:
            requested = requested.resolve(strict=False).relative_to(repo_root)
        except ValueError:
            # Preserve the builder's previous support for an existing absolute
            # hero file, while only remapping missing assets from this checkout.
            if requested.is_file():
                return requested
            raise ValueError(
                f"Missing absolute hero path is outside the project checkout: {asset_path}"
            )

    # Resolve from the project root as well as the current directory. This keeps
    # builds working when invoked outside the repository root.
    for candidate in (requested, repo_root / requested):
        if candidate.is_file():
            return candidate

    external_root = os.environ.get("NOVALITY_PATTERN_ASSET_DIR")
    if external_root:
        external_path = Path(external_root).expanduser() / requested
        if external_path.is_file():
            return external_path

    cache_root = Path(
        os.environ.get("NOVALITY_PATTERN_ASSET_CACHE", ASSET_CACHE_DEFAULT)
    ).expanduser()
    cached_path = cache_root / requested
    marker = cache_root / ".bundle-ready"
    if marker.is_file():
        try:
            installed_hash = marker.read_text(encoding="ascii").strip()
        except OSError:
            installed_hash = ""
        if re.fullmatch(r"[0-9a-fA-F]{64}", installed_hash) and cached_path.is_file():
            return cached_path
        marker.unlink(missing_ok=True)

    bundle_url = os.environ.get("NOVALITY_PATTERN_ASSET_BUNDLE_URL", ASSET_BUNDLE_URL)
    checksum_url = os.environ.get(
        "NOVALITY_PATTERN_ASSET_SHA256_URL", ASSET_BUNDLE_SHA256_URL
    )
    cache_root.mkdir(parents=True, exist_ok=True)
    archive_path = None
    try:
        with urllib.request.urlopen(checksum_url, timeout=30) as response:
            checksum_text = response.read(4096).decode("ascii").strip()
        checksum_fields = checksum_text.split()
        if not checksum_fields:
            raise ValueError("The release checksum file is empty.")
        expected_hash = checksum_fields[0]
        if not re.fullmatch(r"[0-9a-fA-F]{64}", expected_hash):
            raise ValueError("The release checksum file is not a SHA-256 digest.")

        with tempfile.NamedTemporaryFile(
            prefix="novality-assets-", suffix=".zip", dir=cache_root, delete=False
        ) as temp_archive:
            archive_path = Path(temp_archive.name)
            with urllib.request.urlopen(bundle_url, timeout=60) as response:
                shutil.copyfileobj(response, temp_archive)

        digest = hashlib.sha256()
        with archive_path.open("rb") as archive_file:
            for chunk in iter(lambda: archive_file.read(1024 * 1024), b""):
                digest.update(chunk)
        if digest.hexdigest().lower() != expected_hash.lower():
            raise ValueError("Downloaded hero-art bundle failed its SHA-256 check.")

        with zipfile.ZipFile(archive_path) as archive:
            extracted_count = 0
            for member in archive.infolist():
                if "\\" in member.filename or "\0" in member.filename:
                    raise ValueError("Asset bundle contains an unsafe archive path.")
                path = PurePosixPath(member.filename)
                if path.is_absolute() or ".." in path.parts:
                    raise ValueError("Asset bundle contains an unsafe archive path.")
                if member.is_dir() or not ASSET_PATH_RE.fullmatch(path.as_posix()):
                    continue
                extracted_count += 1
                destination = cache_root.joinpath(*path.parts)
                destination.parent.mkdir(parents=True, exist_ok=True)
                temp_path = None
                try:
                    with archive.open(member) as source, tempfile.NamedTemporaryFile(
                        prefix=f".{destination.name}.", dir=destination.parent, delete=False
                    ) as temp_file:
                        temp_path = Path(temp_file.name)
                        shutil.copyfileobj(source, temp_file)
                    temp_path.replace(destination)
                finally:
                    if temp_path is not None:
                        temp_path.unlink(missing_ok=True)
            if not extracted_count:
                raise ValueError("The release ZIP contains no hero PNG assets.")

        marker_temp = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", encoding="ascii", prefix=".bundle-ready.",
                dir=cache_root, delete=False
            ) as marker_file:
                marker_temp = Path(marker_file.name)
                marker_file.write(expected_hash.lower() + "\n")
            marker_temp.replace(marker)
        finally:
            if marker_temp is not None:
                marker_temp.unlink(missing_ok=True)

        if cached_path.is_file():
            return cached_path
        raise FileNotFoundError(
            f"Hero asset {requested} is missing from the downloaded release bundle."
        )
    except Exception as exc:
        raise FileNotFoundError(
            f"Cannot load hero image {requested}. Confirm the GitHub Release asset is "
            f"available, or set NOVALITY_PATTERN_ASSET_DIR to an extracted bundle. "
            f"Details: {exc}"
        ) from exc
    finally:
        if archive_path is not None:
            archive_path.unlink(missing_ok=True)


def load_spec(path):
    spec = importlib.util.spec_from_file_location("spec", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.SPEC


def palette(bw):
    if bw:
        return dict(FOREST="#000000", FOREST_DK="#000000", FOREST_MID="#222222",
                    CREAM="#000000", OAT="#444444", CREAM_ROW="#F2F2F2",
                    GREEN_ROW="#FFFFFF", GOLD="#333333", GOLD_DK="#222222",
                    BERRY="#000000", BERRY_LT="#FFFFFF", INK="#000000",
                    GREY="#222222", PAPER="#FFFFFF", RULE="#333333")
    return dict(FOREST="#1E5B3A", FOREST_DK="#123B25", FOREST_MID="#2E7A50",
                CREAM="#F6EDDA", OAT="#E7D7B8", CREAM_ROW="#F4EAD3",
                GREEN_ROW="#EFF5EE", GOLD="#C9A227", GOLD_DK="#9A7B14",
                BERRY="#9E2B25", BERRY_LT="#F7E7E5", INK="#22312A",
                GREY="#5C6B62", PAPER="#FFFDF8", RULE="#D8CDB6")


def md(s):
    s = escape(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"<i>\1</i>", s)
    s = s.replace("·", "&middot;").replace("—", "&mdash;").replace("–", "&ndash;")
    s = s.replace("✓", "&#10003;").replace("’", "&rsquo;").replace("‘", "&lsquo;")
    s = s.replace("“", "&ldquo;").replace("”", "&rdquo;")
    return s


class Doc(BaseDocTemplate):
    def __init__(self, path, spec, P, bw, verification_ok=False, **kw):
        super().__init__(path, pagesize=letter, leftMargin=M, rightMargin=M,
                         topMargin=0.62 * inch, bottomMargin=0.62 * inch, **kw)
        self.spec, self.P, self.bw = spec, P, bw
        self.verification_ok = verification_ok
        self._heading_index = 0
        self.addPageTemplates([PageTemplate("body",
                            [Frame(M, 0.62 * inch, CW, H - 1.24 * inch, id="F")],
                            onPage=self.furniture)])

    def beforeDocument(self):
        self._heading_index = 0
        title = self.spec.get("title", "Crochet Pattern")
        code = self.spec.get("code", "")
        self.canv.setTitle(f"{title} | Crochet Pattern")
        self.canv.setAuthor("Novality Store")
        self.canv.setSubject(f"US-terms crochet pattern {code}".strip())
        self.canv.setCreator("Novality Store Premium Pattern Publisher")
        self.canv.setKeywords("crochet, pattern, amigurumi, Novality Store")

    def afterFlowable(self, flowable):
        if not isinstance(flowable, Paragraph):
            return
        level = {"h2": 0, "h3": 1}.get(getattr(flowable.style, "name", ""))
        if level is None:
            return
        title = flowable.getPlainText().strip()
        if not title:
            return
        self._heading_index += 1
        key = f"section-{self._heading_index}"
        self.canv.bookmarkPage(key)
        self.canv.addOutlineEntry(title, key, level=level, closed=False)
        self.notify("TOCEntry", (level, title, self.page, key))

    def furniture(self, cv, doc):
        P, s = self.P, self.spec
        pg = doc.page
        cv.saveState()
        if pg > 1:
            cv.setFillColor(P["FOREST"])
            cv.setFont("DJ-B", 7.6)
            cv.drawString(M, H - 0.34 * inch, f"{s['code']}  ·  {s['title'].upper()}")
            cv.setFillColor(P["INK"])
            cv.setFont("DJ", 6.8)
            cv.drawRightString(W - M, H - 0.34 * inch, "Novality Store · US terms")
            cv.setStrokeColor(P["RULE"])
            cv.setLineWidth(0.8)
            cv.line(M, H - 0.42 * inch, W - M, H - 0.42 * inch)
        cv.setStrokeColor(P["RULE"])
        cv.setLineWidth(0.8)
        cv.line(M, 0.52 * inch, W - M, 0.52 * inch)
        badge = "VERIFIED" if self.verification_ok else "REVIEW REQUIRED"
        stamp = (f"Novality Store  |  {s['code']}  |  Page {pg} of "
                 f"{doc.total_pages}  ·  {badge}")
        cv.setFillColor(P["GREY"] if not self.bw else P["INK"])
        cv.setFont("DJ", 7)
        cv.drawCentredString(W / 2, 0.36 * inch, stamp)
        cv.restoreState()


def styles(P, bw):
    ink = P["INK"]
    return {
        "h2": ParagraphStyle("h2", fontName="DS-B", fontSize=13.5, leading=16.5,
                             textColor=P["FOREST"] if not bw else HexColor("#000000"),
                             spaceBefore=10, spaceAfter=2),
        "h3": ParagraphStyle("h3", fontName="DJ-B", fontSize=9.6, leading=12,
                             textColor=P["FOREST_DK"] if not bw else HexColor("#000000"),
                             spaceBefore=8, spaceAfter=2),
        "h4": ParagraphStyle("h4", fontName="DJ-B", fontSize=8.6, leading=11,
                             textColor=P["GOLD_DK"] if not bw else HexColor("#000000"),
                             spaceBefore=6, spaceAfter=1),
        "body": ParagraphStyle("body", fontName="DJ", fontSize=8.6, leading=11.5,
                               textColor=ink, alignment=TA_JUSTIFY, spaceAfter=4),
        "bullet": ParagraphStyle("bullet", fontName="DJ", fontSize=8.6, leading=11.5,
                                 textColor=ink, leftIndent=10, spaceAfter=2.5),
        "cell": ParagraphStyle("cell", fontName="DJ", fontSize=7.7, leading=10, textColor=ink),
        "cellb": ParagraphStyle("cellb", fontName="DJ-B", fontSize=7.7, leading=10, textColor=ink),
        "head": ParagraphStyle("head", fontName="DJ-B", fontSize=7.7, leading=10,
                               textColor=white if not bw else HexColor("#000000"),
                               alignment=TA_CENTER),
        "cap": ParagraphStyle("cap", fontName="DJ", fontSize=6.8, leading=8.6,
                              textColor=P["GREY"] if not bw else ink),
        "small": ParagraphStyle("small", fontName="DJ", fontSize=7, leading=9, textColor=ink),
    }


def rule(P, bw, thick=1.0):
    t = Table([[""]], colWidths=[CW], rowHeights=[0.6])
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, -1), thick,
                            HexColor(P["FOREST"]) if not bw else HexColor("#000000"))]))
    return t


def section_title(text, S, P, bw):
    return [Paragraph(md(text), S["h2"]), rule(P, bw), Spacer(1, 3)]


def callout(title, body, S, P, bw, accent=None, bg=None):
    accent = accent or (HexColor(P["GOLD"]) if not bw else HexColor("#333333"))
    bg = bg or (HexColor(P["GREEN_ROW"]) if not bw else HexColor("#FFFFFF"))
    t = Table([[Paragraph(f"<b>{md(title)}</b>", S["cellb"])],
               [Paragraph(md(body), S["cell"])]], colWidths=[CW])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("LINEBEFORE", (0, 0), (0, -1), 2.4, accent),
        ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return t


def round_table(rows, S, P, bw, widths=None):
    """rows: list of cell-lists including header."""
    ncol = len(rows[0])
    widths = widths or ([0.30 * inch] + [CW - 0.30 * inch - 0.52 * inch - 0.9 * inch]
                        + [0.52 * inch] + [0.9 * inch] if ncol == 4 else None)
    if widths is None:
        widths = [CW / ncol] * ncol
    data, style = [], [("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                       ("GRID", (0, 0), (-1, -1), 0.4, HexColor(P["RULE"])),
                       ("TOPPADDING", (0, 0), (-1, -1), 4),
                       ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                       ("LEFTPADDING", (0, 0), (-1, -1), 4),
                       ("RIGHTPADDING", (0, 0), (-1, -1), 4)]
    head_bg = HexColor(P["FOREST"]) if not bw else HexColor("#FFFFFF")
    for i, r in enumerate(rows):
        if i == 0:
            data.append([Paragraph(md(c), S["head"]) for c in r])
            style.append(("BACKGROUND", (0, 0), (-1, 0), head_bg))
            if bw:
                style.append(("LINEBELOW", (0, 0), (-1, 0), 0.8, HexColor("#333333")))
            continue
        cells = [Paragraph(md(r[0]), S["cellb"])]
        cells.append(Paragraph(md(r[1]), S["cell"]))
        for c in r[2:]:
            cells.append(Paragraph(md(c), S["cell"]))
        data.append(cells)
        if i % 2 == 0:
            style.append(("BACKGROUND", (0, i), (-1, i),
                          HexColor(P["CREAM_ROW"] if not bw else "#F2F2F2")))
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle(style))
    return t


def plain_table(rows, S, P, bw):
    ncol = len(rows[0])
    data, style = [], [("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                       ("GRID", (0, 0), (-1, -1), 0.4, HexColor(P["RULE"])),
                       ("TOPPADDING", (0, 0), (-1, -1), 4),
                       ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                       ("LEFTPADDING", (0, 0), (-1, -1), 4),
                       ("RIGHTPADDING", (0, 0), (-1, -1), 4)]
    for i, r in enumerate(rows):
        st = S["head"] if i == 0 else S["cell"]
        data.append([Paragraph(md(c), st) for c in r])
        if i == 0:
            style.append(("BACKGROUND", (0, 0), (-1, 0),
                          HexColor(P["FOREST"]) if not bw else HexColor("#FFFFFF")))
            if bw:
                style.append(("LINEBELOW", (0, 0), (-1, 0), 0.8, HexColor("#333333")))
        elif i % 2 == 0:
            style.append(("BACKGROUND", (0, i), (-1, i),
                          HexColor(P["CREAM_ROW"] if not bw else "#F2F2F2")))
    t = Table(data, colWidths=[CW / ncol] * ncol, repeatRows=1)
    t.setStyle(TableStyle(style))
    return t


# ---------------------------------------------------------------- flowables
class ComponentMap(Flowable):
    def __init__(self, boxes, P, bw, width=CW, height=1.15 * inch):
        super().__init__()
        self.boxes, self.P, self.bw = boxes, P, bw
        self.width, self.height = width, height

    def draw(self):
        c, n = self.canv, len(self.boxes)
        bw_, gap = (self.width - (n - 1) * 6) / n, 6
        for i, (title, sub) in enumerate(self.boxes):
            x = i * (bw_ + gap)
            y = self.height - 0.95 * inch
            c.setFillColor(HexColor("#FFFFFF") if self.bw else HexColor(self.P["GREEN_ROW"]))
            c.setStrokeColor(HexColor("#333333") if self.bw else HexColor(self.P["FOREST"]))
            c.setLineWidth(0.5 if self.bw else 0.9)
            c.roundRect(x, y, bw_, 0.95 * inch, 4, fill=1, stroke=1)
            c.setFillColor(HexColor("#FFFFFF") if self.bw else HexColor(self.P["FOREST"]))
            c.rect(x, y + 0.73 * inch, bw_, 0.22 * inch, fill=1, stroke=0)
            if self.bw:
                c.setStrokeColor(HexColor("#333333"))
                c.setLineWidth(0.5)
                c.line(x, y + 0.73 * inch, x + bw_, y + 0.73 * inch)
                c.setFillColor(HexColor("#000000"))
            else:
                c.setFillColor(HexColor(self.P["CREAM"]))
            c.setFont("DJ-B", 7.2)
            c.drawCentredString(x + bw_ / 2, y + 0.80 * inch, title)
            c.setFillColor(HexColor("#000000" if self.bw else self.P["INK"]))
            c.setFont("DJ", 6.4)
            lines = sub.split("\n")
            for j, ln in enumerate(lines[:3]):
                c.drawCentredString(x + bw_ / 2, y + 0.58 * inch - j * 8.4, ln)
            if i < n - 1:
                c.setStrokeColor(HexColor("#222222") if self.bw else HexColor(self.P["GOLD"]))
                c.setLineWidth(1.1)
                c.line(x + bw_ + 0.6, y + 0.47 * inch, x + bw_ + gap - 0.6, y + 0.47 * inch)
                c.drawCentredString(x + bw_ + gap / 2, y + 0.44 * inch, ">")


class CountChart(Flowable):
    def __init__(self, counts, P, bw, width=CW, height=1.6 * inch, zones=()):
        super().__init__()
        self.counts, self.P, self.bw = counts, P, bw
        self.width, self.height, self.zones = width, height, zones

    def draw(self):
        c = self.canv
        n = len(self.counts)
        mx = max(self.counts) or 1
        left, bottom = 18, 10
        plot_w, plot_h = self.width - left - 4, self.height - 26
        c.setStrokeColor(HexColor("#333333") if self.bw else HexColor(self.P["RULE"]))
        c.setLineWidth(0.5)
        c.line(left, bottom, left + plot_w, bottom)
        c.line(left, bottom, left, bottom + plot_h)
        c.setFont("DJ", 6)
        c.setFillColor(HexColor("#000000" if self.bw else self.P["INK"]))
        for v in (0, mx // 2, mx):
            y = bottom + plot_h * v / mx
            c.drawRightString(left - 3, y - 2, str(v))
            if v:
                c.setStrokeColor(HexColor("#CCCCCC"))
                c.setLineWidth(0.3)
                c.line(left, y, left + plot_w, y)
        bw_ = plot_w / n
        for i, v in enumerate(self.counts):
            hgt = plot_h * v / mx
            x = left + i * bw_
            if self.bw:
                c.setFillColor(HexColor("#FFFFFF") if i not in self.zones else HexColor("#999999"))
                c.setStrokeColor(HexColor("#000000"))
                c.setLineWidth(0.6)
                c.rect(x + bw_ * 0.18, bottom, bw_ * 0.64, hgt, fill=1, stroke=1)
            else:
                c.setFillColor(HexColor(self.P["FOREST_MID"]) if i not in self.zones
                               else HexColor(self.P["GOLD"]))
                c.rect(x + bw_ * 0.18, bottom, bw_ * 0.64, hgt, fill=1, stroke=0)
        c.setFillColor(HexColor("#000000" if self.bw else self.P["INK"]))
        c.setFont("DJ", 6.2)
        c.drawString(left, 1, "Stated stitch count per round. "
                              + ("Grey bars = marked zones." if self.bw
                                 else "Gold bars = marked zones."))


# ---------------------------------------------------------------- md parse
def parse_md(text):
    """Yield block tuples: ('h2'|'h3'|'h4'|'p'|'bullet'|'num'|'table'|'callout', payload)."""
    blocks, tbl = [], []
    lines = text.splitlines()

    def flush():
        nonlocal tbl
        if len(tbl) >= 2:
            rows = [r for r in tbl if not all(set(c) <= set("-: ") for c in r)]
            if rows:
                blocks.append(("table", rows))
        tbl = []

    for raw in lines:
        line = raw.rstrip()
        s = line.strip()
        if s.startswith("|"):
            tbl.append([c.strip() for c in s.strip("|").split("|")])
            continue
        if not s:
            if tbl:
                continue  # blank line inside a pasted table
            continue
        flush()
        if s == "---":
            continue
        if s.startswith("# "):
            blocks.append(("title", s[2:].strip()))
        elif s.startswith("#### "):
            blocks.append(("h4", s[5:].strip()))
        elif s.startswith("### "):
            blocks.append(("h3", s[3:].strip()))
        elif s.startswith("## "):
            blocks.append(("h2", s[3:].strip()))
        elif s.startswith("> "):
            blocks.append(("quote", s[2:].strip()))
        elif re.match(r"^-\s+", s):
            blocks.append(("bullet", s[2:].strip()))
        elif re.match(r"^\d+\.\s+", s):
            blocks.append(("num", re.sub(r"^\d+\.\s+", "", s)))
        else:
            blocks.append(("p", s))
    flush()
    return blocks


def is_round_table(rows):
    h = [c.lower() for c in rows[0]]
    return (h and (h[0] in ("rnd", "row") or "rnd" in h[0] or "row" in h[0])
            and any("sts" == c.lower() for c in h))


def main_counts(blocks, spec):
    """Stated counts of the spec's main piece table (for ladder + chart)."""
    want = spec.get("main_section", "").lower()
    cur3 = cur4 = ""
    counts, labels = [], []
    for kind, payload in blocks:
        if kind == "h3":
            cur3, cur4 = payload.lower(), ""
        elif kind == "h4":
            cur4 = payload.lower()
        elif kind == "table" and is_round_table(payload):
            cur = cur3 + " | " + cur4
            if want and want not in cur:
                continue
            hdr = [h.strip().lower() for h in payload[0]]
            i_sts = next((i for i, h in enumerate(hdr) if h in ("sts", "stitch count")), 2)
            for r in payload[1:]:
                m = re.search(r"\((\d+)\)", r[i_sts] if len(r) > i_sts else "")
                if m:
                    counts.append(int(m.group(1)))
                    labels.append(r[0])
            if counts:
                break
    return labels, counts


# ---------------------------------------------------------------- build
def build(spec_path, bw=False):
    spec = load_spec(spec_path)
    P = palette(bw)
    src = Path(spec["md"]).read_text(encoding="utf-8")
    blocks = parse_md(src)
    S = styles(P, bw)
    out = Path(spec["out_bw"] if bw else spec["out"])

    probs, unparsed = audit_lib.audit_tables(src)
    try:
        from crochet_checker.verification import stages as _st
        AX = {"Domain Isolation": len(_st.domain_isolation(src)),
              "Edge Lineage": len(_st.edge_lineage(src)),
              "Open Boundaries": len(_st.open_boundary(src)),
              "Gauge Bounding": len(_st.gauge_band(src))}
    except Exception:
        AX = None
    verification_ok = not probs and not unparsed and AX is not None and not any(AX.values())

    def story():
        st = []
        # ---------------- cover
        st.append(Spacer(1, 4))
        hdr = Table([[Paragraph("<b>NOVALITY STORE</b>", ParagraphStyle(
                        "cv", fontName="DS-B", fontSize=12.2, textColor=P["FOREST"] if not bw
                        else HexColor("#000000"))),
                      Paragraph("· Novality Crochet Studio imprint", S["small"]),
                      Paragraph(f"<b>DESIGN CODE {spec['code'].replace('NS-', 'NS ')}</b>",
                                ParagraphStyle("cvr", fontName="DJ-B", fontSize=8.5,
                                               textColor=P["INK"], alignment=2))]],
                    colWidths=[2.0 * inch, CW - 3.9 * inch, 1.9 * inch])
        hdr.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                                 ("BACKGROUND", (0, 0), (-1, -1),
                                  HexColor(P["GREEN_ROW"]) if not bw else HexColor("#FFFFFF")),
                                 ("LEFTPADDING", (0, 0), (-1, -1), 8),
                                 ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                                 ("TOPPADDING", (0, 0), (-1, -1), 5),
                                 ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                                 ("LINEBELOW", (0, 0), (-1, -1), 1.5,
                                  HexColor(P["GOLD"]) if not bw else HexColor("#000000"))]))
        st.append(hdr)
        st.append(Spacer(1, 10))
        from reportlab.platypus import Image as RLImage
        from PIL import Image as PILImage, ImageOps
        hero = resolve_hero_asset(spec["hero"])
        im = PILImage.open(hero).convert("RGB")
        if bw:
            im = ImageOps.autocontrast(im.convert("L"), cutoff=1).convert("RGB")
        tw, th = CW, 3.45 * inch
        ratio = min(tw / im.width, th / im.height)
        iw, ih = im.width * ratio, im.height * ratio
        if bw:
            hero_image = io.BytesIO()
            im.save(hero_image, format="PNG")
            hero_image.seek(0)
            img = RLImage(hero_image, width=iw, height=ih)
        else:
            img = RLImage(str(hero), width=iw, height=ih)
        frame = Table([[img]], colWidths=[CW], rowHeights=[3.55 * inch])
        frame.setStyle(TableStyle([
            ("ALIGN", (0, 0), (-1, -1), "CENTER"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("BOX", (0, 0), (-1, -1), 1.1, HexColor(P["FOREST"]) if not bw else HexColor("#333333")),
            ("BACKGROUND", (0, 0), (-1, -1), HexColor("#FFFFFF")),
        ]))
        st.append(frame)
        chip = Table([[Paragraph("Illustrative render of the finished design - not a "
                                 "photograph of a sample", S["small"])]],
                     colWidths=[3.4 * inch])
        chip.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), HexColor(P["PAPER"])),
            ("BOX", (0, 0), (-1, -1), 0.7, HexColor(P["GOLD"]) if not bw else HexColor("#333333")),
            ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ]))
        chip.hAlign = "RIGHT"
        st.append(Spacer(1, -0.24 * inch))
        st.append(chip)
        st.append(Spacer(1, 0.34 * inch))
        st.append(Paragraph(md(spec["title"]), ParagraphStyle(
            "t", fontName="DS-B", fontSize=30, leading=33,
            textColor=P["FOREST_DK"] if not bw else HexColor("#000000"))))
        st.append(Paragraph(md(spec["subtitle"]), ParagraphStyle(
            "st", fontName="DJ", fontSize=9.4, leading=12.5, textColor=P["INK"])))
        st.append(Spacer(1, 3))
        st.append(Paragraph(md(spec["tagline"]), ParagraphStyle(
            "tg", fontName="DJ-B", fontSize=7.8, leading=10, textColor=P["GOLD_DK"] if not bw
            else HexColor("#000000"))))
        st.append(Spacer(1, 6))
        badge_label = ("✓ 5-AXIOM CHECKS PASSED" if verification_ok
                       else "REVIEW REQUIRED")
        badge_color = ("#000000" if bw else
                       (P["FOREST"] if verification_ok else P["BERRY"]))
        chips = [Paragraph(f"<b>{md(badge_label)}</b>",
                           ParagraphStyle("bd", fontName="DJ-B", fontSize=7.7,
                                          textColor=HexColor(badge_color)))]
        for c in spec["chips"]:
            chips.append(Paragraph(f"<b>{md(c)}</b>", ParagraphStyle(
                "ch", fontName="DJ-B", fontSize=8, textColor=P["INK"], alignment=TA_CENTER)))
        widths = [pdfmetrics.stringWidth(c.text.replace("<b>", "").replace("</b>", ""),
                                         "DJ-B", 8) + 18 for c in chips]
        tblchips = Table([chips], colWidths=widths)
        tstyle = [("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                  ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                  ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                  ("BOX", (0, 0), (0, 0), 1.3, HexColor(P["FOREST"]) if not bw else HexColor("#000000"))]
        for i in range(len(chips)):
            tstyle.append(("BOX", (i, 0), (i, 0), 1.3 if i == 0 else 0.8,
                           HexColor(P["FOREST"]) if (not bw and i == 0) else HexColor("#333333")))
            tstyle.append(("ROUNDEDCORNERS", (i, 0), (i, 0), 4, 4, 4, 4))
        tblchips.setStyle(TableStyle(tstyle))
        st.append(tblchips)
        st.append(Spacer(1, 8))
        sws = spec.get("swatches", [])
        sw, swcols, cmds = [], [], [("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                                    ("TOPPADDING", (0, 0), (-1, -1), 2),
                                    ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]
        for i, (name, hexv) in enumerate(sws):
            hx = hexv if not bw else ("#000000" if i == 0 else "#FFFFFF")
            sqst = ParagraphStyle(f"sq{i}", parent=S["small"], backColor=HexColor(hx),
                                  borderColor=HexColor("#333333"), borderWidth=0.7,
                                  borderPadding=0, spaceBefore=0, spaceAfter=0, leading=10)
            sw.append(Paragraph("&nbsp;", sqst))
            sw.append(Paragraph(md(name), S["small"]))
            swcols += [14, 1.45 * inch]
            cmds += [("LEFTPADDING", (2 * i, 0), (2 * i, 0), 0),
                     ("RIGHTPADDING", (2 * i, 0), (2 * i, 0), 0),
                     ("LEFTPADDING", (2 * i + 1, 0), (2 * i + 1, 0), 5),
                     ("RIGHTPADDING", (2 * i + 1, 0), (2 * i + 1, 0), 4)]
        sw.append(Paragraph("named original colourway", ParagraphStyle(
            "swr", fontName="DJ", fontSize=6.8, textColor=P["GREY"] if not bw else P["INK"],
            alignment=2)))
        swcols.append(max(CW - sum(swcols), 0.5 * inch))
        swt = Table([sw], colWidths=swcols)
        swt.setStyle(TableStyle(cmds))
        st.append(swt)
        st.append(Spacer(1, 8))
        cards = spec.get("cards", [])
        cdata, cstyle = [], [("VALIGN", (0, 0), (-1, -1), "TOP"),
                             ("GRID", (0, 0), (-1, -1), 0.6,
                              HexColor(P["FOREST"]) if not bw else HexColor("#333333")),
                             ("LEFTPADDING", (0, 0), (-1, -1), 6),
                             ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                             ("TOPPADDING", (0, 0), (-1, -1), 5),
                             ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]
        cdata.append([Paragraph(f"<b>{md(c[0])}</b>", S["cellb"]) for c in cards])
        cstyle.append(("LINEBELOW", (0, 0), (-1, 0), 0.9,
                       HexColor(P["FOREST"]) if not bw else HexColor("#000000")))
        cdata.append([Paragraph("<br/>".join(md(x) for x in c[1]), S["cell"]) for c in cards])
        ct = Table(cdata, colWidths=[CW / len(cards)] * len(cards), rowHeights=[None, 1.05 * inch])
        ct.setStyle(TableStyle(cstyle))
        st.append(ct)
        st.append(Spacer(1, 10))
        st.append(Paragraph(md(spec["cover_note_title"]), ParagraphStyle(
            "cnt", fontName="DJ-B", fontSize=8.6, textColor=P["INK"], alignment=TA_CENTER)))
        st.append(Paragraph(md(spec["cover_note"]), ParagraphStyle(
            "cn", fontName="DJ", fontSize=7.8, leading=10.2, textColor=P["INK"],
            alignment=TA_CENTER)))
        st.append(Spacer(1, 12))
        st.append(rule(P, bw, 1.4))
        st.append(Paragraph("© 2026 Novality Store. All rights reserved. Published under the "
                            "Novality Crochet Studio imprint.",
                            ParagraphStyle("cp", fontName="DJ", fontSize=7.4, textColor=P["INK"],
                                           alignment=TA_CENTER)))
        st.append(Paragraph("Personal &amp; small-batch finished-item licence · Design Code "
                            f"{spec['code']} · Independent checks: "
                            f"{'PASS' if verification_ok else 'REVIEW REQUIRED'}",
                            ParagraphStyle("cp2", fontName="DJ", fontSize=6.8,
                                           textColor=P["GREY"] if not bw else P["INK"],
                                           alignment=TA_CENTER)))
        st.append(Paragraph("Cover artwork is an illustrative render of the written design - "
                            "not a photograph of a sample.",
                            ParagraphStyle("cp3", fontName="DJ", fontSize=6.8,
                                           textColor=P["GREY"] if not bw else P["INK"],
                                           alignment=TA_CENTER)))
        st.append(PageBreak())
        st.append(Paragraph("A GUIDE TO YOUR PATTERN", ParagraphStyle(
            "roadmap-kicker", fontName="DJ-B", fontSize=7.4, leading=10,
            textColor=P["GOLD_DK"] if not bw else HexColor("#222222"),
            spaceAfter=3)))
        st.append(Paragraph("Inside this pattern", ParagraphStyle(
            "roadmap-title", fontName="DS-B", fontSize=24, leading=28,
            textColor=P["FOREST_DK"] if not bw else HexColor("#000000"),
            spaceAfter=3)))
        st.append(Paragraph("Use the page numbers below or your reader’s bookmarks to jump to a section.",
                            ParagraphStyle("roadmap-note", fontName="DJ", fontSize=7.6,
                                           leading=10, textColor=P["GREY"] if not bw
                                           else HexColor("#222222"), spaceAfter=4)))
        st.append(rule(P, bw, 1.4))
        st.append(Spacer(1, 8))
        toc = TableOfContents()
        toc.levelStyles = [
            ParagraphStyle("TOCLevel0", fontName="DJ-B", fontSize=9.1, leading=14,
                           textColor=P["INK"] if not bw else HexColor("#000000"),
                           spaceBefore=3),
            ParagraphStyle("TOCLevel1", fontName="DJ", fontSize=8.1, leading=11.5,
                           leftIndent=16,
                           textColor=P["GREY"] if not bw else HexColor("#222222")),
        ]
        toc.dotsMinLevel = 0
        st.append(toc)
        st.append(PageBreak())
        # ---------------- body sections
        skip_until_terms = False
        for kind, payload in blocks:
            if kind in ("title", "quote"):
                continue
            if kind == "h2":
                low = payload.lower()
                if low.startswith("terms of use"):
                    st.append(CondPageBreak(2.6 * inch))
                st.append(CondPageBreak(3.2 * inch) if low.startswith(("instructions",)) else
                          CondPageBreak(2.4 * inch))
                st += section_title(payload, S, P, bw)
                continue
            if kind == "h3":
                st.append(CondPageBreak(1.9 * inch))
                st.append(Paragraph(md(payload), S["h3"]))
                continue
            if kind == "h4":
                st.append(Paragraph(md(payload), S["h4"]))
                continue
            if kind == "p":
                st.append(Paragraph(md(payload), S["body"]))
                continue
            if kind == "bullet":
                st.append(Paragraph("•&nbsp; " + md(payload), S["bullet"]))
                continue
            if kind == "num":
                st.append(Paragraph(md(payload), S["bullet"]))
                continue
            if kind == "table":
                st.append(CondPageBreak(1.6 * inch))
                if is_round_table(payload):
                    rows = [payload[0]] + [r + [""] * (4 - len(r)) if len(r) < 4 else r
                                           for r in payload[1:]]
                    rows = [r[:4] for r in rows]
                    st.append(round_table(rows, S, P, bw,
                                          widths=[0.42 * inch, CW - 1.82 * inch,
                                                  0.5 * inch, 0.9 * inch]))
                else:
                    ncol = max(len(r) for r in payload)
                    rows = [r + [""] * (ncol - len(r)) for r in payload]
                    st.append(plain_table(rows, S, P, bw))
                st.append(Spacer(1, 5))
                continue
        # ---------------- appendices
        labels, counts = main_counts(blocks, spec)
        st.append(CondPageBreak(2 * inch))
        appx = [Spacer(1, 6)]
        appx += section_title("Appendix A - Assembly Map & Count Chart", S, P, bw)
        appx.append(ComponentMap(spec["components"], P, bw))
        appx.append(Spacer(1, 6))
        appx.append(Paragraph(md(spec.get("assembly_note", "Assembly order follows the numbered "
                                          "sections; face work happens while the head is still "
                                          "open.")), S["cap"]))
        appx.append(Spacer(1, 8))
        zones = tuple(spec.get("zones", ()))
        appx.append(CountChart(counts, P, bw, zones=zones))
        st.append(KeepTogether(appx))
        st.append(PageBreak())
        st += section_title("Appendix B - Count Ladder & Verification Summary", S, P, bw)
        half = math.ceil(len(counts) / 2)
        ladder_data = [[Paragraph("Rnd", S["head"]), Paragraph("Sts", S["head"]),
                        Paragraph("Rnd", S["head"]), Paragraph("Sts", S["head"])]]
        for i in range(half):
            row = []
            for j in (i, i + half):
                if j < len(counts) and j < len(labels):
                    row.extend([Paragraph(md(labels[j]), S["cell"]),
                                Paragraph(str(counts[j]), S["cell"])])
                else:
                    row.extend(["", ""])
            ladder_data.append(row)
        ladder = Table(ladder_data,
                       colWidths=[0.7 * inch, 0.6 * inch, 0.7 * inch, 0.6 * inch],
                       repeatRows=1)
        ladder_style = [("GRID", (0, 0), (-1, -1), 0.4, HexColor(P["RULE"])),
                        ("BACKGROUND", (0, 0), (-1, 0), HexColor(P["FOREST"]) if not bw
                         else HexColor("#FFFFFF")),
                        ("TOPPADDING", (0, 0), (-1, -1), 3),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]
        if bw:
            ladder_style.append(("LINEBELOW", (0, 0), (-1, 0), 0.8,
                                 HexColor("#333333")))
        for row_index in range(2, len(ladder_data), 2):
            ladder_style.append(("BACKGROUND", (0, row_index), (-1, row_index),
                                 HexColor("#F2F2F2") if bw else HexColor(P["CREAM_ROW"])))
        ladder.setStyle(TableStyle(ladder_style))
        ladder.hAlign = "CENTER"
        st.append(ladder)
        st.append(Spacer(1, 6))
        audit_status = "PASS" if not probs and not unparsed else "REVIEW REQUIRED"
        if AX is None:
            engine_status = "NOT RUN (engine unavailable)"
            engine_findings = "not reported"
        else:
            finding_total = sum(AX.values())
            engine_status = "PASS" if finding_total == 0 else "REVIEW REQUIRED"
            finding_word = "finding" if finding_total == 1 else "findings"
            engine_findings = f"{finding_total} {finding_word} across four checks"
        mismatch_word = "mismatch" if len(probs) == 1 else "mismatches"
        unparsed_word = "unparsed row" if len(unparsed) == 1 else "unparsed rows"
        verification_summary = (
            f"Independent stitch-table audit: {audit_status} "
            f"({len(counts)} ladder rows; {len(probs)} {mismatch_word}; "
            f"{len(unparsed)} {unparsed_word}). Static-analysis engine: "
            f"{engine_status} ({engine_findings}). A verified badge requires "
            f"both checks to complete with no findings."
        )
        st.append(callout("Verification summary", verification_summary, S, P, bw))
        st.append(Spacer(1, 6))
        ax_rows = [["Check", "What it examines", "Findings"]]
        ax_rows += [[name, description, str(AX[name]) if AX is not None else "not run"]
                    for name, description in (
                        ("Domain Isolation", "Pieces keep separate stitch domains"),
                        ("Edge Lineage", "Each round consumes the prior total"),
                        ("Open Boundaries", "Open edges are closed or sewn deliberately"),
                        ("Gauge Bounding", "Hook and gauge band match stated size"),
                    )]
        at = Table([[Paragraph(md(c), S["head"] if i == 0 else S["cell"])
                     for c in r] for i, r in enumerate(ax_rows)],
                   colWidths=[1.3 * inch, CW - 2.1 * inch, 0.8 * inch])
        ast = [("GRID", (0, 0), (-1, -1), 0.4, HexColor(P["RULE"])),
               ("BACKGROUND", (0, 0), (-1, 0), HexColor(P["FOREST"]) if not bw
                else HexColor("#FFFFFF")),
               ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]
        if bw:
            ast.append(("LINEBELOW", (0, 0), (-1, 0), 0.8, HexColor("#333333")))
        at.setStyle(TableStyle(ast))
        st.append(at)
        st.append(Spacer(1, 8))
        st.append(Paragraph(md(spec.get("colophon", "Diagrams, assembly map and verification "
                                                    "appendix computed from the corrected "
                                                    "master at compile time.")), S["cap"]))
        st.append(Spacer(1, 10))
        st.append(rule(P, bw, 1.2))
        st.append(Paragraph("© 2026 Novality Store. All rights reserved. Published under the "
                            "Novality Crochet Studio imprint.",
                            ParagraphStyle("cpl", fontName="DJ", fontSize=7.4,
                                           textColor=P["INK"], alignment=TA_CENTER)))
        return st

    # Resolve the contents page and total-page footer in two deterministic passes.
    import pymupdf
    out.parent.mkdir(parents=True, exist_ok=True)
    buf = io.BytesIO()
    doc = Doc(buf, spec, P, bw, verification_ok=verification_ok)
    doc.total_pages = 99
    doc.multiBuild(story(), maxPasses=5)
    pages = pymupdf.open(stream=buf.getvalue(), filetype="pdf").page_count
    doc = Doc(str(out), spec, P, bw, verification_ok=verification_ok)
    doc.total_pages = pages
    doc.multiBuild(story(), maxPasses=5)
    print(f"wrote {out} pages: {pages}")
    return pages


if __name__ == "__main__":
    build(sys.argv[1], bw="--bw" in sys.argv)
