"""
Smart Yarn Substitution AI - Find perfect yarn alternatives
When your specified yarn is out of stock or unavailable
"""
import json
from typing import Dict, List, Optional
from dataclasses import dataclass, field, asdict
from pathlib import Path


@dataclass
class YarnProfile:
    """Complete profile of a yarn"""
    name: str
    brand: str
    weight_category: str  # lace, fingering, sport, dk, worsted, bulky, super_bulky
    fiber: str  # cotton, wool, acrylic, blend, etc.
    meter_per_gram: float
    suggested_hook: str
    care: str = ""
    price_range: str = ""  # $, $$, $$$
    colors_available: int = 0
    is_discontinued: bool = False
    texture: str = ""  # soft, smooth, fuzzy, etc.
    best_for: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class SubstitutionResult:
    """A yarn substitution recommendation"""
    original_yarn: str
    substitute_yarn: str
    confidence: float  # 0-100
    match_reasons: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    price_diff: str = ""
    availability: str = "widely_available"
    
    def to_dict(self) -> Dict:
        return asdict(self)


class SmartYarnSubstitution:
    """
    AI-powered yarn substitution engine
    
    Features:
    - Find exact matches by weight, fiber, hook
    - Consider texture and drape
    - Price-aware substitutions
    - Availability checking
    - Gauge compatibility
    - Project-specific recommendations
    """
    
    # Comprehensive yarn database
    YARN_DATABASE = [
        YarnProfile("Red Heart Super Saver", "Red Heart", "worsted", "100% Acrylic",
                   2.36, "5.0mm", "Machine wash/dry", "$", 100, texture="smooth",
                   best_for=["amigurumi", "blankets", "practice"]),
        YarnProfile("Lily Sugar'n Cream", "Lily", "worsted", "100% Cotton",
                   1.96, "5.0mm", "Machine wash/dry", "$", 40, texture="smooth",
                   best_for=["dishcloths", "amigurumi", "market_bags"]),
        YarnProfile("Bernat Blanket", "Bernat", "super_bulky", "100% Polyester",
                   0.44, "8.0mm", "Machine wash", "$$", 50, texture="soft, plush",
                   best_for=["blankets", "scarves", "quick_projects"]),
        YarnProfile("Scheepjes Catona", "Scheepjes", "sport", "100% Mercericized Cotton",
                   4.0, "3.5mm", "Machine wash cool", "$$", 100, texture="smooth, shiny",
                   best_for=["amigurumi", "garments", "colorwork"]),
        YarnProfile("Paintbox Yarns Cotton DK", "Paintbox", "dk", "100% Cotton",
                   2.5, "4.0mm", "Machine wash", "$", 60, texture="smooth",
                   best_for=["amigurumi", "baby", "summer_items"]),
        YarnProfile("Cascade 220", "Cascade", "worsted", "100% Wool",
                   2.01, "5.0mm", "Hand wash", "$$", 200, texture="soft",
                   best_for=["garments", "hats", "colorwork"]),
        YarnProfile("Malaquias Amigurumi", "Malaquias", "dk", "100% Cotton",
                   2.7, "3.5mm", "Hand wash", "$", 100, texture="smooth, tight",
                   best_for=["amigurumi", "toys"]),
        YarnProfile("WeCrochet Dishie", "WeCrochet", "worsted", "100% Cotton",
                   1.96, "5.0mm", "Machine wash", "$", 60, texture="absorbent",
                   best_for=["dishcloths", "towels", "kitchen"]),
        YarnProfile("Hobbii Rainbow Cotton", "Hobbii", "sport", "100% Cotton",
                   2.5, "3.5mm", "Machine wash 60C", "$", 100, texture="smooth",
                   best_for=["amigurumi", "colorwork", "baby"]),
        YarnProfile("Caron Simply Soft", "Caron", "worsted", "100% Acrylic",
                   2.18, "5.0mm", "Machine wash/dry", "$", 50, texture="soft, drapey",
                   best_for=["blankets", "garments", "baby"]),
        YarnProfile("DROPS Safran", "DROPS", "sport", "100% Cotton",
                   3.4, "3.0mm", "Machine wash 60C", "$", 80, texture="smooth, fine",
                   best_for=["amigurumi", "summer", "baby"]),
        YarnProfile("King Cole Merino DK", "King Cole", "dk", "100% Merino Wool",
                   2.38, "4.0mm", "Hand wash", "$$$", 40, texture="luxuriously soft",
                   best_for=["garments", "baby", "luxury_items"]),
    ]
    
    WEIGHT_HOOK_MAP = {
        "lace": ("1.5-2.5mm", 0),
        "fingering": ("2.25-3.5mm", 1),
        "sport": ("3.5-4.5mm", 2),
        "dk": ("3.5-4.5mm", 3),
        "worsted": ("4.5-5.5mm", 4),
        "bulky": ("5.5-8.0mm", 5),
        "super_bulky": ("8.0-12.0mm", 6),
    }
    
    def __init__(self):
        self.yarn_db = self.YARN_DATABASE.copy()
    
    def find_substitutes(self, yarn_name: str = "", weight: str = "",
                        fiber: str = "", hook_size: str = "",
                        project_type: str = "", max_price: str = "",
                        softness_priority: bool = False) -> List[SubstitutionResult]:
        """Find the best yarn substitutions"""
        
        # Find the original yarn
        original = self._find_yarn(yarn_name)
        original_weight = weight or (original.weight_category if original else "")
        original_fiber = fiber or (original.fiber if original else "")
        
        # Score all alternatives
        candidates = []
        
        for yarn in self.yarn_db:
            if original and yarn.name == original.name:
                continue  # Skip the original
            
            score = 0
            reasons = []
            warnings = []
            
            # Weight match (most important)
            if yarn.weight_category == original_weight:
                score += 40
                reasons.append(f"Same weight ({yarn.weight_category})")
            else:
                # Check if adjacent weight
                w1 = self.WEIGHT_HOOK_MAP.get(original_weight, ("", 0))[1]
                w2 = self.WEIGHT_HOOK_MAP.get(yarn.weight_category, ("", 0))[1]
                if abs(w1 - w2) == 1:
                    score += 15
                    reasons.append(f"Close weight ({yarn.weight_category} vs {original_weight})")
                    warnings.append(f"Different weight - adjust hook size")
                else:
                    score += 0
                    warnings.append(f"Very different weight - not recommended")
            
            # Fiber match
            if original_fiber and original_fiber.lower() in yarn.fiber.lower():
                score += 25
                reasons.append(f"Same fiber ({yarn.fiber})")
            elif "cotton" in original_fiber.lower() and "cotton" in yarn.fiber.lower():
                score += 20
                reasons.append("Similar fiber (cotton)")
            elif "acrylic" in original_fiber.lower() and "acrylic" in yarn.fiber.lower():
                score += 20
                reasons.append("Similar fiber (acrylic)")
            elif "wool" in original_fiber.lower() and "wool" in yarn.fiber.lower():
                score += 20
                reasons.append("Similar fiber (wool)")
            else:
                if original_fiber and yarn.fiber != original_fiber:
                    warnings.append(f"Different fiber ({yarn.fiber} vs {original_fiber})")
            
            # Hook size compatibility
            if hook_size:
                try:
                    hook_mm = float(hook_size.replace("mm", ""))
                    suggested = yarn.suggested_hook.replace("mm", "")
                    if "-" in suggested:
                        low, high = [float(x) for x in suggested.split("-")]
                        if low <= hook_mm <= high:
                            score += 15
                            reasons.append("Compatible hook size")
                    else:
                        if abs(float(suggested) - hook_mm) <= 1:
                            score += 10
                except:
                    pass
            
            # Project type match
            if project_type:
                if any(project_type.lower() in b for b in yarn.best_for):
                    score += 15
                    reasons.append(f"Good for {project_type}")
                else:
                    warnings.append(f"May not be ideal for {project_type}")
            
            # Texture/softness priority
            if softness_priority:
                if "soft" in yarn.texture.lower() or "merino" in yarn.fiber.lower():
                    score += 10
                    reasons.append("Soft texture")
            
            # Price filter
            if max_price:
                price_order = {"$": 0, "$$": 1, "$$$": 2}
                if price_order.get(yarn.price_range, 1) > price_order.get(max_price, 2):
                    score -= 20
                    warnings.append("More expensive than budget")
            
            # Widely available bonus
            if yarn.colors_available > 50:
                score += 5
                reasons.append("Widely available")
            
            confidence = min(100, max(0, score))
            
            if confidence >= 30:  # Minimum threshold
                price_diff = ""
                if original:
                    if yarn.price_range == original.price_range:
                        price_diff = "Similar price"
                    else:
                        price_diff = f"{yarn.price_range} vs {original.price_range}"
                
                candidates.append(SubstitutionResult(
                    original_yarn=yarn_name or original_weight,
                    substitute_yarn=yarn.name,
                    confidence=confidence,
                    match_reasons=reasons,
                    warnings=warnings,
                    price_diff=price_diff,
                    availability="widely_available" if yarn.colors_available > 30 else "limited"
                ))
        
        # Sort by confidence
        candidates.sort(key=lambda c: c.confidence, reverse=True)
        return candidates[:5]  # Top 5
    
    def _find_yarn(self, name: str) -> Optional[YarnProfile]:
        """Find a yarn by name"""
        name_lower = name.lower()
        for yarn in self.yarn_db:
            if name_lower in yarn.name.lower() or name_lower in yarn.brand.lower():
                return yarn
        return None
    
    def suggest_for_project(self, project_type: str, difficulty: str = "Beginner",
                           budget: str = "$") -> List[Dict]:
        """Suggest best yarns for a project type"""
        suggestions = []
        
        for yarn in self.yarn_db:
            if any(project_type.lower() in b for b in yarn.best_for):
                suggestions.append({
                    "name": yarn.name,
                    "brand": yarn.brand,
                    "weight": yarn.weight_category,
                    "fiber": yarn.fiber,
                    "hook": yarn.suggested_hook,
                    "price": yarn.price_range,
                    "colors": yarn.colors_available,
                    "texture": yarn.texture,
                    "reason": f"Excellent for {project_type}",
                })
        
        # Filter by budget
        if budget:
            budget_levels = {"$": ["$"], "$$": ["$", "$$"], "$$$": ["$", "$$", "$$$"]}
            allowed = budget_levels.get(budget, ["$", "$$", "$$$"])
            suggestions = [s for s in suggestions if s["price"] in allowed]
        
        return suggestions[:5]
    
    def get_yarn_info(self, name: str) -> Dict:
        """Get detailed info about a yarn"""
        yarn = self._find_yarn(name)
        if not yarn:
            return {"error": f"Yarn '{name}' not found in database"}
        
        return {
            "name": yarn.name,
            "brand": yarn.brand,
            "weight": yarn.weight_category,
            "fiber": yarn.fiber,
            "hook": yarn.suggested_hook,
            "meter_per_gram": yarn.meter_per_gram,
            "care": yarn.care,
            "price_range": yarn.price_range,
            "colors": yarn.colors_available,
            "texture": yarn.texture,
            "best_for": yarn.best_for,
            "discontinued": yarn.is_discontinued,
        }


