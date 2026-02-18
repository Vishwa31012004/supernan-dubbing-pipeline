import os
import json
import time
import whisper
import subprocess

print("=" * 70)
print("DAY 1: AUDIO EXTRACTION AND TRANSCRIPTION")
print("=" * 70)

# Configuration
VIDEO_PATH = "data/input_video.mp4"
AUDIO_PATH = "data/extracted_audio.wav"
TRANSCRIPT_PATH = "data/transcript.json"
WHISPER_MODEL = "medium"  # options: tiny, base, small, medium, large

# Check if video exists
if not os.path.exists(VIDEO_PATH):
    print(f"ERROR: Video not found at {VIDEO_PATH}")
    print("Make sure you downloaded the test video!")
    exit(1)

print(f"\nInput video: {VIDEO_PATH}")
file_size = os.path.getsize(VIDEO_PATH) / (1024*1024)
print(f"File size: {file_size:.1f} MB")

# Step 1: Extract audio from video
print("\n" + "-" * 70)
print("STEP 1: Extracting audio from video...")
print("-" * 70)

start_time = time.time()

try:
    # Using ffmpeg via subprocess
    cmd = [
        'ffmpeg',
        '-i', VIDEO_PATH,
        '-vn',  # no video
        '-acodec', 'pcm_s16le',  # audio codec
        '-ar', '16000',  # sample rate 16kHz (Whisper needs this)
        '-ac', '1',  # mono audio
        '-y',  # overwrite if exists
        AUDIO_PATH
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if os.path.exists(AUDIO_PATH):
        audio_size = os.path.getsize(AUDIO_PATH) / (1024*1024)
        print(f"Audio extracted: {AUDIO_PATH}")
        print(f"Audio size: {audio_size:.1f} MB")
    else:
        print("ERROR: Audio extraction failed")
        exit(1)
        
except Exception as e:
    print(f"ERROR during audio extraction: {e}")
    exit(1)

extraction_time = time.time() - start_time
print(f"Time taken: {extraction_time:.1f} seconds")

# Step 2: Transcribe audio with Whisper
print("\n" + "-" * 70)
print("STEP 2: Transcribing audio with Whisper...")
print("-" * 70)
print(f"Loading Whisper model: {WHISPER_MODEL}")
print("This may take a minute on first run (downloading model)...")

start_time = time.time()

try:
    # Load Whisper model
    model = whisper.load_model(WHISPER_MODEL)
    print("Model loaded successfully!")
    
    print("\nTranscribing... This will take a few minutes...")
    print("(Processing time is roughly equal to video length)")
    
    # Transcribe with word-level timestamps
    result = model.transcribe(
        AUDIO_PATH,
	language='kn',  # Force Kannada (kn = Kannada language code)
	task='transcribe',  
        word_timestamps=True,
        verbose=False, # set to True to see progress
    	initial_prompt="ಈ ವೀಡಿಯೋ ಕನ್ನಡದಲ್ಲಿದೆ"   
    )
    
    print(f"\nTranscription complete!")
    print(f"Detected language: {result['language']}")
    print(f"Number of segments: {len(result['segments'])}")
    
except Exception as e:
    print(f"ERROR during transcription: {e}")
    exit(1)

transcription_time = time.time() - start_time
print(f"Time taken: {transcription_time/60:.1f} minutes")

# Step 3: Save transcript to JSON
print("\n" + "-" * 70)
print("STEP 3: Saving transcript to JSON...")
print("-" * 70)

try:
    # Prepare transcript data
    transcript_data = {
        "source_video": VIDEO_PATH,
        "audio_file": AUDIO_PATH,
        "language": result['language'],
        "full_text": result['text'],
        "model_used": WHISPER_MODEL,
        "total_segments": len(result['segments']),
        "segments": []
    }
    
    # Extract each segment with timestamps
    for segment in result['segments']:
        seg_data = {
            "id": segment['id'],
            "start": segment['start'],
            "end": segment['end'],
            "text": segment['text'].strip(),
            "words": []
        }
        
        # Add word-level timestamps if available
        if 'words' in segment:
            for word in segment['words']:
                seg_data['words'].append({
                    "word": word['word'],
                    "start": word['start'],
                    "end": word['end']
                })
        
        transcript_data['segments'].append(seg_data)
    
    # Save to JSON
    with open(TRANSCRIPT_PATH, 'w', encoding='utf-8') as f:
        json.dump(transcript_data, f, indent=2, ensure_ascii=False)
    
    print(f"Transcript saved: {TRANSCRIPT_PATH}")
    
    # Show preview
    print("\n" + "=" * 70)
    print("TRANSCRIPT PREVIEW (first 500 characters):")
    print("=" * 70)
    preview = transcript_data['full_text'][:500]
    print(preview)
    if len(transcript_data['full_text']) > 500:
        print("...")
    print("=" * 70)
    
except Exception as e:
    print(f"ERROR saving transcript: {e}")
    exit(1)

# Summary
print("\n" + "=" * 70)
print("DAY 1 COMPLETE!")
print("=" * 70)
print(f"\nTotal time: {(extraction_time + transcription_time)/60:.1f} minutes")
print(f"\nFiles created:")
print(f"  1. {AUDIO_PATH}")
print(f"  2. {TRANSCRIPT_PATH}")
print(f"\nNext steps:")
print(f"  - Review transcript.json")
print(f"  - Commit your code to Git")
print(f"  - Move to Day 2: Translation")
print("=" * 70)