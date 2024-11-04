from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from qdrant_client.models import Filter

class NeuralSearcher:
    def __init__(self, collection_name):
        self.collection_name = collection_name
        #Initialize encoder model
        self.model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
        #initialize Adrant client
        self.qdrant_client = QdrantClient("http://10.192.4.185:6333")

    def search(self, text: str):
        #Convert text query into vector
        vector = self.model.encode(text).tolist()

        #Use 'vector' for search for closest vectors in the collection
        search_result = self.qdrant_client.query_points(
            collection_name=self.collection_name,
            query=vector,
            query_filter=None,
            limit=5
        ).points
        #In this function you are interested in payload only
        payloads = [hit.payload for hit in search_result]
        return payloads
    
    def filter(self, text: str):
        
        vector = self.model.encode(text).tolist()

        city_of_interest = "Berlin"

        # Define a filter for cities
        city_filter = Filter(**{
            "must": [{
                "key": "city", # Store city information in a field of the same name 
                "match": { # This condition checks if payload field has the requested value
                    "value": city_of_interest
                }
            }]
        })

        search_result = self.qdrant_client.query_points(
            collection_name=self.collection_name,
            query=vector,
            query_filter=city_filter,
            limit=5
        ).points
        payloads = [hit.payload for hit in search_result]
        return payloads