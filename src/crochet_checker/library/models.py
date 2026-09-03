"""Data models for pattern library."""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class SavedPattern(BaseModel):
    """A saved pattern in the library."""
    id: str
    title: str
    content: str
    tags: List[str] = []
    category: str = "general"
    difficulty: str = "intermediate"
    notes: str = ""
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    usage_count: int = 0
    favorite: bool = False
