"""SQLite-based pattern library."""
import sqlite3
from pathlib import Path
from typing import List, Optional
from datetime import datetime
from .models import SavedPattern

class PatternLibrary:
    """Manage a library of crochet patterns."""
    
    def __init__(self, db_path: str = "patterns.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize the database."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS patterns (
                    id TEXT PRIMARY KEY,
                    title TEXT,
                    content TEXT,
                    tags TEXT,
                    category TEXT,
                    difficulty TEXT,
                    notes TEXT,
                    created_at TEXT,
                    updated_at TEXT,
                    usage_count INTEGER,
                    favorite INTEGER
                )
            """)
    
    def save_pattern(self, pattern: SavedPattern) -> str:
        """Save a pattern to the library."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO patterns
                (id, title, content, tags, category, difficulty, notes, 
                 created_at, updated_at, usage_count, favorite)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                pattern.id, pattern.title, pattern.content,
                ','.join(pattern.tags), pattern.category, pattern.difficulty,
                pattern.notes, pattern.created_at.isoformat(),
                pattern.updated_at.isoformat(), pattern.usage_count,
                1 if pattern.favorite else 0
            ))
        return pattern.id
    
    def get_pattern(self, pattern_id: str) -> Optional[SavedPattern]:
        """Get a pattern by ID."""
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute(
                "SELECT * FROM patterns WHERE id = ?", (pattern_id,)
            ).fetchone()
            
            if row:
                return SavedPattern(
                    id=row[0], title=row[1], content=row[2],
                    tags=row[3].split(',') if row[3] else [],
                    category=row[4], difficulty=row[5], notes=row[6],
                    created_at=datetime.fromisoformat(row[7]),
                    updated_at=datetime.fromisoformat(row[8]),
                    usage_count=row[9], favorite=bool(row[10])
                )
        return None
    
    def list_patterns(self) -> List[SavedPattern]:
        """List all patterns."""
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute("SELECT * FROM patterns").fetchall()
            return [
                SavedPattern(
                    id=row[0], title=row[1], content=row[2],
                    tags=row[3].split(',') if row[3] else [],
                    category=row[4], difficulty=row[5], notes=row[6],
                    created_at=datetime.fromisoformat(row[7]),
                    updated_at=datetime.fromisoformat(row[8]),
                    usage_count=row[9], favorite=bool(row[10])
                )
                for row in rows
            ]
