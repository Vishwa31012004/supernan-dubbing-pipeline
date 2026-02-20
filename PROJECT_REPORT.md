# Day 7 Documentation & Submission Guide

## Deliverables

1. **Code repository** with scripts for Day 1 through Day 6.
2. **Final video output** at `outputs/final_dubbed_video.mp4`.
3. **Validation report** at `outputs/pipeline_report.json`.
4. **Loom walkthrough** (5-10 minutes) covering:
   - Architecture and flow
   - Major scripts and why specific tools were chosen
   - Demo of generated output assets

## Loom Recording Checklist

- [ ] Show input video (`data/input_video.mp4`)
- [ ] Show transcript output (`data/transcript.json`)
- [ ] Show Hindi translation (`data/transcript_hindi.json`)
- [ ] Play Hindi generated audio (`data/hindi_audio_full.mp3`)
- [ ] Play lip-synced output (`outputs/day5_lipsynced_video.mp4`)
- [ ] Show final packaged output (`outputs/final_dubbed_video.mp4`)
- [ ] Open validation JSON report (`outputs/pipeline_report.json`)

## Suggested Narrative (Short)

"This pipeline converts Kannada source speech to English for robust transcription, translates to Hindi, synthesizes natural Hindi audio, uses Wav2Lip to align mouth motion, then validates and packages final output artifacts. The automation scripts support sequential or resumed runs and emit machine-readable reports for QA."

## Risks + Mitigations

- **Wav2Lip compute cost / GPU availability**: run Day 4/5 in Colab.
- **TTS quality variance**: fallback between Edge TTS and ElevenLabs.
- **Duration drift**: Day 6 duration check flags A/V mismatch magnitude.
