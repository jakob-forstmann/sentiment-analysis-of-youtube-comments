import re

import nltk
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords as nltk_stopwords

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
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

pipeline = Pipeline([('vect', TfidfVectorizer()), ('clf', SVC(kernel='poly'))])

param_grid = [
    {},
    ]
grid_search_cv = GridSearchCV(pipeline, param_grid)

train_dataset = pd.read_csv('data/our_dataset_pos_neg.csv')
test_dataset = pd.read_csv('~/Downloads/Youtube Comments - Copy of Sheet2 1.csv')
print(test_dataset.head)
X_train = train_dataset.loc[:, "reviewText"]
y_train = train_dataset.loc[:, "overall"]

best_model = pipeline.fit(X_train, y_train)
#print(grid_search_cv.cv_results_)

#print()

X_test = test_dataset.iloc[0:300, 0]
y_test = test_dataset.iloc[0:300, 1]

prediction = best_model.predict(X_test)
test_score = best_model.score(X_test, y_test)

pos_share = y_test[y_test == 'positive'].size / 300

print(pos_share)

for t, p in zip(y_test, prediction):
    print(t, p)
print(test_score)
