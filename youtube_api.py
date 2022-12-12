from api_KEY import KEY
from googleapiclient.discovery import build

class youtube_API:
    def __init__(self):
        self.youtube = build('youtube', 'v3', developerKey=KEY)
    
    def get_comments_from(self, video_ID, include_comments=False):
        fetch_comments =self.youtube.commentThreads().list(
            part = ["snippet", "replies"],
            videoId=video_ID,
            textFormat="plainText",
        )
        response = fetch_comments.execute()
        comments = []
        for item in response['items']:
            comments.append(item['snippet']['topLevelComment']['snippet']['textDisplay'])
            if include_comments and 'replies' in item.keys():
                for reply in item['replies']["comments"]:
                    print("It works!")
                    comments.append(reply['snippet']['textDisplay'])
        return comments
        
    def __del__(self):
        self.youtube.close()
    
