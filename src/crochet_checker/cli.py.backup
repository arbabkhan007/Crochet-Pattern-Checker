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


@cli.command("render-3d")
@click.argument("pattern_file", type=click.Path(exists=True))
@click.option("--output", "-o", default="output")
def render_3d(pattern_file, output):
    """Generate 3D mesh from pattern."""
    from .simulation import simulate_surface, analyze_pattern_shape
    text = Path(pattern_file).read_text()
    pattern = CrochetParser().parse(text)
    analysis = analyze_pattern_shape(pattern)
    mesh = simulate_surface(pattern)
    stem = Path(pattern_file).stem
    out_dir = Path(output) / stem
    out_dir.mkdir(parents=True, exist_ok=True)
    console.print(f"Shape: [cyan]{analysis.detected_shape.value}[/cyan] ({analysis.confidence:.0%})")
    console.print(f"  {analysis.explanation}")
    console.print(f"Mesh: {mesh.vertex_count} verts, {mesh.face_count} faces")
    filepath = out_dir / f"{stem}.obj"
    mesh.save_obj(str(filepath))
    console.print(f"  Saved: [green]{filepath}[/green]")


@cli.command("pdf")
@click.argument("pattern_file", type=click.Path(exists=True))
@click.option("--output", "-o", default=None, help="Output file path")
@click.option("--designer", default="", help="Designer name")
def pdf_cmd(pattern_file, output, designer):
    """Generate professional PDF/HTML from pattern."""
    from .pdf import PDFConfig, PDFGenerator
    text = Path(pattern_file).read_text()
    pattern = CrochetParser().parse(text)
    report = validate_pattern(pattern)
    config = PDFConfig(designer_name=designer)
    gen = PDFGenerator(config)
    if output is None:
        output = str(Path("output") / Path(pattern_file).stem / (Path(pattern_file).stem + ".html"))
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    gen.save(output, pattern, report)
    console.print(f"[green]PDF/HTML saved to: {output}[/green]")
    console.print(f"  Open in browser and Ctrl+P to save as PDF")


@cli.command("explain")
@click.argument("pattern_file", type=click.Path(exists=True))
@click.option("--ai", "ai_provider", default="rule_based", type=click.Choice(["rule_based","openai","anthropic","gemini","ollama"]))
def explain_cmd(pattern_file, ai_provider):
    """AI explanation of pattern with suggestions."""
    from .ai import PatternExplainer, SuggestionEngine, DescriptionGenerator
    text = Path(pattern_file).read_text()
    pattern = CrochetParser().parse(text)
    report = validate_pattern(pattern)
    result = PatternExplainer().explain(pattern, report)
    suggestions = SuggestionEngine().generate_suggestions(pattern, report)
    description = DescriptionGenerator().generate(pattern, report)
    console.print(f"\n[bold blue]Pattern Explanation[/bold blue]")
    console.print(f"[dim]{result.summary}[/dim]\n")
    console.print(result.explanation)
    console.print(f"\n[bold]Shape:[/bold] {result.shape_guess}")
    console.print(f"[bold]Difficulty:[/bold] {result.difficulty_explanation}")
    console.print(f"\n[bold cyan]Highlights[/bold cyan]")
    for h in result.highlights: console.print(f"  * {h}")
    console.print(f"\n[bold green]Recommendations[/bold green]")
    for r in result.recommendations: console.print(f"  + {r}")
    if suggestions:
        console.print(f"\n[bold yellow]Fix Suggestions[/bold yellow]")
        for s in suggestions: console.print(f"  [{s.confidence}] {s.error_location}: {s.suggestion}")
    console.print(f"\n[bold magenta]Pattern Description[/bold magenta]")
    console.print(f"  Title: {description.title}")
    console.print(f"  {description.short_description}")
    console.print(f"  Skill: {description.skill_level}")
    console.print(f"  Size: {description.finished_size}")
    console.print(f"  Tags: {', '.join(description.tags)}")


@cli.command("image")
@click.argument("pattern_file", type=click.Path(exists=True))
@click.option("--output", "-o", default=None, help="Output file path")
@click.option("--provider", default="placeholder", type=click.Choice(["placeholder", "dalle", "gemini", "stable_diffusion"]))
@click.option("--style", default="watercolor", type=click.Choice(["watercolor", "realistic", "cartoon", "minimalist"]))
def image_cmd(pattern_file, output, provider, style):
    """Generate cover image for pattern."""
    from .image import ImageProvider, ImageConfig
    text = Path(pattern_file).read_text()
    pattern = CrochetParser().parse(text)
    title = getattr(pattern.metadata, "title", None) or Path(pattern_file).stem
    category = getattr(pattern.metadata, "category", "") or ""
    config = ImageConfig(provider=provider, style=style)
    img = ImageProvider(config).generate_cover_image(title, category)
    if output is None:
        output = str(Path("output") / Path(pattern_file).stem / (Path(pattern_file).stem + "_cover.svg"))
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    if img.startswith("<svg"):
        Path(output).write_text(img)
        console.print(f"[green]SVG cover saved to: {output}[/green]")
    else:
        import base64
        out = output.replace(".svg", ".png")
        Path(out).write_bytes(base64.b64decode(img))
        console.print(f"[green]Cover saved to: {out}[/green]")
    console.print(f"  Provider: {provider} | Style: {style}")


