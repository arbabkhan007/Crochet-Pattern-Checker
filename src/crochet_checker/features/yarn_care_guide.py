"""
Yarn Care Guide - Complete washing, blocking, and care instructions for all fiber types
"""
from typing import Dict, List, Optional


class YarnCareGuide:
    """
    Complete yarn care instructions
    
    Features:
    - Washing instructions by fiber
    - Blocking methods
    - Drying techniques
    - Storage tips
    - Stain removal
    - Pilling solutions
    """
    
    FIBER_CARE = {
        "cotton": {
            "wash": "Machine wash warm or cool",
            "dry": "Tumble dry low or lay flat",
            "iron": "High heat OK",
            "bleach": "Chlorine bleach OK",
            "block": "Pin blocking or steam blocking",
            "special": "May shrink slightly on first wash",
            "temp": "40°C / 104°F max",
        },
        "wool": {
            "wash": "Hand wash cold or machine wash delicate",
            "dry": "Lay flat to dry, never hang",
            "iron": "Low heat with pressing cloth",
            "bleach": "Do NOT bleach",
            "block": "Wet blocking (pin and let dry)",
            "special": "May felt if agitated in warm water",
            "temp": "30°C / 86°F max",
        },
        "acrylic": {
            "wash": "Machine wash warm",
            "dry": "Tumble dry low",
            "iron": "Low heat only - melts easily!",
            "bleach": "Non-chlorine bleach only",
            "block": "Steam blocking (hover iron, don't touch)",
            "special": "Kills stitch definition if over-steamed",
            "temp": "30°C / 86°F max",
        },
        "alpaca": {
            "wash": "Hand wash cold gently",
            "dry": "Lay flat, squeeze out water in towel",
            "iron": "Low heat with pressing cloth",
            "bleach": "Do NOT bleach",
            "block": "Gentle wet blocking",
            "special": "Can stretch when wet - support weight",
            "temp": "20°C / 68°F",
        },
        "silk": {
            "wash": "Hand wash cold with gentle soap",
            "dry": "Roll in towel, lay flat",
            "iron": "Cool iron on wrong side",
            "bleach": "Do NOT bleach",
            "block": "Gentle pin blocking",
            "special": "Weakened when wet - handle gently",
            "temp": "20°C / 68°F",
        },
        "bamboo": {
            "wash": "Hand wash cool or machine delicate",
            "dry": "Lay flat - stretches when wet",
            "iron": "Medium heat",
            "bleach": "Non-chlorine only",
            "block": "Light steam or wet blocking",
            "special": "Very drapey - gets heavier when wet",
            "temp": "30°C / 86°F",
        },
        "linen": {
            "wash": "Machine wash warm",
            "dry": "Tumble dry or lay flat",
            "iron": "Hot iron while damp",
            "bleach": "Chlorine bleach OK",
            "block": "Wet blocking works great",
            "special": "Gets softer with each wash",
            "temp": "50°C / 122°F",
        },
        "cashmere": {
            "wash": "Hand wash cold with cashmere shampoo",
            "dry": "Lay flat, reshape while damp",
            "iron": "Very low or steam only",
            "bleach": "Do NOT bleach",
            "block": "Gentle pin blocking",
            "special": "Very delicate - handle with care",
            "temp": "20°C / 68°F",
        },
        "polyester": {
            "wash": "Machine wash warm",
            "dry": "Tumble dry low",
            "iron": "Low heat",
            "bleach": "Non-chlorine bleach",
            "block": "Steam blocking",
            "special": "Very durable, easy care",
            "temp": "40°C / 104°F",
        },
        "nylon": {
            "wash": "Machine wash warm",
            "dry": "Tumble dry low",
            "iron": "Low heat",
            "bleach": "Non-chlorine bleach",
            "block": "Steam blocking",
            "special": "Strong fiber, often blended",
            "temp": "40°C / 104°F",
        },
        " mohair": {
            "wash": "Hand wash cold gently",
            "dry": "Lay flat, fluff when dry",
            "iron": "Do NOT iron - steam only",
            "bleach": "Do NOT bleach",
            "block": "Very gentle steam (hover only)",
            "special": "Fluffy halo - don't compress",
            "temp": "20°C / 68°F",
        },
        "merino": {
            "wash": "Hand wash cold or superwash machine cold",
            "dry": "Lay flat to dry",
            "iron": "Low heat with cloth",
            "bleach": "Do NOT bleach",
            "block": "Wet blocking for best results",
            "special": "Superwash versions can go in machine",
            "temp": "20°C / 68°F",
        },
    }
    
    BLOCKING_METHODS = {
        "wet_blocking": {
            "name": "Wet Blocking",
            "best_for": ["wool", "cotton", "linen", "alpaca"],
            "steps": [
                "Soak finished item in lukewarm water for 20 min",
                "Gently squeeze out water (don't wring!)",
                "Roll in towel and press to remove excess",
                "Lay on blocking mat or towels",
                "Pin to desired dimensions using rust-proof pins",
                "Let dry completely (24-48 hours)",
                "Unpin and enjoy!",
            ],
        },
        "steam_blocking": {
            "name": "Steam Blocking",
            "best_for": ["acrylic", "blends", "delicate fibers"],
            "steps": [
                "Pin item to desired dimensions",
                "Hold steam iron 1-2 inches above fabric",
                "Steam thoroughly - DON'T TOUCH the fabric!",
                "Let cool and dry completely",
                "Remove pins",
            ],
        },
        "pin_blocking": {
            "name": "Pin Blocking (No Water)",
            "best_for": ["lace", "doilies", "lightweight items"],
            "steps": [
                "Lightly mist with water spray bottle",
                "Pin to desired shape on blocking board",
                "Gently stretch and shape",
                "Let air dry",
            ],
        },
    }
    
    STAIN_REMOVAL = {
        "food": "Blot excess. Mix dish soap + cold water. Dab gently. Rinse.",
        "oil": "Apply cornstarch or baking soda. Wait 30 min. Brush off. Wash.",
        "dye": "Soak in cold water + oxygen bleach. Rinse. Repeat if needed.",
        "ink": "Dab with rubbing alcohol on cotton swab. Blot, don't rub.",
        "grass": "Apply white vinegar. Let sit 5 min. Wash normally.",
        "makeup": "Apply shaving cream. Gently work in. Rinse with cold water.",
    }
    
    STORAGE_TIPS = [
        "Store in breathable cotton bags, not plastic",
        "Keep away from direct sunlight to prevent fading",
        "Add cedar blocks or lavender to deter moths",
        "Fold heavy items - don't hang (prevents stretching)",
        "Label yarn with fiber content, dye lot, and purchase date",
        "Store finished items clean - moths are attracted to body oils",
        "Rotate items seasonally to prevent long compression",
        "Use acid-free tissue paper for delicate items",
    ]
    
    PILLING_SOLUTIONS = [
        "Use a fabric shaver/depiller gently",
        "A disposable razor works in a pinch",
        "Prevent pilling: choose tighter twist yarns",
        "Wash items inside out to reduce friction",
        "Hand wash instead of machine when possible",
        "Acrylic pills more than natural fibers",
    ]
    
    def get_care(self, fiber: str) -> Dict:
        """Get care instructions for a fiber"""
        care = self.FIBER_CARE.get(fiber.lower(), self.FIBER_CARE.get("acrylic"))
        return {
            "fiber": fiber,
            "care": care,
        }
    
    def suggest_blocking(self, fiber: str) -> Dict:
        """Suggest best blocking method for a fiber"""
        best_method = None
        for method, info in self.BLOCKING_METHODS.items():
            if fiber.lower() in info["best_for"]:
                best_method = method
                break
        
        if not best_method:
            best_method = "wet_blocking"
        
        return {
            "fiber": fiber,
            "recommended_method": self.BLOCKING_METHODS[best_method]["name"],
            "steps": self.BLOCKING_METHODS[best_method]["steps"],
        }
    
    def get_stain_help(self, stain_type: str) -> Dict:
        """Get stain removal instructions"""
        treatment = self.STAIN_REMOVAL.get(stain_type.lower(), "Blot gently. Test any treatment on an inconspicuous area first.")
        return {
            "stain": stain_type,
            "treatment": treatment,
        }
    
    def get_storage_tips(self) -> List[str]:
        """Get storage tips"""
        return self.STORAGE_TIPS
    
    def get_pilling_solutions(self) -> List[str]:
        """Get pilling solutions"""
        return self.PILLING_SOLUTIONS
    
    def quick_reference_card(self) -> str:
        """Generate a quick reference text"""
        card = "YARN CARE QUICK REFERENCE\n" + "=" * 40 + "\n\n"
        
        for fiber, care in sorted(self.FIBER_CARE.items()):
            card += f"{fiber.upper()}\n"
            card += f"  Wash: {care['wash']}\n"
            card += f"  Dry:  {care['dry']}\n"
            card += f"  Temp: {care['temp']}\n"
            card += f"  Block: {care['block']}\n\n"
        
        return card


