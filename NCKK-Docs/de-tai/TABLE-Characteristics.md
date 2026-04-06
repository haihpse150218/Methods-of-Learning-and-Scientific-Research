# Table: Summary on Characteristics Investigated
## (Giong Table 1 cua Ho-Van 2013 — chi ro research gap)

> **De tai:** HarnessEval — Evaluating Coding Agent Scaffolds Through Ablation-Driven Multi-Dimensional Analysis
> **Muc dich:** Chi ro cac bai bao da lam 1 phan nhung CHUA DU → research gap cua chung ta

---

## Giai thich cac Characteristics (cot)

| Ky hieu | Characteristic | Mo ta | Lien quan den HarnessEval |
|---------|---------------|-------|--------------------------|
| **C1** | Tool Dispatch Evaluation | Danh gia chinh xac/hieu qua cua tool system trong harness | **D1 — Core** |
| **C2** | Context Management Evaluation | Danh gia hieu qua nen/quan ly context | **D2 — Core** |
| **C3** | Backend Portability Analysis | So sanh harness tren nhieu LLM backends | **D3 — Core** |
| **C4** | Component Ablation Study | Tat/doi tung component → do dong gop | **Phuong phap chinh** |
| **C5** | Harness vs LLM Decomposition | Phan tach variance do harness vs do LLM | **Dong gop ly thuyet** |
| **C6** | Unified Multi-Metric Framework | Framework da chieu voi nhieu metrics dong thoi | **Dong gop chinh** |
| **C7** | Coding-Specific Evaluation | Danh gia tren coding tasks (khong phai chatbot/game) | **Pham vi** |
| **C8** | Open-Source Reproducible | Co the tai su dung, open-source toolkit | **RO5** |

---

## Table: Summary on Characteristics Investigated

**Legend:** ✓ = Addressed | △ = Partially addressed | (blank) = Not addressed

| Ref | Paper | Year | C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 |
|-----|-------|------|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| | | | Tool Dispatch Eval | Context Mgmt Eval | Backend Portability | Component Ablation | Harness vs LLM Decomp | Multi-Metric Framework | Coding-Specific | Open-Source |
|[A1]| Bui 2026 (OpenDev) | 2026 | △ | △ | | | | | ✓ | ✓ |
|[A2]| Lou 2026 (AutoHarness) | 2026 | △ | | | △ | | | | |
|[A3]| Cao 2026 (LongContext) | 2026 | ✓ | △ | | | | | ✓ | |
|[B10]| Robeyns 2025 (SICA) | 2025 | △ | | | | | | ✓ | ✓ |
|[C1]| Deng 2025 (SWE-Bench Pro) | 2025 | | | | | | | ✓ | △ |
|[C2]| Thai 2025 (SWE-EVO) | 2025 | | | | | | | ✓ | ✓ |
|[C3]| Prathifkumar 2025 (SWE-Memory) | 2025 | | | | | | | ✓ | |
|[C4]| Fu 2026 (PRDBench) | 2026 | | | | | | △ | ✓ | △ |
|[C5]| Xu 2025 (SWE-Compass) | 2025 | | | | | | △ | ✓ | ✓ |
|[E1]| Chhikara 2025 (Mem0) | 2025 | | ✓ | | | | | | ✓ |
|[E2]| Xu 2025 (A-MEM) | 2025 | | ✓ | | | | | | ✓ |
|[E3]| Yu 2026 (AgeMem) | 2026 | | ✓ | | △ | | | | |
|[E4]| Borro 2026 (Memori) | 2026 | | ✓ | | | | | | ✓ |
|[F1]| Patil 2023 (Gorilla) | 2023 | ✓ | | | | | | | ✓ |
|[F2]| Qin 2023 (ToolLLM) | 2023 | ✓ | | | | | | | ✓ |
|[F3]| Du 2024 (AnyTool) | 2024 | ✓ | | | | | | | |
|[F4]| Qu 2024 (ToolSurvey) | 2024 | ✓ | | | | | △ | | |
|[F5]| Yuan 2024 (EasyTool) | 2024 | △ | | | | | | | |
|[G3]| Ma 2024 (AgentBoard) | 2024 | △ | △ | | | | ✓ | | ✓ |
|[I2]| Wang 2025 (VisualAnalytics) | 2025 | | △ | | | | ✓ | ✓ | |
|[S1]| Wang 2023 (AgentsSurvey) | 2023 | △ | ✓ | | | | | | |
|[S5]| 2025 (EvalSurvey) | 2025 | | | | | | △ | | |
| | | | | | | | | | | |
| **Ours** | **HarnessEval** | **2026** | **✓** | **✓** | **✓** | **✓** | **✓** | **✓** | **✓** | **✓** |

---

## Phan tich Research Gap tu bang

