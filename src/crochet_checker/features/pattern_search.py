"""Pattern Search Engine"""

from dataclasses import dataclass
from typing import List

@dataclass
class SearchResult:
    pattern_id: str
    title: str
    snippet: str
    score: float
    match_type: str

class PatternSearchEngine:
    def __init__(self):
        self.patterns = []
    
    def add_pattern(self, pattern_id: str, title: str, content: str, tags: List[str] = None):
        self.patterns.append({
            'id': pattern_id,
            'title': title.lower(),
            'content': content.lower(),
            'tags': [t.lower() for t in (tags or [])]
        })
    
    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_lower = query.lower()
        results = []
        
        for pattern in self.patterns:
            score = 0.0
            match_type = 'content'
            
            if query_lower in pattern['title']:
                score += 10.0
                match_type = 'title'
            
            for tag in pattern['tags']:
                if query_lower in tag:
                    score += 5.0
                    match_type = 'tag'
            
            if query_lower in pattern['content']:
                score += 1.0
            
            if score > 0:
                idx = pattern['content'].find(query_lower)
                snippet = pattern['content'][max(0, idx-25):idx+len(query)+25] if idx != -1 else pattern['content'][:50]
                
                results.append(SearchResult(
                    pattern_id=pattern['id'],
                    title=pattern['title'].title(),
                    snippet=snippet + "...",
                    score=score,
                    match_type=match_type
                ))
        
        results.sort(key=lambda x: x.score, reverse=True)
        return results[:limit]

def format_search_results(results: List[SearchResult]) -> str:
    if not results:
        return "No patterns found."
    
    output = [f"🔍 Found {len(results)} pattern(s)\n{'=' * 40}\n"]
    
    for i, result in enumerate(results, 1):
        output.append(f"{i}. {result.title}")
        output.append(f"   Match: {result.match_type} (score: {result.score:.1f})")
        output.append(f"   {result.snippet}\n")
    
    return "\n".join(output)
