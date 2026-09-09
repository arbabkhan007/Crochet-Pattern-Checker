"""
Crochet Challenge Generator - Random fun challenges to keep you inspired
"""
import random
from typing import Dict, List
from datetime import datetime


class CrochetChallengeGenerator:
    """
    Generate fun crochet challenges
    
    Features:
    - Random challenges
    - Time-based challenges
    - Color challenges
    - Technique challenges
    - Charity challenges
    - Challenge tracking
    """
    
    CHALLENGES = {
        "speed": [
            "Crochet a complete amigurumi in under 2 hours",
            "Make a scarf in one sitting",
            "Finish a granny square blanket in a weekend",
            "Complete 5 dishcloths in one day",
            "Make a hat in under 3 hours",
        ],
        "color": [
            "Use only 2 colors to make a striking design",
            "Create a rainbow project (7 colors)",
            "Make something using only variegated yarn",
            "Try color pooling intentionally",
            "Use leftover scraps for a whole project",
        ],
        "technique": [
            "Learn and use a stitch you've never tried",
            "Make something with cables",
            "Try tapestry crochet",
            "Learn Tunisian crochet",
            "Make something with hairpin lace",
            "Try broomstick lace",
        ],
        "charity": [
            "Make 10 hats for a homeless shelter",
            "Crochet blankets for 5 premature babies",
            "Make comfort dolls for a children's hospital",
            "Create scarves for 10 people in need",
            "Make shawls for a nursing home",
        ],
        "creative": [
            "Design your own original pattern",
            "Make something inspired by nature",
            "Create a crochet piece of art",
            "Make an item for a room you don't usually crochet for",
            "Crochet something completely impractical but fun",
            "Make a miniature version of something large",
        ],
        "streak": [
            "Crochet every day for 7 days straight",
            "Crochet for 30 minutes every day this week",
            "Complete one small project every day for 5 days",
            "Learn one new stitch every day for a week",
            "Crochet for 100 hours this month",
        ],
        "skill": [
            "Perfect your gauge swatch",
            "Learn to read a crochet chart",
            "Master invisible decreases",
            "Learn 3 new stitches this week",
            "Make your first garment",
            "Try working without a pattern",
        ],
        "fun": [
            "Make a crochet pet",
            "Crochet your favorite food",
            "Make something with glow-in-the-dark yarn",
            "Create a crochet version of your logo",
            "Make matching sets for friends",
            "Crochet something from your childhood memories",
        ],
    }
    
    MONTHLY_THEMES = {
        1: {"name": "Warmth", "emoji": "❄️", "focus": "Winter items"},
        2: {"name": "Love", "emoji": "❤️", "focus": "Gifts for others"},
        3: {"name": "Growth", "emoji": "🌱", "focus": "Learning new skills"},
        4: {"name": "Renewal", "emoji": "🌸", "focus": "Spring cleaning stash"},
        5: {"name": "Joy", "emoji": "🌞", "focus": "Bright colorful projects"},
        6: {"name": "Adventure", "emoji": "🏖️", "focus": "Summer accessories"},
        7: {"name": "Freedom", "emoji": "🎆", "focus": "Bold design choices"},
        8: {"name": "Harvest", "emoji": "🌾", "focus": "Autumn prep"},
        9: {"name": "Balance", "emoji": "🍂", "focus": "WIP completion"},
        10: {"name": "Spooky", "emoji": "🎃", "focus": "Halloween items"},
        11: {"name": "Gratitude", "emoji": "🙏", "focus": "Thank you gifts"},
        12: {"name": "Celebration", "emoji": "🎄", "focus": "Holiday making"},
    }
    
    def generate_random_challenge(self, category: str = None) -> Dict:
        """Generate a random challenge"""
        if category:
            challenges = self.CHALLENGES.get(category, [])
        else:
            all_challenges = []
            for cat_challenges in self.CHALLENGES.values():
                all_challenges.extend(cat_challenges)
            challenges = all_challenges
        
        if not challenges:
            return {"error": "No challenges found"}
        
        challenge = random.choice(challenges)
        category_used = category or random.choice(list(self.CHALLENGES.keys()))
        
        return {
            "challenge": challenge,
            "category": category_used,
            "difficulty": random.choice(["Easy", "Medium", "Hard"]),
            "time_estimate": random.choice(["1-2 hours", "3-5 hours", "1 day", "1 week"]),
            "motivation": self._get_motivation(),
        }
    
    def _get_motivation(self) -> str:
        """Get a motivational message"""
        motivations = [
            "You've got this! Every stitch counts! 💪",
            "Challenge yourself, grow as a crafter! 🌟",
            "The journey is the reward! 🧶",
            "Believe in your hands! They create magic! ✨",
            "Every expert was once a beginner! 🎯",
            "Small steps lead to big accomplishments! 🚀",
            "Your creativity is limitless! 🎨",
            "Enjoy the process, not just the result! 😊",
        ]
        return random.choice(motivations)
    
    def generate_daily_challenge(self) -> Dict:
        """Generate a challenge for today"""
        today = datetime.now()
        day_of_year = today.timetuple().tm_yday
        
        # Use day of year to pick consistent challenge
        random.seed(day_of_year + today.year)
        challenge = self.generate_random_challenge()
        random.seed()  # Reset seed
        
        return {
            **challenge,
            "date": today.strftime("%Y-%m-%d"),
            "is_daily": True,
        }
    
    def get_monthly_theme(self, month: int = None) -> Dict:
        """Get monthly theme"""
        if month is None:
            month = datetime.now().month
        
        theme = self.MONTHLY_THEMES.get(month, self.MONTHLY_THEMES[1])
        
        return {
            **theme,
            "month": month,
            "challenge_ideas": self._get_theme_challenges(month),
        }
    
    def _get_theme_challenges(self, month: int) -> List[str]:
        """Get challenge ideas for a monthly theme"""
        ideas = {
            1: ["Make a cozy hat", "Crochet warm mittens", "Create a scarf"],
            2: ["Make a heart amigurumi", "Crochet a gift for someone special", "Create something pink or red"],
            3: ["Learn a new stitch", "Start a skill-building project", "Try a technique tutorial"],
            4: ["Organize your yarn stash", "Use up scraps", "Clean your crochet tools"],
            5: ["Make something bright yellow", "Create a sunshine project", "Use cheerful colors"],
            6: ["Crochet a beach bag", "Make a sun hat", "Create summer accessories"],
            7: ["Try bold color combinations", "Make a statement piece", "Experiment with texture"],
            8: ["Start autumn prep", "Make warm items", "Use fall colors"],
            9: ["Finish a WIP", "Complete an unfinished project", "Clear your project queue"],
            10: ["Make Halloween decorations", "Crochet a spooky amigurumi", "Create orange/black items"],
            11: ["Make thank you gifts", "Crochet for charity", "Give back to your community"],
            12: ["Holiday decorations", "Gift making", "Festive amigurumi"],
        }
        return ideas.get(month, [])
    
    def generate_7_day_challenge(self) -> Dict:
        """Generate a 7-day challenge"""
        days = []
        categories = list(self.CHALLENGES.keys())
        
        for i in range(7):
            cat = categories[i % len(categories)]
            challenge = random.choice(self.CHALLENGES[cat])
            days.append({
                "day": i + 1,
                "category": cat,
                "challenge": challenge,
            })
        
        return {
            "name": "7-Day Crochet Challenge",
            "days": days,
            "motivation": "One challenge per day for a week! You've got this!",
        }
    
    def get_challenge_stats(self, completed: List[str]) -> Dict:
        """Get stats for completed challenges"""
        total = len(completed)
        
        return {
            "completed": total,
            "message": self._get_completion_message(total),
        }
    
    def _get_completion_message(self, count: int) -> str:
        """Get message based on completion count"""
        if count == 0:
            return "No challenges completed yet. Pick one today!"
        elif count < 5:
            return f"Great start! {count} challenges conquered!"
        elif count < 10:
            return f"Impressive! {count} challenges done! You're on fire!"
        else:
            return f"Amazing! {count} challenges! You're a crochet champion!"


