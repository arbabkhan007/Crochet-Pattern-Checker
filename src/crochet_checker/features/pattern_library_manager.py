"""Enhanced Pattern Library Manager"""

import json
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class Pattern:
    pattern_id: str
    title: str
    content: str
    tags: List[str]
    category: str
    difficulty: str
    created_at: str
    updated_at: str
    file_path: str = ""
    notes: str = ""

class EnhancedPatternLibrary:
    """Complete pattern library management system"""
    
    def __init__(self, library_path: str = "pattern_library"):
        self.library_path = Path(library_path)
        self.library_path.mkdir(parents=True, exist_ok=True)
        self.patterns = {}
        self._load_patterns()
    
    def _load_patterns(self):
        """Load all patterns from disk"""
        for file in self.library_path.glob("*.json"):
            try:
                with open(file, 'r') as f:
                    data = json.load(f)
                    pattern = Pattern(**data)
                    self.patterns[pattern.pattern_id] = pattern
            except Exception:
                pass
    
    def add_pattern(self, title: str, content: str, tags: List[str] = None, 
                   category: str = "general", difficulty: str = "intermediate",
                   file_path: str = "", notes: str = "") -> Pattern:
        """Add a new pattern to the library"""
        pattern_id = f"pattern_{hash(f'{title}{datetime.now()}') % 1000000}"
        now = datetime.now().isoformat()
        
        pattern = Pattern(
            pattern_id=pattern_id,
            title=title,
            content=content,
            tags=tags or [],
            category=category,
            difficulty=difficulty,
            created_at=now,
            updated_at=now,
            file_path=file_path,
            notes=notes
        )
        
        self.patterns[pattern_id] = pattern
        self._save_pattern(pattern)
        
        return pattern
    
    def list_patterns(self, category: str = None, difficulty: str = None) -> List[Pattern]:
        """List patterns with optional filters"""
        patterns = list(self.patterns.values())
        
        if category:
            patterns = [p for p in patterns if p.category == category]
        if difficulty:
            patterns = [p for p in patterns if p.difficulty == difficulty]
        
        return patterns
    
    def search_patterns(self, query: str) -> List[Pattern]:
        """Search patterns by title, content, or tags"""
        query_lower = query.lower()
        results = []
        
        for pattern in self.patterns.values():
            if (query_lower in pattern.title.lower() or
                query_lower in pattern.content.lower() or
                any(query_lower in tag.lower() for tag in pattern.tags)):
                results.append(pattern)
        
        return results
    
    def get_statistics(self) -> Dict:
        """Get library statistics"""
        patterns = list(self.patterns.values())
        
        if not patterns:
            return {"total_patterns": 0, "categories": {}, "difficulties": {}, "total_tags": 0}
        
        categories = {}
        difficulties = {}
        all_tags = set()
        
        for pattern in patterns:
            categories[pattern.category] = categories.get(pattern.category, 0) + 1
            difficulties[pattern.difficulty] = difficulties.get(pattern.difficulty, 0) + 1
            all_tags.update(pattern.tags)
        
        return {
            "total_patterns": len(patterns),
            "categories": categories,
            "difficulties": difficulties,
            "total_tags": len(all_tags)
        }
    
    def _save_pattern(self, pattern: Pattern):
        """Save a pattern to disk"""
        pattern_file = self.library_path / f"{pattern.pattern_id}.json"
        with open(pattern_file, 'w') as f:
            json.dump(asdict(pattern), f, indent=2)

def format_pattern_list(patterns: List[Pattern]) -> str:
    """Format pattern list for display"""
    if not patterns:
        return "No patterns found."
    
    output = [
        f"📚 Pattern Library",
        "=" * 40,
        f"Found {len(patterns)} pattern(s)\n"
    ]
    
    for i, pattern in enumerate(patterns, 1):
        output.append(f"{i}. {pattern.title}")
        output.append(f"   Category: {pattern.category} | Difficulty: {pattern.difficulty}")
        if pattern.tags:
            output.append(f"   Tags: {', '.join(pattern.tags[:5])}")
        output.append("")
    
    return "\n".join(output)

def format_library_stats(stats: Dict) -> str:
    """Format library statistics for display"""
    output = [
        f"📊 Pattern Library Statistics",
        "=" * 40,
        f"Total Patterns: {stats['total_patterns']}",
        f"Total Tags: {stats['total_tags']}",
        ""
    ]
    
    if stats['categories']:
        output.append("Categories:")
        for category, count in sorted(stats['categories'].items()):
            output.append(f"  • {category}: {count}")
        output.append("")
    
    if stats['difficulties']:
        output.append("Difficulties:")
        for difficulty, count in sorted(stats['difficulties'].items()):
            output.append(f"  • {difficulty}: {count}")
    
    return "\n".join(output)
