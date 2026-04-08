# DE CUONG DE TAI NGHIEN CUU KHOA HOC
# Huong 1: HarnessEval — Danh gia ha tang Coding Agent

---

## TEN DE TAI

**Tieng Viet:**
HarnessEval: Khung danh gia da chieu cho ha tang cua Coding Agent dua tren Mo hinh Ngon ngu Lon

**Tieng Anh:**
HarnessEval: A Multi-Dimensional Evaluation Framework for LLM-based Coding Agent Infrastructure

**Tu khoa:** Coding Agent, Harness, Scaffold, Evaluation Framework, Ablation Study, Tool Dispatch, Context Management, SWE-bench, LLM Agent

---

## CHUONG 1: MO DAU

### 1.1. Dat van de

Coding agent dua tren Mo hinh Ngon ngu Lon (LLM) dang cach mang hoa phat trien phan mem. Cac cong cu nhu Claude Code, GitHub Copilot, Cursor va SWE-Agent co the tu dong doc ma nguon, sua loi, tao tinh nang — thay the dang ke cong viec thu cong cua lap trinh vien [A1, I1].

Hieu suat cua coding agent phu thuoc vao 2 yeu to: (1) **LLM co so** (Claude, GPT, DeepSeek) va (2) **harness** — bo khung ha tang bao quanh LLM, bao gom he thong tool dispatch, quan ly context, quan ly phien lam viec va bao mat [A1]. Lou et al. (2026) chung minh rang harness quan trong khong kem model: model nho voi harness tot co the **vuot troi** model lon khong co harness — giam 100% hanh dong bat hop le trong moi truong game [A2]. Bui et al. (2026) mo ta harness nhu "he dieu hanh cho agent" voi kien truc 4 lop phuc tap [A1].

**Tuy nhien, ton tai mot nghich ly lon:** Cong dong da co nhieu benchmark danh gia **dau ra** cua agent (SWE-bench [C1], SWE-Compass [C5], PRDBench [C4]) nhung **khong co benchmark nao danh gia ban than harness**. Khi bao cao "Claude dat 70% tren SWE-bench," chung ta khong biet:

- Tool system goi dung tool bao nhieu phan tram? Bao nhieu tool calls la thua?
- Context compaction co bo mat thong tin quan trong khong? Token waste la bao nhieu?
- Doi model tu Claude sang GPT thi harness con hoat dong tot khong?
- Performance co suy giam khi conversation dai (50 turns vs 200 turns)?

Ket qua phan tich 49 papers gan day (2023-2026) xac nhan: trong so 32 papers de cap evaluation, **tat ca** chi do output (resolve rate, pass@1). Khong paper nao danh gia **harness properties** mot cach doc lap voi LLM [S5]. Day la **research gap** chinh ma nghien cuu nay nham giai quyet.

### 1.2. Muc dich nghien cuu (dinh tinh)

Nghien cuu nay nham **xay dung khung danh gia da chieu dau tien** cho ha tang (harness) cua coding agent, cho phep do luong chat luong cua tung thanh phan harness **doc lap** voi kha nang cua LLM co so. Qua do, cung cap co so khoa hoc de so sanh, lua chon va thiet ke harness hieu qua cho cac ung dung coding agent.

### 1.3. Muc tieu nghien cuu (dinh luong)

**MT1.** Xay dung taxonomy 5 chieu danh gia harness voi it nhat 2 metric do luong cho moi chieu (tong cong 11+ metrics), duoc validate boi it nhat 3 chuyen gia.

**MT2.** Implement modular reference harness bang Python voi cac component co the swap duoc (tool dispatcher, context manager, safety layer, memory store, model backend).

**MT3.** Thuc hien ablation study he thong tren 200 tasks tu SWE-bench Verified voi it nhat 3 cau hinh harness (SWE-Agent, OpenHands, modular harness) va 3 LLM backends (Claude Sonnet, GPT-4o, DeepSeek-V3), tong cong 50+ conditions.

**MT4.** Phat hien va dinh luong **dong gop cua tung component** harness (tool, context, safety, memory) vao hieu suat agent tong the, voi do tin cay thong ke (p < 0.05).

**MT5.** Phat hanh open-source evaluation toolkit va du lieu benchmark tren GitHub de cong dong tai su dung va mo rong.

### 1.4. Doi tuong va pham vi nghien cuu

**Doi tuong:**
- Ha tang (harness/scaffold) cua coding agents dua tren LLM
- 5 thanh phan harness: tool system, context manager, safety layer, memory store, model backend

