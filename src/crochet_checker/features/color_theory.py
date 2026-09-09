"""
Color Theory Tool - Color wheels, palettes, and harmony for crochet projects
"""
import colorsys
import math
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field, asdict


@dataclass
class CrochetColor:
    """A color with crochet-specific info"""
    name: str
    hex_code: str
    yarn_brand: str = ""
    yarn_line: str = ""
    dye_lot: str = ""
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @property
    def rgb(self) -> Tuple[int, int, int]:
        h = self.hex_code.lstrip('#')
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    
    @property
    def hsl(self) -> Tuple[float, float, float]:
        r, g, b = [x / 255.0 for x in self.rgb]
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        return (round(h * 360), round(s * 100), round(l * 100))
    
    @property
    def is_warm(self) -> bool:
        h = self.hsl[0]
        return (h < 60 or h > 300)
    
    @property
    def is_cool(self) -> bool:
        h = self.hsl[0]
        return 120 < h < 270
    
    @property
    def brightness(self) -> str:
        l = self.hsl[2]
        if l < 30: return "dark"
        elif l < 60: return "medium"
        else: return "light"
    
    @property
    def saturation(self) -> str:
        s = self.hsl[1]
        if s < 20: return "muted"
        elif s < 60: return "moderate"
        else: return "vivid"


