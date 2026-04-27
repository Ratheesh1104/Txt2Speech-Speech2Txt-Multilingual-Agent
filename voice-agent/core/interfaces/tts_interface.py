from abc import ABC, abstractmethod

class TTSInterface(ABC):
    @abstractmethod
    async def synthesize(self, text: str):
        pass