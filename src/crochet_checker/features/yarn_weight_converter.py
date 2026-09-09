"""
Yarn Weight Converter - Convert between all yarn weight systems worldwide
"""
from typing import Dict, List, Optional


class YarnWeightConverter:
    """
    Convert between yarn weight systems
    
    Features:
    - US yarn weight categories
    - UK/Australian terms
    - Metric measurements
    - Ply systems
    - WPI (wraps per inch)
    - Hook size recommendations
    - Substitution guide
    """
    
    WEIGHT_CATEGORIES = {
        "0": {
            "name": "Lace",
            "us": "Lace / Fingering 10-count",
            "uk_au": "1-2 ply",
            "wpi": "15+",
            "meters_50g": "300-600+",
            "hook_mm": "1.5-2.25",
            "hook_us": "00-1",
            "knit_needle_mm": "1.5-2.25",
            "common_uses": "Doilies, shawls, fine garments",
            "substitutions": ["Any lace weight yarn"],
        },
        "1": {
            "name": "Super Fine",
            "us": "Sock / Fingering / Baby",
            "uk_au": "2-3 ply",
            "wpi": "14",
            "meters_50g": "250-350",
            "hook_mm": "2.25-3.5",
            "hook_us": "B-1 to E-4",
            "knit_needle_mm": "2.25-3.25",
            "common_uses": "Socks, baby items, lightweight garments",
            "substitutions": ["Any fingering weight"],
        },
        "2": {
            "name": "Fine",
            "us": "Sport / Baby",
            "uk_au": "4 ply",
            "wpi": "12",
            "meters_50g": "200-300",
            "hook_mm": "3.5-4.5",
            "hook_us": "E-4 to 7",
            "knit_needle_mm": "3.25-3.75",
            "common_uses": "Light garments, baby items, accessories",
            "substitutions": ["DK yarn held double ≈ worsted"],
        },
        "3": {
            "name": "Light",
            "us": "DK / Light Worsted",
            "uk_au": "Double Knit (DK)",
            "wpi": "11",
            "meters_50g": "150-250",
            "hook_mm": "4.5-5.5",
            "hook_us": "7 to I-9",
            "knit_needle_mm": "3.75-4.5",
            "common_uses": "Garments, scarves, shawls, baby items",
            "substitutions": ["2 strands of fingering ≈ DK"],
        },
        "4": {
            "name": "Medium",
            "us": "Worsted / Afghan / Aran",
            "uk_au": "Aran / 8-10 ply",
            "wpi": "9-10",
            "meters_50g": "100-200",
            "hook_mm": "5.5-6.5",
            "hook_us": "I-9 to K-10½",
            "knit_needle_mm": "4.5-5.5",
            "common_uses": "Sweaters, blankets, afghans, accessories",
            "substitutions": ["2 strands of DK ≈ worsted"],
        },
        "5": {
            "name": "Bulky",
            "us": "Chunky / Bulky / Craft / Rug",
            "uk_au": "Chunky / 12 ply",
            "wpi": "7-8",
            "meters_50g": "70-120",
            "hook_mm": "6.5-9",
            "hook_us": "K-10½ to M-13",
            "knit_needle_mm": "5.5-8",
            "common_uses": "Sweaters, blankets, scarves, hats",
            "substitutions": ["2 strands of worsted ≈ bulky"],
        },
        "6": {
            "name": "Super Bulky",
            "us": "Super Bulky / Roving",
            "uk_au": "Super Chunky / 14 ply+",
            "wpi": "5-6",
            "meters_50g": "40-70",
            "hook_mm": "9-15",
            "hook_us": "M-13 to P/Q",
            "knit_needle_mm": "8-12.75",
            "common_uses": "Blankets, heavy scarves, hats",
            "substitutions": ["2-3 strands of worsted ≈ super bulky"],
        },
        "7": {
            "name": "Jumbo",
            "us": "Jumbo / Roving",
            "uk_au": "Jumbo",
            "wpi": "1-4",
            "meters_50g": "1-40",
            "hook_mm": "15+",
            "hook_us": "P/Q+",
            "knit_needle_mm": "12.75+",
            "common_uses": "Arm knitting, blankets, rugs",
            "substitutions": ["Multiple strands of bulky"],
        },
    }
    
    WPI_RANGES = {
        (15, 999): "0 - Lace",
        (13, 14): "1 - Super Fine",
        (12, 12): "2 - Fine",
        (11, 11): "3 - Light/DK",
        (9, 10): "4 - Medium/Worsted",
        (7, 8): "5 - Bulky",
        (5, 6): "6 - Super Bulky",
        (1, 4): "7 - Jumbo",
    }
    
    def convert_by_name(self, yarn_name: str) -> Dict:
        """Convert by US yarn weight name"""
        search = yarn_name.lower()
        
        for cat_id, info in self.WEIGHT_CATEGORIES.items():
            if (search in info["us"].lower() or 
                search in info["name"].lower()):
                return {
                    "category": cat_id,
                    "info": info,
                }
        
        return {"error": f"Could not find yarn weight: {yarn_name}"}
    
    def convert_by_uk(self, uk_term: str) -> Dict:
        """Convert by UK/Australian term"""
        search = uk_term.lower()
        
        for cat_id, info in self.WEIGHT_CATEGORIES.items():
            if search in info["uk_au"].lower():
                return {
                    "category": cat_id,
                    "info": info,
                }
        
        return {"error": f"Could not find UK term: {uk_term}"}
    
    def convert_by_wpi(self, wpi: int) -> Dict:
        """Convert by wraps per inch"""
        for (low, high), category in self.WPI_RANGES.items():
            if low <= wpi <= high:
                cat_id = category.split(" - ")[0]
                return {
                    "wpi": wpi,
                    "category": cat_id,
                    "info": self.WEIGHT_CATEGORIES[cat_id],
                }
        
        return {"error": f"WPI {wpi} out of range"}
    
    def get_hook_size(self, category: str, system: str = "mm") -> Dict:
        """Get recommended hook size for a yarn weight"""
        info = self.WEIGHT_CATEGORIES.get(category)
        if not info:
            return {"error": f"Unknown category: {category}"}
        
        if system == "mm":
            return {"hook_mm": info["hook_mm"], "category": info["name"]}
        else:
            return {"hook_us": info["hook_us"], "category": info["name"]}
    
    def suggest_substitute(self, current_yarn: str) -> Dict:
        """Suggest substitute yarns"""
        result = self.convert_by_name(current_yarn)
        if "error" in result:
            return result
        
        info = result["info"]
        
        return {
            "original": current_yarn,
            "category": info["name"],
            "substitutions": info["substitutions"],
            "hook_recommended_mm": info["hook_mm"],
            "alternatives": self._get_alternatives(result["category"]),
        }
    
    def _get_alternatives(self, category: str) -> List[str]:
        """Get alternative yarn names"""
        info = self.WEIGHT_CATEGORIES.get(category, {})
        return [
            info.get("us", ""),
            info.get("uk_au", ""),
        ]
    
    def get_full_reference(self) -> str:
        """Generate full reference chart"""
        ref = "YARN WEIGHT CONVERSION CHART\n" + "=" * 60 + "\n\n"
        
        ref += f"{'Cat':<4} {'US Name':<20} {'UK/AU':<15} {'Hook (mm)':<12} {'WPI':<6}\n"
        ref += "-" * 60 + "\n"
        
        for cat_id, info in sorted(self.WEIGHT_CATEGORIES.items()):
            ref += f"{cat_id:<4} {info['name']:<20} {info['uk_au']:<15} {info['hook_mm']:<12} {info['wpi']:<6}\n"
        
        return ref
    
    def calculate_yardage_substitution(self, pattern_yards: int,
                                      original_weight: str,
                                      substitute_weight: str) -> Dict:
        """Calculate yardage needed when substituting yarn weights"""
        orig = self.WEIGHT_CATEGORIES.get(original_weight)
        sub = self.WEIGHT_CATEGORIES.get(substitute_weight)
        
        if not orig or not sub:
            return {"error": "Unknown yarn weight"}
        
        # Rough conversion based on thickness
        thickness_ratio = int(substitute_weight) / max(1, int(original_weight))
        
        # Thicker yarn = less yardage needed
        adjusted_yards = int(pattern_yards / max(0.5, thickness_ratio))
        
        return {
            "original_pattern": f"{pattern_yards} yards of {orig['name']}",
            "substitute_weight": sub["name"],
            "adjusted_yards_needed": adjusted_yards,
            "ratio": round(thickness_ratio, 2),
            "note": "Thicker yarns require less yardage. Always buy extra!",
        }


