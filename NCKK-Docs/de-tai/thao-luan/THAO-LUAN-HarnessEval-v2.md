# THAO LUAN VA PHAN BIEN (VONG 2): De cuong HarnessEval v2

> Nguoi phan bien: Thanh vien hoi dong bao ve de cuong
> Ngay: 06/04/2026
> De tai: HarnessEval — Danh gia ha tang Coding Agent thong qua phan tich ablation da chieu tren nhieu mo hinh ngon ngu lon
> Phien ban: v2 (sau chinh sua theo phan bien vong 1)
> Diem v1: 7.3/10 — "Can chinh sua dang ke"

---

## 1. Danh gia viec chinh sua

### Goi y 1 (v1): Thu hep scope — chon 3 chieu thay vi 5

- **Trang thai:** DA XU LY
- **Muc do:** 5/5
- **Nhan xet:** Tac gia da giam tu 5 chieu (11 metrics) xuong 3 chieu (7 metrics), giam tu 80 conditions xuong 27 conditions, giam tu 16,000 evaluations xuong 7,050. Day la su thay doi quan trong nhat va duoc thuc hien **rat tot**. Viec chon D1 (Tool Dispatch), D2 (Context Utilization), D3 (Backend Portability) la 3 chieu cot loi hoan toan phu hop voi goi y. Safety va Session Continuity duoc chuyen thanh future work mot cach hop ly. Khong con lo ngai ve scope.

### Goi y 2 (v1): Fork SWE-Agent lam modular harness, khong viet tu dau

- **Trang thai:** DA XU LY
- **Muc do:** 4/5
- **Nhan xet:** Tac gia da doi tu "tu xay harness" sang "fork SWE-Agent" va them tieu chi +/- 3% so voi baseline. Day la quyet dinh dung. Thoi gian du kien giam tu 1-3 thang xuong 2-3 tuan. Tuy nhien, con thieu chi tiet ve **cu the se refactor nhung gi** trong SWE-Agent. 15,000 LOC la nhieu — can xac dinh chinh xac 3 modules nao se duoc tach ra va interface giua chung. Tru 1 diem vi thieu ke hoach refactoring cu the.

### Goi y 3 (v1): Them power analysis va muc risk analysis

- **Trang thai:** DA XU LY
- **Muc do:** 4/5
- **Nhan xet:** Tac gia da them: (1) Threats to Validity voi 3 loai (internal, external, construct), (2) Risk Analysis voi 6 risks va mitigation, (3) Bonferroni correction, (4) Power analysis duoc de cap o muc 3.5. Tuy nhien, power analysis chua duoc **tinh chinh thuc** — chi noi "voi 150 tasks, 27 conditions, alpha = 0.05, power >= 0.80" ma khong cho thay phep tinh cu the. Can tinh: voi ANOVA 2 chieu, 9 x 3 design, 150 observations, minimum detectable effect size la bao nhieu?

### Goi y 4 (v1): Bo phan "Du kien ket qua" hoac viet lai trung tinh

- **Trang thai:** DA XU LY
- **Muc do:** 5/5
- **Nhan xet:** Tac gia da bo hoan toan con so "30-40%" va thay bang 4 hypotheses (H1-H4) trung tinh. Cach viet moi rat tot: "Du thanh cong hay bac bo hypotheses deu la dong gop." Day chinh la tinh than nghien cuu khoa hoc dung dan. Khong con lo ngai ve confirmation bias.

### Goi y 5 (v1): Them pilot study

- **Trang thai:** DA XU LY
- **Muc do:** 4/5
- **Nhan xet:** Pilot study duoc thiet ke voi 5 conditions x 20 tasks x 2 runs = 200 evaluations, chi phi ~$50-80, thoi gian 1-2 tuan. 4 muc dich pilot duoc trinh bay ro rang. Tuy nhien, co mot so lo ngai ve chi tiet (xem muc 3.2 ben duoi).

### Goi y 6 (v1): Dinh nghia formal cho "independence" cua harness evaluation

