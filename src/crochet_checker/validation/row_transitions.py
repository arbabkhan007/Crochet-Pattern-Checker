from pydantic import BaseModel, Field
from ..model.pattern import Pattern
from .stitch_counts import Severity, ValidationFinding

class TransitionReport(BaseModel):
    total_transitions_checked: int = 0
    findings: list[ValidationFinding] = Field(default_factory=list)

class RowTransitionValidator:
    def _produced(self, rr, prev):
        """Stitches produced by a round, resolving context-dependent operations
        ('sc in each st around') against the previous round's count."""
        has_ctx = any(op.into_stitch in ("each_stitch_around", "remaining", "second_chain")
                      for i in rr.instructions for op in i.operations)
        if has_ctx and prev:
            return rr.compute_stitch_count_with_context(prev)
        if has_ctx:
            st = next((i.stated_stitch_count for i in rr.instructions
                       if i.stated_stitch_count is not None), None)
            return st or 0
        return rr.computed_stitch_count

    def validate(self, pattern):
        self.findings = []; r = TransitionReport()
        if pattern.rounds and len(pattern.rounds) >= 2:
            prods = []
            prev_round = None
            for c in pattern.rounds:
                boundary = prev_round is not None and c.round_number < prev_round.round_number
                base = None if (boundary or not prods) else prods[-1]
                prods.append(self._produced(c, base))  # parallel to pattern.rounds
                prev_round = c
            for i in range(1, len(pattern.rounds)):
                p, c = pattern.rounds[i-1], pattern.rounds[i]; r.total_transitions_checked += 1
                if c.round_number < p.round_number:
                    continue  # piece boundary, not a real transition
                if prods[i-1] > 0 and 0 < prods[i] / prods[i-1] < 0.5:
                    self.findings.append(ValidationFinding(validator="row_transitions", severity=Severity.WARNING,
                        location=f"Round {c.round_number}",
                        message=f"Big drop: {prods[i-1]} to {prods[i]}"))
                if c.round_number != p.round_number + 1:
                    self.findings.append(ValidationFinding(validator="row_transitions", severity=Severity.WARNING,
                        location=f"Round {c.round_number}", message=f"Numbering jump: {p.round_number} to {c.round_number}"))
        r.findings = self.findings; return r
