from abc import ABC, abstractmethod
from typing import Optional
import os
import httpx

class LLMProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        pass

class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        
    def generate(self, prompt: str, **kwargs) -> str:
        # Mock logic
        return f"OpenAI generated response for: {prompt[:20]}..."

class OllamaProvider(LLMProvider):
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        
    def generate(self, prompt: str, **kwargs) -> str:
        model = kwargs.get("model", "llama3")
        try:
            # We would usually do:
            # response = httpx.post(f"{self.base_url}/api/generate", json={"model": model, "prompt": prompt, "stream": False})
            # return response.json()["response"]
            return f"Ollama local generated response for: {prompt[:20]}..."
        except Exception as e:
            return f"Error connecting to local Ollama: {str(e)}"

class FireworksProvider(LLMProvider):
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("FIREWORKS_API_KEY")
        self.base_url = "https://api.fireworks.ai/inference/v1/completions"
        
    def generate(self, prompt: str, **kwargs) -> str:
        if not self.api_key:
            return "Error: No Fireworks API Key provided."
        model = kwargs.get("model", "accounts/fireworks/models/llama-v3-8b-instruct")
        # headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        # payload = {"model": model, "prompt": prompt, "max_tokens": 100}
        # response = httpx.post(self.base_url, headers=headers, json=payload)
        # return response.json()["choices"][0]["text"]
        return f"Fireworks generated response for: {prompt[:20]}..."

def get_provider(provider_name: str, **kwargs) -> LLMProvider:
    if provider_name.lower() == "ollama":
        return OllamaProvider(**kwargs)
    elif provider_name.lower() == "fireworks":
        return FireworksProvider(**kwargs)
    return OpenAIProvider(**kwargs)
