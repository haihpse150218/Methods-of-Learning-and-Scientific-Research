# [2025] Beurer-Kellner — Design Patterns for Securing LLM Agents against Prompt Injections

## Metadata
- **arXiv:** 2506.08837v3
- **Venue:** arXiv preprint (cs.LG)
- **Year:** 2025
- **Authors:** Luca Beurer-Kellner, Beat Buesser, Ana-Maria Cretu, Edoardo Debenedetti, Daniel Dobos, Daniel Fabian, Marc Fischer, David Froelicher, Kathrin Grosse, Daniel Naeff, Ezinwanne Ozoani, Andrew Paverd, Florian Tramer, Vaclav Volhejn (Invariant Labs, IBM, EPFL, ETH Zurich, Swisscom, Google, Microsoft, Kyutai)

## 1. Van de (Problem)
As LLM agents become increasingly versatile and handle sensitive tasks with tool access, prompt injection attacks pose a critical security threat. These attacks exploit the agent's resilience on natural language inputs to manipulate behavior, causing unauthorized tool execution, data exfiltration, or privilege escalation. General-purpose agents are unlikely to provide meaningful safety guarantees against prompt injection.

## 2. Dong co / Gap
Existing defenses range from heuristic approaches (detection, adversarial training) to principled isolation mechanisms, but most aim to design safe general-purpose agents. The authors argue this is insufficient -- general-purpose agents cannot provide reliable safety guarantees with current LLM technology. Instead, the focus should shift to building application-specific agents with principled design constraints that trade some utility for provable security properties.

## 3. Phuong phap (Method)
The authors propose six composable design patterns for building LLM agents resistant to prompt injection:
1. **Action-Selector Pattern** -- Agent acts as a translator mapping requests to predefined actions; no feedback from tool outputs
2. **Plan-Then-Execute Pattern** -- Agent formulates a fixed plan before processing untrusted data; provides control flow integrity
3. **LLM Map-Reduce Pattern** -- Dispatches isolated sub-agents to process individual data items; prevents cross-contamination
4. **Dual LLM Pattern** -- Separates privileged LLM (with tools) from quarantined LLM (processes untrusted data, no tools); symbolic variable passing
5. **Code-Then-Execute Pattern** -- Agent writes a formal program instead of planning; program handles tool calls and sub-LLM dispatches
6. **Context-Minimization Pattern** -- Removes user prompt from context after initial processing to prevent injection in later stages

These are applied to 10 case studies spanning diverse domains.

## 4. Dong gop chinh (Contributions)
- Six principled, composable design patterns that provide meaningful resistance to prompt injection by constraining agent capabilities
- Systematic analysis of security-utility trade-offs for each pattern
- Ten detailed case studies demonstrating real-world applicability: OS assistant, SQL agent, email/calendar assistant, customer service chatbot, booking assistant, product recommender, resume screening, medication chatbot, medical diagnosis, software engineering agent
- Clear articulation that general-purpose agents cannot be secured with current technology; application-specific design is necessary
- Best-practice recommendations (Appendix A) for all LLM agents

## 5. Diem manh (Strengths)
- Highly practical and actionable -- each pattern is clearly defined with concrete examples
- Composable patterns can be combined for layered defense
- Extensive case studies covering 10 diverse application domains with detailed threat models
- Principled approach grounded in established security concepts (least privilege, control flow integrity, isolation)
- Includes a dedicated case study on Software Engineering Agents (Section 4.10), directly relevant to coding agents

## 6. Han che (Limitations)
- No empirical evaluation or quantitative measurement of pattern effectiveness
- Patterns intentionally restrict agent capabilities, which may reduce utility for complex tasks
- No single pattern suffices for all threat models; requires careful application-specific analysis
- Does not address adaptive attacks that might evolve to circumvent specific pattern implementations
- The quarantined LLM in the dual LLM pattern can still produce attacker-influenced outputs

## 7. Dataset & Metric
- **Datasets used:** None (conceptual/design paper with case studies)
- **Evaluation metrics:** Qualitative assessment of utility vs. security trade-offs for each design pattern in each case study

## 8. Ket qua chinh
No quantitative results (this is a design pattern paper). Key qualitative findings:
- The Action-Selector pattern provides the strongest security (trivially immune to injection) but lowest utility
- Plan-Then-Execute provides control flow integrity but cannot prevent parameter manipulation
- Map-Reduce and Dual LLM patterns provide strong isolation but add architectural complexity
- Code-Then-Execute generalizes Plan-Then-Execute with more expressiveness
- Context-Minimization addresses direct prompt injection by removing user prompts after initial processing
- For the Software Engineering Agent case study, the recommended design is Dual LLM with strict data formatting

## 9. Keywords
`design patterns` `prompt injection` `LLM agents` `security` `isolation` `dual LLM` `plan-then-execute` `map-reduce` `action-selector` `software engineering agent`

## 10. Lien quan den de tai
Directly relevant to "Coding Agent Harness & Evaluation" -- Section 4.10 specifically addresses Software Engineering Agents, analyzing threat models where remote documentation or third-party code can hijack coding assistants to write insecure code, import malicious packages, or exfiltrate data. The design patterns (especially Dual LLM with strict data formatting, action sandboxing) provide a framework for building secure coding agent harnesses. An evaluation harness should test whether coding agents implement these patterns and measure their resistance to injection through external resources like coding rules, documentation, and MCP servers.
