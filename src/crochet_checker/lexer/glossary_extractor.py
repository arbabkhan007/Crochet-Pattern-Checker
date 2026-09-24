"""Glossary Extractor - Extracts stitch definitions"""
class GlossaryExtractor:
    def extract_glossary(self, text: str):
        glossary = {}
        for line in text.split('\n'):
            if ' - ' in line:
                parts = line.split(' - ')
                if len(parts) == 2:
                    glossary[parts[0].strip()] = parts[1].strip()
        return glossary