# Demo
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  CROCHET CHALLENGE GENERATOR - DEMONSTRATION")
    print("=" * 60)
    
    gen = CrochetChallengeGenerator()
    
    # Random challenges
    print(f"\n🎲 Random Challenges:")
    for i in range(3):
        challenge = gen.generate_random_challenge()
        print(f"  [{challenge['category'].upper()}] {challenge['challenge']}")
        print(f"    Difficulty: {challenge['difficulty']} | Time: {challenge['time_estimate']}")
        print(f"    {challenge['motivation']}\n")
    
    # Category-specific
    print(f"\n🎯 Charity Challenge:")
    charity = gen.generate_random_challenge("charity")
    print(f"  {charity['challenge']}")
    
    print(f"\n🌈 Color Challenge:")
    color = gen.generate_random_challenge("color")
    print(f"  {color['challenge']}")
    
    # Daily challenge
    print(f"\n📅 Today's Challenge:")
    daily = gen.generate_daily_challenge()
    print(f"  {daily['challenge']}")
    print(f"  Category: {daily['category']} | {daily['motivation']}")
    
    # Monthly theme
    print(f"\n🗓️  This Month's Theme:")
    theme = gen.get_monthly_theme()
    print(f"  {theme['emoji']} {theme['name']}")
    print(f"  Focus: {theme['focus']}")
    print(f"  Ideas: {', '.join(theme['challenge_ideas'][:3])}")
    
    # 7-day challenge
    print(f"\n🔥 7-Day Challenge:")
    week = gen.generate_7_day_challenge()
    print(f"  {week['name']}")
    print(f"  {week['motivation']}\n")
    for day in week['days']:
        print(f"  Day {day['day']}: [{day['category']}] {day['challenge']}")
    
    # Stats
    print(f"\n📊 Challenge Stats:")
    stats = gen.get_challenge_stats(["challenge1", "challenge2", "challenge3"])
    print(f"  {stats['message']}")
    
    print(f"\n  Crochet Challenge Generator Complete! 🎯")
