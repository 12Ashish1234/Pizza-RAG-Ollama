from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever
from langchain_core.documents import Document
from langchain_classic.retrievers import ContextualCompressionRetriever
from langchain_community.document_compressors.flashrank_rerank import FlashrankRerank
import os
import pandas as pd
import pickle

# df = pd.read_csv("realistic_restaurant_reviews.csv")
df = pd.read_csv("restaurant_reviews_500.csv")

ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
embeddings = OllamaEmbeddings(model="mxbai-embed-large", base_url=ollama_base_url)

db_location = ".chroma_langchain_db"
bm25_pickle_file = "bm25_retriever.pkl"

add_documents = not os.path.exists(db_location)

documents = []
ids = []

for i, row in df.iterrows():
    document = Document(
        page_content = row["Title"] + " " + row["Review"],
        metadata = {"rating" : row["Rating"], "date": row["Date"]},
        id = str(i)
    )
    ids.append(str(i))
    documents.append(document)

vector_store = Chroma(
    collection_name="restaurant_reviews",
    embedding_function=embeddings,
    persist_directory=db_location,
)

if add_documents:
    vector_store.add_documents(documents=documents, ids=ids)


if os.path.exists(bm25_pickle_file):
    with open(bm25_pickle_file, "rb") as f:
        bm25_retriever = pickle.load(f)
else:
    bm25_retriever = BM25Retriever.from_documents(documents)
    bm25_retriever.k = 10
    with open(bm25_pickle_file, "wb") as f:
        pickle.dump(bm25_retriever, f)

chroma_retriever = vector_store.as_retriever(search_kwargs={"k": 10})

ensemble_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, chroma_retriever],
    weights=[0.5, 0.5]
)

compressor = FlashrankRerank()
retriever = ContextualCompressionRetriever(
    base_compressor=compressor, base_retriever=ensemble_retriever
)