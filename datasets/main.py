from elastic_search_API import elasticSearchAPI
from dataset_converter import save_dataset
import pandas as pd 
from os import path 

datasets_name = ["Electronics.json.gz","Software.json.gz","Home_and_Kitchen.json.gz",
                "Movies_and_Tv.json.gz",
                "All_Beauty.json.gz"]

if not path.isfile("reduced_dataset"):
    df_list = save_dataset(datasets_name,"reduced_dataset")

else: 
    df_list = pd.read_csv("reduced_dataset")
amazon_mapping = {
                    "dynamic": "strict",
                    "properties": {
                        "overall":    {"type": "text"},
                        "reviewText":  {"type": "keyword"},
                      }
                  }
es_API = elasticSearchAPI("amazon_reviews",amazon_mapping)
es_API.store_reviews(df_list,amazon_mapping)

df_list2 = es_API.load_reviews()
dfs_are_equal = df_list2.compare(df_list).empty
assert(dfs_are_equal == True)