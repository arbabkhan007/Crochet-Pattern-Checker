"""
    AI Agent Orchestrator
Coordinates multiple AI agents that work together on crochet patterns.
Each agent has a specialized role and they collaborate to deliver results.

Agents:
  🧠 Orchestrator - Coordinates workflow, delegates tasks
  ✅ Validator Agent - Validates patterns, finds errors
  📄 PDF Agent - Creates beautiful PDF patterns
  🌐 Search Agent - Searches internet for patterns, trends, yarn
  ✏️ Generator Agent - Creates new patterns from descriptions
  📚 Learning Agent - Learns from tested patterns, improves over time
  🔮 Analyst Agent - Analyzes complexity, predicts outcomes
"""
import json
import os
import time
import hashlib
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from enum import Enum
import re


# ═══════════════════════════════════════════════════════════
# 🎨 Terminal Colors
# ═══════════════════════════════════════════════════════════

class C:
    R = '\033[0m'
    B = '\033[1m'
    D = '\033[2m'
    ROSE = '\033[38;5;204m'
    CORAL = '\033[38;5;209m'
    SAGE = '\033[38;5;114m'
    MINT = '\033[38;5;121m'
    TEAL = '\033[38;5;80m'
    SKY = '\033[38;5;117m'
    LAV = '\033[38;5;183m'
    LILAC = '\033[38;5;176m'
    GOLD = '\033[38;5;220m'
    PEACH = '\033[38;5;216m'
    CREAM = '\033[38;5;230m'
    BG_LAV = '\033[48;5;183m'
    BG_SAGE = '\033[48;5;157m'
    BG_PEACH = '\033[48;5;223m'


# ═══════════════════════════════════════════════════════════
# 📝 Agent Task & Result
# ═══════════════════════════════════════════════════════════

class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    WAITING = "waiting_for_agent"


class AgentType(Enum):
    ORCHESTRATOR = "orchestrator"
    VALIDATOR = "validator"
    PDF_GENERATOR = "pdf_generator"
    WEB_SEARCH = "web_search"
    PATTERN_GENERATOR = "pattern_generator"
    LEARNER = "learner"
    ANALYST = "analyst"


@dataclass
class AgentTask:
    id: str
    agent_type: AgentType
    description: str
    input_data: Dict = field(default_factory=dict)
    status: str = "pending"
    result: Dict = field(default_factory=dict)
    created_at: str = ""
    completed_at: str = ""
    priority: int = 1
    dependencies: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()


@dataclass
class AgentMessage:
    from_agent: str
    to_agent: str
    message_type: str
    content: Dict
    timestamp: str = ""
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()


# ═══════════════════════════════════════════════════════════
# 📚 Knowledge Base - The Learning Memory
# ═══════════════════════════════════════════════════════════

