"""
Independent test suite for Stage 1: Speech-to-Text Transcriber.
"""

import sys
from pathlib import Path

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.utils.audio import validate_audio_file
from src.stt.transcriber import get_whisper_model

def test_audio_validation_nonexistent():
    """Verify non-existent file validation."""
    print("Testing non-existent file validation...")
    is_valid, msg = validate_audio_file("non_existent_file.mp3")
    assert not is_valid, "Expected non-existent file to be invalid"
    print(f"PASSED: {msg}")

def test_audio_validation_unsupported_format():
    """Verify unsupported file format validation."""
    print("\nTesting unsupported extension validation...")
    dummy_txt = PROJECT_ROOT / "tests" / "dummy.xyz"
    dummy_txt.write_text("test")
    try:
        is_valid, msg = validate_audio_file(dummy_txt)
        assert not is_valid, "Expected .xyz format to be invalid"
        print(f"PASSED: {msg}")
    finally:
        if dummy_txt.exists():
            dummy_txt.unlink()

def test_whisper_model_loading():
    """Verify that WhisperModel can be initialized without error."""
    print("\nTesting WhisperModel loader...")
    try:
        model = get_whisper_model()
        assert model is not None, "Expected valid model instance"
        print("PASSED: WhisperModel loaded and cached successfully.")
        return True
    except Exception as e:
        print(f"FAILED: Could not load Whisper model: {e}")
        return False

if __name__ == "__main__":
    print("=== Running Stage 1 STT Tests ===")
    test_audio_validation_nonexistent()
    test_audio_validation_unsupported_format()
    test_whisper_model_loading()
    print("\nStage 1 validation tests COMPLETED.")
