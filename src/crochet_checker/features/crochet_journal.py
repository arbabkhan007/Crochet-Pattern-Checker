"""
Crochet Journal - Track your crochet journey, mood, and progress
A personal diary that helps you reflect and grow as a crafter
"""
import json
from typing import Dict, List, Optional
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from pathlib import Path


@dataclass
class JournalEntry:
    """A single journal entry"""
    id: str
    date: str
    project_name: str = ""
    mood: str = ""  # happy, calm, focused, frustrated, inspired, relaxed
    energy: int = 3  # 1-5
    minutes_crocheted: int = 0
    rounds_completed: int = 0
    notes: str = ""
    gratitude: str = ""
    challenges: str = ""
    wins: str = ""
    photo: str = ""
    tags: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'JournalEntry':
        return cls(**data)


class CrochetJournal:
    """
    Personal crochet journal and diary
    
    Features:
    - Daily entries with mood tracking
    - Gratitude journaling
    - Progress reflection
    - Streak tracking
    - Weekly/monthly summaries
    - Mood pattern analysis
    - Photo attachments
    - Search entries
    """
    
    MOODS = {
        "happy": {"emoji": "😊", "color": "#FFD700"},
        "calm": {"emoji": "😌", "color": "#87CEEB"},
        "focused": {"emoji": "🎯", "color": "#4ECCA3"},
        "frustrated": {"emoji": "😤", "color": "#E94560"},
        "inspired": {"emoji": "✨", "color": "#FF69B4"},
        "relaxed": {"emoji": "🧘", "color": "#98FB98"},
        "tired": {"emoji": "😴", "color": "#9370DB"},
        "excited": {"emoji": "🤩", "color": "#FF6347"},
    }
    
    PROMPTS = [
        "What stitch did you learn or practice today?",
        "What was the most satisfying moment?",
        "What would you do differently next time?",
        "How does this project make you feel?",
        "What are you grateful for in your crochet journey?",
        "What's your favorite part of today's session?",
        "Did you discover anything new about your tension or style?",
        "What would you tell a beginner about what you learned?",
    ]
    
    def __init__(self, storage_path: str = "crochet_journal.json"):
        self.storage_path = Path(storage_path)
        self.entries: List[JournalEntry] = []
        self._next_id = 1
        self.load()
    
    def load(self):
        if self.storage_path.exists():
            try:
                data = json.loads(self.storage_path.read_text())
                self.entries = [JournalEntry.from_dict(e) for e in data.get("entries", [])]
                self._next_id = data.get("next_id", 1)
            except Exception:
                pass
    
    def save(self):
        data = {
            "entries": [e.to_dict() for e in self.entries],
            "next_id": self._next_id,
        }
        self.storage_path.write_text(json.dumps(data, indent=2))
    
    def add_entry(self, mood: str = "calm", energy: int = 3,
                 minutes: int = 0, rounds: int = 0,
                 project: str = "", notes: str = "",
                 gratitude: str = "", **kwargs) -> str:
        """Add a journal entry"""
        entry_id = f"J{self._next_id:04d}"
        self._next_id += 1
        
        entry = JournalEntry(
            id=entry_id,
            date=datetime.now().strftime("%Y-%m-%d"),
            project_name=project,
            mood=mood,
            energy=min(5, max(1, energy)),
            minutes_crocheted=minutes,
            rounds_completed=rounds,
            notes=notes,
            gratitude=gratitude,
            **kwargs
        )
        
        self.entries.append(entry)
        self.save()
        return entry_id
    
    def get_daily_prompt(self) -> str:
        """Get a journaling prompt for today"""
        import hashlib
        today = datetime.now().strftime("%Y-%m-%d")
        day_hash = int(hashlib.md5(today.encode()).hexdigest(), 16)
        return self.PROMPTS[day_hash % len(self.PROMPTS)]
    
    def get_streak(self) -> Dict:
        """Get crochet streak info"""
        if not self.entries:
            return {"current": 0, "longest": 0, "total_days": 0}
        
        dates = sorted(set(e.date for e in self.entries))
        current = 0
        longest = 0
        streak = 0
        
        today = datetime.now().strftime("%Y-%m-%d")
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        
        for i, date in enumerate(dates):
            if i == 0:
                streak = 1
            else:
                prev = datetime.strptime(dates[i-1], "%Y-%m-%d")
                curr = datetime.strptime(date, "%Y-%m-%d")
                if (curr - prev).days == 1:
                    streak += 1
                else:
                    streak = 1
            
            longest = max(longest, streak)
            
            if date in (today, yesterday):
                current = streak
        
        return {
            "current": current,
            "longest": longest,
            "total_days": len(dates),
        }
    
    def get_mood_analysis(self) -> Dict:
        """Analyze mood patterns"""
        if not self.entries:
            return {}
        
        mood_counts = {}
        mood_by_day = {}
        total_minutes = sum(e.minutes_crocheted for e in self.entries)
        total_entries = len(self.entries)
        
        for entry in self.entries:
            mood = entry.mood or "unknown"
            mood_counts[mood] = mood_counts.get(mood, 0) + 1
            
            day = datetime.strptime(entry.date, "%Y-%m-%d").strftime("%A")
            if day not in mood_by_day:
                mood_by_day[day] = {}
            mood_by_day[day][mood] = mood_by_day[day].get(mood, 0) + 1
        
        # Most common mood
        top_mood = max(mood_counts.items(), key=lambda x: x[1]) if mood_counts else ("none", 0)
        
        # Best day of week
        day_moods = {}
        for day, moods in mood_by_day.items():
            positive = sum(v for k, v in moods.items() if k in ("happy", "calm", "inspired", "relaxed"))
            total = sum(moods.values())
            day_moods[day] = positive / max(1, total) * 100
        
        best_day = max(day_moods.items(), key=lambda x: x[1]) if day_moods else ("none", 0)
        
        return {
            "total_entries": total_entries,
            "total_minutes": total_minutes,
            "total_hours": round(total_minutes / 60, 1),
            "mood_distribution": mood_counts,
            "top_mood": top_mood[0],
            "top_mood_pct": round(top_mood[1] / total_entries * 100, 1),
            "best_day": best_day[0],
            "best_day_score": round(best_day[1], 1),
            "avg_energy": round(sum(e.energy for e in self.entries) / total_entries, 1),
            "avg_minutes": round(total_minutes / total_entries, 0),
        }
    
    def get_weekly_summary(self, weeks_back: int = 0) -> Dict:
        """Get weekly summary"""
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday() + (weeks_back * 7))
        week_end = week_start + timedelta(days=7)
        
        week_entries = [
            e for e in self.entries
            if week_start <= datetime.strptime(e.date, "%Y-%m-%d") < week_end
        ]
        
        if not week_entries:
            return {"message": "No entries this week"}
        
        total_minutes = sum(e.minutes_crocheted for e in week_entries)
        total_rounds = sum(e.rounds_completed for e in week_entries)
        moods = [e.mood for e in week_entries if e.mood]
        projects = list(set(e.project_name for e in week_entries if e.project_name))
        
        return {
            "week": f"{week_start.strftime('%b %d')} - {week_end.strftime('%b %d')}",
            "entries": len(week_entries),
            "total_minutes": total_minutes,
            "total_hours": round(total_minutes / 60, 1),
            "total_rounds": total_rounds,
            "moods": moods,
            "projects": projects,
            "avg_energy": round(sum(e.energy for e in week_entries) / len(week_entries), 1),
        }
    
    def search(self, query: str) -> List[JournalEntry]:
        """Search journal entries"""
        query_lower = query.lower()
        results = []
        
        for entry in self.entries:
            searchable = f"{entry.notes} {entry.project_name} {entry.mood} {' '.join(entry.tags)}".lower()
            if query_lower in searchable:
                results.append(entry)
        
        return sorted(results, key=lambda e: e.date, reverse=True)
    
    def generate_report(self) -> str:
        """Generate a beautiful journal report"""
        streak = self.get_streak()
        mood = self.get_mood_analysis()
        
        report = f"""
╔══════════════════════════════════════════════════════════╗
║              📖 CROCHET JOURNAL REPORT                    ║
╚══════════════════════════════════════════════════════════╝

🔥 STREAK
═══════════════════════════════════════════════════════════
  Current Streak:    {streak['current']} days
  Longest Streak:    {streak['longest']} days
  Total Days:        {streak['total_days']}

📊 STATISTICS
═══════════════════════════════════════════════════════════
  Total Entries:     {mood.get('total_entries', 0)}
  Total Time:        {mood.get('total_hours', 0)} hours
  Avg Session:       {int(mood.get('avg_minutes', 0))} minutes
  Avg Energy:        {mood.get('avg_energy', 0)}/5

😊 MOOD
═══════════════════════════════════════════════════════════
  Top Mood:          {mood.get('top_mood', 'N/A')} ({mood.get('top_mood_pct', 0)}%)
  Best Day:          {mood.get('best_day', 'N/A')} ({mood.get('best_day_score', 0)}% positive)
"""
        
        if mood.get('mood_distribution'):
            report += "\n  Mood Breakdown:\n"
            for mood_name, count in sorted(mood['mood_distribution'].items(), key=lambda x: -x[1]):
                emoji = self.MOODS.get(mood_name, {}).get("emoji", "•")
                bar = "█" * count
                report += f"    {emoji} {mood_name:12s} {bar} ({count})\n"
        
        # Recent entries
        recent = sorted(self.entries, key=lambda e: e.date, reverse=True)[:5]
        if recent:
            report += f"\n📝 RECENT ENTRIES\n"
            report += f"{'═' * 59}\n\n"
            for entry in recent:
                emoji = self.MOODS.get(entry.mood, {}).get("emoji", "•")
                report += f"  {emoji} {entry.date}"
                if entry.project_name:
                    report += f" | {entry.project_name}"
                report += f"\n"
                if entry.notes:
                    report += f"     {entry.notes[:80]}...\n"
                report += "\n"
        
        report += f"{'═' * 59}\n"
        return report