- **Trang thai:** DA XU LY
- **Muc do:** 5/5
- **Nhan xet:** Day la thay doi **an tuong nhat**. Section 2.2.3 moi dinh nghia "doc lap voi LLM" bang ANOVA 2 chieu — phan tach variance thanh Variance(Harness) + Variance(LLM) + Variance(Interaction) + Error. Cong thuc ro rang, y nghia thong ke duoc giai thich tot. Tac gia dung nhan: "khong co nghia khong tuong tac, ma co nghia co the phan tach." Day chinh la dong gop ly thuyet chinh cua de tai va bay gio da duoc formalize dung cach.

### Goi y 7 (v1): Xem xet lai danh sach tai lieu tham khao

- **Trang thai:** XU LY MOT PHAN
- **Muc do:** 2/5
- **Nhan xet:** Danh sach tai lieu tham khao van **khong co thay doi dang ke** so voi v1. Van chua co papers tu SE venues chinh (ICSE, FSE, ASE, ISSTA). Van chua co papers ve ablation study methodology trong SE. So luong references giam tu 49 xuong 17 (do chi liet ke cac papers duoc cite truc tiep), nhung khong co papers moi duoc them vao. Day la diem chua duoc xu ly.

---

## 2. Danh gia tong quan v2

### Diem tong the

| Tieu chi | Diem v1 | Diem v2 | Thay doi | Nhan xet |
|----------|---------|---------|----------|----------|
| Tinh moi | 8.5 | 8.5 | = | Giu nguyen — research gap van convincing |
| Tinh kha thi | 5.5 | **7.5** | +2.0 | Cai thien **lon** — scope, budget, timeline deu thuc te hon nhieu |
| Chat luong phuong phap | 7.0 | **8.0** | +1.0 | ANOVA 2 chieu, hypotheses, threats to validity — tang dang ke |
| Tai lieu tham khao | 8.0 | **7.0** | -1.0 | Giam vi chua bo sung papers SE venues va ablation methodology |
| Trinh bay | 7.5 | **8.5** | +1.0 | Bang so sanh v1 vs v2 rat huu ich, cau truc ro rang hon |
| **Tong** | **7.3** | **8.1/10** | **+0.8** | **Cai thien ro rang, gan dat muc thong qua** |

### Nhung gi da cai thien

1. **Scope thuc te hon nhieu:** 27 conditions thay vi 80, 7,050 evaluations thay vi 16,000. Day la de tai master's thesis thuc su, khong phai PhD dissertation nua.
2. **Phuong phap vung chac hon:** ANOVA 2 chieu la phuong phap dung de tra loi cau hoi nghien cuu. Hypotheses H1-H4 testable va trung tinh.
3. **Risk management tot hon:** Pilot study, risk analysis, threats to validity — de cuong bay gio co "ke hoach B" cho moi tinh huong xau.
4. **Fork SWE-Agent:** Quyet dinh thuc te, giam rui ro lon nhat cua v1 (tu xay harness).
5. **Budget tang 2-3x:** Tu $800-1,200 len $2,500-3,100 — thuc te hon rat nhieu.

### Nhung gi con can cai thien

1. **Tai lieu tham khao** chua duoc bo sung (xem goi y 7).
2. **Power analysis** chua duoc tinh chinh thuc.
3. **Refactoring plan** cho SWE-Agent fork chua cu the.
4. **M2.2 (Effective Token Ratio)** dung LLM classifier — van co van de, chi thay GPT-judge bang Claude Haiku classifier (van la LLM danh gia LLM).

### Van de MOI do v2 tao ra

1. **ANOVA assumptions chua duoc kiem tra:** ANOVA 2 chieu yeu cau normality, homogeneity of variance, independence. Resolve rate la binary variable (0/1 cho moi task) — phan phoi **khong normal**. Can giai thich tai sao ANOVA van applicable (vd: Central Limit Theorem voi n=150), hoac de xuat alternative (generalized linear model, logistic regression).

2. **Factor A (9 levels) la "gia tao":** Tac gia gom Tool Config (3) x Context Config (3) = 9 levels thanh 1 factor. Nhung day thuc ra la **2 factors rieng biet**. Nen dung **ANOVA 3 chieu** (Tool x Context x Backend) thay vi 2 chieu. Neu dung 2 chieu voi Factor A = 9 levels, mat kha nang phan tach dong gop cua Tool vs Context — chinh la dieu can biet.

