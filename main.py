""" Benchmarks two RAG retrieval strategies across a 10-document technical corpus:
- Strategy A : Raw cosine similarity on the original query.
- Strategy B : AI-enhanced retrieval using query expansion.
Three abstract queries are run through both strategies, and results are printed
side-by-side to demonstrate how expansion bridges vocabulary gaps."""


from src.orchestration import RetrievalOrchestrator
import json

def run_benchmark():
    orchestrator = RetrievalOrchestrator()
    
    # Technical paragraphs for ingestion 
    dataset = [
    # Cluster 1 — Scalability / Peak Load 
    "Horizontal auto-scaling is triggered when CPU utilization exceeds 70%, "
    "automatically provisioning additional compute nodes to distribute traffic load.",

    "Elastic Load Balancing routes incoming requests across healthy instances "
    "using a round-robin algorithm, preventing any single node from becoming a bottleneck.",

    "The caching layer employs Redis with a write-through strategy, reducing "
    "database read pressure by up to 85% during high-concurrency traffic spikes.",

    # Cluster 2 — Security / Encryption 
    "All data persisted to disk is encrypted using AES-256-GCM, with keys rotated "
    "every 90 days via an automated key-management service.",

    "Inter-service communication is secured through mutual TLS (mTLS) 1.3, "
    "ensuring both client and server identities are verified on every request.",

    "Role-based access control (RBAC) enforces the principle of least privilege, "
    "restricting API endpoint access to authenticated and authorized service accounts only.",

    # Cluster 3 — Availability / Fault Tolerance
    "Active-passive failover is configured across two geographically separated data "
    "centers, with DNS-based routing switching traffic within 30 seconds of a primary failure.",

    "Health-check probes run every 10 seconds; instances failing three consecutive "
    "checks are automatically removed from the load-balancer pool and replaced.",

    # Noise paragraphs - unrelated technical content to test retrieval precision
    "The CI/CD pipeline uses blue-green deployments to achieve zero-downtime releases, "
    "with automated rollback triggered by a spike in the 5xx error rate.",

    "Distributed tracing is implemented via OpenTelemetry, exporting spans to Jaeger "
    "for end-to-end latency analysis across microservice boundaries.",
    ]

    orchestrator.ingest(dataset)
    
    queries = [
    # Q1: Query related to sudden traffic surge 
    "How does the system cope with a sudden traffic surge?",

    # Q2: Query related to protect sensitive information
    "What mechanisms are in place to protect sensitive information?",

    # Q3: Query related to keep running if something fails
    "How is the system kept running if something goes wrong?",
    ]
    
    benchmark_results = []

    for q in queries:
        # Result A: Raw Vector Search 
        res_a = orchestrator.execute_search(q, strategy="A")
        # Result B: AI-Enhanced Retrieval 
        res_b = orchestrator.execute_search(q, strategy="B")
        
        benchmark_results.append({
            "Input Query": q,
            "Strategy A (Raw)": res_a,
            "Strategy B (Enhanced)": res_b
        })
    
    print(json.dumps(benchmark_results, indent=2))
    #Save results to a output JSON file 
    with open("output.json", "w") as f:
        json.dump(benchmark_results, f, indent=2)

if __name__ == "__main__":
    run_benchmark()