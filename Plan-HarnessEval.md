# PLAN: HarnessEval — Danh gia ha tang Coding Agent
# (Cap nhat day du sau toan bo quy trinh nghien cuu)

> **Boi canh:** Chuong trinh Thac si Ky thuat phan mem AI — FPT
> **Mon hoc:** Methods of Learning and Scientific Research
> **Deadline nop de cuong:** 11-12/04/2026
> **De tai da chot:** HarnessEval — Danh gia ha tang Coding Agent thong qua phan tich ablation da chieu

---

## 1. Tong quan du an

### 1.1. Hanh trinh chon de tai

```
Buoc 1: Chon nhanh AI
  → LLM & Generative AI → Agent Framework

Buoc 2: Thu hep sub-domain
  → Coding Agent Harness & Evaluation
  → Boi canh: Claude Code source leak (03/2026), benchmark validity issues

Buoc 3: Research 49 papers (8 nhom)
  → A: Harness (3), B: Multi-Agent (10), C: Evaluation (5), D: Security (5)
  → E: Memory (5), F: Tool-Use (5), G: Planning (5), H: Orchestration (5)
  → I: Supplement (2), S: Surveys (4)

Buoc 4: GAP-ANALYSIS tu 49 papers
  → 6 research gaps nhan dien
  → Rank theo Feasibility x Novelty x Value

Buoc 5: Chon Gap 1 (HarnessEval) — diem cao nhat (14/15)

Buoc 6: Viet de cuong v1 → Phan bien hoi dong → De cuong v2
```

### 1.2. De tai da chot

**Ten tieng Viet:** HarnessEval: Danh gia ha tang Coding Agent thong qua phan tich ablation da chieu tren nhieu mo hinh ngon ngu lon

**Ten tieng Anh:** HarnessEval: Evaluating Coding Agent Scaffolds Through Ablation-Driven Multi-Dimensional Analysis

### 1.3. Research Gap

**Gap chinh:** 32/49 papers de cap evaluation nhung **tat ca chi do output** (resolve rate). **Khong paper nao do ban than harness** (tool dispatch, context management, backend portability) mot cach he thong va doc lap voi LLM.

**Bang chung:**
- SWE-bench [C1]: do resolve rate, khong biet TAI SAO agent fail
- ToolLLM [F2]: do tool accuracy rieng le, khong trong harness
- Mem0 [E1]: do memory cho chatbot, khong cho coding
- OpenDev [A1]: mo ta harness chi tiet nhung KHONG benchmark
- AutoHarness [A2]: chung minh harness quan trong nhung chi trong game

### 1.4. 4 Diem khac biet cua HarnessEval

| # | Khac biet | Mo ta |
|---|-----------|-------|
| 1 | **Do HARNESS thay vi do OUTPUT** | Taxonomy 3 chieu cho harness quality (khong phai resolve rate) |
| 2 | **ABLATION tung component** | Tat/doi tung thanh phan → dinh luong dong gop (tool 17%?, context 13%?) |
| 3 | **Cross-backend comparison** | Cung harness, doi LLM → do portability (chua ai lam) |
| 4 | **Framework THONG NHAT** | 1 toolkit thay nhieu papers rieng le (ToolLLM + Mem0 + AIShellJack + SWE-bench) |

---

## 2. Tien do da hoan thanh

### 2.1. Thu thap papers

| Hang muc | Trang thai | Chi tiet |
|----------|------------|---------|
| Chon huong de tai | XONG | Agent Framework → Coding Agent Harness & Evaluation |
| Search 49 papers | XONG | 8 nhom: A-H + I + S |
| Tai 49 PDFs | XONG | 132MB tu arXiv, luu trong NCKK-Docs/de-tai/papers/ |
| Tao INDEX.md | XONG | Bang tong hop 50 papers + 5 surveys |
| Tom tat 49 papers | XONG | 49 file .md trong NCKK-Docs/de-tai/summary/ |
| GAP-ANALYSIS | XONG | 6 gaps nhan dien, rank theo feasibility/novelty/value |

### 2.2. Viet de cuong

