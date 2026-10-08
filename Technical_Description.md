### Technical Pipeline Description

I built this application using a 3-stage pipeline. By breaking it into steps, I was able to get much faster processing speeds and stop the LLM from hallucinating fake tasks.

**1. Speech-to-Text Model (`whisper-large-v3` via Groq API)**
* **Role:** This is the first step. It takes the audio file and turns it into a raw, word-for-word transcript. I chose to run it on Groq because it processes audio incredibly fast compared to running Whisper locally on a CPU.
* **Data Flow:** Takes in audio bytes (`.mp3`, `.wav`) -> Outputs a raw block of text to Stage 2.

**2. First Language Model - Refinement (`gemini-3.5-flash-lite`)**
* **Role:** Whisper is fast, but it doesn't output speaker names and it often mishears technical jargon. This Gemini step reads the raw transcript, figures out who is speaking based on the context, and fixes typos. It removes "ums" and "ahs", but I prompted it strictly so it never changes the actual meaning of the sentences or numbers.
* **Data Flow:** Takes in the raw text -> Outputs a clean, readable text with speaker names to Stage 3.

**3. Second Language Model - Documentation (`gemini-3.5-flash-lite` with Pydantic)**
* **Role:** This is the extraction step. It uses Pydantic JSON schemas to pull out the Executive Summary, Key Decisions, and Action Items. By forcing a strict JSON schema, it prevents the AI from guessing. If a task owner isn't mentioned in the audio, the schema forces the AI to write `"unspecified"` instead of hallucinating a random name.
* **Data Flow:** Takes in the clean text -> Outputs a structured JSON file, which the Streamlit app then uses to build the dashboard and PDF exports.
