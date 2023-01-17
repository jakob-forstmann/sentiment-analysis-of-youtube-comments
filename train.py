import re

import nltk
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords as nltk_stopwords

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import GridSearchCV
import pandas as pd
from elastic_search_API import elasticSearchAPI
from spacy_pipeline import standardPipeline

nltk.download('stopwords')

class StemTokenizer:
    def __init__(self, stopwords):
        self.tokenizer = re.compile("\w\w+")
        self.stopwords = set(stopwords)
        self.ps = PorterStemmer()
    def __call__(self, doc):
        tokens = self.tokenizer.findall(doc)
        return [self.ps.stem(t) for t in tokens if not t in self.stopwords]

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
    
def train_model(dataset:pd.DataFrame,grid_search_cv:GridSearchCV):
    X = dataset.loc[:, "reviewText"]
    y = dataset.loc[:, "overall"]
    grid_search_cv.fit(X, y)
    print(grid_search_cv.cv_results_)

def init_model(preprocesser)->GridSearchCV:
    pipeline = Pipeline([('vect', TfidfVectorizer()), ('clf', LinearSVC())])
    param_grid = [
        {'vect__tokenizer': [preprocesser, None]},
        {'clf': [LinearSVC(), RandomForestClassifier(), MLPClassifier()]}
        ]
    return GridSearchCV(pipeline, param_grid)

dataset = load_dataset()
grid_search_cv = init_model(StemTokenizer(nltk_stopwords.words('english')))
#train_model(dataset,grid_search_cv)
