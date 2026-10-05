import sys
from pathlib import Path

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.pipeline.workflow import MeetingPipeline
from src.utils.config import ASSETS_DIR

def test_pipeline():
    print("Initializing Meeting Pipeline...")
    pipeline = MeetingPipeline()
    
    # Path to your sample audio
    audio_file = ASSETS_DIR / "audio" / "mock_meeting.mp3"
    
    if not audio_file.exists():
        print(f"Error: Could not find sample audio at {audio_file}")
        print("Please check the path or provide a valid audio file.")
        return

    print(f"\n--- Starting Pipeline ---")
    print(f"Target Audio: {audio_file.name}")
    
    print("\n[1/3] Running Stage 1: Transcribing audio to Raw Text...")
    print("(Note: This is running on CPU and may take a moment for a 2-minute file. Please wait...)")
    
    # We can just use the pipeline's run_pipeline method instead of calling them individually
    # but for visual tracking, let's call them one by one like before
    raw_transcript = pipeline.run_transcription(audio_file)
    
    print("\n[2/3] Running Stage 2: Refining Transcript with Gemini...")
    refined_transcript = pipeline.run_refinement(raw_transcript)

    print("\n[3/3] Running Stage 3: Extracting Meeting Documentation...")
    documentation = pipeline.run_documentation(refined_transcript)
    
    print("\n" + "="*50)
    print("=== RAW TRANSCRIPT (Stage 1 Output) ===")
    print("="*50)
    print(raw_transcript)
    
    print("\n" + "="*50)
    print("=== REFINED TRANSCRIPT (Stage 2 Output) ===")
    print("="*50)
    print(refined_transcript)

    print("\n" + "="*50)
    print("=== FINAL MEETING RECORD (Stage 3 Output) ===")
    print("="*50)
    print(documentation["markdown"])
    
    print("\n[SUCCESS] Pipeline Stage 1 -> Stage 2 -> Stage 3 successfully completed!")

if __name__ == "__main__":
    test_pipeline()
