from api_KEY import KEY
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class youtube_API:
    def __init__(self):
        self.youtube = build('youtube', 'v3', developerKey=KEY)
    
    def get_comments_from(self, video_ID, include_replies=False):
        fetch_comments =self.youtube.commentThreads().list(
            part = ["snippet", "replies"],
            videoId=video_ID,
            textFormat="plainText",
        )
        
        comments = []
        try:
            response = fetch_comments.execute()
        except HttpError:
            pass
        else:
            for item in response['items']:
                comments.append(item['snippet']['topLevelComment']['snippet']['textDisplay'])
                if include_replies and 'replies' in item.keys():
                    for reply in item['replies']["comments"]:
                        comments.append(reply['snippet']['textDisplay'])
        return comments
        
    def __del__(self):
        self.youtube.close()
    