**Pham vi:**
- Coding agents xu ly task cap repository-level (khong phai function-level)
- SWE-bench Verified (Python) lam benchmark chinh
- 3 LLM backends: Claude Sonnet, GPT-4o, DeepSeek-V3
- 3 harnesses: SWE-Agent, OpenHands, modular harness tu xay dung
- Thoi gian: 6 thang

### 1.5. Muc luc du kien

- **Chuong 1:** Mo dau (Dat van de, Tong quan tai lieu, Muc dich, Muc tieu, Doi tuong va Pham vi)
- **Chuong 2:** Co so ly thuyet (Kien truc coding agent, Harness design, Evaluation methodology)
- **Chuong 3:** Phuong phap nghien cuu (Taxonomy design, Modular harness, Ablation protocol)
- **Chuong 4:** Ket qua va thao luan (Ablation results, Component contributions, Cross-backend analysis, Design guidelines)
- **Chuong 5:** Ket luan va huong phat trien
- Tai lieu tham khao & Phu luc

---

## CHUONG 2: TONG QUAN TAI LIEU VA CO SO LY THUYET

### 2.1. Tong quan tai lieu

#### 2.1.1. Kien truc Coding Agent Harness

Wang et al. (2023) de xuat framework Profile-Memory-Planning-Action cho LLM agents — tro thanh reference chuan voi hon 3,000 citations [S1]. Bui et al. (2026) cu the hoa framework nay cho coding agents voi OpenDev — harness terminal-native viet bang Rust, bao gom kien truc dual-agent (Planner-Executor), lazy tool discovery, Adaptive Context Compaction (ACC) 5 giai doan giam 54% peak token usage, va event-driven system reminders chong instruction fade-out [A1].

Lou et al. (2026) chung minh gia tri cua harness bang AutoHarness: LLM tu sinh code harness thong qua tinh chinh lap lai voi environment feedback, dat 100% legal action rate tren 145 games, giup model nho (Gemini-2.5-Flash) vuot model lon (Gemini-2.5-Pro) [A2]. Tuy nhien, thuc nghiem chi tren game environment, chua generalize sang coding tasks.

Cao et al. (2026) cho thay coding agents xu ly long-context hieu qua bang cach externalize reasoning qua file-system tools (grep, edit, bash), vuot SOTA 17.3% tren 4/5 benchmarks — nhan manh tool system va file-system interaction la thanh phan cot loi cua harness [A3].

Robeyns et al. (2025) de xuat SICA — coding agent tu cai thien chinh minh, tang SWE-bench tu 17% len 53% sau 15 iterations — cho thay harness khong nen tinh ma co the tu toi uu [B10].

**Nhan xet:** Cac cong trinh tren mo ta harness design rat chi tiet nhung **khong co cong trinh nao benchmark cac thanh phan harness mot cach he thong**. Day la khoang trong nghien cuu chinh.

#### 2.1.2. Benchmark va Evaluation cho Coding Agent

SWE-bench (Jimenez et al., 2024) thiet lap chuan danh gia coding agent voi GitHub issues thuc te. Deng et al. (2025) nang cap voi SWE-Bench Pro — 1,865 tasks tu codebase thuong mai, chong contamination bang copyleft license, yeu cau multi-file editing trung binh 107.4 LOC [C1]. Tuy nhien, Prathifkumar et al. (2025) phat hien bang chung cho thay LLM memorize patches — Claude giai dinh vi file tot hon 3-6x tren SWE-bench so voi benchmark moi, dat nghi van ve benchmark validity [C3].

Thai et al. (2025) de xuat SWE-EVO cho long-horizon evolution — model tot nhat chi dat 21% [C2]. Xu et al. (2025) gioi thieu SWE-Compass voi 2,000 instances tren 10 ngon ngu va 8 loai task [C5]. Fu et al. (2026) dung agent tu tao benchmark (PRDBench) voi PRDJudge dat >90% human alignment [C4].

Ma et al. (2024) de xuat AgentBoard voi metric **progress rate** — do tien do tung buoc thay vi chi pass/fail, dat Pearson > 0.95 voi human judgment [G3]. Survey ve evaluation cho thay 8/10 benchmarks co validity issues — do-nothing agents pass 38% tasks [S5].

**Nhan xet chung:** Tat ca benchmark tren do **output quality** cua agent. Khong benchmark nao do **harness quality** — he thong tool dispatch, context management, safety enforcement — doc lap voi LLM capability.

