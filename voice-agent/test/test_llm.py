import asyncio

import sys
from pathlib import Path

_root = Path(__file__).resolve().parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from infra.llm.ollama_llm import OllamaLLM
from core.services.translation_service import TranslationService


async def main():
    llm = OllamaLLM()
    translator = TranslationService(llm)

    translator.set_target_language("Spanish")

    text = " I’m currently looking into what’s going on and coordinating with tech team members to fix everything quickly so we can get everything back to normal without any more disruptions."

    result = await translator.translate(text)

    print("📝 Input:", text)
    print("🌍 Output:", result)


asyncio.run(main())