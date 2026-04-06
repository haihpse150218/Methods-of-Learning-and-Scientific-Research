# THAO LUAN VA PHAN BIEN: De cuong Ket hop (HarnessEval + SecureCodeBench)

**Nguoi phan bien:** Thanh vien hoi dong
**Ngay:** 06/04/2026
**De cuong duoc phan bien:** "Khung danh gia da chieu cho ha tang Coding Agent: Tich hop hieu suat, bao mat va kha nang thich ung voi nhieu mo hinh ngon ngu lon"

---

## 1. Danh gia tong quan

### Diem manh chinh cua de cuong

1. **Research gap duoc xac dinh ro rang va co can cu:** De cuong nhan dien 2 khoang trong nghien cuu co y nghia — (1) thieu danh gia cap harness va (2) thieu benchmark ket hop correctness + security. Ca hai gap deu duoc chung minh bang cac cong trinh cu the (49 papers), khong phai suy doan.

2. **Thiet ke thuc nghiem bai ban:** Ablation study protocol duoc thiet ke co he thong voi bien doc lap/phu thuoc ro rang. Viec phan biet harness vs. LLM backend la mot goc nhin tot, giup tach biet contribution cua tung thanh phan.

3. **Metric moi co tiem nang:** Secure Resolve Rate (SRR = RR x (1 - ASR)) la mot y tuong don gian nhung huu ich, de giao tiep va co the tro thanh metric tieu chuan neu duoc validate tot.

4. **Cam ket open-source:** Viec phat hanh toolkit va benchmark la diem cong lon ve mat dong gop thuc tien cho cong dong.

5. **Tong quan tai lieu chat luong:** 49 papers duoc tong hop co he thong, phan loai ro rang theo chu de, va mapping duoc tu limitation sang research gap.

### Diem yeu chinh cua de cuong

1. **Pham vi qua rong cho 1 nguoi trong 6 thang:** 5 muc tieu, 5 chieu danh gia, 400+ adversarial instances, 162 conditions (du chi chay 50), xay dung modular harness, validate metric, phat hanh toolkit — day la khoi luong cua mot nhom nghien cuu 3-4 nguoi.

2. **Metric SRR qua don gian hoa:** SRR = RR x (1 - ASR) gia dinh rang correctness va security co trong so bang nhau va quan he multiplicative. Dieu nay chua duoc justify ve mat ly thuyet.

3. **Expert validation yeu:** Chi 3-5 chuyen gia danh gia 30 outputs la qua nho de ket luan co y nghia thong ke ve correlation.

4. **Thieu chi tiet ve "modular harness tu xay dung":** Day la 1 trong 3 doi tuong so sanh chinh nhung khong co mo ta chi tiet kien truc, chi co cau truc folder. Neu harness nay khong tuong duong ve do phuc tap voi SWE-Agent va OpenHands, ket qua ablation se bi bias.

5. **Chi phi va thoi gian tinh toan chua thuc te:** 200 tasks x 50 conditions = 10,000 runs. Moi run tren SWE-bench mat trung binh 5-15 phut va $0.5-2 token cost. Tong chi phi co the len $5,000-20,000 va mat 3-6 thang chi de chay experiments, chua ke xay dung benchmark va viet luan van.

### Diem tong the: 7.0/10

De cuong co y tuong tot, research gap thuyet phuc, nhung pham vi qua tham vong va thieu chi tiet o nhieu cho quan trong. Can thu hep lai dang ke de kha thi cho 1 nguoi trong 6 thang.

---

## 2. Phan bien chi tiet

### 2.1. Ve ten de tai

**Ten de tai co don nghia, ro rang khong?**

