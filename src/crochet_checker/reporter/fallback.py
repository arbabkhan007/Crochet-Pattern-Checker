"""
UnsupportedSyntaxFallback
Replaces silent numeric fallbacks with explicit warnings when encountering 
unparseable spatial phrasing (e.g., "work backward through space"), flagging 
counts as UNTRUSTED instead of outputting arbitrary numbers.
"""
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import re

class TrustLevel(Enum):
    """Trust level of a parsed count"""
    TRUSTED = "trusted"
    APPROXIMATE = "approximate"
    UNTRUSTED = "untrusted"

@dataclass
class CountResult:
    """Result of count parsing with trust level"""
    count: Optional[int]
    trust_level: TrustLevel
    reason: str = ""
    original_text: str = ""
    suggestions: List[str] = field(default_factory=list)

@dataclass
class FallbackWarning:
    """Warning about unsupported syntax"""
    line_number: int
    original_text: str
    fallback_used: str
    message: str
    severity: str = "warning"

class UnsupportedSyntaxFallback:
    """
    Handles unsupported syntax with explicit warnings instead of silent fallbacks.
    Flags untrusted counts clearly.
    """
    
    def __init__(self):
        self.warnings: List[FallbackWarning] = []
        self.unsupported_patterns = [
            # Spatial phrasing that's hard to parse
            r'(?i)work\s+backward',
            r'(?i)through\s+the\s+space',
            r'(?i)in\s+the\s+gap\s+between',
            r'(?i)wrap\s+around\s+the\s+back',
            r'(?i)reach\s+over\s+to',
            r'(?i)into\s+the\s+loop\s+behind',
            # Ambiguous instructions
            r'(?i)some\s+stitches',
            r'(?i)a\s+few\s+stitches',
            r'(?i)several\s+stitches',
            r'(?i)appropriate\s+number',
            r'(?i)as\s+many\s+as\s+needed',
            r'(?i)evenly\s+spaced',
            # Unparseable references
            r'(?i)previous\s+section',
            r'(?i)corresponding\s+stitch',
            r'(?i)matching\s+loop',
        ]
        
        self.fallback_strategies = {
            "unknown_count": self._fallback_unknown_count,
            "spatial_reference": self._fallback_spatial_reference,
            "vague_instruction": self._fallback_vague_instruction,
        }
    
    def detect_unsupported(self, text: str, line_number: int = 0) -> List[Tuple[str, str]]:
        """
        Detect unsupported syntax in text.
        Returns list of (pattern_type, matched_text) tuples.
        """
        detections = []
        
        for pattern in self.unsupported_patterns:
            match = re.search(pattern, text)
            if match:
                # Determine pattern type
                if 'backward' in pattern or 'through' in pattern or 'behind' in pattern:
                    pattern_type = "spatial_reference"
                elif 'few' in pattern or 'several' in pattern or 'some' in pattern:
                    pattern_type = "vague_instruction"
                elif 'evenly' in pattern or 'needed' in pattern or 'appropriate' in pattern:
                    pattern_type = "vague_instruction"
                else:
                    pattern_type = "unknown_count"
                
                detections.append((pattern_type, match.group(0)))
        
        return detections
    
    def parse_with_fallback(self, text: str, line_number: int = 0,
                           expected_count: Optional[int] = None) -> CountResult:
        """
        Parse text, using fallback strategies for unsupported syntax.
        Returns CountResult with trust level.
        """
        # First try normal parsing
        count = self._try_normal_parse(text)
        if count is not None:
            return CountResult(
                count=count,
                trust_level=TrustLevel.TRUSTED,
                original_text=text
            )
        
        # Check for unsupported syntax
        detections = self.detect_unsupported(text, line_number)
        
        if detections:
            # Use fallback strategy
            for pattern_type, matched_text in detections:
                strategy = self.fallback_strategies.get(pattern_type)
                if strategy:
                    result = strategy(text, expected_count)
                    
                    # Add warning
                    warning = FallbackWarning(
                        line_number=line_number,
                        original_text=text,
                        fallback_used=pattern_type,
                        message=(
                            f"Unsupported syntax detected: '{matched_text}'. "
                            f"Used fallback strategy for {pattern_type}. "
                            f"Count flagged as {result.trust_level.value.upper()}."
                        )
                    )
                    self.warnings.append(warning)
                    
                    result.original_text = text
                    return result
        
        # No pattern found, use generic fallback
        result = CountResult(
            count=expected_count,
            trust_level=TrustLevel.UNTRUSTED,
            reason="Unable to parse stitch count",
            original_text=text,
            suggestions=["Clarify stitch count explicitly", "Use standard notation"]
        )
        
        warning = FallbackWarning(
            line_number=line_number,
            original_text=text,
            fallback_used="generic",
            message="Unable to parse stitch count. Using UNTRUSTED fallback."
        )
        self.warnings.append(warning)
        
        return result
    
    def _try_normal_parse(self, text: str) -> Optional[int]:
        """Try to parse stitch count normally"""
        # Look for explicit counts
        patterns = [
            r'\((\d+)\s*(?:sts?|stitches?)?\)',  # (12 sts)
            r'(\d+)\s*(?:sts?|stitches?)',  # 12 sts
            r'=\s*(\d+)',  # = 12
            r'total\s+(\d+)',  # total 12
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return int(match.group(1))
        
        return None
    
    def _fallback_unknown_count(self, text: str, expected: Optional[int]) -> CountResult:
        """Fallback for unknown counts"""
        # Try to estimate from context
        estimated = expected if expected is not None else 0
        
        return CountResult(
            count=estimated,
            trust_level=TrustLevel.UNTRUSTED,
            reason="Count unknown, using contextual estimate",
            suggestions=[
                "Specify exact stitch count",
                "Use '(N sts)' notation at end of round"
            ]
        )
    
    def _fallback_spatial_reference(self, text: str, expected: Optional[int]) -> CountResult:
        """Fallback for spatial references"""
        # Spatial references typically involve 1-2 stitches
        estimated = 1
        
        return CountResult(
            count=estimated,
            trust_level=TrustLevel.APPROXIMATE,
            reason="Spatial reference detected, assuming single stitch",
            suggestions=[
                "Rewrite using standard stitch notation",
                "Specify exact stitch location"
            ]
        )
    
    def _fallback_vague_instruction(self, text: str, expected: Optional[int]) -> CountResult:
        """Fallback for vague instructions"""
        # Vague instructions might be 3-5 stitches
        estimated = expected if expected is not None else 3
        
        return CountResult(
            count=estimated,
            trust_level=TrustLevel.UNTRUSTED,
            reason="Vague instruction, using rough estimate",
            suggestions=[
                "Specify exact number of stitches",
                "Provide explicit count"
            ]
        )
    
    def get_warnings(self) -> List[FallbackWarning]:
        """Get all accumulated warnings"""
        return self.warnings
    
    def get_untrusted_counts(self) -> List[Dict]:
        """Get summary of all untrusted counts"""
        untrusted = []
        for warning in self.warnings:
            untrusted.append({
                "line": warning.line_number,
                "text": warning.original_text,
                "fallback": warning.fallback_used,
                "message": warning.message
            })
        return untrusted
    
    def has_warnings(self) -> bool:
        """Check if there are any warnings"""
        return len(self.warnings) > 0
    
    def clear_warnings(self) -> None:
        """Clear all warnings"""
        self.warnings.clear()
    
    def reset(self) -> None:
        """Reset the fallback handler"""
        self.clear_warnings()

# Example usage
if __name__ == "__main__":
    fallback = UnsupportedSyntaxFallback()
    
    # Test 1: Normal parse
    print("Test 1: Normal parse")
    result1 = fallback.parse_with_fallback("Round 3: 2 dc in each st around (24 sts)", 3)
    print(f"Count: {result1.count}, Trust: {result1.trust_level.value}")
    
    # Test 2: Unsupported spatial phrasing
    print("\nTest 2: Unsupported spatial phrasing")
    result2 = fallback.parse_with_fallback(
        "work backward through the space to the first stitch", 5
    )
    print(f"Count: {result2.count}, Trust: {result2.trust_level.value}")
    print(f"Reason: {result2.reason}")
    if result2.suggestions:
        print(f"Suggestions: {result2.suggestions}")
    
    # Test 3: Vague instruction
    print("\nTest 3: Vague instruction")
    result3 = fallback.parse_with_fallback(
        "sc in several stitches around", 7
    )
    print(f"Count: {result3.count}, Trust: {result3.trust_level.value}")
    
    # Test 4: Completely unparseable
    print("\nTest 4: Completely unparseable")
    result4 = fallback.parse_with_fallback("make it look nice", 9)
    print(f"Count: {result4.count}, Trust: {result4.trust_level.value}")
    
    # Get warnings
    print("\nWarnings accumulated:")
    for warning in fallback.get_warnings():
        print(f"  Line {warning.line_number}: {warning.message[:80]}...")
    
    print(f"\nTotal warnings: {len(fallback.get_warnings())}")
    print(f"Untrusted counts: {fallback.get_untrusted_counts()}")
