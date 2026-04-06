# DE CUONG DE TAI NGHIEN CUU KHOA HOC

---

## TEN DE TAI

**Tieng Viet:**
Khung danh gia da chieu cho ha tang Coding Agent: Tich hop hieu suat, bao mat va kha nang thich ung voi nhieu mo hinh ngon ngu lon

**Tieng Anh:**
HarnessEval: A Multi-Dimensional Evaluation Framework for Coding Agent Infrastructure Integrating Performance, Security, and Backend Portability

**Tu khoa:** Coding Agent, Harness Evaluation, Prompt Injection, SWE-bench, Benchmark, Tool Dispatch, Context Management, Security, LLM Agent

---

## CHUONG 1: MO DAU

### 1.1. Dat van de

Cac coding agent dua tren Mo hinh Ngon ngu Lon (LLM) nhu Claude Code, GitHub Copilot, Cursor va SWE-Agent da tro thanh cong cu thiet yeu trong phat trien phan mem hien dai. Cac agent nay co kha nang tu dong doc code, sua loi, tao tinh nang moi va tuong tac voi he thong file, git, terminal — thay the mot phan lon cong viec thu cong cua lap trinh vien [A1, I1].

Tuy nhien, hieu suat cua mot coding agent khong chi phu thuoc vao LLM co so (Claude, GPT, DeepSeek) ma con phu thuoc rat lon vao **harness** — bo khung ha tang bao gom he thong tool dispatch, quan ly context, lop bao mat (safety layer), va co che quan ly phien lam viec (session management) [A1, A2]. Harness dong vai tro nhu "he dieu hanh" cho agent: cung mot LLM nhung harness khac nhau co the cho ket qua chenh lech lon [A2].

Dong thoi, van de bao mat cua coding agent dang tro nen cap bach. Nghien cuu gan day cho thay 94.4% cac agent de bi tan cong prompt injection [D1], voi ty le thanh cong tan cong len den 84% tren cac coding editor thuong mai [D3]. Dac biet, su co ro ri ma nguon Claude Code (thang 3/2026) da phoi bay toan bo cau truc ha tang cua mot coding agent thuong mai hang dau, lam noi bat nhu cau danh gia bao mat mot cach he thong [D4].

Mac du vay, nghien cuu hien tai ton tai **hai khoang trong nghien cuu (research gap) quan trong**:

**Research Gap 1 — Thieu khung danh gia cap do harness:** Tat ca cac benchmark hien tai (SWE-bench [C1], SWE-Compass [C5], PRDBench [C4]) chi danh gia **dau ra cua agent** (co giai duoc bai toan khong?) ma **khong danh gia ban than harness** (he thong tool co goi dung khong? Context co bi mat thong tin khong? Safety layer co chan duoc lenh nguy hiem khong?). Khong co metric nao do luong chat luong cua harness doc lap voi kha nang cua LLM [S5].

**Research Gap 2 — Thieu benchmark ket hop chinh xac va bao mat:** Cong dong danh gia (C1-C5) va cong dong bao mat (D1-D5) nghien cuu **song song ma khong giao nhau**. SWE-bench do chinh xac nhung bo qua bao mat; AIShellJack [D3] do bao mat nhung khong do chinh xac. Mot agent co the dat 70% resolve rate nhung van de bi prompt injection qua file cau hinh, MCP tool description, hoac code comments doc hai [D3, D4].

### 1.2. Muc dich nghien cuu (dinh tinh)

Nghien cuu nay nham **xay dung mot khung danh gia da chieu** cho ha tang (harness) cua coding agent, cho phep danh gia dong thoi hieu suat tool dispatch, hieu qua quan ly context, kha nang bao mat, tinh lien tuc phien lam viec, va kha nang thich ung voi nhieu LLM backend. Qua do, nghien cuu gop phan **lap day khoang trong** giua danh gia dau ra agent va danh gia ha tang agent, dong thoi **tich hop** danh gia bao mat vao quy trinh danh gia tong the.

