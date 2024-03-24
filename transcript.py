from google.cloud import speech_v1p1beta1 as speech

# Define your Google Cloud credentials
credentials_path = 'path/to/your/credentials.json'
client = speech.SpeechClient.from_service_account_json(credentials_path)

# Function to transcribe speech from a YouTube video URL
def transcribe_youtube_video(url):
    # Use appropriate methods to extract audio from the video (e.g., YouTube DL)
    # For simplicity, assume audio_file contains the audio content extracted from the video

    # Perform speech-to-text transcription
    audio = speech.RecognitionAudio(content=audio_file)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    response = client.recognize(config=config, audio=audio)

    transcripts = []
    for result in response.results:
        transcripts.append(result.alternatives[0].transcript)

    return transcripts

# Example usage
video_url = 'https://www.youtube.com/watch?v=VIDEO_ID'
transcripts = transcribe_youtube_video(video_url)
for transcript in transcripts:
    print("Transcript:", transcript)
