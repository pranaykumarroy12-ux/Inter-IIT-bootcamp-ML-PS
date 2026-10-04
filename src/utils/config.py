"""
Configuration and environment management module.
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# Define key project directories
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
PROMPTS_DIR = PROJECT_ROOT / "prompts"
ASSETS_DIR = PROJECT_ROOT / "assets"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"

# Load environment variables from .env located at project root
ENV_FILE = PROJECT_ROOT / ".env"
load_dotenv(dotenv_path=ENV_FILE)

# Default model identifiers
DEFAULT_STT_MODEL = "large-v3-turbo"
DEFAULT_REFINEMENT_MODEL = "gemini-3.5-flash-lite"
DEFAULT_DOCUMENTATION_MODEL = None  # To be decided in Checkpoint 4 (Stage 3 selection)

def get_gemini_api_key() -> str:
    """
    Retrieve Gemini API key from environment variables.
    Raises ValueError if key is not configured.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is not set in environment or .env file. "
            "Please create a .env file based on .env.example."
        )
    return api_key
