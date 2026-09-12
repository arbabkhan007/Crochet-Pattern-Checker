"""
Pattern Watermark Generator - Add professional watermarks to pattern images and PDFs
"""
from typing import Dict
from pathlib import Path


class PatternWatermarkGenerator:
    """Add watermarks to protect your patterns"""
    
    def __init__(self):
        self.watermark_styles = {
            "subtle": {"opacity": 0.3, "position": "center", "repeat": False},
            "diagonal": {"opacity": 0.4, "position": "diagonal", "repeat": True},
            "corner": {"opacity": 0.5, "position": "bottom-right", "repeat": False},
            "heavy": {"opacity": 0.6, "position": "center", "repeat": True},
        }
    
    def generate_watermark_html(self, text: str, style: str = "subtle", 
                                output_file: str = "watermark_preview.html") -> str:
        """Generate HTML preview of watermark"""
        
        config = self.watermark_styles.get(style, self.watermark_styles["subtle"])
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Pattern Watermark Preview</title>
    <style>
        body {{
            margin: 0;
            padding: 40px;
            background: #f5f5f5;
            font-family: Arial, sans-serif;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            position: relative;
            overflow: hidden;
        }}
        .watermark {{
            position: absolute;
            color: rgba(0, 0, 0, {config['opacity']});
            font-size: 3em;
            font-weight: bold;
            pointer-events: none;
            user-select: none;
        }}
        .watermark.subtle {{
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%) rotate(-15deg);
        }}
        .watermark.diagonal {{
            top: 0;
            left: 0;
            width: 200%;
            height: 200%;
            display: flex;
            flex-wrap: wrap;
            align-content: flex-start;
            transform: rotate(-30deg);
            transform-origin: top left;
        }}
        .watermark.diagonal span {{
            margin: 50px;
        }}
        .watermark.corner {{
            bottom: 20px;
            right: 20px;
            font-size: 2em;
        }}
        .content {{
            position: relative;
            z-index: 1;
        }}
        .controls {{
            margin-top: 20px;
            padding: 20px;
            background: #e8e8e8;
            border-radius: 8px;
        }}
        button {{
            padding: 10px 20px;
            margin: 5px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }}
        button:hover {{ background: #764ba2; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="watermark {style}" id="watermark">
            {self._generate_watermark_content(text, style)}
        </div>
        <div class="content">
            <h1>🧶 Crochet Pattern</h1>
            <h2>Sample Pattern Content</h2>
            <p>This is a preview of how your watermark will look on pattern pages.</p>
            <h3>Materials:</h3>
            <ul>
                <li>Worsted weight yarn - 500 yards</li>
                <li>5.0mm crochet hook</li>
                <li>Stitch markers</li>
            </ul>
            <h3>Instructions:</h3>
            <p>Row 1: Ch 20, sc in 2nd ch from hook and each ch across</p>
            <p>Row 2: Ch 1, turn, sc in each st across</p>
        </div>
    </div>
    
    <div class="controls">
        <h3>Watermark Styles:</h3>
        <button onclick="changeStyle('subtle')">Subtle</button>
        <button onclick="changeStyle('diagonal')">Diagonal</button>
        <button onclick="changeStyle('corner')">Corner</button>
        <button onclick="changeStyle('heavy')">Heavy</button>
    </div>
    
    <script>
        function changeStyle(style) {{
            const watermark = document.getElementById('watermark');
            watermark.className = 'watermark ' + style;
            watermark.innerHTML = {self._generate_watermark_content(text, style, js=True)};
        }}
    </script>
</body>
</html>"""
        
        with open(output_file, 'w') as f:
            f.write(html)
        
        return output_file
    
    def _generate_watermark_content(self, text: str, style: str, js: bool = False) -> str:
        """Generate watermark HTML content"""
        if style == "diagonal" or style == "heavy":
            repeats = 20 if style == "diagonal" else 30
            if js:
                return f"Array({repeats}).fill('<span>{text}</span>').join('')"
            return "".join([f"<span>{text}</span>" for _ in range(repeats)])
        else:
            return text
    
    def generate_watermark_css(self, text: str, style: str = "subtle") -> str:
        """Generate CSS for adding watermarks to existing pages"""
        config = self.watermark_styles.get(style, self.watermark_styles["subtle"])
        
        css = f"""
/* Watermark Styles */
.watermark {{
    position: absolute;
    color: rgba(0, 0, 0, {config['opacity']});
    font-size: 3em;
    font-weight: bold;
    pointer-events: none;
    user-select: none;
    z-index: 9999;
}}

.watermark.subtle {{
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%) rotate(-15deg);
}}

.watermark.corner {{
    bottom: 20px;
    right: 20px;
    font-size: 2em;
}}
"""
        return css


if __name__ == "__main__":
    print("🔒 Pattern Watermark Generator")
    print("=" * 50)
    
    generator = PatternWatermarkGenerator()
    
    print("\n🎨 Generating watermark previews...")
    output = generator.generate_watermark_html("© Your Name 2024", "subtle")
    print(f"✅ Watermark preview saved to: {output}")
    
    print("\n📋 Available styles:")
    for style in generator.watermark_styles:
        print(f"  • {style}")
    
    print("\n💡 Usage:")
    print("  Open the HTML file in your browser to see different watermark styles")
    print("  Choose the style that best protects your patterns")
    
    print("\n✅ Watermark Generator ready!")
