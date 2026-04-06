# [2026] Cao — Coding Agents are Effective Long-Context Processors

## Metadata
- **arXiv:** 2603.20432v1
- **Venue:** arXiv preprint (cs.CL)
- **Year:** 2026
- **Authors:** Weili Cao, Xunjian Yin, Bhuwan Dhingra, Shuyan Zhou

## 1. Van de (Problem)
LLMs have scaled to access massive context windows (millions of tokens), but they fail to effectively process long context, exhibiting significant performance degradation as context length increases. Reasoning over long contexts remains latent and uninterpretable through attention mechanisms, and RAG pipelines rely on fixed, shallow retrieval that limits iterative multi-hop reasoning. The question is whether long-context processing can be externalized from latent attention into explicit, executable interactions.

## 2. Dong co / Gap
Despite context window scaling, LLMs suffer from "context rot" -- performance degrades as input length grows, even before reaching advertised limits. Standard RAG pipelines use fixed retrieval stages that cannot support iterative, multi-hop reasoning. ReAct agents are limited to a fixed action space defined by their tool APIs. No prior work has systematically studied whether off-the-shelf coding agents, trained on code repositories, can transfer their file system navigation and programmatic processing skills to general long-context text processing tasks.

## 3. Phuong phap (Method)
The approach reformulates long-context processing as a **file system navigation and manipulation** problem:
- **Corpus formatting:** Large text corpora are organized as files within a directory hierarchy (mirroring code repository structure). Single long documents are placed as individual text files.
- **Agent interface:** Off-the-shelf coding agents (OpenAI Codex v0.46.0 with GPT-5, and Claude Code with Sonnet 4.5) receive only the file/directory path and query. They freely use native capabilities: terminal commands (grep, ripgrep, head, sed), Python scripts, intermediate file creation, and iterative refinement.
- **No task-specific training:** Agents use their existing software engineering capabilities without modification.
- **Three configurations tested:** (1) Native Codex without retriever, (2) Codex + BM25 retriever, (3) Codex + Gemini dense embeddings retriever.
- **Baselines:** GPT-5 full-context, RAG, ReAct-style search agents, Recursive Language Models (RLM).

## 4. Dong gop chinh (Contributions)
- Demonstrate that off-the-shelf coding agents outperform all baselines on 4 out of 5 long-context benchmarks, establishing new state-of-the-art by 17.3% average improvement
- Identify two key factors: **native tool proficiency** (executable code and terminal commands over passive semantic queries) and **file system familiarity** (inductive priors from training on code repositories for navigating hierarchical structures)
- Discover a counterintuitive finding: equipping coding agents with retrieval tools does not consistently improve and can even degrade performance
- Observe **emergent task-specific processing strategies**: iterative query refinement for multi-hop retrieval, programmatic aggregation for analytical tasks, and direct inference for reading comprehension -- all arising without explicit instruction
- Show that results generalize across different coding agent implementations (Codex and Claude Code)

## 5. Diem manh (Strengths)
- Simple yet powerful insight: reframing long-context QA as file system navigation leverages existing agent capabilities without any architectural changes or task-specific training
- Comprehensive evaluation across five diverse benchmarks spanning 188K to 3 trillion tokens
- Thorough ablation studies (file structure, retriever impact, command usage patterns, emergent strategies, cost analysis)
- The counterintuitive finding about retrieval tools degrading performance is well-analyzed and provides actionable guidance for agent design
- Demonstrates generalization across two distinct coding agent platforms (Codex/GPT-5 and Claude Code/Sonnet 4.5)

## 6. Han che (Limitations)
- Higher cost per query compared to lightweight methods like RAG ($0.703 for Codex on BrowseComp-Plus vs. $0.045 for RAG), though competitive with other strong methods
- Coding agents are primarily aligned and optimized for coding rather than long-context reasoning; future work could specialize them for text processing
- Naively providing retrieval tools can degrade performance; the mechanism by which retrievers suppress agents' native exploration is not fully understood
- Limited to text-based corpora; does not address multimodal long-context processing
- Evaluation uses 200 randomly sampled examples per benchmark due to computational cost

## 7. Dataset & Metric
- **BrowseComp-Plus** (750M tokens, 100K web docs): Accuracy, LLM-as-judge (GPT-5)
- **Oolong-Synthetic** (536K tokens): Score using exact match and exponential decay for numerical answers
- **Oolong-Real** (385K tokens): Same scoring as Oolong-Synthetic
- **LongBench-v2** (188K tokens): Accuracy on multiple-choice questions
- **Natural Questions (NQ)** (3T tokens, Wikipedia): Exact Match (EM) after normalization

## 8. Ket qua chinh
- **BrowseComp-Plus:** Codex (No Retriever) achieves 88.50 vs. best published 80.00 (+11%)
- **Oolong-Synthetic:** Codex achieves 71.75 vs. best published 64.38 (+11%)
- **Oolong-Real:** Claude Code + BM25 achieves 37.46 vs. best published 24.09 (+56%)
- **LongBench-v2:** Codex achieves 61.50 vs. best published 63.30 (-1%, competitive)
- **NQ:** Codex achieves 56.00 vs. best published 50.90 (+10%)
- Folder structure outperforms single file across all retriever configurations (Table 2: 89.0 vs. 83.0 without retriever)
- Agents without retrievers issue 14.92 native search commands vs. 8.33-9.84 with retrievers, showing retrieval tools suppress native exploration

## 9. Keywords
`coding-agent` `long-context` `file-system-navigation` `tool-use` `RAG` `emergent-strategies` `context-processing` `multi-hop-reasoning` `programmatic-aggregation` `benchmark`

## 10. Lien quan den de tai
Relevant to the thesis on "Coding Agent Harness & Evaluation" from two angles. First, it demonstrates that coding agents' effectiveness depends critically on their harness design -- specifically how context is presented to the agent (file system structure vs. single file) and which tools are made available (native tools vs. retrieval tools). The finding that adding retrieval tools can degrade agent performance is a cautionary lesson for harness design. Second, it provides evidence that coding agents possess transferable capabilities (tool proficiency, file system familiarity) that emerge from their software engineering training, which is foundational to understanding what makes coding agent evaluation meaningful. The emergent task-specific strategies observed also suggest that evaluation frameworks must account for diverse agent behaviors rather than assuming fixed processing pipelines.
