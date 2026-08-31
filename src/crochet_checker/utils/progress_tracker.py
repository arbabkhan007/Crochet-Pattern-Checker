"""Progress Tracker - Track crochet progress."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field
from ..model.pattern import Pattern

class ProgressEntry(BaseModel):
    round_number: int
    completed: bool = False
    completed_at: Optional[datetime] = None
    notes: Optional[str] = None

class ProjectProgress(BaseModel):
    pattern_name: str
    total_rounds: int
    completed_rounds: int
    percentage: float
    current_round: int
    estimated_time_remaining: Optional[str] = None
    notes: list[str] = Field(default_factory=list)

class ProgressTracker:
    def __init__(self, pattern, project_name=None):
        self.pattern = pattern
        self.project_name = project_name or pattern.metadata.title or "Untitled"
        self.rounds = pattern.rounds or []
        self.total_rounds = len(self.rounds)
        self.progress = {i: ProgressEntry(round_number=i) for i in range(1, self.total_rounds + 1)}
        self.notes = []
    
    def complete_round(self, round_number, notes=None):
        if round_number in self.progress:
            self.progress[round_number].completed = True
            self.progress[round_number].completed_at = datetime.now()
            if notes: self.progress[round_number].notes = notes
            return True
        return False
    
    def uncomplete_round(self, round_number):
        if round_number in self.progress:
            self.progress[round_number].completed = False
            return True
        return False
    
    def get_current_round(self):
        return next((i for i in range(1, self.total_rounds + 1) if not self.progress[i].completed), self.total_rounds + 1)
    
    def get_percentage(self):
        completed = sum(1 for e in self.progress.values() if e.completed)
        return (completed / self.total_rounds * 100) if self.total_rounds > 0 else 0
    
    def add_note(self, note):
        self.notes.append(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] {note}")
    
    def save(self, filepath):
        data = {"pattern_name": self.project_name, "total_rounds": self.total_rounds,
                "progress": {str(k): {"completed": v.completed, "notes": v.notes} for k, v in self.progress.items()},
                "notes": self.notes}
        Path(filepath).write_text(json.dumps(data, indent=2))
    
    def get_summary(self):
        completed = sum(1 for e in self.progress.values() if e.completed)
        percentage = self.get_percentage()
        current = self.get_current_round()
        remaining = self.total_rounds - completed
        time_est = f"~{remaining * 2} minutes" if remaining > 0 else "Complete!"
        
        lines = [f"\U0001f9f6 {self.project_name}", "\u2501" * 20,
                f"Progress: {completed}/{self.total_rounds} rounds ({percentage:.1f}%)",
                f"Current: Round {current}", f"Time remaining: {time_est}"]
        if self.notes:
            lines.append("\nNotes:")
            lines.extend(f"  \u2022 {n}" for n in self.notes[-5:])
        return "\n".join(lines)

def track_progress(pattern, project_name=None):
    return ProgressTracker(pattern, project_name)
