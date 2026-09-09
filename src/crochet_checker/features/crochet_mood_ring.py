"""
Crochet Mood Ring - Suggest what to crochet based on your current mood
"""
import random
from typing import Dict, List


class CrochetMoodRing:
    """
    Suggest crochet projects based on your mood
    
    Features:
    - Mood-based project suggestions
    - Energy level matching
    - Time available filtering
    - Skill level consideration
    - Seasonal recommendations
    """
    
    MOODS = {
        "happy": {
            "emoji": "😊",
            "energy": "high",
            "suggestions": [
                {"project": "Colorful Granny Square Blanket", "difficulty": "intermediate", "time": "15+ hours", "why": "Bright colors match your mood!"},
                {"project": "Rainbow Amigurumi Set", "difficulty": "beginner", "time": "8 hours", "why": "Fun and playful!"},
                {"project": "Floral Mandala", "difficulty": "advanced", "time": "10 hours", "why": "Beautiful and rewarding"},
            ]
        },
        "calm": {
            "emoji": "😌",
            "energy": "medium",
            "suggestions": [
                {"project": "Simple Scarf in Soft Yarn", "difficulty": "beginner", "time": "6 hours", "why": "Mindless and soothing"},
                {"project": "Repeating Stitch Blanket", "difficulty": "beginner", "time": "20 hours", "why": "Rhythmic and meditative"},
                {"project": "Lace Doily", "difficulty": "advanced", "time": "12 hours", "why": "Peaceful precision"},
            ]
        },
        "stressed": {
            "emoji": "😰",
            "energy": "low",
            "suggestions": [
                {"project": "Simple Dishcloths", "difficulty": "beginner", "time": "2 hours", "why": "Quick wins reduce stress"},
                {"project": "Chunky Cowl", "difficulty": "beginner", "time": "3 hours", "why": "Fast and cozy"},
                {"project": "Fingerless Gloves", "difficulty": "beginner", "time": "4 hours", "why": "Small and satisfying"},
            ]
        },
        "creative": {
            "emoji": "🎨",
            "energy": "high",
            "suggestions": [
                {"project": "Design Your Own Pattern", "difficulty": "advanced", "time": "10+ hours", "why": "Channel that creativity!"},
                {"project": "Freeform Crochet Art", "difficulty": "intermediate", "time": "8 hours", "why": "No rules, just expression"},
                {"project": "Mosaic Colorwork", "difficulty": "advanced", "time": "15 hours", "why": "Complex and beautiful"},
            ]
        },
        "bored": {
            "emoji": "😐",
            "energy": "low",
            "suggestions": [
                {"project": "Learn a New Stitch", "difficulty": "intermediate", "time": "3 hours", "why": "Challenge yourself!"},
                {"project": "Amigurumi Animal", "difficulty": "intermediate", "time": "6 hours", "why": "Fun and engaging"},
                {"project": "Complex Lace Shawl", "difficulty": "advanced", "time": "20 hours", "why": "Keeps your mind busy"},
            ]
        },
        "nostalgic": {
            "emoji": "🥺",
            "energy": "medium",
            "suggestions": [
                {"project": "Vintage Lace Collar", "difficulty": "advanced", "time": "8 hours", "why": "Classic and timeless"},
                {"project": "Traditional Afghan", "difficulty": "intermediate", "time": "25 hours", "why": "Heirloom quality"},
                {"project": "Antique-Style Doilies", "difficulty": "advanced", "time": "10 hours", "why": "Old-world charm"},
            ]
        },
        "energetic": {
            "emoji": "⚡",
            "energy": "high",
            "suggestions": [
                {"project": "Quick Amigurumi Batch", "difficulty": "beginner", "time": "8 hours", "why": "Make multiple small items fast"},
                {"project": "Striped T-Shirt Yarn Basket", "difficulty": "beginner", "time": "4 hours", "why": "Fast and practical"},
                {"project": "Beanie Collection", "difficulty": "beginner", "time": "6 hours", "why": "Quick projects, big impact"},
            ]
        },
        "focused": {
            "emoji": "🎯",
            "energy": "high",
            "suggestions": [
                {"project": "Intricate Lace Shawl", "difficulty": "advanced", "time": "30 hours", "why": "Requires concentration"},
                {"project": "Tapestry Crochet Bag", "difficulty": "advanced", "time": "12 hours", "why": "Complex colorwork"},
                {"project": "Fitted Garment", "difficulty": "advanced", "time": "20 hours", "why": "Precision required"},
            ]
        },
    }
    
    SEASONAL_SUGGESTIONS = {
        "winter": ["Chunky Scarf", "Warm Hat", "Mittens", "Cozy Blanket"],
        "spring": ["Floral Doily", "Light Cardigan", "Easter Bunny", "Garden Gloves"],
        "summer": ["Beach Bag", "Crop Top", "Sun Hat", "Market Tote"],
        "fall": ["Pumpkin Set", "Autumn Leaves", "Warm Socks", "Harvest Table Runner"],
    }
    
    def suggest_by_mood(self, mood: str, energy_level: str = None,
                       time_available: str = None) -> Dict:
        """Get project suggestions based on mood"""
        mood_data = self.MOODS.get(mood.lower(), self.MOODS["calm"])
        
        suggestions = mood_data["suggestions"].copy()
        
        # Filter by energy if provided
        if energy_level:
            energy_map = {"low": ["beginner"], "medium": ["beginner", "intermediate"], "high": ["beginner", "intermediate", "advanced"]}
            allowed = energy_map.get(energy_level, ["beginner", "intermediate", "advanced"])
            suggestions = [s for s in suggestions if s["difficulty"] in allowed]
        
        # Filter by time if provided
        if time_available:
            time_map = {"quick": ["1-3 hours", "2 hours", "3 hours", "4 hours"],
                       "medium": ["6 hours", "8 hours", "10 hours"],
                       "long": ["15+ hours", "20 hours", "25 hours", "30 hours"]}
            allowed_times = time_map.get(time_available, [])
            if allowed_times:
                suggestions = [s for s in suggestions if s["time"] in allowed_times]
        
        return {
            "mood": mood,
            "emoji": mood_data["emoji"],
            "suggestions": suggestions if suggestions else mood_data["suggestions"],
            "tip": self._get_mood_tip(mood),
        }
    
    def _get_mood_tip(self, mood: str) -> str:
        """Get a tip for the mood"""
        tips = {
            "happy": "Your positive energy is perfect for colorful, complex projects!",
            "calm": "Enjoy the meditative rhythm of repetitive stitches.",
            "stressed": "Start small. Quick wins will boost your mood.",
            "creative": "Don't be afraid to experiment and break the rules!",
            "bored": "Challenge yourself with something new!",
            "nostalgic": "Classic patterns connect us to crochet traditions.",
            "energetic": "Batch-make small items for maximum satisfaction!",
            "focused": "Complex patterns need your attention - perfect time!",
        }
        return tips.get(mood.lower(), "Enjoy your crochet time!")
    
    def suggest_by_season(self, season: str) -> Dict:
        """Get seasonal suggestions"""
        items = self.SEASONAL_SUGGESTIONS.get(season.lower(), [])
        return {
            "season": season,
            "suggestions": items,
        }
    
    def get_daily_suggestion(self) -> Dict:
        """Get a random daily suggestion"""
        mood = random.choice(list(self.MOODS.keys()))
        suggestion = random.choice(self.MOODS[mood]["suggestions"])
        
        return {
            "mood": mood,
            "emoji": self.MOODS[mood]["emoji"],
            "project": suggestion["project"],
            "difficulty": suggestion["difficulty"],
            "time": suggestion["time"],
            "why": suggestion["why"],
        }
    
    def quick_pick(self) -> Dict:
        """Quick random pick"""
        all_suggestions = []
        for mood_data in self.MOODS.values():
            all_suggestions.extend(mood_data["suggestions"])
        
        pick = random.choice(all_suggestions)
        return pick


