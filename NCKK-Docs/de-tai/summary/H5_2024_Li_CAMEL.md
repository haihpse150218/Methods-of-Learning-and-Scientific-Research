# [2023] Li — CAMEL: Communicative Agents for "Mind" Exploration of Large Language Model Society

## Metadata
- **arXiv:** 2303.17760
- **Venue:** NeurIPS 2023
- **Year:** 2023
- **Authors:** Guohao Li, Hasan Abed Al Kader Hammoud, Hani Itani, Dmitrii Khizbullin, Bernard Ghanem

## 1. Van de (Problem)
Chat-based LLMs have achieved remarkable progress in complex task-solving, but their success heavily relies on human input to guide conversations, which is challenging, time-consuming, and sometimes impossible for non-domain experts. The key question is whether autonomous communicative agents can replace human intervention to steer conversations toward task completion with minimal supervision.

## 2. Dong co / Gap
Existing approaches require extensive human prompting to guide LLM conversations. There is no scalable framework for studying autonomous cooperation between communicative agents. Several challenges arise when agents cooperate autonomously: role flipping, assistant repeating instructions, flake replies, and infinite loops of messages. CAMEL addresses these through a role-playing framework with inception prompting that requires only a preliminary idea from humans.

## 3. Phuong phap (Method)
CAMEL proposes a **role-playing** framework with three key components: (1) **Task Specification** -- a human provides an idea and selects roles; a task specifier agent elaborates the idea into a concrete, detailed task description. (2) **Inception Prompting** -- carefully designed system prompts for both the AI assistant and AI user that establish roles, communication protocols, constraints (no role flipping, no questions from assistant), output format (always start with "Solution:"), and termination conditions (CAMEL_TASK_DONE token). (3) **Instruction-following Cooperation** -- the AI user gives step-by-step instructions and the AI assistant provides solutions, iterating until task completion. An optional **Critic-in-the-Loop** mechanism allows an AI or human critic to provide feedback for tree-search-like decision-making.

## 4. Dong gop chinh (Contributions)
- Novel role-playing cooperative agent framework requiring minimal human intervention (just an idea and role selection)
- Inception prompting technique that autonomously guides multi-agent conversations toward task completion
- Scalable approach for generating large conversational datasets (25,000 AI Society conversations, Code dataset)
- Identification of key challenges in autonomous cooperation: role flipping, repeating instructions, flake replies, infinite loops
- Demonstration of knowledge emergence through progressive fine-tuning of LLaMA on generated datasets
- Open-source library with agents, data pipelines, and analysis tools

## 5. Diem manh (Strengths)
- Minimal human involvement -- only requires an initial idea, not step-by-step guidance
- Scalable data generation: automatically creates diverse conversational instruction-following datasets
- CAMEL agents outperform single-shot gpt-3.5-turbo by large margins (76.3% vs 10.4% in human eval, 73-76% vs 23-24% in GPT4 eval)
- Knowledge emergence study demonstrates progressive capability building through dataset fine-tuning
- CAMEL-7B achieves competitive HumanEval scores (14.0 pass@1) vs LLaMA-7B (10.5) and Vicuna-7B (11.0)

## 6. Han che (Limitations)
- Only supports static two-agent conversation pattern (assistant-user), not flexible multi-agent topologies
- Does not natively support tool usage or code execution -- agents only generate text/code without running it
- Role flipping and infinite loops still occur despite prompt engineering safeguards
- Evaluation is primarily qualitative (human/GPT4 preference) rather than on standardized benchmarks
- Limited to cooperative settings; competitive or mixed settings not explored

## 7. Dataset & Metric
- **AI Society dataset**: 25,000 conversations (50 assistant roles x 50 user roles x 10 tasks); evaluated via human preference and GPT4 preference against single-shot gpt-3.5-turbo
- **Code dataset**: 100 tasks evaluated via GPT4 preference
- **Math and Science datasets**: single-turn QA for knowledge emergence study
- **HumanEval and HumanEval+**: pass@k for code generation (k=1, k=100) on CAMEL-7B (LLaMA fine-tuned)
- **Knowledge Emergence**: GPT4-based evaluation of progressive fine-tuning across domains

## 8. Ket qua chinh
- AI Society (Human Eval): CAMEL wins 76.3%, gpt-3.5-turbo wins 10.4%, draw 13.3%
- AI Society (GPT4 Eval): CAMEL wins 73.0%, gpt-3.5-turbo wins 23.0%, draw 4.0%
- Code (GPT4 Eval): CAMEL wins 76.0%, gpt-3.5-turbo wins 24.0%, draw 0.0%
- Knowledge Emergence: progressive fine-tuning on AI Society -> Code -> Math -> Science shows consistent improvement
- HumanEval: CAMEL-7B achieves 14.0% pass@1 and 57.9% pass@100, outperforming base LLaMA-7B and Vicuna-7B

## 9. Keywords
role-playing, inception prompting, communicative agents, autonomous cooperation, instruction following, conversational data generation, multi-agent systems, AI society

## 10. Lien quan den de tai
Relevant to coding agent harness and evaluation as an early and influential framework for autonomous multi-agent cooperation. The role-playing paradigm (AI user as task planner, AI assistant as executor) maps directly to coding agent interaction patterns. The Code scenario demonstrates collaborative code generation through conversation. The identified challenges (role flipping, infinite loops, flake replies) are critical failure modes that coding agent evaluation harnesses must detect and handle. The inception prompting design provides templates for structuring agent behavior in coding tasks. However, CAMEL lacks code execution and tool use, which limits its direct applicability to coding agent harnesses compared to later frameworks like AutoGen and MetaGPT.
