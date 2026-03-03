from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

vectorstore = FAISS.load_local(
    "compliance_faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 6})

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

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

rag_chain = (
    {
        "context": itemgetter("input") | retriever,
        "question": itemgetter("input")
    }
    | prompt
    | llm
    | StrOutputParser()
)