@cli.command("config")
@click.option("--set-key", nargs=2, metavar="PROVIDER KEY")
@click.option("--show", is_flag=True)
def config_cmd(set_key, show):
    """Configure AI and image providers."""
    import json
    cf = Path.home() / ".crochet_checker_config.json"
    if show:
        if cf.exists():
            config = json.loads(cf.read_text())
            console.print("\n[bold]Configuration:[/bold]")
            for k, v in config.items(): console.print(f"  {k}: {v[:8]}...{v[-4:]}")
        else:
            console.print("\n[yellow]No config found.[/yellow]")
        console.print("\n[bold]Providers:[/bold] openai, anthropic, gemini, ollama, dalle, stable_diffusion")
        return
    if set_key:
        p, k = set_key
        config = json.loads(cf.read_text()) if cf.exists() else {}
        config[f"{p}_api_key"] = k
        cf.write_text(json.dumps(config, indent=2))
        console.print(f"[green]Key for {p} saved.[/green]")


@cli.command("image")
@click.argument("pattern_file", type=click.Path(exists=True))
@click.option("--output", "-o", default=None)
@click.option("--provider", default="placeholder", type=click.Choice(["placeholder","dalle","gemini","stable_diffusion"]))
@click.option("--style", default="watercolor", type=click.Choice(["watercolor","realistic","cartoon","minimalist"]))
def image_cmd(pattern_file, output, provider, style):
    """Generate cover image for pattern."""
    from .image import ImageProvider, ImageConfig
    text = Path(pattern_file).read_text()
    pattern = CrochetParser().parse(text)
    title = getattr(pattern.metadata, "title", None) or Path(pattern_file).stem
    category = getattr(pattern.metadata, "category", "") or ""
    img = ImageProvider(ImageConfig(provider=provider, style=style)).generate_cover_image(title, category)
    if output is None:
        output = str(Path("output") / Path(pattern_file).stem / (Path(pattern_file).stem + "_cover.svg"))
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    if img.startswith("<svg"):
        Path(output).write_text(img)
        console.print(f"[green]SVG cover saved to: {output}[/green]")
    else:
        import base64
        out = output.replace(".svg", ".png")
        Path(out).write_bytes(base64.b64decode(img))
        console.print(f"[green]Cover saved to: {out}[/green]")
    console.print(f"  Provider: {provider} | Style: {style}")

@cli.command("config")
@click.option("--set-key", nargs=2, metavar="PROVIDER KEY")
@click.option("--show", is_flag=True)
def config_cmd(set_key, show):
    """Configure AI and image providers."""
    import json
    cf = Path.home() / ".crochet_checker_config.json"
    if show:
        if cf.exists():
            config = json.loads(cf.read_text())
            console.print("\n[bold]Configuration:[/bold]")
            for k, v in config.items(): console.print(f"  {k}: {v[:8]}...{v[-4:]}")
        else:
            console.print("\n[yellow]No config found.[/yellow]")
        console.print("\n[bold]Providers:[/bold] openai, anthropic, gemini, ollama, dalle, stable_diffusion")
        return
    if set_key:
        p, k = set_key
        config = json.loads(cf.read_text()) if cf.exists() else {}
        config[f"{p}_api_key"] = k
        cf.write_text(json.dumps(config, indent=2))
        console.print(f"[green]Key for {p} saved.[/green]")



@cli.command("yarn-calc")
@click.argument("pattern_file", type=click.Path(exists=True))
@click.option("--weight", default="worsted", type=click.Choice(["lace","fingering","sport","dk","worsted","aran","bulky","super_bulky","jumbo"]))
@click.option("--grams", default=100)
@click.option("--yards", default=200)
def yarn_calc(pattern_file, weight, grams, yards):
    """Estimate yarn requirements."""
    from .utils import estimate_yarn
    text = Path(pattern_file).read_text()
    pattern = CrochetParser().parse(text)
    est = estimate_yarn(pattern, yarn_weight=weight, grams_per_skein=grams, yards_per_skein=yards)
    console.print(f"\n[bold]Yarn Estimate for {pattern.metadata.title or Path(pattern_file).stem}[/bold]")
    console.print(f"\u2501" * 30)
    console.print(f"Total yarn: [cyan]{est.total_yards:.1f} yards[/cyan] ({est.total_meters:.2f} meters)")
    if est.total_grams: console.print(f"Weight: [cyan]{est.total_grams:.1f} grams[/cyan]")
    console.print(f"Skeins needed: [bold green]{est.skeins_needed:.2f}[/bold green] (with 15% margin)")
    console.print(f"Confidence: [yellow]{est.confidence}[/yellow]")
    if est.notes:
        console.print("\n[bold]Notes:[/bold]")
        for n in est.notes: console.print(f"  \u2022 {n}")


@cli.command("progress")
@click.argument("pattern_file", type=click.Path(exists=True))
@click.option("--complete", "-c", type=int)
@click.option("--uncomplete", "-u", type=int)
@click.option("--note", "-n")
@click.option("--save", "-s")
def progress(pattern_file, complete, uncomplete, note, save):
    """Track crochet progress."""
    from .utils import track_progress
    text = Path(pattern_file).read_text()
    pattern = CrochetParser().parse(text)
    tracker = track_progress(pattern)
    
    if complete and tracker.complete_round(complete): console.print(f"[green]\u2713 Round {complete} complete[/green]")
    if uncomplete and tracker.uncomplete_round(uncomplete): console.print(f"[yellow]\u25cb Round {uncomplete} incomplete[/yellow]")
    if note: tracker.add_note(note); console.print("[blue]\U0001f4dd Note added[/blue]")
    if save: tracker.save(save); console.print(f"[green]\U0001f4be Saved to {save}[/green]")
    
    console.print("\n" + tracker.get_summary())
\n\ndef main(): cli()
if __name__ == "__main__": main()
