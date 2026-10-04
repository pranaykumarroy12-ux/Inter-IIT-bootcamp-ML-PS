"""
Stage 2: Domain-aware transcript refinement module.
Refines raw transcripts using Gemini to correct domain-specific terminology errors.
"""

from src.refinement.refiner import refine_transcript

__all__ = ["refine_transcript"]
