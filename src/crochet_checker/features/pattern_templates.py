
from typing import List
from dataclasses import dataclass

@dataclass
class PatternTemplate:
    template_id: str
    name: str
    category: str
    difficulty: str
    description: str
    content: str
    tags: List[str]

class PatternTemplateLibrary:
    def __init__(self):
        self.templates = {}
        self._load_default_templates()
    
    def _load_default_templates(self):
        self.templates["sphere"] = PatternTemplate(
            template_id="sphere",
            name="Simple Sphere",
            category="basic_shapes",
            difficulty="beginner",
            description="Basic sphere shape - foundation for many amigurumi projects",
            content="Round 1: 6 sc in magic ring (6)\nRound 2: 2 sc in each st around (12)",
            tags=["sphere", "basic", "beginner", "amigurumi"]
        )
        self.templates["bear"] = PatternTemplate(
            template_id="bear",
            name="Simple Bear",
            category="animals",
            difficulty="beginner",
            description="Simple amigurumi bear pattern",
            content="Round 1: 6 sc in magic ring (6)\nRound 2: 2 sc in each st around (12)",
            tags=["bear", "animal", "beginner", "amigurumi", "toy"]
        )
    
    def get_template(self, template_id: str) -> PatternTemplate:
        return self.templates.get(template_id)
    
    def list_templates(self, category: str = None, difficulty: str = None) -> List[PatternTemplate]:
        templates = list(self.templates.values())
        if category:
            templates = [t for t in templates if t.category == category]
        if difficulty:
            templates = [t for t in templates if t.difficulty == difficulty]
        return templates
    
    def search_templates(self, query: str) -> List[PatternTemplate]:
        query_lower = query.lower()
        results = []
        for template in self.templates.values():
            if (query_lower in template.name.lower() or
                query_lower in template.description.lower() or
                any(query_lower in tag.lower() for tag in template.tags)):
                results.append(template)
        return results

def format_template_list(templates: List[PatternTemplate]) -> str:
    if not templates:
        return "No templates found."
    output = [f"📋 Pattern Templates", "=" * 50, f"Found {len(templates)} template(s)\n"]
    for i, template in enumerate(templates, 1):
        output.append(f"{i}. {template.name}")
        output.append(f"   Category: {template.category} | Difficulty: {template.difficulty}")
        output.append(f"   {template.description}")
        output.append("")
    return "\n".join(output)
