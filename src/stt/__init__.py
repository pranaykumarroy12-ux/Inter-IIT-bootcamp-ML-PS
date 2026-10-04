"""
Stage 1: Speech-to-Text module.
Transcribes audio recordings into raw transcripts using faster-whisper.
"""

from src.stt.transcriber import transcribe_audio, get_whisper_model

__all__ = ["transcribe_audio", "get_whisper_model"]
