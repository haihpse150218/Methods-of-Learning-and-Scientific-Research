# [2025] Khan — MACOG: Multi-Agent Code-Orchestrated Generation for Reliable Infrastructure-as-Code

## Metadata
- **arXiv:** 2510.03902
- **Venue:** arXiv preprint (cs.SE)
- **Year:** 2025
- **Authors:** Rana Nameer Hussain Khan, Dawood Wasif, Jin-Hee Cho, Ali Butt

## 1. Van de (Problem)
Infrastructure-as-Code (IaC) generation from natural language is a constrained program construction problem where outputs must satisfy strict provider schemas, cross-resource dependency constraints, security and compliance policies, cost budgets, and deployment correctness. Current LLMs using monolithic single-pass generation produce syntactically invalid, policy-violating, and unscalable Terraform configurations, with even state-of-the-art models (GPT-4) solving only 19% of IaC tasks correctly on the first try.

## 2. Dong co / Gap
Existing approaches treat IaC generation as flat text generation, ignoring its inherent graph structure (resources, dependencies, edges). Few-shot prompting scales poorly for multi-module configurations. RAG retrieval is brittle due to provider schema versioning drift. Single-agent multi-turn repair oscillates in long contexts and overwrites working parts. No prior work integrates grammar-constrained decoding with external validators (terraform validate, OPA/Rego policy engines, deployment sandboxes) in a coordinated multi-agent pipeline for IaC synthesis.

## 3. Phuong phap (Method)
MACOG uses a team of role-specialized agents coordinating via a shared blackboard and finite-state orchestrator, operating on a typed Infrastructure Intermediate Representation (I-IR):

- **Architect:** Parses natural language intent into an I-IR plan (typed resource graph with nodes, edges, effects, invariants).
- **Provider Harmonizer:** Instantiates resources against provider schemas, resolves versions, expands defaults.
- **Engineer:** Compiles I-IR into HCL using grammar- and schema-constrained decoding (only valid HCL tokens permitted), with round-trip equivalence check back to I-IR.
- **Reviewer:** Runs terraform validate, HCL linters, and interface sanity checks; emits precise diagnostics.
- **Security Prover:** Evaluates OPA/Rego policies and Checkov/Regula for least-privilege, encryption, tagging compliance.
- **Cost and Capacity Planner:** Deterministic cost estimation from pinned price catalogs with SKU and quota checks.
- **DevOps:** Executes terraform init/plan/apply in sandboxed environments (LocalStack, ephemeral cloud accounts).
- **Memory Curator:** Stores verified (plan, code, evidence) tuples as reusable motifs indexed by graph structure.

A counterexample-guided repair loop maps validator failures to minimal, targeted edits at I-IR or HCL level, guided by a scalarized routing objective.

## 4. Dong gop chinh (Contributions)
- A multi-agent architecture for IaC generation that decomposes the task into modular subtasks with specialized agents coordinating via a typed intermediate representation and shared blackboard.
- Grammar- and schema-constrained decoding that prevents syntactically invalid HCL generation at token level, with round-trip equivalence verification.
- A counterexample-guided repair loop using structured validator feedback (schema, policy, cost, deploy) for targeted minimal edits rather than speculative rewrites.
- Produces a self-contained evidence bundle (policy traces, cost sheets, deploy logs) enabling offline third-party verification before production deployment.
- Comprehensive evaluation across 10 models showing consistent improvements (e.g., GPT-5: 54.90 RAG to 74.02 MACOG on IaC-Eval).

## 5. Diem manh (Strengths)
- Zero fine-tuning design: all agents operate in instruction-following/zero-shot mode, making the framework model-agnostic.
- Constrained decoding ensures syntactic validity by construction, eliminating a large class of errors before validation.
- The I-IR provides a typed, machine-checkable representation that makes resources, edges, and effects explicit -- far more structured than raw code generation.
- Scales with model quality: strong models get highest absolute scores while smaller models get largest relative lift, making it practical across budget tiers.
- DevOps agent with sandbox execution (LocalStack + ephemeral accounts) provides realistic deployment validation unavailable in most code generation frameworks.

## 6. Han che (Limitations)
- Absolute IaC-Eval scores remain moderate (74.02 for GPT-5, 60.13 for Gemini-2.5 Pro), indicating substantial room for improvement in IaC generation.
- Constrained decoding and multi-validator pipeline add computational overhead and latency compared to single-pass generation.
- Evaluated only on IaC-Eval benchmark; generalization to other IaC frameworks (CloudFormation, Pulumi, Ansible) and real-world production configurations is untested.
- Provider schema drift over time requires maintaining up-to-date grammar automata and price catalogs.
- Open-source models (CodeLlama, WizardCoder) achieve very low scores even with MACOG (10-16 on IaC-Eval), suggesting a capability floor below which orchestration cannot compensate.

## 7. Dataset & Metric
- **Dataset:** IaC-Eval -- a benchmark of natural-language infrastructure intents with associated verification procedures for cloud provisioning (VPC topologies, instance fleets, managed databases, IAM policies, serverless integrations).
- **Metrics:** BLEU (n-gram overlap), CodeBERTScore (semantic similarity), LLM-judge (binary adequacy by held-out judge), IaC-Eval (harness-verified task success through plan, policy, and validation checks).

## 8. Ket qua chinh
- GPT-5 with MACOG: IaC-Eval 74.02 (vs. 54.90 RAG, 35.83 Multi-turn, 12.53 Few-shot), BLEU 11.86, CodeBERTScore 80.54, LLM-judge 94.10.
- Gemini-2.5 Pro with MACOG: IaC-Eval 60.13 (vs. 43.56 RAG, 36.81 Multi-turn, 12.18 Few-shot), BLEU 10.09, CodeBERTScore 71.84, LLM-judge 87.52.
- Average MACOG uplift over RAG across 10 models: +7.3 absolute IaC-Eval points (~+35% relative).
- Ablation (GPT-5): removing DevOps sandbox causes largest IaC-Eval drop (74.02 to 56.93), followed by removing Security Prover (to 61.45) and constrained decoding (to 64.89).
- Strategy ordering across all 10 models: MACOG > RAG > Multi-turn > CoT ~ Few-shot.

## 9. Keywords
Infrastructure-as-Code, Terraform, multi-agent systems, constrained decoding, policy compliance, OPA/Rego, counterexample-guided repair, DevOps automation, blackboard architecture

## 10. Lien quan den de tai
Relevant to "Coding Agent Harness & Evaluation" as a specialized application of multi-agent coding architectures to a constrained domain (IaC). The key transferable insights include: (1) the blackboard + finite-state orchestrator pattern for coordinating specialized agents, (2) the typed intermediate representation (I-IR) approach that makes agent communication structured and verifiable, (3) grammar-constrained decoding to guarantee syntactic validity by construction, (4) the counterexample-guided repair loop with structured validator feedback, and (5) the proof-carrying evidence bundle concept for auditable agent outputs. The IaC-Eval benchmark and multi-metric evaluation methodology (BLEU, CodeBERTScore, LLM-judge, harness-verified success) provide a model for comprehensive coding agent evaluation. However, the focus on Terraform/IaC rather than general-purpose coding limits direct applicability.
