"""
AI Yarn Recommender - Smart yarn suggestions based on project, budget, and preferences
"""
import json
from typing import Dict, List, Optional
from datetime import datetime


class AIYarnRecommender:
    """
    AI-powered yarn recommendations
    
    Features:
    - Project-based suggestions
    - Budget filtering
    - Color palette matching
    - Fiber preference learning
    - Substitute recommendations
    - Seasonal suggestions
    """
    
    YARN_DATABASE = [
        {"name": "Red Heart Super Saver", "brand": "Red Heart", "weight": "worsted",
         "fiber": "acrylic", "yardage": 364, "price": 4.99, "colors": 50,
         "best_for": ["blankets", "scarves", "amigurumi"], "season": "all"},
        {"name": "Scheepjes Catona", "brand": "Scheepjes", "weight": "dk",
         "fiber": "cotton", "yardage": 50, "price": 2.50, "colors": 100,
         "best_for": ["amigurumi", "dishcloths", "doilies"], "season": "all"},
        {"name": "Malabrigo Rios", "brand": "Malabrigo", "weight": "worsted",
         "fiber": "merino", "yardage": 210, "price": 15.99, "colors": 60,
         "best_for": ["scarves", "shawls", "garments"], "season": "fall"},
        {"name": "Lily Sugar'n Cream", "brand": "Lily", "weight": "worsted",
         "fiber": "cotton", "yardage": 120, "price": 2.49, "colors": 20,
         "best_for": ["dishcloths", "market bags", "tops"], "season": "summer"},
        {"name": "Cascade 220", "brand": "Cascade", "weight": "worsted",
         "fiber": "wool", "yardage": 220, "price": 9.99, "colors": 100,
         "best_for": ["sweaters", "hats", "mittens"], "season": "winter"},
        {"name": "WeCrochet Brava", "brand": "WeCrochet", "weight": "dk",
         "fiber": "acrylic", "yardage": 218, "price": 3.99, "colors": 80,
         "best_for": ["garments", "blankets", "accessories"], "season": "all"},
    ]
    
    SEASONAL_PREFERENCES = {
        "winter": ["wool", "acrylic", "alpaca"],
        "spring": ["cotton", "bamboo", "merino"],
        "summer": ["cotton", "linen", "bamboo"],
        "fall": ["wool", "merino", "acrylic"],
    }
    
    def __init__(self, storage_path: str = "yarn_preferences.json"):
        self.storage_path = storage_path
        self.preferences = self._load_preferences()
    
    def _load_preferences(self) -> Dict:
        """Load user preferences"""
        try:
            with open(self.storage_path, 'r') as f:
                return json.load(f)
        except:
            return {
                "favorite_fibers": [],
                "favorite_brands": [],
                "budget_range": [0, 100],
                "color_preferences": [],
            }
    
    def save_preferences(self):
        """Save user preferences"""
        with open(self.storage_path, 'w') as f:
            json.dump(self.preferences, f, indent=2)
    
    def recommend_yarn(self, project_type: str, budget: float = None,
                      season: str = None, difficulty: str = "beginner") -> Dict:
        """
        Recommend yarns for a project
        
        Args:
            project_type: What you're making
            budget: Max budget in dollars
            season: Current season
            difficulty: Skill level
        
        Returns:
            Dict with recommendations
        """
        # Filter yarns
        candidates = self.YARN_DATABASE.copy()
        
        # Filter by project type
        candidates = [y for y in candidates if project_type.lower() in 
                     [b.lower() for b in y.get("best_for", [])]]
        
        # Filter by budget
        if budget:
            candidates = [y for y in candidates if y["price"] <= budget]
        
        # Filter by season
        if season:
            seasonal_fibers = self.SEASONAL_PREFERENCES.get(season.lower(), [])
            candidates = [y for y in candidates if y["fiber"].lower() in 
                         [f.lower() for f in seasonal_fibers]]
        
        # Filter by difficulty
        if difficulty == "beginner":
            # Prefer easy-care fibers
            candidates = sorted(candidates, 
                              key=lambda y: 0 if y["fiber"] in ["acrylic", "cotton"] else 1)
        elif difficulty == "advanced":
            # Can handle delicate fibers
            candidates = sorted(candidates,
                              key=lambda y: 0 if y["fiber"] in ["merino", "silk", "alpaca"] else 1)
        
        # Score each yarn
        scored = []
        for yarn in candidates[:10]:
            score = self._score_yarn(yarn, project_type, season, difficulty)
            scored.append({**yarn, "score": score})
        
        # Sort by score
        scored.sort(key=lambda y: y["score"], reverse=True)
        
        return {
            "project_type": project_type,
            "recommendations": scored[:5],
            "total_matches": len(scored),
            "filters_applied": {
                "budget": budget,
                "season": season,
                "difficulty": difficulty,
            },
        }
    
    def _score_yarn(self, yarn: Dict, project_type: str, 
                   season: str, difficulty: str) -> float:
        """Score a yarn based on multiple factors"""
        score = 0.0
        
        # Project match (0-40 points)
        if project_type.lower() in [b.lower() for b in yarn.get("best_for", [])]:
            score += 40
        elif any(project_type.lower() in b.lower() for b in yarn.get("best_for", [])):
            score += 20
        
        # Season match (0-20 points)
        if season:
            if yarn.get("season", "all") == "all":
                score += 15
            elif yarn.get("season", "").lower() == season.lower():
                score += 20
        
        # Price value (0-20 points)
        price_per_yard = yarn["price"] / max(1, yarn["yardage"])
        if price_per_yard < 0.02:
            score += 20
        elif price_per_yard < 0.05:
            score += 15
        else:
            score += 10
        
        # Color variety (0-10 points)
        if yarn.get("colors", 0) >= 50:
            score += 10
        elif yarn.get("colors", 0) >= 20:
            score += 7
        else:
            score += 5
        
        # Fiber care (0-10 points)
        if difficulty == "beginner":
            if yarn["fiber"].lower() in ["acrylic", "cotton"]:
                score += 10  # Easy care
            else:
                score += 5
        else:
            score += 8  # Any fiber OK
        
        return round(score, 1)
    
    def find_substitute(self, original_yarn: str, project_type: str = "") -> Dict:
        """Find substitute yarns"""
        # Find original yarn
        original = None
        for yarn in self.YARN_DATABASE:
            if original_yarn.lower() in yarn["name"].lower():
                original = yarn
                break
        
        if not original:
            return {"error": f"Yarn '{original_yarn}' not found"}
        
        # Find substitutes with same weight
        substitutes = [y for y in self.YARN_DATABASE 
                      if y["weight"] == original["weight"] 
                      and y["name"] != original["name"]]
        
        # Score substitutes
        scored = []
        for yarn in substitutes:
            score = 0
            if yarn["fiber"] == original["fiber"]:
                score += 30
            if abs(yarn["yardage"] - original["yardage"]) < 50:
                score += 20
            if abs(yarn["price"] - original["price"]) < 3:
                score += 20
            
            if project_type:
                if project_type.lower() in [b.lower() for b in yarn.get("best_for", [])]:
                    score += 30
            
            scored.append({**yarn, "match_score": score})
        
        scored.sort(key=lambda y: y["match_score"], reverse=True)
        
        return {
            "original": original,
            "substitutes": scored[:5],
            "suggestion": f"Best match: {scored[0]['name']} (score: {scored[0]['match_score']}/100)" if scored else "No good substitutes found",
        }
    
    def suggest_color_palette(self, project_type: str, season: str = None) -> Dict:
        """Suggest color palettes"""
        palettes = {
            "winter": {
                "cozy": ["burgundy", "navy", "cream", "forest green"],
                "festive": ["red", "green", "gold", "white"],
            },
            "spring": {
                "fresh": ["pastel pink", "mint", "lavender", "sky blue"],
                "bright": ["coral", "turquoise", "yellow", "lime"],
            },
            "summer": {
                "beach": ["aqua", "sand", "coral", "white"],
                "tropical": ["hot pink", "orange", "turquoise", "yellow"],
            },
            "fall": {
                "harvest": ["pumpkin", "mustard", "burgundy", "olive"],
                "cozy": ["charcoal", "rust", "cream", "navy"],
            },
        }
        
        if season:
            season_palettes = palettes.get(season.lower(), palettes["fall"])
        else:
            season_palettes = palettes["fall"]  # Default
        
        return {
            "season": season or "fall",
            "palettes": season_palettes,
            "project_type": project_type,
        }
    
    def learn_preference(self, yarn_name: str, liked: bool = True):
        """Learn from user feedback"""
        for yarn in self.YARN_DATABASE:
            if yarn_name.lower() in yarn["name"].lower():
                if liked:
                    if yarn["brand"] not in self.preferences["favorite_brands"]:
                        self.preferences["favorite_brands"].append(yarn["brand"])
                    if yarn["fiber"] not in self.preferences["favorite_fibers"]:
                        self.preferences["favorite_fibers"].append(yarn["fiber"])
                break
        
        self.save_preferences()


