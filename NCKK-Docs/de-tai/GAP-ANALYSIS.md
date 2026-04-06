# GAP-ANALYSIS: Coding Agent Harness & Evaluation

> Synthesized from 49 research papers (2023--2026) covering coding agents, multi-agent systems, tool learning, memory, planning, security, and evaluation benchmarks.

---

## 1. Keyword Frequency Analysis

### Top 20 Keywords (by approximate occurrence across 49 papers)

| Rank | Keyword | Count | Theme |
|------|---------|-------|-------|
| 1 | multi-agent systems / orchestration | 22 | Architecture |
| 2 | LLM agent | 21 | Core Concept |
| 3 | coding agent / code generation | 19 | Core Concept |
| 4 | benchmark / evaluation | 18 | Evaluation |
| 5 | tool use / tool learning / function calling | 14 | Tool System |
| 6 | security / prompt injection / safety | 12 | Security |
| 7 | memory (long-term, short-term, persistent) | 11 | Memory |
| 8 | planning / reasoning / CoT | 11 | Planning |
| 9 | SWE-bench / SWE-agent | 9 | Benchmark |
| 10 | harness / scaffold | 8 | Architecture |
| 11 | context management / compaction | 8 | Context |
| 12 | self-improvement / self-reflection | 7 | Self-Improvement |
| 13 | ReAct / tree search | 7 | Planning |
| 14 | survey / taxonomy | 7 | Meta |
| 15 | multi-language / cross-language | 5 | Multi-Language |
| 16 | open-source | 5 | Implementation |
| 17 | software development lifecycle (SDLC) | 5 | Production |
| 18 | contamination / data leakage | 4 | Evaluation |
| 19 | MCP (Model Context Protocol) | 4 | Tool System |
| 20 | Infrastructure-as-Code / domain-specific | 3 | Production |

### Keyword Clusters by Theme

**Theme A -- Agent Architecture & Harness Design:**
multi-agent systems, coding agent, harness, scaffold, compound AI system, orchestration, ReAct, dual-agent, assembly-line workflow, blackboard architecture, self-organizing teams

**Theme B -- Tool & API Integration:**
tool use, tool learning, function calling, API calls, MCP, tool documentation, tool selection, tool retrieval, DFSDT, hierarchical agents

**Theme C -- Context & Memory Management:**
context management, context compaction, long-term memory, short-term memory, persistent memory, Zettelkasten, knowledge graph, semantic triples, cross-session, selective forgetting, collaborative memory

**Theme D -- Planning & Reasoning:**
planning, CoT, tree search, task decomposition, reflection, PDDL, multi-plan selection, best-first search, CoT-decoding, external planner

**Theme E -- Evaluation & Benchmarking:**
benchmark, SWE-bench, evaluation, pass rate, progress rate, Fix Rate, agent-as-judge, PRDJudge, contamination, failure analysis, multi-dimensional assessment

**Theme F -- Security & Safety:**
prompt injection, security, defense-in-depth, sandboxing, MITRE ATT&CK, dual LLM pattern, access control, trust boundaries, coding rules exploitation

**Theme G -- Self-Improvement & Adaptation:**
self-improving agent, meta-improvement loop, lesson learning, knowledge distillation, retriever-aware training, cross-language transfer

---

## 2. Research Landscape Table

Legend: Y = covered as primary contribution, P = partially addressed, (blank) = not covered

