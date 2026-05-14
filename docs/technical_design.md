# Technical Design

## 1. Similarity Metric: Cosine vs. Euclidean

This system uses **cosine similarity** via FAISS `IndexFlatIP` on L2-normalized vectors.

Cosine similarity measures the angle between vectors, ignoring their magnitude. Most text embedding models output normalized or near-normalized vectors, so cosine better captures semantic similarity focusing on meaning rather than size.

Euclidean distance focuses on raw distances, not necessarily semantic meaning. Switching from Euclidean to cosine similarity can improve relevance dramatically, without changing the model, the data, or the prompt.

In short: text embeddings from GTR-T5-Large vary in magnitude across documents. Cosine ignores this and compares direction only which is what semantic similarity requires. Euclidean would incorrectly penalize longer documents for having larger norms.

> **Note:** For normalized vectors, cosine similarity and dot product produce identical rankings and dot product is computationally faster. Our use of `IndexFlatIP` with `normalize_L2` exploits exactly this.

---

## 2. Migration to Vertex AI Vector Search (Matching Engine)

### Current vs. Production Architecture

```

# Current (demo)

Query → GTR-T5-Large (local) → FAISS IndexFlatIP (in-memory) → Top-k Results

# Production

Query → Vertex AI Embedding API → Vertex AI Vector Search → Top-k Results

```

### Three Component Swaps

**Embedder** : Replace `MockTextEmbeddingModel` with Vertex AI:

```python
from vertexai.language_models import TextEmbeddingModel
model = TextEmbeddingModel.from_pretrained("text-embedding-005")
embeddings = model.get_embeddings(texts)
```

**Vector Store** : Replace FAISS with Matching Engine index upsert + query:

```python
index.upsert_datapoints(datapoints=[...])
index_endpoint.find_neighbors(deployed_index_id="my_index",
                              queries=[query_embedding], num_neighbors=3)
```

**Generative Model** : Replace `MockGenerativeModel` hardcoded map with Gemini:

```python
from vertexai.generative_models import GenerativeModel
model = GenerativeModel("gemini-1.5-pro")
response = model.generate_content(f"Expand this search query with technical synonyms: {query}")
```

### Why Vertex AI Vector Search over FAISS in Production

FAISS requires you to build and maintain complex infrastructure, and has limited or no support for metadata filtering, high availability, and disaster recovery. Vertex AI Vector Search eliminates this it is fully managed, scales to billions of vectors, and integrates natively with Vertex AI embeddings and Gemini, keeping the entire pipeline within one ecosystem. It also natively supports dot product on normalized vectors, preserving the same cosine-equivalent metric used here.

---

## 3. Test Coverage

`test_pipeline.py` validates each layer independently embedding shape and
semantic separation, expansion correctness per query, vector store top-result
accuracy, and end-to-end Strategy A vs B divergence. These tests serve as a
regression baseline: any component swap during production migration should pass
the same suite without modification.
