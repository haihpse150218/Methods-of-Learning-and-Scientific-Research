# [2025] Liu — Lessons Learned: A Multi-Agent Framework for Code LLMs to Learn and Improve

## Metadata
- **arXiv:** 2505.23946
- **Venue:** NeurIPS 2025
- **Year:** 2025
- **Authors:** Yuanzhe Liu, Ryan Deng, Tim Kaler, Xuhao Chen, Charles E. Leiserson, Yao Ma, Jie Chen

## 1. Van de (Problem)
Different LLMs excel at different coding tasks and optimization categories, with no single model dominating across all problems. This complementary strength at a fine-grained level is not exploited by existing multi-agent frameworks that assign fixed roles (planner, coder, debugger) or simply aggregate independent solutions. The question is how to leverage multiple LLM agents to collaboratively solve coding problems without knowing their individual strengths a priori.

## 2. Dong co / Gap
Existing multi-agent collaboration frameworks either assign pre-specified roles to agents (e.g., AgentVerse, MetaGPT, MapCoder) or independently propose solutions that are aggregated (e.g., MoA, LLM-Debate). These approaches do not allow agents to learn from each other's successes and failures during the problem-solving process. Additionally, code optimization is an under-explored but critical task where LLMs lack explicit training on low-level system knowledge (caching, vectorization, parallelization).

## 3. Phuong phap (Method)
LessonL is a lesson-based multi-agent collaboration framework with three core mechanisms:

1. **Lesson Solicitation:** After each agent generates a solution, the framework grades it (speedup, slowdown, functional incorrectness, syntax error) and prompts the agent to articulate a lesson -- explaining why the solution succeeded or failed.
2. **Lesson Banking and Selection:** Lessons are deposited into a shared bank. In each round, at most k lessons are selected based on: (a) speedup-based ranking (top k/2 by speedup), and (b) semantic relevance to the original code (top k/2 by cosine similarity using CodeBERT embeddings).
3. **Effectiveness Adjustment:** A dynamic adjustment factor f tracks whether lessons actually deliver their promised speedup when applied by other agents, updating lesson priorities across rounds.

The process iterates for T rounds, with agents generating updated solutions informed by selected lessons. The framework extends to code generation by soliciting lessons only for functional incorrectness.

## 4. Dong gop chinh (Contributions)
- Finding that LLMs have complementary strengths at a fine-grained task level, motivating collaborative approaches.
- A novel lesson-based framework where agents learn from each other's successes and failures through an explicit lesson solicitation-banking-selection mechanism.
- State-of-the-art performance on code optimization (ParEval, PolyBench) and code generation (HumanEval, HumanEval+, MBPP, MBPP+) benchmarks.
- Empirical evidence that a team of small LLMs (7B-14B) can significantly outperform a much larger LLM (GPT-4o) under similar resource budgets.
- Pareto-optimal cost-performance tradeoff compared to competing multi-agent methods.

## 5. Diem manh (Strengths)
- Agents do not need pre-assigned roles; their complementary strengths emerge naturally through lesson sharing.
- Lessons are interpretable and reusable, enabling explication of coding knowledge and creation of educational materials.
- Communication is more economical since lessons are more concise than full code solutions.
- Performance consistently improves over multiple rounds (up to 10), unlike MoA and MapCoder which degrade.
- Demonstrated Pareto optimality on cost vs. speedup, making it practical for budget-constrained settings.

## 6. Han che (Limitations)
- Learning from lessons defers time to first token, as lesson solicitation and subsequent trials add overhead, potentially affecting user experience.
- Currently applied only to function-level code snippets, not yet extended to repository-level tasks (e.g., SWE-bench).
- Some problems remain too challenging for small LLMs even with collaboration (syntax errors, semantic errors, lack of speedup).
- Effectiveness adjustment mechanism has different optimal strategies for serial vs. OpenMP modes, suggesting task-dependent tuning is needed.

## 7. Dataset & Metric
- **Datasets:** ParEval (60 tasks, serial + OpenMP modes), PolyBench (30 numerical tasks), HumanEval (164), HumanEval+ (80x more tests), MBPP (~1000), MBPP+ (35x more tests).
- **Metrics:** Code optimization: geometric mean speedup, proportion of correct code, proportion achieving >2x speedup. Code generation: pass@1.

## 8. Ket qua chinh
- Code optimization on ParEval (serial): LessonL achieves 0.91 correctness and 2.16x geometric mean speedup, outperforming GPT-4o (1.72x), OpenAI o3 (2.21x in speedup but lower correctness), MapCoder (1.85x), and MoA (1.76x).
- Code optimization on ParEval (OpenMP): LessonL achieves 3.46x speedup vs. GPT-4o's 2.93x.
- Code generation: LessonL achieves best on HumanEval (0.915), HumanEval+ (0.878), MBPP (0.899); best or second on MBPP+ (0.765).
- A team of 3 small open-source models (Deepseek7B, Qwen7B, Qwen14B) outperforms GPT-4o across all benchmarks.
- Adding more agents improves performance with diminishing returns; biggest gain is from 1 to 3 agents.

## 9. Keywords
Multi-agent collaboration, code optimization, lesson learning, LLM agents, code generation, peer learning, knowledge sharing, Pareto optimality

## 10. Lien quan den de tai
Directly relevant to "Coding Agent Harness & Evaluation." LessonL provides a novel inter-agent communication mechanism (lessons) that could be integrated into coding agent harnesses. The finding that small LLMs collaborating can outperform large LLMs is significant for harness design decisions. The lesson banking and selection mechanism offers an alternative to fixed-role multi-agent architectures. The cost analysis framework (speedup vs. dollars/FLOPS) provides a practical evaluation methodology for coding agent systems. The extension from code optimization to code generation demonstrates the framework's generalizability across coding tasks.
