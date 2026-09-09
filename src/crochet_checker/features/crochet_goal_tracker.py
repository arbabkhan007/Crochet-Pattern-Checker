"""
Crochet Goal Tracker - Set, track, and achieve crochet goals with milestones
"""
import json
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from pathlib import Path


class CrochetGoalTracker:
    """
    Set and track crochet goals
    
    Features:
    - Goal creation with deadlines
    - Progress tracking
    - Milestone celebrations
    - Goal categories
    - Streak tracking
    - Achievement system
    """
    
    GOAL_CATEGORIES = {
        "projects": {"emoji": "🧶", "name": "Projects Completed"},
        "skills": {"emoji": "🎯", "name": "New Skills Learned"},
        "time": {"emoji": "⏰", "name": "Crochet Time"},
        "stashes": {"emoji": "📦", "name": "Stash Goals"},
        "gifts": {"emoji": "🎁", "name": "Gifts Made"},
        "challenges": {"emoji": "🏆", "name": "Challenges"},
    }
    
    MILESTONES = {
        "projects_1": {"name": "First Project", "desc": "Complete your first project", "icon": "🌟"},
        "projects_10": {"name": "Productive Crafter", "desc": "Complete 10 projects", "icon": "🏅"},
        "projects_50": {"name": "Master Maker", "desc": "Complete 50 projects", "icon": "👑"},
        "projects_100": {"name": "Century Club", "desc": "Complete 100 projects", "icon": "💯"},
        "hours_10": {"name": "Getting Started", "desc": "Crochet for 10 hours", "icon": "⏰"},
        "hours_100": {"name": "Dedicated", "desc": "Crochet for 100 hours", "icon": "🎯"},
        "hours_500": {"name": "Committed", "desc": "Crochet for 500 hours", "icon": "🏆"},
        "hours_1000": {"name": "Lifetime Crafter", "desc": "Crochet for 1000 hours", "icon": "💎"},
        "streak_7": {"name": "Week Warrior", "desc": "7-day streak", "icon": "🔥"},
        "streak_30": {"name": "Monthly Master", "desc": "30-day streak", "icon": "⚡"},
        "streak_100": {"name": "Unstoppable", "desc": "100-day streak", "icon": "🌟"},
        "gifts_5": {"name": "Generous", "desc": "Give 5 handmade gifts", "icon": "🎁"},
        "gifts_20": {"name": "Gift Guru", "desc": "Give 20 handmade gifts", "icon": "💝"},
    }
    
    def __init__(self, storage_path: str = "crochet_goals.json"):
        self.storage_path = Path(storage_path)
        self.data = {
            "goals": [],
            "completed_goals": 0,
            "total_hours": 0,
            "total_projects": 0,
            "gifts_given": 0,
            "streak": 0,
            "last_crochet_date": None,
            "milestones_earned": [],
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
    
    def set_goal(self, title: str, category: str, target: int,
                deadline: str = None, description: str = "") -> Dict:
        """Set a new goal"""
        goal = {
            "id": f"G{len(self.data['goals']) + 1:04d}",
            "title": title,
            "category": category,
            "target": target,
            "current": 0,
            "deadline": deadline,
            "description": description,
            "status": "active",
            "created": datetime.now().strftime("%Y-%m-%d"),
            "completed": None,
        }
        
        self.data["goals"].append(goal)
        self.save()
        
        return goal
    
    def update_progress(self, goal_id: str, progress: int) -> Dict:
        """Update goal progress"""
        goal = next((g for g in self.data["goals"] if g["id"] == goal_id), None)
        if not goal:
            return {"error": "Goal not found"}
        
        goal["current"] = progress
        new_milestones = []
        
        # Check if goal completed
        if progress >= goal["target"] and goal["status"] == "active":
            goal["status"] = "completed"
            goal["completed"] = datetime.now().strftime("%Y-%m-%d")
            self.data["completed_goals"] += 1
            
            # Update global stats
            if goal["category"] == "projects":
                self.data["total_projects"] += progress
            elif goal["category"] == "time":
                self.data["total_hours"] += progress
            elif goal["category"] == "gifts":
                self.data["gifts_given"] += progress
            
            # Check milestones
            new_milestones = self._check_milestones()
        
        self.save()
        
        return {
            "goal": goal["title"],
            "progress": f"{progress}/{goal['target']}",
            "percentage": round(progress / goal["target"] * 100, 1),
            "completed": goal["status"] == "completed",
            "new_milestones": new_milestones,
        }
    
    def log_crochet_session(self, hours: float = 1) -> Dict:
        """Log a crochet session and update streak"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        if self.data["last_crochet_date"] == today:
            # Already logged today
            self.data["total_hours"] += hours
            self.save()
            return {"message": "Session logged", "streak": self.data["streak"],
                    "total_hours": round(self.data["total_hours"], 1),
                    "hours_logged": hours, "new_milestones": []}
        
        # Check if streak continues
        if self.data["last_crochet_date"]:
            yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
            if self.data["last_crochet_date"] == yesterday:
                self.data["streak"] += 1
            else:
                self.data["streak"] = 1
        else:
            self.data["streak"] = 1
        
        self.data["last_crochet_date"] = today
        self.data["total_hours"] += hours
        
        new_milestones = self._check_milestones()
        self.save()
        
        return {
            "hours_logged": hours,
            "total_hours": round(self.data["total_hours"], 1),
            "streak": self.data["streak"],
            "new_milestones": new_milestones,
        }
    
    def _check_milestones(self) -> List[str]:
        """Check for newly earned milestones"""
        new = []
        
        checks = {
            "projects_1": self.data["total_projects"] >= 1,
            "projects_10": self.data["total_projects"] >= 10,
            "projects_50": self.data["total_projects"] >= 50,
            "projects_100": self.data["total_projects"] >= 100,
            "hours_10": self.data["total_hours"] >= 10,
            "hours_100": self.data["total_hours"] >= 100,
            "hours_500": self.data["total_hours"] >= 500,
            "hours_1000": self.data["total_hours"] >= 1000,
            "streak_7": self.data["streak"] >= 7,
            "streak_30": self.data["streak"] >= 30,
            "streak_100": self.data["streak"] >= 100,
            "gifts_5": self.data["gifts_given"] >= 5,
            "gifts_20": self.data["gifts_given"] >= 20,
        }
        
        for milestone_id, achieved in checks.items():
            if achieved and milestone_id not in self.data["milestones_earned"]:
                self.data["milestones_earned"].append(milestone_id)
                new.append(milestone_id)
        
        return new
    
    def get_dashboard(self) -> Dict:
        """Get goal tracking dashboard"""
        active_goals = [g for g in self.data["goals"] if g["status"] == "active"]
        completed_goals = [g for g in self.data["goals"] if g["status"] == "completed"]
        
        # Upcoming deadlines
        today = datetime.now()
        upcoming = []
        for g in active_goals:
            if g.get("deadline"):
                try:
                    dl = datetime.strptime(g["deadline"], "%Y-%m-%d")
                    days = (dl - today).days
                    if days >= 0:
                        upcoming.append({**g, "days_left": days})
                except ValueError:
                    pass
        
        upcoming.sort(key=lambda x: x["days_left"])
        
        return {
            "total_hours": round(self.data["total_hours"], 1),
            "total_projects": self.data["total_projects"],
            "gifts_given": self.data["gifts_given"],
            "streak": self.data["streak"],
            "active_goals": len(active_goals),
            "completed_goals": len(completed_goals),
            "milestones_earned": len(self.data["milestones_earned"]),
            "upcoming_deadlines": upcoming[:5],
            "active_goal_list": active_goals,
        }
    
    def get_milestones_display(self) -> List[Dict]:
        """Get all milestones with earned status"""
        milestones = []
        for mid, info in self.MILESTONES.items():
            milestones.append({
                "id": mid,
                "name": info["name"],
                "desc": info["desc"],
                "icon": info["icon"],
                "earned": mid in self.data["milestones_earned"],
            })
        return milestones


# Demo
if __name__ == "__main__":
    import os
    print("\n" + "=" * 60)
    print("  CROCHET GOAL TRACKER - DEMONSTRATION")
    print("=" * 60)
    
    tracker = CrochetGoalTracker(storage_path="/tmp/demo_goals.json")
    
    # Set goals
    g1 = tracker.set_goal("Finish 5 blankets", "projects", 5, description="For charity")
    g2 = tracker.set_goal("Crochet 20 hours this month", "time", 20)
    g3 = tracker.set_goal("Make 10 holiday gifts", "gifts", 10, 
                         deadline=(datetime.now() + timedelta(days=60)).strftime("%Y-%m-%d"))
    print(f"✅ Set 3 goals")
    
    # Update progress
    print(f"\n📈 Updating progress...")
    result = tracker.update_progress(g1["id"], 3)
    print(f"  {result['goal']}: {result['progress']} ({result['percentage']}%)")
    
    result = tracker.update_progress(g2["id"], 12)
    print(f"  {result['goal']}: {result['progress']} ({result['percentage']}%)")
    
    # Log sessions
    print(f"\n⏰ Logging sessions...")
    for _ in range(5):
        session = tracker.log_crochet_session(hours=2)
    
    print(f"  Total hours: {session['total_hours']}")
    print(f"  Current streak: {session['streak']} days")
    
    if session.get("new_milestones"):
        for m in session["new_milestones"]:
            info = tracker.MILESTONES[m]
            print(f"  🏆 Milestone: {info['icon']} {info['name']}!")
    
    # Dashboard
    print(f"\n📊 Goal Dashboard:")
    dash = tracker.get_dashboard()
    print(f"  Total Hours: {dash['total_hours']}")
    print(f"  Total Projects: {dash['total_projects']}")
    print(f"  Gifts Given: {dash['gifts_given']}")
    print(f"  Streak: {dash['streak']} days")
    print(f"  Active Goals: {dash['active_goals']}")
    print(f"  Completed: {dash['completed_goals']}")
    
    if dash["upcoming_deadlines"]:
        print(f"\n  Upcoming Deadlines:")
        for g in dash["upcoming_deadlines"]:
            print(f"    ⏰ {g['title']} - {g['days_left']} days left")
    
    # Milestones
    print(f"\n🏆 Milestones:")
    milestones = tracker.get_milestones_display()
    earned = [m for m in milestones if m["earned"]]
    for m in earned:
        print(f"  {m['icon']} {m['name']} - {m['desc']}")
    
    # Cleanup
    if os.path.exists("/tmp/demo_goals.json"):
        os.remove("/tmp/demo_goals.json")
    
    print(f"\n  Crochet Goal Tracker Complete! 🎯")
