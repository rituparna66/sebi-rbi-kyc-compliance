# KYC Compliance RAG — SEBI/RBI Regulatory Agent

> Retrieval-constrained LLM system that answers KYC/AML compliance questions from 50+ SEBI and RBI circulars, produces source-attributed audit trails, and auto-flags AML risk patterns — aligned to the RBI master circular schema.

**Stack:** LangChain · FAISS · GPT-3.5 · Streamlit · Python · RAGAS  
**Status:** v2 (hybrid retrieval + re-ranking + evaluation suite)

---

## Why this project exists

Indian financial institutions spend thousands of compliance-analyst hours cross-referencing SEBI and RBI circulars against customer onboarding flows. A compliance analyst typically needs 15–25 minutes to locate the right clause across the master circular, cross-check applicability, and document the decision for audit.

This system reduces that to **under 30 seconds** with full source attribution — every answer is grounded in the exact circular paragraph it came from, so the human analyst can verify in one click rather than re-reading the full document.

**Built for:** KYC teams, compliance officers, internal audit, and regtech products targeting Indian banking/NBFC clients.

---

## What v2 changes

v1 worked. v2 makes it production-defensible.

| Component | v1 | v2 | Why it matters |
|---|---|---|---|
| **Chunking** | Fixed 512-token splits | Semantic chunking on paragraph + clause boundaries | Stops splitting mid-clause; retrieval returns complete regulatory provisions |
| **Retrieval** | Dense FAISS only (k=5) | Hybrid: BM25 + FAISS, fused via RRF | Catches exact-term queries (e.g., "Rule 9(14)") that dense embeddings miss |
| **Ranking** | Similarity score only | Cross-encoder re-ranker (top-20 → top-5) | Re-ranker filters noisy matches; precision@5 jumped substantially |
| **Evaluation** | Manual spot-checks | RAGAS suite: faithfulness, answer relevance, context precision, context recall | Numbers, not vibes |
| **Observability** | Print statements | LangSmith tracing on every query | Debuggable in production |

### Measured improvements (v1 → v2)

Evaluated on a hand-labelled set of 50 compliance questions spanning KYC, AML, PEP screening, and beneficial ownership:

| Metric | v1 | v2 | Δ |
|---|---|---|---|
| **Faithfulness** (answer grounded in retrieved context) | 0.71 | 0.94 | +32% |
| **Answer relevance** | 0.78 | 0.89 | +14% |
| **Context precision@5** | 0.62 | 0.87 | +40% |
| **Hallucination rate** (manual review) | ~35% | near-zero | — |
| **Avg. response latency** | 2.1s | 2.6s | +0.5s (acceptable trade-off) |

> The hallucination reduction is the main safety win: in v1, GPT-3.5 would occasionally fabricate circular references. Retrieval-constrained generation with proper context precision eliminates this.

---

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                       User Query                             │
│  ("What's the KYC requirement for a foreign PEP?")           │
└─────────────────────────┬────────────────────────────────────┘
                          │
        ┌─────────────────┴─────────────────┐
        ▼                                   ▼
 ┌──────────────┐                   ┌──────────────┐
 │  BM25 (tf-idf)│                   │ FAISS (dense │
 │   top-20     │                   │ embeddings)  │
 │              │                   │   top-20     │
 └──────┬───────┘                   └──────┬───────┘
        └────────────┬──────────────────────┘
                     ▼
         ┌───────────────────────┐
         │  Reciprocal Rank      │
         │  Fusion (RRF)         │
         │  → top-20 candidates  │
         └───────────┬───────────┘
                     ▼
         ┌───────────────────────┐
         │  Cross-Encoder        │
         │  Re-ranker            │
         │  → top-5 chunks       │
         └───────────┬───────────┘
                     ▼
         ┌───────────────────────┐
         │  GPT-3.5 + structured │
         │  prompt (RBI schema)  │
         └───────────┬───────────┘
                     ▼
         ┌───────────────────────┐
         │  Output:              │
         │  • Answer             │
         │  • Source citations   │
         │  • AML risk flags     │
         │  • Audit trail JSON   │
         └───────────────────────┘
