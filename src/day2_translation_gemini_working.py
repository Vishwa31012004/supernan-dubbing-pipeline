import json
import os
import time
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key
load_dotenv()

print("="*70)
print("DAY 2: TRANSLATION TO HINDI (GOOGLE GEMINI - STABLE)")
print("="*70)

# Configuration
TRANSCRIPT_PATH = "data/transcript.json"
HINDI_TRANSCRIPT_PATH = "data/transcript_hindi.json"

# Get API key
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    print("\n❌ ERROR: GOOGLE_API_KEY not found in .env!")
    exit(1)

print("✓ API key loaded")

# Configure Gemini (OLD stable way)
try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    print("✓ Gemini Pro initialized")
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
print("\nTranslating to Hindi with Gemini Pro...")
print("(This will take 8-12 minutes for 52 segments)")
print("Cost: FREE!")

hindi_segments = []

for i, segment in enumerate(transcript_data['segments']):
    # Progress
    if (i + 1) % 10 == 0 or i == 0:
        print(f"  Progress: {i+1}/{transcript_data['total_segments']}")
    
    try:
        # Create prompt
        prompt = f"""You are an expert Hindi translator specializing in childcare content.

Translate this text to natural, conversational Hindi (Devanagari script).
Context: Baby massage training video for Indian nannies.
Use appropriate Hindi terminology for childcare.

English text: {segment['text']}

Provide ONLY the Hindi translation, nothing else."""

        # Generate translation
        response = model.generate_content(prompt)
        
        # Extract text
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
        
        # Rate limiting
        time.sleep(1.2)  # 1.2 seconds between requests
        
    except Exception as e:
        error_msg = str(e)
        print(f"\n⚠ Segment {i} error: {error_msg[:80]}")
        
        # Retry once with simpler prompt
        try:
            time.sleep(2)
            simple_prompt = f"Translate to Hindi: {segment['text']}"
            response = model.generate_content(simple_prompt)
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

# Combine text
full_hindi_text = " ".join([seg['hindi_text'] for seg in hindi_segments])

# Create output
hindi_transcript = {
    "source_video": transcript_data.get('source_video', ''),
    "audio_file": transcript_data.get('audio_file', ''),
    "original_language": transcript_data.get('language', 'unknown'),
    "target_language": "hi",
    "full_hindi_text": full_hindi_text,
    "translation_model": "gemini-pro",
    "total_segments": len(hindi_segments),
    "segments": hindi_segments
}

# Save
print(f"\n✓ Saving to {HINDI_TRANSCRIPT_PATH}...")
with open(HINDI_TRANSCRIPT_PATH, 'w', encoding='utf-8') as f:
    json.dump(hindi_transcript, f, indent=2, ensure_ascii=False)

# Summary
successful = sum(1 for seg in hindi_segments if seg['hindi_text'] != "[Translation failed]")
failed = len(hindi_segments) - successful

print("\n" + "="*70)
print("✅ DAY 2 COMPLETE!")
print("="*70)
print(f"Segments translated: {successful}/{len(hindi_segments)}")
if failed > 0:
    print(f"Segments failed: {failed}")
print(f"Cost: $0.00 (FREE with Gemini Pro!)")

# Preview
print("\n" + "="*70)
print("HINDI PREVIEW (first 200 chars):")
print("="*70)
print(full_hindi_text[:200])
if len(full_hindi_text) > 200:
    print("...")
print("="*70)

# Check Hindi
has_hindi = any('\u0900' <= c <= '\u097F' for c in full_hindi_text)
print(f"\n✓ Contains Hindi Devanagari: {has_hindi}")

if has_hindi:
    print("\n🎉 SUCCESS! Gemini Pro translation working!")
else:
    print("\n⚠ Warning: No Hindi script detected")

print("\nNext: Day 3 - Text-to-Speech")
print("="*70)