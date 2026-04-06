# [2025] Tawosi — ALMAS: an Autonomous LLM-based Multi-Agent Software Engineering Framework

## Metadata
- **arXiv:** 2510.03463v2
- **Venue:** 2025 IEEE/ACM International Conference on Automated Software Engineering Workshops (ASEW)
- **Year:** 2025
- **Authors:** Vali Tawosi, Keshav Ramani, Salwa Alamir, Xiaomo Liu (J.P. Morgan AI Research)

## 1. Van de (Problem)
AI-assisted coding tools typically operate as isolated components (code completion, bug detection, test generation) rather than as an integrated ecosystem spanning the entire software development lifecycle (SDLC). This fragmentation limits overall effectiveness and introduces friction in developer workflows. A successful LLM system must factor in multiple stages of the SDLC beyond just code generation.

## 2. Dong co / Gap
Existing multi-agent systems for software development have several shortcomings: (1) most solutions are fragmented, addressing only specific SDLC phases; (2) context window length restrictions and attention dilution effects limit LLMs on large codebases; (3) prior frameworks use static team compositions without agile role alignment; (4) common failures in multi-agent systems include poor task verification and communication breakdowns. ALMAS addresses these by combining agile role decomposition, a novel retrieval strategy (Meta-RAG), and a "three Cs" approach (Context-aware, Collaborative, Cost-effective).

## 3. Phuong phap (Method)
ALMAS is a multi-agent framework aligned with agile software development roles:
- **Sprint Agent:** Acts as Product Manager and Scrum Master -- refines user tasks, breaks them into sub-tasks with descriptions, acceptance criteria, and effort estimates (using few-shot learning from past examples)
- **Supervisor Agent:** Routes sub-tasks to the most suitable LLMs based on specialty, size, and cost, maintaining a diverse agent pool
- **Summary Agent:** Preprocesses code repositories into concise, structured natural-language summaries per code unit, addressing context window limitations
- **Control Agent:** Uses Meta-RAG (Retrieval Augmented Generation over code summaries) to localize relevant code for each sub-task
- **Code Agent (Developer Agent):** Implements sub-tasks using localized code and summaries, writes and commits code with unit tests
- **Peer Agent:** Reviews code for functionality, vulnerabilities, hallucinations, performance, and quality; provides reports for human review

Key design principles:
- Dual operational modes: autonomous execution and interactive collaboration with human developers
- Tiered agent allocation: lightweight agents for routine tasks, advanced agents for complex architectural decisions
- Integration with SDLC tools: Jira, Bitbucket, CI/CD, VS Code/IntelliJ via plugins
- Error handling: failed tests trigger Control Agent for localization; after repeated failures, control passes to human developer with summarized action history

## 4. Dong gop chinh (Contributions)
- A vision and blueprint for an end-to-end multi-agent framework that mirrors agile software development team roles
- Meta-RAG: a novel retrieval strategy using structured code summaries for context-aware code localization
- Tiered resource allocation strategy that routes tasks to appropriate LLMs based on complexity and cost
- A case study demonstrating end-to-end application generation (Python Streamlit stock visualization app) and code augmentation with Jira and Bitbucket integration

## 5. Diem manh (Strengths)
- Comprehensive SDLC coverage: planning, development, testing, code review, and integration in one framework
- Practical industry orientation: designed at J.P. Morgan with integration to real developer tools (Jira, Bitbucket, IDE plugins)
- Cost-efficiency by design: Supervisor Agent selects optimal LLMs per task; code summaries reduce token usage
- Modular architecture allows agents to be used individually or in combination, and each can use a different LLM
- Addresses known multi-agent failure modes (poor verification, communication breakdowns) with built-in validation and error handling

## 6. Han che (Limitations)
- Primarily a vision/position paper with limited empirical evaluation -- only one illustrative case study
- No benchmarking against existing frameworks (ChatDev, MetaGPT, SWE-Agent) or standard benchmarks (SWE-bench)
- The case study uses only GPT-4o; no evaluation of multi-LLM routing effectiveness
- Scalability to large, complex real-world codebases is not demonstrated
- End-to-end evaluation is explicitly deferred to future work

## 7. Dataset & Metric
- **Evaluation:** Single case study -- creation of a Python Streamlit stock options visualization application + code augmentation (adding a bar chart feature)
- **Tools used:** GPT-4o for all agents, Jira for task management, Bitbucket for version control
- **No formal metrics reported** -- the paper is a vision/framework paper rather than an empirical evaluation

## 8. Ket qua chinh
- Successfully demonstrated end-to-end workflow: Sprint Agent decomposed user task into sub-tasks with story points, Code Agent generated a working Streamlit application with unit tests, Peer Agent conducted code review
- Code Augmentation phase: Control Agent localized relevant code via Meta-RAG summaries, Code Agent implemented new bar chart feature, Peer Agent reviewed code differences
- The paper explicitly states that "the necessary end-to-end evaluation will be explored more thoroughly in future"

## 9. Keywords
multi-agent systems, software development lifecycle, agile methodology, LLM, code generation, code review, Meta-RAG, code summarization, context-aware development, J.P. Morgan

## 10. Lien quan den de tai
Relevant to "Coding Agent Harness & Evaluation" as an architectural reference for multi-agent coding frameworks. ALMAS provides a blueprint for how agile roles can map to specialized coding agents, with built-in validation through the Peer Agent (code review) and Developer Agent (unit testing). The Meta-RAG approach for code localization and the tiered LLM routing strategy are relevant design patterns. However, the paper lacks empirical evaluation and benchmarking, making it more of a vision document than a validated contribution. It is referenced by TheBotCompany (B1) as a related framework with static team composition.
