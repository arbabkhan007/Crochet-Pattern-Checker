"""
Engine package - Spatial tracking and state management

Layers (per 4-pattern audit):
  - CanvasQueue (Ring & Linear Buffer)   -> forward-only traversal
  - PostVsHeadLoopTracker                 -> post vs head loop consumption
  - GlobalAnchorGraph                     -> multi-depth lookups across rounds
  - StitchConsumer (Loop State Allocator) -> loop lifecycle states
"""

from .canvas_queue import (
    CanvasQueue,
    CanvasElement,
    StitchStatus,
    BackwardTraversalError,
    OrphanedStitchError,
    PostVsHeadLoopTracker,
)
from .stitch_consumer import StitchConsumer, ConsumptionResult
from .consumer import StitchConsumer as LoopStateAllocator
from .state_machine import StateMachine
from .assembly_graph import AssemblyGraph
from .anchor_graph import GlobalAnchorGraph, AnchorNode, AnchorType

__all__ = [
    # Canvas Queue
    'CanvasQueue',
    'CanvasElement',
    'StitchStatus',
    'BackwardTraversalError',
    'OrphanedStitchError',
    'PostVsHeadLoopTracker',
    # Stitch Consumption
    'StitchConsumer',
    'ConsumptionResult',
    'LoopStateAllocator',
    # State Machine
    'StateMachine',
    # Assembly Graph
    'AssemblyGraph',
    # Anchor Graph
    'GlobalAnchorGraph',
    'AnchorNode',
    'AnchorType',
]
