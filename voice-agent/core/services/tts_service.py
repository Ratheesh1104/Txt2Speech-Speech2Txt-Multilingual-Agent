from core.interfaces.tts_interface import TTSInterface

class TTSService:
    def __init__(self, tts_engine: TTSInterface):
        self.tts_engine = tts_engine

    async def speak(self, text: str):
        if not text:
            return
        await self.tts_engine.synthesize(text)