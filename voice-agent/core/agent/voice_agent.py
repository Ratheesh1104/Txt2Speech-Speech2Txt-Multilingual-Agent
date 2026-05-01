class VoiceAgent:
    def __init__(self, stt, translator, tts):
        self.stt = stt
        self.translator = translator
        self.tts = tts

    async def process_audio(self, audio_bytes):
        text = await self.stt.process(audio_bytes)

        if not text:
            return ""

        translated =    await self.translator.translate(text)

        return translated