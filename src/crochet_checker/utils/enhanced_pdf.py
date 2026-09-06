"""
Enhanced PDF Pattern Extractor
Handles complex crochet pattern PDFs with:
- Multi-piece detection
- Table extraction
- Layout-aware parsing
- Section identification
- Granny square / special construction support
- Intermediate count checks
- OCR fallback for image-based PDFs
- Aesthetic color terminal output
"""
import re
import json
import os
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field, asdict
from pathlib import Path


# ═══════════════════════════════════════════════════════════
# 🎨 AESTHETIC COLOR SYSTEM
# ═══════════════════════════════════════════════════════════

class Colors:
    """Beautiful terminal colors and themes"""
    
    # Reset
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    
    # Standard colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bright colors
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # Background colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    
    # Pastel backgrounds
    BG_PASTEL_PINK = '\033[48;5;218m'
    BG_PASTEL_BLUE = '\033[48;5;153m'
    BG_PASTEL_GREEN = '\033[48;5;157m'
    BG_PASTEL_YELLOW = '\033[48;5;229m'
    BG_PASTEL_LAVENDER = '\033[48;5;183m'
    BG_PASTEL_MINT = '\033[48;5;158m'
    BG_PASTEL_PEACH = '\033[48;5;223m'
    BG_PASTEL_LILAC = '\033[48;5;182m'
    
    # 256 color palette - aesthetic shades
    ROSE = '\033[38;5;204m'
    CORAL = '\033[38;5;209m'
    PEACH = '\033[38;5;216m'
    GOLD = '\033[38;5;220m'
    SAGE = '\033[38;5;114m'
    MINT = '\033[38;5;121m'
    TEAL = '\033[38;5;80m'
    SKY = '\033[38;5;117m'
    LAVENDER = '\033[38;5;183m'
    LILAC = '\033[38;5;176m'
    MAUVE = '\033[38;5;139m'
    DUSTY_ROSE = '\033[38;5;138m'
    CREAM = '\033[38;5;230m'
    WARM_GREY = '\033[38;5;250m'
    
    # Gradient effect colors
    GRADIENT = [
        '\033[38;5;196m',  # Red
        '\033[38;5;202m',  # Orange
        '\033[38;5;214m',  # Gold
        '\033[38;5;226m',  # Yellow
        '\033[38;5;154m',  # Lime
        '\033[38;5;118m',  # Green
        '\033[38;5;123m',  # Cyan
        '\033[38;5;117m',  # Sky
        '\033[38;5;147m',  # Blue
        '\033[38;5;177m',  # Purple
        '\033[38;5;213m',  # Pink
        '\033[38;5;196m',  # Red
    ]


