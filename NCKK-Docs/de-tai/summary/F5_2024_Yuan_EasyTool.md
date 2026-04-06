# [2024] Yuan — EasyTool: Enhancing LLM-based Agents with Concise Tool Instruction

## Metadata
- **arXiv:** 2401.06201
- **Venue:** Preprint
- **Year:** 2024
- **Authors:** Siyu Yuan, Kaitao Song, Jiangjie Chen, Xu Tan, Yongliang Shen, Kan Ren, Dongsheng Li, Deqing Yang

## 1. Van de (Problem)
LLM-based agents require understanding many tool functions from diverse tool documentations to use tools effectively. However, real-world tool documentation suffers from three critical issues -- inconsistency (different formats across sources), redundancy (excessive irrelevant information like URLs, IDs), and incompleteness (lack of usage examples and scenarios) -- which severely hinder LLMs' ability to select and invoke tools correctly.

## 2. Dong co / Gap
Existing approaches either fine-tune LLMs on tool-use data (which cannot extend to closed-source LLMs and lacks flexibility for new tools) or directly feed raw tool documentation into prompts (which wastes context with redundant information and fails with unusual tools). Naive prompt compression methods (e.g., LLMLingua) are unsuitable because they may remove essential parameters and function names. No prior work specifically addresses the quality of tool documentation as a first-class problem, despite it being a critical bottleneck affecting tool retrieval, selection, and execution.

## 3. Phuong phap (Method)
EasyTool is a two-stage framework that transforms raw tool documentation into concise, unified tool instructions:

**Stage 1 -- Tool Description Generation (Section 4.1):**
- Uses ChatGPT to rewrite verbose tool documentation into a concise description that retains only core functionality information.
- Eliminates irrelevant content (URLs, pricing, IDs) while preserving what each function does.
- Achieves 70.43% token reduction on ToolBench (2,530 -> 748 tokens) and 97.35% on RestBench (3,881 -> 103 tokens).

**Stage 2 -- Tool Functionality Guidelines Construction (Section 4.2):**
- Uses ChatGPT to generate structured usage scenarios with concrete parameter examples for each tool function.
- Output format: {"Scenario": description, "Parameters": {param: value}} for each function.
- Generated examples are verified by actually executing the tools to confirm parameter correctness.
- These guidelines serve as demonstrations to help LLMs understand when and how to use each tool.

The resulting tool instruction (description + guidelines) replaces raw documentation in the agent pipeline, applicable to any LLM in a plug-and-play manner.

## 4. Dong gop chinh (Contributions)
- First work to systematically identify and address the three deficiencies of tool documentation (inconsistency, redundancy, incompleteness) as a core bottleneck for LLM tool use.
- Proposed EasyTool, a simple yet effective framework that creates high-quality, unified tool instructions from heterogeneous documentation.
- Demonstrated significant token reduction (70-97%) while simultaneously improving tool-use performance.
- Showed that EasyTool is model-agnostic: it improves performance for ChatGPT, GPT-4, Vicuna-7B, Mistral-Instruct-7B, and ToolLLaMA-7B.
- Demonstrated that EasyTool-enhanced descriptions also improve tool retrieval quality (NDCG@1: 73.4 vs. 68.2 for BERT Retriever, and 76.7 avg vs. 75.0).

## 5. Diem manh (Strengths)
- Plug-and-play: requires no model training, works with both open-source and closed-source LLMs.
- Dramatic efficiency gains: 70%+ token reduction means more tools can fit in context and inference is cheaper.
- ChatGPT + DFSDT + EasyTool surpasses GPT-4 + DFSDT in success rate on ToolBench (52.8% vs. 15.0% average), demonstrating that better tool documentation matters more than a stronger base model.
- Enables previously non-functional models (Vicuna-7B, Mistral-7B score 0% with ReACT/DFSDT) to achieve meaningful performance (37-47% average) through better tool instructions alone.
- Error analysis shows EasyTool reduces tool name errors from 25% to 0% and parameter errors from 6% to 0% for ChatGPT.

## 6. Han che (Limitations)
- Only handles tool documentation that fits within ChatGPT's input limit; very long documentation requires preprocessing.
- Focuses on single-tool documentation; does not capture inter-tool dependencies that could improve multi-tool orchestration.
- Only works on models with instruction-following capability; cannot help models that fundamentally lack this ability.
- The quality of generated instructions depends on ChatGPT's understanding of the documentation, which may introduce errors for very specialized tools.
- Future work could explore training specialized models using EasyTool-generated instructions.

## 7. Dataset & Metric
- **Datasets**: (1) ToolBench (I2-Category: 200 test, I3-Instruction: 100 test) -- multi-tool real-world QA with RapidAPI tools; (2) RestBench (TMDB subset) -- 55 RESTful APIs for web service tasks; (3) FuncQA -- 13 arithmetic tools, 68 one-hop + 60 multi-hop math problems.
- **Metrics**: Pass Rate (instruction completion), Win Rate (pairwise vs. ChatGPT-ReACT), Success Rate (GPT-4 judges answer quality), NDCG@1/@5 (retrieval quality), Correct Path Rate CP% (RestBench), Accuracy with 0.1% tolerance (FuncQA), Tool Error Rate.

## 8. Ket qua chinh
- **ToolBench**: ChatGPT+DFSDT+EasyTool achieves 69.8% avg pass rate, 82.3% win rate, 52.8% success rate -- surpassing GPT-4+DFSDT (53.8/65.0/15.5%). With EasyTool-Retriever: 67.5/80.0/51.3%.
- **Token Reduction**: ToolBench 70.43% reduction (2,530->748), RestBench 97.35% reduction (3,881->103).
- **Retrieval**: EasyTool+GPT Ada achieves NDCG@1=73.4, NDCG@5=82.7 (avg 76.7/85.6), outperforming BERT Retriever (75.0/82.5).
- **RestBench**: EasyTool improves correct path rate by ~3-5% for both Vicuna-13B and ChatGPT-based RestGPT.
- **FuncQA**: ChatGPT+EasyTool achieves 91.66% one-hop and 48.53% multi-hop accuracy with only 2.34% error rate, vs. ReACT's 41.17% and 9.38%.
- **Error Reduction**: ChatGPT name errors 25%->0%, parameter errors 6%->0%; GPT-4 name errors 17%->0%, parameter errors 5%->1%.

## 9. Keywords
Tool documentation, tool instruction, prompt engineering, token reduction, LLM agents, tool utilization, plug-and-play, ToolBench, RestBench, concise instructions

## 10. Lien quan den de tai
EasyTool is relevant to "Coding Agent Harness & Evaluation" in several ways: (1) It demonstrates that the quality of tool/API documentation is a critical factor in agent performance -- directly applicable to designing coding agent harnesses where tool descriptions must be clear and standardized; (2) The 70%+ token reduction approach enables fitting more tools into limited context windows, important for coding agents with many available commands/tools; (3) The finding that better tool instructions can make a weaker model outperform a stronger one (ChatGPT+EasyTool > GPT-4) suggests that harness design (how tools are presented) can matter more than model capability; (4) The unified instruction format provides a template for standardizing tool interfaces in coding agent evaluation frameworks.
