import json
import os
import asyncio
import edge_tts
from pydub import AudioSegment
import time

print("="*70)
print("DAY 3: TEXT-TO-SPEECH (MICROSOFT EDGE TTS)")
print("="*70)

# Configuration
HINDI_TRANSCRIPT_PATH = "data/transcript_hindi.json"
HINDI_AUDIO_PATH = "data/hindi_audio_full.mp3"
SEGMENTS_FOLDER = "data/hindi_segments"
VOICE = "hi-IN-SwaraNeural"  # Female voice (change to hi-IN-MadhurNeural for male)

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

print(f"\nUsing voice: {VOICE}")
print("Generating Hindi audio with Microsoft Edge TTS...")
print("(This will take 5-8 minutes)")

# Async function to generate audio for one segment
async def generate_segment_audio(segment_id, text):
    try:
        segment_file = os.path.join(SEGMENTS_FOLDER, f"segment_{segment_id:03d}.mp3")
        
        # Skip if failed translation
        if text.startswith('[Translation failed'):
            return None
        
        # Generate audio
        communicate = edge_tts.Communicate(text, VOICE)
        await communicate.save(segment_file)
        
        return segment_file
        
    except Exception as e:
        print(f"\n⚠ Segment {segment_id} error: {str(e)[:50]}")
        return None

# Generate all segments
async def generate_all_segments():
    segment_audio_files = []
    failed_segments = []
    
    for i, segment in enumerate(hindi_data['segments']):
        # Progress
        if (i + 1) % 10 == 0 or i == 0:
            print(f"  Progress: {i+1}/{hindi_data['total_segments']}")
        
        hindi_text = segment['hindi_text']
        
        # Generate audio
        audio_file = await generate_segment_audio(i, hindi_text)
        
        if audio_file:
            segment_audio_files.append({
                'id': i,
                'file': audio_file,
                'text': hindi_text,
                'start': segment['start'],
                'end': segment['end']
            })
        else:
            failed_segments.append(i)
    
    return segment_audio_files, failed_segments

# Run async generation
print("\nGenerating audio segments...")
segment_audio_files, failed_segments = asyncio.run(generate_all_segments())

# Summary
successful = len(segment_audio_files)
print(f"\n✓ Audio generated: {successful}/{hindi_data['total_segments']} segments")
if failed_segments:
    print(f"⚠ Failed segments: {len(failed_segments)}")

# Combine all segments
print("\nCombining segments into single audio file...")

try:
    combined_audio = AudioSegment.silent(duration=0)
    
    for seg_info in segment_audio_files:
        # Load segment
        segment_audio = AudioSegment.from_mp3(seg_info['file'])
        
        # Add to combined
        combined_audio += segment_audio
        
        # Add small pause (200ms)
        combined_audio += AudioSegment.silent(duration=200)
    
    # Export
    print(f"✓ Exporting to {HINDI_AUDIO_PATH}...")
    combined_audio.export(HINDI_AUDIO_PATH, format="mp3", bitrate="128k")
    
    # Duration
    duration_seconds = len(combined_audio) / 1000
    duration_minutes = duration_seconds / 60
    
    print(f"✓ Combined audio saved!")
    print(f"  Duration: {duration_minutes:.2f} minutes ({duration_seconds:.1f} seconds)")
    
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

# Save metadata
metadata = {
    "source_transcript": HINDI_TRANSCRIPT_PATH,
    "output_audio": HINDI_AUDIO_PATH,
    "tts_method": "Microsoft Edge TTS",
    "voice": VOICE,
    "language": "hi-IN",
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
print("✅ DAY 3 COMPLETE - EDGE TTS!")
print("="*70)
print(f"Hindi audio: {HINDI_AUDIO_PATH}")
print(f"Voice: {VOICE}")
print(f"Segments: {successful}/{hindi_data['total_segments']}")
print(f"Duration: {duration_minutes:.2f} minutes")
print(f"Quality: High (Edge TTS)")
print(f"Cost: $0.00 (FREE!)")
print(f"\nNext steps:")
print(f"  1. Play: start {HINDI_AUDIO_PATH}")
print(f"  2. Commit: git add . && git commit -m 'Day 3: Edge TTS'")
print(f"  3. Move to Day 4: Lip Sync")
print("="*70)