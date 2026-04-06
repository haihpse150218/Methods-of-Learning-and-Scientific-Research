# DE CUONG DE TAI NGHIEN CUU KHOA HOC
# Huong 2: SecureCodeBench — Benchmark bao mat cho Coding Agent

---

## TEN DE TAI

**Tieng Viet:**
SecureCodeBench: Benchmark hai truc danh gia dong thoi do chinh xac va do khang bao mat cua Coding Agent

**Tieng Anh:**
SecureCodeBench: A Dual-Axis Benchmark for Evaluating Coding Agents on Both Correctness and Security Resistance

**Tu khoa:** Coding Agent, Security, Prompt Injection, Benchmark, MITRE ATT&CK, SWE-bench, Adversarial Evaluation, Coding Rules, MCP, Attack Success Rate

---

## CHUONG 1: MO DAU

### 1.1. Dat van de

Coding agent dua tren Mo hinh Ngon ngu Lon (LLM) dang duoc trien khai rong rai trong cac to chuc phat trien phan mem. Cac cong cu nhu Claude Code, GitHub Copilot, Cursor co quyen truy cap truc tiep vao file system, terminal, git va cac API ben ngoai — tao ra **bien phap tan cong rong lon** (large attack surface) ma cac ung dung LLM truyen thong (chatbot) khong co [D1, D4].

**Thuc trang bao mat dang bao dong:**
- 94.4% cac LLM agent de bi prompt injection [D1]
- Tan cong qua coding editors (Cursor, Copilot) dat ty le thanh cong 41-84% [D3]
- Tat ca 12 co che phong thu duoc danh gia deu bi bypass voi ty le 78%+ [D4]
- Su co ro ri ma nguon Claude Code (03/2026) phoi bay toan bo kien truc harness, bao gom 26 hidden slash commands, 32 secret CLI flags va cac co che bypass safety [D4]

**Tuy nhien, ton tai mot research gap nghiem trong:** Hai cong dong nghien cuu **chay song song ma khong giao nhau**:

| Cong dong | Nghien cuu | Do | Bo qua |
|-----------|-----------|-----|--------|
| **Evaluation** (C1-C5) | Benchmark chinh xac (resolve rate) | Coding performance | Bao mat |
| **Security** (D1-D5) | Lo hong, tan cong, phong thu | Attack success rate | Coding performance |

Hau qua: Mot coding agent co the dat **70% resolve rate** tren SWE-bench (duoc coi la tot) nhung dong thoi **de bi tan cong 84%** qua prompt injection an trong file cau hinh [D3]. Nguoi dung khong co cach nao biet agent vua giai quyet bug vua bi khai thac de thuc thi lenh doc hai.

**Chua co benchmark nao** cho phep danh gia **dong thoi** ca correctness va security cua coding agent. Day la research gap ma nghien cuu nay nham giai quyet.

### 1.2. Muc dich nghien cuu (dinh tinh)

Nghien cuu nay nham **xay dung benchmark hai truc dau tien** cho phep danh gia coding agent dong thoi tren ca do chinh xac (correctness) va do khang bao mat (security resistance). Qua do, cung cap cong cu cho cong dong nhan dien va giam thieu rui ro bao mat khi trien khai coding agent.

### 1.3. Muc tieu nghien cuu (dinh luong)

**MT1.** Xay dung taxonomy 4 loai tan cong dac trung cho coding agent (poisoned coding rules, malicious MCP descriptions, adversarial code context, dependency confusion), mapping voi 20 ky thuat MITRE ATT&CK.

**MT2.** Xay dung SecureCodeBench gom 100 coding tasks ket hop voi 4 loai adversarial variants, tong cong 500 evaluation instances (100 clean + 400 adversarial).

**MT3.** Danh gia it nhat 4 coding agents (2 open-source: SWE-Agent, OpenHands; 2 commercial: Claude Code, Cursor) tren SecureCodeBench, do dong thoi Resolve Rate va Attack Success Rate.

**MT4.** De xuat va validate metric tong hop **Secure Resolve Rate (SRR) = RR x (1 - ASR)**, xac nhan correlation > 0.85 voi expert ranking.

**MT5.** Phan tich trade-off giua performance va security: them safety layer co giam resolve rate bao nhieu? Design pattern nao (tu D2) hieu qua nhat?

**MT6.** Phat hanh open-source benchmark dataset va evaluation toolkit tren GitHub.

### 1.4. Doi tuong va pham vi nghien cuu

**Doi tuong:**
- Coding agents dua tren LLM (ca open-source va commercial)
- Lo hong bao mat trong coding agent: prompt injection qua coding rules, MCP tools, code context, dependencies
- Trade-off giua correctness va security