Ten tieng Viet kha dai va phuc tap: "Khung danh gia da chieu cho ha tang Coding Agent: Tich hop hieu suat, bao mat va kha nang thich ung voi nhieu mo hinh ngon ngu lon." Ten nay co 2 van de:
- Tu "da chieu" kha chung chung — bao nhieu chieu? Chieu nao?
- Phan phu "Tich hop hieu suat, bao mat va kha nang thich ung voi nhieu mo hinh ngon ngu lon" qua dai, doc nhu mo ta thay vi ten de tai.

Ten tieng Anh tot hon: "HarnessEval: A Multi-Dimensional Evaluation Framework..." — co brand name (HarnessEval), scope ro rang (coding agent infrastructure), va tu khoa chinh (performance, security, portability).

**Co diem moi, tu khoa, pham vi ro rang khong?**

- Diem moi: "harness evaluation" (thay vi agent evaluation) — day la diem khac biet chinh nhung chua duoc lam noi bat du trong ten.
- Pham vi: "nhieu mo hinh ngon ngu lon" la qua rong — thuc te chi test 2-3 LLM. Nen ghi cu the hon.

**Goi y chinh sua:**
- Tieng Viet: "HarnessEval: Khung danh gia ha tang Coding Agent tren 5 chieu — Hieu suat, Bao mat, va Tinh tuong thich Backend"
- Hoac ngan gon hon: "Danh gia ha tang Coding Agent: Tu tool dispatch den prompt injection resistance"

### 2.2. Ve dat van de va research gap

**Research gap co thuyet phuc khong?**

**Gap 1 (Harness-level evaluation):** Kha thuyet phuc. De cuong chi ra dung rang SWE-bench, SWE-Compass, PRDBench deu chi do output. Tuy nhien, can phan biet ro: viec danh gia harness *doc lap voi LLM* co thuc su can thiet khong, hay chi la cach nhin khac ve cung mot van de? Neu doi harness va output tot hon, co phai harness tot hon khong, hay la do LLM phu hop hon voi harness do?

**Gap 2 (Security-integrated benchmark):** Thuyet phuc hon Gap 1. De cuong dua ra bang chung cu the: 94.4% agents de bi prompt injection (D1), 84% attack success rate (D3), nhung khong co benchmark nao ket hop security vao evaluation chinh thong. Day la gap thuc su.

**Co gap nao bi "tao ra" (artificial gap) khong?**

**Canh bao voi Gap 1:** Ly do "khai niem harness moi (2026)" co the bi phan bien la: harness luon ton tai (SWE-Agent la mot harness tu 2024), chi la thuat ngu "harness evaluation" la moi. Viec dat ten cho mot van de khong co nghia la van de do chua duoc nghien cuu. Tren thuc te, cac paper so sanh agent framework (AutoGen vs MetaGPT vs CrewAI) da ngam danh gia harness roi — chi la khong dung tu "harness evaluation".

**Bang chung co du manh khong?**

- Cac con so 94.4%, 84%, 38% deu co reference cu the — tot.
- Tuy nhien, su co "ro ri ma nguon Claude Code (thang 3/2026)" duoc dung nhu evidence nhung khong co reference hoc thuat — chi la su kien thuc te. Nen than trong khi dung su kien chua duoc peer-review lam can cu nghien cuu.

### 2.3. Ve muc dich va muc tieu

**Muc dich (dinh tinh) co ro rang khong?**

Muc dich duoc phat bieu ro: "xay dung khung danh gia da chieu cho harness, lap day khoang trong giua danh gia output va danh gia ha tang." Tuy nhien, cum tu "lap day khoang trong" la qua tham vong cho 1 luan van thac si — nen noi "dong gop vao viec thu hep khoang trong" thi chinh xac hon.

**Muc tieu (dinh luong) co do luong duoc khong?**