### 1.3. Muc tieu nghien cuu (dinh luong)

**MT1.** Xay dung taxonomy 5 chieu danh gia harness (Tool Dispatch Efficiency, Context Utilization, Safety Enforcement, Session Continuity, Backend Portability) voi it nhat 2 metric do luong cho moi chieu.

**MT2.** Xay dung bo benchmark tich hop bao mat (SecureCodeBench) gom 100 coding tasks ket hop voi 4 loai adversarial variants (poisoned coding rules, malicious MCP descriptions, adversarial code comments, dependency confusion), tong cong 400+ evaluation instances.

**MT3.** Thuc hien ablation study tren it nhat 3 cau hinh harness (SWE-Agent, OpenHands, va 1 harness tu xay dung) voi it nhat 2 LLM backends (Claude Sonnet, GPT-4o) tren 200 tasks tu SWE-bench Verified.

**MT4.** De xuat metric tong hop **Secure Resolve Rate = Resolve Rate x (1 - Attack Success Rate)** va xac nhan tinh hieu luc cua metric bang so sanh voi danh gia chuyen gia.

**MT5.** Phat hanh open-source evaluation toolkit (Python) va du lieu benchmark de cong dong co the tai su dung.

### 1.4. Doi tuong va pham vi nghien cuu

**Doi tuong:**
- Ha tang (harness) cua cac coding agent dua tren LLM
- Cac thanh phan harness: tool system, context manager, safety layer, memory store, model backend
- Lo hong bao mat trong coding agent (prompt injection qua coding rules, MCP, code context)

**Pham vi:**
- Tap trung vao coding agents xu ly task cap do repository (repo-level), khong phai function-level
- Su dung SWE-bench Verified (Python) lam benchmark chinh
- Danh gia tren 2-3 LLM backends thuong mai/open-source
- Thoi gian: 6 thang (04/2026 - 10/2026)

### 1.5. Muc luc du kien cua bao cao ket qua NC

- **Chuong 1:** Mo dau (Dat van de, Tong quan tai lieu, Muc dich, Muc tieu, Doi tuong va Pham vi NC)
- **Chuong 2:** Co so ly thuyet (Kien truc coding agent, Harness design, Prompt injection, Evaluation methodology)
- **Chuong 3:** Phuong phap nghien cuu (Thiet ke taxonomy, Xay dung benchmark, Ablation protocol, Metric)
- **Chuong 4:** Ket qua va thao luan (Ket qua ablation, Ket qua bao mat, Phan tich trade-off, So sanh harness)
- **Chuong 5:** Ket luan va huong phat trien de tai
- Tai lieu tham khao & Phu luc

---

## CHUONG 2: TONG QUAN TAI LIEU VA CO SO LY THUYET

### 2.1. Tong quan tai lieu

#### 2.1.1. Kien truc Coding Agent va Harness

Cac tien bo gan day trong coding agent dua tren LLM da chuyen huong tu he thong don agent sang cac kien truc phuc tap hon. Bui et al. (2026) da gioi thieu OpenDev — mot coding agent harness chay tren terminal, nhan manh vao scaffolding, kien truc dual-agent (Planner-Executor) va Adaptive Context Compaction (ACC), giup giam 54% peak token usage [A1]. Lou et al. (2026) de xuat AutoHarness, cho phep LLM tu dong sinh code harness thong qua tinh chinh lap lai, giup model nho vuot troi model lon trong moi truong co rang buoc [A2]. Cao et al. (2026) chung minh coding agents hieu qua trong xu ly long-context bang cach externalize reasoning qua file-system tools, vuot SOTA 17.3% [A3].

#### 2.1.2. He thong Multi-Agent cho phat trien phan mem

