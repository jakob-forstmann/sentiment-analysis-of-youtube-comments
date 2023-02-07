from fastapi import FastAPI;
from fastapi.middleware.cors import CORSMiddleware
import sys
# sys.path.insert(1, ".") # inserting path to import the module
from API.youtube_api import Youtube_API

# Initialization of FastAPI #
app = FastAPI()

# Adding all origins to CORS to allow for the api to be called #
allowed_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = allowed_origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

# Initialization of YouTubeAPI #
youtube_api = Youtube_API()

# video_id1 = "1CBQM2X8BZQ" # Actual on YouTube 3026
# video_id2 = "hewcSfw89e8" # Actual on YouTube 220
# video_id3 = "SKAIwoOt5qs" # Actual on YouTube 3408

@app.get("/")
async def root():
    return {"message": "App Connected!"}

@app.get("/fetch_all_comments/{video_id}")
async def get_youtube_video_comments(video_id: str):
    all_comments = youtube_api.get_all_comments_from_video(video_id)
    if all_comments:
        return {'videoComments': all_comments, "message": "All Comments Fetched!"}
    return {"message": "Comments Not Fetched!"}