| ID | Paper (Short Name) | Harness/Scaffold | Tool System | Context/Memory | Planning/Reasoning | Multi-Agent | Security/Safety | Eval Framework | Benchmark Design | Self-Improvement | Long-Horizon | Multi-Language | Production Focus | Open-Source |
|----|-------------------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| A1 | Bui 2026 (OpenDev) | **Y** | **Y** | **Y** | **Y** | P | **Y** | P | | | **Y** | | P | **Y** |
| A2 | Lou 2026 (AutoHarness) | **Y** | P | | P | | P | **Y** | **Y** | | | | | |
| A3 | Cao 2026 (LongContext) | P | **Y** | P | P | | | **Y** | P | | **Y** | | | |
| B1 | Lyu 2026 (TheBotCompany) | **Y** | P | **Y** | **Y** | **Y** | | P | **Y** | | **Y** | P | | **Y** |
| B2 | Loose 2026 (FuzzHarness) | **Y** | **Y** | P | P | **Y** | | **Y** | | | | | | |
| B3 | Chen 2026 (ToolToTeammate) | | P | | | P | | **Y** | | | | | | |
| B4 | Tawosi 2025 (ALMAS) | P | P | P | P | **Y** | | | | | | | **Y** | |
| B5 | Xiong 2025 (KGACG) | P | | P | **Y** | **Y** | | | | | | | | |
| B6 | Raghavan 2025 (MOSAIC) | P | | **Y** | **Y** | **Y** | | P | P | | | | | |
| B7 | Liu 2025 (LessonL) | | | | P | **Y** | | P | | **Y** | | | | **Y** |
| B8 | Moumoula 2025 (XL-CoGen) | | | | P | **Y** | | P | | | | **Y** | | |
| B9 | Khan 2025 (MACOG) | **Y** | **Y** | P | P | **Y** | **Y** | **Y** | **Y** | | | | P | |
| B10 | Robeyns 2025 (SICA) | **Y** | **Y** | | P | P | P | **Y** | P | **Y** | | | | **Y** |
| C1 | Deng 2025 (SWE-Bench Pro) | | | | | | | **Y** | **Y** | | P | P | **Y** | P |
| C2 | Pham 2025 (SWE-EVO) | | | | | | | **Y** | **Y** | | **Y** | | | **Y** |
| C3 | Prathifkumar 2025 (SWEMemory) | | | | | | | **Y** | P | | | | | |
| C4 | Fu 2026 (AutoBenchmark/PRDBench) | | | | | | | **Y** | **Y** | | | | | P |
| C5 | Xu 2025 (SWE-Compass) | | | | | | | **Y** | **Y** | | | **Y** | | **Y** |
| D1 | Chhabra 2025 (AgenticSecurity) | | P | | | P | **Y** | P | P | | | | | |
| D2 | Beurer-Kellner 2025 (SecurePatterns) | P | | | | | **Y** | | | | | | | |
| D3 | Liu 2025 (AIShellJack) | | | | | | **Y** | **Y** | **Y** | | | | | |
| D4 | Maloyan 2026 (PromptInjection SoK) | P | P | | | P | **Y** | P | P | | | | | |
| D5 | Hossain 2025 (DefensePipeline) | | | | | **Y** | **Y** | P | | | | | | |
| E1 | Chhikara 2025 (Mem0) | | | **Y** | | | | P | | | P | | | **Y** |
| E2 | Xu 2025 (A-Mem) | | | **Y** | | | | P | | | P | | | **Y** |
| E3 | Yu 2026 (AgeMem) | | | **Y** | P | | | P | | P | **Y** | | | |
| E4 | Borro 2026 (Memori) | | | **Y** | | | | P | | | | | P | **Y** |
| E5 | Rezazadeh 2025 (CollabMemory) | | | **Y** | | **Y** | P | P | | | | | P | |
| F1 | Patil 2023 (Gorilla) | | **Y** | | | | | **Y** | **Y** | | | | | **Y** |
| F2 | Qin 2023 (ToolLLM) | | **Y** | | **Y** | | | **Y** | **Y** | | | | | **Y** |
| F3 | Du 2024 (AnyTool) | | **Y** | | **Y** | P | | **Y** | P | | | | | |
| F4 | Qu 2024 (ToolLearningSurvey) | | **Y** | | **Y** | | P | P | P | | | | | |
| F5 | Yuan 2024 (EasyTool) | | **Y** | | | | | P | | | | | | |
| G1 | Huang 2024 (PlanningSurvey) | | | P | **Y** | | | P | P | | | | | |
| G2 | Liu 2024 (LLM+P) | | | | **Y** | | | P | P | | | | | **Y** |
| G3 | Ma 2024 (AgentBoard) | | P | P | **Y** | | | **Y** | **Y** | | P | | | **Y** |
| G4 | Koh 2024 (TreeSearch) | | | | **Y** | | | P | | | | | | |
| G5 | Wang 2024 (CoT-Decoding) | | | | **Y** | | | | | | | | | |
| H1 | Wu 2023 (AutoGen) | P | **Y** | | P | **Y** | P | | | | | | | **Y** |
| H2 | Chen 2023 (AgentVerse) | | P | | P | **Y** | | P | | | | | | **Y** |
| H3 | Hong 2023 (MetaGPT) | **Y** | P | | P | **Y** | | P | P | | | | | **Y** |
| H4 | Shen 2024 (alpha-UMi) | | **Y** | | **Y** | **Y** | | P | | | | | | |
| H5 | Li 2023 (CAMEL) | | | | P | **Y** | | P | | | | | | **Y** |
| I1 | Wang 2025 (AgenticProgramming) | P | P | P | P | P | P | P | P | | | | | |
| I2 | Wang 2025 (VisualAnalytics) | | | P | | | | **Y** | | | | | | |
| S1 | Wang 2023 (AutonomousAgents) | P | P | **Y** | **Y** | P | | P | | | | | | |
| S2 | Han 2024 (MASChallenges) | | | | | **Y** | P | | | | | | | |
| S3 | Liu 2025 (MemorySurvey) | | | **Y** | | | | P | P | | | | | |
| S5 | 2025 (EvalSurvey) | | | | | | | **Y** | **Y** | | | | | |