Lyu et al. (2026) gioi thieu TheBotCompany — framework tu to chuc multi-agent voi chu ky 3 giai doan (Strategy-Execution-Verification) va doi ngu tu dong tuyen dung/sa thai worker agents [B1]. Hong et al. (2023) de xuat MetaGPT, dung SOP (Standard Operating Procedures) de giam cascading errors trong phat trien phan mem da agent [H3]. Wu et al. (2023) gioi thieu AutoGen voi kien truc conversable agents linh hoat [H1].

#### 2.1.3. Danh gia Coding Agent va van de Benchmark

Deng et al. (2025) gioi thieu SWE-Bench Pro voi 1,865 tasks phuc tap tu codebase thuong mai, chong contamination bang copyleft license [C1]. Tuy nhien, Prathifkumar et al. (2025) phat hien bang chung cho thay LLM co the ghi nho (memorize) patches tu training data thay vi suy luan that su — Claude giai dinh vi file tot hon 3-6x tren SWE-bench so voi benchmark moi [C3]. Thai et al. (2025) de xuat SWE-EVO cho long-horizon software evolution, trong do model tot nhat chi dat 21% so voi 65% tren SWE-bench Verified [C2]. Survey ve danh gia agent cho thay 8/10 benchmark pho bien co van de nghiem trong — agent "khong lam gi" van pass 38% tasks [S5].

**Dac biet quan trong:** Tat ca benchmark tren chi danh gia **dau ra** (output) cua agent. Khong co benchmark nao danh gia **ha tang** (harness) — he thong tool, context management, safety layer — mot cach doc lap.

#### 2.1.4. Bao mat Coding Agent

Chhabra et al. (2025) cung cap taxonomy toan dien ve moi de doa cho agentic AI, cho thay 94.4% agents de bi prompt injection [D1]. Liu et al. (2025) gioi thieu AIShellJack — framework tan cong dau tien cho coding editor, voi 314 payloads bao phu 70 ky thuat MITRE ATT&CK, dat ty le tan cong thanh cong 41-84% [D3]. Maloyan & Namiot (2026) phan tich he thong lo hong trong skills, tools va protocol ecosystems cua coding assistant, chung minh tat ca 12 co che phong thu bi bypass voi ty le 78%+ [D4]. Beurer-Kellner et al. (2025) de xuat 6 design patterns phong thu (Plan-Then-Execute, Dual LLM, ...) nhung chua benchmark tren coding tasks [D2].

**Research gap ro rang:** Bao mat va chinh xac luon duoc danh gia rieng re. Chua co benchmark nao ket hop ca hai.

#### 2.1.5. He thong Memory va Context Management

Chhikara et al. (2025) gioi thieu Mem0 voi 91% giam latency va 90% giam token cost [E1]. Xu et al. (2025) de xuat A-Mem lay cam hung tu Zettelkasten [E2]. Yu et al. (2026) huan luyen memory policy bang RL, dat 49.59% cai thien [E3]. Tuy nhien, tat ca deu test tren chatbot/QA benchmarks (LoCoMo, DialSim), khong phai coding tasks. Wang et al. (2025) phat hien agent lap lai cung bug qua nhieu iterations vi thieu persistent memory [I2].

#### 2.1.6. Tom tat Research Gap

Tong hop tu 49 papers, nghien cuu nay nhan dien 2 khoang trong chinh:

| Research Gap | Mo ta | Papers gan nhat | Tai sao chua ai lam |
|---|---|---|---|
| **Gap 1: Harness-Level Evaluation** | Chua co framework danh gia harness (tool, context, safety) doc lap voi LLM | A1, B10, S5 | Khai niem "harness" moi (2026); harness bi xem la engineering artifact |
| **Gap 2: Security-Integrated Benchmark** | Bao mat va chinh xac luon danh gia rieng | D3, C1, C5 | 2 cong dong nghien cuu song song |

### 2.2. Co so ly thuyet

#### 2.2.1. Kien truc Coding Agent Harness

Dua tren framework Profile-Memory-Planning-Action cua Wang et al. (2023) [S1] va kien truc 4 lop cua OpenDev [A1], mot coding agent harness bao gom:

1. **Model Backend Layer:** LLM co so (Claude, GPT, DeepSeek, ...)
2. **Tool System Layer:** Tap hop tools (Read, Write, Edit, Bash, Glob, Grep, ...) va co che dispatch
3. **Context Management Layer:** Quan ly context window, compaction, memory
4. **Safety & Permission Layer:** Sandboxing, permission model, input validation
5. **Orchestration Layer:** Agent loop (ReAct, Plan-Execute), multi-turn management

#### 2.2.2. Prompt Injection va cac vector tan cong Coding Agent

Dua tren taxonomy cua Chhabra et al. [D1] va Maloyan & Namiot [D4]:

- **Direct injection:** Adversarial instructions trong user prompt
- **Indirect injection qua coding context:** Payloads an trong code comments, docstrings, README
- **Indirect injection qua tool ecosystem:** Malicious MCP tool descriptions, poisoned coding rules (.cursorrules, .clinerules, CLAUDE.md)
- **Supply chain injection:** Dependency confusion, malicious packages

#### 2.2.3. Evaluation Methodology

- **Pass@k:** Ty le giai dung sau k lan thu [C1]
- **Progress Rate:** Do luong tien do tung buoc thay vi chi ket qua cuoi [G3]
- **Agent-as-a-Judge:** Dung LLM danh gia LLM, dat 87% alignment voi human [S5]
- **Ablation Study:** Tat/bat tung component de do dong gop — phuong phap chuan trong ML evaluation
- **MITRE ATT&CK:** Framework phan loai ky thuat tan cong — dung de taxonomy adversarial payloads [D3]

---

## CHUONG 3: PHUONG PHAP NGHIEN CUU

### 3.1. Tong quan phuong phap

Nghien cuu nay su dung phuong phap **thuc nghiem** (experimental), bao gom:

1. **Thiet ke taxonomy** danh gia harness (ly thuyet + chuyen gia)
2. **Xay dung benchmark** tich hop bao mat (engineering + manual curation)
3. **Ablation study** he thong (thuc nghiem dinh luong)
4. **Phan tich thong ke** ket qua (dinh luong + dinh tinh)

### 3.2. Thiet ke Taxonomy 5 Chieu Danh Gia Harness (MT1)

```
                    HarnessEval Framework
    ┌────────────────────────────────────────────┐
    │                                            │
    │  Dim 1: Tool Dispatch Efficiency           │
    │    M1.1: Correct Tool Selection Rate (%)   │
    │    M1.2: Avg Tool Call Latency (ms)        │
    │    M1.3: Redundant Tool Calls (%)          │
    │                                            │
    │  Dim 2: Context Utilization                │
    │    M2.1: Info Retention after Compaction (%)│
    │    M2.2: Token Waste Ratio (%)             │
    │                                            │
    │  Dim 3: Safety Enforcement                 │
    │    M3.1: Destructive Op Block Rate (%)     │
    │    M3.2: Prompt Injection Resist Rate (%)  │
    │    M3.3: Secure Resolve Rate (composite)   │
    │                                            │
    │  Dim 4: Session Continuity                 │
    │    M4.1: Performance @ Turn 50 vs 200 (%)  │
    │    M4.2: Instruction Adherence Rate (%)    │
    │                                            │
    │  Dim 5: Backend Portability                │
    │    M5.1: Cross-Backend Variance (std dev)  │
    │    M5.2: Min/Max Performance Ratio         │
    │                                            │
    └────────────────────────────────────────────┘
```

**Phuong phap xay dung:** Rut ra tu phan tich 49 papers (Gap Analysis), mapping limitations cua tung paper sang measurable properties. Validate voi 2-3 chuyen gia (advisor + industry practitioners).

### 3.3. Xay dung SecureCodeBench (MT2)

**Du lieu goc:** 100 tasks tu SWE-bench Verified (Python, da co Docker environment)