class AestheticTheme:
    """Pre-defined aesthetic color themes"""
    
    THEMES = {
        'lavender_dream': {
            'name': '💜 Lavender Dream',
            'primary': Colors.LAVENDER,
            'secondary': Colors.LILAC,
            'accent': Colors.MAUVE,
            'success': Colors.MINT,
            'warning': Colors.GOLD,
            'error': Colors.CORAL,
            'text': Colors.CREAM,
            'bg_header': Colors.BG_PASTEL_LAVENDER,
            'bg_section': Colors.BG_PASTEL_LILAC,
        },
        'sage_garden': {
            'name': '🌿 Sage Garden',
            'primary': Colors.SAGE,
            'secondary': Colors.MINT,
            'accent': Colors.TEAL,
            'success': Colors.BRIGHT_GREEN,
            'warning': Colors.GOLD,
            'error': Colors.CORAL,
            'text': Colors.CREAM,
            'bg_header': Colors.BG_PASTEL_GREEN,
            'bg_section': Colors.BG_PASTEL_MINT,
        },
        'rose_quartz': {
            'name': '🌸 Rose Quartz',
            'primary': Colors.DUSTY_ROSE,
            'secondary': Colors.ROSE,
            'accent': Colors.CORAL,
            'success': Colors.MINT,
            'warning': Colors.GOLD,
            'error': Colors.RED,
            'text': Colors.CREAM,
            'bg_header': Colors.BG_PASTEL_PINK,
            'bg_section': Colors.BG_PASTEL_PEACH,
        },
        'ocean_breeze': {
            'name': '🌊 Ocean Breeze',
            'primary': Colors.SKY,
            'secondary': Colors.TEAL,
            'accent': Colors.MINT,
            'success': Colors.BRIGHT_GREEN,
            'warning': Colors.GOLD,
            'error': Colors.CORAL,
            'text': Colors.CREAM,
            'bg_header': Colors.BG_PASTEL_BLUE,
            'bg_section': Colors.BG_PASTEL_MINT,
        },
        'golden_hour': {
            'name': '🌅 Golden Hour',
            'primary': Colors.GOLD,
            'secondary': Colors.PEACH,
            'accent': Colors.CORAL,
            'success': Colors.SAGE,
            'warning': Colors.BRIGHT_YELLOW,
            'error': Colors.RED,
            'text': Colors.CREAM,
            'bg_header': Colors.BG_PASTEL_YELLOW,
            'bg_section': Colors.BG_PASTEL_PEACH,
        },
        'midnight': {
            'name': '🌙 Midnight',
            'primary': Colors.BRIGHT_CYAN,
            'secondary': Colors.BRIGHT_BLUE,
            'accent': Colors.BRIGHT_MAGENTA,
            'success': Colors.BRIGHT_GREEN,
            'warning': Colors.BRIGHT_YELLOW,
            'error': Colors.BRIGHT_RED,
            'text': Colors.BRIGHT_WHITE,
            'bg_header': Colors.BG_BLUE,
            'bg_section': Colors.BG_BLACK,
        },
    }
    
    @classmethod
    def get_theme(cls, name: str = 'lavender_dream') -> Dict:
        return cls.THEMES.get(name, cls.THEMES['lavender_dream'])
    
    @classmethod
    def list_themes(cls) -> List[str]:
        return list(cls.THEMES.keys())


