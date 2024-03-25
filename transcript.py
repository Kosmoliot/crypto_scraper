from youtube_transcript_api import YouTubeTranscriptApi
from googleapiclient.discovery import build

def transcript(video_id):
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    video_transc = []
    for item in transcript_list:
        video_transc.append(item['text'])
    return ' '.join(video_transc)
    


# # Define API key and channel ID
# API_KEY = "AIzaSyDXIB6xTdYB996unF3cq8rwFb8wGh63WjE"
# CHANNEL_ID = "UCHop-jpf-huVT1IYw79ymPw"

# # Define the YouTube API service
# youtube = build("youtube", "v3", developerKey=API_KEY)

# # Retrieve videos from the channel
# request = youtube.search().list(
#     part="snippet",
#     channelId=CHANNEL_ID,
#     maxResults=50  # Adjust the number of results as needed
# )
# response = request.execute()

# # Extract video IDs from the response
# video_ids = [item["id"]["videoId"] for item in response["items"] if item["id"]["kind"] == "youtube#video"]

print(transcript('qKL0EbFms0g'))
