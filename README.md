# Supernan Video Dubbing Pipeline

**Author:** Vishwanath S  
**Project:** AI Automation Intern Assignment

End-to-end pipeline to dub a Kannada training video into Hindi audio with lip-sync.

## ✅ Project Status: COMPLETE (7/7)

| Day | Stage | Script | Status |
|---|---|---|---|
| 1 | Audio extraction + Kannada → English transcript | `src/day1_english_only.py` | ✅ |
| 2 | English → Hindi translation | `src/day2_translation_free.py` | ✅ |
| 3 | Hindi text-to-speech | `src/day3_tts_edge.py` / `src/day3_tts_elevenlabs.py` | ✅ |
| 4-5 | Lip-sync generation with Wav2Lip | `src/day4_lipsync_wav2lip.py` | ✅ |
| 6 | Final packaging + validation report | `src/day6_integrate_pipeline.py` | ✅ |
| 7 | Documentation + demo checklist | `PROJECT_REPORT.md` | ✅ |

---

## Quick Start

### 1) Core dependencies

- Python 3.10+
- `ffmpeg` / `ffprobe`
- Optional cloud GPU for Wav2Lip (Colab recommended)

Install Python packages as needed for the selected TTS stack:

```bash
pip install openai-whisper googletrans==4.0.0rc1 edge-tts pydub python-dotenv elevenlabs
```

### 2) Run pipeline step-by-step

```bash
python src/day1_english_only.py
python src/day2_translation_free.py
python src/day3_tts_edge.py
python src/day4_lipsync_wav2lip.py --wav2lip-root /path/to/Wav2Lip
python src/day6_integrate_pipeline.py
```

### 3) Orchestrated run

```bash
python src/run_full_pipeline.py
# Resume from a stage:
python src/run_full_pipeline.py --from-stage day3
```

---

## Inputs and Outputs

### Required Input
- `data/input_video.mp4`

### Produced Artifacts
- `data/transcript.json`
- `data/transcript_hindi.json`
- `data/hindi_audio_full.mp3`
- `outputs/day5_lipsynced_video.mp4`
- `outputs/final_dubbed_video.mp4`
- `outputs/pipeline_report.json`

---

## Wav2Lip Notes

- Use `Wav2Lip_Colab_Notebook.txt` if running on Google Colab.
- Download `wav2lip_gan.pth` checkpoint before executing Day 4/5 script.
- Day 6 treats Wav2Lip output as the final muxed dubbed video and records a duration check report.

---

## Completion Checklist

- [x] Source transcription produced
- [x] Hindi translation generated
- [x] Hindi speech synthesized
- [x] Lip-sync video rendered
- [x] Final dubbed video packaged
- [x] Validation report generated
- [x] Documentation checklist prepared
