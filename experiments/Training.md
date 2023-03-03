# experiments

## Overview 
In this folder you can find the code used for the experiments we performed,the code to compute the distributions of the amazon  respectively the youtube comments dataset and the code to create these datasets. For the results of these experiments please look at the folder data. To reproduce our experiments simply execute the corresponding file with the prefix train f.ex to test the impact of the different pipelines on the accuarcy of the model execute `train_different_pipelines.py`. Furthermore you can test the impact of the different pipelines on the training using the amazon review dataset by executing `train_differenet_pipelines.py -ds amazaon` 

 
# used datasets:
We used two different datasets to train our model.At first we trained our model with the [amazon reviews dataset](https://nijianmo.github.io/amazon/index.html). Unfortunately this model reached an accuracy of only about 50% on youtbe comments, so we decided to use a youtube comments dataset instead.
We also tested the impact of different pipelines to the accuarcy of the model in the file `experiments.train.py`. 

## how to create the youtube comments dataset
0) obtain a valid Youtube API token
1 store your token in the file `web/application/API/API_KEYS.py `like this:
  ```
  file API_KEYS.py 
  YOUTUBE_API_KEY =##your API Key 
  ``` 
2) After you have ramdomly chosen videos, execute the file `random_youtube_comments.py`. 
   It will prompt you to input a video ID, retrieves the comments from the YouTube video with the given ID and stores them in a csv file.

### additional helper files
- `training_with_Amazon_reviews/download_datasets.sh`: this file will download the chosen categories from the website. Please store them in the data folder if you want to generate the amazon dataset from scratch

- `compute_distributions.py`: this file can be as a starting point to generate different plots. 
Please note that if you want to generate the number reviews per year for each category you have to crete the amazon dataset agian but this time keep the categories.
