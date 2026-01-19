import aiohttp
from typing import Dict, Any, Optional
from .base import BaseModelClient


class OllamaClient(BaseModelClient):
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3.1"):
        self.base_url = base_url.rstrip('/')
        self.model = model
    
    async def generate(self, prompt: str, **kwargs) -> str:
        url = f"{self.base_url}/api/generate"
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            **kwargs
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                if response.status != 200:
                    raise Exception(f"Ollama API error: {response.status}")
                
                result = await response.json()
                return result.get('response', '')
    
    async def summarize(self, content: str, max_length: Optional[int] = None) -> str:
        length_instruction = f" in approximately {max_length} words" if max_length else ""
        
        prompt = f"""Summarize the following content clearly and concisely{length_instruction}:

{content}

Summary:"""
        
        return await self.generate(prompt)
    
    async def extract_info(self, content: str, query: str) -> str:
        prompt = f"""Extract relevant information from the following content related to: {query}

Content:
{content}

Extracted information:"""
        
        return await self.generate(prompt)
    
    async def chat(self, messages: list, **kwargs) -> str:
        url = f"{self.base_url}/api/chat"
        
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            **kwargs
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                if response.status != 200:
                    raise Exception(f"Ollama API error: {response.status}")
                
                result = await response.json()
                return result.get('message', {}).get('content', '')
