# THAO LUAN VA PHAN BIEN: De cuong HarnessEval

> Nguoi phan bien: Thanh vien hoi dong bao ve de cuong
> Ngay: 06/04/2026
> De tai: HarnessEval — Khung danh gia da chieu cho ha tang cua Coding Agent dua tren Mo hinh Ngon ngu Lon

---

## 1. Danh gia tong quan

### 1.1. Diem manh chinh cua de cuong

1. **Research gap xac dinh ro rang va co gia tri:** Viec tat ca 32/49 papers chi danh gia output cua agent ma khong ai danh gia ban than harness la mot nhan xet sac ben. Day la goc nhin "meta-evaluation" co y nghia khoa hoc that su.

2. **Cau truc de cuong chat che:** De cuong trinh bay logic tu van de → muc dich → phuong phap → ket qua du kien mot cach mach lac. Muc tieu dinh luong cu the (5 MT), co metric ro rang.

3. **Phuong phap nghien cuu co chieu sau:** Viec ket hop taxonomy design + modular harness implementation + ablation study la mot thiet ke nghien cuu 3 tang co he thong. Viec dung fractional factorial design de giam 729 conditions xuong 80 cho thay tac gia hieu ve thiet ke thuc nghiem.

4. **Tai lieu tham khao cap nhat va phong phu:** 49 papers tu 2023-2026, bao gom ca cac papers moi nhat (2026) nhu Bui et al., Lou et al. Cho thay tac gia nam bat duoc xu huong nghien cuu hien tai.

5. **Tinh thuc tien cao:** Open-source toolkit, design guidelines cho developer — co gia tri ung dung thuc te, khong chi la nghien cuu ly thuyet.

### 1.2. Diem yeu chinh cua de cuong

1. **Pham vi qua rong cho master's thesis 6 thang:** 5 chieu, 11 metrics, 3 harnesses, 3 backends, 80 conditions, 16,000 evaluations — day giong scope cua mot PhD dissertation hon la master's thesis.

2. **"Do harness doc lap voi LLM" la mot tuyen bo kho chung minh:** Harness va LLM tuong tac chat che (harness prompt LLM, LLM quyet dinh tool call). Viec tach roi hai yeu to nay ve mat thuc nghiem chua duoc lam ro du.

3. **Du kien ket qua qua cu the va co bias xac nhan:** Viec viet san "tool system dong gop ~30-40%" truoc khi lam thuc nghiem cho thay tac gia co the da co ket luan truoc, de dan den confirmation bias.

4. **Modular harness tu xay dung la rui ro lon:** Implement mot harness du tot de so sanh cong bang voi SWE-Agent va OpenHands (da phat trien nhieu thang/nam) la cuc ky kho trong 1 thang.

5. **Thieu ban luan ve threats to validity:** De cuong khong de cap internal validity, external validity, construct validity — day la thieu sot nghiem trong cho mot nghien cuu thuc nghiem.

### 1.3. Diem tong the

| Tieu chi | Diem (thang 10) | Nhan xet |
|----------|-----------------|----------|
| Tinh moi | 8.5 | Goc nhin meta-evaluation moi, nhung can kiem chung "dau tien" |
| Tinh kha thi | 5.5 | Scope qua rong, thoi gian va ngan sach cang |
| Chat luong phuong phap | 7.0 | Thiet ke tot nhung co lo hong ve validity |
| Tai lieu tham khao | 8.0 | Phong phu, cap nhat |
| Trinh bay | 7.5 | Mach lac, co cau truc |
| **Tong** | **7.3/10** | **Can chinh sua dang ke ve scope va phuong phap** |

---

## 2. Phan bien chi tiet

### 2.1. Ve ten de tai

**Ten de tai co don nghia, ro rang khong?**

Ten tieng Anh "HarnessEval: A Multi-Dimensional Evaluation Framework for LLM-based Coding Agent Infrastructure" kha dai nhung truyen dat du y. Tuy nhien, co mot so van de:

