"""Visual Pattern Debugger"""
from typing import List
from dataclasses import dataclass

@dataclass
class DebugPoint:
    line_number: int
    round_number: int
    stitch_count: int

class PatternDebugger:
    def __init__(self):
        self.breakpoints: List[int] = []
    
    def set_breakpoint(self, line_number: int):
        if line_number not in self.breakpoints:
            self.breakpoints.append(line_number)
            self.breakpoints.sort()
