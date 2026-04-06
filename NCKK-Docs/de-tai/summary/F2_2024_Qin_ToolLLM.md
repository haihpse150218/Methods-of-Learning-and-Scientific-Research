# [2023] Qin — ToolLLM: Facilitating Large Language Models to Master 16000+ Real-world APIs

## Metadata
- **arXiv:** 2307.16789
- **Venue:** Preprint
- **Year:** 2023
- **Authors:** Yujia Qin, Shihao Liang, Yining Ye, Kunlun Zhu, Lan Yan, Yaxi Lu, Yankai Lin, Xin Cong, Xiangru Tang, Bill Qian, Sihan Zhao, Lauren Hong, Runchu Tian, Ruobing Xie, Jie Zhou, Mark Gerstein, Dahai Li, Zhiyuan Liu, Maosong Sun

## 1. Van de (Problem)
Open-source LLMs like LLaMA have achieved versatile capabilities through instruction tuning, but they remain significantly limited in tool-use capabilities compared to closed-source SOTA models like ChatGPT. Current instruction tuning focuses on basic language tasks and neglects the tool-use domain, leaving a large gap in the ability to interact with real-world APIs.

## 2. Dong co / Gap
Prior tool-learning datasets have three key limitations: (1) **Limited APIs** -- they either fail to involve real-world RESTful APIs or consider only a small scope; (2) **Constrained scenarios** -- existing works only handle single-tool instructions, whereas real tasks require multi-tool interplay; (3) **Inferior planning and reasoning** -- existing methods use CoT or ReACT which propagate errors and explore limited action spaces. Additionally, prior works often do not execute real API calls, missing crucial feedback for subsequent planning.

## 3. Phuong phap (Method)
- **ToolBench Dataset Construction** (3 stages): (i) Collect 16,464 real REST APIs from RapidAPI Hub spanning 49 categories, filtered from 53,190 to 3,451 high-quality tools; (ii) Use ChatGPT to generate diverse instructions covering single-tool (I1), intra-category multi-tool (I2), and intra-collection multi-tool (I3) scenarios (~200k qualified pairs); (iii) Annotate solution paths using ChatGPT with real API execution, producing 126,486 (instruction, solution path) pairs.
- **DFSDT (Depth-First Search-based Decision Tree)**: A novel reasoning strategy that expands the search space by building a decision tree. Unlike ReACT's linear chain, DFSDT allows the model to backtrack from failed paths and explore alternatives, significantly improving pass rates on complex multi-tool instructions.
- **ToolLLaMA**: Fine-tune LLaMA-2 7B on ToolBench instruction-solution pairs with extended context length (8192 via positional interpolation).
- **API Retriever**: A neural retriever (Sentence-BERT based) trained to recommend relevant APIs from the full 16k+ pool given an instruction, eliminating manual API selection.
- **ToolEval**: An automatic evaluator using ChatGPT with two metrics: pass rate and win rate. Achieves 87.1% agreement (pass rate) and 80.3% agreement (win rate) with human evaluation.

## 4. Dong gop chinh (Contributions)
- Created **ToolBench**, the largest and most comprehensive tool-use instruction tuning dataset with 16,464 real APIs, 126,486 instances, multi-tool scenarios, and real API call traces.
- Proposed **DFSDT**, a tree-based reasoning strategy that significantly outperforms ReACT by enabling backtracking and multi-path exploration.
- Developed **ToolEval**, a reliable automatic evaluator for tool-use capabilities with high human agreement.
- **ToolLLaMA** achieves comparable performance to ChatGPT on tool use and generalizes to unseen APIs and out-of-distribution domains (APIBench).
- Trained a neural **API retriever** that effectively selects relevant APIs from a pool of 16k+, sometimes finding better APIs than the ground truth set.

## 5. Diem manh (Strengths)
- Massive scale: 16,464 real-world REST APIs with actual execution, far exceeding prior benchmarks.
- DFSDT is a principled improvement over ReACT, achieving 63.8% average pass rate vs. 35.2% for ReACT on ChatGPT.
- ToolLLaMA generalizes remarkably to unseen instructions, unseen tools, and even unseen categories, and performs on par with ChatGPT.
- Strong OOD generalization: ToolLLaMA matches Gorilla on APIBench despite never training on those APIs.
- The entire pipeline (data construction, training, evaluation) is automated with minimal human supervision, making it scalable.

## 6. Han che (Limitations)
- Heavy reliance on ChatGPT for data generation, solution annotation, and evaluation -- introducing potential biases and cost.
- API reliability issues: RapidAPI endpoints can go offline or change, affecting reproducibility.
- DFSDT increases computational cost (more API calls per instruction) compared to ReACT.
- Only tested with LLaMA-2 7B; scaling behavior to larger models is unexplored.
- ToolEval still has ~13-20% disagreement with human evaluation.

## 7. Dataset & Metric
- **Dataset**: ToolBench -- 3,451 tools, 16,464 APIs from RapidAPI, 126,486 instruction-solution pairs across 3 scenarios (I1: single-tool, I2: intra-category multi-tool, I3: intra-collection multi-tool); 469,585 real API calls; avg 4.0 reasoning traces per instance.
- **Metrics**: Pass Rate (successful instruction completion), Win Rate (pairwise comparison against ChatGPT-ReACT baseline via ChatGPT evaluator).

## 8. Ket qua chinh
- **DFSDT vs ReACT** (on ChatGPT): DFSDT achieves 58.0/49.4/70.6 pass rate on I1/I2/I3 vs. 37.8/49.4/27.6 for ReACT.
- **ToolLLaMA + DFSDT**: Average pass rate 66.7%, win rate 60.6%, comparable to ChatGPT+DFSDT (64.8%, 64.3%) and outperforming Text-Davinci-003, Claude-2.
- **With API Retriever**: ToolLLaMA+DFSDT-Retriever achieves 67.3% pass rate, 63.1% win rate -- slightly improving over ground-truth API setting.
- **OOD on APIBench**: ToolLLaMA+our retriever achieves 16.77/51.16/40.59 AST accuracy on HuggingFace/TorchHub/TensorHub, outperforming Gorilla+BM25 on HuggingFace and TorchHub.

## 9. Keywords
Tool learning, API calls, instruction tuning, multi-tool reasoning, depth-first search, decision tree, ToolBench, ToolEval, LLaMA, RapidAPI, RESTful APIs

## 10. Lien quan den de tai
ToolLLM is highly relevant to "Coding Agent Harness & Evaluation" in multiple ways: (1) ToolBench provides a template for constructing large-scale tool-use benchmarks with real API execution; (2) DFSDT demonstrates how tree-search reasoning can improve agent decision-making, directly applicable to coding agent planning; (3) ToolEval offers an automated evaluation framework using LLM-as-judge with pass/win rate metrics, which can inform coding agent evaluation design; (4) The multi-tool, multi-step reasoning scenarios mirror real coding agent workflows that require orchestrating multiple tools sequentially.