- Tu "Infrastructure" trong ten co the gay nham lan voi cloud infrastructure, DevOps. Nen dung "Scaffold" hoac giu "Harness" — vi chinh tac gia da dinh nghia "harness" la thuat ngu chinh.
- "Multi-Dimensional" la tu qua chung, nhieu framework nao cung tu nhan la multi-dimensional. Nen cu the hoa: "5-Dimensional" hoac bo di.
- "HarnessEval" la mot ten tot — ngan gon, de nho, co tinh branding.

**Goi y chinh sua:**
> "HarnessEval: Evaluating Coding Agent Scaffolds Through Ablation-Driven Multi-Dimensional Analysis"

Them "Ablation-Driven" de lam noi bat phuong phap nghien cuu, phan biet voi cac framework danh gia khac.

### 2.2. Ve dat van de va research gap

**Research gap co thuyet phuc khong?**

Research gap duoc trinh bay **kha thuyet phuc** voi bang chung dinh luong (32/49 papers chi do output). Tuy nhien, toi co nhieu lo ngai:

**Lo ngai 1: "Artificial gap" — Gap co phai la gap thuc su hay do khong ai can?**

Cau hoi quan trong nhat: **Tai sao cac nhom nghien cuu hang dau (OpenAI, Anthropic, Princeton — nhom phat trien SWE-Agent) khong lam viec nay?** Co phai vi:
- (a) Ho chua nghi ra? → Kho tin, vi ho la nguoi tao ra harness.
- (b) Ho dang lam nhung chua cong bo? → Co the, nhung khong co bang chung.
- (c) Ho cho rang khong can thiet vi harness evaluation khong tach roi duoc khoi LLM evaluation? → **Day la kha nang cao nhat va can duoc thao luan nghiem tuc.**

Khi ban viet "Khi bao cao Claude dat 70% tren SWE-bench, chung ta khong biet tool system goi dung tool bao nhieu phan tram" — cau hoi la: **co ai can biet khong?** Neu resolve rate da la 70%, nguoi dung quan tam resolve rate, khong quan tam tool call efficiency. Day giong nhu hoi "xe chay 200km/h nhung hop so sang so may lan?" — thong tin nay co the thu vi nhung khong phai luc nao cung actionable.

**Lo ngai 2: Lam sao biet 49 papers la representative?**

Tac gia noi phan tich 49 papers nhung khong mo ta search strategy. Day la mot systematic review hay chi la convenience sampling? Neu chi search tren arXiv voi mot vai tu khoa, co the bo sot papers tren venue khac (ICSE, FSE, ASE — cac hoi nghi SE chinh).

**Lo ngai 3: "Harness quan trong khong kem model" — bang chung con yeu**

Lou et al. (2026) chi chung minh tren game environment, khong phai coding. Bui et al. (2026) la paper cua chinh Anthropic mo ta san pham cua ho (OpenDev) — co conflict of interest. Can them bang chung doc lap, khach quan.

### 2.3. Ve muc dich va muc tieu

**Muc dich (dinh tinh) co ro rang khong?**

Muc dich viet: "xay dung khung danh gia da chieu **dau tien**..." — tu "dau tien" la mot claim manh, can than trong. Neu co mot paper nao do (du la workshop paper, technical report, blog post) da de xuat evaluation cho harness component, claim nay se bi vo hieu hoa.

**Phan tich tung muc tieu dinh luong:**

