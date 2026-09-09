"""
Pattern Translator - Convert patterns between US, UK, and International terms
"""
from typing import Dict, List, Optional
import re


class PatternTranslator:
    """
    Translate crochet patterns between terminology systems
    
    Features:
    - US to UK conversion
    - UK to US conversion
    - Abbreviation expansion
    - Symbol chart generation
    - Multi-language support
    """
    
    US_TO_UK = {
        "sc": "dc",  # single crochet → double crochet
        "hdc": "htr",  # half double crochet → half treble
        "dc": "tr",  # double crochet → treble
        "tr": "dtr",  # treble → double treble
        "dtr": "trtr",  # double treble → triple treble
        "sl st": "ss",  # slip stitch → slip stitch
        "ch": "ch",  # chain → chain
        "sp": "sp",  # space → space
        "st": "st",  # stitch → stitch
        "sk": "miss",  # skip → miss
        "inc": "inc",  # increase → increase
        "dec": "dec",  # decrease → decrease
    }
    
    UK_TO_US = {v: k for k, v in US_TO_UK.items() if k != v}
    # Fix circular mappings
    UK_TO_US.update({
        "dc": "sc",
        "htr": "hdc",
        "tr": "dc",
        "dtr": "tr",
        "trtr": "dtr",
    })
    
    ABBREVIATION_EXPANSIONS = {
        "sc": "single crochet",
        "dc": "double crochet",
        "hdc": "half double crochet",
        "tr": "treble crochet",
        "dtr": "double treble",
        "sl st": "slip stitch",
        "ch": "chain",
        "sp": "space",
        "st": "stitch",
        "sts": "stitches",
        "sk": "skip",
        "inc": "increase",
        "dec": "decrease",
        "rep": "repeat",
        "rnd": "round",
        "rnds": "rounds",
        "beg": "beginning",
        "rem": "remaining",
        "yo": "yarn over",
        "yrh": "yarn round hook",
        "fp": "front post",
        "bp": "back post",
        "mc": "magic circle",
        "mr": "magic ring",
        "fo": "fasten off",
        "ch-sp": "chain space",
    }
    
    CROCHET_SYMBOLS = {
        "ch": "○",  # chain
        "sc": "x",  # single crochet
        "dc": "T",  # double crochet
        "hdc": "†",  # half double
        "tr": "T̃",  # treble
        "sl st": "•",  # slip stitch
        "inc": "/\\",  # increase
        "dec": "\\/",  # decrease
        "fpdc": "T⟩",  # front post
        "bpdc": "T⟨",  # back post
    }
    
    INTERNATIONAL_TERMS = {
        "en-us": "US Terms",
        "en-uk": "UK Terms",
        "de": "German (DE)",
        "fr": "French (FR)",
        "es": "Spanish (ES)",
        "nl": "Dutch (NL)",
        "it": "Italian (IT)",
        "jp": "Japanese (JP)",
    }
    
    def translate_to_uk(self, pattern: str) -> Dict:
        """Convert US pattern to UK terms"""
        translated = pattern
        changes = []
        
        # Replace each US term with UK equivalent
        for us_term, uk_term in self.US_TO_UK.items():
            if us_term != uk_term:
                # Use word boundaries to avoid partial matches
                pattern_new = re.sub(
                    rf'\b{re.escape(us_term)}\b',
                    uk_term,
                    translated,
                    flags=re.IGNORECASE
                )
                if pattern_new != translated:
                    changes.append(f"{us_term} → {uk_term}")
                translated = pattern_new
        
        return {
            "original": pattern,
            "translated": translated,
            "terminology": "UK",
            "changes": list(set(changes)),
            "change_count": len(set(changes)),
        }
    
    def translate_to_us(self, pattern: str) -> Dict:
        """Convert UK pattern to US terms"""
        translated = pattern
        changes = []
        
        for uk_term, us_term in self.UK_TO_US.items():
            if uk_term != us_term:
                pattern_new = re.sub(
                    rf'\b{re.escape(uk_term)}\b',
                    us_term,
                    translated,
                    flags=re.IGNORECASE
                )
                if pattern_new != translated:
                    changes.append(f"{uk_term} → {us_term}")
                translated = pattern_new
        
        return {
            "original": pattern,
            "translated": translated,
            "terminology": "US",
            "changes": list(set(changes)),
            "change_count": len(set(changes)),
        }
    
    def expand_abbreviations(self, pattern: str) -> Dict:
        """Expand abbreviations to full terms"""
        expanded = pattern
        expansions = []
        
        # Sort by length (longest first) to avoid partial matches
        sorted_abbrs = sorted(self.ABBREVIATION_EXPANSIONS.items(), 
                            key=lambda x: -len(x[0]))
        
        for abbr, full in sorted_abbrs:
            pattern_new = re.sub(
                rf'\b{re.escape(abbr)}\b',
                full,
                expanded,
                flags=re.IGNORECASE
            )
            if pattern_new != expanded:
                expansions.append(f"{abbr} → {full}")
            expanded = pattern_new
        
        return {
            "original": pattern,
            "expanded": expanded,
            "expansions": list(set(expansions)),
            "expansion_count": len(set(expansions)),
        }
    
    def generate_symbol_chart(self, pattern: str) -> Dict:
        """Convert pattern to symbol chart notation"""
        symbols = []
        
        for abbr in pattern.split():
            abbr_clean = abbr.lower().strip("(),.*")
            symbol = self.CROCHET_SYMBOLS.get(abbr_clean, abbr_clean)
            symbols.append(symbol)
        
        return {
            "original": pattern,
            "symbols": " ".join(symbols),
            "symbol_list": symbols,
            "legend": {v: k for k, v in self.CROCHET_SYMBOLS.items()},
        }
    
    def get_conversion_table(self) -> str:
        """Get US to UK conversion table"""
        table = "US to UK CONVERSION TABLE\n" + "=" * 40 + "\n\n"
        table += f"{'US Term':<20} {'UK Term':<20}\n"
        table += "-" * 40 + "\n"
        
        for us, uk in sorted(self.US_TO_UK.items()):
            marker = " (same)" if us == uk else ""
            table += f"{us:<20} {uk:<20}{marker}\n"
        
        return table
    
    def detect_terminology(self, pattern: str) -> Dict:
        """Detect whether pattern uses US or UK terms"""
        us_score = 0
        uk_score = 0
        
        # US-specific terms
        us_indicators = ["single crochet", "hdc", "sc in each"]
        uk_indicators = ["double crochet", "htr", "treble", "miss"]
        
        for indicator in us_indicators:
            us_score += pattern.lower().count(indicator)
        
        for indicator in uk_indicators:
            uk_score += pattern.lower().count(indicator)
        
        # Abbreviation detection
        if " sc " in pattern.lower() or "sc in" in pattern.lower():
            us_score += 2
        if " htr " in pattern.lower() or " dtr " in pattern.lower():
            uk_score += 2
        
        if us_score > uk_score:
            detected = "US"
            confidence = min(100, us_score * 20)
        elif uk_score > us_score:
            detected = "UK"
            confidence = min(100, uk_score * 20)
        else:
            detected = "Unknown"
            confidence = 0
        
        return {
            "detected": detected,
            "confidence": f"{confidence}%",
            "us_score": us_score,
            "uk_score": uk_score,
        }


