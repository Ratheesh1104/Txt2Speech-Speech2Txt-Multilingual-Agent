import sounddevice as sd
import queue

class AudioRecorder:
    def __init__(self, sample_rate=16000, frame_duration_ms=30):
        self.sample_rate = sample_rate
        self.frame_size = int(sample_rate * frame_duration_ms / 1000)  # 480 samples
        self.frame_bytes = self.frame_size * 2  # int16 = 2 bytes

        self.q = queue.Queue()

        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            dtype="int16",
            callback=self.callback
        )

        self.buffer = b""

    def callback(self, indata, frames, time, status):
        if status:
            print("⚠️ Audio status:", status)

        self.buffer += indata.tobytes()

        # Split into valid frames
        while len(self.buffer) >= self.frame_bytes:
            frame = self.buffer[:self.frame_bytes]
            self.buffer = self.buffer[self.frame_bytes:]
            self.q.put(frame)

    def start(self):
        self.stream.start()

    def read_chunk(self):
        return self.q.get()