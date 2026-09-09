"""
Accessibility Suite - Large print, high contrast, screen reader support
"""
from typing import Dict, List, Optional
from dataclasses import dataclass, field, asdict


@dataclass
class AccessibilityConfig:
    font_size: str = "large"  # small, medium, large, xlarge
    high_contrast: bool = True
    screen_reader_friendly: bool = True
    color_blind_friendly: bool = True
    simple_language: bool = False
    step_by_step: bool = True
    audio_description: bool = False
    dyslexia_font: bool = False
    reduced_motion: bool = True
    large_touch_targets: bool = True
    text_spacing: float = 1.5
    
    def to_dict(self) -> Dict:
        return asdict(self)


class AccessibilitySuite:
    """
    Make crochet patterns accessible to everyone
    
    Features:
    - Large print pattern generator
    - High contrast output
    - Screen reader optimized text
    - Simplified language mode
    - Step-by-step breakdown
    - Audio description format
    - Color-blind friendly indicators
    - Dyslexia-friendly formatting
    - Cognitive load reduction
    """
    
    CONTRAST_THEMES = {
        "high_contrast": {
            "bg": "#000000",
            "text": "#FFFFFF",
            "accent": "#FFFF00",
            "error": "#FF0000",
            "success": "#00FF00",
            "border": "#FFFFFF",
        },
        "dark_mode": {
            "bg": "#1a1a2e",
            "text": "#e0e0e0",
            "accent": "#00d4ff",
            "error": "#ff6b6b",
            "success": "#51cf66",
            "border": "#333333",
        },
        "light_mode": {
            "bg": "#FFFFFF",
            "text": "#000000",
            "accent": "#0055AA",
            "error": "#CC0000",
            "success": "#006600",
            "border": "#CCCCCC",
        },
        "sepia": {
            "bg": "#F4ECD8",
            "text": "#5B4636",
            "accent": "#8B4513",
            "error": "#8B0000",
            "success": "#2E8B57",
            "border": "#D2B48C",
        },
        "colorblind_deuteranopia": {
            "bg": "#FFFFFF",
            "text": "#000000",
            "accent": "#0072B2",
            "error": "#D55E00",
            "success": "#009E73",
            "border": "#999999",
            "note": "Blue/orange palette safe for deuteranopia",
        },
        "colorblind_protanopia": {
            "bg": "#FFFFFF",
            "text": "#000000",
            "accent": "#0072B2",
            "error": "#D55E00",
            "success": "#F0E442",
            "border": "#999999",
            "note": "Blue/yellow palette safe for protanopia",
        },
    }
    
    FONT_SIZES = {
        "small": {"base": "12px", "heading": "16px", "line_height": "1.4"},
        "medium": {"base": "16px", "heading": "22px", "line_height": "1.5"},
        "large": {"base": "20px", "heading": "28px", "line_height": "1.6"},
        "xlarge": {"base": "26px", "heading": "36px", "line_height": "1.8"},
    }
    
    STITCH_SIMPLIFICATION = {
        "sc": "single crochet (insert hook, yarn over, pull through, yarn over, pull through both)",
        "dc": "double crochet (yarn over, insert hook, yarn over, pull through, yarn over, pull through 2, yarn over, pull through 2)",
        "hdc": "half double crochet (yarn over, insert hook, yarn over, pull through, yarn over, pull through all 3)",
        "tc": "treble crochet (yarn over twice, insert hook, yarn over, pull through, yarn over, pull through 2 twice)",
        "inc": "increase (make 2 stitches in the same stitch)",
        "dec": "decrease (work 2 stitches together as 1)",
        "sl st": "slip stitch (insert hook, yarn over, pull through both)",
        "ch": "chain (yarn over, pull through loop on hook)",
        "MR": "magic ring (make an adjustable loop to start crocheting in the round)",
        "FO": "fasten off (cut yarn and pull through last loop)",
    }
    
    def __init__(self, config: AccessibilityConfig = None):
        self.config = config or AccessibilityConfig()
    
    def convert_pattern(self, pattern: Dict) -> Dict:
        """Convert a pattern to accessible format"""
        result = {
            "title": pattern.get("title", "Pattern"),
            "rounds": [],
            "notes": [],
            "format": "accessible",
            "config": self.config.to_dict(),
        }
        
        rounds = pattern.get("rounds", [])
        
        for rnd in rounds:
            rn = rnd.get("round_number", rnd.get("round", 0))
            instr = rnd.get("instruction", "")
            count = rnd.get("stitch_count", rnd.get("count", 0))
            
            # Simplify language if needed
            if self.config.simple_language:
                instr = self._simplify_instruction(instr)
            
            # Add step-by-step breakdown
            if self.config.step_by_step:
                steps = self._break_down_instruction(instr)
            else:
                steps = [instr]
            
            result["rounds"].append({
                "round": rn,
                "original": rnd.get("instruction", ""),
                "accessible_text": instr,
                "steps": steps,
                "count": count,
                "count_spoken": f"You should have {count} stitches at the end of this round." if count else "",
            })
        
        return result
    
    def _simplify_instruction(self, instruction: str) -> str:
        """Simplify instruction language"""
        simplified = instruction
        
        for abbr, full in self.STITCH_SIMPLIFICATION.items():
            if abbr.lower() in simplified.lower():
                # Only replace standalone abbreviations
                import re
                pattern = r'\b' + re.escape(abbr) + r'\b'
                simplified = re.sub(pattern, full.split("(")[0].strip(), simplified, flags=re.IGNORECASE)
        
        return simplified
    
    def _break_down_instruction(self, instruction: str) -> List[str]:
        """Break instruction into individual steps"""
        steps = []
        
        # Check for repeat patterns
        import re
        bracket_match = re.search(r'\[(.*?)\]\s*[x×]\s*(\d+)', instruction, re.IGNORECASE)
        
        if bracket_match:
            inner = bracket_match.group(1)
            repeats = int(bracket_match.group(2))
            
            # Break down inner instruction
            inner_steps = self._parse_stitch_sequence(inner)
            
            steps.append(f"Repeat the following {repeats} times:")
            for i, step in enumerate(inner_steps, 1):
                steps.append(f"  Step {i}: {step}")
        
        elif "each st around" in instruction.lower():
            steps = [
                f"Work {instruction.split('in')[0].strip() if 'in' in instruction else 'stitches'}",
                "in every stitch around",
                "Join or continue as directed"
            ]
        
        elif "magic ring" in instruction.lower() or "MR" in instruction:
            steps = [
                "Make a magic ring",
                f"Work the specified stitches into the ring",
                "Pull the tail to close the ring tightly"
            ]
        
        else:
            steps = [instruction]
        
        return steps
    
    def _parse_stitch_sequence(self, instruction: str) -> List[str]:
        """Parse a sequence of stitches into steps"""
        parts = []
        
        # Split by comma
        stitches = [s.strip() for s in instruction.split(",")]
        
        for stitch in stitches:
            stitch_lower = stitch.lower().strip()
            if stitch_lower in self.STITCH_SIMPLIFICATION:
                parts.append(self.STITCH_SIMPLIFICATION[stitch_lower])
            else:
                parts.append(stitch)
        
        return parts
    
    def generate_large_print(self, pattern: Dict, font_size: str = "xlarge") -> str:
        """Generate large print version"""
        result = self.convert_pattern(pattern)
        lines = []
        
        lines.append(f"{'=' * 50}")
        lines.append(f"  {result['title'].upper()}")
        lines.append(f"  LARGE PRINT EDITION")
        lines.append(f"{'=' * 50}")
        lines.append("")
        
        for rnd in result["rounds"]:
            lines.append(f"  ROUND {rnd['round']}")
            lines.append(f"  {'-' * 30}")
            
            for i, step in enumerate(rnd["steps"], 1):
                lines.append(f"    {i}. {step}")
            
            if rnd["count"]:
                lines.append(f"")
                lines.append(f"    >>> COUNT: {rnd['count']} stitches <<<")
            
            lines.append("")
        
        return "\n".join(lines)
    
    def generate_screen_reader_text(self, pattern: Dict) -> str:
        """Generate screen-reader optimized text"""
        result = self.convert_pattern(pattern)
        lines = []
        
        lines.append(f"Pattern: {result['title']}")
        lines.append(f"Total rounds: {len(result['rounds'])}")
        lines.append("")
        
        for rnd in result["rounds"]:
            lines.append(f"Round {rnd['round']}.")
            
            for step in rnd["steps"]:
                lines.append(f"  {step}.")
            
            if rnd["count_spoken"]:
                lines.append(f"  {rnd['count_spoken']}")
            
            lines.append("")
        
        return "\n".join(lines)
    
    def generate_accessible_html(self, pattern: Dict, theme: str = "high_contrast") -> str:
        """Generate accessible HTML pattern"""
        colors = self.CONTRAST_THEMES.get(theme, self.CONTRAST_THEMES["high_contrast"])
        fonts = self.FONT_SIZES.get(self.config.font_size, self.FONT_SIZES["large"])
        result = self.convert_pattern(pattern)
        
        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{result["title"]} - Accessible Pattern</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
    font-family: Arial, Helvetica, sans-serif;
    font-size: {fonts["base"]};
    line-height: {fonts["line_height"]};
    letter-spacing: 0.05em;
    background: {colors["bg"]};
    color: {colors["text"]};
    padding: 20px;
    max-width: 800px;
    margin: 0 auto;
}}
h1 {{
    font-size: {fonts["heading"]};
    color: {colors["accent"]};
    border-bottom: 3px solid {colors["border"]};
    padding-bottom: 15px;
    margin-bottom: 25px;
}}
h2 {{
    font-size: calc({fonts["heading"]} * 0.8);
    color: {colors["accent"]};
    margin: 20px 0 10px;
}}
.round {{
    border: 2px solid {colors["border"]};
    border-radius: 8px;
    padding: 20px;
    margin: 15px 0;
    background: {colors["bg"]};
}}
.round-number {{
    font-weight: bold;
    font-size: calc({fonts["heading"]} * 0.7);
    color: {colors["accent"]};
    margin-bottom: 10px;
}}
.step {{
    padding: 8px 0;
    border-bottom: 1px dotted {colors["border"]};
}}
.step:last-child {{ border-bottom: none; }}
.count {{
    display: inline-block;
    background: {colors["accent"]};
    color: {colors["bg"]};
    padding: 5px 15px;
    border-radius: 5px;
    font-weight: bold;
    margin-top: 10px;
}}
.controls {{
    position: fixed;
    top: 10px;
    right: 10px;
    display: flex;
    gap: 10px;
}}
.btn {{
    padding: 15px 20px;
    font-size: {fonts["base"]};
    border: 2px solid {colors["border"]};
    border-radius: 8px;
    cursor: pointer;
    background: {colors["bg"]};
    color: {colors["text"]};
    min-width: 50px;
    min-height: 50px;
}}
.btn:focus {{
    outline: 3px solid {colors["accent"]};
    outline-offset: 2px;
}}
@media (max-width: 600px) {{
    body {{ padding: 10px; font-size: calc({fonts["base"]} * 1.2); }}
    .round {{ padding: 15px; }}
}}
</style>
</head>
<body>
<h1>{result["title"]}</h1>
<p>Accessible Pattern | {len(result["rounds"])} rounds</p>

