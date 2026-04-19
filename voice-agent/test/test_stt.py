import sys
from pathlib import Path

_root = Path(__file__).resolve().parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))


import asyncio

from infra.audio.recorder import AudioRecorder
from core.services.vad_service import VADService
from infra.audio.buffer import AudioBuffer

from infra.stt.whisper_stt import WhisperSTT
from core.services.stt_service import STTService


async def main():
    recorder = AudioRecorder()
    vad = VADService()
    buffer = AudioBuffer()

    stt_engine = WhisperSTT(model_size="small")
    stt_service = STTService(stt_engine)

    recorder.start()

    print("🎤 Speak (Tamil/Hindi/English)...")

    while True:
        chunk = recorder.read_chunk()

        if vad.is_speech(chunk):
            buffer.add(chunk)
        else:
            if buffer.has_data():
                print("🔄 Processing speech...")

                audio_data = buffer.get_audio()

                text = await stt_service.process(audio_data)

                if text:
                    print(f"📝 Transcription: {text}\n")
                else:
                    print("⚠️ No speech detected\n")


if __name__ == "__main__":
    asyncio.run(main())