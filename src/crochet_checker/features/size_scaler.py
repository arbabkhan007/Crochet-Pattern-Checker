"""Pattern Size Scaler"""

from dataclasses import dataclass
from typing import Tuple, Optional
import re

@dataclass
class SizeScale:
    original_size: str
    target_size: str
    scale_factor: float
    original_gauge: Tuple[float, float]
    target_gauge: Tuple[float, float]
    hook_size_change: Optional[str]

SIZE_MULTIPLIERS = {'tiny': 0.5, 'small': 0.75, 'medium': 1.0, 'large': 1.5, 'xlarge': 2.0}

def detect_pattern_size(pattern_text: str) -> str:
    text_lower = pattern_text.lower()
    if 'tiny' in text_lower or 'mini' in text_lower:
        return 'tiny'
    elif 'small' in text_lower:
        return 'small'
    elif 'large' in text_lower:
        return 'large'
    return 'medium'

def scale_pattern(pattern_text: str, target_size: str, original_size: Optional[str] = None) -> Tuple[str, SizeScale]:
    if original_size is None:
        original_size = detect_pattern_size(pattern_text)
    
    scale_factor = SIZE_MULTIPLIERS[target_size] / SIZE_MULTIPLIERS[original_size]
    
    def scale_count(match):
        count = int(match.group(1))
        scaled = round(count * scale_factor)
        if scaled % 2 != 0:
            scaled += 1 if scaled > count else -1
        return f"({max(1, scaled)})"
    
    scaled_text = re.sub(r'\((\d+)\)', scale_count, pattern_text)
    
    hook_change = "Use hook 0.5-1.0 mm larger" if scale_factor > 1.2 else "Use hook 0.5-1.0 mm smaller" if scale_factor < 0.8 else None
    
    return scaled_text, SizeScale(
        original_size=original_size,
        target_size=target_size,
        scale_factor=scale_factor,
        original_gauge=(5.6, 5.9),
        target_gauge=(5.6 / scale_factor, 5.9 / scale_factor),
        hook_size_change=hook_change
    )

def format_scale_info(info: SizeScale) -> str:
    return f"""📏 Pattern Scaling Information
{'=' * 40}
Original Size: {info.original_size}
Target Size: {info.target_size}
Scale Factor: {info.scale_factor:.2f}x
{'⚠️  Hook Adjustment: ' + info.hook_size_change if info.hook_size_change else '✅ No hook size change needed'}"""
