"""HTML and PDF generation for parsed crochet patterns."""

from __future__ import annotations

from dataclasses import dataclass
from html import escape
from pathlib import Path
from typing import TYPE_CHECKING

from ..model.pattern import Pattern
from ..visualization.measurements import measure_pattern

if TYPE_CHECKING:
    from ..validation import ValidationReport


@dataclass(slots=True)
class PDFConfig:
    """Presentation settings shared by HTML and PDF output."""

    designer_name: str = ""
    page_size: str = "A4"
    accent_color: str = "#7c3f58"


class PDFGenerator:
    """Render a parsed pattern as standalone HTML or a real PDF file."""

    def __init__(self, config: PDFConfig | None = None) -> None:
        self.config = config or PDFConfig()

    @staticmethod
    def _display_count(item, previous_count: int) -> int:
        for instruction in item.instructions:
            if instruction.stated_stitch_count is not None:
                return instruction.stated_stitch_count
        if previous_count:
            return item.compute_stitch_count_with_context(previous_count)
        return item.computed_stitch_count

    def generate_html(
        self,
        pattern: Pattern,
        validation_report: ValidationReport | None = None,
    ) -> str:
        """Build a complete, escaped HTML document for ``pattern``."""

        title = pattern.metadata.title or "Crochet Pattern"
        designer = self.config.designer_name or pattern.metadata.designer or ""
        items = pattern.rounds or pattern.rows
        item_label = "Round" if pattern.rounds else "Row"
        measurements = measure_pattern(pattern)

        rows: list[str] = []
        previous_count = 0
        for item in items:
            number = item.round_number if pattern.rounds else item.row_number
            count = self._display_count(item, previous_count)
            instructions = " ".join(
                instruction.source_text for instruction in item.instructions
            )
            rows.append(
                "<tr>"
                f"<th scope=\"row\">{escape(item_label)} {number}</th>"
                f"<td>{escape(instructions)}</td>"
                f"<td>({count} sts)</td>"
                "</tr>"
            )
            previous_count = count

        yarn = escape(pattern.yarn.name) if pattern.yarn and pattern.yarn.name else "Yarn appropriate for the project"
        hook = (
            f"{pattern.hook.size_mm:g} mm crochet hook"
            if pattern.hook and pattern.hook.size_mm
            else "Crochet hook appropriate for the yarn"
        )
        designer_html = (
            f"<p class=\"designer\">Designed by {escape(designer)}</p>"
            if designer
            else ""
        )
        validation_html = ""
        if validation_report is not None:
            validation_html = (
                "<section><h2>Validation Report</h2>"
                f"<p>Status: <strong>{escape(validation_report.overall_status)}</strong>; "
                f"score: {validation_report.score}/100; "
                f"errors: {len(validation_report.errors)}; "
                f"warnings: {len(validation_report.warnings)}.</p></section>"
            )

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<style>
@page {{ size: {escape(self.config.page_size)}; margin: 18mm; }}
:root {{ color: #222; font: 11pt/1.45 Arial, sans-serif; }}
body {{ margin: 0 auto; max-width: 900px; }}
h1, h2 {{ color: {escape(self.config.accent_color)}; }}
h1 {{ border-bottom: 3px solid {escape(self.config.accent_color)}; padding-bottom: .25em; }}
table {{ border-collapse: collapse; width: 100%; }}
th, td {{ border: 1px solid #bbb; padding: .45em; text-align: left; vertical-align: top; }}
thead th {{ background: #f3edf0; }}
tbody th, td:last-child {{ white-space: nowrap; }}
.designer {{ font-style: italic; }}
</style>
</head>
<body>
<header><h1>{escape(title)}</h1>{designer_html}</header>
<section>
<h2>Materials</h2>
<ul><li>{yarn}</li><li>{escape(hook)}</li><li>Yarn needle</li><li>Scissors</li><li>Stitch markers</li></ul>
</section>
<section>
<h2>Finished Measurements</h2>
<p>Approximately {measurements.max_diameter_inches:.1f} inches across and {measurements.total_height_inches:.1f} inches tall at the parser's default stitch dimensions.</p>
</section>
<section>
<h2>Abbreviations</h2>
<dl><dt>ch</dt><dd>Chain</dd><dt>sc</dt><dd>Single Crochet</dd><dt>hdc</dt><dd>Half Double Crochet</dd><dt>dc</dt><dd>Double Crochet</dd><dt>inc</dt><dd>Increase</dd><dt>dec</dt><dd>Decrease</dd></dl>
</section>
<section>
<h2>Pattern Instructions</h2>
<table><thead><tr><th>{escape(item_label)}</th><th>Instructions</th><th>Stitch count</th></tr></thead><tbody>{''.join(rows)}</tbody></table>
</section>
{validation_html}
</body>
</html>
"""

    def generate(
        self,
        pattern: Pattern,
        validation_report: ValidationReport | None = None,
    ) -> str:
        """Backward-compatible alias for :meth:`generate_html`."""

        return self.generate_html(pattern, validation_report)

    def save(
        self,
        output_path: str | Path,
        pattern: Pattern,
        validation_report: ValidationReport | None = None,
    ) -> str:
        """Write HTML, or use WeasyPrint when ``output_path`` ends in ``.pdf``."""

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        html = self.generate_html(pattern, validation_report)
        if output.suffix.lower() == ".pdf":
            try:
                from weasyprint import HTML
            except (ImportError, OSError) as exc:  # pragma: no cover - environment-specific
                raise RuntimeError(
                    "PDF output requires WeasyPrint and its native rendering libraries"
                ) from exc
            HTML(string=html, base_url=str(output.parent.resolve())).write_pdf(output)
        else:
            output.write_text(html, encoding="utf-8")
        return str(output)


def generate_pdf_html(
    pattern: Pattern,
    validation_report: ValidationReport | None = None,
    config: PDFConfig | None = None,
) -> str:
    """Convenience wrapper returning standalone pattern HTML."""

    return PDFGenerator(config).generate_html(pattern, validation_report)


def generate_pdf(
    pattern: Pattern,
    output_path: str | Path,
    format: str = "modern",
) -> str:
    """Compatibility wrapper that writes HTML or PDF based on the file suffix."""

    del format  # Retained for backward compatibility with the original public API.
    return PDFGenerator().save(output_path, pattern)