| Muc tieu | Do luong duoc? | Binh luan |
|---|---|---|
| MT1: Taxonomy 5 chieu, 2+ metric/chieu | Co | Nhung "validated boi chuyen gia" chua ro tieu chi nao la "validated" |
| MT2: 100 tasks + 400 adversarial | Co | Nhung chat luong cua adversarial variants moi la quan trong, khong chi so luong |
| MT3: 3 harness x 2 backend x 200 tasks | Co | Nhung 50 conditions x 200 tasks = 10,000 runs — chi phi va thoi gian? |
| MT4: Correlation > 0.85 voi expert | Co | Nhung 3-5 experts x 30 outputs la qua it cho statistical significance |
| MT5: Open-source toolkit | Co | Nhung "phat hanh" co nghia la gi? PyPI? GitHub? Documentation? |

**Co qua nhieu muc tieu cho 6 thang khong?**

**Co — day la van de lon nhat cua de cuong.** 5 muc tieu, moi muc tieu la 1 cong trinh dang ke:
- MT1 (taxonomy): 1-2 thang tu thiet ke + validate
- MT2 (benchmark): 2-3 thang tu tao 400 adversarial instances chat luong
- MT3 (ablation): 2-3 thang chay experiments
- MT4 (validate metric): 1 thang thu thap expert judgment
- MT5 (toolkit): 1-2 thang code + documentation

Tong: 7-11 thang cho 1 nguoi, khong tinh thoi gian viet luan van.

**Goi y:** Nen giam xuong 3 muc tieu chinh. Vi du: (1) Taxonomy + metric, (2) Benchmark nho hon (50 tasks x 2 loai tan cong = 100 instances), (3) Ablation study tren 2 harness x 2 backend = 4 conditions chinh.

**Phan biet muc dich vs muc tieu co dung khong?**

Co — muc dich dinh tinh (xay dung khung danh gia), muc tieu dinh luong (so lieu cu the). Tuy nhien, mot so muc tieu (MT5: open-source toolkit) la output, khong phai muc tieu nghien cuu. MT5 nen la phan phu, khong phai muc tieu chinh.

### 2.4. Ve phuong phap nghien cuu

**Phuong phap co phu hop khong?**

Phuong phap thuc nghiem (experimental) la phu hop cho loai nghien cuu nay. Tuy nhien, co mot so van de:

1. **Thieu phuong phap dinh tinh bo sung:** Taxonomy 5 chieu duoc "rut ra tu phan tich 49 papers" nhung khong co systematic methodology (e.g., Grounded Theory, Thematic Analysis). Viec map "limitations sang measurable properties" can co quy trinh cu the hon — ai lam? bao nhieu vong? inter-rater agreement nhu the nao?

2. **"Validate voi 2-3 chuyen gia" la qua mo ho:** 2-3 chuyen gia khong du de tao content validity. Can it nhat Delphi method voi 5-7 experts, hoac Card Sorting study de validate taxonomy.

**Ablation study design co hop ly khong?**

Thiet ke ablation study la diem manh nhung cung la diem yeu cua de cuong:

- **Diem manh:** Bien doc lap/phu thuoc ro rang; co controlled variables.
- **Diem yeu nghiem trong:** 3 x 2 x 3 x 3 x 3 = 162 conditions la full factorial design. Du chi chay 50 conditions, viec chon 50 conditions nao la rat chu quan. De cuong noi "uu tien cac conditions co thay doi lon" — nhung lam sao biet condition nao thay doi lon khi chua chay?

**Goi y:** Dung fractional factorial design (Taguchi method) thay vi tu chon 50/162 conditions. Dieu nay co ly thuyet chi tiet va duoc chap nhan trong cong dong ML.

**Sample size (200 tasks, 50 conditions) co du khong?**

- 200 tasks tu SWE-bench Verified: Phu hop — day la con so du lon de co statistical power.
- 50 conditions: Van de khong phai so luong conditions ma la so luong *replications* moi condition. De cuong khong noi moi condition chay bao nhieu lan. Neu chi chay 1 lan moi condition, ket qua se khong reproducible (LLM co stochastic output). Can it nhat 3 runs/condition voi temperature > 0.

**Co van de ve validity (internal/external) khong?**

