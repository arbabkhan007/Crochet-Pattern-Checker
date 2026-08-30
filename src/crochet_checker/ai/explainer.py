"""Pattern explanation engine."""
from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, Field
from ..model.pattern import Pattern
from ..validation import ValidationReport, ValidationFinding
from ..visualization.measurements import measure_pattern, PatternMeasurements

class ExplanationResult(BaseModel):
    summary: str = ""
    explanation: str = ""
    highlights: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
    shape_guess: str = ""
    difficulty_explanation: str = ""

class PatternExplainer:
    def explain(self, pattern, report):
        m = measure_pattern(pattern)
        return ExplanationResult(
            summary=self._summary(pattern, report, m),
            explanation=self._explanation(pattern, report, m),
            highlights=self._highlights(pattern, report, m),
            recommendations=self._recommendations(pattern, report, m),
            shape_guess=self._guess_shape(pattern, m),
            difficulty_explanation=self._difficulty(pattern),
        )
    def _summary(self, p, r, m):
        items = p.rounds or p.rows; n = len(items) if items else 0
        label = "rounds" if p.rounds else "rows"
        title = p.metadata.title or "This pattern"
        s = r.overall_status
        v = "passes all checks" if "PASS" in s and "WARNING" not in s else "passes with minor warnings" if "PASS" in s else "needs review" if "REVIEW" in s else "has errors"
        parts = [f"{title} has {n} {label} and {v}."]
        if m.max_diameter_inches > 0: parts.append(f"It produces approximately {m.max_diameter_inches:.1f} inches across and {m.total_height_inches:.1f} inches tall.")
        return " ".join(parts)
    def _explanation(self, p, r, m):
        lines = [f"**Construction:** Worked in {p.construction.value.replace(chr(95),chr(32))}s."]
        items = p.rounds or p.rows
        if items and len(items) >= 2:
            fc = items[0].computed_stitch_count
            if fc == 0:
                for i in items[0].instructions:
                    if i.stated_stitch_count: fc = i.stated_stitch_count; break
            lc = items[-1].computed_stitch_count
            if lc == 0:
                for i in items[-1].instructions:
                    if i.stated_stitch_count: lc = i.stated_stitch_count; break
            if fc > 0 and lc > 0:
                if lc > fc: lines.append(f"**Growth:** {fc} to {lc} stitches - increasing.")
                elif lc < fc: lines.append(f"**Shrinking:** {fc} to {lc} stitches - decreasing.")
                else: lines.append(f"**Steady:** stays at {fc} stitches.")
        if r.errors:
            lines.append(f"\n**Errors ({len(r.errors)}):**")
            for e in r.errors[:3]: lines.append(f"  - [{e.location}] {e.message}")
        if r.warnings:
            lines.append(f"\n**Warnings ({len(r.warnings)}):**")
            for w in r.warnings[:3]: lines.append(f"  - [{w.location}] {w.message}")
        return chr(10).join(lines)
    def _highlights(self, p, r, m):
        h = []; items = p.rounds or p.rows
        if not items: return ["No rounds detected"]
        fs = items[0].computed_stitch_count
        for i in items[0].instructions:
            if i.stated_stitch_count: fs = i.stated_stitch_count; break
        ls = items[-1].computed_stitch_count
        for i in items[-1].instructions:
            if i.stated_stitch_count: ls = i.stated_stitch_count; break
        h.append(f"Starts with {fs} stitches"); h.append(f"Ends with {ls} stitches")
        h.append(f"Total {len(items)} rounds" if p.rounds else f"Total {len(items)} rows")
        if m.max_diameter_inches > 0: h.append(f"~{m.max_diameter_inches:.1f} inches across")
        h.append(f"Score: {r.score}/100")
        return h
    def _recommendations(self, p, r, m):
        recs = []
        if r.errors: recs.append("Fix errors before crocheting")
        if r.warnings: recs.append("Review warnings")
        items = p.rounds or p.rows
        if items:
            if not p.gauge: recs.append("Add gauge for consistent sizing")
            if not p.yarn or not p.yarn.weight: recs.append("Add yarn weight info")
            if any("magic ring" in r2.source_text.lower() for r2 in items[:2]): recs.append("Uses magic ring!")
        return recs if recs else ["Pattern looks clean!"]
    def _guess_shape(self, p, m):
        items = p.rounds or p.rows
        if not items: return "unknown"
        fc = items[0].computed_stitch_count or 6; lc = items[-1].computed_stitch_count or 6
        has_dec = False
        if len(items) >= 3:
            for r in items[-3:]:
                for inst in r.instructions:
                    for op in inst.operations:
                        if op.stitch_type.value in ("decrease", "sc2tog"): has_dec = True
        if has_dec and lc <= fc + 2: return "sphere or amigurumi"
        elif lc > fc and not has_dec: return "flat circle or cone"
        elif lc < fc: return "decreasing shape"
        else: return "tube or straight piece"
    def _difficulty(self, p):
        items = p.rounds or p.rows
        if not items: return "Unable to determine"
        n = len(items)
        has_complex = False; has_repeats = False
        for r in items:
            for inst in r.instructions:
                for op in inst.operations:
                    if op.stitch_type.value in ("treble", "double_treble"): has_complex = True
                if inst.repeat_count and inst.repeat_count > 1: has_repeats = True
        parts = []
        if n <= 5: parts.append("Short - beginner-friendly")
        elif n <= 15: parts.append("Medium-length")
        else: parts.append("Long pattern")
        if has_complex: parts.append("advanced stitches")
        if has_repeats: parts.append("has repeats")
        return ". ".join(parts) + "."

def explain_pattern(pattern, report):
    return PatternExplainer().explain(pattern, report)
