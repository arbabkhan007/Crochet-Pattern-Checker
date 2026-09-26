from pydantic import BaseModel


class Yarn(BaseModel):
    name: str | None = None
    brand: str | None = None
    color: str | None = None
    weight: str | None = None
    hook_size_mm: float | None = None


class Hook(BaseModel):
    size_mm: float | None = None
    us_size: str | None = None


class Gauge(BaseModel):
    stitches_per_unit: int
    rows_per_unit: int
    unit_size: float = 4.0
    unit: str = "inches"
