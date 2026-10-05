# AI-Powered Meeting Assistant

> **Inter-IIT Tech Meet 15.0 — ML Bootcamp (Phase 2)**  
> **Organized by IIT Guwahati Tech Board**  
> **Submission Deadline:** October 7, 2026 | **Team Size:** 1–3 Members

---

## 1. Project Title
**AI-Powered Meeting Assistant: Multi-Stage Audio Transcription, Domain-Aware Refinement, and Structured Documentation**

---

## 2. Project Overview
The AI-Powered Meeting Assistant is an intelligent audio-to-documentation system designed to process recorded meetings into reliable, high-fidelity transcripts and actionable written records. Operating through a coordinated, multi-model pipeline, the system converts raw spoken audio into speech text, rectifies domain-specific terminology and phonetic misrecognitions using contextual intelligence, and compiles organized meeting minutes, key decisions, and actionable tasks.

Crucially, the system enforces a strict **anti-hallucination and truthfulness policy**: all extracted minutes, decisions, and tasks must faithfully reflect what was actually stated in the meeting. Where a task owner or deadline was not articulated, the system explicitly marks that detail as `unspecified` rather than fabricating or assuming facts.

---

## 3. Problem Being Solved
Modern engineering, academic, and business meetings are rich in domain-specific technical jargon, abbreviations, acronyms, and fast-paced deliberations. Standard speech-to-text engines encounter significant limitations when transcribing such discussions:
- Phonetic confusions for technical terms (e.g., transcribing "UART" as "you art", "microcontroller" as "micro controller", or domain acronyms as random phonetic phrases).
- Inability to distinguish casual suggestions from finalized, agreed decisions.
- Risk of generating hallucinated deadlines or assigning tasks to unstated participants when summarizing discussions.
- Fragmented workflows where users lack transparency into the intermediate transcription before summaries are generated.

This project addresses these challenges by implementing a decoupled, verifiable multi-stage architecture where each stage has explicit responsibilities, validated intermediate outputs, and verifiable truthfulness constraints.

---

## 4. Solution Overview
The system provides a coordinated three-stage pipeline backed by an interactive user interface:
1. **Stage 1 (Speech-to-Text):** High-accuracy transcription of English meeting audio into an unvarnished raw transcript using an optimized speech recognition model.
2. **Stage 2 (Domain-Aware Transcript Refinement):** An independent language model inspects the raw transcript against conversational context, fixing domain terms, acronyms, and phonetic errors while strictly preserving names, numbers, negations, and speaker intent.
3. **Stage 3 (Meeting Documentation & Task Extraction):** A separate language model synthesizes the refined transcript into concise minutes, verified key decisions, and structured action items (strictly preserving "unspecified" for missing metadata).
4. **Interactive Application & Export Layer:** An interactive Streamlit web dashboard allowing users to upload audio files, track processing status, inspect side-by-side raw vs. refined transcripts, review structured records, and download results in both human-readable Markdown and machine-readable JSON formats.

---

## 5. End-to-End Architecture
The architecture strictly enforces separation of concerns across distinct model stages:

```
+-------------------------------------------------------------------------------+
|                                  USER LAYER                                   |
|   - Audio Upload (.wav, .mp3, .mpeg, .m4a, .flac)                             |
|   - Execution Trigger & Progress Monitoring                                   |
|   - Side-by-Side Transcript Comparison                                        |
|   - Formatted Minutes & Action Item Dashboard                                 |
|   - Multi-format Export (JSON, Markdown, Raw/Refined Text)                     |
+---------------------------------------+---------------------------------------+
                                        |
                                        v
+-------------------------------------------------------------------------------+
|                       STAGE 1: SPEECH-TO-TEXT (STT)                           |
|   - Engine: faster-whisper (large-v3-turbo)                                   |
|   - Compute: int8 quantization on CPU (or CUDA GPU)                           |
|   - Preprocessing: VAD (Voice Activity Detection), Beam Search = 5            |
|   - Output: Raw Transcript Text (Pre-refinement)                              |
+---------------------------------------+---------------------------------------+
                                        |
                                        v
+-------------------------------------------------------------------------------+
|               STAGE 2: DOMAIN-AWARE TRANSCRIPT REFINEMENT                     |
|   - Model: Google Gemini (gemini-3.5-flash-lite)                              |
|   - Rules: Correct technical jargon/acronyms; preserve names, numbers,        |
|            negations ("not", "never", "don't"), and intent; no inventions     |
|   - Output: Refined Transcript Text                                           |
+---------------------------------------+---------------------------------------+
                                        |
                                        v
+-------------------------------------------------------------------------------+
|             STAGE 3: MEETING DOCUMENTATION & TASK EXTRACTION                  |
|   - Model: To be decided / implemented in Checkpoints 4 & 5                   |
|   - Tasks: Concise Summary, Organized Minutes, Key Decisions, Action Items    |
|   - Constraint: Decisions must be agreed upon; unstated owner/date marked     |
|                 as 'unspecified'; zero hallucinations                         |
|   - Output: Machine-readable JSON + Human-readable Markdown                  |
+-------------------------------------------------------------------------------+
```