class ColorTheory:
    """
    Color theory tools for crochet projects
    
    Features:
    - Color wheel generation
    - Complementary colors
    - Analogous color schemes
    - Triadic color schemes
    - Split-complementary
    - Monochromatic palettes
    - Contrast checking
    - Yarn color matching
    - Seasonal palettes
    - Mood-based palettes
    """
    
    SEASONAL_PALETTES = {
        "spring": [
            ("#FFB7C5", "Cherry Blossom"), ("#98FB98", "Pale Green"),
            ("#FFFACD", "Lemon Chiffon"), ("#DDA0DD", "Plum"),
            ("#87CEEB", "Sky Blue"), ("#FFDAB9", "Peach"),
        ],
        "summer": [
            ("#FF6347", "Tomato"), ("#00CED1", "Dark Turquoise"),
            ("#FFD700", "Gold"), ("#FF69B4", "Hot Pink"),
            ("#32CD32", "Lime Green"), ("#FF4500", "Orange Red"),
        ],
        "autumn": [
            ("#8B4513", "Saddle Brown"), ("#D2691E", "Chocolate"),
            ("#DAA520", "Goldenrod"), ("#B22222", "Firebrick"),
            ("#556B2F", "Dark Olive"), ("#CD853F", "Peru"),
        ],
        "winter": [
            ("#191970", "Midnight Blue"), ("#DC143C", "Crimson"),
            ("#2F4F4F", "Dark Slate"), ("#F5F5F5", "White Smoke"),
            ("#4169E1", "Royal Blue"), ("#800020", "Burgundy"),
        ],
    }
    
    MOOD_PALETTES = {
        "calm": [("#B0C4DE", "Light Steel"), ("#E6E6FA", "Lavender"),
                ("#F0FFF0", "Honeydew"), ("#F5F5DC", "Beige"),
                ("#E0FFFF", "Light Cyan")],
        "energetic": [("#FF4500", "Orange Red"), ("#FFD700", "Gold"),
                     ("#FF1493", "Deep Pink"), ("#00FF7F", "Spring Green"),
                     ("#FF6347", "Tomato")],
        "romantic": [("#FFB6C1", "Light Pink"), ("#DDA0DD", "Plum"),
                    ("#FFC0CB", "Pink"), ("#DB7093", "Pale Violet"),
                    ("#FFF0F5", "Lavender Blush")],
        "earthy": [("#8B4513", "Saddle Brown"), ("#D2B48C", "Tan"),
                  ("#556B2F", "Dark Olive"), ("#DEB887", "Burlywood"),
                  ("#A0522D", "Sienna")],
        "ocean": [("#003366", "Navy"), ("#006994", "Pacific"),
                 ("#40E0D0", "Turquoise"), ("#E0FFFF", "Light Cyan"),
                 ("#F0FFFF", "Azure")],
        "sunset": [("#FF4500", "Orange Red"), ("#FF8C00", "Dark Orange"),
                  ("#FFD700", "Gold"), ("#FF1493", "Deep Pink"),
                  ("#8B008B", "Dark Magenta")],
    }
    
    YARN_BRAND_COLORS = {
        "Red Heart Super Saver": [
            "#CC0000", "#000080", "#228B22", "#FFD700", "#FFFFFF",
            "#000000", "#FF69B4", "#808080", "#8B4513", "#FFA500"
        ],
        "Scheepjes Catona": [
            "#FFFFFF", "#106", "#256", "#384", "#145",
            "#608", "#392", "#252", "#104", "#611"
        ],
    }
    
    def complementary(self, hex_code: str) -> str:
        """Get the complementary color"""
        r, g, b = self._hex_to_rgb(hex_code)
        h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
        comp_h = (h + 0.5) % 1.0
        cr, cg, cb = colorsys.hls_to_rgb(comp_h, l, s)
        return self._rgb_to_hex(int(cr*255), int(cg*255), int(cb*255))
    
    def analogous(self, hex_code: str, count: int = 5, angle: float = 30) -> List[str]:
        """Get analogous colors"""
        r, g, b = self._hex_to_rgb(hex_code)
        h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
        
        colors = []
        start_angle = -angle * (count // 2) / 360
        for i in range(count):
            new_h = (h + start_angle + (i * angle / 360)) % 1.0
            cr, cg, cb = colorsys.hls_to_rgb(new_h, l, s)
            colors.append(self._rgb_to_hex(int(cr*255), int(cg*255), int(cb*255)))
        
        return colors
    
    def triadic(self, hex_code: str) -> List[str]:
        """Get triadic color scheme"""
        r, g, b = self._hex_to_rgb(hex_code)
        h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
        
        colors = [hex_code]
        for offset in [1/3, 2/3]:
            new_h = (h + offset) % 1.0
            cr, cg, cb = colorsys.hls_to_rgb(new_h, l, s)
            colors.append(self._rgb_to_hex(int(cr*255), int(cg*255), int(cb*255)))
        
        return colors
    
    def split_complementary(self, hex_code: str) -> List[str]:
        """Get split-complementary scheme"""
        r, g, b = self._hex_to_rgb(hex_code)
        h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
        
        colors = [hex_code]
        for offset in [15/360, -15/360]:
            new_h = (h + 0.5 + offset) % 1.0
            cr, cg, cb = colorsys.hls_to_rgb(new_h, l, s)
            colors.append(self._rgb_to_hex(int(cr*255), int(cg*255), int(cb*255)))
        
        return colors
    
    def monochromatic(self, hex_code: str, count: int = 5) -> List[str]:
        """Get monochromatic palette"""
        r, g, b = self._hex_to_rgb(hex_code)
        h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
        
        colors = []
        for i in range(count):
            new_l = 0.2 + (i * 0.6 / (count - 1)) if count > 1 else 0.5
            cr, cg, cb = colorsys.hls_to_rgb(h, new_l, s)
            colors.append(self._rgb_to_hex(int(cr*255), int(cg*255), int(cb*255)))
        
        return colors
    
    def contrast_ratio(self, color1: str, color2: str) -> float:
        """Calculate WCAG contrast ratio"""
        r1, g1, b1 = self._hex_to_rgb(color1)
        r2, g2, b2 = self._hex_to_rgb(color2)
        
        def luminance(r, g, b):
            rs, gs, bs = r/255, g/255, b/255
            rs = rs/12.92 if rs <= 0.03928 else ((rs+0.055)/1.055)**2.4
            gs = gs/12.92 if gs <= 0.03928 else ((gs+0.055)/1.055)**2.4
            bs = bs/12.92 if bs <= 0.03928 else ((bs+0.055)/1.055)**2.4
            return 0.2126*rs + 0.7152*gs + 0.0722*bs
        
        l1 = luminance(r1, g1, b1)
        l2 = luminance(r2, g2, b2)
        
        lighter = max(l1, l2)
        darker = min(l1, l2)
        
        return round((lighter + 0.05) / (darker + 0.05), 2)
    
    def suggest_palette(self, base_color: str, scheme: str = "complementary") -> Dict:
        """Suggest a complete palette based on a base color"""
        color = CrochetColor("base", base_color)
        
        schemes = {
            "complementary": self.complementary(base_color),
            "analogous": self.analogous(base_color),
            "triadic": self.triadic(base_color),
            "split_complementary": self.split_complementary(base_color),
            "monochromatic": self.monochromatic(base_color),
        }
        
        palette = schemes.get(scheme, self.complementary(base_color))
        
        return {
            "base_color": base_color,
            "scheme": scheme,
            "palette": palette,
            "is_warm": color.is_warm,
            "brightness": color.brightness,
            "saturation": color.saturation,
            "hsl": color.hsl,
            "contrast_notes": self._get_contrast_notes(palette),
        }
    
    def _get_contrast_notes(self, palette: List[str]) -> List[str]:
        """Get contrast notes for a palette"""
        notes = []
        if len(palette) >= 2:
            ratio = self.contrast_ratio(palette[0], palette[1])
            if ratio >= 7:
                notes.append(f"Excellent contrast ({ratio}:1) - great for text")
            elif ratio >= 4.5:
                notes.append(f"Good contrast ({ratio}:1) - meets WCAG AA")
            elif ratio >= 3:
                notes.append(f"Moderate contrast ({ratio}:1) - large text only")
            else:
                notes.append(f"Low contrast ({ratio}:1) - may be hard to see")
        return notes
    
    def _hex_to_rgb(self, hex_code: str) -> Tuple[int, int, int]:
        h = hex_code.lstrip('#')
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    
    def _rgb_to_hex(self, r: int, g: int, b: int) -> str:
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def generate_color_wheel_html(self) -> str:
        """Generate an interactive color wheel as HTML"""
        return '''<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Color Wheel</title>
<style>
body { font-family: -apple-system, sans-serif; background: #1a1a2e; color: #eee; padding: 20px; text-align: center; }
.wheel { width: 300px; height: 300px; border-radius: 50%; margin: 20px auto;
    background: conic-gradient(red, yellow, lime, aqua, blue, magenta, red);
    cursor: crosshair; position: relative; }
.selector { width: 20px; height: 20px; border: 3px solid white; border-radius: 50%;
    position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
    pointer-events: none; box-shadow: 0 0 10px rgba(0,0,0,0.5); }
.palette { display: flex; gap: 10px; justify-content: center; margin: 20px; flex-wrap: wrap; }
.swatch { width: 60px; height: 60px; border-radius: 8px; border: 2px solid #333;
    cursor: pointer; transition: transform 0.2s; }
.swatch:hover { transform: scale(1.1); }
.controls { margin: 20px; }
button { padding: 10px 20px; margin: 5px; border: none; border-radius: 6px;
    cursor: pointer; background: #4ECCA3; color: #1a1a2e; font-weight: bold; }
.info { margin: 10px; font-size: 0.9em; color: #888; }
</style></head>
<body>
<h1>🎨 Color Theory for Crochet</h1>
<div class="wheel" id="wheel" onclick="pickColor(event)">
    <div class="selector" id="selector"></div>
</div>
<div id="selectedColor" class="info">Click the wheel to pick a color</div>
<div class="palette" id="palette"></div>
<div class="controls">
    <button onclick="setScheme('complementary')">Complementary</button>
    <button onclick="setScheme('analogous')">Analogous</button>
    <button onclick="setScheme('triadic')">Triadic</button>
    <button onclick="setScheme('split')">Split Comp</button>
    <button onclick="setScheme('mono')">Monochromatic</button>
</div>
<div id="contrast" class="info"></div>
<script>
let baseColor = "#ff0000";
let scheme = "complementary";

function pickColor(e) {
    const rect = e.target.getBoundingClientRect();
    const x = e.clientX - rect.left - rect.width/2;
    const y = e.clientY - rect.top - rect.height/2;
    const angle = Math.atan2(y, x);
    const dist = Math.sqrt(x*x + y*y);
    
    if (dist > rect.width/2) return;
    
    const h = ((angle * 180/Math.PI) + 360) % 360;
    const s = Math.min(100, dist / (rect.width/2) * 100);
    const l = 50;
    
    const rgb = hslToRgb(h/360, s/100, l/100);
    baseColor = rgbToHex(rgb[0], rgb[1], rgb[2]);
    
    document.getElementById('selectedColor').innerHTML = 
        'Selected: <span style="color:' + baseColor + '">' + baseColor + '</span>';
    document.getElementById('selector').style.background = baseColor;
    
    updatePalette();
}

function setScheme(s) { scheme = s; updatePalette(); }

function updatePalette() {
    const colors = getSchemeColors(baseColor, scheme);
    const pal = document.getElementById('palette');
    pal.innerHTML = '';
    
    colors.forEach((c, i) => {
        const div = document.createElement('div');
        div.className = 'swatch';
        div.style.background = c;
        div.title = c;
        div.onclick = () => navigator.clipboard.writeText(c);
        pal.appendChild(div);
    });
    
    if (colors.length >= 2) {
        const ratio = getContrastRatio(colors[0], colors[1]);
        document.getElementById('contrast').innerHTML = 
            'Contrast Ratio: ' + ratio.toFixed(1) + ':1 ' + 
            (ratio >= 4.5 ? '✅ Good' : ratio >= 3 ? '⚠️ Moderate' : '❌ Low');
    }
}

function getSchemeColors(hex, scheme) {
    const r = parseInt(hex.slice(1,3),16)/255;
    const g = parseInt(hex.slice(3,5),16)/255;
    const b = parseInt(hex.slice(5,7),16)/255;
    let [h,l,s] = rgbToHsl(r,g,b);
    
    let colors = [hex];
    
    if (scheme === 'complementary') {
        const [cr,cg,cb] = hslToRgb((h+0.5)%1, l, s);
        colors.push(rgbToHex(cr*255,cg*255,cb*255));
    } else if (scheme === 'analogous') {
        for (let i = 1; i <= 4; i++) {
            const nh = (h + (i-2)*30/360 + 1) % 1;
            const [cr,cg,cb] = hslToRgb(nh, l, s);
            colors.push(rgbToHex(cr*255,cg*255,cb*255));
        }
    } else if (scheme === 'triadic') {
        for (let off of [1/3, 2/3]) {
            const [cr,cg,cb] = hslToRgb((h+off)%1, l, s);
            colors.push(rgbToHex(cr*255,cg*255,cb*255));
        }
    } else if (scheme === 'split') {
        for (let off of [15/360, -15/360]) {
            const [cr,cg,cb] = hslToRgb((h+0.5+off+1)%1, l, s);
            colors.push(rgbToHex(cr*255,cg*255,cb*255));
        }
    } else if (scheme === 'mono') {
        for (let i = 1; i < 5; i++) {
            const nl = 0.2 + i*0.15;
            const [cr,cg,cb] = hslToRgb(h, nl, s);
            colors.push(rgbToHex(cr*255,cg*255,cb*255));
        }
    }
    
    return colors;
}

function hslToRgb(h,s,l) {
    let r,g,b;
    if (s === 0) { r=g=b=l; }
    else {
        const hue2rgb = (p,q,t) => { if(t<0)t+=1;if(t>1)t-=1;if(t<1/6)return p+(q-p)*6*t;if(t<1/2)return q;if(t<2/3)return p+(q-p)*(2/3-t)*6;return p; };
        const q = l<0.5 ? l*(1+s) : l+s-l*s;
        const p = 2*l-q;
        r=hue2rgb(p,q,h+1/3); g=hue2rgb(p,q,h); b=hue2rgb(p,q,h-1/3);
    }
    return [Math.round(r*255),Math.round(g*255),Math.round(b*255)];
}

function rgbToHsl(r,g,b) {
    r/=255;g/=255;b/=255;
    const max=Math.max(r,g,b),min=Math.min(r,g,b);
    let h,s,l=(max+min)/2;
    if(max===min){h=s=0;}else{
        const d=max-min;s=l>0.5?d/(2-max-min):d/(max+min);
        switch(max){case r:h=((g-b)/d+(g<b?6:0))/6;break;case g:h=((b-r)/d+2)/6;break;case b:h=((r-g)/d+4)/6;break;}
    }
    return [h,s,l];
}

function rgbToHex(r,g,b) { return '#'+[r,g,b].map(x=>Math.round(x).toString(16).padStart(2,'0')).join(''); }

function getContrastRatio(c1,c2) {
    const lum = (hex) => { const [r,g,b] = [1,3,5].map(i=>{let v=parseInt(hex.slice(i,i+2),16)/255;return v<=0.03928?v/12.92:Math.pow((v+0.055)/1.055,2.4);}); return 0.2126*r+0.7152*g+0.0722*b; };
    const l1=lum(c1),l2=lum(c2);
    return (Math.max(l1,l2)+0.05)/(Math.min(l1,l2)+0.05);
}
</script>
</body></html>'''


# Demo
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  COLOR THEORY TOOL - DEMONSTRATION")
    print("=" * 60)
    
    ct = ColorTheory()
    
    base = "#E94560"
    
    print(f"\n🎨 Base Color: {base}")
    
    # Schemes
    print(f"\n  Complementary: {ct.complementary(base)}")
    print(f"  Analogous:     {ct.analogous(base)}")
    print(f"  Triadic:       {ct.triadic(base)}")
    print(f"  Split-Comp:    {ct.split_complementary(base)}")
    print(f"  Mono:          {ct.monochromatic(base)}")
    
    # Color info
    color = CrochetColor("test", base)
    print(f"\n  HSL: {color.hsl}")
    print(f"  Warm: {color.is_warm}")
    print(f"  Brightness: {color.brightness}")
    print(f"  Saturation: {color.saturation}")
    
    # Contrast
    print(f"\n  Contrast with white: {ct.contrast_ratio(base, '#FFFFFF')}:1")
    print(f"  Contrast with black: {ct.contrast_ratio(base, '#000000')}:1")
    
    # Seasonal palettes
    print(f"\n🌸 Seasonal Palettes:")
    for season, colors in ct.SEASONAL_PALETTES.items():
        swatches = " ".join(f"■{c[0]}" for c in colors[:3])
        print(f"  {season:8s}: {swatches}")
    
    # HTML wheel
    html = ct.generate_color_wheel_html()
    print(f"\n✅ Interactive color wheel: {len(html)} chars")
    
    print(f"\n  Color Theory Complete! 🎨")
