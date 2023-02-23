from os import path,strerror
import errno
from elastic_search_API import elasticSearchAPI
from experiments.training_with_Amazon_reviews.dataset_converter import save_dataset
import pandas as pd

def prepare_mapping(first_column,second_column):
    """
    defines the mapping for the index 
    first_column and second_column must have the same name as in 
    the csv file in the data directory.
    """
    return {
                    "dynamic": "strict",
                    "properties": {
                        first_column:    {"type": "text"},
                        second_column:  {"type": "keyword"},
                      }
                  }

def create_amazon_data():
    """ 
    create an amazon dataset by randomly picking reviews from 5 categories
    see save_dataset for more details
    """
    datasets_name = ["../data/Electronics.json.gz","../data/Software.json.gz",
                    "../data/Home_and_Kitchen.json.gz",
                    "../data/Movies_and_Tv.json.gz",
                    "../data/All_Beauty.json.gz"]
    df_list = save_dataset(datasets_name,"../data/amazon_reviews.csv")
    return df_list


def load_comments_from_disk(file_path:str):
    """
    loads a csv file with the youtube comments from file_path
    """
    if not path.isfile(file_path) :
        raise FileNotFoundError(errno.ENOENT,strerror(errno.ENOENT), file_path)
    return pd.read_csv(file_path)

def load_reviews_from_disk(file_path:str):
    """
    loads a csv file with the amazon comments from file_path
    if the csv file does not exist it will be created
    """
    if not path.isfile(file_path) :
        df_list = create_amazon_data()
    else: 
        df_list = pd.read_csv(file_path)
    return df_list

def get_available_indices():
    return {
            "youtube": youtube_index,
            "amazon": amazon_index
            }


amazon_reviews = load_reviews_from_disk("../data/amazon_reviews.csv")
amazon_mapping = prepare_mapping("overall","reviewText")
amazon_index = elasticSearchAPI("amazon_reviews",amazon_mapping)
amazon_index.store_reviews(amazon_reviews)
youtube_comments = load_comments_from_disk("../data/youtube_data.csv")
youtube_mapping = prepare_mapping("comment","sentiment")
youtube_index = elasticSearchAPI("youtube_comments", youtube_mapping)
youtube_index.store_reviews(youtube_comments)

