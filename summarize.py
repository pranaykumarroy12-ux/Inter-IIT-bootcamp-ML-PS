"""
Root entry point / convenience script for Stage 3: Meeting Documentation.
Delegates to modular implementation in src.summarization.summarizer.
"""

from src.summarization.summarizer import generate_meeting_documentation

if __name__ == "__main__":
    test_refined_transcript = "In today's meeting, John said we should finish the frontend by Friday. Sarah agreed. No other decisions were made."
    print("Testing Stage 3 Documentation with sample text...\n")
    
    result = generate_meeting_documentation(test_refined_transcript)
    
    print("=== JSON RECORD ===")
    print(result["json_record"])
    print("\n=== MARKDOWN RECORD ===")
    print(result["markdown"])