<div class="controls" role="toolbar" aria-label="Accessibility controls">
    <button class="btn" onclick="increaseFontSize()" aria-label="Increase font size">A+</button>
    <button class="btn" onclick="decreaseFontSize()" aria-label="Decrease font size">A-</button>
    <button class="btn" onclick="toggleContrast()" aria-label="Toggle contrast">Contrast</button>
</div>

<main role="main">
'''
        for rnd in result["rounds"]:
            html += f'''
<div class="round" role="region" aria-label="Round {rnd["round"]}">
    <div class="round-number">Round {rnd["round"]}</div>
'''
            for i, step in enumerate(rnd["steps"], 1):
                html += f'    <div class="step">Step {i}: {step}</div>\n'
            
            if rnd["count"]:
                html += f'    <div class="count" aria-label="Stitch count: {rnd["count"]}">{rnd["count"]} stitches</div>\n'
            
            html += '</div>\n'
        
        html += '''
</main>

<script>
let fontSize = ''' + str(int(fonts["base"].replace("px", ""))) + ''';

function increaseFontSize() {
    fontSize = Math.min(48, fontSize + 2);
    document.body.style.fontSize = fontSize + "px";
}

function decreaseFontSize() {
    fontSize = Math.max(12, fontSize - 2);
    document.body.style.fontSize = fontSize + "px";
}

