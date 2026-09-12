"""Pattern Search Engine - Search patterns"""
class PatternSearchEngine:
    def __init__(self):
        self.patterns = ["Bunny Pattern", "Granny Square", "Baby Blanket"]
    
    def search(self, query: str) -> list:
        return [p for p in self.patterns if query.lower() in p.lower()]

if __name__ == "__main__":
    print("🔍 Pattern Search Engine - Working!")
    engine = PatternSearchEngine()
    results = engine.search("bunny")
    print(f"Found {len(results)} patterns")