# Demo
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  YARN CARE GUIDE - DEMONSTRATION")
    print("=" * 60)
    
    guide = YarnCareGuide()
    
    # Test fibers
    for fiber in ["wool", "cotton", "acrylic", "silk"]:
        print(f"\n🧶 {fiber.upper()}")
        care = guide.get_care(fiber)
        print(f"  Wash: {care['care']['wash']}")
        print(f"  Dry: {care['care']['dry']}")
        print(f"  Temp: {care['care']['temp']}")
    
    # Blocking methods
    print(f"\n📌 Blocking for Wool:")
    block = guide.suggest_blocking("wool")
    print(f"  Method: {block['recommended_method']}")
    for i, step in enumerate(block['steps'][:3], 1):
        print(f"  {i}. {step}")
    
    print(f"\n📌 Blocking for Acrylic:")
    block = guide.suggest_blocking("acrylic")
    print(f"  Method: {block['recommended_method']}")
    for i, step in enumerate(block['steps'][:3], 1):
        print(f"  {i}. {step}")
    
    # Stain removal
    print(f"\n🧼 Stain Removal - Oil:")
    stain = guide.get_stain_help("oil")
    print(f"  {stain['treatment']}")
    
    # Storage
    print(f"\n📦 Storage Tips:")
    for tip in guide.get_storage_tips()[:3]:
        print(f"  • {tip}")
    
    # Pilling
    print(f"\n🔍 Pilling Solutions:")
    for solution in guide.get_pilling_solutions()[:3]:
        print(f"  • {solution}")
    
    # Quick reference
    ref = guide.quick_reference_card()
    print(f"\n✅ Quick reference card: {len(ref)} chars")
    
    print(f"\n  Yarn Care Guide Complete! 🧼")
