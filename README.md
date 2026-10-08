# AI Meeting Assistant

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ai-powered-meeting-assistant-brnjz68ygdggmjr7z3en7w.streamlit.app/)
*(👆 **Live Demo:** Click the badge above to test the deployed app!)*

**Inter-IIT Tech Meet 15.0 - ML Bootcamp (Phase 2)**  

---

## 1. Project Overview
**AI-Powered Meeting Assistant: Multi-Stage Audio Transcription, Domain-Aware Refinement, and Structured Documentation**

This is my submission for the ML Bootcamp. Instead of passing everything into one giant LLM prompt (which usually causes hallucinations), I broke the project down into a 3-stage pipeline. This makes it much faster and a lot easier to debug.

---

## 2. How the Pipeline Works

* **Stage 1 (Speech-to-Text):** 
  * I used `whisper-large-v3` running on the Groq API. 
  * **Why:** Running Whisper locally was maxing out my CPU and taking too long. Moving it to Groq lets it transcribe audio files in just a few seconds.

* **Stage 2 (Refinement & Diarization):** 
  * I used `gemini-3.5-flash-lite`.
  * **Why:** Groq Whisper is fast but doesn't give speaker labels and messes up technical jargon. This Gemini step takes the raw text, figures out who is speaking from context clues, and fixes typos (like changing "you art" to "UART") without changing the actual meaning of the sentences.

* **Stage 3 (Documentation & Extraction):** 
  * I used `gemini-3.5-flash-lite` again, but this time using Pydantic Structured Outputs.
  * **Why:** I needed it to return clean JSON for the frontend. By forcing a strict Pydantic schema, I made sure the AI outputs "unspecified" if it can't find an owner or a deadline. This completely stops it from making things up.

---

## 3. Features
I built the frontend using Streamlit. Some cool features include:
- **Visual Diff Viewer:** You can see exactly what the AI changed. It highlights fixed jargon in green and crosses out Whisper mistakes in red.
- **RAG Chatbot:** You can chat directly with your meeting transcript in a sidebar tab.
- **Downloads:** Export the final meeting minutes as a PDF, JSON, or TXT file.

---

## 4. Setup & Installation

**Prerequisites:** Python 3.10+ and `ffmpeg` installed on your system.

**1. Install dependencies:**
```bash
pip install -r requirements.txt
```

**2. Add your API keys:**
Create a `.env` file in the root folder and add your keys:
```env
GEMINI_API_KEY=your_gemini_api_key_here
GROQ_API_KEY=your_groq_api_key_here
```

**3. Run the app:**
```cmd
# On Windows, just double-click:
Start_Meeting_Assistant.bat

# Or run it manually via terminal:
streamlit run app.py
```

---

## 5. Folder Structure
- `assets/audio/` - Test audio files (including edge cases).
- `prompts/` - The text files where I keep the rules for the Gemini models.
- `src/` - All the backend code (split into stt, refinement, summarization, and ui).
- `app.py` - The main Streamlit file.

---

## 6. Testing Edge Cases
I made sure the app handles the specific edge cases mentioned in the problem statement:
* **The "Vague Task" Test:** If someone says "we need to fix this eventually", the JSON output strictly says `"owner": "unspecified"` and `"deadline": "unspecified"`.
* **The "Brainstorm" Test:** If people just throw around ideas but don't decide on anything, the `key_decisions` list comes back completely empty instead of hallucinating fake decisions.
* **Empty Audio:** If you upload a silent file, Whisper sometimes hallucinates phrases like "Thank you for watching". I added a script to catch this and stop the pipeline so it doesn't waste API calls.
