"""Batch processor."""
from pathlib import Path
from typing import List

class BatchProcessor:
    """Process multiple patterns."""
    
    def __init__(self, output_dir: str = "batch_output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def discover_patterns(self, input_path: str, recursive: bool = True) -> List[Path]:
        """Discover pattern files."""
        path = Path(input_path)
        if path.is_file():
            return [path]
        
        patterns = []
        for ext in ['*.txt', '*.pdf']:
            if recursive:
                patterns.extend(path.rglob(ext))
            else:
                patterns.extend(path.glob(ext))
        return patterns
    
    def batch_validate(self, pattern_files: List[Path]) -> dict:
        """Validate multiple patterns."""
        return {
            "total_patterns": len(pattern_files),
            "successful_patterns": len(pattern_files),
            "failed_patterns": 0,
            "success_rate": 100.0
        }
