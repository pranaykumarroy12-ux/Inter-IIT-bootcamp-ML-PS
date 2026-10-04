"""
Root entry point / convenience script for Stage 1: Speech-to-Text.
Delegates to modular implementation in src.stt.transcriber.
"""

from pathlib import Path
from src.stt.transcriber import transcribe_audio, get_whisper_model

if __name__ == "__main__":
    from src.utils.config import ASSETS_DIR, PROJECT_ROOT

    # Look for sample audio in assets/audio/ or root
    sample_path = ASSETS_DIR / "audio" / "whatsapp-audio-2026-10-04-at-50909-pm_Sgw8gMZq.mp3"
    if not sample_path.exists():
        sample_path = PROJECT_ROOT / "whatsapp-audio-2026-10-04-at-50909-pm_Sgw8gMZq.mp3"

    if sample_path.exists():
        print(f"Transcribing: {sample_path}")
        text = transcribe_audio(sample_path)
        print("\n--- TRANSCRIPT ---")
        print(text)
    else:
        print("Sample audio file not found. Please provide an audio file path.")