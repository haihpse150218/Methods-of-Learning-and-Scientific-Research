# [2025] Prathifkumar et al. — Does SWE-Bench-Verified Test Agent Ability or Model Memory?

## Metadata
- **arXiv:** 2512.10218v2
- **Venue:** arXiv preprint (cs.SE)
- **Year:** 2025 (v2: 22 Dec 2025)
- **Authors:** Thanosan Prathifkumar, Noble Saji Mathews, Meiyappan Nagappan (Central Peel Secondary School; University of Waterloo)

## 1. Van de (Problem)
SWE-Bench-Verified has become the de facto benchmark for evaluating LLM-based software engineering agents, but it is built entirely on open-source GitHub repositories whose data is likely present in the training corpora of major LLMs (GPT-4, Claude). This raises the question of whether high scores on SWE-Bench-Verified reflect genuine reasoning ability or memorization of previously seen tasks.

## 2. Dong co / Gap
Prior work has shown that 94% of SWE-Bench instances were created before the training cutoffs of popular LLMs, and there is measurable data leakage (8.7-10.6%). However, existing studies compared performance on fix generation given the issue and repo. This paper isolates the localization step (finding the right files) with minimal context, making it logically impossible to solve without either reasoning or memorization. The stark performance gap between SWE-Bench-Verified and newer/cross-project benchmarks suggests the benchmark may be measuring recall rather than problem-solving skill.

## 3. Phuong phap (Method)
The authors test two Claude Sonnet models (3.5 and 3.7) on file localization -- predicting which files need to be edited to fix a bug -- under two minimal-context settings: (1) Issue + File Structure (issue text plus repository file paths, but no file content), and (2) Issue Only (just the issue text, no file names or structure). They compare localization accuracy across four datasets: SWE-Bench-Verified (500 issues), BeetleBox (500 issues from 5 Python repos not in SWE-Bench: Ansible, Apache Airflow, PostHog, Localstack, Langchain), and two SWE-rebench splits (Jan 2025: 109 issues, Sep 2025: 50 issues). Evaluation measures: percentage of issues with all ground-truth files predicted, and percentage with at least one correct file.

## 4. Dong gop chinh (Contributions)
- Demonstrates that Claude models perform 3-6x better on file localization in SWE-Bench-Verified compared to BeetleBox and SWE-rebench, even with minimal context
- Shows the performance gap persists even in the "Issue Only" setting (no file names given), strongly suggesting memorization of the benchmark itself
- Provides evidence that SWE-Bench-Verified scores may not reflect true agent ability on real software issues
- Advocates for shifting to continuously refreshed benchmarks (e.g., SWE-rebench) to limit contamination

## 5. Diem manh (Strengths)
- Clean experimental design that isolates localization from fix generation, making the memorization signal clearer
- Uses minimal-context settings that make the task logically unsolvable without prior knowledge, strengthening the contamination argument
- Compares against multiple alternative benchmarks (BeetleBox, SWE-rebench) for robust cross-validation
- Practical and important finding for the community: warns against over-reliance on a single static benchmark

## 6. Han che (Limitations)
- Only tests two models from the Claude family; does not evaluate GPT-4, GPT-5, or open-source models
- Short paper (4 pages) with limited depth of analysis; no investigation of which specific tasks are memorized
- BeetleBox repos are still popular open-source Python projects, so some leakage may exist there too
- Does not propose a concrete decontamination method or new benchmark, only recommends using refreshed datasets
- File localization accuracy is a proxy; does not directly measure whether full resolution rates are inflated

## 7. Dataset & Metric
- **Datasets:** SWE-Bench-Verified (500 issues), BeetleBox (500 issues from 5 non-SWE-Bench Python repos), SWE-rebench Jan 2025 split (109 issues), SWE-rebench Sep 2025 split (50 issues)
- **Metrics:** Percentage of issues with all ground-truth files in output; Percentage of issues with at least one ground-truth file in output

## 8. Ket qua chinh
- Issue + File Structure, all files correct: SWE-Bench 76%/73% (Claude 3.5/3.7) vs BeetleBox 21%/17.6% vs SWE-rebench(09/2025) 28%/22%
- Issue Only, all files correct: SWE-Bench 65%/63.2% vs BeetleBox 12.2%/12% vs SWE-rebench(09/2025) 12%/8%
- Performance gap is ~6x when comparing SWE-Bench to BeetleBox in Issue Only setting
- The gap is larger in the "Issue Only" setting, consistent with memorization rather than reasoning
- Results on SWE-rebench fall between BeetleBox and SWE-Bench, consistent with partial but reduced leakage

## 9. Keywords
SWE-Bench-Verified, data leakage, benchmark contamination, file localization, memorization, Claude Sonnet, BeetleBox, SWE-rebench, coding agents

## 10. Lien quan den de tai
Highly relevant to "Coding Agent Harness & Evaluation." This paper provides critical evidence that SWE-Bench-Verified -- the most widely used coding agent benchmark -- may be compromised by data leakage, meaning leaderboard scores could overstate true agent capabilities. For anyone designing an evaluation harness, this work underscores the importance of (1) using continuously refreshed or decontaminated benchmarks, (2) testing on cross-project/cross-language datasets, and (3) not relying on a single static benchmark. These insights directly inform the design of more trustworthy evaluation pipelines for coding agents.
