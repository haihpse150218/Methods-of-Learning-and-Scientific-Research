# [2025] Raghavan — MOSAIC: Multi-agent Orchestration for Task-Intelligent Scientific Coding

## Metadata
- **arXiv:** 2510.08804
- **Venue:** arXiv preprint (cs.CL)
- **Year:** 2025
- **Authors:** Siddeshwar Raghavan, Tanwi Mallick

## 1. Van de (Problem)
Scientific code generation requires algorithms that are rigorous, interconnected with deep domain knowledge, and incorporate domain-specific reasoning -- unlike general-purpose coding. Existing LLM-based coding frameworks rely on sample test cases for verification and cannot handle chained subproblems across scientific domains (physics, chemistry, biology, mathematics, material science) where no I/O test cases are available.

## 2. Dong co / Gap
Current multi-agent coding frameworks (MapCoder, CodeSIM, AgentCoder) depend on validation I/O test cases to iteratively refine code, making them unsuitable for scientific coding benchmarks like SciCode where test cases are absent. Scientific problems also involve long chains of dependent subproblems where context must be preserved and errors can propagate, causing hallucinations when LLMs operate near their context limits.

## 3. Phuong phap (Method)
MOSAIC is a training-free, LLM-agnostic, four-agent framework structured as a student-teacher system inspired by knowledge distillation:

- **Bucketing Module:** Routes problems to the appropriate scientific domain.
- **Teacher Module:** Uses a Code Rationale Builder and Self-Reflection Agent on a small validation subset (<=5%) to produce domain-specific pseudocode as few-shot examples.
- **Student Module** with three agents:
  - **Rationale Agent:** Generates step-by-step reasoning plans using few-shot pseudocode, with a Consolidated Context Window (CCW) containing only function signatures and one-line summaries to prevent hallucination.
  - **Coding Agent:** Converts the rationale into executable code.
  - **Debugger Agent:** Performs up to k rounds of error correction in collaboration with the Coding Agent, resolving syntax and import errors.

## 4. Dong gop chinh (Contributions)
- Introduces MOSAIC, a training-free, LLM-agnostic multi-agent framework for scientific code generation that operates without validation I/O test cases.
- Designs and integrates four specialized agents (Self-Reflection, Rationale, Coding, Debugging) that collaboratively decompose problems, self-reflect, and maintain context across chained subproblems.
- Achieves up to 24% higher problem-solving accuracy over baselines on SciCode, and competitive results on MBPP/HumanEval/APPS.
- Ablation studies reveal each agent's contribution and demonstrate that careful orchestration is critical -- simply stacking components does not guarantee improvement.

## 5. Diem manh (Strengths)
- LLM-agnostic design works with GPT-4o, Claude Sonnet 4, Gemini 2.5 Flash, and open-source models without fine-tuning.
- The Consolidated Context Window (CCW) effectively mitigates hallucinations by limiting context to function signatures and summaries rather than full code history.
- Comprehensive ablation study clearly shows the contribution of each component.
- Addresses a real gap: scientific code generation where no test cases exist for iterative debugging.
- Shifts error distribution from syntactic errors (inexecutable code) to semantic errors, increasing executability from 54.3% to 71.8%.

## 6. Han che (Limitations)
- Relies on domain bucketing using keyword-based classification, which drops accuracy by 10-12% when automated.
- Performance on Biology domain remains consistently low across all backbones due to qualitatively different error types and sparse validation data.
- Struggles with very long problems (>10 subproblems) where context maintenance degrades even with CCW.
- Open-source models perform substantially worse (3x fewer main problems solved) than closed-source models, limiting accessibility.
- No semantic validation mechanism -- the Debugger Agent only addresses syntactic errors.

## 7. Dataset & Metric
- **Datasets:** SciCode (65 main problems, 283 subproblems across 5 scientific domains), MBPP (500 test), HumanEval (134 test), APPS (5000+ problems).
- **Metrics:** Number of correct main problems and subproblems solved (SciCode); percentage of test cases passed (MBPP, HumanEval, APPS).

## 8. Ket qua chinh
- On SciCode with GPT-4o: 12/65 main problems and 113/283 subproblems solved (vs. 7/65 and 94/283 for baseline), an 8.5% improvement and 24% over best alternative method.
- On MBPP: 84.90% (best among all methods). On HumanEval: 92.53% (second best after CodeSIM's 93.60%). On APPS: 24.71% (best).
- Consistent improvements across all three LLM backbones (GPT-4o, Claude Sonnet 4, Gemini 2.5 Flash).
- Open-source DeepSeek R1 (32B) achieved best open-source result: 4/65 main, 84/283 subproblems.

## 9. Keywords
Multi-agent framework, scientific code generation, LLM orchestration, knowledge distillation, self-reflection, context window management, SciCode benchmark

## 10. Lien quan den de tai
Highly relevant to "Coding Agent Harness & Evaluation." MOSAIC demonstrates a multi-agent architecture for code generation with specialized roles (planning, coding, debugging) -- directly paralleling the agent harness design pattern. Its evaluation on SciCode and general coding benchmarks provides methodology for benchmarking coding agents. The Consolidated Context Window (CCW) technique for managing context across chained tasks is applicable to any coding agent harness. The ablation study methodology for isolating agent contributions is a model for evaluating multi-agent coding systems.
