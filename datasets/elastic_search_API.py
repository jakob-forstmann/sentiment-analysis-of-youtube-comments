import random
import pandas as pd
from credentials import es_url
from elasticsearch import Elasticsearch
from elasticsearch import RequestError


class elasticSearchAPI():
    def __init__(self, index_name):
        self.es = Elasticsearch(es_url)
        self.index_name = index_name
        self.allowed_columns = {}

    def create_index(self, mapping):
        es = Elasticsearch(es_url)
        self.allowed_columns = list(mapping["properties"].keys())
        es.indices.delete(index=self.index_name)
        try:
            es.indices.create(self.index_name, mapping)
        except RequestError:
            print("index already exists")

    def store_reviews(self, reviews: pd.DataFrame):
        data = reviews.to_dict(orient="list")
        try:
            self.es.index(self.index_name, data, refresh="wait_for")
        except RequestError as err:
            print(f" allowed columns: {self.allowed_columns}")
            print(f"raw error msg {err}")

    def load_reviews(self) -> pd.DataFrame:
        response = self.es.search(index=self.index_name)
        response_data = response["hits"]["hits"]
        final_columns = {}
        data = response_data[0]["_source"]
        for name in self.allowed_columns:
            column = data[name]
            final_columns[name] = column
        return pd.DataFrame(final_columns)