- **Internal validity:** Viec "tu xay dung" 1 trong 3 harness tao ra confound — nguoi xay dung cung la nguoi danh gia. Unconscious bias co the lam cho modular harness "tuong thich tot hon" voi taxonomy ma chinh nguoi do thiet ke.
- **External validity:** Chi test tren Python SWE-bench tasks. Ket qua co the khong generalize sang ngon ngu khac (Java, JavaScript, Rust). De cuong can acknowledge han che nay ro rang hon.
- **Construct validity:** Metric "Correct Tool Selection Rate" gia dinh co mot ground truth tool sequence cho moi task. Nhung tren thuc te, co nhieu cach giai dung voi nhieu tool sequence khac nhau. Lam sao xac dinh "correct"?

### 2.5. Ve tinh kha thi

**6 thang co du thoi gian khong?**

**Khong du** voi pham vi hien tai. Phan tich chi tiet:

| Giai doan | Thoi gian de cuong | Thoi gian thuc te du kien | Ly do |
|---|---|---|---|
| GD1: Taxonomy + benchmark | 2 thang | 3-4 thang | Tao 400 adversarial instances chat luong can manual curation ky luong |
| GD2: Xay dung harness + toolkit | 1 thang | 2-3 thang | Adapter cho SWE-Agent/OpenHands phuc tap hon du kien; Docker debugging |
| GD3: Chay thuc nghiem | 2 thang | 2-4 thang | 10,000 runs x 10 phut = 1,667 gio compute; failures, retries, debugging |
| GD4: Phan tich + validate | 1 thang | 1-2 thang | Expert recruitment mat thoi gian; statistical analysis |
| GD5: Viet luan van | 1 thang | 2 thang | Viet + chinh sua + advisor review |

Tong thuc te: 10-15 thang cho 1 nguoi.

**Chi phi $500-1,000 co thuc te khong?**

**Khong thuc te.** Tinh toan chi phi API:

- 200 tasks x 50 conditions = 10,000 runs
- Moi run SWE-bench task trung binh dung 50,000-200,000 tokens (input + output)
- Claude Sonnet 4 pricing: ~$3/M input + $15/M output tokens
- GPT-4o pricing: ~$2.5/M input + $10/M output tokens
- Uoc tinh toi thieu: 10,000 runs x 100K tokens/run x $8/M tokens = **$8,000**
- Chua tinh retries, debugging, pilot runs

De cuong can tinh lai chi phi thuc te, hoac giam so luong conditions/tasks dang ke. Voi ngan sach $1,000-1,600, chi co the chay khoang **1,500-2,000 runs** — tuong duong 10 conditions x 200 tasks, khong phai 50 conditions.

**1 nguoi co lam duoc khong?**

**Kho nhung co the** neu thu hep pham vi:
- Giam tu 5 muc tieu xuong 3
- Giam tu 400 adversarial instances xuong 100
- Giam tu 50 conditions xuong 10-15 conditions chinh
- Bo modular harness tu xay dung, thay bang 1 harness co san khac (e.g., Aider, Continue)
- Bo MT5 (open-source toolkit) ra khoi muc tieu chinh — bien thanh "bonus output"

**Rui ro gi co the xay ra?**

1. **API cost vuot ngan sach:** Rui ro cao. LLM API pricing co the thay doi; SWE-bench tasks co the mat nhieu token hon du kien.
2. **SWE-Agent/OpenHands API thay doi:** Cac project open-source cap nhat lien tuc. Version duoc dung trong de cuong co the khong con tuong thich sau 3 thang.
3. **Expert recruitment:** Tim 3-5 chuyen gia san sang danh gia 30 outputs (moi nguoi mat 2-3 gio) la khong de.
4. **Docker environment failures:** SWE-bench Docker environments co the fail vi dependency issues. De cuong [C3] da chi ra rang 38% tasks co the pass ma khong can lam gi — cho thay benchmark co noise.
5. **Ket qua khong nhu mong doi:** Neu SRR correlation < 0.85, MT4 coi nhu that bai. Can co plan B (e.g., dieu chinh cong thuc SRR).

