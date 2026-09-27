"""Enterprise REST API for validation and certification."""

from __future__ import annotations

from typing import Any

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from ..parser.parser import parse_pattern
from ..validation import validate_pattern
from .certification import EnterpriseCertifier
from .report import CertificationReportWriter
from .gauge import GaugeCalibrator, GaugeMeasurement
from .security import RateLimiter, require_api_key
from .vision import GaugeImageIngestor


rate_limiter = RateLimiter(
    max_requests=int(
        __import__("os").environ.get(
            "CROCHET_RATE_LIMIT",
            "60",
        )
    )
)

app = FastAPI(
    title="Crochet Pattern Enterprise Validator",
    version="1.0.0",
    description=(
        "Compiler-based crochet pattern validation, risk analysis, "
        "gauge calibration, and certification."
    ),
)


class BatchPatternRequest(BaseModel):
    patterns: list[PatternRequest] = Field(
        min_length=1,
        max_length=100,
    )


class PatternRequest(BaseModel):
    pattern_text: str = Field(min_length=1)
    gauge_verified: bool = False
    yarn_profile_known: bool = False
    geometry_verified: bool = False
    ai_conflicts: bool = False
    safety_passed: bool = True
    tolerance_passed: bool = False


class ImageGaugeRequest(BaseModel):
    stitch_count: int = Field(gt=0)
    row_count: int = Field(gt=0)
    width_cm: float = Field(gt=0)
    height_cm: float = Field(gt=0)
    confidence: float = Field(default=0.90, ge=0.0, le=1.0)


class GaugeRequest(BaseModel):
    target_stitches_per_10cm: float = Field(gt=0)
    target_rows_per_10cm: float = Field(gt=0)
    measured_stitches_per_10cm: float = Field(gt=0)
    measured_rows_per_10cm: float = Field(gt=0)
    tolerance_percent: float = Field(default=5.0, gt=0)


def _messages(items) -> list[str]:
    return [
        getattr(item, "message", str(item))
        for item in items
    ]


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "healthy",
        "service": "crochet-pattern-enterprise-validator",
        "version": "1.0.0",
    }


@app.post("/validate")
def validate(
    request: PatternRequest,
    identity: str = Depends(require_api_key),
) -> dict[str, Any]:
    rate_limiter.check(identity)
    try:
        pattern = parse_pattern(request.pattern_text)
        report = validate_pattern(pattern)

        return {
            "valid": report.valid,
            "score": report.score,
            "overall_status": report.overall_status,
            "errors": _messages(report.errors),
            "warnings": _messages(report.warnings),
            "stitch_count": report.stitch_count,
            "pattern_hash": EnterpriseCertifier.pattern_hash(pattern),
        }
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


@app.post("/certify")
def certify(
    request: PatternRequest,
    identity: str = Depends(require_api_key),
) -> dict[str, Any]:
    rate_limiter.check(identity)
    try:
        pattern = parse_pattern(request.pattern_text)
        compiler_report = validate_pattern(pattern)

        certificate = EnterpriseCertifier().certify(
            pattern,
            compiler_report,
            gauge_verified=request.gauge_verified,
            yarn_profile_known=request.yarn_profile_known,
            geometry_verified=request.geometry_verified,
            ai_conflicts=request.ai_conflicts,
            safety_passed=request.safety_passed,
            tolerance_passed=request.tolerance_passed,
        )

        return certificate.to_dict()
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


@app.post("/gauge/calibrate")
def calibrate_gauge(
    request: GaugeRequest,
    identity: str = Depends(require_api_key),
) -> dict[str, Any]:
    rate_limiter.check(identity)
    target = GaugeMeasurement(
        stitches_per_10cm=request.target_stitches_per_10cm,
        rows_per_10cm=request.target_rows_per_10cm,
        source="pattern",
        confidence=1.0,
    )

    measured = GaugeMeasurement(
        stitches_per_10cm=request.measured_stitches_per_10cm,
        rows_per_10cm=request.measured_rows_per_10cm,
        source="measurement",
        confidence=0.85,
    )

    result = GaugeCalibrator(
        tolerance_percent=request.tolerance_percent,
    ).calibrate(target, measured)

    return result.to_dict()


