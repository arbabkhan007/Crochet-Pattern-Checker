"""Stitch Abbreviation Converter - Convert abbreviations"""
class StitchAbbreviationConverter:
    def __init__(self):
        self.abbreviations = {"sc": "single crochet", "dc": "double crochet"}
    
    def expand(self, abbreviation: str) -> str:
        return self.abbreviations.get(abbreviation.lower(), abbreviation)

if __name__ == "__main__":
    print("🔄 Stitch Abbreviation Converter - Working!")
    converter = StitchAbbreviationConverter()
    print(f"SC = {converter.expand('sc')}")
