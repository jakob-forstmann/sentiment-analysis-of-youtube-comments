"""
convert the data of dataframe with reviews from the amazon dataset into our 
three categories and cleans the data
"""
import random
import gzip
import json

import pandas as pd

def convert_star_rating(rating: pd.DataFrame):
    """ converts a five star rating into two  categories: negative,neutral and positive """
    star_rating_converter = {
        1: "negative",
        2: "negative",
        3: "neutral",
        4: "positive",
        5: "positive"
    }
    rating["overall"] = rating["overall"].map(star_rating_converter)


def delete_unused_columns(rating: pd.DataFrame,keep_review_time=False):
    """ delete all columns except rating and the review text """
    rating.drop(columns=["image", "vote", "style", "verified", "reviewTime", "summary",
                            "reviewerName", "asin", "reviewerID"],
                axis=1, inplace=True)
    if keep_review_time is False:
        rating.drop(columns=["unixReviewTime"])


def filter_duplicates_entries(rating: pd.DataFrame):
    """ drops reviews which have the same rating and the same review text"""
    rating.drop_duplicates(["reviewText", "overall"],inplace=True)

def clean_data(rating: pd.DataFrame,keep_review_time=False) -> pd.DataFrame:
    delete_unused_columns(rating)
    convert_star_rating(rating)
    filter_duplicates_entries(rating)
    return rating


def create_dataset(source_files: list[str],n_reviews=2000):
    """randomly picks 2000 reviews from different categories stored in source_files"""
    data = []
    # calculated on https://www.unixtimestamp.com/
    UNIX_TIMESTAMP_2015 = 1420070400
    for source in source_files:
        n_reviews_last_five_years = 0
        with gzip.open(source) as file:
            for line in file:
                this_review = json.loads(line.strip())
                if this_review['unixReviewTime'] > UNIX_TIMESTAMP_2015:
                    n_reviews_last_five_years += 1
        share = min(n_reviews / n_reviews_last_five_years, 1)
        with gzip.open(source) as file:
            for line in file:
                this_review = json.loads(line.strip())
                if this_review['unixReviewTime'] > UNIX_TIMESTAMP_2015 and random.random() < share:
                    data.append(this_review)
    random.shuffle(data)
    picked_reviews = pd.DataFrame.from_dict(data)
    return picked_reviews

def save_dataset(dest_file:str,reviews:pd.DataFrame):
    reviews.to_csv(dest_file,index=False)
