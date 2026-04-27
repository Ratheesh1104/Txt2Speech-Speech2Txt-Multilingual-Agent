import edge_tts
import asyncio
import sounddevice as sd
import numpy as np
import tempfile
from pydub import AudioSegment


class EdgeTTS:
    def __init__(self, voice="en-US-AriaNeural"):
        self.voice = voice

    async def synthesize(self, text: str):
        # create temp mp3 file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")

        # generate speech (edge-tts always outputs mp3)
        communicate = edge_tts.Communicate(text=text, voice=self.voice)
        await communicate.save(temp_file.name)

        # load mp3 properly
        audio = AudioSegment.from_file(temp_file.name, format="mp3")

        # convert to numpy array
        samples = np.array(audio.get_array_of_samples())

        # handle stereo audio
        if audio.channels == 2:
            samples = samples.reshape((-1, 2))

        # play audio
        sd.play(samples, samplerate=audio.frame_rate)
        sd.wait()