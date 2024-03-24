from youtube_transcript_api import YouTubeTranscriptApi

transript_list = YouTubeTranscriptApi.get_transcript('ywvLImBgDNg')
for item in transript_list:
    print(item['text'])