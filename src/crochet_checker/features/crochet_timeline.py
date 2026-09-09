"""
Crochet Timeline - Visual journey of your crochet history and milestones
"""
import json
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path


class CrochetTimeline:
    """
    Visual timeline of your crochet journey
    
    Features:
    - Add milestones and events
    - Visual timeline generation
    - Journey statistics
    - Photo attachments
    - Memory preservation
    - Export timeline
    """
    
    MILESTONE_TYPES = {
        "first_project": {"emoji": "🌱", "name": "First Project"},
        "first_gift": {"emoji": "🎁", "name": "First Gift Given"},
        "first_sale": {"emoji": "💰", "name": "First Sale"},
        "new_skill": {"emoji": "🎯", "name": "New Skill Learned"},
        "challenge": {"emoji": "🏆", "name": "Challenge Completed"},
        "project": {"emoji": "🧶", "name": "Project Completed"},
        "event": {"emoji": "📅", "name": "Event Attended"},
        "achievement": {"emoji": "⭐", "name": "Achievement Unlocked"},
        "memory": {"emoji": "💭", "name": "Special Memory"},
        "milestone": {"emoji": "🎉", "name": "Milestone Reached"},
    }
    
    def __init__(self, storage_path: str = "crochet_timeline.json"):
        self.storage_path = Path(storage_path)
        self.events: List[Dict] = []
        self.load()
    
    def load(self):
        if self.storage_path.exists():
            try:
                data = json.loads(self.storage_path.read_text())
                self.events = data.get("events", [])
            except Exception:
                pass
    
    def save(self):
        self.storage_path.write_text(json.dumps({"events": self.events}, indent=2))
    
    def add_event(self, title: str, event_type: str = "project",
                 date: str = None, description: str = "",
                 photo: str = "", tags: List[str] = None) -> Dict:
        """Add a timeline event"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        event = {
            "id": f"TL{len(self.events) + 1:04d}",
            "title": title,
            "type": event_type,
            "date": date,
            "description": description,
            "photo": photo,
            "tags": tags or [],
            "created": datetime.now().isoformat(),
        }
        
        self.events.append(event)
        self.events.sort(key=lambda e: e["date"])
        self.save()
        
        return event
    
    def get_timeline(self, year: int = None, event_type: str = None) -> List[Dict]:
        """Get timeline events filtered"""
        events = self.events.copy()
        
        if year:
            events = [e for e in events if e["date"].startswith(str(year))]
        
        if event_type:
            events = [e for e in events if e["type"] == event_type]
        
        return events
    
    def get_journey_stats(self) -> Dict:
        """Get journey statistics"""
        if not self.events:
            return {"message": "No events yet. Start your journey!"}
        
        first_event = min(e["date"] for e in self.events)
        last_event = max(e["date"] for e in self.events)
        
        # Calculate days crocheting
        start = datetime.strptime(first_event, "%Y-%m-%d")
        end = datetime.strptime(last_event, "%Y-%m-%d")
        days_active = (end - start).days + 1
        
        # By type
        by_type = {}
        for event in self.events:
            etype = event["type"]
            by_type[etype] = by_type.get(etype, 0) + 1
        
        # By year
        by_year = {}
        for event in self.events:
            year = event["date"][:4]
            by_year[year] = by_year.get(year, 0) + 1
        
        # Tags
        all_tags = []
        for event in self.events:
            all_tags.extend(event.get("tags", []))
        tag_counts = {}
        for tag in all_tags:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        return {
            "total_events": len(self.events),
            "first_event": first_event,
            "last_event": last_event,
            "days_active": days_active,
            "years_active": len(by_year),
            "events_by_type": by_type,
            "events_by_year": by_year,
            "top_tags": sorted(tag_counts.items(), key=lambda x: -x[1])[:5],
            "most_active_year": max(by_year.items(), key=lambda x: x[1])[0] if by_year else None,
        }
    
    def get_year_highlights(self, year: int) -> Dict:
        """Get highlights for a specific year"""
        year_events = [e for e in self.events if e["date"].startswith(str(year))]
        
        if not year_events:
            return {"message": f"No events in {year}"}
        
        by_type = {}
        for event in year_events:
            etype = event["type"]
            if etype not in by_type:
                by_type[etype] = []
            by_type[etype].append(event["title"])
        
        # First and last events
        first = min(year_events, key=lambda e: e["date"])
        last = max(year_events, key=lambda e: e["date"])
        
        return {
            "year": year,
            "total_events": len(year_events),
            "first_event": f"{first['date']}: {first['title']}",
            "last_event": f"{last['date']}: {last['title']}",
            "by_type": by_type,
            "highlights": [e["title"] for e in year_events if e["type"] in ("achievement", "milestone", "challenge")],
        }
    
    def generate_timeline_html(self) -> str:
        """Generate visual timeline HTML"""
        events = self.events
        
        items = ""
        for event in events:
            type_info = self.MILESTONE_TYPES.get(event["type"], self.MILESTONE_TYPES["project"])
            emoji = type_info["emoji"]
            
            items += f"""
            <div class="event">
                <div class="date">{event['date']}</div>
                <div class="icon">{emoji}</div>
                <div class="content">
                    <h3>{event['title']}</h3>
                    <p>{event.get('description', '')}</p>
                    {''.join(f'<span class="tag">#{tag}</span>' for tag in event.get('tags', []))}
                </div>
            </div>"""
        
        stats = self.get_journey_stats()
        
        return f'''<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Crochet Timeline</title>
<style>
body {{ font-family: -apple-system, sans-serif; background: #1a1a2e; color: #eee; padding: 20px; }}
h1 {{ text-align: center; color: #4ECCA3; }}
.stats {{ text-align: center; margin: 20px 0; }}
.stat {{ display: inline-block; margin: 0 20px; }}
.stat-num {{ font-size: 2em; font-weight: bold; color: #4ECCA3; }}
.timeline {{ max-width: 700px; margin: 40px auto; position: relative; padding-left: 60px; }}
.timeline::before {{ content: ''; position: absolute; left: 25px; top: 0; bottom: 0; width: 2px; background: #4ECCA3; }}
.event {{ position: relative; margin: 30px 0; padding: 15px; background: #16213e; border-radius: 8px; border-left: 3px solid #4ECCA3; }}
.event .date {{ position: absolute; left: -55px; top: 15px; font-size: 0.8em; color: #888; width: 45px; text-align: right; }}
.event .icon {{ position: absolute; left: -42px; top: 15px; font-size: 1.5em; background: #1a1a2e; padding: 2px; }}
.event h3 {{ margin: 0 0 8px 0; color: #4ECCA3; }}
.event p {{ margin: 0; color: #ccc; font-size: 0.9em; }}
.tag {{ display: inline-block; background: #0f3460; padding: 2px 8px; border-radius: 10px; font-size: 0.75em; margin: 5px 5px 0 0; color: #4ECCA3; }}
</style></head>
<body>
<h1>🧶 My Crochet Journey</h1>
<div class="stats">
    <div class="stat"><div class="stat-num">{stats.get('total_events', 0)}</div>Memories</div>
    <div class="stat"><div class="stat-num">{stats.get('years_active', 0)}</div>Years</div>
    <div class="stat"><div class="stat-num">{stats.get('days_active', 0)}</div>Days Active</div>
</div>
<div class="timeline">{items}</div>
</body></html>'''


# Demo
if __name__ == "__main__":
    import os
    print("\n" + "=" * 60)
    print("  CROCHET TIMELINE - DEMONSTRATION")
    print("=" * 60)
    
    timeline = CrochetTimeline(storage_path="/tmp/demo_timeline.json")
    
    # Add events
    timeline.add_event("Learned single crochet", "first_project",
                      "2023-01-15", "Made my first chain and sc!", tags=["beginner", "first"])
    
    timeline.add_event("First amigurumi bunny", "project",
                      "2023-03-20", "Completed my first stuffed animal", tags=["amigurumi"])
    
    timeline.add_event("Learned colorwork", "new_skill",
                      "2023-06-10", "Tried tapestry crochet for the first time", tags=["colorwork", "skill"])
    
    timeline.add_event("Won crochet contest", "achievement",
                      "2023-09-05", "1st place at local craft fair!", tags=["award", "fair"])
    
    timeline.add_event("First pattern sale", "first_sale",
                      "2024-01-12", "Sold my first pattern on Etsy", tags=["business"])
    
    timeline.add_event("Made 100th project", "milestone",
                      "2024-06-30", "Century club! 100 completed projects", tags=["milestone"])
    
    print(f"✅ Added 6 timeline events")
    
    # Stats
    print(f"\n📊 Journey Stats:")
    stats = timeline.get_journey_stats()
    print(f"  Total Events: {stats['total_events']}")
    print(f"  First: {stats['first_event']}")
    print(f"  Last: {stats['last_event']}")
    print(f"  Days Active: {stats['days_active']}")
    print(f"  Years: {stats['years_active']}")
    
    print(f"\n  By Type:")
    for etype, count in stats['events_by_type'].items():
        emoji = timeline.MILESTONE_TYPES.get(etype, {}).get("emoji", "•")
        print(f"    {emoji} {etype}: {count}")
    
    # Year highlights
    print(f"\n📅 2023 Highlights:")
    highlights = timeline.get_year_highlights(2023)
    print(f"  Events: {highlights['total_events']}")
    print(f"  First: {highlights['first_event']}")
    print(f"  Last: {highlights['last_event']}")
    
    # HTML
    html = timeline.generate_timeline_html()
    print(f"\n✅ Visual timeline: {len(html)} chars")
    
    # Cleanup
    if os.path.exists("/tmp/demo_timeline.json"):
        os.remove("/tmp/demo_timeline.json")
    
    print(f"\n  Crochet Timeline Complete! 📅")
