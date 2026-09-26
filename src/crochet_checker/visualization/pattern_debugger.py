"""Visual Pattern Debugger"""

from dataclasses import dataclass


@dataclass
class DebugPoint:
    line_number: int
    round_number: int
    stitch_count: int


class PatternDebugger:
    def __init__(self):
        self.breakpoints: list[int] = []

    def set_breakpoint(self, line_number: int):
        if line_number not in self.breakpoints:
            self.breakpoints.append(line_number)
            self.breakpoints.sort()


# Legacy compatibility method.
def _legacy_generate_visual_map(self, pattern_text):
    # Return a deterministic textual visual map for legacy callers.
    lines = str(pattern_text).splitlines()
    output = ["PATTERN VISUAL MAP"]
    for index, line in enumerate(lines, start=1):
        marker = "*" if index in self.breakpoints else " "
        output.append(f"{marker} {index:03d} | {line}")
    return "\\n".join(output)


PatternDebugger.generate_visual_map = _legacy_generate_visual_map
