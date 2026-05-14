# Retrieval Benchmark: Strategy A vs Strategy B

## Overview

This benchmark compares two RAG retrieval strategies across three abstract queries
on a 10-document technical corpus:

- **Strategy A** - Raw cosine similarity on the original query embedding.
- **Strategy B** - AI-enhanced retrieval using query expansion, where the query is
  first enriched with technical synonyms before embedding.

---

## Query 1: Traffic Surge Handling

> _"How does the system cope with a sudden traffic surge?"_

| Rank | Strategy A (Raw)                    | Strategy B (Enhanced)                               |
| ---- | ----------------------------------- | --------------------------------------------------- |
| 1    | Horizontal auto-scaling (CPU > 70%) | **Redis caching layer (85% DB pressure reduction)** |
| 2    | Health-check probes                 | Horizontal auto-scaling (CPU > 70%)                 |
| 3    | Elastic Load Balancing              | Elastic Load Balancing                              |

**Observation:** Strategy A missed the Redis caching chunk entirely a critical
component of traffic surge handling. Strategy B's expansion (`high-concurrency`,
`traffic spike`, `Redis cache`) pulled it in as the top result.

<!-- Insert output screenshot here -->

---

## Query 2: Sensitive Information Protection

> _"What mechanisms are in place to protect sensitive information?"_

| Rank | Strategy A (Raw)       | Strategy B (Enhanced)      |
| ---- | ---------------------- | -------------------------- |
| 1    | AES-256-GCM encryption | **RBAC / least privilege** |
| 2    | mTLS 1.3               | AES-256-GCM encryption     |
| 3    | RBAC / least privilege | mTLS 1.3                   |

**Observation:** Both strategies retrieve the same three chunks, but Strategy B
re-ranks them surfacing RBAC (access control) first, which is arguably the
most direct answer to "protecting sensitive information" from an access perspective.

<!-- Insert output screenshot here -->

---

## Query 3: System Availability Under Failure

> _"How is the system kept running if something goes wrong?"_

| Rank | Strategy A (Raw)                        | Strategy B (Enhanced)                 |
| ---- | --------------------------------------- | ------------------------------------- |
| 1    | Health-check probes                     | Health-check probes                   |
| 2    | Active-passive failover                 | Active-passive failover               |
| 3    | **CI/CD blue-green deployment (noise)** | **Elastic Load Balancing (relevant)** |

**Observation:** Strategy A retrieved the CI/CD pipeline chunk a noise paragraph
unrelated to fault tolerance. Strategy B's expansion (`failover`, `high availability`,
`disaster recovery`) correctly displaced it with the Load Balancing chunk.

<!-- Insert output screenshot here -->

---

## Summary

| Query               | Strategy A Issue              | Strategy B Improvement             |
| ------------------- | ----------------------------- | ---------------------------------- |
| Traffic surge       | Missed Redis caching chunk    | Retrieved caching as top result    |
| Data protection     | Suboptimal ranking            | Re-ranked RBAC to top              |
| System availability | Retrieved noise (CI/CD) chunk | Replaced noise with relevant chunk |

Query expansion consistently bridges the vocabulary gap between abstract user
queries and technically worded corpus documents, improving both recall and ranking
precision across all three test cases.
