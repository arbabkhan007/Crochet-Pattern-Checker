"""Crochet Hook Size Guide - Hook size reference"""
class CrochetHookSizeGuide:
    def __init__(self):
        self.sizes = {"fingering": "3.5mm", "worsted": "5.0mm", "bulky": "6.5mm"}
    
    def get_hook_size(self, yarn_weight: str) -> str:
        return self.sizes.get(yarn_weight.lower(), "5.0mm")

if __name__ == "__main__":
    print("🪝 Crochet Hook Size Guide - Working!")
    guide = CrochetHookSizeGuide()
    print(f"Worsted weight hook: {guide.get_hook_size('worsted')}")