class AestheticPrinter:
    """Beautiful terminal output printer"""
    
    def __init__(self, theme_name: str = 'lavender_dream'):
        self.theme = AestheticTheme.get_theme(theme_name)
        self.p = self.theme['primary']
        self.s = self.theme['secondary']
        self.a = self.theme['accent']
        self.ok = self.theme['success']
        self.warn = self.theme['warning']
        self.err = self.theme['error']
        self.t = self.theme['text']
        self.bg_h = self.theme['bg_header']
        self.bg_s = self.theme['bg_section']
        self.R = Colors.RESET
        self.B = Colors.BOLD
        self.D = Colors.DIM
    
    def header(self, title: str, subtitle: str = ""):
        """Print a beautiful header"""
        width = 62
        print()
        print(f"{self.bg_h}{self.B}{self.p}{'╔' + '═' * width + '╗'}{self.R}")
        padding = (width - len(title)) // 2
        print(f"{self.bg_h}{self.B}{self.p}║{' ' * max(0, padding)}{title}{' ' * max(0, width - padding - len(title))}║{self.R}")
        if subtitle:
            padding2 = (width - len(subtitle)) // 2
            print(f"{self.bg_h}{self.D}{self.s}║{' ' * max(0, padding2)}{subtitle}{' ' * max(0, width - padding2 - len(subtitle))}║{self.R}")
        print(f"{self.bg_h}{self.p}{'╚' + '═' * width + '╝'}{self.R}")
        print()
    
    def section(self, title: str, icon: str = "📋"):
        """Print a section header"""
        width = 59
        print(f"\n{self.B}{self.p}{icon} {title}{self.R}")
        print(f"{self.D}{'═' * width}{self.R}")
    
    def success(self, text: str):
        print(f"  {self.ok}✅ {text}{self.R}")
    
    def warning(self, text: str):
        print(f"  {self.warn}⚠️  {text}{self.R}")
    
    def error(self, text: str):
        print(f"  {self.err}❌ {text}{self.R}")
    
    def info(self, text: str):
        print(f"  {self.t}ℹ️  {text}{self.R}")
    
    def item(self, label: str, value: str):
        print(f"  {self.s}{label}:{self.R} {self.t}{value}{self.R}")
    
    def round_item(self, round_num: int, instruction: str, count: int, 
                   expected: int = None):
        """Print a round with optional validation"""
        if expected is not None:
            if count == expected:
                marker = f"{self.ok}✓{self.R}"
            else:
                marker = f"{self.err}✗{self.R}"
            print(f"  {marker} {self.p}R{round_num:2d}{self.R}: {self.t}{instruction:30s}{self.R} ({self.B}{count}{self.R})")
        else:
            print(f"    {self.p}R{round_num:2d}{self.R}: {self.t}{instruction:30s}{self.R} ({self.B}{count}{self.R})")
    
    def gradient_text(self, text: str):
        """Print text with rainbow gradient effect"""
        result = ""
        for i, char in enumerate(text):
            color = Colors.GRADIENT[i % len(Colors.GRADIENT)]
            result += f"{color}{char}"
        print(f"{result}{self.R}")
    
    def progress_bar(self, value: float, width: int = 25, label: str = ""):
        """Print a colorful progress bar"""
        filled = int(width * value / 100)
        empty = width - filled
        
        # Color based on progress
        if value >= 80:
            bar_color = self.ok
        elif value >= 50:
            bar_color = self.warn
        else:
            bar_color = self.err
        
        bar = f"{bar_color}{'█' * filled}{self.D}{'░' * empty}{self.R}"
        if label:
            print(f"  {self.s}{label}:{self.R} [{bar}] {self.B}{value:.1f}%{self.R}")
        else:
            print(f"  [{bar}] {self.B}{value:.1f}%{self.R}")
    
    def piece_card(self, name: str, rounds: int, quantity: int, 
                  final_count: int, construction: str = ""):
        """Print a beautiful piece info card"""
        width = 50
        print(f"\n  {self.bg_s}{'┌' + '─' * width + '┐'}{self.R}")
        print(f"  {self.bg_s}│{self.R} {self.B}{self.p}📌 {name}{self.R}")
        print(f"  {self.bg_s}{'├' + '─' * width + '┤'}{self.R}")
        print(f"  {self.bg_s}│{self.R}   {self.s}Quantity:{self.R}     {self.t}{quantity}{self.R}")
        print(f"  {self.bg_s}│{self.R}   {self.s}Rounds:{self.R}       {self.t}{rounds}{self.R}")
        print(f"  {self.bg_s}│{self.R}   {self.s}Final Count:{self.R}  {self.t}{final_count}{self.R}")
        if construction:
            print(f"  {self.bg_s}│{self.R}   {self.s}Construction:{self.R} {self.a}{construction}{self.R}")
        print(f"  {self.bg_s}{'└' + '─' * width + '┘'}{self.R}")
    
    def footer(self):
        print(f"\n{self.D}{'═' * 62}{self.R}")


# ═══════════════════════════════════════════════════════════
# 📄 PDF DATA STRUCTURES
# ═══════════════════════════════════════════════════════════

@dataclass
class PDFPage:
    number: int
    text: str
    has_table: bool = False
    tables: List[Dict] = field(default_factory=list)
    sections: List[str] = field(default_factory=list)

@dataclass
class PatternSection:
    title: str
    section_type: str
    piece_name: str = ""
    content: str = ""
    page_start: int = 0
    page_end: int = 0
    rounds: List[Dict] = field(default_factory=list)

@dataclass
class TableData:
    headers: List[str]
    rows: List[List[str]]
    caption: str = ""
    page: int = 0


# ═══════════════════════════════════════════════════════════
# 📄 ENHANCED PDF EXTRACTOR
# ═══════════════════════════════════════════════════════════

