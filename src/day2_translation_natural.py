import json
import os
import re
import time
from deep_translator import GoogleTranslator
from dotenv import load_dotenv

load_dotenv()

translator = GoogleTranslator(source='en', target='hi')

def detect_emotion(text):
    """Detect emotion based on keywords in the text"""
    text_lower = text.lower()
    
    if any(w in text_lower for w in ['careful', 'danger', 'never', 'dont', "don't", 'warning', 'stop']):
        return 'serious'
    elif any(w in text_lower for w in ['good job', 'great', 'excellent', 'perfect', 'well done', 'bravo', 'amazing']):
        return 'happy'
    elif any(w in text_lower for w in ['gently', 'soft', 'slowly', 'calm', 'relax', 'soothe']):
        return 'gentle'
    elif any(w in text_lower for w in ['make sure', 'remember', 'always', 'must', 'should', 'need to', 'important']):
        return 'instructional'
    elif any(w in text_lower for w in ['try', 'you can', 'lets', "let's", 'come', 'now we']):
        return 'encouraging'
    elif any(w in text_lower for w in ['worry', 'concern', 'problem', 'issue', 'pain', 'cry', 'sick']):
        return 'concerned'
    elif any(w in text_lower for w in ['love', 'happy', 'smile', 'enjoy', 'fun', 'play']):
        return 'warm'
    else:
        return 'instructional'

def translate_with_emotion(text):
    """Translate to Hindi and add emotion tag"""
    try:
        hindi = translator.translate(text)
        emotion = detect_emotion(text)
        return hindi, emotion, f"{hindi} [{emotion}]"
    except Exception as e:
        print(f"  Translation error: {e}")
        time.sleep(2)
        try:
            hindi = translator.translate(text)
            emotion = detect_emotion(text)
            return hindi, emotion, f"{hindi} [{emotion}]"
        except:
            return text, "neutral", f"{text} [neutral]"

def main():
    print("=" * 70)
    print("DAY 2: NATURAL HINDI TRANSLATION WITH EMOTIONS (deep-translator)")
    print("=" * 70)

    transcript_path = "data/transcript.json"
    if not os.path.exists(transcript_path):
        print("❌ data/transcript.json not found!")
        return

    with open(transcript_path, 'r', encoding='utf-8') as f:
        transcript = json.load(f)

    segments = transcript.get("segments", [])
    print(f"✓ Loaded {len(segments)} segments")
    print("Translating to natural spoken Hindi with emotions...\n")

    translated_segments = []

    for i, segment in enumerate(segments):
        if (i + 1) % 10 == 0 or i == 0:
            print(f"  Progress: {i+1}/{len(segments)}")

        original_text = segment.get("text", "").strip()

        if not original_text:
            segment_copy = dict(segment)
            segment_copy["hindi_text"] = ""
            segment_copy["hindi_with_emotion"] = ""
            segment_copy["emotion"] = "neutral"
            translated_segments.append(segment_copy)
            continue

        hindi_text, emotion, hindi_with_emotion = translate_with_emotion(original_text)

        segment_copy = dict(segment)
        segment_copy["hindi_text"] = hindi_text
        segment_copy["hindi_with_emotion"] = hindi_with_emotion
        segment_copy["emotion"] = emotion

        translated_segments.append(segment_copy)
        time.sleep(0.3)  # small delay to avoid blocking

    output = dict(transcript)
    output["segments"] = translated_segments

    with open("data/transcript_hindi_with_emotions.json", 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Translation complete!")
    print(f"Saved to: data/transcript_hindi_with_emotions.json")

    print("\n--- SAMPLE OUTPUT (first 5 segments) ---")
    for seg in translated_segments[:5]:
        if seg.get("text"):
            print(f"Original : {seg.get('text', '')}")
            print(f"Hindi    : {seg.get('hindi_with_emotion', '')}")
            print()

    # Emotion summary
    emotions = [s.get('emotion', 'neutral') for s in translated_segments if s.get('emotion')]
    from collections import Counter
    emotion_counts = Counter(emotions)
    print("Emotion distribution:")
    for emotion, count in emotion_counts.most_common():
        print(f"  {emotion}: {count} segments")

    print("=" * 70)

if __name__ == "__main__":
    main()