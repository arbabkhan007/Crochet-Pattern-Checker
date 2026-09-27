"""Enterprise REST API for validation and certification."""

from __future__ import annotations

from typing import Any

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field

from ..parser.parser import parse_pattern
from ..validation import validate_pattern
from .certification import EnterpriseCertifier
from .gauge import GaugeCalibrator, GaugeMeasurement
from .security import RateLimiter, require_api_key


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


class PatternRequest(BaseModel):
    pattern_text: str = Field(min_length=1)
    gauge_verified: bool = False
    yarn_profile_known: bool = False
    geometry_verified: bool = False
    ai_conflicts: bool = False
    safety_passed: bool = True
    tolerance_passed: bool = False


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
