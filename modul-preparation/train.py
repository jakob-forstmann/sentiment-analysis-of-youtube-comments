import joblib
import re

import nltk
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords as nltk_stopwords
import pandas as pd
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV, train_test_split

from datasets.elastic_search_API import elasticSearchAPI


class StemTokenizer:
    def __init__(self, regex=r"\w\w+"):
        self.tokenizer = re.compile(regex)
        self.stemmer = PorterStemmer()

    def __call__(self, doc):
        tokens = self.tokenizer.findall(doc)
        tokens = [self.stemmer.stem(t) for t in tokens]
        return tokens


def load_dataset() -> pd.DataFrame:
    amazon_mapping = {
        "dynamic": "strict",
        "properties": {
            "overall":    {"type": "text"},
            "reviewText":  {"type": "keyword"},
        }
    }
    # TODO: rename to YouTube
    es_API = elasticSearchAPI("amazon_reviews", amazon_mapping)
    return es_API.load_reviews()

nltk.download('stopwords')
youtube_data = load_dataset()
comments_train, comments_test, sentiment_train, sentiment_test = train_test_split(
    youtube_data,
    test_size=0.25,
    random_state=42,
)

pipeline = Pipeline([('vect', TfidfVectorizer()), ('clf', LinearSVC())])
param_grid = {
    'vect__tokenizer': [None, StemTokenizer()],
    'vect__ngram_range': [(1, 1), (1, 2)],
    'vect__stop_words': [None, set(nltk_stopwords.words('english'))],
    'vect__sublinear_tf': [False, True],
}

grid_search_cv = GridSearchCV(pipeline, param_grid)
best_model = grid_search_cv.fit(youtube_data.loc[:, 'comments'], youtube_data.loc[:, 'sentiment'])
test_accuracy = best_model.score(comments_test, sentiment_test)

pd.DataFrame(grid_search_cv.cv_results_).to_csv('cv_results.csv')
joblib.dump(best_model, './youtube_model.joblib')

print("Training finished")
print(f"Final model as test accuracy of {test_accuracy:2%}.")
