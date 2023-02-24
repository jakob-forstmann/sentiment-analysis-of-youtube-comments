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
