"""
Quick Tutorial Generator - Fast tutorial creation without timeouts
Alternative to ai_tutorial_generator
"""
import json
import os
from datetime import datetime
from pathlib import Path


class QuickTutorialGenerator:
    """Generate crochet tutorials quickly and efficiently"""
    
    def __init__(self, output_dir="tutorials"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.tutorials = []
    
    def generate_text_tutorial(self, pattern_name: str, steps: list, difficulty: str = "Beginner"):
        """Generate a text-based tutorial"""
        tutorial = {
            "title": pattern_name,
            "difficulty": difficulty,
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "steps": steps,
            "type": "text"
        }
        
        # Save as JSON
        filename = f"{pattern_name.lower().replace(' ', '_')}_tutorial.json"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(tutorial, f, indent=2)
        
        self.tutorials.append(tutorial)
        return str(filepath)
    
    def generate_html_tutorial(self, pattern_name: str, steps: list, difficulty: str = "Beginner"):
        """Generate an HTML tutorial page"""
        steps_html = "\n".join([f"<li>{step}</li>" for step in steps])
        
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>{pattern_name} - Tutorial</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }}
        h1 {{ color: #667eea; }}
        .difficulty {{ background: #667eea; color: white; padding: 5px 15px; border-radius: 20px; display: inline-block; }}
        ol {{ line-height: 2; }}
        .tip {{ background: #f0f0f0; padding: 15px; border-left: 4px solid #667eea; margin: 20px 0; }}
    </style>
</head>
<body>
    <h1>{pattern_name}</h1>
    <span class="difficulty">{difficulty}</span>
    
    <h2>Steps:</h2>
    <ol>
        {steps_html}
    </ol>
    
    <div class="tip">
        <strong>💡 Tip:</strong> Take your time with each step. Practice makes perfect!
    </div>
    
    <p><em>Generated on {datetime.now().strftime("%B %d, %Y")}</em></p>
</body>
</html>"""
        
        filename = f"{pattern_name.lower().replace(' ', '_')}_tutorial.html"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w') as f:
            f.write(html_content)
        
        return str(filepath)
    
    def generate_markdown_tutorial(self, pattern_name: str, steps: list, difficulty: str = "Beginner"):
        """Generate a Markdown tutorial"""
        steps_md = "\n".join([f"{i+1}. {step}" for i, step in enumerate(steps)])
        
        md_content = f"""# {pattern_name}

**Difficulty:** {difficulty}  
**Created:** {datetime.now().strftime("%B %d, %Y")}

## Steps

{steps_md}

## Tips

- Take your time with each step
- Practice the basic stitches first
- Don't worry about perfection - handmade items have character!

---

*Happy crocheting!* 🧶
"""
        
        filename = f"{pattern_name.lower().replace(' ', '_')}_tutorial.md"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w') as f:
            f.write(md_content)
        
        return str(filepath)
    
    def generate_all_formats(self, pattern_name: str, steps: list, difficulty: str = "Beginner"):
        """Generate tutorial in all formats (text, HTML, Markdown)"""
        results = {
            "text": self.generate_text_tutorial(pattern_name, steps, difficulty),
            "html": self.generate_html_tutorial(pattern_name, steps, difficulty),
            "markdown": self.generate_markdown_tutorial(pattern_name, steps, difficulty)
        }
        
        return results
    
    def list_tutorials(self):
        """List all generated tutorials"""
        tutorials = []
        for file in self.output_dir.glob("*_tutorial.*"):
            tutorials.append(file.name)
        return tutorials


# Demo
if __name__ == "__main__":
    print("🚀 Quick Tutorial Generator")
    print("=" * 60)
    
    generator = QuickTutorialGenerator()
    
    # Sample tutorial data
    pattern_name = "Simple Scarf"
    steps = [
        "Chain 20 stitches",
        "Single crochet in second chain from hook",
        "Single crochet in each chain across (19 stitches)",
        "Chain 1 and turn",
        "Repeat rows 2-4 for 60 inches",
        "Fasten off and weave in ends"
    ]
    
    print(f"\n📝 Generating tutorials for: {pattern_name}")
    
    # Generate all formats
    results = generator.generate_all_formats(pattern_name, steps, "Beginner")
    
    print("\n✅ Generated tutorials:")
    for format_type, filepath in results.items():
        print(f"  • {format_type}: {filepath}")
    
    print(f"\n📂 All tutorials saved in: {generator.output_dir}")
    print(f"📊 Total tutorials: {len(generator.list_tutorials())}")
    
    print("\n✨ Quick Tutorial Generator complete!")
