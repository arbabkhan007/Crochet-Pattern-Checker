"""
Intricate Stitch Dictionary - Comprehensive dictionary of complex stitches
"""

class IntricateStitchDictionary:
    def __init__(self):
        self.stitches = {
            'bobble': {
                'abbreviation': 'bobble',
                'difficulty': 'intermediate',
                'instructions': 'Yarn over, insert hook, yarn over, pull up loop (5 times in same stitch), yarn over, pull through all 6 loops',
                'tips': ['Keep loops loose', 'Work into same stitch', 'Pull through all at once']
            },
            'popcorn': {
                'abbreviation': 'pc',
                'difficulty': 'intermediate',
                'instructions': '5 dc in same stitch, remove hook, insert in first dc, pull loop through',
                'tips': ['Push out to form popcorn', 'Secure with slip stitch']
            },
            'cable_stitch': {
                'abbreviation': 'cable',
                'difficulty': 'advanced',
                'instructions': 'Skip 2 stitches, dc in next 2, dc in each of skipped stitches (front cross)',
                'tips': ['Use cable needle if needed', 'Keep tension even']
            },
            'bullion': {
                'abbreviation': 'bull',
                'difficulty': 'expert',
                'instructions': 'Yarn over 5 times, insert hook, pull up loop, pull through 2 loops (5 times)',
                'tips': ['Use small hook to pull through wraps', 'Keep wraps even']
            },
            'solomon_knot': {
                'abbreviation': 'SK',
                'difficulty': 'advanced',
                'instructions': 'Long chain stitch (1/2 inch), sc in 2nd chain from hook',
                'tips': ['Keep chains uniform length', 'Creates lace-like fabric']
            },
            'hairpin_lace': {
                'abbreviation': 'HPL',
                'difficulty': 'expert',
                'instructions': 'Using hairpin lace tool, create loops, join with crochet stitches',
                'tips': ['Keep loops even', 'Use specific tool']
            },
            'broomstick_lace': {
                'abbreviation': 'BSL',
                'difficulty': 'expert',
                'instructions': 'Pull loops up on large hook/dowel, group loops, crochet together',
                'tips': ['Use smooth dowel', 'Keep loops same size']
            },
            'overlay_crochet': {
                'abbreviation': 'OC',
                'difficulty': 'advanced',
                'instructions': 'Work stitches over previous rows, creating raised design',
                'tips': ['Use contrasting color', 'Work in back loops only for base']
            }
        }
    
    def get_stitch_info(self, stitch_name: str) -> dict:
        """Get detailed information about a stitch"""
        return self.stitches.get(stitch_name.lower(), {
            'error': 'Stitch not found in dictionary'
        })
    
    def get_stitches_by_difficulty(self, difficulty: str) -> list:
        """Get all stitches of a certain difficulty"""
        return [name for name, info in self.stitches.items() if info['difficulty'] == difficulty]
    
    def search_stitches(self, keyword: str) -> list:
        """Search for stitches by keyword"""
        results = []
        for name, info in self.stitches.items():
            if keyword.lower() in name or keyword.lower() in info['instructions'].lower():
                results.append(name)
        return results
    
    def generate_stitch_guide(self, stitch_list: list) -> str:
        """Generate a guide for multiple stitches"""
        guide = "🧵 STITCH GUIDE\n" + "=" * 60 + "\n\n"
        
        for stitch_name in stitch_list:
            if stitch_name in self.stitches:
                info = self.stitches[stitch_name]
                guide += f"\n{stitch_name.upper()}\n"
                guide += f"Abbreviation: {info['abbreviation']}\n"
                guide += f"Difficulty: {info['difficulty']}\n"
                guide += f"Instructions: {info['instructions']}\n"
                guide += "Tips:\n"
                for tip in info['tips']:
                    guide += f"  • {tip}\n"
                guide += "\n" + "-" * 60 + "\n"
        
        return guide

if __name__ == "__main__":
    print("📚 Intricate Stitch Dictionary")
    print("=" * 60)
    
    dictionary = IntricateStitchDictionary()
    
    # Get info on complex stitch
    stitch_info = dictionary.get_stitch_info('bullion')
    print(f"\nBullion Stitch:")
    print(f"Difficulty: {stitch_info['difficulty']}")
    print(f"Instructions: {stitch_info['instructions']}")
    
    # Get all expert stitches
    expert_stitches = dictionary.get_stitches_by_difficulty('expert')
    print(f"\nExpert Level Stitches: {', '.join(expert_stitches)}")
    
    # Generate guide
    guide = dictionary.generate_stitch_guide(['bobble', 'cable_stitch', 'bullion'])
    print("\n" + guide)
