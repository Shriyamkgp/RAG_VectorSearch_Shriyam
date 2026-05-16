# RAG Retrieval Benchmark: Cosine Similarity vs. Query Expansion

A local Retrieval-Augmented Generation (RAG) pipeline that benchmarks two retrieval
strategies on a technical corpus, demonstrating how AI-enhanced query expansion
outperforms raw vector search on abstract queries.

---

## Overview

When a user's query uses abstract language ("what if something breaks?") but the
corpus uses technical terms ("failover", "health-check"), raw cosine similarity
fails. This project demonstrates that gap and how query expansion bridges it.

---

## Retrieval Strategies

| Strategy | Method                | Description                                                |
| -------- | --------------------- | ---------------------------------------------------------- |
| **A**    | Raw Vector Search     | Embeds the query as it is and retrieves via cosine similarity |
| **B**    | AI-Enhanced Retrieval | Expands the query with technical synonyms before embedding |

---

## Project Structure

```

├── main.py # Benchmark entry point
├── src/
│ ├── embedding.py # Embedding and generative models
│ ├── orchestration.py # RAG pipeline orchestrator
│ └── storage.py # FAISS vector store
├── test/
│ └── test_pipeline.py # Unit tests
├── docs/
│ ├── retrieval_benchmark.md # Strategy A vs B output analysis
│ └── technical_design.md # Design decisions and production path
├── output.json # Benchmark results
└── requirements.txt

```

---

## Quickstart

```bash
# Install dependencies
pip install -r requirements.txt

# Run benchmark
python main.py

# Run tests
pytest test/test_pipeline.py -v
```

---

## Results Summary

Query expansion (Strategy B) consistently outperforms raw search (Strategy A) by:

- Retrieving missed but relevant chunks (e.g. Redis caching for traffic queries)
- Replacing noise documents with semantically correct results
- Re-ranking results closer to user intent

See [`docs/retrieval_benchmark.md`](docs/retrieval_benchmark.md) for the full
side-by-side output analysis.

---

## Production Path

This pipeline uses GTR-T5-Large and FAISS as local proxies for Vertex AI
Text Embedding API and Vertex AI Vector Search. See
[`docs/technical_design.md`](docs/technical_design.md) for the migration plan.
