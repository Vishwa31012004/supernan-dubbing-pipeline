import json
import os
import time
from dotenv import load_dotenv
from google import genai

# Load API key
load_dotenv()

print("="*70)
print("DAY 2: TRANSLATION TO HINDI (GOOGLE GEMINI)")
print("="*70)

# Configuration
TRANSCRIPT_PATH = "data/transcript.json"
HINDI_TRANSCRIPT_PATH = "data/transcript_hindi.json"

# Get API key
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    print("\n❌ ERROR: GOOGLE_API_KEY not found!")
    exit(1)

print("✓ API key loaded")

# Configure Gemini with correct API
try:
    client = genai.Client(api_key=api_key)
    print("✓ Gemini client initialized")
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

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
print("\nTranslating to Hindi with Gemini...")
print("(This will take 5-8 minutes)")
print("Cost: FREE!")

hindi_segments = []

for i, segment in enumerate(transcript_data['segments']):
    # Progress
    if (i + 1) % 10 == 0 or i == 0:
        print(f"  Progress: {i+1}/{transcript_data['total_segments']}")
    
    try:
        # Create prompt
        prompt = f"""Translate this text to natural, conversational Hindi.
Context: Baby massage training video for Indian nannies.
Use appropriate Hindi childcare terminology.

English: {segment['text']}

Hindi translation only (Devanagari script):"""

        # Generate with correct method
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=prompt,
            config={
                'temperature': 0.3,
                'max_output_tokens': 500
            }
        )
        
        hindi_text = response.text.strip()
        
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
        
        # Delay for rate limits
        time.sleep(1)
        
    except Exception as e:
        print(f"\n⚠ Segment {i} error: {str(e)[:100]}")
        
        # Fallback: try without config
        try:
            response = client.models.generate_content(
                model='gemini-1.5-flash',
                contents=f"Translate to Hindi: {segment['text']}"
            )
            hindi_text = response.text.strip()
        except:
            hindi_text = "[Translation failed]"
        
        hindi_segments.append({
            "id": segment['id'],
            "start": segment['start'],
            "end": segment['end'],
            "original_text": segment['text'],
            "hindi_text": hindi_text,
            "words": segment.get('words', [])
        })
        
        time.sleep(2)

# Combine
full_hindi_text = " ".join([seg['hindi_text'] for seg in hindi_segments])

# Output
hindi_transcript = {
    "source_video": transcript_data.get('source_video', ''),
    "audio_file": transcript_data.get('audio_file', ''),
    "original_language": transcript_data.get('language', 'unknown'),
    "target_language": "hi",
    "full_hindi_text": full_hindi_text,
    "translation_model": "gemini-1.5-flash",
    "total_segments": len(hindi_segments),
    "segments": hindi_segments
}

# Save
print(f"\n✓ Saving to {HINDI_TRANSCRIPT_PATH}...")
with open(HINDI_TRANSCRIPT_PATH, 'w', encoding='utf-8') as f:
    json.dump(hindi_transcript, f, indent=2, ensure_ascii=False)

# Summary
print("\n" + "="*70)
print("✅ DAY 2 COMPLETE!")
print("="*70)
print(f"Segments translated: {len(hindi_segments)}")
print(f"Cost: $0.00 (FREE!)")
print("\n" + "="*70)
print("HINDI PREVIEW:")
print("="*70)
print(full_hindi_text[:200])
print("="*70)

has_hindi = any('\u0900' <= c <= '\u097F' for c in full_hindi_text)
print(f"\n✓ Hindi Devanagari: {has_hindi}")
print("\nNext: Day 3 - Text-to-Speech")
print("="*70)