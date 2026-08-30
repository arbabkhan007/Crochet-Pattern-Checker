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
@click.version_option(version="0.1.0", prog_name="crochet-pattern-checker")
def cli():
    """Crochet Pattern Checker"""

@cli.command("check")
@click.argument("pattern_file", type=click.Path(exists=True))
@click.option("--strict", is_flag=True)
@click.option("--json", "output_json", is_flag=True)
@click.option("--verbose", "-v", is_flag=True)
def check(pattern_file, strict, output_json, verbose):
    """Check a crochet pattern."""
    text = Path(pattern_file).read_text()
    if not output_json:
        console.print(f"\n[bold]Crochet Pattern Checker[/bold] v0.1.0")
        console.print(f"Checking: [cyan]{Path(pattern_file).name}[/cyan]\n")
    parser = CrochetParser(); pattern = parser.parse(text)
    if not output_json:
        console.print(f"[bold]Construction:[/bold] {pattern.construction.value}")
        items = pattern.rounds or pattern.rows
        console.print(f"[bold]Total:[/bold] {len(items)}")
        prev = 0
        for i, r in enumerate(items):
            num = r.round_number if hasattr(r,'round_number') else r.row_number
            sc = r.computed_stitch_count if i==0 else r.compute_stitch_count_with_context(prev)
            dc = sc
            for inst in r.instructions:
                if inst.stated_stitch_count is not None: dc = inst.stated_stitch_count; break
            console.print(f"  {'Round' if hasattr(r,'round_number') else 'Row'} {num}: {dc} stitches")
            prev = dc
        console.print()
    report = validate_pattern(pattern, strict=strict)
    if output_json:
        click.echo(json.dumps(report.to_dict(), indent=2, default=str)); return
    status = report.overall_status
    colors = {"PASS":"green","PASS_WITH_WARNINGS":"yellow","NEEDS_REVIEW":"orange3","ERROR":"red"}
    c = colors.get(status, "white")
    t = Text(); t.append("Status: ", style="bold"); t.append(status, style=f"bold {c}")
    t.append(f"  |  Score: {report.score}/100", style="bold")
    console.print(Panel(t, title="Validation Report", border_style=c))
    table = Table(title="Summary"); table.add_column("Check", style="cyan"); table.add_column("Status"); table.add_column("Findings")
    if report.stitch_counts:
        e = len(report.stitch_counts.errors); w = len([f for f in report.stitch_counts.findings if f.severity==Severity.WARNING])
        table.add_row("Stitch Counts", Text("✓" if e==0 else "✗", style="green" if e==0 else "red"), f"{e} errors, {w} warnings")
    if report.row_transitions:
        e = len([f for f in report.row_transitions.findings if f.severity in (Severity.ERROR, Severity.CRITICAL)])
        w = len([f for f in report.row_transitions.findings if f.severity==Severity.WARNING])
        table.add_row("Transitions", Text("✓" if e==0 else "⚠", style="green" if e==0 else "yellow"), f"{e} errors, {w} warnings")
    console.print(table)
    if report.errors:
        console.print("\n[bold red]ERRORS:[/bold red]")
        for f in report.errors: console.print(f"  [red]✗[/red] [{f.location}] {f.message}")
    if report.warnings:
        console.print("\n[bold yellow]WARNINGS:[/bold yellow]")
        for f in report.warnings: console.print(f"  [yellow]⚠[/yellow] [{f.location}] {f.message}")
    if report.errors: sys.exit(1)

def main(): cli()
if __name__ == "__main__": main()
