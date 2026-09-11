"""Christmas Collection (NS 11, NS 12, NS 13) data package."""
from .x01_gnome import PATTERN as X01
from .x02_tree import PATTERN as X02
from .x03_bundle import PATTERN as X03

PATTERNS = [X01, X02, X03]
BY_ID = {p["id"]: p for p in PATTERNS}