# Demo
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  SMART YARN SUBSTITUTION - DEMONSTRATION")
    print("=" * 60)
    
    sub = SmartYarnSubstitution()
    
    # Find substitutes
    print("\n🔍 Finding substitutes for 'Red Heart Super Saver' (worsted)...")
    results = sub.find_substitutes(
        yarn_name="Red Heart Super Saver",
        project_type="blankets"
    )
    
    for r in results:
        print(f"\n  {'=' * 40}")
        print(f"  ✅ {r.substitute_yarn} ({r.confidence}% match)")
        for reason in r.match_reasons:
            print(f"     • {reason}")
        for warn in r.warnings:
            print(f"     ⚠️  {warn}")
        if r.price_diff:
            print(f"     💰 {r.price_diff}")
    
    # Suggest for project
    print(f"\n\n💡 Best yarns for Amigurumi:")
    suggestions = sub.suggest_for_project("amigurumi", budget="$")
    for s in suggestions:
        print(f"  • {s['name']} ({s['weight']}, {s['fiber']}, {s['price']})")
    
    # Get yarn info
    print(f"\n\n📋 Yarn Info:")
    info = sub.get_yarn_info("Scheepjes Catona")
    for key, val in info.items():
        if key != "error":
            print(f"  {key}: {val}")
    
    print(f"\n  Smart Yarn Substitution Complete! 🧶")
