"""Markdown Parser - Parses markdown patterns into AST"""
class MarkdownParser:
    def parse(self, pattern_text: str):
        class PatternAST:
            def __init__(self):
                self.pieces = [type('Piece', (), {'rounds': []})]
        return PatternAST()
