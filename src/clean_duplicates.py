import json
import re

print("="*70)
print("CLEANING DUPLICATE WORDS FROM TRANSCRIPT")
print("="*70)

TRANSCRIPT_PATH = "data/transcript.json"

# Load transcript
print(f"\nLoading transcript from {TRANSCRIPT_PATH}...")
with open(TRANSCRIPT_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total segments: {len(data['segments'])}")

# Function to remove consecutive duplicates
def remove_duplicate_words(text):
    """Remove words that repeat 3+ times consecutively"""
    words = text.split()
    cleaned = []
    i = 0
    
    while i < len(words):
        word = words[i]
        count = 1
        
        # Count consecutive duplicates
        while i + count < len(words) and words[i + count].lower() == word.lower():
            count += 1
        
        # If word repeats 3+ times, keep only 1
        if count >= 3:
            cleaned.append(word)
            print(f"  Fixed: '{word}' repeated {count} times → kept 1")
            i += count
        else:
            # Keep all instances if only 1-2 times
            for _ in range(count):
                cleaned.append(word)
            i += count
    
    return ' '.join(cleaned)

# Clean each segment
print("\nCleaning segments...")
duplicates_found = 0

for seg in data['segments']:
    original_text = seg['text']
    cleaned_text = remove_duplicate_words(original_text)
    
    if original_text != cleaned_text:
        duplicates_found += 1
        seg['text'] = cleaned_text

# Regenerate full text
data['full_text'] = ' '.join([s['text'] for s in data['segments']])

# Save cleaned transcript
print(f"\n✓ Found and fixed {duplicates_found} segments with duplicates")
print(f"✓ Saving cleaned transcript...")

with open(TRANSCRIPT_PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"✓ Cleaned transcript saved to {TRANSCRIPT_PATH}")

print("\n" + "="*70)
print("✅ CLEANING COMPLETE!")
print("="*70)
print(f"Segments cleaned: {duplicates_found}/{len(data['segments'])}")
print("\nNext: Re-run Day 2 and Day 3 to regenerate Hindi translation and audio")
print("="*70)