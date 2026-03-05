
# sebi-rbi-kyc-compliance

# SEBI–RBI KYC Compliance RAG System

> A domain-specific Retrieval-Augmented Generation pipeline for answering SEBI and RBI KYC compliance queries — grounded in source regulatory documents, not model assumptions.

---

## The Problem

Financial institutions in India operate under a layered and frequently amended regulatory framework. SEBI and RBI KYC guidelines span hundreds of circulars, master directions, and amendments — many of which override or partially supersede earlier clauses.

Compliance teams and fintech engineers face a recurring challenge: getting accurate, clause-specific answers without manually combing through the full regulatory corpus. Generic LLM responses are unreliable here — they hallucinate clause numbers, miss amendment history, and carry no source attribution.

This project addresses that gap directly.

---

## What This System Does

The pipeline ingests structured SEBI and RBI regulatory documents, filters to active clauses only, and builds a semantic search index over the corpus. When a query is submitted, it retrieves the most relevant regulatory context and passes it to an LLM — which generates a grounded, source-backed response.

The system does not rely on the model's parametric knowledge. Every answer is traceable to a retrieved document chunk.

---

## Technical Stack

| Layer | Technology |
|---|---|
| Language | Python 3 |
| LLM + Embeddings | OpenAI API (GPT + text-embedding-ada-002) |
| Vector Search | FAISS |
| Regulatory Dataset | Structured JSON |
| Runtime | Google Colab |

---

## System Architecture

```
Regulatory Documents (SEBI Circulars + RBI Master Directions)
        │
        ▼
  Document Ingestion
        │
        ▼
  Active Clause Filtering         ← removes superseded / inactive text
        │
        ▼
  Text Chunking                   ← clause-level segmentation
        │
        ▼
  Embedding Generation            ← OpenAI text-embedding-ada-002
        │
        ▼
  FAISS Vector Index
        │
   Query Input
        │
        ▼
  Semantic Retrieval              ← top-k relevant chunks
        │
        ▼
  Context-Grounded Generation     ← LLM constrained to retrieved context
        │
        ▼
  Compliance Answer + Source Reference
```

---

## Engineering Highlights

**Clause-level filtering** — The ingestion pipeline identifies and removes outdated or inactive regulatory text before indexing. This prevents stale circulars from surfacing in retrieval and reduces the risk of incorrect answers based on superseded rules.

**Semantic retrieval over legal text** — Embedding-based search enables the system to surface relevant clauses even when the query phrasing doesn't match regulatory language verbatim — a critical requirement given how differently compliance questions are framed versus how regulations are written.

**Retrieval-constrained generation** — The LLM is explicitly prompted to answer only from retrieved context. This architectural decision directly addresses hallucination risk in high-stakes compliance scenarios.

**Secure credential handling** — API keys are separated from version-controlled code via environment variables, following standard fintech security practices.

**Modular pipeline design** — Each stage (ingestion, filtering, chunking, indexing, retrieval, generation) is independently scoped, making the system extensible for production deployment or additional regulatory corpora.

---

## Why It Matters for Fintech

Regulatory misinterpretation is not just a compliance inconvenience — it carries direct financial and operational risk. Incorrect KYC procedures can trigger RBI/SEBI enforcement action, delay onboarding pipelines, and expose institutions to AML/CFT liability.

This project demonstrates how RAG architecture can be applied to close the gap between regulatory complexity and operational accuracy — a pattern applicable across KYC, AML monitoring, credit risk disclosures, and audit reporting in the Indian fintech stack.

---

## Skills Demonstrated

- Retrieval-Augmented Generation (RAG) architecture
- Vector database design and semantic search (FAISS)
- Embedding generation and similarity-based retrieval
- Compliance domain modeling for Indian financial regulation
- LLM prompt engineering for grounded, constrained generation
- Secure API key management
- Modular ML pipeline design

---

## Roadmap

- [ ] Structured citation output with circular number and clause reference
- [ ] FastAPI wrapper for REST-based query interface
- [ ] Docker containerization for portable deployment
- [ ] Automated ingestion of new SEBI/RBI circulars on release
- [ ] Frontend interface for compliance and legal teams
- [ ] Support for multi-hop queries across related regulatory documents

---

## Dataset Coverage

| Regulator | Document Type | Coverage |
|---|---|---|
| SEBI | KYC Circulars | 2016 – 2023 |
| RBI | Master Direction on KYC | 2016 (as amended through 2023) |
| FATF / PMLA | Overlay Guidelines | Referenced |

---

## Disclaimer

This project is built for research and technical demonstration purposes only. It does not constitute legal or compliance advice. Outputs should not be used as the sole basis for regulatory decisions without independent verification by a qualified compliance professional.

---

*Built to explore applied RAG in Indian fintech compliance. Feedback and contributions welcome.*