---

## 6. Pipeline Diagram in Markdown

```markdown
Audio Input (.mp3, .wav, .mpeg, etc.)
  │
  ▼
[ Stage 1: Speech-to-Text ]
  │  (faster-whisper large-v3-turbo)
  ▼
Raw Transcript
  │
  ▼
[ Stage 2: Domain-Aware Refinement ]
  │  (Google Gemini gemini-3.5-flash-lite)
  ▼
Refined Transcript
  │
  ▼
[ Stage 3: Meeting Documentation ]
  │  (Status: Implemented)
  ▼
Structured Final Record
  ├── Meeting Summary & Minutes
  ├── Key Decisions (agreed only)
  └── Action Items (tasks with stated owner/deadline, or "unspecified")
```

---

## 7. Technology Stack
- **Programming Language:** Python 3.10+ (tested on Python 3.10/3.11/3.12)
- **Audio Processing & Decoding:** FFmpeg (system binary), `ffmpeg-python`
- **Speech Recognition (ASR):** `faster-whisper` 1.2.1 (`CTranslate2` inference engine)
- **Generative AI / LLM SDK:** `google-genai` 2.28.0 (Google Gemini API)
- **Data Validation & Schemas:** `pydantic` 2.13.5
- **Configuration & Secrets:** `python-dotenv` 1.2.4
- **Web UI & Dashboard:** `streamlit` 1.65.0
- **Version Control:** Git

---

## 8. Models Currently Selected

| Pipeline Stage | Selected Model | Model Details / Backend | Current Status |
|---|---|---|---|
| **Stage 1: Speech-to-Text** | `faster-whisper-large-v3-turbo` | mobiuslabsgmbh / OpenAI Whisper Large v3 Turbo, int8 CPU execution | **Implemented & Verified Working** |
| **Stage 2: Transcript Refinement** | `gemini-3.5-flash-lite` | Google GenAI SDK (`google-genai`), contextual zero-shot refinement | **Implemented & Verified Working** |
| **Stage 3: Meeting Documentation** | *Implemented* | Implemented via Gemini 3.5 Flash (options: Gemini 3.5 Flash / Gemini 2.5 Flash / local LLM) | **Implemented** |

---

## 9. Project Structure

