"""
Multi-piece validation - validates each piece independently.
Eliminates false positives from piece boundaries.
"""

from .stitch_counts import StitchCountValidator, ValidationFinding


class MultiPieceValidator:
    """Validates multi-piece patterns by checking each piece independently."""

    def __init__(self):
        self.findings = []

    def validate(self, pattern) -> list[ValidationFinding]:
        """
        Validate a multi-piece pattern.

        If pattern has pieces, validate each piece independently.
        If pattern has no pieces, fall back to normal validation.
        """
        findings = []

        # Check if pattern has multiple pieces
        if hasattr(pattern, "pieces") and pattern.pieces:
            # Multi-piece pattern - validate each piece independently
            for piece in pattern.pieces:
                piece_findings = self._validate_piece(piece, pattern)
                findings.extend(piece_findings)
        else:
            # Single piece pattern - use normal validator
            validator = StitchCountValidator()
            findings = validator.validate(pattern)

        return findings

    def _validate_piece(self, piece, pattern) -> list[ValidationFinding]:
        """Validate a single piece independently."""
        findings = []

        # Create a mini-pattern for this piece
        from ..model.pattern import Pattern

        mini_pattern = Pattern(
            metadata=pattern.metadata,
            construction=pattern.construction,
            rounds=piece.rounds if piece.is_rounds else [],
            rows=piece.rows if not piece.is_rounds else [],
        )

        # Validate this piece
        validator = StitchCountValidator()
        piece_findings = validator.validate(mini_pattern)

        # Add piece context to findings
        for finding in piece_findings:
            finding.message = f"[{piece.name}] {finding.message}"

        return piece_findings

    def validate_transitions(self, pattern) -> list[ValidationFinding]:
        """
        Validate transitions BETWEEN pieces (optional).

        This is separate from validating within pieces.
        Most patterns don't need this, but some do.
        """
        findings = []

        if not hasattr(pattern, "pieces") or len(pattern.pieces) < 2:
            return findings

        # Check if pieces should connect (e.g., continuous patterns)
        # For most amigurumi, pieces are separate, so no transitions to check

        return findings


def validate_multi_piece(pattern) -> list[ValidationFinding]:
    """Convenience function for multi-piece validation."""
    validator = MultiPieceValidator()
    return validator.validate(pattern)
