"""PDF generation engine for crochet patterns."""
from __future__ import annotations
import html as html_lib
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from ..model.pattern import Pattern
from ..validation import ValidationReport
from ..visualization.measurements import PatternMeasurements, measure_pattern


TEMPLATES = {
    "minimal": {"primary": "#2C3E50", "secondary": "#7F8C8D", "accent": "#4A90D9", "bg": "#FFFFFF", "card_bg": "#F8F9FA", "round_bg": "#FAFBFC", "border": "#E0E0E0", "font_heading": "Georgia, serif", "font_body": "Georgia, serif", "font_mono": "Courier New, monospace"},
    "craft": {"primary": "#5B4A69", "secondary": "#9B8EA8", "accent": "#E8A87C", "bg": "#FFF8F0", "card_bg": "#FFF0E5", "round_bg": "#FFF5ED", "border": "#E8D5C4", "font_heading": "Palatino, serif", "font_body": "Palatino, serif", "font_mono": "Courier New, monospace"},
    "modern": {"primary": "#1A1A2E", "secondary": "#16213E", "accent": "#E94560", "bg": "#FFFFFF", "card_bg": "#F5F5F5", "round_bg": "#FAFAFA", "border": "#E0E0E0", "font_heading": "Helvetica Neue, Arial, sans-serif", "font_body": "Helvetica Neue, Arial, sans-serif", "font_mono": "SF Mono, monospace"},
    "ocean": {"primary": "#0B3D2E", "secondary": "#1A6B52", "accent": "#38A3A5", "bg": "#F0F8F5", "card_bg": "#E5F5EE", "round_bg": "#F0FAF5", "border": "#C5E0D5", "font_heading": "Garamond, serif", "font_body": "Garamond, serif", "font_mono": "Courier New, monospace"},
    "berry": {"primary": "#6B2D5B", "secondary": "#A04E8C", "accent": "#D4738E", "bg": "#FFF5F8", "card_bg": "#FFE8F0", "round_bg": "#FFF0F5", "border": "#E8C5D5", "font_heading": "Baskerville, serif", "font_body": "Baskerville, serif", "font_mono": "Courier New, monospace"},
    "sunset": {"primary": "#C0392B", "secondary": "#E67E22", "accent": "#F39C12", "bg": "#FFFAF0", "card_bg": "#FFF5E5", "round_bg": "#FFF8ED", "border": "#F0D5B5", "font_heading": "Copperplate, serif", "font_body": "Optima, sans-serif", "font_mono": "Courier New, monospace"},
}

class PDFConfig(BaseModel):
    template: str = "minimal"
    include_cover: bool = True
    include_abbreviations: bool = True
    include_validation: bool = True
    include_measurements: bool = True
    designer_name: str = ""
    copyright_text: str = ""
    pattern_version: str = "1.0"

class PDFGenerator:
    def __init__(self, config=None):
        self.config = config or PDFConfig()
        self.theme = TEMPLATES.get(self.config.template, TEMPLATES["minimal"])
    def generate(self, pattern, validation_report=None):
        m = measure_pattern(pattern); s = []
        if self.config.include_cover: s.append(self._cover(pattern, m))
        s.append(self._materials(pattern))
        if self.config.include_abbreviations: s.append(self._abbrevs())
        s.append(self._instructions(pattern, m))
        if self.config.include_measurements: s.append(self._measurements(m))
        if self.config.include_validation and validation_report: s.append(self._validation(validation_report))
        if self.config.designer_name or self.config.copyright_text: s.append(self._footer())
        return self._wrap(chr(10).join(s), pattern)
    def save(self, filepath, pattern, validation_report=None):
        from pathlib import Path
        content = self.generate(pattern, validation_report)
        if str(filepath).endswith(".pdf"):
            try:
                from weasyprint import HTML
                HTML(string=content).write_pdf(filepath)
            except ImportError:
                html_path = str(filepath).replace(".pdf", ".html")
                Path(html_path).write_text(content, encoding="utf-8")
                raise ImportError(f"WeasyPrint not installed. Saved HTML to {html_path}. Install: pip install weasyprint")
        else:
            Path(filepath).write_text(content, encoding="utf-8")
    def _wrap(self, body, pattern):
        t = html_lib.escape(pattern.metadata.title or "Crochet Pattern")
        return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><title>{t}</title>
