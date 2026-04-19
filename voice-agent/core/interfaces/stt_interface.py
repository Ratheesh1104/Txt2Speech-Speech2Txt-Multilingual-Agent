from abc import ABC, abstractmethod

class STTInterface(ABC):
    @abstractmethod
    async def transcribe(self, audio_bytes: bytes) -> str:
        pass