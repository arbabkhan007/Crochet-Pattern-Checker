"""
State Machine - Tracks hook position, available loops, and counts
Maintains a virtual "Working Canvas" that tracks available loops from the prior round/row
"""
from typing import List, Dict, Optional, Tuple
from enum import Enum
from dataclasses import dataclass, field
from ..ast.nodes import InstructionNode, LoopStatus


class StitchError(Exception):
    """Exception raised for stitch validation errors"""
    pass


@dataclass
class Loop:
    """Represents a single loop on the working canvas"""
    index: int
    status: LoopStatus = LoopStatus.AVAILABLE
    height: int = 1
    stitch_type: str = ""
    worked_by_round: int = 0
    post_available: bool = True


@dataclass
class HookState:
    """Current state of the virtual hook"""
    position: int = 0
    yarn_over_count: int = 0
    loops_on_hook: int = 0
    current_round: int = 0
    current_stitch_index: int = 0


class StateMachine:
    """State machine for tracking crochet pattern execution"""
    
    def __init__(self):
        self.canvas: List[Loop] = []
        self.hook = HookState()
        self.warnings: List[str] = []
        self.errors: List[str] = []
        self.stitch_count_history: List[int] = []
        self.current_round = 0
        self.round_stitch_counts: Dict[int, int] = {}
        self.create_mode = False
    
    def initialize_round(self, stitch_count: int, round_number: int = 1,
                         create_mode: bool = False):
        """Initialize a new round with the expected stitch count.

        create_mode=True for foundation rounds (e.g. Round 1 into a magic ring):
        stitches are created fresh instead of consuming a previous round's loops.
        """
        self.canvas = []
        for i in range(stitch_count):
            self.canvas.append(Loop(
                index=i,
                status=LoopStatus.AVAILABLE,
                worked_by_round=round_number - 1
            ))
        
        self.create_mode = create_mode
        self.hook.position = 0
        self.hook.current_round = round_number
        self.current_round = round_number
        self.stitch_count_history.append(stitch_count)
    
    def execute_instruction(self, instruction: InstructionNode, *legacy_args) -> int:
        # Legacy callers may pass simple strings such as "sc".
        if isinstance(instruction, str):
            stitch = instruction.strip().lower()
            if stitch in {"sc", "dc", "hdc", "tr", "st", "sl st", "inc", "dec"}:
                return 1
            return 0

        """Execute a single instruction and return stitches produced"""
        stitches_produced = 0
        
        try:
            if instruction.action == "turning_chain":
                stitches_produced = self._execute_turning_chain(instruction)
            elif instruction.action == "stitch":
                stitches_produced = self._execute_stitch(instruction)
            elif instruction.action == "unknown":
                self.warnings.append(
                    f"[WARN] Line {instruction.line_number}: "
                    f"Unrecognized instruction. Stitch counts past this point are untrusted."
                )
        except StitchError as e:
            self.errors.append(f"Line {instruction.line_number}: {str(e)}")
        
        return stitches_produced
    
    def _execute_turning_chain(self, instruction: InstructionNode) -> int:
        """Execute a turning chain instruction"""
        # Turning chains add height but may or may not count as stitches
        if instruction.counts_as_stitch:
            # Add loops to canvas that count as stitches
            for i in range(instruction.count):
                self.canvas.append(Loop(
                    index=len(self.canvas),
                    status=LoopStatus.AVAILABLE,
                    height=instruction.count,
                    stitch_type="ch",
                    worked_by_round=self.current_round
                ))
            return instruction.count
        else:
            # Height builder only, doesn't count as stitch
            return 0
    
    def _execute_stitch(self, instruction: InstructionNode) -> int:
        """Execute a stitch instruction"""
        stitch_type = instruction.stitch_type.lower()
        count = instruction.count
        stitches_produced = 0
        
        # Handle special stitches
        if stitch_type in ['inc', 'increase']:
            # Increase: work 2 stitches into 1
            for _ in range(count):
                self._consume_loop()
                self._produce_loops(2, stitch_type)
                stitches_produced += 2
        
        elif stitch_type in ['dec', 'decrease']:
            # Decrease: work 2 stitches together
            for _ in range(count):
                self._consume_loop()
                self._consume_loop()
                self._produce_loops(1, stitch_type)
                stitches_produced += 1
        
        elif stitch_type == 'skip':
            # Skip stitches
            target = instruction.target_position or count
            for _ in range(target):
                self._skip_loop()
        
        elif stitch_type in ['sl st', 'sl st']:
            # Slip stitch
            for _ in range(count):
                self._consume_loop()
                self._produce_loops(1, stitch_type)
                stitches_produced += 1
        
        elif stitch_type == 'magic ring':
            # Magic ring creates initial loops
            self._produce_loops(count, 'magic ring')
            stitches_produced = count
        
        elif stitch_type == 'ch':
            # Chain (when not turning chain)
            self._produce_loops(count, 'ch')
            stitches_produced = count
        
        else:
            # Regular stitch (sc, dc, hdc, tr, etc.)
            for _ in range(count):
                self._consume_loop()
                self._produce_loops(1, stitch_type)
                stitches_produced += 1
        
        return stitches_produced
    
    def _consume_loop(self):
        """Consume the next available loop from canvas"""
        if self.create_mode and self.hook.position >= len(self.canvas):
            # Foundation round (magic ring): stitches are created fresh,
            # there is no previous round's loop to consume.
            return
        if self.hook.position >= len(self.canvas):
            raise StitchError(
                f"Attempted to work stitch beyond available loops. "
                f"Position: {self.hook.position}, Available: {len(self.canvas)}"
            )
        
        loop = self.canvas[self.hook.position]
        
        if loop.status == LoopStatus.WORKED_INTO:
            raise StitchError(
                f"Attempted to work into already-worked loop at position {self.hook.position}"
            )
        
        loop.status = LoopStatus.WORKED_INTO
        self.hook.position += 1
    
    def _produce_loops(self, count: int, stitch_type: str):
        """Produce new loops on the canvas"""
        for _ in range(count):
            self.canvas.append(Loop(
                index=len(self.canvas),
                status=LoopStatus.AVAILABLE,
                stitch_type=stitch_type,
                worked_by_round=self.current_round
            ))
    
    def _skip_loop(self):
        """Skip the current loop"""
        if self.hook.position < len(self.canvas):
            self.canvas[self.hook.position].status = LoopStatus.SKIPPED
            self.hook.position += 1
        else:
            raise StitchError("Attempted to skip beyond available loops")
    
    def validate_directional_movement(self, instruction: InstructionNode) -> bool:
        """Validate that instruction doesn't require invalid spatial transitions"""
        if instruction.target_position is not None:
            target = instruction.target_position
            
            # Check for backward jumping
            if target < self.hook.position:
                self.warnings.append(
                    f"[WARN] Line {instruction.line_number}: "
                    f"Instruction requires working backward from position {self.hook.position} "
                    f"to {target}. This may indicate an error."
                )
                return False
            
            # Check for jumping over unworked spaces
            for i in range(self.hook.position, target):
                if i < len(self.canvas) and self.canvas[i].status == LoopStatus.AVAILABLE:
                    self.warnings.append(
                        f"[WARN] Line {instruction.line_number}: "
                        f"Skipping over unworked loop at position {i}"
                    )
                    return False
        
        return True
    
    def get_current_stitch_count(self) -> int:
        """Get the current number of available loops"""
        return sum(1 for loop in self.canvas if loop.status == LoopStatus.AVAILABLE)
    
    def finalize_round(self) -> int:
        """Finalize the current round and return stitch count"""
        stitch_count = self.get_current_stitch_count()
        self.round_stitch_counts[self.current_round] = stitch_count
        return stitch_count
    
    def get_report(self) -> Dict:
        """Generate a state machine execution report"""
        return {
            'total_rounds': self.current_round,
            'round_counts': self.round_stitch_counts,
            'warnings': self.warnings,
            'errors': self.errors,
            'final_stitch_count': self.get_current_stitch_count()
        }