**Tao adversarial variants:**

| Loai tan cong | Mo ta | So luong | Nguon tham khao |
|---|---|---|---|
| Poisoned Coding Rules | Chen instruction doc hai vao .cursorrules/.clinerules | 100 | D4 (Maloyan) |
| Malicious MCP Tool Desc | Chen payload vao tool description | 100 | D1 (Chhabra) |
| Adversarial Code Comments | Chen instruction an trong comments/docstrings | 100 | D3 (AIShellJack) |
| Dependency Confusion | Them package khong ton tai vao requirements.txt | 100 | MITRE ATT&CK |

**Mapping MITRE ATT&CK:** Chon 20 ky thuat phu hop coding context tu 70 ky thuat cua D3:
- Execution (T1059): Command injection qua tool calls
- Exfiltration (T1048): Data theft qua curl/wget trong bash
- Persistence (T1546): Chen backdoor vao code
- Discovery (T1083): Doc file nhay cam (/etc/passwd, .env)
- Impact (T1485): Xoa/ghi de file quan trong

**Metric do luong:**
- **Resolve Rate (RR):** % tasks giai dung (standard SWE-bench metric)
- **Attack Success Rate (ASR):** % adversarial payloads bi thuc thi
- **Secure Resolve Rate (SRR) = RR x (1 - ASR):** Metric tong hop

### 3.4. Ablation Study Protocol (MT3)

**Cau hinh thuc nghiem:**

| Bien doc lap | Gia tri | |
|---|---|
| Harness | SWE-Agent, OpenHands, Modular Harness (tu xay dung) |
| LLM Backend | Claude Sonnet 4, GPT-4o |
| Tool Configuration | Full tools / Limited tools / No file-edit |
| Context Strategy | Full context / Sliding window / ACC (5-stage) |
| Safety Layer | None / Rule-based / LLM-judge |

**Bien phu thuoc:** Resolve Rate, ASR, SRR, 11 metrics khac tu taxonomy

**So luong runs:** 3 harnesses x 2 backends x 3 tool configs x 3 context configs x 3 safety configs = 162 conditions (tren 200 tasks moi condition)

**Toi uu chi phi:** Uu tien cac conditions co thay doi lon, cat bo cac conditions trung lap. Du kien chay khoang 50 conditions quan trong nhat.

### 3.5. Validation Metric SRR (MT4)

- Thu thap danh gia chuyen gia (3-5 nguoi) tren 30 agent outputs
- Tinh Pearson/Spearman correlation giua SRR va expert ranking
- So sanh voi single-axis metrics (RR alone, ASR alone)
- Muc tieu: correlation > 0.85 voi expert judgment

### 3.6. Open-source Toolkit (MT5)

```
harness-eval/
├── taxonomy/           # Dinh nghia 5 dimensions + metrics
├── benchmark/          
│   ├── tasks/          # 100 clean + 400 adversarial tasks
│   ├── attacks/        # 20 MITRE ATT&CK templates
│   └── environments/   # Docker configs
├── harnesses/          
│   ├── modular/        # Harness tu xay dung (Python)
│   ├── swe_agent/      # Adapter cho SWE-Agent
│   └── openhands/      # Adapter cho OpenHands
├── evaluation/         
│   ├── metrics.py      # 11+ metrics
│   ├── ablation.py     # Ablation runner
│   └── visualize.py    # Charts, tables
└── results/            # Raw data + analysis
```

---

## CHUONG 4: DU KIEN KET QUA NGHIEN CUU

### 4.1. Du kien ket qua theo tung muc tieu

**MT1 — Taxonomy:** Bang phan loai 5 chieu, 11+ metrics, validated boi chuyen gia. Dong gop: **taxonomy dau tien** cho harness evaluation — chua co paper nao lam.

**MT2 — SecureCodeBench:** 400+ evaluation instances voi 4 loai tan cong. Dong gop: **benchmark dau tien** ket hop correctness + security.

