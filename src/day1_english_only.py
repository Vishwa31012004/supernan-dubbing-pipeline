import os
import json
import time
import subprocess
import whisper

print("="*70)
print("DAY 1: AUDIO EXTRACTION AND ENGLISH TRANSLATION")
print("="*70)

# Configuration
VIDEO_PATH = "data/input_video.mp4"
AUDIO_PATH = "data/extracted_audio.wav"
TRANSCRIPT_PATH = "data/transcript.json"
WHISPER_MODEL = "medium"  # Using medium for better translation

# Check video
if not os.path.exists(VIDEO_PATH):
    print(f"❌ Video not found: {VIDEO_PATH}")
    exit(1)

file_size = os.path.getsize(VIDEO_PATH) / (1024*1024)
print(f"\n✓ Input video: {VIDEO_PATH}")
print(f"✓ Size: {file_size:.1f} MB")

# STEP 1: Extract Audio (skip if already exists)
print("\n" + "-"*70)
print("STEP 1: Extracting audio...")
print("-"*70)

if os.path.exists(AUDIO_PATH):
    print(f"✓ Audio already exists: {AUDIO_PATH}")
else:
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
            print(f"✓ Audio extracted: {audio_size:.1f} MB")
        else:
            print("❌ Audio extraction failed")
            exit(1)
            
    except Exception as e:
        print(f"❌ Error: {e}")
        exit(1)

# STEP 2: Transcribe with Whisper in ENGLISH TRANSLATION MODE
print("\n" + "-"*70)
print("STEP 2: Translating Kannada to English with Whisper...")
print("-"*70)
print(f"Model: {WHISPER_MODEL}")
print("Mode: TRANSLATE (Kannada → English)")


start_time = time.time()

try:
    # Load model
    print("\nLoading Whisper model...")
    model = whisper.load_model(WHISPER_MODEL)
    print("✓ Model loaded")
    
    # Transcribe with TRANSLATE task - THIS IS THE KEY!
    print("\nTranslating to English...")
    print("(Processing...)\n")
    
    result = model.transcribe(
        AUDIO_PATH,
        task='translate',  # CRITICAL: Forces English output!
        language='kn',     
        word_timestamps=True,
        verbose=True,     
        fp16=False         # Use FP32 for better quality
    )
    
    print(f"\n✓ Translation complete!")
    print(f"✓ Source language: {result['language']}")
    print(f"✓ Total segments: {len(result['segments'])}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

transcription_time = time.time() - start_time
print(f"✓ Time: {transcription_time/60:.1f} minutes")

# STEP 3: Save CLEAN English transcript
print("\n" + "-"*70)
print("STEP 3: Saving clean English transcript...")
print("-"*70)

try:
    # Clean the text - remove any non-ASCII characters
    clean_text = result['text'].encode('ascii', 'ignore').decode('ascii')
    
    transcript_data = {
        "source_video": VIDEO_PATH,
        "audio_file": AUDIO_PATH,
        "source_language": "kn",
        "output_language": "en",
        "full_text": clean_text,
        "model_used": WHISPER_MODEL,
        "translation_mode": True,
        "total_segments": len(result['segments']),
        "segments": []
    }
    
    for segment in result['segments']:
        # Clean each segment text
        clean_seg_text = segment['text'].encode('ascii', 'ignore').decode('ascii').strip()
        
        seg_data = {
            "id": segment['id'],
            "start": segment['start'],
            "end": segment['end'],
            "text": clean_seg_text,
            "words": []
        }
        
        if 'words' in segment:
            for word in segment['words']:
                # Only include ASCII words
                clean_word = word['word'].encode('ascii', 'ignore').decode('ascii').strip()
                if clean_word:  # Only add if not empty
                    seg_data['words'].append({
                        "word": clean_word,
                        "start": word['start'],
                        "end": word['end']
                    })
        
        transcript_data['segments'].append(seg_data)
    
    with open(TRANSCRIPT_PATH, 'w', encoding='utf-8') as f:
        json.dump(transcript_data, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Saved: {TRANSCRIPT_PATH}")
    
    # Preview
    print("\n" + "="*70)
    print("ENGLISH TRANSLATION PREVIEW (first 300 characters):")
    print("="*70)
    preview = clean_text[:300]
    print(preview)
    if len(clean_text) > 300:
        print("...")
    print("="*70)
    
    # Check for non-English characters
    non_ascii = sum(1 for c in clean_text if ord(c) > 127)
    print(f"\nNon-English characters removed: {non_ascii}")
    
except Exception as e:
    print(f"❌ Error saving: {e}")
    exit(1)

# Summary
print("\n" + "="*70)
print("STAGE 1 COMPLETE: TRANSCRIPTION")
print("="*70)
print(f"Processing time: {transcription_time/60:.1f} minutes")
print(f"Segments extracted: {len(result['segments'])}")
print(f"Output: {TRANSCRIPT_PATH}")
print("="*70)