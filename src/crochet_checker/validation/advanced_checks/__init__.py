"""Conservative deterministic checks for advanced crochet constructions.

All text adapters require explicit evidence. Missing measurements, directions,
or stitch locations remain unknown rather than being estimated. These rules
are separate from the optional provider/LLM integrations.
"""

from __future__ import annotations

from .anatomy import (
    TorsoAxis,
    anatomy_findings,
    check_anatomical_attachment,
    detect_torso_axes,
    normalized_anatomical_height,
)
from .assembly import (
    AssemblyStep,
    ConstructionMode,
    assembly_findings,
    classify_construction_mode,
    parse_numbered_assembly_steps,
)
from .common import AdvancedFinding, meaningful_text, unique_findings
from .curvature import check_flat_curvature, curvature_findings
from .inserts import check_folded_tube_closure, check_insert_diameter, insert_findings
from .inventory import inventory_findings, validate_bom_and_stuffing_sanity
from .loop_occupancy import (
    RoundLoopState,
    build_loop_states,
    check_surface_loop_join,
    color_crease_findings,
    loop_occupancy_findings,
)
from .oval_chain import ChainWork, oval_findings, validate_oval_foundation
from .spatial import (
    FeatureBounds,
    attachment_bounds_from_text,
    find_spatial_collisions,
    quadruped_compass_findings,
    quadruped_findings_from_text,
    seam_stretch_mismatch,
    spatial_findings,
    stitch_to_angle,
)
from .turned_rows import (
    RowOrientation,
    RowProfile,
    annotate_row_turns,
    turned_row_findings,
)


def find_advanced_findings(text: str) -> list[AdvancedFinding]:
    """Run the requested rule families against written text and explicit quantities."""
    source = meaningful_text(text)
    findings: list[AdvancedFinding] = []
    findings.extend(oval_findings(source))
    findings.extend(loop_occupancy_findings(source))
    findings.extend(turned_row_findings(source))
    findings.extend(spatial_findings(source))
    findings.extend(quadruped_findings_from_text(source))
    findings.extend(anatomy_findings(source))
    findings.extend(curvature_findings(source))
    findings.extend(insert_findings(source))
    findings.extend(inventory_findings(source))
    findings.extend(assembly_findings(source))
    return unique_findings(findings)


__all__ = [
    "AdvancedFinding",
    "AssemblyStep",
    "ChainWork",
    "ConstructionMode",
    "FeatureBounds",
    "RowOrientation",
    "RowProfile",
    "RoundLoopState",
    "TorsoAxis",
    "anatomy_findings",
    "annotate_row_turns",
    "assembly_findings",
    "attachment_bounds_from_text",
    "build_loop_states",
    "check_anatomical_attachment",
    "check_flat_curvature",
    "check_folded_tube_closure",
    "check_insert_diameter",
    "check_surface_loop_join",
    "classify_construction_mode",
    "color_crease_findings",
    "curvature_findings",
    "detect_torso_axes",
    "find_advanced_findings",
    "find_spatial_collisions",
    "insert_findings",
    "inventory_findings",
    "loop_occupancy_findings",
    "normalized_anatomical_height",
    "oval_findings",
    "parse_numbered_assembly_steps",
    "quadruped_compass_findings",
    "quadruped_findings_from_text",
    "seam_stretch_mismatch",
    "spatial_findings",
    "stitch_to_angle",
    "turned_row_findings",
    "unique_findings",
    "validate_bom_and_stuffing_sanity",
    "validate_oval_foundation",
]
