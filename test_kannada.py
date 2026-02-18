import whisper

print("Loading Whisper model...")
model = whisper.load_model("small")

print("Transcribing with Kannada settings...")
result = model.transcribe(
    "data/extracted_audio.wav",  # Direct path instead of AUDIO_PATH
    language='kn',
    task='transcribe',
    word_timestamps=True,
    verbose=False,
    initial_prompt="ಈ ವೀಡಿಯೋ ಕನ್ನಡದಲ್ಲಿದೆ"
)

print("\n" + "="*60)
print("TRANSCRIPTION RESULT:")
print("="*60)
print(f"Detected language: {result['language']}")
print(f"\nFirst segment text:")
print(result['segments'][0]['text'])
print("\nFull text preview (first 200 chars):")
print(result['text'][:200])
print("="*60)

# Check if contains Kannada Unicode
has_kannada = any('\u0c80' <= char <= '\u0cff' for char in result['text'])
print(f"\nContains Kannada script: {has_kannada}")

if not has_kannada:
    print("\nWARNING: Text appears to be in English/Latin script!")
    print("This means Whisper is translating instead of transcribing.")
else:
    print("\nSUCCESS: Proper Kannada script detected!")