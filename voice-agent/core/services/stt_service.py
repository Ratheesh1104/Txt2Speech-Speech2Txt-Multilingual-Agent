from core.interfaces.stt_interface import STTInterface

class STTService:
    def __init__(self, stt_engine: STTInterface):
        self.stt_engine = stt_engine

    async def process(self, audio_bytes: bytes) -> str:
        if not audio_bytes:
            return ""

        text = await self.stt_engine.transcribe(audio_bytes)
        return text