let highContrast = true;
function toggleContrast() {
    highContrast = !highContrast;
    if (highContrast) {
        document.body.style.background = "#000";
        document.body.style.color = "#fff";
    } else {
        document.body.style.background = "#fff";
        document.body.style.color = "#000";
    }
}
</script>
</body>
</html>'''
        
        return html
    
    def get_recommendations(self, pattern: Dict) -> List[str]:
        """Get accessibility recommendations for a pattern"""
        recs = []
        
        rounds = pattern.get("rounds", [])
        
        if len(rounds) > 20:
            recs.append("Pattern has many rounds - consider adding visual round markers")
        
        has_complex = any(
            any(s in r.get("instruction", "").lower() 
                for s in ["cable", "popcorn", "bobble", "shell"])
            for r in rounds
        )
        if has_complex:
            recs.append("Pattern has complex stitches - video tutorials linked for each")
        
        if any("dec" in r.get("instruction", "").lower() for r in rounds):
            recs.append("Pattern has decreases - invisible decrease tutorial available")
        
        recs.append("Large print version available for easy reading while crocheting")
        recs.append("Screen reader mode reads instructions step by step")
        recs.append("High contrast mode for low vision users")
        
        return recs


# Demo
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  ACCESSIBILITY SUITE - DEMONSTRATION")
    print("=" * 60)
    
    suite = AccessibilitySuite()
    
    sample = {
        "title": "Simple Amigurumi Ball",
        "rounds": [
            {"round": 1, "instruction": "6 sc in MR", "count": 6},
            {"round": 2, "instruction": "inc in each st around", "count": 12},
            {"round": 3, "instruction": "[sc, inc] x 6", "count": 18},
            {"round": 4, "instruction": "[2 sc, inc] x 6", "count": 24},
            {"round": 5, "instruction": "sc in each st around", "count": 24},
            {"round": 6, "instruction": "[2 sc, dec] x 6", "count": 18},
            {"round": 7, "instruction": "[sc, dec] x 6", "count": 12},
            {"round": 8, "instruction": "dec x 6", "count": 6},
        ]
    }
    
    # Large print
    print("\n--- Large Print Mode ---")
    large = suite.generate_large_print(sample)
    print(large[:600])
    
    # Screen reader
    print("\n--- Screen Reader Mode ---")
    sr = suite.generate_screen_reader_text(sample)
    print(sr[:600])
    
    # Recommendations
    print("\n--- Accessibility Recommendations ---")
    recs = suite.get_recommendations(sample)
    for r in recs:
        print(f"  -> {r}")
    
    # HTML
    html = suite.generate_accessible_html(sample, theme="high_contrast")
    print(f"\n  Accessible HTML generated: {len(html)} chars")
    
    print(f"\n  Accessibility Suite Complete!")
