# [2026] Borro — Memori: A Persistent Memory Layer for Efficient, Context-Aware LLM Agents

## Metadata
- **arXiv:** 2603.19935v1
- **Venue:** arXiv preprint (cs.LG)
- **Year:** 2026
- **Authors:** Luiz C. Borro, Luiz A. B. Macarini, Gordon Tindall, Michael Montero, Adam B. Struck

## 1. Van de (Problem)
Existing memory approaches for LLM agents force vendor lock-in and rely on injecting large volumes of raw conversation text into prompts, leading to high token costs, context degradation ("context rot"), and degraded performance. Memory in LLM systems is fundamentally a data structuring problem, not merely a storage problem.

## 2. Dong co / Gap
Current systems (Mem0, Zep, LangMem) either store raw text chunks and retrieve them via naive RAG (resulting in noisy, cluttered vector spaces), or use flat natural-language memory representations that lack structured relationships. None effectively transform unstructured conversational data into compact, high-signal representations that are both token-efficient and reasoning-effective. The gap between retrieval-based systems and full-context performance remains significant.

## 3. Phuong phap (Method)
Memori is an LLM-agnostic persistent memory layer with two core components:

1. **Advanced Augmentation pipeline** -- a background memory creation pipeline that distills raw dialogue into structured memory assets:
   - **Semantic Extraction & Triple Generation:** Deconstructs dialogue into atomic semantic triples (subject-predicate-object), each linked to the exact conversation of origin. Produces a low-noise, high-signal index for vector search.
   - **Conversation Summarization:** Generates concise high-level overviews of each conversation capturing overarching intent, chronological progression, and implicit context. Triples link back to these summaries for broader context.

2. **Intelligent Recall engine** -- retrieves memories using a hybrid search approach combining cosine similarity over embeddings (Gemma-300) with BM25 keyword matching, indexed via FAISS. Supports intelligent ranking and decay.

The system operates as a decoupled memory layer between application logic and the LLM, integrating via a lightweight SDK that intercepts LLM client requests.

## 4. Dong gop chinh (Contributions)
- Introduce Memori, an LLM-agnostic persistent memory layer that treats memory as a data structuring problem rather than a storage problem
- Design the Advanced Augmentation pipeline that transforms noisy conversations into dual-layered structured assets (semantic triples + conversation summaries)
- Achieve 81.95% overall accuracy on LoCoMo, outperforming all retrieval-based baselines (Zep 79.09%, LangMem 78.05%, Mem0 62.47%)
- Demonstrate extreme token efficiency: only 1,294 tokens per query (~5% of full context), 67% fewer than Zep, 20x fewer than full-context
- Provide open-source implementation (github.com/MemoriLabs/Memori)

## 5. Diem manh (Strengths)
- Very strong token efficiency (1,294 tokens, ~$0.001 per query) while achieving state-of-the-art retrieval-based accuracy
- Clean architectural design: decoupled memory layer that is LLM-agnostic and integrates via SDK wrapping
- Dual-layered representation (triples for precise facts + summaries for narrative context) elegantly addresses the granularity-context tradeoff
- Practical production orientation with cost analysis using real GPT-4.1-mini pricing
- Hybrid retrieval (cosine similarity + BM25) combines semantic and lexical matching

## 6. Han che (Limitations)
- Evaluated only on LoCoMo benchmark; no evaluation on task-oriented, agentic, or multi-domain settings
- Full-context ceiling (87.52%) still significantly outperforms Memori (81.95%), indicating ~6% accuracy gap from information loss during structuring
- Open-domain reasoning is the weakest category (63.54%), as granular triples struggle with broad synthesis queries
- No latency analysis reported; the paper focuses only on token cost
- Limited baselines: only compares against Mem0, Zep, LangMem, and full-context; misses A-Mem, MemGPT, and other recent systems
- Short paper (6 pages + appendices) with limited technical depth on the extraction pipeline internals

## 7. Dataset & Metric
- **Dataset:** LoCoMo -- 10 extended conversations with QA pairs across 4 categories (single-hop: 830, multi-hop: 282, temporal: 321, open-domain: 96; adversarial excluded)
- **Metrics:** LLM-as-a-Judge accuracy (%) using GPT-4.1-mini (CORRECT/WRONG binary), Token Usage (added tokens to context), Context Cost ($), Context Footprint (%)

## 8. Ket qua chinh
- Overall accuracy: Memori 81.95% vs Zep 79.09%, LangMem 78.05%, Mem0 62.47%, Full-Context 87.52%
- Single-Hop: 87.87% (best among retrieval systems, close to full-context 88.53%)
- Multi-Hop: 72.70% (outperforms Zep 69.16%, trails full-context 77.70%)
- Temporal: 80.37% (outperforms Mem0 66.47%, trails LangMem 86.92%)
- Open-Domain: 63.54% (weakest category)
- Token usage: 1,294 tokens per query (4.97% of full context) vs Mem0 1,764 (6.78%), Zep 3,911 (15.02%), Full-Context 26,031 (100%)
- Cost per query: $0.001035 vs Zep $0.003129, Full-Context $0.020825

## 9. Keywords
Persistent memory layer, semantic triples, conversation summarization, LLM memory, context efficiency, data structuring, knowledge graph, retrieval-augmented generation

## 10. Lien quan den de tai
**Relevance to "Coding Agent Harness & Evaluation":** Memori's approach of structuring unstructured data into semantic triples is directly applicable to coding agent harnesses -- e.g., structuring code interactions into (entity, relationship, entity) triples like (function_X, calls, function_Y) or (user, prefers, coding_style_Z). The extreme token efficiency (5% of full context) is critical for production coding agents where API costs scale with conversation length. The LLM-agnostic, SDK-based architecture provides a reusable pattern for adding persistent memory to any coding agent framework. The dual representation (triples for facts + summaries for context) maps well to coding scenarios where agents need both precise code facts and broader project context.
