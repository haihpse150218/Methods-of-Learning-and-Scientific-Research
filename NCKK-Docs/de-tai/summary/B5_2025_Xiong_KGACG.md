# [2025] Xiong — Knowledge-Guided Multi-Agent Framework for Application-Level Software Code Generation (KGACG)

## Metadata
- **arXiv:** 2510.19868v1
- **Venue:** (preprint, arXiv cs.SE)
- **Year:** 2025
- **Authors:** Qian Xiong, Bo Yang (Beijing Forestry University), Weisong Sun, Yiran Zhang, Tianlin Li, Yang Liu (Nanyang Technological University), Zhi Jin (Wuhan University)

## 1. Van de (Problem)
Automated code generation driven by LLMs has enhanced development efficiency, yet generating complex application-level software code remains challenging. Existing methods perform inadequately in large-scale application-level code generation, failing to ensure reasonable organizational structures of project code and making it difficult to maintain the code generation process across multi-file repositories.

## 2. Dong co / Gap
Single LLM pipelines reveal three systematic deficits for application-level code: (1) context isolation -- the model sees only the current prompt and cannot reason over multi-file repositories; (2) lack of grounding -- generated code is rarely executed or tested, allowing silent semantic errors to propagate; (3) absence of iteration -- the session ends after one response, preventing self-correction loops. While multi-agent frameworks have started to address these issues, existing methods struggle with large-scale code projects, failing to handle multicomponent coordination, diverse requirement adaptation, and long-term maintainability. Generated code often neglects readability and accumulates technical debt.

## 3. Phuong phap (Method)
KGACG is a three-agent collaborative framework that transforms Software Requirements Specification (SRS) and Architectural Design Document (ADD) into executable code through iterative feedback:

1. **COPA (Code Organization & Planning Agent):**
   - Analyzes SRS and ADD to extract business processes, module specifications, and constraints
   - Generates a detailed code implementation plan (code plan) with implementation order, class hierarchies, access modifiers, and method interface specifications
   - Creates project directory structures with package layouts, entry points, and dependency configurations
   - Draws on knowledge bases: SRS/ADD knowledge (functional requirements, user stories), ADDs (interface contracts, design patterns), and Standards (IEEE 830, ISO 29148)

2. **CA (Coding Agent):**
   - Generates executable source code following COPA's plan and project structure
   - Consults Coding Knowledge base: Open Source Projects, API Library, Domain Experts, Coding Standards, and Coding Tools
   - Performs third-party API analysis, code generation following dependency graphs, just-in-time compilation and self-debugging
   - Code rectification: analyzes error reports from TA or compilation, determines root causes, generates targeted fixes

3. **TA (Testing Agent):**
   - Generates test plans from SRS/ADD, mapping functional requirements to test boundaries and scope
   - Generates test cases using equivalence partitioning and boundary value analysis (one positive, one negative, one invalid input, one boundary pair per method)
   - Executes unit tests, evaluates results, compiles test reports with coverage, pass/fail status, defect classification, and traceability links
   - Dynamically updates tests when SRS, ADD, or generated code changes

**Feedback loop:** TA test reports feed back to CA for code fixes; compilation errors trigger COPA to cross-reference with original SRS/ADD and update the plan; COPA updates synchronize to CA for incremental rebuilding.

## 4. Dong gop chinh (Contributions)
- A knowledge-guided multi-agent framework (KGACG) with three specialized agents (COPA, CA, TA) for application-level code generation from SRS and ADD documents
- Structured knowledge bases for each agent: SRS/ADD Knowledge, Coding Knowledge (5 pillars), and Testing Knowledge (4 pillars)
- A closed-loop feedback mechanism connecting planning, coding, and testing agents for iterative optimization
- A case study demonstrating the framework on a Java Tank Battle game application

## 5. Diem manh (Strengths)
- Addresses the full pipeline from requirements documents (SRS/ADD) to executable, tested code -- more comprehensive than code-only generation
- Knowledge-guided approach with curated domain knowledge bases (standards, coding conventions, testing criteria) grounds agent behavior in established software engineering practices
- Strong traceability: test cases are annotated with requirement IDs and method signatures, enabling automatic regeneration when specifications change
- Structured plan documents (JSON format) enable incremental rebuilding and module reuse, reducing redundancy
- Testing agent uses systematic test design techniques (equivalence partitioning, boundary value analysis) aligned with ISTQB standards

## 6. Han che (Limitations)
- Only a vision/framework paper with a single illustrative case study (Java Tank Battle game); no quantitative evaluation or benchmarking
- No comparison with existing multi-agent code generation frameworks (ChatDev, MetaGPT, AgileCoder)
- Assumes availability of detailed SRS and ADD documents, which may not exist in many real-world projects
- Scalability to large, complex industrial codebases is not demonstrated
- The knowledge bases (Open Source Projects, Domain Experts, etc.) are described conceptually but their construction and maintenance are not detailed

## 7. Dataset & Metric
- **Evaluation:** Single case study -- Java Tank Battle game (JavaFX-based)
- **No formal metrics reported** -- the paper demonstrates the collaborative process through a walkthrough example
- **Artifacts shown:** Code implementation plan (JSON), project directory structure, third-party API list, generated source code (GameStateData class), unit tests (CollisionCheckerTest), test reports

## 8. Ket qua chinh
- Case study walkthrough: COPA analyzed SRS/ADD for Tank Battle game, produced JSON implementation plan with dependency graph and package structure
- CA generated GameStateData class and integrated JavaFX APIs following COPA's plan
- During compilation, CA resolved NullPointerException in CollisionChecker by requesting COPA plan updates via feedback loop
- TA designed unit tests (GameStateDataTest, CollisionCheckerTest) using boundary value analysis, identified a defect in checkCollision method (failed to detect diagonal tank collisions)
- TA generated structured test report (3 tests total, 3 failed at 100% failure rate in the example), providing step-by-step modification instructions

## 9. Keywords
multi-agent framework, application-level code generation, knowledge-guided, software requirements specification, architectural design document, LLM, code planning, testing agent, feedback loop, KGACG

## 10. Lien quan den de tai
Relevant to "Coding Agent Harness & Evaluation" as a framework design reference for structured multi-agent code generation. KGACG's three-agent architecture (planning, coding, testing) with a closed feedback loop demonstrates a pattern where the testing agent effectively serves as an evaluation harness for the coding agent's output. The knowledge-guided approach (curated standards, coding conventions, testing criteria) and traceability between requirements and test cases are relevant design patterns for evaluation frameworks. However, the paper lacks empirical validation and benchmarking, limiting its evidential contribution. The emphasis on SRS/ADD as inputs distinguishes it from benchmark-oriented evaluation approaches.
