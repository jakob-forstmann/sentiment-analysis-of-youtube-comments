from os import path,strerror
import errno
import pandas as pd
from .elastic_search_API import elasticSearchAPI
from experiments.training_with_Amazon_reviews.dataset_converter import save_dataset

raw_amazon_dataset_path = ["../data/Electronics.json.gz","../data/Software.json.gz",
                    "../data/Home_and_Kitchen.json.gz",
                    "../data/Movies_and_Tv.json.gz",
                    "../data/All_Beauty.json.gz"]


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

def load_comments_from_disk(file_path:str):
    """ loads a csv file with the youtube comments 
    from file_path"""
    if not path.isfile(file_path) :
        raise FileNotFoundError(errno.ENOENT,strerror(errno.ENOENT), file_path)
    return pd.read_csv(file_path)

def load_reviews_from_disk(file_path:str):
    """
    loads a csv file with the amazon comments from file_path
    if the csv file does not exist it will be created"""
    if not path.isfile(file_path):
        reviews = create_dataset(raw_amazon_dataset_path)
        save_dataset("../data/amazon_reviews.csv",reviews)
    else:
        # like on https://stackoverflow.com/questions/918154/relative-paths-in-python
        dirname = path.dirname(__file__)
        filename = path.join(dirname, file_path)
        reviews = pd.read_csv(filename)
    return reviews

def load_comments():
    youtube_comments = load_comments_from_disk("./data/youtube_data.csv")
    youtube_mapping = prepare_mapping("comment","sentiment")
    youtube_index = elasticSearchAPI("youtube_comments", youtube_mapping)
    youtube_index.store_reviews(youtube_comments)
    return youtube_index

def load_reviews():
    amazon_reviews = load_reviews_from_disk("../data/amazon_reviews.csv")
    amazon_mapping = prepare_mapping("overall","reviewText")
    amazon_index =elasticSearchAPI("amazon_reviews",amazon_mapping)
    amazon_index.store_reviews(amazon_reviews)
    return amazon_index