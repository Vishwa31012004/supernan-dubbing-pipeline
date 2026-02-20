import argparse
import subprocess
import sys


STAGES = {
    "day1": [sys.executable, "src/day1_english_only.py"],
    "day2": [sys.executable, "src/day2_translation_free.py"],
    "day3": [sys.executable, "src/day3_tts_edge.py"],
    "day4_5": [sys.executable, "src/day4_lipsync_wav2lip.py"],
    "day6": [sys.executable, "src/day6_integrate_pipeline.py"],
}


def run_stage(name: str) -> None:
    cmd = STAGES[name]
    print("\n" + "=" * 70)
    print(f"RUNNING {name.upper()}")
    print("=" * 70)
    print("$", " ".join(cmd))
    result = subprocess.run(cmd)
    if result.returncode != 0:
        raise RuntimeError(f"Stage {name} failed with exit code {result.returncode}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the full 7-day dubbing pipeline")
    parser.add_argument(
        "--from-stage",
        choices=list(STAGES.keys()),
        default="day1",
        help="Resume pipeline from a specific stage",
    )
    args = parser.parse_args()

    stage_names = list(STAGES.keys())
    start_index = stage_names.index(args.from_stage)

    try:
        for stage in stage_names[start_index:]:
            run_stage(stage)

        print("\n✅ Pipeline completed through Day 6.")
        print("📌 Day 7 deliverables are documentation + Loom recording.")
        return 0

    except Exception as exc:
        print(f"\n❌ Pipeline failed: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
