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

    # -- shared math -------------------------------------------------
    def _ctx(self, inst):
        return any(op.into_stitch in ("each_stitch_around", "remaining") for op in inst.operations)
    def _base(self, exp, instructions):
        """Stitches available to a context-dependent row: the previous row's
        count, or (for a first row) the foundation chain length."""
        if exp is not None: return exp
        ch = max((op.count for i in instructions for op in i.operations
                  if op.stitch_type == StitchType.CHAIN), default=0)
        return ch if ch >= 2 else None
    def _resolve(self, inst, avail):
        t, rem = 0, avail
        for op in inst.operations:
            if op.into_stitch in ("each_stitch_around", "remaining"):
                t += rem * STITCH_PRODUCTION.get(op.stitch_type, 1); rem = 0
            elif op.into_stitch == "second_chain":
                t += 1; rem -= 2
            else:
                t += op.count * STITCH_PRODUCTION.get(op.stitch_type, 1)
                rem -= op.count * STITCH_CONSUMPTION.get(op.stitch_type, 1)
        return t
    def _stated(self, rr):
        for i in rr.instructions:
            if i.stated_stitch_count is not None: return i.stated_stitch_count
        return None
    def _count(self, cr, exp):
        """(produced, consumed, ambiguous) for one row/round given the previous count."""
        base = self._base(exp, cr.instructions)
        prod, cons, amb = 0, 0, False
        for inst in cr.instructions:
            if inst.is_ambiguous: amb = True; continue
            if self._ctx(inst):
                if base is not None:
                    prod += self._resolve(inst, base); cons += base
                else: amb = True
            else:
                prod += inst.total_stitches_produced; cons += inst.total_stitches_consumed
        return prod, cons, amb

    # -- patterns ----------------------------------------------------
    def _rounds(self, rounds, r):
        if not rounds: return
        exp = None
        prev_num = 0
        for i, cr in enumerate(rounds):
            if cr.round_number < prev_num:
                exp = None  # numbering restarts: start of a new piece
            prev_num = cr.round_number
            rn = cr.round_number; loc = f"Round {rn}"
            prod, cons, amb = self._count(cr, exp)
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
            rn = cr.row_number; loc = f"Row {rn}"
            prod, cons, amb = self._count(cr, exp)
            if exp is not None and not amb and cons != exp:
                self.findings.append(ValidationFinding(validator="stitch_counts", severity=Severity.ERROR,
                    location=loc, message=f"Row {rn} consumes {cons} but Row {rn-1} produced {exp}.",
                    expected=exp, actual=cons))
            st = self._stated(cr)
            if st is not None and not amb and st != prod:
                self.findings.append(ValidationFinding(validator="stitch_counts", severity=Severity.ERROR,
                    location=loc, message=f"Row {rn} states {st} but produces {prod}.",
                    expected=st, actual=prod))
            if not amb: exp = prod
            elif st is not None: exp = st
            r.total_rows_checked += 1
            if amb:
                self.findings.append(ValidationFinding(validator="stitch_counts", severity=Severity.WARNING,
                    location=loc, message=f"Row {rn} has context-dependent operations.", confidence=0.7))

def validate_stitch_counts(pattern): return StitchCountValidator().validate(pattern)
