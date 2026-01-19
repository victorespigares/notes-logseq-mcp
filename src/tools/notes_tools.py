from pathlib import Path
from typing import List, Dict, Any
from ..utils.file_utils import search_markdown_files, read_markdown_file, get_file_metadata


class NotesTools:
    def __init__(self, notes_path: Path):
        self.notes_path = notes_path
    
    def search_notes(self, query: str, case_sensitive: bool = False, max_results: int = 20) -> List[Dict[str, Any]]:
        if not self.notes_path.exists():
            raise FileNotFoundError(f"Notes directory not found: {self.notes_path}")
        
        results = search_markdown_files(self.notes_path, query, case_sensitive)
        
        return results[:max_results]
    
    def get_note_content(self, relative_path: str) -> Dict[str, Any]:
        file_path = self.notes_path / relative_path
        
        if not file_path.exists():
            raise FileNotFoundError(f"Note not found: {relative_path}")
        
        content = read_markdown_file(file_path)
        metadata = get_file_metadata(file_path)
        
        return {
            'content': content,
            'metadata': metadata
        }
    
    def list_recent_notes(self, limit: int = 10) -> List[Dict[str, Any]]:
        if not self.notes_path.exists():
            raise FileNotFoundError(f"Notes directory not found: {self.notes_path}")
        
        notes = []
        
        for file_path in self.notes_path.rglob('*.md'):
            try:
                metadata = get_file_metadata(file_path)
                metadata['relative_path'] = str(file_path.relative_to(self.notes_path))
                notes.append(metadata)
            except Exception:
                continue
        
        notes.sort(key=lambda x: x['modified'], reverse=True)
        
        return notes[:limit]