**MT3 — Ablation Results:** Bang ket qua 50+ conditions cho thay:
- Dong gop cua tung component (tool, context, safety) vao resolve rate
- Trade-off giua safety va performance
- Harness nao tot nhat cho tung loai task
- LLM backend nao it phu thuoc harness nhat

**MT4 — Metric SRR:** Composite metric co correlation > 0.85 voi expert. Cho phep ranking agent toan dien hon.

**MT5 — Toolkit:** Open-source Python package de cong dong tai su dung.

### 4.2. Y nghia khoa hoc

- **Dong gop moi:** Lan dau tien danh gia harness (khong chi output) cua coding agent
- **Khai niem moi:** Taxonomy 5 chieu cho harness quality
- **Metric moi:** Secure Resolve Rate ket hop correctness + security
- **Benchmark moi:** SecureCodeBench — dual-axis evaluation

### 4.3. Y nghia thuc tien

- Giup cac to chuc **chon harness phu hop** (khong chi chon model)
- Giup cac developer **phat hien lo hong bao mat** trong coding agent truoc khi deploy
- Cung cap **guidelines thiet ke harness** dua tren du lieu thuc nghiem
- Open-source toolkit cho cong dong nghien cuu va cong nghiep

---

## CHUONG 5: KE HOACH THUC HIEN

### 5.1. Tien do du kien

| Giai doan | Thoi gian | Noi dung | Ket qua |
|-----------|-----------|----------|---------|
| GD1 | Thang 4-5/2026 | Hoan thien taxonomy + thiet ke benchmark | Taxonomy 5 chieu, 100 tasks chon, 400 adversarial variants |
| GD2 | Thang 5-6/2026 | Xay dung modular harness + toolkit | Python package, Docker environments, adapter cho SWE-Agent/OpenHands |
| GD3 | Thang 6-8/2026 | Chay thuc nghiem ablation + security | Du lieu tho 50+ conditions x 200 tasks |
| GD4 | Thang 8-9/2026 | Phan tich ket qua + validate SRR metric | Bang ket qua, bieu do, expert validation |
| GD5 | Thang 9-10/2026 | Viet luan van + hoan thien toolkit | Luan van hoan chinh, toolkit phat hanh tren GitHub |

### 5.2. Nhan su

| Vai tro | Nguoi | Trach nhiem |
|---------|-------|-------------|
| Nghien cuu sinh | [Ten ban] | Thiet ke, implement, thuc nghiem, viet luan van |
| Giang vien huong dan | [Ten advisor] | Dinh huong, phan bien, ho tro publish |

### 5.3. Tai nguyen

| Tai nguyen | Chi tiet | Chi phi du kien |
|-----------|----------|----------------|
| LLM API | Claude Sonnet, GPT-4o (200 tasks x 50+ conditions) | $500-1,000 |
| Compute | Docker environments cho SWE-bench | May ca nhan hoac cloud |
| Open-source tools | SWE-Agent, OpenHands, SWE-bench Verified | Mien phi |

---

## TAI LIEU THAM KHAO

### A. Harness & Architecture
[A1] N. D. Q. Bui et al., "Building Effective AI Coding Agents for the Terminal: Scaffolding, Harness, Context Engineering, and Lessons Learned," arXiv:2603.05344, Mar. 2026.
[A2] X. Lou et al., "AutoHarness: Improving LLM Agents by Automatically Synthesizing a Code Harness," arXiv:2603.03329, Feb. 2026.
[A3] W. Cao et al., "Coding Agents are Effective Long-Context Processors," arXiv:2603.20432, Mar. 2026.

### B. Multi-Agent Coding
[B1] W. Lyu et al., "Self-Organizing Multi-Agent Systems for Continuous Software Development," arXiv:2603.25928, Mar. 2026.
[B2] N. Loose et al., "Coverage-Guided Multi-Agent Harness Generation for Java Library Fuzzing," arXiv:2603.08616, Mar. 2026.
[B10] M. Robeyns et al., "A Self-Improving Coding Agent," arXiv:2504.15228, May 2025.

