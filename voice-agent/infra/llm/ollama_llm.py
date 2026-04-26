import requests
import json

class OllamaLLM:
    def __init__(self, model="qwen2.5:1.5b"):
        self.model = model
        self.url = "http://localhost:11434/api/generate"

    async def generate(self, prompt: str) -> str:
        response = requests.post(
            self.url,
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
        )

        result = response.json()
        return result.get("response", "").strip()