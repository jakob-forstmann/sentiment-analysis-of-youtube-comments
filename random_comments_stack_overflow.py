import json
import urllib.request
import string
import random

import googleapiclient

from youtube_api import youtube_API
from api_KEY import KEY as API_KEY

count = 50
random = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(3))

urlData = "https://www.googleapis.com/youtube/v3/search?key={}&maxResults={}&part=snippet&type=video&q={}".format(API_KEY,count,random)
webURL = urllib.request.urlopen(urlData)
data = webURL.read()
encoding = webURL.info().get_content_charset('utf-8')
results = json.loads(data.decode(encoding))

youtube_api = youtube_API()
all_comments = []

for data in results['items']:
    videoId = (data['id']['videoId'])
    try:
        comments = youtube_api.get_comments_from(videoId)
        all_comments.extend(comments)
    except googleapiclient.errors.HttpError:
        continue

all_comments_string = "\n".join(all_comments)
with open("data/labeled_youtube_data.csv", "w") as file:
    file.write(all_comments_string)
   

