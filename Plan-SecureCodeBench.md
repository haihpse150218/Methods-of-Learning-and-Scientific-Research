# PLAN: SecureCodeBench — Benchmark bao mat cho Coding Agent
# (Gap 2 — Dual-Axis Correctness + Security Evaluation)

> **Boi canh:** Chuong trinh Thac si Ky thuat phan mem AI — FPT
> **Mon hoc:** Methods of Learning and Scientific Research
> **De tai:** SecureCodeBench — Benchmark hai truc danh gia dong thoi do chinh xac va do khang bao mat cua Coding Agent
> **Trang thai:** De cuong v1 da viet, da phan bien (6.7/10). CHUA viet v2.

---

## 1. Tong quan du an

### 1.1. Hanh trinh chon de tai

```
Buoc 1-4: Giong HarnessEval (chon huong → research 49 papers → GAP-ANALYSIS)

Buoc 5: Chon Gap 2 (SecureCodeBench) — diem 13/15
  → Ly do: Thuc te (vu Claude Code leak), ket hop 2 linh vuc (security + evaluation)
  → Rui ro: Can Ethics section, SRR metric co the qua don gian

Buoc 6: Viet de cuong v1 → Phan bien hoi dong (6.7/10)
  → CHUA viet v2
```

### 1.2. De tai

**Ten tieng Viet:** SecureCodeBench: Benchmark hai truc danh gia dong thoi do chinh xac va do khang bao mat cua Coding Agent

**Ten tieng Anh:** SecureCodeBench: A Dual-Axis Benchmark for Evaluating Coding Agents on Both Correctness and Security Resistance

### 1.3. Research Gap

**Gap chinh:** Hai cong dong nghien cuu **chay song song ma khong giao nhau**:
- Evaluation (C1-C5): do correctness (resolve rate) → **bo qua security**
- Security (D1-D5): do attack success rate → **bo qua correctness**
- Ket qua: Agent dat 70% resolve rate nhung de bi tan cong 84% [D3]

**Bang chung:**
- D3 (AIShellJack): 314 payloads, ASR 41-84% tren Cursor/Copilot — nhung khong do coding performance
- C1 (SWE-Bench Pro): 1,865 tasks — nhung khong co adversarial variants
- D4 (Maloyan 2026): 42 attack techniques — tat ca 12 defenses bi bypass 78%+
- D2 (SecurePatterns): 6 design patterns phong thu — nhung chua benchmark tren coding tasks

### 1.4. 4 Diem khac biet cua SecureCodeBench

| # | Khac biet | Mo ta |
|---|-----------|-------|
| 1 | **Benchmark DUAL-AXIS dau tien** | Do dong thoi correctness (RR) + security (ASR) tren cung tasks |
| 2 | **4 vector tan cong dac thu coding** | Poisoned coding rules, malicious MCP, adversarial code comments, dependency confusion |
| 3 | **Metric tong hop SRR** | Secure Resolve Rate = RR x (1-ASR) — phat agent giai tot nhung de hack |
| 4 | **Trade-off analysis** | Them safety layer → giam ASR nhung cung giam RR bao nhieu? |

### 1.5. Boi canh thuc te — Vu Claude Code Leak (03/2026)

- Anthropic vo tinh publish sourcemap trong npm → 1,884 file TypeScript bi phoi bay
- 26 hidden slash commands, 32 secret CLI flags, bypass safety mechanisms
- Cong dong fork/clone hang tram repos (claw-code, v.v.)
- Ke tan cong hieu ro safety layer → co the bypass
- **SecureCodeBench** cho phep danh gia muc do anh huong

---

## 2. Tien do da hoan thanh

