# [2023] Hong — MetaGPT: Meta Programming for a Multi-Agent Collaborative Framework

## Metadata
- **arXiv:** 2308.00352
- **Venue:** ICLR 2024
- **Year:** 2023
- **Authors:** Sirui Hong, Mingchen Zhuge, Jiaqi Chen, Xiawu Zheng, Yuheng Cheng, Ceyao Zhang, Jinlin Wang, Zili Wang, Steven Ka Shing Yau, Zijuan Lin, Liyang Zhou, Chenyu Ran, Lingfeng Xiao, Chenglin Wu, Jurgen Schmidhuber

## 1. Van de (Problem)
Existing LLM-based multi-agent systems can solve simple dialogue tasks but struggle with complex software engineering tasks due to cascading hallucinations caused by naively chaining LLMs. Pure natural-language communication between agents leads to information distortion (like the telephone game), logic inconsistencies, and unproductive collaboration.

## 2. Dong co / Gap
Prior multi-agent frameworks (CAMEL, ChatDev, AgentVerse) rely on unconstrained natural language communication and lack structured workflows. They have not tapped into effective workflows with structured output formats, making it harder to handle complex software engineering issues. MetaGPT fills this gap by encoding human Standardized Operating Procedures (SOPs) into the multi-agent workflow, requiring structured intermediate outputs (PRDs, design docs, code) rather than free-form chat.

## 3. Phuong phap (Method)
MetaGPT is a meta-programming framework with three key components: (1) **Agents in SOPs** -- five specialized roles (Product Manager, Architect, Project Manager, Engineer, QA Engineer) following a sequential assembly-line workflow. Each role has a defined profile, goals, constraints, and produces structured outputs (PRDs, system designs, task lists, code, tests). (2) **Communication Protocol** -- structured communication interfaces replace free-form dialogue; a shared message pool with publish-subscribe mechanism allows agents to selectively consume relevant messages based on role profiles, avoiding information overload. (3) **Iterative Programming with Executable Feedback** -- after initial code generation, the Engineer executes code and tests iteratively, using execution results and debugging memory to self-correct up to 3 retries.

## 4. Dong gop chinh (Contributions)
- Meta-programming framework that integrates human SOPs into LLM-based multi-agent collaboration, reducing hallucinations
- Structured communication protocol with publish-subscribe mechanism replacing free-form natural language chat
- Executable feedback mechanism for iterative code debugging, improving pass@1 by 4.2% (HumanEval) and 5.4% (MBPP)
- State-of-the-art results on HumanEval (85.9%) and MBPP (87.7%) code generation benchmarks
- Custom SoftwareDev benchmark of 70 real-world software development tasks for evaluating end-to-end code generation

## 5. Diem manh (Strengths)
- SOP-based workflow dramatically reduces unproductive "idle chatter" and cascading hallucinations between agents
- Structured outputs (PRDs, design docs, interface specs) enforce quality standards at each stage
- 100% task completion rate on SoftwareDev benchmark, with executability score of 3.75/4.0
- Comprehensive ablation study showing each role contributes meaningfully to final quality
- Executable feedback reduces human revision cost from 2.25 to 0.83 corrections per task

## 6. Han che (Limitations)
- Each project is executed independently -- no cross-project learning or self-improvement mechanism
- Sequential workflow is rigid; does not support dynamic reorganization of agent roles
- Higher token usage than ChatDev (31,255 vs 19,292) though more productive per token
- Static conversation pattern (assembly line) -- not flexible for tasks requiring iterative back-and-forth collaboration
- SoftwareDev benchmark is self-generated and relatively small (70 tasks, 7 used for comparison)

## 7. Dataset & Metric
- **HumanEval** (Chen et al., 2021): Pass@1 on 164 programming tasks
- **MBPP** (Austin et al., 2021): Pass@1 on 427 Python tasks
- **SoftwareDev** (custom, 70 tasks): Executability (1-4 scale), Cost (time, tokens, expense), Code Statistics (files, lines), Productivity (tokens per code line), Human Revision Cost
- Baselines: AlphaCode, Incoder, CodeGeeX, CodeGen, PaLM Coder, Codex, CodeT, GPT-4, AutoGPT, LangChain, AgentVerse, ChatDev

## 8. Ket qua chinh
- HumanEval: 85.9% Pass@1 (vs GPT-4 at 67.0%, MetaGPT w/o feedback at 81.7%)
- MBPP: 87.7% Pass@1 (vs GPT-4 at 67.7%, MetaGPT w/o feedback at 82.3%)
- SoftwareDev: Executability 3.75 vs ChatDev 2.25; Human Revision Cost 0.83 vs ChatDev 2.5
- Running time 541s vs ChatDev 762s; Productivity 124.3 tokens/line vs ChatDev 248.9
- Ablation: adding all 4 roles (4 agents) achieves executability 4.0 with only 2.5 revisions needed
- Full capability coverage (PRD, design, API, code, execution, task management, code review) vs partial in competitors

## 9. Keywords
meta-programming, standardized operating procedures, multi-agent collaboration, software development, structured communication, code generation, executable feedback, assembly-line workflow

## 10. Lien quan den de tai
Highly relevant to coding agent harness and evaluation. MetaGPT directly addresses automated software development through multi-agent collaboration with structured workflows. The SOP-based design provides a concrete model for coding agent harness architecture -- how to decompose software tasks, enforce quality through structured intermediate artifacts, and validate through executable feedback. The SoftwareDev benchmark and its multi-dimensional evaluation metrics (executability, cost, productivity, human revision cost) offer a practical template for evaluating coding agents. The comparison with other frameworks (AutoGPT, ChatDev, AgentVerse) provides useful context for the thesis.
