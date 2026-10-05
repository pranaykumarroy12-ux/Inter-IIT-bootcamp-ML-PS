# Developer & Engineering Architecture Guide (DEV_GUIDE.md)

> **Document Purpose:** This is an internal technical reference for developers and coding agents working on the AI-Powered Meeting Assistant project (Inter-IIT Bootcamp ML PS). It documents the current codebase, architectural decisions, model integrations, data flows, and strict development guardrails.

---

## A. PROJECT STATE

- **Stage 1 (Speech-to-Text):** `DONE` — Implemented in `src/stt/transcriber.py` using `faster-whisper` (`large-v3-turbo`) with int8 quantization on CPU. Lazy loading enabled. Independently verified with tests.
- **Stage 2 (Domain-Aware Refinement):** `DONE` — Implemented in `src/refinement/refiner.py` using Google Gemini (`gemini-3.5-flash-lite`) via `google-genai` SDK. Prompt template externalized to `prompts/stage2_refine.txt`. Independently verified with tests.
- **Stage 1 → Stage 2 Pipeline Connection:** `DONE` — Implemented in `src/pipeline/workflow.py` (`MeetingPipeline`).
- **Stage 3 (Meeting Documentation & Task Extraction):** `DONE` — Implemented in `src/summarization/summarizer.py`. Model selection and structured schema design required before coding.
- **Interactive UI (Streamlit):** `NOT STARTED` — Scheduled for Checkpoint 7 (`app.py`).
- **Output / Export Generation:** `NOT STARTED` — Scheduled for Checkpoint 10.
- **Current Blockers:** None.

---

## B. REQUIREMENT → IMPLEMENTATION MAP

| PS Requirement | Implementation Strategy | File(s) | Status |
|---|---|---|---|
| **Audio Input & Validation** | Validate file existence, >0 bytes size, supported extensions (`.mp3`, `.wav`, `.mpeg`, etc.) with clear error messaging. | `src/utils/audio.py` | **Complete** |
| **Stage 1: Speech-to-Text** | Transcribe spoken English meeting audio to verbatim raw transcript using `faster-whisper` `large-v3-turbo`. | `src/stt/transcriber.py`, `stt.py` | **Complete** |
| **Raw Transcript Review** | Keep raw transcript separate and intact before any post-processing. | `src/pipeline/workflow.py`, `src/stt/transcriber.py` | **Complete** |
| **Stage 2: Domain-Aware Refinement** | Refine raw transcript to fix domain terms, acronyms, and phonetic misrecognitions while strictly preserving names, numbers, negations, and intent. | `src/refinement/refiner.py`, `prompts/stage2_refine.txt`, `refine.py` | **Complete** |
| **Distinct Language-Model Stages** | Stage 2 (refinement) and Stage 3 (minutes/tasks) must be decoupled as independent model calls with separate prompts and responsibilities. | `src/refinement/`, `src/summarization/`, `src/pipeline/` | **Enforced in Architecture** |
| **Stage 3: Concise Meeting Summary & Minutes** | Synthesize refined transcript into organized account of discussion points. | `src/summarization/summarizer.py` | *Complete* |
| **Stage 3: Key Decisions Extraction** | Record only agreed-upon decisions; proposals/suggestions must not be marked as decisions; empty list if none reached. | `prompts/stage3_document.txt`, `src/summarization/summarizer.py` | *Complete* |
| **Stage 3: Actionable Tasks Extraction** | Record task description, owner, and deadline. If owner or deadline not stated, mark explicitly as `unspecified`. No unstated assignments. | `prompts/stage3_document.txt`, `src/summarization/summarizer.py` | *Complete* |
| **Dual Format Records** | Produce final meeting record in both human-readable Markdown and machine-readable structured JSON conveying identical information. | `src/summarization/summarizer.py`, `outputs/` | *Complete & 10* |
| **Interactive Interface** | Web application allowing audio upload, processing trigger, progress status, transcript inspection, and download buttons. | `app.py` | *Pending Checkpoint 7* |
| **Downloadable Outputs** | Export buttons for raw transcript, refined transcript, minutes, decisions, and action items in JSON and Markdown. | `app.py`, `src/pipeline/workflow.py` | *Pending Checkpoint 10* |
| **Submission Quality & Reproducibility** | Full instructions, requirements, setup scripts, sample audio, and verification tests. | `README.md`, `DEV_GUIDE.md`, `requirements.txt`, `tests/` | **Complete** |

