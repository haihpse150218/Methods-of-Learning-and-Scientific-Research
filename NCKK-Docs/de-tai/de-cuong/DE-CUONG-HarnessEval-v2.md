# DE CUONG DE TAI NGHIEN CUU KHOA HOC — VERSION 2
# (Da chinh sua theo phan bien hoi dong)

---

## TEN DE TAI

**Tieng Viet:**
HarnessEval: Danh gia ha tang Coding Agent thong qua phan tich ablation da chieu tren nhieu mo hinh ngon ngu lon

**Tieng Anh:**
HarnessEval: Evaluating Coding Agent Scaffolds Through Ablation-Driven Multi-Dimensional Analysis

**Tu khoa:** Coding Agent, Harness, Scaffold, Evaluation, Ablation Study, Tool Dispatch, Context Management, Backend Portability, SWE-bench

> **Thay doi so voi v1:** Doi "Infrastructure" thanh "Scaffolds" (tranh nham DevOps). Them "Ablation-Driven" lam noi bat phuong phap. Bo "Multi-Dimensional" chung chung.

---

## CHUONG 1: MO DAU

### 1.1. Dat van de

Coding agent dua tren Mo hinh Ngon ngu Lon (LLM) dang duoc trien khai rong rai trong phat trien phan mem. Tuy nhien, hieu suat cua coding agent phu thuoc vao hai yeu to: (1) **LLM co so** va (2) **harness** — bo khung ha tang bao gom tool system, context management va cac lop ho tro khac [A1].

Lou et al. (2026) chung minh rang harness co vai tro then chot: model nho voi harness tot co the vuot model lon khong co harness, giam 100% hanh dong bat hop le trong moi truong co rang buoc [A2]. Bui et al. (2026) mo ta harness nhu "he dieu hanh cho agent" voi kien truc nhieu lop phuc tap bao gom dual-agent architecture, Adaptive Context Compaction giam 54% token usage, va event-driven system reminders [A1].

**Nghich ly hien tai:** Cong dong da co nhieu benchmark danh gia **dau ra** cua agent — SWE-bench voi 1,865 tasks [C1], SWE-Compass voi 2,000 instances tren 10 ngon ngu [C5], PRDBench voi agent-driven evaluation [C4]. Tuy nhien, phan tich 49 papers gan day (2023-2026) cho thay **khong co cong trinh nao danh gia ban than harness mot cach he thong** [S5]. Khi bao cao "Agent A dat 70%," chung ta khong biet component nao cua harness dong gop vao ket qua do.

**Tai sao day la research gap that su (khong phai artificial gap)?**

Cau hoi hop ly la: tai sao cac nhom phat trien harness (Princeton — SWE-Agent, Anthropic — Claude Code) khong tu lam? Ba ly do chinh:

1. **Vai tro khac nhau:** Ho la *developers*, co incentive de xuat harness moi, khong phai *evaluators* co incentive so sanh he thong. Giong nhu hang xe hoi san xuat xe nhung to chuc khac (Euro NCAP, IIHS) danh gia an toan.

2. **Linh vuc phat trien qua nhanh:** Tu 2023-2026, so luong coding agent tang tu vai he thong len hang chuc. Chua ai dung lai de meta-evaluate vi dang chay dua xay dung.

3. **Bang chung gian tiep:** Lou et al. (2026) da so sanh harness tren game tasks [A2]; Robeyns et al. (2025) tu cai thien harness nhung khong do tung component [B10] — cho thay nhu cau ton tai nhung chua duoc formalize.

**Research gap:** Thieu khung danh gia cho phep (a) do luong chat luong tung thanh phan harness, (b) phan tach dong gop cua harness vs. LLM co so, va (c) so sanh cac harness khac nhau tren cac chieu chat luong thong nhat.

### 1.2. Muc dich nghien cuu (dinh tinh)

Nghien cuu nay nham **xay dung khung danh gia tong hop dau tien** cho ha tang (harness) cua coding agent, cho phep phan tach va dinh luong dong gop cua tung thanh phan harness vao hieu suat agent tong the, doc lap voi kha nang cua LLM co so.

