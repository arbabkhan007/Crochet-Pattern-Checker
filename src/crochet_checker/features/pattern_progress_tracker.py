"""Pattern Progress Tracker - Track project progress"""
class PatternProgressTracker:
    def __init__(self):
        self.progress = 0
        self.total_rows = 0
    
    def set_total_rows(self, rows: int):
        self.total_rows = rows
    
    def complete_row(self):
        self.progress += 1
    
    def get_percentage(self) -> float:
        return (self.progress / self.total_rows * 100) if self.total_rows > 0 else 0

if __name__ == "__main__":
    print("📈 Pattern Progress Tracker - Working!")
    tracker = PatternProgressTracker()
    tracker.set_total_rows(20)
    tracker.complete_row()
    tracker.complete_row()
    print(f"Progress: {tracker.get_percentage():.0f}%")
