import json
import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from pydub import AudioSegment
import time

load_dotenv()

print("="*70)
print("DAY 3: TEXT-TO-SPEECH (ELEVENLABS - ULTRA NATURAL)")
print("="*70)

# Configuration
HINDI_TRANSCRIPT_PATH = "data/transcript_hindi.json"
HINDI_AUDIO_PATH = "data/hindi_audio_full.mp3"
SEGMENTS_FOLDER = "data/hindi_segments"

# Voice IDs (Rachel - warm female voice)
VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # Rachel
# Other options:
# "EXAVITQu4vr4xnSDxMaL" = Bella (calm female)
# "pNInz6obpgDQGcFmaJgB" = Adam (deep male)
# "ErXwobaYiN019PkySvjV" = Antoni (friendly male)

# Check API key
api_key = os.getenv('ELEVENLABS_API_KEY')
if not api_key:
    print("\n❌ ERROR: ELEVENLABS_API_KEY not found in .env!")
    exit(1)

print("✓ API key loaded")

# Create folders
os.makedirs(SEGMENTS_FOLDER, exist_ok=True)

# Initialize client
client = ElevenLabs(api_key=api_key)
print("✓ ElevenLabs client initialized")

# Load transcript
print(f"\nLoading Hindi transcript from {HINDI_TRANSCRIPT_PATH}...")
try:
    with open(HINDI_TRANSCRIPT_PATH, 'r', encoding='utf-8') as f:
        hindi_data = json.load(f)
    print(f"✓ Loaded {hindi_data['total_segments']} segments")
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

print(f"\nVoice: Rachel (Ultra natural, warm)")
print("Generating Hindi audio with ElevenLabs...")
print("(This will take 8-12 minutes)")
print("Cost: FREE (within 10k char limit)")

# Generate segments
segment_audio_files = []
failed_segments = []
total_chars = 0

for i, segment in enumerate(hindi_data['segments']):
    # Progress
    if (i + 1) % 10 == 0 or i == 0:
        print(f"  Progress: {i+1}/{hindi_data['total_segments']}")
    
    try:
        hindi_text = segment['hindi_text']
        
        # Skip failed translations
        if hindi_text.startswith('[Translation failed'):
            failed_segments.append(i)
            continue
        
        # Track characters
        total_chars += len(hindi_text)
        
        # Generate audio
        audio_generator = client.text_to_speech.convert(
            text=hindi_text,
            voice_id=VOICE_ID,
            model_id="eleven_multilingual_v2"
        )
        
        # Save segment
        segment_file = os.path.join(SEGMENTS_FOLDER, f"segment_{i:03d}.mp3")
        with open(segment_file, "wb") as f:
            for chunk in audio_generator:
                f.write(chunk)
        
        segment_audio_files.append({
            'id': i,
            'file': segment_file,
            'text': hindi_text,
            'start': segment['start'],
            'end': segment['end']
        })
        
        # Small delay
        time.sleep(0.3)
        
    except Exception as e:
        print(f"\n⚠ Segment {i} error: {str(e)[:60]}")
        failed_segments.append(i)
        time.sleep(1)

# Character usage
print(f"\n✓ Total characters used: {total_chars:,}")
print(f"✓ Audio generated: {len(segment_audio_files)}/{hindi_data['total_segments']}")
if failed_segments:
    print(f"⚠ Failed: {len(failed_segments)}")

# Combine segments
print("\nCombining segments into single audio file...")

try:
    combined_audio = AudioSegment.silent(duration=0)
    
    for seg_info in segment_audio_files:
        segment_audio = AudioSegment.from_mp3(seg_info['file'])
        combined_audio += segment_audio
        combined_audio += AudioSegment.silent(duration=200)
    
    # Export
    print(f"✓ Exporting to {HINDI_AUDIO_PATH}...")
    combined_audio.export(HINDI_AUDIO_PATH, format="mp3", bitrate="192k")
    
    duration_seconds = len(combined_audio) / 1000
    duration_minutes = duration_seconds / 60
    
    print(f"✓ Combined audio saved!")
    print(f"  Duration: {duration_minutes:.2f} minutes ({duration_seconds:.1f}s)")
    
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

# Metadata
metadata = {
    "source_transcript": HINDI_TRANSCRIPT_PATH,
    "output_audio": HINDI_AUDIO_PATH,
    "tts_method": "ElevenLabs (Ultra Natural)",
    "voice": "Rachel",
    "voice_id": VOICE_ID,
    "model": "eleven_multilingual_v2",
    "language": "hi",
    "total_segments": len(segment_audio_files),
    "failed_segments": failed_segments,
    "duration_seconds": duration_seconds,
    "characters_used": total_chars,
    "segments": segment_audio_files
}

with open("data/hindi_audio_metadata.json", 'w', encoding='utf-8') as f:
    json.dump(metadata, f, indent=2, ensure_ascii=False)

# Summary
print("\n" + "="*70)
print("✅ DAY 3 COMPLETE - ELEVENLABS ULTRA NATURAL!")
print("="*70)
print(f"Hindi audio: {HINDI_AUDIO_PATH}")
print(f"Voice: Rachel (Human-like quality)")
print(f"Segments: {len(segment_audio_files)}/{hindi_data['total_segments']}")
print(f"Duration: {duration_minutes:.2f} minutes")
print(f"Characters: {total_chars:,} (FREE tier limit: 10,000)")
print(f"Quality: ⭐⭐⭐⭐⭐ Ultra Natural")
print(f"\nThis sounds like a REAL PERSON talking!")
print(f"\nNext steps:")
print(f"  1. Play: start {HINDI_AUDIO_PATH}")
print(f"  2. Commit: git add . && git commit -m 'Day 3: ElevenLabs'")
print(f"  3. Move to Day 4: Lip Sync")
print("="*70)