### 2.6. Ve dong gop khoa hoc

**Dong gop co du cho luan van thac si khong?**

**Co** — neu thuc hien duoc dung 3/5 muc tieu (taxonomy, benchmark, ablation study), dong gop da du cho luan van thac si. Tuy nhien, can phan biet ro: dong gop la *framework va benchmark*, khong phai *phat hien khoa hoc moi*. Day la nghien cuu dang "systems paper" hon la "discovery paper."

**Co publish duoc o dau khong?**

- **Workshop papers:** ICSE-NIER, ESEC/FSE Demo Track, NeurIPS Workshop on LLM Agents — kha thi neu co ket qua ablation tot.
- **Full conference:** ICSE, ASE, ISSTA — kho hon, can ket qua ablation study thuyet phuc va insight moi (khong chi la "chung toi xay dung framework va do metric").
- **Journal:** Empirical Software Engineering — phu hop ve format nhung can ket qua rong hon.

Luu y: De publish, de cuong can co **insight hoac phat hien bat ngo**, khong chi la "chung toi xay dung benchmark va ket qua la X." Vi du: "Safety layer giam resolve rate 30% nhung khong giam attack success rate" — loai phat hien nhu vay moi thu hut reviewers.

**So voi cac cong trinh lien quan thi moi o dau?**

| Cong trinh | Danh gia gi | De cuong nay moi o dau |
|---|---|---|
| SWE-bench (C1) | Agent output (resolve rate) | Danh gia harness components, khong chi output |
| AIShellJack (D3) | Security cua coding editor | Ket hop security + correctness trong 1 benchmark |
| OpenDev (A1) | 1 harness cu the | So sanh nhieu harness tren cung benchmark |
| SWE-Compass (C5) | Tong hop nhieu benchmark | Them chieu bao mat va harness-level metrics |

Diem moi thuc su nam o **goc nhin tich hop** (khong phai tung phan rieng le). Can lam noi bat dieu nay hon trong de cuong.

---

## 3. Cau hoi phan bien (10 cau hoi kho nhat ma hoi dong se hoi)

### Cau 1: "Lam sao phan biet contribution cua harness va contribution cua LLM?"

**Tai sao hoi dong hoi:** Day la cau hoi cot loi cua de tai. Neu khong tra loi duoc, toan bo framework mat y nghia. Mot harness "tot" voi Claude co the "te" voi GPT — vay harness tot hay LLM tot?

**Goi y tra loi:** Do "backend portability" (chieu 5) chinh la de tra loi cau nay. Harness tot la harness co **variance thap** giua cac backend. Dong thoi, ablation study giu LLM co dinh va doi harness → contribution cua harness; giu harness co dinh va doi LLM → contribution cua LLM. Interaction effect duoc do bang 2-way ANOVA.

### Cau 2: "Voi 3-5 chuyen gia va 30 samples, lam sao chung minh correlation > 0.85 co y nghia thong ke?"

**Tai sao hoi dong hoi:** Validation cua SRR metric la MT4 — mot muc tieu chinh. Nhung sample size qua nho de co statistical power. Pearson correlation voi n=30 can r > 0.36 de significant (p<0.05), nhung 0.85 la claim rat cao.

**Goi y tra loi:** Thua nhan han che ve sample size. Bo sung bang: (1) bootstrap confidence intervals, (2) leave-one-out cross-validation, (3) so sanh SRR voi baseline metrics (RR alone, ASR alone) de cho thay SRR co discriminative power tot hon. Giam muc tieu xuong 0.70 thay vi 0.85.

### Cau 3: "Secure Resolve Rate = RR x (1 - ASR) — tai sao multiplicative? Tai sao khong additive hoac weighted?"

