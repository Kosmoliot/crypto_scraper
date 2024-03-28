import os
from youtube_transcript_api import YouTubeTranscriptApi
from googleapiclient.discovery import build
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime, timedelta


load_dotenv()

# Define API key and channel ID
API_KEY = os.environ['YOUTUBE_API_KEY']
# OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
CHANNEL_ID = "UCHop-jpf-huVT1IYw79ymPw"

# Python module to get the video transcript
def transcript(video_id):
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    video_transc = []
    for item in transcript_list:
        video_transc.append(item['text'])
    return ' '.join(video_transc)

# Using Youtube API to get the video IDs  
def video_id_list():
    # Define the YouTube API service
    youtube = build("youtube", "v3", developerKey=API_KEY)

    # Define the time period
    start_date = datetime(2024, 1, 1).strftime('%Y-%m-%dT%H:%M:%SZ')
    end_date = datetime(2024, 12, 31).strftime('%Y-%m-%dT%H:%M:%SZ')

    # Retrieve videos from the channel
    request = youtube.search().list(
        part="snippet",
        channelId=CHANNEL_ID,
        publishedAfter = start_date,
        publishedBefore = end_date,
        maxResults=100,  # Adjust the number of results as needed
        type="video",   # Video length from 4 to 20 minutes
        videoDuration="medium"
    )
    response = request.execute()

    # Extract video IDs from the response
    video_ids = [item["id"]["videoId"] for item in response["items"] if item["id"]["kind"] == "youtube#video"]
    return video_ids

# Using OPENAI to search video transcript for crypto Tokens/Coins
def transcript_filter(text):
    client = OpenAI()

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are crypto trader, your goal is to identify crypto tokens, projects and protocols in the text. Print them in a python list."},
        {"role": "user", "content": text}
    ]
    )
    return completion.choices[0].message.content

# text = transcript(video_id_list()[-1])
# print(transcript_filter(text))

print(video_id_list())