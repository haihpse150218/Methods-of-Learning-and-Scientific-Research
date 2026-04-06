# [2024] Huang — Understanding the Planning of LLM Agents: A Survey

## Metadata
- **arXiv:** 2402.02716
- **Venue:** arXiv preprint
- **Year:** 2024
- **Authors:** Xu Huang, Weiwen Liu, Xiaolong Chen, Xingmei Wang, Hao Wang, Defu Lian, Yasheng Wang, Ruiming Tang, Enhong Chen

## 1. Van de (Problem)
LLM-based autonomous agents rely heavily on planning capabilities, yet existing surveys on LLMs cover decision-making, reasoning, and tool use without providing a dedicated, systematic analysis of planning ability. There is no unified taxonomy that organizes the rapidly growing body of work on how LLMs plan, making it difficult for researchers to understand the landscape and identify open challenges.

## 2. Dong co / Gap
Prior surveys treat planning as one aspect among many (e.g., surveys on autonomous agents, reasoning, tool learning). This paper fills the gap by offering the first survey focused exclusively on the planning ability of LLM-based agents, proposing a five-category taxonomy and conducting comparative experiments across four benchmarks.

## 3. Phuong phap (Method)
The authors perform a literature survey and propose a taxonomy that classifies LLM-agent planning methods into five categories:
1. **Task Decomposition** -- divide-and-conquer; decomposition-first vs. interleaved (CoT, ReAct, HuggingGPT).
2. **Multi-Plan Selection** -- generate multiple candidate plans and select the best via search algorithms (ToT, GoT, CoT-SC, LLM-MCTS).
3. **External Planner-Aided Planning** -- integrate symbolic planners (PDDL) or neural planners with LLMs (LLM+P, SwiftSage).
4. **Reflection and Refinement** -- iterative self-correction loop (Reflexion, CRITIC, Self-Refine).
5. **Memory-Augmented Planning** -- RAG-based or embodied memory to store and retrieve past experiences (REMEMBER, MemoryBank).

They also benchmark six prompt-based methods (Z-CoT, F-CoT, CoT-SC, SayCan, ReAct, Reflexion) on ALFWorld, ScienceWorld, HotPotQA, and FEVER.

## 4. Dong gop chinh (Contributions)
- First systematic taxonomy dedicated to LLM-agent planning, covering five distinct research directions.
- Formal mathematical formulation for each planning category, providing a unified framework.
- Comparative experimental evaluation of six representative methods on four interactive benchmarks, revealing cost-performance trade-offs.
- Identification of key open challenges: hallucinations, plan feasibility, plan efficiency, multi-modal feedback, and fine-grained evaluation.

## 5. Diem manh (Strengths)
- Comprehensive coverage of the planning landscape with clear categorization and formal notation.
- Practical benchmark comparison showing that performance increases with token cost, and that reflection is crucial for complex tasks.
- Each category includes a dedicated discussion section analyzing trade-offs and limitations.
- Covers both prompt-based and fine-tuning-based approaches for completeness.

## 6. Han che (Limitations)
- Experiments are limited to prompt-based methods due to budget constraints; fine-tuning and external-planner methods are not empirically compared.
- Uses older API (text-davinci-003); results may not generalize to newer models like GPT-4.
- Benchmarks are primarily text-based interactive environments; real-world multi-modal or code-based planning tasks are not evaluated.
- The survey is a snapshot of a fast-moving field (Feb 2024) and may already be missing recent advances.

## 7. Dataset & Metric
| Benchmark | Domain | Metric |
|-----------|--------|--------|
| ALFWorld | Text-based household game | Success Rate (SR) |
| ScienceWorld | Text-based science simulation | Average Reward (AR) |
| HotPotQA | Multi-hop QA | Success Rate (SR) |
| FEVER | Fact verification | Success Rate (SR) |

Expenses measured by token cost via OpenAI API.

## 8. Ket qua chinh
- Reflexion achieves highest SR on ALFWorld (0.71) and HotPotQA (0.39) but at the highest cost.
- ReAct achieves best reward on ScienceWorld (19.39) with moderate cost.
- Few-shot CoT consistently outperforms Zero-shot CoT, especially on complex tasks.
- CoT-SC provides good balance of cost and performance on QA tasks.
- Key finding: **performance scales with token expenditure**; reflection doubles token usage vs. ReAct but yields meaningful improvements on complex tasks.

## 9. Keywords
LLM agents, planning, task decomposition, multi-plan selection, tree search, reflection, memory-augmented planning, Chain-of-Thought, ReAct, Reflexion

## 10. Lien quan den de tai
This survey provides the theoretical foundation for understanding how coding agents plan. The five-category taxonomy (especially task decomposition, multi-plan selection via tree search, and reflection) directly maps to strategies used in coding agent harnesses like SWE-bench solvers. The paper's discussion of fine-grained evaluation gaps and the need for step-wise metrics is directly relevant to designing evaluation frameworks for coding agents. The benchmark methodology and cost-performance analysis inform how to evaluate coding agent harnesses efficiently.
