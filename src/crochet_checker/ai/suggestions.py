"""Fix suggestion engine."""
from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, Field
from ..model.pattern import Pattern
from ..validation import ValidationReport, ValidationFinding

class Suggestion(BaseModel):
    error_location: str = ""
    error_message: str = ""
    suggestion: str = ""
    confidence: str = "medium"
    corrected_text: Optional[str] = None
    explanation: str = ""

class SuggestionEngine:
    def generate_suggestions(self, pattern, report):
        sugs = []
        for err in report.errors:
            s = self._suggest(pattern, err)
            if s: sugs.append(s)
        return sugs
    def _suggest(self, p, err):
        msg = err.message.lower()
        if "stitch count" in msg or "mismatch" in msg or "inconsistent" in msg:
            return Suggestion(error_location=err.location, error_message=err.message,
                suggestion="Check the stitch count - each inc=2 sts, dec=1 st (uses 2)",
                confidence="medium", explanation="Count carefully: sc=1, inc=2, dec=1")
        if "missing" in msg:
            return Suggestion(error_location=err.location, error_message=err.message,
                suggestion="Add stitch count in parentheses at end of round", confidence="high")
        if "unknown" in msg:
            return Suggestion(error_location=err.location, error_message=err.message,
                suggestion="Check abbreviation: sc, hdc, dc, tr, sl st, ch", confidence="medium")
        return Suggestion(error_location=err.location, error_message=err.message,
            suggestion="Review this round manually", confidence="low")

def generate_suggestions(pattern, report):
    return SuggestionEngine().generate_suggestions(pattern, report)
