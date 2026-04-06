# [2024] Du — AnyTool: Self-Reflective, Hierarchical Agents for Large-Scale API Calls

## Metadata
- **arXiv:** 2402.04253
- **Venue:** Preprint
- **Year:** 2024
- **Authors:** Yu Du, Fangyun Wei, Hongyang Zhang

## 1. Van de (Problem)
Effectively utilizing a vast collection of 16,000+ real-world APIs to address diverse user queries is extremely challenging. Existing approaches like ToolLLM use a two-phase retrieve-then-solve pipeline, but the retrieval phase suffers from low accuracy and lacks feedback mechanisms, often leading to unresolved queries due to incorrect API candidates being provided to the solver.

## 2. Dong co / Gap
Prior work (ToolLLM) employs a trained neural API retriever that may overlook truly relevant APIs and provides no mechanism to recover from retrieval errors. Additionally, the evaluation protocol in ToolBench has a significant flaw: when the API retriever selects completely unrelated APIs, GPT-4 labels queries as "non-solvable," which inflates pass rates artificially (up to 99% with random API selection). AnyTool addresses both the retrieval limitation and the evaluation flaw. Furthermore, integrating all 16K+ APIs into a single LLM context exceeds the maximum context length, even for GPT-4-128K.

## 3. Phuong phap (Method)
- **Hierarchical API Retriever**: A three-tier agent structure mirroring RapidAPI's organization: (1) Meta-agent selects relevant categories, (2) Category agents identify relevant tools within categories, (3) Tool agents select specific APIs and add them to an API-candidate pool. Each agent type has its own function set, and agents operate independently in a multi-threaded manner.
- **Solver**: Uses the API-candidate pool to resolve the user query via GPT-4's function calling feature. Implements either DFSDT or CoT reasoning, with a "finish" function that can yield "Give Solution," "Try Backtrack," or "Give Up."
- **Self-Reflection Mechanism**: A closed-loop process that re-activates AnyTool when the initial solution fails. It identifies failure reasons, incorporates them into historical context, and re-activates agents in ascending order (tool -> category -> meta-agent) to discover new APIs. The solver is then re-run with the expanded API-candidate pool. Only 4-6 iterations needed for up to 20% improvement.
- **Revised Evaluation Protocol**: Bypasses the solvability check step entirely; directly evaluates whether the agent's solution resolves the query (R = Solved / (Solved + Unsolved)), after manually filtering non-solvable queries from the benchmark.
- **AnyToolBench**: A new benchmark of 400 instances constructed by having GPT-4 explore the API pool, generate queries based on actual API responses, and verify solutions.

## 4. Dong gop chinh (Contributions)
- Introduced a **plug-and-play** hierarchical agent system requiring no training, powered entirely by GPT-4's function calling.
- Designed a **three-tier hierarchical API retriever** that leverages RapidAPI's structure to efficiently navigate 16K+ APIs within context length limits.
- Proposed a **self-reflection mechanism** that creates a closed-loop system, enabling recovery from both retrieval and solving failures.
- Identified and corrected a **flaw in ToolBench's evaluation protocol** that artificially inflated pass rates, and proposed a more rigorous alternative.
- Created **AnyToolBench**, a new benchmark that better reflects practical application scenarios.

## 5. Diem manh (Strengths)
- No training required -- entirely relies on GPT-4 function calling, making it immediately deployable ("plug-and-play").
- Outperforms ToolLLM by +35.4% average pass rate on filtered ToolBench and achieves 73.8% on AnyToolBench vs. ToolLLM's 18.9%.
- Self-reflection provides principled error recovery, with performance saturating at only 4-6 iterations.
- The hierarchical structure elegantly solves the context length problem when dealing with 16K+ APIs.
- Thorough ablation studies validating each component (hierarchy, self-reflection, DFSDT, pool size, agent count).

## 6. Han che (Limitations)
- Heavy reliance on GPT-4 -- high cost (avg 13.5x10^4 tokens, 43.3 API calls per query) and latency tied to GPT-4's server stability.
- Performance in "extremely complex scenarios" has not been verified due to lack of appropriate datasets.
- Cannot be deployed locally since it depends on GPT-4's function calling feature.
- Self-reflection adds computational overhead (avg 4.6 self-reflection rounds per query).
- The approach inherits GPT-4's limitations in reasoning and factual accuracy.

## 7. Dataset & Metric
- **Datasets**: (1) Filtered ToolBench -- 6 subsets (G1-I/T/C, G2-I/C, G3-I) with 115-142 queries each after removing non-solvable queries; (2) AnyToolBench -- 400 instances created from actual API responses.
- **Metric**: Revised pass rate R = #(Solved) / (#(Solved) + #(Unsolved)), evaluated by GPT-4-32K. Human-GPT-4 correlation: 96.5%.

## 8. Ket qua chinh
- **Filtered ToolBench**: AnyTool achieves 58.2% average pass rate vs. ToolLLM's best at 25.6% and GPT-4+DFSDT at 38.9%.
- **AnyToolBench**: AnyTool achieves 73.8% vs. ToolLLM (18.9%), ToolLLM+GPT-4 solver (36.6%), and GPT-4 plain agent (14.0%).
- **Ablation**: Removing hierarchical structure drops pass rate by ~36-47 points; removing self-reflection drops by ~39-47 points; replacing DFSDT with CoT drops by ~8 points.
- **Original ToolBench**: AnyTool achieves 44.8% average vs. ToolLLM's 20.4% and ToolLLM+GPT-4's 32.2%.

## 9. Keywords
Hierarchical agents, self-reflection, API retrieval, function calling, GPT-4, tool utilization, large-scale APIs, ToolBench, divide-and-conquer, closed-loop reasoning

## 10. Lien quan den de tai
AnyTool is directly relevant to "Coding Agent Harness & Evaluation" through: (1) Its hierarchical agent architecture demonstrates how to manage large tool spaces efficiently -- applicable to coding agents with many available tools/commands; (2) The self-reflection mechanism provides a template for building self-correcting agent harnesses; (3) The identification and correction of evaluation protocol flaws in ToolBench highlights the critical importance of rigorous evaluation design; (4) The plug-and-play, training-free approach shows how powerful agents can be built purely through prompt engineering and function calling, relevant to harness design.
