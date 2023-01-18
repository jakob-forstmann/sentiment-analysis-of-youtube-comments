from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import GridSearchCV
import nltk
from nltk.corpus import stopwords as nltk_stopwords
from nltk.stem import LancasterStemmer
from nltk.stem import WordNetLemmatizer

import pandas as pd
import json 
from elastic_search_API import elasticSearchAPI
import test_different_pipelines as pipelines
nltk.download('stopwords')

def load_dataset()->pd.DataFrame:
    amazon_mapping = {
                    "dynamic": "strict",
                    "properties": {
                        "overall":    {"type": "text"},
                        "reviewText":  {"type": "keyword"},
                      }
                  }
    # TODO:use the same instance of class elasticSearchAPI as in the file main.py 
    # currently not possible because main.py requires many files stored in the folder /datasets
    # after putting some of this code into a module this shouldn´t be a problem anymore             
    es_API = elasticSearchAPI("amazon_reviews",amazon_mapping)
    return es_API.load_reviews()
    
def train_model_with(tokenizer):
    dataset = load_dataset()
    grid_search_cv = init_model(tokenizer)
    X = dataset.loc[0:1000, "reviewText"]
    y = dataset.loc[0:1000, "overall"]
    grid_search_cv.fit(X, y)
    print(grid_search_cv.cv_results_)

def init_model(preprocesser)->GridSearchCV:
    pipeline = Pipeline([('vect', TfidfVectorizer()), ('clf', LinearSVC())])
    param_grid = [
        {'vect__tokenizer': [preprocesser, None]},
        {'clf': [LinearSVC(), RandomForestClassifier(), MLPClassifier()]}
        ]
    return GridSearchCV(pipeline, param_grid)


train_model_with(pipelines.StemTokenizer(lemmatizer=WordNetLemmatizer()))
train_model_with(pipelines.StemTokenizer(stemmer=LancasterStemmer(),lemmatizer=WordNetLemmatizer()))
train_model_with(pipelines.StandardPipeline)
train_model_with(pipelines.StandardPipeline(nltk_stopwords.words('english')))