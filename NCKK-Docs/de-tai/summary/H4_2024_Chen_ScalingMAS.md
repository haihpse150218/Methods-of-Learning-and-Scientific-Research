# [2024] Shen — Small LLMs Are Weak Tool Learners: A Multi-LLM Agent (alpha-UMi)

## Metadata
- **arXiv:** 2401.07324
- **Venue:** Preprint (Feb 2024)
- **Year:** 2024
- **Authors:** Weizhou Shen, Chenliang Li, Hongzhan Chen, Ming Yan, Xiaojun Quan, Hehong Chen, Ji Zhang, Fei Huang

## 1. Van de (Problem)
LLM agents for tool learning must master multiple capabilities simultaneously -- task planning, tool selection/invocation, and result summarization. Training a single small open-source LLM to handle all these capabilities leads to performance limitations, as these abilities draw on different facets of LLMs (reasoning vs. accurate API calling vs. conclusion-drawing) and are difficult to optimize jointly in a capacity-constrained model.

## 2. Dong co / Gap
Conventional approaches focus on training a single LLM for all tool-use capabilities. However, small LLMs (e.g., LLaMA-7B) struggle to achieve peak performance across planning, calling, and summarizing simultaneously due to limited model capacity. Existing multi-agent frameworks (MetaGPT, ChatDev, AutoGen) rely on powerful closed-source LLMs and do not address the challenge of fine-tuning open-source small LLMs for multi-agent tool use. alpha-UMi fills this gap with a multi-LLM decomposition and a novel progressive fine-tuning strategy.

## 3. Phuong phap (Method)
The alpha-UMi framework decomposes the tool-learning task into three specialized LLM components: (1) **Planner** -- generates rationales and decides the next step (call tool, summarize, or give up). (2) **Caller** -- guided by the planner's rationale, generates the specific API call action. (3) **Summarizer** -- produces the final user-facing answer from the execution trajectory. Training uses **Global-to-Local Progressive Fine-Tuning (GLPFT)**: Stage 1 (global) fine-tunes a backbone LLM on the full dataset without distinguishing sub-tasks; Stage 2 (local) creates three copies of the backbone and fine-tunes each on its respective sub-task data with role-specific loss masking.

## 4. Dong gop chinh (Contributions)
- Demonstration that small LLMs are weak tool learners when trained as a single model, motivating multi-LLM decomposition
- alpha-UMi framework decomposing tool learning into planner, caller, and summarizer with specialized small LLMs
- GLPFT training strategy that bridges global task understanding and local role specialization
- alpha-UMi with 7B backbone outperforms Single-LLM with 13B backbone, showing cost-effectiveness
- Thorough analysis including data scaling laws and training dynamics explaining why the approach works

## 5. Diem manh (Strengths)
- Principled decomposition that reduces cognitive burden on each small LLM, enabling specialization
- GLPFT strategy effectively transfers global knowledge to local specialists, outperforming direct multi-task or one-stage alternatives
- 7B alpha-UMi outperforms 13B Single-LLM, demonstrating that smaller specialized models can beat larger general ones
- Inference time is similar to Single-LLM since sub-tasks are distributed without generating extra content
- Consistent improvement across all data scales, unlike Single-LLM which shows metric-specific optima at different scales

## 6. Han che (Limitations)
- 3x storage cost compared to Single-LLM (three copies of the backbone model)
- 1.3x training compute and 1.5x training time
- Not explored: combining small LLMs with powerful closed-source LLMs in a "large + small" hybrid
- Framework applicability beyond tool learning tasks not demonstrated
- Relies on existing benchmarks with ChatGPT/GPT-4 generated trajectories for training data

## 7. Dataset & Metric
- **ToolBench** (Qin et al., 2023b): Plan ACC, Action EM, Hallucination rate, Argument F1, Rouge-L; in-domain and out-of-domain splits; also real-time pass rate and win rate via RapidAPI
- **ToolAlpaca** (Tang et al., 2023): Process correctness (Proc.) and Answer correctness (Ans.) judged by GPT-4
- **MATH** and **GSM8K**: accuracy for mathematical reasoning (supplementary evaluation)
- Baselines: ChatGPT, GPT-4, ToolLLaMA, Single-LLM, Multi-LLM_one-stage, Single-LLM_multi-task

## 8. Ket qua chinh
- ToolBench (static, 7B): alpha-UMi achieves Plan ACC 88.92, Act. EM 58.94, Hallu. 0.57, far surpassing Single-LLM (81.92, 45.11, 2.32)
- ToolBench (static, 13B): alpha-UMi achieves Plan ACC 88.73, Act. EM 63.03, Hallu. 0.24
- ToolAlpaca: alpha-UMi (13B) achieves 41 Proc. and 35 Ans., matching or exceeding GPT-4 (41, 44)
- Real-time ToolBench: alpha-UMi (13B) achieves 72.2 pass rate and 67.7 win rate, competitive with GPT-4 (57.2/64.4 with ReACT, 64.8/64.3 with DFSDT)
- MATH: alpha-UMi 7B achieves 25.60 ACC vs Single-LLM 17.38; 13B achieves 28.54 vs 20.26
- GSM8K: alpha-UMi 7B achieves 49.73 vs Single-LLM 37.90

## 9. Keywords
tool learning, multi-LLM agent, small language models, fine-tuning, task decomposition, planner-caller-summarizer, progressive fine-tuning, API calling

## 10. Lien quan den de tai
Relevant to coding agent harness design through its demonstration of how to decompose agent capabilities into specialized components. The planner-caller-summarizer architecture maps to coding agent workflows where planning, code generation/execution, and result interpretation are distinct skills. The GLPFT training strategy provides insights for training smaller, specialized coding agents. The finding that specialized small models can outperform larger general ones has implications for cost-effective coding agent deployment and evaluation harness design.
