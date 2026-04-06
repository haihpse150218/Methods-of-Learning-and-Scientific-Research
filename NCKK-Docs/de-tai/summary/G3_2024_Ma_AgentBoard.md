# [2024] Ma — AgentBoard: An Analytical Evaluation Board of Multi-turn LLM Agents

## Metadata
- **arXiv:** 2401.13178
- **Venue:** NeurIPS 2024 (Datasets and Benchmarks Track)
- **Year:** 2024
- **Authors:** Chang Ma, Junlei Zhang, Zhihao Zhu, Cheng Yang, Yujiu Yang, Yaohui Jin, Zhenzhong Lan, Lingpeng Kong, Junxian He

## 1. Van de (Problem)
Evaluating LLM-based agents across diverse scenarios is difficult because existing benchmarks lack unified multi-round, partially-observable environments and rely solely on binary success rate as the evaluation metric. This coarse metric fails to capture incremental progress and obscures meaningful differences between models, especially when most agents achieve near-zero success rates on hard tasks.

## 2. Dong co / Gap
Prior benchmarks (AgentBench, GAIA, MINT, ToolEval, etc.) each miss at least one of four critical properties: task diversity, multi-round interaction, partially-observable environments, and fine-grained progress metrics. No existing benchmark combines all four with an analytical evaluation toolkit. AgentBoard is the first to satisfy all these criteria simultaneously.

## 3. Phuong phap (Method)
AgentBoard consists of:
1. **Unified Benchmark:** 9 diverse environments across 4 task categories (Embodied AI: AlfWorld, ScienceWorld, BabyAI; Game: Jericho, PDDL; Web: WebShop, WebArena; Tool: Tool-Query, Tool-Operation) with 1013 tasks total.
2. **Fine-grained Progress Rate Metric:** Tasks are decomposed into human-annotated subgoals. Progress rate tracks the fraction of subgoals achieved, providing a continuous metric that differentiates models even when success rates are similar or zero. Validated via user study (Pearson correlation > 0.95 with human judgments).
3. **Unified Reflex Agent Framework:** A simple act-only agent with sliding-window memory, modeled as a POMDP, that interacts with environments over multiple rounds.
4. **Analytical Evaluation Toolkit:** Open-source web panel (via Weights & Biases) supporting progress rate tracking, grounding accuracy analysis, long-range interaction analysis, sub-skill scoring (memory, planning, grounding, world modeling, self-reflection, spatial navigation), and trajectory visualization.

## 4. Dong gop chinh (Contributions)
- First comprehensive LLM agent benchmark combining task diversity, multi-round interaction, partial observability, fine-grained metrics, and analytical evaluation in a unified framework.
- Novel progress rate metric based on human-annotated subgoals, shown to be more discriminative than success rate.
- Large-scale evaluation of 20+ LLMs (proprietary and open-weight) revealing that GPT-4 dominates, code-trained models show stronger agentic abilities, and open-weight models struggle with multi-turn interaction.
- Sub-skill analysis framework decomposing agent abilities into 6 dimensions (memory, planning, grounding, world modeling, self-reflection, spatial navigation).
- Open-source toolkit with interactive visualization for detailed agent analysis.

## 5. Diem manh (Strengths)
- Progress rate is validated against human judgments with very high correlation, making it a credible alternative to binary success rate.
- Covers 9 environments spanning embodied AI, games, web, and tool use -- the broadest task coverage among agent benchmarks.
- Analytical toolkit enables deep investigation of failure modes beyond aggregate scores.
- Identifies actionable insights: code training improves agent performance; agent-specific instruction tuning (AgentLM, xLAM) yields further gains.
- All environments are unified into a consistent text-based interaction format.

## 6. Han che (Limitations)
- Relies on human-annotated subgoals, which is labor-intensive and subjective; does not scale easily to new tasks.
- Evaluates agents only in simulated environments; real-world benchmarking with variable ground truth and security concerns is left for future work.
- Uses a simplistic reflex agent framework; more sophisticated agent architectures (multi-agent, retrieval-augmented) are not benchmarked.
- Exclusively text-based; does not evaluate multi-modal agent capabilities.
- Progress rate metric requires environment-specific subgoal definitions, limiting generalizability.

## 7. Dataset & Metric
| Environment | Category | # Tasks | Metric |
|-------------|----------|---------|--------|
| AlfWorld | Embodied AI | 134 | Progress Rate (subgoal) + Success Rate |
| ScienceWorld | Embodied AI | 185 | Progress Rate (subgoal) + Success Rate |
| BabyAI | Embodied AI | 90 | Progress Rate (subgoal) + Success Rate |
| Jericho | Game | 72 | Progress Rate (subgoal) + Success Rate |
| PDDL | Game | 80 | Progress Rate (match) + Success Rate |
| WebShop | Web | 200 | Progress Rate (match) + Success Rate |
| WebArena | Web | 120 | Progress Rate (match) + Success Rate |
| Tool-Query | Tool | 92 | Progress Rate (subgoal) + Success Rate |
| Tool-Operation | Tool | 40 | Progress Rate (subgoal/match) + Success Rate |

Additional analyses: grounding accuracy, long-range interaction curves, sub-skill radar charts.

## 8. Ket qua chinh
- **GPT-4** leads with 70.0% average progress rate and 47.9% success rate across all tasks.
- **Progress rate is more discriminative than success rate:** e.g., Llama2-13b and Mistral-7b have similar ~2-4% success rates but progress rates differ meaningfully (18.9% vs. 24.6%).
- **Proprietary models outperform open-weight:** GPT-4 >> Claude2 >> GPT-3.5-Turbo; among open-weight, Llama3-70b and DeepSeek-67b lead.
- **Code-trained models show stronger agentic abilities:** CodeLlama-34b outperforms Llama2-70b by 6.2% in progress rate; Lemur-70b also benefits from code pretraining.
- **All models degrade significantly on hard tasks** (complex subgoal sequences).
- **Open-weight models plateau around step 6** in long-range interactions while GPT-4 maintains progress over 30+ steps.
- **Grounding accuracy:** GPT-4 achieves 85.6% average; open-weight models are substantially lower, with instruction tuning alone insufficient to boost agentic performance.

## 9. Keywords
LLM agent evaluation, benchmark, progress rate, multi-turn interaction, partially-observable environments, grounding accuracy, sub-skill analysis, AgentBoard

## 10. Lien quan den de tai
AgentBoard is directly relevant to "Coding Agent Harness & Evaluation" as it addresses the core challenge of how to evaluate agents beyond binary pass/fail. The progress rate metric (tracking subgoal completion) parallels the need for fine-grained evaluation of coding agents -- instead of just checking if a patch resolves an issue, one could track intermediate progress (file localization, test creation, partial fix). The sub-skill decomposition (planning, grounding, self-reflection, memory) maps to coding agent capabilities. The finding that code-trained models perform better as agents reinforces the importance of code-specific evaluation. The analytical toolkit design (visualization, trajectory analysis) provides a template for coding agent harness dashboards.
