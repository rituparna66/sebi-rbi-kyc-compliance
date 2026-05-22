import pickle
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from operator import itemgetter
from sentence_transformers import CrossEncoder

# Load FAISS
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = FAISS.load_local(
    "compliance_faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)
faiss_retriever = vectorstore.as_retriever(search_kwargs={"k": 20})

# Load BM25
with open("bm25_retriever.pkl", "rb") as f:
    bm25_retriever = pickle.load(f)

# Hybrid retriever (BM25 + FAISS, equal weight)
hybrid_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, faiss_retriever],
    weights=[0.5, 0.5]
)

# Cross-encoder re-ranker
cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def rerank(inputs):
    query = inputs["query"]
    docs = inputs["docs"]
    pairs = [[query, doc.page_content] for doc in docs]
    scores = cross_encoder.predict(pairs)
    ranked = sorted(zip(scores, docs), key=lambda x: x[0], reverse=True)
    return [doc for _, doc in ranked[:5]]  # top 5 after reranking

# LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

prompt = PromptTemplate.from_template(
    """
You are a regulatory compliance assistant.
Answer ONLY using the provided regulatory clauses.
If the answer is not found, say: "Not found in regulations."

Context:
{context}

Question:
{question}
"""
)

def build_context(docs):
    return "\n\n".join([d.page_content for d in docs])

rag_chain = (
    {
        "docs": itemgetter("input") | hybrid_retriever,
        "query": itemgetter("input")
    }
    | RunnableLambda(lambda x: {
        "context": build_context(rerank({"query": x["query"], "docs": x["docs"]})),
        "question": x["query"]
    })
    | prompt
    | llm
    | StrOutputParser()
)