3. **H3 (eta-squared >= 0.20) co the qua cao:** Eta-squared >= 0.20 la "large effect" theo Cohen (1988). Trong thuc te, nhieu nghien cuu thuc nghiem chi dat eta-squared 0.06-0.14 (medium effect). Neu ket qua la eta-squared = 0.15, de tai se tuyen bo H3 bi bac bo — nhung 15% variance giai thich boi harness van la mot phat hien co y nghia. Threshold 0.20 co the tu lam kho minh.

4. **Conflict of interest voi fork:** Tac gia fork SWE-Agent, modify no, roi dung chinh no lam tool do luong. Day co van de objectivity: neu modular harness "dat" tieu chi +/- 3%, ai kiem chung? Can nguoi doc lap chay lai.

---

## 3. Phan bien chi tiet v2

### 3.1. Ve ANOVA 2 chieu (moi trong v2)

**Co phu hop cho bai toan nay khong?**

Y tuong dung ANOVA de phan tach variance la **dung huong** va la dong gop tot. Tuy nhien, co 3 van de ky thuat:

**Van de 1: Violation of normality assumption.**
Resolve rate cua moi task la binary (solved = 1, not solved = 0). Khi aggregate qua 150 tasks, resolve rate cua moi condition la proportion (vd: 45/150 = 30%). Voi 27 conditions, ban co 27 data points (moi cai la 1 proportion). ANOVA tren 27 data points la **cuc ky yeu** ve statistical power. De dung ANOVA dung, can treat moi task nhu 1 observation — luc do co 150 x 27 = 4,050 observations, nhung dependent variable la binary → can **logistic regression** hoac **generalized linear mixed model (GLMM)** thay vi ANOVA.

**Van de 2: Nen dung ANOVA 3 chieu, khong phai 2 chieu.**
Nhu da noi o muc 2, gom Tool x Context thanh 1 factor lam mat thong tin. ANOVA 3 chieu (Tool x Context x Backend) cho phep:
- Main effect cua Tool (tra loi H1)
- Main effect cua Context (tra loi H2)
- Main effect cua Backend
- Interaction Tool x Backend, Context x Backend (tra loi H4)
- 3-way interaction

Day la thiet ke phan tich **tot hon nhieu** va khong ton them chi phi (cung data).

**Van de 3: Multiple testing.**
Voi 7 metrics, moi metric chay 1 ANOVA, can correction cho 7 tests. Bonferroni duoc de cap nhung chua ro ap dung cho bao nhieu comparisons tong cong.

**Eta-squared >= 0.20 co realistic khong?**

Kho noi truoc khi co data, nhung:
- Trong educational research, eta-squared 0.01-0.06 la common.
- Trong software engineering, effect sizes thuong nho hon ky vong (Kampenes et al., 2007).
- Harness configuration **co the** co large effect vi no quyet dinh tools co san — nhung cung co the bi dominated boi LLM quality.

**Goi y:** Ha threshold xuong eta-squared >= 0.10 (medium effect) hoac, tot hon, **khong dat threshold** — chi report eta-squared va de nguoi doc tu danh gia. Viec dat threshold cung co the dan den "failed hypothesis" khi ket qua thuc ra co y nghia.

### 3.2. Ve Pilot Study (moi trong v2)

**Thiet ke pilot co hop ly khong?**

Nhin chung **hop ly** va la mot bo sung tot. Tuy nhien:

**200 evaluations co du de validate metrics?**

5 conditions x 20 tasks x 2 runs = 200 evaluations. Voi 20 tasks/condition, **khong du power** de detect effect sizes (can ~64 tasks/condition cho d = 0.5). Nhung muc dich cua pilot khong phai de kiem dinh gia thuyet ma de:
1. Debug pipeline — 200 la du
2. Uoc tinh chi phi — 200 la du
3. Validate metrics phan biet duoc — **co the khong du**. 20 tasks co the cho ket qua nhieu noise.

