from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from API.Youtube import Youtube
from API.Comment import Comment

# Initialization of FastAPI #
app = FastAPI()

# Adding all origins to CORS to allow for the api to be called #
allowed_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Initialization of Classes #
youtube = Youtube()
comment = Comment()

# No need, but kept it for debug purposes #
@app.get("/")
async def root():
    return {"message": "App Connected!"}

# Responds with Classified comments of Video Id #
@app.get("/fetch_all_comments/{video_id}")
async def get_youtube_video_comments(video_id: str):
    all_comments = youtube.get_all_comments_from_video(video_id)
    classified_comments = comment.get_classified_comments(all_comments)
    if classified_comments:
        return {'videoComments': classified_comments, "message": "All Comments Fetched!"}
    return {"message": "Comments Not Fetched!"}
