"""
Stage 1: Speech-to-Text Module.
Transcribes audio recordings into raw transcripts using the Groq Whisper API.
"""

import os
from typing import Optional
from groq import Groq
from src.utils.config import get_groq_api_key, DEFAULT_STT_MODEL

def transcribe_audio(
    audio_path: str,
    model_name: str = DEFAULT_STT_MODEL,
    client: Optional[Groq] = None
) -> str:
    """
    Transcribes an audio file using Groq's high-speed Whisper API.
    
    Args:
        audio_path: Path to the audio file.
        model_name: The Groq model identifier (e.g., whisper-large-v3).
        client: Optional pre-configured Groq client instance.
        
    Returns:
        str: The raw transcribed text.
    """
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    if client is None:
        client = Groq(api_key=get_groq_api_key())
        
    print(f"Transcribing {audio_path} via Groq API...")
    
    with open(audio_path, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=(os.path.basename(audio_path), file.read()),
            model=model_name,
            # We can use the prompt parameter to guide Whisper's spelling
            # but Whisper doesn't follow strict instructions like Gemini does.
            prompt="Meeting transcription, software engineering, domain terms.",
            response_format="text",
            language="en" # Force English transcription
        )
        
    return transcription.strip()
