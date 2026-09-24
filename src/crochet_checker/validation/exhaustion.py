"""
OrphanedStitchAnalyzer (Exhaustion Check)
Inspects the active canvas at the end of each round and raises an OrphanedStitchError 
if base stitches are left unworked without an explicit skip or leave unworked directive.
"""
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

class StitchState(Enum):
    """State of a stitch in the canvas"""
    UNTOUCHED = "untouched"
    WORKED = "worked"
    SKIPPED = "skipped"
    INTENTIONALLY_UNWORKED = "intentionally_unworked"

@dataclass
class CanvasStitch:
    """Represents a stitch in the canvas"""
    stitch_id: str
    round_number: int
    position: int
    state: StitchState = StitchState.UNTOUCHED
    worked_by_round: Optional[int] = None
    skip_directive: Optional[str] = None

@dataclass
class ExhaustionReport:
    """Report of round exhaustion check"""
    round_number: int
    total_stitches: int
    worked_stitches: int
    skipped_stitches: int
    unworked_stitches: List[str]
    intentionally_unworked: List[str]
    is_exhausted: bool
    orphans: List[str]
    warnings: List[str] = field(default_factory=list)

try:
    from ..engine.canvas_queue import OrphanedStitchError as EngineOrphanedStitchError
except ImportError:  # pragma: no cover - run as __main__ demo
    import importlib.util
    from pathlib import Path
    _spec = importlib.util.spec_from_file_location(
        "canvas_queue", Path(__file__).resolve().parents[1] / "engine" / "canvas_queue.py")
    _canvas_mod = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_canvas_mod)
    EngineOrphanedStitchError = _canvas_mod.OrphanedStitchError


def _raise_orphaned_error(round_number: int, orphans: List[str]) -> None:
    """Raise the validation OrphanedStitchError (a subclass of the canonical
    engine error, so `except` on either class works) with structured attributes."""
    err = OrphanedStitchError(
        f"Round {round_number} has {len(orphans)} orphaned stitches: {orphans}"
    )
    err.round_number = round_number
    err.orphans = orphans
    raise err


class OrphanedStitchError(EngineOrphanedStitchError):
    """Validation-facing alias of the canonical engine OrphanedStitchError."""
    pass

class OrphanedStitchAnalyzer:
    """
    Analyzes canvas at end of each round to detect orphaned stitches.
    Ensures all base stitches are properly worked, skipped, or intentionally left.
    """
    
    def __init__(self):
        self.canvas: Dict[str, CanvasStitch] = {}
        self.round_stitches: Dict[int, List[str]] = {}
        self.skip_directives: List[Dict] = []
        self.stitch_counter: int = 0
        
    def add_stitch(self, round_number: int, position: int) -> CanvasStitch:
        """Add a stitch to the canvas"""
        stitch_id = f"r{round_number}_p{position}_{self.stitch_counter}"
        
        stitch = CanvasStitch(
            stitch_id=stitch_id,
            round_number=round_number,
            position=position
        )
        
        self.canvas[stitch_id] = stitch
        
        if round_number not in self.round_stitches:
            self.round_stitches[round_number] = []
        self.round_stitches[round_number].append(stitch_id)
        
        self.stitch_counter += 1
        return stitch
    
    def get_stitch(self, stitch_id: str) -> Optional[CanvasStitch]:
        """Get a stitch by ID"""
        return self.canvas.get(stitch_id)
    
    def get_stitches_in_round(self, round_number: int) -> List[CanvasStitch]:
        """Get all stitches in a round"""
        if round_number not in self.round_stitches:
            return []
        return [self.canvas[sid] for sid in self.round_stitches[round_number]]
    
    def work_stitch(self, stitch_id: str, worked_by_round: int) -> bool:
        """Mark a stitch as worked"""
        stitch = self.get_stitch(stitch_id)
        if not stitch:
            return False
        
        if stitch.state == StitchState.UNTOUCHED:
            stitch.state = StitchState.WORKED
            stitch.worked_by_round = worked_by_round
            return True
        return False
    
    def skip_stitch(self, stitch_id: str, directive: str = "skip") -> bool:
        """Mark a stitch as skipped"""
        stitch = self.get_stitch(stitch_id)
        if not stitch:
            return False
        
        if stitch.state == StitchState.UNTOUCHED:
            stitch.state = StitchState.SKIPPED
            stitch.skip_directive = directive
            return True
        return False
    
    def add_skip_directive(self, round_number: int, positions: List[int], 
                          directive: str) -> None:
        """Add a directive to skip specific positions"""
        self.skip_directives.append({
            "round": round_number,
            "positions": positions,
            "directive": directive
        })
        
        # Mark stitches as intentionally unworked
        for pos in positions:
            stitch = self._get_stitch_at_position(round_number, pos)
            if stitch:
                stitch.state = StitchState.INTENTIONALLY_UNWORKED
                stitch.skip_directive = directive
    
    def _get_stitch_at_position(self, round_number: int, position: int) -> Optional[CanvasStitch]:
        """Get stitch at specific position in round"""
        for stitch_id in self.round_stitches.get(round_number, []):
            stitch = self.canvas[stitch_id]
            if stitch.position == position:
                return stitch
        return None
    
    def analyze_exhaustion(self, round_number: int, raise_on_orphans: bool = True) -> ExhaustionReport:
        """
        Analyze if a round is exhausted (all stitches accounted for).
        
        Args:
            round_number: The round to analyze
            raise_on_orphans: If True, raises OrphanedStitchError when orphans found
            
        Returns:
            ExhaustionReport with analysis results
        """
        stitches = self.get_stitches_in_round(round_number)
        
        worked = []
        skipped = []
        unworked = []
        intentionally_unworked = []
        
        for stitch in stitches:
            if stitch.state == StitchState.WORKED:
                worked.append(stitch.stitch_id)
            elif stitch.state == StitchState.SKIPPED:
                skipped.append(stitch.stitch_id)
            elif stitch.state == StitchState.INTENTIONALLY_UNWORKED:
                intentionally_unworked.append(stitch.stitch_id)
            elif stitch.state == StitchState.UNTOUCHED:
                unworked.append(stitch.stitch_id)
        
        # Orphans are unworked stitches without a skip directive
        orphans = unworked.copy()
        
        # Generate warnings
        warnings = []
        if len(orphans) > 0:
            warnings.append(f"Found {len(orphans)} orphaned stitches")
        
        if len(skipped) > len(stitches) * 0.5:
            warnings.append(f"More than 50% of stitches were skipped ({len(skipped)}/{len(stitches)})")
        
        report = ExhaustionReport(
            round_number=round_number,
            total_stitches=len(stitches),
            worked_stitches=len(worked),
            skipped_stitches=len(skipped),
            unworked_stitches=unworked,
            intentionally_unworked=intentionally_unworked,
            is_exhausted=len(orphans) == 0,
            orphans=orphans,
            warnings=warnings
        )
        
        if raise_on_orphans and not report.is_exhausted:
            _raise_orphaned_error(round_number, orphans)
        
        return report
    
    def analyze_all_rounds(self, raise_on_orphans: bool = False) -> Dict[int, ExhaustionReport]:
        """Analyze exhaustion for all rounds"""
        reports = {}
        for round_number in sorted(self.round_stitches.keys()):
            try:
                reports[round_number] = self.analyze_exhaustion(round_number, raise_on_orphans)
            except OrphanedStitchError:
                # If raise_on_orphans is True, this will be caught
                # If False, we already got the report
                pass
        return reports
    
    def get_round_summary(self, round_number: int) -> Dict:
        """Get summary of a specific round"""
        stitches = self.get_stitches_in_round(round_number)
        
        state_counts = {}
        for state in StitchState:
            count = len([s for s in stitches if s.state == state])
            state_counts[state.value] = count
        
        return {
            "round": round_number,
            "total_stitches": len(stitches),
            "state_counts": state_counts,
            "worked": state_counts.get("worked", 0),
            "skipped": state_counts.get("skipped", 0),
            "intentionally_unworked": state_counts.get("intentionally_unworked", 0),
            "orphans": state_counts.get("untouched", 0)
        }
    
    def validate_pattern(self) -> List[str]:
        """
        Validate entire pattern for orphaned stitches.
        Returns list of validation errors.
        """
        errors = []
        
        for round_number in sorted(self.round_stitches.keys()):
            try:
                report = self.analyze_exhaustion(round_number, raise_on_orphans=False)
                if not report.is_exhausted:
                    errors.append(
                        f"Round {round_number}: {len(report.orphans)} orphaned stitches"
                    )
            except Exception as e:
                errors.append(f"Round {round_number}: {str(e)}")
        
        return errors
    
    def reset(self) -> None:
        """Reset the analyzer"""
        self.canvas.clear()
        self.round_stitches.clear()
        self.skip_directives.clear()
        self.stitch_counter = 0