**Tai sao hoi dong hoi:** Cong thuc metric la tam diem cua nghien cuu. Viec chon phep nhan thay vi phep cong (hoac weighted sum) can co ly luan ly thuyet. Hien de cuong khong justify.

**Goi y tra loi:** Multiplicative co y nghia la: neu ASR = 100% (bi hack hoan toan), thi SRR = 0 bat ke RR bao nhieu — dieu nay hop ly vi agent bi compromise khong co gia tri. Additive (RR - ASR) co the am. Tuy nhien, nen thua nhan rang trong so bang nhau giua RR va ASR la gia dinh can duoc test empirically, va de xuat weighted variant: SRR_w = RR x (1 - ASR)^w voi w la weight cho security.

### Cau 4: "Ban noi 'tu xay dung modular harness' — vay ban danh gia chinh san pham cua minh. Co conflict of interest khong?"

**Tai sao hoi dong hoi:** Internal validity concern. Nguoi thiet ke taxonomy + benchmark + 1 trong 3 harness la cung 1 nguoi. Unconscious bias co the anh huong ket qua.

**Goi y tra loi:** (1) Modular harness khong phai la "san pham" — no la cong cu nghien cuu de ablation, giong nhu viec tao "baseline model" trong ML. (2) De giam bias: public release tat ca code va data de nguoi khac reproduce; metric duoc tinh tu dong (khong co subjective judgment); expert validation la de cross-check.

### Cau 5: "400 adversarial instances — lam sao dam bao chat luong? Ai review? Co inter-annotator agreement khong?"

**Tai sao hoi dong hoi:** Chat luong cua benchmark quyet dinh gia tri cua toan bo nghien cuu. Neu adversarial variants qua de (agent luon phat hien) hoac qua kho (khong ai vuot qua), benchmark mat gia tri.

**Goi y tra loi:** (1) Base tasks lay tu SWE-bench Verified — da duoc community validate. (2) Adversarial variants se duoc tao theo template tu D3 (AIShellJack — 314 payloads da duoc test). (3) Pilot study tren 20 instances truoc khi tao 400. (4) Thua nhan rang 1 nguoi tao 400 instances co risk ve chat luong — co the giam xuong 100-200 instances nhung dam bao chat luong bang manual review.

### Cau 6: "Chi test tren Python va SWE-bench. Ket qua co generalize duoc khong?"

**Tai sao hoi dong hoi:** External validity. SWE-bench chi co Python repositories. Coding agents thuc te lam viec voi nhieu ngon ngu. Taxonomy 5 chieu co dung cho Java/Rust coding agents khong?

**Goi y tra loi:** (1) Taxonomy la language-agnostic (tool dispatch, context management, safety layer khong phu thuoc ngon ngu). (2) Benchmark hien tai la Python-specific, day la han che can acknowledge. (3) Future work co the mo rong sang SWE-bench-java (neu co) hoac CrossCodeEval. (4) Python la ngon ngu pho bien nhat trong coding agent benchmarks — bat dau tu day la hop ly.

### Cau 7: "162 conditions ma chi chay 50 — tieu chi chon 50 la gi? Co cherry-picking khong?"

**Tai sao hoi dong hoi:** Day la van de methodology nghiem trong. Viec chon 50/162 conditions ma khong co tieu chi ro rang co the bi coi la cherry-picking de co ket qua dep.

**Goi y tra loi:** Su dung fractional factorial design (Taguchi L50 hoac tuong tu) — phuong phap chuan trong Design of Experiments. Tieu chi: (1) Moi bien doc lap xuat hien o moi muc it nhat 1 lan, (2) Cover tat ca 2-way interactions. Pre-register experimental plan truoc khi chay.

### Cau 8: "So voi viec don gian chay SWE-bench tren nhieu agent roi so sanh, de cuong nay them gia tri gi?"

**Tai sao hoi dong hoi:** Day la cau hoi "so what?". Hien tai, nhieu to chuc da benchmark coding agents bang SWE-bench. De cuong can chi ra gia tri tang them cu the.

