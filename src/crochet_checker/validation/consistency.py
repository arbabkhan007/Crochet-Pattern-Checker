from pydantic import BaseModel, Field
from ..model.pattern import Pattern
from .stitch_counts import Severity, ValidationFinding

class ConsistencyReport(BaseModel):
    findings: list[ValidationFinding] = Field(default_factory=list)

class ConsistencyValidator:
    def validate(self, pattern):
        self.findings = []
        if pattern.rounds:
            for r in pattern.rounds:
                if not r.instructions:
                    self.findings.append(ValidationFinding(validator="consistency", severity=Severity.ERROR,
                        location=f"Round {r.round_number}", message=f"Round {r.round_number} empty."))
        return ConsistencyReport(findings=self.findings)