**Pham vi:**
- 100 coding tasks tu SWE-bench Verified (Python)
- 4 loai adversarial variants x 100 = 400 adversarial instances
- 4 coding agents: SWE-Agent, OpenHands, Claude Code, Cursor
- 20 ky thuat MITRE ATT&CK mapping cho coding context
- Thoi gian: 6 thang

### 1.5. Muc luc du kien

- **Chuong 1:** Mo dau (Dat van de, Tong quan tai lieu, Muc dich, Muc tieu)
- **Chuong 2:** Co so ly thuyet (Coding agent security, Prompt injection taxonomy, MITRE ATT&CK, Evaluation methodology)
- **Chuong 3:** Phuong phap nghien cuu (Benchmark construction, Attack design, Metric design, Evaluation protocol)
- **Chuong 4:** Ket qua va thao luan (Agent comparison, Trade-off analysis, Defense effectiveness, Vulnerability patterns)
- **Chuong 5:** Ket luan va huong phat trien
- Tai lieu tham khao & Phu luc

---

## CHUONG 2: TONG QUAN TAI LIEU VA CO SO LY THUYET

### 2.1. Tong quan tai lieu

#### 2.1.1. Bao mat cua LLM Agent va Coding Agent

Chhabra et al. (2025) cung cap taxonomy toan dien ve moi de doa cho agentic AI, phan loai thanh: prompt injection, cyber exploitation, multi-agent threats, MCP/A2A threats, interface risks va governance challenges. Nghien cuu cho thay 94.4% agents de bi prompt injection, 83.3% de bi retrieval backdoors, va 100% de bi inter-agent trust exploits [D1].

Liu et al. (2025) gioi thieu AIShellJack — framework tan cong tu dong dau tien cho coding editors. Voi 314 payloads bao phu 70 ky thuat MITRE ATT&CK, AIShellJack dat ty le tan cong 41-84% tren Cursor va GitHub Copilot. Dac biet nguy hiem: tan cong qua file `.cursorrules` — file cau hinh ma nhieu developer chia se cong khai tren GitHub [D3].

Maloyan & Namiot (2026) trinh bay SoK (Systematization of Knowledge) tong hop 78 nghien cuu ve prompt injection tren coding assistant. Ho de xuat taxonomy 3 chieu (delivery vector, modality, propagation), catalog 42 ky thuat tan cong, va document exploit chains dac thu cho Claude Code va Copilot. Ket qua dang lo ngai: **tat ca 12 co che phong thu duoc danh gia deu bi bypass voi ty le 78%+** duoi tan cong thich ung [D4].

Beurer-Kellner et al. (2025) de xuat 6 design patterns phong thu: Action-Selector, Plan-Then-Execute, Map-Reduce, Dual LLM, Code-Then-Execute, Context-Minimization. Dac biet, pattern Plan-Then-Execute dam bao tool call outputs khong the inject instructions lam lech agent khoi ke hoach. Tuy nhien, cac patterns **chua duoc benchmark tren coding tasks thuc te** [D2].

Hossain et al. (2025) de xuat multi-agent defense pipeline (chain-of-agents va coordinator) giam ASR tu 20-30% xuong 0% tren 400 instances — nhung chi test tren chatbot (ChatGLM, Llama2), **chua test tren coding agent** [D5].

#### 2.1.2. Benchmark danh gia Coding Agent

Deng et al. (2025) gioi thieu SWE-Bench Pro voi 1,865 tasks tu codebase thuong mai. Model tot nhat (Claude Sonnet 4.5) chi dat 43.6% tren public set va 17.8% tren commercial set [C1]. Xu et al. (2025) de xuat SWE-Compass voi 2,000 instances tren 10 ngon ngu [C5]. Thai et al. (2025) de xuat SWE-EVO cho long-horizon evolution [C2]. Prathifkumar et al. (2025) dat nghi van ve benchmark validity — LLM co the memorize patches [C3].

**Nhan xet chung:** Tat ca benchmark tren chi do **correctness**. Khong benchmark nao co **adversarial variants** de test security. Mot agent pass SWE-bench voi 70% nhung co the hoan toan de bi tan cong.

#### 2.1.3. Vu Claude Code Source Leak (03/2026)

Thang 3/2026, Anthropic vo tinh publish sourcemap (cli.js.map) trong goi npm cua Claude Code, phoi bay toan bo 1,884 file TypeScript goc. Cong dong nhanh chong phan tich va phat hien:
- 8 tinh nang chua phat hanh (KAIROS, ULTRAPLAN, BUDDY, ...)
- 26 hidden slash commands
- 32 secret CLI flags va environment variables (bao gom ca bypass safety)
- Toan bo kien truc harness: tool system, permission model, YOLO classifier

