# [2025] Chhabra — Agentic AI Security: Threats, Defenses, Evaluation, and Open Challenges

## Metadata
- **arXiv:** 2510.23883v2
- **Venue:** arXiv preprint (cs.AI)
- **Year:** 2025 (posted Feb 2026)
- **Authors:** Anshuman Chhabra, Shrestha Datta, Shahriar Kabir Nahin, Prasant Mohapatra (University of South Florida)

## 1. Van de (Problem)
Agentic AI systems powered by LLMs are emerging as powerful automation platforms with autonomy, planning, tool use, memory, and the ability to act upon digital/physical environments. Their expanded capabilities create new and amplified security risks distinct from both traditional AI safety and conventional software security. A comprehensive systematization of these threats, defenses, and evaluation methods is needed.

## 2. Dong co / Gap
Prior surveys on autonomous AI agents mostly detail capabilities and propose evaluation benchmarks, or explore topics like trust and risk management without a singular focus on security. Risk management frameworks such as the NIST Generative AI Profile provide baseline guidance but adapting them to autonomous agents remains a work in progress. This survey fills the gap by providing a unified taxonomy of agentic AI security threats, a thorough review of defense strategies, and guidelines for benchmarking security-critical agentic applications.

## 3. Phuong phap (Method)
This is a survey paper. The authors propose a comprehensive taxonomy of security threats organized into five categories: (i) Prompt Injection and Jailbreaks, (ii) Autonomous Cyber-Exploitation and Tool Abuse, (iii) Multi-Agent and Protocol-Level Threats, (iv) Interface and Environment Risks, and (v) Governance and Autonomy Concerns. They then systematically review defense strategies (prompt-injection-resistant designs, policy filtering, sandboxing, detection/monitoring, and standards) and survey existing benchmarks for both capability and security evaluation.

## 4. Dong gop chinh (Contributions)
- A broad taxonomy of agentic AI security threats covering prompt injection, cyber-exploitation, multi-agent/protocol threats (MCP, A2A), interface risks, and governance concerns
- Comprehensive review of defense strategies: agent-focused, user-focused, system-focused defenses; policy filtering; sandboxing; monitoring
- Detailed survey of security and capability benchmarks (Table 2) covering 30+ benchmarks across domains
- Identification of open challenges: long-horizon security, multi-agent security, adaptive attacks, physical-world agentic AI, human-agent security interfaces
- Secure-by-design defense coverage table (Table 1) mapping defense approaches to security components

## 5. Diem manh (Strengths)
- Extremely comprehensive coverage of the agentic AI security landscape with 276 references
- Well-structured taxonomy with clear visual diagrams (Figures 2-9)
- Covers emerging threats specific to agentic protocols (MCP, A2A) which are very timely
- Bridges the gap between AI safety and conventional cybersecurity perspectives
- Identifies under-explored areas like long-horizon security and adaptive attacks

## 6. Han che (Limitations)
- As a survey, no novel empirical experiments or new defense mechanisms are proposed
- The rapidly evolving nature of the field means some coverage may quickly become outdated
- Limited discussion of quantitative comparison between defense approaches
- Focus primarily on software-based agents; physical-world agentic AI security is acknowledged but less developed

## 7. Dataset & Metric
- **Datasets used:** N/A (survey paper); reviews benchmarks including BrowserGym, WebArena, AgentDojo, AgentHarm, ToolEmu, InjecAgent, ASB, SafeArena, WASP, MCPSecBench, and others
- **Evaluation metrics reviewed:** ASR (Attack Success Rate), CuP (Completion Under Policy), Risk Ratio, TSR, Leakage Rate, Refusal Rate, pass@k, end-state and process-aware metrics

## 8. Ket qua chinh
- 94.4% of state-of-the-art LLM agents are vulnerable to prompt injection; 83.3% to retrieval-based backdoors; 100% to inter-agent trust exploits
- EchoLeak (CVE-2025-32711) demonstrated real-world prompt injection against Microsoft Copilot
- GPT-4 achieves 87% success rate exploiting one-day vulnerabilities from CVE descriptions
- Existing defenses are categorized into agent-focused (training, prompt engineering), user-focused (confirmation), and system-focused (isolation, detection, monitoring)
- Key benchmark finding: end-state metrics are insufficient; process-aware and distribution-based metrics are needed

## 9. Keywords
`agentic AI` `LLM security` `prompt injection` `multi-agent threats` `MCP protocol` `tool abuse` `sandboxing` `defense taxonomy` `security benchmarks` `survey`

## 10. Lien quan den de tai
This survey is highly relevant to "Coding Agent Harness & Evaluation" as it provides the most comprehensive overview of security threats and evaluation benchmarks for agentic AI systems. It covers the security aspects of coding agents specifically (mentioning Devin, SWE-bench), reviews harness/benchmark design principles (process-aware evaluation, sandboxing, reproducibility), and catalogs the defense patterns that a coding agent harness should test against. The benchmark taxonomy (Table 2) and defense coverage analysis (Table 1) directly inform the design of evaluation frameworks for coding agents.
