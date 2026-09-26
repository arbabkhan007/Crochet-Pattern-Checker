"""
Engine package - Spatial tracking and state management

Layers (per 4-pattern audit):
  - CanvasQueue (Ring & Linear Buffer)   -> forward-only traversal
  - PostVsHeadLoopTracker                 -> post vs head loop consumption
  - GlobalAnchorGraph                     -> multi-depth lookups across rounds
  - StitchConsumer (Loop State Allocator) -> loop lifecycle states
"""

from .anchor_graph import AnchorNode, AnchorType, GlobalAnchorGraph
from .assembly_graph import AssemblyGraph
from .canvas_queue import (
    BackwardTraversalError,
    CanvasElement,
    CanvasQueue,
    OrphanedStitchError,
    PostVsHeadLoopTracker,
    StitchStatus,
)
from .consumer import StitchConsumer as LoopStateAllocator
from .state_machine import StateMachine
from .stitch_consumer import ConsumptionResult, StitchConsumer

__all__ = [
    # Canvas Queue
    "CanvasQueue",
    "CanvasElement",
    "StitchStatus",
    "BackwardTraversalError",
    "OrphanedStitchError",
    "PostVsHeadLoopTracker",
    # Stitch Consumption
    "StitchConsumer",
    "ConsumptionResult",
    "LoopStateAllocator",
    # State Machine
    "StateMachine",
    # Assembly Graph
    "AssemblyGraph",
    # Anchor Graph
    "GlobalAnchorGraph",
    "AnchorNode",
    "AnchorType",
]
