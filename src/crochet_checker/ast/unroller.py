"""Repeat Unroller - Expands repeat patterns"""
class Unroller:
    def unroll(self, pattern_text: str) -> str:
        import re
        match = re.search(r'\*(.+?)\*\s*repeat\s*(\d+)\s*times', pattern_text)
        if match:
            pattern = match.group(1)
            times = int(match.group(2))
            return (pattern + ' ') * times
        return pattern_text
