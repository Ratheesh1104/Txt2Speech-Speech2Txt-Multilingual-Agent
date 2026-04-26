from core.interfaces.llm_interface import LLMInterface

class TranslationService:
    def __init__(self, llm: LLMInterface):
        self.llm = llm
        self.target_language = "Spanish"  # default

    def set_target_language(self, lang: str):
        self.target_language = lang

    def build_prompt(self, text: str) -> str:
        return f"""
You are a strict translation engine.

Your task:
- ALWAYS translate the input into {self.target_language}
- NEVER return English unless the target language is English
- EVEN IF the input is already in English, you MUST translate it to {self.target_language}

Rules:
1. Detect the source language automatically
2. Convert meaning internally (do NOT output English)
3. Output ONLY the final translation in {self.target_language}
4. Do NOT explain, do NOT include multiple versions
5. Do NOT repeat the input
6. Do NOT output English at any step

Input:
{text}

Output:
(ONLY the translated sentence in {self.target_language})
"""

    async def translate(self, text: str) -> str:
        prompt = self.build_prompt(text)
        response = await self.llm.generate(prompt)
        return response