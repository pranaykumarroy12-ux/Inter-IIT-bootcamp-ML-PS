"""
Audio utility functions for validation, format verification, and inspection.
Addresses PS requirement: Handle unsupported, empty, or unreadable files with a clear error message.
"""

from pathlib import Path
from typing import Tuple

SUPPORTED_AUDIO_EXTENSIONS = {
    ".wav", ".mp3", ".m4a", ".mpeg", ".mp4", ".ogg", ".flac", ".aac", ".wma"
}

def validate_audio_file(file_path: str | Path) -> Tuple[bool, str]:
    """
    Validates whether an audio file exists, is non-empty, and has a supported extension.

    Returns:
        Tuple[bool, str]: (is_valid, message)
    """
    path = Path(file_path)

    if not path.exists():
        return False, f"File does not exist: {path}"

    if not path.is_file():
        return False, f"Path is not a regular file: {path}"

    if path.stat().st_size == 0:
        return False, f"File is empty (0 bytes): {path.name}"

    suffix = path.suffix.lower()
    if suffix not in SUPPORTED_AUDIO_EXTENSIONS:
        return False, (
            f"Unsupported audio format '{suffix}'. Supported formats: "
            f"{', '.join(sorted(SUPPORTED_AUDIO_EXTENSIONS))}"
        )

    return True, "Audio file is valid."
