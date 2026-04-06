# [2024] Qu — Tool Learning with Large Language Models: A Survey

## Metadata
- **arXiv:** 2405.17935
- **Venue:** Frontiers of Computer Science, 2024
- **Year:** 2024
- **Authors:** Changle Qu, Sunhao Dai, Xiaochi Wei, Hengyi Cai, Shuaiqiang Wang, Dawei Yin, Jun Xu, Ji-Rong Wen

## 1. Van de (Problem)
Tool learning with LLMs has emerged as a promising paradigm for augmenting LLM capabilities to tackle complex problems. However, the existing literature is fragmented and lacks systematic organization, posing barriers to entry for newcomers and making it difficult for researchers to understand the current state, methodologies, benchmarks, and open challenges in this rapidly growing field.

## 2. Dong co / Gap
While prior surveys cover LLMs, agents, reasoning, and retrieval-augmented generation, they do not extensively explore tool learning as a focused topic. Earlier foundational works by Mialon et al. (2023) and Qin et al. (2023) highlighted the promise of tools for LLMs, but the field has since seen rapid growth with many new studies. This survey provides a broader, more up-to-date, and systematically organized review covering both the "why" (benefits) and "how" (implementation) of tool learning, along with a comprehensive catalog of 33 benchmarks and evaluation methods.

## 3. Phuong phap (Method)
This is a survey paper. The authors systematically review 150+ papers and organize the literature along two primary dimensions:

**Why Tool Learning (6 benefits):**
1. Knowledge Acquisition (search engines, databases, knowledge graphs, weather/maps)
2. Expertise Enhancement (calculators, Python interpreters, domain-specific tools)
3. Automation and Efficiency (scheduling, reminders, project management, shopping)
4. Interaction Enhancement (multi-modal tools, machine translators, NLP tools)
5. Enhanced Interpretability and User Trust (transparent decision-making via tool traces)
6. Improved Robustness and Adaptability (reduced sensitivity to prompt variations)

**How Tool Learning (4-stage workflow):**
1. **Task Planning** -- intent understanding and task decomposition (tuning-free: CoT, ReACT, ART; tuning-based: Toolformer, TaskMatrix.AI, Toolink)
2. **Tool Selection** -- retriever-based (TF-IDF, BM25, Sentence-BERT, COLT) and LLM-based (CoT, ReACT, ToolLLaMA, AnyTool)
3. **Tool Calling** -- parameter extraction and API invocation (tuning-free: RestGPT, EasyTool; tuning-based: Gorilla, GPT4Tools)
4. **Response Generation** -- synthesizing tool outputs into user responses (direct insertion vs. information integration methods)

**Two Paradigms:** One-step task solving (plan everything upfront) vs. Iterative task solving (progressive interaction with tools based on feedback).

## 4. Dong gop chinh (Contributions)
- Provides the first comprehensive, systematically organized survey dedicated to tool learning with LLMs, reviewing 150+ papers.
- Establishes a clear taxonomy of the tool learning workflow into four stages (task planning, tool selection, tool calling, response generation) with sub-categories for each.
- Catalogs 33 benchmarks with detailed comparison (focus areas, tool counts, instance counts, executability, multi-tool support).
- Identifies 7 key challenges and future directions for the field.
- Maintains a living GitHub repository for tracking relevant papers and resources.

## 5. Diem manh (Strengths)
- Exceptionally thorough coverage: 150+ papers, 33 benchmarks, toolkits, and evaluation methods all in one place.
- Clear dual-axis organization ("why" and "how") makes the survey accessible to newcomers.
- Practical GPT-4 examples for each stage of the tool learning workflow help illustrate abstract concepts.
- The benchmark comparison table (Table 1) is an invaluable reference, covering focus areas, tool sources, executability, and dates.
- Identifies concrete, actionable future research directions (latency, evaluation, safety, unified frameworks, real-world benchmarks, multi-modal).

## 6. Han che (Limitations)
- As a survey, it does not introduce new methods or empirical results.
- The field is evolving so rapidly that the survey may quickly become outdated despite the living repository.
- Coverage is primarily focused on text-based tool learning; multi-modal tool learning (Section 6.7) is acknowledged as underexplored.
- Does not provide in-depth empirical comparison or meta-analysis across methods -- the review is largely qualitative.
- Some important subtopics (e.g., tool creation by LLMs, tool composition) receive relatively brief treatment.

## 7. Dataset & Metric
The survey catalogs 33 benchmarks including (selected highlights):
- **General**: API-Bank (73 tools, 314 instances), APIBench (1,645 tools, 16,450 instances), ToolBench1/2 (232/16,464 tools), MetaTool (199 tools), T-Eval (15 tools), ToolEyes (568 tools), AppWorld (457 tools)
- **Specialized**: ToolQA (13 tools), ToolEmu (311 tools), RoTBench (568 tools), SciToolBench (2,446 tools), StableToolBench (16,464 tools)

**Evaluation metrics by stage:**
- Task Planning: Tool Usage Awareness, Pass Rate, Accuracy
- Tool Selection: Recall@K, NDCG, COMP@K
- Tool Calling: Consistent with stipulations (parameter matching)
- Response Generation: BLEU, ROUGE-L, Exact Match

## 8. Ket qua chinh
As a survey, there are no novel experimental results. Key observations from the literature review include:
- Tuning-based methods generally outperform tuning-free methods but are limited to tools seen during training and face catastrophic forgetting.
- Tuning-free methods offer greater flexibility and compatibility across LLMs but struggle with prompt design.
- Current retrieval methods focus too much on semantic similarity and ignore hierarchical tool structure.
- Existing benchmarks suffer from quality issues (inaccessible/non-functional tools) and synthetic queries that may not reflect real user needs.
- Even GPT-4 shows poor resistance to noise and safety issues in tool learning contexts.

## 9. Keywords
Tool learning, survey, LLM agents, task planning, tool selection, tool calling, response generation, benchmarks, evaluation, API, retrieval-augmented generation

## 10. Lien quan den de tai
This survey is a foundational reference for "Coding Agent Harness & Evaluation": (1) The four-stage taxonomy (task planning, tool selection, tool calling, response generation) provides an organizing framework applicable to coding agent pipeline design; (2) The comprehensive benchmark catalog (33 benchmarks) directly informs what evaluation dimensions and metrics should be considered for coding agent benchmarks; (3) The identified challenges -- especially rigorous evaluation, unified frameworks, real-world benchmarks, and safety -- are directly relevant to designing robust coding agent evaluation harnesses; (4) The distinction between one-step and iterative task solving paradigms maps directly to coding agent architectures (single-pass vs. iterative debugging/refinement).
