"""Assembly Graph - Manages piece assembly"""
class AssemblyGraph:
    def __init__(self):
        self.pieces = []
    
    def add_piece(self, piece_name: str):
        self.pieces.append(piece_name)
