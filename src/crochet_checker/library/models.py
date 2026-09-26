"""Data models for pattern library."""

from datetime import datetime

from pydantic import BaseModel


class SavedPattern(BaseModel):
    """A saved pattern in the library."""

    id: str
    title: str
    content: str
    tags: list[str] = []
    category: str = "general"
    difficulty: str = "intermediate"
    notes: str = ""
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    usage_count: int = 0
    favorite: bool = False
