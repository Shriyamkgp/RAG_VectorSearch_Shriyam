""" Unit tests for the RAG benchmark pipeline. 
Covers embedding, query expansion, vector storage, and end-to-end retrieval for both Strategy A (raw cosine similarity) and Strategy B (query expansion)."""


from src.orchestration import RetrievalOrchestrator
from src.embedding import MockTextEmbeddingModel, MockGenerativeModel
from src.storage import VectorStore

SAMPLE_CORPUS = [
    "Horizontal auto-scaling is triggered when CPU utilization exceeds 70%.",
    "All data persisted to disk is encrypted using AES-256-GCM.",
    "Active-passive failover is configured across two geographically separated data centers.",
    "Elastic Load Balancing routes incoming requests across healthy instances.",
    "Role-based access control enforces the principle of least privilege.",
]


# ── MockTextEmbeddingModel ─────────────────────────────────────────────────

# Ensures embedder returns one vector per input text with consistent dimensions
def test_embedding_shape():
    model = MockTextEmbeddingModel()
    results = model.get_embeddings(["sentence one", "sentence two"])
    assert len(results) == 2 and len(results[0]) == len(results[1])

# Ensures semantically different texts produce different vectors
def test_different_texts_give_different_embeddings():
    model = MockTextEmbeddingModel()
    e1 = model.get_embeddings(["auto-scaling"])[0]
    e2 = model.get_embeddings(["AES-256 encryption"])[0]
    assert e1 != e2


# ── MockGenerativeModel ────────────────────────────────────────────────────

# Ensures known queries are expanded with relevant technical terms
def test_expansion_returns_relevant_terms():
    model = MockGenerativeModel()
    r1 = model.generate_content("How does the system cope with a sudden traffic surge?")
    r2 = model.generate_content("What mechanisms are in place to protect sensitive information?")
    r3 = model.generate_content("How is the system kept running if something goes wrong?")
    assert "auto-scaling"  in r1.text.lower()
    assert "aes-256"       in r2.text.lower() or "encryption" in r2.text.lower()
    assert "failover"      in r3.text.lower()

# Ensures unknown queries fall back without raising errors
def test_unknown_query_returns_fallback():
    response = MockGenerativeModel().generate_content("some random unrelated query")
    assert "some random unrelated query" in response.text


# ── VectorStore ────────────────────────────────────────────────────────────

# Ensures the store returns the closest document as the top result
def test_vector_store_retrieves_correct_top_result():
    store = VectorStore(dimension=3)
    store.add_vectors([[1,0,0],[0,1,0],[0,0,1]], ["doc_a","doc_b","doc_c"])
    assert store.search([0,1,0], k=1)[0] == "doc_b"


# ── RetrievalOrchestrator ──────────────────────────────────────────────────

# Ensures Strategy A returns the correct number of string results
def test_retrieval_flow():
    orchestrator = RetrievalOrchestrator()
    orchestrator.ingest(["Sample chunk 1", "Sample chunk 2", "Sample chunk 3"])
    results = orchestrator.execute_search("Sample", strategy="A")
    assert len(results) == 3 and isinstance(results[0], str)

# Ensures Strategy B retrieves contextually relevant chunks via query expansion
def test_strategy_b_retrieves_relevant_chunks():
    orchestrator = RetrievalOrchestrator()
    orchestrator.ingest(SAMPLE_CORPUS)
    results = orchestrator.execute_search("How does the system cope with a sudden traffic surge?", strategy="B")
    combined = " ".join(results).lower()
    assert "auto-scaling" in combined or "load balancing" in combined

# Ensures Strategy B produces different results than Strategy A on abstract queries
def test_strategy_a_and_b_differ():
    orchestrator = RetrievalOrchestrator()
    orchestrator.ingest(SAMPLE_CORPUS)
    query = "How does the system cope with a sudden traffic surge?"
    assert orchestrator.execute_search(query, strategy="A") != orchestrator.execute_search(query, strategy="B")