# [2026] Maloyan — Prompt Injection Attacks on Agentic Coding Assistants: A Systematic Analysis of Vulnerabilities in Skills, Tools, and Protocol Ecosystems

## Metadata
- **arXiv:** 2601.17548v1
- **Venue:** arXiv preprint (cs.CR)
- **Year:** 2026
- **Authors:** Narek Maloyan, Dmitry Namiot

## 1. Van de (Problem)
The proliferation of agentic AI coding assistants (Claude Code, GitHub Copilot, Cursor, OpenAI Codex CLI) leveraging LLMs integrated with external tools, file systems, and shell access through protocols like MCP has fundamentally expanded the attack surface. These systems introduce critical security vulnerabilities through prompt injection, but existing work lacks a unified taxonomy and systematic analysis of the full threat landscape across skills, tools, and protocol ecosystems.

## 2. Dong co / Gap
Prior work addresses prompt injection in fragmented ways -- some focus on text-based attacks, others on tool abuse, and MCP-specific threats are underappreciated. There is no unified classification framework that bridges disparate attack taxonomies. Additionally, existing defenses are evaluated primarily against static attacks, while adaptive attacks consistently bypass them (>85% success against all evaluated defenses). The skill-based architecture of modern coding assistants introduces unique attack surfaces not previously documented.

## 3. Phuong phap (Method)
This is a Systematization of Knowledge (SoK) paper following structured literature review methodology. The authors:
- Collected papers from arXiv, IEEE Xplore, ACM DL, and USENIX (Jan 2024 - Dec 2025), yielding 78 primary sources from 183 initial results
- Propose a three-dimensional attack taxonomy: (1) Delivery Vector (direct/indirect/protocol-level), (2) Attack Modality (text/semantic/multimodal), (3) Propagation Behavior (single-shot/persistent/viral)
- Catalog 42 distinct attack techniques and critically analyze 18 defense mechanisms
- Synthesize empirical findings from MCPSecBench, IDEsaster, and Nasr et al.
- Document novel skill-specific exploit chains for Claude Code skills and Copilot Extensions

## 4. Dong gop chinh (Contributions)
- **Unified 3D Taxonomy:** Novel three-dimensional classification organizing attacks by delivery vector, modality, and propagation behavior, bridging disparate prior classifications
- **Skill-Specific Exploit Chains:** First detailed analysis of vulnerabilities in skill-based architectures, including concrete exploit chains for Claude Code skills and Copilot Extensions not previously documented
- **Meta-Analysis:** Consolidated findings from 78 studies showing 85%+ attack success rates across platforms and that adaptive attacks bypass 90%+ of published defenses
- **Attack Catalog:** 42 systematically cataloged attack techniques including protocol-level attacks specific to MCP ecosystems (tool poisoning, rug pull, shadowing, tool squatting)
- **Defense-in-Depth Framework:** Six-layer defense proposal: cryptographic tool identity, capability scoping, runtime intent verification, sandboxed execution, provenance tracking, human-in-the-loop gates

## 5. Diem manh (Strengths)
- Very timely coverage of MCP and skill ecosystem vulnerabilities, which are rapidly becoming the dominant architecture
- Concrete, documented exploit chains with real CVEs (CVE-2025-49150, CVE-2025-53773, CVE-2025-58335, etc.)
- Platform vulnerability assessment comparing Claude Code (Low), Copilot (High), Cursor (Critical), Codex CLI (High), Gemini CLI (Medium)
- The "Von Neumann Bottleneck" analogy effectively explains the fundamental architectural limitation (LLMs conflate instructions and data in context window)
- Practical defense framework with tiered human-in-the-loop approach (Silent/Logged/Confirmed/Blocked)

## 6. Han che (Limitations)
- No independent replication experiments; attack success rates and defense evaluations are drawn from existing sources (MCPSecBench, IDEsaster, Nasr et al.)
- Rapid evolution of the field means findings may be outdated quickly
- Major platforms (Claude, GPT-4, Copilot) are closed-source, limiting visibility into internal defense mechanisms
- Existing benchmarks may not reflect real-world attack sophistication
- Primarily evaluates static defenses; adaptive defense systems remain understudied
- Selection bias: successful attacks by sophisticated actors may never be disclosed

## 7. Dataset & Metric
- **Datasets used:** Meta-analysis synthesizing data from MCPSecBench (17 attack types across 4 surfaces), IDEsaster (30+ CVEs across major AI IDEs), Nasr et al. defense bypass study, and 78 primary literature sources
- **Evaluation metrics:** Attack Success Rate (ASR), defense bypass rates, platform vulnerability ratings (L/M/H), CVE severity assessments

## 8. Ket qua chinh
- **85%+ of attacks** successfully compromise at least one major platform (from MCPSecBench)
- **All 12 evaluated defenses** can be bypassed with attack success rates exceeding 78% using adaptive optimization (gradient descent, RL, random search) -- from Nasr et al.
- **Defense bypass rates under adaptive attacks:** Protect AI <5% reported but 93% adaptive; PromptGuard <3% reported but 91% adaptive; PIGuard <5% reported but 89% adaptive; Model Armor <10% reported but 78% adaptive
- **Platform vulnerability:** Claude Code rated Low overall, Cursor rated Critical, Copilot rated High
- **41%-84% attack success rates** across platforms for rules file exploitation (from AIShellJack)
- **73% of tested platforms** fail to adequately enforce at least one trust boundary

## 9. Keywords
`prompt injection` `coding assistants` `MCP` `skills` `tool poisoning` `Claude Code` `Copilot` `Cursor` `defense-in-depth` `SoK` `exploit chains` `trust boundaries`

## 10. Lien quan den de tai
This paper is a cornerstone reference for "Coding Agent Harness & Evaluation." It provides the most comprehensive taxonomy of attacks specifically targeting coding assistants (the exact systems an evaluation harness would test). The skill-specific exploit chains, platform vulnerability comparisons, and defense bypass analysis directly inform what a coding agent evaluation harness must test for. The proposed defense-in-depth framework (cryptographic identity, capability scoping, runtime verification, sandboxing, provenance tracking, human-in-the-loop) defines the security properties that a harness should verify. The meta-analysis showing all static defenses are bypassable with adaptive attacks highlights the importance of continuous evaluation.
