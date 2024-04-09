import os, json
from youtube_transcript_api import YouTubeTranscriptApi
from googleapiclient.discovery import build
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime

load_dotenv()

# Define API key and channel ID
API_KEY = os.getenv('YOUTUBE_API_KEY')
if not API_KEY:
    raise ValueError("YOUTUBE_API_KEY environment variable is not set.")

CHANNEL_ID = "UCHop-jpf-huVT1IYw79ymPw"

class ChicoVideo():
    """Class to store video parameters."""
    def __init__(self, video_id, video_date, video_title, video_coins) -> None:
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

def formatted_date(given_date):
    """Formating date to a necessary format"""
    date_format = given_date.split(',')
    return datetime(int(date_format[0]), int(date_format[1]), int(date_format[2]))


def fetch_video_data(start_date, end_date):
    """Retrieve video IDs, date, title, and coins list."""
    try:    
        # Define the YouTube API service. Achieving resource cleanup by using "with" statement
        with build("youtube", "v3", developerKey=API_KEY) as youtube:
            
            # Define the time period
            start_date_str = formatted_date(start_date).strftime('%Y-%m-%dT%H:%M:%SZ')
            end_date_str = formatted_date(end_date).strftime('%Y-%m-%dT%H:%M:%SZ')
        
            videos =[]
            request = youtube.search().list(
                part="snippet",
                channelId=CHANNEL_ID,
                publishedAfter=start_date_str,
                publishedBefore=end_date_str,
                maxResults=10,  # Adjust the number of results as needed
                type="video",   # Necessary for using videoDuration parameter
                videoDuration="medium" , # Video length from 4 to 20 minutes
            )
            response = request.execute()
            
            # Extract video IDs, date, title, and coim list fro, the response
            for item in response.get("items", []):
                if item["id"]["kind"] == "youtube#video":
                    video_id = item["id"]["videoId"]
                    published_date = item["snippet"]["publishedAt"]
                    video_title = item["snippet"]["title"]
                    video_coins = filter_transcript(get_transcript(video_id))
                    videos.append(ChicoVideo(video_id, published_date, video_title, video_coins))
            return videos

    except Exception as e:
        print(f"Failed to retrieve a list of videos: {e}")
        return []


def get_video_data(start_date, end_date):
    cache_filename = f'cached_data_{start_date}_{end_date}.json'
    if os.path.exists(cache_filename):
        with open(cache_filename, 'r') as file:
            return json.load(file)

    existing_data = []
    for filename in os.listdir('.'):
        if filename.startswith('cached_data'):
            cached_start_date, cached_end_date = filename.split('_')[2:0]
            if start_date <= cached_start_date and end_date >= cached_end_date:
                pass
        pass



    # Load cached data if available    
    # if os.path.exists('cached_data.json'):
    #     with open('cached_data.json', 'r') as file:
    #         return json.load(file)
        

    # Cache the data
    # with open('cached_data.json', 'w') as file:
    #     json.dump(videos, file, default=lambda x: x.__dict__)



def filter_transcript(text):
    """"Filter transcript using OpenAI."""
    try:
        client = OpenAI()

        # Using GPT-3.5 to generate the list of coins from the youtube video transcript
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

# if __name__ == "__main__":
#     fetch_video_data()

start_date = '2024,3,1'
end_date = '2024,12,31'
# print(fetch_video_data(start_date, end_date))
get_video_data(start_date, end_date)
