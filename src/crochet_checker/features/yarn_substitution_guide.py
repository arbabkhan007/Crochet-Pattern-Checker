"""Yarn Substitution Guide - Find yarn alternatives"""
class YarnSubstitutionGuide:
    def __init__(self):
        self.yarns = {"cotton": ["bamboo", "linen"], "wool": ["acrylic", "alpaca"]}
    
    def find_substitutes(self, yarn_type: str) -> list:
        return self.yarns.get(yarn_type.lower(), ["acrylic"])

if __name__ == "__main__":
    print("🧶 Yarn Substitution Guide - Working!")
    guide = YarnSubstitutionGuide()
    print(f"Substitutes for cotton: {guide.find_substitutes('cotton')}")
