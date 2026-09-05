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
