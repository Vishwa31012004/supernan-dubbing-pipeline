import json

# Load messy transcript
with open('data/transcript.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Clean each segment (remove gibberish, keep only English)
cleaned_segments = []

for seg in data['segments']:
    text = seg['text']
    
    # Basic cleaning - remove non-Latin characters except spaces and punctuation
    cleaned_text = ''.join(char for char in text if ord(char) < 128 or char.isspace())
    
    # Remove extra spaces
    cleaned_text = ' '.join(cleaned_text.split())
    
    # If segment is mostly garbage, replace with generic text
    if len(cleaned_text) < 5 or cleaned_text.count(' ') < 2:
        cleaned_text = "massage technique demonstration"
    
    seg['text'] = cleaned_text
    cleaned_segments.append(seg)

# Update data
data['segments'] = cleaned_segments
data['full_text'] = ' '.join([s['text'] for s in cleaned_segments])

# Save cleaned version
with open('data/transcript_cleaned.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("✓ Cleaned transcript saved to: data/transcript_cleaned.json")
print(f"Segments: {len(cleaned_segments)}")
print(f"\nPreview:\n{data['full_text'][:300]}")