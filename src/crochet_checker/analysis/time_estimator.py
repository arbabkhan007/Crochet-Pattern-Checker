"""Time Estimator"""
from dataclasses import dataclass

@dataclass
class TimeEstimate:
    total_hours: float

class TimeEstimator:
    def estimate(self, pattern_text: str, skill_level: str = 'intermediate') -> TimeEstimate:
        stitch_count = pattern_text.lower().count('sc') + pattern_text.lower().count('dc')
        base_minutes = stitch_count * 0.1
        multiplier = {'beginner': 1.5, 'intermediate': 1.0, 'advanced': 0.8}.get(skill_level, 1.0)
        return TimeEstimate(total_hours=(base_minutes * multiplier) / 60)
