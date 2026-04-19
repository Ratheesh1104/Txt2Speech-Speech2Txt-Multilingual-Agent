from faster_whisper import WhisperModel
import tempfile
import wave
import os
import asyncio

class WhisperSTT:
    def __init__(self,model_size="base"):
        self.model = WhisperModel(model_size, device="cpu", compute_type="int8", cpu_threads=2)

    def _save_wav(self, audio_bytes):
        temp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")

        with wave.open(temp.name, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(16000)
            wf.writeframes(audio_bytes)
        return temp.name

    async def transcribe(self, audio_bytes) -> str:
        wav_path = self._save_wav(audio_bytes)

        segments, _ = self.model.transcribe(
            wav_path,
            best_of=1,
            vad_filter=True,
        )

        text = " ".join([segment.text for segment in segments])
        os.remove(wav_path)
        return text