#### 2.1.3. He thong Tool va Context Management

Qin et al. (2023) gioi thieu ToolLLM voi 16,000+ APIs va DFSDT reasoning [F2]. Du et al. (2024) de xuat AnyTool voi hierarchical self-reflective retrieval [F3]. Yuan et al. (2024) cho thay giam 70%+ token bang cach don gian hoa tool documentation [F5]. Survey cua Qu et al. (2024) tong hop 33 benchmarks va 7 thach thuc cua tool learning [F4].

Ve memory, Chhikara et al. (2025) gioi thieu Mem0 voi 91% giam latency [E1], Xu et al. (2025) de xuat A-Mem kieu Zettelkasten [E2], nhung **tat ca chi test tren chatbot/QA benchmarks** (LoCoMo), khong phai coding. Wang et al. (2025) phat hien agent **lap lai cung bug** qua nhieu iterations vi thieu persistent memory [I2].

#### 2.1.4. Tong hop Research Gap

| Khia canh | Duoc nghien cuu | Chua duoc nghien cuu |
|-----------|-----------------|----------------------|
| Agent output evaluation | C1-C5, G3, S5 (32/49 papers) | — |
| Harness design | A1, A2, A3, B10 (9/49 papers) | **Harness evaluation/benchmarking** |
| Tool-use evaluation | F1-F5 (benchmark API calls) | **Tool dispatch efficiency trong coding harness** |
| Context management | A1 (ACC), E1-E5 (memory) | **Context utilization metrics cho coding** |
| Cross-backend portability | — | **Hoan toan chua duoc nghien cuu** |
| Session continuity | A1 (de cap instruction fade-out) | **Chua co metric do luong** |

### 2.2. Co so ly thuyet

#### 2.2.1. Kien truc Coding Agent Harness — Mo hinh 5 lop

```
┌──────────────────────────────────────────┐
│  Layer 5: Orchestration                  │ ← Agent loop (ReAct, Plan-Execute)
├──────────────────────────────────────────┤
│  Layer 4: Safety & Permission            │ ← Sandboxing, permission model
├──────────────────────────────────────────┤
│  Layer 3: Context & Memory Management    │ ← Compaction, persistent memory
├──────────────────────────────────────────┤
│  Layer 2: Tool System                    │ ← Read, Write, Edit, Bash, Grep...
├──────────────────────────────────────────┤
│  Layer 1: Model Backend                  │ ← Claude, GPT, DeepSeek, Qwen...
└──────────────────────────────────────────┘
```

#### 2.2.2. Ly thuyet Ablation Study

Ablation study la phuong phap chuan trong ML: loai bo (tat) tung component de do dong gop cua no vao ket qua tong the. Ap dung cho harness: tat tool X, doi context strategy Y, loai bo safety layer Z → do thay doi resolve rate.

#### 2.2.3. Metric Design Principles

- **Independence:** Metric phai do harness quality doc lap voi LLM capability
- **Composability:** Cac metric co the ket hop thanh score tong hop
- **Actionability:** Ket qua phai chi ra duoc cach cai thien harness cu the

---

## CHUONG 3: PHUONG PHAP NGHIEN CUU

### 3.1. Tong quan phuong phap

Phuong phap **thuc nghiem** (experimental) voi 3 giai doan:
1. Thiet ke taxonomy va metrics (ly thuyet + expert validation)
2. Implement modular harness va evaluation toolkit (engineering)
3. Ablation study he thong (thuc nghiem dinh luong)

### 3.2. Taxonomy 5 Chieu Danh Gia Harness (MT1)

| Chieu | Metric | Mo ta | Cach do |
|-------|--------|-------|---------|
| **D1. Tool Dispatch** | M1.1 Correct Selection Rate | % tool calls chon dung tool | So sanh voi ground-truth tool sequence tu expert |
| | M1.2 Avg Latency | Thoi gian trung binh giua cac tool calls | Timestamp logging |
| | M1.3 Redundant Call Rate | % tool calls khong can thiet | Expert annotation tren sample |
| **D2. Context Utilization** | M2.1 Info Retention | % thong tin quan trong con lai sau compaction | So sanh output truoc/sau compaction tren cung task |
| | M2.2 Token Waste Ratio | % tokens khong lien quan den task | Phan tich token attribution |
| **D3. Safety Enforcement** | M3.1 Destructive Op Block Rate | % lenh nguy hiem (rm -rf, push --force) bi chan | Inject 50 destructive commands |
| | M3.2 Permission Adherence | % actions tuan thu permission model | Log analysis |
| **D4. Session Continuity** | M4.1 Performance Decay | Ty le suy giam resolve rate theo do dai conversation | Do resolve rate tai turn 20, 50, 100, 200 |
| | M4.2 Instruction Adherence | % responses van tuan thu system prompt | GPT-judge kiem tra adherence |
| **D5. Backend Portability** | M5.1 Cross-Backend Variance | Do lech chuan resolve rate giua cac backends | std(resolve_rate) qua 3 backends |
| | M5.2 Min/Max Ratio | Ty le performance thap nhat / cao nhat | min(RR) / max(RR) |

