"""
Independent test suite for Stage 2: Domain-Aware Transcript Refinement.
"""

import sys
from pathlib import Path

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.refinement.refiner import refine_transcript

def test_empty_input_validation():
    """Verify that empty inputs raise a ValueError."""
    print("Testing empty input validation...")
    try:
        refine_transcript("")
        print("FAILED: Empty string did not raise ValueError.")
        return False
    except ValueError:
        print("PASSED: Empty string raised ValueError as expected.")
        return True

def test_domain_refinement_execution():
    """Verify that domain terminology refinement works end-to-end with Gemini."""
    print("\nTesting domain terminology refinement...")
    test_text = """
    Today we are going to discus the micro controller architecure.
    The UART module will comunicate with the sensor using serial
    comunication. We also need to configure the baud rate to
    nine thousand six hundred bits per second.
    """
    try:
        refined = refine_transcript(test_text)
        print("Result received from Gemini:")
        print(refined)
        
        # Check that key domain corrections took place
        assert "microcontroller" in refined.lower(), "Expected 'microcontroller' in refined text"
        assert "communicate" in refined.lower(), "Expected 'communicate' in refined text"
        assert "9600" in refined or "9,600" in refined or "nine thousand six hundred" in refined.lower()
        print("PASSED: Domain refinement output verified.")
        return True
    except Exception as e:
        print(f"FAILED: Exception occurred: {e}")
        return False

if __name__ == "__main__":
    print("=== Running Stage 2 Refinement Tests ===")
    t1 = test_empty_input_validation()
    t2 = test_domain_refinement_execution()
    if t1 and t2:
        print("\nAll Stage 2 tests PASSED.")
    else:
        print("\nSome Stage 2 tests FAILED.")
