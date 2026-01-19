"""
Logseq structure parser and analyzer.
Understands Logseq page structure, properties, templates, and formatting.
"""
from pathlib import Path
from typing import Dict, List, Optional, Any
import re


class LogseqParser:
    """Parse and analyze Logseq page structure."""
    
    @staticmethod
    def parse_properties(content: str) -> Dict[str, Any]:
        """
        Extract properties from Logseq page.
        Properties are in format: property:: value
        """
        properties = {}
        property_pattern = r'^(\w+(?:-\w+)*)::(.+)$'
        
        for line in content.split('\n'):
            line = line.strip()
            match = re.match(property_pattern, line)
            if match:
                key = match.group(1).strip()
                value = match.group(2).strip()
                properties[key] = value
        
        return properties
    
    @staticmethod
    def parse_outline_structure(content: str) -> List[Dict[str, Any]]:
        """
        Parse Logseq outline structure.
        Returns hierarchical structure based on indentation.
        """
        lines = content.split('\n')
        structure = []
        
        for line in lines:
            if not line.strip():
                continue
            
            # Count indentation (tabs or spaces)
            indent_match = re.match(r'^(\t+|- |\s+)', line)
            indent_level = 0
            if indent_match:
                indent_str = indent_match.group(1)
                if '\t' in indent_str:
                    indent_level = indent_str.count('\t')
                elif '- ' in indent_str:
                    indent_level = indent_str.count('- ')
                else:
                    indent_level = len(indent_str) // 2
            
            # Extract bullet content
            bullet_content = line.strip().lstrip('- \t')
            
            structure.append({
                'level': indent_level,
                'content': bullet_content,
                'raw': line
            })
        
        return structure
    
    @staticmethod
    def extract_template_structure(template_content: str) -> Dict[str, Any]:
        """
        Extract structure from a template page.
        Returns properties, sections, and outline structure.
        """
        properties = LogseqParser.parse_properties(template_content)
        outline = LogseqParser.parse_outline_structure(template_content)
        
        # Extract sections (lines starting with ##)
        sections = []
        for line in template_content.split('\n'):
            if line.strip().startswith('##'):
                sections.append(line.strip().lstrip('# '))
        
        return {
            'properties': properties,
            'sections': sections,
            'outline': outline,
            'raw_content': template_content
        }
    
    @staticmethod
    def find_templates(logseq_path: Path) -> Dict[str, Path]:
        """
        Find all template pages in Logseq.
        Templates are usually in pages/ with 'template' property or in templates/ folder.
        """
        templates = {}
        pages_path = logseq_path / "pages"
        templates_path = logseq_path / "templates"
        
        # Check templates folder
        if templates_path.exists():
            for template_file in templates_path.glob("*.md"):
                template_name = template_file.stem
                templates[template_name] = template_file
        
        # Check pages with template property
        if pages_path.exists():
            for page_file in pages_path.glob("*.md"):
                try:
                    content = page_file.read_text(encoding='utf-8')
                    if 'template::' in content.lower() or 'template-name::' in content.lower():
                        template_name = page_file.stem
                        templates[template_name] = page_file
                except Exception:
                    continue
        
        return templates
    
    @staticmethod
    def analyze_page_structure(content: str) -> Dict[str, Any]:
        """
        Comprehensive analysis of a Logseq page structure.
        Returns properties, outline hierarchy, sections, and formatting patterns.
        """
        properties = LogseqParser.parse_properties(content)
        outline = LogseqParser.parse_outline_structure(content)
        
        # Detect formatting patterns
        has_todos = bool(re.search(r'TODO|DOING|DONE|LATER|NOW', content))
        has_tags = bool(re.search(r'#\w+', content))
        has_links = bool(re.search(r'\[\[.*?\]\]', content))
        has_queries = bool(re.search(r'\{\{query', content))
        
        # Extract sections
        sections = []
        current_section = None
        for line in content.split('\n'):
            if line.strip().startswith('##'):
                current_section = line.strip().lstrip('# ')
                sections.append(current_section)
        
        # Analyze indentation style
        indent_style = 'tabs' if '\t' in content else 'spaces'
        
        return {
            'properties': properties,
            'outline': outline,
            'sections': sections,
            'has_todos': has_todos,
            'has_tags': has_tags,
            'has_links': has_links,
            'has_queries': has_queries,
            'indent_style': indent_style,
            'line_count': len(content.split('\n'))
        }
    
    @staticmethod
    def format_as_logseq_outline(items: List[str], indent_level: int = 0) -> str:
        """
        Format a list of items as Logseq outline with proper indentation.
        """
        formatted = []
        indent = '\t' * indent_level
        
        for item in items:
            if isinstance(item, dict):
                # Nested structure
                formatted.append(f"{indent}- {item.get('content', '')}")
                if 'children' in item:
                    formatted.append(LogseqParser.format_as_logseq_outline(
                        item['children'], 
                        indent_level + 1
                    ))
            else:
                formatted.append(f"{indent}- {item}")
        
        return '\n'.join(formatted)
    
    @staticmethod
    def merge_with_template(template_structure: Dict[str, Any], new_content: str) -> str:
        """
        Merge new content with template structure.
        Preserves template properties and structure while adding new content.
        """
        result_lines = []
        
        # Add template properties first
        if template_structure.get('properties'):
            for key, value in template_structure['properties'].items():
                result_lines.append(f"{key}:: {value}")
            result_lines.append("")
        
        # Add template sections with new content
        if template_structure.get('sections'):
            for section in template_structure['sections']:
                result_lines.append(f"## {section}")
                result_lines.append("")
        
        # Add new content as outline
        for line in new_content.split('\n'):
            if line.strip() and not line.strip().startswith('##'):
                if not line.strip().startswith('-'):
                    result_lines.append(f"- {line.strip()}")
                else:
                    result_lines.append(line)
            elif line.strip().startswith('##'):
                result_lines.append(line)
            else:
                result_lines.append(line)
        
        return '\n'.join(result_lines)
