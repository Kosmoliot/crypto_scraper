import os
import json
from datetime import datetime
from youtube_transcript_api import YouTubeTranscriptApi
from googleapiclient.discovery import build
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

API_KEY = os.getenv('YOUTUBE_API_KEY')
if not API_KEY:
    raise ValueError("YOUTUBE_API_KEY environment variable is not set.")

CHANNEL_ID = "UCHop-jpf-huVT1IYw79ymPw"


class ChicoVideo:
    """Class to store video parameters."""
    def __init__(self, video_id, video_date, video_title, video_coins):
        self.video_id = video_id
        self.video_date = video_date
        self.video_title = video_title
        self.video_coins = video_coins


def get_transcript(video_id):
    """Retrieve transcript for a given video ID."""
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        video_transcript = ' '.join(item['text'] for item in transcript_list)
        return video_transcript
    except Exception as e:
        print(f"Failed to retrieve transcript for video {video_id}: {e}")
        return None


def parse_date(date_str):
    """Parse date string to datetime object."""
    return datetime.strptime(date_str, "%Y,%m,%d")


def fetch_video_data(start_date, end_date):
    """Retrieve video data from YouTube API."""
    try:
        start_date_str = parse_date(start_date).strftime('%Y-%m-%dT%H:%M:%SZ')
        end_date_str = parse_date(end_date).strftime('%Y-%m-%dT%H:%M:%SZ')

        cache_filename = f"cache_data/cache_data_{start_date}_{end_date}.json"

        if os.path.exists(cache_filename):
            with open(cache_filename, 'r') as file:
                return json.load(file)

        with build("youtube", "v3", developerKey=API_KEY) as youtube:
            videos = []

            request = youtube.search().list(
                part="snippet",
                channelId=CHANNEL_ID,
                publishedAfter=start_date_str,
                publishedBefore=end_date_str,
                maxResults=1000,
                type="video",
                videoDuration="medium",
            )
            response = request.execute()

            for item in response.get("items", []):
                if item["id"]["kind"] == "youtube#video":
                    video_id = item["id"]["videoId"]
                    published_date = item["snippet"]["publishedAt"]
                    video_title = item["snippet"]["title"]
                    video_coins = filter_transcript(get_transcript(video_id))
                    videos.append(ChicoVideo(video_id, published_date, video_title, video_coins))

        with open(cache_filename, 'w') as file:
            json.dump([vars(video) for video in videos], file)

        with open(cache_filename, 'r') as file:
            return json.load(file)

    except Exception as e:
        print(f"Failed to retrieve a list of videos: {e}")
        return []


def filter_transcript(text):
    """"Filter transcript using OpenAI."""
    try:
        client = OpenAI()

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": """You are analyzing a cryptocurrency youtube content creator.
                Your goal is to identify all the crypto coins or protocols that youtube content creator 
                regards as profitable or 'bullish'. Please put all of these crypto coin's or protocol's 
                names in a single python list format, i.e. all names in single quotes inside square brackets, 
                separated by comma and no other text"""},
                {"role": "user", "content": text}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Failed to filter transcript: {e}")

# Example usage
if __name__ == "__main__":
    start_date = '2024,4,1'
    end_date = '2024,5,31'
    print(fetch_video_data(start_date, end_date))
