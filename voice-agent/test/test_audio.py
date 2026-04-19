import sys
from pathlib import Path
_root = Path(__file__).resolve().parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))
from core.services.vad_service import VADService
from infra.audio.buffer import AudioBuffer
from infra.audio.recorder import AudioRecorder

recorder = AudioRecorder()
vad = VADService()
buffer = AudioBuffer()

recorder.start()

print("🎤 Listening... Speak now")

while True:
    chunk = recorder.read_chunk()
    print("Frame size:", len(chunk)) 

    if vad.is_speech(chunk):
        print("🟢 Speech detected")
        buffer.add(chunk)
    else:
        if buffer.has_data():
            print("🔴 Silence detected → sending chunk")
            audio_data = buffer.get_audio()
            print(f"Captured audio size: {len(audio_data)} bytes\n")