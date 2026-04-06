# [2023] Patil — Gorilla: Large Language Model Connected with Massive APIs

## Metadata
- **arXiv:** 2305.15334
- **Venue:** Preprint (under review)
- **Year:** 2023
- **Authors:** Shishir G. Patil, Tianjun Zhang, Xin Wang, Joseph E. Gonzalez

## 1. Van de (Problem)
LLMs have difficulty effectively using tools via API calls, largely due to their inability to generate accurate input arguments and their tendency to hallucinate wrong API usage. Existing approaches only consider a small, well-documented set of APIs that can be easily injected into the prompt, making it infeasible to scale to the vast space of real-world, changing cloud APIs.

## 2. Dong co / Gap
Prior work on integrating tools into LLMs focused on a small number of hand-coded tools with simple prompting strategies. However, in the real world there are potentially millions of changing APIs with overlapping functionality, nuanced limitations, and constraints. Current LLMs (GPT-4, Claude, etc.) hallucinate non-existent APIs or pick incorrect libraries when prompted to make API calls. No systematic fine-tuning and evaluation pipeline existed for large-scale API usage.

## 3. Phuong phap (Method)
- **APIBench**: Constructed a comprehensive benchmark by scraping API documentation (model cards) from three major ML model hubs: TorchHub (94 APIs), TensorFlow Hub (626 APIs), and HuggingFace (925 APIs) -- totaling 1,645 APIs. Each API is converted to a structured JSON format.
- **Instruction Generation**: Used GPT-4 with Self-Instruct to generate 10 synthetic user-question prompts per API, producing 16,450 (instruction, API) pairs.
- **Gorilla Model**: Fine-tuned LLaMA-7B on these instruction-API pairs using standard instruction fine-tuning. Trained in two modes: zero-shot and retriever-aware (appending retrieved API documentation to the prompt during training).
- **AST Sub-Tree Matching**: Proposed a novel evaluation metric that parses generated API calls into ASTs and checks if the candidate call is a functional sub-tree of the reference API call, handling default arguments and multiple valid solutions.

## 4. Dong gop chinh (Contributions)
- Introduced **APIBench**, one of the most comprehensive API call benchmarks for ML, covering 1,645 APIs across three hubs.
- Released **Gorilla**, a fine-tuned LLaMA-7B that surpasses GPT-4 in API call accuracy while substantially reducing hallucination.
- Proposed **retriever-aware training**, enabling the model to adapt to test-time changes in API documentation without retraining.
- Developed **AST sub-tree matching** as a principled evaluation metric for functional correctness of generated API calls.
- Demonstrated that Gorilla can reason about API constraints (e.g., parameter size, accuracy thresholds).

## 5. Diem manh (Strengths)
- Gorilla (7B params) outperforms GPT-4 in zero-shot API call accuracy by 20.43% and reduces hallucination to near zero on some benchmarks.
- Retriever-aware training elegantly solves the problem of adapting to evolving API documentation at test time.
- AST-based evaluation is more robust than string matching for assessing functional correctness of API calls.
- The benchmark and model are fully open-sourced, enabling reproducibility.
- Practical system with both zero-shot and retrieval inference modes.

## 6. Han che (Limitations)
- Dataset is limited to ML APIs (TorchHub, TensorFlow Hub, HuggingFace); generalization to RESTful APIs and other domains is not evaluated.
- ML APIs have high functional similarity, which may bias predictions and disadvantage certain sub-groups.
- Adding non-optimal retrievers (BM25, GPT-Index) at test time can significantly hurt performance (up to 52% accuracy degradation), indicating sensitivity to retriever quality.
- Only single API calls are evaluated; multi-step API compositions or chaining are not addressed.
- LLaMA-7B base model limits reasoning capability compared to larger models.

## 7. Dataset & Metric
- **Dataset**: APIBench -- 1,645 APIs from TorchHub (94), TensorFlow Hub (626), HuggingFace (925); 16,450 instruction-API pairs; split 80/20 (Torch/TensorFlow) and 90/10 (HuggingFace) for train/test.
- **Metrics**: AST sub-tree matching accuracy, hallucination rate (API call not matching any API in the database), error rate (wrong API selected).

## 8. Ket qua chinh
- **Zero-shot**: Gorilla achieves 59.13% (TorchHub), 71.68% (HuggingFace), 83.79% (TensorFlow) overall accuracy, outperforming GPT-4 (38.70%, 19.80%, 18.20%) by large margins.
- **With GPT-Index retriever**: Gorilla achieves 61.82% (TorchHub), 47.46% (HuggingFace), 64.96% (TensorFlow).
- **Hallucination**: Gorilla zero-shot achieves 6.98% hallucination on TorchHub vs. GPT-4's 36.55%; near-zero hallucination with retriever on some benchmarks.
- **Constraints**: Gorilla matches or outperforms GPT-3.5 on constraint-aware API selection with the highest zero-shot accuracy (47.88%).

## 9. Keywords
API calls, tool use, LLM fine-tuning, retrieval-augmented generation, hallucination reduction, AST matching, APIBench, LLaMA, self-instruct

## 10. Lien quan den de tai
Gorilla directly addresses the core challenge of enabling LLMs to select and invoke the correct tool/API from a massive set -- a foundational capability for any Coding Agent. The retriever-aware training paradigm is relevant for building agent harnesses that must adapt to evolving tool landscapes. The AST sub-tree matching evaluation metric provides a principled approach for evaluating code generation correctness in agent benchmarks. The work's focus on reducing hallucination in tool invocation is critical for reliable coding agent evaluation.
