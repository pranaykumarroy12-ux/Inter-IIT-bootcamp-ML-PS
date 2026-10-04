"""
Stage 1: Speech-to-Text Transcriber.
Implements speech transcription using faster-whisper (large-v3-turbo).
"""

from pathlib import Path
from typing import Optional, Union
from faster_whisper import WhisperModel
from src.utils.audio import validate_audio_file
from src.utils.config import DEFAULT_STT_MODEL

_CACHED_MODEL: Optional[WhisperModel] = None

def get_whisper_model(
    model_size: str = DEFAULT_STT_MODEL,
    device: str = "cpu",
    compute_type: str = "int8"
) -> WhisperModel:
    """
    Lazily loads and caches the WhisperModel instance to avoid redundant reload overhead.
    """
    global _CACHED_MODEL
    if _CACHED_MODEL is None:
        print(f"Loading Whisper model '{model_size}' (device={device}, compute_type={compute_type})...")
        _CACHED_MODEL = WhisperModel(
            model_size,
            device=device,
            compute_type=compute_type
        )
        print("Whisper model loaded successfully!")
    return _CACHED_MODEL


def transcribe_audio(
    audio_file: Union[str, Path],
    model: Optional[WhisperModel] = None,
    beam_size: int = 5,
    vad_filter: bool = True
) -> str:
    """
    Transcribes an audio file into a raw text transcript using faster-whisper.

    Args:
        audio_file: Path to the audio file.
        model: Optional pre-loaded WhisperModel. If None, uses cached default.
        beam_size: Beam search width (default: 5).
        vad_filter: Whether to apply Voice Activity Detection filtering (default: True).

    Returns:
        str: Raw transcript text.

    Raises:
        ValueError: If audio file validation fails.
    """
    is_valid, msg = validate_audio_file(audio_file)
    if not is_valid:
        raise ValueError(f"Invalid audio input: {msg}")

    if model is None:
        model = get_whisper_model()

    audio_path_str = str(Path(audio_file).resolve())
    segments, info = model.transcribe(
        audio_path_str,
        beam_size=beam_size,
        vad_filter=vad_filter
    )

    transcript = " ".join(segment.text.strip() for segment in segments if segment.text)
    return transcript.strip()
