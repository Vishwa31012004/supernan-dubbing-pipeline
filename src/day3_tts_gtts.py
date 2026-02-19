import json
import os
from gtts import gTTS
from pydub import AudioSegment
import time

print("="*70)
print("DAY 3: TEXT-TO-SPEECH (HINDI AUDIO GENERATION)")
print("="*70)

# Configuration
HINDI_TRANSCRIPT_PATH = "data/transcript_hindi.json"
HINDI_AUDIO_PATH = "data/hindi_audio_full.mp3"
SEGMENTS_FOLDER = "data/hindi_segments"

# Create segments folder
os.makedirs(SEGMENTS_FOLDER, exist_ok=True)

# Load Hindi transcript
print(f"\nLoading Hindi transcript from {HINDI_TRANSCRIPT_PATH}...")
try:
    with open(HINDI_TRANSCRIPT_PATH, 'r', encoding='utf-8') as f:
        hindi_data = json.load(f)
    print(f"✓ Loaded {hindi_data['total_segments']} segments")
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

# Generate audio for each segment
print("\nGenerating Hindi audio for each segment...")
print("(This will take 5-10 minutes)")
print("Method: Google TTS (gTTS) - FREE")

segment_audio_files = []
failed_segments = []

for i, segment in enumerate(hindi_data['segments']):
    # Progress
    if (i + 1) % 10 == 0 or i == 0:
        print(f"  Progress: {i+1}/{hindi_data['total_segments']}")
    
    try:
        hindi_text = segment['hindi_text']
        
        # Skip failed translations
        if hindi_text.startswith('[Translation failed'):
            print(f"\n⚠ Segment {i}: Skipping failed translation")
            failed_segments.append(i)
            continue
        
        # Generate audio with gTTS
        tts = gTTS(text=hindi_text, lang='hi', slow=False)
        
        # Save segment audio
        segment_file = os.path.join(SEGMENTS_FOLDER, f"segment_{i:03d}.mp3")
        tts.save(segment_file)
        
        # Store info
        segment_audio_files.append({
            'id': i,
            'file': segment_file,
            'text': hindi_text,
            'start': segment['start'],
            'end': segment['end']
        })
        
        # Small delay to avoid rate limiting
        time.sleep(0.2)
        
    except Exception as e:
        print(f"\n⚠ Segment {i} error: {str(e)[:50]}")
        failed_segments.append(i)
        time.sleep(1)

# Summary
successful = len(segment_audio_files)
print(f"\n✓ Audio generated: {successful}/{hindi_data['total_segments']} segments")
if failed_segments:
    print(f"⚠ Failed segments: {len(failed_segments)}")

# Combine all segments into one audio file
print("\nCombining all segments into single audio file...")

try:
    # Create silence for gaps
    combined_audio = AudioSegment.silent(duration=0)
    
    for seg_info in segment_audio_files:
        # Load segment audio
        segment_audio = AudioSegment.from_mp3(seg_info['file'])
        
        # Add segment
        combined_audio += segment_audio
        
        # Add small pause between segments (250ms)
        combined_audio += AudioSegment.silent(duration=250)
    
    # Export combined audio
    print(f"✓ Exporting to {HINDI_AUDIO_PATH}...")
    combined_audio.export(HINDI_AUDIO_PATH, format="mp3")
    
    # Get duration
    duration_seconds = len(combined_audio) / 1000
    duration_minutes = duration_seconds / 60
    
    print(f"✓ Combined audio saved!")
    print(f"  Duration: {duration_minutes:.2f} minutes ({duration_seconds:.1f} seconds)")
    
except Exception as e:
    print(f"❌ Error combining audio: {e}")
    exit(1)

# Save metadata
metadata = {
    "source_transcript": HINDI_TRANSCRIPT_PATH,
    "output_audio": HINDI_AUDIO_PATH,
    "tts_method": "gTTS (Google Text-to-Speech)",
    "language": "hi",
    "total_segments": len(segment_audio_files),
    "failed_segments": failed_segments,
    "duration_seconds": duration_seconds,
    "segments": segment_audio_files
}

metadata_file = "data/hindi_audio_metadata.json"
with open(metadata_file, 'w', encoding='utf-8') as f:
    json.dump(metadata, f, indent=2, ensure_ascii=False)

print(f"✓ Metadata saved: {metadata_file}")

# Final summary
print("\n" + "="*70)
print("✅ DAY 3 COMPLETE!")
print("="*70)
print(f"Hindi audio generated: {HINDI_AUDIO_PATH}")
print(f"Total segments: {successful}/{hindi_data['total_segments']}")
print(f"Duration: {duration_minutes:.2f} minutes")
print(f"Cost: $0.00 (FREE!)")
print(f"\nSegment files saved in: {SEGMENTS_FOLDER}/")
print(f"\nNext steps:")
print(f"  1. Play audio: {HINDI_AUDIO_PATH}")
print(f"  2. Commit: git add . && git commit -m 'Day 3 complete'")
print(f"  3. Move to Day 4: Lip Sync")
print("="*70)