"""Pattern Notes Manager - Manage pattern notes"""
class PatternNotesManager:
    def __init__(self):
        self.notes = []
    
    def add_note(self, note: str):
        self.notes.append(note)
    
    def get_notes(self) -> list:
        return self.notes

if __name__ == "__main__":
    print("📝 Pattern Notes Manager - Working!")
    manager = PatternNotesManager()
    manager.add_note("Use 4mm hook")
    print(f"Notes: {len(manager.get_notes())}")
