from pydantic import BaseModel, Field
from ..model.pattern import Pattern
from .stitch_counts import Severity, ValidationFinding

class TransitionReport(BaseModel):
    total_transitions_checked: int = 0
    findings: list[ValidationFinding] = Field(default_factory=list)

class RowTransitionValidator:
    def validate(self, pattern):
        self.findings = []; r = TransitionReport()
        if pattern.rounds and len(pattern.rounds) >= 2:
            for i in range(1, len(pattern.rounds)):
                p, c = pattern.rounds[i-1], pattern.rounds[i]; r.total_transitions_checked += 1
                pc, cc = p.computed_stitch_count, c.computed_stitches_consumed
                if pc > 0 and cc > 0 and cc/pc < 0.5:
                    self.findings.append(ValidationFinding(validator="row_transitions", severity=Severity.WARNING,
                        location=f"Round {c.round_number}", message=f"Big drop: {pc} to {cc}"))
                if c.round_number != p.round_number + 1:
                    self.findings.append(ValidationFinding(validator="row_transitions", severity=Severity.WARNING,
                        location=f"Round {c.round_number}", message=f"Numbering jump: {p.round_number} to {c.round_number}"))
        r.findings = self.findings; return r
