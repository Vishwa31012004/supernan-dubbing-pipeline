import json
import time
from googletrans import Translator

print("="*70)
print("DAY 2: TRANSLATION TO HINDI (GOOGLE TRANSLATE - FREE)")
print("="*70)

# Configuration
TRANSCRIPT_PATH = "data/transcript.json"
HINDI_TRANSCRIPT_PATH = "data/transcript_hindi.json"

# Initialize translator
translator = Translator()
print("✓ Google Translator initialized")

# Load transcript
print(f"\nLoading transcript from {TRANSCRIPT_PATH}...")
try:
    with open(TRANSCRIPT_PATH, 'r', encoding='utf-8') as f:
        transcript_data = json.load(f)
    print(f"✓ Loaded {transcript_data['total_segments']} segments")
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

# Translate segments
print("\nTranslating to Hindi using Google Translate...")
print("(This will take 3-5 minutes)")
print("Cost: FREE!")

hindi_segments = []

for i, segment in enumerate(transcript_data['segments']):
    # Progress
    if (i + 1) % 10 == 0 or i == 0:
        print(f"  Progress: {i+1}/{transcript_data['total_segments']}")
    
    try:
        # Translate to Hindi
        translation = translator.translate(
            segment['text'],
            src='en',
            dest='hi'
        )
        
        hindi_text = translation.text
        
        # Create segment
        hindi_segment = {
            "id": segment['id'],
            "start": segment['start'],
            "end": segment['end'],
            "original_text": segment['text'],
            "hindi_text": hindi_text,
            "words": segment.get('words', [])
        }
        
        hindi_segments.append(hindi_segment)
        
        # Small delay
        time.sleep(0.1)
        
    except Exception as e:
        print(f"\n⚠ Segment {i} error: {str(e)[:50]}")
        hindi_segments.append({
            "id": segment['id'],
            "start": segment['start'],
            "end": segment['end'],
            "original_text": segment['text'],
            "hindi_text": f"[Translation failed: {segment['text']}]",
            "words": segment.get('words', [])
        })
        time.sleep(0.5)

# Combine text
full_hindi_text = " ".join([seg['hindi_text'] for seg in hindi_segments])

# Create output
hindi_transcript = {
    "source_video": transcript_data.get('source_video', ''),
    "audio_file": transcript_data.get('audio_file', ''),
    "original_language": transcript_data.get('language', 'unknown'),
    "target_language": "hi",
    "full_hindi_text": full_hindi_text,
    "translation_method": "Google Translate (Free)",
    "total_segments": len(hindi_segments),
    "segments": hindi_segments
}

# Save
print(f"\n✓ Saving to {HINDI_TRANSCRIPT_PATH}...")
with open(HINDI_TRANSCRIPT_PATH, 'w', encoding='utf-8') as f:
    json.dump(hindi_transcript, f, indent=2, ensure_ascii=False)

# Summary
successful = sum(1 for seg in hindi_segments if not seg['hindi_text'].startswith("[Translation failed"))
failed = len(hindi_segments) - successful

print("\n" + "="*70)
print("✅ DAY 2 COMPLETE!")
print("="*70)
print(f"Segments translated: {successful}/{len(hindi_segments)}")
if failed > 0:
    print(f"Segments failed: {failed}")
print(f"Cost: $0.00 (FREE!)")

# Preview
print("\n" + "="*70)
print("HINDI PREVIEW (first 200 chars):")
print("="*70)
preview = full_hindi_text[:200] if len(full_hindi_text) > 200 else full_hindi_text
print(preview)
if len(full_hindi_text) > 200:
    print("...")
print("="*70)

# Check Hindi
has_hindi = any('\u0900' <= c <= '\u097F' for c in full_hindi_text)
print(f"\n✓ Contains Hindi Devanagari: {has_hindi}")

if has_hindi:
    print("\n🎉 SUCCESS! Hindi translation complete!")
else:
    print("\n⚠ Warning: No Hindi script detected")

print("\nNext steps:")
print("  1. Review: notepad data\\transcript_hindi.json")
print("  2. Commit: git add . && git commit -m 'Day 2 complete'")
print("  3. Move to Day 3: Text-to-Speech")
print("="*70)