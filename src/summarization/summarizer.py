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
    owner: str = Field(description="The assigned person. If not explicitly stated, MUST be 'unspecified'.")
    deadline: str = Field(description="The task deadline. If not explicitly stated, MUST be 'unspecified'.")

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
        # Fallback if file is missing
        template = "Analyze this meeting transcript and output a structured record:\n{refined_transcript}"
    return template.format(refined_transcript=refined_transcript)

def _convert_schema_to_markdown(record: MeetingRecordSchema) -> str:
    """Converts the structured Pydantic object into a human-readable Markdown format."""
    md = f"## Meeting Summary & Minutes\n\n{record.summary_and_minutes}\n\n"
    
    md += "## Key Decisions\n\n"
    if not record.key_decisions:
        md += "No key decisions were recorded.\n\n"
    else:
        for decision in record.key_decisions:
            md += f"- {decision}\n"
        md += "\n"
            
    md += "## Action Items\n\n"
    if not record.action_items:
        md += "No action items were assigned.\n"
    else:
        for idx, item in enumerate(record.action_items, 1):
            md += f"{idx}. **Task:** {item.task_description}\n"
            md += f"   - **Owner:** {item.owner}\n"
            md += f"   - **Deadline:** {item.deadline}\n"
            
    return md

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
    - 'markdown': A human-readable Markdown formatted string
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
        "json_record": record.model_dump(),
        "markdown": _convert_schema_to_markdown(record)
    }