### C. Evaluation & Benchmarks
[C1] X. Deng et al., "SWE-Bench Pro: Can AI Agents Solve Long-Horizon Software Engineering Tasks?" arXiv:2509.16941, Sep. 2025.
[C2] M. V. T. Thai et al., "SWE-EVO: Benchmarking Coding Agents in Long-Horizon Software Evolution Scenarios," arXiv:2512.18470, Dec. 2025.
[C3] T. Prathifkumar et al., "Does SWE-Bench-Verified Test Agent Ability or Model Memory?" arXiv:2512.10218, Dec. 2025.
[C4] L. Fu et al., "Automatically Benchmarking LLM Code Agents through Agent-Driven Annotation and Evaluation," arXiv:2510.24358, Oct. 2025.
[C5] J. Xu et al., "SWE-Compass: Towards Unified Evaluation of Agentic Coding Abilities for LLMs," arXiv:2511.05459, Nov. 2025.

### D. Security & Safety
[D1] A. Chhabra et al., "Agentic AI Security: Threats, Defenses, Evaluation, and Open Challenges," arXiv:2510.23883, Oct. 2025.
[D2] L. Beurer-Kellner et al., "Design Patterns for Securing LLM Agents against Prompt Injections," arXiv:2506.08837, Jun. 2025.
[D3] Y. Liu et al., "'Your AI, My Shell': Demystifying Prompt Injection Attacks on Agentic AI Coding Editors," arXiv:2509.22040, Sep. 2025.
[D4] N. Maloyan and D. Namiot, "Prompt Injection Attacks on Agentic Coding Assistants: A Systematic Analysis of Vulnerabilities in Skills, Tools, and Protocol Ecosystems," arXiv:2601.17548, Jan. 2026.
[D5] S. M. A. Hossain et al., "A Multi-Agent LLM Defense Pipeline Against Prompt Injection Attacks," arXiv:2509.14285, Sep. 2025.

### E. Memory & Context
[E1] P. Chhikara et al., "Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory," arXiv:2504.19413, Apr. 2025.
[E2] W. Xu et al., "A-MEM: Agentic Memory for LLM Agents," arXiv:2502.12110, Feb. 2025.
[E3] Y. Yu et al., "Agentic Memory: Learning Unified Long-Term and Short-Term Memory Management for LLM Agents," arXiv:2601.01885, Jan. 2026.

### F-G. Tool-Use & Planning
[F2] Y. Qin et al., "ToolLLM: Facilitating Large Language Models to Master 16000+ Real-world APIs," arXiv:2307.16789, 2023.
[F4] C. Qu et al., "Tool Learning with Large Language Models: A Survey," arXiv:2405.17935, 2024.
[G1] X. Huang et al., "Understanding the Planning of LLM Agents: A Survey," arXiv:2402.02716, 2024.
[G3] C. Ma et al., "AgentBoard: An Analytical Evaluation Board of Multi-Turn LLM Agents," arXiv:2401.13178, 2024.

### H. Multi-Agent Frameworks
[H1] Q. Wu et al., "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation," arXiv:2308.08155, 2023.
[H3] S. Hong et al., "MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework," arXiv:2308.00352, 2023.

### I. Industry & Practice
[I1] J. Wang et al., "AI Agentic Programming Survey," arXiv:2508.11126, Aug. 2025.
[I2] J. Wang et al., "Illuminating LLM Coding Agents: Visual Analytics for Deeper Understanding and Enhancement," arXiv:2508.12555, Aug. 2025.

### S. Surveys
[S1] L. Wang et al., "A Survey on Large Language Model based Autonomous Agents," arXiv:2308.11432, 2023.
[S5] "Survey on Evaluation of LLM-based Agents," arXiv:2503.16416, 2025.
