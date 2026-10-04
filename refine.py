"""
Root entry point / convenience script for Stage 2: Transcript Refinement.
Delegates to modular implementation in src.refinement.refiner.
"""

from src.refinement.refiner import refine_transcript

if __name__ == "__main__":
    test_transcript = """
    Today we are going to discus the micro controller architecure.
    The UART module will comunicate with the sensor using serial
    comunication. We also need to configure the baud rate to
    nine thousand six hundred bits per second.
    """

    print("Sending transcript to Gemini...")
    refined = refine_transcript(test_transcript)

    print("\nREFINED TRANSCRIPT:")
    print(refined)