---

## C. CURRENT ARCHITECTURE

```
+-------------------------------------------------------------------------------+
| STAGE 1: SPEECH-TO-TEXT                                                       |
| File: src/stt/transcriber.py                                                  |
|                                                                               |
|   Input:  Audio file path (.wav, .mp3, .mpeg, .m4a, etc.)                     |
|           ↓                                                                   |
|   Logic:  validate_audio_file() -> WhisperModel("large-v3-turbo")            |
|           beam_size=5, vad_filter=True, device="cpu", compute_type="int8"     |
|           ↓                                                                   |
|   Output: Raw Transcript string                                               |
+---------------------------------------+---------------------------------------+
                                        |
                                        v
+-------------------------------------------------------------------------------+
| STAGE 2: DOMAIN-AWARE TRANSCRIPT REFINEMENT                                   |
| File: src/refinement/refiner.py                                               |
|                                                                               |
|   Input:  Raw Transcript string                                               |
|           ↓                                                                   |
|   Logic:  load_refinement_prompt() from prompts/stage2_refine.txt             |
|           client = genai.Client(api_key=GEMINI_API_KEY)                       |
|           client.models.generate_content("gemini-3.5-flash-lite")             |
|           Rules: Fix technical jargon; preserve names, numbers, negations;    |
|                  zero hallucinations or additions                             |
|           ↓                                                                   |
|   Output: Refined Transcript string                                           |
+---------------------------------------+---------------------------------------+
                                        |
                                        v
+-------------------------------------------------------------------------------+
| STAGE 3: MEETING DOCUMENTATION (PENDING IMPLEMENTATION)                       |
| File: src/summarization/summarizer.py                                         |
|                                                                               |
|   Input:  Refined Transcript string                                           |
|           ↓                                                                   |
|   Logic:  Structured prompt execution (Pydantic schema validation)            |
|           Extract: summary, minutes, agreed decisions, action items           |
|           Enforce: unstated owner/deadline -> "unspecified"                   |
|           ↓                                                                   |
|   Output: Structured record (JSON) + Formatted text (Markdown)                |
+-------------------------------------------------------------------------------+
```

---

## D. FILE-BY-FILE GUIDE

### 1. `src/utils/config.py`
- **Purpose:** Central management of project paths (`PROJECT_ROOT`, `PROMPTS_DIR`, `ASSETS_DIR`, `OUTPUTS_DIR`) and environment secrets.
- **Main Functions:** `get_gemini_api_key() -> str`.
- **Inputs:** OS environment variables and `.env` file.
- **Outputs:** Resolved paths and validated API key string.
- **Dependencies:** `pathlib`, `os`, `python-dotenv`.
- **Callers:** `src/refinement/refiner.py`, `tests/test_refine.py`, `stt.py`.
- **Status:** Complete.
- **Critical Guardrail:** Do NOT hardcode API keys or system-dependent absolute path prefixes here.

### 2. `src/utils/audio.py`
- **Purpose:** Audio input validation and format checking to satisfy the PS requirement of handling empty/unreadable/unsupported files with clear messages.
- **Main Functions:** `validate_audio_file(file_path: str | Path) -> Tuple[bool, str]`.
- **Inputs:** File path.
- **Outputs:** Boolean flag and user-friendly explanation string.
- **Dependencies:** `pathlib`.
- **Callers:** `src/stt/transcriber.py`, `src/pipeline/workflow.py`, `tests/test_stt.py`.
- **Status:** Complete.

