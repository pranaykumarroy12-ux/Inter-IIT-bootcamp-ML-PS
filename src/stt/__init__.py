"""
Stage 1: Speech-to-Text module.
Transcribes audio recordings into raw transcripts using Google Gemini 1.5 Flash Audio.
"""

from src.stt.transcriber import transcribe_audio

__all__ = ["transcribe_audio"]