| Hang muc | Trang thai | Chi tiet |
|----------|------------|---------|
| De cuong ket hop (Gap 1+2) | XONG | DE-CUONG.md |
| De cuong HarnessEval v1 | XONG | DE-CUONG-HarnessEval.md |
| De cuong SecureCodeBench v1 | XONG | DE-CUONG-SecureCodeBench.md |
| Phan bien Ket hop | XONG | THAO-LUAN-KetHop.md (7.0/10) |
| Phan bien HarnessEval | XONG | THAO-LUAN-HarnessEval.md (7.3/10) |
| Phan bien SecureCodeBench | XONG | THAO-LUAN-SecureCodeBench.md (6.7/10) |
| **De cuong HarnessEval v2** | **XONG** | **DE-CUONG-HarnessEval-v2.md** (chinh sua theo phan bien) |

### 2.3. Visualization

| File | Noi dung |
|------|---------|
| visualize-HarnessEval.html | Y tuong de tai (10 sections, nen sang) |
| visualize-ThaoLuan-HarnessEval.html | Thao luan phan bien (6 sections) |

---

## 3. Cau truc thu muc hien tai

```
NCKK-Docs/
├── examples/                           # Mau Ho-Van 2013
├── de-tai/
│   ├── papers/                         # 49 PDFs (132MB)
│   ├── summary/                        # 49 file .md tom tat
│   ├── INDEX.md                        # Bang tong hop 50 papers
│   ├── GAP-ANALYSIS.md                 # 6 gaps, ranking, 3 de tai de xuat
│   ├── DE-CUONG.md                     # v1 ket hop (Gap 1+2)
│   ├── DE-CUONG-HarnessEval.md         # v1 Gap 1 rieng
│   ├── DE-CUONG-HarnessEval-v2.md      # ★ v2 Gap 1 (PHIEN BAN CHINH)
│   ├── DE-CUONG-SecureCodeBench.md     # v1 Gap 2 rieng
│   ├── THAO-LUAN-KetHop.md            # Phan bien ket hop (7.0/10)
│   ├── THAO-LUAN-HarnessEval.md       # Phan bien Gap 1 (7.3/10)
│   ├── THAO-LUAN-SecureCodeBench.md   # Phan bien Gap 2 (6.7/10)
│   ├── visualize-HarnessEval.html      # Visualization y tuong
│   ├── visualize-ThaoLuan-HarnessEval.html  # Visualization thao luan
│   └── download_papers.sh             # Script tai papers tu arXiv
```

---

## 4. De cuong v2 — Tom tat noi dung chinh

### 4.1. Taxonomy 3 chieu (giam tu 5 chieu v1)

| Chieu | Metrics | Cach do |
|-------|---------|---------|
| **D1. Tool Dispatch** | M1.1 Correct Selection Rate, M1.2 Redundant Call Rate, M1.3 Tool Utilization Breadth | Annotator + log analysis |
| **D2. Context Utilization** | M2.1 Info Retention Score (BERTScore), M2.2 Effective Token Ratio (LLM classifier) | So sanh full vs compacted context |
| **D3. Backend Portability** | M3.1 Cross-Backend Std Dev, M3.2 Min/Max Ratio | std(RR) qua 3 backends |

**Da bo (future work):** D4 Safety Enforcement, D5 Session Continuity

### 4.2. Phuong phap

| Hang muc | V1 | V2 | Ly do |
|----------|-----|-----|-------|
| Harness | Tu xay tu dau | **Fork SWE-Agent** | Giam rui ro, 2-3 tuan thay vi 1-3 thang |
| Conditions | 80 (fractional factorial) | **27 (full factorial 3x3x3)** | Kha thi, van du power |
| Evaluations | 16,000 | **7,050** | Giam 56%, tiet kiem budget |
| Pilot study | Khong | **200 evals (5 conditions x 20 tasks x 2 runs)** | Validate truoc khi cam ket |
| Phan tich | T-test | **ANOVA 2 chieu + Bonferroni** | Phan tach harness vs LLM |
| Runs | 1 run/condition | **3 runs cho 10 conditions chinh** | Reproducibility |

### 4.3. Gia thuyet nghien cuu

