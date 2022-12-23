import os
import re
import nltk
import pandas as pd
import numpy as np

from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import EnglishStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('punkt')
nltk.download('stopwords')

lemmatizer = WordNetLemmatizer()
stemmer = EnglishStemmer()
english_stopwords = stopwords.words('english')

def filter_duplicates_entries(ratings: pd.DataFrame):
    """ drops reviews which have the same rating and the same review text"""
    # review_text = ratings["reviewText"]
    # duplicated_reviews = ratings["reviewText"].duplicated()
    # use slightly more code instead of simply groupBy because using groupBy requires
    # to concentate the resulting groups again resulting in slighty slower code.
    # since this code is already slow we avoid to slow down again.
    # ratings = ratings[review_text.isin(review_text[duplicated_reviews])].sort_values("reviewText")
    # print(ratings)
    return ratings.drop_duplicates(subset = ["reviewText", "overall"])


# Routine that converts a five star rating into three categories: negative,neutral and positive
def convert_star_rating(ratings: pd.DataFrame):
    converter = {
        1: "negative",
        2: "negative",
        3: "neutral",
        4: "positive",
        5: "positive"
    }
    return ratings["overall"].map(converter)

# Routine that deletes unused columns
def delete_unused_columns(ratings: pd.DataFrame):
    return ratings.drop(columns=["vote", "image", "style", "verified", "reviewTime", "summary",
                                  "unixReviewTime", "reviewerName", "asin", "reviewerID"], axis=1)

def remove_punctuations(tokens):
    return [re.sub('^[^A-Za-z]+', '', token) for token in tokens]

def remove_blank_tokens(tokens):
    return filter(lambda token: token != "", tokens)

def remove_stopwords(tokens):
    return [word for word in tokens if word not in english_stopwords]

def lemmatize_tokens(tokens):
    return [lemmatizer.lemmatize(token) for token in tokens]

def lower_reviews(review):
    return str(review).lower()

# Just declaring the Number of files variable
NUMBER_OF_FILES = 0
ratings = pd.DataFrame()

def get_all_ratings_docs():
    """creates a single dataframe containing all the docs"""

    # Retriving the file names with the help of os module
    data_file_names = os.listdir('./SplitedData/')
    # write the directory scructure you have for the dataset, and if in the same folder just comment and ignore the below cell
    data_file_names = [f'./SplitedData/{file_names}' for file_names in data_file_names]

    ratings = pd.DataFrame()

    for data_file_name in data_file_names:
        rating = pd.read_json(data_file_name, encoding="ascii", lines=True)
        ratings = pd.concat([ratings, rating])
    return ratings

def prepare_data():
    """ deletes unneccessary columns,converts a star rating and checks for duplicates"""

    cleaned_dataframes = pd.DataFrame()
    ratings = get_all_ratings_docs()
    ratings = delete_unused_columns(ratings)
    ratings['overall'] = convert_star_rating(ratings)
    ratings = filter_duplicates_entries(ratings)
    cleaned_dataframes = pd.concat([cleaned_dataframes, ratings], ignore_index=True)
    return cleaned_dataframes

def normalize_reviews(reviews):
    """ It normalizes the reviews"""
    preprocessed_reviews = pd.DataFrame()

    for review in reviews:
        review = lower_reviews(review)
        tokenized = word_tokenize(review)
        no_specials = remove_punctuations(tokenized)
        no_blanks = remove_blank_tokens(no_specials)
        no_stopwords = remove_stopwords(no_blanks)
        lemmatized = lemmatize_tokens(no_stopwords)
        preprocessed_reviews = pd.concat([preprocessed_reviews, pd.Series(' '.join(lemmatized))], ignore_index=True)

    return preprocessed_reviews

if __name__ == "__main__":

    clean_ratings = prepare_data()
    normalized_review = normalize_reviews(clean_ratings['reviewText'])
    clean_ratings["reviewText"] = normalized_review
    clean_ratings.to_csv('./normalized_data')