```

**Document processing (offline, one-time):**
- 50+ PDFs from SEBI + RBI ingested
- Section-aware parsing (preserves circular number, chapter, clause hierarchy)
- Semantic chunking via `langchain_experimental.text_splitter.SemanticChunker`
- Dual index: BM25 (sparse) + FAISS (dense, `text-embedding-3-small`)

---

## Output format

Every response returns structured JSON aligned to the RBI master circular schema:

```json
{
  "query": "What's the KYC requirement for a foreign PEP?",
  "answer": "Foreign Politically Exposed Persons (PEPs) require enhanced due diligence...",
  "sources": [
    {
      "circular": "RBI/DBR.AML.BC.No.81/14.01.001/2015-16",
      "clause": "Part III, Section 23(3)",
      "chunk_id": "rbi_2015_kyc_ch3_s23_p3",
      "relevance_score": 0.91
    }
  ],
  "aml_risk_flags": ["PEP_FOREIGN", "ENHANCED_DD_REQUIRED"],
  "audit_trail": {
    "timestamp": "2026-04-20T10:23:41Z",
    "model": "gpt-3.5-turbo",
    "retrieval_method": "hybrid_rrf_rerank",
    "chunks_retrieved": 20,
    "chunks_used": 5
  }
}
```

This structure means the output is **directly consumable** by downstream compliance systems — no parsing layer needed.

---

## Quickstart

```bash
# 1. Clone and install
git clone https://github.com/rituparna66/sebi-rbi-kyc-compliance.git
cd sebi-rbi-kyc-compliance
pip install -r requirements.txt

# 2. Set OpenAI key
export OPENAI_API_KEY="sk-..."

# 3. Build the index (runs once, ~5 min)
python scripts/build_index.py --docs_dir data/circulars/

# 4. Run evaluation suite
python scripts/evaluate.py --test_set data/eval/kyc_50q.json

# 5. Launch Streamlit UI
streamlit run app.py
```

### Expected output from evaluation

```
RAGAS Evaluation — v2
─────────────────────────────────────
Faithfulness:         0.94
Answer Relevance:     0.89
Context Precision@5:  0.87
Context Recall:       0.82
─────────────────────────────────────
50 questions · 2.6s avg latency
```

---

## Repository structure

```
sebi-rbi-kyc-compliance/
├── app.py                      # Streamlit UI
├── src/
│   ├── ingestion/              # PDF parsing + chunking
│   ├── retrieval/
│   │   ├── hybrid.py           # BM25 + FAISS + RRF
│   │   └── reranker.py         # Cross-encoder
│   ├── generation/
│   │   └── prompts.py          # Structured output prompts
│   └── evaluation/
│       └── ragas_runner.py     # Full metrics suite
├── scripts/
│   ├── build_index.py
│   └── evaluate.py
├── data/
│   ├── circulars/              # Source PDFs (git-ignored)
│   └── eval/
│       └── kyc_50q.json        # Hand-labelled eval set
├── notebooks/
│   └── v1_vs_v2_comparison.ipynb
└── docs/
    └── architecture.md
```

---

## Design decisions worth explaining

**Why GPT-3.5 and not GPT-4?**  
Compliance queries are well-scoped when retrieval is accurate. Once v2's hybrid+rerank pipeline pushes context precision above 0.85, GPT-3.5 is sufficient — and at ~10x lower cost, it makes the system actually deployable for mid-sized NBFCs. GPT-4 is a drop-in upgrade if a client needs it.

**Why hybrid retrieval?**  
Dense embeddings excel at semantic similarity ("enhanced due diligence" ≈ "additional verification requirements"). BM25 excels at exact-token matches ("Section 23(3)", "Form 60"). Compliance questions need both. RRF fusion gives us the union without tuning weights.

**Why a cross-encoder re-ranker on top?**  
Hybrid retrieval gets us to top-20 with high recall. The cross-encoder reads the query and each candidate together (rather than comparing precomputed vectors) and produces a far more accurate final ordering. The cost: ~200ms extra latency. The gain: 40% jump in context precision@5.

**Why hand-labelled evaluation instead of LLM-judge?**  
For regulatory use cases, LLM-judge metrics (e.g., GPT-4 scoring GPT-3.5) introduce correlated errors. A 50-question set scored manually by someone who understands the circulars is the only defensible eval for compliance work. RAGAS metrics complement but don't replace it.

---

## Roadmap

- [ ] v3: Fine-tuned embedding model on Indian regulatory corpus
- [ ] v3: Conversational memory with compliance context retention
- [ ] v3: Multi-document reasoning (cross-referencing between SEBI and RBI circulars in a single answer)
- [ ] v3: API endpoint + Dockerfile for deployment

---

## Author

**Rituparna Mohanty** — ML Engineer with a physics background specialising in RAG systems, quantitative ML, and regulatory/fintech applications.

- Portfolio: [rituparna66.netlify.app](https://rituparna66.netlify.app)
- LinkedIn: [rituparnamohanty-322a02112](https://linkedin.com/in/rituparnamohanty-322a02112)
- Email: mohanty.rituparna80@gmail.com

---

## License

MIT — use, fork, and adapt freely. Attribution appreciated but not required.


