"""Pattern description generator for marketing."""
from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, Field
from ..model.pattern import Pattern
from ..validation import ValidationReport
from ..visualization.measurements import measure_pattern, PatternMeasurements

class PatternDescription(BaseModel):
    title: str = ""
    short_description: str = ""
    full_description: str = ""
    materials_list: list[str] = Field(default_factory=list)
    skill_level: str = ""
    finished_size: str = ""
    tags: list[str] = Field(default_factory=list)
    features: list[str] = Field(default_factory=list)

class DescriptionGenerator:
    def generate(self, pattern, report=None):
        m = measure_pattern(pattern)
        return PatternDescription(
            title=self._title(pattern, m), short_description=self._short(pattern, m),
            full_description=self._full(pattern, m, report),
            materials_list=self._materials(pattern), skill_level=self._skill(pattern, m),
            finished_size=self._size(m), tags=self._tags(pattern, m),
            features=self._features(pattern, m))
    def _has_st(self, items, vals, last_n=None):
        check = items[-last_n:] if last_n else items
        for r in check:
            for inst in r.instructions:
                for op in inst.operations:
                    if op.stitch_type.value in vals: return True
        return False
    def _title(self, p, m):
        t = p.metadata.title or "Crochet Pattern"; items = p.rounds or p.rows
        if items:
            fc = items[0].computed_stitch_count or 6; lc = items[-1].computed_stitch_count or 6
            hd = self._has_st(items, ["decrease","sc2tog"], 3)
            if lc > fc and not hd: s = "Flat Circle"
            elif lc <= fc+2 and hd: s = "Amigurumi"
            else: s = "Crochet"
        else: s = "Crochet"
        return f"{s} {t}"
    def _short(self, p, m):
        items = p.rounds or p.rows; n = len(items) if items else 0
        parts = []
        if n: parts.append(f"{n}-round pattern")
        if m.max_diameter_inches > 0: parts.append(f"~{m.max_diameter_inches:.1f} inches")
        return "A " + ", ".join(parts) + " crochet pattern" if parts else "A crochet pattern"
    def _full(self, p, m, r):
        lines = [f"Create your own {p.metadata.title or 'pattern'}!", ""]
        items = p.rounds or p.rows
        if items: lines.append(f"**What You'll Make:** {len(items)} {'rounds' if p.rounds else 'rows'} of stitches.")
        if m.max_diameter_inches > 0: lines.append(f"**Size:** ~{m.max_diameter_inches:.1f}in x {m.total_height_inches:.1f}in ({m.max_diameter_inches*2.54:.1f}cm x {m.total_height_inches*2.54:.1f}cm)")
        if r and "PASS" in r.overall_status: lines.append("**Quality:** Validated pattern!")
        lines.append(f"**Construction:** {p.construction.value.replace(chr(95),chr(32))}s, US terms.")
        lines.append(f"**Skill:** {self._skill(p, m)}")
        return chr(10).join(lines)
    def _materials(self, p):
        mats = []
        if p.yarn and p.yarn.name: mats.append(f"Yarn: {p.yarn.name}")
        if p.hook and p.hook.size_mm: mats.append(f"Hook: {p.hook.size_mm}mm")
        if not mats: mats = ["Yarn (see pattern)", "Hook (see pattern)"]
        mats.extend(["Yarn needle", "Scissors", "Stitch markers"])
        return mats
    def _skill(self, p, m):
        items = p.rounds or p.rows
        if not items: return "Beginner"
        n = len(items); hc = self._has_st(items, ["treble","double_treble"])
        hi = self._has_st(items, ["increase"]); hd = self._has_st(items, ["decrease","sc2tog"])
        if n <= 5 and not hc: return "Beginner"
        if n <= 15 and not hc: return "Easy" if hi and hd else "Beginner-Easy"
        if hc: return "Intermediate"
        return "Easy-Intermediate"
    def _size(self, m):
        if m.max_diameter_inches <= 0: return "Not determined"
        return f'{m.max_diameter_inches:.1f}" x {m.total_height_inches:.1f}" ({m.max_diameter_inches*2.54:.1f}cm x {m.total_height_inches*2.54:.1f}cm)'
    def _tags(self, p, m):
        tags = ["crochet", "pattern"]; items = p.rounds or p.rows
        if items:
            if p.rounds: tags.extend(["rounds", "circular"])
            if m.max_diameter_inches < 4: tags.extend(["amigurumi", "small"])
            elif m.max_diameter_inches < 8: tags.append("medium")
            else: tags.append("large")
            if any("magic ring" in r.source_text.lower() for r in items[:2]): tags.extend(["magic ring", "center start"])
        return tags
    def _features(self, p, m):
        f = []; items = p.rounds or p.rows
        if items: f.append(f"{len(items)} rounds of instructions"); f.append("Stitch counts every round")
        if m.max_diameter_inches > 0: f.append(f"~{m.max_diameter_inches:.1f} inches across")
        f.extend(["US terminology", "Validated pattern"])
        return f

def generate_description(pattern, report=None):
    return DescriptionGenerator().generate(pattern, report)
