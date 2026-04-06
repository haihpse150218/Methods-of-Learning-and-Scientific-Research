# [2024] Liu — LLM+P: Empowering Large Language Models with Optimal Planning Proficiency

## Metadata
- **arXiv:** 2304.11477
- **Venue:** arXiv preprint (v3, Sep 2023)
- **Year:** 2024
- **Authors:** Bo Liu, Yuqian Jiang, Xiaohan Zhang, Qiang Liu, Shiqi Zhang, Joydeep Biswas, Peter Stone

## 1. Van de (Problem)
LLMs like GPT-4 cannot reliably solve long-horizon robot planning problems -- they generate plans that appear plausible in natural language but are often infeasible or suboptimal because LLMs lack true understanding of preconditions, effects, and constraints. Classical planners can find correct and optimal plans but require formal PDDL input, which is hard for end users to provide.

## 2. Dong co / Gap
LLMs excel at linguistic competence (knowing *how* to say things) but lack functional competence (knowing *what* to say) for planning. Classical planners guarantee correctness and optimality but require structured PDDL input. No prior work systematically combined both strengths: using LLMs as translators from natural language to PDDL, then delegating actual planning to a sound-and-complete classical planner.

## 3. Phuong phap (Method)
LLM+P is a three-stage pipeline:
1. **NL-to-PDDL Translation:** Given a natural language problem description and a domain PDDL file, the LLM (GPT-4) translates the problem into a PDDL problem file using in-context learning (one example problem-PDDL pair as demonstration).
2. **Classical Planning:** The generated PDDL problem file is fed into the Fast-Downward planner (with SEQ-OPT-FDSS-1 for optimal plans or LAMA for sub-optimal) to find a solution.
3. **PDDL-to-NL Translation:** The LLM translates the symbolic plan back into natural language for the user.

Key assumptions: a domain PDDL is pre-provided by a human expert, and one minimal example problem+PDDL pair is given as context.

## 4. Dong gop chinh (Contributions)
- First framework to combine LLMs with classical planners (LLM+P), enabling optimal planning from natural language input without finetuning.
- A diverse benchmark of 7 robot planning domains (140 problems) from International Planning Competitions.
- Empirical demonstration that LLM-as-Planner (direct plan generation) fails on most problems while LLM+P achieves high success rates.
- Real-robot demonstration showing LLM+P enables a service robot to execute optimal tidy-up plans.
- Public codebase for reproducibility.

## 5. Diem manh (Strengths)
- Guarantees plan correctness and optimality by delegating to a sound-and-complete planner, avoiding LLM hallucinations in plan generation.
- Requires no finetuning or retraining of the LLM -- purely in-context learning with one example.
- Practical: demonstrated on a real robot performing household tasks.
- Clean separation of concerns: LLM handles NL-to-formal translation, planner handles search.

## 6. Han che (Limitations)
- Requires a human-provided domain PDDL file for each new domain -- does not auto-generate domain specifications.
- The LLM does not auto-detect when to invoke LLM+P vs. answer directly.
- PDDL translation errors (e.g., missing initial conditions, incorrect predicates) cause the planner to fail or produce wrong solutions.
- Limited to classical planning domains expressible in PDDL; does not handle partial observability, stochastic environments, or continuous actions.
- In-context example is essential -- without it, LLM generates incorrect PDDL files.

## 7. Dataset & Metric
| Domain | # Problems | Metric |
|--------|-----------|--------|
| Barman | 20 | Success Rate (%) -- optimal plans found |
| Blocksworld | 20 | Success Rate (%) |
| Floortile | 20 | Success Rate (%) |
| Grippers | 20 | Success Rate (%) |
| Storage | 20 | Success Rate (%) |
| Termes | 20 | Success Rate (%) |
| Tyreworld | 20 | Success Rate (%) |

Baselines: LLM-as-P (no context), LLM-as-P (with context), LLM-as-P (ToT), LLM+P (no context), LLM+P (full).

## 8. Ket qua chinh
- **LLM-as-Planner** (GPT-4 directly generating plans) achieves 0% success on 4/7 domains and at most 35% on the easiest domain (Grippers with context).
- **LLM+P** achieves 100% on Barman, 90% on Blocksworld, 100% on Grippers, 85% on Storage, 90% on Tyreworld.
- **LLM+P fails** on Floortile (0%) and struggles on Termes (20%) due to complex spatial constraints that GPT-4 cannot translate correctly into PDDL.
- **ToT-based planning** (LLM-as-P with tree search) times out on most problems due to excessive LLM calls, making it impractical for long-horizon planning.
- In-context example is crucial: LLM+P without context achieves 0% on all domains.

## 9. Keywords
LLM+P, classical planning, PDDL, external planner, Fast-Downward, optimal planning, robot planning, in-context learning, natural language to formal language

## 10. Lien quan den de tai
LLM+P exemplifies the "external planner-aided" approach from the planning taxonomy, showing that LLMs alone are unreliable planners but excel as translators between natural language and formal representations. For coding agent harness design, this suggests a similar pattern: use LLMs to interpret task descriptions and translate them into structured formats, then leverage deterministic tools (test runners, static analyzers, compilers) for verification. The finding that in-context examples are essential parallels the importance of few-shot prompting in coding agent harnesses. The failure modes (missing preconditions, incorrect state tracking) are analogous to coding agents failing to account for dependencies or side effects.
