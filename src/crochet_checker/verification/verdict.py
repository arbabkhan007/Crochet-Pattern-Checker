"""Honest verdict over the checkers this repo actually runs.

This is not the full specification. Chart detection, photo stitch
classification, a hosted language model, and a stitch-accessibility mesh
are not implemented. Those engines are listed as skipped.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from ..validation.validator import validate_pattern

from .batch import batch_names
from .limits import unread_notes
from .span import span_names


SKIPPED = (
    "chart image detector",
    "photo stitch classifier",
    "hosted language model",
    "vision training set",
    "process cluster",
)


@dataclass
class Verdict:
    status: str
    score: int
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    engines_ran: list[str] = field(default_factory=list)
    engines_skipped: list[str] = field(default_factory=list)
    not_checked: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "status": self.status,
            "score": self.score,
            "errors": self.errors,
            "warnings": self.warnings,
            "engines_ran": self.engines_ran,
            "engines_skipped": self.engines_skipped,
            "not_checked": self.not_checked,
        }


def verify_pattern(text: str) -> Verdict:
    """Run the deterministic checker and label the engines that did not run."""
    report = validate_pattern(text)
    return Verdict(
        status=str(report.overall_status),
        score=int(report.score),
        errors=[str(getattr(item, "message", item)) for item in report.errors],
        warnings=[str(getattr(item, "message", item)) for item in report.warnings],
        engines_ran=[
            "text checker",
            "dialect scope",
            "termination",
            "stitch reachability",
            "references",
            "chart text",
            "short-row gap",
            "ambiguity",
            "gauge band",
            "prose frill",
            "eyes on a frill",
            "closed join",
            "chain underside",
            "dropped body",
            "front and back post",
            "eyes before stuffing",
            "row-end density",
            "incoming cover",
            "missing color",
            "round order",
            "every base stitch",
            "chain length",
            "unclosed repeat",
            "missing star",
            "decrease cover",
            "over-double increase",
            "written-as count",
            "eye count",
            "future round",
            "make count",
            "zero repeat",
            *batch_names(),
            *span_names(),
        ],
        engines_skipped=list(SKIPPED),
        not_checked=unread_notes(text),
    )
