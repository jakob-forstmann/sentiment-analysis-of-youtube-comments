# Please try to Create API_KEYS file in the same Directory
from API.API_KEYS import YOUTUBE_API_KEY
from googleapiclient.discovery import build


class Youtube:
    def __init__(self):
        self.youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

    def get_all_comments_from_video(self, video_ID, include_comments=False):
        comments = []

        # Fetch and Read the first batch of comments #
        response = self.get_comments_from_video(video_ID)
        video_comments = self.read_comments_from_response(response)

        # Save first batch of comments #
        comments = video_comments

        # Get the response if more comments exists till next page token occur #
        # next_page_token = self.get_next_page_token_if_exists(response)
        while "nextPageToken" in response.keys():
            next_page_token = response["nextPageToken"]
            # Fetching and reading the comments #
            response = self.get_comments_from_video(video_ID, next_page_token)
            video_comments = self.read_comments_from_response(response)

            # Append the comments fetched from more pages #
            for video_comment in video_comments:
                print(video_comment)
                comments.append(video_comment)

            # Increment for Comments #
            # next_page_token = self.get_next_page_token_if_exists(response)

        return comments

    # Fetch the comments from the Youtube api with VideoID and NextPageToken if needed #
    def get_comments_from_video(self, videoId, pageToken="", part=["snippet", "replies"], textFormat="plainText", maxResults=100):
        response = self.youtube.commentThreads().list(
            part=part,
            videoId=videoId,
            pageToken=pageToken,
            textFormat=textFormat,
            maxResults=maxResults,
        ).execute()

        return response

    # Read comments from the response of youtube api #
    def read_comments_from_response(self, response, include_comments=False):
        comments = []  # To save comments
        for item in response['items']:
            comments.append(item['snippet']["topLevelComment"]
                            ["snippet"]["textDisplay"])
            if include_comments and 'replies' in item.keys():
                for reply in item['replies']["comments"]:
                    comments.append(reply['snippet']['textDisplay'])

        return comments

    def get_next_page_token_if_exists(self, response):
        if "nextPageToken" in response.keys():
            return response["nextPageToken"]

        return False

    def __del__(self):
        self.youtube.close()
