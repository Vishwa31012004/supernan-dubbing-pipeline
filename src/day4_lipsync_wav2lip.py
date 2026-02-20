import argparse
import os
import subprocess
import sys
from pathlib import Path


def run_command(cmd: list[str]) -> None:
    print("\n$", " ".join(cmd))
    completed = subprocess.run(cmd, text=True)
    if completed.returncode != 0:
        raise RuntimeError(f"Command failed with exit code {completed.returncode}")


def ensure_file(path: Path, label: str) -> None:
    if not path.exists():
        raise FileNotFoundError(f"{label} not found: {path}")


def find_wav2lip_root(explicit_root: str | None) -> Path:
    if explicit_root:
        root = Path(explicit_root).expanduser().resolve()
        if (root / "inference.py").exists():
            return root
        raise FileNotFoundError(f"Wav2Lip root does not contain inference.py: {root}")

    candidates = [
        Path("Wav2Lip"),
        Path("../Wav2Lip"),
        Path("/content/Wav2Lip"),
    ]

    for candidate in candidates:
        if (candidate / "inference.py").exists():
            return candidate.resolve()

    raise FileNotFoundError(
        "Could not find Wav2Lip repository. Clone it and pass --wav2lip-root."
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Day 4/5: Run Wav2Lip to generate lip-synced Hindi dubbed video."
    )
    parser.add_argument("--input-video", default="data/input_video.mp4")
    parser.add_argument("--input-audio", default="data/hindi_audio_full.mp3")
    parser.add_argument("--output-video", default="outputs/day5_lipsynced_video.mp4")
    parser.add_argument("--wav2lip-root", default=None)
    parser.add_argument(
        "--checkpoint",
        default="checkpoints/wav2lip_gan.pth",
        help="Path relative to wav2lip root (or absolute path).",
    )
    parser.add_argument("--resize-factor", type=int, default=1)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the command without executing Wav2Lip.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()

    input_video = Path(args.input_video)
    input_audio = Path(args.input_audio)
    output_video = Path(args.output_video)

    try:
        ensure_file(input_video, "Input video")
        ensure_file(input_audio, "Input Hindi audio")

        wav2lip_root = find_wav2lip_root(args.wav2lip_root)
        checkpoint = Path(args.checkpoint)
        if not checkpoint.is_absolute():
            checkpoint = wav2lip_root / checkpoint
        ensure_file(checkpoint, "Wav2Lip checkpoint")

        output_video.parent.mkdir(parents=True, exist_ok=True)

        cmd = [
            sys.executable,
            str(wav2lip_root / "inference.py"),
            "--checkpoint_path",
            str(checkpoint),
            "--face",
            str(input_video),
            "--audio",
            str(input_audio),
            "--outfile",
            str(output_video),
            "--resize_factor",
            str(args.resize_factor),
        ]

        print("=" * 70)
        print("DAY 4/5: WAV2LIP LIP-SYNC")
        print("=" * 70)
        print(f"Wav2Lip root : {wav2lip_root}")
        print(f"Input video  : {input_video}")
        print(f"Input audio  : {input_audio}")
        print(f"Output video : {output_video}")

        if args.dry_run:
            print("\nDry run enabled. Command preview only.")
            print(" ".join(cmd))
            return 0

        run_command(cmd)

        if output_video.exists() and output_video.stat().st_size > 0:
            print("\n✅ Lip-sync complete!")
            print(f"Saved: {output_video}")
            return 0

        raise RuntimeError("Wav2Lip command finished but output video was not created.")

    except Exception as exc:
        print(f"\n❌ Error: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
