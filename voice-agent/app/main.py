import asyncio

from infra.audio.recorder import AudioRecorder
from core.services.vad_service import VADService
from infra.audio.buffer import AudioBuffer

from infra.stt.whisper_stt import WhisperSTT
from core.services.stt_service import STTService

from infra.llm.ollama_llm import OllamaLLM
from core.services.translation_service import TranslationService

from infra.tts.edge_tts import EdgeTTS
from core.services.tts_service import TTSService

from core.agent.voice_agent import VoiceAgent
from core.pipeline.streaming_pipeline import StreamingPipeline


async def main():
    # audio
    recorder = AudioRecorder()
    vad = VADService()
    buffer = AudioBuffer()

    # stt
    stt_engine = WhisperSTT("small")
    stt_service = STTService(stt_engine)

    # llm
    llm = OllamaLLM()
    translator = TranslationService(llm)
    translator.set_target_language("Spanish")

    # tts
    tts_engine = EdgeTTS("es-ES-ElviraNeural")
    tts_service = TTSService(tts_engine)

    # agent
    agent = VoiceAgent(stt_service, translator, tts_service)

    # pipeline
    pipeline = StreamingPipeline(
        recorder, vad, buffer, agent, tts_service
    )

    recorder.start()

    print("🎤 AI Assistant Ready... Speak now")

    await pipeline.run()


if __name__ == "__main__":
    asyncio.run(main())