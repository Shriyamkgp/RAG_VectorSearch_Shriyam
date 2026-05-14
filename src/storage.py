""" Manages vector storage and similarity search using a FAISS flat index.
- add_vectors() : Normalizes and indexes document embeddings.
- search()      : Returns top-k documents nearest to the query vector via cosine similarity (IndexFlatIP on L2-normalized vectors)."""


import faiss
import numpy as np

class VectorStore:
    def __init__(self, dimension):
        # Using IndexFlatIP with normalized vectors for Cosine Similarity 
        self.index = faiss.IndexFlatIP(dimension)
        self.documents = []

    def add_vectors(self, vectors, documents):
        vecs = np.array(vectors).astype('float32')
        faiss.normalize_L2(vecs)
        self.index.add(vecs)
        self.documents.extend(documents)

    def search(self, query_vector, k=3):
        vec = np.array([query_vector]).astype('float32')
        faiss.normalize_L2(vec)
        distances, indices = self.index.search(vec, k)
        return [self.documents[i] for i in indices[0]]