> **Thay doi so voi v1:** Doi "dau tien" thanh "tong hop dau tien" (acknowledge rang tung khia canh da co nguoi nghien cuu rieng le). Them "doc lap voi kha nang cua LLM" va giai thich ro "doc lap" nghia la gi (xem muc 2.2.3).

### 1.3. Muc tieu nghien cuu (dinh luong)

**MT1.** Xay dung taxonomy **3 chieu** danh gia harness (Tool Dispatch Efficiency, Context Utilization, Backend Portability) voi tong cong **7 metrics**, duoc validate boi it nhat 5 chuyen gia (do inter-rater agreement bang Fleiss' kappa, muc tieu kappa >= 0.6).

**MT2.** Fork va refactor SWE-Agent thanh modular harness voi cac component co the swap duoc (tool set, context strategy, model backend), dam bao **resolve rate tuong duong SWE-Agent goc** (+/- 3%) tren 50 tasks kiem chung.

**MT3.** Thuc hien ablation study tren **150 tasks** tu SWE-bench Verified voi **27 conditions** (3 tool configs x 3 context configs x 3 backends), bao gom **pilot study** (5 conditions x 20 tasks) truoc khi chay full experiment. Report mean +/- std tu 3 runs cho 10 conditions chinh.

**MT4.** Phan tach variance dong gop cua harness vs. LLM bang **ANOVA 2 chieu** (harness configuration x LLM backend), voi muc y nghia thong ke p < 0.05 sau Bonferroni correction.

**MT5.** Phat hanh open-source evaluation toolkit tren GitHub voi documentation, examples, va CI/CD pipeline.

> **Thay doi so voi v1:**
> - Giam tu 5 chieu → **3 chieu** (Safety va Session Continuity chuyen thanh future work)
> - Giam tu 80 conditions → **27 conditions** (kha thi 6 thang)
> - Them pilot study vao MT3
> - Them ANOVA 2 chieu vao MT4 (giai quyet van de "doc lap voi LLM")
> - MT2 doi tu "tu xay harness" thanh "fork SWE-Agent" (giam rui ro)
> - Them tieu chi chat luong cho MT2 (tuong duong SWE-Agent +/- 3%)
> - Doi Cohen's kappa → Fleiss' kappa (phu hop nhieu nguoi danh gia)
> - Them Bonferroni correction vao MT4

### 1.4. Gia thuyet nghien cuu

**H1:** Tool system co effect size lon nhat (Cohen's d > 0.5) trong 3 thanh phan harness doi voi resolve rate.

**H2:** Context management co effect size trung binh (Cohen's d 0.3-0.5).

**H3:** Harness configuration giai thich it nhat 20% variance cua resolve rate (eta-squared >= 0.20 trong ANOVA), doc lap voi LLM backend.

**H4:** Variance cua resolve rate giua cac LLM backends giam khi harness chat luong cao hon (interaction effect co y nghia thong ke).

> **Moi so voi v1:** Them phan gia thuyet — khong du doan ket qua cu the ("30-40%") ma chi neu huong ky vong co the kiem chung. Tranh confirmation bias.

### 1.5. Doi tuong va pham vi nghien cuu

**Doi tuong:**
- Ha tang (harness/scaffold) cua coding agents dua tren LLM
- 3 thanh phan harness: tool system, context manager, model backend

**Pham vi:**
- 150 tasks tu SWE-bench Verified (Python)
- 3 LLM backends: Claude Sonnet 4, GPT-4o, DeepSeek-V3
- Harness goc: SWE-Agent (fork va refactor)
- Thoi gian: 6 thang

**Ngoai pham vi (future work):**
- Safety/Security evaluation (→ de tai rieng: SecureCodeBench)
- Session continuity / long-horizon evaluation
- Ngon ngu khac ngoai Python
- Commercial harnesses (Claude Code, Cursor) — chi open-source

### 1.6. Muc luc du kien

- **Chuong 1:** Mo dau
- **Chuong 2:** Tong quan tai lieu va Co so ly thuyet
- **Chuong 3:** Phuong phap nghien cuu
- **Chuong 4:** Ket qua va thao luan
- **Chuong 5:** Ket luan va huong phat trien
- Tai lieu tham khao & Phu luc

---

## CHUONG 2: TONG QUAN TAI LIEU VA CO SO LY THUYET

### 2.1. Tong quan tai lieu

#### 2.1.1. Kien truc Coding Agent Harness

Wang et al. (2023) de xuat framework Profile-Memory-Planning-Action, duoc cite hon 3,000 lan [S1]. Bui et al. (2026) cu the hoa cho coding agents voi OpenDev — dual-agent architecture, 5-stage ACC giam 54% token, event-driven reminders chong instruction fade-out [A1]. Lou et al. (2026) chung minh harness co the tu sinh va giup model nho vuot model lon [A2]. Cao et al. (2026) cho thay coding agents xu ly long-context hieu qua bang file-system tools, vuot SOTA 17.3% [A3]. Robeyns et al. (2025) de xuat SICA — agent tu cai thien, tang SWE-bench tu 17% len 53% — nhung khong do tung component [B10].

**Nhan xet:** Cac cong trinh mo ta harness chi tiet nhung **khong benchmark** cac thanh phan.

#### 2.1.2. Benchmark Coding Agent

SWE-Bench Pro [C1] co 1,865 tasks da ngon ngu, chong contamination. SWE-EVO [C2] do long-horizon evolution (model tot nhat chi 21%). SWE-Compass [C5] bao phu 10 ngon ngu, 8 loai task. Prathifkumar et al. [C3] phat hien LLM co the memorize patches — nghi van benchmark validity. AgentBoard [G3] de xuat progress rate metric dat Pearson > 0.95 voi human judgment. Survey [S5] cho thay 8/10 benchmarks co validity issues.

**Nhan xet:** Tat ca do **output quality**. Khong benchmark nao do **harness quality**.

#### 2.1.3. Tool Learning va Context Management

ToolLLM [F2] danh gia 16,000+ APIs voi DFSDT reasoning. AnyTool [F3] de xuat hierarchical self-reflective retrieval. EasyTool [F5] giam 70% token qua don gian hoa tool documentation. Mem0 [E1] giam 91% latency cho persistent memory. A-MEM [E2] dung Zettelkasten approach. Wang et al. [I2] phat hien agent lap lai cung bug vi thieu persistent memory.

**Nhan xet:** Moi paper do **1 component rieng le**. Khong ai do **tat ca components cung luc** trong 1 harness va so sanh dong gop tuong doi.

#### 2.1.4. Tong hop Research Gap

| Khia canh | Da co | Chua co |
|-----------|-------|---------|
| Do output cua agent | SWE-bench, SWE-Compass, AgentBoard | — |
| Do tool accuracy rieng le | ToolLLM, AnyTool, Gorilla | Do tool **trong** harness coding |
| Do memory rieng le | Mem0, A-MEM (tren chatbot) | Do memory **trong** harness coding |
| Mo ta harness design | OpenDev, AutoHarness | **Do luong** harness quality |
| So sanh cross-backend | — | **Hoan toan chua ai lam** |
| Phan tach harness vs LLM contribution | — | **Hoan toan chua ai lam** |

### 2.2. Co so ly thuyet

#### 2.2.1. Kien truc Harness — Mo hinh 5 lop

Dua tren [S1] va [A1], coding agent harness gom 5 lop:

```
┌────────────────────────────────────┐
│ L5: Orchestration (agent loop)     │ ← Ngoai pham vi v2
├────────────────────────────────────┤
│ L4: Safety & Permission            │ ← Ngoai pham vi v2 (future work)
├────────────────────────────────────┤
│ L3: Context & Memory Management    │ ← DANH GIA (D2)
├────────────────────────────────────┤
│ L2: Tool System                    │ ← DANH GIA (D1)
├────────────────────────────────────┤
│ L1: Model Backend                  │ ← DANH GIA (D3: Portability)
└────────────────────────────────────┘
```

Nghien cuu nay tap trung danh gia **L1-L3** (3 lop duoi). L4-L5 de cho future work.

#### 2.2.2. Ablation Study trong Software Engineering

Ablation study la phuong phap chuan trong ML: loai bo tung component de do dong gop. Ap dung cho harness:

- **Tat/thay doi tool set** → do thay doi resolve rate
- **Doi context strategy** → do thay doi resolve rate
- **Doi LLM backend** → do portability

**Luu y ve confounding variables:** Khi tat tool X, performance giam co the vi (a) agent mat cong cu, hoac (b) harness dispatch kem. De giai quyet: thay vi "tat hoan toan," **giam** so luong tools (12 → 8 → 5 → 3) va thay doi **loai** tools, ghi nhan task nao can tool nao de phan biet 2 nguyen nhan.

#### 2.2.3. Dinh nghia "Doc lap voi LLM" — ANOVA 2 chieu

"Doc lap voi LLM" **khong co nghia** harness va LLM khong tuong tac. No co nghia: **co the phan tach** phan variance do harness vs. phan do LLM.

**Phuong phap:** ANOVA 2 chieu (two-way ANOVA)
- Factor A: Harness configuration (9 levels: 3 tool configs x 3 context configs)
- Factor B: LLM backend (3 levels: Claude, GPT, DeepSeek)
- Dependent variable: Resolve rate

```
Tong variance = Variance(Harness) + Variance(LLM) + Variance(Harness x LLM) + Error

Neu Variance(Harness) co y nghia thong ke → harness CO ANH HUONG doc lap
Neu Variance(Harness x LLM) co y nghia → co INTERACTION (harness tot hon cho LLM nao do)
Eta-squared (η²) cho biet % variance duoc giai thich boi moi factor
```

Day la **dong gop ly thuyet chinh** cua de tai — formalize cach phan tach harness quality khoi LLM quality.

> **Moi so voi v1:** Them section 2.2.3 hoan toan moi, giai quyet truc tiep cau hoi #1 cua hoi dong ("Lam sao tach roi harness va LLM?").

---

## CHUONG 3: PHUONG PHAP NGHIEN CUU

### 3.1. Tong quan phuong phap

Phuong phap **thuc nghiem** (experimental), 4 giai doan:

1. Thiet ke taxonomy + expert validation
2. Fork SWE-Agent thanh modular harness
3. Pilot study (5 conditions x 20 tasks)
4. Full ablation study (27 conditions x 150 tasks)

### 3.2. Taxonomy 3 Chieu Danh Gia Harness (MT1)

| Chieu | Metric | Dinh nghia formal | Cach do | Validation |
|-------|--------|-------------------|---------|------------|
| **D1. Tool Dispatch** | M1.1 Correct Tool Selection Rate | % tool calls chon tool phu hop voi muc dich (tu tap hop acceptable tools, khong phai 1 ground-truth duy nhat) | 2 annotators gan nhan "acceptable/not" cho 500 tool calls mau. Tinh Fleiss' kappa. | Kappa >= 0.6 |
| | M1.2 Redundant Call Rate | % tool calls ma ket qua khong duoc su dung trong 3 buoc tiep theo | Tu dong do bang log analysis: tool output co xuat hien trong context 3 turns sau khong? | Validate tren 100 mau voi human check |
| | M1.3 Tool Utilization Breadth | So tool types duoc su dung / tong so tools kha dung | Tu dong do bang log analysis | — |
| **D2. Context Utilization** | M2.1 Info Retention Score | Cosine similarity giua full-context response va compacted-context response tren cung task | Chay cung task 2 lan: 1 lan full context, 1 lan sau compaction. Do BERTScore giua 2 outputs. | Validate voi human preference tren 30 cap |
| | M2.2 Effective Token Ratio | % tokens trong context co lien quan den task hien tai | Dung LLM classifier (Claude Haiku) phan loai tung segment: relevant/irrelevant. | Validate classifier accuracy tren 200 segments voi human labels |
| **D3. Backend Portability** | M3.1 Cross-Backend Std Dev | Standard deviation cua resolve rate qua 3 LLM backends | std(RR_claude, RR_gpt, RR_deepseek) | — |
| | M3.2 Min/Max Ratio | min(RR) / max(RR) qua cac backends | Ty le truc tiep | Gia tri cao = portable |

> **Thay doi so voi v1:**
> - Giam tu 5 chieu (11 metrics) → **3 chieu (7 metrics)**
> - M1.1: Doi "ground-truth duy nhat" → **tap hop acceptable tools** (giai quyet cau hoi #4)
> - M2.2: Doi "token waste" mo ho → **LLM classifier + human validation** (giai quyet cau hoi #9)
> - Bo M4.2 (GPT-judge, circular reasoning) va D4 (Session Continuity)

### 3.3. Fork SWE-Agent thanh Modular Harness (MT2)

**Tai sao fork thay vi tu xay?**
- SWE-Agent: open-source (MIT), ~15,000 LOC, da ho tro nhieu backends
- Fork va refactor: thay doi **3 modules** (tool_config, context_strategy, model_backend)
- Giu nguyen orchestration logic → dam bao baseline quality

**Tieu chi chap nhan MT2:**
- Modular harness dat resolve rate **tuong duong SWE-Agent goc +/- 3%** tren 50 tasks kiem chung
- Co the swap tool set (12/8/5/3 tools) bang config file
- Co the swap context strategy (full/sliding-window/summary) bang config file
- Co the swap backend (Claude/GPT/DeepSeek) bang config file

**Thoi gian du kien:** 2-3 tuan (thay vi 1-3 thang neu tu xay)

### 3.4. Pilot Study (MT3 — giai doan 1)

**Truoc khi cam ket full experiment, chay pilot:**

| Hang muc | Chi tiet |
|----------|---------|
| **So conditions** | 5 (thay vi 27): Full, Tat 2 tools, Tat context mgmt, Doi GPT, Doi DeepSeek |
| **So tasks** | 20 (chon ngau nhien tu 150) |
| **So runs** | 2 runs/condition (do reproducibility) |
| **Tong evaluations** | 5 x 20 x 2 = **200 evaluations** |
| **Chi phi du kien** | ~$50-80 |
| **Thoi gian** | 1-2 tuan |

**Muc dich pilot:**
1. Validate metrics: cac metrics co **phan biet duoc** giua conditions khong? (neu 2 conditions cho ket qua giong nhau → merge → giam tong conditions)
2. Uoc tinh chi phi chinh xac cho full experiment
3. Debug pipeline (Docker, API, logging)
4. Tinh preliminary effect sizes de xac nhan power analysis

### 3.5. Full Ablation Study (MT3, MT4 — giai doan 2)

**Thiet ke thuc nghiem:**

| Factor | Levels | Chi tiet |
|--------|--------|---------|
| Tool Config | 3 | Full (12 tools) / Medium (8 tools) / Minimal (5 tools) |
| Context Strategy | 3 | Full context / Sliding window (50K tokens) / Summary-based |
| LLM Backend | 3 | Claude Sonnet 4 / GPT-4o / DeepSeek-V3 |
| **Tong conditions** | **27** | 3 x 3 x 3 full factorial |

**Dataset:** 150 tasks tu SWE-bench Verified
- Chon bang **stratified random sampling** theo do kho (easy/medium/hard dua tren so luong models da giai duoc)
- Loai bo tasks co Docker environment khong on dinh (pre-filter)

**So runs:**
- 10 conditions quan trong nhat: **3 runs** (report mean +/- std)
- 17 conditions con lai: **1 run**
- Tong evaluations: (10 x 3 + 17 x 1) x 150 = **7,050 evaluations**

> **Thay doi so voi v1:** Giam tu 16,000 → **7,050 evaluations** (giam 56%). Van du power cho ANOVA.

**Phan tich thong ke (MT4):**
- ANOVA 2 chieu: Factor A (Tool x Context = 9 levels) x Factor B (Backend = 3 levels)
- Report: F-statistic, p-value (sau Bonferroni correction), eta-squared (η²)
- Post-hoc: Tukey HSD cho pairwise comparisons
- Effect size: Cohen's d cho moi comparison
- Power analysis: voi 150 tasks, 27 conditions, alpha = 0.05, power >= 0.80

### 3.6. Threats to Validity

**Internal validity:**
- **Confounding:** Tat tool co the thay doi bai toan, khong chi harness quality. Mitigation: giam tools theo muc do (12→8→5), khong tat hoan toan. Ghi nhan task nao **can** tool bi tat → loai khoi phan tich component do.
- **LLM non-determinism:** Temperature > 0 gay variance. Mitigation: set temperature = 0 cho tat ca backends. Chay 3 runs cho conditions chinh.
- **SWE-bench environment instability:** Mot so Docker env khong on dinh. Mitigation: pre-filter tasks, retry 2 lan neu fail.

**External validity:**
- Chi test tren Python (SWE-bench Verified). Tool system cho Python (pytest, pip) khac Java (maven, junit). **Ket qua can caution khi generalize sang ngon ngu khac.**
- Chi test open-source harnesses (SWE-Agent fork). Commercial harnesses (Claude Code, Cursor) co the co behavior khac.

**Construct validity:**
- M1.1 (Correct Selection) phu thuoc annotator judgment. Mitigation: 2 annotators, do Fleiss' kappa.
- M2.2 (Effective Token Ratio) dung LLM classifier. Mitigation: validate classifier tren 200 segments voi human labels.

### 3.7. Risk Analysis

| Risk | Xac suat | Tac dong | Mitigation |
|------|----------|---------|------------|
| SWE-bench Docker fail nhieu tasks | Trung binh | Giam sample size | Pre-filter, backup tasks |
| API cost vuot budget | Cao | Khong du tien chay het | Pilot study uoc tinh truoc, dung DeepSeek (re nhat) cho nhieu conditions |
| Modular harness kem SWE-Agent >3% | Thap | MT2 fail | Giu nguyen code SWE-Agent, chi refactor config |
| Metrics khong phan biet giua conditions | Trung binh | Taxonomy vo nghia | Pilot study phat hien som, doi metric |
| Expert khong co thoi gian validate | Trung binh | MT1 cham tre | Online survey thay vi meeting, tang so expert |
| DeepSeek API khong on dinh | Thap | Mat 1 backend | Backup: Qwen2.5-72B hoac Llama-3.1-70B |

---

## CHUONG 4: DU KIEN KET QUA NGHIEN CUU

### 4.1. Ket qua du kien (trung tinh — chi neu hypotheses)

**MT1:** Taxonomy 3 chieu, 7 metrics, Fleiss' kappa >= 0.6.

**MT2:** Modular harness tuong duong SWE-Agent +/- 3%.

**MT3 — Ablation:** Nghien cuu se tra loi:
- Component nao dong gop nhieu nhat vao resolve rate? (**H1:** Tool system co effect size lon nhat)
- Context management anh huong the nao? (**H2:** Effect size trung binh)
- Harness configuration giai thich bao nhieu % variance? (**H3:** >= 20%)
- Harness tot co giam gap giua cac backends khong? (**H4:** Interaction effect co y nghia)

> **Thay doi so voi v1:** Khong du doan con so cu the ("30-40%"). Chi neu hypotheses co the kiem chung. Du thanh cong hay bac bo hypotheses deu la dong gop.

**MT4:** ANOVA table phan tach variance harness vs LLM.

**MT5:** GitHub repo voi documentation, CI/CD.

### 4.2. Y nghia khoa hoc

- **Dong gop ly thuyet:** Formalize cach phan tach harness quality khoi LLM quality (ANOVA 2 chieu)
- **Dong gop thuc nghiem:** Dinh luong dong gop tung component harness lam dau
- **Toolkit:** Framework danh gia co the tai su dung

### 4.3. Y nghia thuc tien

- **Developer:** Biet nen uu tien cai thien component nao cua harness
- **Researcher:** Framework chuan de so sanh harness moi
- **Industry:** Guidelines thiet ke harness dua tren du lieu

### 4.4. Publishability

| Venue | Loai | Phu hop |
|-------|------|---------|
| ICSE 2027 NIER | Conference (New Ideas) | Rat phu hop — coding agent + evaluation |
| MSR 2027 | Conference | Phu hop — mining SE data |
| LLM Agents Workshop (NeurIPS/ICML) | Workshop | Phu hop — agent evaluation |
| EMNLP Demo Track | Conference | Phu hop — toolkit demonstration |

---

## CHUONG 5: KE HOACH THUC HIEN

| Giai doan | Thoi gian | Noi dung | San pham |
|-----------|-----------|----------|----------|
| GD1 | Tuan 1-6 | Thiet ke taxonomy + expert validation (5 experts, Fleiss' kappa) | Taxonomy v1.0, validation report |
| GD1.5 | Tuan 7-8 | **Pilot study** (5 conditions x 20 tasks x 2 runs = 200 evals) | Pilot report: metrics validation, cost estimate, effect sizes |
| GD2 | Tuan 9-11 | Fork SWE-Agent + refactor modular + verify +/- 3% | Modular harness v1.0 |
| GD3 | Tuan 12-18 | Full ablation (27 conditions x 150 tasks = 7,050 evals) | Raw data, ANOVA results |
| GD4 | Tuan 19-22 | Phan tich + guidelines + viet luan van | Luan van ban thao |
| GD5 | Tuan 23-24 | Review, chinh sua, phat hanh toolkit | Luan van final, GitHub release |

> **Thay doi so voi v1:** Them GD1.5 (pilot study). Tang GD3 tu 8 tuan → 7 tuan (it evaluations hon). Tong van 6 thang nhung phan bo hop ly hon.

### Chi phi du kien (da tinh lai)

| Hang muc | Tinh toan | Chi phi |
|----------|-----------|---------|
| Pilot | 200 evals x $0.27 = $54 | ~$80 (voi retry) |
| Full experiment | 7,050 evals x $0.27 = $1,904 | ~$2,500 (voi retry 30%) |
| Backup/debugging | 20% contingency | ~$500 |
| **Tong** | | **$2,500 - 3,100** |

> **Thay doi so voi v1:** Tang tu $800-1,200 → **$2,500-3,100** (thuc te hon, van trong kha nang). Giam so evaluations tu 16,000 → 7,050 giup giam chi phi.

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
[E1] P. Chhikara et al., "Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory," arXiv:2504.19413, 2025.
[E2] W. Xu et al., "A-MEM: Agentic Memory for LLM Agents," arXiv:2502.12110, 2025.
[F2] Y. Qin et al., "ToolLLM: Facilitating LLMs to Master 16000+ Real-world APIs," arXiv:2307.16789, 2023.
[F3] Y. Du et al., "AnyTool: Self-Reflective Hierarchical Agents for Large-Scale API Use," arXiv:2402.04253, 2024.
[F5] S. Yuan et al., "EASYTOOL: Enhancing LLM-based Agents with Concise Tool Instruction," arXiv:2401.06201, 2024.
[G3] C. Ma et al., "AgentBoard: An Analytical Evaluation Board of Multi-Turn LLM Agents," arXiv:2401.13178, 2024.
[I2] J. Wang et al., "Illuminating LLM Coding Agents: Visual Analytics," arXiv:2508.12555, 2025.
[S1] L. Wang et al., "A Survey on LLM based Autonomous Agents," arXiv:2308.11432, 2023.
[S5] "Survey on Evaluation of LLM-based Agents," arXiv:2503.16416, 2025.

---

## PHU LUC A: BANG SO SANH V1 vs V2

| Hang muc | V1 (truoc phan bien) | V2 (sau phan bien) | Ly do thay doi |
|----------|---------------------|--------------------|----|
| So chieu | 5 | **3** | Giam scope, Safety/Session → future work |
| So metrics | 11 | **7** | Bo metrics mo ho (M4.2 GPT-judge) |
| So conditions | 80 | **27** | Full factorial 3x3x3, kha thi 6 thang |
| So evaluations | 16,000 | **7,050** | Giam 56%, van du power |
| Harness | Tu xay tu dau | **Fork SWE-Agent** | Giam rui ro, giam thoi gian |
| Budget | $800-1,200 | **$2,500-3,100** | Thuc te hon (tinh retry, pilot) |
| Pilot study | Khong co | **Co (200 evals)** | Validate truoc khi cam ket |
| ANOVA | Khong co | **Co (2 chieu)** | Phan tach harness vs LLM |
| Hypotheses | Du doan "30-40%" | **H1-H4 trung tinh** | Tranh confirmation bias |
| Threats to validity | Khong co | **Co (3 loai)** | Yeu cau cua hoi dong |
| Risk analysis | Khong co | **Co (6 risks)** | Yeu cau cua hoi dong |
| Expert validation | 3 experts, Cohen's kappa | **5 experts, Fleiss' kappa** | Thong ke tot hon |
| Claim "dau tien" | "Taxonomy dau tien" | **"Tong hop dau tien"** | Chinh xac hon |
