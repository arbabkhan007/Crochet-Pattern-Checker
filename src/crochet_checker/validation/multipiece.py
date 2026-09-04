"""Multi-piece pattern detection and validation."""
from typing import List, Dict, Tuple
import re

class MultiPieceDetector:
    """Detect and separate multi-piece patterns."""
    
    def __init__(self):
        self.piece_markers = [
            r'#{1,3}\s*\d+\.',  # ### 1. Head
            r'#{1,3}\s*[A-Z][a-z]+',  # ### Head
            r'\*\*Section \d+',  # **Section 1
            r'\b(Head|Body|Tail|Legs|Arms|Wings|Snout|Horns)\b.*:',
        ]
    
    def detect_pieces(self, pattern_text: str) -> List[Dict]:
        """Detect separate pieces in a pattern."""
        lines = pattern_text.split('\n')
        pieces = []
        current_piece = None
        current_lines = []
        
        for line in lines:
            # Check if this line starts a new piece
            is_new_piece = False
            for marker in self.piece_markers:
                if re.search(marker, line, re.IGNORECASE):
                    is_new_piece = True
                    break
            
            if is_new_piece and current_lines:
                # Save previous piece
                if current_piece:
                    pieces.append({
                        'name': current_piece,
                        'content': '\n'.join(current_lines)
                    })
                
                # Start new piece
                current_piece = line.strip('#').strip('*').strip()
                current_lines = [line]
            elif current_piece:
                current_lines.append(line)
        
        # Save last piece
        if current_piece and current_lines:
            pieces.append({
                'name': current_piece,
                'content': '\n'.join(current_lines)
            })
        
        return pieces
    
    def validate_pieces(self, pieces: List[Dict]) -> Dict:
        """Validate each piece separately."""
        from ..parser import parse_pattern
        from ..validation import validate_pattern
        
        results = []
        
        for piece in pieces:
            try:
                pattern = parse_pattern(piece['content'])
                report = validate_pattern(pattern)
                
                results.append({
                    'name': piece['name'],
                    'status': report.status.value,
                    'score': report.overall_score,
                    'errors': len(report.errors),
                    'warnings': len(report.warnings),
                    'rounds': len(pattern.rounds or pattern.rows)
                })
            except Exception as e:
                results.append({
                    'name': piece['name'],
                    'status': 'ERROR',
                    'score': 0,
                    'errors': 1,
                    'warnings': 0,
                    'error_message': str(e)
                })
        
        return {
            'total_pieces': len(pieces),
            'pieces': results,
            'overall_status': 'PASS' if all(r['status'] == 'PASS' for r in results) else 'PASS_WITH_WARNINGS'
        }

def detect_and_validate_multipiece(pattern_text: str) -> Dict:
    """Detect pieces and validate each separately."""
    detector = MultiPieceDetector()
    pieces = detector.detect_pieces(pattern_text)
    
    if len(pieces) > 1:
        return detector.validate_pieces(pieces)
    else:
        return {'total_pieces': 1, 'pieces': [], 'message': 'Single piece pattern'}
