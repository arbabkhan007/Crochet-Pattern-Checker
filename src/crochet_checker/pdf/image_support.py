"""Image support for PDF generation."""
from pathlib import Path
from typing import List

def generate_pattern_images(pattern, output_dir: str) -> List[str]:
    """Generate all images for a pattern."""
    from ..visualization import StitchChartGenerator, PatternDiagramGenerator
    
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    images = []
    
    try:
        chart_gen = StitchChartGenerator()
        
        # Create simple pattern data
        items = pattern.rounds or pattern.rows
        pattern_data = []
        
        for item in items[:10]:  # Limit to first 10 rounds for chart
            round_num = item.round_number if hasattr(item, 'round_number') else item.row_number
            stitches = []
            
            for instruction in item.instructions:
                stitch_type = 'sc'
                count = 1
                
                if hasattr(instruction, 'stitch_type'):
                    stitch_type = instruction.stitch_type
                if hasattr(instruction, 'count'):
                    count = instruction.count
                
                for _ in range(count):
                    stitches.append({'type': stitch_type})
            
            pattern_data.append({
                'round': round_num,
                'stitches': stitches
            })
        
        chart_file = str(Path(output_dir) / 'stitch_chart.svg')
        chart_gen.generate_chart(pattern_data, chart_file)
        images.append(chart_file)
    except Exception as e:
        print(f"Warning: Could not generate stitch chart: {e}")
    
    return images
