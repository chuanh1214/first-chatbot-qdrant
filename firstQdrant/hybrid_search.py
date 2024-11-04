from qdrant_client import QdrantClient
from qdrant_client import models

class HybridSearcher:
    DENSE_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    SPARSE_MODEL = "prithivida/Splade_PP_en_v1"
    def __init__(self, collection_name):
        self.collection_name = collection_name
        #initialize Adrant client
        self.qdrant_client = QdrantClient("http://10.192.4.185:6333")
        self.qdrant_client.set_model(self.DENSE_MODEL)
        self.qdrant_client.set_sparse_model(self.SPARSE_MODEL)

    def search(self, text: str):
        search_result = self.qdrant_client.query(
            collection_name=self.collection_name,
            query_text=text,
            query_filter=None,
            limit=5
        )
        # `search_result` contains found vector ids with similarity scores 

        # Select and return metadata
        metadata = [hit.metadata for hit in search_result]
        return metadata
    
    def filter(self, text: str):
        city_of_interest = "Berlin"

        city_filter = models.Filter(
            must=[
                models.FieldCondition(
                    key="city",
                    match=models.MatchValue(value=city_of_interest)
                )
            ]
        )

        search_result = self.qdrant_client.query(
            collection_name=self.collection_name,
            query_text=text,
            query_filter=city_filter,
            limit=5
        )
        # `search_result` contains found vector ids with similarity scores 

        # Select and return metadata
        metadata = [hit.metadata for hit in search_result]
        return metadata