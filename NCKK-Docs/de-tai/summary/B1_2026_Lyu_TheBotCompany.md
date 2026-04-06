# [2026] Lyu — Self-Organizing Multi-Agent Systems for Continuous Software Development (TheBotCompany)

## Metadata
- **arXiv:** 2603.25928v1
- **Venue:** ACM Conference (Conference'17, Washington, DC, USA)
- **Year:** 2026
- **Authors:** Wenhan Lyu, Yue Xiao, Yixuan Zhang, Yifan Sun (William & Mary)

## 1. Van de (Problem)
Most existing LLM-based multi-agent systems for software development focus on completing small, isolated tasks in single sessions. They lack the ability to sustain persistent, continuous software development over days or weeks, with cumulative progress tracking, adaptive team composition, and iterative refinement across milestones.

## 2. Dong co / Gap
Three specific gaps exist in current approaches: (1) **Limited persistent orchestration** -- systems like ChatDev, MetaGPT, SWE-Agent are designed for single-session execution with no built-in mechanism to track cumulative progress or resume work across sessions. (2) **Static, session-scoped team composition** -- agent roles are predetermined at design time and remain fixed, unlike real software teams that evolve as projects progress. (3) **Synchronous human oversight** -- existing systems require real-time human monitoring rather than supporting asynchronous intervention as in real-world workflows.

## 3. Phuong phap (Method)
TheBotCompany is an open-source orchestration framework built around three innovations:
- **Three-phase state machine (Strategy -> Execution -> Verification):** Each milestone passes through Athena (planning), Ares (implementation), and Apollo (verification) managers in sequence. Apollo acts as an adversarial verifier that can reject milestones and trigger fix rounds with halved budgets.
- **Self-organizing agent teams:** Only three manager roles are permanent. Managers dynamically hire, specialize, reassign, and retire worker agents based on milestone demands via persistent skill files.
- **Asynchronous human oversight:** A web-based monitoring dashboard (PWA) with live agent streaming, push notifications, and issue-based intervention allows humans to steer development without blocking agents.
- Infrastructure includes a per-project SQLite issue tracker, agent-local knowledge base (note.md), structured directives for orchestrator communication, and budget management with exponential decay on verification failures.

## 4. Dong gop chinh (Contributions)
- Design and implementation of TheBotCompany, an open-source framework introducing persistent, milestone-driven development with asynchronous human oversight
- A self-organizing team model where managers dynamically compose worker teams based on evolving milestone demands, replacing fixed-role teams
- Empirical evaluation on 4 real-world long-running projects (Go, Python, Rust, C++) over days of continuous operation, plus ProjDevBench benchmarks
- Demonstration that the verification phase catches substantive defects and shapes future planning through anti-pattern accumulation
- Practical lessons for multi-agent system design including cost crossover points and oversight granularity tiers

## 5. Diem manh (Strengths)
- Addresses a genuine gap: persistent, multi-day autonomous software development is largely unexplored
- Comprehensive three-phase lifecycle mirrors real software engineering practice (plan-implement-review)
- Strong empirical evaluation across 4 projects in 4 languages, completing 164 milestones and 616 cycles over 137 wall-clock hours without human intervention
- Outperforms all single-agent baselines on ProjDevBench hard problems (+9.6/+10.7 points over same-model Claude Code baseline)
- Self-aware termination and anti-pattern accumulation demonstrate emergent intelligent behavior

## 6. Han che (Limitations)
- All experiments use Claude-family models only; unknown if multi-agent coordination benefit holds with other LLM backends
- Only 4 long-running projects evaluated, skewing toward system projects with deterministic correctness oracles
- Single-run results with non-deterministic LLMs preclude variance estimation
- On problems admitting compact single-session solutions (e.g., P16), multi-agent overhead reduces both score and cost-efficiency
- Consumes 1.65x more output tokens per attempt than single-agent Claude Code baseline

## 7. Dataset & Metric
- **Benchmarks:** ProjDevBench (5 hardest problems: P3, P4, P15, P16, P17) -- end-to-end coding benchmark with execution score (max 80) and overall score (max 100)
- **Long-running projects:** M2Sim (Go, CPU simulator), GroundDB (Python, database engine), RustLaTex (Rust, LaTeX compiler), PyInterpreter (C++, Python interpreter)
- **Metrics:** Milestones completed, commits, LOC, test cases added, benchmark scores, Apollo rejection rate, cost per milestone, token breakdown (manager vs worker), cycle waste ratio, failure taxonomy

## 8. Ket qua chinh
- Completed 164 milestones across 4 projects over 137 hours without human intervention; cycle waste ratio was low (max 6.9% in RustLaTex)
- ProjDevBench: TheBotCompany (Sonnet 4.5) achieves 53.2 execution / 70.0 overall, leading all single-agent baselines; same-model gap is +9.6 exec / +10.7 overall
- Verification phase rejection rate varies with specification clarity (0% for exact oracles, up to 18.6% for iterative quality targets); anti-pattern knowledge accumulates and durably shapes planning
- Worker agents consume 70.6% of total cost; orchestration overhead (Athena) remains modest at 9.8%
- Failure modes are predominantly domain-specific; orchestration failures are rare and recover within one cycle

## 9. Keywords
multi-agent systems, continuous software development, self-organizing teams, LLM orchestration, milestone-driven development, verification phase, persistent state, coding agents, ProjDevBench

## 10. Lien quan den de tai
Directly relevant to "Coding Agent Harness & Evaluation": TheBotCompany represents a harness/orchestration framework for coding agents with a built-in evaluation mechanism (the Apollo verification phase). It demonstrates how to structure multi-agent coding workflows with persistent state, addresses the challenge of evaluating agent output through adversarial verification, and benchmarks against ProjDevBench -- an end-to-end development benchmark. The self-organizing team model and three-phase lifecycle are key architectural patterns for coding agent orchestration. The comparison with single-agent baselines provides evidence for when multi-agent coordination adds value versus overhead.
