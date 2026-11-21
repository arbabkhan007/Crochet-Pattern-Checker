"""FastAPI web application for crochet pattern checker."""

from __future__ import annotations

from pathlib import Path

from fastapi import BackgroundTasks, FastAPI, File, HTTPException, Query, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from .. import __version__
from ..calculators import (
    convert_terminology,
    estimate_yarn,
    gauge_to_size,
    recommend_hook,
    shape_from_counts,
    stitch_count_chart,
)
from ..parser.parser import CrochetParser
from ..pdf import TEMPLATES, PDFConfig, PDFGenerator
from ..report import build_report
from ..simulation import analyze_pattern_shape, simulate_surface
from ..simulation.assembly_map import assembly_map_svg, written_assembly
from ..simulation.geometry_map import geometry_map_svg, written_geometry
from ..simulation.stitch_sim import stitch_model_obj
from ..simulation.stitch_sim import simulate_stitches, stitch_map_svg
from .import_url import ImportError_, import_pattern_page
from ..validation import validate_pattern
from ..visualization import measure_pattern, render_2d_preview

app = FastAPI(
    title="Crochet Pattern Checker",
    version=__version__,
    description=(
        "Deterministic crochet pattern checker: stitch counts, gauge, "
        "yarn, hooks, US/UK conversion, diagrams, and printable sheets. "
        "Written counts only â€” never a measurement."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Optional web companion ("studio"). Built from web/studio with `npm run build`.
# Mounted only when the bundle exists, so the API works with or without it.
# The Python engine in this module stays authoritative: the studio calls
# /api/check rather than reimplementing validation, and its own scoring is
# labelled in the UI as a browser-side pre-check.
_STUDIO_DIR = Path(__file__).resolve().parents[3] / "web" / "studio" / "dist"
if _STUDIO_DIR.is_dir():
    app.mount("/studio", StaticFiles(directory=str(_STUDIO_DIR), html=True), name="studio")


class CheckRequest(BaseModel):
    pattern_text: str = Field(min_length=1, max_length=200_000)


class GaugeRequest(BaseModel):
    stitches: int = Field(gt=0, le=100_000)
    rows: int = Field(gt=0, le=100_000)
    sts_per_4in: float = Field(gt=0, le=200)
    rows_per_4in: float = Field(gt=0, le=200)


class ConvertRequest(BaseModel):
    pattern_text: str = Field(min_length=1, max_length=200_000)
    direction: str = "us-to-uk"


class YarnRequest(BaseModel):
    total_stitches: int = Field(ge=0, le=10_000_000)
    stitch: str = "sc"


class ChartRequest(BaseModel):
    counts: list[int] = Field(min_length=1, max_length=1_000)


class ConsensusRunRequest(BaseModel):
    pattern_text: str = Field(min_length=1, max_length=100_000)


class DraftChangeRequest(BaseModel):
    from_text: str = Field(min_length=1, max_length=5_000)
    to_text: str = Field(max_length=5_000)
    reason: str = Field(min_length=1, max_length=2_000)


class ConsensusDraftRequest(BaseModel):
    changes: list[DraftChangeRequest] = Field(min_length=1, max_length=20)


@app.get("/", response_class=HTMLResponse)
async def index():
    return get_frontend_html()


@app.post("/api/check")
async def check_pattern(request: CheckRequest):
    try:
        pattern = CrochetParser().parse(request.pattern_text)
        report = validate_pattern(pattern)
        m = measure_pattern(pattern)
        return {
            "status": report.overall_status,
            "score": report.score,
            "errors": [
                {"message": e.message, "location": e.location} for e in report.errors
            ],
            "warnings": [
                {"message": w.message, "location": w.location} for w in report.warnings
            ],
            "rounds": m.total_rounds,
            "max_stitches": m.max_stitch_count,
            "max_diameter_inches": round(m.max_diameter_inches, 2),
            "total_height_inches": round(m.total_height_inches, 2),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


class ImportUrlRequest(BaseModel):
    url: str


@app.post("/api/import/url")
async def import_url(request: ImportUrlRequest):
    """Fetch a public pattern page and return its text.

    This returns text only. Whether that text is a pattern, and whether its
    counts are consistent, is decided by /api/check - not here.
    """
    try:
        page = import_pattern_page(request.url)
    except ImportError_ as error:
        raise HTTPException(status_code=error.status, detail=str(error)) from error
    return {
        "url": page.url,
        "title": page.title,
        "text": page.text,
        "content_type": page.content_type,
        "truncated": page.truncated,
    }


@app.post("/api/upload")
async def upload_pattern(file: UploadFile = File(...)):
    try:
        text = (await file.read()).decode("utf-8")
    except Exception:
        raise HTTPException(status_code=400, detail="Could not read file") from None
    try:
        pattern = CrochetParser().parse(text)
        report = validate_pattern(pattern)
        m = measure_pattern(pattern)
        return {
            "status": report.overall_status,
            "score": report.score,
            "errors": [
                {"message": e.message, "location": e.location} for e in report.errors
            ],
            "warnings": [
                {"message": w.message, "location": w.location} for w in report.warnings
            ],
            "rounds": m.total_rounds,
            "max_stitches": m.max_stitch_count,
            "max_diameter_inches": round(m.max_diameter_inches, 2),
            "total_height_inches": round(m.total_height_inches, 2),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e



def _written_views(pattern):
    stitch_sim = simulate_stitches(pattern)
    assembly = written_assembly(pattern)
    geometry = written_geometry(pattern)
    return {
        "stitch_svg": stitch_map_svg(stitch_sim, "Stitch map"),
        "stitch_obj": stitch_model_obj(stitch_sim),
        "stitches": stitch_sim.stitch_count,
        "joins": stitch_sim.join_count,
        "assembly_svg": assembly_map_svg(assembly, "Assembly map"),
        "piece_joins": len(assembly.edges),
        "geometry_svg": geometry_map_svg(geometry, "Geometry map"),
        "geometry_note": geometry.notes[0],
        "note": stitch_sim.notes[0],
    }


@app.post("/api/render")
async def render_pattern(request: CheckRequest):
    try:
        pattern = CrochetParser().parse(request.pattern_text)
        report = validate_pattern(pattern)
        svg = render_2d_preview(pattern, report)
        views = _written_views(pattern)
        return {
            "svg": svg,
            "status": report.overall_status,
            **views,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@app.post("/api/simulate")
async def simulate_pattern(request: CheckRequest):
    try:
        pattern = CrochetParser().parse(request.pattern_text)
        analysis = analyze_pattern_shape(pattern)
        mesh = simulate_surface(pattern)
        views = _written_views(pattern)
        return {
            "shape": analysis.detected_shape.value,
            "confidence": round(analysis.confidence, 2),
            "vertices": len(mesh.vertices),
            "faces": len(mesh.faces),
            "assembly_note": "An assembly line is drawn only when two written pieces are named.",
            "status": "success",
            **views,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


class PdfRequest(BaseModel):
    pattern_text: str
    designer: str | None = None
    template: str = "minimal"
    page_size: str = "A4"
    copyright_text: str = ""
    pattern_version: str = "1.0"
    include_cover: bool = True
    include_charts: bool = True
    include_validation: bool = True
    include_checklist: bool = True
    include_color_key: bool = True
    include_materials: bool = True
    include_abbreviations: bool = True
    include_measurements: bool = True
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


@app.post("/api/pdf")
async def generate_pdf(request: PdfRequest, designer: str | None = None):
    try:
        pattern = CrochetParser().parse(request.pattern_text)
        report = validate_pattern(pattern)
        page_size = request.page_size if request.page_size in {"A4", "Letter", "A5", "Legal"} else "A4"
        binding = request.binding if request.binding in {"none", "left"} else "none"
        template = request.template if request.template in TEMPLATES else "minimal"
        config = PDFConfig(
            designer_name=designer or request.designer or "",
            template=template,
            page_size=page_size,
            copyright_text=request.copyright_text,
            pattern_version=request.pattern_version,
            include_cover=request.include_cover,
            include_charts=request.include_charts,
            include_validation=request.include_validation,
            include_checklist=request.include_checklist,
            include_color_key=request.include_color_key,
            include_materials=request.include_materials,
            include_abbreviations=request.include_abbreviations,
            include_measurements=request.include_measurements,
            large_print=request.large_print,
            ink_saver=request.ink_saver,
            landscape=request.landscape,
            binding=binding,
            compact=request.compact,
            include_marks=request.include_marks,
            include_change=request.include_change,
            include_index=request.include_index,
            include_ruled_notes=request.include_ruled_notes,
            include_used_stitches=request.include_used_stitches,
            duplex=request.duplex,
            cards=request.cards,
            crop_marks=request.crop_marks,
            include_ladder=request.include_ladder,
            include_parse=request.include_parse,
            include_maker=request.include_maker,
            include_map=request.include_map,
        )
        html = PDFGenerator(config).generate(pattern, report)
        return {"html": html, "status": "success", "template": template, "page_size": page_size, "large_print": bool(request.large_print), "landscape": bool(request.landscape), "duplex": bool(request.duplex), "cards": bool(request.cards)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@app.get("/api/health")
async def health():
    return {"status": "ok", "version": __version__}


@app.get("/api/version")
async def version():
    return {"name": "crochet-pattern-checker", "version": __version__}


@app.post("/api/gauge")
async def gauge(request: GaugeRequest):
    """Finished size from a gauge swatch. Estimate, not a measurement."""
    try:
        result = gauge_to_size(
            request.stitches, request.rows, request.sts_per_4in, request.rows_per_4in
        )
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    return {
        "width_in": result.width_in,
        "height_in": result.height_in,
        "width_cm": result.width_cm,
        "height_cm": result.height_cm,
        "note": result.note,
    }


@app.post("/api/convert")
async def convert(request: ConvertRequest):
    """Convert US <-> UK stitch terminology."""
    try:
        converted = convert_terminology(request.pattern_text, request.direction)
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    return {"direction": request.direction, "converted": converted}


@app.post("/api/yarn")
async def yarn(request: YarnRequest):
    """Rough yardage estimate. Not weighed."""
    try:
        estimate = estimate_yarn(request.total_stitches, request.stitch)
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    return {
        "yards": estimate.yards,
        "metres": estimate.metres,
        "balls_100g": estimate.balls_100g,
        "note": estimate.note,
    }


@app.post("/api/chart")
async def chart(request: ChartRequest):
    """Bar chart and silhouette from written per-round stitch counts."""
    if any(count < 0 for count in request.counts):
        raise HTTPException(status_code=422, detail="counts cannot be negative")
    return {
        "chart": stitch_count_chart(request.counts),
        "shape": shape_from_counts(request.counts),
        "note": "Written counts only; this is not a stitch diagram or measurement.",
    }


@app.get("/api/hooks")
async def hooks(weight: str = "worsted"):
    """Hook recommendation for a yarn weight (0-7 or name)."""
    try:
        rec = recommend_hook(weight)
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    return {
        "weight_number": rec.weight_number,
        "weight_name": rec.weight_name,
        "hook_mm_low": rec.hook_mm_low,
        "hook_mm_high": rec.hook_mm_high,
        "hook_us": rec.hook_us,
        "gauge_sts_per_4in": rec.gauge_sts_per_4in,
        "source": rec.source,
    }


@app.post("/api/report")
async def report(request: CheckRequest):
    """Self-contained HTML report: verdict, chart, findings."""
    try:
        pattern = CrochetParser().parse(request.pattern_text)
        validation = validate_pattern(pattern)
        items = pattern.rounds or pattern.rows
        counts: list[int] = []
        prev = 0
        for i, item in enumerate(items):
            try:
                value = (
                    item.computed_stitch_count
                    if i == 0
                    else item.compute_stitch_count_with_context(prev)
                )
            except Exception:
                value = prev
            counts.append(int(value or 0))
            prev = int(value or 0)
        return {
            "html": build_report(pattern, validation),
            "status": validation.overall_status,
            "score": validation.score,
            "chart": stitch_count_chart(counts),
        }
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


def _consensus_service():
    """Lazily create the local history/provider service; credentials stay server-side."""
    service = getattr(app.state, "consensus_service", None)
    if service is None:
        from ..ai_providers.service import ConsensusService

        service = ConsensusService()
        app.state.consensus_service = service
    return service


@app.get("/consensus", response_class=HTMLResponse)
async def consensus_dashboard():
    """Small, dependency-free dashboard for provider runs and revision history."""
    return _consensus_dashboard_html()


@app.get("/api/consensus/providers")
async def consensus_provider_status():
    service = _consensus_service()
    settings = service.settings
    return {
        "status": service.catalog.public_status(),
        "settings": {
            "min_participating_models": settings.min_participating_models,
            "min_participation_ratio": settings.min_participation_ratio,
            "consensus_threshold": settings.consensus_threshold,
            "cross_examination_enabled": settings.enable_cross_examination,
            "adversarial_review_enabled": settings.enable_adversarial_review,
            "strict_required_participation": settings.strict_required_participation,
            "max_revisions": settings.max_revisions,
            "required_roles": list(settings.required_roles),
        },
        "security_note": "Local configuration status only; no live model availability is probed. Credentials are never returned.",
    }


@app.post("/api/consensus/runs", status_code=202)
async def create_consensus_run(request: ConsensusRunRequest, background_tasks: BackgroundTasks):
    if not request.pattern_text.strip():
        raise HTTPException(status_code=422, detail="pattern_text must contain non-whitespace text")
    service = _consensus_service()
    run_id = service.create_run(request.pattern_text)
    background_tasks.add_task(service.execute, run_id)
    record = service.store.get_run(run_id) or {}
    return {"run_id": run_id, "status": "queued", "pattern_hash": record.get("pattern_hash"), "progress": record.get("progress"), "status_url": f"/api/consensus/runs/{run_id}"}


@app.post("/api/consensus/check")
async def run_consensus_now(request: ConsensusRunRequest):
    if not request.pattern_text.strip():
        raise HTTPException(status_code=422, detail="pattern_text must contain non-whitespace text")
    return await _consensus_service().run_now(request.pattern_text)


@app.get("/api/consensus/runs")
async def list_consensus_runs(limit: int = Query(default=50, ge=1, le=200)):
    service = _consensus_service()
    return {"runs": service.store.list_runs(limit), "limit": limit}


@app.get("/api/consensus/runs/{run_id}")
async def get_consensus_run(run_id: str):
    run = _consensus_service().store.get_run(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="Consensus run not found")
    return run


@app.post("/api/consensus/runs/{run_id}/drafts", status_code=202)
async def create_consensus_draft(run_id: str, request: ConsensusDraftRequest, background_tasks: BackgroundTasks):
    service = _consensus_service()
    try:
        child_id, metadata = service.create_revision(run_id, [item.model_dump() for item in request.changes])
    except KeyError as error:
        raise HTTPException(status_code=404, detail="Parent consensus run not found") from error
    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error
    background_tasks.add_task(service.execute, child_id)
    return {"draft": metadata, "status_url": f"/api/consensus/runs/{child_id}"}


def _consensus_dashboard_html() -> str:
    from .consensus_dashboard import dashboard_html

    return dashboard_html()



def get_frontend_html() -> str:
    from .frontend import frontend_html

    return frontend_html()
