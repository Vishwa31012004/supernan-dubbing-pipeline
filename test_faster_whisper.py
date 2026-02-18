from faster_whisper import WhisperModel

print("Loading Faster-Whisper model...")
model = WhisperModel("small", device="cpu", compute_type="int8")

print("Transcribing in Kannada...")
segments, info = model.transcribe(
    "data/extracted_audio.wav",
    language="kn",
    task="transcribe",
    word_timestamps=True
)

print(f"\nDetected language: {info.language}")
print(f"Language probability: {info.language_probability:.2f}")

# Get first segment
first_segment = next(segments)
print(f"\nFirst segment text:")
print(first_segment.text)

# Check if Kannada
has_kannada = any('\u0c80' <= char <= '\u0cff' for char in first_segment.text)
print(f"\nContains Kannada script: {has_kannada}")

if has_kannada:
    print("✅ SUCCESS! Kannada script detected!")
else:
    print("❌ Still English/other language")