# Demo
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  CROCHET MOOD RING - DEMONSTRATION")
    print("=" * 60)
    
    ring = CrochetMoodRing()
    
    # Test different moods
    for mood in ["happy", "stressed", "creative", "focused"]:
        print(f"\n{ring.MOODS[mood]['emoji']} Mood: {mood.upper()}")
        result = ring.suggest_by_mood(mood)
        for s in result["suggestions"][:2]:
            print(f"  • {s['project']} ({s['difficulty']}, {s['time']})")
            print(f"    Why: {s['why']}")
        print(f"  💡 {result['tip']}")
    
    # Filtered suggestions
    print(f"\n🎯 Stressed + Low Energy + Quick:")
    result = ring.suggest_by_mood("stressed", energy_level="low", time_available="quick")
    for s in result["suggestions"]:
        print(f"  • {s['project']}")
    
    # Seasonal
    print(f"\n🍂 Fall Suggestions:")
    seasonal = ring.suggest_by_season("fall")
    for item in seasonal["suggestions"]:
        print(f"  • {item}")
    
    # Daily suggestion
    print(f"\n✨ Today's Suggestion:")
    daily = ring.get_daily_suggestion()
    print(f"  {daily['emoji']} {daily['project']}")
    print(f"  ({daily['difficulty']}, {daily['time']})")
    print(f"  {daily['why']}")
    
    # Quick pick
    print(f"\n🎲 Random Pick:")
    pick = ring.quick_pick()
    print(f"  {pick['project']}")
    
    print(f"\n  Crochet Mood Ring Complete! 💫")
