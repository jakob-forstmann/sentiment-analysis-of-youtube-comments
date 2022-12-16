#!/usr/bin/env python
# coding: utf-8

# In[4]:


pip install google-api-python-client


# In[1]:


from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import csv


# In[11]:


api_key = "Youtube API"
api_service_name = "youtube"
api_version = "v3"

youtube = build(api_service_name, api_version, developerKey=api_key)


# In[12]:


request = youtube.commentThreads().list(
    part="snippet",
    videoId="hj4kzcdd8ZE",
    maxResults=15,
    textFormat="plainText"
)
response = request.execute()


# In[8]:


with open("comments.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Comment", "Author", "Publish Date"])

    # Iterate through the comments and write them to the CSV file
    for item in response["items"]:
        comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        author = item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
        published_at = item["snippet"]["topLevelComment"]["snippet"]["publishedAt"]
        writer.writerow([comment, author, published_at])


# In[ ]:




