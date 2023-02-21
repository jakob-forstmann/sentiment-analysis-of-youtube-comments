# How to reproduce the training results 

## Overview 
We used two different datasets to train our model.At first we trained our model with the [amazon reviews dataset](https://nijianmo.github.io/amazon/index.html). Unfortunately this model reached an accuracy of only about 50% on youtbe comments, so we decided to use a youtube comments dataset instead.
We also tested the impact of different pipelines to the accuarcy of the model in the file `experiments.train.py`. 

## used approach to get the youtube comments
This code imports the pandas library and a module called youtube_API, creates an instance of the youtube_API class, prompts the user to input a video ID, retrieves the comments from the YouTube video with the given ID using the youtube_API method "get_comments_from", converts the comments to a pandas series, and saves the series as a CSV file with a filename based on the video ID. In summary, this code fetches comments from a YouTube video and stores them in a CSV file for further analysis.


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
