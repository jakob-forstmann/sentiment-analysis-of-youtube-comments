import random
import gzip
import json

import pandas as pd


class Converter():
    """
    converts a dataset into a usable dataframe"""

    def __init__(self):
        self.funcs_to_clean_data = {
            "delete": self.delete_unused_columns,
            "convert": self.convert_star_rating,
            "remove duplicates": self.filter_duplicates_entries
        }
        self._converted_dataframes = []
        self.star_rating_converter = {
            1: "negative",
            2: "negative",
            3: "neutral",
            4: "positive",
            5: "positive"
        }
        self.UNIX_TIMESTAMP_2015 = 1420070400 # calculated on https://www.unixtimestamp.com/


    def clean_data(self, rating: pd.DataFrame, operations=["delete", "convert", "remove duplicates"]) -> pd.DataFrame:
        """ clean a converted dataframe with the passed functions

            supported functions are:
            delete unused columns
            convert an amazon rating into three categories:positive, neutral, negative
            remove reviews with the same rating and the same review text
        """
        for operation in operations:
            try:
                self.funcs_to_clean_data[operation](rating)
            except KeyError(operation):
                print(f"operation {operation} not supported")
        return rating

    def convert_star_rating(self, rating: pd.DataFrame):
        """ converts a five star rating into three categories: negative, neutral and positive """
        rating["overall"] = rating["overall"].map(self.star_rating_converter)

    def delete_unused_columns(self, rating: pd.DataFrame):
        """ delete all columns except rating and the review text """
        rating.drop(columns=["image", "vote", "style", "verified", "reviewTime", "summary",
                             "unixReviewTime", "reviewerName", "asin", "reviewerID"],
                    axis=1, inplace=True)

    def filter_duplicates_entries(self, rating: pd.DataFrame):
        """ drops reviews which have the same rating and the same review text"""
        review_text = rating["reviewText"]
        duplicated_reviews = review_text.duplicated()
        # use slightly more code instead of simply groupBy because using groupBy requires
        # to concentate the resulting groups again resulting in slighty slower code.
        # since this code is already slow we avoid to slow down again.
        rating = rating[review_text.isin(review_text[duplicated_reviews])
                        ].sort_values("reviewText")
        rating.drop_duplicates(["reviewText", "overall"], inplace=True)

    def save_dataset(self, source_files: list[str], dest_file: str, n_reviews=2000):
        data = []
        for source in source_files:
            n_reviews_last_five_years = 0
            with gzip.open(source) as file:
                for line in file:
                    this_review = json.loads(line.strip())
                    if this_review['unixReviewTime'] < self.UNIX_TIMESTAMP_2015:
                        n_reviews_last_five_years += 1
            share = min(n_reviews / n_reviews_last_five_years, 1)

            with gzip.open(source) as file:
                for line in file:
                    this_review = json.loads(line.strip())
                    if this_review['unixReviewTime'] < self.UNIX_TIMESTAMP_2015 and random.random() < share:
                        data.append(this_review)
        random.shuffle(data)

        df = pd.DataFrame.from_dict(data)
        df = self.clean_data(df)

        df.to_csv(dest_file)

