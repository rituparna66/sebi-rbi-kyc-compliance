import json
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import pickle

with open("documents_for_embedding.json", "r", encoding="utf-8") as f:
    data = json.load(f)

documents = [
    Document(
        page_content=item["content"],
        metadata=item["metadata"] | {"id": item["id"]}
    )
    for item in data
]

# FAISS index (same as before)
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = FAISS.from_documents(documents, embeddings)
vectorstore.save_local("compliance_faiss_index")

# BM25 index (new in v2)
from langchain_community.retrievers import BM25Retriever
bm25_retriever = BM25Retriever.from_documents(documents)
bm25_retriever.k = 20

with open("bm25_retriever.pkl", "wb") as f:
    pickle.dump(bm25_retriever, f)

print("v2 index built: FAISS + BM25")
