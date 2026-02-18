import os
import sys
import subprocess

print("=" * 60)
print("Testing Setup")
print("=" * 60)

# checking python
print(f"\nPython: {sys.version.split()[0]}")

# whisper check
try:
    import whisper
    print("Whisper - OK")
except ImportError:
    print("ERROR: Whisper not found")
    sys.exit(1)

# pytorch
try:
    import torch
    print(f"PyTorch - OK ({torch.__version__})")
except ImportError:
    print("ERROR: PyTorch missing")
    sys.exit(1)

# ffmpeg python package
try:
    import ffmpeg
    print("ffmpeg-python - OK")
except ImportError:
    print("ERROR: ffmpeg-python not installed")
    sys.exit(1)

# test ffmpeg binary using subprocess instead
try:
    result = subprocess.run(['ffmpeg', '-version'], 
                          capture_output=True, 
                          text=True,
                          shell=True)
    if 'ffmpeg version' in result.stdout:
        print("ffmpeg binary - OK")
    else:
        print("WARNING: ffmpeg response unclear")
except Exception as e:
    print(f"WARNING: {e}")

# look for video file
video = "data/input_video.mp4"
if os.path.exists(video):
    print(f"Video found: {video}")
    size_mb = os.path.getsize(video) / (1024*1024)
    print(f"  Size: {size_mb:.1f} MB")
else:
    print(f"WARNING: Video not found at {video}")
    print("Download from Google Drive link")

# check directories
print("\nFolders:")
for d in ['data', 'src', 'outputs', 'logs']:
    status = "YES" if os.path.exists(d) else "NO"
    print(f"  {d}: {status}")

print("=" * 60)
print("Setup complete!")
print("=" * 60)