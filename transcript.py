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
    start_date = datetime(2024, 3, 20).strftime('%Y-%m-%dT%H:%M:%SZ')
    end_date = datetime(2024, 12, 31).strftime('%Y-%m-%dT%H:%M:%SZ')

    # Retrieve videos from the channel
    request = youtube.search().list(
        part="snippet",
        channelId=CHANNEL_ID,
        publishedAfter = start_date,
        publishedBefore = end_date,
        maxResults=100,  # Adjust the number of results as needed
        type="video",   # Necessary for using videoDuration parameter
        videoDuration="medium"  # Video length from 4 to 20 minutes
    )
    response = request.execute()

    # Extract video IDs from the response
    videos = []
    for item in response.get("items", []):
        if item["id"]["kind"] == "youtube#video":
            video_id = item["id"]["videoId"]
            published_date = item["snippet"]["publishedAt"]
            videos.append({"video_id": video_id, "published_date": published_date})

    return videos

# Using OPENAI to search video transcript for crypto Tokens/Coins
def transcript_filter(text):
    client = OpenAI()

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are crypto trader, your goal is to identify crypto coins. Display them as a python list."},
        {"role": "user", "content": text}
    ]
    )
    return completion.choices[0].message.content

text = transcript(video_id_list()[0]['video_id'])
print(video_id_list()[-1]['published_date'])
print(transcript_filter(text))

# for item in video_id_list():
#     print(item)