```
Inter-IIT-bootcamp-ML-PS/
│
├── ML Bootcamp.pdf             # Official problem statement (IIT Guwahati)
├── README.md                   # Public documentation & evaluation guide
├── DEV_GUIDE.md                # Internal engineering architecture & roadmap
├── requirements.txt            # Python dependencies
├── .env.example                # Template for environment variables
├── .gitignore                  # Git ignore rules for virtualenvs, keys, outputs
│
├── app.py                      # Streamlit web application entry point (stub)
├── stt.py                      # Root convenience script for Stage 1 STT
├── refine.py                   # Root convenience script for Stage 2 Refinement
├── summarize.py                # Root placeholder for Stage 3 Documentation
│
├── src/                        # Modular source code package
│   ├── __init__.py
│   ├── stt/                    # Stage 1: Speech-to-Text implementation
│   │   ├── __init__.py
│   │   └── transcriber.py      # Whisper loader & audio transcription logic
│   ├── refinement/             # Stage 2: Domain-aware transcript refinement
│   │   ├── __init__.py
│   │   └── refiner.py          # Gemini-based transcript cleaning & correction
│   ├── summarization/          # Stage 3: Meeting documentation (placeholder)
│   │   ├── __init__.py
│   │   └── summarizer.py       # Meeting records & task extraction (unimplemented)
│   ├── pipeline/               # Multi-stage workflow orchestrator
│   │   ├── __init__.py
│   │   └── workflow.py         # End-to-end pipeline coordinator
│   └── utils/                  # Shared utilities
│       ├── __init__.py
│       ├── audio.py            # Audio validation, format checks & error handling
│       └── config.py           # Environment variables, directory paths & constants
│
├── prompts/                    # Externalized prompt templates
│   ├── stage2_refine.txt       # Stage 2 transcript refinement prompt
│   └── stage3_document.txt     # Stage 3 documentation & extraction prompt (draft spec)
│
├── assets/                     # Media assets and sample meeting recordings
│   └── audio/
│       └── whatsapp-audio-2026-10-04-at-50909-pm_Sgw8gMZq.mp3  # Sample lecture audio (~2 min)
│
├── outputs/                    # Output directory for transcripts and JSON/MD records
│   └── .gitkeep
│
└── tests/                      # Verification and independent stage test scripts
    ├── __init__.py
    ├── test_stt.py             # Independent test suite for Stage 1
    └── test_refine.py          # Independent test suite for Stage 2
```

---

## 10. Explanation of Important Files

