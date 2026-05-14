""" Provides mock implementations of the embedding and generative models.
- MockTextEmbeddingModel : Encodes texts into dense vectors using GTR-T5-Large.
- MockGenerativeModel    : Simulates query expansion by mapping each query to a predefined set of technical synonyms and related terms."""


from sentence_transformers import SentenceTransformer

class MockTextEmbeddingModel:
    def __init__(self):
        self.client = SentenceTransformer('sentence-transformers/gtr-t5-large')  # Vertex AI proxy

    def get_embeddings(self, texts):
        return self.client.encode(texts).tolist()

class MockGenerativeModel:
    def generate_content(self, prompt):
        # Query → technical synonyms map
        expansions = {
        "How does the system cope with a sudden traffic surge?": (
            "sudden traffic surge, peak load handling, horizontal auto-scaling, "
            "elastic load balancing, caching strategy, high-concurrency, "
            "traffic spike mitigation, compute node provisioning, Redis cache"
        ),

        "What mechanisms are in place to protect sensitive information?": (
            "protect sensitive information, data security, encryption at rest AES-256, "
            "TLS mTLS in transit, role-based access control RBAC, "
            "key management, least privilege, authentication authorization"
        ),

        "How is the system kept running if something goes wrong?": (
            "system availability, fault tolerance, failover strategy, "
            "active-passive failover, health check probes, "
            "high availability, disaster recovery, load balancer pool, "
            "automatic instance replacement, uptime"
        ),
        }

        # Returns mocked expansion 
        expanded_text = expansions.get(
            prompt, f"{prompt} related technical implementation details"
        )
        
        class MockResponse:
            def __init__(self, text): self.text = text
        return MockResponse(expanded_text)