| Hang muc | Trang thai | File |
|----------|------------|------|
| Research 49 papers | XONG | INDEX.md, summary/*.md |
| GAP-ANALYSIS | XONG | GAP-ANALYSIS.md |
| De cuong v1 | XONG | DE-CUONG-SecureCodeBench.md |
| Phan bien hoi dong | XONG | THAO-LUAN-SecureCodeBench.md (6.7/10) |
| **De cuong v2** | **CHUA** | Can ap dung 7 goi y tu phan bien |
| Visualization | CHUA | Can tao visualize-SecureCodeBench.html |

---

## 3. Ket qua phan bien va cach xu ly

### 3.1. Diem hoi dong: 6.7/10 — Can chinh sua lon

| Tieu chi | Diem | Nhan xet |
|----------|------|----------|
| Tinh moi | 8.0 | Dual-axis moi, SRR metric hay |
| Tinh kha thi | 5.0 | Budget thap, commercial agents kho test |
| Phuong phap | 6.5 | SRR qua don gian, thieu ethics |
| Tai lieu TK | 8.0 | 49 papers |
| Trinh bay | 7.0 | Tot nhung thieu ethics section |
| **Tong** | **6.7** | **Can chinh sua lon** |

### 3.2. Van de nghiem trong nhat (can xu ly trong v2)

| # | Van de | Muc do | Cach xu ly du kien |
|---|--------|--------|-------------------|
| 1 | **THIEU Ethics & Responsible Disclosure** | NGHIEM TRONG | Them section rieng: IRB, responsible disclosure, sandboxing |
| 2 | **Budget khong thuc te** ($500-800 vs $2,000-2,500) | CAO | Tinh lai chi tiet, giam scope neu can |
| 3 | **6 muc tieu qua nhieu** | CAO | Giam xuong 4 muc tieu |
| 4 | **SRR = RR x (1-ASR) qua don gian** | TRUNG BINH | De xuat weighted version, so sanh ca 2 |
| 5 | **Commercial agents (Cursor) kho test tu dong** | TRUNG BINH | Focus open-source, Cursor chi lam manual sample |
| 6 | **Adversarial variants co "realistic" khong?** | TRUNG BINH | Lay mau tu real-world GitHub repos co .cursorrules |

### 3.3. 10 cau hoi kho va cach tra loi (tom tat)

| # | Cau hoi | Cach tra loi |
|---|---------|-------------|
| 1 | "Tao 400 adversarial payloads co ethical khong?" | Responsible disclosure, chi test local, sandbox, khong public payloads doc hai |
| 2 | "SRR = RR x (1-ASR) tai sao nhan? Tai sao khong cong?" | Nhan vi security breach 1 lan = compromise ca session. So sanh voi weighted version |
| 3 | "So voi AIShellJack [D3] thi khac gi?" | AIShellJack chi do security. SecureCodeBench do DONG THOI correctness + security |
| 4 | "Cursor la IDE, khong co API. Lam sao test tu dong?" | Focus open-source (SWE-Agent, OpenHands). Cursor chi test manual sample 20-30 tasks |
| 5 | "Agent update defense giua luc study?" | Lock version, ghi ro version tested. Hoan toan co the xay ra — la limitation |
| 6 | "400 adversarial variants ai tao? Bao lau?" | Dung template + semi-automated generation. 2-3 tuan, 2 nguoi review doc lap |
| 7 | "20 MITRE techniques chon theo tieu chi gi?" | Chon theo: (a) applicable cho coding context, (b) co precedent trong D3/D4 |
| 8 | "Open-source benchmark co bi weaponize khong?" | Release benchmark KHONG co payloads. Payloads chi share qua responsible disclosure |
| 9 | "Chi Python — generalize sang ngon ngu khac?" | Acknowledge limitation. Python la starting point vi SWE-bench |
| 10 | "Vu Claude leak co phu hop viet trong paper academic?" | Dung nhu boi canh thuc te (nhu Heartbleed, Log4j). Khong sensationalize, chi cite facts |

---

## 4. De cuong v1 — Tom tat

### 4.1. Phuong phap

- 100 tasks tu SWE-bench Verified
- 4 loai adversarial variants x 100 = 400 instances + 100 clean = 500 tong
- 4 agents: SWE-Agent, OpenHands, Claude Code, Cursor
- 20 MITRE ATT&CK techniques
- Metric: RR, ASR, SRR = RR x (1-ASR)

### 4.2. Nhung gi can thay doi cho v2

```
[CAN THEM] Ethics & Responsible Disclosure section
[CAN GIAM] 6 muc tieu → 4 muc tieu
[CAN SUA]  SRR → de xuat weighted version, so sanh ca 2
[CAN SUA]  Budget $500-800 → $1,500-2,500
[CAN SUA]  Cursor → bo hoac chi manual sample
[CAN THEM] Pilot study (50-100 evals truoc)
[CAN THEM] Threats to validity
[CAN THEM] Risk analysis
```

---

## 5. Tai nguyen

### 5.1. Papers quan trong nhat cho Gap 2

| Paper | Vai tro |
|-------|---------|
| D1 (AgenticSecurity) | Taxonomy moi de doa — 94.4% agents vulnerable |
| D2 (SecurePatterns) | 6 design patterns phong thu — test hieu qua |
| D3 (AIShellJack) | 314 payloads, 70 MITRE techniques — nguon payload |
| D4 (Maloyan 2026) | SoK, 42 attack techniques — taxonomy tan cong |
| D5 (DefensePipeline) | Multi-agent defense — baseline defense |
| C1 (SWE-Bench Pro) | Tasks goc de tao adversarial variants |

### 5.2. Repos lien quan

| Repo | Vai tro |
|------|---------|
| `princeton-nlp/SWE-agent` | Agent goc de test |
| `All-Hands-AI/OpenHands` | Agent co safety features |
| `haihpse150218/claw-code-free` | Kinh nghiem harness/security |
| MITRE ATT&CK framework | Taxonomy ky thuat tan cong |

---

## 6. RESUME GUIDE

> **Ngay cap nhat:** 06/04/2026
> **Trang thai:** De cuong v1 xong, phan bien xong (6.7/10). CHUA viet v2.

### 6.1. Trang thai hien tai

```
[XONG] Research 49 papers
[XONG] GAP-ANALYSIS (Gap 2 rank #2, diem 13/15)
[XONG] De cuong v1 (DE-CUONG-SecureCodeBench.md)
[XONG] Phan bien (THAO-LUAN-SecureCodeBench.md, 6.7/10)

[CHUA] De cuong v2 (ap dung phan bien)
[CHUA] Visualization
[CHUA] Nop cho advisor
[CHUA] Bat dau thuc hien
```

### 6.2. File quan trong

| Thu tu | File | Muc dich |
|--------|------|---------|
| 1 | **Plan-SecureCodeBench.md** (file nay) | Tong quan, resume guide |
| 2 | **DE-CUONG-SecureCodeBench.md** | De cuong v1 |
| 3 | **THAO-LUAN-SecureCodeBench.md** | Phan bien + 10 cau hoi + goi y |
| 4 | **GAP-ANALYSIS.md** | Gap 2 analysis |

### 6.3. Neu muon viet v2

```
1. Doc THAO-LUAN-SecureCodeBench.md — xem 6 van de + 10 cau hoi
2. Tao DE-CUONG-SecureCodeBench-v2.md (KHONG ghi de v1)
3. Ap dung:
   a. THEM section Ethics & Responsible Disclosure
   b. GIAM 6 → 4 muc tieu
   c. DE XUAT weighted SRR, so sanh voi simple SRR
   d. TINH LAI budget ($1,500-2,500)
   e. BO Cursor (hoac chi manual sample)
   f. THEM pilot study (50-100 evals)
   g. THEM threats to validity + risk analysis
4. Moi section them note "Thay doi so voi v1"
5. Cuoi file them Phu Luc: bang V1 vs V2
```

### 6.4. Y tuong 1 cau

> **"SWE-bench chi hoi: Agent co giai duoc khong? SecureCodeBench hoi them: Agent co BI HACK trong luc giai khong?"**

---

## 7. So sanh voi Gap 1 (HarnessEval)

| Tieu chi | HarnessEval (Gap 1) | SecureCodeBench (Gap 2) |
|----------|--------------------|-----------------------|
| Diem phan bien | 7.3/10 | 6.7/10 |
| V2 da viet? | DA VIET | CHUA |
| Novelty | 5/5 (hoan toan moi) | 4/5 (rat moi) |
| "Wow factor" | Academic (framework moi) | Industry (vu leak, bao mat) |
| Rui ro chinh | "Artificial gap?" | Ethics, SRR qua don gian |
| Budget | $2,500-3,100 | $1,500-2,500 |
| Co the ket hop? | Gap 1 co Safety dimension → co the bao gom Gap 2 nhu 1 phan | Gap 2 doc lap duoc |
