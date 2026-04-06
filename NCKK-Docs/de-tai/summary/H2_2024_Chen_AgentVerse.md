# [2023] Chen — AgentVerse: Facilitating Multi-Agent Collaboration and Exploring Emergent Behaviors

## Metadata
- **arXiv:** 2308.10848
- **Venue:** Preprint (Oct 2023)
- **Year:** 2023
- **Authors:** Weize Chen, Yusheng Su, Jingwei Zuo, Cheng Yang, Chenfei Yuan, Chi-Min Chan, Heyang Yu, Yaxi Lu, Yi-Hsin Hung, Chen Qian, Yujia Qin, Xin Cong, Ruobing Xie, Zhiyuan Liu, Maosong Sun, Jie Zhou

## 1. Van de (Problem)
While LLM-based autonomous agents have shown impressive individual capabilities, complex real-world tasks often require cooperation among multiple agents to achieve better efficiency and effectiveness. Existing multi-agent studies focus on narrow, specific tasks with static agent roles, limiting generalizability and adaptability across diverse problem domains.

## 2. Dong co / Gap
Prior multi-agent collaboration works use fixed, manually-assigned agent roles and static group compositions, which hinders scalability and adaptability. There is no general framework that dynamically adjusts group composition based on task progress, inspired by how human teams naturally reorganize during problem-solving. AgentVerse addresses this by automating expert recruitment and enabling iterative group adjustment.

## 3. Phuong phap (Method)
AgentVerse models the problem-solving process as an MDP with four iterative stages: (1) **Expert Recruitment** -- a recruiter agent dynamically generates expert role descriptions based on the goal, forming an adaptive multi-agent group that can be adjusted between rounds. (2) **Collaborative Decision-Making** -- agents engage in discussion using either horizontal structure (democratic, all agents contribute equally) or vertical structure (solver proposes, reviewers refine iteratively). (3) **Action Execution** -- agents execute collectively-decided actions in the environment. (4) **Evaluation** -- a feedback mechanism assesses current state vs. goal and provides verbal feedback for the next iteration. The entire process loops until the goal is met.

## 4. Dong gop chinh (Contributions)
- General multi-agent framework inspired by human group problem-solving with dynamic agent composition
- Automated expert recruitment that generates task-specific agent roles without manual assignment
- Extensive experiments across text understanding, reasoning, coding, tool utilization, and embodied AI
- Discovery and categorization of emergent social behaviors in multi-agent groups: volunteer, conformity, and destructive behaviors
- Open-source implementation at github.com/OpenBMB/AgentVerse

## 5. Diem manh (Strengths)
- Dynamic group composition adapts to task progress, unlike static role assignment in other frameworks
- Comprehensive evaluation across diverse task categories (understanding, reasoning, coding, tools, embodied AI)
- Interesting analysis of emergent behaviors provides insights into multi-agent dynamics and safety
- Framework is general and modular -- applicable to both benchmark tasks and open-ended scenarios
- Group setup with GPT-4 consistently outperforms single-agent CoT baselines

## 6. Han che (Limitations)
- GPT-3.5-Turbo agents are susceptible to erroneous feedback from peers, sometimes degrading performance in Group setup vs Solo
- Destructive behaviors (agent destruction, environment destruction) emerge without safeguards, raising safety concerns
- Evaluation metrics for open-ended tasks (e.g., consulting) are subjective and hard to standardize
- Scalability to large numbers of agents not thoroughly explored
- All experiments use zero-shot setting only; few-shot or fine-tuned agents not investigated

## 7. Dataset & Metric
- **FED** (Mehri & Eskenazi, 2020): conversation quality evaluation
- **Commongen-Challenge** (Madaan et al., 2023): creative writing
- **MGSM** (Shi et al., 2023): multilingual mathematical reasoning
- **Logic Grid Puzzles** (Srivastava et al., 2022): logical reasoning
- **HumanEval** (Chen et al., 2021): pass@1 for code completion
- **Tool utilization**: 10 custom multi-tool tasks (success count)
- **Minecraft**: embodied AI crafting tasks
- Compared settings: CoT (single), Solo (AgentVerse single-agent), Group (AgentVerse multi-agent)

## 8. Ket qua chinh
- General understanding/reasoning: Group setup achieves best results on most tasks with GPT-4 (e.g., 96.8 on FED, 99.1 on Creative Writing, 66.5 on Logic Puzzles)
- Coding (HumanEval): GPT-4 Group achieves 89.0 pass@1, up from 83.5 (CoT) and 87.2 (Solo)
- Tool utilization: AgentVerse group completes 9/10 complex multi-tool tasks vs. 3/10 for standalone ReAct agent
- Emergent behaviors identified: volunteer (time/resource/assistance contribution), conformity (realigning with group goals), destructive (harmful shortcuts for efficiency)

## 9. Keywords
multi-agent collaboration, expert recruitment, emergent behaviors, dynamic group composition, LLM agents, collaborative decision-making, embodied AI, tool utilization

## 10. Lien quan den de tai
Relevant to the thesis on coding agent harness and evaluation. AgentVerse's dynamic expert recruitment and iterative evaluation loop provide a model for how coding agent teams can be composed and assessed. The coding experiments (HumanEval) directly demonstrate multi-agent advantages for code generation. The emergent behavior analysis (especially destructive behaviors) highlights important safety considerations for coding agent evaluation. The framework's four-stage pipeline (recruit, decide, execute, evaluate) maps well to coding agent harness design patterns.
