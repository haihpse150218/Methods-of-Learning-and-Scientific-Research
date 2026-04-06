# [2026] Fu et al. — Automatically Benchmarking LLM Code Agents through Agent-driven Annotation and Evaluation

## Metadata
- **arXiv:** 2510.24358v3
- **Venue:** AAMAS 2026 (25th International Conference on Autonomous Agents and Multiagent Systems)
- **Year:** 2026
- **Authors:** Lingyue Fu, Bolun Zhang, Hao Guan, Yaoming Zhu, Lin Qiu, Weiwen Liu, Xuezhi Cao, Xunliang Cai, Weinan Zhang, Yong Yu (Shanghai Jiao Tong University, Meituan)

## 1. Van de (Problem)
Existing benchmarks for code agent evaluation face two major limitations: (1) creating high-quality project-level evaluation datasets requires extensive domain expertise, leading to prohibitive annotation costs and limited diversity; (2) while Agent-as-a-Judge paradigms offer flexibility beyond rigid unit tests, their reliance on In-Context Learning with general LLMs often results in inaccurate assessments that misalign with human standards.

## 2. Dong co / Gap
Current benchmarks either require PhD-level expert annotators (e.g., PaperBench) or rely on narrow unit test pass rates that cannot comprehensively assess diverse, complex software projects. General-purpose LLM judges achieve at most ~83% human alignment, which is insufficient for reliable project-level evaluation. There is no scalable pipeline for creating diverse project-level benchmarks with flexible, human-aligned evaluation metrics.

## 3. Phuong phap (Method)
The authors propose a two-part solution: (1) **PRDBench** -- an agent-driven benchmark construction pipeline where code agents generate project scaffolds and Product Requirement Documents (PRDs) with criteria schemes, while human annotators only verify quality (avg 8 hours per project). Tasks are sourced from real-world requirements, academic projects, and theses across 20 domains. The scaffold is removed after annotation so agents must build from scratch. (2) **PRDJudge** -- a specialized fine-tuned evaluation agent based on Qwen3-Coder-30B, trained on 911 high-quality evaluation trajectories using LoRA. PRDJudge executes three types of tests (Unit Test, Shell Interaction, File Comparison) using six core tools, and scores code on a 0-1-2 scale (Fail/Partial/Pass). Evaluation follows two phases: DEV (zero-shot generation from PRD) and DEBUG (iterative refinement using PRDJudge feedback).

## 4. Dong gop chinh (Contributions)
- Designs an agent-driven data production pipeline that reduces annotation from PhD-level expertise to undergraduate-level verification, averaging 8 hours per project
- Constructs PRDBench with 50 project-level Python tasks across 20 domains, each with structured PRDs and 1,258 total evaluation metrics
- Introduces PRDJudge, a fine-tuned evaluation agent achieving over 90% human alignment in fixed-interface scenarios (94.19% UAR, 96.07% PAR)
- Reveals that foundation models dictate zero-shot development ceilings while commercial frameworks excel at iterative debugging
- Shows unconstrained models risk performance degradation during long-context debugging due to regressions

## 5. Diem manh (Strengths)
- Scalable benchmark construction pipeline that dramatically reduces human annotation cost while maintaining quality
- Three complementary metric types (Unit Test, Shell Interaction, File Comparison) cover a broad spectrum of QA scenarios
- PRDJudge significantly outperforms general-purpose LLM judges (Claude-4.5, GPT-5.2) in stability and accuracy
- Comprehensive evaluation of 8 minimal agents and 4 commercial agents with detailed cost-effectiveness analysis
- Two-phase evaluation (DEV + DEBUG) captures both initial generation and iterative refinement capabilities

## 6. Han che (Limitations)
- Only Python tasks; does not cover other programming languages
- 50 tasks is relatively small for broad generalization claims
- Free development mode (unconstrained interfaces) introduces significant evaluation noise that PRDJudge cannot yet handle reliably
- PRDJudge training relies on one-time expensive human annotation of ground truth scores
- Scaffold removal may not fully prevent data leakage if seed tasks come from public sources

## 7. Dataset & Metric
- **Dataset:** PRDBench -- 50 project-level Python tasks across 20 domains (Data Analysis, AI, Web Security, Automation, etc.), with 1,258 evaluation metrics (408 Unit Test, 732 Shell Interaction, 118 File Comparison). Average PRD: 105 lines of requirements.
- **Metrics:** Average pass rate (%) across metrics using 0/1/2 scoring; Human Alignment Rate (HAR) for judging PRDJudge; Unanimous Agreement Rate (UAR) and Pairwise Agreement Rate (PAR) for stability.

## 8. Ket qua chinh
- PRDJudge achieves 91.75% in-domain and 92.69% out-of-domain HAR, approaching human inter-annotator agreement (95.83%)
- Best code agent: Claude-4.5 (Minimal) achieves 69.19% DEV but drops to 56.40% after DEBUG (-12.79%), showing regression risk
- GPT-5.2 (Minimal) achieves 62.49% DEV and improves to 69.00% after DEBUG (+6.51%)
- Commercial Claude Code achieves highest DEBUG score (70.25%) with +13.60% improvement from feedback
- Unit tests are hardest to debug; Shell Interaction and File Comparison show more improvement after DEBUG
- Cost-effectiveness: minimal agents are more cost-effective in DEV; commercial agents better in DEBUG

## 9. Keywords
PRDBench, PRDJudge, Agent-as-a-Judge, code agent evaluation, benchmark construction, Product Requirement Document, fine-tuned judge, project-level coding, automated evaluation

## 10. Lien quan den de tai
Directly relevant to "Coding Agent Harness & Evaluation." PRDBench addresses the core challenge of scalable benchmark creation for project-level code agents, and PRDJudge demonstrates that fine-tuned evaluation agents can achieve near-human accuracy for automated scoring. The agent-driven annotation pipeline, the three-type metric taxonomy (Unit Test, Shell Interaction, File Comparison), and the two-phase DEV/DEBUG evaluation protocol all provide concrete design patterns for building comprehensive coding agent evaluation harnesses. The finding that general-purpose LLM judges are unreliable for complex project evaluation motivates the need for specialized, fine-tuned evaluators in any harness design.
