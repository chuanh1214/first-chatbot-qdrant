from fastapi import FastAPI
#File neural_searcher
from neural_searcher import NeuralSearcher
#File hybrid_search
from hybrid_search import HybridSearcher

app = FastAPI()

#Create a neural searcher instance
neural_searcher = NeuralSearcher(collection_name="startups")

#Create a hybrid searcher instance
hybrid_searcher = HybridSearcher(collection_name="startupsFastembed")

#Neural_search
@app.get("/api/search")
def search_startups(q:str):
    return {"result": neural_searcher.search(text=q)}

@app.get("/api/filter")
def filter_startups(q:str):
    return {"result": neural_searcher.filter(text=q)}

#Hybrid_search
@app.get("/api/hybrid_search")
def search_startupsFastembed(q:str):
    return {"result": hybrid_searcher.search(text=q)}

@app.get("/api/hybrid_filter")
def filter_startupsFastembed(q:str):
    return {"resutl": hybrid_searcher.filter(text=q)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)