from rag_chain import rag_chain

question = "Is Aadhaar mandatory for KYC under Indian regulations?"

response = rag_chain.invoke({"input": question})

print("\nAnswer:\n")
print(response)
