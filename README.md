# sebi-rbi-kyc-compliance
SEBI–RBI COMPLIANCE RAG SYSTEM

* PROJECT SUMMARY

This project implements a Retrieval-Augmented Generation (RAG) system that answers compliance-related queries using structured SEBI and RBI regulatory documents.

The system retrieves relevant regulatory clauses and generates grounded responses using an LLM. It is designed to reduce hallucinations in financial compliance scenarios.

* WHY THIS PROJECT MATTERS

Financial institutions operate under strict regulatory oversight. Misinterpreting RBI or SEBI guidelines can lead to compliance risks.

This project demonstrates the ability to build a domain-specific RAG pipeline using regulatory data, implement semantic search over structured legal text, and generate context-aware responses grounded in source material.

* TECHNICAL STACK

- Python
- OpenAI API (LLM and Embeddings)
- FAISS for vector similarity search
- JSON-based regulatory dataset
- Google Colab

* SYSTEM ARCHITECTURE

- Regulatory document ingestion
- Active clause filtering
- Text chunking
- Embedding generation
- Vector index creation
- Semantic retrieval
- Context-grounded answer generation

The system answers strictly from retrieved regulatory context rather than relying on general model knowledge.

* ENGINEERING HIGHLIGHTS

- Designed clause-level filtering to remove outdated or inactive regulatory text
- Implemented embedding-based semantic retrieval
- Structured the pipeline to minimize irrelevant matches
- Separated API keys from version-controlled code
- Built a modular architecture for future API deployment

* SKILLS DEMONSTRATED

- Retrieval-Augmented Generation
- Vector databases
- Embeddings
- Compliance domain modeling
- Secure API key handling
- LLM integration workflow

* FUTURE IMPROVEMENTS

- Structured citation output with clause numbering
- FastAPI deployment
- Docker containerization
- Automated regulatory update ingestion
- Frontend interface for compliance users

* DISCLAIMER

This project is for research and technical demonstration purposes only and does not constitute legal advice.
