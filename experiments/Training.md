# How to reproduce the training results 

## Overview 
We used two different datasets to train our model.At first we trained our model with the [amazon reviews dataset](https://nijianmo.github.io/amazon/index.html). Unfortunately this model reached an accuracy of only about 50% on youtbe comments, so we decided to use a youtube comments dataset instead.
We also tested the impact of different pipelines to the accuarcy of the model in the file `experiments.train.py`. 

## used approach to get the youtube comments
This code imports the pandas library and a module called youtube_API, creates an instance of the youtube_API class, prompts the user to input a video ID, retrieves the comments from the YouTube video with the given ID using the youtube_API method "get_comments_from", converts the comments to a pandas series, and saves the series as a CSV file with a filename based on the video ID. In summary, this code fetches comments from a YouTube video and stores them in a CSV file for further analysis.


Approach Used: 

The code uses the Google API Python client library to connect to the YouTube Data API and retrieve comments from a specific YouTube video.

First, the necessary libraries are imported, including the build and HttpError classes from the googleapiclient.discovery module, as well as the csv module for writing the comments to a CSV file.

Next, the API key, API service name, and API version are set up. The API key is a unique identifier that allows the code to authenticate with the YouTube Data API.

Then, the YouTube API client is built using the build() method, passing in the API service name, API version, and API key as arguments.

After that, a request object is created to retrieve comment threads from a specific YouTube video. The part parameter specifies which resource properties should be included in the API response, while textFormat specifies the format in which the comment text should be returned. The videoId parameter specifies the ID of the YouTube video from which to retrieve comments.

Once the request object is set up, the execute() method is called on the YouTube API client to execute the API request and retrieve the comment threads.

Finally, the comments are written to a CSV file named "comments.csv" using the csv module. The code iterates through the comment threads returned in the API response, extracts the comment text from each thread, and writes it to the CSV file.

How can it be reproduced? :

To reproduce the results of this code, we need to follow these steps:

Obtain a valid YouTube Data API key from Google. We can do this by creating a new project in the Google Cloud Console, enabling the YouTube Data API, and creating a new API key in the API credentials section.

Install the Google API Python client library by running the command pip install google-api-python-client in your command prompt or terminal.

Copy the code into a new Python script.

Replace "Your_API_Key" in the api_key variable with your own valid YouTube Data API key.

Replace "unjcGyx8AKc" in the videoId parameter of the request object with the ID of the YouTube video from which you want to retrieve comments. You can find the video ID in the URL of the YouTube video.

If we want to retrieve more or fewer than 20 comments, we can adjust the maxResults parameter in the request object.

Run the Python script, and it will retrieve the comments from the specified YouTube video and write them to a CSV file named "comments.csv" in the same directory as the script.

Note that the CSV file will only contain the comment text itself. If we want to include additional information about the comments, such as the author or timestamp, we need to modify the writerow() function accordingly.


## the amazon review dataset 
Since this dataset is fairly large we limited ourself to the 5 core datasets and chose five categories. From each category we included d about 2000 reviews 
in our training dataset.The five chosen categories are:
-All Beauty
-Electronics
-Home and Kitchen
-Movie and TV Software

There is a helper script download_datasets.sh which will download the chosen five categories from the website. 
### how to reproduce the training results using the amazon review dataset
This guide assumes a running elastic search istance on your local machine. Furthermore you will need to create a file `credentials.py` in the folder module_preparation containg your elastic user name and password.
After everthing is set up you can follow these steps to reprocude our training results:
1) execute the file `modul_preparation.main.py`. This file will load the datasets and store them in elastic search.
2) execute the file `modul_preparation/train.py`. 