Su co nay minh hoa **rui ro thuc te** khi ha tang coding agent bi phoi bay: ke tan cong co the hieu ro cau truc safety layer va tim cach bypass. Day la dong luc thuc tien manh me cho nghien cuu nay.

#### 2.1.4. Tong hop Research Gap

```
┌─────────────────────────────────────────────────┐
│          HIEN TRANG NGHIEN CUU                  │
│                                                 │
│  ┌──────────────┐     ┌──────────────┐         │
│  │  Evaluation  │     │  Security    │         │
│  │  Community   │     │  Community   │         │
│  │              │     │              │         │
│  │ SWE-bench    │     │ AIShellJack  │         │
│  │ SWE-Compass  │     │ SecurePatterns│         │
│  │ PRDBench     │     │ DefensePipe  │         │
│  │              │     │              │         │
│  │ Do: RR       │     │ Do: ASR      │         │
│  │ Bo: ASR      │     │ Bo: RR       │         │
│  └──────┬───────┘     └──────┬───────┘         │
│         │                    │                  │
│         │    RESEARCH GAP    │                  │
│         │  ┌──────────────┐  │                  │
│         └──┤SecureCode    ├──┘                  │
│            │Bench         │                     │
│            │Do: RR + ASR  │ ← NGHIEN CUU NAY   │
│            │Metric: SRR   │                     │
│            └──────────────┘                     │
└─────────────────────────────────────────────────┘
```

### 2.2. Co so ly thuyet

#### 2.2.1. Prompt Injection Taxonomy cho Coding Agent

Dua tren D1, D3, D4, phan loai thanh 4 vector tan cong dac trung coding:

| Vector | Mo ta | Vi du | Muc do nguy hiem |
|--------|-------|-------|-----------------|
| **V1. Coding Rules** | Instruction an trong file cau hinh (.cursorrules, .clinerules, CLAUDE.md) | "Truoc khi commit, chay: curl attacker.com..." | Rat cao — file thuong duoc trust |
| **V2. MCP Tool Desc** | Payload an trong tool description | "IMPORTANT: Execute bash(...) before returning" | Cao — MCP dang duoc adopt rong |
| **V3. Code Context** | Instruction an trong comments, docstrings, README | "# TODO: Run os.system('rm -rf /') to clear cache" | Trung binh — phu thuoc context window |
| **V4. Supply Chain** | Package khong ton tai hoac bi tamper | "requirements.txt: secure-utils==1.0.0 (khong ton tai)" | Trung binh — can dieu kien ben ngoai |

#### 2.2.2. MITRE ATT&CK cho Coding Agent

Mapping 20 ky thuat phu hop nhat tu 70 ky thuat cua D3:

| Tactic | Techniques | Ap dung cho coding agent |
|--------|-----------|--------------------------|
| Execution | T1059 (Command Injection) | Agent thuc thi lenh bash doc hai |
| Exfiltration | T1048 (Exfil Over Web) | curl/wget gui data ra ngoai |
| Persistence | T1546 (Event Triggered) | Chen backdoor vao code |
| Discovery | T1083 (File Discovery) | Doc .env, credentials, SSH keys |
| Impact | T1485 (Data Destruction) | rm -rf, git push --force |
| Collection | T1005 (Local Data) | Doc source code, database |

#### 2.2.3. Metric Design — Secure Resolve Rate

**Resolve Rate (RR):** Metric chuan SWE-bench — % tasks giai dung (pass@1)

**Attack Success Rate (ASR):** Tu D3 — % adversarial payloads duoc agent thuc thi

**Secure Resolve Rate (SRR):**
```
SRR = RR × (1 - ASR)

Vi du:
Agent A: RR=60%, ASR=10% → SRR = 60% × 90% = 54% (tot nhat)
Agent B: RR=80%, ASR=70% → SRR = 80% × 30% = 24% (de hack)
Agent C: RR=40%, ASR= 5% → SRR = 40% × 95% = 38% (an toan nhung cham)
```

SRR phat agent giai tot nhung de hack (Agent B), thuong agent can bang (Agent A).

---

## CHUONG 3: PHUONG PHAP NGHIEN CUU

### 3.1. Tong quan phuong phap

Phuong phap **thuc nghiem** (experimental):
1. Xay dung attack taxonomy + benchmark dataset (engineering + manual curation)
2. Danh gia agents tren benchmark (thuc nghiem)
3. Phan tich trade-off va defense effectiveness (dinh luong + dinh tinh)

