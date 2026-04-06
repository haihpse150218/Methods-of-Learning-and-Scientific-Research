# [2025] Liu — "Your AI, My Shell": Demystifying Prompt Injection Attacks on Agentic AI Coding Editors

## Metadata
- **arXiv:** 2509.22040v1
- **Venue:** Proc. ACM Softw. Eng., Vol. 1, No. 1, Article 1 (October 2025)
- **Year:** 2025
- **Authors:** Yue Liu, Yanjie Zhao, Yunbo Lyu, Ting Zhang, Haoyu Wang, David Lo (Singapore Management University, Huazhong University of Science and Technology, Monash University)

## 1. Van de (Problem)
Agentic AI coding editors (Cursor, GitHub Copilot) have system privileges including file system access, shell command execution, and interaction with external systems. Attackers can poison external development resources (coding rule files, MCP servers) with malicious instructions, causing AI editors to execute unauthorized terminal commands on developers' machines -- effectively turning "your AI" into "attacker's shell." No prior work had systematically evaluated this attack surface.

## 2. Dong co / Gap
Prior research on prompt injection focused primarily on text generation and recommendation contexts (chatbots, Q&A systems). These studies did not assess the unique threats posed by agentic systems that can autonomously interact with systems and execute real-world actions with elevated privileges. There was no existing benchmark or systematic framework for evaluating prompt injection vulnerabilities specifically in agentic AI coding editors.

## 3. Phuong phap (Method)
The authors develop **AIShellJack**, an automated testing framework with three stages:
1. **Data Collection:** Collect coding rules from `awesome-cursorrules`, matching codebases from GitHub, and construct 314 attack payloads covering 70 MITRE ATT&CK techniques using the `atomic-red-team` repository
2. **Simulation:** Automated simulation engine that loads codebases with embedded attack payloads into AI coding editors, initiates coding tasks ("Refactor this codebase according to @rules"), and logs all executed terminal commands
3. **Analysis:** Multi-criteria semantic matching algorithm to determine attack success by comparing expected vs. executed commands, using token matching with equivalence pairs and setup command filtering (threshold theta=0.2)

Evaluated on Cursor (Auto Mode) and GitHub Copilot in VSCode, with Claude-4-Sonnet and Gemini-2.5-Pro models.

## 4. Dong gop chinh (Contributions)
- First identification and systematic evaluation of prompt injection attacks targeting agentic AI coding editors through external resource poisoning (coding rule files)
- **AIShellJack** framework: 314 attack payloads covering 70 MITRE ATT&CK techniques across 5 development scenarios (TypeScript, PyTorch, C++, Chrome Extension, Django)
- Large-scale empirical analysis across two editors (Cursor, GitHub Copilot) and multiple LLMs showing attack success rates from 41% to 84%
- Analysis of 11 MITRE ATT&CK attack categories with per-category success rates
- Ablation studies on user instruction variation and payload template design

## 5. Diem manh (Strengths)
- Addresses a critical real-world security gap with practical implications for millions of developers
- Comprehensive attack coverage using established MITRE ATT&CK framework (70 techniques, 314 payloads)
- Rigorous evaluation with manual validation (99.1% accuracy, Cohen's kappa = 0.96)
- Multi-editor, multi-model evaluation providing broad coverage
- Ablation studies show attack success is robust to user prompt variations (only 10% range)

## 6. Han che (Limitations)
- Only collects revised codebases and executed commands; does not analyze intermediate reasoning/conversational logs of the AI editors
- Only evaluates coding rule files as attack vector; does not test project templates, third-party libraries, or MCP servers
- Attack payloads use straightforward language without advanced obfuscation or evasion techniques
- Research conducted on specific editor versions that may be updated; results are a snapshot in time
- Single-run evaluation per test case (no repeated trials)

## 7. Dataset & Metric
- **Datasets used:** 5 coding rules from `awesome-cursorrules` repository; 5 matching GitHub codebases (1.4k-10k LOC); 314 attack payloads from `atomic-red-team` covering 70 MITRE ATT&CK techniques
- **Evaluation metrics:**
  - **Execution Rate:** Percentage of cases where the AI editor executes any terminal command
  - **Attack Success Rate (ASR):** Percentage of cases where executed commands align with the malicious intent of the payload

## 8. Ket qua chinh
- **Overall ASR up to 84%** (Cursor Auto Mode on ts-lep scenario): prompt injection attacks are highly effective
- Execution rates consistently range from 74% to 89% across all configurations
- ASR varies by editor and model: Cursor Auto Mode 66.9%-84.1%; GitHub Copilot with VSCode 41.1%-52.2%
- Per MITRE ATT&CK category ASRs: Initial Access 93.3%, Discovery 91.1%, Impact 83%, Collection 77%, Privilege Escalation 71.5%, Command & Control 80%, Credential Access 68.2%, Exfiltration 55.6%
- GitHub Copilot is 20-30% more resistant than Cursor
- Ablation: Attack success does not depend significantly on user prompt variation, but does depend on payload template framing
- AI editors can autonomously refine and optimize attack strategies step by step

## 9. Keywords
`prompt injection` `agentic AI` `coding editors` `Cursor` `GitHub Copilot` `MITRE ATT&CK` `security evaluation` `coding rules` `AIShellJack` `attack surface`

## 10. Lien quan den de tai
This paper is directly central to "Coding Agent Harness & Evaluation." AIShellJack is itself an evaluation harness for testing the security of coding agents against prompt injection attacks through external resources. The methodology -- constructing attack payloads mapped to MITRE ATT&CK, automating simulation of agent interactions, and measuring attack success via semantic matching -- provides a concrete blueprint for building coding agent security evaluation frameworks. The findings (41-84% ASR) establish critical baselines that any coding agent harness must account for, and the attack taxonomy through coding rules is directly applicable to evaluating agents like Claude Code, Cursor, and Copilot.
