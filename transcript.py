from youtube_transcript_api import YouTubeTranscriptApi

transcript_list = YouTubeTranscriptApi.get_transcript('ywvLImBgDNg')
for item in transcript_list:
    print(item['text'])