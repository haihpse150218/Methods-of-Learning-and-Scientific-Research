# [2025] Xu et al. — SWE-Compass: Towards Unified Evaluation of Agentic Coding Abilities for Large Language Models

## Metadata
- **arXiv:** 2511.05459v3
- **Venue:** arXiv preprint (cs.SE)
- **Year:** 2025 (v3: 11 Nov 2025)
- **Authors:** Jingxuan Xu, Ken Deng, Weihao Li, Songwei Yu, Huaixi Tang, Haoyang Huang, Zhiyi Lai, Zizheng Zhan, Yanan Wu, Chenchen Zhang, Kepeng Lei, Yifan Yao, Xinping Lei, Wenqiang Zhu, Zongxian Feng, Han Li, Junqi Xiong, Dailin Li, Zuchen Gao, Kun Wu, Wen Xiang, Ziqi Zhan, Yuanxing Zhang, Wuxuan Gong, Ziyuan Gao, Guanxiang Wang, Yirong Xue, Mengtong Li, Mengfei Xie, Xiaojiang Zhang, Jinghui Wang, Wenhao Zhuang, Zheng Lin, Huiming Wang, Zhaoxiang Zhang, Yuqun Zhang, Haotian Zhang, Bin Chen, Jiaheng Liu (Kuaishou Technology, Nanjing University)

## 1. Van de (Problem)
Evaluating LLMs for software engineering has been limited by narrow task coverage (mostly bug fixing), language bias (predominantly Python), and insufficient alignment with real-world developer workflows. Existing benchmarks like SWE-Bench and its variants converge on bug fixing as the dominant evaluation axis, neglecting critical developer activities such as feature implementation, refactoring, configuration, test generation, and performance optimization across diverse programming languages and scenarios.

## 2. Dong co / Gap
Current benchmarks are overwhelmingly confined to Python-centric bug fixing tasks. This narrowness prevents systematic capability diagnosis and obscures whether strong performance stems from generalizable reasoning or artifact-specific adaptation. No existing benchmark systematically structures evaluation along orthogonal axes of task type and programming scenario across multiple languages, making it impossible to identify specific model strengths and weaknesses across the full software development lifecycle.

## 3. Phuong phap (Method)
SWE-Compass is constructed through a five-step pipeline: (1) **User Analysis** -- iterative Active Learning on Stack Overflow and GitHub discussions to identify 8 task types, 8 programming scenarios, and 10 languages; (2) **Data Collection** -- gathering ~50,000 high-quality PRs from GitHub repositories (500+ stars, active maintenance, 3+ contributors); (3) **Environment Building** -- constructing Docker images for reproducible execution (initial 2% success, raised to 8% with expert intervention, yielding ~4,000 images); (4) **Task Building** -- three complementary strategies: Checklist Synthesis (for Code Understanding), Reverse Masking (for Config/Deployment and Test Generation), and Heuristic Filtering (for patch-based tasks like Bug Fixing, Refactoring, Feature Implementation/Enhancement, Performance Optimization); (5) **Data Validation** -- difficulty filtering, balanced sampling, and manual verification. Evaluation uses task-type-aligned metrics: Pass@1, Performance Optimization Score, Line Coverage, and LLM-as-a-Judge Score. Two agent frameworks are evaluated: SWE-Agent and Claude Code, across 10 LLMs.

## 4. Dong gop chinh (Contributions)
- Introduces a comprehensive benchmark with 2,000 instances spanning 8 task types, 8 programming scenarios, and 10 programming languages -- the broadest coverage of any SWE benchmark
- Establishes a systematic taxonomy derived from real developer discussions, aligning evaluation with actual development workflows
- Reveals consistent hierarchies of task difficulty (Code Understanding easiest; Test Generation and Performance Optimization hardest) and language stratification (JVM/JS ecosystems easier; systems languages harder)
- Provides detailed failure mode analysis showing Requirement Misinterpretation (30-34%) and Incomplete Solution & Side Effects (29-42%) dominate failures across all models
- Demonstrates that stronger models improve more consistently across languages rather than specializing