### Coverage Summary (Y or P counts out of 49 papers)

| Feature | Full (Y) | Partial (P) | Total Coverage | Not Covered |
|---------|----------|-------------|----------------|-------------|
| Harness/Scaffold Design | 9 | 6 | 15 (31%) | 34 (69%) |
| Tool System | 12 | 12 | 24 (49%) | 25 (51%) |
| Context/Memory Mgmt | 8 | 10 | 18 (37%) | 31 (63%) |
| Planning/Reasoning | 11 | 14 | 25 (51%) | 24 (49%) |
| Multi-Agent Orchestration | 14 | 7 | 21 (43%) | 28 (57%) |
| Security/Safety | 7 | 7 | 14 (29%) | 35 (71%) |
| Evaluation Framework | 15 | 17 | 32 (65%) | 17 (35%) |
| Benchmark Design | 11 | 10 | 21 (43%) | 28 (57%) |
| Self-Improvement | 2 | 1 | 3 (6%) | 46 (94%) |
| Long-Horizon Tasks | 5 | 4 | 9 (18%) | 40 (82%) |
| Multi-Language Support | 2 | 2 | 4 (8%) | 45 (92%) |
| Production/Industrial | 2 | 4 | 6 (12%) | 43 (88%) |
| Open-Source Implementation | 17 | 1 | 18 (37%) | 31 (63%) |

---

## 3. Gap Identification

