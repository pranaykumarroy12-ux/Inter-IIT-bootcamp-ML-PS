"""
Stage 3: Meeting Documentation Module.
Generates concise meeting summary, organized minutes, key decisions, and action items
from a refined transcript using Google Gemini structured outputs (Pydantic).
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from google import genai
from google.genai import types

from src.utils.config import get_gemini_api_key, PROMPTS_DIR, DEFAULT_DOCUMENTATION_MODEL

_PROMPT_TEMPLATE_PATH = PROMPTS_DIR / "stage3_document.txt"

# --- Pydantic Schemas for Structured Output Enforcement ---

class ActionItem(BaseModel):
    task_description: str = Field(description="The actionable task to be done.")
    owner: str = Field(description="The explicitly named assigned person. If assigned to 'someone', 'we', or not named, output exactly 'unspecified'.")
    deadline: str = Field(description="The strict date or time deadline. If the audio uses vague terms (like 'eventually', 'soon', 'later') or if it is missing, output exactly 'unspecified'.")

class MeetingRecordSchema(BaseModel):
    summary_and_minutes: str = Field(description="Concise summary and organized account of the main discussion points. Use markdown formatting (headings/bullets) inside this string.")
    key_decisions: List[str] = Field(description="List of explicitly agreed-upon decisions. Empty list if none.")
    action_items: List[ActionItem] = Field(description="List of actionable tasks. Empty list if none.")

# --- Helper Functions ---

def load_documentation_prompt(refined_transcript: str) -> str:
    """Loads prompt template from file and populates with refined transcript text."""
    if _PROMPT_TEMPLATE_PATH.exists():
        template = _PROMPT_TEMPLATE_PATH.read_text(encoding="utf-8")
    else:
        # Fallback if file is missing (Ensures edge cases are still handled correctly)
        template = (
            "You are an expert meeting documentation assistant.\n"
            "Your task is to analyze the following refined meeting transcript and produce a structured meeting record.\n\n"
            "CRITICAL REQUIREMENTS & CONSTRAINTS:\n"
            "1. Grounding: All output MUST reflect what was explicitly stated. Do NOT invent or assume any facts.\n"
            "2. Meeting Minutes: Provide a concise summary and an organized account of the main discussion points.\n"
            "3. Key Decisions:\n"
            "   - Extract only decisions that were explicitly agreed upon by participants.\n"
            "   - Do NOT present a suggestion, proposal, or open discussion as an agreed decision.\n"
            "4. Action Items:\n"
            "   - Extract ANY explicitly stated task or work that needs to be done.\n"
            "   - If the owner is not explicitly named (e.g., 'someone', 'we', or unstated), you MUST mark the owner EXACTLY as 'unspecified'. NEVER invent or guess an owner.\n"
            "   - If the deadline is not a strict date/time (e.g., 'eventually', 'soon', or omitted), you MUST mark the deadline EXACTLY as 'unspecified'. NEVER invent a deadline.\n\n"
            "REFINED TRANSCRIPT:\n{refined_transcript}"
        )
    return template.format(refined_transcript=refined_transcript)

# --- Main Generation Logic ---

from src.utils.retries import with_retries

@with_retries(max_retries=3)
def generate_meeting_documentation(
    refined_transcript: str,
    model_name: str = DEFAULT_DOCUMENTATION_MODEL,
    client: Optional[genai.Client] = None
) -> Dict[str, Any]:
    """
    Analyzes a refined transcript to produce structured meeting documentation.
    
    Returns a dictionary containing:
    - 'json_record': The raw dictionary matching the Pydantic schema
    """
    if not refined_transcript or not refined_transcript.strip():
        raise ValueError("Cannot document an empty transcript.")

    if client is None:
        client = genai.Client(api_key=get_gemini_api_key())

    prompt = load_documentation_prompt(refined_transcript)

    # Use Gemini's structured output capability to enforce the JSON schema
    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=MeetingRecordSchema,
            temperature=0.2, # Low temp for factual extraction
        )
    )

    if not response.parsed:
        raise RuntimeError("Model failed to return structured output.")

    # response.parsed is an instance of MeetingRecordSchema because of response_schema
    record: MeetingRecordSchema = response.parsed

    return {
        "json_record": record.model_dump()
    }
