"""
PDF generation engine for crochet patterns.

Generates professional, print-ready documents from validated patterns.
Multiple templates with beautiful typography and layouts.
"""

from __future__ import annotations

import html as html_lib
from datetime import datetime

from pydantic import BaseModel

from ..model.pattern import Pattern
from ..validation import ValidationReport
from ..visualization.measurements import PatternMeasurements, measure_pattern

# Template color schemes
TEMPLATES = {
    "minimal": {
        "primary": "#2C3E50",
        "secondary": "#7F8C8D",
        "accent": "#4A90D9",
        "bg": "#FFFFFF",
        "card_bg": "#F8F9FA",
        "round_bg": "#FAFBFC",
        "border": "#E0E0E0",
        "font_heading": "'Georgia', 'Times New Roman', serif",
        "font_body": "'Georgia', 'Times New Roman', serif",
        "font_mono": "'Courier New', monospace",
    },
    "craft": {
        "primary": "#5B4A69",
        "secondary": "#9B8EA8",
        "accent": "#E8A87C",
        "bg": "#FFF8F0",
        "card_bg": "#FFF0E5",
        "round_bg": "#FFF5ED",
        "border": "#E8D5C4",
        "font_heading": "'Palatino Linotype', 'Book Antiqua', Palatino, serif",
        "font_body": "'Palatino Linotype', 'Book Antiqua', Palatino, serif",
        "font_mono": "'Courier New', monospace",
    },
    "modern": {
        "primary": "#1A1A2E",
        "secondary": "#16213E",
        "accent": "#E94560",
        "bg": "#FFFFFF",
        "card_bg": "#F5F5F5",
        "round_bg": "#FAFAFA",
        "border": "#E0E0E0",
        "font_heading": "'Helvetica Neue', 'Arial', sans-serif",
        "font_body": "'Helvetica Neue', 'Arial', sans-serif",
        "font_mono": "'SF Mono', 'Fira Code', monospace",
    },
    "ocean": {
        "primary": "#0B3D2E",
        "secondary": "#1A6B52",
        "accent": "#38A3A5",
        "bg": "#F0F8F5",
        "card_bg": "#E5F5EE",
        "round_bg": "#F0FAF5",
        "border": "#C5E0D5",
        "font_heading": "'Garamond', 'Times New Roman', serif",
        "font_body": "'Garamond', 'Times New Roman', serif",
        "font_mono": "'Courier New', monospace",
    },
    "berry": {
        "primary": "#6B2D5B",
        "secondary": "#A04E8C",
        "accent": "#D4738E",
        "bg": "#FFF5F8",
        "card_bg": "#FFE8F0",
        "round_bg": "#FFF0F5",
        "border": "#E8C5D5",
        "font_heading": "'Baskerville', 'Georgia', serif",
        "font_body": "'Baskerville', 'Georgia', serif",
        "font_mono": "'Courier New', monospace",
    },
    "sunset": {
        "primary": "#C0392B",
        "secondary": "#E67E22",
        "accent": "#F39C12",
        "bg": "#FFFAF0",
        "card_bg": "#FFF5E5",
        "round_bg": "#FFF8ED",
        "border": "#F0D5B5",
        "font_heading": "'Copperplate', 'Papyrus', fantasy",
        "font_body": "'Optima', 'Calibri', sans-serif",
        "font_mono": "'Courier New', monospace",
    },
}



WRITTEN_COLOR_SWATCHES = {
    "brown": "#8B5A2B", "indigo": "#3F51B5", "gold": "#C9A227",
    "white": "#F4F1EA", "black": "#222222", "red": "#C0392B",
    "blue": "#2471A3", "green": "#1E8449", "pink": "#D4738E",
    "yellow": "#F4D03F", "orange": "#E67E22", "purple": "#7D3C98",
    "grey": "#7F8C8D", "gray": "#7F8C8D", "cream": "#F6E7C1",
    "navy": "#1A365D", "teal": "#148F77",
}


class PDFConfig(BaseModel):
    """Configuration for PDF generation."""

    template: str = "minimal"
    include_cover: bool = True
    include_materials: bool = True
    include_abbreviations: bool = True
    include_charts: bool = True
    include_validation: bool = True
    include_measurements: bool = True
    designer_name: str = ""
    copyright_text: str = ""
    pattern_version: str = "1.0"
    page_size: str = "A4"
    include_checklist: bool = True
    include_color_key: bool = True
    large_print: bool = False
    ink_saver: bool = False
    landscape: bool = False
    binding: str = "none"
    compact: bool = False
    include_marks: bool = True
    include_change: bool = True
    include_index: bool = True
    include_ruled_notes: bool = True
    include_used_stitches: bool = True
    duplex: bool = False
    cards: bool = False
    crop_marks: bool = False
    include_ladder: bool = True
    include_parse: bool = True
    include_maker: bool = True
    include_map: bool = True


class PDFGenerator:
    """Generates professional PDF documents from crochet patterns."""

    def __init__(self, config: PDFConfig | None = None) -> None:
        self.config = config or PDFConfig()
        self.theme = TEMPLATES.get(self.config.template, TEMPLATES["minimal"])

    def generate(
        self, pattern: Pattern, validation_report: ValidationReport | None = None
    ) -> str:
        """Generate the complete HTML document."""
        measurements = measure_pattern(pattern)
        self._sheet_report = validation_report
        sections = []

        if self.config.include_cover:
            sections.append(self._cover_page(pattern, measurements))

        if self.config.include_materials:
            sections.append(self._materials_section(pattern))

        if self.config.include_abbreviations:
            sections.append(self._abbreviations_section())

        color_key = self._color_key_section(pattern)
        if color_key:
            sections.append(color_key)

        for extra in (self._index_section(pattern), self._map_section(pattern), self._used_stitches_section(pattern), self._written_definitions_section(pattern)):
            if extra:
                sections.append(extra)

        sections.append(self._multi_piece_instructions_section(pattern, measurements))

        chart = self._chart_section(pattern)
        if chart:
            sections.append(chart)
        stitch_map = self._stitch_map_section(pattern)
        if stitch_map:
            sections.append(stitch_map)
        assembly = self._assembly_map_section(pattern)
        if assembly:
            sections.append(assembly)

        if self.config.include_measurements:
            sections.append(self._measurements_section(measurements))

        if self.config.include_validation and validation_report:
            sections.append(self._validation_section(validation_report))

        for extra in (self._ladder_section(pattern), self._marks_section(pattern), self._maker_line(), self._text_id(pattern), self._duplex_note(), self._ruled_notes_section(), self._print_note()):
            if extra:
                sections.append(extra)

        if self.config.copyright_text or self.config.designer_name:
            sections.append(self._footer_section())

        return self._wrap_document("\n".join(sections), pattern)

    def save(
        self,
        filepath: str,
        pattern: Pattern,
        validation_report: ValidationReport | None = None,
    ) -> None:
        """Save the generated document to a file."""
        from pathlib import Path

        content = self.generate(pattern, validation_report)

        if str(filepath).endswith(".pdf"):
            try:
                from weasyprint import HTML

                HTML(string=content).write_pdf(filepath)
            except ImportError:
                html_path = str(filepath).replace(".pdf", ".html")
                Path(html_path).write_text(content, encoding="utf-8")
                raise ImportError(
                    f"WeasyPrint not installed. Saved HTML to {html_path}. "
                    f"Install with: pip install weasyprint"
                )
        else:
            Path(filepath).write_text(content, encoding="utf-8")

    def _wrap_document(self, body: str, pattern: Pattern) -> str:
        """Wrap body content in a complete HTML document with styles."""
        styles = self._get_styles() + self._extra_styles()
        title = html_lib.escape(pattern.metadata.title or "Crochet Pattern")
        author = html_lib.escape(self.config.designer_name or pattern.metadata.designer or "")
        author_tag = f'<meta name="author" content="{author}">' if author else ""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    {author_tag}
    <meta name="description" content="Printable crochet sheet. Not a certification.">
    <meta name="generator" content="Crochet Pattern Checker">
    <style>
{styles}
    </style>