<style>
@page {{ size: A4; margin: 2cm; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: Georgia, serif; color: #2C3E50; line-height: 1.6; max-width: 210mm; margin: 0 auto; padding: 20mm; }}
.page-break {{ page-break-before: always; }}
h1 {{ font-size: 28px; margin-bottom: 10px; }}
h2 {{ font-size: 20px; margin: 30px 0 15px 0; border-bottom: 2px solid #EEE; padding-bottom: 8px; }}
h3 {{ font-size: 16px; margin: 20px 0 10px 0; }}
p {{ margin: 8px 0; }}
table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
th, td {{ padding: 8px 12px; text-align: left; border-bottom: 1px solid #EEE; }}
th {{ background: #F8F9FA; font-weight: bold; }}
.cover {{ text-align: center; padding: 80px 0; page-break-after: always; }}
.cover h1 {{ font-size: 42px; margin-bottom: 20px; }}
.cover .subtitle {{ font-size: 18px; color: #7F8C8D; margin-bottom: 30px; }}
.cover .designer {{ font-size: 16px; color: #95A5A6; margin-top: 40px; }}
.info-box {{ background: #F8F9FA; border-radius: 8px; padding: 20px; margin: 15px 0; }}
.info-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }}
.round {{ margin: 12px 0; padding: 8px 15px; border-left: 3px solid #4A90D9; background: #FAFBFC; }}
.round-number {{ font-weight: bold; color: #4A90D9; }}
.stitch-count {{ float: right; color: #7F8C8D; font-size: 14px; }}
.note {{ background: #FFF3CD; border-radius: 5px; padding: 12px; margin: 10px 0; border-left: 4px solid #FFC107; }}
.success {{ color: #27AE60; }} .warning {{ color: #F39C12; }} .error {{ color: #E74C3C; }}
.footer {{ margin-top: 60px; padding-top: 20px; border-top: 1px solid #EEE; font-size: 12px; color: #999; text-align: center; }}
.measurement-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin: 15px 0; }}
.measurement-card {{ background: #F0F7FF; border-radius: 8px; padding: 15px; text-align: center; }}
.measurement-value {{ font-size: 24px; font-weight: bold; color: #2980B9; }}
.measurement-label {{ font-size: 12px; color: #7F8C8D; }}
@media print {{ body {{ padding: 0; }} }}
</style></head><body>{body}</body></html>"""
    def _cover(self, pattern, m):
        t = html_lib.escape(pattern.metadata.title or "Crochet Pattern")
        d = html_lib.escape(self.config.designer_name or "Anonymous")
        return f"""<div class="cover"><h1>{t}</h1>
<div class="info-box" style="max-width:400px;margin:30px auto"><div class="info-grid">
<div><b>Rounds:</b> {m.total_rounds}</div><div><b>Max Stitches:</b> {m.max_stitch_count}</div>
<div><b>Diameter:</b> {m.max_diameter_inches:.1f} in</div><div><b>Height:</b> {m.total_height_inches:.1f} in</div>
</div></div><p class="designer">Designed by {d}</p>
<p class="designer" style="font-size:12px;margin-top:10px">Version {self.config.pattern_version} | {datetime.now().strftime("%B %Y")}</p></div>"""
    def _materials(self, pattern):
        items = []
        if pattern.yarn and pattern.yarn.name: items.append(f"<p><b>Yarn:</b> {html_lib.escape(pattern.yarn.name)}</p>")
        else: items.append("<p><b>Yarn:</b> [Specify yarn]</p>")
        if pattern.hook and pattern.hook.size_mm: items.append(f"<p><b>Hook:</b> {pattern.hook.size_mm}mm</p>")
        else: items.append("<p><b>Hook:</b> [Specify hook size]</p>")
        return f"<h2>Materials</h2><div class='info-box'>{chr(10).join(items)}</div>"
    def _abbrevs(self):
        rows = chr(10).join(f"<tr><td>{a}</td><td>{n}</td></tr>" for a,n in [
            ("ch","Chain"),("sl st","Slip Stitch"),("sc","Single Crochet"),("hdc","Half Double Crochet"),
            ("dc","Double Crochet"),("tr","Treble Crochet"),("inc","Increase (2 in 1)"),("dec","Decrease"),
            ("MR","Magic Ring"),("st(s)","Stitch(es)")])
        return f"<h2>Abbreviations (US)</h2><table><thead><tr><th>Abbr</th><th>Meaning</th></tr></thead><tbody>{rows}</tbody></table>"
    def _instructions(self, pattern, m):
        items = pattern.rounds or pattern.rows
        if not items: return "<h2>Instructions</h2><p>No instructions found.</p>"
        label = "Round" if pattern.rounds else "Row"
        prev = 0; rounds = []
        for i, r in enumerate(items):
            num = r.round_number if hasattr(r,"round_number") else r.row_number
            sc = r.computed_stitch_count
            if sc == 0: sc = r.compute_stitch_count_with_context(prev)
            dc = sc
            for inst in r.instructions:
                if inst.stated_stitch_count is not None: dc = inst.stated_stitch_count; break
            text = html_lib.escape(r.source_text)
            rounds.append(f'<div class="round"><span class="round-number">{label} {num}:</span><span class="stitch-count">({dc} sts)</span><p>{text}</p></div>')
            prev = dc if dc > 0 else prev
        return f"<h2>Instructions</h2><p><b>Construction:</b> {pattern.construction.value.replace(chr(95),' ').title()}</p>{chr(10).join(rounds)}"
    def _measurements(self, m):
        return f"""<h2>Finished Measurements</h2>
<div class="measurement-grid">
<div class="measurement-card"><div class="measurement-value">{m.max_diameter_inches:.1f}"</div><div class="measurement-label">Diameter</div></div>
<div class="measurement-card"><div class="measurement-value">{m.total_height_inches:.1f}"</div><div class="measurement-label">Height</div></div>
<div class="measurement-card"><div class="measurement-value">{m.max_stitch_count}</div><div class="measurement-label">Max Stitches</div></div>
</div>
<table><tr><th>Measurement</th><th>mm</th><th>inches</th></tr>
<tr><td>Max Radius</td><td>{m.max_radius_mm:.1f}</td><td>{m.max_radius_inches:.2f}</td></tr>
<tr><td>Max Circumference</td><td>{m.max_circumference_mm:.1f}</td><td>{m.max_circumference_inches:.2f}</td></tr>
<tr><td>Total Height</td><td>{m.total_height_mm:.1f}</td><td>{m.total_height_inches:.2f}</td></tr></table>"""
    def _validation(self, report):
        s = report.overall_status; sc = report.score
        c = "success" if "PASS" in s else "warning" if "REVIEW" in s else "error"
        errs = ""
        if report.errors:
            errs = "<h3>Errors</h3><ul>" + chr(10).join(f"<li><b>[{e.location}]</b> {html_lib.escape(e.message)}</li>" for e in report.errors) + "</ul>"
        warns = ""
        if report.warnings:
            warns = "<h3>Warnings</h3><ul>" + chr(10).join(f"<li><b>[{w.location}]</b> {html_lib.escape(w.message)}</li>" for w in report.warnings[:5]) + "</ul>"
        return f"""<div class="page-break"></div><h2>Validation Report</h2>
<div class="info-box"><p><b>Status:</b> <span class="{c}">{s}</span></p><p><b>Score:</b> {sc}/100</p>
<p><b>Errors:</b> {len(report.errors)} | <b>Warnings:</b> {len(report.warnings)}</p></div>{errs}{warns}
<p style="margin-top:20px;font-size:12px;color:#999"><i>Validated by Crochet Pattern Checker. Mathematical validation does not guarantee physical correctness.</i></p>"""
    def _footer(self):
        parts = []
        if self.config.designer_name: parts.append(f"Designed by {html_lib.escape(self.config.designer_name)}")
        if self.config.copyright_text: parts.append(html_lib.escape(self.config.copyright_text))
        parts.append(f"Crochet Pattern Checker v0.4.0 | {datetime.now().year}")
        return f'<div class="footer">{" | ".join(parts)}</div>'

def generate_pdf_html(pattern, config=None, validation_report=None):
    return PDFGenerator(config).generate(pattern, validation_report)