**Validation:** Trinh bay taxonomy cho 3 chuyen gia (advisor + 2 industry practitioners), thu thap feedback, chinh sua. Tinh inter-rater agreement (Cohen's kappa) tren 20 mau danh gia.

### 3.3. Modular Reference Harness (MT2)

```python
# Kien truc modular — moi component co the swap
class ModularHarness:
    def __init__(self, config):
        self.backend    = load_backend(config.backend)      # claude/gpt/deepseek
        self.tools      = load_tools(config.tool_set)       # full/limited/minimal
        self.context    = load_context(config.context_mgr)  # full/sliding/acc
        self.safety     = load_safety(config.safety_mode)   # none/rules/llm-judge
        self.memory     = load_memory(config.memory_type)   # none/mem0/flat
        self.metrics    = MetricsCollector()                 # Thu thap 11 metrics

    def run(self, task):
        # Agent loop voi logging toan dien
        while not done:
            action = self.backend.decide(context)
            self.metrics.log_tool_call(action)
            result = self.tools.execute(action)
            self.context.update(result)
            self.safety.check(action, result)
```

### 3.4. Ablation Study Protocol (MT3, MT4)

**Thiet ke thuc nghiem:**

| Bien | Gia tri | So dieu kien |
|------|---------|-------------|
| Harness | SWE-Agent, OpenHands, ModularHarness | 3 |
| LLM Backend | Claude Sonnet, GPT-4o, DeepSeek-V3 | 3 |
| Tool Config | Full (12 tools) / Limited (5 tools) / Read-only | 3 |
| Context Strategy | Full context / Sliding window / ACC | 3 |
| Safety Layer | None / Rule-based / LLM-judge | 3 |

**Tong so dieu kien ly thuyet:** 3 x 3 x 3 x 3 x 3 = 729
**Chien luoc cat giam:** Dung fractional factorial design (Latin square), chay ~60 conditions chinh + 20 conditions kiem chung = **80 conditions**

**Moi condition:** 200 tasks x 1 run = 200 evaluations
**Tong so evaluations:** ~16,000 (chia batch chay trong 4-6 tuan)

**Phan tich thong ke:**
- ANOVA de xac dinh component nao anh huong nhieu nhat
- Effect size (Cohen's d) cho tung component
- Interaction effects giua cac components
- p < 0.05 la nguong chap nhan

### 3.5. So sanh Cross-Harness (MT3)

So sanh 3 harnesses tren **cung** 200 tasks, **cung** backend (Claude Sonnet):
- Do 11 metrics cho moi harness
- Radar chart 5 chieu cho moi harness
- Nhan dien diem manh/yeu cua tung harness

---

## CHUONG 4: DU KIEN KET QUA NGHIEN CUU

### 4.1. Ket qua du kien

**MT1 — Taxonomy:** Bang phan loai 5 chieu, 11 metrics — **dong gop dau tien trong linh vuc**, chua co paper nao de xuat.

**MT2 — Modular Harness:** Python toolkit open-source cho phep cong dong tu danh gia harness cua minh.

**MT3 — Ablation Results:**
- Du kien phat hien: tool system dong gop ~30-40% vao resolve rate, context management ~20-30%, safety layer giam ~5-10% performance nhung can thiet
- Cross-backend: harness tot giam variance giua backends (std < 5%)
- Session continuity: performance giam ~15-25% sau 100 turns

**MT4 — Component Contributions:** Dinh luong chinh xac dong gop tung component voi p < 0.05.

**MT5 — Toolkit:** GitHub repo voi documentation, examples, CI/CD.

### 4.2. Y nghia khoa hoc
- **Khai niem moi:** Harness-level evaluation — chuyen tu "danh gia agent" sang "danh gia ha tang agent"
- **Taxonomy moi:** 5 chieu, 11 metrics — co the tro thanh chuan cho linh vuc
- **Phuong phap moi:** Ablation study he thong cho harness components
- **Du lieu moi:** Ket qua thuc nghiem 80+ conditions, 16,000+ evaluations

### 4.3. Y nghia thuc tien
- **Cho developer:** Biet chon harness nao phu hop (khong chi chon model)
- **Cho researcher:** Framework chuan de so sanh harness moi
- **Cho cong nghiep:** Guidelines thiet ke harness dua tren du lieu
- **Cho cong dong:** Open-source toolkit de tai su dung

---

## CHUONG 5: KE HOACH THUC HIEN

| Giai doan | Thoi gian | Noi dung | San pham |
|-----------|-----------|----------|----------|
| GD1 | Thang 1-2 | Thiet ke taxonomy + validate voi expert | Taxonomy v1.0, expert feedback report |
| GD2 | Thang 2-3 | Implement modular harness + adapters | Python package, Docker envs |
| GD3 | Thang 3-5 | Chay ablation study (80 conditions) | Raw data, 16,000+ evaluations |
| GD4 | Thang 5-6 | Phan tich ket qua + viet luan van | Luan van, toolkit v1.0 tren GitHub |

### Chi phi du kien
| Hang muc | Chi tiet | Chi phi |
|----------|----------|---------|
| LLM API | Claude + GPT-4o + DeepSeek (80 conditions x 200 tasks) | $800-1,200 |
| Compute | Docker VMs cho SWE-bench | $200-400 (cloud) hoac may ca nhan |
| **Tong** | | **$1,000-1,600** |

---

## TAI LIEU THAM KHAO

[A1] N. D. Q. Bui et al., "Building Effective AI Coding Agents for the Terminal: Scaffolding, Harness, Context Engineering, and Lessons Learned," arXiv:2603.05344, 2026.
[A2] X. Lou et al., "AutoHarness: Improving LLM Agents by Automatically Synthesizing a Code Harness," arXiv:2603.03329, 2026.
[A3] W. Cao et al., "Coding Agents are Effective Long-Context Processors," arXiv:2603.20432, 2026.
[B10] M. Robeyns et al., "A Self-Improving Coding Agent," arXiv:2504.15228, 2025.
[C1] X. Deng et al., "SWE-Bench Pro: Can AI Agents Solve Long-Horizon SE Tasks?" arXiv:2509.16941, 2025.
[C2] M. V. T. Thai et al., "SWE-EVO: Benchmarking Coding Agents in Long-Horizon Software Evolution," arXiv:2512.18470, 2025.
[C3] T. Prathifkumar et al., "Does SWE-Bench-Verified Test Agent Ability or Model Memory?" arXiv:2512.10218, 2025.
[C4] L. Fu et al., "Automatically Benchmarking LLM Code Agents through Agent-Driven Annotation," arXiv:2510.24358, 2025.
[C5] J. Xu et al., "SWE-Compass: Towards Unified Evaluation of Agentic Coding Abilities," arXiv:2511.05459, 2025.
[D1] A. Chhabra et al., "Agentic AI Security: Threats, Defenses, Evaluation, and Open Challenges," arXiv:2510.23883, 2025.
[E1] P. Chhikara et al., "Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory," arXiv:2504.19413, 2025.
[E2] W. Xu et al., "A-MEM: Agentic Memory for LLM Agents," arXiv:2502.12110, 2025.
[F2] Y. Qin et al., "ToolLLM: Facilitating LLMs to Master 16000+ Real-world APIs," arXiv:2307.16789, 2023.
[F3] Y. Du et al., "AnyTool: Self-Reflective Hierarchical Agents for Large-Scale API Use," arXiv:2402.04253, 2024.
[F4] C. Qu et al., "Tool Learning with Large Language Models: A Survey," arXiv:2405.17935, 2024.
[F5] S. Yuan et al., "EASYTOOL: Enhancing LLM-based Agents with Concise Tool Instruction," arXiv:2401.06201, 2024.
[G3] C. Ma et al., "AgentBoard: An Analytical Evaluation Board of Multi-Turn LLM Agents," arXiv:2401.13178, 2024.
[I1] "AI Agentic Programming Survey," arXiv:2508.11126, 2025.
[I2] J. Wang et al., "Illuminating LLM Coding Agents: Visual Analytics," arXiv:2508.12555, 2025.
[S1] L. Wang et al., "A Survey on LLM based Autonomous Agents," arXiv:2308.11432, 2023.
[S5] "Survey on Evaluation of LLM-based Agents," arXiv:2503.16416, 2025.
