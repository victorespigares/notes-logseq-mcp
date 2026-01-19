from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class BaseModelClient(ABC):
    @abstractmethod
    async def generate(self, prompt: str, **kwargs) -> str:
        pass
    
    @abstractmethod
    async def summarize(self, content: str, max_length: Optional[int] = None) -> str:
        pass
    
    @abstractmethod
    async def extract_info(self, content: str, query: str) -> str:
        pass
