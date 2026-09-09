"""
Crochet Challenges - Daily/weekly challenges with rewards and streaks
"""
import json
import random
from typing import Dict, List, Optional
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from pathlib import Path


@dataclass
class Challenge:
    id: str
    name: str
    description: str
    category: str
    difficulty: str
    points: int
    requirements: Dict = field(default_factory=dict)
    reward: str = ""
    expires_at: str = ""
    is_completed: bool = False
    completed_at: str = ""
    
    def to_dict(self) -> Dict:
        return asdict(self)


class ChallengeSystem:
    """
    Crochet challenge system with rewards
    
    Features:
    - Daily challenges
    - Weekly challenges
    - Monthly challenges
    - Achievement badges
    - XP and leveling system
    - Challenge streaks
    - Community challenges
    """
    
    DAILY_CHALLENGES = [
        {"name": "Starter Stitches", "desc": "Complete 10 single crochets", "category": "basic", "difficulty": "easy", "points": 10},
        {"name": "Chain Master", "desc": "Chain 50 stitches in a row", "category": "basic", "difficulty": "easy", "points": 10},
        {"name": "Round Tracker", "desc": "Complete 3 rounds of any pattern", "category": "progress", "difficulty": "easy", "points": 15},
        {"name": "Yarn Explorer", "desc": "Try a new yarn weight today", "category": "exploration", "difficulty": "medium", "points": 20},
        {"name": "Speed Demon", "desc": "Crochet for 30 minutes straight", "category": "time", "difficulty": "medium", "points": 25},
        {"name": "Color Play", "desc": "Use 3 different colors in one project", "category": "colorwork", "difficulty": "medium", "points": 20},
        {"name": "Magic Ring Master", "desc": "Start a project with magic ring", "category": "technique", "difficulty": "easy", "points": 10},
        {"name": "Count Check", "desc": "Verify stitch counts for 5 rounds", "category": "validation", "difficulty": "easy", "points": 15},
        {"name": "Photo Memory", "desc": "Take a progress photo of your WIP", "category": "documentation", "difficulty": "easy", "points": 10},
        {"name": "Pattern Reader", "desc": "Read through a full pattern before starting", "category": "preparation", "difficulty": "easy", "points": 10},
    ]
    
    WEEKLY_CHALLENGES = [
        {"name": "Finish Line", "desc": "Complete a full project this week", "category": "completion", "difficulty": "hard", "points": 100},
        {"name": "New Technique", "desc": "Learn a new stitch or technique", "category": "learning", "difficulty": "medium", "points": 50},
        {"name": "Granny Square", "desc": "Make a complete granny square", "category": "classic", "difficulty": "medium", "points": 40},
        {"name": "Amigurumi Animal", "desc": "Start or finish an amigurumi animal", "category": "amigurumi", "difficulty": "hard", "points": 75},
        {"name": "Gift Maker", "desc": "Make something as a gift for someone", "category": "gifting", "difficulty": "medium", "points": 60},
        {"name": "Stash Dive", "desc": "Use yarn from your stash you haven't touched in 6+ months", "category": "stash", "difficulty": "medium", "points": 40},
        {"name": "Pattern Tester", "desc": "Validate/test 3 patterns", "category": "validation", "difficulty": "medium", "points": 45},
    ]
    
    MONTHLY_CHALLENGES = [
        {"name": "Blanket Month", "desc": "Complete a blanket or afghan", "category": "blanket", "difficulty": "hard", "points": 300},
        {"name": "12 Squares", "desc": "Make 12 granny squares", "category": "squares", "difficulty": "hard", "points": 250},
        {"name": "Wardrobe Piece", "desc": "Make a wearable item", "category": "fashion", "difficulty": "hard", "points": 200},
        {"name": "Charity Crochet", "desc": "Make 3 items for charity", "category": "charity", "difficulty": "hard", "points": 350},
    ]
    
    ACHIEVEMENTS = {
        "first_stitch": {"name": "First Stitch", "desc": "Complete your first challenge", "icon": "🧶"},
        "streak_7": {"name": "Week Warrior", "desc": "7-day crochet streak", "icon": "🔥"},
        "streak_30": {"name": "Monthly Master", "desc": "30-day crochet streak", "icon": "🌟"},
        "streak_100": {"name": "Centurion", "desc": "100-day crochet streak", "icon": "💎"},
        "projects_5": {"name": "Productive", "desc": "Complete 5 projects", "icon": "🏆"},
        "projects_25": {"name": "Prolific", "desc": "Complete 25 projects", "icon": "👑"},
        "patterns_validated_10": {"name": "Eagle Eye", "desc": "Validate 10 patterns", "icon": "🦅"},
        "patterns_validated_50": {"name": "Quality Inspector", "desc": "Validate 50 patterns", "icon": "🔍"},
        "all_categories": {"name": "Renaissance", "desc": "Complete challenges in all categories", "icon": "🎨"},
        "night_owl": {"name": "Night Owl", "desc": "Complete a challenge after midnight", "icon": "🦉"},
        "early_bird": {"name": "Early Bird", "desc": "Complete a challenge before 7am", "icon": "🐦"},
    }
    
    LEVELS = [
        (0, "Beginner Hooker", "🧵"),
        (100, "Chain Charmer", "🪡"),
        (300, "Stitch Specialist", "🧶"),
        (600, "Pattern Pro", "📐"),
        (1000, "Yarn Yoda", "🧙"),
        (2000, "Crochet Queen/King", "👑"),
        (5000, "Legend of the Hook", "🏆"),
        (10000, "Crochet God/Goddess", "✨"),
    ]
    
    def __init__(self, storage_path: str = ".challenges.json"):
        self.storage_path = Path(storage_path)
        self.user_data = {
            "xp": 0,
            "level": 0,
            "streak": 0,
            "longest_streak": 0,
            "last_active": "",
            "completed_challenges": [],
            "unlocked_achievements": [],
            "projects_completed": 0,
            "patterns_validated": 0,
            "categories_completed": set(),
            "daily_challenge": None,
            "weekly_challenge": None,
            "monthly_challenge": None,
            "challenge_date": "",
        }
        self.load()
    
    def load(self):
        if self.storage_path.exists():
            try:
                data = json.loads(self.storage_path.read_text())
                self.user_data.update(data)
                self.user_data["categories_completed"] = set(data.get("categories_completed", []))
            except Exception:
                pass
    
    def save(self):
        data = dict(self.user_data)
        data["categories_completed"] = list(data.get("categories_completed", set()))
        self.storage_path.write_text(json.dumps(data, indent=2))
    
    def get_daily_challenge(self) -> Dict:
        """Get today's daily challenge"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        if self.user_data.get("challenge_date") != today or not self.user_data.get("daily_challenge"):
            # Generate new daily challenge
            seed = int(datetime.now().strftime("%Y%m%d"))
            random.seed(seed)
            challenge = random.choice(self.DAILY_CHALLENGES)
            self.user_data["daily_challenge"] = {
                **challenge,
                "id": f"daily_{today}",
                "completed": False
            }
            self.user_data["challenge_date"] = today
            self.save()
        
        return self.user_data["daily_challenge"]
    
    def get_weekly_challenge(self) -> Dict:
        """Get this week's challenge"""
        week_start = (datetime.now() - timedelta(days=datetime.now().weekday())).strftime("%Y-%m-%d")
        
        if (self.user_data.get("weekly_challenge") or {}).get("week") != week_start:
            seed = int(week_start.replace("-", ""))
            random.seed(seed)
            challenge = random.choice(self.WEEKLY_CHALLENGES)
            self.user_data["weekly_challenge"] = {
                **challenge,
                "id": f"weekly_{week_start}",
                "week": week_start,
                "completed": False
            }
            self.save()
        
        return self.user_data["weekly_challenge"]
    
    def complete_challenge(self, challenge_id: str) -> Dict:
        """Mark a challenge as complete"""
        result = {"success": False, "message": ""}
        
        # Check daily
        dc = self.user_data.get("daily_challenge", {})
        if dc.get("id") == challenge_id and not dc.get("completed"):
            dc["completed"] = True
            xp_earned = dc.get("points", 10)
            self.user_data["xp"] += xp_earned
            self.user_data["completed_challenges"].append(challenge_id)
            self.user_data["categories_completed"].add(dc.get("category", ""))
            result = {"success": True, "xp_earned": xp_earned, "message": f"+{xp_earned} XP!"}
            
            # Update streak
            self._update_streak()
        
        # Check weekly
        wc = self.user_data.get("weekly_challenge") or {}
        if wc.get("id") == challenge_id and not wc.get("completed"):
            wc["completed"] = True
            xp_earned = wc.get("points", 50)
            self.user_data["xp"] += xp_earned
            self.user_data["completed_challenges"].append(challenge_id)
            result = {"success": True, "xp_earned": xp_earned, "message": f"+{xp_earned} XP!"}
        
        # Check level up
        old_level = self.user_data["level"]
        new_level = self._calculate_level()
        if new_level > old_level:
            self.user_data["level"] = new_level
            result["level_up"] = True
            result["new_level"] = self.LEVELS[new_level][1]
        
        # Check achievements
        new_achievements = self._check_achievements()
        if new_achievements:
            result["new_achievements"] = new_achievements
        
        self.save()
        return result
    
    def _update_streak(self):
        """Update daily streak"""
        today = datetime.now().strftime("%Y-%m-%d")
        last = self.user_data.get("last_active", "")
        
        if last == today:
            return  # Already counted today
        
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        if last == yesterday:
            self.user_data["streak"] += 1
        else:
            self.user_data["streak"] = 1
        
        self.user_data["last_active"] = today
        if self.user_data["streak"] > self.user_data.get("longest_streak", 0):
            self.user_data["longest_streak"] = self.user_data["streak"]
    
    def _calculate_level(self) -> int:
        xp = self.user_data["xp"]
        level = 0
        for threshold, name, icon in self.LEVELS:
            if xp >= threshold:
                level = self.LEVELS.index((threshold, name, icon))
        return level
    
    def _check_achievements(self) -> List[Dict]:
        """Check for new achievements"""
        new = []
        unlocked = set(self.user_data.get("unlocked_achievements", []))
        
        if "first_stitch" not in unlocked and len(self.user_data["completed_challenges"]) >= 1:
            new.append(self.ACHIEVEMENTS["first_stitch"])
            unlocked.add("first_stitch")
        
        if "streak_7" not in unlocked and self.user_data.get("streak", 0) >= 7:
            new.append(self.ACHIEVEMENTS["streak_7"])
            unlocked.add("streak_7")
        
        if "streak_30" not in unlocked and self.user_data.get("streak", 0) >= 30:
            new.append(self.ACHIEVEMENTS["streak_30"])
            unlocked.add("streak_30")
        
        self.user_data["unlocked_achievements"] = list(unlocked)
        return new
    
    def get_profile(self) -> Dict:
        """Get user profile with stats"""
        level_data = self.LEVELS[min(self.user_data["level"], len(self.LEVELS)-1)]
        next_level = self.LEVELS[min(self.user_data["level"]+1, len(self.LEVELS)-1)]
        
        xp_for_next = next_level[0]
        xp_current = level_data[0]
        progress = ((self.user_data["xp"] - xp_current) / max(1, xp_for_next - xp_current)) * 100
        
        return {
            "level": self.user_data["level"],
            "level_name": level_data[1],
            "level_icon": level_data[2],
            "xp": self.user_data["xp"],
            "xp_for_next": xp_for_next,
            "level_progress": round(progress, 1),
            "streak": self.user_data["streak"],
            "longest_streak": self.user_data.get("longest_streak", 0),
            "challenges_completed": len(self.user_data["completed_challenges"]),
            "achievements_unlocked": len(self.user_data.get("unlocked_achievements", [])),
            "total_achievements": len(self.ACHIEVEMENTS),
            "categories": len(self.user_data.get("categories_completed", set())),
        }
    
    def display_profile(self):
        """Display user profile"""
        profile = self.get_profile()
        
        print(f"\n{'=' * 50}")
        print(f"  {profile['level_icon']} Level {profile['level']}: {profile['level_name']}")
        print(f"{'=' * 50}")
        print(f"  XP: {profile['xp']} / {profile['xp_for_next']} ({profile['level_progress']}%)")
        
        bar_width = 25
        filled = int(bar_width * profile['level_progress'] / 100)
        bar = "#" * filled + "-" * (bar_width - filled)
        print(f"  [{bar}]")
        
        print(f"\n  🔥 Streak: {profile['streak']} days (Best: {profile['longest_streak']})")
        print(f"  ✅ Challenges: {profile['challenges_completed']}")
        print(f"  🏆 Achievements: {profile['achievements_unlocked']}/{profile['total_achievements']}")
        print(f"  📂 Categories: {profile['categories']}")


# Demo
if __name__ == "__main__":
    import os
    print("\n" + "=" * 60)
    print("  CROCHET CHALLENGES - DEMONSTRATION")
    print("=" * 60)
    
    cs = ChallengeSystem(storage_path="/tmp/demo_challenges.json")
    
    # Show daily challenge
    daily = cs.get_daily_challenge()
    print(f"\n  Today's Challenge:")
    print(f"  {daily['name']}: {daily['desc']}")
    print(f"  Points: {daily['points']} XP")
    
    # Complete it
    result = cs.complete_challenge(daily["id"])
    print(f"\n  Completed! {result.get('message', '')}")
    if result.get("new_achievements"):
        for a in result["new_achievements"]:
            print(f"  🏆 Achievement unlocked: {a['icon']} {a['name']}!")
    
    # Weekly
    weekly = cs.get_weekly_challenge()
    print(f"\n  This Week's Challenge:")
    print(f"  {weekly['name']}: {weekly['desc']}")
    print(f"  Points: {weekly['points']} XP")
    
    # Show profile
    cs.display_profile()
    
    # Cleanup
    if os.path.exists("/tmp/demo_challenges.json"):
        os.remove("/tmp/demo_challenges.json")
    
    print(f"\n  Challenge System Complete!")
