# [2026] Lou — AutoHarness: Improving LLM Agents by Automatically Synthesizing a Code Harness

## Metadata
- **arXiv:** 2603.03329v1
- **Venue:** arXiv preprint (cs.CL)
- **Year:** 2026
- **Authors:** Xinghua Lou, Miguel Lazaro-Gredilla, Antoine Dedieu, Carter Wendelken, Wolfgang Lehrach, Kevin P. Murphy

## 1. Van de (Problem)
When LLMs are used as agents in structured environments (e.g., games), they frequently attempt illegal or invalid actions despite understanding the task. For example, in the Kaggle GameArena chess competition, 78% of Gemini-2.5-Flash losses were due to simple illegal moves rather than strategic blunders. Hand-coded harnesses that filter invalid actions are brittle and require manual effort for each new environment.

## 2. Dong co / Gap
Traditional approaches to mitigate invalid actions involve fine-tuning on game trajectories (expensive, not scalable, can degrade other capabilities) or hand-designed harnesses (brittle, labor-intensive, not generalizable). There is a gap in automatically generating code harnesses that constrain LLM agents to only produce valid actions, offloading validity checking from the LLM's internal reasoning to an external, verifiable program.

## 3. Phuong phap (Method)
The authors propose "code as harness" -- using an LLM to automatically synthesize its own code harness through iterative refinement guided by tree search with Thompson sampling:
- **Tree search with Thompson sampling:** Maintains multiple code hypotheses in a tree structure. Each node's heuristic value is the average legal move accuracy. Thompson sampling balances exploration (trying new code structures) vs. exploitation (refining working code).
- **Evaluator-Critic-Refiner loop:** New code is rolled out in 10 parallel environments (up to 1000 steps). Failed steps are fed to a Critic that consolidates error messages, which are then given to the Refiner LLM to generate improved code.
- **Two harness types:** (1) **Harness-as-action-filter** -- generates `is_legal_action()` and `propose_action()` functions; the LLM still makes strategic decisions but the harness filters illegal moves. (2) **Harness-as-policy** -- generates the entire policy as code (`propose_action()` directly outputs the best move), eliminating LLM calls at inference time entirely.
- Training uses Gemini-2.5-Flash as the code generation model.

## 4. Dong gop chinh (Contributions)
- Propose "code as harness" paradigm where an LLM automatically synthesizes code to constrain or replace itself at inference time
- Demonstrate that auto-synthesized harnesses achieve 100% legal action rate across all 145 TextArena games
- Show that a smaller model (Gemini-2.5-Flash) with an auto-harness can outperform a larger model (Gemini-2.5-Pro) without one
- Introduce harness-as-policy variant that generates pure Python code as the entire policy, achieving highest average reward (0.870) on 1P games with near-zero inference cost
- Formulate harness generation as a search problem over the space of programs using Thompson sampling-guided tree search

## 5. Diem manh (Strengths)
- Elegant and general approach: the LLM writes its own guardrails as executable code, which is verifiable and deterministic
- Strong empirical results: 100% legal action rate on all 145 games, and smaller model + harness beats larger model without harness
- Harness-as-policy is extremely cost-effective: pure Python code runs at near-zero inference cost while outperforming GPT-5.2-High ($640 in API costs)
- Scalable: average training converges in only 14.5 tree search iterations
- Clean separation between validity checking (code) and strategic reasoning (LLM), offloading constraint satisfaction to verifiable programs

## 6. Han che (Limitations)
- Evaluated only on text-based game environments (TextArena); unclear how well it generalizes to other agent domains like software engineering or robotics
- Harness-as-policy currently only works for 1-player games; 2-player games require opponent modeling which is harder to encode as static code
- A separate harness must be generated for each environment/game; no cross-environment transfer or reusable harness library yet
- The approach assumes the environment provides clear feedback on whether actions are legal, which may not hold in all real-world settings
- Limited to environments with discrete, well-defined action spaces

## 7. Dataset & Metric
- **Dataset:** TextArena -- 145 text-based games (both 1-player and 2-player), including Chess, Checkers, Blackjack, Sudoku, and many variants. 32 games selected for end-to-end agent evaluation (16 1P + 16 2P).
- **Metrics:** Legal action success rate (fraction of legal moves), average reward (for 1P games), win/draw/loss rate (for 2P games), number of learning steps to convergence.

## 8. Ket qua chinh
- **100% legal action rate** achieved on all 145 games with the auto-synthesized harness
- **2P games:** Gemini-2.5-Flash+Harness wins 9/16 games against Gemini-2.5-Pro (56.3% win rate vs. 38.2% for Pro). Against vanilla Flash, wins 12/16 games (64.8% win rate)
- **1P games:** Gemini-2.5-Flash+Harness achieves 0.745 average reward vs. 0.707 for Gemini-2.5-Pro and 0.673 for vanilla Flash
- **Harness-as-policy (1P):** Achieves highest average reward of 0.870, outperforming GPT-5.2 (0.635), Gemini-2.5-Pro (0.707), and GPT-5.2-High (0.844), at near-zero inference cost
- Training converges in average 14.5 iterations; 19/32 games finish in under 10 iterations

## 9. Keywords
`code-harness` `LLM-agent` `action-validity` `tree-search` `Thompson-sampling` `code-synthesis` `iterative-refinement` `TextArena` `game-playing` `rejection-sampling`

## 10. Lien quan den de tai
Highly relevant to the thesis on "Coding Agent Harness & Evaluation." This paper directly addresses the concept of a "harness" -- the code layer between an LLM and its environment that constrains agent behavior. While applied to game environments rather than software engineering, the core idea of automatically synthesizing harness code to enforce action validity is transferable to coding agent evaluation. The harness-as-action-filter pattern (validate then retry) mirrors safety mechanisms in coding agents. The paper also demonstrates that harness quality directly impacts agent performance, supporting the thesis premise that harness design is a critical factor in agent evaluation.