# Demo
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  YARN WEIGHT CONVERTER - DEMONSTRATION")
    print("=" * 60)
    
    converter = YarnWeightConverter()
    
    # Convert by name
    print(f"\n🧶 Converting 'Worsted':")
    result = converter.convert_by_name("worsted")
    if "error" not in result:
        info = result["info"]
        print(f"  Category: {result['category']}")
        print(f"  Name: {info['name']}")
        print(f"  UK/AU: {info['uk_au']}")
        print(f"  Hook: {info['hook_mm']}mm ({info['hook_us']})")
        print(f"  WPI: {info['wpi']}")
        print(f"  Uses: {info['common_uses']}")
    
    # Convert by UK term
    print(f"\n🇬🇧 Converting 'DK':")
    result = converter.convert_by_uk("DK")
    if "error" not in result:
        print(f"  = {result['info']['name']} (US)")
        print(f"  Hook: {result['info']['hook_mm']}mm")
    
    # Convert by WPI
    print(f"\n📏 Converting WPI 9:")
    result = converter.convert_by_wpi(9)
    if "error" not in result:
        print(f"  = {result['info']['name']}")
        print(f"  Hook: {result['info']['hook_mm']}mm")
    
    # Hook sizes
    print(f"\n🪝 Recommended hooks for Medium/Worsted:")
    hook = converter.get_hook_size("4", "mm")
    print(f"  mm: {hook['hook_mm']}")
    
    # Substitution
    print(f"\n🔄 Substituting 'Worsted':")
    sub = converter.suggest_substitute("worsted")
    if "error" not in sub:
        print(f"  Category: {sub['category']}")
        print(f"  Alternatives: {', '.join(sub['alternatives'])}")
    
    # Yardage adjustment
    print(f"\n📐 Yardage substitution:")
    print(f"  Pattern needs 500 yards of Worsted")
    print(f"  Using Bulky instead:")
    yards = converter.calculate_yardage_substitution(500, "4", "5")
    if "error" not in yards:
        print(f"  Need: {yards['adjusted_yards_needed']} yards of Bulky")
        print(f"  Ratio: {yards['ratio']}x")
    
    # Full reference
    print(f"\n📋 Full Reference Chart:")
    print(converter.get_full_reference())
    
    print(f"\n  Yarn Weight Converter Complete! 🧶")
