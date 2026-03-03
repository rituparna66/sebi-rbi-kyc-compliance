import json
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

with open("documents_for_embedding.json", "r", encoding="utf-8") as f:
    data = json.load(f)

documents = [
    Document(
        page_content=item["content"],
        metadata=item["metadata"] | {"id": item["id"]}
    )
    for item in data
]

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

vectorstore = FAISS.from_documents(documents, embeddings)
vectorstore.save_local("compliance_faiss_index")

print("Index built successfully.")
