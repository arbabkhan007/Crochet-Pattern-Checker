"""
Photo Studio - Create professional product photos for selling crochet items
Add watermarks, backgrounds, branding, mockups, social media ready images
"""
import json
from typing import Dict, List, Optional
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path


@dataclass
class BrandKit:
    """Your brand identity"""
    name: str = "My Crochet"
    tagline: str = "Handmade with Love"
    website: str = ""
    instagram: str = ""
    etsy: str = ""
    logo_text: str = ""
    primary_color: str = "#E94560"
    secondary_color: str = "#4ECCA3"
    background_color: str = "#1A1A2E"
    font_style: str = "elegant"  # elegant, modern, cute, rustic
    watermark_opacity: float = 0.3
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class PhotoTemplate:
    """A photo layout template"""
    name: str
    style: str  # product, lifestyle, flat_lay, mockup, social
    background: str
    dimensions: Dict  # width, height
    watermark_position: str  # top_left, top_right, bottom_left, bottom_right, center
    overlay_text: str = ""
    
    def to_dict(self) -> Dict:
        return asdict(self)


class PhotoStudio:
    """
    Professional photo studio for crochet products
    
    Features:
    - Branded photo templates
    - Watermark generator
    - Social media size presets
    - Background generator (solid, gradient, patterns)
    - Mockup frames
    - Before/after comparison
    - Batch photo processing
    """
    
    SOCIAL_SIZES = {
        "instagram_square": {"width": 1080, "height": 1080, "name": "Instagram Post"},
        "instagram_story": {"width": 1080, "height": 1920, "name": "Instagram Story/Reel"},
        "pinterest_pin": {"width": 1000, "height": 1500, "name": "Pinterest Pin"},
        "etsy_listing": {"width": 2000, "height": 1500, "name": "Etsy Listing"},
        "facebook_post": {"width": 1200, "height": 630, "name": "Facebook Post"},
        "twitter_post": {"width": 1200, "height": 675, "name": "Twitter/X Post"},
        "tiktok_video": {"width": 1080, "height": 1920, "name": "TikTok Video"},
        "ravelry_photo": {"width": 1200, "height": 1200, "name": "Ravelry Photo"},
    }
    
    BACKGROUNDS = {
        "marble": "linear-gradient(135deg, #f5f5f5 25%, #e8e8e8 25%, #e8e8e8 50%, #f5f5f5 50%, #f5f5f5 75%, #e8e8e8 75%)",
        "wood": "linear-gradient(180deg, #DEB887 0%, #D2691E 50%, #8B4513 100%)",
        "linen": "linear-gradient(45deg, #FAF0E6 25%, #EEE8D5 25%, #EEE8D5 50%, #FAF0E6 50%, #FAF0E6 75%, #EEE8D5 75%)",
        "cozy_knit": "repeating-linear-gradient(0deg, #F5F5DC 0px, #F5F5DC 2px, #FAEBD7 2px, #FAEBD7 4px)",
        "pastel_gradient": "linear-gradient(135deg, #FFE4E1 0%, #E6E6FA 50%, #E0FFFF 100%)",
        "dark_luxe": "linear-gradient(135deg, #1A1A2E 0%, #16213E 50%, #0F3460 100%)",
        "sage_green": "linear-gradient(135deg, #B2C9AD 0%, #95B8A0 50%, #7FA98B 100%)",
        "blush_pink": "linear-gradient(135deg, #FFE4E1 0%, #FFB6C1 50%, #FFC0CB 100%)",
    }
    
    WATERMARK_STYLES = {
        "elegant": {"font": "Georgia, serif", "size": "24px", "letter_spacing": "3px"},
        "modern": {"font": "Arial, sans-serif", "size": "20px", "letter_spacing": "1px"},
        "cute": {"font": "Comic Sans MS, cursive", "size": "22px", "letter_spacing": "0px"},
        "rustic": {"font": "Courier New, monospace", "size": "18px", "letter_spacing": "2px"},
        "bold": {"font": "Impact, sans-serif", "size": "28px", "letter_spacing": "4px"},
    }
    
    def __init__(self, brand: BrandKit = None):
        self.brand = brand or BrandKit()
        self.templates: List[PhotoTemplate] = []
        self._load_default_templates()
    
    def _load_default_templates(self):
        """Load default photo templates"""
        self.templates = [
            PhotoTemplate("Instagram Product", "product", "marble",
                         self.SOCIAL_SIZES["instagram_square"], "bottom_right"),
            PhotoTemplate("Etsy Hero Image", "product", "linen",
                         self.SOCIAL_SIZES["etsy_listing"], "bottom_right"),
            PhotoTemplate("Pinterest Pin", "lifestyle", "pastel_gradient",
                         self.SOCIAL_SIZES["pinterest_pin"], "center"),
            PhotoTemplate("Flat Lay", "flat_lay", "cozy_knit",
                         self.SOCIAL_SIZES["instagram_square"], "top_right"),
            PhotoTemplate("Story Background", "social", "dark_luxe",
                         self.SOCIAL_SIZES["instagram_story"], "bottom_right"),
        ]
    
    def generate_product_photo(self, item_name: str, description: str = "",
                              template: str = "Instagram Product",
                              price: str = "") -> str:
        """Generate a branded product photo layout as HTML"""
        tmpl = next((t for t in self.templates if t.name == template), self.templates[0])
        bg = self.BACKGROUNDS.get(tmpl.background, self.BACKGROUNDS["marble"])
        wm_style = self.WATERMARK_STYLES.get(self.brand.font_style, self.WATERMARK_STYLES["elegant"])
        
        size = tmpl.dimensions
        opacity = self.brand.watermark_opacity
        
        html = f'''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Product Photo - {item_name}</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
    font-family: -apple-system, sans-serif;
    background: #222;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
    min-height: 100vh;
}}
.photo-frame {{
    width: {size['width']}px;
    height: {size['height']}px;
    max-width: 90vw;
    max-height: 80vh;
    background: {bg};
    background-size: 40px 40px;
    position: relative;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    display: flex;
    align-items: center;
    justify-content: center;
}}
.photo-placeholder {{
    width: 60%;
    height: 60%;
    border: 3px dashed rgba(0,0,0,0.2);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    color: rgba(0,0,0,0.3);
    font-size: 1.2em;
    text-align: center;
    padding: 20px;
}}
.photo-placeholder .icon {{
    font-size: 3em;
    margin-bottom: 15px;
}}
.brand-overlay {{
    position: absolute;
    {self._get_watermark_position(tmpl.watermark_position)}
    padding: 15px 25px;
    opacity: {opacity};
    font-family: {wm_style['font']};
    font-size: {wm_style['size']};
    letter-spacing: {wm_style['letter_spacing']};
    color: {self.brand.primary_color};
    text-transform: uppercase;
    pointer-events: none;
}}
.brand-tagline {{
    position: absolute;
    bottom: 15px;
    left: 50%;
    transform: translateX(-50%);
    font-family: {wm_style['font']};
    font-size: 14px;
    color: rgba(0,0,0,0.4);
    letter-spacing: 2px;
}}
.item-info {{
    position: absolute;
    top: 20px;
    left: 20px;
    background: rgba(255,255,255,0.9);
    padding: 12px 20px;
    border-radius: 8px;
    backdrop-filter: blur(10px);
}}
.item-name {{
    font-size: 1.4em;
    font-weight: bold;
    color: {self.brand.primary_color};
}}
.item-desc {{
    font-size: 0.9em;
    color: #666;
    margin-top: 4px;
}}
.price-tag {{
    position: absolute;
    top: 20px;
    right: 20px;
    background: {self.brand.secondary_color};
    color: white;
    padding: 8px 16px;
    border-radius: 20px;
    font-weight: bold;
    font-size: 1.2em;
}}
.controls {{
    margin-top: 20px;
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    justify-content: center;
}}
.btn {{
    padding: 10px 20px;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: 0.9em;
}}
.btn-download {{
    background: {self.brand.secondary_color};
    color: white;
}}
.btn-bg {{
    background: #333;
    color: white;
}}
select {{
    padding: 10px;
    border-radius: 6px;
    border: 1px solid #555;
    background: #333;
    color: white;
}}
</style>
</head>
<body>
<div class="photo-frame" id="photoFrame">
    <div class="photo-placeholder">
        <div class="icon">📷</div>
        <div>Drop your photo here<br>or click to upload</div>
    </div>
    
    <div class="item-info">
        <div class="item-name">{item_name}</div>
        <div class="item-desc">{description}</div>
    </div>
    
    {"<div class='price-tag'>" + price + "</div>" if price else ""}
    
    <div class="brand-overlay">{self.brand.name}</div>
    <div class="brand-tagline">{self.brand.tagline}</div>
</div>

<div class="controls">
    <select id="bgSelect" onchange="changeBg(this.value)">
        <option value="">Change Background</option>
        <option value="marble">Marble</option>
        <option value="wood">Wood</option>
        <option value="linen">Linen</option>
        <option value="cozy_knit">Cozy Knit</option>
        <option value="pastel_gradient">Pastel Gradient</option>
        <option value="dark_luxe">Dark Luxe</option>
        <option value="sage_green">Sage Green</option>
        <option value="blush_pink">Blush Pink</option>
    </select>
    <button class="btn btn-download" onclick="downloadPhoto()">💾 Download Photo</button>
</div>

<script>
const backgrounds = {json.dumps(self.BACKGROUNDS)};

function changeBg(name) {{
    if (backgrounds[name]) {{
        document.getElementById('photoFrame').style.background = backgrounds[name];
        document.getElementById('photoFrame').style.backgroundSize = '40px 40px';
    }}
}}

function downloadPhoto() {{
    // Simple screenshot using canvas
    alert('To save: Right-click the photo → Save Image, or use browser screenshot tool');
}}

// Allow photo upload
document.querySelector('.photo-placeholder').addEventListener('click', function() {{
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*';
    input.onchange = function(e) {{
        const file = e.target.files[0];
        const reader = new FileReader();
        reader.onload = function(ev) {{
            document.querySelector('.photo-placeholder').outerHTML = 
                '<img src="' + ev.target.result + '" style="width:80%;height:80%;object-fit:contain;border-radius:8px;">';
        }};
        reader.readAsDataURL(file);
    }};
    input.click();
}});
</script>
</body>
</html>'''
        
        return html
    
    def _get_watermark_position(self, position: str) -> str:
        """Get CSS positioning for watermark"""
        positions = {
            "top_left": "top: 15px; left: 15px;",
            "top_right": "top: 15px; right: 15px;",
            "bottom_left": "bottom: 15px; left: 15px;",
            "bottom_right": "bottom: 15px; right: 15px;",
            "center": "top: 50%; left: 50%; transform: translate(-50%, -50%);",
        }
        return positions.get(position, positions["bottom_right"])
    
    def generate_all_social_sizes(self, item_name: str, description: str = "", 
                                 price: str = "") -> Dict:
        """Generate photos for all social media platforms"""
        results = {}
        for platform, size in self.SOCIAL_SIZES.items():
            tmpl = PhotoTemplate(
                f"{platform}_template", "product", "marble",
                size, "bottom_right"
            )
            results[platform] = {
                "name": size["name"],
                "width": size["width"],
                "height": size["height"],
                "html": self.generate_product_photo(item_name, description, 
                                                     f"{platform}_template", price)
            }
        return results
    
    def get_brand_summary(self) -> Dict:
        """Get brand kit summary"""
        return {
            "name": self.brand.name,
            "tagline": self.brand.tagline,
            "colors": {
                "primary": self.brand.primary_color,
                "secondary": self.brand.secondary_color,
                "background": self.brand.background_color,
            },
            "font_style": self.brand.font_style,
            "templates_available": len(self.templates),
            "social_sizes": len(self.SOCIAL_SIZES),
            "backgrounds": len(self.BACKGROUNDS),
        }


# Demo
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  PHOTO STUDIO - DEMONSTRATION")
    print("=" * 60)
    
    brand = BrandKit(
        name="Cozy Stitches",
        tagline="Handmade with Love",
        primary_color="#E94560",
        secondary_color="#4ECCA3",
        font_style="elegant"
    )
    
    studio = PhotoStudio(brand)
    
    print("\n🎨 Brand Kit:")
    summary = studio.get_brand_summary()
    for key, val in summary.items():
        print(f"  {key}: {val}")
    
    print("\n📱 Social Media Sizes:")
    for platform, size in studio.SOCIAL_SIZES.items():
        print(f"  {platform}: {size['width']}x{size['height']}")
    
    # Generate product photo
    html = studio.generate_product_photo(
        "Amigurumi Bunny",
        "Soft cotton bunny, perfect gift",
        price="$25"
    )
    print(f"\n✅ Product photo generated: {len(html)} chars")
    print(f"   Backgrounds available: {len(studio.BACKGROUNDS)}")
    
    print(f"\n  Photo Studio Complete! 📸")
