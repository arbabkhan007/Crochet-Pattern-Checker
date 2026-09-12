"""
Crochet Code Generator - Generate patterns programmatically with Python code
"""
from typing import List, Dict


class PatternCodeGenerator:
    """Generate crochet patterns using Python code"""
    
    def __init__(self):
        self.stitch_library = {
            "sc": {"yarn_per_stitch": 0.5, "height": 1},
            "dc": {"yarn_per_stitch": 0.8, "height": 2},
            "hdc": {"yarn_per_stitch": 0.65, "height": 1.5},
            "tr": {"yarn_per_stitch": 1.0, "height": 3},
        }
    
    def generate_granny_square(self, rounds: int = 4) -> Dict:
        """Generate granny square pattern"""
        pattern = ["Magic ring"]
        stitch_count = 0
        
        # Round 1
        pattern.append("Round 1: Ch 3 (counts as dc), 2 dc, ch 2")
        pattern.append("  *3 dc, ch 2* 3 times, sl st to top of ch-3")
        stitch_count = 12
        
        # Rounds 2+
        for r in range(2, rounds + 1):
            pattern.append(f"Round {r}: Sl st to ch-2 sp, ch 3")
            pattern.append(f"  *3 dc, ch 2, 3 dc, ch 2, 3 dc, ch 2, 3 dc, ch 1* in each corner")
            pattern.append(f"  Repeat around, sl st to top of ch-3")
            stitch_count += 8 * (r - 1)
        
        return {
            "name": f"Granny Square ({rounds} rounds)",
            "pattern": pattern,
            "final_stitch_count": stitch_count,
            "estimated_yards": stitch_count * 0.7 / 3,  # Rough estimate
        }
    
    def generate_ripple_blanket(self, width_sts: int = 100, rows: int = 50) -> Dict:
        """Generate ripple/chevron blanket pattern"""
        pattern = []
        
        # Foundation
        pattern.append(f"Ch {width_sts + 3}")
        
        # Rows
        for row in range(1, rows + 1):
            if row == 1:
                pattern.append(f"Row 1: Dc in 4th ch from hook and each ch across")
            else:
                pattern.append(f"Row {row}: Ch 3, turn, dc in each st across")
        
        return {
            "name": "Ripple Blanket",
            "pattern": pattern,
            "dimensions": {"width_stitches": width_sts, "rows": rows},
            "estimated_yards": rows * width_sts * 0.8 / 3,
        }
    
    def generate_amigurumi_sphere(self, final_size: int = 30) -> Dict:
        """Generate amigurumi sphere pattern"""
        pattern = []
        current_count = 0
        
        pattern.append("Magic ring")
        
        # Increase rounds
        round_num = 1
        while current_count < final_size:
            if round_num == 1:
                pattern.append(f"Round {round_num}: 6 sc in magic ring (6)")
                current_count = 6
            else:
                inc_every = max(1, current_count // 6)
                pattern.append(f"Round {round_num}: *sc {inc_every - 1}, inc* around ({current_count + 6})")
                current_count += 6
            round_num += 1
        
        # Even rounds
        for i in range(5):
            pattern.append(f"Round {round_num}: Sc in each st around ({current_count})")
            round_num += 1
        
        # Decrease rounds
        while current_count > 6:
            dec_every = max(1, current_count // 6)
            pattern.append(f"Round {round_num}: *sc {dec_every - 1}, dec* around ({current_count - 6})")
            current_count -= 6
            round_num += 1
        
        pattern.append(f"Round {round_num}: Dec around (6)")
        pattern.append("Fasten off, stuff firmly")
        
        return {
            "name": "Amigurumi Sphere",
            "pattern": pattern,
            "final_size": final_size,
            "total_rounds": round_num,
        }
    
    def generate_pattern_code(self, pattern_type: str, **kwargs) -> str:
        """Generate Python code that creates a pattern"""
        if pattern_type == "granny_square":
            code = f"""
# Granny Square Pattern Generator
def generate_granny_square(rounds={kwargs.get('rounds', 4)}):
    pattern = ["Magic ring"]
    
    # Round 1
    pattern.append("Round 1: Ch 3, 2 dc, ch 2, *3 dc, ch 2* 3 times, sl st")
    
    # Subsequent rounds
    for r in range(2, rounds + 1):
        pattern.append(f"Round {{r}}: Sl st to ch-2 sp, ch 3, *3 dc, ch 2* around")
    
    return pattern

# Generate and print
pattern = generate_granny_square()
for line in pattern:
    print(line)
"""
        elif pattern_type == "rectangle":
            width = kwargs.get('width', 20)
            height = kwargs.get('height', 30)
            code = f"""
# Rectangle Pattern Generator
def generate_rectangle(width={width}, height={height}):
    pattern = [f"Ch {{width + 1}}"]
    
    for row in range(1, height + 1):
        if row == 1:
            pattern.append(f"Row 1: Sc in 2nd ch from hook and each ch across")
        else:
            pattern.append(f"Row {{row}}: Ch 1, turn, sc in each st across")
    
    return pattern

# Generate and print
pattern = generate_rectangle()
for line in pattern:
    print(line)
"""
        else:
            code = "# Pattern generator not found"
        
        return code


if __name__ == "__main__":
    print("💻 Crochet Code Generator")
    print("=" * 50)
    
    gen = PatternCodeGenerator()
    
    print("\n🟦 Generating granny square...")
    granny = gen.generate_granny_square(4)
    print(f"  Pattern: {granny['name']}")
    print(f"  Rounds: {len(granny['pattern'])}")
    print(f"  Final stitch count: {granny['final_stitch_count']}")
    print(f"  Estimated yarn: {granny['estimated_yards']:.1f} yards")
    
    print("\n🌊 Generating ripple blanket...")
    ripple = gen.generate_ripple_blanket(80, 40)
    print(f"  Pattern: {ripple['name']}")
    print(f"  Rows: {ripple['dimensions']['rows']}")
    print(f"  Estimated yarn: {ripple['estimated_yards']:.1f} yards")
    
    print("\n⚪ Generating amigurumi sphere...")
    sphere = gen.generate_amigurumi_sphere(30)
    print(f"  Pattern: {sphere['name']}")
    print(f"  Total rounds: {sphere['total_rounds']}")
    
    print("\n🐍 Generating Python code...")
    code = gen.generate_pattern_code("granny_square", rounds=5)
    print(code)
    
    print("\n✅ Code Generator ready!")
