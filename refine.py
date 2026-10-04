from google import genai
from dotenv import load_dotenv
import os

# Load variables from .env
load_dotenv()

# Get Gemini API key
api_key = os.getenv("GEMINI_API_KEY")

# Create Gemini client
client = genai.Client(api_key=api_key)


def refine_transcript(raw_text):
    prompt = f"""
You are a transcript correction assistant.

Your task is to clean and refine the following meeting transcript.

Rules:
- Correct obvious speech-to-text errors.
- Correct technical terms, acronyms, and jargon when the intended term is clear.
- Preserve the original meaning exactly.
- Preserve all numbers, names, dates, and factual information exactly in meaning.
- You may convert clearly spoken numbers into standard numeric notation when the meaning is unambiguous.
- Never guess or invent a number that is unclear in the transcript.
- Do not add information that was not present.
- Do not remove important information.
- Preserve negations such as "not", "never", and "don't".
- Return only the refined transcript.

RAW TRANSCRIPT:
{raw_text}
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text

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