"""PDF generation for crochet patterns.

Produces professional pattern documents as HTML (print-ready, and renderable
to real PDFs via WeasyPrint when installed).
"""
from __future__ import annotations

import html
from pathlib import Path
from typing import Optional

try:
    from pydantic import BaseModel, Field
except Exception:  # pragma: no cover - pydantic is a hard dependency in practice
    BaseModel = object
    def Field(default=None, **_):  # type: ignore
        return default

STITCH_NAMES = {
    "single_crochet": "Single Crochet (sc)",
    "half_double_crochet": "Half Double Crochet (hdc)",
    "double_crochet": "Double Crochet (dc)",
    "treble": "Treble (tr)",
    "slip_stitch": "Slip Stitch (sl st)",
    "chain": "Chain (ch)",
    "increase": "Increase (inc)",
    "decrease": "Decrease (dec)",
    "magic_ring": "Magic Ring (MR)",
}

_CSS = """
<style>
  @page { size: A4; margin: 18mm 16mm; }
  * { box-sizing: border-box; }
  body { font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
         color: #2b2b2b; font-size: 10.5pt; line-height: 1.5; margin: 0; }
  h1 { font-size: 22pt; margin: 0 0 2pt 0; color: #1f2937; }
  h2 { font-size: 13pt; margin: 18pt 0 6pt 0; color: #1f2937;
       border-bottom: 1.5px solid #d1d5db; padding-bottom: 3pt; }
  .meta { color: #6b7280; font-size: 10pt; margin-bottom: 10pt; }
  table { border-collapse: collapse; width: 100%; margin: 6pt 0; }
  th, td { border: 1px solid #d1d5db; padding: 4pt 7pt; text-align: left;
           font-size: 9.5pt; vertical-align: top; }
  th { background: #f3f4f6; }
  .round { margin: 0 0 7pt 0; page-break-inside: avoid; }
  .round .rn { font-weight: 700; }
  .round .count { color: #6b7280; font-size: 9.5pt; }
  .note { background: #f9fafb; border-left: 3px solid #9ca3af;
          padding: 6pt 9pt; margin: 6pt 0; font-size: 9.5pt; }
  .footer { margin-top: 24pt; padding-top: 8pt; border-top: 1px solid #e5e7eb;
            color: #9ca3af; font-size: 8.5pt; }
  .ok { color: #15803d; font-weight: 600; }
  .bad { color: #b91c1c; font-weight: 600; }
</style>
"""


class PDFConfig(BaseModel):
    designer_name: str = ""
    store_name: str = ""
    include_validation: bool = True


def _esc(t: str) -> str:
    return html.escape(str(t))


def _round_label(a: int, b: int) -> str:
    return f"Round {a}" if a == b else f"Rounds {a}-{b}"


def _grouped_rounds(pattern):
    """Merge consecutive rounds/rows that share identical source text (e.g. 'Round 7-12').

    Returns list of dicts: {first, last, text, count}.
    """
    rounds = pattern.rounds if pattern.rounds else pattern.rows
    attr = "round_number" if pattern.rounds else "row_number"
    # Resolve stitch count per round, using context (previous round) where needed.
    counts = {}
    running = 0
    for r in rounds:
        has_ctx = any(op.into_stitch in ("each_stitch_around", "remaining")
                      for i in r.instructions for op in i.operations)
        if has_ctx and running > 0:
            c = r.compute_stitch_count_with_context(running)
        else:
            c = r.computed_stitch_count
        if c == 0:
            c = next((i.stated_stitch_count for i in r.instructions
                      if i.stated_stitch_count is not None), running)
        running = c
        counts[id(r)] = c
    groups = []
    for r in rounds:
        if groups and groups[-1]["text"] == r.source_text:
            groups[-1]["last"] = getattr(r, attr)
        else:
            groups.append({"first": getattr(r, attr), "last": getattr(r, attr),
                           "text": r.source_text, "count": counts[id(r)]})
    return groups


