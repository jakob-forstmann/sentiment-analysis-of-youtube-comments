# Project title: sentiment-analysis-of-english- youtube-comments
## Team members: 
- Kushal Gaywala, kushal.gaywala@stud.uni-heidelberg.de
- Rishabh Tiwari, rishabh.tiwari@stud.uni-heidelberg.de
- Jonathan Alexander Hirsch, ww251@stud.uni-heidelberg.de 
- Jakob Forstmann, jakob.forstmann@stud.uni-heidelberg.de

## utilzed libraries: 
- pandas: used to clean up the data 
- NLTK: used to preprocess the data
- re: used to implement regular expression during processing
- googleapiclient: used to fetch comments from youtube
## used dataset 
We use the Movies and TV [amazon reviews dataset](https://nijianmo.github.io/amazon/index.html) from the following paper:

Justifying recommendations using distantly-labeled reviews and fined-grained aspects

Jianmo Ni, Jiacheng Li, Julian McAuley
Empirical Methods in Natural Language Processing (EMNLP), 2019

## Project State 12.12.2022:

### planning state:

- did the conversion of the dataframe from csv format to a pandas dataframe
- dropped unused columns, removed duplicated entries and convert from an five star rating into our three categories
- since the dataset is too huge to do prepocessing on the entire dataset we did the prepocessing only on about the first thousand
  entries of the dataset
- we are working on splitting the dataset using relevance sampling instead of using just the first thousand entries
- we implemented a module to get the comments from a video with a given ID using the Google API Client (we created a Google Developer Key for that purpose)

### Future planning:
- Rishabh and Jonathan are going to use linear Support Vector Machines (SVM) for our classification problem since they among the best models for Sentiment    Analysis.
- they are going to use the data set for training and hyperparameter tuning of the SVM.
- finally the SVM should than be tested on comments from YouTube.
- Jakob will after he is done with the relevance sampling start to evaluate if any prepocessing is necessary for the raw comments fetched from youtube.
- Shortly after this is done we will start implement an API to acesss our model and the routes the user will use to acess the API
- Lastly we will implement the website most likely using svelte-kit

### High-level-architecture design:

- the conversion,the sampling and the statistics about the dataset are all in seperates classes
- They will, combinded with the code for the prepocessing, eventually become part of the module prepocessing
- to spit the entire dataset in a smaller dataset one has to follow three steps:
  - set the number of splitted file the entire dataset was split into
  - call converter.convert_to_dataframe() and converter.clean_data()
  - finally to call the code for the samling one has to use the statistics class to compute the number of reviews per sentiment
- after the orignal dataset was split into a smaller one, we can then proceed with the prepocessing definied in prepocessing.py

#### preprocessing pipeline
- The code for the code conversion into dataframe was pre-written by Jakob, we used pandas dataframe for the data processing.
- We first tried it doing it using the whole dataset but it overloaded my RAM(8GB) then we tried different methods as follows:
  - We first tried to use the code from the paper but it does not increase the performance so we ditched that idea.
  - Installing linux as secondary OS and increasing the swapped memory but it did not work.
  - Then, We tried to split files into 9 different files and again it was the same issue.
  - We also tried to process by converting into a zip format but neither of the methods increased the performance.
  - So, We settled on using only using 1 file and after we were satisfied with the normalized data.
- For the normalization of the data, We used NLTK library and it's different modules like:
  - Stem: Used WordNet Lemmatizer for lematization of the tokens after tokenization.
  - Snowball: Used snowball stemmer but it reduces an token to root form more than expected at that point it is not really a human understanble word, so didn't stemmed the data.
  - Corpus: Used to remove stopwords form the dataset
- re: It is a python module used to implement regular expression during processing to remove the unnecessary punctuations.
#### Example of the Preprocessing:
| overall | verified | reviewTime  | reviewerID     | asin       | style           | reviewerName | review_text               | summary | unixReviewTime |
| ------- | :------- | :---------- | :------------- | :--------- | :-------------- | :----------- | :------------------------ | :------ | :------------- |
| 5.0     | true     | 03 11, 2013 | A3478QRKQDOPQ2 | 0001527665 | Format: VHS Tape | jacki       | really happy they got evangelised .. spoiler alert==happy ending liked that..since started bit worrisome... but yeah great stories these missionary movies, really short only half hour but still great | great | 1362960000     |

After preprocessing:
- I cannot really see the lemmatization part of the processing in the normalized data and the stemming was overdone so did not use it, I think I am not able to understand it properly.
,overall,reviewText
0,positive,really happy got evangelised spoiler alert==happy ending liked since started bit worrisome yeah great story missionary movie really short half hour still great

### Data-Analysis:

#### statistics

- number of samples: 3410019

- number of positives reviews: 2694711

- number of negative reviews: 365608

- number of neutral reviews: 349700

number of revies per year

![number reviews per year](datasets/reviews_full_plot.png)

Because this dataset with 3410019 reviews is to big to perform to do preprocessing we are working on splitting the dataset to a choosen number of reviews.
For the smaller dataset we will test if keeping the unbalanced distribution is better or distributing the number of reviews per category equally.

#### example from the dataset

| overall | verified | reviewTime  | reviewerID     | asin       | style           | reviewerName | review_text               | summary | unixReviewTime |
| ------- | :------- | :---------- | :------------- | :--------- | :-------------- | :----------- | :------------------------ | :------ | :------------- |
| 5.0     | true     | 04 12, 2016 | A2CFV9UPFTTM10 | 0005419263 | Format:Audio CD | SuzieQ       | The little ones love this | Love it | 1460419200     |

We will only work with the columns overall and review_text,since we are not interested in all other columns.



## project log
Contribution by Rishabh and Jonathan:

Date: 15/11/22
1) https://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html - for the pipelining of the data and more traditional models.
2) https://www.tensorflow.org/tutorials - To train the data 
3) We studied about the sickit learn tutorial/implemented it/learning the usage of the sickit learn for the vectorization and training the data set. 

Date: 20/11/22

1) We continued to study scikit learn and its usage for text analysis.

Date 12/11/22

1) We studied about Fitting and predicting: estimator basics
2) Transformers and pre-processors
3) Pipelines: chaining pre-processors and estimators
4) Model evaluation


Next steps would be: We would like to train the model using vector machines. 