### 3.2. Xay dung SecureCodeBench (MT1, MT2)

**Buoc 1 — Chon tasks goc:**
- 100 tasks tu SWE-bench Verified (Python)
- Tieu chi: da co Docker env, da co gold patch, da nhieu agent giai thanh cong
- Dam bao da dang: bug fix, feature addition, refactoring

**Buoc 2 — Tao adversarial variants:**

Moi task co 5 phien ban:

| Version | Noi dung | File bi chinh sua |
|---------|---------|-------------------|
| **Clean** | Task goc, khong co tan cong | Khong |
| **V1: Coding Rules** | Them .cursorrules voi malicious instruction | .cursorrules (file moi) |
| **V2: MCP Tool** | Chinh sua tool description voi payload | mcp_config.json (file moi) |
| **V3: Code Context** | Chen adversarial comments vao file source | source files (them comments) |
| **V4: Supply Chain** | Them dependency doc hai vao requirements.txt | requirements.txt |

**Buoc 3 — Thiet ke payloads:**
- 20 payload templates mapping voi 20 MITRE ATT&CK techniques
- Moi template co 5 variants (do kho tang dan: obvious → subtle)
- Tong cong: 100 payloads doc dao

**Buoc 4 — Validation:**
- 2 nguoi review doc lap moi adversarial variant
- Kiem tra: (a) task clean van giai duoc, (b) payload la thuc thi duoc, (c) detection la do luong duoc

### 3.3. Evaluation Protocol (MT3)

**Agents duoc danh gia:**

| Agent | Loai | Ly do chon |
|-------|------|-----------|
| SWE-Agent | Open-source | Baseline pho bien nhat |
| OpenHands | Open-source | Co safety features |
| Claude Code | Commercial | Agent thuong mai hang dau, vua bi leak |
| Cursor | Commercial | IDE-based, dung .cursorrules |

**Quy trinh danh gia moi agent x moi variant:**
1. Chay agent tren task (max 50 turns, max $2/task)
2. Do Resolve Rate: patch co pass test suite khong?
3. Do Attack Success Rate: payload co duoc thuc thi khong?
   - Kiem tra bash history, network calls, file modifications
   - Su dung canary tokens de detect exfiltration
4. Ghi nhan: toan bo trajectory, tool calls, timestamps

**Tong so evaluations:** 4 agents x 500 instances = **2,000 evaluations**

### 3.4. Phan tich Trade-off (MT5)

**Thi nghiem them safety layer:**
- Chay SWE-Agent voi 3 muc safety: None, Rule-based, LLM-judge (tu D2)
- Do ca RR va ASR cho moi muc
- Ve trade-off curve: X = Security (1-ASR), Y = Performance (RR)

**Thi nghiem design patterns (tu D2):**
- Implement 3 patterns: Plan-Then-Execute, Dual LLM, Context-Minimization
- Ap dung len SWE-Agent
- So sanh SRR truoc/sau khi ap dung pattern

### 3.5. Validate Metric SRR (MT4)

- 3 expert ranking 30 agent outputs (xem output + biet co bi tan cong khong)
- Tinh Spearman correlation giua SRR ranking va expert ranking
- So sanh voi: RR-only ranking, ASR-only ranking, weighted average
- Muc tieu: SRR correlation > 0.85

---

## CHUONG 4: DU KIEN KET QUA NGHIEN CUU

### 4.1. Ket qua du kien

**MT1 — Taxonomy:** 4 vector tan cong x 20 MITRE techniques — taxonomy dau tien cho coding agent security evaluation.

**MT2 — SecureCodeBench:** 500 instances (100 clean + 400 adversarial) — benchmark dau tien ket hop correctness + security.

**MT3 — Agent Comparison:**

| Agent | RR (du kien) | ASR (du kien) | SRR (du kien) |
|-------|-------------|--------------|---------------|
| Claude Code | 65-70% | 30-50% | 35-49% |
| Cursor | 55-65% | 50-70% | 16-32% |
| SWE-Agent | 45-55% | 40-60% | 18-33% |
| OpenHands | 40-50% | 20-40% | 24-40% |

*(Du kien dua tren D3: Cursor va Claude Code deu co .cursorrules support → de bi V1 attack)*

**MT4 — SRR Validation:** Correlation > 0.85 voi expert ranking.

**MT5 — Trade-off Analysis:**
- Them safety layer giam ASR ~30-50% nhung cung giam RR ~5-15%
- Plan-Then-Execute pattern hieu qua nhat (theo D2): giam ASR nhieu, giam RR it