**Goi y:** Tang pilot len 30-40 tasks/condition (tong ~300-400 evaluations). Chi phi chi tang them ~$30-50 nhung cho ket qua tin cay hon nhieu.

**Timeline 1-2 tuan co kha thi khong?**

Phu thuoc vao:
- Da co SWE-Agent fork chua? (Pilot o Tuan 7-8, fork o Tuan 9-11 — **thu tu sai?**)
- Setup Docker cho SWE-bench mat bao lau?

**Van de nghiem trong: Pilot study (GD1.5, Tuan 7-8) xay ra TRUOC khi fork SWE-Agent (GD2, Tuan 9-11).** Vay pilot chay tren harness nao? SWE-Agent goc chua duoc refactor? Neu vay, pilot khong test duoc modular harness — chi test duoc pipeline. Can **dao thu tu**: fork truoc (Tuan 7-9), pilot sau (Tuan 10-11), hoac chay pilot tren SWE-Agent goc va chap nhan rang pilot chi validate pipeline + cost, khong validate modularity.

### 3.3. Ve Fork SWE-Agent (thay doi tu v1)

**Fork co thuc su giai quyet van de conflict of interest?**

Khong hoan toan. Van de v1 la: "tu xay harness de so sanh voi harness khac — co bias." V2 doi sang: "fork SWE-Agent va modify" — giam bias vi baseline la SWE-Agent goc, nhung **tac gia van la nguoi modify**. Neu modify sai, ket qua bi sai.

**Tuy nhien**, fork **tot hon nhieu** so voi tu xay vi:
- Baseline quality duoc dam bao (SWE-Agent da duoc validated)
- Tieu chi +/- 3% la measurable va verifiable
- Nguoi doc co the so sanh code changes (diff giua fork va goc)
- Open-source nen nguoi khac co the reproduce

**Tieu chi "+/- 3% baseline" co hop ly khong?**

- 3% tren SWE-bench la kha nhay cam. Neu SWE-Agent dat 25% resolve rate, 3% la 22-28% — kha rong.
- Nhung neu SWE-Agent dat 50%, thi 47-53% la hop ly.
- **Can xac dinh benchmark cu the:** +/- 3% **absolute** hay **relative**? (3% absolute = 22-28%, 3% relative cua 25% = 24.25-25.75%). De cuong nen lam ro.
- **Can xac dinh tren backend nao?** +/- 3% tren Claude Sonnet 4 hay tren trung binh 3 backends?

### 3.4. Ve Gia thuyet H1-H4 (moi trong v2)

