from __future__ import annotations
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
from ..model.pattern import Pattern
from ..model.stitch import STITCH_CONSUMPTION, STITCH_PRODUCTION, StitchType

class Severity(str, Enum):
    INFO="INFO"; WARNING="WARNING"; ERROR="ERROR"; CRITICAL="CRITICAL"

class ValidationFinding(BaseModel):
    validator: str; severity: Severity; location: str = ""; message: str
    expected: Optional[int] = None; actual: Optional[int] = None
    suggested_fix: Optional[str] = None; confidence: float = 1.0

class StitchCountReport(BaseModel):
    pattern_title: str = ""; is_consistent: bool = True; total_rows_checked: int = 0
    findings: list[ValidationFinding] = Field(default_factory=list)
    @property
    def errors(self): return [f for f in self.findings if f.severity in (Severity.ERROR, Severity.CRITICAL)]
    @property
    def has_errors(self): return len(self.errors) > 0

class StitchCountValidator:
    def validate(self, pattern):
        self.findings = []
        r = StitchCountReport(pattern_title=pattern.metadata.title or "Untitled")
        if pattern.rounds: self._rounds(pattern.rounds, r)
        elif pattern.rows: self._rows(pattern.rows, r)
        r.findings = self.findings; r.is_consistent = not r.has_errors
        return r
    def _rounds(self, rounds, r):
        if not rounds: return
        exp = None
        for i, cr in enumerate(rounds):
            rn = cr.round_number; loc = f"Round {rn}"
            prod, cons, amb = 0, 0, False
            for inst in cr.instructions:
                if inst.is_ambiguous: amb = True; continue
                if self._ctx(inst):
                    if exp is not None:
                        prod += self._resolve(inst, exp); cons += exp
                    else: amb = True
                else:
                    prod += inst.total_stitches_produced; cons += inst.total_stitches_consumed
            if exp is not None and not amb and cons != exp:
                self.findings.append(ValidationFinding(validator="stitch_counts", severity=Severity.ERROR,
                    location=loc, message=f"Round {rn} consumes {cons} but Round {rn-1} produced {exp}.",
                    expected=exp, actual=cons))
            st = self._stated(cr)
            if st is not None and not amb and st != prod:
                self.findings.append(ValidationFinding(validator="stitch_counts", severity=Severity.ERROR,
                    location=loc, message=f"Round {rn} states {st} but produces {prod}.",
                    expected=st, actual=prod))
            if not amb: exp = prod
            elif st is not None: exp = st
            r.total_rows_checked += 1
            if amb:
                self.findings.append(ValidationFinding(validator="stitch_counts", severity=Severity.WARNING,
                    location=loc, message=f"Round {rn} has context-dependent operations.", confidence=0.7))
    def _rows(self, rows, r):
        exp = None
        for cr in rows:
            prod = sum(i.total_stitches_produced for i in cr.instructions if not i.is_ambiguous)
            cons = sum(i.total_stitches_consumed for i in cr.instructions if not i.is_ambiguous)
            if exp is not None and cons != exp:
                self.findings.append(ValidationFinding(validator="stitch_counts", severity=Severity.ERROR,
                    location=f"Row {cr.row_number}", message=f"Row {cr.row_number} mismatch.", expected=exp, actual=cons))
            if not any(i.is_ambiguous for i in cr.instructions): exp = prod
            r.total_rows_checked += 1
    def _ctx(self, inst): return any(op.into_stitch in ("each_stitch_around","remaining") for op in inst.operations)
    def _resolve(self, inst, avail):
        t, rem = 0, avail
        for op in inst.operations:
            if op.into_stitch in ("each_stitch_around","remaining"):
                t += rem * STITCH_PRODUCTION.get(op.stitch_type,1); rem = 0
            else:
                t += op.count * STITCH_PRODUCTION.get(op.stitch_type,1)
                rem -= op.count * STITCH_CONSUMPTION.get(op.stitch_type,1)
        return t
    def _stated(self, rr):
        for i in rr.instructions:
            if i.stated_stitch_count is not None: return i.stated_stitch_count
        return None

def validate_stitch_counts(pattern): return StitchCountValidator().validate(pattern)
