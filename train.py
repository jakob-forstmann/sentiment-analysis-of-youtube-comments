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

nltk.download('stopwords')

class StemTokenizer:
    def __init__(self, stopwords):
        self.tokenizer = re.compile("\w\w+")
        self.stopwords = set(stopwords)
        self.ps = PorterStemmer()
    def __call__(self, doc):
        tokens = self.tokenizer.findall(doc)
        return [self.ps.stem(t) for t in tokens if not t in self.stopwords]

pipeline = Pipeline([('vect', TfidfVectorizer()), ('clf', LinearSVC())])

param_grid = [
    {'vect__tokenizer': [StemTokenizer(nltk_stopwords.words('english')), None]},
    {'clf': [LinearSVC(), RandomForestClassifier(), MLPClassifier()]}
    ]
grid_search_cv = GridSearchCV(pipeline, param_grid)

dataset = pd.read_csv('data/our_dataset.csv')
X = dataset.loc[:, "reviewText"]
y = dataset.loc[:, "overall"]

grid_search_cv.fit(X, y)
print(grid_search_cv.cv_results_)
