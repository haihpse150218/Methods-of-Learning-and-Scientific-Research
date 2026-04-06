# [2025] Pham et al. — SWE-EVO: Benchmarking Coding Agents in Long-Horizon Software Evolution Scenarios

## Metadata
- **arXiv:** 2512.18470v4
- **Venue:** arXiv preprint (cs.SE)
- **Year:** 2025 (v4: 26 Jan 2026)
- **Authors:** Minh Vu Thai Pham, Tue Le, Dung Nguyen Manh, Huy Nhat Phan, Nghi D. Q. Bui (FPT Software AI Center, University of Melbourne)

## 1. Van de (Problem)
Existing benchmarks for AI coding agents (e.g., SWE-Bench) focus on isolated, single-issue tasks such as fixing one bug or adding a small feature. However, real-world software engineering is a long-horizon endeavor where developers interpret high-level requirements, coordinate changes across many files, and evolve codebases over multiple iterations while preserving existing functionality. Current benchmarks are showing signs of saturation and do not capture this complexity.

## 2. Dong co / Gap
SWE-Bench confines tasks to isolated GitHub issues, often inflating performance through incomplete fixes or data contamination. Up to 80% of real software engineering involves maintaining and evolving legacy codebases rather than building from scratch. No existing benchmark evaluates agents on multi-step software evolution tasks that span multiple commits, require long-horizon planning, and demand multi-file coordinated changes aligned with release-note-level specifications.

## 3. Phuong phap (Method)
SWE-EVO is constructed in three stages: (1) Repository selection and data scraping from SWE-Bench and SWE-gym repositories; (2) Candidate selection by targeting codebase evolution between two release versions, using release notes as the Software Requirement Specification (SRS); (3) Execution-based filtering to retain only instances with verifiable FAIL_TO_PASS tests. The benchmark comprises 48 tasks across 7 mature open-source Python projects (dvc, dask, pydantic, requests, modin, scikit-learn, conan). Agents receive a release-note item and a pre-release codebase, and must produce patches evolving the codebase to the next version. Two input settings are evaluated: release-note only, and release-note + PR/issue context. The authors also propose Fix Rate, a soft metric that captures partial progress by measuring the fraction of FAIL_TO_PASS tests fixed while penalizing regressions on PASS_TO_PASS tests.

## 4. Dong gop chinh (Contributions)
- Introduces SWE-EVO, the first benchmark targeting long-horizon software evolution rather than single-issue repair
- Proposes Fix Rate, a soft-score metric that captures partial progress on complex tasks with large test suites
- Provides comprehensive evaluation with 2 agent frameworks (OpenHands, SWE-agent) and 11 state-of-the-art models
- Demonstrates a significant capability gap: best model (GPT-5) achieves only ~21% on SWE-EVO vs 65% on SWE-Bench Verified
- Conducts trajectory-level failure mode analysis revealing distinct failure patterns across model families

## 5. Diem manh (Strengths)
- Addresses a genuine gap in benchmark coverage: multi-file, multi-step evolution tasks closer to real-world SE
- Tasks are substantially more demanding than SWE-Bench (avg 21 files edited, 874 total tests, 610 lines edited per instance)
- Compatible with existing SWE-Bench infrastructure for reproducibility
- Fix Rate metric provides meaningful differentiation between models that binary Resolved Rate collapses
- Detailed failure mode taxonomy (Syntax Error, Incorrect Implementation, Instruction Following, Tool-Use, Stuck in Loop, Gave Up Prematurely) with LLM-as-judge analysis

## 6. Han che (Limitations)
- Only covers Python projects (7 repositories); does not generalize to other languages
- Small scale with only 48 task instances, limiting statistical power for fine-grained comparisons
- Relies on release notes as specifications, which may not capture all evolution scenarios (e.g., security patches, performance optimizations without explicit notes)
- Tasks are derived from existing SWE-Bench/SWE-gym repositories, potentially inheriting their biases

## 7. Dataset & Metric
- **Dataset:** SWE-EVO -- 48 tasks across 7 open-source Python repos (dvc: 26, dask: 8, requests: 4, pydantic: 3, modin: 3, scikit-learn: 2, conan: 2). Avg 21 files edited, 610 lines edited, 874 total tests per instance.
- **Metrics:** Resolved Rate (%) -- binary pass/fail; Patch Apply Rate (%) -- syntactic validity; Fix Rate (%) -- soft score measuring fraction of FAIL_TO_PASS tests fixed without regressions.

## 8. Ket qua chinh
- Best model GPT-5 with SWE-agent achieves 20.83% Resolved Rate on SWE-EVO (release-note + PR/issue), vs 65% on SWE-Bench Verified
- Clear scaling trend: larger models consistently outperform smaller variants (gpt-5 > gpt-5-mini > gpt-5-nano)
- Providing PR/issue context yields only modest improvements over release-note only (e.g., GPT-5: 20.83% vs 16.67%)
- Fix Rate reveals finer distinctions: GPT-5 achieves 31.44% Fix Rate vs 20.83% Resolved Rate on SWE-agent
- Failure analysis: strongest models (GPT-5) fail primarily on Instruction Following (~60%); weaker models struggle with Tool-Use and Syntax Errors
- Difficulty correlates with number of associated PRs per instance

## 9. Keywords
SWE-EVO, software evolution, long-horizon benchmark, coding agents, SWE-Bench, multi-file editing, Fix Rate, release notes, software maintenance

## 10. Lien quan den de tai
Directly relevant to "Coding Agent Harness & Evaluation." SWE-EVO extends the evaluation paradigm beyond single-issue resolution (SWE-Bench) to long-horizon software evolution, which is a more realistic measure of coding agent capabilities. The benchmark's construction methodology (leveraging release notes and version histories), its Fix Rate metric for partial-credit evaluation, and its failure mode taxonomy all provide valuable design insights for building comprehensive coding agent evaluation harnesses. The finding that even the best agents achieve only ~21% highlights the need for better agent architectures and evaluation frameworks.
