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
from elastic_search_API import elasticSearchAPI
import test_different_pipelines as pipelines
nltk.download('stopwords')
nltk.download('wordnet')


# NOTE: For testing different pipelines only the first 100 entries of the datasets
# are used so each training of the model does not take 20 minute on my machine
training_results = []


def load_dataset() -> pd.DataFrame:
    amazon_mapping = {
        "dynamic": "strict",
        "properties": {
            "overall":    {"type": "text"},
            "reviewText":  {"type": "keyword"},
        }
    }
    # TODO:use the same instance of class elasticSearchAPI as in the file main.py
    # currently not possible because main.py requires many files stored in the folder datasets
    # after putting the code into a module importing from main.py shouldn´t be a problem anymore
    es_API = elasticSearchAPI("amazon_reviews", amazon_mapping)
    return es_API.load_reviews()


def train_model_with(tokenizer):
    dataset = load_dataset()
    grid_search_cv = init_model(tokenizer)
    X = dataset.loc[0:100, "reviewText"]
    y = dataset.loc[0:100, "overall"]
    grid_search_cv.fit(X, y)
    training_results.append(grid_search_cv.cv_results_)


def init_model(preprocesser) -> GridSearchCV:
    pipeline = Pipeline([('vect', TfidfVectorizer()), ('clf', LinearSVC())])
    param_grid = [
        {'vect__tokenizer': [preprocesser, None]},
        {'clf': [LinearSVC(), RandomForestClassifier(), MLPClassifier()]}
    ]
    return GridSearchCV(pipeline, param_grid)


custom_stopwords = set(["delivery time", "product",
                       "price", "credit card", "video", "refund"])


# with Porter Stemmer and only alphanumeric characters
train_model_with(pipelines.StemTokenizer())

# with Porter Stemmer, only alphanumeric characters and Lemmatizer
stem_tokenizer = pipelines.StemTokenizer()
stem_tokenizer.enable_lemmatizer = True
stem_tokenizer.lemmatizer = WordNetLemmatizer()
train_model_with(stem_tokenizer)

# with Lancaster Stemmer and only alphanumeric characters
stem_tokenizer = pipelines.StemTokenizer()
stem_tokenizer.lemmatizer = LancasterStemmer()
train_model_with(stem_tokenizer)

# with Porter stemmer, only alphanumeric characters,custom stopwords and Lemmatizer
stem_tokenizer = pipelines.StemTokenizer()
stem_tokenizer.enable_lemmatizer = True
stem_tokenizer.lemmatizer = WordNetLemmatizer()
stem_tokenizer.stopwords.update(custom_stopwords)
train_model_with(stem_tokenizer)

stem_tokenizer = pipelines.StemTokenizer(r"(\w+)|((?::|;|=)(?:-)?(?:\)|D|P))")
stem_tokenizer.lemmatizer = WordNetLemmatizer()
stem_tokenizer.stopwords.update(custom_stopwords)
train_model_with(stem_tokenizer)

# with stopwords from spacy and only alphanumeric characters
train_model_with(pipelines.StandardPipeline())


# with stopwords from spacy,only alphanumeric characters and lemmatizer
spacy_standard_pipeline = pipelines.StandardPipeline()
spacy_standard_pipeline.enable_lemmatizer = True
train_model_with(spacy_standard_pipeline)

# with custom stopwords,only alphanumeric characters and lemmatizer
spacy_pipeline = pipelines.StandardPipeline()
spacy_pipeline.stop_words = spacy_pipeline.stop_words.union(custom_stopwords)
spacy_standard_pipeline.enable_lemmatizer = True
train_model_with(spacy_pipeline)

training_results_df = pd.DataFrame(training_results)
training_results_df.to_csv("trainig_results")
