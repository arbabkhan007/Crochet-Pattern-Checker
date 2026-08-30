from typing import Optional
from pydantic import BaseModel, Field
class Yarn(BaseModel):
    name: Optional[str] = None; brand: Optional[str] = None; color: Optional[str] = None
    weight: Optional[str] = None; hook_size_mm: Optional[float] = None
class Hook(BaseModel):
    size_mm: Optional[float] = None; us_size: Optional[str] = None
class Gauge(BaseModel):
    stitches_per_unit: int; rows_per_unit: int; unit_size: float = 4.0; unit: str = "inches"
