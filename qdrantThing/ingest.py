from langchain.vectorstores import Qdrant
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

loader = PyPDFLoader("automl.pdf")
documents = loader.load()
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500,
    chunk_overlap = 50
)
texts = text_splitter.split_documents(documents)

#load the embedding model
model_name = "BAAI/bge-large-en"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': False}

embeddings = HuggingFaceBgeEmbeddings(
    model_name = model_name,
    model_kwargs = model_kwargs,
    encode_kwargs = encode_kwargs
)

print("Embedding Model Loaded............")

url = "http://10.192.4.185:6333"
collection_name = "chatbot_db_pdf"

qdrant = Qdrant.from_documents(
    texts,
    embeddings,
    url = url,
    prefer_grpc = False,
    collection_name = collection_name
)

print("Qdrant Index Created..............")