### 3. `src/stt/transcriber.py`
- **Purpose:** Executes Stage 1 Speech-to-Text using `faster-whisper`.
- **Main Functions:**
  - `get_whisper_model(...) -> WhisperModel`: Singleton lazy loader for the model to prevent massive RAM usage on import.
  - `transcribe_audio(audio_file, ...) -> str`: Performs transcription with VAD filtering and beam search.
- **Inputs:** Audio file path.
- **Outputs:** Plain text raw transcript string.
- **Dependencies:** `faster_whisper`, `src.utils.audio`, `src.utils.config`.
- **Callers:** `stt.py`, `src/pipeline/workflow.py`, `tests/test_stt.py`.
- **Status:** Complete.
- **Critical Guardrail:** Do NOT instantiate `WhisperModel` at module level; keep lazy loading. Do not alter `compute_type="int8"` on CPU as it prevents out-of-memory errors.

### 4. `src/refinement/refiner.py`
- **Purpose:** Executes Stage 2 domain-aware transcript correction via Google Gemini.
- **Main Functions:**
  - `load_refinement_prompt(raw_text: str) -> str`: Loads prompt template from file (with code fallback).
  - `refine_transcript(raw_text: str, model_name: str, client=None) -> str`: Invokes Gemini API and returns cleaned transcript.
- **Inputs:** Raw transcript string.
- **Outputs:** Refined transcript string.
- **Dependencies:** `google-genai`, `src.utils.config`.
- **Callers:** `refine.py`, `src/pipeline/workflow.py`, `tests/test_refine.py`.
- **Status:** Complete.
- **Critical Guardrail:** Ensure prompt enforces strict preservation of negations ("not", "never", "don't") and numeric values.

### 5. `src/summarization/summarizer.py`
- **Purpose:** Stage 3 Meeting documentation generator (Minutes, Decisions, Action Items).
- **Main Functions:** `generate_meeting_documentation(refined_transcript: str)` (currently raises `NotImplementedError`).
- **Inputs:** Refined transcript string.
- **Outputs:** Expected: Dictionary / Pydantic model with structured minutes, decisions, and tasks.
- **Dependencies:** `pydantic`, LLM SDK.
- **Callers:** `summarize.py`, `src/pipeline/workflow.py`.
- **Status:** Not implemented yet. (Reserved for Checkpoint 5).

### 6. `src/pipeline/workflow.py`
- **Purpose:** End-to-end pipeline coordinator tying all stages together.
- **Main Functions:** `MeetingPipeline.run_pipeline(audio_path)`.
- **Inputs:** Audio file path.
- **Outputs:** Dictionary containing `raw_transcript`, `refined_transcript`, and `documentation`.
- **Dependencies:** `src.stt.transcriber`, `src.refinement.refiner`, `src.summarization.summarizer`.
- **Status:** In Progress (Stages 1 and 2 wired; Stage 3 pending).

### 7. `prompts/stage2_refine.txt`
- **Purpose:** Contains the exact prompt engineering instructions for Stage 2 transcript cleaning.
- **Status:** Complete.

### 8. `prompts/stage3_document.txt`
- **Purpose:** Draft specification and prompt template for Stage 3 documentation and task extraction.
- **Status:** Draft / Specification for Checkpoint 5.

### 9. Root Convenience Scripts (`stt.py`, `refine.py`, `summarize.py`, `app.py`)
- **Purpose:** Root-level scripts allowing direct command-line execution or Streamlit launch while delegating core logic to `src/`.

---

## E. DATA FLOW