# Example usage
if __name__ == "__main__":
    analyzer = OrphanedStitchAnalyzer()
    
    # Simulate Round 1: 6 sc, work all
    print("Round 1: 6 sc (work all)")
    round1_stitches = []
    for i in range(6):
        stitch = analyzer.add_stitch(1, i)
        round1_stitches.append(stitch.stitch_id)
    
    # Work all stitches
    for stitch_id in round1_stitches:
        analyzer.work_stitch(stitch_id, 1)
    
    # Check exhaustion
    report = analyzer.analyze_exhaustion(1, raise_on_orphans=False)
    print(f"✅ Round 1 exhausted: {report.is_exhausted}")
    print(f"   Worked: {report.worked_stitches}/{report.total_stitches}")
    
    # Simulate Round 2: 6 sc, skip 2 with directive
    print("\nRound 2: 6 sc (skip positions 2,3 with directive)")
    round2_stitches = []
    for i in range(6):
        stitch = analyzer.add_stitch(2, i)
        round2_stitches.append(stitch.stitch_id)
    
    # Add skip directive
    analyzer.add_skip_directive(2, [2, 3], "skip 2 sts")
    
    # Work remaining stitches
    for i, stitch_id in enumerate(round2_stitches):
        if i not in [2, 3]:
            analyzer.work_stitch(stitch_id, 2)
    
    # Check exhaustion
    report = analyzer.analyze_exhaustion(2, raise_on_orphans=False)
    print(f"✅ Round 2 exhausted: {report.is_exhausted}")
    print(f"   Worked: {report.worked_stitches}, Intentionally unworked: {len(report.intentionally_unworked)}")
    
    # Simulate Round 3: Orphaned stitches (error case)
    print("\nRound 3: 6 sc (leave 2 orphaned - ERROR)")
    round3_stitches = []
    for i in range(6):
        stitch = analyzer.add_stitch(3, i)
        round3_stitches.append(stitch.stitch_id)
    
    # Only work 4 stitches
    for stitch_id in round3_stitches[:4]:
        analyzer.work_stitch(stitch_id, 3)
    
    # Check exhaustion (should fail)
    try:
        report = analyzer.analyze_exhaustion(3, raise_on_orphans=True)
        print(f"✅ Round 3 exhausted: {report.is_exhausted}")
    except OrphanedStitchError as e:
        print(f"❌ {e}")
    
    # Get summaries
    print(f"\nRound 1 summary: {analyzer.get_round_summary(1)}")
    print(f"Round 2 summary: {analyzer.get_round_summary(2)}")
    print(f"Round 3 summary: {analyzer.get_round_summary(3)}")
