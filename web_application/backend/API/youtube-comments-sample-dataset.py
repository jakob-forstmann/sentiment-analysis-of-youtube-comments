from API_KEYS import YOUTUBE_API_KEY
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import csv

api_key = YOUTUBE_API_KEY
api_service_name = "youtube"
api_version = "v3"

youtube = build(api_service_name, api_version, developerKey=api_key)

request = youtube.commentThreads().list(
    part="snippet",
    videoId="hj4kzcdd8ZE",
    maxResults=1000,
    textFormat="plainText"
)
response = request.execute()

with open("comments.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Comment", "Author", "Publish Date"])

    # Iterate through the comments and write them to the CSV file
    for item in response["items"]:
        comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        author = item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
        published_at = item["snippet"]["topLevelComment"]["snippet"]["publishedAt"]
        writer.writerow([comment, author, published_at])
