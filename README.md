<div align="center">

# 🏛️ SEBI–RBI KYC Compliance RAG System

**A domain-specific Retrieval-Augmented Generation pipeline for Indian financial regulation**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT%20%2B%20Embeddings-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com)
[![FAISS](https://img.shields.io/badge/FAISS-Vector%20Search-00A3E0?style=for-the-badge&logo=meta&logoColor=white)](https://faiss.ai)
[![Colab](https://img.shields.io/badge/Google%20Colab-Runtime-F9AB00?style=for-the-badge&logo=googlecolab&logoColor=white)](https://colab.research.google.com)
[![Status](https://img.shields.io/badge/Status-Active-2ea44f?style=for-the-badge)]()
[![Domain](https://img.shields.io/badge/Domain-Fintech%20%7C%20RegTech-C9A44A?style=for-the-badge)]()

<br/>

> *Answers SEBI and RBI KYC compliance queries grounded in source regulatory documents —*
> *not model assumptions.*

</div>

---

## 🔴 The Problem

Financial institutions in India operate under a layered, frequently amended regulatory framework. SEBI and RBI KYC guidelines span hundreds of circulars, master directions, and amendments — many of which override or partially supersede earlier clauses.

Compliance teams and fintech engineers face a recurring challenge: getting accurate, clause-specific answers without manually combing through the full regulatory corpus.

> **Generic LLMs are unreliable here.** They hallucinate clause numbers, miss amendment history, and carry no source attribution. This project addresses that gap directly.

---

## 🟡 What This System Does

The pipeline ingests structured SEBI and RBI regulatory documents, filters to **active clauses only**, and builds a semantic search index over the corpus.

When a query is submitted:
1. The system retrieves the most relevant regulatory context from the vector index
2. That context is passed to an LLM as the **sole source of truth**
3. The model generates a grounded, source-backed compliance answer

> The system does not rely on the model's parametric knowledge. Every answer is traceable to a retrieved document chunk.

---

## 🔵 Technical Stack

| Layer | Technology | Purpose |
|:---|:---|:---|
| 🐍 Language | Python 3.10+ | Core pipeline |
| 🤖 LLM | OpenAI GPT | Answer generation |
| 🔢 Embeddings | text-embedding-ada-002 | Semantic encoding |
| 🗄️ Vector DB | FAISS | Similarity search |
| 📂 Dataset | Structured JSON | Regulatory corpus |
| ☁️ Runtime | Google Colab | Development & execution |

---

## 🟢 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              REGULATORY DOCUMENT CORPUS                     │
│        SEBI Circulars (2016–2023)  ·  RBI Master Direction  │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
              ┌────────────────────────┐
              │   Document Ingestion   │
              └────────────┬───────────┘
                           │
                           ▼
              ┌────────────────────────┐
              │  Active Clause Filter  │  ← removes superseded / inactive text
              └────────────┬───────────┘
                           │
                           ▼
              ┌────────────────────────┐
              │     Text Chunking      │  ← clause-level segmentation
              └────────────┬───────────┘
                           │
                           ▼
              ┌────────────────────────┐
              │  Embedding Generation  │  ← text-embedding-ada-002
              └────────────┬───────────┘
                           │
                           ▼
              ┌────────────────────────┐
              │   FAISS Vector Index   │
              └────────────┬───────────┘
                           │
               ┌───────────┴───────────┐
               │      Query Input      │
               └───────────┬───────────┘
                           │
                           ▼
              ┌────────────────────────┐
              │  Semantic Retrieval    │  ← top-k relevant chunks
              └────────────┬───────────┘
                           │
                           ▼
              ┌────────────────────────┐
              │  Grounded Generation   │  ← LLM constrained to context
              └────────────┬───────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│          Compliance Answer  +  Source Reference             │
└─────────────────────────────────────────────────────────────┘
```

---

## ⚙️ Engineering Highlights

### 🔹 Clause-Level Filtering
The ingestion pipeline identifies and removes outdated or inactive regulatory text before indexing. This prevents stale circulars from surfacing in retrieval and reduces the risk of incorrect answers based on superseded rules — a non-trivial problem given how frequently SEBI and RBI amend their KYC frameworks.

### 🔹 Semantic Retrieval over Legal Text
Embedding-based search enables the system to surface relevant clauses even when the query phrasing doesn't match regulatory language verbatim — critical given how differently compliance questions are framed versus how regulations are written.

### 🔹 Retrieval-Constrained Generation
The LLM is explicitly prompted to answer only from retrieved context. This architectural decision directly addresses hallucination risk in high-stakes compliance scenarios where a wrong clause reference carries real regulatory consequences.

### 🔹 Secure Credential Handling
API keys are separated from version-controlled code via environment variables, following standard fintech security and secrets management practices.

### 🔹 Modular Pipeline Design
Each stage — ingestion, filtering, chunking, indexing, retrieval, generation — is independently scoped, making the system extensible for production deployment or additional regulatory corpora.

---

## 💼 Why It Matters for Fintech

| Risk Area | Impact Without This System |
|:---|:---|
| 🔴 KYC Onboarding | Wrong circular applied → onboarding delays or rejection |
| 🔴 AML / CFT | Misclassified customer type → missed due diligence obligations |
| 🟡 Regulatory Audit | No source attribution → compliance trail gaps |
| 🟡 Circular Amendments | Outdated clause used → enforcement action exposure |

> This project demonstrates how RAG architecture can close the gap between regulatory complexity and operational accuracy — a pattern applicable across KYC, AML monitoring, credit risk disclosures, and audit reporting in the Indian fintech stack.

---

## 📊 Dataset Coverage

| Regulator | Document Type | Version Coverage |
|:---|:---|:---|
| 🟡 SEBI | KYC Circulars | 2016 – 2023 |
| 🔵 RBI | Master Direction on KYC | 2016 (as amended through 2023) |
| ⚪ FATF / PMLA | Overlay Guidelines | Referenced |

---

## 🧠 Skills Demonstrated

```
Retrieval-Augmented Generation (RAG)    Vector Databases (FAISS)
Embedding Generation & Similarity       Compliance Domain Modelling
LLM Prompt Engineering                  Secure API Key Management
Modular ML Pipeline Design              Indian Financial Regulation (SEBI / RBI)
```

---

## 🗺️ Roadmap

- [ ] 📎 Structured citation output with circular number and clause reference
- [ ] 🚀 FastAPI wrapper for REST-based query interface
- [ ] 🐳 Docker containerization for portable deployment
- [ ] 🔄 Automated ingestion of new SEBI/RBI circulars on release
- [ ] 🖥️ Frontend interface for compliance and legal teams
- [ ] 🔗 Multi-hop query support across related regulatory documents

---

## ⚠️ Disclaimer

This project is built for **research and technical demonstration purposes only**. It does not constitute legal or compliance advice. Outputs should not be used as the sole basis for regulatory decisions without independent verification by a qualified compliance professional.

---

<div align="center">

*Built to explore applied RAG in Indian fintech compliance.*
*Feedback and contributions welcome.*

**[⭐ Star this repo](.) · [🐛 Report an Issue](.) · [🤝 Contribute](.)**

</div>