```
[ User provides Audio File (.mp3/.wav/.mpeg) ]
                       │
                       ▼
            src/utils/audio.py
         (validate_audio_file)
                       │ (valid format & size > 0)
                       ▼
           src/stt/transcriber.py
             (transcribe_audio)
                       │
               [ RAW TRANSCRIPT ]
                       │
                       ▼
          src/refinement/refiner.py
            (refine_transcript)
          uses prompts/stage2_refine.txt
                       │
             [ REFINED TRANSCRIPT ]
                       │
                       ▼
       src/summarization/summarizer.py  (Stage 3: Pending)
         (generate_meeting_documentation)
          uses prompts/stage3_document.txt
                       │
         [ STRUCTURED MEETING RECORD ]
         ├── Summary & Minutes
         ├── Decisions List (confirmed only)
         └── Action Items List (owner/deadline or 'unspecified')
                       │
                       ▼
       app.py / outputs/ export generation
         ├── Export JSON (machine-readable)
         └── Export Markdown (human-readable)
```

---

## F. MODEL GUIDE

### Stage 1: Speech-to-Text (STT) Model
- **Model Identifier:** `mobiuslabsgmbh/faster-whisper-large-v3-turbo` (via `faster-whisper` library)
- **Role:** High-accuracy transcription of English conversational speech into verbatim raw text.
- **Why Selected:** Whisper `large-v3-turbo` provides near-identical accuracy to Whisper `large-v3` but operates up to 4x faster with significantly reduced memory footprint. Using `faster-whisper` (CTranslate2) allows efficient execution on both CPU (`int8`) and GPU (`float16`).
- **Current Runtime Configuration:**
  - Device: `cpu`
  - Compute Type: `int8`
  - Beam Size: 5
  - VAD Filter: Enabled (`vad_filter=True`)
  - Local Cache: Pre-downloaded in HuggingFace cache (`~1.6 GB`).

### Stage 2: Transcript Refinement Model
- **Model Identifier:** `gemini-3.5-flash-lite` (Google Gemini API via `google-genai` SDK)
- **Role:** Contextual correction of phonetic errors, technical jargon, and domain-specific acronyms in the raw transcript.
- **Why Selected:** Fast inference latency, low cost/quota usage, and strong instruction-following for zero-shot text correction without semantic drift.
- **Prompt:** Defined in `prompts/stage2_refine.txt`.
- **Input:** Raw transcript text string.
- **Output:** Cleaned transcript string.

### Stage 3: Meeting Documentation Model
- **Model Identifier:** *Not implemented/selected yet.*
- **Role:** Synthesis of the refined transcript into concise minutes, verified key decisions, and actionable tasks.
- **Candidate Options for Checkpoint 4 Decision:**
  - Option A: `gemini-3.5-flash` or `gemini-2.5-flash` with Pydantic structured output (`response_schema`).
  - Option B: `gemini-3.5-flash-lite` with JSON schema enforcement.
  - Option C: Local HuggingFace LLM (e.g., Llama-3 / Qwen-2.5) via `transformers` (heavy on CPU).

---

## G. PROMPT GUIDE

### Storage Location
All prompt templates are stored externally in the `prompts/` directory:
- `prompts/stage2_refine.txt`: Stage 2 Refinement Prompt
- `prompts/stage3_document.txt`: Stage 3 Documentation Prompt Specification

### Stage 2 Prompt Analysis
- **Location:** `prompts/stage2_refine.txt`
- **Variable Placeholder:** `{raw_text}`
- **Core Directives:**
  1. Correct obvious STT misrecognitions and technical jargon.
  2. Preserve exact meaning, names, dates, numbers, and facts.
  3. Never guess or invent numbers that are unclear.
  4. Preserve all negations (`not`, `never`, `don't`).
  5. Return only the refined transcript text (no conversational preamble or commentary).
- **Anti-Hallucination Guardrail:** Strict prohibition against adding facts not present in the raw text.

### Stage 3 Prompt Specification (Upcoming)
- **Location:** `prompts/stage3_document.txt`
- **Variable Placeholder:** `{refined_transcript}`
- **Core Directives:**
  1. Produce concise summary and organized meeting minutes.
  2. Extract only agreed-upon decisions. Suggestions or unresolved debates must NOT be marked as decisions.
  3. Extract action items. When an owner or deadline is not explicitly articulated in the text, record `"unspecified"`. Never invent names or dates.
  4. Dual output matching: JSON and Markdown must reflect identical content.

