import whisperai
import openai
import pyaudio
import wave

# Function to capture audio from microphone
def capture_audio_from_video_call():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 5  # Adjust this according to the length of your video call
    WAVE_OUTPUT_FILENAME = "output.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* Recording audio from the video call...")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* Finished recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    # Read the recorded audio file
    with open(WAVE_OUTPUT_FILENAME, 'rb') as f:
        audio_data = f.read()

    return audio_data

# Initialize OpenAI
openai.api_key = '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'

# Use WhisperAI for video-to-text transcription
video_transcript = whisperai.transcribe_video(capture_audio_from_video_call())

print("Video Transcript:")
print(video_transcript)

# Transcribe audio to text using OpenAI
audio_transcript = openai.Transcript.create(
    audio=capture_audio_from_video_call(),
    language="en",
    speakers=1
)

print("Audio Transcript:")
print(audio_transcript)

search_prompt = input("Enter the search prompt: ")

response_search = openai.Completion.create(
    engine="davinci",
    prompt=video_transcript + "\nSearch Prompt: " + search_prompt,
    max_tokens=100,
    temperature=0.3,
    stop=None,
)

search_results = response_search.choices[0].text.strip()

print("Search Results:")
print(search_results)
