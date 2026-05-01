import asyncio

class StreamingPipeline:
    def __init__(self, recorder, vad, buffer, agent, tts):
        self.recorder = recorder
        self.vad = vad
        self.buffer = buffer
        self.agent = agent
        self.tts = tts
        self.is_speaking = False

        self.audio_q = asyncio.Queue()
        self.text_q = asyncio.Queue()

    async def audio_worker(self):
        loop = asyncio.get_running_loop()

        silence_count = 0
        SILENCE_THRESHOLD = 8   # tune (higher = more stable)
        MIN_CHUNKS = 12        # minimum speech before sending

        chunk_count = 0

        while True:
            chunk = await loop.run_in_executor(
                None, self.recorder.read_chunk
            )

            if self.is_speaking:
                self.buffer.clear()
                continue

            if self.vad.is_speech(chunk):
                silence_count = 0
                chunk_count += 1
                self.buffer.add(chunk)

            else:
                silence_count += 1

                # ✅ only flush after sustained silence
                if silence_count >= SILENCE_THRESHOLD and self.buffer.has_data():

                    if chunk_count >= MIN_CHUNKS:
                        audio = self.buffer.get_audio()
                        print(f"📦 Sending audio ({len(audio)} bytes)")
                        await self.audio_q.put(audio)
                    else:
                        # discard tiny noise
                        self.buffer.clear()

                    # reset state
                    silence_count = 0
                    chunk_count = 0
        

    async def stt_llm_worker(self):
        print("🔄 Starting STT/LLM worker...")
        while True:
            print("🔄 Waiting for audio...")
            audio = await self.audio_q.get()

            print("🔄 Processing speech...")

            result = await self.agent.process_audio(audio)

            if result:
                await self.text_q.put(result)

    async def tts_worker(self):
        while True:
            text = await self.text_q.get()

            print(f"🗣️ Speaking: {text}")
            self.is_speaking = True
            self.buffer.clear()
            await self.tts.speak(text)
            self.is_speaking = False

    async def run(self):
        await asyncio.gather(
            self.audio_worker(),
            self.stt_llm_worker(),
            self.tts_worker()
        )