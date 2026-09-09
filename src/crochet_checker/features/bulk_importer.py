"""Bulk Pattern Importer - Import multiple patterns at once"""

import os
from pathlib import Path
from typing import List, Dict
from dataclasses import dataclass
import json

@dataclass
class ImportedPattern:
    pattern_id: str
    title: str
    file_path: str
    content: str
    tags: List[str]
    status: str
    error_message: str = ""

class BulkPatternImporter:
    """Import multiple patterns from files or directories"""
    
    def __init__(self, library_path: str = "patterns_library"):
        self.library_path = Path(library_path)
        self.library_path.mkdir(parents=True, exist_ok=True)
        self.patterns = []
    
    def import_from_directory(self, directory: str, recursive: bool = True) -> List[ImportedPattern]:
        """Import all pattern files from a directory"""
        dir_path = Path(directory)
        if not dir_path.exists():
            return [ImportedPattern("", "", directory, "", [], "error", "Directory not found")]
        
        imported = []
        pattern_files = []
        
        if recursive:
            pattern_files.extend(dir_path.rglob("*.txt"))
            pattern_files.extend(dir_path.rglob("*.md"))
            pattern_files.extend(dir_path.rglob("*.pattern"))
        else:
            pattern_files.extend(dir_path.glob("*.txt"))
            pattern_files.extend(dir_path.glob("*.md"))
            pattern_files.extend(dir_path.glob("*.pattern"))
        
        for file_path in pattern_files:
            result = self.import_single_file(str(file_path))
            imported.append(result)
        
        self.patterns.extend([p for p in imported if p.status == "success"])
        return imported
    
    def import_single_file(self, file_path: str) -> ImportedPattern:
        """Import a single pattern file"""
        try:
            path = Path(file_path)
            if not path.exists():
                return ImportedPattern("", "", file_path, "", [], "error", "File not found")
            
            content = path.read_text()
            pattern_id = f"pattern_{hash(file_path) % 100000}"
            title = self._extract_title(content, path.stem)
            tags = self._generate_tags(content)
            
            library_file = self.library_path / f"{pattern_id}.json"
            pattern_data = {
                "id": pattern_id,
                "title": title,
                "file_path": file_path,
                "content": content,
                "tags": tags,
            }
            
            with open(library_file, 'w') as f:
                json.dump(pattern_data, f, indent=2)
            
            return ImportedPattern(
                pattern_id=pattern_id,
                title=title,
                file_path=file_path,
                content=content,
                tags=tags,
                status="success"
            )
        except Exception as e:
            return ImportedPattern("", "", file_path, "", [], "error", str(e))
    
    def _extract_title(self, content: str, filename: str) -> str:
        """Extract pattern title from content or filename"""
        lines = content.split('\n')
        for line in lines[:5]:
            line = line.strip()
            if line and not line.startswith('#') and len(line) > 3:
                return line
        return filename.replace('_', ' ').replace('-', ' ').title()
    
    def _generate_tags(self, content: str) -> List[str]:
        """Auto-generate tags based on content"""
        tags = []
        content_lower = content.lower()
        
        if 'amigurumi' in content_lower:
            tags.append('amigurumi')
        if 'hat' in content_lower:
            tags.append('hat')
        if 'scarf' in content_lower:
            tags.append('scarf')
        if 'blanket' in content_lower:
            tags.append('blanket')
        if 'beginner' in content_lower or 'easy' in content_lower:
            tags.append('beginner')
        elif 'intermediate' in content_lower:
            tags.append('intermediate')
        elif 'advanced' in content_lower:
            tags.append('advanced')
        
        return tags if tags else ['uncategorized']
    
    def get_import_summary(self, imported: List[ImportedPattern]) -> str:
        """Generate summary of import results"""
        success = [p for p in imported if p.status == "success"]
        errors = [p for p in imported if p.status == "error"]
        
        output = [
            "📦 Bulk Import Summary",
            "=" * 40,
            f"✅ Successfully imported: {len(success)}",
            f"❌ Failed: {len(errors)}",
            f"📁 Total processed: {len(imported)}",
            ""
        ]
        
        if success:
            output.append("Successfully imported patterns:")
            for p in success[:10]:
                output.append(f"  • {p.title} ({', '.join(p.tags[:3])})")
            if len(success) > 10:
                output.append(f"  ... and {len(success) - 10} more")
        
        return "\n".join(output)

def format_import_results(imported: List[ImportedPattern]) -> str:
    """Format import results for display"""
    importer = BulkPatternImporter()
    return importer.get_import_summary(imported)