### Cot C1 (Tool Dispatch Evaluation): △ nhieu, ✓ it
- **F1, F2, F3** danh gia tool accuracy nhung **RIENG LE** (tren API benchmarks), **KHONG TRONG harness coding**
- **A1** mo ta tool system nhung **KHONG DO LUONG** hieu qua
- **A3** dung tools hieu qua nhung **KHONG CO METRIC** danh gia tool dispatch
- → **Gap:** Chua ai do tool dispatch efficiency **ben trong** 1 coding agent harness voi metrics formal

### Cot C2 (Context Management Evaluation): ✓ nhung sai domain
- **E1, E2, E3, E4** danh gia memory/context nhung **TREN CHATBOT** (LoCoMo, DialSim), **KHONG PHAI CODING**
- **A1** mo ta ACC (giam 54% token) nhung **KHONG BENCHMARK** hieu qua
- **I2** phat hien agent lap lai bug (thieu memory) nhung **KHONG DE XUAT METRIC**
- → **Gap:** Chua ai do context utilization **tren coding tasks** voi metrics nhu Info Retention hay Effective Token Ratio

### Cot C3 (Backend Portability): HOAN TOAN TRONG
- **KHONG CO PAPER NAO** so sanh cung 1 harness tren nhieu LLM backends
- Moi paper test voi 1 model (hoac nhieu model nhung doi CA harness lan model)
- → **Gap:** Portability la khia canh **hoan toan chua duoc nghien cuu**

### Cot C4 (Component Ablation): Gan nhu trong
- **A2** lam ablation nhung **TRONG GAME**, khong coding
- **E3** co ablation mot phan cho memory nhung **KHONG CHO TOOL hay CONTEXT**
- **KHONG AI** tat/doi tung component cua coding harness de do dong gop
- → **Gap:** Ablation study cho coding agent harness **chua ton tai**

### Cot C5 (Harness vs LLM Decomposition): HOAN TOAN TRONG
- **KHONG CO PAPER NAO** phan tach: "bao nhieu % performance do harness, bao nhieu % do LLM?"
- Day la cau hoi co ban nhat nhung chua ai tra loi
- → **Gap:** ANOVA/GLMM decomposition cho harness vs LLM **hoan toan moi**

### Cot C6 (Multi-Metric Framework): △ nhieu, ✓ rat it
- **G3** (AgentBoard) co multi-metric nhung **CHI DO OUTPUT** (progress rate), khong do harness
- **I2** (VisualAnalytics) co multi-level analysis nhung **KHONG CO FORMAL METRICS**
- **C5** (SWE-Compass) co nhieu chieu nhung **CHI CHINH XAC** (task types, languages), khong phai harness quality
- → **Gap:** Chua co framework **da metric thong nhat** danh gia **harness** (khong phai output)

### Cot C7 (Coding-Specific): ✓ nhieu nhung khong lien quan harness eval
- Nhieu papers lam tren coding tasks nhung **KHONG AI DANH GIA HARNESS**
- SWE-bench [C1], SWE-Compass [C5] la coding-specific nhung chi do output
- → **Gap nay khong phai gap chinh** — chi la dieu kien can (pham vi)

### Cot C8 (Open-Source): ✓ trung binh
- Nhieu papers co open-source nhung **KHONG CO TOOLKIT DANH GIA HARNESS**
- → **Gap:** Chua co open-source toolkit chuyen cho harness evaluation

---

## Tom tat Gap bang hinh anh

```
                C1    C2    C3    C4    C5    C6    C7    C8
                Tool  Ctx   Port  Abl   Dec   Multi Code  Open
Papers hien tai: △     △*    ___   ___   ___   △     ✓     ✓
                 |     |      |     |     |     |
                 |     |      |     |     |     |
                 ▼     ▼      ▼     ▼     ▼     ▼
Gap:           Trong  Sai   Hoan  Hoan  Hoan  Khong
               harness domain toan  toan  toan  formal
                             trong trong trong
                             
HarnessEval:    ✓     ✓      ✓     ✓     ✓     ✓     ✓     ✓
                ← LAP DAY TAT CA CAC GAP →

△* = Co nhung tren chatbot, khong phai coding
___ = Hoan toan trong (khong ai lam)
```

---

## Ket luan

Bang tren cho thay:
1. **3 cot hoan toan trong** (C3, C4, C5) — khong paper nao lam
2. **2 cot co nhung sai domain/context** (C1 trong harness, C2 tren coding)
3. **1 cot co nhung khong formal** (C6 multi-metric framework)
4. HarnessEval la **cong trinh dau tien** lap day tat ca 6 gaps nay dong thoi

Day chinh la **research gap** thuyet phuc nhat — khong phai "khong ai lam" (co the vi khong can) ma la **"nhieu nguoi lam 1 phan nhung CHUA AI GHEP LAI va DANH GIA TOAN DIEN trong coding harness."**
