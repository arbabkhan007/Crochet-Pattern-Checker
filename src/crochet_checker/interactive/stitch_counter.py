"""Interactive Stitch Counter"""
from typing import Dict
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class CounterState:
    current_round: int = 1
    current_stitch: int = 0
    total_stitches: int = 0
    round_stitches: Dict[int, int] = field(default_factory=dict)

class InteractiveStitchCounter:
    def __init__(self, target_rounds: Dict[int, int] = None):
        self.state = CounterState()
        self.target_rounds = target_rounds or {}
    
    def complete_stitch(self, stitch_type: str = "sc"):
        self.state.current_stitch += 1
        self.state.total_stitches += 1
        if self.state.current_round not in self.state.round_stitches:
            self.state.round_stitches[self.state.current_round] = 0
        self.state.round_stitches[self.state.current_round] += 1
    
    def get_progress(self) -> Dict:
        return {'current_round': self.state.current_round, 'total_stitches': self.state.total_stitches}
