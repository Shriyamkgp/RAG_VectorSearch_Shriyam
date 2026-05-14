""" Orchestrates the RAG pipeline by coordinating embedding, storage, and retrieval.
- ingest()         : Embeds and indexes paragraphs into the vector store.
- execute_search() : Runs Strategy A (raw query) or Strategy B (AI-expanded query) and returns the top-3 matching chunks."""


from src.embedding import MockTextEmbeddingModel, MockGenerativeModel
from src.storage import VectorStore

class RetrievalOrchestrator:
    def __init__(self):
        self.embedder = MockTextEmbeddingModel()
        self.generator = MockGenerativeModel()
        self.store = None

    def ingest(self, paragraphs):
        embeddings = self.embedder.get_embeddings(paragraphs)
        self.store = VectorStore(dimension=len(embeddings[0]))
        self.store.add_vectors(embeddings, paragraphs)

    def execute_search(self, query, strategy="A"):
        search_query = query
        
        if strategy == "B":
            # Strategy B: AI-Enhanced Retrieval (Query Expansion) 
            response = self.generator.generate_content(query)
            search_query = response.text
            
        query_vec = self.embedder.get_embeddings([search_query])[0]
        return self.store.search(query_vec, k=3) # Top 3 chunks 