# Demo
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  PATTERN TRANSLATOR - DEMONSTRATION")
    print("=" * 60)
    
    translator = PatternTranslator()
    
    # US pattern
    us_pattern = """
    Row 1: Ch 20. Sc in 2nd ch from hook and each ch across. (19 sc)
    Row 2: Ch 1, turn. Sc in each st across. (19 sc)
    Row 3: Ch 1, turn. Hdc in each st across. (19 hdc)
    Row 4: Ch 3, turn. Dc in each st across. (19 dc)
    Rep rows 2-4 until piece measures 12 inches.
    """
    
    print(f"\n🇺🇸 Original US Pattern:")
    print(us_pattern[:200] + "...")
    
    # Convert to UK
    print(f"\n🇬🇧 Converted to UK:")
    uk_result = translator.translate_to_uk(us_pattern)
    print(uk_result["translated"][:200] + "...")
    print(f"\n  Changes: {uk_result['change_count']}")
    for change in uk_result["changes"]:
        print(f"    {change}")
    
    # Convert back to US
    uk_pattern = "Ch 20. Dc in 2nd ch from hook and each ch across. (19 dc)"
    print(f"\n🇬🇧 UK Pattern: {uk_pattern}")
    us_result = translator.translate_to_us(uk_pattern)
    print(f"🇺🇸 Back to US: {us_result['translated']}")
    
    # Expand abbreviations
    print(f"\n📖 Expanding Abbreviations:")
    abbrev_pattern = "Ch 20, sc in each st, hdc in next 3 sts, dc in last st"
    expanded = translator.expand_abbreviations(abbrev_pattern)
    print(f"  Original: {abbrev_pattern}")
    print(f"  Expanded: {expanded['expanded']}")
    
    # Symbol chart
    print(f"\n📊 Symbol Chart:")
    symbols = translator.generate_symbol_chart("ch sc sc dc tr sl st")
    print(f"  Original: ch sc sc dc tr sl st")
    print(f"  Symbols: {symbols['symbols']}")
    
    # Detect terminology
    print(f"\n🔍 Detecting Terminology:")
    detection = translator.detect_terminology(us_pattern)
    print(f"  Detected: {detection['detected']} ({detection['confidence']} confidence)")
    
    # Conversion table
    print(f"\n📋 Conversion Table:")
    print(translator.get_conversion_table()[:300] + "...")
    
    print(f"\n  Pattern Translator Complete! 🌐")
"""Pattern Translator - Convert between US and UK crochet terms"""

US_TO_UK = {
    'single crochet': 'double crochet',
    'sc': 'dc',
    'double crochet': 'treble crochet',
    'dc': 'tr',
    'half double crochet': 'half treble crochet',
    'hdc': 'htr',
    'treble crochet': 'double treble crochet',
    'tr': 'dtr',
}

UK_TO_US = {v: k for k, v in US_TO_UK.items() if k != v}

def translate_pattern(pattern_text: str, from_term: str = 'US', to_term: str = 'UK') -> str:
    if from_term.upper() == to_term.upper():
        return pattern_text
    
    mapping = US_TO_UK if from_term.upper() == 'US' else UK_TO_US
    translated = pattern_text
    
    import re
    for term in sorted(mapping.keys(), key=len, reverse=True):
        replacement = mapping[term]
        if term != replacement:
            pattern = re.compile(re.escape(term), re.IGNORECASE)
            translated = pattern.sub(replacement, translated)
    
    return translated

def detect_term_system(pattern_text: str) -> str:
    text_lower = pattern_text.lower()
    us_score = sum(text_lower.count(ind) for ind in ['single crochet', ' sc ', 'sc '])
    uk_score = sum(text_lower.count(ind) for ind in ['treble crochet', ' tr ', 'tr '])
    
    if us_score > uk_score * 1.5:
        return 'US'
    elif uk_score > us_score * 1.5:
        return 'UK'
    return 'Unknown'