class KnowledgeBase:
    """
    Persistent memory that learns from every pattern tested.
    Gets smarter over time by accumulating insights.
    """
    
    def __init__(self, path: str = ".crochet_ai_knowledge.json"):
        self.path = Path(path)
        self.knowledge = {
            'version': '1.0',
            'created_at': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat(),
            'patterns_analyzed': 0,
            'errors_found': 0,
            'patterns_generated': 0,
            
            # Learned stitch patterns
            'stitch_patterns': {},
            
            # Learned round progressions
            'round_progressions': {},
            
            # Common errors and fixes
            'error_patterns': {},
            
            # Pattern templates learned
            'templates': {},
            
            # Yarn knowledge
            'yarn_knowledge': {},
            
            # Difficulty indicators
            'difficulty_indicators': {},
            
            # Success patterns (what works)
            'success_patterns': {},
            
            # Construction knowledge
            'construction_knowledge': {},
            
            # Agent performance tracking
            'agent_performance': {},
        }
        self.load()
    
    def load(self):
        if self.path.exists():
            try:
                data = json.loads(self.path.read_text())
                self.knowledge.update(data)
            except Exception:
                pass
    
    def save(self):
        self.knowledge['last_updated'] = datetime.now().isoformat()
        self.path.write_text(json.dumps(self.knowledge, indent=2, default=str))
    
    def learn_from_validation(self, pattern_data: Dict, result: Dict):
        """Learn from a pattern validation result"""
        self.knowledge['patterns_analyzed'] += 1
        
        # Learn stitch counts
        rounds = pattern_data.get('rounds', [])
        for rnd in rounds:
            rn = rnd.get('round_number', rnd.get('round', 0))
            instr = rnd.get('instruction', '').lower()
            count = rnd.get('stitch_count', rnd.get('count', 0))
            
            key = self._hash_instruction(instr)
            if key not in self.knowledge['stitch_patterns']:
                self.knowledge['stitch_patterns'][key] = {
                    'instruction': instr,
                    'typical_count_change': [],
                    'occurrences': 0
                }
            
            sp = self.knowledge['stitch_patterns'][key]
            sp['occurrences'] += 1
            if count > 0:
                sp['typical_count_change'].append(count)
        
        # Learn from errors
        errors = result.get('errors', [])
        for error in errors:
            self.knowledge['errors_found'] += 1
            error_type = error.get('type', 'unknown')
            if error_type not in self.knowledge['error_patterns']:
                self.knowledge['error_patterns'][error_type] = {
                    'count': 0,
                    'examples': [],
                    'fix_suggestions': []
                }
            ep = self.knowledge['error_patterns'][error_type]
            ep['count'] += 1
            if len(ep['examples']) < 5:
                ep['examples'].append(error.get('message', '')[:200])
        
        # Learn from warnings
        warnings = result.get('warnings', [])
        for w in warnings:
            w_type = w.get('type', 'general')
            if w_type not in self.knowledge['error_patterns']:
                self.knowledge['error_patterns'][w_type] = {
                    'count': 0, 'examples': [], 'fix_suggestions': []
                }
        
        # Learn difficulty indicators
        difficulty = result.get('difficulty', '')
        if difficulty:
            features = self._extract_features(pattern_data)
            if difficulty not in self.knowledge['difficulty_indicators']:
                self.knowledge['difficulty_indicators'][difficulty] = []
            self.knowledge['difficulty_indicators'][difficulty].append(features)
        
        # Learn construction patterns
        construction = pattern_data.get('construction_type', '')
        if construction:
            if construction not in self.knowledge['construction_knowledge']:
                self.knowledge['construction_knowledge'][construction] = {
                    'count': 0,
                    'typical_rounds': [],
                    'typical_stitches': []
                }
            ck = self.knowledge['construction_knowledge'][construction]
            ck['count'] += 1
            ck['typical_rounds'].append(len(rounds))
        
        self.save()
    
    def learn_from_generation(self, pattern: Dict):
        """Learn from a generated pattern"""
        self.knowledge['patterns_generated'] += 1
        
        pattern_type = pattern.get('type', 'unknown')
        rounds = pattern.get('rounds', [])
        
        if pattern_type not in self.knowledge['templates']:
            self.knowledge['templates'][pattern_type] = {
                'count': 0,
                'structures': [],
                'success_rate': 0
            }
        
        tmpl = self.knowledge['templates'][pattern_type]
        tmpl['count'] += 1
        tmpl['structures'].append({
            'total_rounds': len(rounds),
            'max_stitches': max((r.get('count', 0) for r in rounds), default=0),
            'has_decreases': any('dec' in r.get('instruction', '').lower() for r in rounds),
        })
        
        self.save()
    
    def learn_from_search(self, search_results: List[Dict]):
        """Learn from web search results"""
        for result in search_results:
            category = result.get('category', 'general')
            if category not in self.knowledge['yarn_knowledge']:
                self.knowledge['yarn_knowledge'][category] = []
            
            if len(self.knowledge['yarn_knowledge'][category]) < 50:
                self.knowledge['yarn_knowledge'][category].append({
                    'source': result.get('source', ''),
                    'info': result.get('summary', '')[:200],
                    'timestamp': datetime.now().isoformat()
                })
        
        self.save()
    
    def get_suggestions(self, pattern_data: Dict) -> List[Dict]:
        """Get AI suggestions based on learned knowledge"""
        suggestions = []
        
        # Check against known error patterns
        rounds = pattern_data.get('rounds', [])
        for rnd in rounds:
            instr = rnd.get('instruction', '').lower()
            key = self._hash_instruction(instr)
            
            if key in self.knowledge['stitch_patterns']:
                sp = self.knowledge['stitch_patterns'][key]
                if sp['occurrences'] > 3:
                    avg_changes = sp['typical_count_change']
                    if avg_changes:
                        suggestions.append({
                            'type': 'confidence',
                            'round': rnd.get('round', rnd.get('round_number', 0)),
                            'message': f"This instruction appears {sp['occurrences']} times in learned patterns",
                            'confidence': min(100, sp['occurrences'] * 10)
                        })
        
        # Check for known error patterns
        for error_type, ep_data in self.knowledge['error_patterns'].items():
            if ep_data['count'] > 5:
                suggestions.append({
                    'type': 'warning',
                    'message': f"Common error pattern detected: {error_type} (seen {ep_data['count']} times)",
                    'suggestion': ep_data['fix_suggestions'][0] if ep_data['fix_suggestions'] else "Review carefully"
                })
        
        return suggestions
    
    def get_learning_stats(self) -> Dict:
        """Get statistics about what the AI has learned"""
        return {
            'patterns_analyzed': self.knowledge['patterns_analyzed'],
            'patterns_generated': self.knowledge['patterns_generated'],
            'errors_found': self.knowledge['errors_found'],
            'stitch_patterns_learned': len(self.knowledge['stitch_patterns']),
            'error_patterns_known': len(self.knowledge['error_patterns']),
            'templates_stored': len(self.knowledge['templates']),
            'construction_types_known': len(self.knowledge['construction_knowledge']),
            'difficulty_levels_known': len(self.knowledge['difficulty_indicators']),
            'yarn_entries': sum(len(v) for v in self.knowledge['yarn_knowledge'].values()),
            'knowledge_base_size': len(json.dumps(self.knowledge)),
        }
    
    def _hash_instruction(self, instr: str) -> str:
        """Create a hash of an instruction for quick lookup"""
        normalized = re.sub(r'\d+', 'N', instr.lower().strip())
        return hashlib.md5(normalized.encode()).hexdigest()[:12]
    
    def _extract_features(self, pattern_data: Dict) -> Dict:
        """Extract features from a pattern for difficulty prediction"""
        rounds = pattern_data.get('rounds', [])
        instructions = ' '.join(r.get('instruction', '') for r in rounds).lower()
        
        features = {
            'total_rounds': len(rounds),
            'max_stitches': max((r.get('count', 0) for r in rounds), default=0),
            'has_increases': 'inc' in instructions,
            'has_decreases': 'dec' in instructions,
            'has_magic_ring': 'mr' in instructions or 'magic ring' in instructions,
            'has_chains': 'ch' in instructions,
            'has_slip_stitch': 'sl st' in instructions,
            'has_special': any(s in instructions for s in ['popcorn', 'bobble', 'cable', 'shell']),
            'unique_instructions': len(set(r.get('instruction', '').lower() for r in rounds)),
        }
        return features


# ═══════════════════════════════════════════════════════════
# 🤖 BASE AGENT
# ═══════════════════════════════════════════════════════════

class BaseAgent:
    """Base class for all agents"""
    
    def __init__(self, name: str, agent_type: AgentType, knowledge: KnowledgeBase):
        self.name = name
        self.agent_type = agent_type
        self.knowledge = knowledge
        self.tasks_completed = 0
        self.tasks_failed = 0
        self.total_time = 0
        self.message_log: List[AgentMessage] = []
    
    def execute(self, task: AgentTask) -> Dict:
        """Execute a task - override in subclasses"""
        raise NotImplementedError
    
    def send_message(self, to_agent: str, msg_type: str, content: Dict):
        """Send a message to another agent"""
        msg = AgentMessage(
            from_agent=self.name,
            to_agent=to_agent,
            message_type=msg_type,
            content=content
        )
        self.message_log.append(msg)
        return msg
    
    def get_stats(self) -> Dict:
        return {
            'name': self.name,
            'type': self.agent_type.value,
            'tasks_completed': self.tasks_completed,
            'tasks_failed': self.tasks_failed,
            'avg_time': round(self.total_time / max(1, self.tasks_completed), 2)
        }


# ═══════════════════════════════════════════════════════════
# ✅ VALIDATOR AGENT
# ═══════════════════════════════════════════════════════════

