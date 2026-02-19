import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

load_dotenv()

api_key = os.getenv('ELEVENLABS_API_KEY')

if not api_key:
    print("❌ API key not found!")
    exit(1)

print(f"✓ API key loaded: {api_key[:15]}...")

try:
    print("\nTesting ElevenLabs with Hindi...")
    
    client = ElevenLabs(api_key=api_key)
    
    # Correct method: text_to_speech.convert
    audio = client.text_to_speech.convert(
        text="नमस्ते, यह एक परीक्षण है।",
        voice_id="21m00Tcm4TlvDq8ikWAM",  # Rachel
        model_id="eleven_multilingual_v2"
    )
    
    # Save audio
    with open("test_hindi.mp3", "wb") as f:
        for chunk in audio:
            f.write(chunk)
    
    print("✅ SUCCESS! ElevenLabs is working!")
    print("Test audio saved: test_hindi.mp3")
    print("\nPlay it: start test_hindi.mp3")
    
except Exception as e:
    print(f"❌ Error: {e}")