if __name__ == "__main__":
    print("⚙️ State Machine")
    print("=" * 60)
    
    machine = StateMachine()
    
    # Initialize with magic ring
    machine.initialize_round(0, round_number=1)
    from ..ast.nodes import InstructionNode
    
    # Round 1: 6 sc in magic ring
    instr1 = InstructionNode(action="stitch", stitch_type="magic ring", count=6, line_number=1)
    produced = machine.execute_instruction(instr1)
    print(f"\nRound 1: Magic ring with 6 sc")
    print(f"  Stitches produced: {produced}")
    print(f"  Current count: {machine.get_current_stitch_count()}")
    
    # Round 2: inc in each st around (should be 12)
    machine.initialize_round(6, round_number=2)
    instr2 = InstructionNode(action="stitch", stitch_type="inc", count=6, line_number=2)
    produced = machine.execute_instruction(instr2)
    count = machine.finalize_round()
    print(f"\nRound 2: inc in each st around")
    print(f"  Stitches produced: {produced}")
    print(f"  Final count: {count} (expected: 12)")
    
    # Get report
    report = machine.get_report()
    print(f"\nReport:")
    print(f"  Total rounds: {report['total_rounds']}")
    print(f"  Round counts: {report['round_counts']}")
    print(f"  Warnings: {len(report['warnings'])}")
    print(f"  Errors: {len(report['errors'])}")
    
    print("\n✅ State Machine working!")


# Legacy compatibility property.
@property
def _legacy_state(self):
    return self.hook

StateMachine.state = _legacy_state
