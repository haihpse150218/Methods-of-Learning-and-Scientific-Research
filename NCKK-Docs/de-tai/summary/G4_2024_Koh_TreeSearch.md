# [2024] Koh — Tree Search for Language Model Agents

## Metadata
- **arXiv:** 2407.01476
- **Venue:** Transactions on Machine Learning Research (TMLR), 09/2025
- **Year:** 2024
- **Authors:** Jing Yu Koh, Stephen McAleer, Daniel Fried, Ruslan Salakhutdinov

## 1. Van de (Problem)
LM-powered autonomous agents struggle with multi-step reasoning, planning, and using environmental feedback on realistic computer tasks. Existing agents greedily commit to each action without the ability to explore alternatives or backtrack from errors, leading to compounding failures. On benchmarks like VisualWebArena and WebArena, even the best agents achieve success rates far below human performance.

## 2. Dong co / Gap
While search algorithms (BFS, MCTS) have proven transformative in games (AlphaGo, Deep Blue), they have not been successfully applied to realistic web environments where the action space is large, rewards are sparse, and there are no clear win conditions. Prior work applied tree search only to simplified text environments or math/code tasks. This paper is the first to demonstrate effective inference-time tree search for LM agents in realistic, complex web environments.

## 3. Phuong phap (Method)
The approach is a best-first tree search algorithm inspired by A* search, operating within the actual web environment:

1. **Agent Backbone:** Any off-the-shelf LM agent (e.g., GPT-4o with Set-of-Marks, Llama-3-70B with captions) generates candidate actions via nucleus sampling (temperature=1.0, top-p=0.95), producing 20 samples per step with the top-b most common actions used for branching.

2. **Value Function:** A multimodal LM (GPT-4o) scores each state by estimating the likelihood of reaching the goal, using the task instruction, trajectory of screenshots, and previous actions. Self-consistency is applied by averaging over 20 sampled reasoning chains to reduce noise.

3. **Search Algorithm:** Best-first search with hyperparameters: max depth d, branching factor b, search budget c (max node expansions). At each iteration, the highest-valued state from the frontier (priority queue) is expanded. If the value exceeds threshold theta, the agent commits; otherwise it backtracks (by resetting the environment and replaying the action sequence to a previous state). Search terminates when budget c is exhausted or a high-value state is found.

Default parameters: d=5, b=5, c=20.

## 4. Dong gop chinh (Contributions)
- First inference-time tree search algorithm demonstrated to significantly improve LM agent performance on realistic web benchmarks (VisualWebArena and WebArena).
- Sets new SOTA on VisualWebArena: 26.4% success rate (39.7% relative improvement over GPT-4o baseline without search).
- Demonstrates that performance scales with increased test-time compute (larger search budget c yields higher success rates).
- Shows the approach is model-agnostic: works with both GPT-4o and Llama-3-70B, with even larger relative gains on weaker models (+119.7% for Llama-3).
- Provides ablation studies on search budget, depth, branching factor, and value function quality.

## 5. Diem manh (Strengths)
- Complementary to any existing agent: can be applied on top of any base LM agent without retraining or finetuning.
- Grounded in actual environment interaction, not just text-level search -- the agent executes actions and receives real environmental feedback.
- Scales with compute: even a small search budget (c=5) yields 30.6% relative improvement; increasing to c=20 gives 51%.
- Outperforms trajectory-level reranking (a simpler alternative), demonstrating the value of mid-trajectory backtracking.
- Explicitly addresses the compounding error problem in sequential decision-making.

## 6. Han che (Limitations)
- Search is slow: a budget of c=20 means up to 20x more LM calls per search iteration, making it expensive for production deployment.
- Backtracking requires environment reset and action replay, which is impractical for environments with destructive/irreversible actions (e.g., placing an order on an e-commerce site).
- Value function is domain-specific (tailored to web navigation with screenshots); adapting to other domains (e.g., coding, SWE tasks) requires designing new value functions.
- Capped at max 5 actions due to compute constraints, making hard tasks (requiring 10+ actions) still largely unsolved.
- Does not finetune custom value function models; using ground-truth rewards as the value function achieves 43.5% vs. 37.0%, suggesting significant headroom.

## 7. Dataset & Metric
| Benchmark | # Tasks | Metric |
|-----------|---------|--------|
| VisualWebArena (VWA) | 910 | Success Rate (binary: task completed or not) |
| WebArena (WA) | 812 | Success Rate |

Ablations on 200-task VWA subset. Results broken down by website (Classifieds, Reddit, Shopping for VWA; CMS, Map, Shopping, Reddit, GitLab for WA) and by difficulty (easy/medium/hard).

## 8. Ket qua chinh
- **VWA:** GPT-4o + SoM baseline 18.9% --> with search **26.4%** (+39.7% relative). Llama-3 baseline 7.6% --> with search **16.7%** (+119.7% relative).
- **WA:** GPT-4o baseline 15.0% --> with search **19.2%** (+28.0% relative). Llama-3 baseline 7.6% --> with search **10.1%** (+32.2% relative).
- **Scaling:** Success rate increases monotonically with search budget c (24.5% at c=0 to 37.0% at c=20 on 200-task VWA subset).
- **Depth and breadth both matter:** d=5, b=5 achieves +51% over no search; reducing either dimension degrades performance.
- **Medium-difficulty tasks benefit most:** +75% relative improvement on medium tasks vs. +24% on easy and +47% on hard.
- **Trajectory reranking plateaus at ~30%** with 7 trajectories, underperforming tree search (c=5) at equivalent compute.
- **Value function quality matters:** GPT-4o with self-consistency (n=20) achieves 37.0%; without SC only 28.5%; ground-truth reward reaches 43.5%.

## 9. Keywords
tree search, best-first search, inference-time compute, web agents, VisualWebArena, WebArena, value function, backtracking, test-time scaling, LM agents

## 10. Lien quan den de tai
This paper is highly relevant to coding agent harness design. The core idea -- using tree search with backtracking at inference time to improve agent performance -- directly applies to coding agents (e.g., SWE-bench solvers). The authors explicitly note that programming is a domain where "actions are non-destructive as they can always be undone or reset," making tree search particularly suitable for coding tasks. The value function concept maps to using test execution results, linting scores, or compilation feedback as heuristics to guide search in a coding agent harness. The finding that performance scales with test-time compute supports the design of harnesses that allow configurable compute budgets. The need for domain-specific value functions highlights a key design challenge for coding agent evaluation frameworks.
