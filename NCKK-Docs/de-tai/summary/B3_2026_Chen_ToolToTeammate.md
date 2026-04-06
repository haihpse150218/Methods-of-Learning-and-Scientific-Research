# [2026] Chen — From Tool to Teammate: LLM Coding Agents as Collaborative Partners for Behavioral Labeling in Educational Dialogue Analysis

## Metadata
- **arXiv:** 2603.27440v1
- **Venue:** (preprint, arXiv cs.HC)
- **Year:** 2026
- **Authors:** Eason Chen, Isabel Wang, Nina Yuan, Sophia Judicke, Kayla Beigh, Xinyi Tang (Carnegie Mellon University)

## 1. Van de (Problem)
Behavioral analysis of tutoring dialogues is essential for understanding student learning, yet manual coding remains a bottleneck. Trained coders must manually analyze hundreds of sessions over weeks. While LLMs can perform qualitative coding tasks, developing effective prompts still relies heavily on researcher effort through trial-and-error iteration, limiting scalability and reproducibility of LLM-assisted educational research.

## 2. Dong co / Gap
Existing approaches treat LLMs as static tools to be configured by humans. Automated prompt optimization methods (APE, DSPy, OPRO) optimize a fixed metric through algorithmic search but do not perform qualitative error analysis or propose theory-grounded modifications. No prior work uses coding agents as research teammates that autonomously iterate on labeling prompts through systematic error analysis, with documented reasoning and researcher oversight at each step.

## 3. Phuong phap (Method)
An iterative agent-driven prompt refinement methodology where LLM coding agents serve as research teammates:
1. **Develop-test-analyze cycle (Algorithm 1):** In each iteration, the agent runs the classifier (LLM) on labeled validation data, computes Cohen's Kappa and per-category metrics, analyzes disagreements between classifier labels and human consensus, proposes theory-grounded prompt modifications with documented reasoning, and the researcher reviews for pedagogical validity.
2. **Four experiments across agent-classifier combinations:**
   - Experiment 1: Claude Code agent + GPT-5.2 classifier, 21 iterations (exploratory)
   - Experiment 2: Three independent agents (OpenAI Codex, Claude Code, Gemini) + GPT-5.2 classifier, ~10 iterations each
   - Experiment 3: Same three agents + Claude Opus 4.5 classifier
   - Experiment 4: Same three agents + Gemini 3 Pro classifier
3. **Labeling framework:** Three dimensions -- Student Intent (Answer-Seeking, Help-Seeking, Other), Topic Type (Conceptual, Procedural), Follow-up Type (Engage, Escalate, Switch)
4. **Validation:** 4-fold cross-validation on 80 labeled sessions from 659 AI tutoring sessions in a discrete mathematics course

## 4. Dong gop chinh (Contributions)
- A collaborative workflow where LLM coding agents autonomously execute develop-test-analyze cycles while researchers provide theoretical oversight, shifting agents from tools to teammates
- Empirical evidence that iterative refinement enables substantial performance gains: best agent achieves test kappa = 0.78 (SD=0.08), matching human inter-rater reliability (kappa = 0.78)
- Discovery of a "same-family advantage" where agents converge faster when the classifier shares their model architecture, though cross-family classifiers can ultimately achieve comparable performance
- Surfacing of an undocumented labeling pattern: human coders consistently treated expressions of confusion as engagement rather than disengagement ("confusion = engagement" insight)
- Evidence that continued iteration beyond the optimum leads to regression, underscoring the need for held-out validation

## 5. Diem manh (Strengths)
- Cost-effective: approximately $5-8 per agent per classifier, total ~$22 for three independent validations in Experiment 2
- Rigorous cross-validation design (4-fold) that reveals overfitting gap (validation kappa 0.91-0.93 vs. test kappa 0.72-0.78)
- Independent convergence of three agents on similar disambiguation rules validates that the methodology identifies genuine data patterns rather than agent-specific artifacts
- Transparent and reproducible: all prompts, iteration logs, and evaluation scripts released publicly
- Practical discovery of pedagogically meaningful insight (confusion = engagement) that was implicit in human coding but undocumented

## 6. Han che (Limitations)
- Small validation set (80 sessions) limits statistical power and creates overfitting potential
- Session-level labeling does not capture within-session dynamics (e.g., intent shifts mid-conversation)
- Only three model families examined (GPT, Claude, Gemini); other combinations may yield different patterns
- No comparison against fine-tuned models which might achieve higher performance with sufficient training data
- Lacks a fully independent final test set separated from all tuning phases

## 7. Dataset & Metric
- **Dataset:** 659 chatbot tutoring sessions from an undergraduate discrete mathematics course (~120 students), Fall 2024 and Spring 2025. 80 sessions randomly sampled as validation set, stratified by length and topic area.
- **Metrics:** Cohen's Kappa (primary), F1 score, per-dimension kappa (Student Intent, Topic Type, Follow-up Type), 4-fold cross-validated test kappa
- **Human baseline:** Inter-rater reliability kappa = 0.89 overall (0.78 Student Intent, 0.73 Topic Type, 0.70 Follow-up Type)

## 8. Ket qua chinh
- Best cross-validated test performance: Codex achieves kappa = 0.78 (SD=0.08), matching human inter-rater reliability
- Development-set performance reaches kappa = 0.91-0.93 across agents, but cross-validation reveals overfitting gap (delta kappa ~ 0.15-0.21)
- All three agents independently converge on the "confusion = engagement" disambiguation rule
- Same-family advantage manifests as faster convergence (fewer iterations to peak) rather than higher performance ceilings
- GPT-5.2 classifier enables highest ceiling performance (kappa = 0.93 for both Codex and Gemini)
- Continued iteration beyond optimum causes regression (Codex v7 -> v10: kappa drops from 0.93 to 0.91)
- Two regression patterns identified: over-correction (restructuring decision priorities) and output format instability (aggressive prompt shortening)

## 9. Keywords
LLM coding agents, behavioral labeling, prompt engineering, educational dialogue analysis, AI tutoring, inter-rater reliability, Cohen's Kappa, iterative refinement, same-family advantage, human-AI collaboration

## 10. Lien quan den de tai
Relevant to "Coding Agent Harness & Evaluation" from the evaluation methodology perspective. The paper demonstrates how coding agents (Codex, Claude Code, Gemini) can be evaluated through iterative refinement cycles with systematic error analysis. The cross-agent validation framework -- where multiple independent agents tackle the same task and their convergence validates methodology robustness -- is a transferable evaluation pattern. The findings on regression during continued iteration, overfitting risks, and same-family classifier advantages provide practical guidance for evaluating coding agent outputs. However, the application domain (educational dialogue labeling) is not directly about code generation or software engineering harnesses.
