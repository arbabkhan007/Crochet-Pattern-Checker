"""
Advanced Pattern Scaler - Scale complex patterns to any size
"""

class AdvancedPatternScaler:
    def __init__(self):
        self.scaling_factors = {
            'linear': {'method': 'multiply_stitches', 'complexity': 'simple'},
            'proportional': {'method': 'maintain_ratios', 'complexity': 'moderate'},
            'shaped': {'method': 'adjust_shaping', 'complexity': 'advanced'}
        }
    
    def scale_pattern(self, original_pattern: dict, target_size: dict, scaling_method: str = 'proportional') -> dict:
        """Scale complex pattern to new size"""
        scale_factor = target_size.get('width', 10) / original_pattern.get('width', 10)
        
        scaled_pattern = {
            'original_size': original_pattern,
            'target_size': target_size,
            'scale_factor': scale_factor,
            'scaling_method': scaling_method,
            'adjusted_stitches': self._calculate_adjusted_stitches(original_pattern, scale_factor, scaling_method),
            'adjusted_rows': self._calculate_adjusted_rows(original_pattern, scale_factor, scaling_method),
            'yarn_adjustment': self._calculate_yarn_adjustment(scale_factor),
            'hook_adjustment': self._recommend_hook_adjustment(scale_factor),
            'scaling_notes': self._get_scaling_notes(scaling_method)
        }
        
        return scaled_pattern
    
    def _calculate_adjusted_stitches(self, original: dict, factor: float, method: str) -> int:
        original_stitches = original.get('stitches', 100)
        
        if method == 'linear':
            return int(original_stitches * factor)
        elif method == 'proportional':
            # Maintain pattern repeats
            repeat_multiple = original.get('repeat_multiple', 1)
            scaled = int(original_stitches * factor)
            # Round to nearest multiple
            return (scaled // repeat_multiple) * repeat_multiple
        else:  # shaped
            return int(original_stitches * factor * 1.1)  # Account for shaping
    
    def _calculate_adjusted_rows(self, original: dict, factor: float, method: str) -> int:
        original_rows = original.get('rows', 50)
        return int(original_rows * factor)
    
    def _calculate_yarn_adjustment(self, scale_factor: float) -> dict:
        # Yarn increases with area (square of scale factor)
        yarn_factor = scale_factor ** 2
        return {
            'factor': yarn_factor,
            'percentage_increase': (yarn_factor - 1) * 100,
            'note': 'Yarn needs scale with area, not linear dimension'
        }
    
    def _recommend_hook_adjustment(self, scale_factor: float) -> str:
        if scale_factor > 1.5:
            return "Consider larger hook (1-2 sizes up) to maintain drape"
        elif scale_factor < 0.7:
            return "Consider smaller hook (1 size down) for tighter fabric"
        else:
            return "Same hook size should work"
    
    def _get_scaling_notes(self, method: str) -> list:
        notes = {
            'linear': ['Simple multiplication', 'May not maintain pattern integrity', 'Best for basic patterns'],
            'proportional': ['Maintains pattern repeats', 'Better for complex patterns', 'Calculates multiples automatically'],
            'shaped': ['Accounts for shaping changes', 'Most accurate for 3D items', 'Requires manual adjustments']
        }
        return notes.get(method, [])
    
    def generate_scaling_report(self, scaled: dict) -> str:
        """Generate detailed scaling report"""
        report = "📐 PATTERN SCALING REPORT\n" + "=" * 60 + "\n\n"
        report += f"Original: {scaled['original_size']['width']}\" x {scaled['original_size']['height']}\"\n"
        report += f"Target: {scaled['target_size']['width']}\" x {scaled['target_size']['height']}\"\n"
        report += f"Scale Factor: {scaled['scale_factor']:.2f}x\n\n"
        
        report += f"Adjusted Stitches: {scaled['adjusted_stitches']}\n"
        report += f"Adjusted Rows: {scaled['adjusted_rows']}\n\n"
        
        report += f"Yarn Adjustment: {scaled['yarn_adjustment']['percentage_increase']:.0f}% more yarn needed\n"
        report += f"Hook: {scaled['hook_adjustment']}\n\n"
        
        report += "Notes:\n"
        for note in scaled['scaling_notes']:
            report += f"  • {note}\n"
        
        return report

if __name__ == "__main__":
    print("📐 Advanced Pattern Scaler")
    print("=" * 60)
    
    scaler = AdvancedPatternScaler()
    
    # Test scaling a blanket pattern
    original = {
        'width': 40,
        'height': 50,
        'stitches': 200,
        'rows': 250,
        'repeat_multiple': 8
    }
    
    target = {'width': 60, 'height': 75}
    
    result = scaler.scale_pattern(original, target, 'proportional')
    
    print(scaler.generate_scaling_report(result))
