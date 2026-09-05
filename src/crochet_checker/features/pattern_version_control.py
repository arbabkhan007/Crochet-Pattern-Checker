
import json
from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import difflib

@dataclass
class PatternVersion:
    version_id: str
    pattern_id: str
    content: str
    timestamp: str
    change_description: str
    diff_from_previous: str = ""

class PatternVersionControl:
    def __init__(self, versions_path: str = "pattern_versions"):
        self.versions_path = Path(versions_path)
        self.versions_path.mkdir(parents=True, exist_ok=True)
        self.versions = {}
        self._load_versions()
    
    def _load_versions(self):
        for file in self.versions_path.glob("*.json"):
            try:
                with open(file, 'r') as f:
                    data = json.load(f)
                    version = PatternVersion(**data)
                    if version.pattern_id not in self.versions:
                        self.versions[version.pattern_id] = []
                    self.versions[version.pattern_id].append(version)
            except Exception:
                pass
    
    def save_version(self, pattern_id: str, content: str, description: str = "") -> PatternVersion:
        version_num = len(self.versions.get(pattern_id, [])) + 1
        version_id = f"{pattern_id}_v{version_num}"
        diff = ""
        if pattern_id in self.versions and self.versions[pattern_id]:
            previous = self.versions[pattern_id][-1]
            diff = self._calculate_diff(previous.content, content)
        
        version = PatternVersion(
            version_id=version_id,
            pattern_id=pattern_id,
            content=content,
            timestamp=datetime.now().isoformat(),
            change_description=description,
            diff_from_previous=diff
        )
        
        if pattern_id not in self.versions:
            self.versions[pattern_id] = []
        self.versions[pattern_id].append(version)
        self._save_version(version)
        return version
    
    def get_versions(self, pattern_id: str) -> List[PatternVersion]:
        return self.versions.get(pattern_id, [])
    
    def _calculate_diff(self, text1: str, text2: str) -> str:
        diff = difflib.unified_diff(text1.splitlines(keepends=True), text2.splitlines(keepends=True), lineterm='')
        return ''.join(diff)
    
    def _save_version(self, version: PatternVersion):
        version_file = self.versions_path / f"{version.version_id}.json"
        with open(version_file, 'w') as f:
            json.dump(asdict(version), f, indent=2)

def format_version_history(versions: List[PatternVersion]) -> str:
    if not versions:
        return "No version history available."
    output = [f"📝 Version History", "=" * 50, f"Total Versions: {len(versions)}\n"]
    for i, version in enumerate(versions, 1):
        output.append(f"Version {i}: {version.version_id}")
        output.append(f"  Time: {version.timestamp}")
        if version.change_description:
            output.append(f"  Changes: {version.change_description}")
        output.append("")
    return "\n".join(output)
