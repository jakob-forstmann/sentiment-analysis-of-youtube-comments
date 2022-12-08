import pandas as pd


class Converter():
    """
    convert the dataset into a usable dataframe"""

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

    def file_to_dataframe(self, file_names_prefix, files_extension, number_of_splitted_files=1):
        """convert a file splitted into number_of_splitted_files into a dataframe.The file is
            splitted to avoid a memory error during the conversion.Since the conversion might still
            take several minutes we use a smaller dataset created in the file relevance_sampling.py"""
        if len(self._converted_dataframes) == 0:
            for i in range(0, number_of_splitted_files):
                file_name = file_names_prefix+str(i)+files_extension
                rating = pd.read_json(file_name, encoding="ascii", lines=True)
                self._converted_dataframes.append(rating)
        return self._converted_dataframes

    def clean_data(self, operations: []):
        """ clean the converted dataframe with the following steps:
            - remove all columns except for rating and the review text
            - convert the star rating into three categories negative,neutral and positive
            - remove reviews with the same text and the same sentiment """
        for rating in self._converted_dataframes:
            for operation in operations:
                self.funcs_to_clean_data[operation](rating)
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
