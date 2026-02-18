\# Supernan Video Dubbing Pipeline



\*\*Author:\*\* Vishwanath S  

\*\*Project:\*\* AI Automation Intern Assignment  

\*\*Timeline:\*\* 7 days | \*\*Progress: 2/7 Complete\*\* ✅✅⬜⬜⬜⬜⬜



---



\## ✅ Day 1: COMPLETE - Clean English Translation



\### Results:

\- \*\*Source:\*\* Kannada audio from training video

\- \*\*Output:\*\* Clean English text (ASCII only)

\- \*\*Model:\*\* Whisper medium (translate mode)

\- \*\*Segments:\*\* 68 with word-level timestamps

\- \*\*Processing time:\*\* 10.8 minutes

\- \*\*Quality:\*\* Pure English, no mixed scripts



\### Technical Approach:

```python

result = model.transcribe(

&nbsp;   audio\_path,

&nbsp;   task='translate',      # Force English translation

&nbsp;   language='kn',         # Source: Kannada

&nbsp;   word\_timestamps=True,

&nbsp;   fp16=False            # Better quality

)

```



\### Key Achievement:

Successfully forced Whisper to output \*\*pure English\*\* instead of mixed Kannada/English by using `task='translate'` parameter.



---



\## ✅ Day 2: COMPLETE - Hindi Translation  



\### Results:

\- \*\*Source:\*\* Clean English (68 segments)

\- \*\*Output:\*\* Hindi Devanagari script

\- \*\*Method:\*\* Google Translate (googletrans)

\- \*\*Success rate:\*\* 68/68 (100%) ✅

\- \*\*Processing time:\*\* ~4 minutes

\- \*\*Cost:\*\* $0.00 (FREE)



\### Sample Output:

> अब देखते हैं कि बच्चों की मालिश या मसाज कैसे करें सबसे पहले हमें मालिश के लिए सामग्री तैयार करनी होगी...



\### Why Google Translate:

\- ✅ Zero cost for proof-of-concept

\- ✅ No API setup complexity

\- ✅ Reliable and fast

\- ✅ Good quality for training content

\- ✅ Can upgrade to GPT-4/Gemini for production



---



\## 📊 Progress Summary



| Day | Task | Status | Time | Output |

|-----|------|--------|------|--------|

| 1 | Audio + Transcription | ✅ | 10.8 min | 68 English segments |

| 2 | Hindi Translation | ✅ | 4 min | 68 Hindi segments |

| 3 | Text-to-Speech | ⏳ | - | Hindi audio |

| 4-5 | Lip Sync | ⏳ | - | Synced video |

| 6 | Integration | ⏳ | - | Final pipeline |

| 7 | Documentation | ⏳ | - | Loom + GitHub |



\*\*Total time so far:\*\* ~15 minutes of processing time  

\*\*Days completed:\*\* 2/7 (29%)  



---



\## 🎯 Next: Day 3 - Text-to-Speech



Generate natural Hindi audio from translated text using:

\- Option 1: ElevenLabs (high quality, paid)

\- Option 2: Google TTS (free, good quality)

\- Option 3: gTTS (free, basic quality)



\*\*Goal:\*\* Convert Hindi text → Hindi audio with proper timing



---



\## 📁 Project Structure

```

supernan-dubbing-pipeline/

├── data/

│   ├── input\_video.mp4           # Original Kannada video

│   ├── extracted\_audio.wav       # Extracted audio

│   ├── transcript.json           # English translation

│   └── transcript\_hindi.json     # Hindi translation ✅

├── src/

│   ├── day1\_english\_only.py      # Clean English extraction

│   ├── day2\_translation\_free.py  # Hindi translation

│   └── ...

├── .env                          # API keys (gitignored)

├── .gitignore

├── README.md

└── requirements.txt

```



---



\## 🔑 Key Learnings



1\. \*\*Whisper Translation Mode:\*\* Using `task='translate'` forces clean English output from any language

2\. \*\*ASCII Filtering:\*\* Remove non-English characters for clean text pipeline

3\. \*\*Free Tools:\*\* Google Translate works well for MVP/proof-of-concept

4\. \*\*Pragmatic Decisions:\*\* Sometimes simpler solutions are better than complex APIs



---



\## 🚀 Technologies Used



\- \*\*Audio:\*\* ffmpeg, Whisper (medium model)

\- \*\*Translation:\*\* Google Translate (googletrans)

\- \*\*Python:\*\* 3.12.7

\- \*\*Version Control:\*\* Git with detailed commits

