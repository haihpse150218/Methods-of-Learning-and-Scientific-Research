# [2025] Robeyns — A Self-Improving Coding Agent (SICA)

## Metadata
- **arXiv:** 2504.15228
- **Venue:** arXiv preprint (cs.AI)
- **Year:** 2025
- **Authors:** Maxime Robeyns, Martin Szummer, Laurence Aitchison

## 1. Van de (Problem)
LLM-based coding agents are typically designed and optimized manually through hand-crafted prompting strategies, tool definitions, and agent architectures. This manual approach is ad hoc, explores only a small fraction of the solution space, and requires significant human effort. The question is whether a coding agent can autonomously modify its own codebase to improve its performance on benchmark tasks, eliminating the distinction between a meta-agent (that improves) and a target agent (that performs tasks).

## 2. Dong co / Gap
Prior work on automated agent design (ADAS) uses a separate meta-agent to improve a target agent, but is not truly self-improving since the meta-agent and target agent are distinct systems. The meta-agent in ADAS edits only a single forward function written in a domain-specific language. Godel Agent allows partial self-modification but is not a general-purpose coding agent and was evaluated only on language/math benchmarks. STOP (Self-Taught Optimizer) focuses on recursively self-improving code generation but only on algorithmic tasks, not arbitrary software engineering. No prior work demonstrates a fully self-referential, general-purpose coding agent that edits its own Python codebase to improve on real coding benchmarks like SWE-Bench.

## 3. Phuong phap (Method)
SICA implements a self-referential meta-improvement loop:

1. **Initial Agent (A_0):** A sophisticated coding agent implemented in standard Python with tools (file open/close/edit, shell commands, calculator), sub-agents (coding agent, problem-solver, reasoning agent using o3-mini), and an asynchronous overseer (LLM running in concurrent thread every 30s to detect pathological behaviors like loops).

2. **Meta-Improvement Loop (Algorithm 1):**
   - Evaluate the current best agent A_i on a benchmark suite B, storing results p_i.
   - The best-performing agent (by utility score) becomes the meta-agent for the next iteration.
   - The meta-agent examines the archive of all previous agents and their benchmark results, identifies improvements, and implements them by editing its own codebase to produce A_{i+1}.
   - The new agent is evaluated and the cycle repeats.

3. **Utility Function:** Combines benchmark score (w=0.5), cost efficiency (w=0.25, capped at $10/problem), and time efficiency (w=0.25, capped at 300s), with a timeout penalty factor of 0.5.

4. **Benchmark Suite:** Includes SWE-Bench Verified (50 random subset), LiveCodeBench (50 random), and two synthetic benchmarks (file editing from real repos, symbol navigation in Python codebases).

Key discovered improvements across iterations include: smart edit tools (diff-based instead of full file overwrite), file edit verification, AST-based symbol locator, code context summarization, and hybrid symbol locator.

## 4. Dong gop chinh (Contributions)
- SICA: a fully self-referential coding agent that eliminates the meta-agent/target-agent distinction -- the same agent edits its own codebase to improve itself.
- Empirical evidence that self-improvement works: performance on SWE-Bench Verified improves from 17% to 53% over 15 iterations, with additional gains on LiveCodeBench and synthetic benchmarks.
- Demonstrates a non-gradient-based, data-efficient learning mechanism driven by LLM reflection and code updates.
- Open-source implementation in standard Python (https://github.com/MaximeRobeyns/self_improving_coding_agent) as a reference framework for building self-improving agent systems.

## 5. Diem manh (Strengths)
- Fully self-referential: the agent that does the improving IS the agent being improved, enabling compounding improvements where better coding ability leads to better self-modifications.
- Discovers non-trivial tool improvements autonomously (AST-based symbol locators, smart diff-based editing, file edit verification) -- innovations a human developer might also implement.
- Sample-efficient: each meta-improvement step learns from detailed inspection of the archive, not from large-scale training data.
- Safety-conscious design with asynchronous overseer for monitoring agent behavior in real-time and evaluation-gated progression.
- The utility function balances performance, cost, and speed, reflecting practical deployment concerns.

## 6. Han che (Limitations)
- Difficulty generating truly novel, innovative modification ideas -- the agent tends to fixate on variations of early ideas, leading to path dependency and high variance across runs.
- 5-minute timeout and $10/problem cost cap constrain the initial agent's performance, making initial benchmark scores lower than the underlying model's potential (e.g., Sonnet 3.5 v2 on SWE-Bench).
- Much of the initial improvement comes from basic tool optimizations (faster file editing) rather than fundamental algorithmic breakthroughs.
- Self-improvement shows diminishing returns on reasoning-heavy tasks (AIME, GPQA Diamond) where the base model already performs well and scaffolding additions may interfere with the reasoning model's chain-of-thought.
- Total API cost of ~$7,000 for 15 iterations is substantial, and the approach may face benchmark saturation with static evaluation sets.

## 7. Dataset & Metric
- **Datasets:** SWE-Bench Verified (50 random subset), LiveCodeBench (50 random), synthetic file editing benchmark (from real GitHub repo commits), synthetic symbol navigation benchmark (Python codebases).
- **Metrics:** Utility function U = 0.5*p_score + 0.25*(1 - min(1, p_cost/$10)) + 0.25*(1 - min(1, p_time/300s)), with 0.5 timeout penalty. Individual benchmark accuracy reported separately.

## 8. Ket qua chinh
- SWE-Bench Verified (50 subset): 17% (iteration 0) to 53% (iteration 11-15), a 3x improvement.
- File editing benchmark: 82% (iteration 0) to 94% (iteration 15), with key improvement from implementing diff-based smart edit tool at iteration 1.
- Symbol navigation: 35% (iteration 0) to 71% (iteration 15), with major jump at iteration 9 when AST-based symbol locator was implemented.
- LiveCodeBench: 65% to 71% (modest improvement, competitive programming less amenable to scaffolding improvements).
- AIME/GPQA Diamond (reasoning tasks): marginal improvement (~76% mean accuracy), showing limits of scaffolding-based self-improvement when base model already strong.
- Average time per problem decreased slightly despite added complexity.
- Total 15-iteration run cost: ~$7,000.

## 9. Keywords
Self-improving agents, meta-programming, self-referential systems, coding agents, automated agent design, SWE-Bench, tool discovery, non-gradient learning, agent architecture search

## 10. Lien quan den de tai
Directly and highly relevant to "Coding Agent Harness & Evaluation." SICA demonstrates that the agent harness itself (tools, prompts, sub-agent configurations, oversight mechanisms) can be automatically improved through self-referential modification. Key insights for agent harness design include: (1) the utility function combining performance, cost, and speed as a holistic evaluation metric, (2) the asynchronous overseer pattern for safety monitoring during long-running agent tasks, (3) the archive-based meta-improvement loop as a systematic approach to agent architecture search, (4) the sub-agent delegation pattern for managing context length in extended runs, and (5) empirical evidence that tool quality (smart editing, AST navigation) is often more impactful than prompting strategies. The benchmark suite mixing real (SWE-Bench, LiveCodeBench) and synthetic tasks provides a practical template for evaluating coding agent harnesses.
