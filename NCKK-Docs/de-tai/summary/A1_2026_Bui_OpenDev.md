# [2026] Bui — Building Effective AI Coding Agents for the Terminal: Scaffolding, Harness, Context Engineering, and Lessons Learned

## Metadata
- **arXiv:** 2603.05344v3
- **Venue:** arXiv preprint (cs.AI)
- **Year:** 2026
- **Authors:** Nghi D. Q. Bui

## 1. Van de (Problem)
AI coding assistance is shifting from IDE plugins to terminal-native agents that operate directly where developers manage source control, execute builds, and deploy environments. However, building production-ready CLI-based coding agents requires solving three fundamental engineering challenges: managing finite context windows over long sessions, preventing destructive operations when the agent executes arbitrary shell commands, and extending capabilities without overwhelming the prompt budget.

## 2. Dong co / Gap
Most production terminal-native agentic tools are closed-source with undocumented architectural decisions, and existing open-source frameworks either target benchmarks rather than interactive use or lack published technical reports. There is no comprehensive open-source technical report documenting the design decisions, trade-offs, and lessons learned for building a production-grade, terminal-native, interactive coding agent. Three critical open questions remain: how multi-model architectures should balance cost/latency/capability, how safety mechanisms prevent destructive operations, and how systems sustain long-running conversations within finite context limits.

## 3. Phuong phap (Method)
OpenDev is a compound AI system (not a single monolithic LLM) written in Rust, organized into four architectural layers: Entry & UI, Agent, Tool & Context, and Persistence. Key methods include:
- **Per-workflow LLM binding architecture:** Five specialized model roles (Action, Thinking, Critique, Vision, Compact) each independently configurable per workflow.
- **Extended ReAct execution loop:** Extends standard ReAct with explicit thinking phases, optional self-critique, and staged context compaction integrated directly into the reasoning loop.
- **Dual-agent architecture:** Separates planning (read-only Planner subagent) from execution (Normal Mode with full access), enforced at the schema level rather than runtime permission checks.
- **Adaptive Context Compaction:** Five-stage progressive compaction triggered by token utilization thresholds (70% warning, 80% masking, 85% pruning, 90% aggressive masking, 99% full LLM summarization).
- **Defense-in-depth safety:** Five independent safety layers from prompt-level guardrails down to user-defined lifecycle hooks.
- **Event-driven system reminders:** Inject targeted behavioral guidance at decision points to counteract instruction fade-out in long sessions.

## 4. Dong gop chinh (Contributions)
- Per-workflow LLM configurability via a compound AI architecture enabling fine-grained cost/latency/capability trade-offs
- Extended ReAct execution pipeline with explicit thinking, optional self-critique, and staged context compaction
- Behavioral steering over long horizons through event-driven system reminders and conditional prompt composition
- Token-efficient extensibility via registry-based tool architecture with lazy MCP tool discovery, and a five-layer defense-in-depth safety architecture
- Context engineering as a first-class concern: Adaptive Context Compaction, event-driven reminders, and experience-driven memory pipeline (ACE playbook)

## 5. Diem manh (Strengths)
- Extremely detailed and transparent engineering report bridging the gap between closed-source industrial practice and open academic discourse
- Comprehensive four-layer architecture with clean separation of concerns (scaffolding vs. harness, commands vs. tools, plan mode vs. normal mode)
- Practical safety architecture with five independent layers; failure of any single layer does not compromise the remaining four
- Model-agnostic design: switching providers requires only configuration changes, not code changes
- Open-source implementation in Rust with reproducible design decisions and configuration schemas

## 6. Han che (Limitations)
- No formal benchmark evaluation results reported in the first 15 pages; the paper explicitly states its purpose is not to present a novel algorithmic breakthrough but to share design decisions and lessons learned
- Single-author system report, so design decisions may reflect individual preferences rather than community-validated best practices
- The five-stage compaction thresholds (70%, 80%, 85%, 90%, 99%) appear to be hand-tuned heuristics without empirical justification for the specific values
- Complexity of the system (five model roles, five safety layers, four architectural layers, six ReAct phases) may create steep learning curves for contributors

## 7. Dataset & Metric
Not explicitly evaluated on standard benchmarks within the first 15 pages. The paper references Terminal-Bench and LongCLI-Bench as motivating benchmarks but does not report OpenDev's scores on them.

## 8. Ket qua chinh
The paper is primarily a systems/engineering contribution rather than an empirical evaluation paper. Key engineering results include:
- A working open-source terminal-native coding agent with dual-mode (Plan/Normal) operation
- Successful elimination of brittle state-machine designs for plan mode by delegating to schema-isolated subagents
- Progressive context compaction that avoids expensive full LLM summarization in most cases by applying cheaper strategies (masking, pruning) first
- Doom-loop detection via MD5 fingerprinting of repeated tool calls (threshold >= 3 repetitions)

## 9. Keywords
`coding-agent` `terminal-native` `CLI` `context-engineering` `ReAct` `scaffolding` `harness` `compound-AI-system` `safety` `multi-model-architecture` `context-compaction` `open-source`

## 10. Lien quan den de tai
Directly relevant to the thesis on "Coding Agent Harness & Evaluation." OpenDev provides a detailed reference architecture for both the scaffolding (agent construction before the first prompt) and harness (runtime orchestration including tool dispatch, context management, safety enforcement) of a coding agent. The paper's explicit distinction between scaffolding and harness, its five-layer safety architecture, and its Adaptive Context Compaction mechanism are all central concepts for understanding how coding agent harnesses are designed and evaluated. The discussion of design trade-offs (e.g., eager vs. lazy prompt building, state-machine vs. subagent planning) provides valuable engineering lessons for the thesis.
