import webrtcvad

class VADService:
    def __init__(self, aggressiveness=1):  
        self.vad = webrtcvad.Vad(aggressiveness)

    def is_speech(self, chunk, sample_rate=16000):
        try:
            result = self.vad.is_speech(chunk, sample_rate)
            return result
        except Exception as e:
            print("VAD error:", e)
            return False