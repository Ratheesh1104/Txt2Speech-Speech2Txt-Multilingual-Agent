import sys
from pathlib import Path

_root = Path(__file__).resolve().parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

import asyncio

from infra.tts.edge_tts import EdgeTTS
from core.services.tts_service import TTSService


async def main():
    tts_engine = EdgeTTS(voice="en-US-AriaNeural")
    tts = TTSService(tts_engine)

    await tts.speak("Hello, this is your AI assistant speaking.")


asyncio.run(main())
