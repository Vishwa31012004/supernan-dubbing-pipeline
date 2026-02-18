import os
import json
import time
import subprocess
import whisper

print("="*70)
print("DAY 1: AUDIO EXTRACTION AND TRANSCRIPTION")
print("="*70)

# Configuration
VIDEO_PATH = "data/input_video.mp4"
AUDIO_PATH = "data/extracted_audio.wav"
TRANSCRIPT_PATH = "data/transcript.json"
WHISPER_MODEL = "medium"  # Options: tiny, base, small, medium, large

# Check video exists
if not os.path.exists(VIDEO_PATH):
    print(f"❌ Video not found: {VIDEO_PATH}")
    exit(1)

file_size = os.path.getsize(VIDEO_PATH) / (1024*1024)
print(f"\n✓ Input video: {VIDEO_PATH}")
print(f"✓ Size: {file_size:.1f} MB")

# STEP 1: Extract Audio
print("\n" + "-"*70)
print("STEP 1: Extracting audio from video...")
print("-"*70)

start_time = time.time()

try:
    cmd = [
        'ffmpeg',
        '-i', VIDEO_PATH,
        '-vn',
        '-acodec', 'pcm_s16le',
        '-ar', '16000',
        '-ac', '1',
        '-y',
        AUDIO_PATH
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if os.path.exists(AUDIO_PATH):
        audio_size = os.path.getsize(AUDIO_PATH) / (1024*1024)
        print(f"✓ Audio extracted: {AUDIO_PATH}")
        print(f"✓ Size: {audio_size:.1f} MB")
    else:
        print("❌ Audio extraction failed")
        exit(1)
        
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

extraction_time = time.time() - start_time
print(f"✓ Time: {extraction_time:.1f} seconds")

# STEP 2: Transcribe with Whisper
print("\n" + "-"*70)
print("STEP 2: Transcribing with Whisper...")
print("-"*70)
print(f"Model: {WHISPER_MODEL}")
print("Note: First run downloads model (~460MB)")
print("Processing will take ~15-20 minutes...")

start_time = time.time()

try:
    # Load model
    print("\nLoading Whisper model...")
    model = whisper.load_model(WHISPER_MODEL)
    print("✓ Model loaded")
    
    # Transcribe
    print("\nTranscribing audio...")
    print("(Whisper will auto-detect language and translate to English)")
    
    result = model.transcribe(
        AUDIO_PATH,
        word_timestamps=True,
        verbose=False
    )
    
    print(f"\n✓ Transcription complete!")
    print(f"✓ Language detected: {result['language']}")
    print(f"✓ Total segments: {len(result['segments'])}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

transcription_time = time.time() - start_time
print(f"✓ Time: {transcription_time/60:.1f} minutes")

# STEP 3: Save to JSON
print("\n" + "-"*70)
print("STEP 3: Saving transcript...")
print("-"*70)

try:
    transcript_data = {
        "source_video": VIDEO_PATH,
        "audio_file": AUDIO_PATH,
        "language": result['language'],
        "full_text": result['text'],
        "model_used": WHISPER_MODEL,
        "total_segments": len(result['segments']),
        "segments": []
    }
    
    for segment in result['segments']:
        seg_data = {
            "id": segment['id'],
            "start": segment['start'],
            "end": segment['end'],
            "text": segment['text'].strip(),
            "words": []
        }
        
        if 'words' in segment:
            for word in segment['words']:
                seg_data['words'].append({
                    "word": word['word'],
                    "start": word['start'],
                    "end": word['end']
                })
        
        transcript_data['segments'].append(seg_data)
    
    with open(TRANSCRIPT_PATH, 'w', encoding='utf-8') as f:
        json.dump(transcript_data, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Saved: {TRANSCRIPT_PATH}")
    
    # Preview
    print("\n" + "="*70)
    print("TRANSCRIPT PREVIEW (first 300 characters):")
    print("="*70)
    preview = transcript_data['full_text'][:300]
    print(preview)
    if len(transcript_data['full_text']) > 300:
        print("...")
    print("="*70)
    
except Exception as e:
    print(f"❌ Error saving: {e}")
    exit(1)

# Summary
print("\n" + "="*70)
print("✅ DAY 1 COMPLETE!")
print("="*70)
print(f"\nTotal time: {(extraction_time + transcription_time)/60:.1f} minutes")
print(f"\nFiles created:")
print(f"  1. {AUDIO_PATH} ({audio_size:.1f} MB)")
print(f"  2. {TRANSCRIPT_PATH} ({len(result['segments'])} segments)")
print(f"\nLanguage: {result['language']}")
print(f"Note: Whisper auto-translated to English")
print(f"\nNext: Run Day 2 to translate English → Hindi")
print("="*70)