**Goi y tra loi:** (1) SWE-bench leaderboard chi noi "Agent A dat 45%, Agent B dat 38%" nhung khong noi **tai sao** — do tool system, context management, hay LLM? Taxonomy cho phep **diagnose**. (2) Security evaluation hien khong co — mot agent dat 70% resolve rate nhung bi prompt injection 80% thi khong duoc deploy. SRR giai quyet van de nay. (3) Backend portability giup to chuc biet agent nao it phu thuoc vao 1 LLM cu the — quan trong khi LLM pricing thay doi.

### Cau 9: "Metric 'Correct Tool Selection Rate' — ground truth tool sequence lay tu dau?"

**Tai sao hoi dong hoi:** Construct validity concern. Mot coding task co the duoc giai bang nhieu tool sequence khac nhau. Ai quyet dinh sequence nao la "correct"?

**Goi y tra loi:** (1) Khong dinh nghia "correct" la duy nhat 1 sequence. (2) Su dung "gold" tool traces tu successful runs (chay nhieu lan, lay common patterns). (3) Metric do "unnecessary tool calls" (e.g., goi Bash de doc file khi co Read tool) — day de dinh nghia hon. (4) Co the chuyen sang "Tool Efficiency Score" thay vi "Correct Selection Rate" de tranh van de nay.

### Cau 10: "De cuong reference su kien 'ro ri ma nguon Claude Code thang 3/2026' — day co phai la nguon hoc thuat khong? Va viec su dung ma nguon bi ro ri co van de dao duc khong?"

**Tai sao hoi dong hoi:** Research ethics. Su dung ma nguon bi ro ri (leaked source code) co the vi pham intellectual property va ethical guidelines cua truong.

**Goi y tra loi:** (1) De cuong chi reference su kien nhu motivating example, khong su dung ma nguon bi ro ri lam du lieu nghien cuu. (2) Tat ca du lieu va tool su dung deu la open-source (SWE-bench, SWE-Agent, OpenHands). (3) Nen bo reference nay khoi de cuong de tranh controversy va thay bang cac nguon hoc thuat (D1, D3, D4) da du manh.

---

## 4. Goi y cai thien

### Goi y 1 (uu tien CAO): Thu hep pham vi — giam tu 5 xuong 3 muc tieu

**Hien tai:** 5 muc tieu chinh, moi muc tieu la 1 cong trinh lon.

**Goi y:** Giu 3 muc tieu:
- MT1: Taxonomy (nhung giam tu 5 chieu xuong 3 chieu chinh: Tool Dispatch, Safety Enforcement, Backend Portability)
- MT2: SecureCodeBench (giam tu 400 xuong 100-150 adversarial instances, 2 loai tan cong thay vi 4)
- MT3: Ablation study (giam xuong 8-12 conditions chinh thay vi 50)

MT4 (validate SRR) nen la 1 phan cua MT3. MT5 (toolkit) nen la output phu, khong phai muc tieu.

### Goi y 2 (uu tien CAO): Tinh lai chi phi thuc te va dieu chinh ngan sach

**Hien tai:** $500-1,000 cho LLM API.

**Goi y:** Tinh chi tiet: so luong runs x trung binh tokens/run x gia/token. Voi pham vi thu hep (12 conditions x 100 tasks x 3 replications = 3,600 runs), chi phi co the giam xuong $2,000-3,000 — van gap 2-3 lan ngan sach hien tai. Can: (1) xin tai tro tu advisor/lab, (2) su dung LLM gia re hon cho pilot runs, (3) dung open-source models (DeepSeek, Qwen) thay vi chi thuong mai.

### Goi y 3 (uu tien CAO): Bo "modular harness tu xay dung", thay bang harness co san thu 3

**Hien tai:** So sanh SWE-Agent, OpenHands, va 1 harness tu xay dung.