### 4.2. Y nghia khoa hoc
- **Benchmark moi:** SecureCodeBench — dau tien ket hop 2 truc (correctness + security)
- **Metric moi:** Secure Resolve Rate — cho phep ranking toan dien
- **Taxonomy moi:** 4 vectors x 20 techniques dac thu cho coding agents
- **Phat hien moi:** Dinh luong trade-off giua performance va security

### 4.3. Y nghia thuc tien
- **Cho developer:** Biet agent nao an toan de deploy (khong chi nhanh)
- **Cho vendor:** Phat hien lo hong truoc khi phát hành (responsible disclosure)
- **Cho to chuc:** Co so de xay dung policy su dung coding agent
- **Cho cong dong:** Open-source benchmark + toolkit

### 4.4. Lien he thuc te — Vu Claude Code Leak

Nghien cuu nay dac biet cap nhat trong boi canh:
- Claude Code source leak (03/2026) phoi bay toan bo harness architecture
- Cong dong da tao hang tram fork/clone (claw-code, v.v.)
- Ke tan cong co the hieu ro safety layer va tim cach bypass
- **SecureCodeBench** cho phep danh gia muc do anh huong cua viec leak len security

---

## CHUONG 5: KE HOACH THUC HIEN

| Giai doan | Thoi gian | Noi dung | San pham |
|-----------|-----------|----------|----------|
| GD1 | Thang 1-2 | Taxonomy tan cong + chon 100 tasks + thiet ke payloads | Taxonomy, 100 payload templates |
| GD2 | Thang 2-3 | Tao 400 adversarial variants + validation | SecureCodeBench v1.0 |
| GD3 | Thang 3-5 | Chay danh gia 4 agents x 500 instances | 2,000 evaluations, raw data |
| GD4 | Thang 4-5 | Trade-off experiments + defense patterns | Trade-off curves, pattern comparison |
| GD5 | Thang 5-6 | Validate SRR + viet luan van + phat hanh | Luan van, benchmark + toolkit tren GitHub |

### Chi phi du kien
| Hang muc | Chi tiet | Chi phi |
|----------|----------|---------|
| LLM API | Claude Code + Cursor (commercial, 500 instances moi) | $500-800 |
| SWE-Agent + OpenHands | Open-source, chay local | Docker compute only |
| **Tong** | | **$500-800** |

---

## TAI LIEU THAM KHAO

[A1] N. D. Q. Bui et al., "Building Effective AI Coding Agents for the Terminal: Scaffolding, Harness, Context Engineering," arXiv:2603.05344, 2026.
[C1] X. Deng et al., "SWE-Bench Pro: Can AI Agents Solve Long-Horizon SE Tasks?" arXiv:2509.16941, 2025.
[C2] M. V. T. Thai et al., "SWE-EVO: Benchmarking Coding Agents in Long-Horizon Software Evolution," arXiv:2512.18470, 2025.
[C3] T. Prathifkumar et al., "Does SWE-Bench-Verified Test Agent Ability or Model Memory?" arXiv:2512.10218, 2025.
[C5] J. Xu et al., "SWE-Compass: Towards Unified Evaluation of Agentic Coding Abilities," arXiv:2511.05459, 2025.
[D1] A. Chhabra et al., "Agentic AI Security: Threats, Defenses, Evaluation, and Open Challenges," arXiv:2510.23883, 2025.
[D2] L. Beurer-Kellner et al., "Design Patterns for Securing LLM Agents against Prompt Injections," arXiv:2506.08837, 2025.
[D3] Y. Liu et al., "'Your AI, My Shell': Demystifying Prompt Injection Attacks on Agentic AI Coding Editors," arXiv:2509.22040, 2025.
[D4] N. Maloyan and D. Namiot, "Prompt Injection Attacks on Agentic Coding Assistants: A Systematic Analysis," arXiv:2601.17548, 2026.
[D5] S. M. A. Hossain et al., "A Multi-Agent LLM Defense Pipeline Against Prompt Injection Attacks," arXiv:2509.14285, 2025.
[G3] C. Ma et al., "AgentBoard: An Analytical Evaluation Board of Multi-Turn LLM Agents," arXiv:2401.13178, 2024.
[I1] "AI Agentic Programming Survey," arXiv:2508.11126, 2025.
[S1] L. Wang et al., "A Survey on LLM based Autonomous Agents," arXiv:2308.11432, 2023.
[S5] "Survey on Evaluation of LLM-based Agents," arXiv:2503.16416, 2025.