**H1: Tool system co effect size lon nhat (Cohen's d > 0.5)**

- Testable? **Co** — so sanh effect size cua Tool thay doi vs Context thay doi.
- Hop ly? Kha hop ly vi tool system quyet dinh agent co the lam gi (cung capabilities).
- Van de: "lon nhat" la so sanh tuong doi — neu ca 3 component deu co d > 0.5, H1 van dung nhung khong noi gi ve magnitude.

**H2: Context management co effect size trung binh (Cohen's d 0.3-0.5)**

- Testable? **Co**.
- Van de: Range 0.3-0.5 kha hep. Neu d = 0.29 hay d = 0.51, gia thuyet bi bac bo nhung ket qua van co y nghia. **Gia thuyet nen la directional** ("Context management co effect size nho hon Tool system") thay vi dat range cu the.

**H3: Eta-squared >= 0.20**

- Testable? **Co**.
- Van de: Nhu da phan tich, threshold 0.20 co the qua cao. Xem muc 3.1.

**H4: Interaction effect co y nghia thong ke**

- Testable? **Co**.
- Day la gia thuyet **thu vi nhat** vi no noi rang harness tot "san phang" su khac biet giua cac LLMs. Neu dung, day la insight co gia tri thuc tien cao.
- Van de: "Co y nghia thong ke" khong co nghia "co y nghia thuc te." Interaction effect co the significant nhung effect size rat nho.

**Co bi trung lap voi nhau khong?**

H1 va H2 co moi quan he logic: neu H1 dung (Tool > 0.5) va H2 dung (Context = 0.3-0.5), chung implicit noi Tool > Context. Nen viet 1 gia thuyet thay vi 2: "H1: Tool system co effect size lon hon Context management." Giam tu 4 xuong 3 hypotheses, moi cai doc lap.

**Effect size thresholds co hop ly?**

Cohen's d > 0.5 la "medium-to-large." Trong software engineering experiments, day la threshold hop ly nhung khong phai luc nao cung dat duoc. Goi y: report effect sizes va confidence intervals thay vi chi test against thresholds. Mot effect size d = 0.4 voi narrow CI van co gia tri hon d = 0.6 voi wide CI.

### 3.5. Ve Threats to Validity (moi trong v2)

**Co du 3 loai?**

Co — Internal, External, Construct deu co. Day la cai thien tot so voi v1 (khong co gi).

**Co thieu threat nao quan trong?**

1. **Statistical conclusion validity** (loai thu 4 theo Wohlin et al.): Van de multiple testing voi 7 metrics x nhieu comparisons chua duoc trinh bay nhu validity threat. Bonferroni duoc de cap nhung chua ro ap dung o dau.

2. **Construct validity — thieu:** LLM versioning. Claude Sonnet 4, GPT-4o co the **bi update** trong 6 thang nghien cuu. Neu OpenAI update GPT-4o giua chung, ket qua truoc va sau update khong so sanh duoc. Can: (a) ghi nhan model version/snapshot, (b) chay tat ca experiments trong thoi gian ngan, hoac (c) dung versioned API (neu co).

3. **External validity — thieu:** Survivor bias trong SWE-bench task selection. 150/500 tasks duoc chon — cac tasks bi loai (Docker unstable) co the la tasks kho, noi harness quan trong hon. Viec loai chung co the **lam giam** measured effect cua harness.

4. **Internal validity — thieu:** Experimenter bias. Tac gia la nguoi fork SWE-Agent, chay experiments, va phan tich ket qua — cung 1 nguoi. Nen co nguoi doc lap chay lai it nhat 1 subset cua experiments.

### 3.6. Ve Budget moi ($2,500-3,100)

**Co thuc te hon v1 khong?**

Rat nhieu. V1 la $800-1,200 cho 16,000 evaluations (khoang $0.05-0.075/eval — **bat kha thi**). V2 la $2,500-3,100 cho 7,050 evaluations (khoang $0.35-0.44/eval — **hop ly hon**).

**Con underestimate o dau?**

1. **Retry rate 30% co the thap:** SWE-bench Docker setup notoriously unstable. Retry rate 40-50% thuc te hon, dac biet cho DeepSeek (API it on dinh hon Claude/GPT). Tang len: 7,050 x 1.5 = 10,575 evals → ~$2,855 API cost.

2. **Khong tinh chi phi human annotation:** M1.1 can 2 annotators cho 500 tool calls. Neu tra $0.10-0.20/annotation = $100-200. M2.2 can human labels cho 200 segments. M2.1 can human preference cho 30 cap. Tong: **~$200-400 annotation cost** chua duoc tinh.

3. **Khong tinh chi phi compute:** Docker instances cho SWE-bench can may manh. Neu chay tren cloud (EC2/GCP), 7,050 evaluations x 20 phut/eval = 2,350 gio compute. c5.xlarge ($0.17/hr) = **~$400**. Chua tinh disk storage cho Docker images.

4. **Nen tang thuc te hon:** Budget nen la **$3,500-4,500** (them annotation + compute + higher retry rate). Day van la reasonable cho master's thesis nhung can duoc ghi nhan.

---

## 4. Cau hoi phan bien vong 2 (5 cau hoi moi)

### Cau hoi 1: Ve thu tu pilot va fork

**Hoi:** "Theo ke hoach, pilot study (GD1.5, Tuan 7-8) xay ra TRUOC khi fork SWE-Agent (GD2, Tuan 9-11). Vay pilot chay tren harness nao? Neu chay tren SWE-Agent goc, pilot khong validate duoc tinh modular — chi validate pipeline. Ban co thay day la van de khong, va se xu ly nhu the nao?"

**Goi y tra loi:** Co 2 phuong an: (1) Dao thu tu — fork truoc (Tuan 7-9), pilot sau (Tuan 10-11). Uu diem: pilot test duoc modular harness. Nhuoc diem: mat thoi gian fork truoc khi biet pipeline co chay khong. (2) Chia pilot thanh 2 pha — Pilot A (Tuan 7-8) tren SWE-Agent goc de validate pipeline + cost + debug Docker, Pilot B (Tuan 12) tren modular harness de validate metrics + modularity. Phuong an 2 tot hon vi giam rui ro o ca 2 giai doan.

### Cau hoi 2: Ve ANOVA va binary outcome

**Hoi:** "Resolve rate cua moi task la binary (solved/not solved). ANOVA gia dinh dependent variable lien tuc va normally distributed. Ban se xu ly vi pham nay nhu the nao? Co nen dung logistic regression hoac GLMM thay vi ANOVA khong?"

**Goi y tra loi:** Dung, day la van de ky thuat quan trong. Co 3 cach: (1) Aggregate resolve rate qua nhieu tasks → proportion → gan normal voi n=150 (Central Limit Theorem). Dung ANOVA tren proportions. Nhuoc diem: mat thong tin task-level. (2) Dung **GLMM** voi binary outcome, random effect cho task, fixed effects cho Tool/Context/Backend. Day la phan tich **dung** nhat ve mat thong ke. (3) Dung ca hai: ANOVA cho de trinh bay + GLMM cho robustness check. Nen chon phuong an 3 — report ANOVA (de doc) va GLMM (de chinh xac), kiem tra xem ket luan co nhat quan khong.

### Cau hoi 3: Ve M2.2 va LLM classifier

**Hoi:** "V1 bi gop y vi dung GPT-judge (LLM danh gia LLM — circular reasoning). V2 thay GPT-judge bang Claude Haiku classifier cho M2.2. Nhung day van la dung LLM de danh gia context cua LLM agent — van de circular reasoning co thuc su duoc giai quyet chua?"

**Goi y tra loi:** Phan biet: (1) V1 dung GPT-judge de do *chat luong output cua GPT agent* → **circular** (cung model family, cung bias). (2) V2 dung Claude Haiku de phan loai *token relevance* — day la task don gian hon (classification, khong phai evaluation), va Haiku khong phai model duoc danh gia. Van de giam di nhung chua het. Mitigation tot nhat: validate classifier tren 200 segments voi human labels (da co trong ke hoach) va **report classifier accuracy**. Neu accuracy > 90% thi tin cay. Neu < 80% thi can doi sang heuristic-based approach.

### Cau hoi 4: Ve viec SWE-Agent fork bi outdated

**Hoi:** "SWE-Agent dang duoc phat trien tich cuc (commits hang ngay). Khi ban fork vao Tuan 9 va chay experiments den Tuan 18, fork cua ban se bi outdated 2-3 thang so voi mainline. Ket qua cua ban co con valid khi SWE-Agent da thay doi dang ke?"

**Goi y tra loi:** Day la threat to validity can acknowledge. Tuy nhien: (1) Nghien cuu do **relative** contribution cua components, khong phai absolute performance. Neu SWE-Agent update tang performance 5%, dong gop tuong doi cua tool vs context van co the giong nhau. (2) Ghi nhan chinh xac commit hash cua fork de reproducibility. (3) Trong discussion, acknowledge rang ket qua chi valid cho SWE-Agent version X, can re-validate cho versions moi. (4) Day la van de chung cua moi nghien cuu tren open-source systems — khong phai unique cho de tai nay.

### Cau hoi 5: Ve viec H4 co thuc su testable

**Hoi:** "H4 noi 'variance giua cac LLM backends giam khi harness chat luong cao hon.' Nhung ban chi co 3 backends va 9 harness configs. Voi 3 data points (3 backends), standard deviation rat khong on dinh. Lam sao ban tinh 'variance giam' mot cach co y nghia thong ke?"

**Goi y tra loi:** Dung, voi chi 3 backends, variance across backends kho estimate. Cach tot hon de test H4: thay vi tinh std(3 backends) cho moi harness config, dung **interaction term** trong ANOVA. Neu interaction Harness x Backend co y nghia → co harness-backend dependency. Sau do, visualize bang interaction plot: neu cac duong (moi duong = 1 backend) **hoi tu** o harness configs tot → H4 duoc support. Khong can tinh variance truc tiep tren 3 diem.

---

## 5. Diem cuoi cung va quyet dinh

### Diem moi

| Tieu chi | Diem v1 | Diem v2 |
|----------|---------|---------|
| Tinh moi | 8.5 | 8.5 |
| Tinh kha thi | 5.5 | 7.5 |
| Chat luong phuong phap | 7.0 | 8.0 |
| Tai lieu tham khao | 8.0 | 7.0 |
| Trinh bay | 7.5 | 8.5 |
| **Tong** | **7.3/10** | **8.1/10** |

### Quyet dinh: THONG QUA CO DIEU KIEN

De cuong v2 da **cai thien dang ke** so voi v1. Scope thuc te, phuong phap vung chac hon, risk management tot. De tai co the bat dau trien khai **voi dieu kien** sau:

### Dieu kien thong qua (can xu ly truoc khi bat dau nghien cuu)

1. **Sua thu tu timeline:** Dao GD1.5 (pilot) va GD2 (fork) — hoac chia pilot thanh 2 pha (Pilot A tren SWE-Agent goc, Pilot B tren modular harness). Gui lai timeline da sua cho hoi dong.

2. **Lam ro thiet ke ANOVA:** Doi tu ANOVA 2 chieu (9 levels x 3 levels) sang **ANOVA 3 chieu** (3 Tool x 3 Context x 3 Backend), hoac giai thich tai sao 2 chieu la du. Them GLMM nhu robustness check cho binary outcome. Gui lai muc 3.5 da sua.

3. **Ha threshold H3 hoac bo threshold:** Doi eta-squared >= 0.20 thanh >= 0.10, hoac tot hon, bo threshold va chi report observed eta-squared. Giai thich su thay doi.

### 3 dieu can lam truoc khi bat dau nghien cuu

**1. Setup ky thuat (Tuan 1-2, song song voi GD1):**
Cai dat SWE-bench Docker environment tren may nghien cuu. Chay 5-10 tasks voi SWE-Agent goc de xac nhan pipeline hoat dong. Ghi nhan thoi gian trung binh/task, ty le Docker failures, va chi phi thuc te/evaluation. So sanh voi uoc tinh trong de cuong.

**2. Bo sung tai lieu tham khao (Tuan 1-3):**
Tim va them 5-8 papers tu SE venues (ICSE, FSE, ASE). Tim 2-3 papers ve ablation study methodology trong SE (vd: Arcuri & Briand, ICSE 2011 ve statistical tests trong SE). Xac minh cac papers 2026 — ghi ro "preprint" neu chua peer review.

**3. Lien he expert som (Tuan 1-2):**
Gui email moi expert validate taxonomy ngay tu dau. 5 experts can co: it nhat 2 tu industry (lam viec voi coding agents), it nhat 2 tu academia (chuyen ve SE evaluation). Xac nhan ho co thoi gian trong 6 tuan dau. Day la bottleneck lon nhat — bat dau som.

---

> *Nhan xet tong ket: De cuong v2 cho thay tac gia da tiep thu phan bien vong 1 mot cach nghiem tuc va co he thong. 5/7 goi y duoc xu ly tot (diem 4-5/5), 1 xu ly mot phan, 1 con yeu. De tai da chuyen tu "scope PhD" sang "scope master's thuc te." Dong gop ly thuyet (ANOVA phan tach harness vs LLM) duoc formalize tot. Cac van de con lai (thu tu timeline, ANOVA assumptions, threshold H3) la van de ky thuat co the sua nhanh — khong can viet lai de cuong. Voi 3 dieu kien tren duoc dap ung, de tai san sang de bat dau trien khai.*

---
*Het phan bien vong 2.*
