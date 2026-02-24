# src/day3_tts_elevenlabs_v3.py
# Uses ElevenLabs V3 model with your chosen voice H6QPv2pQZDcGqLwDTIJQ

import json
import os
import re
import time
import subprocess
import requests
from dotenv import load_dotenv

load_dotenv()

ELEVENLABS_API_KEY = "b0452bb802d8e89ddf5111fc039969e85d6617a8924cbdf9ee017ea82afa2757"
VOICE_ID = "21m00Tcm4TlvDq8ikWAM"
MODEL_ID = "eleven_v3"

EMOTION_SETTINGS = {
    "calm":          {"stability": 0.5, "similarity_boost": 0.75, "style": 0.5},
    "instructional": {"stability": 0.5, "similarity_boost": 0.80, "style": 0.5},
    "warm":          {"stability": 0.5, "similarity_boost": 0.85, "style": 0.5},
    "concerned":     {"stability": 0.0, "similarity_boost": 0.80, "style": 0.5},
    "encouraging":   {"stability": 0.0, "similarity_boost": 0.80, "style": 0.5},
    "serious":       {"stability": 1.0, "similarity_boost": 0.75, "style": 0.5},
    "happy":         {"stability": 0.0, "similarity_boost": 0.85, "style": 0.5},
    "gentle":        {"stability": 0.5, "similarity_boost": 0.80, "style": 0.5},
    "neutral":       {"stability": 0.5, "similarity_boost": 0.75, "style": 0.5},
}

def generate_segment_audio(hindi_text, emotion, output_path):
    if not hindi_text.strip():
        return False

    settings = EMOTION_SETTINGS.get(emotion, EMOTION_SETTINGS["neutral"])

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }

    payload = {
        "text": hindi_text,
        "model_id": MODEL_ID,
        "voice_settings": {
            "stability": settings["stability"],
            "similarity_boost": settings["similarity_boost"],
            "style": settings["style"],
            "use_speaker_boost": True
        }
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)

        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                f.write(response.content)
            return True
        else:
            print(f"  ❌ Error {response.status_code}: {response.text[:150]}")
            return False
    except Exception as e:
        print(f"  ❌ Exception: {e}")
        return False

def combine_audio_segments(segment_files, output_path):
    list_file = "data/segment_list.txt"
    with open(list_file, 'w') as f:
        for seg_file in segment_files:
            f.write(f"file '{os.path.abspath(seg_file)}'\n")

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", list_file,
        "-c", "copy",
        output_path
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ffmpeg error: {result.stderr}")
        return False
    return True

def main():
    print("=" * 70)
    print("DAY 3: ELEVENLABS V3 - EMOTIONAL HINDI AUDIO")
    print(f"Voice ID : {VOICE_ID}")
    print(f"Model    : {MODEL_ID}")
    print("=" * 70)

    if not ELEVENLABS_API_KEY:
        print("❌ ELEVENLABS_API_KEY not found in .env!")
        return

    transcript_path = "data/transcript_hindi_with_emotions.json"
    if not os.path.exists(transcript_path):
        print("❌ transcript_hindi_with_emotions.json not found!")
        print("Run day2_translation_natural.py first!")
        return

    with open(transcript_path, 'r', encoding='utf-8') as f:
        transcript = json.load(f)

    segments = transcript.get("segments", [])
    print(f"✓ Loaded {len(segments)} segments\n")

    segments_dir = "data/audio_segments"
    os.makedirs(segments_dir, exist_ok=True)

    segment_files = []
    success_count = 0
    total_chars = 0

    for i, segment in enumerate(segments):
        hindi_text = segment.get("hindi_text", "").strip()
        emotion = segment.get("emotion", "neutral")

        if not hindi_text:
            continue

        seg_file = os.path.join(segments_dir, f"seg_{i:04d}.mp3")
        total_chars += len(hindi_text)

        if (i + 1) % 5 == 0 or i == 0:
            print(f"  Segment {i+1}/{len(segments)} | Emotion: {emotion} | Text: {hindi_text[:40]}...")

        success = generate_segment_audio(hindi_text, emotion, seg_file)

        if success:
            segment_files.append(seg_file)
            success_count += 1

        time.sleep(0.5)  # avoid rate limit

    print(f"\n✓ Generated: {success_count} segments")
    print(f"✓ Total characters used: {total_chars}")

    if segment_files:
        print("\nCombining all segments into one audio file...")
        output_path = "data/hindi_audio_emotional.mp3"
        combined = combine_audio_segments(segment_files, output_path)

        if combined:
            size = os.path.getsize(output_path) / 1024
            print(f"\n✅ DAY 3 COMPLETE!")
            print(f"Audio saved : data/hindi_audio_emotional.mp3 ({size:.1f} KB)")
            print(f"Model used  : V3 ✓")
            print(f"Emotions    : ✓")
        else:
            print("❌ Failed to combine segments")
    else:
        print("❌ No audio segments generated - check your API key!")

    print("=" * 70)

if __name__ == "__main__":
    main()