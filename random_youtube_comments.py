import pandas as pd
from youtube_api import youtube_API

api_instance = youtube_API()
video_id = input("video ID: ")
comments = api_instance.get_comments_from(video_id)

df = pd.Series(comments)
df.to_csv(f"data/labeled_youtube_comments_{video_id}.csv")
