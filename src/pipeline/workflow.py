"""
Pipeline Workflow Orchestrator.
Coordinates Stage 1 (Speech-to-Text), Stage 2 (Transcript Refinement),
and Stage 3 (Meeting Documentation).
"""

from pathlib import Path
from typing import Dict, Any, Union, Optional
from src.stt.transcriber import transcribe_audio
from src.refinement.refiner import refine_transcript
from src.utils.audio import validate_audio_file

class MeetingPipeline:
    """
    End-to-end meeting processing pipeline.
    """

    def __init__(self):
        pass

    def run_transcription(self, audio_path: Union[str, Path]) -> str:
        """Runs Stage 1: Audio -> Raw Transcript."""
        is_valid, msg = validate_audio_file(audio_path)
        if not is_valid:
            raise ValueError(f"Cannot process audio: {msg}")
        return transcribe_audio(audio_path)

    def run_refinement(self, raw_transcript: str) -> str:
        """Runs Stage 2: Raw Transcript -> Refined Transcript."""
        return refine_transcript(raw_transcript)

    def run_documentation(self, refined_transcript: str) -> Dict[str, Any]:
        """Runs Stage 3: Refined Transcript -> Meeting Minutes, Decisions, Action Items."""
        from src.summarization.summarizer import generate_meeting_documentation
        return generate_meeting_documentation(refined_transcript)

    def run_pipeline(self, audio_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Runs the end-to-end pipeline.
        Note: Stage 3 is currently pending implementation.
        """
        raw_transcript = self.run_transcription(audio_path)
        refined_transcript = self.run_refinement(raw_transcript)
        
        # When Stage 3 is implemented, documentation will be called here
        return {
            "raw_transcript": raw_transcript,
            "refined_transcript": refined_transcript,
            "documentation": None  # Stage 3 placeholder
        }