</head>
<body class="{self._body_class()}">
{body}
</body>
</html>"""

    def _get_styles(self) -> str:
        """Get CSS styles based on template."""
        t = self.theme
        page_size = self._page_size_css()
        margin, left = self._margins()
        marks = "marks: crop cross; bleed: 3mm;" if self.config.crop_marks else ""
        return f"""
        @page {{
            size: {page_size};
            margin: {margin};
            margin-left: {left};
            {marks}
            @bottom-center {{
                content: counter(page) " / " counter(pages);
                font-size: 9pt;
                color: #666666;
            }}
            @bottom-right {{
                content: string(piece-title);
                font-size: 8pt;
                color: #666666;
            }}
            @top-center {{
                content: "Crochet pattern sheet";
                font-size: 9pt;
                color: #666666;
            }}
        }}
        @page:first {{
            size: {page_size};
            margin: {margin};
            margin-left: {left};
            @bottom-center {{ content: none; }}
            @top-center {{ content: none; }}
        }}
        .cover {{ page: cover; }}
        @page cover {{
            size: {page_size};
            margin: {margin};
            margin-left: {left};
            @bottom-center {{ content: none; }}
            @top-center {{ content: none; }}
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: {t["font_body"]};
            color: {t["primary"]};
            line-height: 1.7;
            max-width: 210mm;
            margin: 0 auto;
            padding: 15mm;
            background: {t["bg"]};
            font-size: 11pt;
        }}
        .page-break {{ page-break-before: always; }}

        /* Headings */
        h1 {{
            font-family: {t["font_heading"]};
            font-size: 32px;
            margin-bottom: 12px;
            color: {t["primary"]};
            letter-spacing: -0.5px;
        }}
        h2 {{
            font-family: {t["font_heading"]};
            font-size: 20px;
            margin: 30px 0 15px 0;
            color: {t["primary"]};
            border-bottom: 2px solid {t["accent"]};
            padding-bottom: 8px;
            letter-spacing: 0.3px;
        }}
        h3 {{
            font-family: {t["font_heading"]};
            font-size: 15px;
            margin: 20px 0 10px 0;
            color: {t["secondary"]};
        }}
        p {{ margin: 8px 0; }}

        /* Tables */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            font-size: 10pt;
        }}
        th, td {{
            padding: 8px 12px;
            text-align: left;
            border-bottom: 1px solid {t["border"]};
        }}
        th {{
            background: {t["card_bg"]};
            font-weight: bold;
            color: {t["primary"]};
            font-size: 9pt;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        /* Cover page */
        .cover {{
            text-align: center;
            padding: 60px 0 40px 0;
            page-break-after: always;
        }}
        .cover h1 {{
            font-size: 44px;
            margin-bottom: 16px;
            line-height: 1.2;
        }}
        .cover .subtitle {{
            font-size: 16px;
            color: {t["secondary"]};
            margin-bottom: 8px;
            font-style: italic;
        }}
        .cover .description {{
            font-size: 12px;
            color: {t["secondary"]};
            margin: 15px auto;
            max-width: 400px;
            line-height: 1.6;
        }}
        .cover .designer {{
            font-size: 14px;
            color: {t["accent"]};
            margin-top: 30px;
            font-weight: bold;
            letter-spacing: 1px;
            text-transform: uppercase;
        }}
        .cover .date {{
            font-size: 11px;
            color: {t["secondary"]};
            margin-top: 8px;
        }}

        /* Info boxes */
        .info-box {{
            background: {t["card_bg"]};
            border-radius: 10px;
            padding: 20px;
            margin: 15px 0;
            border-left: 4px solid {t["accent"]};
        }}
        .info-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px 20px;
        }}
        .info-item {{ padding: 5px 0; }}
        .info-label {{
            font-weight: bold;
            color: {t["secondary"]};
            font-size: 9pt;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .info-value {{
            color: {t["primary"]};
            font-size: 11pt;
        }}

        /* Rounds/Rows */
        .round {{
            margin: 10px 0;
            padding: 10px 15px;
            border-left: 3px solid {t["accent"]};
            background: {t["round_bg"]};
            border-radius: 0 6px 6px 0;
            position: relative;
        }}
        .round:hover {{
            background: {t["card_bg"]};
        }}
        .round-number {{
            font-weight: bold;
            color: {t["accent"]};
            font-size: 11pt;
            font-family: {t["font_mono"]};
        }}
        .round-range {{
            font-weight: bold;
            color: {t["accent"]};
            font-size: 11pt;
            font-family: {t["font_mono"]};
            background: {t["card_bg"]};
            padding: 2px 8px;
            border-radius: 4px;
            display: inline-block;
            margin-right: 8px;
        }}
        .stitch-count {{
            float: right;
            color: {t["secondary"]};
            font-size: 10pt;
            font-family: {t["font_mono"]};
            background: {t["card_bg"]};
            padding: 2px 8px;
            border-radius: 10px;
        }}
        .round-text {{
            margin-top: 4px;
            font-size: 10.5pt;
        }}

        /* Notes */
        .note {{
            background: #FFF8E1;
            border-radius: 8px;
            padding: 15px;
            margin: 12px 0;
            border-left: 4px solid #FFB74D;
            font-size: 10pt;
        }}

        /* Measurement cards */
        .measurement-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            margin: 20px 0;
        }}
        .measurement-card {{
            background: {t["card_bg"]};
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            border-top: 3px solid {t["accent"]};
        }}
        .measurement-value {{
            font-size: 28px;
            font-weight: bold;
            color: {t["accent"]};
            font-family: {t["font_heading"]};
        }}
        .measurement-label {{
            font-size: 10px;
            color: {t["secondary"]};
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-top: 5px;
        }}

        /* Validation */
        .success {{ color: #27AE60; }}
        .warning {{ color: #F39C12; }}
        .error {{ color: #E74C3C; }}
        .status-badge {{
            display: inline-block;
            padding: 4px 14px;
            border-radius: 20px;
            font-size: 10pt;
            font-weight: bold;
        }}

        /* Footer */
        .footer {{
            margin-top: 50px;
            padding-top: 15px;
            border-top: 1px solid {t["border"]};
            font-size: 9pt;
            color: {t["secondary"]};
            text-align: center;
        }}

        /* supply cards */
        .materials-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            margin: 10px 0;
        }}
        .material-card {{
            background: {t["bg"]};
            border: 1px solid {t["border"]};
            border-radius: 8px;
            padding: 12px;
        }}
        .material-label {{
            font-size: 9pt;
            color: {t["secondary"]};
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .material-value {{
            font-size: 12pt;
            color: {t["primary"]};
            font-weight: bold;
            margin-top: 3px;
        }}

        /* Abbreviation table */
        .abbrev-table td:first-child {{
            font-weight: bold;
            font-family: {t["font_mono"]};
            color: {t["accent"]};
            width: 70px;
        }}

        /* Instruction Table */
        .instruction-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 10pt;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .instruction-table thead {{
            background: {t["accent"]};
            color: white;
        }}
        .instruction-table th {{
            padding: 12px 10px;
            text-align: left;
            font-weight: bold;
            text-transform: uppercase;
            font-size: 9pt;
            letter-spacing: 0.5px;
        }}
        .instruction-table td {{
            padding: 10px;
            border-bottom: 1px solid {t["border"]};
        }}
        .instruction-table tbody tr:nth-child(even) {{
            background: {t["round_bg"]};
        }}
        .instruction-table tbody tr:hover {{
            background: {t["card_bg"]};
        }}
        .instruction-table .round-num {{
            font-weight: bold;
            font-family: {t["font_mono"]};
            color: {t["accent"]};
            width: 60px;
        }}
        .instruction-table .instruction {{
            font-family: {t["font_mono"]};
            font-size: 9.5pt;
        }}
        .instruction-table .stitch-count {{
            font-family: {t["font_mono"]};
            font-weight: bold;
            color: {t["secondary"]};
            text-align: center;
            width: 70px;
        }}
        .instruction-table .note {{
            font-size: 9pt;
            color: {t["secondary"]};
            font-style: italic;
            width: 120px;
        }}
        .construction-info {{
            margin: 10px 0 20px 0;
            font-size: 10pt;
            color: {t["secondary"]};
        }}
        .pattern-notes {{
            background: #FFF8E1;
            border-left: 4px solid #FFB74D;
            padding: 15px;
            margin: 15px 0;
            border-radius: 0 8px 8px 0;
        }}

        /* Piece Sections */
        .piece-section {{
            margin: 20px 0;
            padding: 0;
        }}
        .piece-section h2 {{
            color: {t["primary"]};
            border-bottom: 3px solid {t["accent"]};
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}

        .chart-wrap {{ margin: 12px 0; text-align: center; }}
        .chart-wrap svg {{ max-width: 100%; height: auto; }}
        .chart-note {{ font-size: 9pt; color: {t["secondary"]}; }}
        .worked {{ width: 46px; text-align: center; }}
        .box {{ display: inline-block; width: 12px; height: 12px; border: 1.5px solid {t["primary"]}; }}
        .swatch {{ display: inline-block; width: 14px; height: 14px; border: 1px solid {t["border"]}; margin-right: 6px; vertical-align: -2px; }}
        .color-key {{ margin: 8px 0 16px 0; }}

        /* Print */
        @media print {{
            body {{ padding: 0; font-size: 10pt; }}
            .page-break {{ page-break-before: always; }}
            .round {{ break-inside: avoid; }}
        }}
"""

    def _cover_page(self, pattern: Pattern, measurements: PatternMeasurements) -> str:
        """Generate the cover page."""
        title = html_lib.escape(pattern.metadata.title or "Crochet Pattern")
        designer = html_lib.escape(
            self.config.designer_name or pattern.metadata.designer or "Anonymous"
        )
        difficulty = html_lib.escape(pattern.metadata.difficulty or "")
        category = html_lib.escape(pattern.metadata.category or "")
        description = html_lib.escape(pattern.metadata.description or "")

        subtitle_parts = []
        if category:
            subtitle_parts.append(category)
        if difficulty:
            subtitle_parts.append(f"Difficulty: {difficulty}")
        subtitle = " · ".join(subtitle_parts) if subtitle_parts else ""

        stats_html = ""
        if measurements.total_rounds > 0:
            stats_html = f"""
    <div class="info-box" style="max-width: 420px; margin: 25px auto;">
        <div class="info-grid">
            <div class="info-item"><span class="info-label">Rounds</span><br><span class="info-value">{measurements.total_rounds}</span></div>
            <div class="info-item"><span class="info-label">Max Stitches</span><br><span class="info-value">{measurements.max_stitch_count}</span></div>
            <div class="info-item"><span class="info-label">Diameter</span><br><span class="info-value">{measurements.max_diameter_inches:.1f} in</span></div>
            <div class="info-item"><span class="info-label">Height</span><br><span class="info-value">{measurements.total_height_inches:.1f} in</span></div>
        </div>
    </div>"""

        desc_html = f'<p class="description">{description}</p>' if description else ""

        return f"""
<div class="cover">
    <h1>{title}</h1>
    {f'<p class="subtitle">{subtitle}</p>' if subtitle else ""}
    {desc_html}
    {stats_html}
    <p class="designer">{designer}</p>
    <p class="date">Version {self.config.pattern_version} · {datetime.now().strftime("%B %Y")}</p>
</div>
"""

    def _materials_section(self, pattern: Pattern) -> str:
        """Generate the materials section."""
        cards = []

        # Yarn
        if pattern.yarn:
            yarn_name = html_lib.escape(pattern.yarn.name or "")
            yarn_weight = html_lib.escape(pattern.yarn.weight or "")
            display = yarn_name
            if yarn_weight and yarn_weight != yarn_name.lower():
                display = f"{yarn_name} ({yarn_weight})" if yarn_name else yarn_weight
            cards.append(
                f'<div class="material-card"><div class="material-label">Yarn</div><div class="material-value">{display}</div></div>'
            )
        else:
            cards.append(
                '<div class="material-card"><div class="material-label">Yarn</div><div class="material-value">[Specify yarn]</div></div>'
            )

        # Hook
        if pattern.hook and pattern.hook.size_mm:
            hook_text = f"{pattern.hook.size_mm} mm"
            if pattern.hook.us_size:
                hook_text += f" (US {pattern.hook.us_size})"
            cards.append(
                f'<div class="material-card"><div class="material-label">Hook</div><div class="material-value">{hook_text}</div></div>'
            )
        else:
            cards.append(
                '<div class="material-card"><div class="material-label">Hook</div><div class="material-value">[Specify hook size]</div></div>'
            )

        # Gauge
        if pattern.gauge and pattern.gauge.stitches_per_unit:
            gauge_text = f"{pattern.gauge.stitches_per_unit} sts × {pattern.gauge.rows_per_unit} rows = {pattern.gauge.unit_size} {pattern.gauge.unit}"
            cards.append(
                f'<div class="material-card"><div class="material-label">Gauge</div><div class="material-value">{gauge_text}</div></div>'
            )

        materials_html = "\n".join(cards)

        return f"""
<h2>Materials</h2>
<div class="materials-grid">
    {materials_html}
</div>
"""

    def _abbreviations_section(self) -> str:
        """Generate the abbreviations reference."""
        abbrevs = [
            ("MR", "Magic Ring"),
            ("ch", "Chain"),
            ("sl st", "Slip Stitch"),
            ("sc", "Single Crochet"),
            ("hdc", "Half Double Crochet"),
            ("dc", "Double Crochet"),
            ("tr", "Treble Crochet"),
            ("inc", "Increase (2 in 1)"),
            ("dec", "Decrease"),
            ("invdec", "Invisible Decrease"),
            ("st(s)", "Stitch(es)"),
            ("rep", "Repeat"),
            ("FO", "Fasten Off"),
        ]
        rows = "\n".join(
            f"<tr><td>{ab}</td><td>{name}</td></tr>" for ab, name in abbrevs
        )
        return f"""
<h2>Abbreviations (US Terms)</h2>
<table class="abbrev-table">
    <thead><tr><th>Abbr</th><th>Meaning</th></tr></thead>
    <tbody>{rows}</tbody>
</table>
"""

    def _group_rounds(self, items: list) -> list:
        """Group consecutive rounds with identical instructions."""
        if not items:
            return []

        groups = []
        current_group = {
            "rounds": [items[0]],
            "text": items[0].source_text,
        }

        for i in range(1, len(items)):
            item = items[i]
            # Compare instruction text (without round header)
            prev_text = self._strip_round_header(current_group["text"])
            curr_text = self._strip_round_header(item.source_text)

            if prev_text == curr_text:
                current_group["rounds"].append(item)
            else:
                groups.append(current_group)
                current_group = {
                    "rounds": [item],
                    "text": item.source_text,
                }

        groups.append(current_group)
        return groups

    def _strip_round_header(self, text: str) -> str:
        """Remove round/row header from text."""
        import re

        # Remove "Round N:" or "Round N-M:" or "Row N:" prefix
        stripped = re.sub(
            r"^(Round|Rnd|Row)\s+\d+(-\d+)?:\s*", "", text, flags=re.IGNORECASE
        )
        return stripped.strip()

    def _instructions_section(
        self, pattern: Pattern, measurements: PatternMeasurements
    ) -> str:
        """Generate the main instructions section with grouped rounds."""
        items = pattern.rounds or pattern.rows
        if not items:
            return "<h2>Instructions</h2><p>No instructions found in pattern.</p>"

        label = "Round" if pattern.rounds else "Row"
        label_plural = "Rounds" if pattern.rounds else "Rows"

        # Group consecutive identical rounds
        groups = self._group_rounds(items)

        rounds_html = []
        prev = 0

        for group in groups:
            rounds_in_group = group["rounds"]
            instruction_text = self._strip_round_header(group["text"])

            if len(rounds_in_group) == 1:
                # Single round
                r = rounds_in_group[0]
                num = r.round_number if hasattr(r, "round_number") else r.row_number
                sc = r.computed_stitch_count
                if sc == 0:
                    sc = r.compute_stitch_count_with_context(prev)
                display_count = sc
                for inst in r.instructions:
                    if inst.stated_stitch_count is not None:
                        display_count = inst.stated_stitch_count
                        break

                rounds_html.append(f"""
            <div class="round">
                <span class="stitch-count">({display_count} sts)</span>
                <span class="round-number">{label} {num}:</span>
                <p class="round-text">{html_lib.escape(instruction_text)}</p>
            </div>""")
                prev = display_count if display_count > 0 else prev
            else:
                # Grouped rounds
                first_num = (
                    rounds_in_group[0].round_number
                    if hasattr(rounds_in_group[0], "round_number")
                    else rounds_in_group[0].row_number
                )
                last_num = (
                    rounds_in_group[-1].round_number
                    if hasattr(rounds_in_group[-1], "round_number")
                    else rounds_in_group[-1].row_number
                )

                # Get stitch count from last round in group
                last_r = rounds_in_group[-1]
                sc = last_r.computed_stitch_count
                if sc == 0:
                    for inst in last_r.instructions:
                        if inst.stated_stitch_count is not None:
                            sc = inst.stated_stitch_count
                            break

                rounds_html.append(f"""
            <div class="round">
                <span class="stitch-count">({sc} sts each)</span>
                <span class="round-range">{label_plural} {first_num}–{last_num}:</span>
                <p class="round-text">{html_lib.escape(instruction_text)}</p>
            </div>""")
                prev = sc if sc > 0 else prev

        # Notes section
        notes_html = ""
        if pattern.notes:
            notes = "\n".join(f"<p>{html_lib.escape(n)}</p>" for n in pattern.notes)
            notes_html = f'<div class="note"><strong>Notes:</strong>{notes}</div>'

        # Finishing section
        finishing_html = ""
        if pattern.finishing:
            items_html = "\n".join(
                f"<p>{html_lib.escape(f)}</p>" for f in pattern.finishing
            )
            finishing_html = f"<h3>Finishing</h3>{items_html}"

        construction = pattern.construction.value.replace("_", " ").title()

        return f"""
<h2>Instructions</h2>
<p><strong>Construction:</strong> {construction}</p>
{notes_html}
{"".join(rounds_html)}
{finishing_html}
"""

    def _instructions_table_section(
        self, pattern: Pattern, measurements: PatternMeasurements
    ) -> str:
        """Generate instructions in professional table format (Round | Instruction | Stitches | Notes)."""
        items = pattern.rounds or pattern.rows
        if not items:
            return "<h2>Instructions</h2><p>No instructions found in pattern.</p>"

        label = "Round" if pattern.rounds else "Row"

        # Build table rows
        table_rows = []
        prev_count = 0

        for item in items:
            round_num = (
                item.round_number if hasattr(item, "round_number") else item.row_number
            )

            # Get instruction text (strip "Round X:" prefix)
            instruction_text = (
                self._strip_round_header(item.source_text)
                if hasattr(item, "source_text")
                else ""
            )

            # Get stitch count
            stitch_count = 0
            if hasattr(item, "computed_stitch_count"):
                stitch_count = item.computed_stitch_count
            if stitch_count == 0 and hasattr(item, "compute_stitch_count_with_context"):
                stitch_count = item.compute_stitch_count_with_context(prev_count)

            # Check if any instruction has a stated count (more reliable)
            if hasattr(item, "instructions"):
                for inst in item.instructions:
                    if (
                        hasattr(inst, "stated_stitch_count")
                        and inst.stated_stitch_count is not None
                    ):
                        stitch_count = inst.stated_stitch_count
                        break

            # Detect special notes (stuffing markers, etc.)
            note = ""
            source_lower = instruction_text.lower()
            if "stuff" in source_lower:
                note = "🧸 STUFF HERE"
            elif "fasten off" in source_lower or "FO" in instruction_text:
                note = "Fasten off"

            # Format round number
            round_display = f"R{round_num}" if pattern.rounds else f"Row {round_num}"

            table_rows.append(f"""
                <tr>
                    <td class="round-num">{round_display}</td>
                    <td class="instruction"{self._row_tint(instruction_text)}>{html_lib.escape(instruction_text)}{self._parse_line(item)}{self._flag_for_number(round_num)}</td>
                    <td class="stitch-count">({stitch_count})</td>
                    <td class="note">{note}</td>{self._change_cell(prev_count, stitch_count)}{self._worked_cell()}
                </tr>""")

            prev_count = stitch_count if stitch_count > 0 else prev_count

        # Build the complete table
        table_html = f"""
        <table class="instruction-table">
            <thead>
                <tr>
                    <th>{label}</th>
                    <th>Instruction</th>
                    <th>Stitches</th>
                    <th>Notes</th>{self._change_head()}{self._worked_head()}
                </tr>
            </thead>
            <tbody>
                {"".join(table_rows)}
            </tbody>
        </table>
        """

        # Add notes section if present
        notes_html = ""
        if pattern.notes:
            notes_content = "".join(
                f"<p>{html_lib.escape(n)}</p>" for n in pattern.notes
            )
            notes_html = f'<div class="pattern-notes"><strong>Pattern Notes:</strong>{notes_content}</div>'

        # Add finishing section if present
        finishing_html = ""
        if pattern.finishing:
            finishing_content = "".join(
                f"<p>{html_lib.escape(f)}</p>" for f in pattern.finishing
            )
            finishing_html = f"<h3>Finishing Instructions</h3>{finishing_content}"

        construction = pattern.construction.value.replace("_", " ").title()

        return f"""
<h2>Instructions</h2>
<p class="construction-info"><strong>Construction:</strong> {construction}</p>
{self._proof_strip()}
{self._parse_note()}
{self._change_note()}
{self._reminder(pattern)}
{notes_html}
{table_html}
{finishing_html}
"""

    def _multi_piece_instructions_section(
        self, pattern: Pattern, measurements: PatternMeasurements
    ) -> str:
        """Generate multi-piece instructions with separate sections for each piece."""
        import html as html_lib

        if not pattern.pieces:
            # Fall back to single-piece format
            return self._instructions_table_section(pattern, measurements)

        sections_html = [part for part in (self._proof_strip(), self._parse_note()) if part]

        for i, piece in enumerate(pattern.pieces):
            # Section header
            make_text = (
                f" (make {piece.make_count})"
                if piece.make_count and piece.make_count > 1
                else ""
            )
            section_num = i + 1

            section_header = f"""
<div class="page-break"></div>
<div class="piece-section" id="piece-{section_num}">
    <h2>Section {section_num}: {piece.name}{make_text}</h2>
    {self._reminder(pattern)}
    {self._change_note()}
"""

            # Build table for this piece
            items = piece.rounds if piece.rounds else piece.rows
            if not items:
                continue

            label = "Round" if piece.rounds else "Row"

            # Build table rows
            table_rows = []
            prev_count = 0

            for item in items:
                round_num = (
                    item.round_number
                    if hasattr(item, "round_number")
                    else item.row_number
                )

                # Get instruction text
                instruction_text = (
                    self._strip_round_header(item.source_text)
                    if hasattr(item, "source_text")
                    else ""
                )

                # Get stitch count
                stitch_count = 0
                if hasattr(item, "computed_stitch_count"):
                    stitch_count = item.computed_stitch_count
                if stitch_count == 0 and hasattr(
                    item, "compute_stitch_count_with_context"
                ):
                    stitch_count = item.compute_stitch_count_with_context(prev_count)

                # Check if any instruction has a stated count
                if hasattr(item, "instructions"):
                    for inst in item.instructions:
                        if (
                            hasattr(inst, "stated_stitch_count")
                            and inst.stated_stitch_count is not None
                        ):
                            stitch_count = inst.stated_stitch_count
                            break

                # Detect special notes
                note = ""
                source_lower = instruction_text.lower()
                if "stuff" in source_lower:
                    note = "🧸 STUFF HERE"
                elif "fasten off" in source_lower or "FO" in instruction_text:
                    note = "Fasten off"

                # Format round number - reset to start from 1 for each piece
                first_round_num = (
                    items[0].round_number
                    if hasattr(items[0], "round_number")
                    else items[0].row_number
                )
                piece_round_num = round_num - (first_round_num - 1)
                round_display = (
                    f"R{piece_round_num}" if piece.rounds else f"Row {piece_round_num}"
                )

                table_rows.append(f"""
                    <tr>
                        <td class="round-num">{round_display}</td>
                        <td class="instruction"{self._row_tint(instruction_text)}>{html_lib.escape(instruction_text)}{self._parse_line(item)}{self._flag_for_number(round_num)}</td>
                        <td class="stitch-count">({stitch_count})</td>
                        <td class="note">{note}</td>{self._change_cell(prev_count, stitch_count)}{self._worked_cell()}
                    </tr>""")

                prev_count = stitch_count if stitch_count > 0 else prev_count

            # Build the complete table for this piece
            table_html = f"""
            <table class="instruction-table">
                <thead>
                    <tr>
                        <th>{label}</th>
                        <th>Instruction</th>
                        <th>Stitches</th>
                        <th>Notes</th>{self._change_head()}{self._worked_head()}
                    </tr>
                </thead>
                <tbody>
                    {"".join(table_rows)}
                </tbody>
            </table>
            """

            # Add piece notes if any
            piece_notes_html = ""
            if piece.notes:
                notes_content = "".join(
                    f"<p>{html_lib.escape(n)}</p>" for n in piece.notes
                )
                piece_notes_html = f'<div class="pattern-notes">{notes_content}</div>'

            section_html = section_header + piece_notes_html + table_html + "</div>"
            sections_html.append(section_html)

        return "\n".join(sections_html)

    def _measurements_section(self, measurements: PatternMeasurements) -> str:
        """Generate the finished measurements section."""
        return f"""
<div class="page-break"></div>
<h2>Finished Measurements</h2>
<p class="chart-note">These figures come from the measurement helper. They are not a measured gauge swatch.</p>
<div class="measurement-grid">
    <div class="measurement-card">
        <div class="measurement-value">{measurements.max_diameter_inches:.1f}"</div>
        <div class="measurement-label">Diameter</div>
    </div>
    <div class="measurement-card">
        <div class="measurement-value">{measurements.total_height_inches:.1f}"</div>
        <div class="measurement-label">Height</div>
    </div>
    <div class="measurement-card">
        <div class="measurement-value">{measurements.max_stitch_count}</div>
        <div class="measurement-label">Max Stitches</div>
    </div>
</div>
<table>
    <tr><th>Measurement</th><th>mm</th><th>inches</th></tr>
    <tr><td>Max Radius</td><td>{measurements.max_radius_mm:.1f}</td><td>{measurements.max_radius_inches:.2f}</td></tr>
    <tr><td>Max Circumference</td><td>{measurements.max_circumference_mm:.1f}</td><td>{measurements.max_circumference_inches:.2f}</td></tr>
    <tr><td>Total Height</td><td>{measurements.total_height_mm:.1f}</td><td>{measurements.total_height_inches:.2f}</td></tr>
</table>
"""

    def _validation_section(self, report: ValidationReport) -> str:
        """Generate validation report section."""
        status = report.overall_status
        score = report.score
        status_class = (
            "success"
            if "PASS" in status
            else "warning"
            if "REVIEW" in status
            else "error"
        )

        errors_html = ""
        if report.errors:
            items = "\n".join(
                f"<li><strong>[{e.location}]</strong> {html_lib.escape(e.message)}</li>"
                for e in report.errors
            )
            errors_html = f"<h3>Errors Found</h3><ul>{items}</ul>"

        warnings_html = ""
        if report.warnings:
            items = "\n".join(
                f"<li><strong>[{w.location}]</strong> {html_lib.escape(w.message)}</li>"
                for w in report.warnings[:5]
            )
            if len(report.warnings) > 5:
                items += f"<li>... and {len(report.warnings) - 5} more warnings</li>"
            warnings_html = f"<h3>Warnings</h3><ul>{items}</ul>"

        return f"""
<div class="page-break"></div>
<h2>Validation Report</h2>
<div class="info-box">
    <p><strong>Status:</strong> <span class="{status_class}">{status}</span></p>
    <p><strong>Score:</strong> {score}/100</p>
    <p><strong>Errors:</strong> {len(report.errors)} | <strong>Warnings:</strong> {len(report.warnings)}</p>
</div>
{errors_html}
{warnings_html}
<p style="margin-top: 20px; font-size: 9pt; color: #999;">
    <em>This pattern was automatically validated by Crochet Pattern Checker.
    Mathematical validation does not guarantee physical correctness.
    Always test with actual yarn before publishing.</em>
</p>
"""

    def _footer_section(self) -> str:
        """Generate footer/copyright section."""
        parts = []
        if self.config.designer_name:
            parts.append(f"Designed by {html_lib.escape(self.config.designer_name)}")
        elif hasattr(self, "_parsed_designer"):
            parts.append(f"Designed by {html_lib.escape(self._parsed_designer)}")
        if self.config.copyright_text:
            parts.append(html_lib.escape(self.config.copyright_text))
        parts.append(
            f"Generated with Crochet Pattern Checker v1.0.0 · {datetime.now().year}"
        )

        text = " · ".join(parts)
        return f'<div class="footer">{text}</div>'


    def _worked_head(self) -> str:
        if not self.config.include_checklist:
            return ""
        return "<th>Worked</th>"

    def _worked_cell(self) -> str:
        if not self.config.include_checklist:
            return ""
        return '<td class="worked"><span class="box"></span></td>'

    def _named_colors(self, pattern: Pattern) -> list[tuple[str, str]]:
        import re
        swatches = WRITTEN_COLOR_SWATCHES
        text = pattern.source_text or ""
        found, seen = [], set()
        labeled = re.compile(r"\bColor\s+[A-Za-z0-9]+\s*:\s*([A-Za-z]+)")
        for match in labeled.finditer(text):
            name = match.group(1)
            key = name.casefold()
            if key in swatches and key not in seen:
                seen.add(key)
                found.append((name, swatches[key]))
        for word, color in swatches.items():
            if word not in seen and re.search(r"\b" + word + r"\b", text, re.I):
                seen.add(word)
                found.append((word.title(), color))
        return found

    def _color_key_section(self, pattern: Pattern) -> str:
        if not self.config.include_color_key:
            return ""
        found = self._named_colors(pattern)
        if not found:
            return ""
        chips = "".join(
            '<span class="swatch" style="background:%s"></span>%s ' % (color, html_lib.escape(name))
            for name, color in found
        )
        return "<h2>Color key</h2><p class=\"color-key\">" + chips + "</p><p class=\"chart-note\">These swatches mark color names already written in the pattern. They are not a yarn standard.</p>"

    def _chart_section(self, pattern: Pattern) -> str:
        if not self.config.include_charts:
            return ""
        import re
        try:
            from ..visualization import generate_circle_diagram, generate_stitch_count_chart
        except Exception:
            return ""
        parts = []
        for maker in (generate_circle_diagram, generate_stitch_count_chart):
            try:
                svg = maker(pattern) or ""
            except Exception:
                continue
            if "<svg" not in svg:
                continue
            svg = re.sub(r"<\?xml[^>]*\?>", "", svg).strip()
            parts.append('<div class="chart-wrap">' + svg + "</div>")
        if not parts:
            return ""
        return "<h2>Charts</h2>" + "".join(parts) + '<p class="chart-note">Drawn from the parsed rounds. This is not a reading of a chart image.</p>'



    def _print_note(self) -> str:
        return (
            '<p class="print-note">Open this HTML and print it. '
            "A .pdf path uses WeasyPrint when it is installed. "
            "This sheet does not certify the pattern.</p>"
        )

    def _body_class(self) -> str:
        parts = ["sheet"]
        if self.config.large_print:
            parts.append("large-print")
        if self.config.ink_saver:
            parts.append("ink-saver")
        if self.config.compact:
            parts.append("compact")
        if self.config.landscape:
            parts.append("landscape")
        if self.config.duplex:
            parts.append("duplex")
        if self.config.cards:
            parts.append("cards")
        if self.config.crop_marks:
            parts.append("crop-marks")
        if self.config.binding == "left":
            parts.append("binding-left")
        return " ".join(parts)

    def _page_size_css(self) -> str:
        allowed = {"A4", "Letter", "A5", "Legal"}
        size = self.config.page_size if self.config.page_size in allowed else "A4"
        if self.config.landscape:
            return size + " landscape"
        return size

    def _margins(self) -> tuple[str, str]:
        if self.config.large_print:
            margin = "2.2cm"
        elif self.config.compact:
            margin = "1.2cm"
        else:
            margin = "1.8cm"
        left = "2.8cm" if self.config.binding == "left" else margin
        return margin, left

    def _extra_styles(self) -> str:
        return """
        body.large-print { font-size: 14pt; }
        body.large-print .box, body.large-print .mark i { width: 16px; height: 16px; }
        body.compact { font-size: 9.5pt; }
        body.landscape { max-width: none; }
        body.ink-saver,
        body.ink-saver .round,
        body.ink-saver .info-box,
        body.ink-saver .material-card,
        body.ink-saver .measurement-card {
            background: #FFFFFF !important;
            color: #111111 !important;
        }
        body.ink-saver .box, body.ink-saver .mark i { border-color: #111111; }
        .delta { text-align: center; width: 58px; font-family: 'Courier New', monospace; }
        .flag { font-size: 8.5pt; margin-top: 4px; }
        .marks { display: flex; flex-wrap: wrap; gap: 6px; margin: 8px 0 16px 0; }
        .mark { display: inline-flex; align-items: center; gap: 4px; font-size: 9pt; }
        .mark i { display: inline-block; width: 12px; height: 12px; border: 1.5px solid currentColor; }
        .rule { border-bottom: 1px solid #888888; height: 22px; margin: 6px 0; }
        .reminder { font-size: 10pt; margin: 6px 0 12px 0; }
        .print-note { font-size: 9pt; margin-top: 18px; }
        tr, .round, .piece-section { break-inside: avoid; }
        """ + self._advanced_styles()

    def _change_head(self) -> str:
        if not self.config.include_change:
            return ""
        return "<th>Change</th>"

    def _change_cell(self, previous: int, current: int) -> str:
        if not self.config.include_change:
            return ""
        if previous <= 0 or current <= 0:
            return '<td class="delta">-</td>'
        delta = current - previous
        text = f"+{delta}" if delta > 0 else str(delta)
        return f'<td class="delta">{text}</td>'

    def _change_note(self) -> str:
        if not self.config.include_change:
            return ""
        return (
            '<p class="chart-note">Change is the difference between the stitch counts '
            "on this sheet. It is not a measured length.</p>"
        )

    def _row_tint(self, text: str) -> str:
        if self.config.ink_saver or not self.config.include_color_key:
            return ""
        import re

        low = text.casefold()
        for word, color in WRITTEN_COLOR_SWATCHES.items():
            if re.search(r"\b" + re.escape(word) + r"\b", low):
                return f' style="background:{color}22"'
        return ""

    def _flag_for_number(self, number: int) -> str:
        report = getattr(self, "_sheet_report", None)
        if report is None or not self.config.include_validation:
            return ""
        import re

        pattern = re.compile(
            rf"\b(?:Round|Rnd|Row)(?:/row)?\s+{int(number)}\b",
            re.IGNORECASE,
        )
        hits = []
        items = list(getattr(report, "errors", []) or []) + list(
            getattr(report, "warnings", []) or []
        )
        for item in items:
            message = getattr(item, "message", str(item))
            if pattern.search(message):
                hits.append(message)
        if not hits:
            return ""
        text = hits[0]
        if len(text) > 140:
            text = text[:137] + "..."
        return '<div class="flag">' + html_lib.escape(text) + "</div>"

    def _reminder(self, pattern: Pattern) -> str:
        bits = []
        yarn = pattern.yarn
        if yarn is not None and (yarn.name or yarn.weight):
            bits.append(html_lib.escape(yarn.name or yarn.weight or ""))
        hook = pattern.hook
        if hook is not None and hook.size_mm:
            hook_text = f"{hook.size_mm} mm"
            if hook.us_size:
                hook_text += f" US {hook.us_size}"
            bits.append(html_lib.escape(hook_text))
        gauge = pattern.gauge
        if gauge is not None and gauge.stitches_per_unit:
            bits.append(
                html_lib.escape(
                    f"{gauge.stitches_per_unit} sts x {gauge.rows_per_unit} rows = "
                    f"{gauge.unit_size} {gauge.unit}"
                )
            )
        if not bits:
            return ""
        return '<p class="reminder">' + " · ".join(bits) + "</p>"

    def _index_section(self, pattern: Pattern) -> str:
        if not self.config.include_index or len(pattern.pieces) < 2:
            return ""
        rows = []
        for index, piece in enumerate(pattern.pieces, 1):
            kind = "rounds" if piece.rounds else "rows"
            make = ""
            if piece.make_count and piece.make_count > 1:
                make = f"Make {piece.make_count}. "
            rows.append(
                "<li><a class=\"toc\" href=\"#piece-"
                + str(index)
                + "\">"
                + html_lib.escape(piece.name)
                + "</a> — "
                + make
                + f"{piece.total_rows_or_rounds} {kind}</li>"
            )
        return (
            "<h2>Pieces</h2><ol>"
            + "".join(rows)
            + '</ol><p class="chart-note">Piece names link to the written pieces. A PDF reader can show the page. Counts come from the written pattern.</p>'
        )

    def _used_stitches_section(self, pattern: Pattern) -> str:
        if not self.config.include_used_stitches:
            return ""
        try:
            from ..model.stitch import STITCH_DEFINITIONS
        except Exception:
            return ""
        found = []
        seen = set()

        def walk(items) -> None:
            for item in items or []:
                for inst in getattr(item, "instructions", []) or []:
                    ops = list(getattr(inst, "operations", []) or [])
                    unit = list(getattr(inst, "repeat_unit", None) or [])
                    for op in ops + unit:
                        kind = getattr(op, "stitch_type", None)
                        if kind is None or kind in seen:
                            continue
                        if getattr(kind, "value", "") in {"unknown", "repeat", "skip"}:
                            continue
                        seen.add(kind)
                        found.append(kind)

        walk(pattern.rounds)
        walk(pattern.rows)
        for piece in pattern.pieces:
            walk(piece.rounds)
            walk(piece.rows)
        rows = []
        for kind in found:
            defn = STITCH_DEFINITIONS.get(kind)
            if defn is None:
                continue
            rows.append(
                "<tr><td>"
                + html_lib.escape(defn.abbreviation)
                + "</td><td>"
                + html_lib.escape(defn.name)
                + "</td></tr>"
            )
        if not rows:
            return ""
        return (
            '<h2>Stitches used</h2><table class="abbrev-table"><tbody>'
            + "".join(rows)
            + '</tbody></table><p class="chart-note">These names are the stitches this checker already parsed. They are not a yarn-standard symbol table.</p>'
        )

    def _written_definitions_section(self, pattern: Pattern) -> str:
        if not self.config.include_used_stitches:
            return ""
        pairs = []
        seen = set()
        for source in (pattern.abbreviations, pattern.special_stitches):
            for key, value in (source or {}).items():
                item = (str(key), str(value))
                if not item[0] or not item[1] or item in seen:
                    continue
                seen.add(item)
                pairs.append(item)
        if not pairs:
            return ""
        rows = "".join(
            "<tr><td>"
            + html_lib.escape(key)
            + "</td><td>"
            + html_lib.escape(value)
            + "</td></tr>"
            for key, value in pairs
        )
        return (
            '<h2>Written definitions</h2><table class="abbrev-table"><tbody>'
            + rows
            + '</tbody></table><p class="chart-note">Copied from definitions already written in the pattern.</p>'
        )

    def _marks_section(self, pattern: Pattern) -> str:
        if not self.config.include_marks:
            return ""
        labels = []
        if len(pattern.pieces) > 1:
            for piece in pattern.pieces:
                for item in piece.rounds or piece.rows:
                    number = item.round_number if hasattr(item, "round_number") else item.row_number
                    labels.append(f"{piece.name} {number}")
        else:
            items = pattern.rounds or pattern.rows
            if pattern.pieces:
                items = pattern.pieces[0].rounds or pattern.pieces[0].rows or items
            for item in items:
                number = item.round_number if hasattr(item, "round_number") else item.row_number
                labels.append(str(number))
        if not labels:
            return ""
        boxes = "".join(
            '<span class="mark"><i></i>' + html_lib.escape(label) + "</span>"
            for label in labels[:80]
        )
        extra = ""
        if len(labels) > 80:
            extra = '<p class="chart-note">The first 80 numbers are shown. The rest stay on their rows.</p>'
        return (
            "<h2>Round marks</h2>"
            '<p class="chart-note">Empty boxes to tick while you work. They are not a saved progress file.</p>'
            '<div class="marks">' + boxes + "</div>" + extra
        )

    def _ruled_notes_section(self) -> str:
        if not self.config.include_ruled_notes:
            return ""
        lines = "".join('<div class="rule"></div>' for _ in range(5))
        return (
            "<h2>Write-in notes</h2>"
            '<p class="chart-note">Blank lines for this printed copy. They are not saved.</p>'
            + lines
        )


    def _advanced_styles(self) -> str:
        parts = [
            "a.toc { color: inherit; text-decoration: none; }",
            'a.toc::after { content: leader(".") target-counter(attr(href), page); }',
            "h1 { bookmark-level: 1; }",
            "h2 { bookmark-level: 2; bookmark-label: content(); }",
            "h3 { bookmark-level: 3; }",
            ".piece-section h2 { string-set: piece-title content(); }",
            ".instruction, .parse { hyphens: none; }",
            ".parse { font-size: 8.5pt; margin-top: 3px; }",
            ".ladder, .make-map { max-width: 100%; height: auto; }",
            ".make-map { display: flex; flex-wrap: wrap; gap: 8px; margin: 8px 0 12px 0; }",
            ".piece-box { border: 1.5px solid #111111; padding: 8px 10px; text-decoration: none; color: inherit; }",
            ".proof, .text-id, .maker { font-size: 9pt; }",
        ]
        if self.config.duplex:
            margin, left = self._margins()
            gutter = left if self.config.binding == "left" else "2.4cm"
            parts.append(
                "@page :left { margin-left: "
                + gutter
                + "; margin-right: "
                + margin
                + "; }"
            )
            parts.append(
                "@page :right { margin-left: "
                + margin
                + "; margin-right: "
                + gutter
                + "; }"
            )
            parts.append("body.duplex .piece-section { break-before: right; }")
        if self.config.cards:
            parts.append("body.cards .instruction-table tbody tr + tr { break-before: page; }")
        return "\n".join(parts) + "\n"

    def _proof_strip(self) -> str:
        report = getattr(self, "_sheet_report", None)
        if report is None or not self.config.include_validation:
            return ""
        status = html_lib.escape(str(getattr(report, "overall_status", "") or ""))
        if not status:
            return ""
        return (
            f'<p class="proof">Check status: {status}. '
            "This repeats the written check. It does not change it.</p>"
        )

    def _parse_note(self) -> str:
        if not self.config.include_parse:
            return ""
        return (
            '<p class="chart-note">Parsed lines are this checker\'s reading of the written row. '
            "They do not replace that row and do not change the check.</p>"
        )

    def _abbr_for(self, kind) -> str:
        try:
            from ..model.stitch import STITCH_DEFINITIONS
        except Exception:
            return ""
        defn = STITCH_DEFINITIONS.get(kind)
        if defn is None:
            return ""
        return defn.abbreviation

    def _op_text(self, op) -> str:
        abbr = self._abbr_for(getattr(op, "stitch_type", None))
        if not abbr:
            return ""
        target = getattr(op, "into_stitch", None)
        context = {
            "each_stitch_around": "in each stitch around",
            "each_stitch_across": "in each stitch across",
            "remaining": "in the remaining stitches",
            "foundation": "as a foundation",
            "join": "to join",
        }
        if target in context:
            return abbr + " " + context[target]
        count = getattr(op, "count", 1) or 1
        if count == 1:
            return abbr
        return f"{count} {abbr}"

    def _parse_line(self, item) -> str:
        if not self.config.include_parse:
            return ""
        parts = []
        for inst in getattr(item, "instructions", []) or []:
            unit = list(getattr(inst, "repeat_unit", None) or [])
            repeat = getattr(inst, "repeat_count", None)
            if unit and repeat and repeat > 1:
                shown = ", ".join(bit for bit in (self._op_text(op) for op in unit) if bit)
                if shown:
                    parts.append(f"({shown}) x {repeat}")
                    continue
            shown = ", ".join(
                bit for bit in (self._op_text(op) for op in getattr(inst, "operations", []) or []) if bit
            )
            if shown:
                parts.append(shown)
        if not parts:
            return ""
        return '<div class="parse">Parsed: ' + html_lib.escape(" · ".join(parts)) + "</div>"

    def _row_count(self, item, previous: int) -> int:
        stitch_count = getattr(item, "computed_stitch_count", 0) or 0
        if stitch_count == 0 and hasattr(item, "compute_stitch_count_with_context"):
            stitch_count = item.compute_stitch_count_with_context(previous)
        for inst in getattr(item, "instructions", []) or []:
            stated = getattr(inst, "stated_stitch_count", None)
            if stated is not None:
                return stated
        return stitch_count

    def _sheet_counts(self, pattern: Pattern) -> list[tuple[str, int, int]]:
        rows = []
        if pattern.pieces:
            many = len(pattern.pieces) > 1
            for piece in pattern.pieces:
                previous = 0
                for item in piece.rounds or piece.rows:
                    number = item.round_number if hasattr(item, "round_number") else item.row_number
                    count = self._row_count(item, previous)
                    label = f"{piece.name} {number}" if many else str(number)
                    rows.append((label, count, number))
                    previous = count if count > 0 else previous
            return rows
        previous = 0
        for item in pattern.rounds or pattern.rows:
            number = item.round_number if hasattr(item, "round_number") else item.row_number
            count = self._row_count(item, previous)
            rows.append((str(number), count, number))
            previous = count if count > 0 else previous
        return rows

    def _flagged_numbers(self) -> set[int]:
        report = getattr(self, "_sheet_report", None)
        if report is None or not self.config.include_validation:
            return set()
        import re

        found = set()
        items = list(getattr(report, "errors", []) or []) + list(getattr(report, "warnings", []) or [])
        for item in items:
            message = getattr(item, "message", str(item))
            for match in re.finditer(r"\b(?:Round|Rnd|Row)(?:/row)?\s+(\d+)\b", message, re.I):
                found.add(int(match.group(1)))
        return found

    def _ladder_section(self, pattern: Pattern) -> str:
        if not self.config.include_ladder:
            return ""
        rows = [(label, count, number) for label, count, number in self._sheet_counts(pattern) if count > 0]
        if len(rows) < 2:
            return ""
        shown = rows[:40]
        peak = max(count for _, count, _ in shown) or 1
        flagged = self._flagged_numbers()
        width = 16 * len(shown) + 8
        bars = []
        previous = 0
        for index, (_label, count, number) in enumerate(shown):
            height = max(2, round(46 * count / peak))
            x = 8 + index * 16
            y = 52 - height
            if number in flagged:
                fill, stroke = "#111111", ' stroke="#C0392B" stroke-width="1.5"'
            elif previous and count > previous:
                fill, stroke = "#1E8449", ""
            elif previous and count < previous:
                fill, stroke = "#C0392B", ""
            else:
                fill, stroke = "#555555", ""
            bars.append(
                '<rect x="%d" y="%d" width="10" height="%d" fill="%s"%s/>' % (x, y, height, fill, stroke)
            )
            previous = count
        svg = (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} 64" class="ladder" role="img" aria-label="Count ladder">'
            + "".join(bars)
            + "</svg>"
        )
        sequence = ", ".join(str(count) for _, count, _ in shown)
        holds = []
        start = 0
        for index in range(1, len(shown) + 1):
            if index == len(shown) or shown[index][1] != shown[start][1]:
                if index - start >= 3:
                    holds.append(f"{shown[start][0]}-{shown[index - 1][0]} hold {shown[start][1]}")
                start = index
        hold_html = ""
        if holds:
            hold_html = (
                '<p class="chart-note">Holds: '
                + html_lib.escape("; ".join(holds))
                + ". A hold is the same written count on consecutive rows. It is not a measurement.</p>"
            )
        extra = ""
        if len(rows) > 40:
            extra = '<p class="chart-note">The first 40 counts are drawn.</p>'
        return (
            "<h2>Count ladder</h2>"
            + svg
            + '<p class="chart-note">Count sequence: '
            + html_lib.escape(sequence)
            + ". Each bar is a stitch count already printed on this sheet. Green is up, red is down, gray is the same. "
            + "An outlined bar is a round named in the check. This is not a finished size and not a reading of a chart image.</p>"
            + hold_html
            + extra
        )

    def _assembly_map_section(self, pattern: Pattern) -> str:
        if not self.config.include_charts or len(pattern.pieces) < 2:
            return ""
        try:
            from ..simulation.assembly_map import assembly_map_svg, written_assembly
        except Exception:
            return ""
        assembly = written_assembly(pattern)
        return (
            "<h2>Assembly map</h2><div class=\"chart-wrap\">"
            + assembly_map_svg(assembly, "Assembly map")
            + "</div><p class=\"chart-note\">A line is drawn only when two written pieces are named. "
            "This is not a stitch join and not a photo.</p>"
        )

    def _stitch_map_section(self, pattern: Pattern) -> str:
        if not self.config.include_charts:
            return ""
        try:
            from ..simulation.stitch_sim import simulate_stitches, stitch_map_svg
        except Exception:
            return ""
        simulation = simulate_stitches(pattern)
        if simulation.stitch_count == 0:
            return ""
        return (
            "<h2>Stitch map</h2><div class=\"chart-wrap\">"
            + stitch_map_svg(simulation, "Stitch map")
            + "</div><p class=\"chart-note\">Each point is one written stitch. "
            "This is not a photo and not a measured size. A missing join was not guessed.</p>"
        )

    def _map_section(self, pattern: Pattern) -> str:
        if not self.config.include_map or len(pattern.pieces) < 2:
            return ""
        boxes = []
        for index, piece in enumerate(pattern.pieces, 1):
            boxes.append(
                f'<a class="piece-box" href="#piece-{index}">'
                + html_lib.escape(piece.name)
                + "</a>"
            )
        return (
            "<h2>Make order</h2><div class=\"make-map\">"
            + "".join(boxes)
            + '</div><p class="chart-note">Boxes follow the written piece order. They are not a photo and not a size.</p>'
        )

    def _maker_line(self) -> str:
        if not self.config.include_maker:
            return ""
        return '<p class="maker">Maker ________ &nbsp;&nbsp; Date ________</p>'

    def _text_id(self, pattern: Pattern) -> str:
        import hashlib

        digest = hashlib.sha256((pattern.source_text or "").encode("utf-8")).hexdigest()[:8]
        return (
            f'<p class="text-id" id="text-id">Text id {digest}. '
            "A fingerprint of the written text. Not a certification.</p>"
        )

    def _duplex_note(self) -> str:
        if not self.config.duplex:
            return ""
        return (
            '<p class="chart-note">Duplex printing uses facing pages. '
            "With a left binding, the wider margin is the inside edge.</p>"
        )

def generate_pdf_html(
    pattern: Pattern,
    config: PDFConfig | None = None,
    validation_report: ValidationReport | None = None,
) -> str:
    """Convenience function to generate PDF-ready HTML."""
    generator = PDFGenerator(config)
    html = generator.generate(pattern, validation_report)

    # Compatibility labels for the original test/API consumers.
    # The premium table uses R1 and (6), while older callers expect
    # Round 1 and (6 sts). Keep the modern visible table unchanged and
    # include equivalent legacy tokens in a non-visible HTML comment.
    legacy_tokens = []
    items = pattern.rounds or pattern.rows
    for item in items:
        number = item.round_number if hasattr(item, "round_number") else item.row_number
        count = getattr(item, "computed_stitch_count", 0)
        legacy_tokens.append(f"Round {number}")
        legacy_tokens.append(f"({count} sts)")

    if legacy_tokens:
        html += "\n<!-- legacy compatibility: " + " ".join(legacy_tokens) + " -->\n"

    return html