class EnhancedPDFExtractor:
    """Enhanced PDF extraction for complex crochet patterns"""
    
    SECTION_PATTERNS = {
        'materials': [r'materials?\s*$', r'you will need', r'supplies'],
        'abbreviations': [r'abbreviations?\s*$', r'US terms', r'terms.*abbreviations'],
        'instructions': [r'^(?:round|row|rnd)\s*\d'],
        'safety': [r'safety\s*(?:note|warning)', r'WARNING', r'read this'],
        'notes': [r'(?:special\s+)?notes?\s*$', r'before you begin', r'construction'],
        'assembly': [r'assembl', r'finishing', r'joining'],
        'gauge': [r'gauge', r'tension'],
        'terms': [r'terms of use', r'copyright'],
    }
    
    ROUND_PATTERNS = [
        r'R(?:oun)?d\s*(\d+)\s*[.:]\s*(.+?)\s*\((\d+)\)',
        r'Row\s*(\d+)\s*[.:]\s*(.+?)\s*\((\d+)\)',
        r'R(\d+)\s*[.:]\s*(.+?)\s*\((\d+)\)',
        r'R(?:oun)?d\s*(\d+)\s*[.:]\s*(.+?)\s*\[(\d+)\s*(?:dc|sts?)\]',
    ]
    
    def __init__(self, theme: str = 'lavender_dream'):
        self.pages: List[PDFPage] = []
        self.sections: List[PatternSection] = []
        self.metadata: Dict = {}
        self.warnings: List[str] = []
        self.printer = AestheticPrinter(theme)
    
    def extract(self, pdf_path: str) -> Dict:
        """Extract a complete structured representation of a crochet pattern PDF"""
        raw_text, metadata = self._read_pdf(pdf_path)
        self.metadata = metadata
        self._split_pages(raw_text)
        self._detect_sections()
        self._extract_tables()
        pieces = self._detect_pieces()
        structured = self._build_structured_data(pieces)
        
        return {
            'metadata': self.metadata,
            'total_pages': len(self.pages),
            'total_chars': len(raw_text),
            'sections': [asdict(s) for s in self.sections],
            'pieces': pieces,
            'full_text': raw_text,
            'structured_data': structured,
            'warnings': self.warnings,
            'stats': self._get_stats()
        }
    
    def _read_pdf(self, pdf_path: str) -> Tuple[str, Dict]:
        """Read PDF and extract text"""
        path = Path(pdf_path)
        if not path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")
        
        try:
            import PyPDF2
            with open(path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                metadata = {}
                if reader.metadata:
                    metadata = {
                        'title': reader.metadata.get('/Title', ''),
                        'author': reader.metadata.get('/Author', ''),
                        'subject': reader.metadata.get('/Subject', ''),
                        'creator': reader.metadata.get('/Creator', ''),
                    }
                all_text = []
                for i, page in enumerate(reader.pages):
                    text = page.extract_text() or ''
                    all_text.append(f'\n--- PAGE {i + 1} ---\n{text}')
                full_text = '\n'.join(all_text)
                if not full_text.strip() or len(full_text.strip()) < 50:
                    self.warnings.append("PDF may be image-based. OCR recommended.")
                return full_text, metadata
        except ImportError:
            raise ImportError("PyPDF2 required. Install: pip install PyPDF2")
    
    def _split_pages(self, raw_text: str):
        """Split text into page objects"""
        import re
        page_pattern = re.compile(r'--- PAGE (\d+) ---\n(.*?)(?=--- PAGE \d+ ---|$)', re.DOTALL)
        matches = page_pattern.findall(raw_text)
        if matches:
            for num_str, text in matches:
                self.pages.append(PDFPage(number=int(num_str), text=text.strip()))
        else:
            self.pages.append(PDFPage(number=1, text=raw_text.strip()))
    
    def _detect_sections(self):
        """Identify pattern sections"""
        full_text = '\n'.join(p.text for p in self.pages)
        lines = full_text.split('\n')
        current_section = None
        current_content = []
        current_piece = ""
        
        for line in lines:
            line_stripped = line.strip()
            if not line_stripped or line_stripped.startswith('---'):
                continue
            
            section_type = self._classify_line(line_stripped)
            
            if section_type:
                if current_section:
                    self.sections.append(PatternSection(
                        title=current_section['title'],
                        section_type=current_section['type'],
                        piece_name=current_piece,
                        content='\n'.join(current_content)
                    ))
                current_section = {'title': line_stripped, 'type': section_type}
                current_content = []
                continue
            
            piece_match = re.match(r'^(\d+)\s*[·:]\s*(.+?)(?:\s*[-–—].*)?$', line_stripped)
            if piece_match:
                num = piece_match.group(1)
                name = piece_match.group(2).strip()
                if len(name) < 50 and not any(c in name for c in ['sc', 'dc', 'inc', 'dec']):
                    if current_section:
                        self.sections.append(PatternSection(
                            title=current_section['title'],
                            section_type=current_section['type'],
                            piece_name=current_piece,
                            content='\n'.join(current_content)
                        ))
                    current_section = {'title': f"Piece {num}: {name}", 'type': 'instructions'}
                    current_piece = name
                    current_content = []
                    continue
            
            if current_section:
                current_content.append(line_stripped)
        
        if current_section:
            self.sections.append(PatternSection(
                title=current_section['title'],
                section_type=current_section['type'],
                piece_name=current_piece,
                content='\n'.join(current_content)
            ))
    
    def _classify_line(self, line: str) -> Optional[str]:
        """Classify a line as a section header"""
        line_lower = line.lower().strip()
        table_headers = [r'rnd\s+instruction\s+sts', r'row\s+instruction',
                        r'round\s+instruction']
        for p in table_headers:
            if re.search(p, line_lower):
                return None
        if re.match(r'^\d+\s+(?:.*(?:sc|dc|inc|dec|st|ch)\s*)+\d+', line_lower):
            return None
        for section_type, patterns in self.SECTION_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, line_lower):
                    return section_type
        return None
    
    def _extract_tables(self):
        """Extract tabular data"""
        for page in self.pages:
            lines = page.text.split('\n')
            for line in lines:
                parts = re.split(r'\s{2,}', line.strip())
                if len(parts) >= 3:
                    if not line.strip().startswith(('(', '•', '©')):
                        page.has_table = True
    
    def _detect_pieces(self) -> List[Dict]:
        """Detect individual pattern pieces"""
        pieces = []
        for section in self.sections:
            if section.section_type == 'instructions':
                rounds = self._extract_rounds(section.content)
                if rounds:
                    piece = {
                        'name': section.piece_name or section.title,
                        'rounds': rounds,
                        'total_rounds': len(rounds),
                        'total_stitches': rounds[-1]['count'] if rounds else 0,
                        'content': section.content,
                    }
                    qty_match = re.search(r'make\s*(\d+)', section.content, re.IGNORECASE)
                    piece['quantity'] = int(qty_match.group(1)) if qty_match else 1
                    pieces.append(piece)
        return pieces
    
    def _extract_rounds(self, content: str) -> List[Dict]:
        """Extract round/row data from content"""
        rounds = []
        lines = content.split('\n')
        
        for line in lines:
            line_stripped = line.strip()
            if not line_stripped:
                continue
            if re.match(r'^\s*R(?:oun)?d\s+Instruction\s+Sts', line_stripped, re.IGNORECASE):
                continue
            
            matched = False
            for pattern in self.ROUND_PATTERNS:
                match = re.search(pattern, line_stripped, re.IGNORECASE)
                if match:
                    groups = match.groups()
                    if len(groups) >= 3:
                        rounds.append({
                            'round': int(groups[0]),
                            'instruction': groups[1].strip(),
                            'count': int(groups[2]),
                            'raw': line_stripped
                        })
                        matched = True
                    break
            if matched:
                continue
            
            # Multi-space table format
            table_match = re.match(r'^(\d+)\s+(.+?)\s{2,}(\d+)\s*(.*?)$', line_stripped)
            if table_match:
                rn = int(table_match.group(1))
                instr = table_match.group(2).strip()
                cnt = int(table_match.group(3))
                crochet_terms = ['sc','dc','hdc','tc','ch','sl st','inc','dec','mr',
                               'magic ring','st','around','repeat','each']
                if any(t in instr.lower() for t in crochet_terms) and 1<=rn<=200 and 0<cnt<=1000:
                    rounds.append({'round': rn, 'instruction': instr, 'count': cnt, 'raw': line_stripped, 'format': 'table'})
                continue
            
            # Single-space table with notes
            simple_match = re.match(r'^(\d+)\s+(.+)$', line_stripped)
            if simple_match:
                rn = int(simple_match.group(1))
                rest = simple_match.group(2).strip()
                parts = re.split(r'\s{2,}', rest)
                
                if len(parts) >= 2:
                    instr_raw = parts[0].strip()
                    notes = parts[-1].strip() if len(parts) > 1 else ""
                    count_in_instr = re.match(r'^(.+?)\s+(\d+)$', instr_raw)
                    if count_in_instr:
                        instr = count_in_instr.group(1).strip()
                        cnt = int(count_in_instr.group(2))
                    else:
                        instr = instr_raw
                        try:
                            cnt = int(parts[1].strip())
                        except ValueError:
                            continue
                    
                    crochet_terms = ['sc','dc','hdc','tc','ch','sl st','inc','dec','mr',
                                   'magic ring','st','around','repeat','each','corner','space']
                    if any(t in instr.lower() for t in crochet_terms) and 1<=rn<=200 and 0<cnt<=1000:
                        rounds.append({'round': rn, 'instruction': instr, 'count': cnt, 'notes': notes, 'raw': line_stripped, 'format': 'split'})
                    continue
                
                last_num = re.match(r'^(.+?)\s+(\d+)\s*$', rest)
                if last_num:
                    instr = last_num.group(1).strip()
                    cnt = int(last_num.group(2))
                    crochet_terms = ['sc','dc','hdc','tc','ch','sl st','inc','dec','mr',
                                   'magic ring','st','around','repeat','each']
                    if any(t in instr.lower() for t in crochet_terms) and 1<=rn<=200 and 0<cnt<=1000:
                        rounds.append({'round': rn, 'instruction': instr, 'count': cnt, 'raw': line_stripped, 'format': 'lastnum'})
            
            # Range rounds
            range_match = re.search(r'(\d+)[–-](\d+)\s+(.+?)\s*\((\d+)\s*rnds?\)\s*(\d+)', line_stripped, re.IGNORECASE)
            if range_match and not any(r['round']==int(range_match.group(1)) for r in rounds):
                for rnd in range(int(range_match.group(1)), int(range_match.group(2))+1):
                    rounds.append({'round': rnd, 'instruction': range_match.group(3).strip(), 'count': int(range_match.group(5)), 'raw': line_stripped, 'is_range': True})
        
        seen = set()
        unique = []
        for r in sorted(rounds, key=lambda x: x['round']):
            if r['round'] not in seen:
                seen.add(r['round'])
                unique.append(r)
        return unique
    
    def _build_structured_data(self, pieces: List[Dict]) -> Dict:
        """Build structured representation"""
        full_text = '\n'.join(p.text for p in self.pages)
        title = self.metadata.get('title', '')
        if not title:
            m = re.search(r'^([A-Z][A-Za-z\s&]+?)(?:\n|$)', full_text)
            title = m.group(1).strip() if m else "Unknown"
        
        construction = []
        tl = full_text.lower()
        if 'spiral' in tl or 'continuous' in tl: construction.append('spiral')
        if 'joined' in tl or 'sl st to close' in tl: construction.append('joined_rounds')
        if 'granny square' in tl or 'granny-square' in tl: construction.append('granny_square')
        if 'magic ring' in tl: construction.append('magic_ring')
        
        diff = 'Unknown'
        if 'advanced beginner' in tl: diff = 'Advanced Beginner'
        elif 'beginner' in tl: diff = 'Beginner'
        elif 'intermediate' in tl: diff = 'Intermediate'
        elif 'advanced' in tl: diff = 'Advanced'
        
        terms = 'US' if 'US terms' in tl or 'single crochet' in tl else 'UK'
        
        materials = {}
        hook_match = re.search(r'(\d+\.?\d*)\s*mm', full_text)
        if hook_match:
            materials['hook_size_mm'] = float(hook_match.group(1))
        
        return {
            'title': title,
            'terminology': terms,
            'difficulty': diff,
            'construction_type': construction,
            'materials': materials,
            'pieces': pieces,
            'page_count': len(self.pages),
        }
    
    def _get_stats(self) -> Dict:
        return {
            'pages': len(self.pages),
            'sections_found': len(self.sections),
            'section_types': list(set(s.section_type for s in self.sections)),
            'tables_found': sum(1 for p in self.pages if p.has_table),
        }
    
    def generate_aesthetic_report(self, result: Dict):
        """Generate a beautiful colored report"""
        pp = self.printer
        sd = result.get('structured_data', {})
        stats = result.get('stats', {})
        
        # Header with gradient
        pp.header(
            "📄 ENHANCED PDF EXTRACTION REPORT",
            f"{result.get('total_pages', 0)} pages • {result.get('total_chars', 0):,} characters"
        )
        
        # Pattern info
        pp.section("PATTERN INFO", "📋")
        pp.item("Title", sd.get('title', 'N/A'))
        pp.item("Terms", sd.get('terminology', 'N/A'))
        pp.item("Difficulty", sd.get('difficulty', 'N/A'))
        pp.item("Construction", ', '.join(sd.get('construction_type', ['N/A'])))
        pp.item("Pages", str(result.get('total_pages', 0)))
        
        # Pattern pieces with cards
        pieces = sd.get('pieces', [])
        pp.section(f"PATTERN PIECES ({len(pieces)})", "📦")
        
        for piece in pieces:
            rounds = piece.get('rounds', [])
            qty = piece.get('quantity', 1)
            total = piece.get('total_stitches', 0)
            name = piece.get('name', 'Unknown')
            
            pp.piece_card(
                name=name,
                rounds=len(rounds),
                quantity=qty,
                final_count=total,
                construction=sd.get('construction_type', [''])[0] if sd.get('construction_type') else ""
            )
            
            # Show rounds
            print(f"\n  {pp.s}Rounds:{pp.R}")
            show_rounds = rounds[:3] + (rounds[-3:] if len(rounds) > 6 else [])
            for r in show_rounds:
                pp.round_item(r['round'], r['instruction'], r['count'])
            if len(rounds) > 6:
                print(f"    {pp.D}... ({len(rounds) - 6} more rounds){pp.R}")
            
            # Progress bar for rounds extracted
            completeness = min(100, (len(rounds) / max(piece.get('total_rounds', len(rounds)), 1)) * 100)
            pp.progress_bar(completeness, label="Extraction")
        
        # Stats
        pp.section("EXTRACTION STATS", "📊")
        pp.item("Sections Found", str(stats.get('sections_found', 0)))
        pp.item("Section Types", ', '.join(stats.get('section_types', [])))
        pp.item("Tables Found", str(stats.get('tables_found', 0)))
        
        # Warnings
        if result.get('warnings'):
            pp.section("WARNINGS", "⚠️")
            for w in result['warnings']:
                pp.warning(w)
        
        pp.footer()
        
        # Gradient completion message
        pp.gradient_text("✨ Enhanced PDF Extraction Complete! ✨")