@app.post("/gauge/image")
async def calibrate_gauge_image(
    image: UploadFile = File(...),
    stitch_count: int = 1,
    row_count: int = 1,
    width_cm: float = 1.0,
    height_cm: float = 1.0,
    confidence: float = 0.90,
    identity: str = Depends(require_api_key),
) -> dict[str, Any]:
    """Upload a gauge image with confirmed measurements."""

    rate_limiter.check(identity)

    allowed = {
        "image/png",
        "image/jpeg",
        "image/webp",
    }

    if image.content_type not in allowed:
        raise HTTPException(
            status_code=415,
            detail="Use PNG, JPEG, or WEBP images.",
        )

    upload_dir = __import__("pathlib").Path(
        ".crochet_cache/uploads"
    )
    upload_dir.mkdir(parents=True, exist_ok=True)

    destination = upload_dir / (
        image.filename or "gauge-swatch-upload"
    )

    content = await image.read()

    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail="Image must be smaller than 10 MB.",
        )

    destination.write_bytes(content)

    try:
        result = GaugeImageIngestor().calibrate_confirmed_measurement(
            str(destination),
            stitch_count=stitch_count,
            row_count=row_count,
            width_cm=width_cm,
            height_cm=height_cm,
            confirmed_by_user=True,
            confidence=confidence,
        )
        return result.to_dict()
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


@app.post("/report", response_class=HTMLResponse)
def certification_report(
    request: PatternRequest,
    identity: str = Depends(require_api_key),
) -> HTMLResponse:
    """Generate an HTML commercial certification report."""

    rate_limiter.check(identity)

    try:
        pattern = parse_pattern(request.pattern_text)
        compiler_report = validate_pattern(pattern)

        certificate = EnterpriseCertifier().certify(
            pattern,
            compiler_report,
            gauge_verified=request.gauge_verified,
            yarn_profile_known=request.yarn_profile_known,
            geometry_verified=request.geometry_verified,
            ai_conflicts=request.ai_conflicts,
            safety_passed=request.safety_passed,
            tolerance_passed=request.tolerance_passed,
        )

        html = CertificationReportWriter().render(
            certificate,
            title="Crochet Pattern Enterprise Certificate",
        )

        return HTMLResponse(
            content=html,
            media_type="text/html",
        )
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


@app.post("/batch/validate")
def batch_validate(
    request: BatchPatternRequest,
    identity: str = Depends(require_api_key),
) -> dict[str, Any]:
    """Validate up to 100 patterns and return a production summary."""

    rate_limiter.check(identity)

    results = []
    passed = 0
    failed = 0

    for index, item in enumerate(request.patterns):
        try:
            pattern = parse_pattern(item.pattern_text)
            report = validate_pattern(pattern)

            valid = bool(report.valid)

            if valid:
                passed += 1
            else:
                failed += 1

            results.append(
                {
                    "index": index,
                    "valid": valid,
                    "score": report.score,
                    "overall_status": report.overall_status,
                    "errors": _messages(report.errors),
                    "warnings": _messages(report.warnings),
                    "stitch_count": report.stitch_count,
                    "pattern_hash": EnterpriseCertifier.pattern_hash(
                        pattern
                    ),
                }
            )
        except Exception as exc:
            failed += 1
            results.append(
                {
                    "index": index,
                    "valid": False,
                    "score": 0,
                    "overall_status": "ERROR",
                    "errors": [str(exc)],
                    "warnings": [],
                }
            )

    total = len(request.patterns)

    return {
        "total": total,
        "passed": passed,
        "failed": failed,
        "success_rate": round(passed / total, 4),
        "results": results,
    }
