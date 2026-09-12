"""Crochet Symbol Dictionary - Symbol reference"""
class CrochetSymbolDictionary:
    def __init__(self):
        self.symbols = {"sc": "⊕", "dc": "⊗", "hdc": "⊙"}
    
    def get_symbol(self, stitch: str) -> str:
        return self.symbols.get(stitch.lower(), "?")

if __name__ == "__main__":
    print("📖 Crochet Symbol Dictionary - Working!")
    dictionary = CrochetSymbolDictionary()
    print(f"SC symbol: {dictionary.get_symbol('sc')}")