def generate_pdf_html(pattern, validation_report=None, config: Optional[PDFConfig] = None) -> str:
    config = config or PDFConfig()
    title = pattern.metadata.title or "Crochet Pattern"
    designer = config.designer_name or (pattern.metadata.designer or "")
    rows = pattern.rounds if pattern.rounds else pattern.rows
    is_round = bool(pattern.rounds)
    unit = "Round" if is_round else "Row"

    parts = ["<!DOCTYPE html>", "<html><head><meta charset='utf-8'>",
             f"<title>{_esc(title)}</title>", _CSS, "</head><body>"]

    parts.append(f"<h1>{_esc(title)}</h1>")
    meta_bits = []
    if designer:
        meta_bits.append(f"Designed by {_esc(designer)}")
    if config.store_name:
        meta_bits.append(f"<b>{_esc(config.store_name)}</b>")
    meta_bits.append(f"{len(rows)} {unit.lower()}s &middot; {pattern.construction.value.replace('_', ' ')}")
    parts.append(f"<div class='meta'>{' &nbsp;|&nbsp; '.join(meta_bits)}</div>")

    # Materials
    parts.append("<h2>Materials</h2><table>")
    m = pattern
    if m.yarn is not None:
        parts.append(f"<tr><td>Yarn</td><td>{_esc(m.yarn)}</td></tr>")
    if m.hook is not None:
        parts.append(f"<tr><td>Hook</td><td>{_esc(m.hook)}</td></tr>")
    if m.gauge is not None:
        parts.append(f"<tr><td>Gauge</td><td>{_esc(m.gauge)}</td></tr>")
    if m.yarn is None and m.hook is None:
        parts.append("<tr><td>Yarn &amp; hook</td><td>As stated by the designer (see pattern notes).</td></tr>")
    parts.append("</table>")

    # Abbreviations
    used = set()
    for r in rows:
        for i in r.instructions:
            for op in i.operations:
                used.add(op.stitch_type.value)
    parts.append("<h2>Abbreviations</h2><table>")
    for key in ["magic_ring", "chain", "single_crochet", "half_double_crochet",
                "double_crochet", "treble", "increase", "decrease", "slip_stitch"]:
        if key in used:
            parts.append(f"<tr><td>{STITCH_NAMES[key].split(' (')[0]}</td><td>{STITCH_NAMES[key].split(' (')[1].rstrip(')')}</td></tr>")
    parts.append("<tr><td>inc / dec</td><td>increase / decrease</td></tr>")
    parts.append("<tr><td>( ) x N</td><td>work the group in parentheses N times</td></tr>")
    parts.append("<tr><td>(N) at end of line</td><td>stitch count after that " + unit.lower() + "</td></tr>")
    parts.append("</table>")

    # Instructions
    parts.append(f"<h2>Instructions</h2>")
    for g in _grouped_rounds(pattern):
        if is_round:
            label = _round_label(g["first"], g["last"])
        else:
            label = f"Row {g['first']}" if g["first"] == g["last"] else f"Rows {g['first']}-{g['last']}"
        c = f" ({g['count']} sts)" if g["count"] else ""
        parts.append(f"<div class='round'><span class='rn'>{_esc(label)}:</span> {_esc(g['text'])}"
                     f"<span class='count'>{c}</span></div>")

    # Measurements
    try:
        from ..visualization import measure_pattern
        meas = measure_pattern(pattern)
        parts.append("<h2>Finished Measurements</h2><table>")
        parts.append(f"<tr><td>Total {unit.lower()}s</td><td>{meas.total_rounds}</td></tr>")
        if meas.max_stitch_count:
            parts.append(f"<tr><td>Widest stitch count</td><td>{meas.max_stitch_count} sts</td></tr>")
        if meas.max_circumference_mm:
            parts.append(f"<tr><td>Approx. circumference</td><td>{meas.max_circumference_mm / 25.4:.1f} in "
                         f"({meas.max_circumference_mm / 10:.0f} cm)</td></tr>")
        parts.append(f"<tr><td>Approx. height (worked fabric)</td><td>{meas.total_height_mm / 25.4:.1f} in "
                     f"({meas.total_height_mm / 10:.0f} cm)</td></tr>")
        parts.append("<tr><td colspan='2' style='color:#6b7280'>Estimates based on a 6 mm single crochet "
                     "stitch; actual size varies with tension.</td></tr>")
        parts.append("</table>")
    except Exception:
        pass

    # Validation report
    if validation_report is not None and config.include_validation:
        parts.append("<h2>Validation Report</h2>")
        status = validation_report.overall_status
        cls = "ok" if status in ("PASS", "PASS_WITH_WARNINGS") else "bad"
        parts.append(f"<p><span class='{cls}'>Status: {_esc(status)}</span> &mdash; score "
                     f"{validation_report.score}/100 &middot; {len(validation_report.errors)} error(s), "
                     f"{len(validation_report.warnings)} warning(s)</p>")
        findings = [f for f in validation_report.all_findings
                    if f.severity.value in ("ERROR", "CRITICAL", "WARNING")]
        if findings:
            parts.append("<table><tr><th>Location</th><th>Message</th></tr>")
            for f in findings[:20]:
                parts.append(f"<tr><td>{_esc(f.location)}</td><td>{_esc(f.message)}</td></tr>")
            parts.append("</table>")
        else:
            parts.append("<p>No errors found.</p>")

    parts.append(f"<div class='footer'>Generated by Crochet Pattern Checker"
                 + (f" &middot; {_esc(designer)}" if designer else "") + "</div>")
    parts.append("</body></html>")
    return "\n".join(parts)


class PDFGenerator:
    def __init__(self, config: Optional[PDFConfig] = None):
        self.config = config or PDFConfig()

    def generate(self, pattern, report=None) -> str:
        return generate_pdf_html(pattern, validation_report=report, config=self.config)

    def save(self, output_path: str, pattern, report=None) -> str:
        html_text = self.generate(pattern, report)
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html_text, encoding="utf-8")
        return str(out)


def generate_pdf(pattern, output_path: str, format: str = "modern") -> str:
    """Generate a pattern document.

    Writes real PDF via WeasyPrint when available; otherwise writes print-ready
    HTML that can be opened in a browser and printed to PDF.
    """
    html_text = generate_pdf_html(pattern)
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    try:
        from weasyprint import HTML  # type: ignore
        HTML(string=html_text).write_pdf(str(out))
        return str(out)
    except Exception:
        txt_path = out.with_suffix(".html")
        txt_path.write_text(html_text, encoding="utf-8")
        return str(txt_path)
