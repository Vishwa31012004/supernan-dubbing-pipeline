import os
import subprocess
import sys

INPUT_VIDEO = "data/input_video_small.mp4"
INPUT_AUDIO = "data/hindi_audio_emotional.mp3"
OUTPUT_VIDEO = "data/output_lipsynced.mp4"
WAV2LIP_DIR = "Wav2Lip"
CHECKPOINT = "Wav2Lip/checkpoints/wav2lip_gan.pth"

def check_files():
    print("Checking required files...")
    if not os.path.exists(INPUT_VIDEO):
        print(f"❌ Input video not found: {INPUT_VIDEO}")
        return False
    if not os.path.exists(INPUT_AUDIO):
        print(f"❌ Audio not found: {INPUT_AUDIO}")
        return False
    if not os.path.exists(WAV2LIP_DIR):
        print(f"❌ Wav2Lip folder not found!")
        return False
    if not os.path.exists(CHECKPOINT):
        print(f"❌ Checkpoint not found: {CHECKPOINT}")
        return False
    print("✓ All files found!")
    return True

def run_lipsync():
    print("=" * 70)
    print("DAY 4: LIP SYNC WITH WAV2LIP")
    print("=" * 70)

    if not check_files():
        return

    cmd = [
    sys.executable,
    "inference.py",
    "--checkpoint_path", "../" + CHECKPOINT,
    "--face", "../" + INPUT_VIDEO,
    "--audio", "../" + INPUT_AUDIO,
    "--outfile", "../" + OUTPUT_VIDEO,
    "--nosmooth",
    "--pads", "0", "10", "0", "0",
    "--face_det_batch_size", "4"
]

    print(f"Input video : {INPUT_VIDEO}")
    print(f"Input audio : {INPUT_AUDIO}")
    print(f"Output video: {OUTPUT_VIDEO}")
    print("\nRunning Wav2Lip... (this takes 5-15 minutes)")
    print("=" * 70)

    result = subprocess.run(cmd, cwd=WAV2LIP_DIR)

    if result.returncode == 0:
        if os.path.exists(OUTPUT_VIDEO):
            size = os.path.getsize(OUTPUT_VIDEO) / (1024*1024)
            print(f"\n✅ DAY 4 COMPLETE!")
            print(f"Lip synced video: {OUTPUT_VIDEO} ({size:.1f} MB)")
        else:
            print("❌ Output video not created")
    else:
        print(f"❌ Wav2Lip failed: {result.returncode}")

if __name__ == "__main__":
    run_lipsync()