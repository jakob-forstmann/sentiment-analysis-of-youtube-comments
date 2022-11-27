"""
We split the dataset  Movies_and_TV_5.json into different files because otherwise
converting the json to a dataframe will result in a memory error. Even with this method
the conversion can take some minutes. After you have splitted the file change the variable.
NUMBER_OF_SPLIITED_FILES accordingly.
"""
import pandas as pd
NUMBER_OF_SPLITTED_FILES = 9


def prepare_data(file_name_prefix, file_name_suffix) -> [pd.DataFrame]:
    """ deletes unneccessary columns,converts a star rating and checks for duplicates"""
    cleaned_dataframes = []
    for i in range(0, NUMBER_OF_SPLITTED_FILES):
        file_name = file_name_prefix+str(i)+file_name_suffix
        rating = pd.read_json(file_name, encoding="ascii", lines=True)
        delete_unused_columns(rating)
        convert_star_rating(rating)
        filter_duplicates_entries(rating)
        cleaned_dataframes.append(rating)
    return cleaned_dataframes


def convert_star_rating(rating: pd.DataFrame):
    """ converts a five star rating into three categories: negative,neutral and positive """
    converter = {
        1: "negative",
        2: "negative",
        3: "neutral",
        4: "positive",
        5: "positive"
    }
    rating["overall"] = rating["overall"].map(converter)


def delete_unused_columns(rating: pd.DataFrame):
    """ delete all columns except rating and the review text """
    rating.drop(columns=["image", "vote", "style", "verified", "reviewTime", "summary",
                                  "unixReviewTime", "reviewerName", "asin", "reviewerID"],
                axis=1, inplace=True)


def filter_duplicates_entries(rating: pd.DataFrame):
    """ drops reviews which have the same rating and the same review text"""

    review_text = rating["reviewText"]
    duplicated_reviews = rating["reviewText"].duplicated()
    # use slightly more code instead of simply groupBy because using groupBy requires
    # to concentate the resulting groups again resulting in slighty slower code.
    # since this code is already slow we avoid to slow down again.
    rating = rating[review_text.isin(review_text[duplicated_reviews])
                    ].sort_values("reviewText")
    rating.drop_duplicates(["reviewText", "overall"], inplace=True)


prepare_data("Movies_and_TV0", ".json")
