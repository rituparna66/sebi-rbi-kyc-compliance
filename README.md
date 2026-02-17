# sebi-rbi-kyc-compliance
SEBI–RBI Compliance RAG System
Project Summary

Built a Retrieval-Augmented Generation (RAG) system that answers compliance-related queries using structured SEBI and RBI regulatory documents.

The system retrieves relevant clauses from curated regulatory text and generates grounded, context-aware responses using LLMs — minimizing hallucination risk in financial compliance scenarios.

Why This Project Matters

Financial institutions operate under strict regulatory oversight. Incorrect interpretation of RBI or SEBI guidelines can lead to compliance violations.

This system demonstrates:

Building domain-specific RAG pipelines

Working with regulatory/legal datasets

Reducing LLM hallucination through retrieval grounding

Secure API key handling

Structured data filtering and clause selection

Technical Stack

Python

OpenAI API (LLM + Embeddings)

FAISS (Vector Similarity Search)

JSON-based regulatory dataset

Google Colab

System Architecture

Regulatory document ingestion

Active clause filtering

Text chunking

Embedding generation

Vector index construction

Semantic retrieval

Context-grounded answer generation

The model responds strictly using retrieved compliance context.

Engineering Highlights

Designed clause-level filtering to avoid outdated regulatory text

Implemented embedding-based semantic search

Structured retrieval pipeline to minimize irrelevant matches

Separated secrets from code using environment variables

Built a modular pipeline for future API deployment

Key Skills Demonstrated

Retrieval-Augmented Generation

Vector databases

Embeddings

Compliance domain modeling

Secure configuration management

LLM integration in production-style workflow

Future Roadmap

Add structured citations in responses

API deployment (FastAPI)

Docker containerization

Automated regulation updates

Enterprise-ready UI

Disclaimer

This project is intended for research and technical demonstration purposes and does not constitute legal advice.
