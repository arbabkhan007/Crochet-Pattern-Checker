"""
Crochet Time Capsule - Save messages to your future self and track your crochet journey
"""
import json
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from pathlib import Path


class CrochetTimeCapsule:
    """
    Save messages and memories for your future crochet self
    
    Features:
    - Messages to future self
    - Project snapshots (what you're working on now)
    - Skill reflections
    - Favorite memories
    - Predictions for the future
    - Time-based unlocks
    """
    
    PROMPTS = [
        "What's your current favorite stitch?",
        "What project are you most proud of?",
        "What's the hardest thing you've learned so far?",
        "What do you hope to learn in the next year?",
        "Who has inspired your crochet journey?",
        "What's your funniest crochet mistake?",
        "What yarn is your absolute favorite?",
        "What advice would you give your past self?",
        "What are you working on right now?",
        "How has crochet changed your life?",
    ]
    
    def __init__(self, storage_path: str = "crochet_time_capsule.json"):
        self.storage_path = Path(storage_path)
        self.data = {
            "capsules": [],
            "snapshots": [],
            "predictions": [],
        }
        self.load()
    
    def load(self):
        if self.storage_path.exists():
            try:
                self.data.update(json.loads(self.storage_path.read_text()))
            except Exception:
                pass
    
    def save(self):
        self.storage_path.write_text(json.dumps(self.data, indent=2))
    
    def create_capsule(self, message: str, open_date: str = None,
                      open_days: int = 365, prompt: str = "",
                      mood: str = "", current_project: str = "") -> Dict:
        """Create a time capsule message"""
        if open_date is None:
            open_date = (datetime.now() + timedelta(days=open_days)).strftime("%Y-%m-%d")
        
        capsule = {
            "id": f"TC{len(self.data['capsules']) + 1:04d}",
            "message": message,
            "created": datetime.now().strftime("%Y-%m-%d"),
            "open_date": open_date,
            "prompt": prompt,
            "opened": False,
            "mood": mood,
            "current_project": current_project,
        }
        
        self.data["capsules"].append(capsule)
        self.save()
        
        return capsule
    
    def create_snapshot(self, project_name: str, notes: str = "",
                       photo: str = "", current_skill: str = "") -> Dict:
        """Create a project snapshot"""
        snapshot = {
            "id": f"SN{len(self.data['snapshots']) + 1:04d}",
            "project": project_name,
            "notes": notes,
            "photo": photo,
            "skill_level": current_skill,
            "date": datetime.now().strftime("%Y-%m-%d"),
        }
        
        self.data["snapshots"].append(snapshot)
        self.save()
        
        return snapshot
    
    def make_prediction(self, prediction: str, category: str = "skill") -> Dict:
        """Make a prediction about your crochet future"""
        pred = {
            "id": f"PR{len(self.data['predictions']) + 1:04d}",
            "prediction": prediction,
            "category": category,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "check_date": (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d"),
            "came_true": None,
        }
        
        self.data["predictions"].append(pred)
        self.save()
        
        return pred
    
    def check_capsules(self) -> List[Dict]:
        """Check which capsules are ready to open"""
        today = datetime.now().strftime("%Y-%m-%d")
        ready = []
        
        for capsule in self.data["capsules"]:
            if not capsule["opened"] and capsule["open_date"] <= today:
                ready.append(capsule)
        
        return ready
    
    def open_capsule(self, capsule_id: str) -> Dict:
        """Open a time capsule"""
        capsule = next((c for c in self.data["capsules"] if c["id"] == capsule_id), None)
        if not capsule:
            return {"error": "Capsule not found"}
        
        if capsule["open_date"] > datetime.now().strftime("%Y-%m-%d"):
            days_left = (datetime.strptime(capsule["open_date"], "%Y-%m-%d") - datetime.now()).days
            return {"error": f"Not ready yet! {days_left} days remaining"}
        
        capsule["opened"] = True
        self.save()
        
        return {
            "id": capsule["id"],
            "message": capsule["message"],
            "from_date": capsule["created"],
            "prompt": capsule["prompt"],
            "days_sealed": (datetime.now() - datetime.strptime(capsule["created"], "%Y-%m-%d")).days,
        }
    
    def get_random_prompt(self) -> str:
        """Get a random journaling prompt"""
        import random
        return random.choice(self.PROMPTS)
    
    def get_journey_stats(self) -> Dict:
        """Get journey statistics"""
        capsules = self.data["capsules"]
        snapshots = self.data["snapshots"]
        predictions = self.data["predictions"]
        
        # Check predictions
        today = datetime.now().strftime("%Y-%m-%d")
        checkable = [p for p in predictions if p["check_date"] <= today and p["came_true"] is None]
        checked = [p for p in predictions if p["came_true"] is not None]
        correct = sum(1 for p in checked if p["came_true"])
        
        return {
            "capsules_created": len(capsules),
            "capsules_opened": sum(1 for c in capsules if c["opened"]),
            "capsules_sealed": sum(1 for c in capsules if not c["opened"]),
            "snapshots_taken": len(snapshots),
            "predictions_made": len(predictions),
            "predictions_checkable": len(checkable),
            "predictions_checked": len(checked),
            "predictions_correct": correct,
            "accuracy": f"{round(correct / max(1, len(checked)) * 100)}%" if checked else "N/A",
        }
    
    def get_year_in_review(self) -> Dict:
        """Generate a year-in-review summary"""
        today = datetime.now()
        year_ago = (today - timedelta(days=365)).strftime("%Y-%m-%d")
        
        year_capsules = [c for c in self.data["capsules"] if c["created"] >= year_ago]
        year_snapshots = [s for s in self.data["snapshots"] if s["date"] >= year_ago]
        year_predictions = [p for p in self.data["predictions"] if p["date"] >= year_ago]
        
        return {
            "capsules_written": len(year_capsules),
            "snapshots_taken": len(year_snapshots),
            "predictions_made": len(year_predictions),
            "oldest_capsule": year_capsules[0]["created"] if year_capsules else None,
            "recent_snapshots": [s["project"] for s in year_snapshots[-5:]],
        }
    
    def generate_reflection_html(self) -> str:
        """Generate a reflection page"""
        capsules = self.data["capsules"]
        opened = [c for c in capsules if c["opened"]]
        
        items = ""
        for c in opened:
            items += f"""
            <div class="capsule">
                <div class="date">Written: {c['created']} | Opened: {c['open_date']}</div>
                <div class="message">{c['message']}</div>
                {f'<div class="prompt">Prompt: {c["prompt"]}</div>' if c.get('prompt') else ''}
            </div>"""
        
        return f'''<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Crochet Time Capsules</title>
<style>
body {{ font-family: Georgia, serif; background: #f5f0e8; color: #333; padding: 20px; max-width: 700px; margin: 0 auto; }}
h1 {{ text-align: center; color: #764ba2; }}
.intro {{ text-align: center; font-style: italic; color: #666; margin: 20px 0; }}
.capsule {{ background: white; border: 2px solid #ddd; border-radius: 12px; padding: 20px; margin: 20px 0;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1); position: relative; }}
.capsule::before {{ content: "💌"; position: absolute; top: -15px; left: 20px; font-size: 2em; }}
.date {{ color: #999; font-size: 0.85em; margin-bottom: 10px; }}
.message {{ font-size: 1.1em; line-height: 1.6; }}
.prompt {{ color: #764ba2; font-style: italic; margin-top: 10px; padding-top: 10px; border-top: 1px solid #eee; }}
.sealed {{ opacity: 0.6; text-align: center; padding: 30px; }}
</style></head>
<body>
<h1>💌 My Crochet Time Capsules</h1>
<p class="intro">Messages from my past self to my future self</p>
{items if items else '<div class="sealed">No capsules opened yet. Create one and wait!</div>'}
<p class="intro" style="margin-top: 40px;">Keep creating, keep growing 🧶</p>
</body></html>'''


# Demo
if __name__ == "__main__":
    import os
    print("\n" + "=" * 60)
    print("  CROCHET TIME CAPSULE - DEMONSTRATION")
    print("=" * 60)
    
    capsule = CrochetTimeCapsule(storage_path="/tmp/demo_capsule.json")
    
    # Random prompt
    print(f"\n💭 Prompt: {capsule.get_random_prompt()}")
    
    # Create capsules
    c1 = capsule.create_capsule(
        "I just finished my first amigurumi bunny! It took me 3 days but I'm so proud. I hope in a year I'll be making complex patterns effortlessly.",
        open_days=365,
        prompt="What's your current project and how do you feel about it?",
        mood="excited"
    )
    
    c2 = capsule.create_capsule(
        "Today I learned how to do cable stitches! My hands hurt but it was worth it. Future me - I hope you've mastered colorwork by now!",
        open_days=180,
        prompt="What new skill did you just learn?"
    )
    
    # Create capsule that's already openable
    c3 = capsule.create_capsule(
        "Just started my crochet journey. So excited to learn!",
        open_date=(datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
        prompt="How did you feel starting?"
    )
    
    print(f"\n✅ Created 3 capsules")
    
    # Take snapshots
    s1 = capsule.create_snapshot("Granny Square Blanket", "Working on round 12, using 6 colors",
                                current_skill="intermediate")
    s2 = capsule.create_snapshot("Amigurumi Bunny", "Finally got the ears right!",
                                current_skill="intermediate")
    print(f"✅ Created 2 snapshots")
    
    # Make predictions
    p1 = capsule.make_prediction("I'll learn to read patterns without counting every stitch", "skill")
    p2 = capsule.make_prediction("I'll design my own original pattern", "achievement")
    p3 = capsule.make_prediction("I'll have completed 20+ projects", "milestone")
    print(f"✅ Made 3 predictions")
    
    # Check capsules
    print(f"\n🔍 Checking capsules...")
    ready = capsule.check_capsules()
    print(f"  {len(ready)} capsule(s) ready to open!")
    
    # Open ready capsule
    if ready:
        opened = capsule.open_capsule(ready[0]["id"])
        print(f"\n📬 Opening capsule from {opened['from_date']}:")
        print(f"  \"{opened['message']}\"")
        print(f"  Sealed for {opened['days_sealed']} days")
    
    # Stats
    print(f"\n📊 Journey Stats:")
    stats = capsule.get_journey_stats()
    print(f"  Capsules Created: {stats['capsules_created']}")
    print(f"  Opened: {stats['capsules_opened']}")
    print(f"  Still Sealed: {stats['capsules_sealed']}")
    print(f"  Snapshots: {stats['snapshots_taken']}")
    print(f"  Predictions: {stats['predictions_made']}")
    
    # Year review
    print(f"\n📅 Year in Review:")
    review = capsule.get_year_in_review()
    print(f"  Capsules: {review['capsules_written']}")
    print(f"  Snapshots: {review['snapshots_taken']}")
    print(f"  Predictions: {review['predictions_made']}")
    
    # HTML
    html = capsule.generate_reflection_html()
    print(f"\n✅ Reflection page: {len(html)} chars")
    
    # Cleanup
    if os.path.exists("/tmp/demo_capsule.json"):
        os.remove("/tmp/demo_capsule.json")
    
    print(f"\n  Crochet Time Capsule Complete! 💌")
