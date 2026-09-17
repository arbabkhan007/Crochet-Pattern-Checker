from __future__ import annotations
from pydantic import BaseModel, Field
from ..model.pattern import Pattern
from ..model.stitch import STITCH_CONSUMPTION, STITCH_PRODUCTION, StitchType
from .stitch_counts import Severity, ValidationFinding

class TransitionReport(BaseModel):
    total_transitions_checked: int = 0
    findings: list[ValidationFinding] = Field(default_factory=list)

class RowTransitionValidator:
    """Checks suspicious transitions between consecutive rounds.

    Context-dependent operations ("sc in each st around") are resolved
    against the previous round's production before comparing, so an
    every-stitch round is never mistaken for a 1-stitch round.
    """

    def validate(self, pattern):
        self.findings = []; r = TransitionReport()
        if pattern.rounds and len(pattern.rounds) >= 2:
            exp = None
            for i, c in enumerate(pattern.rounds):
                if i == 0:
                    exp = self._produced(c, None)
                    continue
                p = pattern.rounds[i-1]
                r.total_transitions_checked += 1
                cc = self._consumed(c, exp) if exp is not None else c.computed_stitches_consumed
                if exp and cc and cc / exp < 0.5:
                    self.findings.append(ValidationFinding(validator="row_transitions", severity=Severity.WARNING,
                        location=f"Round {c.round_number}", message=f"Big drop: {exp} to {cc}",
                        expected=exp, actual=cc, confidence=0.6))
                if c.round_number != p.round_number + 1:
                    self.findings.append(ValidationFinding(validator="row_transitions", severity=Severity.WARNING,
                        location=f"Round {c.round_number}", message=f"Numbering jump: {p.round_number} to {c.round_number}"))
                exp = self._produced(c, exp)
        r.findings = self.findings; return r

    def _ctx(self, inst):
        return any(op.into_stitch in ("each_stitch_around", "remaining") for op in inst.operations)

    def _chain_only_ring(self, rnd):
        """Foundation rings: a round that only chains and joins produces its stated size."""
        ops = [op for i in rnd.instructions if not i.is_ambiguous for op in i.operations]
        if ops and all(op.stitch_type in (StitchType.CHAIN, StitchType.SLIP_STITCH) for op in ops):
            return self._stated(rnd)
        return None

    def _produced(self, rnd, avail):
        amb = any(i.is_ambiguous for i in rnd.instructions)
        ring = self._chain_only_ring(rnd)
        if ring is not None:
            return ring
        total = 0
        for inst in rnd.instructions:
            if inst.is_ambiguous: continue
            if self._ctx(inst):
                if avail is not None:
                    total += self._resolve(inst, avail)
                else:
                    return None  # unresolved context at pattern start
            else:
                total += inst.total_stitches_produced
        if amb:
            st = self._stated(rnd)
            if st is not None: return st
        return total

    def _consumed(self, rnd, avail):
        total = 0
        for inst in rnd.instructions:
            if inst.is_ambiguous: continue
            if self._ctx(inst):
                total += avail or 0
            else:
                total += inst.total_stitches_consumed
        return total

    def _resolve(self, inst, avail):
        t, rem = 0, avail
        for op in inst.operations:
            if op.into_stitch in ("each_stitch_around", "remaining"):
                t += rem * STITCH_PRODUCTION.get(op.stitch_type, 1); rem = 0
            else:
                t += op.count * STITCH_PRODUCTION.get(op.stitch_type, 1)
                rem -= op.count * STITCH_CONSUMPTION.get(op.stitch_type, 1)
        return t

    def _stated(self, rnd):
        for i in rnd.instructions:
            if i.stated_stitch_count is not None: return i.stated_stitch_count
        return None
