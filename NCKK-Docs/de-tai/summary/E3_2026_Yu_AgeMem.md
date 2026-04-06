# [2026] Yu — Agentic Memory (AgeMem): Learning Unified Long-Term and Short-Term Memory Management for LLM Agents

## Metadata
- **arXiv:** 2601.01885v1
- **Venue:** arXiv preprint (cs.CL)
- **Year:** 2026
- **Authors:** Yi Yu, Liuyi Yao, Yuexiang Xie, Qingquan Tan, Jiaqi Feng, Yaliang Li, Libing Wu

## 1. Van de (Problem)
LLM agents face fundamental limitations in long-horizon reasoning due to finite context windows. Existing memory systems treat long-term memory (LTM) and short-term memory (STM) as separate, loosely coupled modules managed by heuristics or auxiliary controllers, which limits adaptability and prevents end-to-end optimization of unified memory management.

## 2. Dong co / Gap
Three key challenges remain unaddressed: (C1) Functional heterogeneity coordination -- LTM and STM serve complementary but distinct purposes (storage vs. context management) and no existing system orchestrates them synergistically. (C2) Training paradigm mismatch -- RL frameworks assume continuous trajectories with stable rewards, but memory operations produce fragmented, discontinuous experiences with sparse rewards. (C3) Practical deployment constraints -- many agent memory systems rely on auxiliary expert LLMs for memory control, increasing inference cost and training complexity. No prior work integrates unified memory management directly into the agent's policy via learnable, end-to-end RL training.

## 3. Phuong phap (Method)
AgeMem exposes memory operations as tool-based actions within the agent's policy:
- **LTM tools:** ADD (store new knowledge), UPDATE (modify entries), DELETE (remove entries)
- **STM tools:** RETRIEVE (fetch from LTM to context), SUMMARY (compress context), FILTER (remove irrelevant segments)

**Three-stage progressive RL training:**
- **Stage 1 (LTM construction):** Agent is exposed to contextual information in a casual conversational setting and learns to store salient information into LTM
- **Stage 2 (STM control under distractors):** Context is reset; agent is presented with distractors and learns to use SUMMARY and FILTER to manage context efficiently
- **Stage 3 (Integrated reasoning):** Agent receives a formal query requiring coordinated use of both LTM retrieval and STM management to produce answers

**Step-wise GRPO:** A variant of Group Relative Policy Optimization that broadcasts the terminal reward to all preceding steps in the trajectory, enabling long-range credit assignment across the three heterogeneous stages.

**Composite reward function:** R = w_task * R_task + w_context * R_context + w_memory * R_memory + P_penalty, covering task completion (LLM-judge), context efficiency, and memory quality.

## 4. Dong gop chinh (Contributions)
- Propose AgeMem, the first unified framework that jointly manages LTM and STM through learnable tool-based actions integrated into the agent's policy
- Design a three-stage progressive RL strategy with step-wise GRPO to handle sparse/discontinuous rewards from memory operations
- Demonstrate consistent improvements over strong baselines (LangMem, A-Mem, Mem0, Mem0^g) across five long-horizon benchmarks and two LLM backbones
- Show that RL training produces higher-quality long-term memories (MQ scores of 0.533 and 0.605 vs baselines avg ~0.5)
- Validate through ablation that each component (LTM, STM, RL) contributes progressively, with the full system achieving +13.9% to +21.7% over no-memory baselines

## 5. Diem manh (Strengths)
- First work to unify LTM and STM management in a single learnable framework, replacing heuristic pipelines with end-to-end optimization
- Principled RL training strategy (three-stage progressive + step-wise GRPO) that addresses the fundamental challenge of sparse, discontinuous rewards in memory operations
- Evaluated on diverse benchmarks spanning embodied action (ALFWorld), game reasoning (SciWorld), planning (PDDL), grounded language (BabyAI), and knowledge QA (HotpotQA)
- Thorough ablation study demonstrating the progressive contribution of LTM, RL, and STM components
- Trained only on HotpotQA but transfers well to all five benchmarks, demonstrating generalization

## 6. Han che (Limitations)
- Uses a fixed set of 6 memory management tools; more fine-grained control operations could be explored
- Evaluated only on Qwen2.5-7B-Instruct and Qwen3-4B-Instruct; generalization to larger models or different architectures is unknown
- RL training is computationally expensive (requires generating K rollouts per task instance across 3 stages)
- Relies on an LLM-based judge for task reward and memory quality evaluation, introducing potential bias
- Broader coverage of tasks and environments would strengthen empirical understanding

## 7. Dataset & Metric
- **Datasets:** ALFWorld (embodied action), SciWorld (game-based reasoning), PDDL (planning), BabyAI (grounded language), HotpotQA (multi-hop QA)
- **Metrics:** Success Rate (SR) for ALFWorld/SciWorld/BabyAI, Progress Rate (PR) for PDDL, LLM-as-a-Judge (J) for HotpotQA, Memory Quality (MQ) via LLM-based evaluator

## 8. Ket qua chinh
- AgeMem with Qwen2.5-7B achieves average 41.96% across 5 benchmarks (vs best baseline Mem0 at 37.14%, A-Mem at 36.78%, no-memory at 28.05%)
- AgeMem with Qwen3-4B achieves average 54.31% (vs best baseline Mem0 at 44.70%)
- Relative gains of 49.59% (Qwen2.5) and 23.52% (Qwen3) over no-memory baselines
- RL training contributes 8.53-8.72 percentage points improvement over AgeMem-noRL
- Memory Quality: AgeMem achieves MQ=0.533 (Qwen2.5) and MQ=0.605 (Qwen3), highest among all methods
- STM management reduces token usage by 3.1-5.1% compared to RAG-based STM approaches
- Ablation: Full system (+LT/ST/RL) achieves +13.9% (ALFWorld), +21.7% (SciWorld), +16.1% (HotpotQA) over no-memory baseline

## 9. Keywords
Agentic memory, unified memory management, long-term memory, short-term memory, reinforcement learning, GRPO, tool-based actions, LLM agents, long-horizon reasoning

## 10. Lien quan den de tai
**Relevance to "Coding Agent Harness & Evaluation":** AgeMem is highly relevant as it addresses the core challenge of how coding agents should manage memory across long task horizons. The unified LTM+STM framework maps directly to coding agent needs: LTM for persisting knowledge about codebases, past solutions, and user preferences; STM for managing the active context window during complex multi-file edits. The tool-based memory interface (ADD, UPDATE, DELETE, RETRIEVE, SUMMARY, FILTER) provides a concrete design pattern for coding agent harnesses. The RL-based training strategy for learning when and how to use memory tools could be applied to train coding agents to make better decisions about what context to retain or discard. The evaluation across diverse task types demonstrates the kind of cross-domain benchmarking relevant for coding agent evaluation.
