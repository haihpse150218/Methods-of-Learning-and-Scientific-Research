# [2025] Xu — A-Mem: Agentic Memory for LLM Agents

## Metadata
- **arXiv:** 2502.12110v11
- **Venue:** arXiv preprint (cs.CL)
- **Year:** 2025
- **Authors:** Wujiang Xu, Zujie Liang, Kai Mei, Hang Gao, Juntao Tan, Yongfeng Zhang

## 1. Van de (Problem)
Current memory systems for LLM agents provide basic storage and retrieval but rely on predefined memory structures, fixed operations, and rigid workflows. This inflexibility limits their adaptability across diverse tasks and prevents the memory from evolving organically as knowledge accumulates over long-term interactions.

## 2. Dong co / Gap
Existing systems (Mem0, MemGPT, MemoryBank) require developers to predefine memory storage structures, specify storage points in workflows, and establish retrieval timing. Graph databases (e.g., Mem0^g) add structure but rely on predefined schemas and relationships, fundamentally limiting adaptability. None of these systems allow memories to autonomously forge new connections or develop new organizational patterns as knowledge evolves.

## 3. Phuong phap (Method)
A-Mem is inspired by the Zettelkasten method and consists of three core mechanisms:

1. **Note Construction** -- Each interaction is stored as an atomic note with structured attributes: original content, timestamp, LLM-generated keywords, tags, contextual description, dense embedding vector, and a link set. The LLM autonomously enriches notes beyond raw content.

2. **Link Generation** -- When a new note is created, the system retrieves top-k most similar existing notes via embedding cosine similarity, then uses an LLM to determine whether meaningful connections exist based on shared attributes and contextual descriptions. Linked notes form "boxes" (analogous to Zettelkasten).

3. **Memory Evolution** -- For each linked neighbor, the LLM decides whether to update its context, keywords, and tags based on new information. This allows existing memories to continuously refine and develop higher-order patterns over time.

Retrieval uses cosine similarity over embeddings to fetch top-k relevant notes plus their linked notes as additional context.

## 4. Dong gop chinh (Contributions)
- Introduce A-Mem, an agentic memory system that autonomously organizes and evolves memories without predefined structures or operations
- Design a memory evolution mechanism where new memories trigger dynamic link generation and updates to existing memories' representations
- Demonstrate consistent superiority over baselines (LoCoMo, ReadAgent, MemoryBank, MemGPT) across six foundation models on the LoCoMo and DialSim datasets
- Show excellent scaling properties: retrieval time grows minimally from 0.31us to 3.70us when scaling from 1K to 1M memory entries
- Achieve 85-93% reduction in token usage compared to baselines like LoCoMo and MemGPT

## 5. Diem manh (Strengths)
- Evaluated across 6 foundation models (GPT-4o-mini, GPT-4o, Qwen-2.5 1.5B/3B, Llama 3.2 1B/3B) showing broad generalizability
- Thorough ablation study validates the complementary importance of both link generation and memory evolution modules
- Excellent scaling analysis up to 1M memory entries with minimal retrieval time increase
- Cost-efficient: ~1,200 tokens per memory operation vs 16,900 for baselines, ~$0.0003 per operation
- Open-source code for both benchmark evaluation and production-ready system

## 6. Han che (Limitations)
- Memory organization quality depends on the underlying LLM's capabilities; different LLMs may generate varying contextual descriptions and connections
- Only handles text-based interactions; no support for multimodal information (images, audio)
- Evaluated primarily on conversational QA benchmarks (LoCoMo, DialSim); unclear how well it generalizes to task-oriented or agentic workflows
- No comparison with Mem0 (the 2025 paper) as a baseline, only the earlier open-source mem0 library
- The paper does not evaluate latency end-to-end (only retrieval time), missing the cost of note construction and memory evolution LLM calls

## 7. Dataset & Metric
- **Datasets:** LoCoMo (7,512 QA pairs across 5 categories: single-hop, multi-hop, temporal, open-domain, adversarial; ~9K tokens per conversation, up to 35 sessions) and DialSim (multi-party dialogues from TV shows, 1,300 sessions, 350K tokens)
- **Metrics:** F1 Score, BLEU-1 (primary); ROUGE-L, ROUGE-2, METEOR, SBERT Similarity (supplementary)

## 8. Ket qua chinh
- On LoCoMo with GPT-4o-mini: A-Mem ranks #1 across all categories with average F1=27.02, BLEU-1=20.09 (vs LoCoMo baseline F1=25.02, MemGPT F1=26.65)
- Particularly strong on Multi-Hop: F1=27.02 vs LoCoMo's 25.02 and MemGPT's 26.65 (with GPT-4o-mini)
- With GPT-4o: A-Mem achieves F1=32.86 on Multi-Hop, F1=45.85 on Temporal (best across all models)
- On DialSim: A-Mem F1=3.45 vs LoCoMo 2.55, MemGPT 1.18 (35% improvement over best baseline)
- Ablation: removing both LG and ME modules drops Multi-Hop F1 from 27.02 to 9.65; link generation alone (w/o ME) achieves F1=21.35
- Scaling: retrieval time at 1M entries is 3.70us (A-Mem) vs 1.91us (MemoryBank) vs 120,069us (ReadAgent)

## 9. Keywords
Agentic memory, Zettelkasten, LLM agents, long-term memory, memory evolution, link generation, knowledge network, conversational AI

## 10. Lien quan den de tai
**Relevance to "Coding Agent Harness & Evaluation":** A-Mem's self-evolving memory architecture is highly relevant for coding agents that need to accumulate and organize knowledge across tasks -- e.g., learning code patterns, linking related debugging experiences, and evolving understanding of a codebase over time. The Zettelkasten-inspired approach of atomic notes with dynamic linking could be adapted for a coding agent harness where each code interaction becomes a self-organizing knowledge unit. The scaling analysis (up to 1M entries) demonstrates viability for long-running coding agents. The memory evolution mechanism could help agents refine their understanding of recurring code patterns and project conventions.
