"""Canvas Queue - Manages stitch canvas"""
class CanvasQueue:
    def __init__(self):
        self.canvas = []
        self.current_stitch_count = 0
    
    def initialize_round(self, count: int):
        self.canvas = [None] * count
        self.current_stitch_count = count
