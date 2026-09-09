"""Pattern Collection System - Group and organize patterns"""

import json
from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class PatternCollection:
    collection_id: str
    name: str
    description: str
    pattern_ids: List[str]
    tags: List[str]
    created_at: str
    updated_at: str

class PatternCollectionManager:
    """Manage collections of patterns"""
    
    def __init__(self, collections_path: str = "collections"):
        self.collections_path = Path(collections_path)
        self.collections_path.mkdir(parents=True, exist_ok=True)
        self.collections = {}
        self._load_collections()
    
    def _load_collections(self):
        """Load all collections from disk"""
        for file in self.collections_path.glob("*.json"):
            with open(file, 'r') as f:
                data = json.load(f)
                collection = PatternCollection(**data)
                self.collections[collection.collection_id] = collection
    
    def create_collection(self, name: str, description: str = "", pattern_ids: List[str] = None, tags: List[str] = None) -> PatternCollection:
        """Create a new collection"""
        collection_id = f"collection_{hash(name) % 100000}"
        now = datetime.now().isoformat()
        
        collection = PatternCollection(
            collection_id=collection_id,
            name=name,
            description=description,
            pattern_ids=pattern_ids or [],
            tags=tags or [],
            created_at=now,
            updated_at=now
        )
        
        self.collections[collection_id] = collection
        self._save_collection(collection)
        
        return collection
    
    def add_pattern_to_collection(self, collection_id: str, pattern_id: str) -> bool:
        """Add a pattern to a collection"""
        if collection_id not in self.collections:
            return False
        
        collection = self.collections[collection_id]
        if pattern_id not in collection.pattern_ids:
            collection.pattern_ids.append(pattern_id)
            collection.updated_at = datetime.now().isoformat()
            self._save_collection(collection)
        
        return True
    
    def list_collections(self) -> List[PatternCollection]:
        """List all collections"""
        return list(self.collections.values())
    
    def _save_collection(self, collection: PatternCollection):
        """Save a collection to disk"""
        collection_file = self.collections_path / f"{collection.collection_id}.json"
        with open(collection_file, 'w') as f:
            json.dump(asdict(collection), f, indent=2)

def format_collections(collections: List[PatternCollection]) -> str:
    """Format collections for display"""
    if not collections:
        return "No collections found."
    
    output = [
        f"📚 Pattern Collections",
        "=" * 40,
        f"Found {len(collections)} collection(s)\n"
    ]
    
    for collection in collections:
        output.append(f"📁 {collection.name}")
        if collection.description:
            output.append(f"   {collection.description}")
        output.append(f"   Patterns: {len(collection.pattern_ids)}")
        if collection.tags:
            output.append(f"   Tags: {', '.join(collection.tags)}")
        output.append("")
    
    return "\n".join(output)
