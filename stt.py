import whisper
import sounddevice as sd
from scipy.io.wavfile import write

# Settings
SAMPLE_RATE = 16000
DURATION = 5

print("Loading Whisper model...")
model = whisper.load_model("base")

print("\n🎙️ Speak now...")
audio = sd.rec(
    int(DURATION * SAMPLE_RATE),
    samplerate=SAMPLE_RATE,
    channels=1,
    dtype="int16"
)

sd.wait()
write("audio.wav", SAMPLE_RATE, audio)

print("✅ Recording completed!")
print("🤖 Converting speech to text...")

result = model.transcribe("audio.wav")

text = result["text"].strip()

print("\n📝 Customer said:")
print(text)