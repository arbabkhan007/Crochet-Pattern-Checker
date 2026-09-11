"""Christmas Collection (NS 11, NS 12, NS 13) data package."""
from .x01_gnome import PATTERN as X01
from .x02_tree import PATTERN as X02
from .x03_bundle import PATTERN as X03
from .x04_skirt import PATTERN as X04
from .x05_wreath import PATTERN as X05

PATTERNS = [X01, X02, X03]
NEW = [X04, X05]
BY_ID = {p["id"]: p for p in PATTERNS + NEW}