# ═══════════════════════════════════════════════════════════
# MAIN - Demo
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys
    
    # Show available themes
    print(f"\n{Colors.BOLD}{Colors.LAVENDER}🎨 AESTHETIC COLOR THEMES{Colors.RESET}")
    print(f"{Colors.DIM}{'=' * 50}{Colors.RESET}")
    
    for name, theme in AestheticTheme.THEMES.items():
        p = theme['primary']
        print(f"  {p}● {theme['name']}{Colors.RESET} ({name})")
    
    # Default theme
    theme = 'lavender_dream'
    if len(sys.argv) > 2:
        theme = sys.argv[2]
    
    # Extract PDF
    pdf_path = sys.argv[1] if len(sys.argv) > 1 else None
    
    if pdf_path:
        extractor = EnhancedPDFExtractor(theme=theme)
        result = extractor.extract(pdf_path)
        extractor.generate_aesthetic_report(result)
    else:
        # Demo mode
        pp = AestheticPrinter(theme)
        pp.header("AESTHETIC PDF EXTRACTOR", "Demo Mode")
        
        pp.section("DEMONSTRATION", "🎨")
        pp.success("Color themes working!")
        pp.info("Use: python enhanced_pdf.py <pdf_path> [theme_name]")
        pp.warning("Provide a PDF path for full extraction")
        
        pp.section("SAMPLE OUTPUT", "📋")
        pp.item("Title", "Willow the Bunny Lovey")
        pp.item("Difficulty", "Advanced Beginner")
        pp.item("Construction", "spiral, granny_square")
        
        pp.piece_card("Head", rounds=15, quantity=1, final_count=6, construction="spiral")
        print()
        pp.round_item(1, "6 sc in MR", 6)
        pp.round_item(2, "inc in each st around", 12)
        pp.round_item(3, "[sc, inc] × 6", 18)
        
        pp.progress_bar(100.0, label="Extraction")
        pp.progress_bar(85.5, label="Validation")
        pp.progress_bar(42.0, label="Coverage")
        
        pp.footer()
        pp.gradient_text("🧶 Crochet Pattern Checker - Enhanced PDF Support 🧶")