### Gap 1: Harness-Level Evaluation Framework for Coding Agents
**What is the gap?** While 15 papers touch on harness/scaffold design and 32 address evaluation, **no paper provides a systematic framework for evaluating the harness itself** (as opposed to the agent's task performance). Existing benchmarks (SWE-bench, SWE-Compass, PRDBench) evaluate the *agent's coding output*. There is no benchmark that evaluates *harness properties*: how well the harness manages context, dispatches tools, enforces safety, handles long sessions, and supports multiple LLM backends.

**Closest papers:** A1 (OpenDev) describes harness design decisions but lacks benchmark evaluation; B10 (SICA) self-improves the harness but does not systematically evaluate harness components; S5 (EvalSurvey) reviews evaluation methods but not harness-level evaluation.

**Why unaddressed?** The harness concept is relatively new (explicitly coined by A1 in 2026). Most researchers frame the problem as "evaluate the agent" rather than "evaluate the infrastructure that enables the agent." The harness is often treated as a fixed engineering artifact rather than a variable worthy of study.

### Gap 2: Security-Aware Evaluation Benchmarks for Coding Agents
**What is the gap?** Security papers (D1--D5) catalog threats and propose defenses, while evaluation papers (C1--C5, S5) design benchmarks for correctness. **No paper combines both:** a benchmark that evaluates coding agents on both task correctness AND security resistance simultaneously. D3 (AIShellJack) evaluates security only; C1 (SWE-Bench Pro) evaluates correctness only. A coding agent could achieve high resolve rates while being vulnerable to prompt injection through coding rules, MCP servers, or third-party documentation.

**Closest papers:** D3 (AIShellJack) benchmarks security but not coding performance; D2 (SecurePatterns) proposes design patterns but no quantitative evaluation; C5 (SWE-Compass) has multi-dimensional evaluation but no security dimension.

**Why unaddressed?** The security and evaluation communities have developed largely in parallel. Security researchers focus on attack/defense without measuring impact on functional performance; benchmark designers focus on correctness without testing adversarial robustness.

### Gap 3: Memory-Augmented Coding Agent Evaluation
**What is the gap?** Memory papers (E1--E5, E3) advance memory architectures for general conversational agents, but **none evaluate memory systems in coding-specific scenarios** (e.g., remembering codebase structure across sessions, recalling past debugging patterns, retaining user coding preferences). All memory evaluations use conversational QA benchmarks (LoCoMo, DialSim). No benchmark tests whether memory helps a coding agent solve related tasks faster, avoid repeated bugs, or maintain project context.

**Closest papers:** E3 (AgeMem) evaluates on diverse tasks but not coding; A1 (OpenDev) describes ACE memory pipeline but does not benchmark it; I2 (VisualAnalytics) identifies "repeated bug" as a symptom of missing memory but does not propose a solution.

**Why unaddressed?** Memory research has been driven by conversational AI use cases (chatbots, customer service). Coding-specific memory needs (AST-level knowledge, dependency relationships, test result history) require domain-specific structuring that generic memory systems do not address.

### Gap 4: Multi-Language, Long-Horizon Coding Agent Benchmarks
**What is the gap?** Only 4/49 papers address multi-language support. C5 (SWE-Compass) covers 10 languages but has very few samples per language-task cell. C2 (SWE-EVO) addresses long-horizon evolution but only in Python. B8 (XL-CoGen) addresses cross-language but only at function level (MBPP). **No benchmark combines multi-language support with long-horizon, repository-level tasks.** Real-world codebases often span multiple languages (Python backend + TypeScript frontend + Go infrastructure).

**Closest papers:** C5 (SWE-Compass) -- multi-language but not long-horizon; C2 (SWE-EVO) -- long-horizon but Python-only; C1 (SWE-Bench Pro) -- multi-language (Python, JS, Go) but single-issue tasks.

**Why unaddressed?** Building Docker-based reproducible environments for multi-language, multi-file tasks is extremely difficult (C5 reports only 2--8% environment build success rate). Long-horizon task definition requires substantial manual effort to identify version transitions and create verifiable test suites.

### Gap 5: Self-Improving Harness Design
**What is the gap?** Only B10 (SICA) and B7 (LessonL) address self-improvement, and only SICA applies it to the harness itself. **No paper explores systematic methods for a coding agent harness to learn from past evaluations and automatically improve its tool configurations, context management strategies, or safety policies.** The harness is always manually designed and remains static across evaluations.

**Closest papers:** B10 (SICA) -- self-modifies agent code but focuses on tool improvements, not harness-level architectural choices; B7 (LessonL) -- inter-agent lesson sharing but applied to code optimization, not harness design.

**Why unaddressed?** Self-improvement of infrastructure (as opposed to task performance) requires meta-level reasoning about system architecture. It also requires a clear objective function for harness quality, which does not yet exist (see Gap 1).

### Gap 6: Unified Harness Combining Tool, Memory, Security, and Context Management
**What is the gap?** Each component has been studied independently: tools (F1--F5), memory (E1--E5), security (D1--D5), context management (A1, A3). **No paper presents a unified harness architecture that integrates all four with systematic ablation showing each component's contribution.** Papers either focus on one component deeply or propose vision papers (B4/ALMAS, B5/KGACG) without empirical validation.

**Closest papers:** A1 (OpenDev) comes closest with 4-layer architecture but lacks benchmark evaluation; B9 (MACOG) integrates multiple components but for IaC only; B1 (TheBotCompany) integrates orchestration + verification but not security or memory.

**Why unaddressed?** Building a complete harness requires significant engineering effort across multiple domains. Research incentives favor novel contributions in single areas over integration work.

---

## 4. Gap Ranking

| Rank | Gap | Feasibility (1--5) | Novelty (1--5) | Value (1--5) | Total (weighted) | Notes |
|------|-----|:---:|:---:|:---:|:---:|-------|
| **1** | **Harness-Level Evaluation Framework** | 4 | 5 | 5 | **14** | High feasibility: can build on SWE-bench infrastructure. Very novel: no existing work. High value: addresses a foundational need. |
| **2** | **Security-Aware Coding Benchmarks** | 4 | 4 | 5 | **13** | Combine AIShellJack-style attacks with SWE-bench-style tasks. Practical and timely. |
| **3** | **Memory-Augmented Coding Agent Eval** | 3 | 4 | 4 | **11** | Requires designing coding-specific memory benchmarks. Moderate engineering effort. High novelty in coding domain. |
| **4** | **Multi-Language Long-Horizon Benchmarks** | 2 | 4 | 4 | **10** | Docker environment building is extremely hard (2--8% success rate). May be too labor-intensive for a master's thesis. |
| **5** | **Self-Improving Harness** | 2 | 5 | 4 | **11** | Very novel but requires substantial engineering. SICA spent $7,000 on 15 iterations. Feasibility risk for a master's student. |

### Scoring Criteria
- **Feasibility:** 5 = easily achievable in 6 months with Python; 1 = requires infrastructure beyond a master's scope
- **Novelty:** 5 = no existing paper addresses it; 1 = well-explored area
- **Value:** 5 = both scientifically significant and practically useful; 1 = incremental contribution

---

## 5. Proposed Thesis Topics

### Topic 1: A Harness-Level Evaluation Framework for Coding Agents (Rank #1)

**Thesis Title:**
- **Vietnamese:** Khung danh gia cap do Harness cho cac Coding Agent dua tren Mo hinh Ngon ngu Lon
- **English:** HarnessEval: A Multi-Dimensional Evaluation Framework for Coding Agent Harness Infrastructure

**Research Questions:**
1. What measurable properties define harness quality independently of the underlying LLM's capability?
2. How do different harness configurations (tool selection, context management strategy, safety layers) affect agent performance on standardized coding benchmarks?
3. Can a lightweight ablation protocol isolate the contribution of each harness component (tools, memory, safety, context compaction) to overall agent performance?

**Proposed Method:**
- Design a harness evaluation taxonomy with 5 dimensions: **Tool Dispatch Efficiency** (correct tool selection rate, latency), **Context Utilization** (token waste ratio, information retention after compaction), **Safety Enforcement** (attack success rate under prompt injection, destructive operation prevention rate), **Session Continuity** (performance degradation over conversation length), and **Backend Portability** (performance variance across LLM backends).
- Implement a reference harness in Python with modular, swappable components for each dimension.
- Evaluate on SWE-bench Verified subset (200 tasks) with 3 LLM backends (GPT-4o, Claude Sonnet, DeepSeek-V3) under systematic ablation of harness components.
- Compare at least 3 open-source harnesses (SWE-Agent, OpenHands, OpenDev) using the proposed evaluation dimensions.

**Expected Contributions:**
- First formal taxonomy of harness quality dimensions for coding agents
- Open-source modular evaluation toolkit (Python)
- Empirical evidence quantifying the contribution of each harness component
- Guidelines for harness design based on task complexity and LLM capability

**Required Resources:**
- API access to 3 LLM providers (estimated $500--$1,000 for 200 tasks x 3 backends x ablation conditions)
- Docker environment for SWE-bench evaluation
- 6 months development + evaluation time
- Python, Docker, basic familiarity with SWE-Agent codebase

---

### Topic 2: Security-Integrated Coding Agent Evaluation (Rank #2)

**Thesis Title:**
- **Vietnamese:** Danh gia tich hop bao mat cho Coding Agent: Ket hop do chinh xac va do khang tan cong
- **English:** SecureCodeBench: A Dual-Axis Benchmark for Evaluating Coding Agents on Both Correctness and Security Resistance

**Research Questions:**
1. To what extent does optimizing for task correctness compromise security resistance (and vice versa) in coding agents?
2. Which harness design patterns (from D2/SecurePatterns) most effectively maintain coding performance while resisting prompt injection attacks through coding rules and tool descriptions?
3. Can a unified scoring function balance correctness and security to rank coding agents more holistically?

**Proposed Method:**
- Construct SecureCodeBench by extending a subset of SWE-bench Verified (100 tasks) with adversarial variants: (a) poisoned coding rule files (.cursorrules-style), (b) malicious MCP tool descriptions, (c) adversarial documentation in repository files.
- For each task, measure both **Resolve Rate** (standard SWE-bench metric) and **Security Score** (inspired by AIShellJack: percentage of adversarial payloads resisted).
- Map 20 MITRE ATT&CK techniques relevant to coding contexts (from D3) to create attack payloads.
- Evaluate 3--5 coding agents (SWE-Agent, OpenHands, Claude Code, Cursor) on the dual-axis benchmark.
- Propose a **Secure Resolve Rate** = Resolve Rate * (1 - Attack Success Rate) as a composite metric.

**Expected Contributions:**
- First benchmark combining coding correctness and security evaluation
- Taxonomy of security-relevant attack vectors specific to coding agents
- Empirical trade-off analysis between correctness and security across harness designs
- Composite metric for holistic coding agent ranking

**Required Resources:**
- API access for 3--5 coding agents ($500--$800)
- Docker environment for SWE-bench evaluation
- Manual construction of 100 adversarial task variants (estimated 2--3 weeks)
- Python, familiarity with MITRE ATT&CK framework

---

### Topic 3: Memory-Augmented Harness for Coding Agents (Rank #3)

**Thesis Title:**
- **Vietnamese:** Harness tich hop bo nho cho Coding Agent: Danh gia tac dong cua bo nho dai han len hieu suat giai quyet loi
- **English:** CodeMemory: Evaluating the Impact of Persistent Memory on Coding Agent Performance Across Related Tasks

**Research Questions:**
1. Does persistent memory (storing past debugging experiences, code patterns, and resolution strategies) improve coding agent performance on subsequent related tasks?
2. What memory representation (flat text, semantic triples, knowledge graph) is most effective for coding-specific knowledge?
3. How does memory quality degrade over time, and what forgetting policies best preserve useful coding knowledge?

**Proposed Method:**
- Design a **sequential coding task benchmark** where tasks are drawn from the same repository and share dependencies (e.g., 5 related issues from django or scikit-learn, ordered chronologically).
- Implement 3 memory backends integrated into a coding agent harness: (a) Mem0-style flat extraction, (b) Memori-style semantic triples, (c) A-Mem-style Zettelkasten with dynamic linking.
- Measure per-task resolve rate with and without memory across task sequences of length 3, 5, and 10.
- Analyze what the agent memorizes (code patterns, file locations, API usage, test strategies) and what helps vs. hurts.
- Evaluate memory overhead (latency, token cost, storage) following Mem0's evaluation methodology.

**Expected Contributions:**
- First evaluation of persistent memory impact on coding agent performance
- Comparison of 3 memory architectures in coding-specific settings
- Sequential coding benchmark design (reusable for future research)
- Practical guidelines for memory configuration in coding agent harnesses

**Required Resources:**
- API access for 1--2 LLM backends ($300--$500)
- Docker environment for SWE-bench-style evaluation
- Implementation of 3 memory backends in Python (can leverage open-source Mem0 and A-Mem code)
- 6 months: 2 months benchmark construction, 2 months implementation, 2 months evaluation

---

## Appendix A: Paper Index by Category

### A -- Harness/Scaffold Architecture
- A1: Bui 2026 (OpenDev) -- Terminal-native agent with 4-layer architecture
- A2: Lou 2026 (AutoHarness) -- Auto-synthesized code harness for action validity
- A3: Cao 2026 (LongContext) -- Coding agents as long-context processors

### B -- Multi-Agent Code Generation & Orchestration
- B1: Lyu 2026 (TheBotCompany) -- Persistent multi-day development
- B2: Loose 2026 (FuzzHarness) -- Multi-agent fuzz harness generation
- B3: Chen 2026 (ToolToTeammate) -- Agents as research teammates
- B4: Tawosi 2025 (ALMAS) -- Agile SDLC framework (vision paper)
- B5: Xiong 2025 (KGACG) -- Knowledge-guided code generation (vision paper)
- B6: Raghavan 2025 (MOSAIC) -- Scientific coding with student-teacher model
- B7: Liu 2025 (LessonL) -- Lesson-based inter-agent learning
- B8: Moumoula 2025 (XL-CoGen) -- Cross-language code generation
- B9: Khan 2025 (MACOG) -- Infrastructure-as-Code generation
- B10: Robeyns 2025 (SICA) -- Self-improving coding agent

### C -- Benchmarks & Evaluation
- C1: Deng 2025 (SWE-Bench Pro) -- Contamination-resistant enterprise benchmark
- C2: Pham 2025 (SWE-EVO) -- Long-horizon software evolution
- C3: Prathifkumar 2025 (SWEMemory) -- Benchmark contamination evidence
- C4: Fu 2026 (PRDBench) -- Agent-driven benchmark construction + PRDJudge
- C5: Xu 2025 (SWE-Compass) -- Multi-language, multi-task benchmark

### D -- Security & Safety
- D1: Chhabra 2025 (AgenticSecurity) -- Security threat taxonomy survey
- D2: Beurer-Kellner 2025 (SecurePatterns) -- 6 design patterns for prompt injection defense
- D3: Liu 2025 (AIShellJack) -- Attack framework for coding editors
- D4: Maloyan 2026 (PromptInjection SoK) -- Systematization of knowledge on coding assistant attacks
- D5: Hossain 2025 (DefensePipeline) -- Multi-agent defense architecture

### E -- Memory Systems
- E1: Chhikara 2025 (Mem0) -- Production-ready persistent memory
- E2: Xu 2025 (A-Mem) -- Zettelkasten-inspired agentic memory
- E3: Yu 2026 (AgeMem) -- Unified LTM+STM with RL training
- E4: Borro 2026 (Memori) -- Semantic triples for persistent memory
- E5: Rezazadeh 2025 (CollabMemory) -- Multi-user access-controlled memory

### F -- Tool Learning & API Integration
- F1: Patil 2023 (Gorilla) -- Fine-tuned LLM for API calls
- F2: Qin 2023 (ToolLLM) -- 16,000+ APIs with DFSDT reasoning
- F3: Du 2024 (AnyTool) -- Hierarchical self-reflective API retrieval
- F4: Qu 2024 (ToolLearningSurvey) -- Comprehensive tool learning survey
- F5: Yuan 2024 (EasyTool) -- Concise tool documentation

### G -- Planning & Reasoning
- G1: Huang 2024 (PlanningSurvey) -- 5-category planning taxonomy
- G2: Liu 2024 (LLM+P) -- Classical planner integration
- G3: Ma 2024 (AgentBoard) -- Multi-turn evaluation with progress rate
- G4: Koh 2024 (TreeSearch) -- Inference-time tree search for web agents
- G5: Wang 2024 (CoT-Decoding) -- Reasoning without prompting

### H -- Multi-Agent Frameworks
- H1: Wu 2023 (AutoGen) -- Conversable agents + conversation programming
- H2: Chen 2023 (AgentVerse) -- Dynamic expert recruitment
- H3: Hong 2023 (MetaGPT) -- SOP-based assembly-line workflow
- H4: Shen 2024 (alpha-UMi) -- Planner-Caller-Summarizer decomposition
- H5: Li 2023 (CAMEL) -- Role-playing cooperative agents

### I -- Industry & Practice
- I1: Wang 2025 (AgenticProgramming) -- SLR survey of agentic programming
- I2: Wang 2025 (VisualAnalytics) -- Visual analytics for coding agents

### S -- Foundational Surveys
- S1: Wang 2023 (AutonomousAgents) -- Profile-Memory-Planning-Action framework
- S2: Han 2024 (MASChallenges) -- Multi-agent system challenges
- S3: Liu 2025 (MemorySurvey) -- 3-generation memory taxonomy
- S5: 2025 (EvalSurvey) -- Evaluation methods survey (benchmark validity issues)

---

## Appendix B: Key Statistics

- **Papers by year:** 2023: 5, 2024: 10, 2025: 22, 2026: 12
- **Papers with empirical evaluation:** 35/49 (71%)
- **Papers that are surveys/SoK:** 8/49 (16%)
- **Papers with open-source code:** 18/49 (37%)
- **Papers evaluating on SWE-bench variants:** 8/49 (16%)
- **Papers addressing coding agents specifically:** 28/49 (57%)
- **Papers addressing security of coding agents:** 7/49 (14%)
- **Most underrepresented areas:** Self-Improvement (6%), Multi-Language (8%), Production Focus (12%), Long-Horizon (18%)
