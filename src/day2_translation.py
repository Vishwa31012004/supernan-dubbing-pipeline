import json
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

print("="*70)
print("DAY 2: TRANSLATION TO HINDI")
print("="*70)

# Configuration
TRANSCRIPT_PATH = "data/transcript.json"
HINDI_TRANSCRIPT_PATH = "data/transcript_hindi.json"

# Check API key
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    print("ERROR: OPENAI_API_KEY not found in .env file!")
    print("Please create .env file with your API key")
    exit(1)

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Load transcript
print(f"\nLoading transcript from {TRANSCRIPT_PATH}...")
with open(TRANSCRIPT_PATH, 'r', encoding='utf-8') as f:
    transcript_data = json.load(f)

print(f"Loaded {transcript_data['total_segments']} segments")
print(f"Source language: {transcript_data.get('language', 'unknown')}")

# Translate each segment
print("\nTranslating to Hindi...")
print("(This may take a few minutes)")

hindi_segments = []
total_cost = 0

for i, segment in enumerate(transcript_data['segments']):
    # Show progress
    if (i + 1) % 10 == 0:
        print(f"  Progress: {i+1}/{transcript_data['total_segments']} segments")
    
    # Prepare translation prompt
    prompt = f"""Translate the following text to natural, conversational Hindi. 
This is from a childcare training video about baby massage.
Use appropriate childcare terminology in Hindi.

English text: {segment['text']}

Provide ONLY the Hindi translation, nothing else."""

    try:
        # Call GPT-4 API
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a professional translator specializing in Hindi. Translate naturally and appropriately for childcare context."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,  # Lower temperature for more consistent translation
            max_tokens=200
        )
        
        # Get translation
        hindi_text = response.choices[0].message.content.strip()
        
        # Create translated segment
        hindi_segment = {
            "id": segment['id'],
            "start": segment['start'],
            "end": segment['end'],
            "original_text": segment['text'],
            "hindi_text": hindi_text,
            "words": segment.get('words', [])  # Keep original timing
        }
        
        hindi_segments.append(hindi_segment)
        
    except Exception as e:
        print(f"\nError translating segment {i}: {e}")
        # Keep original if translation fails
        hindi_segments.append({
            "id": segment['id'],
            "start": segment['start'],
            "end": segment['end'],
            "original_text": segment['text'],
            "hindi_text": "[TRANSLATION FAILED]",
            "words": segment.get('words', [])
        })

# Combine all Hindi text
full_hindi_text = " ".join([seg['hindi_text'] for seg in hindi_segments])

# Create Hindi transcript
hindi_transcript = {
    "source_video": transcript_data.get('source_video', ''),
    "audio_file": transcript_data.get('audio_file', ''),
    "original_language": transcript_data.get('language', 'unknown'),
    "target_language": "hi",
    "full_hindi_text": full_hindi_text,
    "model_used": "gpt-4",
    "total_segments": len(hindi_segments),
    "segments": hindi_segments
}

# Save Hindi transcript
print(f"\nSaving Hindi transcript to {HINDI_TRANSCRIPT_PATH}...")
with open(HINDI_TRANSCRIPT_PATH, 'w', encoding='utf-8') as f:
    json.dump(hindi_transcript, f, indent=2, ensure_ascii=False)

print(f"\n✅ Translation complete!")
print(f"Total segments translated: {len(hindi_segments)}")

# Show preview
print("\n" + "="*70)
print("HINDI TRANSLATION PREVIEW (first 300 characters):")
print("="*70)
print(full_hindi_text[:300] + "...")
print("="*70)

# Cost estimate
estimated_cost = len(hindi_segments) * 0.002  # Rough estimate
print(f"\nEstimated API cost: ${estimated_cost:.3f}")

print("\n" + "="*70)
print("DAY 2 COMPLETE!")
print("="*70)
print(f"\nFiles created:")
print(f"  - {HINDI_TRANSCRIPT_PATH}")
print(f"\nNext steps:")
print(f"  - Review Hindi translation quality")
print(f"  - Commit to Git")
print(f"  - Move to Day 3: Text-to-Speech")
print("="*70)