"""
Stage 2: Domain-Aware Transcript Refinement.
Refines raw STT transcripts using Google Gemini to correct terminology and phonetic errors
while strictly preserving names, numbers, negations, and speaker intent.
"""

from pathlib import Path
from typing import Optional
from google import genai
from src.utils.config import get_gemini_api_key, PROMPTS_DIR, DEFAULT_REFINEMENT_MODEL

_PROMPT_TEMPLATE_PATH = PROMPTS_DIR / "stage2_refine.txt"

# Fallback prompt template if prompt file is unavailable
_FALLBACK_PROMPT_TEMPLATE = """You are a transcript correction assistant.

Your task is to clean and refine the following meeting transcript.

Rules:
- Correct obvious speech-to-text errors.
- Correct technical terms, acronyms, and jargon when the intended term is clear.
- Preserve the original meaning exactly.
- Preserve all numbers, names, dates, and factual information exactly in meaning.
- You may convert clearly spoken numbers into standard numeric notation when the meaning is unambiguous.
- Never guess or invent a number that is unclear in the transcript.
- Do not add information that was not present.
- Do not remove important information.
- Preserve negations such as "not", "never", and "don't".
- Return only the refined transcript.

RAW TRANSCRIPT:
{raw_text}
"""

def load_refinement_prompt(raw_text: str) -> str:
    """Loads prompt template from file and populates with raw transcript text."""
    if _PROMPT_TEMPLATE_PATH.exists():
        template = _PROMPT_TEMPLATE_PATH.read_text(encoding="utf-8")
    else:
        template = _FALLBACK_PROMPT_TEMPLATE
    return template.format(raw_text=raw_text)

from src.utils.retries import with_retries

@with_retries(max_retries=3)
def refine_transcript(
    raw_text: str,
    model_name: str = DEFAULT_REFINEMENT_MODEL,
    client: Optional[genai.Client] = None
) -> str:
    """
    Refines a raw speech-to-text transcript using an LLM.

    Args:
        raw_text: The raw transcript text from Stage 1.
        model_name: The Gemini model identifier (default: gemini-3.5-flash-lite).
        client: Optional pre-configured genai.Client instance.

    Returns:
        str: Cleaned and refined transcript.

    Raises:
        ValueError: If raw_text is empty or API key is missing.
    """
    if not raw_text or not raw_text.strip():
        raise ValueError("Cannot refine an empty or whitespace-only transcript.")

    if client is None:
        api_key = get_gemini_api_key()
        client = genai.Client(api_key=api_key)

    prompt = load_refinement_prompt(raw_text)

    response = client.models.generate_content(
        model=model_name,
        contents=prompt
    )

    if response.text is None:
        raise RuntimeError("Model returned empty response during transcript refinement.")

    return response.text.strip()
