import sounddevice as sd
import queue
from collections import deque

class AudioRecorder:
    def __init__(self, sample_rate=16000, frame_duration_ms=30):
        self.sample_rate = sample_rate
        self.frame_size = int(sample_rate * frame_duration_ms / 1000)

        self.q = queue.Queue()
        self.buffer = b""

        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            dtype="int16",
            callback=self.callback
        )

    def callback(self, indata, frames, time, status):
        self.buffer += indata.tobytes()

        while len(self.buffer) >= self.frame_size * 2:
            frame = self.buffer[:self.frame_size * 2]
            self.buffer = self.buffer[self.frame_size * 2:]
            self.q.put(frame)

    def start(self):
        self.stream.start()

    def read_chunk(self):
        return self.q.get()