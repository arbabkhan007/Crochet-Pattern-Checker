"""
PDF generation engine for crochet patterns.

Generates professional, print-ready documents from validated patterns.
Multiple templates with beautiful typography and layouts.
"""

from __future__ import annotations

import html as html_lib
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

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


class PDFGenerator:
    """Generates professional PDF documents from crochet patterns."""

    def __init__(self, config: Optional[PDFConfig] = None) -> None:
        self.config = config or PDFConfig()
        self.theme = TEMPLATES.get(self.config.template, TEMPLATES["minimal"])

    def generate(self, pattern: Pattern, validation_report: Optional[ValidationReport] = None) -> str:
        """Generate the complete HTML document."""
        measurements = measure_pattern(pattern)
        sections = []

        if self.config.include_cover:
            sections.append(self._cover_page(pattern, measurements))

        sections.append(self._materials_section(pattern))

        if self.config.include_abbreviations:
            sections.append(self._abbreviations_section())

        sections.append(self._multi_piece_instructions_section(pattern, measurements))

        if self.config.include_measurements:
            sections.append(self._measurements_section(measurements))

        if self.config.include_validation and validation_report:
            sections.append(self._validation_section(validation_report))

        if self.config.copyright_text or self.config.designer_name:
            sections.append(self._footer_section())

        return self._wrap_document("\n".join(sections), pattern)

    def save(self, filepath: str, pattern: Pattern, validation_report: Optional[ValidationReport] = None) -> None:
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
        styles = self._get_styles()
        title = html_lib.escape(pattern.metadata.title or "Crochet Pattern")
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
{styles}
    </style>
