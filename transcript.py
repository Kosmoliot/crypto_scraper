import os
from youtube_transcript_api import YouTubeTranscriptApi
from googleapiclient.discovery import build
from dotenv import load_dotenv
from openai import OpenAI


def transcript(video_id):
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    video_transc = []
    for item in transcript_list:
        video_transc.append(item['text'])
    return ' '.join(video_transc)
    


# Define API key and channel ID
load_dotenv()
API_KEY = os.environ['YOUTUBE_API_KEY']
# OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
CHANNEL_ID = "UCHop-jpf-huVT1IYw79ymPw"


# Define the YouTube API service
youtube = build("youtube", "v3", developerKey=API_KEY)

# Retrieve videos from the channel
request = youtube.search().list(
    part="snippet",
    channelId=CHANNEL_ID,
    maxResults=100  # Adjust the number of results as needed
)
response = request.execute()

# Extract video IDs from the response
video_ids = [item["id"]["videoId"] for item in response["items"] if item["id"]["kind"] == "youtube#video"]

text = transcript(video_ids[0])

client = OpenAI()

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are crypto trader, your goal is to identify crypto tokens, projects and protocols in the text."},
    {"role": "user", "content": text}
  ]
)

# print(completion.choices[0].message)

print(video_ids)