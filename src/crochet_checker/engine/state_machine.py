"""State Machine - Tracks pattern state"""
class StateMachine:
    def __init__(self):
        self.state = {'stitches': 0}
    
    def execute_instruction(self, stitch_type: str, count: int):
        self.state['stitches'] += count
