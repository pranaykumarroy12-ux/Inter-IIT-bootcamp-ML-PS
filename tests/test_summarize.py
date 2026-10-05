"""
Independent test suite for Stage 3: Meeting Documentation.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.summarization.summarizer import generate_meeting_documentation

def test_meeting_documentation():
    print("Testing Stage 3 Meeting Documentation generation...")
    transcript = (
        "Alice: We need to update the database schema for the new user profiles. "
        "Bob, can you handle that by next Tuesday? "
        "Bob: Yes, I'll get that done. Also, I think we should switch our hosting to AWS. "
        "Alice: Let's agree to migrate to AWS next quarter. Charlie, look into the pricing but no hard deadline right now."
    )
    
    try:
        result = generate_meeting_documentation(transcript)
        json_rec = result["json_record"]
        md_rec = result["markdown"]
        
        print("\nJSON OUTPUT:")
        print(json_rec)
        
        # Validation checks
        assert "summary_and_minutes" in json_rec
        assert "key_decisions" in json_rec
        assert "action_items" in json_rec
        
        assert len(json_rec["action_items"]) > 0
        
        # Verify the 'unspecified' deadline logic for Charlie's task
        charlie_task = next((task for task in json_rec["action_items"] if "Charlie" in task["owner"]), None)
        assert charlie_task is not None
        assert charlie_task["deadline"].lower() == "unspecified"
        
        print("\nPASSED: Stage 3 Documentation generated and strictly validated rules.")
        return True
    except Exception as e:
        print(f"\nFAILED: {e}")
        return False

if __name__ == "__main__":
    test_meeting_documentation()
