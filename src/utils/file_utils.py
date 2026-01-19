import os
import re
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime


def search_markdown_files(directory: Path, query: str, case_sensitive: bool = False) -> List[Dict[str, Any]]:
    results = []
    
    if not directory.exists():
        return results
    
    pattern = re.compile(query if case_sensitive else query, re.IGNORECASE if not case_sensitive else 0)
    
    for file_path in directory.rglob('*.md'):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                matches = pattern.findall(content)
                
                if matches:
                    lines = content.split('\n')
                    matching_lines = []
                    
                    for i, line in enumerate(lines, 1):
                        if pattern.search(line):
                            matching_lines.append({
                                'line_number': i,
                                'content': line.strip()
                            })
                    
                    results.append({
                        'path': str(file_path),
                        'relative_path': str(file_path.relative_to(directory)),
                        'matches_count': len(matches),
                        'matching_lines': matching_lines[:10],
                        'modified': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                    })
        except Exception as e:
            continue
    
    return sorted(results, key=lambda x: x['matches_count'], reverse=True)


def read_markdown_file(file_path: Path) -> str:
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def write_markdown_file(file_path: Path, content: str) -> None:
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)


def get_file_metadata(file_path: Path) -> Dict[str, Any]:
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    stat = file_path.stat()
    
    return {
        'path': str(file_path),
        'size': stat.st_size,
        'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
        'modified': datetime.fromtimestamp(stat.st_mtime).isoformat()
    }
