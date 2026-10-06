# AI-Powered Meeting Assistant

> **Inter-IIT Tech Meet 15.0 - ML Bootcamp (Phase 2)**  
> **Organized by IIT Guwahati Tech Board**  
> **Submission Deadline:** October 7, 2026

---

## 1. Project Title
**AI-Powered Meeting Assistant: Multi-Stage Audio Transcription, Domain-Aware Refinement, and Structured Documentation**

---

## 2. Technical Description (Model Architecture & Roles)
This application employs a strict, decoupled three-stage pipeline connecting distinct AI models to ensure speed, accuracy, and truthfulness.

* **Stage 1 (Speech-to-Text):** 
  * **Model:** `whisper-large-v3` (via Groq API)
  * **Role:** Transcribes the uploaded English audio file into a raw, word-for-word transcript at ultra-high speeds (processing hour-long meetings in seconds).
  * **Data Flow:** Audio File → Groq Whisper API → Raw Transcript String.
* **Stage 2 (Domain-Aware Transcript Refinement):** 
  * **Model:** `gemini-3.5-flash-lite` (via Google GenAI SDK)
  * **Role:** Analyzes the raw transcript to correct domain-specific technical jargon, acronyms, and phonetic misrecognitions. It strictly preserves names, numbers, negations, and speaker intent. **Contextual Diarization** is also performed here, where the model logically injects speaker labels (e.g., `Speaker 1:`, `Speaker 2:`) based on conversational shifts.
  * **Data Flow:** Raw Transcript String → Gemini API (Refinement Prompt) → Refined Transcript String.
* **Stage 3 (Meeting Documentation & Task Extraction):** 
  * **Model:** `gemini-3.5-flash-lite` (via Google GenAI SDK with Pydantic Structured Outputs)
  * **Role:** Synthesizes the refined transcript into organized minutes, verified key decisions, and actionable tasks. The model is structurally forced to return `unspecified` if a task owner or deadline is not explicitly stated in the audio, mathematically preventing hallucinations.
  * **Data Flow:** Refined Transcript String → Gemini API (Extraction Prompt + Pydantic Schema) → Structured JSON Record & Markdown.

---

## 3. Features & User Interface
The frontend is a modern, responsive Single Page Application (SPA) built entirely in Streamlit with custom CSS. It features:
- **Performance Metrics:** Real-time tracking of latency and processing speeds for each pipeline stage.
- **Embedded Audio Player:** Listen to the source audio while reviewing the transcript.
- **AI Visual Correction Highlights:** A side-by-side diff viewer that highlights exactly what the AI fixed in green, and what Whisper misspelled in red strikethrough.
- **Structured Downloads:** Export the final results in `.txt` (Raw & Refined), `.pdf` (Professional Meeting Record), and `.json` (Machine-readable structured data).

---

## 4. Setup & Installation

### Prerequisites
- Python 3.10+
- `ffmpeg` installed and added to your system PATH.

### Step 1: Install Dependencies
The project has been heavily optimized for speed and low overhead. It relies on an ultra-lean stack (just Streamlit, Groq, Google GenAI, and Pydantic).
```bash
pip install -r requirements.txt
```

### Step 2: Configure API Keys
The application requires two API keys to run the high-speed pipeline.
Create a `.env` file in the root directory and add your keys:
```env
# Google Gemini API Key for Stage 2 (Refinement) & Stage 3 (Documentation)
GEMINI_API_KEY=your_gemini_api_key_here

# Groq API Key for Stage 1 (Ultra-fast Whisper STT)
GROQ_API_KEY=your_groq_api_key_here
```

### Step 3: Run the Application
You can launch the dashboard by running the provided batch script (Windows):
```cmd
Start_Meeting_Assistant.bat
```
Or manually via Streamlit:
```bash
streamlit run app.py
```

---

## 5. Directory Structure
```text
📦 AI-Meeting-Assistant
 ┣ 📂 assets/audio          # Edge-case audio files for testing
 ┣ 📂 prompts/              # Strict rule templates for Stage 2 & 3 LLMs
 ┣ 📂 src/
 ┃ ┣ 📂 pipeline/           # Orchestrates the end-to-end data flow
 ┃ ┣ 📂 refinement/         # Stage 2 implementation
 ┃ ┣ 📂 stt/                # Stage 1 implementation (Groq)
 ┃ ┣ 📂 summarization/      # Stage 3 implementation (Structured Pydantic outputs)
 ┃ ┣ 📂 ui/                 # Streamlit UI Components (Sidebar, Theme, Views)
 ┃ ┗ 📂 utils/              # Helper functions (Config, Audio validation, PDF Export, Visual Diff)
 ┣ 📜 app.py                # Main Streamlit Application Router
 ┣ 📜 DEV_GUIDE.md          # Internal Architecture Documentation
 ┗ 📜 requirements.txt      # Python dependencies
```

---

## 6. Edge Case Handling (Verification)
The pipeline has been rigorously tested against edge cases to ensure strict compliance with Inter-IIT rules:
* **The "Vague Boss" Test:** If an owner/deadline is not explicitly stated (e.g., "Someone needs to fix the bug eventually"), the output strictly logs the Action Item with `"owner": "unspecified"` and `"deadline": "unspecified"`.
* **The "Brainstorm" Test:** If participants merely propose ideas without reaching a final agreement, the `key_decisions` array remains perfectly empty `[]`. Proposals are never logged as confirmed decisions.
* **The "Empty Room" Test:** The pipeline detects whitespace/empty audio early, gracefully halting processing with a UI warning to save API quotas and prevent crashes.
