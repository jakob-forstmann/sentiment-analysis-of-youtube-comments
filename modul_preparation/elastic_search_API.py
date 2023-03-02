import pandas as pd
from itertools import count
from elasticsearch import Elasticsearch
from elasticsearch import RequestError,ConflictError
from .credentials import es_url

class elasticSearchAPI():
    """ 
    defines methods to create an index and load or store data to it
    creating an instance of this class with an already existing index name 
    uses the already created index with the passed name from elasticsearch
    """
    _autoincrement_id = count(0)
    created_indicies = {}
    def __init__(self,index_name,mapping=None):
        try:
            self.es = Elasticsearch(es_url)
            self.es.info()
        except ConnectionError as err:
            print(f"Connection to elastic search failed with message {err}")
        self.index_name = index_name
        self.document_id = self._autoincrement_id
        self.allowed_columns = list(mapping["properties"].keys())
        self.mapping = mapping
    
    def create_index(self):
        """
        create an index with a strict mapping with the named passed to the constructor
        """
        try:
            self.es.indices.create(index=self.index_name,mappings=self.mapping)
        except RequestError as err:
            if err.status_code ==400:
                print(f"inserting into existing index {self.index_name}")
            else:
                print(f"error creating index{err}")

    def store_reviews(self,reviews: pd.DataFrame):
        """
        stores a dataframe into the index passed to the constructor 
        throws an error if the strict mapping defined in the constructor 
        is not matched
        """
        data = reviews.to_dict(orient="list")
        try:
            self.create_index()
            self.es.create(index=self.index_name,id=self.document_id,document=data,refresh="wait_for")
        except ConflictError:
            print(f"the data with the columns {reviews.columns}was already inserted")
        except RequestError as err:
            print(f" allowed columns: {self.allowed_columns}")
            print(f"raw error msg {err}")

    def load_reviews(self) -> pd.DataFrame:
        response = self.es.search(index=self.index_name)
        response_data = response["hits"]["hits"]
        final_columns = {}
        if response["hits"]["total"]["value"]<=0:
            print("no results")
        else:
            data = response_data[0]["_source"]
            for name in self.allowed_columns:
                column = data[name]
                final_columns[name] = column
        return pd.DataFrame(final_columns)
