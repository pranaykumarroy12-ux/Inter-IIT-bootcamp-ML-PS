from faster_whisper import WhisperModel

print("Loading Whisper model...")

model = WhisperModel(
    "large-v3-turbo",
    device="cpu",
    compute_type="int8"
)

print("Model loaded!")


def transcribe_audio(audio_file):
    segments, info = model.transcribe(
        audio_file,
        beam_size=5,
        vad_filter=True
    )

    transcript = " ".join(segment.text for segment in segments)

    return transcript


audio_file = r"D:\Inter-IIT bootcamp\WhatsApp Audio 2026-10-04 at 5.09.09 PM.mpeg"

print("Transcribing...")

text = transcribe_audio(audio_file)

print("\n--- TRANSCRIPT ---")
print(text)