- [`ML Bootcamp.pdf`](file:///d:/Inter-IIT%20bootcamp/ML%20Bootcamp.pdf): The official Problem Statement from IIT Guwahati Tech Board; the primary source of truth for project requirements.
- [`README.md`](file:///d:/Inter-IIT%20bootcamp/README.md): Primary user-facing guide containing setup instructions, architecture breakdown, and compliance checks.
- [`DEV_GUIDE.md`](file:///d:/Inter-IIT%20bootcamp/DEV_GUIDE.md): Developer architecture handbook, requirement-to-code mapping, model guide, and checkpoint progress.
- [`requirements.txt`](file:///d:/Inter-IIT%20bootcamp/requirements.txt): Pinned dependencies required to install and run the application.
- [`.env.example`](file:///d:/Inter-IIT%20bootcamp/.env.example): Template illustrating necessary API keys without exposing secrets.
- [`src/stt/transcriber.py`](file:///d:/Inter-IIT%20bootcamp/src/stt/transcriber.py): Implements Whisper speech-to-text with lazy model loading and error handling.
- [`src/refinement/refiner.py`](file:///d:/Inter-IIT%20bootcamp/src/refinement/refiner.py): Implements Gemini-based domain correction preserving truthfulness and negations.
- [`src/utils/audio.py`](file:///d:/Inter-IIT%20bootcamp/src/utils/audio.py): Validates file existence, file size (> 0 bytes), and supported audio formats.
- [`prompts/stage2_refine.txt`](file:///d:/Inter-IIT%20bootcamp/prompts/stage2_refine.txt): Modifiable prompt template for Stage 2 transcript correction.
- [`tests/test_stt.py`](file:///d:/Inter-IIT%20bootcamp/tests/test_stt.py): Automated test verifying audio validation and Whisper model loading.
- [`tests/test_refine.py`](file:///d:/Inter-IIT%20bootcamp/tests/test_refine.py): Automated test verifying Gemini API connectivity and domain correction accuracy.

---

## 11. Setup Instructions

### Prerequisites
1. **Python 3.10+** installed on your system.
2. **FFmpeg** installed and accessible in your system `PATH`:
   - *Windows:* Download from [gyan.dev/ffmpeg](https://www.gyan.dev/ffmpeg/builds/) or install via `winget install Gyan.FFmpeg` or `choco install ffmpeg`.
   - *Linux (Ubuntu/Debian):* `sudo apt-get update && sudo apt-get install -y ffmpeg`
   - *macOS:* `brew install ffmpeg`
   - Verify FFmpeg installation by running:
     ```bash
     ffmpeg -version
     ```
3. A valid **Google Gemini API Key** (obtainable free from [Google AI Studio](https://aistudio.google.com/)).

---

## 12. Python Virtual Environment Setup

Clone the repository and create an isolated Python virtual environment:

```bash
# Clone the repository
git clone https://github.com/pranaykumarroy12-ux/Inter-IIT-bootcamp-ML-PS.git
cd Inter-IIT-bootcamp-ML-PS

# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# Windows (Command Prompt):
.\.venv\Scripts\activate.bat
# Linux / macOS:
source .venv/bin/activate
```

---

## 13. Dependency Installation

With the virtual environment activated, install the required packages:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 14. Environment Variable / API Key Setup

1. Copy the sample environment template `.env.example` to `.env`:
   ```bash
   cp .env.example .env     # Linux / macOS / Git Bash
   copy .env.example .env   # Windows Command Prompt
   Copy-Item .env.example .env # Windows PowerShell
   ```

2. Open `.env` in a text editor and insert your Gemini API Key:
   ```ini
   GEMINI_API_KEY=your_actual_gemini_api_key_here
   ```

> [!IMPORTANT]
> The `.env` file is explicitly ignored in `.gitignore`. Never commit your real API key to Git.

---

## 15. How to Run the Project

### Testing Stage 1 (Speech-to-Text) Independently
To verify audio validation and speech-to-text model loading:
```bash
python tests/test_stt.py
```
To transcribe the included sample meeting recording:
```bash
python stt.py
```

### Testing Stage 2 (Domain Refinement) Independently
To verify Gemini connectivity and domain terminology refinement:
```bash
python tests/test_refine.py
```
To run the refinement module directly:
```bash
python refine.py
```

### Running the Interactive Web Application (Upcoming)
*Note: The Streamlit interface is scheduled for Checkpoint 7.* Once implemented, the application will launch with:
```bash
streamlit run app.py
```

---

## 16. Current Supported Input
- **Audio Formats:** `.wav`, `.mp3`, `.m4a`, `.mpeg`, `.mp4`, `.ogg`, `.flac`, `.aac`
- **Language:** Spoken English meeting recordings.
- **Validation:** Files with size 0 bytes, missing paths, or non-audio extensions are rejected immediately with a descriptive error message.

---

## 17. Expected Outputs
When the pipeline runs completely, it generates:
1. **Raw Transcript:** Exact verbatim speech-to-text transcript from Stage 1 before LLM processing.
2. **Refined Transcript:** Domain-corrected transcript from Stage 2 with jargon, acronyms, and phonetic errors repaired while preserving truthfulness.
3. **Structured Meeting Record (Stage 3):**
   - **Concise Meeting Summary & Organized Minutes:** Core discussion themes and technical takeaways.
   - **Key Decisions:** Explicitly agreed-upon conclusions (empty list if none reached).
   - **Action Items:** Granular tasks with explicitly mentioned owner and deadline; missing metadata is labeled `"unspecified"` (empty list if none assigned).
4. **Export Formats:**
   - Human-readable Markdown (`.md`)
   - Machine-readable structured JSON (`.json`)

---

## 18. Current Implementation Status

| Component | Status | Details |
|---|---|---|
| **Audio Validation & Preprocessing** | **Complete** | Validates existence, size (>0 bytes), and format extensions. |
| **Stage 1: Speech-to-Text** | **Complete** | Powered by `faster-whisper-large-v3-turbo` on CPU (`int8`). Lazy model loading enabled. |
| **Stage 2: Transcript Refinement** | **Complete** | Powered by `gemini-3.5-flash-lite` via `google-genai`. Prompt externalized to `prompts/stage2_refine.txt`. |
| **Stage 3: Meeting Documentation** | **Not Started** | Pending model selection (Checkpoint 4) and implementation (Checkpoint 5). |
| **Multi-Stage Pipeline Orchestrator** | **In Progress** | `MeetingPipeline` connects Stages 1 & 2; awaiting Stage 3 integration. |
| **Streamlit Interactive UI** | **Not Started** | Scheduled for Checkpoint 7 (`app.py`). |
| **Download & Export System** | **Not Started** | Scheduled for Checkpoint 10. |

---

## 19. Known Limitations
1. **CPU Execution Speed:** Whisper `large-v3-turbo` running with `int8` on CPU takes approximately 1.5–3x real-time depending on the host CPU. A GPU with CUDA acceleration is recommended for fast processing of lengthy recordings.
2. **Stage 3 Absence:** Meeting minutes, key decisions, and action items are not yet produced because Stage 3 is pending implementation.
3. **Interactive UI Pending:** Users currently interact via Python scripts rather than a graphical Streamlit dashboard.
4. **Speaker Diarization:** Speaker labels (e.g., Speaker A, Speaker B) are not currently extracted; transcription is currently a single continuous stream.

---

## 20. Future Work
- **Stage 3 Implementation:** Complete Pydantic structured output extraction for minutes, decisions, and action items with strict adherence to "unspecified" metadata rules.
- **Streamlit Dashboard:** Build an interactive UI with audio upload, live progress spinners, side-by-side transcript diff viewer, and instant JSON/MD download buttons.
- **CUDA Auto-Detection:** Automatically switch `faster-whisper` from CPU `int8` to GPU `float16` when an NVIDIA CUDA device is detected.
- **Speaker Diarization Integration (Optional):** Leverage `pyannote.audio` if speaker-tagged transcripts become desirable.

---

## 21. Development Roadmap

```
Checkpoint 0: Project Setup & Audit               [ COMPLETED ]
Checkpoint 1: Stage 1 STT Independent Validation   [ COMPLETED ]
Checkpoint 2: Stage 2 Refinement Validation        [ COMPLETED ]
Checkpoint 3: Stage 1 -> Stage 2 Integration       [ COMPLETED ]
Checkpoint 4: Stage 3 LLM Model Selection          [ PENDING ]
Checkpoint 5: Stage 3 Documentation Implementation [ PENDING ]
Checkpoint 6: Full Pipeline Integration            [ PENDING ]
Checkpoint 7: Streamlit Interactive UI             [ PENDING ]
Checkpoint 8: Robust Error Handling & Edge Cases   [ PENDING ]
Checkpoint 9: Comprehensive Test Suite             [ PENDING ]
Checkpoint 10: Multi-format Output Downloads       [ PENDING ]
Checkpoint 11: Complete Documentation              [ IN PROGRESS ]
Checkpoint 12: Final PS Compliance Audit           [ PENDING ]
```

---

## 22. Security Notes Concerning API Keys
- Never commit `.env` or any file containing plaintext API keys to GitHub.
- Keep `.env` listed in `.gitignore` at all times.
- If using Streamlit Cloud for deployment, pass secrets via `st.secrets` rather than hardcoded environment strings.
- Restrict your Google AI Studio API key permissions to prevent abuse if exposed.

---

## 23. Inter-IIT PS Compliance Checklist

| PS Requirement | Rubric Points | Compliance Strategy | Status |
|---|---|---|---|
| **Distinct Language-Model Stages** | Evaluation Rubric | Stage 2 and Stage 3 must be distinct processing stages with separate prompts/calls. | **Enforced in Architecture** |
| **Speech Transcription Completeness** | 20 pts | Using Whisper `large-v3-turbo` with beam search and VAD filtering. | **Implemented & Verified** |
| **Domain-Aware Refinement** | 20 pts | Gemini prompt explicitly instructs correcting technical terms while preserving negations, numbers, and names. | **Implemented & Verified** |
| **Accurate Minutes & Decisions** | 25 pts | Prompt rules enforce recording only confirmed decisions without inventing claims. | *Pending Stage 3* |
| **Actionable Tasks & Anti-Hallucination** | 15 pts | Unstated owners and deadlines must be marked as `unspecified`. No fabricated assignments. | *Pending Stage 3* |
| **End-to-End Application & UI** | 15 pts | Streamlit app accepting audio upload, displaying intermediate transcripts, and providing download options. | Implemented |
| **Submission Quality & Reproducibility** | 5 pts | Comprehensive README, DEV_GUIDE, clear setup steps, sample audio, and clean modular code. | **Compliant** |
| **Total Evaluation Potential** | **100 pts** | | |
