"""Stitch Counter Pro - Track stitch counts"""
class StitchCounterPro:
    def __init__(self):
        self.count = 0
    
    def add_stitches(self, count: int):
        self.count += count
    
    def get_count(self) -> int:
        return self.count

if __name__ == "__main__":
    print("🔢 Stitch Counter Pro - Working!")
    counter = StitchCounterPro()
    counter.add_stitches(10)
    counter.add_stitches(5)
    print(f"Total stitches: {counter.get_count()}")
