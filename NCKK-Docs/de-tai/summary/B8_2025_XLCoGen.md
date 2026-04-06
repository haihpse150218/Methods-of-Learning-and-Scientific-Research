# [2025] Moumoula — Beyond Language Barriers: Multi-Agent Coordination for Multi-Language Code Generation (XL-CoGen)

## Metadata
- **arXiv:** 2509.19918
- **Venue:** arXiv preprint (cs.SE)
- **Year:** 2025
- **Authors:** Micheline Benedicte Moumoula, Serge Lionel Nikiema, Alberick Euraste Djire, Abdoul Kader Kabore, Jacques Klein, Tegawende F. Bissyande

## 1. Van de (Problem)
LLMs exhibit substantial performance disparities across programming languages, with high-resource languages like Python and JavaScript achieving far superior code generation quality compared to lower-resource languages such as Rust, Perl, OCaml, and Erlang. This disparity stems from imbalanced training data, varying language complexity, and differences in language popularity. Existing multi-agent code generation frameworks focus exclusively on single-language (typically Python) contexts.

## 2. Dong co / Gap
Current multi-agent approaches (AgentCoder, MapCoder, CodeCoR) have not been systematically extended to cross-language scenarios. Translation-based approaches like LANTERN focus on code repair rather than generation from scratch. LLM-based intermediate language selection is biased toward high-performing languages like Python regardless of actual translation compatibility with the target language, leading to suboptimal cross-language transfer. No existing framework systematically leverages cross-language knowledge transfer using empirically validated transfer matrices.

## 3. Phuong phap (Method)
XL-CoGen is a structured three-stage multi-agent methodology:

- **Stage 1 -- Initial Code Generation and Validation:** Prompt adaptation (language-agnostic terminology), test case standardization (JSON format with type annotations), code generation in the target language, and validation through test execution.
- **Stage 2 -- Cross-Language Generation and Transfer:** When Stage 1 fails, the system selects the top-3 intermediate languages using an empirically-derived transfer matrix (based on standalone generation reliability and cross-language translation success rates, not LLM intuition). It generates code in each intermediate language, validates it, then back-translates to the target language.
- **Stage 3 -- Language-Specific Error Correction and Refinement:** A bug analysis agent diagnoses root causes (code logic, test case formatting, component interactions), then a code repair agent and test repair agent iteratively fix issues with a single retry iteration.

## 4. Dong gop chinh (Contributions)
- A structured multi-stage approach combining initial generation, strategic intermediate language selection, and iterative error correction for cross-language code generation.
- A data-driven cross-language transfer matrix methodology that empirically identifies optimal intermediate languages based on demonstrated translation success rather than LLM heuristics.
- Up to 13 percentage-point gains over the strongest fine-tuned baseline and up to 30 percentage points over single-language multi-agent methods.
- Demonstrates that XL-CoGen significantly outperforms language-specific fine-tuning (77.2% vs. 68.1% baseline and 58-64.3% for fine-tuned variants on Rust).
- Ablation study showing Stage 2 (cross-language transfer) is the critical enabler, providing the knowledge foundation for Stage 3 refinement.

## 5. Diem manh (Strengths)
- Data-driven transfer matrix eliminates LLM bias toward popular languages, achieving up to 9.7 percentage-point gains over LLM-based language selection for Erlang.
- Consistent improvements across both high-performing (10-14 pp) and low-performing languages (24-29 pp), substantially narrowing the cross-language performance gap.
- Outperforms domain-specific fine-tuning without any training, preserving general problem-solving capabilities.
- Each stage builds upon previous artifacts rather than discarding them, creating cumulative knowledge transfer.
- Works with both closed-source (GPT-4.1-mini) and open-source (DeepSeek-V3) models.

## 6. Han che (Limitations)
- Limited to single retry iteration in Stage 3 for computational efficiency, potentially leaving additional improvements on the table.
- Transfer matrix is pre-computed from benchmark data and may not generalize to all problem domains or newer languages.
- Evaluated only on MBPP-dedup (~974 tasks), a relatively simple benchmark; performance on more complex tasks (e.g., repository-level) is unknown.
- Some languages like Rust still show high compilation failure rates (22.9% for DeepSeek-V3) even after full pipeline.
- Only two LLM backbones evaluated (GPT-4.1-mini and DeepSeek-V3).

## 7. Dataset & Metric
- **Datasets:** MBPP-dedup (~974 tasks) for primary evaluation; Oxen.ai Rust dataset (16,500 samples from Ace-Code-87k) for fine-tuning comparison; BabelCode-MBPP for cross-language evaluation across 17 programming languages.
- **Metrics:** Pass@1 (percentage of problems where generated solutions pass all test cases); semantic code validity evaluation categorizing errors into compilation errors, runtime errors, and functional errors.

## 8. Ket qua chinh
- For high-performing languages: Python reaches 86.5% (DeepSeek-V3) and 87.9% (GPT-4.1-mini); TypeScript reaches 85.1% and 86.3%.
- For challenging languages: Rust improves from 53.2% to 67.7% (DeepSeek-V3) and 60.9% to 77.2% (GPT-4.1-mini) -- gains of ~14-16 pp. Perl improves from 39.2% to 68.5% (DeepSeek-V3) and 51.4% to 72.5% (GPT-4.1-mini) -- gains of ~21-29 pp. OCaml improves from 49.9% to 71.9% (DeepSeek-V3).
- Strategic transfer matrix outperforms LLM-based language selection by up to 10 percentage points.
- XL-CoGen (77.2%) significantly outperforms all fine-tuned GPT-4.1-mini variants on Rust (best: 64.3% with 1k samples).
- Stage 2 (cross-language transfer) is the most critical component; Stage 3 refinement is most effective when built on Stage 2's knowledge foundation.

## 9. Keywords
Cross-language code generation, multi-agent framework, transfer matrix, intermediate language selection, code translation, low-resource programming languages, multi-language benchmarking

## 10. Lien quan den de tai
Relevant to "Coding Agent Harness & Evaluation" in its multi-agent architecture for code generation and its systematic evaluation methodology across diverse programming languages. The transfer matrix approach for selecting optimal intermediate representations is a novel technique for coding agent design. The three-stage pipeline (generate, transfer, repair) offers a reusable pattern for agent harnesses. The cross-language evaluation framework and error categorization (compilation, runtime, functional) provide a richer evaluation methodology than pass/fail metrics alone. However, the focus on cross-language generation rather than agentic coding tasks (e.g., repository-level issue resolution) makes it less directly applicable than papers focused on SWE-bench-style evaluation.
