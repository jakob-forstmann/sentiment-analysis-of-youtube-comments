"""
We split the dataset  Movies_and_TV_5.json into different files because otherwise
converting the json to a dataframe will result in a memory error. Even with this method
the conversion can take some minutes. After you have splitted the file change the variable 
NUMBER_OF_SPLIITED_FILES accordingly.
"""
import pandas as pd
NUMBER_OF_SPLITTED_FILES = 9


def prepare_data():
    """ deletes unneccessary columns,converts a star rating and checks for duplicates"""
    ratings = []
    for i in range(0, NUMBER_OF_SPLITTED_FILES):
        file_name = "Movies_and_TV0"+str(i)+".json"
        rating = pd.read_json(file_name, encoding="ascii", lines=True)
        delete_unused_columns(rating)
        convert_star_rating(rating)
        ratings.append(rating)


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
    rating = rating.drop(columns=["vote", "image", "style", "verified", "reviewTime", "summary",
                                  "unixReviewTime", "reviewerName", "asin", "reviewerID"], axis=1)


prepare_data()
