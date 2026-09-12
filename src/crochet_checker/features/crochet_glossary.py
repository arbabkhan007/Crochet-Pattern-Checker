"""Crochet Glossary - Term definitions"""
class CrochetGlossary:
    def __init__(self):
        self.terms = {"sc": "Single crochet", "dc": "Double crochet", "ch": "Chain"}
    
    def define(self, term: str) -> str:
        return self.terms.get(term.lower(), "Term not found")

if __name__ == "__main__":
    print("📖 Crochet Glossary - Working!")
    glossary = CrochetGlossary()
    print(f"SC: {glossary.define('sc')}")
