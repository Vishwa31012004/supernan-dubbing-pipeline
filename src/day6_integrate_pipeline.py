import argparse
import json
import subprocess
from pathlib import Path


def ffprobe_duration(path: Path) -> float:
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        str(path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(result.stdout.strip())


def save_report(report_path: Path, payload: dict) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with report_path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Day 6: Validate and package final dubbed video assets."
    )
    parser.add_argument("--lipsynced-video", default="outputs/day5_lipsynced_video.mp4")
    parser.add_argument("--hindi-audio", default="data/hindi_audio_full.mp3")
    parser.add_argument("--final-video", default="outputs/final_dubbed_video.mp4")
    parser.add_argument("--report", default="outputs/pipeline_report.json")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    lipsynced_video = Path(args.lipsynced_video)
    hindi_audio = Path(args.hindi_audio)
    final_video = Path(args.final_video)
    report_path = Path(args.report)

    if not lipsynced_video.exists():
        print(f"❌ Missing lip-synced video: {lipsynced_video}")
        return 1
    if not hindi_audio.exists():
        print(f"❌ Missing Hindi audio: {hindi_audio}")
        return 1

    final_video.parent.mkdir(parents=True, exist_ok=True)

    try:
        video_duration = ffprobe_duration(lipsynced_video)
        audio_duration = ffprobe_duration(hindi_audio)
        diff = abs(video_duration - audio_duration)

        # The Day 5 output is already muxed by Wav2Lip, so packaging is a copy.
        final_video.write_bytes(lipsynced_video.read_bytes())

        report = {
            "day6_status": "completed",
            "inputs": {
                "lipsynced_video": str(lipsynced_video),
                "hindi_audio": str(hindi_audio),
            },
            "outputs": {"final_video": str(final_video)},
            "durations_seconds": {
                "video": round(video_duration, 3),
                "audio": round(audio_duration, 3),
                "absolute_difference": round(diff, 3),
            },
            "notes": [
                "Wav2Lip output is treated as final dubbed video.",
                "Duration difference under 1s is typically acceptable.",
            ],
        }
        save_report(report_path, report)

        print("✅ Day 6 integration complete")
        print(f"Final video : {final_video}")
        print(f"Report      : {report_path}")
        print(f"Video (s)   : {video_duration:.2f}")
        print(f"Audio (s)   : {audio_duration:.2f}")
        print(f"Diff (s)    : {diff:.2f}")
        return 0

    except subprocess.CalledProcessError as exc:
        print(f"❌ ffprobe failed: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