## 5. Diem manh (Strengths)
- Unparalleled breadth: 8 task types x 8 scenarios x 10 languages provides multi-dimensional diagnostic capability no other benchmark offers
- Grounded in real-world GitHub PRs with reproducible Docker-based execution environments
- Task-type-aligned metrics (Pass@1, Performance Optimization Score, Line Coverage, LLM-as-Judge) match evaluation to the nature of each task
- Cross-language analysis reveals important patterns (JVM determinism helps; systems languages are harder; Python is mid-tier due to dataset selection effects)
- Two complementary agent frameworks (SWE-Agent vs Claude Code) reveal that workflow design matters as much as model capability

## 6. Han che (Limitations)
- Very low environment build success rate (2-8%) means the 4,000 working images are a small, potentially biased subset of the 50,000 PRs collected
- Some task types (Code Understanding, Test Generation, Config & Deployment) use synthesis or reverse masking rather than fully natural tasks
- LLM-as-a-Judge evaluation for Code Understanding introduces its own reliability concerns
- 2,000 instances spread across 8x8x10 dimensions means some cells have very few samples
- All evaluations are offline (no networking), which may not capture real-world agent behavior

## 7. Dataset & Metric
- **Dataset:** SWE-Compass -- 2,000 verified instances from 40 repositories, spanning 8 task types (Feature Implementation, Feature Enhancement, Bug Fixing, Refactoring, Performance Optimization, Code Understanding, Test Case Generation, Configuration & Deployment), 8 programming scenarios, and 10 programming languages (Python, JavaScript, TypeScript, Java, C, C++, Go, Rust, Kotlin, C#). Average 4.7 modified files per instance.
- **Metrics:** Pass@1 (for FI, FE, BF, RF); Performance Optimization Score (for PO); Line Coverage (for TG); LLM-as-a-Judge Score (for CU).

## 8. Ket qua chinh
- Claude-Sonnet-4 ranks first on both frameworks: 32.9% AVG (Claude Code), 31.8% AVG (SWE-Agent)
- Scores cluster in the low-to-mid 20s overall (10-33% range), showing the benchmark is challenging
- Task hierarchy: Code Understanding (~56%) > Configuration & Deployment (~51-65%, high variance) > Feature Enhancement (~32%) > Bug Fixing/Refactoring (~24%) > Feature Implementation (~21%) > Test Generation (~25%) > Performance Optimization (~25%)
- Language stratification: JVM ecosystems (Java/Kotlin/JavaScript) score higher; systems languages (C/C++/Rust/Go) are harder; Python is mid-tier
- Two frameworks are complementary: SWE-Agent better at BF and multi-file localization; Claude Code better at deterministic tasks (CD, CU, TG)
- Dominant failure modes across all models: Requirement Misinterpretation (30-34%) and Incomplete Solution & Side Effects (29-42%), together >60% of failures
- Stronger models show lower cross-language variability, indicating broad capability rather than specialization

## 9. Keywords
SWE-Compass, coding benchmark, multi-language evaluation, task taxonomy, software engineering, agentic coding, SWE-Agent, Claude Code, failure analysis, programming scenarios

## 10. Lien quan den de tai
Directly relevant to "Coding Agent Harness & Evaluation." SWE-Compass provides the most comprehensive multi-dimensional evaluation framework for coding agents, spanning task types, scenarios, and languages. Its design principles (real-world alignment, comprehensive coverage, systematic taxonomy, evaluation fidelity) and construction methodology (Active Learning for taxonomy discovery, Docker-based reproducible environments, task-type-aligned metrics) offer a blueprint for building thorough evaluation harnesses. The finding that failure modes are dominated by requirement misinterpretation and incomplete solutions (not raw coding ability) suggests that harness design should prioritize testing comprehension and holistic solution quality rather than narrow code generation. The cross-language and cross-framework analyses also highlight the need for multi-dimensional evaluation rather than single-benchmark rankings.
