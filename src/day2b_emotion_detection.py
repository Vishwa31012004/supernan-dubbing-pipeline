import json
import re

print("="*70)
print("DAY 2B: EMOTION DETECTION & TAGGING")
print("="*70)

INPUT_PATH = "data/transcript_hindi_natural.json"
OUTPUT_PATH = "data/transcript_hindi_with_emotions.json"

# Load Hindi transcript
with open(INPUT_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"✓ Loaded {data['total_segments']} segments")

# Emotion detection rules (based on keywords and punctuation)
def detect_emotion(text, original_english=""):
    """Detect emotion from text content"""
    
    text_lower = text.lower()
    english_lower = original_english.lower()
    
    # Emotion keywords
    emotions = {
        'happy': ['!', 'good', 'great', 'wonderful', 'excellent', 'love', 'खुश', 'अच्छा', 'बढ़िया'],
        'excited': ['!!', 'amazing', 'wow', 'fantastic', 'वाह', 'शानदार'],
        'calm': ['gently', 'slowly', 'softly', 'peaceful', 'आराम', 'धीरे', 'शांति'],
        'serious': ['important', 'must', 'careful', 'attention', 'ध्यान', 'सावधान', 'ज़रूरी'],
        'concerned': ['careful', 'watch', 'caution', 'avoid', 'don\'t', 'सावधान', 'मत'],
        'instructional': ['first', 'then', 'next', 'now', 'after', 'पहले', 'फिर', 'अब'],
    }
    
    # Check for emotion indicators
    detected = 'neutral'
    confidence = 0
    
    for emotion, keywords in emotions.items():
        matches = sum(1 for keyword in keywords if keyword in text_lower or keyword in english_lower)
        if matches > confidence:
            confidence = matches
            detected = emotion
    
    # Punctuation-based detection
    if '!' in text:
        if detected == 'neutral':
            detected = 'excited'
    elif '?' in text:
        detected = 'curious'
    
    return detected

# Process segments
print("\nDetecting emotions...")
for i, segment in enumerate(data['segments']):
    if (i + 1) % 10 == 0:
        print(f"  Progress: {i+1}/{data['total_segments']}")
    
    emotion = detect_emotion(
        segment['hindi_text'],
        segment.get('original_text', '')
    )
    
    # Add emotion tag
    segment['emotion'] = emotion
    segment['hindi_text_with_emotion'] = f"[{emotion}] {segment['hindi_text']}"

# Save
data['emotion_detection_enabled'] = True
with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"\n✅ Emotion detection complete!")
print(f"Saved to: {OUTPUT_PATH}")

# Summary
emotions_found = {}
for seg in data['segments']:
    emotion = seg['emotion']
    emotions_found[emotion] = emotions_found.get(emotion, 0) + 1

print("\nEmotion distribution:")
for emotion, count in sorted(emotions_found.items()):
    print(f"  {emotion}: {count} segments")

print("="*70)