| MT | Danh gia | Van de |
|----|----------|--------|
| MT1 | **Kha** — Co metric cu the (11+ metrics, 3 expert, Cohen's kappa) | "It nhat 3 chuyen gia" — 3 la so toi thieu, nen la 5-7 de co thong ke tot hon. Cohen's kappa cho 3 nguoi khong phu hop — nen dung Fleiss' kappa. |
| MT2 | **Yeu** — Mo ho ve chat luong | "Implement modular reference harness" — khong co metric nao do chat luong cua harness nay. No chi can chay duoc hay phai dat performance tuong duong SWE-Agent? |
| MT3 | **Kha** — Cu the ve so luong | "200 tasks, 50+ conditions" — nhung khong ro tieu chi chon 200 tasks tu SWE-bench Verified (tong co 500 tasks). Random sampling? Stratified? |
| MT4 | **Trung binh** — p < 0.05 la can thiet nhung chua du | Khong de cap multiple comparison correction (Bonferroni, FDR). Voi 11 metrics va nhieu conditions, van de multiple testing la nghiem trong. |
| MT5 | **Yeu** — Khong co metric | "Phat hanh open-source" — khong co tieu chi nao de biet khi nao MT5 "hoan thanh." So sao GitHub? So nguoi dung? Documentation coverage? |

**Phan biet muc dich vs muc tieu:**

Muc dich (1.2) va MT1-MT5 (1.3) co su chong cheo. Muc dich da noi "xay dung khung danh gia" — giong het MT1. Muc dich nen la **why** (vi sao can lam), muc tieu la **what** (lam cai gi cu the). Hien tai muc dich doc giong nhu phien ban tom tat cua muc tieu.

### 2.4. Ve phuong phap nghien cuu

**2.4.1. Taxonomy 5 chieu co hop ly khong?**

Day la phan quan trong nhat cua de cuong. Toi co nhieu cau hoi:

**Tai sao 5 chieu ma khong phai 3 hoac 7?**

- **Co the giam xuong 3:** D1 (Tool Dispatch), D2 (Context Utilization), va D5 (Backend Portability) la 3 chieu "cot loi." D3 (Safety) va D4 (Session Continuity) co the xem la thuoc tinh phu, khong phai chieu danh gia doc lap. Safety la ràng buoc (constraint), khong phai metric hieu suat. Session continuity thuc chat la bien the cua context management theo thoi gian.
- **Co the tang len 7:** Thieu cac chieu quan trong:
  - **Error Recovery:** Khi tool call fail hoac LLM hallucinate, harness xu ly ra sao? Day la thanh phan cuc ky quan trong ma SWE-Agent va OpenHands xu ly rat khac nhau.
  - **Orchestration Strategy:** Cach harness dieu phoi agent loop (ReAct vs Plan-Execute vs Tree-of-Thought) anh huong lon den hieu suat. De cuong liet ke Layer 5 (Orchestration) trong mo hinh 5 lop nhung **khong co chieu danh gia tuong ung**.
  - **Cost Efficiency:** Token cost per resolved task — rat thuc te cho industry adoption.

**Nhu vay, mo hinh 5 lop (Section 2.2.1) co 5 layers, nhung taxonomy (Section 3.2) cung co 5 chieu — day co phai la trung hop khong?** Hay tac gia da map 1-1 layer sang dimension? Neu vay, can giai thich tai sao moi layer chinh xac tuong ung mot evaluation dimension — dieu nay khong hien nhien.

**2.4.2. Van de voi tung metric:**

- **M1.1 Correct Selection Rate:** "So sanh voi ground-truth tool sequence tu expert" — **ai la expert?** Tac gia? Advisor? Thuê annotator? Mot coding task co nhieu cach giai dung voi nhieu tool sequence khac nhau. Ground-truth cho tool sequence la **khong duy nhat**. Day la van de construct validity nghiem trong.
- **M1.3 Redundant Call Rate:** "Expert annotation tren sample" — bao nhieu sample? Inter-annotator agreement bao nhieu la chap nhan duoc? Redundancy la khai niem chu quan — mot tool call co the "thua" voi nguoi nay nhung "can thiet de kham pha" voi nguoi khac.
- **M2.1 Info Retention:** "So sanh output truoc/sau compaction" — dung cai gi de so sanh? ROUGE? BERTScore? Human judgment? Metric nay can operationalize ro hon.
- **M2.2 Token Waste Ratio:** "Phan tich token attribution" — day la bai toan research rieng (token attribution cho LLM). Lam sao xac dinh token nao "khong lien quan"? Can dinh nghia formal.
- **M4.2 Instruction Adherence:** "GPT-judge kiem tra adherence" — dung GPT de judge trong nghien cuu ve LLM agent co van de circular reasoning khong? LLM danh gia LLM.

**2.4.3. Ablation study design:**

**Van de chinh: Confounding variables**

Khi ban "tat" tool system (tu 12 tools xuong 5 tools), performance giam. Nhung giam vi:
- (a) Harness mat tool → agent khong co cong cu → fail? (confound voi task requirement)
- (b) Harness tool dispatch kem? (dieu ban muon do)

Hai dieu nay khac nhau hoan toan. Neu task can `grep` ma ban tat `grep`, tat nhien fail — nhung do khong phai loi cua harness, do la loi cua cau hinh. **Ablation study cho harness khong giong ablation study cho neural network** (noi tat mot layer la straightforward). Tat mot tool trong harness co the lam thay doi bai toan, khong chi lam thay doi "chat luong harness."

**Van de voi fractional factorial design:**

Latin square yeu cau cac factors doc lap. Nhung cac component harness **tuong tac voi nhau** — tool system can context de biet goi tool nao, safety layer phai biet tool nao dang chay. Tat safety layer co the lam tool system chay nhanh hon (khong bi check). Cac interaction effects nay phuc tap va fractional factorial co the bo sot.

**16,000 evaluations — co thuc hien duoc khong?**

Moi SWE-bench task can trung binh 10-30 phut de agent chay (bao gom setup Docker, chay tests). 16,000 evaluations x 20 phut = 5,333 gio = 222 ngay chay lien tuc. Du chay parallel 10 luong, van can 22 ngay — chua tinh retry, failure, debugging. Trong 4-6 tuan cua GD3, day la **rat cang**.

Them nua, chi phi: 16,000 evaluations x trung binh $0.10-0.50 per task (bao gom retries, long conversations) = $1,600-8,000. Con so $800-1,200 trong de cuong co ve **underestimate nghiem trong**.

### 2.5. Ve tinh kha thi

**6 thang co du khong?**

| Giai doan | Thoi gian de cuong | Thoi gian thuc te du kien | Rui ro |
|-----------|-------------------|---------------------------|--------|
| GD1: Taxonomy + Expert validation | 2 thang | 2-3 thang | Tim 3 expert san long review va cho feedback mat thoi gian. Scheduling la bottleneck. |
| GD2: Implement modular harness | 1 thang | 2-3 thang | SWE-Agent co ~15,000 LOC, OpenHands ~50,000 LOC. Viet harness tu dau du la "modular" cung can it nhat 3,000-5,000 LOC voi tests. 1 thang la **bat kha thi** neu muon chat luong tuong duong. |
| GD3: Ablation study | 2 thang | 3-4 thang | 16,000 evaluations, debugging failures, re-runs. SWE-bench setup notoriously kho (Docker, dependency issues). |
| GD4: Phan tich + Viet | 1 thang | 2 thang | Phan tich thong ke 80 conditions x 11 metrics can nhieu thoi gian. |
| **Tong** | **6 thang** | **9-12 thang** | **Overrun 50-100%** |

**$800-1,200 API cost co thuc te khong?**

Tinh nhanh:
- 80 conditions x 200 tasks = 16,000 runs
- Moi run trung binh 20 turns, moi turn ~2,000 tokens input + 500 tokens output
- Claude Sonnet: ~$3/M input, $15/M output → moi run ~$0.12 input + $0.15 output = $0.27
- GPT-4o: tuong tu
- 16,000 x $0.27 = **$4,320** chi rieng API calls thanh cong
- Chua tinh: retries (20-30% tasks fail lan dau), debugging runs, pilot experiments

**Uoc tinh thuc te: $3,000-6,000** — gap 3-5x so voi de cuong.

**Implement modular harness trong 1 thang:**

Nhu da phan tich, day la rui ro lon nhat. Goi y: **Dung fork SWE-Agent** lam base va modify thanh modular, thay vi viet tu dau. Nhu vay giam effort tu 3 thang xuong 1 thang va dam bao baseline performance.

**Risks va mitigation strategies:**

De cuong **hoan toan khong co muc risk analysis**. Day la thieu sot lon. Cac risks chinh:
1. SWE-bench Docker setup fail cho 1 so tasks → mitigation: pre-filter tasks
2. API cost vuot ngan sach → mitigation: pilot study 10% truoc
3. Modular harness qua yeu → mitigation: fork SWE-Agent
4. Expert khong co thoi gian validate → mitigation: thu thap feedback qua survey thay vi meeting
5. DeepSeek API khong on dinh → mitigation: co backup model (Qwen, Llama)

### 2.6. Ve dong gop khoa hoc

**"Taxonomy dau tien" — co chac la dau tien khong?**

Toi nghi ngo claim nay. Can kiem tra ky:
- AgentBoard (Ma et al., 2024) da co multi-dimensional evaluation voi **progress rate** — day co phai la mot dang harness evaluation khong? (Tuy AgentBoard do output quality, nhung metric "progress" do process, khong chi do ket qua cuoi.)
- Cac papers ve tool-use evaluation (ToolLLM, AnyTool) da co metrics cho tool selection accuracy — day la D1 trong taxonomy cua tac gia.
- Papers ve LLM safety evaluation da co metrics cho safety enforcement — day la D3.

Nhu vay, **tung chieu rieng le da co nguoi nghien cuu**. Dong gop cua tac gia la **tong hop chung lai thanh framework thong nhat cho coding agent harness**. Nen viet lai claim thanh: "Framework tong hop dau tien..." thay vi "Taxonomy dau tien..."

**Dong gop co du cho master's thesis?**

Neu thuc hien day du MT1-MT5 — **qua du**, tham chi qua nhieu cho master's. Van de la khong ai co the lam tat ca trong 6 thang. Goi y: **chon MT1 + MT3 (taxonomy + ablation study) la core**, MT2 don gian hoa (fork SWE-Agent), MT5 la bonus.

**Publishability?**

De tai co kha nang publish duoc tai:
- **Workshop papers:** LLM Agents Workshop (NeurIPS, ICML)
- **Conference:** EMNLP, ACL (demo track voi toolkit), MSR (Mining Software Repositories)
- **Nen target:** ICSE 2027 NIER (New Ideas and Emerging Results) — phu hop nhat vi la coding agent + evaluation

Tuy nhien, de publish thi can:
- Scale thuc nghiem du lon (200 tasks la ok, nhung can nhieu backend hon)
- Comparison voi naive baselines
- Reproducibility (open-source la diem cong)

---

## 3. Cau hoi phan bien (10 cau hoi kho)

### Cau hoi 1: Ve tinh doc lap cua harness evaluation
**Hoi:** "Ban noi do harness 'doc lap voi LLM.' Nhung tool dispatch efficiency phu thuoc vao LLM quyet dinh goi tool nao — do la quyet dinh cua LLM, khong phai cua harness. Lam sao ban tach roi hai yeu to nay?"

**Goi y tra loi:** Harness quyet dinh **cung cap** tools nao, format tool description ra sao, retry policy khi tool fail. LLM quyet dinh **chon** tool. Nghien cuu nay do chat luong cua "buffet" (harness), khong phai "khau vi" (LLM) — cung nhu danh gia nha hang qua thuc don va dich vu, khong phai qua khau vi khach hang. Tuy nhien, can acknowledge day la limitation — harness va LLM co coupling.

### Cau hoi 2: Ve artificial gap
**Hoi:** "Tai sao nhom phat trien SWE-Agent (Princeton) va Anthropic (Claude Code) — nhung nguoi hieu harness nhat — khong tu lam viec nay? Co phai vi ho biet rang danh gia harness rieng le khong co y nghia?"

**Goi y tra loi:** (1) Cac nhom nay la developers, khong phai evaluators — ho co incentive de xuat harness moi, khong phai de xuat cach so sanh harness. (2) Su tang truong cuc nhanh cua linh vuc (2023-2026) khien chua ai dung lai de meta-evaluate. (3) Thuc te Lou et al. (2026) da gian tiep acknowledge viec nay khi so sanh harness tren game tasks. Nghien cuu nay formalize quy trinh so sanh do.

### Cau hoi 3: Ve scale thuc nghiem
**Hoi:** "16,000 evaluations nghe nhieu, nhung moi condition chi co 200 data points. Voi 11 metrics, power analysis cho thay ban can bao nhieu samples de detect effect size trung binh (Cohen's d = 0.5) voi power 0.80?"

**Goi y tra loi:** Voi two-sample t-test, d = 0.5, alpha = 0.05, power = 0.80 → can ~64 samples/group. 200 tasks la du. Tuy nhien, khi so sanh nhieu conditions (80), can Bonferroni correction → alpha giam xuong 0.05/C(80,2) — luc nay 200 co the khong du. Can trinh bay power analysis chinh thuc trong de cuong.

### Cau hoi 4: Ve construct validity cua metrics
**Hoi:** "M1.1 (Correct Selection Rate) dung 'ground-truth tool sequence tu expert.' Nhung mot task co the co 5 cach giai dung voi 5 tool sequences khac nhau. Ground-truth cua ban la gi — tat ca cach giai dung, hay chi mot cach? Ai quyet dinh?"

**Goi y tra loi:** Ground-truth nen la **tap hop cac tool sequences chap nhan duoc** (set of acceptable sequences), khong phai mot sequence duy nhat. Can dinh nghia equivalence classes cho tool sequences (vi du: grep + read = search + read ve mat muc dich). Dung 2-3 annotators va do inter-annotator agreement. Neu agreement thap, metric nay co van de construct validity.

### Cau hoi 5: Ve modular harness
**Hoi:** "Modular harness cua ban tu xay trong 1 thang — SWE-Agent phat trien 2 nam voi doi ngu Princeton. Khi so sanh va modular harness thua SWE-Agent tren moi chieu, ban se ket luan gi? Day co phai la unfair comparison?"

**Goi y tra loi:** (1) Muc dich khong phai de so sanh "harness nao tot hon" ma de **do dong gop cua tung component**. Modular harness la cong cu thuc nghiem (tat/bat component) khong phai san pham canh tranh. (2) Nen viet ro dieu nay trong scope. (3) Tuy nhien, nen fork SWE-Agent lam base de dam bao baseline quality.

### Cau hoi 6: Ve tinh tong quat hoa
**Hoi:** "Ban chi test tren Python (SWE-bench Verified). Harness tot cho Python co tot cho Java, Rust, JavaScript khong? Ket qua cua ban generalize duoc toi dau?"

**Goi y tra loi:** Day la external validity limitation can acknowledge ro rang. SWE-bench Verified la benchmark duoc chap nhan rong rai nhat, dung lam starting point. Tuong lai co the mo rong voi SWE-Compass (10 ngon ngu). Tuy nhien, co co so de nghi ngu generalizability vi: (1) tool system cho Python (pytest, pip) khac voi Java (maven, junit), (2) context pattern khac nhau giua ngon ngu.

### Cau hoi 7: Ve chi phi va hieu qua
**Hoi:** "Gia su ket qua cho thay tool system dong gop 35% vao resolve rate. So nay co y nghia gi cho developer? Ho nen lam gi voi thong tin nay?"

**Goi y tra loi:** Cau hoi rat tot — day la actionability. Con so 35% chi la descriptive. Can di sau hon: tool system **cu the nao** dong gop 35%? Tool nao quan trong nhat? (grep? edit? bash?) Config nao toi uu? De cuong can them muc "Design Guidelines" duoc derive tu ket qua — vd: "Toi thieu can 5 core tools: read, write, edit, bash, grep. Them tools khac chi tang 2-3%."

### Cau hoi 8: Ve reproducibility
**Hoi:** "LLM outputs khong deterministic (temperature > 0). Ban chay moi condition 1 lan (200 tasks x 1 run). Lam sao dam bao ket qua reproducible? Neu chay lai, ket qua co thay doi bao nhieu?"

**Goi y tra loi:** Day la van de nghiem trong. Can: (1) set temperature = 0 cho tat ca backends (neu co the), (2) chay it nhat 3 runs cho moi condition va report mean ± std, (3) report confidence intervals. Tuy nhien 3 runs x 80 conditions x 200 tasks = 48,000 evaluations — gap 3x ngan sach. Trade-off: chay 3 runs cho 10-15 conditions quan trong nhat, 1 run cho phan con lai.

### Cau hoi 9: Ve GPT-judge
**Hoi:** "Ban dung GPT-judge de do M4.2 (Instruction Adherence). Day la LLM danh gia LLM — co van de circular reasoning khong? Neu GPT co cung bias voi model duoc danh gia thi sao?"

**Goi y tra loi:** Dung, day la van de. Can: (1) validate GPT-judge voi human judgment tren sample (tinh correlation), (2) dung GPT khac model voi model duoc danh gia (vd: dung Claude judge khi danh gia GPT agent va nguoc lai), (3) report inter-judge agreement giua GPT va human.

### Cau hoi 10: Ve so sanh voi don gian hon
**Hoi:** "Thay vi 5 chieu, 11 metrics, 80 conditions — ban co the chi dung 1 metric don gian: 'resolve rate khi doi backend' (portability) de chung minh harness quan trong. Tai sao can phuc tap hon?"

**Goi y tra loi:** Portability chi la 1 goc nhin. Developer can biet **tai sao** harness A tot hon B — khong chi biet **rang** A tot hon B. 5 chieu cho diagnostic power — giong nhu xet nghiem mau cho biet cu the co quan nao co van de, khong chi biet "suc khoe tong the." Tuy nhien, cau hoi nay goi y mot chien luoc tot hon: **bat dau voi 2-3 chieu cot loi, mo rong sau** — thay vi 5 chieu cung luc.

---

## 4. Goi y cai thien

### Goi y 1: Thu hep scope — chon 3 chieu thay vi 5
Giam tu 5 chieu xuong 3 chieu cot loi: **D1 (Tool Dispatch), D2 (Context Utilization), D5 (Backend Portability)**. D3 (Safety) va D4 (Session Continuity) de cho "future work." Ly do:
- 3 chieu x 3 harnesses x 3 backends = 27 conditions (thay vi 80) → kha thi trong 6 thang
- Giam chi phi tu $3,000-6,000 xuong $1,000-2,000
- Van giu duoc core contribution

### Goi y 2: Fork SWE-Agent lam modular harness, khong viet tu dau
SWE-Agent da la open-source (MIT license). Fork va refactor thanh modular architecture:
- Thay doi tool set → da co san trong SWE-Agent
- Doi backend → SWE-Agent da ho tro nhieu model
- Doi context strategy → chi can modify 1 module
Nhu vay giam GD2 tu 2-3 thang xuong 2-3 tuan va dam bao quality.

### Goi y 3: Them power analysis va muc risk analysis
- Trinh bay power analysis chinh thuc: sample size, effect size, alpha, power
- Them muc "Threats to Validity" voi 3 loai: internal, external, construct
- Them muc "Risk Mitigation" voi 5 risks chinh va mitigation plan
- Them multiple comparison correction (Bonferroni hoac Benjamini-Hochberg FDR)

### Goi y 4: Bo phan "Du kien ket qua" hoac viet lai trung tinh
Viet "du kien tool system dong gop 30-40%" tao bias xac nhan. Nen viet:
- "Nghien cuu se dinh luong dong gop cua tung component"
- Khong dua ra con so cu the — de ket qua thuc nghiem tu noi
- Chi neu hypotheses (vi du: H1: "Tool system co effect size lon nhat"), khong phai predictions

### Goi y 5: Them pilot study
Truoc khi chay full experiment (80 conditions), chay pilot:
- 5 conditions x 20 tasks = 100 evaluations
- Muc dich: (1) validate metrics co phan biet duoc giua conditions khong, (2) uoc tinh cost chinh xac, (3) debug pipeline
- Neu pilot cho thay 2 conditions khong khac biet thong ke, co the merge → giam tong so conditions

### Goi y 6: Dinh nghia formal cho "independence" cua harness evaluation
Can mot section ly thuyet giai thich:
- Khi nao metric M do harness quality va khi nao no do LLM quality?
- De xuat: chay **cung harness voi nhieu LLM** → phan variance do harness vs. LLM → dung ANOVA 2 chieu (harness x LLM) de phan tach
- Day chinh la gia tri khoa hoc lon nhat cua de tai — nen lam ro hon

### Goi y 7: Xem xet lai danh sach tai lieu tham khao
- Them papers tu SE venues (ICSE, FSE, ASE, ISSTA) — hien tai hau het la arXiv preprints
- Kiem tra xem co paper nao da lam "evaluation of agent infrastructure" du la ngoai coding domain
- Them papers ve ablation study methodology (khong chi trong ML ma con trong SE)
- Xac minh lai cac papers 2026 — mot so co the chua duoc peer review

---

## 5. Ket luan phan bien

### Quyet dinh: CAN CHINH SUA DANG KE TRUOC KHI THONG QUA

De cuong co y tuong tot, goc nhin moi, va trinh bay mach lac. Tuy nhien, scope qua rong cho master's thesis 6 thang, mot so metric chua duoc operationalize ro rang, va thieu phan tich feasibility nghiem tuc (chi phi, thoi gian, risks). De cuong can chinh sua dang ke truoc khi co the trien khai.

### 3 dieu can lam ngay

**1. Thu hep scope ngay lap tuc:**
Giam tu 5 chieu xuong 3 chieu, giam tu 80 conditions xuong 25-30 conditions. Tinh lai chi phi va timeline voi scope moi. Day la viec quan trong nhat — mot de tai kha thi va hoan thanh duoc co gia tri hon mot de tai tham vong nhung dang do.

**2. Lam ro construct validity cua metrics:**
Viet lai phan 3.2 (Taxonomy) voi dinh nghia formal cho moi metric. Dac biet: M1.1 (ground-truth la gi?), M2.2 (token nao la "waste"?), M4.2 (validate GPT-judge nhu the nao?). Moi metric can: definition, operationalization, validation procedure, known limitations.

**3. Them pilot study vao ke hoach:**
Chen GD1.5 (2 tuan) giua GD1 va GD2: chay pilot voi 5 conditions x 20 tasks. Dung ket qua pilot de: (a) validate metrics, (b) uoc tinh chi phi chinh xac, (c) quyet dinh so conditions cuoi cung. Dieu nay se giam rui ro dang ke cho toan bo du an.

---

> *"Mot de tai nghien cuu tot khong phai la de tai lon nhat, ma la de tai duoc thiet ke de co the that bai mot cach co y nghia — nghia la du thanh cong hay that bai, chung ta deu hoc duoc dieu gi do." Hien tai, de cuong nay duoc thiet ke de chi co the thanh cong neu moi thu deu suon se — va trong nghien cuu, moi thu khong bao gio suon se.*

---
*Het phan bien.*
