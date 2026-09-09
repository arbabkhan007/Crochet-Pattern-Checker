"""Novality Store pattern audit pipeline.

Single source of truth for the 10 corrected Novality Store patterns:
the same data drives the deterministic stitch-count audit, the corrected
markdown source files in patterns/, and the final customer PDFs in
final_patterns/.
"""
from . import schema
from .p01_hamish import PATTERN as P01
from .p02_halloween import PATTERN as P02
from .p03_axel import PATTERN as P03
from .p04_coco import PATTERN as P04
from .p05_duck import PATTERN as P05
from .p06_momo import PATTERN as P06
from .p07_trio import PATTERN as P07
from .p08_ember import PATTERN as P08
from .p09_shelby import PATTERN as P09
from .p10_willow import PATTERN as P10

PATTERNS = [P01, P02, P03, P04, P05, P06, P07, P08, P09, P10]
BY_ID = {p["id"]: p for p in PATTERNS}

__all__ = ["schema", "PATTERNS", "BY_ID"]
