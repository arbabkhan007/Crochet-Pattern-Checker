"""Multi-piece validation - validates each piece independently."""
from typing import Optional
from .stitch_counts import StitchCountValidator, ValidationFinding

class MultiPieceValidator:
    def validate(self, pattern):
        findings = []
        if hasattr(pattern, 'pieces') and pattern.pieces:
            for piece in pattern.pieces:
                piece_findings = self._validate_piece(piece, pattern)
                findings.extend(piece_findings)
        else:
            validator = StitchCountValidator()
            findings = validator.validate(pattern)
        return findings
    
    def _validate_piece(self, piece, pattern):
        from ..model.pattern import Pattern
        mini_pattern = Pattern(
            metadata=pattern.metadata,
            construction=pattern.construction,
            rounds=piece.rounds if piece.is_rounds else [],
            rows=piece.rows if not piece.is_rounds else [],
        )
        validator = StitchCountValidator()
        piece_findings = validator.validate(mini_pattern)
        for finding in piece_findings:
            finding.message = f"[{piece.name}] {finding.message}"
        return piece_findings

def validate_multi_piece(pattern):
    validator = MultiPieceValidator()
    return validator.validate(pattern)
