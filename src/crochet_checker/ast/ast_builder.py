"""AST Builder - Builds abstract syntax tree"""
class ASTBuilder:
    def build(self, pattern_text: str):
        class PatternAST:
            def __init__(self):
                self.pieces = [type('Piece', (), {'rounds': []})]
        return PatternAST()
