import pandas as pd
from credentials import es_url
from elasticsearch import Elasticsearch
from elasticsearch import RequestError


class elasticSearchAPI():
    def __init__(self, index_name,mapping):
        try:
            self.es = Elasticsearch(es_url)
            self.es.info()
        except ConnectionError as err:
            print(f"Connection to elastic search failed with message {err}")
        self.index_name = index_name
        self.allowed_columns = list(mapping["properties"].keys())
        self.mapping = mapping

    def create_index(self):
        try:
            self.es.indices.create(index=self.index_name,mappings=self.mapping)
        except RequestError as err:
            if err.status_code ==400:
                print(f"inserting into existing index {self.index_name}")
            else:
                print(f"error creating index{err}")
       
    def store_reviews(self,reviews: pd.DataFrame):
        data = reviews.to_dict(orient="list")
        try:
            self.create_index()
            self.es.index(index=self.index_name,document=data, refresh="wait_for")
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



