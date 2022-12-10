import pandas as pd
from dataset_statistics import DataSet


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

    def file_to_dataframe(self, file_names_prefix, files_extension) -> []:
        """ converts each splitted_file into one dataframe
            returns a list of dataframes """
        if len(self._converted_dataframes) == 0:
            for i in range(0, DataSet.number_of_splitted_files):
                file_name = file_names_prefix+str(i)+files_extension
                rating = pd.read_json(file_name, encoding="ascii", lines=True)
                self._converted_dataframes.append(rating)
        return self._converted_dataframes

    def clean_data(self, operations=["delete", "convert", "remove duplicates"]) -> []:
        """ clean a converted dataframe with the passed functions

            supported functions are:
            delete unused columns
            convert an amazon rating into three categories:positive, neutral, negative
            remove reviews with the same rating and the same review text
        """
        for rating in self._converted_dataframes:
            for operation in operations:
                try:
                    self.funcs_to_clean_data[operation](rating)
                except KeyError(operation):
                    print(f"operation {operation} not supported")
        return self._converted_dataframes

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
