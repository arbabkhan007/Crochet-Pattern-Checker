"""
Yarn Stash Manager Pro - Advanced yarn inventory and stash management
"""
import json
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path


class YarnStashManagerPro:
    """
    Advanced yarn stash management
    
    Features:
    - Detailed yarn catalog
    - Usage tracking
    - Project assignments
    - Stash value calculation
    - Reorganization suggestions
    - Shopping list
    """
    
    YARN_TYPES = {
        "natural": ["wool", "cotton", "silk", "alpaca", "cashmere", "mohair", "linen"],
        "synthetic": ["acrylic", "polyester", "nylon"],
        "blends": ["wool/acrylic", "cotton/acrylic", "bamboo/cotton"],
        "specialty": ["bouclé", "chenille", "eyelash", "ribbon", "novelty"],
    }
    
    STORAGE_LOCATIONS = [
        "Main stash", "Craft room", "Bedroom closet", "Under bed",
        "Office", "Travel bag", "Work in progress", "Quarantine",
    ]
    
    def __init__(self, storage_path: str = "yarn_stash_pro.json"):
        self.storage_path = Path(storage_path)
        self.data = {
            "yarns": [],
            "projects": [],
            "shopping_list": [],
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
    
    def add_yarn(self, name: str, brand: str = "", color: str = "",
                weight: str = "", yards: float = 0, grams: float = 0,
                fiber: str = "", location: str = "Main stash",
                dye_lot: str = "", purchased: str = "", cost: float = 0) -> Dict:
        """Add yarn to stash"""
        yarn = {
            "id": f"Y{len(self.data['yarns']) + 1:04d}",
            "name": name,
            "brand": brand,
            "color": color,
            "weight": weight,
            "yards": yards,
            "grams": grams,
            "fiber": fiber,
            "location": location,
            "dye_lot": dye_lot,
            "purchased": purchased or datetime.now().strftime("%Y-%m-%d"),
            "cost": cost,
            "assigned_to": None,
            "used": 0,
            "notes": "",
        }
        
        self.data["yarns"].append(yarn)
        self.save()
        return yarn
    
    def assign_to_project(self, yarn_id: str, project_name: str) -> Dict:
        """Assign yarn to a project"""
        yarn = next((y for y in self.data["yarns"] if y["id"] == yarn_id), None)
        if not yarn:
            return {"error": "Yarn not found"}
        
        yarn["assigned_to"] = project_name
        
        # Add to projects if new
        if project_name not in [p["name"] for p in self.data["projects"]]:
            self.data["projects"].append({
                "name": project_name,
                "yarns": [yarn_id],
                "status": "planning",
            })
        else:
            project = next(p for p in self.data["projects"] if p["name"] == project_name)
            if yarn_id not in project["yarns"]:
                project["yarns"].append(yarn_id)
        
        self.save()
        return {"yarn": yarn["name"], "assigned_to": project_name}
    
    def log_usage(self, yarn_id: str, yards_used: float) -> Dict:
        """Log yarn usage"""
        yarn = next((y for y in self.data["yarns"] if y["id"] == yarn_id), None)
        if not yarn:
            return {"error": "Yarn not found"}
        
        yarn["used"] += yards_used
        remaining = yarn["yards"] - yarn["used"]
        
        self.save()
        
        return {
            "yarn": yarn["name"],
            "used": yards_used,
            "remaining": max(0, remaining),
            "percentage_used": round(yarn["used"] / max(1, yarn["yards"]) * 100, 1),
        }
    
    def get_stash_stats(self) -> Dict:
        """Get stash statistics"""
        yarns = self.data["yarns"]
        
        total_yards = sum(y["yards"] for y in yarns)
        total_grams = sum(y["grams"] for y in yarns)
        total_value = sum(y["cost"] for y in yarns)
        
        # By weight
        by_weight = {}
        for yarn in yarns:
            w = yarn["weight"] or "Unknown"
            by_weight[w] = by_weight.get(w, 0) + 1
        
        # By fiber
        by_fiber = {}
        for yarn in yarns:
            f = yarn["fiber"] or "Unknown"
            by_fiber[f] = by_fiber.get(f, 0) + 1
        
        # By location
        by_location = {}
        for yarn in yarns:
            loc = yarn["location"] or "Unknown"
            by_location[loc] = by_location.get(loc, 0) + 1
        
        # Assigned vs unassigned
        assigned = sum(1 for y in yarns if y.get("assigned_to"))
        unassigned = len(yarns) - assigned
        
        # Smallest skeins (need to use up)
        smallest = sorted([y for y in yarns if y["yards"] > 0 and (y["yards"] - y["used"]) < 50],
                         key=lambda y: y["yards"] - y["used"])[:5]
        
        return {
            "total_yarns": len(yarns),
            "total_yards": round(total_yards, 1),
            "total_grams": round(total_grams, 1),
            "total_value": round(total_value, 2),
            "by_weight": by_weight,
            "by_fiber": by_fiber,
            "by_location": by_location,
            "assigned": assigned,
            "unassigned": unassigned,
            "projects": len(self.data["projects"]),
            "smallest_skeins": [{"name": y["name"], "remaining": round(y["yards"] - y["used"], 1)} for y in smallest],
        }
    
    def find_yarn(self, weight: str = None, color: str = None,
                 fiber: str = None, min_yards: float = None) -> List[Dict]:
        """Find yarns matching criteria"""
        results = self.data["yarns"]
        
        if weight:
            results = [y for y in results if y["weight"] and weight.lower() in y["weight"].lower()]
        if color:
            results = [y for y in results if y["color"] and color.lower() in y["color"].lower()]
        if fiber:
            results = [y for y in results if y["fiber"] and fiber.lower() in y["fiber"].lower()]
        if min_yards:
            results = [y for y in results if (y["yards"] - y["used"]) >= min_yards]
        
        return results
    
    def add_to_shopping_list(self, name: str, weight: str = "",
                            yards_needed: float = 0, notes: str = "") -> Dict:
        """Add to shopping list"""
        item = {
            "id": f"SL{len(self.data['shopping_list']) + 1:04d}",
            "name": name,
            "weight": weight,
            "yards_needed": yards_needed,
            "notes": notes,
            "added": datetime.now().strftime("%Y-%m-%d"),
            "purchased": False,
        }
        
        self.data["shopping_list"].append(item)
        self.save()
        return item
    
    def get_shopping_list(self) -> List[Dict]:
        """Get shopping list"""
        return [item for item in self.data["shopping_list"] if not item.get("purchased")]
    
    def suggest_organizing(self) -> Dict:
        """Suggest stash organization"""
        yarns = self.data["yarns"]
        
        # Group by weight
        by_weight = {}
        for yarn in yarns:
            w = yarn["weight"] or "Unknown"
            if w not in by_weight:
                by_weight[w] = []
            by_weight[w].append(yarn["name"])
        
        # Unused yarns
        unused = [y for y in yarns if not y.get("assigned_to") and y["yards"] > 0]
        
        # Small scraps
        scraps = [y for y in yarns if 0 < (y["yards"] - y["used"]) < 20]
        
        return {
            "organization_suggestions": [
                f"Group by weight: {len(by_weight)} categories",
                f"Organize by location: {len(set(y['location'] for y in yarns))} locations",
            ],
            "unused_count": len(unused),
            "unused_yarns": [y["name"] for y in unused[:5]],
            "scrap_count": len(scraps),
            "scraps": [y["name"] for y in scraps[:5]],
            "tip": "Consider using scraps for amigurumi stuffing or colorwork!",
        }


# Demo
if __name__ == "__main__":
    import os
    print("\n" + "=" * 60)
    print("  YARN STASH MANAGER PRO - DEMONSTRATION")
    print("=" * 60)
    
    stash = YarnStashManagerPro(storage_path="/tmp/demo_stash_pro.json")
    
    # Add yarns
    stash.add_yarn("Super Saver Red", "Red Heart", "Red", "Worsted", 364, 198, "Acrylic", cost=4.99)
    stash.add_yarn("Merino Grey", "Malabrigo", "Grey", "Worsted", 210, 100, "Merino Wool", cost=15.99)
    stash.add_yarn("Cotton White", "Lily Sugar'n Cream", "White", "Worsted", 120, 71, "Cotton", cost=2.49)
    stash.add_yarn("Bamboo Blue", "WeCrochet", "Blue", "DK", 250, 100, "Bamboo", cost=8.99)
    stash.add_yarn("Scraps Mix", "", "Various", "Various", 15, 10, "Mixed", cost=0)
    
    print(f"✅ Added 5 yarns to stash")
    
    # Assign to project
    stash.assign_to_project("Y0001", "Granny Blanket")
    stash.assign_to_project("Y0002", "Winter Scarf")
    print(f"✅ Assigned 2 yarns to projects")
    
    # Log usage
    stash.log_usage("Y0001", 100)
    print(f"✅ Logged usage on Y0001")
    
    # Stats
    print(f"\n📊 Stash Statistics:")
    stats = stash.get_stash_stats()
    print(f"  Total Yarns: {stats['total_yarns']}")
    print(f"  Total Yards: {stats['total_yards']}")
    print(f"  Total Value: ${stats['total_value']}")
    print(f"  Assigned: {stats['assigned']} | Unassigned: {stats['unassigned']}")
    
    print(f"\n  By Weight:")
    for w, count in stats['by_weight'].items():
        print(f"    {w}: {count}")
    
    # Find yarn
    print(f"\n🔍 Finding 'Worsted' weight yarns:")
    found = stash.find_yarn(weight="worsted")
    for y in found:
        print(f"  • {y['name']} ({y['color']}, {y['yards']}yds)")
    
    # Smallest skeins
    print(f"\n📏 Smallest Skeins (use these up!):")
    for y in stats['smallest_skeins'][:3]:
        print(f"  • {y['name']}: {y['remaining']}yds left")
    
    # Shopping list
    stash.add_to_shopping_list("Black Worsted", "Worsted", 300, "For new project")
    print(f"\n🛒 Shopping List:")
    for item in stash.get_shopping_list():
        print(f"  • {item['name']} ({item['yards_needed']}yds needed)")
    
    # Organization
    print(f"\n📦 Organization Suggestions:")
    org = stash.suggest_organizing()
    for sug in org['organization_suggestions']:
        print(f"  • {sug}")
    print(f"  Unused: {org['unused_count']} | Scraps: {org['scrap_count']}")
    print(f"  💡 {org['tip']}")
    
    # Cleanup
    if os.path.exists("/tmp/demo_stash_pro.json"):
        os.remove("/tmp/demo_stash_pro.json")
    
    print(f"\n  Yarn Stash Manager Pro Complete! 🧶")

