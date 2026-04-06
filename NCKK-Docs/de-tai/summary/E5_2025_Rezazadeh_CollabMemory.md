# [2025] Rezazadeh — Collaborative Memory: Multi-User Memory Sharing in LLM Agents with Dynamic Access Control

## Metadata
- **arXiv:** 2505.18279v1
- **Venue:** arXiv preprint (cs.MA), under review
- **Year:** 2025
- **Authors:** Alireza Rezazadeh, Zichao Li, Ange Lou, Yuying Zhao, Wei Wei, Yujia Bao

## 1. Van de (Problem)
Complex tasks are increasingly delegated to ensembles of specialized LLM agents serving multiple users. While persistent memory enhances single-agent performance, existing approaches assume a monolithic, single-user, single-agent paradigm with globally accessible memory. This overlooks the benefits and challenges of knowledge transfer across users under dynamic, asymmetric permissions in real-world multi-user, multi-agent settings.

## 2. Dong co / Gap
Two key challenges remain unaddressed in multi-user, multi-agent memory systems: (1) **Information Asymmetry** -- different users have access to different agents, and each agent connects to different resources, requiring memory systems to enforce access constraints to prevent unauthorized information sharing; (2) **Dynamic Access Patterns** -- permissions evolve over time as roles change and policies update, requiring the memory system to adapt in real time. No existing LLM memory system (MemGPT, MemTree, GraphRAG, Memory Sharing) combines provenance-aware fragment storage with formal, time-varying access control policies.

## 3. Phuong phap (Method)
Collaborative Memory consists of three key components:

1. **Dynamic Bipartite Access Graphs:** Two time-varying bipartite graphs formalize permissions: G_UA(t) (user-to-agent) and G_AR(t) (agent-to-resource). These evolve over time to reflect user onboarding, role changes, and policy updates.

2. **Two-Tier Memory System:**
   - **Private Memory** -- fragments visible only to their originating user, storing user-specific insights
   - **Shared Memory** -- selectively shared fragments that enable cross-user knowledge transfer
   - Each fragment carries immutable provenance attributes: contributing agents, accessed resources, timestamps, and originating user

3. **Fine-grained Read/Write Policies:**
   - **Read policies** (pi^read) dynamically construct a memory view tailored to each agent's current permissions, filtering and transforming fragments according to access constraints
   - **Write policies** (pi^write/private, pi^write/shared) project interaction logs into structured memory fragments, allocating them to private or shared tiers with optional transformations (anonymization, redaction, paraphrasing)
   - Policies are configurable at system, agent, user, and per-time levels

The system uses a coordinator LLM for agent selection, domain-specialized agents with resources, and an aggregator LLM for response synthesis. All components use GPT-4o with text-embedding-3-large for embeddings.

## 4. Dong gop chinh (Contributions)
- First formulation of memory sharing that explicitly accounts for fine-grained access asymmetries in multi-agent, multi-user LLM systems
- Formalize dynamic bipartite access graphs to model time-varying user-agent-resource permissions
- Design a two-tier (private/shared) memory architecture with immutable provenance for full auditability
- Introduce configurable read/write policies at multiple granularity levels (system, agent, user, time)
- Demonstrate across three progressively complex scenarios that collaborative memory reduces resource utilization by up to 59-61% while maintaining accuracy

## 5. Diem manh (Strengths)
- Addresses a genuinely novel and practically important problem: access-controlled memory sharing in multi-user, multi-agent systems
- Formally grounded: bipartite access graphs with provable adherence to access control constraints, connecting to established ABAC/RBAC frameworks
- Three well-designed evaluation scenarios of increasing complexity (fully collaborative, asymmetric, dynamically evolving)
- Practical enterprise relevance: privacy compliance, role-based access, dynamic permission management
- Decoupled and extensible design that integrates with alternative memory structures (e.g., MemTree)

## 6. Han che (Limitations)
- Evaluated only in simulated multi-user environments; no real-world multi-user deployment data due to regulatory and privacy obstacles
- Limited scale: controlled environments with moderate numbers of users (5) and agents (4-6); large-scale enterprise settings with high concurrency are unexplored
- LLM-based policy enforcement may occasionally hallucinate or breach policies despite formal guarantees
- Resource utilization is measured via API call counts rather than actual latency, which is unpredictable in production
- No comparison with other multi-agent memory systems beyond isolated (no-sharing) baselines; lacks comparison with Memory Sharing [Gao & Zhang, 2024]

## 7. Dataset & Metric
- **Datasets:**
  - Scenario 1: MultiHop-RAG (609 news articles, 2,556 multi-hop queries across 6 domains)
  - Scenario 2: Synthetic dataset of 200 business project queries across 4 user roles
  - Scenario 3: SciQAG (scientific QA across biology, chemistry, physics; 100 queries, 5 users)
- **Metrics:** Accuracy (LLM-as-Judge normalized correctness), Agent Utilization (mean distinct agents per query), Resource Utilization (mean knowledge-base/API calls per query)

## 8. Ket qua chinh
- Scenario 1 (Fully Collaborative): Accuracy remains above 0.90 across all query indices; resource usage decreases by up to 61% at 50% overlap and 59% at 75% overlap compared to isolated memory
- Scenario 2 (Asymmetric): Even limited cross-user visibility reduces overall resource calls; intermediate insights from one user flow to others with matching privileges
- Scenario 3 (Dynamic): Accuracy rises as access is granted (t0-t4) and declines as access is revoked (t5-t8), demonstrating tight coupling between access graph and performance; access matrices confirm strict adherence to policies
- Cross-user memory fragments are increasingly reused over time, reducing the need for redundant resource queries

## 9. Keywords
Collaborative memory, multi-agent systems, multi-user memory sharing, access control, dynamic permissions, bipartite access graphs, provenance, private/shared memory, LLM agents

## 10. Lien quan den de tai
**Relevance to "Coding Agent Harness & Evaluation":** Collaborative Memory is highly relevant for coding agent harnesses in team settings where multiple developers interact with coding agents that share a codebase. The access control framework addresses real concerns: (1) different developers may have different repository permissions; (2) agents should share useful code patterns and solutions across team members while respecting access boundaries; (3) permissions evolve as team members join/leave projects. The private/shared memory tiers map to individual developer preferences (private) vs. shared team knowledge like coding conventions and resolved issues (shared). The provenance tracking ensures auditability of agent decisions, which is critical for coding agent evaluation. The resource utilization reduction (up to 61%) demonstrates that collaborative memory can significantly reduce redundant API calls in multi-user coding environments.
