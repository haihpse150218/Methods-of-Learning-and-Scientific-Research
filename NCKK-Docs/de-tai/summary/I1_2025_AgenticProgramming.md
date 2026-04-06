# [2025] Wang — AI Agentic Programming: A Survey of Techniques, Challenges, and Opportunities

## Metadata
- **arXiv:** 2508.11126
- **Venue:** Preprint (Sep 2025)
- **Year:** 2025
- **Authors:** Huanting Wang, Jingzhi Gong, Huawei Zhang, Jie Xu, Zheng Wang

## 1. Van de (Problem)
AI agentic programming -- where LLM-based coding agents autonomously plan, execute, and interact with tools like compilers, debuggers, and version control systems -- is an emerging paradigm reshaping software development. However, the field lacks a standard taxonomy, benchmark suite, and comprehensive understanding of system architectures, behavioral characteristics, and evaluation methodologies. Existing development tools are designed for humans, not autonomous agents, creating fundamental gaps.

## 2. Dong co / Gap
Despite rapid progress, there is no systematic survey that charts the conceptual landscape of AI agentic programming, identifies common patterns and architectures, and assesses the suitability of current development ecosystems for autonomous agents. Current tools abstract away internal states, transformation traces, and execution metadata that AI agents need for principled reasoning. The field needs a comprehensive review to clarify foundational concepts, identify key challenges, and guide future research.

## 3. Phuong phap (Method)
The authors conduct a systematic literature review (SLR) following established methodology: (1) Automatic search across Google Scholar, ACM DL, IEEE Xplore, SpringerLink, arXiv yielding 7,700 papers. (2) Three-stage study selection: title/abstract screening (395 papers), full-text review (141 papers), citation chaining (152 final papers). (3) Data extraction and analysis producing a hierarchical taxonomy along two axes: **Agentic Behaviour Dimensions** (reactivity vs. proactivity, single-turn vs. multi-turn, tool-augmented vs. standalone, static vs. adaptive) and **Agent System Categories** (interactive code assistants, autonomous task-oriented agents, planning-centric agents, multi-agent collaborative systems).

## 4. Dong gop chinh (Contributions)
- Comprehensive taxonomy of AI agentic programming along behavioral dimensions and system architecture categories
- Systematic review of 152 academic papers and industry tools covering 2022-2025
- Comparative analysis of key enablers: LLMs, prompting strategies, tool integration, context management, feedback loops
- Identification of key challenges including tool ecosystem gaps, reliability, safety, and evaluation
- Mapping of future research opportunities bridging programming languages, software engineering, AI, and HCI

## 5. Diem manh (Strengths)
- Timely and comprehensive coverage of a fast-evolving field with rigorous SLR methodology
- Clear two-dimensional taxonomy (behavior + architecture) providing useful framework for classifying systems
- Practical comparative tables (Table 1: LLMs for coding, Table 4: context management mechanisms across agents)
- Historical context tracing evolution from program synthesis to code completion to agentic programming
- Bridges multiple perspectives: software engineering, AI/ML, programming languages, and HCI

## 6. Han che (Limitations)
- Survey covers only first 15 pages here; full treatment of evaluation, challenges, and opportunities likely in later sections
- Rapidly evolving field means some content may be outdated quickly
- Focus primarily on LLM-driven agents; limited coverage of hybrid symbolic-neural approaches
- Industry tools and products are described qualitatively rather than with standardized benchmarks
- Survey methodology may miss non-English publications and non-academic tools

## 7. Dataset & Metric
This is a survey paper and does not introduce new datasets or metrics. It reviews and categorizes existing benchmarking practices and evaluation strategies across the surveyed papers. Key benchmarks mentioned include HumanEval, MBPP, SWE-bench, and various tool-use benchmarks. The survey methodology itself processed 7,700 initial papers down to 152 final papers through systematic screening.

## 8. Ket qua chinh
- 152 papers included in final corpus; 53% from 2024, 22% from 2023, 20% from 2025, 5% from 2022
- Four agent system categories identified: interactive code assistants, autonomous task-oriented agents, planning-centric agents, multi-agent collaborative systems
- Key enablers: LLMs (GPT-5, Claude 4 Opus, DeepSeek, Gemini), structured prompting (CoT, ReAct, scratchpad), tool integration (compilers, debuggers, test frameworks, VCS), context management (vector DBs, sliding windows, embedding-based search), feedback loops
- Critical gap identified: current development tools designed for humans lack the hooks for iterative development, state tracking, and rich feedback propagation needed by AI agents
- Taxonomy shows progression from reactive/single-turn/static agents toward proactive/multi-turn/adaptive/tool-augmented agents

## 9. Keywords
agentic programming, AI coding agents, survey, taxonomy, LLM agents, software development, tool integration, context management, code generation, autonomous agents

## 10. Lien quan den de tai
Directly and highly relevant to the thesis on coding agent harness and evaluation. This survey provides the conceptual foundation and taxonomy for understanding the landscape of coding agents that the thesis aims to evaluate. The behavioral dimensions (reactivity vs. proactivity, tool-augmented vs. standalone) and system categories (autonomous task-oriented, multi-agent collaborative) map directly to the types of agents a harness must support. The identified gap -- that current tools lack hooks for AI agents -- motivates the design of specialized evaluation harnesses. The comparative tables of LLMs and context management strategies provide practical design considerations for building coding agent evaluation infrastructure.