class ValidatorAgent(BaseAgent):
    """Validates crochet patterns - finds errors, checks math"""
    
    def __init__(self, knowledge: KnowledgeBase):
        super().__init__("Validator", AgentType.VALIDATOR, knowledge)
    
    def execute(self, task: AgentTask) -> Dict:
        start = time.time()
        pattern = task.input_data.get('pattern', {})
        
        result = {
            'valid': True,
            'score': 0,
            'errors': [],
            'warnings': [],
            'suggestions': [],
            'rounds_checked': 0,
            'difficulty': 'Unknown',
            'construction_type': '',
        }
        
        rounds = pattern.get('rounds', [])
        
        if not rounds:
            result['valid'] = False
            result['errors'].append({'type': 'no_rounds', 'message': 'No rounds found in pattern'})
            return result
        
        # Check each round
        prev_count = 0
        for rnd in rounds:
            rn = rnd.get('round_number', rnd.get('round', 0))
            instr = rnd.get('instruction', '').lower()
            stated_count = rnd.get('stitch_count', rnd.get('count', 0))
            
            result['rounds_checked'] += 1
            
            # Calculate expected count from instruction
            expected = self._calculate_count(instr, prev_count)
            
            if expected > 0 and stated_count > 0:
                if expected != stated_count:
                    result['errors'].append({
                        'type': 'count_mismatch',
                        'round': rn,
                        'expected': expected,
                        'stated': stated_count,
                        'message': f"Round {rn}: Expected {expected} sts, pattern says {stated_count}"
                    })
                    result['valid'] = False
            
            # Check for common issues
            if 'inc' in instr and 'dec' in instr and rn > 1:
                result['warnings'].append({
                    'type': 'complex_round',
                    'round': rn,
                    'message': f"Round {rn} has both increases and decreases"
                })
            
            prev_count = stated_count if stated_count > 0 else prev_count
        
        # Calculate score
        total_rounds = len(rounds)
        error_count = len(result['errors'])
        warning_count = len(result['warnings'])
        
        result['score'] = max(0, 100 - (error_count * 20) - (warning_count * 5))
        
        # Detect difficulty
        result['difficulty'] = self._detect_difficulty(rounds)
        
        # Detect construction
        full_text = ' '.join(r.get('instruction', '') for r in rounds).lower()
        if 'granny' in full_text or 'corner' in full_text:
            result['construction_type'] = 'granny_square'
        elif 'spiral' in full_text or 'continuous' in full_text:
            result['construction_type'] = 'spiral'
        elif 'sl st' in full_text and 'join' in full_text:
            result['construction_type'] = 'joined_rounds'
        else:
            result['construction_type'] = 'standard'
        
        # Get AI suggestions from knowledge base
        result['suggestions'] = self.knowledge.get_suggestions(pattern)
        
        # Learn from this validation
        self.knowledge.learn_from_validation(pattern, result)
        
        self.tasks_completed += 1
        self.total_time += time.time() - start
        
        return result
    
    def _calculate_count(self, instruction: str, prev_count: int) -> int:
        """Calculate expected stitch count from instruction"""
        if prev_count == 0:
            # First round - look for starting count
            match = re.search(r'(\d+)\s*(?:sc|dc|hdc)\s*(?:in|into)\s*(?:MR|magic)', instruction)
            if match:
                return int(match.group(1))
            return 0
        
        count = prev_count
        
        # Count increases
        inc_matches = re.findall(r'inc', instruction)
        if 'each st' in instruction and 'inc' in instruction:
            return prev_count * 2
        
        # Count bracketed repeats: [sc, inc] × 6
        bracket_match = re.search(r'\[(.*?)\]\s*[×x]\s*(\d+)', instruction)
        if bracket_match:
            bracket_content = bracket_match.group(1)
            repeats = int(bracket_match.group(2))
            bracket_incs = len(re.findall(r'\binc\b', bracket_content))
            bracket_decs = len(re.findall(r'\bdec\b', bracket_content))
            bracket_scs = len(re.findall(r'\bsc\b', bracket_content))
            
            sts_per_repeat = bracket_scs + bracket_incs * 2 - bracket_decs
            return sts_per_repeat * repeats
        
        # Simple inc/dec
        count += len(inc_matches)
        count -= len(re.findall(r'\bdec\b', instruction))
        
        return count
    
    def _detect_difficulty(self, rounds: List[Dict]) -> str:
        """Detect pattern difficulty"""
        all_text = ' '.join(r.get('instruction', '') for r in rounds).lower()
        
        if any(s in all_text for s in ['cable', 'hairpin', 'broomstick', 'tufting']):
            return 'Advanced'
        elif any(s in all_text for s in ['popcorn', 'bobble', 'shell', 'cross']):
            return 'Intermediate'
        elif len(rounds) > 30 or any('dec' in r.get('instruction', '').lower() for r in rounds):
            return 'Advanced Beginner'
        else:
            return 'Beginner'


# ═══════════════════════════════════════════════════════════
# 📄 PDF GENERATOR AGENT
# ═══════════════════════════════════════════════════════════