# Demo
if __name__ == "__main__":
    import os
    print("\n" + "=" * 60)
    print("  AI YARN RECOMMENDER - DEMONSTRATION")
    print("=" * 60)
    
    rec = AIYarnRecommender(storage_path="/tmp/demo_yarn_prefs.json")
    
    # Get recommendations
    print("\n🧶 Recommending yarn for scarf...")
    results = rec.recommend_yarn("scarf", budget=10, season="winter")
    print(f"  Found {results['total_matches']} matches")
    for i, yarn in enumerate(results["recommendations"][:3], 1):
        print(f"  {i}. {yarn['name']} - ${yarn['price']} (score: {yarn['score']})")
    
    # Find substitute
    print("\n🔄 Finding substitutes for Malabrigo Rios...")
    subs = rec.find_substitute("Malabrigo Rios", "scarf")
    if "error" not in subs:
        print(f"  Original: {subs['original']['name']}")
        print(f"  {subs['suggestion']}")
        for i, yarn in enumerate(subs["substitutes"][:3], 1):
            print(f"  {i}. {yarn['name']} (match: {yarn['match_score']})")
    
    # Color palette
    print("\n🎨 Winter Color Palette:")
    palette = rec.suggest_color_palette("scarf", "winter")
    for style, colors in palette["palettes"].items():
        print(f"  {style.title()}: {', '.join(colors)}")
    
    # Learn preference
    print("\n📚 Learning preferences...")
    rec.learn_preference("Red Heart Super Saver", liked=True)
    print(f"  Favorite brands: {rec.preferences['favorite_brands']}")
    print(f"  Favorite fibers: {rec.preferences['favorite_fibers']}")
    
    # Cleanup
    if os.path.exists("/tmp/demo_yarn_prefs.json"):
        os.remove("/tmp/demo_yarn_prefs.json")
    
    print(f"\n  AI Yarn Recommender Complete! 🧶")