</head>
<body>
{body}
</body>
</html>"""

    def _get_styles(self) -> str:
        """Get CSS styles based on template."""
        t = self.theme
        return f"""
        @page {{
            size: {self.config.page_size};
            margin: 1.8cm;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: {t['font_body']};
            color: {t['primary']};
            line-height: 1.7;
            max-width: 210mm;
            margin: 0 auto;
            padding: 15mm;
            background: {t['bg']};
            font-size: 11pt;
        }}
        .page-break {{ page-break-before: always; }}

        /* Headings */
        h1 {{
            font-family: {t['font_heading']};
            font-size: 32px;
            margin-bottom: 12px;
            color: {t['primary']};
            letter-spacing: -0.5px;
        }}
        h2 {{
            font-family: {t['font_heading']};
            font-size: 20px;
            margin: 30px 0 15px 0;
            color: {t['primary']};
            border-bottom: 2px solid {t['accent']};
            padding-bottom: 8px;
            letter-spacing: 0.3px;
        }}
        h3 {{
            font-family: {t['font_heading']};
            font-size: 15px;
            margin: 20px 0 10px 0;
            color: {t['secondary']};
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
            border-bottom: 1px solid {t['border']};
        }}
        th {{
            background: {t['card_bg']};
            font-weight: bold;
            color: {t['primary']};
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
            color: {t['secondary']};
            margin-bottom: 8px;
            font-style: italic;
        }}
        .cover .description {{
            font-size: 12px;
            color: {t['secondary']};
            margin: 15px auto;
            max-width: 400px;
            line-height: 1.6;
        }}
        .cover .designer {{
            font-size: 14px;
            color: {t['accent']};
            margin-top: 30px;
            font-weight: bold;
            letter-spacing: 1px;
            text-transform: uppercase;
        }}
        .cover .date {{
            font-size: 11px;
            color: {t['secondary']};
            margin-top: 8px;
        }}

        /* Info boxes */
        .info-box {{
            background: {t['card_bg']};
            border-radius: 10px;
            padding: 20px;
            margin: 15px 0;
            border-left: 4px solid {t['accent']};
        }}
        .info-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px 20px;
        }}
        .info-item {{ padding: 5px 0; }}
        .info-label {{
            font-weight: bold;
            color: {t['secondary']};
            font-size: 9pt;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .info-value {{
            color: {t['primary']};
            font-size: 11pt;
        }}

        /* Rounds/Rows */
        .round {{
            margin: 10px 0;
            padding: 10px 15px;
            border-left: 3px solid {t['accent']};
            background: {t['round_bg']};
            border-radius: 0 6px 6px 0;
            position: relative;
        }}
        .round:hover {{
            background: {t['card_bg']};
        }}
        .round-number {{
            font-weight: bold;
            color: {t['accent']};
            font-size: 11pt;
            font-family: {t['font_mono']};
        }}
        .round-range {{
            font-weight: bold;
            color: {t['accent']};
            font-size: 11pt;
            font-family: {t['font_mono']};
            background: {t['card_bg']};
            padding: 2px 8px;
            border-radius: 4px;
            display: inline-block;
            margin-right: 8px;
        }}
        .stitch-count {{
            float: right;
            color: {t['secondary']};
            font-size: 10pt;
            font-family: {t['font_mono']};
            background: {t['card_bg']};
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
            background: {t['card_bg']};
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            border-top: 3px solid {t['accent']};
        }}
        .measurement-value {{
            font-size: 28px;
            font-weight: bold;
            color: {t['accent']};
            font-family: {t['font_heading']};
        }}
        .measurement-label {{
            font-size: 10px;
            color: {t['secondary']};
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
            border-top: 1px solid {t['border']};
            font-size: 9pt;
            color: {t['secondary']};
            text-align: center;
        }}

        /* Materials grid */
        .materials-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            margin: 10px 0;
        }}
        .material-card {{
            background: {t['bg']};
            border: 1px solid {t['border']};
            border-radius: 8px;
            padding: 12px;
        }}
        .material-label {{
            font-size: 9pt;
            color: {t['secondary']};
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .material-value {{
            font-size: 12pt;
            color: {t['primary']};
            font-weight: bold;
            margin-top: 3px;
        }}

        /* Abbreviation table */
        .abbrev-table td:first-child {{
            font-weight: bold;
            font-family: {t['font_mono']};
            color: {t['accent']};
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
            background: {t['accent']};
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
            border-bottom: 1px solid {t['border']};
        }}
        .instruction-table tbody tr:nth-child(even) {{
            background: {t['round_bg']};
        }}
        .instruction-table tbody tr:hover {{
            background: {t['card_bg']};
        }}
        .instruction-table .round-num {{
            font-weight: bold;
            font-family: {t['font_mono']};
            color: {t['accent']};
            width: 60px;
        }}
        .instruction-table .instruction {{
            font-family: {t['font_mono']};
            font-size: 9.5pt;
        }}
        .instruction-table .stitch-count {{
            font-family: {t['font_mono']};
            font-weight: bold;
            color: {t['secondary']};
            text-align: center;
            width: 70px;
        }}
        .instruction-table .note {{
            font-size: 9pt;
            color: {t['secondary']};
            font-style: italic;
            width: 120px;
        }}
        .construction-info {{
            margin: 10px 0 20px 0;
            font-size: 10pt;
            color: {t['secondary']};
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
            color: {t['primary']};
            border-bottom: 3px solid {t['accent']};
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}

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
        if category: subtitle_parts.append(category)
        if difficulty: subtitle_parts.append(f"Difficulty: {difficulty}")
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

        desc_html = f'<p class="description">{description}</p>' if description else ''

        return f"""
<div class="cover">
    <h1>{title}</h1>
    {f'<p class="subtitle">{subtitle}</p>' if subtitle else ''}
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
            cards.append(f'<div class="material-card"><div class="material-label">Yarn</div><div class="material-value">{display}</div></div>')
        else:
            cards.append('<div class="material-card"><div class="material-label">Yarn</div><div class="material-value">[Specify yarn]</div></div>')

        # Hook
        if pattern.hook and pattern.hook.size_mm:
            hook_text = f"{pattern.hook.size_mm} mm"
            if pattern.hook.us_size:
                hook_text += f" (US {pattern.hook.us_size})"
            cards.append(f'<div class="material-card"><div class="material-label">Hook</div><div class="material-value">{hook_text}</div></div>')
        else:
            cards.append('<div class="material-card"><div class="material-label">Hook</div><div class="material-value">[Specify hook size]</div></div>')

        # Gauge
        if pattern.gauge and pattern.gauge.stitches_per_unit:
            gauge_text = f"{pattern.gauge.stitches_per_unit} sts × {pattern.gauge.rows_per_unit} rows = {pattern.gauge.unit_size} {pattern.gauge.unit}"
            cards.append(f'<div class="material-card"><div class="material-label">Gauge</div><div class="material-value">{gauge_text}</div></div>')

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
            ("MR", "Magic Ring"), ("ch", "Chain"), ("sl st", "Slip Stitch"),
            ("sc", "Single Crochet"), ("hdc", "Half Double Crochet"),
            ("dc", "Double Crochet"), ("tr", "Treble Crochet"),
            ("inc", "Increase (2 in 1)"), ("dec", "Decrease"),
            ("invdec", "Invisible Decrease"), ("st(s)", "Stitch(es)"),
            ("rep", "Repeat"), ("FO", "Fasten Off"),
        ]
        rows = "\n".join(f"<tr><td>{ab}</td><td>{name}</td></tr>" for ab, name in abbrevs)
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
        stripped = re.sub(r'^(Round|Rnd|Row)\s+\d+(-\d+)?:\s*', '', text, flags=re.IGNORECASE)
        return stripped.strip()

    def _instructions_section(self, pattern: Pattern, measurements: PatternMeasurements) -> str:
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
                num = r.round_number if hasattr(r, 'round_number') else r.row_number
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
                first_num = rounds_in_group[0].round_number if hasattr(rounds_in_group[0], 'round_number') else rounds_in_group[0].row_number
                last_num = rounds_in_group[-1].round_number if hasattr(rounds_in_group[-1], 'round_number') else rounds_in_group[-1].row_number

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
            items_html = "\n".join(f"<p>{html_lib.escape(f)}</p>" for f in pattern.finishing)
            finishing_html = f"<h3>Finishing</h3>{items_html}"

        construction = pattern.construction.value.replace("_", " ").title()

        return f"""
<h2>Instructions</h2>
<p><strong>Construction:</strong> {construction}</p>
{notes_html}
{"".join(rounds_html)}
{finishing_html}
"""

    def _instructions_table_section(self, pattern: Pattern, measurements: PatternMeasurements) -> str:
        """Generate instructions in professional table format (Round | Instruction | Stitches | Notes)."""
        items = pattern.rounds or pattern.rows
        if not items:
            return "<h2>Instructions</h2><p>No instructions found in pattern.</p>"

        label = "Round" if pattern.rounds else "Row"
        
        # Build table rows
        table_rows = []
        prev_count = 0
        
        for item in items:
            round_num = item.round_number if hasattr(item, 'round_number') else item.row_number
            
            # Get instruction text (strip "Round X:" prefix)
            instruction_text = self._strip_round_header(item.source_text) if hasattr(item, 'source_text') else ""
            
            # Get stitch count
            stitch_count = 0
            if hasattr(item, 'computed_stitch_count'):
                stitch_count = item.computed_stitch_count
            if stitch_count == 0 and hasattr(item, 'compute_stitch_count_with_context'):
                stitch_count = item.compute_stitch_count_with_context(prev_count)
            
            # Check if any instruction has a stated count (more reliable)
            if hasattr(item, 'instructions'):
                for inst in item.instructions:
                    if hasattr(inst, 'stated_stitch_count') and inst.stated_stitch_count is not None:
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
                    <td class="instruction">{html_lib.escape(instruction_text)}</td>
                    <td class="stitch-count">({stitch_count})</td>
                    <td class="note">{note}</td>
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
                    <th>Notes</th>
                </tr>
            </thead>
            <tbody>
                {''.join(table_rows)}
            </tbody>
        </table>
        """
        
        # Add notes section if present
        notes_html = ""
        if pattern.notes:
            notes_content = "".join(f"<p>{html_lib.escape(n)}</p>" for n in pattern.notes)
            notes_html = f'<div class="pattern-notes"><strong>Pattern Notes:</strong>{notes_content}</div>'
        
        # Add finishing section if present
        finishing_html = ""
        if pattern.finishing:
            finishing_content = "".join(f"<p>{html_lib.escape(f)}</p>" for f in pattern.finishing)
            finishing_html = f"<h3>Finishing Instructions</h3>{finishing_content}"
        
        construction = pattern.construction.value.replace("_", " ").title()
        
        return f"""
<h2>Instructions</h2>
<p class="construction-info"><strong>Construction:</strong> {construction}</p>
{notes_html}
{table_html}
{finishing_html}
"""

    def _multi_piece_instructions_section(self, pattern: Pattern, measurements: PatternMeasurements) -> str:
        """Generate multi-piece instructions with separate sections for each piece."""
        import html as html_lib
        
        if not pattern.pieces:
            # Fall back to single-piece format
            return self._instructions_table_section(pattern, measurements)
        
        sections_html = []
        
        for i, piece in enumerate(pattern.pieces):
            # Section header
            make_text = f" (make {piece.make_count})" if piece.make_count and piece.make_count > 1 else ""
            section_num = i + 1
            
            section_header = f"""
<div class="page-break"></div>
<div class="piece-section">
    <h2>Section {section_num}: {piece.name}{make_text}</h2>
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
                round_num = item.round_number if hasattr(item, 'round_number') else item.row_number
                
                # Get instruction text
                instruction_text = self._strip_round_header(item.source_text) if hasattr(item, 'source_text') else ""
                
                # Get stitch count
                stitch_count = 0
                if hasattr(item, 'computed_stitch_count'):
                    stitch_count = item.computed_stitch_count
                if stitch_count == 0 and hasattr(item, 'compute_stitch_count_with_context'):
                    stitch_count = item.compute_stitch_count_with_context(prev_count)
                
                # Check if any instruction has a stated count
                if hasattr(item, 'instructions'):
                    for inst in item.instructions:
                        if hasattr(inst, 'stated_stitch_count') and inst.stated_stitch_count is not None:
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
                first_round_num = items[0].round_number if hasattr(items[0], 'round_number') else items[0].row_number
                piece_round_num = round_num - (first_round_num - 1)
                round_display = f"R{piece_round_num}" if piece.rounds else f"Row {piece_round_num}"
                
                table_rows.append(f"""
                    <tr>
                        <td class="round-num">{round_display}</td>
                        <td class="instruction">{html_lib.escape(instruction_text)}</td>
                        <td class="stitch-count">({stitch_count})</td>
                        <td class="note">{note}</td>
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
                        <th>Notes</th>
                    </tr>
                </thead>
                <tbody>
                    {''.join(table_rows)}
                </tbody>
            </table>
            """
            
            # Add piece notes if any
            piece_notes_html = ""
            if piece.notes:
                notes_content = "".join(f"<p>{html_lib.escape(n)}</p>" for n in piece.notes)
                piece_notes_html = f'<div class="pattern-notes">{notes_content}</div>'
            
            section_html = section_header + piece_notes_html + table_html + "</div>"
            sections_html.append(section_html)
        
        return "\n".join(sections_html)

    def _measurements_section(self, measurements: PatternMeasurements) -> str:
        """Generate the finished measurements section."""
        return f"""
<div class="page-break"></div>
<h2>Finished Measurements</h2>
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
        status_class = "success" if "PASS" in status else "warning" if "REVIEW" in status else "error"

        errors_html = ""
        if report.errors:
            items = "\n".join(f"<li><strong>[{e.location}]</strong> {html_lib.escape(e.message)}</li>" for e in report.errors)
            errors_html = f"<h3>Errors Found</h3><ul>{items}</ul>"

        warnings_html = ""
        if report.warnings:
            items = "\n".join(f"<li><strong>[{w.location}]</strong> {html_lib.escape(w.message)}</li>" for w in report.warnings[:5])
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
        elif hasattr(self, '_parsed_designer'):
            parts.append(f"Designed by {html_lib.escape(self._parsed_designer)}")
        if self.config.copyright_text:
            parts.append(html_lib.escape(self.config.copyright_text))
        parts.append(f"Generated with Crochet Pattern Checker v0.6.0 · {datetime.now().year}")

        text = " · ".join(parts)
        return f'<div class="footer">{text}</div>'


def generate_pdf_html(pattern: Pattern, config: Optional[PDFConfig] = None,
                      validation_report: Optional[ValidationReport] = None) -> str:
    """Convenience function to generate PDF-ready HTML."""
    generator = PDFGenerator(config)
    return generator.generate(pattern, validation_report)