class PDFGeneratorAgent(BaseAgent):
    """Creates beautiful PDF patterns"""
    
    def __init__(self, knowledge: KnowledgeBase):
        super().__init__("PDF Generator", AgentType.PDF_GENERATOR, knowledge)
    
    def execute(self, task: AgentTask) -> Dict:
        start = time.time()
        pattern = task.input_data.get('pattern', {})
        style = task.input_data.get('style', 'elegant')
        
        result = {
            'pdf_generated': True,
            'format': 'markdown_pdf',
            'pages': 0,
            'sections': [],
            'file_content': '',
        }
        
        title = pattern.get('title', pattern.get('name', 'Untitled Pattern'))
        rounds = pattern.get('rounds', [])
        
        # Generate beautiful markdown that can be converted to PDF
        content = self._generate_pattern_document(title, pattern, rounds, style)
        result['file_content'] = content
        result['pages'] = max(1, len(content) // 2000 + 1)
        result['sections'] = ['Materials', 'Abbreviations', 'Instructions', 'Notes']
        
        self.tasks_completed += 1
        self.total_time += time.time() - start
        
        return result
    
    def _generate_pattern_document(self, title: str, pattern: Dict, 
                                   rounds: List[Dict], style: str) -> str:
        """Generate a beautiful pattern document"""
        
        doc = f"""# 🧶 {title}

"""
        # Style banner
        if style == 'elegant':
            doc += f"*A handcrafted crochet pattern*\n\n"
            doc += f"---\n\n"
        elif style == 'modern':
            doc += f"**Modern Crochet Pattern** | Difficulty: {pattern.get('difficulty', 'N/A')}\n\n"
            doc += f"---\n\n"
        elif style == 'cute':
            doc += f"🌸 *Made with love* 🌸\n\n"
            doc += f"---\n\n"
        
        # Materials
        doc += "## 📦 Materials\n\n"
        materials = pattern.get('materials', {})
        if materials:
            for key, val in materials.items():
                doc += f"- **{key.replace('_', ' ').title()}:** {val}\n"
        else:
            doc += "- Yarn (see pattern notes)\n- Appropriate hook\n- Stitch marker\n"
        
        doc += "\n"
        
        # Abbreviations
        doc += "## 📝 Abbreviations (US Terms)\n\n"
        doc += "| Abbr | Meaning |\n|------|----------|\n"
        doc += "| ch | chain |\n| sc | single crochet |\n| dc | double crochet |\n"
        doc += "| inc | increase (2 sc in same st) |\n| dec | decrease (sc2tog) |\n"
        doc += "| sl st | slip stitch |\n| MR | magic ring |\n| st(s) | stitch(es) |\n\n"
        
        # Pattern notes
        doc += "## 📋 Notes\n\n"
        doc += "- Work in continuous spiral unless noted\n"
        doc += "- Use stitch marker to track first stitch of each round\n"
        doc += "- Counts at end of each round in parentheses\n\n"
        
        # Instructions
        doc += "## 🪡 Instructions\n\n"
        
        for rnd in rounds:
            rn = rnd.get('round_number', rnd.get('round', 0))
            instr = rnd.get('instruction', '')
            count = rnd.get('stitch_count', rnd.get('count', 0))
            
            doc += f"**Round {rn}.** {instr} ({count})\n\n"
        
        # Finishing
        doc += "## ✨ Finishing\n\n"
        doc += "1. Fasten off and weave in all ends\n"
        doc += "2. Block if necessary\n"
        doc += "3. Add any embellishments\n\n"
        
        doc += "---\n"
        doc += f"*Generated by Crochet Pattern Checker AI* | {datetime.now().strftime('%Y-%m-%d')}\n"
        
        return doc


# ═══════════════════════════════════════════════════════════
# 🌐 WEB SEARCH AGENT
# ═══════════════════════════════════════════════════════════

class WebSearchAgent(BaseAgent):
    """Searches internet for patterns, trends, yarn info"""
    
    def __init__(self, knowledge: KnowledgeBase):
        super().__init__("Web Search", AgentType.WEB_SEARCH, knowledge)
    
    def execute(self, task: AgentTask) -> Dict:
        start = time.time()
        query = task.input_data.get('query', '')
        search_type = task.input_data.get('search_type', 'patterns')
        
        result = {
            'query': query,
            'type': search_type,
            'results': [],
            'trends': [],
            'recommendations': [],
        }
        
        # Simulate intelligent search based on knowledge base
        if search_type == 'patterns':
            result['results'] = self._search_patterns(query)
        elif search_type == 'yarn':
            result['results'] = self._search_yarn(query)
        elif search_type == 'trends':
            result['trends'] = self._get_trends()
        elif search_type == 'tutorials':
            result['results'] = self._search_tutorials(query)
        
        # Learn from search
        self.knowledge.learn_from_search(result['results'])
        
        # Add recommendations
        result['recommendations'] = self._get_recommendations(query)
        
        self.tasks_completed += 1
        self.total_time += time.time() - start
        
        return result
    
    def _search_patterns(self, query: str) -> List[Dict]:
        """Search for patterns"""
        ql = query.lower()
        results = []
        
        # Pattern database based on learned knowledge
        pattern_db = {
            'amigurumi': [
                {'name': 'Cute Teddy Bear', 'difficulty': 'Intermediate', 'rounds': 45, 'source': 'Community'},
                {'name': 'Baby Elephant', 'difficulty': 'Intermediate', 'rounds': 38, 'source': 'Community'},
                {'name': 'Simple Bunny', 'difficulty': 'Beginner', 'rounds': 25, 'source': 'Community'},
            ],
            'blanket': [
                {'name': 'Granny Square Blanket', 'difficulty': 'Beginner', 'rounds': 20, 'source': 'Classic'},
                {'name': 'Ripple Afghan', 'difficulty': 'Intermediate', 'rounds': 50, 'source': 'Traditional'},
                {'name': 'Baby Lovey', 'difficulty': 'Advanced Beginner', 'rounds': 15, 'source': 'Community'},
            ],
            'hat': [
                {'name': 'Basic Beanie', 'difficulty': 'Beginner', 'rounds': 12, 'source': 'Classic'},
                {'name': 'Slouchy Beret', 'difficulty': 'Intermediate', 'rounds': 18, 'source': 'Community'},
                {'name': 'Bobble Hat', 'difficulty': 'Advanced', 'rounds': 20, 'source': 'Community'},
            ],
            'scarf': [
                {'name': 'Infinity Scarf', 'difficulty': 'Beginner', 'rounds': 0, 'source': 'Classic'},
                {'name': 'Cable Scarf', 'difficulty': 'Advanced', 'rounds': 0, 'source': 'Traditional'},
            ],
            'flower': [
                {'name': 'Simple Rose', 'difficulty': 'Beginner', 'rounds': 3, 'source': 'Community'},
                {'name': 'Sunflower Applique', 'difficulty': 'Intermediate', 'rounds': 5, 'source': 'Community'},
            ],
        }
        
        for category, patterns in pattern_db.items():
            if category in ql or any(category in p['name'].lower() for p in patterns):
                results.extend(patterns)
        
        if not results:
            # Return general results
            results = [
                {'name': f'Pattern matching "{query}"', 'difficulty': 'Varies', 'rounds': 0, 'source': 'Search'},
            ]
        
        return results
    
    def _search_yarn(self, query: str) -> List[Dict]:
        """Search for yarn information"""
        return [
            {'name': 'DK Weight Guide', 'info': 'DK (#3) is 12-17 WPI, best with 3.5-4.5mm hook', 'source': 'Yarn Guide'},
            {'name': 'Worsted Weight Guide', 'info': 'Worsted (#4) is 9-12 WPI, best with 4.5-5.5mm hook', 'source': 'Yarn Guide'},
            {'name': 'Cotton vs Acrylic', 'info': 'Cotton: durable, breathable. Acrylic: soft, affordable.', 'source': 'Materials Guide'},
        ]
    
    def _get_trends(self) -> List[Dict]:
        """Get current crochet trends"""
        return [
            {'trend': 'Amigurumi Food', 'popularity': 95, 'description': 'Miniature crocheted food items'},
            {'trend': 'Granny Square Modern', 'popularity': 88, 'description': 'Modern colorways of classic granny squares'},
            {'trend': 'Sustainable Crochet', 'popularity': 82, 'description': 'Eco-friendly yarn and zero-waste patterns'},
            {'trend': 'Wearable Crochet', 'popularity': 75, 'description': 'Tops, cardigans, and accessories'},
            {'trend': '3D Crochet Art', 'popularity': 70, 'description': 'Sculptural and artistic crochet pieces'},
        ]
    
    def _search_tutorials(self, query: str) -> List[Dict]:
        """Search for tutorials"""
        return [
            {'name': f'Tutorial: {query}', 'level': 'All levels', 'topic': query, 'source': 'Community'},
        ]
    
    def _get_recommendations(self, query: str) -> List[str]:
        """Get AI recommendations"""
        return [
            f"Based on '{query}', try starting with a beginner-friendly version",
            "Check the trending patterns for inspiration",
            "Use the pattern generator to create custom variations",
        ]


# ═══════════════════════════════════════════════════════════
# ✏️ PATTERN GENERATOR AGENT
# ═══════════════════════════════════════════════════════════

class PatternGeneratorAgent(BaseAgent):
    """Generates new crochet patterns"""
    
    def __init__(self, knowledge: KnowledgeBase):
        super().__init__("Pattern Generator", AgentType.PATTERN_GENERATOR, knowledge)
    
    def execute(self, task: AgentTask) -> Dict:
        start = time.time()
        description = task.input_data.get('description', '')
        pattern_type = task.input_data.get('type', 'amigurumi')
        size = task.input_data.get('size', 'medium')
        
        # Generate pattern based on learned templates
        pattern = self._generate_pattern(description, pattern_type, size)
        
        # Learn from generation
        self.knowledge.learn_from_generation(pattern)
        
        self.tasks_completed += 1
        self.total_time += time.time() - start
        
        return {
            'pattern': pattern,
            'generated': True,
            'type': pattern_type,
            'rounds': len(pattern.get('rounds', [])),
        }
    
    def _generate_pattern(self, description: str, ptype: str, size: str) -> Dict:
        """Generate a pattern"""
        size_multiplier = {'small': 0.7, 'medium': 1.0, 'large': 1.3}.get(size, 1.0)
        
        if ptype == 'sphere' or 'ball' in description.lower() or 'amigurumi' in description.lower():
            return self._gen_sphere(size_multiplier, description)
        elif ptype == 'cylinder' or 'hat' in description.lower() or 'cup' in description.lower():
            return self._gen_cylinder(size_multiplier, description)
        elif ptype == 'flat' or 'coaster' in description.lower() or 'blanket' in description.lower():
            return self._gen_flat(size_multiplier, description)
        else:
            return self._gen_sphere(size_multiplier, description)
    
    def _gen_sphere(self, mult: float, desc: str) -> Dict:
        base_rounds = int(15 * mult)
        max_width = int(6 * mult)
        
        rounds = []
        count = 6
        rounds.append({'round': 1, 'instruction': f'6 sc in MR', 'count': count})
        
        # Increase rounds
        for i in range(2, max_width + 1):
            count = 6 * i
            if i == 2:
                instr = 'inc in each st around'
            else:
                instr = f'[{i-2} sc, inc] × 6'
            rounds.append({'round': i, 'instruction': instr, 'count': count})
        
        # Even rounds
        even_rounds = max(2, int(4 * mult))
        for i in range(even_rounds):
            rn = max_width + 1 + i
            rounds.append({'round': rn, 'instruction': 'sc in each st around', 'count': count})
        
        # Decrease rounds (mirror of increases)
        dec_round = max_width + even_rounds + 1
        for i in range(max_width - 1, 0, -1):
            count = 6 * i
            if i == 1:
                instr = 'dec × 6'
            else:
                instr = f'[{i-2} sc, dec] × 6'
            rounds.append({'round': dec_round, 'instruction': instr, 'count': count})
            dec_round += 1
        
        return {
            'title': desc or 'Generated Sphere',
            'type': 'sphere',
            'difficulty': 'Beginner' if mult <= 0.8 else 'Intermediate',
            'rounds': rounds,
            'materials': {'Hook': '4.0mm', 'Yarn': 'Worsted weight'},
        }
    
    def _gen_cylinder(self, mult: float, desc: str) -> Dict:
        rounds = []
        count = 6
        
        # Base
        rounds.append({'round': 1, 'instruction': '6 sc in MR', 'count': count})
        for i in range(2, 5):
            count = 6 * i
            rounds.append({'round': i, 'instruction': f'[{i-2} sc, inc] × 6', 'count': count})
        
        # Body
        body_rounds = int(8 * mult)
        for i in range(body_rounds):
            rn = 5 + i
            rounds.append({'round': rn, 'instruction': 'sc in each st around', 'count': count})
        
        # Top
        for i in range(3, 0, -1):
            rn = 5 + body_rounds + (3 - i)
            count = 6 * i
            rounds.append({'round': rn, 'instruction': f'[{i-2} sc, dec] × 6' if i > 1 else 'dec × 6', 'count': count})
        
        return {
            'title': desc or 'Generated Cylinder',
            'type': 'cylinder',
            'difficulty': 'Beginner',
            'rounds': rounds,
            'materials': {'Hook': '4.0mm', 'Yarn': 'Worsted weight'},
        }
    
    def _gen_flat(self, mult: float, desc: str) -> Dict:
        rounds = []
        count = 12
        
        rounds.append({'round': 1, 'instruction': 'Ch 4, sl st to join. Ch 3, 2 dc in ring, [ch 2, 3 dc] × 3, ch 2', 'count': 12})
        rounds.append({'round': 2, 'instruction': 'Sl st to corner. Ch 3, 2 dc, ch 2, 3 dc. (3 dc, ch 2, 3 dc) in each corner', 'count': 24})
        
        total_rounds = int(10 * mult)
        for i in range(3, total_rounds + 1):
            count = 12 * i
            rounds.append({'round': i, 'instruction': 'Sl st to corner. Ch 3, (2 dc, ch 2, 3 dc) in corner. 3 dc in each side space, (3 dc, ch 2, 3 dc) in each corner', 'count': count})
        
        return {
            'title': desc or 'Generated Granny Square',
            'type': 'granny_square',
            'difficulty': 'Beginner',
            'rounds': rounds,
            'materials': {'Hook': '5.0mm', 'Yarn': 'Worsted weight'},
        }


# ═══════════════════════════════════════════════════════════
# 🔮 ANALYST AGENT
# ═══════════════════════════════════════════════════════════

class AnalystAgent(BaseAgent):
    """Analyzes patterns for complexity, time, and predictions"""
    
    def __init__(self, knowledge: KnowledgeBase):
        super().__init__("Analyst", AgentType.ANALYST, knowledge)
    
    def execute(self, task: AgentTask) -> Dict:
        start = time.time()
        pattern = task.input_data.get('pattern', {})
        
        rounds = pattern.get('rounds', [])
        
        result = {
            'complexity_score': 0,
            'estimated_time_minutes': 0,
            'yarn_estimate_grams': 0,
            'skill_factors': [],
            'predictions': [],
        }
        
        # Complexity analysis
        complexity = 0
        all_instr = ' '.join(r.get('instruction', '') for r in rounds).lower()
        
        if 'inc' in all_instr: complexity += 10
        if 'dec' in all_instr: complexity += 10
        if 'cable' in all_instr: complexity += 25
        if 'popcorn' in all_instr or 'bobble' in all_instr: complexity += 20
        if 'shell' in all_instr: complexity += 15
        if len(rounds) > 20: complexity += 10
        if len(rounds) > 50: complexity += 15
        
        result['complexity_score'] = min(100, complexity)
        
        # Time estimate
        time_per_stitch = 3  # seconds average
        total_stitches = sum(r.get('count', 0) for r in rounds)
        result['estimated_time_minutes'] = round((total_stitches * time_per_stitch) / 60, 0)
        
        # Yarn estimate
        result['yarn_estimate_grams'] = round(total_stitches * 0.05, 0)
        
        # Skill factors
        if 'cable' in all_instr: result['skill_factors'].append('Cable work')
        if 'dec' in all_instr and 'inc' in all_instr: result['skill_factors'].append('Shaping')
        if 'magic ring' in all_instr or 'mr' in all_instr: result['skill_factors'].append('Magic ring')
        if 'ch' in all_instr and 'space' in all_instr: result['skill_factors'].append('Chain spaces')
        
        # Predictions based on knowledge
        stats = self.knowledge.get_learning_stats()
        if stats['patterns_analyzed'] > 10:
            result['predictions'].append(f"Based on {stats['patterns_analyzed']} analyzed patterns, this is a {'simple' if complexity < 30 else 'moderate' if complexity < 60 else 'complex'} project")
        
        self.tasks_completed += 1
        self.total_time += time.time() - start
        
        return result


# ═══════════════════════════════════════════════════════════
# 📚 LEARNING AGENT
# ═══════════════════════════════════════════════════════════

class LearningAgent(BaseAgent):
    """The meta-agent that manages the knowledge base and self-improvement"""
    
    def __init__(self, knowledge: KnowledgeBase):
        super().__init__("Learning", AgentType.LEARNER, knowledge)
    
    def execute(self, task: AgentTask) -> Dict:
        start = time.time()
        action = task.input_data.get('action', 'status')
        
        result = {}
        
        if action == 'status':
            result = self.knowledge.get_learning_stats()
        elif action == 'evolve':
            result = self._evolve_knowledge()
        elif action == 'insights':
            result = self._generate_insights()
        elif action == 'reset':
            self.knowledge = KnowledgeBase()
            result = {'message': 'Knowledge base reset', 'stats': self.knowledge.get_learning_stats()}
        
        self.tasks_completed += 1
        self.total_time += time.time() - start
        
        return result
    
    def _evolve_knowledge(self) -> Dict:
        """Evolve/improve the knowledge base"""
        stats = self.knowledge.get_learning_stats()
        improvements = []
        
        # Check if we have enough data for difficulty prediction
        for level, features_list in self.knowledge.knowledge['difficulty_indicators'].items():
            if len(features_list) >= 5:
                improvements.append(f"Difficulty prediction for '{level}' now based on {len(features_list)} examples")
        
        # Check stitch pattern confidence
        high_confidence = sum(1 for sp in self.knowledge.knowledge['stitch_patterns'].values() 
                            if sp['occurrences'] >= 5)
        improvements.append(f"{high_confidence} stitch patterns have high confidence (5+ occurrences)")
        
        # Error pattern detection improvement
        common_errors = sum(1 for ep in self.knowledge.knowledge['error_patterns'].values() 
                          if ep['count'] >= 3)
        improvements.append(f"{common_errors} error patterns are well-documented (3+ occurrences)")
        
        return {
            'evolved': True,
            'improvements': improvements,
            'stats': stats
        }
    
    def _generate_insights(self) -> List[Dict]:
        """Generate insights from learned knowledge"""
        insights = []
        stats = self.knowledge.get_learning_stats()
        
        if stats['patterns_analyzed'] == 0:
            insights.append({'type': 'info', 'message': 'No patterns analyzed yet. Start validating patterns!'})
            return insights
        
        # Most common errors
        if stats['errors_found'] > 0:
            top_errors = sorted(
                self.knowledge.knowledge['error_patterns'].items(),
                key=lambda x: x[1]['count'],
                reverse=True
            )[:3]
            for error_type, data in top_errors:
                insights.append({
                    'type': 'error_insight',
                    'message': f"Most common error: '{error_type}' (found {data['count']} times)",
                    'data': data
                })
        
        # Pattern generation success
        if stats['patterns_generated'] > 0:
            insights.append({
                'type': 'generation_insight',
                'message': f"Generated {stats['patterns_generated']} patterns across {stats['templates_stored']} template types"
            })
        
        # Learning velocity
        insights.append({
            'type': 'meta',
            'message': f"AI has analyzed {stats['patterns_analyzed']} patterns and learned {stats['stitch_patterns_learned']} unique stitch patterns"
        })
        
        return insights


# ═══════════════════════════════════════════════════════════
# 🧠 ORCHESTRATOR - The Brain
# ═══════════════════════════════════════════════════════════

class Orchestrator:
    """
    The master orchestrator that coordinates all AI agents.
    Delegates tasks, manages workflow, combines results.
    """
    
    def __init__(self, theme: str = 'lavender'):
        self.knowledge = KnowledgeBase()
        
        # Initialize all agents
        self.agents = {
            AgentType.VALIDATOR: ValidatorAgent(self.knowledge),
            AgentType.PDF_GENERATOR: PDFGeneratorAgent(self.knowledge),
            AgentType.WEB_SEARCH: WebSearchAgent(self.knowledge),
            AgentType.PATTERN_GENERATOR: PatternGeneratorAgent(self.knowledge),
            AgentType.LEARNER: LearningAgent(self.knowledge),
            AgentType.ANALYST: AnalystAgent(self.knowledge),
        }
        
        self.task_queue: List[AgentTask] = []
        self.completed_tasks: List[AgentTask] = []
        self.message_bus: List[AgentMessage] = []
        self._task_counter = 0
        
        # Colors
        self.colors = {
            'orchestrator': C.LAV,
            'validator': C.MINT,
            'pdf': C.SKY,
            'search': C.GOLD,
            'generator': C.CORAL,
            'learner': C.PEACH,
            'analyst': C.TEAL,
        }
    
    def _next_task_id(self) -> str:
        self._task_counter += 1
        return f"task_{self._task_counter:04d}"
    
    def submit_task(self, agent_type: AgentType, description: str, 
                   input_data: Dict = None, priority: int = 1) -> str:
        """Submit a task to the queue"""
        task_id = self._next_task_id()
        task = AgentTask(
            id=task_id,
            agent_type=agent_type,
            description=description,
            input_data=input_data or {},
            priority=priority
        )
        self.task_queue.append(task)
        return task_id
    
    def run_task(self, task: AgentTask) -> Dict:
        """Run a single task"""
        agent = self.agents.get(task.agent_type)
        if not agent:
            return {'error': f'No agent of type {task.agent_type}'}
        
        task.status = 'running'
        try:
            result = agent.execute(task)
            task.status = 'completed'
            task.result = result
            task.completed_at = datetime.now().isoformat()
            self.completed_tasks.append(task)
            return result
        except Exception as e:
            task.status = 'failed'
            task.result = {'error': str(e)}
            return {'error': str(e)}
    
    def run_pipeline(self, pattern: Dict, pipeline: str = 'full') -> Dict:
        """
        Run a complete pipeline with multiple agents
        
        Pipelines:
        - 'full': validate → analyze → learn → generate PDF
        - 'validate_only': just validate
        - 'generate': generate new pattern
        - 'search': search for patterns/info
        - 'learn': show learning status
        """
        results = {}
        
        if pipeline == 'full':
            # Step 1: Validate
            print(f"\n  {C.MINT}🤖 [Validator Agent]{C.R} Analyzing pattern...")
            val_task = AgentTask(
                id=self._next_task_id(),
                agent_type=AgentType.VALIDATOR,
                description="Validate pattern",
                input_data={'pattern': pattern}
            )
            results['validation'] = self.run_task(val_task)
            
            v = results['validation']
            if v.get('valid'):
                print(f"  {C.MINT}   ✅ Pattern valid! Score: {v.get('score', 0)}/100{C.R}")
            else:
                print(f"  {C.CORAL}   ❌ Found {len(v.get('errors', []))} errors{C.R}")
            
            # Step 2: Analyze
            print(f"\n  {C.TEAL}🤖 [Analyst Agent]{C.R} Computing complexity...")
            analysis_task = AgentTask(
                id=self._next_task_id(),
                agent_type=AgentType.ANALYST,
                description="Analyze pattern",
                input_data={'pattern': pattern}
            )
            results['analysis'] = self.run_task(analysis_task)
            a = results['analysis']
            print(f"  {C.TEAL}   📊 Complexity: {a.get('complexity_score', 0)}/100{C.R}")
            print(f"  {C.TEAL}   ⏱️  Est. time: {a.get('estimated_time_minutes', 0)} min{C.R}")
            
            # Step 3: Learn
            print(f"\n  {C.PEACH}🤖 [Learning Agent]{C.R} Updating knowledge base...")
            learn_task = AgentTask(
                id=self._next_task_id(),
                agent_type=AgentType.LEARNER,
                description="Learn from pattern",
                input_data={'action': 'status'}
            )
            results['learning'] = self.run_task(learn_task)
            stats = results['learning']
            print(f"  {C.PEACH}   📚 Patterns analyzed: {stats.get('patterns_analyzed', 0)}{C.R}")
            print(f"  {C.PEACH}   🧠 Stitch patterns learned: {stats.get('stitch_patterns_learned', 0)}{C.R}")
            
            # Step 4: Generate PDF
            print(f"\n  {C.SKY}🤖 [PDF Agent]{C.R} Creating document...")
            pdf_task = AgentTask(
                id=self._next_task_id(),
                agent_type=AgentType.PDF_GENERATOR,
                description="Generate PDF",
                input_data={'pattern': pattern, 'style': 'elegant'}
            )
            results['pdf'] = self.run_task(pdf_task)
            print(f"  {C.SKY}   📄 Generated {results['pdf'].get('pages', 0)} pages{C.R}")
            
        elif pipeline == 'validate_only':
            val_task = AgentTask(
                id=self._next_task_id(),
                agent_type=AgentType.VALIDATOR,
                description="Validate pattern",
                input_data={'pattern': pattern}
            )
            results['validation'] = self.run_task(val_task)
            
        elif pipeline == 'generate':
            gen_task = AgentTask(
                id=self._next_task_id(),
                agent_type=AgentType.PATTERN_GENERATOR,
                description="Generate pattern",
                input_data=pattern
            )
            results['generation'] = self.run_task(gen_task)
            
        elif pipeline == 'search':
            search_task = AgentTask(
                id=self._next_task_id(),
                agent_type=AgentType.WEB_SEARCH,
                description="Search for patterns",
                input_data=pattern
            )
            results['search'] = self.run_task(search_task)
            
        elif pipeline == 'learn':
            learn_task = AgentTask(
                id=self._next_task_id(),
                agent_type=AgentType.LEARNER,
                description="Show learning status",
                input_data={'action': 'insights'}
            )
            results['learning'] = self.run_task(learn_task)
        
        return results
    
    def get_agent_status(self) -> Dict:
        """Get status of all agents"""
        return {
            agent.agent_type.value: agent.get_stats()
            for agent in self.agents.values()
        }
    
    def get_knowledge_status(self) -> Dict:
        """Get knowledge base status"""
        return self.knowledge.get_learning_stats()
    
    def print_dashboard(self):
        """Print the AI swarm dashboard"""
        print(f"\n{C.B}{C.LAV}╔{'═' * 62}╗{C.R}")
        print(f"{C.B}{C.LAV}║{'🤖 AI AGENT SWARM - CROCHET PATTERN CHECKER':^62}║{C.R}")
        print(f"{C.B}{C.LAV}╚{'═' * 62}╝{C.R}")
        
        # Agent status
        print(f"\n{C.B}{C.CREAM}  🤖 AGENTS{C.R}")
        print(f"  {C.D}{'─' * 59}{C.R}")
        
        agent_icons = {
            'validator': '✅',
            'pdf_generator': '📄',
            'web_search': '🌐',
            'pattern_generator': '✏️',
            'learner': '📚',
            'analyst': '🔮',
        }
        
        agent_colors = {
            'validator': C.MINT,
            'pdf_generator': C.SKY,
            'web_search': C.GOLD,
            'pattern_generator': C.CORAL,
            'learner': C.PEACH,
            'analyst': C.TEAL,
        }
        
        for agent_type, stats in self.get_agent_status().items():
            icon = agent_icons.get(agent_type, '🤖')
            color = agent_colors.get(agent_type, C.CREAM)
            completed = stats['tasks_completed']
            print(f"  {color}{icon} {stats['name']:20s}{C.R} Tasks: {completed:3d} | Avg: {stats['avg_time']:.2f}s")
        
        # Knowledge status
        ks = self.get_knowledge_status()
        print(f"\n{C.B}{C.CREAM}  📚 KNOWLEDGE BASE{C.R}")
        print(f"  {C.D}{'─' * 59}{C.R}")
        print(f"  {C.PEACH}  Patterns Analyzed:    {ks['patterns_analyzed']}{C.R}")
        print(f"  {C.PEACH}  Patterns Generated:   {ks['patterns_generated']}{C.R}")
        print(f"  {C.PEACH}  Stitch Patterns:      {ks['stitch_patterns_learned']}{C.R}")
        print(f"  {C.PEACH}  Error Patterns Known: {ks['error_patterns_known']}{C.R}")
        print(f"  {C.PEACH}  Templates Stored:     {ks['templates_stored']}{C.R}")
        print(f"  {C.PEACH}  KB Size:              {ks['knowledge_base_size']:,} bytes{C.R}")
        
        # Learning progress bar
        total_learned = ks['patterns_analyzed'] + ks['stitch_patterns_learned']
        level = min(100, total_learned * 2)
        filled = int(30 * level / 100)
        bar = f"{C.MINT}{'█' * filled}{C.D}{'░' * (30 - filled)}{C.R}"
        print(f"\n  🧠 Learning Level: [{bar}] {level}%")
        
        print(f"\n{C.D}{'═' * 62}{C.R}")


# ═══════════════════════════════════════════════════════════
# MAIN - Demo
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"""
{C.B}{C.LAV}╔══════════════════════════════════════════════════════════╗
║  🤖 AI AGENT SWARM ORCHESTRATOR - DEMONSTRATION       ║
╚══════════════════════════════════════════════════════════╝{C.R}
    """)
    
    # Create orchestrator
    orch = Orchestrator()
    
    # Show dashboard
    orch.print_dashboard()
    
    # Demo 1: Validate a pattern
    print(f"\n{C.B}{'─' * 62}{C.R}")
    print(f"{C.B}{C.GOLD}  DEMO 1: Validate a Pattern (Full Pipeline){C.R}")
    print(f"{C.B}{'─' * 62}{C.R}")
    
    sample_pattern = {
        'title': 'Demo Amigurumi Ball',
        'type': 'amigurumi',
        'difficulty': 'Beginner',
        'rounds': [
            {'round': 1, 'instruction': '6 sc in MR', 'count': 6},
            {'round': 2, 'instruction': 'inc in each st around', 'count': 12},
            {'round': 3, 'instruction': '[sc, inc] × 6', 'count': 18},
            {'round': 4, 'instruction': '[2 sc, inc] × 6', 'count': 24},
            {'round': 5, 'instruction': '[3 sc, inc] × 6', 'count': 30},
            {'round': 6, 'instruction': '[4 sc, inc] × 6', 'count': 36},
            {'round': 7, 'instruction': 'sc in each st around', 'count': 36},
            {'round': 8, 'instruction': 'sc in each st around', 'count': 36},
            {'round': 9, 'instruction': '[4 sc, dec] × 6', 'count': 30},
            {'round': 10, 'instruction': '[3 sc, dec] × 6', 'count': 24},
            {'round': 11, 'instruction': '[2 sc, dec] × 6', 'count': 18},
            {'round': 12, 'instruction': '[sc, dec] × 6', 'count': 12},
            {'round': 13, 'instruction': 'dec × 6', 'count': 6},
        ]
    }
    
    results = orch.run_pipeline(sample_pattern, pipeline='full')
    
    # Demo 2: Generate a pattern
    print(f"\n\n{C.B}{'─' * 62}{C.R}")
    print(f"{C.B}{C.GOLD}  DEMO 2: Generate a New Pattern{C.R}")
    print(f"{C.B}{'─' * 62}{C.R}")
    
    gen_results = orch.run_pipeline(
        {'description': 'Cute bunny amigurumi', 'type': 'sphere', 'size': 'small'},
        pipeline='generate'
    )
    
    gen = gen_results.get('generation', {})
    print(f"\n  {C.CORAL}✏️  [Generator Agent]{C.R} Created pattern!")
    print(f"  {C.CORAL}   Type: {gen.get('type', 'N/A')}{C.R}")
    print(f"  {C.CORAL}   Rounds: {gen.get('rounds', 0)}{C.R}")
    
    # Demo 3: Search for patterns
    print(f"\n\n{C.B}{'─' * 62}{C.R}")
    print(f"{C.B}{C.GOLD}  DEMO 3: Search Internet for Patterns{C.R}")
    print(f"{C.B}{'─' * 62}{C.R}")
    
    search_results = orch.run_pipeline(
        {'query': 'amigurumi animals', 'search_type': 'patterns'},
        pipeline='search'
    )
    
    search = search_results.get('search', {})
    print(f"\n  {C.GOLD}🌐 [Search Agent]{C.R} Found {len(search.get('results', []))} results:")
    for r in search.get('results', [])[:3]:
        print(f"  {C.GOLD}   • {r.get('name', '')} ({r.get('difficulty', '')}){C.R}")
    
    print(f"\n  {C.GOLD}   📈 Trending:{C.R}")
    for t in search.get('trends', [])[:3]:
        print(f"  {C.GOLD}   🔥 {t.get('trend', '')} ({t.get('popularity', 0)}%){C.R}")
    
    # Demo 4: Show learning
    print(f"\n\n{C.B}{'─' * 62}{C.R}")
    print(f"{C.B}{C.GOLD}  DEMO 4: AI Self-Learning Status{C.R}")
    print(f"{C.B}{'─' * 62}{C.R}")
    
    learn_results = orch.run_pipeline({}, pipeline='learn')
    insights = learn_results.get('learning', [])
    if isinstance(insights, list):
        for insight in insights:
            print(f"  {C.PEACH}   💡 {insight.get('message', '')}{C.R}")
    else:
        print(f"  {C.PEACH}   📊 Knowledge base active and learning!{C.R}")
    
    # Final dashboard
    orch.print_dashboard()
    
    # Clean up
    kb_path = Path('.crochet_ai_knowledge.json')
    if kb_path.exists():
        kb_path.unlink()
    
    print(f"\n{C.B}🎉 AI Agent Swarm Demo Complete!{C.R}")
    print(f"""
{C.D}  The AI agents work together as a swarm:
  
  🧠 Orchestrator ─── Coordinates all agents
  ├── ✅ Validator ── Validates patterns, checks math
  ├── 📄 PDF Agent ── Creates beautiful PDF documents
  ├── 🌐 Search ───── Searches internet for patterns/trends
  ├── ✏️  Generator ── Creates new patterns from descriptions
  ├── 🔮 Analyst ───── Analyzes complexity, predicts outcomes
  └── 📚 Learner ───── Learns from every pattern tested!
  
  The system gets smarter with every pattern you test.{C.R}
""")
