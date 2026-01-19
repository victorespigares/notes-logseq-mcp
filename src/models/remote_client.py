import aiohttp
from typing import Dict, Any, Optional
from .base import BaseModelClient


class RemoteClient(BaseModelClient):
    def __init__(self, api_key: str, model: str = "claude-3.5-sonnet", provider: str = "anthropic"):
        self.api_key = api_key
        self.model = model
        self.provider = provider
        
        # Set base URL based on provider
        provider_urls = {
            "anthropic": "https://api.anthropic.com",
            "openai": "https://api.openai.com",
            "perplexity": "https://api.perplexity.ai"
        }
        self.base_url = provider_urls.get(provider, "https://api.anthropic.com")
    
    async def generate(self, prompt: str, **kwargs) -> str:
        url = f"{self.base_url}/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            **kwargs
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"Remote API error ({self.provider}): {response.status} - {error_text}")
                
                result = await response.json()
                return result['choices'][0]['message']['content']
    
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
        url = f"{self.base_url}/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            **kwargs
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"Remote API error ({self.provider}): {response.status} - {error_text}")
                
                result = await response.json()
                return result['choices'][0]['message']['content']
