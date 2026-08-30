"""Command-line interface for the Crochet Pattern Checker."""
import json, sys
from pathlib import Path
import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from .parser import CrochetParser
from .validation import Severity, validate_pattern
console = Console()

@click.group()
@click.version_option(version="0.2.0", prog_name="crochet-pattern-checker")
def cli():
    """Crochet Pattern Checker - Verify, Visualize, and Publish crochet patterns."""

@cli.command("check")
@click.argument("pattern_file", type=click.Path(exists=True))
@click.option("--strict", is_flag=True)
@click.option("--json", "output_json", is_flag=True)
@click.option("--verbose", "-v", is_flag=True)
def check(pattern_file, strict, output_json, verbose):
    """Check a crochet pattern."""
    text = Path(pattern_file).read_text()
    if not output_json:
        console.print(f"\n[bold]Crochet Pattern Checker[/bold] v0.2.0")
        console.print(f"Checking: [cyan]{Path(pattern_file).name}[/cyan]\n")
    pattern = CrochetParser().parse(text)
    if not output_json:
        console.print(f"[bold]Construction:[/bold] {pattern.construction.value}")
        items = pattern.rounds or pattern.rows
        console.print(f"[bold]Total:[/bold] {len(items)}")
        prev = 0
        for i, r in enumerate(items):
            num = r.round_number if hasattr(r,"round_number") else r.row_number
            sc = r.computed_stitch_count if i==0 else r.compute_stitch_count_with_context(prev)
            dc = sc
            for inst in r.instructions:
                if inst.stated_stitch_count is not None: dc = inst.stated_stitch_count; break
            console.print(f"  {chr(8220)+'Round' if hasattr(r,'round_number') else 'Row'} {num}: {dc} stitches")
            prev = dc
        console.print()
    report = validate_pattern(pattern, strict=strict)
    if output_json:
        click.echo(json.dumps(report.to_dict(), indent=2, default=str)); return
    _display(report, verbose)
    if report.errors: sys.exit(1)

@cli.command("render")
@click.argument("pattern_file", type=click.Path(exists=True))
@click.option("--output", "-o", default="output")
def render(pattern_file, output):
    """Generate visual diagrams and charts."""
    from .visualization import generate_circle_diagram, generate_stitch_count_chart, generate_crochet_chart, render_2d_preview, measure_pattern
    text = Path(pattern_file).read_text()
    pattern = CrochetParser().parse(text)
    report = validate_pattern(pattern)
    stem = Path(pattern_file).stem
    out_dir = Path(output) / stem
    out_dir.mkdir(parents=True, exist_ok=True)
    console.print(f"Generating visuals for [cyan]{Path(pattern_file).name}[/cyan]")
    (out_dir/"diagram.svg").write_text(generate_circle_diagram(pattern)); console.print("  OK diagram.svg")
    (out_dir/"stitch_counts.svg").write_text(generate_stitch_count_chart(pattern)); console.print("  OK stitch_counts.svg")
    (out_dir/"crochet_chart.svg").write_text(generate_crochet_chart(pattern)); console.print("  OK crochet_chart.svg")
    (out_dir/"preview.svg").write_text(render_2d_preview(pattern, report)); console.print("  OK preview.svg")
    m = measure_pattern(pattern)
    console.print(f"\n[bold]Measurements:[/bold]")
    console.print(f"  Max radius: {m.max_radius_mm:.1f} mm ({m.max_radius_inches:.2f} in)")
    console.print(f"  Max diameter: {m.max_radius_mm*2:.1f} mm ({m.max_diameter_inches:.2f} in)")
    console.print(f"  Total height: {m.total_height_mm:.1f} mm ({m.total_height_inches:.2f} in)")
    console.print(f"  Max stitches: {m.max_stitch_count}")
    console.print(f"\n[green]Done! Files saved to {out_dir}[/green]")

@cli.command("measure")
@click.argument("pattern_file", type=click.Path(exists=True))
def measure(pattern_file):
    """Show pattern measurements."""
    from .visualization import measure_pattern
    text = Path(pattern_file).read_text()
    pattern = CrochetParser().parse(text)
    m = measure_pattern(pattern)
    console.print(f"\n[bold]Pattern Measurements[/bold]")
    console.print(f"  Total rounds: {m.total_rounds}")
    console.print(f"  Max stitch count: {m.max_stitch_count}")
    console.print(f"  Max radius: {m.max_radius_mm:.1f} mm ({m.max_radius_inches:.2f} in)")
    console.print(f"  Max circumference: {m.max_circumference_mm:.1f} mm ({m.max_circumference_inches:.2f} in)")
    console.print(f"  Total height: {m.total_height_mm:.1f} mm ({m.total_height_inches:.2f} in)")

def _display(report, verbose=False):
    status = report.overall_status
    colors = {"PASS":"green","PASS_WITH_WARNINGS":"yellow","NEEDS_REVIEW":"orange3","ERROR":"red"}
    c = colors.get(status,"white")
    t = Text(); t.append("Status: ", style="bold"); t.append(status, style=f"bold {c}")
    t.append(f"  |  Score: {report.score}/100", style="bold")
    console.print(Panel(t, title="Validation Report", border_style=c))
    table = Table(title="Summary"); table.add_column("Check", style="cyan"); table.add_column("Status"); table.add_column("Findings")
    if report.stitch_counts:
        e = len(report.stitch_counts.errors); w = len([f for f in report.stitch_counts.findings if f.severity==Severity.WARNING])
        table.add_row("Stitch Counts", Text("OK" if e==0 else "X", style="green" if e==0 else "red"), f"{e} errors, {w} warnings")
    if report.row_transitions:
        e = len([f for f in report.row_transitions.findings if f.severity in (Severity.ERROR, Severity.CRITICAL)])
        table.add_row("Transitions", Text("OK" if e==0 else "warn", style="green" if e==0 else "yellow"), f"{e} errors")
    console.print(table)
    if report.errors:
        console.print("\n[bold red]ERRORS:[/bold red]")
        for f in report.errors: console.print(f"  [red]X[/red] [{f.location}] {f.message}")
    if report.warnings:
        console.print("\n[bold yellow]WARNINGS:[/bold yellow]")
        for f in report.warnings: console.print(f"  [yellow]![/yellow] [{f.location}] {f.message}")

def main(): cli()
if __name__ == "__main__": main()
