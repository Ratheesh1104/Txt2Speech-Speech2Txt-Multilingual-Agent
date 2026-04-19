class AudioBuffer:
    def __init__(self):
        self.buffer = []

    def add(self, chunk):
        self.buffer.append(chunk)

    def clear(self):
        self.buffer = []

    def has_data(self):
        return len(self.buffer) > 0

    def get_audio(self):
        audio = b"".join(self.buffer)
        self.clear()
        return audio