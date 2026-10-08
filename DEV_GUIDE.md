# Developer Guide

Welcome to the codebase for the AI Meeting Assistant. This guide explains how the project is structured and how you can navigate or modify the code.

## 1. Project Structure

I split the code into logical folders so you don't have to hunt through a massive 1000-line script. Everything is modular:

- `src/stt/` - Handles the Speech-to-Text integration with the Groq API.
- `src/refinement/` - The first Gemini pass. It takes the messy Groq output, fixes jargon, and figures out who is speaking.
- `src/summarization/` - The second Gemini pass. It uses Pydantic to strictly extract Action Items and Decisions into JSON.
- `src/ui/` - All the Streamlit frontend code is split into components here (sidebar, chat, etc.).
- `src/utils/` - Helpers for PDF generation, checking file types, and loading API keys.
- `prompts/` - The plain text files containing the instructions we send to Gemini.

## 2. Modifying the AI Behavior

I deliberately kept the AI prompts out of the Python code so they are easier to tweak. If you want to change how the AI behaves, just edit the text files in the `prompts/` directory:

- `stage2_refine.txt`: Controls how jargon is fixed and how the AI guesses speaker names.
- `stage3_document.txt`: Controls the strict rules for extracting JSON without hallucinating.

## 3. Working with the UI

The frontend uses Streamlit, but I broke it down into components inside `src/ui/` to keep it clean.
- If you want to add a new page to the sidebar menu, look at `sidebar.py`.
- If you want to tweak the custom dark theme or colors, check `theme.py`.
- The main routing for the app happens at the bottom of `app.py`.

## 4. The Edge Case Logic

When testing or modifying the code, keep in mind we have strict guardrails built-in for the hackathon edge cases:
1. **Silence / Hallucination Catcher:** In `src/ui/processing.py`, there is a block of code that intercepts empty transcripts (or Whisper's weird "Thank you" hallucination) and kills the pipeline early. This saves API calls.
2. **Pydantic Validation:** In `src/summarization/summarizer.py`, we force Gemini to output `{"owner": "unspecified"}` if a task doesn't have an owner. If you change the Pydantic schema in the future, make sure you don't break this validation!

## 5. Running Tests

If you add new features, you can test the individual backend pieces without having to launch the whole Streamlit app. Just run the test scripts:
```bash
python -m tests.test_stt
python -m tests.test_refine
```