**Goi y:** Thay bang Aider, Continue, hoac mot harness open-source khac. Ly do: (1) Giam thoi gian 2-3 thang (khong can xay dung), (2) Tang internal validity (khong danh gia san pham cua minh), (3) Ket qua co gia tri thuc tien hon (so sanh cac tool thuc te).

### Goi y 4 (uu tien TRUNG BINH): Tang chat luong expert validation

**Hien tai:** 3-5 experts, 30 samples.

**Goi y:** (1) Tang len 7-10 experts (co the dung online survey de giam effort), (2) Tinh inter-rater reliability (Krippendorff's alpha), (3) Su dung ranking thay vi scoring (de hon cho experts), (4) Bootstrap confidence interval cho correlation.

### Goi y 5 (uu tien TRUNG BINH): Lam ro phuong phap xay dung taxonomy

**Hien tai:** "Rut ra tu phan tich 49 papers, mapping limitations sang measurable properties."

**Goi y:** Su dung Thematic Analysis hoac Concept Matrix method cu the. Mo ta: (1) Ai coding? (2) Bao nhieu vong review? (3) Tieu chi gi de mot dimension duoc giu lai? (4) Co inter-coder reliability khong? Neu chi 1 nguoi lam, phai thua nhan la researcher-driven taxonomy va giam claim ve "objectivity."

### Goi y 6 (uu tien TRUNG BINH): Them plan B cho MT4

**Hien tai:** Muc tieu correlation > 0.85. Neu khong dat, MT4 that bai.

**Goi y:** (1) Giam muc tieu xuong > 0.70. (2) Neu SRR khong dat, de xuat variant (weighted SRR, threshold-based SRR). (3) Bao cao ca truong hop SRR that bai — do cung la ket qua khoa hoc.

### Goi y 7 (uu tien THAP): Them reproducibility protocol

**Goi y:** (1) Pre-register experimental design (conditions, hypotheses, analysis plan) tren OSF hoac GitHub truoc khi chay experiments. (2) Report tat ca results, ke ca negative. (3) Cong khai random seeds, API versions, Docker images. Dieu nay tang uy tin khoa hoc dang ke.

---

## 5. Ket luan phan bien

### Quyet dinh: **CHINH SUA VA BM VE LAI** (Major Revisions Required)

De cuong co y tuong nghien cuu tot, research gap thuyet phuc (dac biet Gap 2), va thiet ke thuc nghiem co ban dau tot. Tuy nhien, pham vi qua rong cho 1 nguoi trong 6 thang, chi phi chua thuc te, va mot so van de methodology can giai quyet truoc khi bat dau thuc hien.

### 3 dieu can lam ngay:

1. **Thu hep pham vi:** Giam tu 5 muc tieu xuong 3, giam conditions tu 50 xuong 10-15, giam adversarial instances tu 400 xuong 100-150. Viet lai ke hoach voi thoi gian thuc te. Day la dieu quan trong nhat — mot de cuong kha thi tot hon mot de cuong hoan hao nhung khong thuc hien duoc.

2. **Tinh lai chi phi API va xac dinh nguon tai chinh:** Tinh cu the: so runs x tokens/run x gia/token. Neu ngan sach khong du, can xin tai tro hoac dung open-source LLMs (DeepSeek-V3, Qwen2.5-Coder) thay the 1 trong 2 LLM backends thuong mai.

3. **Bo modular harness tu xay dung:** Thay bang 1 harness open-source co san (Aider, Continue, hoac Devika). Dieu nay giam 2-3 thang cong viec va tang internal validity cua nghien cuu.

---

*Phan bien duoc thuc hien nghiem tuc voi muc dich giup hoc vien hoan thien de cuong. Cac nhan xet tren day mang tinh xay dung va dua tren kinh nghiem danh gia nhieu de cuong tuong tu. Chuc hoc vien chinh sua thanh cong va hoan thanh tot luan van.*