---

## H. CHECKPOINTS & ROADMAP

- [x] **CHECKPOINT 0 — Project Setup & Audit:** Repository audit, environment setup, package listing, and directory restructuring.
- [x] **CHECKPOINT 1 — STT Working Independently:** `src/stt/transcriber.py` verified with unit tests and sample audio.
- [x] **CHECKPOINT 2 — Stage 2 LLM Working Independently:** `src/refinement/refiner.py` verified with Gemini API and domain test inputs.
- [x] **CHECKPOINT 3 — Stage 1 → Stage 2 Integration:** `MeetingPipeline` orchestrating raw STT output directly into refinement model.
- [x] **CHECKPOINT 4 — Stage 3 LLM Selection:** Formalize model selection and API approach for meeting minutes and task extraction.
- [x] **CHECKPOINT 5 — Stage 3 Implementation:** Build `src/summarization/summarizer.py` with structured schema enforcement (Pydantic).
- [ ] **CHECKPOINT 6 — Full Pipeline Integration:** Connect Stage 1 -> Stage 2 -> Stage 3 end-to-end with validation.
- [ ] **CHECKPOINT 7 — Streamlit UI:** Build interactive interface in `app.py` with file upload, live progress indicators, and transcript views.
- [ ] **CHECKPOINT 8 — Error Handling & Edge Cases:** Robust handling of empty files, noisy audio, API rate limits, and network dropouts.
- [ ] **CHECKPOINT 9 — Testing & Verification:** End-to-end integration tests on sample meeting recordings.
- [ ] **CHECKPOINT 10 — Output / Download Functionality:** Dual format export buttons (JSON and Markdown download).
- [x] **CHECKPOINT 11 — Documentation:** Comprehensive `README.md` and `DEV_GUIDE.md`.
- [ ] **CHECKPOINT 12 — Final PS Compliance Audit:** Verification against the 100-point evaluation rubric prior to submission.

---

## I. CURRENTLY COMPLETED WORK

1. **Problem Statement Analysis:** Complete extraction of all rules, evaluation rubric (100 pts), deliverables, and constraints from `ML Bootcamp.pdf`.
2. **Project Reorganization:** Restructured flat directory into clean `src/` modular layout with `stt`, `refinement`, `summarization`, `pipeline`, and `utils`.
3. **Stage 1 (STT):** Encapsulated `faster-whisper-large-v3-turbo` with lazy loading, audio validation, int8 quantization, and independent test runner.
4. **Stage 2 (Refinement):** Encapsulated `gemini-3.5-flash-lite` with externalized prompt template (`prompts/stage2_refine.txt`) and independent test runner.
5. **Sample Audio Relocation:** Moved `whatsapp-audio-2026-10-04-at-50909-pm_Sgw8gMZq.mp3` to `assets/audio/` using `git mv` to preserve Git history.
6. **Environment & Git Hygiene:** Created `.env.example`, updated `.gitignore` for Python artifacts and outputs, and added `google-genai` to `requirements.txt`.
7. **Regression Testing:** Both `tests/test_stt.py` and `tests/test_refine.py` execute and pass cleanly.

---

## J. REMAINING WORK

### Priority 1: Required for PS (Core Functionality)
1. **Checkpoint 4 & 5 (Stage 3):** Implement meeting minutes, key decisions, and actionable task extraction with schema validation and strict "unspecified" enforcement for missing owners/deadlines.
2. **Checkpoint 6 (Pipeline Integration):** Complete `run_pipeline` connecting all 3 stages.
3. **Checkpoint 7 (Interactive UI):** Implement Streamlit app (`app.py`) allowing audio upload, pipeline execution, transcript review, and results visualization.
4. **Checkpoint 10 (Downloads):** Provide JSON and Markdown download functionality.

