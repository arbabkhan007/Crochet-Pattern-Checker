"""Yarn Stash Manager - Manage yarn collection"""
class YarnStashManager:
    def __init__(self):
        self.stash = []
    
    def add_yarn(self, color: str, yardage: int):
        self.stash.append({"color": color, "yardage": yardage})
    
    def get_total_yardage(self) -> int:
        return sum(y["yardage"] for y in self.stash)

if __name__ == "__main__":
    print("🧶 Yarn Stash Manager - Working!")
    manager = YarnStashManager()
    manager.add_yarn("red", 200)
    manager.add_yarn("blue", 150)
    print(f"Total yardage: {manager.get_total_yardage()} yards")
