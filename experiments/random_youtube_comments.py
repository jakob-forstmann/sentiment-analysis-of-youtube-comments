import pandas as pd
from web_application.backend.API.Youtube import Youtube

api_instance = Youtube()
video_id = input("video ID: ")
comments = api_instance.get_all_comments_from_video(video_id)

df = pd.Series(comments)
df.to_csv(f"data/labeled_youtube_comments_{video_id}.csv")
