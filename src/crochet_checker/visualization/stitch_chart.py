"""Generate stitch charts for crochet patterns."""
from typing import List, Dict
import xml.etree.ElementTree as ET
from xml.dom import minidom

class StitchChartGenerator:
    """Generate visual stitch charts in SVG format."""
    
    STITCH_SYMBOLS = {
        'ch': {'symbol': 'o', 'color': '#999999'},
        'sc': {'symbol': '+', 'color': '#000000'},
        'dc': {'symbol': 'T', 'color': '#0000FF'},
        'hdc': {'symbol': 't', 'color': '#0080FF'},
        'tr': {'symbol': 'TT', 'color': '#0000FF'},
        'sl': {'symbol': '.', 'color': '#999999'},
        'inc': {'symbol': 'V', 'color': '#00AA00'},
        'dec': {'symbol': '^', 'color': '#FF0000'},
        'mr': {'symbol': 'O', 'color': '#FF00FF'},
    }
    
    def __init__(self, stitch_size: int = 20):
        self.stitch_size = stitch_size
    
    def generate_chart(self, pattern_data: List[Dict], output_file: str):
        """Generate a stitch chart from pattern data."""
        max_stitches = max(len(round_data.get('stitches', [])) for round_data in pattern_data)
        num_rounds = len(pattern_data)
        
        width = (max_stitches + 2) * self.stitch_size
        height = (num_rounds + 2) * self.stitch_size
        
        svg = ET.Element('svg', {
            'xmlns': 'http://www.w3.org/2000/svg',
            'width': str(width),
            'height': str(height),
            'viewBox': f'0 0 {width} {height}'
        })
        
        ET.SubElement(svg, 'rect', {
            'width': '100%',
            'height': '100%',
            'fill': '#FFFFFF'
        })
        
        title = ET.SubElement(svg, 'text', {
            'x': str(width // 2),
            'y': '20',
            'text-anchor': 'middle',
            'font-size': '16',
            'font-weight': 'bold'
        })
        title.text = 'Stitch Chart'
        
        for round_idx, round_data in enumerate(pattern_data):
            y = (round_idx + 2) * self.stitch_size
            
            label = ET.SubElement(svg, 'text', {
                'x': '10',
                'y': str(y + self.stitch_size // 2),
                'font-size': '12',
                'fill': '#666666'
            })
            label.text = f"R{round_data.get('round', round_idx + 1)}"
            
            stitches = round_data.get('stitches', [])
            for stitch_idx, stitch in enumerate(stitches):
                x = (stitch_idx + 2) * self.stitch_size
                stitch_type = stitch.get('type', 'sc')
                symbol_data = self.STITCH_SYMBOLS.get(stitch_type, {'symbol': '?', 'color': '#000000'})
                
                text = ET.SubElement(svg, 'text', {
                    'x': str(x),
                    'y': str(y + self.stitch_size // 2),
                    'text-anchor': 'middle',
                    'font-size': str(self.stitch_size // 2),
                    'fill': symbol_data['color']
                })
                text.text = symbol_data['symbol']
        
        xml_str = minidom.parseString(ET.tostring(svg)).toprettyxml(indent='  ')
        with open(output_file, 'w') as f:
            f.write(xml_str)
        
        return output_file
