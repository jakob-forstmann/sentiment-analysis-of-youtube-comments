from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import GridSearchCV, train_test_split
import nltk
from nltk.stem import LancasterStemmer
from nltk.stem import WordNetLemmatizer
import pandas as pd
import argparse
from modul_preparation.main import get_available_indices
import test_different_pipelines as pipelines
nltk.download('stopwords')
nltk.download('wordnet')

# NOTE: For testing different pipelines only the first 100 entries of the datasets
# are used so each training of the model does not take 20 minute on my machine
training_results = []

def choose_dataset():
    usage = """specify the dataset to use: available commands are youtube or amazon which
    maps to either our smaller youtube comments or the amazon reviews dataset with 
    about 10.000 reviews equally taken from 5 categories """
    parser = argparse.ArgumentParser("training the model",usage)
    parser.add_argument("--dataset","-ds",default="youtube",
                        choices=["youtube","amazon"],dest="chosen_index")
    args = parser.parse_args()
    return args.chosen_index

def load_dataset() -> pd.DataFrame:
    user_choice = choose_dataset()
    indices = get_available_indices()
    index_to_load_from = indices[user_choice]
    return index_to_load_from.load_reviews()


def train_model_with(tokenizer):
    dataset = load_dataset()
    grid_search_cv = init_model(tokenizer)
    colum_names = dataset.columns
    X = dataset.loc[0:100, colum_names[0]]
    y = dataset.loc[0:100, colum_names[1]]
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


if __name__ == "__main__":
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
    training_results_df.to_csv("trainig_results_different_preprocessing.csv")