### Priority 2: Important for Robustness
1. **API Error Handling & Retries:** Wrap Gemini API calls in `tenacity` retry logic with exponential backoff for rate limits.
2. **Chunking for Long Transcripts:** Add token/character chunking if transcripts exceed LLM context or single-call limits.
3. **CUDA Device Detection:** Auto-detect GPU availability to switch Whisper to CUDA float16 when available.

### Priority 3: Optional Improvements
1. **Speaker Diarization:** Experiment with `pyannote.audio` if speaker segmentation is desired.
2. **Audio Waveform / Playback:** Add audio player widget in Streamlit UI.

---

## K. KNOWN BUGS / RISKS

1. **CPU Execution Latency:** Whisper `large-v3-turbo` on CPU requires ~1.5x–3x real-time duration. For a 2-minute audio recording, transcription takes several minutes on CPU. Users must be notified with clear progress spinners in the UI.
2. **Gemini Automatic Function Calling Warning:** The SDK generates a minor warning: `"Direct use of automatic function calling (AFC) in Models.generate_content is not recommended"`. This is purely an SDK notice and does not affect text generation, but can be silenced or addressed via clean configuration.
3. **Free-Tier API Rate Limits:** Google Gemini free-tier keys are subject to Requests Per Minute (RPM) and Requests Per Day (RPD) limits. Repeated rapid tests may trigger 429 quota exhaustion.
4. **Windows Path Separators:** Always use `pathlib.Path` or raw strings to avoid Windows backslash escaping errors.

---

## L. TESTING STRATEGY

### Unit & Stage Tests
- **Audio Validation:** Test with non-existent file, empty file (0 bytes), invalid extensions (`.txt`, `.xyz`), and valid audio files.
- **Stage 1 STT:** Test model loading, parameter passing, and transcription on short audio clips.
- **Stage 2 Refinement:** Test with known noisy transcripts containing domain acronyms (e.g., UART, microcontrollers) to verify technical term correction and preservation of numbers/negations.

### Stage 3 & Anti-Hallucination Tests (Upcoming)
- **Unspecified Metadata Test:** Input a transcript where tasks are mentioned without owners or deadlines. Verify that output explicitly sets `owner: "unspecified"` and `deadline: "unspecified"`.
- **Decision vs. Proposal Test:** Input a transcript where an idea is proposed ("Maybe we should switch to React?") but participants decline ("No, let's stick with Vue"). Verify that React is NOT listed as a key decision.
- **Empty Meeting Test:** Input a conversational recording with no decisions or action items. Verify that decisions and action items return empty lists `[]`.

---

## M. DEVELOPMENT RULES FOR FUTURE CODING AGENTS

1. **Read DEV_GUIDE.md before modifying code.** Never make speculative changes without checking the existing architecture.
2. **Read the relevant PS requirement before implementing a feature.** `ML Bootcamp.pdf` is the primary source of truth.
3. **Do not rewrite working code unnecessarily.** Stage 1 and Stage 2 are working. Do not replace them without explicit justification.
4. **Keep stages modular.** Stages 1, 2, and 3 must remain decoupled and independently runnable.
5. **Keep Stage 1, Stage 2, and Stage 3 independently testable.** Maintain separate test scripts in `tests/`.
6. **Do not hardcode API keys.** Always load keys via `src/utils/config.py` from `.env`.
7. **Do not hardcode meeting outputs.** All pipeline outputs must be dynamically generated by the models.
8. **Do not fabricate owners, deadlines, or decisions.** If missing from the recording, mark as `"unspecified"`.
9. **Update DEV_GUIDE.md when architecture or implementation changes.**
10. **Update README.md when setup or user-facing behavior changes.**
11. **Prefer small incremental changes.** Work checkpoint by checkpoint.
12. **After each significant change, test the affected stage** to ensure zero regressions.
