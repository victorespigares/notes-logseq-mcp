import json
import os
from pathlib import Path
from typing import Dict, Any


class Config:
    def __init__(self, config_path: str = "config.json"):
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        config_file = Path(self.config_path)
        if not config_file.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def get_notes_path(self) -> Path:
        path = self.config.get('notes_path', '')
        return Path(os.path.expanduser(path))
    
    def get_logseq_path(self) -> Path:
        path = self.config.get('logseq_path', '')
        return Path(os.path.expanduser(path))
    
    def get_model_config(self, provider: str = None) -> Dict[str, Any]:
        if provider is None:
            provider = self.config['models'].get('default_provider', 'local')
        
        if provider == 'local':
            return self.config['models']['ollama']
        elif provider == 'remote':
            return self.config['models']['remote']
        else:
            raise ValueError(f"Unknown provider: {provider}")
    
    def get_logging_level(self) -> str:
        return self.config.get('logging', {}).get('level', 'INFO')
