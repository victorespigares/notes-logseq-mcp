from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
from ..utils.file_utils import write_markdown_file, read_markdown_file
from ..utils.logseq_parser import LogseqParser


class LogseqTools:
    def __init__(self, logseq_path: Path):
        self.logseq_path = logseq_path
        self.pages_path = logseq_path / "pages"
        self.journals_path = logseq_path / "journals"
        
        self.pages_path.mkdir(parents=True, exist_ok=True)
        self.journals_path.mkdir(parents=True, exist_ok=True)
    
    def create_page(self, title: str, content: str, overwrite: bool = False) -> Dict[str, Any]:
        if not self.logseq_path.exists():
            raise FileNotFoundError(f"Logseq directory not found: {self.logseq_path}")
        
        safe_title = self._sanitize_filename(title)
        page_path = self.pages_path / f"{safe_title}.md"
        
        if page_path.exists() and not overwrite:
            existing_content = read_markdown_file(page_path)
            content = f"{existing_content}\n\n---\n\n{content}"
        
        write_markdown_file(page_path, content)
        
        return {
            'title': title,
            'path': str(page_path),
            'created': datetime.now().isoformat(),
            'overwritten': overwrite
        }
    
    def update_page(self, title: str, content: str, append: bool = True) -> Dict[str, Any]:
        safe_title = self._sanitize_filename(title)
        page_path = self.pages_path / f"{safe_title}.md"
        
        if not page_path.exists():
            return self.create_page(title, content)
        
        if append:
            existing_content = read_markdown_file(page_path)
            content = f"{existing_content}\n\n{content}"
        
        write_markdown_file(page_path, content)
        
        return {
            'title': title,
            'path': str(page_path),
            'updated': datetime.now().isoformat(),
            'appended': append
        }
    
    def create_journal_entry(self, content: str, date: Optional[str] = None) -> Dict[str, Any]:
        if date is None:
            date = datetime.now().strftime("%Y_%m_%d")
        
        journal_path = self.journals_path / f"{date}.md"
        
        if journal_path.exists():
            existing_content = read_markdown_file(journal_path)
            content = f"{existing_content}\n\n{content}"
        
        write_markdown_file(journal_path, content)
        
        return {
            'date': date,
            'path': str(journal_path),
            'created': datetime.now().isoformat()
        }
    
    def get_page_context(self, title: str) -> Optional[Dict[str, Any]]:
        """
        Get context about an existing Logseq page.
        Returns structure, properties, and formatting information.
        """
        safe_title = self._sanitize_filename(title)
        page_path = self.pages_path / f"{safe_title}.md"
        
        if not page_path.exists():
            return None
        
        content = read_markdown_file(page_path)
        analysis = LogseqParser.analyze_page_structure(content)
        
        return {
            'title': title,
            'path': str(page_path),
            'exists': True,
            'analysis': analysis,
            'content': content
        }
    
    def find_template(self, template_name: str) -> Optional[Dict[str, Any]]:
        """
        Find and analyze a template by name.
        Returns template structure and properties.
        """
        templates = LogseqParser.find_templates(self.logseq_path)
        
        # Try exact match first
        if template_name in templates:
            template_path = templates[template_name]
            content = read_markdown_file(template_path)
            structure = LogseqParser.extract_template_structure(content)
            return {
                'name': template_name,
                'path': str(template_path),
                'structure': structure
            }
        
        # Try case-insensitive match
        for name, path in templates.items():
            if name.lower() == template_name.lower():
                content = read_markdown_file(path)
                structure = LogseqParser.extract_template_structure(content)
                return {
                    'name': name,
                    'path': str(path),
                    'structure': structure
                }
        
        return None
    
    def list_available_templates(self) -> List[str]:
        """
        List all available templates in Logseq.
        """
        templates = LogseqParser.find_templates(self.logseq_path)
        return list(templates.keys())
    
    def create_page_with_context(self, 
                                  title: str, 
                                  content: str, 
                                  template_name: Optional[str] = None,
                                  preserve_structure: bool = True,
                                  overwrite: bool = False) -> Dict[str, Any]:
        """
        Intelligently create or update a Logseq page.
        
        Args:
            title: Page title
            content: Content to add (will be formatted as Logseq outline)
            template_name: Optional template to use for new pages
            preserve_structure: If updating, preserve existing structure
            overwrite: If True, replace entire page
        """
        safe_title = self._sanitize_filename(title)
        page_path = self.pages_path / f"{safe_title}.md"
        
        # Check if page exists
        page_exists = page_path.exists()
        
        if page_exists and not overwrite:
            # Update existing page preserving structure
            if preserve_structure:
                existing_content = read_markdown_file(page_path)
                existing_analysis = LogseqParser.analyze_page_structure(existing_content)
                
                # Format new content as outline
                formatted_content = self._format_content_as_outline(content)
                
                # Append to existing content
                final_content = f"{existing_content}\n\n{formatted_content}"
            else:
                # Simple append
                existing_content = read_markdown_file(page_path)
                final_content = f"{existing_content}\n\n{content}"
        
        elif template_name:
            # Use template for new page
            template_info = self.find_template(template_name)
            if template_info:
                template_structure = template_info['structure']
                final_content = LogseqParser.merge_with_template(template_structure, content)
            else:
                # Template not found, use default formatting
                final_content = self._format_content_as_outline(content)
        
        else:
            # New page without template
            final_content = self._format_content_as_outline(content)
        
        write_markdown_file(page_path, final_content)
        
        return {
            'title': title,
            'path': str(page_path),
            'created': datetime.now().isoformat(),
            'was_existing': page_exists,
            'used_template': template_name,
            'overwritten': overwrite
        }
    
    def _format_content_as_outline(self, content: str) -> str:
        """
        Format content as Logseq outline structure.
        Converts plain text or markdown to bullet points.
        """
        lines = content.split('\n')
        formatted_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                formatted_lines.append('')
                continue
            
            # Keep headers as-is
            if line.startswith('#'):
                formatted_lines.append(line)
            # Keep existing bullets
            elif line.startswith('-') or line.startswith('*'):
                formatted_lines.append(line)
            # Convert to bullet
            else:
                formatted_lines.append(f"- {line}")
        
        return '\n'.join(formatted_lines)
    
    def _sanitize_filename(self, filename: str) -> str:
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        
        filename = filename.strip()
        
        return filename