# Demo
if __name__ == "__main__":
    import os
    print("\n" + "=" * 60)
    print("  CROCHET JOURNAL - DEMONSTRATION")
    print("=" * 60)
    
    journal = CrochetJournal(storage_path="/tmp/demo_journal.json")
    
    # Add entries
    journal.add_entry(mood="happy", energy=4, minutes=45, rounds=5,
                     project="Bunny Amigurumi", notes="Finally got the ears right!",
                     gratitude="Grateful for patience today")
    
    journal.add_entry(mood="calm", energy=3, minutes=30, rounds=3,
                     project="Granny Blanket", notes="Mindless crochet while watching TV")
    
    journal.add_entry(mood="frustrated", energy=2, minutes=20, rounds=1,
                     project="Bunny Amigurumi", notes="Kept messing up round 7, had to frog twice")
    
    journal.add_entry(mood="inspired", energy=5, minutes=60, rounds=8,
                     project="New Design", notes="Started sketching a new fox pattern!")
    
    journal.add_entry(mood="relaxed", energy=4, minutes=40, rounds=4,
                     project="Granny Blanket", notes="Perfect evening crochet session")
    
    print(f"\n✅ Added 5 journal entries")
    
    # Daily prompt
    print(f"\n💭 Today's Prompt:")
    print(f"  {journal.get_daily_prompt()}")
    
    # Streak
    streak = journal.get_streak()
    print(f"\n🔥 Streak: {streak['current']} days (Best: {streak['longest']})")
    
    # Mood analysis
    mood = journal.get_mood_analysis()
    print(f"\n😊 Mood Analysis:")
    print(f"  Top mood: {mood['top_mood']} ({mood['top_mood_pct']}%)")
    print(f"  Best day: {mood['best_day']}")
    print(f"  Avg energy: {mood['avg_energy']}/5")
    print(f"  Total time: {mood['total_hours']} hours")
    
    # Search
    print(f"\n🔍 Search: 'bunny'")
    results = journal.search("bunny")
    for r in results:
        print(f"  {r.date}: {r.notes[:50]}")
    
    # Full report
    print(journal.generate_report())
    
    # Cleanup
    if os.path.exists("/tmp/demo_journal.json"):
        os.remove("/tmp/demo_journal.json")
    
    print(f"\n  Crochet Journal Complete! 📖")
