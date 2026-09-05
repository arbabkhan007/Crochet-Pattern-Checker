
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
from typing import Dict, Any

class PatternExporter:
    def export_to_json(self, pattern_data: Dict[str, Any], output_path: str) -> str:
        with open(output_path, 'w') as f:
            json.dump(pattern_data, f, indent=2)
        return output_path
    
    def export_to_xml(self, pattern_data: Dict[str, Any], output_path: str) -> str:
        root = ET.Element("pattern")
        metadata = ET.SubElement(root, "metadata")
        ET.SubElement(metadata, "title").text = pattern_data.get("title", "Untitled")
        ET.SubElement(metadata, "category").text = pattern_data.get("category", "general")
        content = ET.SubElement(root, "content")
        content.text = pattern_data.get("content", "")
        xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
        with open(output_path, 'w') as f:
            f.write(xml_str)
        return output_path
    
    def export_to_yaml(self, pattern_data: Dict[str, Any], output_path: str) -> str:
        yaml_content = [f"title: {pattern_data.get('title', 'Untitled')}"]
        yaml_content.append(f"category: {pattern_data.get('category', 'general')}")
        yaml_content.append("\ncontent: |")
        for line in pattern_data.get("content", "").split('\n'):
            yaml_content.append(f"  {line}")
        with open(output_path, 'w') as f:
            f.write('\n'.join(yaml_content))
        return output_path
    
    def export_to_markdown(self, pattern_data: Dict[str, Any], output_path: str) -> str:
        md_content = [f"# {pattern_data.get('title', 'Untitled')}", ""]
        md_content.append(f"**Category:** {pattern_data.get('category', 'general')}")
        md_content.append("\n## Pattern\n")
        md_content.append("```")
        md_content.append(pattern_data.get("content", ""))
        md_content.append("```")
        with open(output_path, 'w') as f:
            f.write('\n'.join(md_content))
        return output_path

def export_pattern_to_file(pattern_data: Dict[str, Any], output_path: str, format: str = "json") -> str:
    exporter = PatternExporter()
    if format == "json":
        return exporter.export_to_json(pattern_data, output_path)
    elif format == "xml":
        return exporter.export_to_xml(pattern_data, output_path)
    elif format == "yaml":
        return exporter.export_to_yaml(pattern_data, output_path)
    elif format == "markdown":
        return exporter.export_to_markdown(pattern_data, output_path)
