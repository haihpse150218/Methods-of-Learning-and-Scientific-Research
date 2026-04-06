# [2023] Wu — AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation

## Metadata
- **arXiv:** 2308.08155
- **Venue:** ICLR 2024 (submitted Oct 2023)
- **Year:** 2023
- **Authors:** Qingyun Wu, Gagan Bansal, Jieyu Zhang, Yiran Wu, Beibin Li, Erkang Zhu, Li Jiang, Xiaoyun Zhang, Shaokun Zhang, Jiale Liu, Ahmed Awadallah, Ryen W. White, Doug Burger, Chi Wang

## 1. Van de (Problem)
Building complex LLM applications that require multi-agent cooperation is difficult due to the lack of a generic, flexible framework. Existing approaches are either single-agent (AutoGPT, LangChain Agents) or multi-agent but with static conversation patterns and limited capabilities (CAMEL, BabyAGI). Developers need a unified infrastructure that supports customizable agents, flexible conversation topologies, human involvement, and code execution.

## 2. Dong co / Gap
Prior multi-agent systems only support static conversation patterns (fixed topology regardless of input), lack code execution capability, and do not support human-in-the-loop interaction. There is no general-purpose infrastructure that combines all of these: flexible conversation patterns (static and dynamic), execution capability, tool usage, and configurable human involvement. AutoGen aims to fill this gap as a generic multi-agent conversation framework.

## 3. Phuong phap (Method)
AutoGen introduces two core concepts: (1) **Conversable Agents** -- generic agent abstractions that can be backed by LLMs, humans, tools, or combinations thereof. The base `ConversableAgent` class supports unified conversation interfaces (send, receive, generate_reply) and is specialized into `AssistantAgent` (LLM-backed) and `UserProxyAgent` (human/tool-backed). (2) **Conversation Programming** -- a paradigm for defining multi-agent workflows via two dimensions: *computation* (how agents generate responses) and *control flow* (the sequence/conditions of message passing). Control can be specified via natural language prompts, Python code, or a fusion of both. AutoGen also provides a `GroupChatManager` for dynamic multi-agent group chats with automatic speaker selection.

## 4. Dong gop chinh (Contributions)
- Open-source framework for building multi-agent LLM applications with customizable, conversable agents
- Conversation programming paradigm that unifies complex LLM workflows as multi-agent conversations with flexible control flow
- Support for both static and dynamic conversation patterns, including dynamic group chat with automatic speaker selection
- Demonstrated six diverse applications (math, RAG, decision-making, multi-agent coding, group chat, chess) showing versatility
- Reduced development effort significantly (e.g., OptiGuide code reduced from 430 to 100 lines)

## 5. Diem manh (Strengths)
- Highly modular and extensible design -- agents can be easily customized, reused, and composed
- Supports flexible human involvement (configurable modes: ALWAYS, NEVER, TERMINATE) enabling human-in-the-loop workflows
- Unified interface for combining LLMs, tools, and human inputs in a single framework
- Strong empirical results across diverse domains (math, QA, coding, decision-making, games)
- Practical impact: reduced development code and user interactions by 3-5x in OptiGuide application

## 6. Han che (Limitations)
- Early experimental stage; optimal agent topologies and conversation patterns not well understood
- Safety concerns with allowing agents to execute code and install packages in external environments
- No formal evaluation of scalability to large numbers of agents
- Dynamic group chat speaker selection relies on role-play prompting heuristics rather than principled methods
- Limited discussion on cost and token efficiency of multi-agent conversations

## 7. Dataset & Metric
- **MATH dataset** (Hendrycks et al., 2021): success ratio on 120 level-5 problems and full dataset
- **Natural Questions** (Kwiatkowski et al., 2019): F1 and Recall for QA tasks
- **ALFWorld** (Shridhar et al., 2021): average and best-of-3 success rate on 134 unseen tasks
- **OptiGuide** coding tasks: F1 score and Recall on 100 safe/unsafe coding tasks
- Compared against: ChatGPT+Code Interpreter, ChatGPT+Plugin, GPT-4, Multi-Agent Debate, LangChain ReAct

## 8. Ket qua chinh
- Math (MATH): AutoGen achieved 69.48% on 120 level-5 problems, outperforming ChatGPT+Code (52.5%), GPT-4 (45%), and others
- QA (Natural Questions): AutoGen achieved 66.65% F1 and 62.59% Recall with GPT-3.5, outperforming DPR baselines
- ALFWorld: 3-agent system (with grounding agent) achieved 77% average success, ~15% improvement over 2-agent system
- OptiGuide: Multi-agent design boosted F1 for identifying unsafe code by 8% (GPT-4) and 35% (GPT-3.5) over single-agent

## 9. Keywords
multi-agent systems, LLM framework, conversation programming, conversable agents, human-in-the-loop, code execution, dynamic group chat, AutoGen

## 10. Lien quan den de tai
Directly relevant as a foundational multi-agent framework for coding agents. AutoGen's conversable agent design and conversation programming paradigm provide the infrastructure layer for building coding agent harnesses. The multi-agent coding application (OptiGuide) demonstrates how agent roles (Writer, Safeguard, Commander) can be orchestrated for code generation and validation tasks. The framework's support for code execution, tool use, and flexible conversation patterns is essential for designing evaluation harnesses for coding agents.
