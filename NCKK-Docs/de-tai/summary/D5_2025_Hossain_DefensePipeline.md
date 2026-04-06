# [2025] Hossain — A Multi-Agent LLM Defense Pipeline Against Prompt Injection Attacks

## Metadata
- **arXiv:** 2509.14285v4
- **Venue:** arXiv preprint (cs.CR)
- **Year:** 2025
- **Authors:** S M Asif Hossain, Ruksat Khan Shayoni, Mohd Ruhul Ameen, Akif Islam, M. F. Mridha, Jungpil Shin (Wichita State University, Marshall University, University of Rajshahi, American International University-Bangladesh, University of Aizu)

## 1. Van de (Problem)
Prompt injection attacks represent a major vulnerability in LLM deployments where malicious instructions embedded in user inputs can override system prompts and induce unintended behaviors. Traditional security approaches including static input sanitization and content filtering prove inadequate against sophisticated prompt injection techniques that exploit the fundamental architecture of LLMs where system prompts and user inputs are processed as unified text sequences.

## 2. Dong co / Gap
Existing defense strategies (input preprocessing, output filtering, prompt engineering, model fine-tuning) exhibit limitations in handling novel attack vectors and maintaining system utility. Multi-agent architectures offer a promising alternative by utilizing distributed intelligence to implement defense-in-depth strategies. Prior multi-agent security frameworks lacked comprehensive empirical validation across diverse attack scenarios and practical deployment guidelines.

## 3. Phuong phap (Method)
The authors propose two complementary multi-agent defense pipeline architectures:
1. **Chain-of-Agents Pipeline:** User query goes to Domain LLM first, which generates a candidate answer. A Guard agent then mandatorily vets the output for policy violations, attack indicators, and format compliance before release.
2. **Coordinator Pipeline:** A Coordinator agent intercepts queries upfront, classifying them as safe or malicious. Malicious inputs trigger a safe refusal; safe inputs are routed to the Domain LLM for processing, then checked by the Guard agent.

The system includes an API Gateway, Event Orchestrator, Policy Store, Buffer stages, and Logger & Metrics components. Coordinator handles pre-input screening/routing, trust boundaries, context isolation. Guard handles output validation, redaction/token blocking, format enforcement.

Evaluated on ChatGLM-6B and Llama2-13B with 55 unique prompt injection attacks across 8 categories.

## 4. Dong gop chinh (Contributions)
- **Novel Architecture Design:** Two complementary multi-agent configurations (chain-of-agents and coordinator pipeline) providing flexible deployment options for different security requirements
- **Comprehensive Evaluation Framework:** Systematic assessment using 55 unique prompt injection attacks, grouped into 8 categories, totaling 400 attack instances across two LLM platforms
- **Empirical Validation:** Demonstration of 100% attack mitigation (ASR reduced to 0%) across all tested scenarios while preserving system functionality
- **Practical Implementation Guidelines:** Detailed analysis of deployment considerations, performance trade-offs, and scalability factors

## 5. Diem manh (Strengths)
- Achieves perfect defense (0% ASR) across all 400 evaluation instances, compared to 20-30% baseline ASR
- Covers 8 diverse attack categories: direct overrides, code execution, data exfiltration, formatting attacks, obfuscation, tool/agent manipulation, role-play attacks, multi-turn persistence
- Two complementary architectures offer flexibility: chain-of-agents for post-generation validation, coordinator for pre-input gating
- Clear separation of Coordinator and Guard agent responsibilities (Table III)
- Multi-dimensional assessment across five criteria: attack prevention, category coverage, consistency, scalability, implementation complexity

## 6. Han che (Limitations)
- Only tested on two relatively older/smaller models (ChatGLM-6B and Llama2-13B), not on state-of-the-art models like GPT-4, Claude, etc.
- 55 unique attacks may not cover the full space of sophisticated or adaptive adversarial strategies
- Does not evaluate against adaptive attacks where the adversary knows the defense architecture
- Multi-turn persistence attacks tested in single-turn setting (except a small subset)
- Scalability and latency overhead of the multi-agent pipeline not quantitatively measured
- No evaluation of false positive rates on legitimate queries

## 7. Dataset & Metric
- **Datasets used:** HPI_ATTACK_DATASET -- 55 unique prompt injection attacks across 8 categories, each manually validated and labeled with expected failure modes. Three subsets: v1 Taxonomy (25 cases), Phase 2 Chain (15 cases), Phase 2 Coordinator (15 cases). Total 400 evaluation instances.
- **Evaluation metrics:**
  - **Attack Success Rate (ASR):** Percentage of attacks that successfully bypass defenses
  - **Category coverage:** Whether all attack categories are mitigated
  - **Consistency:** Variance across runs
  - **Multi-dimensional radar chart:** Attack prevention, category coverage, consistency, scalability, implementation complexity

## 8. Ket qua chinh
- **Baseline ASR (no defense):** ChatGLM 30%, Llama2 20% across different evaluation suites
- **Defended ASR:** 0% across all three architectures (v1 Taxonomy, Phase2 Coordinator, Phase2 Chain) -- 100% attack reduction
- **Category-specific baseline vulnerability:** Delegate attacks 100% ASR, Role-play coercion 66.7%, Reconnaissance/Environment 60%, Directory traversal 50%, Exfiltration 50%, Obfuscation 33.3%, Formatting 20%, Override/CTA/Navigation 0%
- All category-specific ASRs reduced to 0% with defense enabled
- All three architectures achieved identical protection despite differing baseline resilience and design complexity
- Taxonomy filter excelled in simplicity; multi-agent pipelines offered deeper contextual analysis at the cost of greater complexity

## 9. Keywords
`prompt injection` `multi-agent defense` `LLM security` `chain-of-agents` `coordinator pipeline` `guard agent` `attack mitigation` `ChatGLM` `Llama2` `defense pipeline`

## 10. Lien quan den de tai
This paper is relevant to "Coding Agent Harness & Evaluation" as it demonstrates a concrete multi-agent defense architecture that could be integrated into coding agent harnesses. The chain-of-agents and coordinator pipeline patterns provide actionable designs for building safety layers around coding agents. The evaluation framework with 55 attacks across 8 categories offers a reusable methodology for testing coding agent defenses. However, the limitation of testing only on older models (ChatGLM-6B, Llama2-13B) and the lack of adaptive attack evaluation means the 100% mitigation claim should be interpreted cautiously when applied to more capable coding agent systems.
