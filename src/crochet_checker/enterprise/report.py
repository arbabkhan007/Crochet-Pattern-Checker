"""Commercial certification report generation."""

from __future__ import annotations

import html
from pathlib import Path


class CertificationReportWriter:
    """Generate standalone HTML certification reports."""

    def render(self, certification, title: str = "Crochet Pattern Certificate") -> str:
        level = certification.level.value
        level_class = level.lower().replace("_", "-")

        risks = "".join(
            f"""
            <li class="risk-{html.escape(item.severity)}">
                <strong>{html.escape(item.category)}</strong>:
                {html.escape(item.message)}
                <br>
                <small>{html.escape(item.recommendation)}</small>
            </li>
            """
            for item in certification.risks
        )

        evidence = "".join(
            f"<li>{html.escape(item)}</li>"
            for item in certification.evidence
        )

        assumptions = "".join(
            f"<li>{html.escape(item)}</li>"
            for item in certification.assumptions
        )

        return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{html.escape(title)}</title>
<style>
body {{
    font-family: Arial, sans-serif;
    margin: 0;
    background: #f3f4f6;
    color: #202124;
}}
main {{
    max-width: 900px;
    margin: 40px auto;
    background: white;
    padding: 42px;
    box-shadow: 0 4px 20px #0002;
}}
h1 {{
    margin-top: 0;
    color: #243b53;
}}
.badge {{
    display: inline-block;
    padding: 10px 18px;
    border-radius: 8px;
    font-weight: bold;
    background: #e8f5e9;
    color: #1b5e20;
}}
.badge.rejected, .badge.sample-required {{
    background: #ffebee;
    color: #b71c1c;
}}
.badge.conditionally-certified {{
    background: #fff8e1;
    color: #8d6e00;
}}
.grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
    margin: 24px 0;
}}
.card {{
    background: #f7fafc;
    padding: 16px;
    border-radius: 8px;
}}
.card strong {{
    display: block;
    font-size: 24px;
    margin-top: 6px;
}}
section {{
    margin-top: 30px;
}}
li {{
    margin: 8px 0;
}}
.risk-critical {{
    color: #b71c1c;
}}
.risk-high {{
    color: #c62828;
}}
.risk-medium {{
    color: #8d6e00;
}}
code {{
    word-break: break-all;
}}
footer {{
    margin-top: 42px;
    border-top: 1px solid #ddd;
    padding-top: 16px;
    color: #667085;
    font-size: 12px;
}}
</style>
</head>
<body>
<main>
<h1>{html.escape(title)}</h1>

<p>
    <span class="badge {level_class}">
        {html.escape(level)}
    </span>
</p>

<div class="grid">
    <div class="card">
        Compiler valid
        <strong>{html.escape(str(certification.compiler_valid))}</strong>
    </div>
    <div class="card">
        Confidence
        <strong>{certification.confidence:.1%}</strong>
    </div>
    <div class="card">
        Physical sample
        <strong>{"REQUIRED" if certification.sample_required else "NOT REQUIRED"}</strong>
    </div>
</div>

<section>
<h2>Pattern identity</h2>
<p>Pattern hash:</p>
<code>{html.escape(certification.pattern_hash)}</code>
<p>Engine version: {html.escape(certification.engine_version)}</p>
<p>Created: {html.escape(certification.created_at)}</p>
</section>

<section>
<h2>Evidence</h2>
<ul>{evidence or "<li>No evidence recorded.</li>"}</ul>
</section>

<section>
<h2>Assumptions</h2>
<ul>{assumptions or "<li>No unresolved assumptions.</li>"}</ul>
</section>

<section>
<h2>Risk assessment</h2>
<ul>{risks or "<li>No risks detected.</li>"}</ul>
</section>

<section>
<h2>Recommendation</h2>
<p>
    {"Production approval is permitted under the configured policy."
    if certification.approved_for_production
    else
    "Do not approve for production until the listed risks are resolved."}
</p>
</section>

<footer>
This report is generated from deterministic validation and configured
material assumptions. AI output cannot override compiler results.
</footer>
</main>
</body>
</html>
"""

    def write(
        self,
        certification,
        output_path: str,
        title: str = "Crochet Pattern Certificate",
    ) -> str:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            self.render(certification, title),
            encoding="utf-8",
        )
        return str(path)
