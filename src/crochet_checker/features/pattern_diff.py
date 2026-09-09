"""Pattern Diff Tool"""

import difflib
from dataclasses import dataclass
from typing import List

@dataclass
class DiffResult:
    added_lines: List[str]
    removed_lines: List[str]
    unchanged_lines: int
    similarity_ratio: float
    summary: str

def diff_patterns(pattern1: str, pattern2: str) -> DiffResult:
    lines1 = pattern1.splitlines(keepends=True)
    lines2 = pattern2.splitlines(keepends=True)
    
    added = [line[1:].rstrip() for line in difflib.unified_diff(lines1, lines2) if line.startswith('+') and not line.startswith('+++')]
    removed = [line[1:].rstrip() for line in difflib.unified_diff(lines1, lines2) if line.startswith('-') and not line.startswith('---')]
    unchanged = sum(1 for line in difflib.unified_diff(lines1, lines2) if line.startswith(' '))
    
    similarity = difflib.SequenceMatcher(None, pattern1, pattern2).ratio()
    
    if similarity == 1.0:
        summary = "✅ Patterns are identical"
    elif similarity > 0.95:
        summary = f"✅ Patterns are very similar ({similarity*100:.1f}% match)"
    elif similarity > 0.80:
        summary = f"⚠️  Patterns have moderate differences ({similarity*100:.1f}% match)"
    else:
        summary = f"❌ Patterns are significantly different ({similarity*100:.1f}% match)"
    
    return DiffResult(
        added_lines=added,
        removed_lines=removed,
        unchanged_lines=unchanged,
        similarity_ratio=similarity,
        summary=summary
    )

def format_diff_result(diff: DiffResult) -> str:
    output = [f"🔍 Pattern Comparison\n{'=' * 40}\n{diff.summary}\n",
              f"Similarity: {diff.similarity_ratio*100:.1f}%",
              f"Added lines: {len(diff.added_lines)}",
              f"Removed lines: {len(diff.removed_lines)}"]
    
    if diff.added_lines:
        output.append("\n➕ Added:")
        output.extend(f"  {line}" for line in diff.added_lines[:10])
    
    if diff.removed_lines:
        output.append("\n➖ Removed:")
        output.extend(f"  {line}" for line in diff.removed_lines[:10])
    
    return "\n".join(output)