- **H1:** Tool system co effect size lon nhat (Cohen's d > 0.5)
- **H2:** Context management co effect size trung binh (d = 0.3-0.5)
- **H3:** Harness configuration giai thich >= 20% variance (eta-squared)
- **H4:** Harness tot giam gap giua cac backends (interaction effect)

### 4.4. Budget (da tinh lai)

| Hang muc | Chi phi |
|----------|---------|
| Pilot (200 evals) | ~$80 |
| Full experiment (7,050 evals) | ~$2,500 |
| Contingency 20% | ~$500 |
| **Tong** | **$2,500-3,100** |

### 4.5. Timeline 6 thang

```
Thang 1 ──── GD1: Taxonomy + Expert validation (5 experts, Fleiss' kappa)
        └─── GD1.5: Pilot study (200 evals)
Thang 2 ──── GD2: Fork SWE-Agent → Modular harness (verify +/- 3%)
Thang 3-4 ── GD3: Full ablation (27 conditions x 150 tasks = 7,050 evals)
Thang 5 ──── GD4: Phan tich ANOVA + guidelines + viet luan van
Thang 6 ──── GD5: Review, chinh sua, phat hanh toolkit GitHub
```

---

## 5. Ket qua phan bien va cach xu ly

### 5.1. Diem hoi dong danh gia v1

| Tieu chi | Diem | Nhan xet |
|----------|------|----------|
| Tinh moi | 8.5/10 | Meta-evaluation moi, goc nhin hay |
| Tinh kha thi | 5.5/10 | Scope qua rong, budget thap |
| Phuong phap | 7.0/10 | Tot nhung co lo hong validity |
| Tai lieu TK | 8.0/10 | 49 papers cap nhat |
| Trinh bay | 7.5/10 | Mach lac |
| **Tong** | **7.3/10** | **Can chinh sua dang ke** |

### 5.2. 7 goi y va cach xu ly trong v2

| # | Goi y | Cach xu ly trong v2 |
|---|-------|---------------------|
| 1 | Thu hep scope 5→3 chieu | DA LAM: 3 chieu (Tool, Context, Portability). Safety/Session → future work |
| 2 | Fork SWE-Agent thay vi tu xay | DA LAM: Fork + refactor, tieu chi +/- 3% baseline |
| 3 | Them power analysis + threats to validity | DA LAM: ANOVA, Bonferroni, 3 loai validity, 6 risks |
| 4 | Bo du kien ket qua cu the | DA LAM: Thay "30-40%" bang H1-H4 trung tinh |
| 5 | Them pilot study | DA LAM: 200 evals truoc full experiment |
| 6 | Dinh nghia formal "doc lap voi LLM" | DA LAM: Section 2.2.3 ANOVA 2 chieu |
| 7 | Them papers tu SE venues | CAN LAM: Tim them tu ICSE, FSE, ASE |

### 5.3. 10 cau hoi kho nhat va cach tra loi

| # | Cau hoi | Cach tra loi |
|---|---------|-------------|
| 1 | "Lam sao tach harness va LLM?" | ANOVA 2 chieu phan tach variance. Harness = "buffet", LLM = "khau vi" |
| 2 | "Tai sao Princeton/Anthropic khong lam? Artificial gap?" | Ho la developers, khong phai evaluators. Linh vuc tang qua nhanh |
| 3 | "Power analysis cho 11 metrics x 80 conditions?" | Da giam xuong 7 metrics x 27 conditions. 150 tasks du cho d=0.5 |
| 4 | "Ground-truth tool sequence khong duy nhat?" | Doi thanh TAP HOP acceptable sequences + 2 annotators |
| 5 | "Modular harness tu xay so voi SWE-Agent 2 nam?" | Doi thanh FORK SWE-Agent. Muc dich la cong cu thuc nghiem, khong phai san pham |
| 6 | "Generalize tu Python sang ngon ngu khac?" | Acknowledge limitation. Future work: SWE-Compass (10 ngon ngu) |
| 7 | "35% contribution — developer lam gi?" | Them Design Guidelines derive tu du lieu cu the |
| 8 | "Reproducibility khi LLM non-deterministic?" | temperature=0, 3 runs cho conditions chinh, report mean+/-std |
| 9 | "GPT-judge = circular reasoning?" | Da bo M4.2 (GPT-judge). M2.2 dung LLM classifier validated voi human |
| 10 | "Tai sao 5 chieu khong phai 3?" | Da giam xuong 3 chieu. Bat dau core, mo rong sau |

---

## 6. 6 Research Gaps da nhan dien (tu GAP-ANALYSIS)

| Rank | Gap | F | N | V | Tong | Trang thai |
|------|-----|---|---|---|------|-----------|
| **1** | **Harness-Level Evaluation Framework** | 4 | 5 | 5 | **14** | **DA CHON → DE CUONG v2** |
| 2 | Security-Aware Coding Benchmarks | 4 | 4 | 5 | 13 | De cuong v1 rieng (SecureCodeBench) |
| 3 | Memory-Augmented Coding Agent Eval | 3 | 4 | 4 | 11 | Future work |
| 4 | Multi-Language Long-Horizon Benchmarks | 2 | 4 | 4 | 10 | Kho, kha thi thap |
| 5 | Self-Improving Harness Design | 2 | 5 | 4 | 11 | Rui ro cao, phu hop PhD |
| 6 | Unified Harness (Tool+Memory+Security+Context) | — | — | — | — | Qua lon cho 1 nguoi |

---

## 7. Tai nguyen va cong cu

### 7.1. Papers va tai lieu

| Loai | So luong | Vi tri |
|------|----------|--------|
| PDFs goc | 49 files (132MB) | NCKK-Docs/de-tai/papers/ |
| Summaries | 49 files .md | NCKK-Docs/de-tai/summary/ |
| Index | 1 file | NCKK-Docs/de-tai/INDEX.md |
| Gap Analysis | 1 file (378 dong) | NCKK-Docs/de-tai/GAP-ANALYSIS.md |
| De cuong | 4 phien ban | DE-CUONG*.md |
| Thao luan | 3 files | THAO-LUAN-*.md |
| Visualizations | 2 files HTML | visualize-*.html |

### 7.2. Nguon tai papers

- **arXiv.org** — mien phi, da tai 49 papers
- **Semantic Scholar** — API search
- **Papers with Code** — co code
- **Can bo sung:** ICSE, FSE, ASE (SE venues) — theo goi y hoi dong

### 7.3. Repos lien quan

| Repo | Vai tro |
|------|---------|
| `haihpse150218/claw-code-free` | Kinh nghiem harness design |
| `haihpse150218/antigravity-awesome-skills` | Skills/playbooks cho agent |
| `princeton-nlp/SWE-agent` | **Base de fork → modular harness** |
| `All-Hands-AI/OpenHands` | So sanh cross-harness |
| `syifan/thebotcompany` | Reference multi-agent |

### 7.4. Ky nang

- Python (developer chuyen nghiep) → implement modular harness, toolkit
- Kinh nghiem coding agent harness (claw-code-free)
- Docker (SWE-bench evaluation)

---

## 8. Next Actions (sau khi nop de cuong)

| # | Viec can lam | Uu tien | Thoi gian |
|---|-------------|---------|-----------|
| 1 | Nop de cuong v2 cho advisor | CAO | 11-12/04/2026 |
| 2 | Tim them papers tu ICSE/FSE/ASE | Trung binh | Tuan sau |
| 3 | Setup SWE-bench Docker environment | CAO | Bat dau GD1 |
| 4 | Lien he 5 experts cho taxonomy validation | CAO | Song song GD1 |
| 5 | Fork SWE-Agent va bat dau refactor | Trung binh | GD2 |
| 6 | Chay pilot study (200 evals) | CAO | Sau GD1 |
| 7 | Viet de cuong SecureCodeBench v2 (neu can) | Thap | Sau khi HarnessEval on dinh |

---

## 9. Bai hoc rut ra tu quy trinh

1. **Research gap phai co bang chung dinh luong** — "32/49 papers chi do output" thuyet phuc hon "chua co ai lam"
2. **Scope can thuc te** — v1 qua tham vong (80 conditions, $1200) → v2 giam 56% evaluations, tang 3x budget
3. **Phan bien som giup nhieu** — phat hien van de truoc khi bat tay lam
4. **Pilot study la bat buoc** — khong cam ket full experiment khi chua validate metrics
5. **Fork > Tu xay** — dung vai nguoi khac (SWE-Agent) lam base, tap trung vao dong gop moi
6. **Hypotheses > Predictions** — "H1: tool co effect size lon nhat" tot hon "tool dong gop 30-40%"
7. **Visualization giup hieu** — HTML visualization lam ro y tuong nhanh hon van ban

---

## 10. Git History

```
b8dd4d5 — Initial commit
20ca919 — Add research planning materials
1722e89 — Add Agent Framework research plan and 50-paper index
6828ea1 — Add 49 paper summaries
6ba631b — Add comprehensive GAP-ANALYSIS
d77ba4b — Add research proposal combining HarnessEval + SecureCodeBench
d03a570 — Add 2 separate proposals (HarnessEval v1 + SecureCodeBench v1)
2f90168 — Add 3 thesis defense review documents
c822605 — Add HarnessEval v2 + visualization files
```
