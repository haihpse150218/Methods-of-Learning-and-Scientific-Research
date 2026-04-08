# PLAN: Ket hop HarnessEval + SecureCodeBench
# (Gap 1 + Gap 2 trong 1 de tai)

> **Boi canh:** Chuong trinh Thac si Ky thuat phan mem AI — FPT
> **Mon hoc:** Methods of Learning and Scientific Research
> **De tai:** Khung danh gia da chieu cho ha tang Coding Agent — Tich hop hieu suat, bao mat va kha nang thich ung
> **Trang thai:** De cuong v1 da viet, da phan bien (7.0/10). CHUA viet v2.

---

## 1. Tong quan

### 1.1. Y tuong

Ket hop **Gap 1 (HarnessEval)** va **Gap 2 (SecureCodeBench)** thanh 1 de tai thong nhat:
- **HarnessEval** cung cap framework 5 chieu (Tool, Context, Safety, Session, Portability)
- **SecureCodeBench** cung cap benchmark adversarial cho chieu Safety
- Safety tro thanh 1 trong 5 chieu, khong phai de tai rieng

### 1.2. Ten de tai

**Tieng Viet:** Khung danh gia da chieu cho ha tang Coding Agent: Tich hop hieu suat, bao mat va kha nang thich ung voi nhieu mo hinh ngon ngu lon

**Tieng Anh:** HarnessEval: A Multi-Dimensional Evaluation Framework for Coding Agent Infrastructure Integrating Performance, Security, and Backend Portability

### 1.3. Uu va nhuoc diem cua cach ket hop

| Uu diem | Nhuoc diem |
|---------|-----------|
| De tai toan dien hon — 1 framework thay vi 2 | Scope RAT LON cho 1 nguoi / 6 thang |
| Security la 1 chieu tu nhien cua harness | Budget cao ($1,500-2,000 cho evaluation only) |
| "Wow factor" cao — ca framework + security | 5 muc tieu co the khong hoan thanh het |
| Publication potential cao hon (nhieu dong gop) | Rui ro "all framework, no substance" |

---

## 2. Tien do da hoan thanh

| Hang muc | Trang thai | File |
|----------|------------|------|
| Research 49 papers | XONG | INDEX.md, summary/*.md |
| GAP-ANALYSIS | XONG | GAP-ANALYSIS.md |
| De cuong Ket hop v1 | XONG | DE-CUONG.md |
| Phan bien Ket hop | XONG | THAO-LUAN-KetHop.md (7.0/10) |
| **De cuong v2** | **CHUA** | Can ap dung phan bien |

---

## 3. Ket qua phan bien: 7.0/10

### 3.1. Van de chinh

| # | Van de | Muc do |
|---|--------|--------|
| 1 | **Scope qua rong** — 5 MT, 400 adversarial instances, 50 conditions, tu xay harness, 6 thang | NGHIEM TRONG |
| 2 | **Budget $500-1,000 qua thap** — thuc te $5,000-20,000 | NGHIEM TRONG |
| 3 | **Tu xay harness roi tu danh gia** — conflict of interest | CAO |
| 4 | **Expert validation mau nho** — 3-5 experts tren 30 samples | TRUNG BINH |
| 5 | **SRR formula chua justified** — tai sao nhan? Tai sao khong cong? | TRUNG BINH |

### 3.2. 3 viec can lam ngay (theo hoi dong)

1. **Giam scope:** 5 MT → 3 MT, 400 adversarial → 100-150, 50 conditions → 10-15
2. **Tinh lai budget:** thuc te va xin funding hoac dung open-source LLMs
3. **Bo tu xay harness:** dung SWE-Agent/OpenHands co san

---

## 4. Nhung gi can lam cho v2

```
[CAN GIAM] 5 muc tieu → 3 muc tieu cot loi
[CAN GIAM] 400 adversarial → 100-150 instances
[CAN GIAM] 50 conditions → 10-15 conditions
[CAN SUA]  Tu xay harness → fork SWE-Agent
[CAN SUA]  Budget $500-1,000 → $2,000-3,500
[CAN SUA]  SRR → de xuat + justify multiplicative vs additive
[CAN THEM] Ethics & Responsible Disclosure
[CAN THEM] Pilot study
[CAN THEM] Threats to validity + Risk analysis
[CAN THEM] Power analysis
```

---

## 5. So sanh 3 huong de tai

| Tieu chi | HarnessEval (Gap 1) | SecureCodeBench (Gap 2) | Ket hop (Gap 1+2) |
|----------|--------------------|-----------------------|-------------------|
| Diem phan bien | **7.3**/10 | 6.7/10 | 7.0/10 |
| V2 da viet? | **DA VIET** | Chua | Chua |
| Scope | Vua phai (27 conditions) | Vua phai (500 instances) | **QUA LON** |
| Budget | $2,500-3,100 | $1,500-2,500 | $3,500-5,000+ |
| Novelty | 5/5 | 4/5 | 5/5 |
| Kha thi 6 thang | **Cao (sau v2)** | Trung binh | Thap |
| Rui ro | Thap | Trung binh (ethics) | **Cao** |
| Khuyen nghi | **UU TIEN #1** | Backup / future work | Chi lam neu co >9 thang |

### Khuyen nghi chinh

> **Neu chi co 6 thang:** Chon **HarnessEval (Gap 1)** — da co v2 hoan chinh, scope hop ly.
>
> **Neu co 9-12 thang:** Co the lam **Ket hop** nhung phai giam scope dang ke.
>
> **SecureCodeBench** co the lam **sau** HarnessEval nhu bai bao thu 2, hoac nhu **future work** trong luan van.

---

## 6. RESUME GUIDE

> **Ngay cap nhat:** 06/04/2026
> **Trang thai:** De cuong Ket hop v1 xong, phan bien xong (7.0/10). CHUA viet v2.

### 6.1. Trang thai

```
[XONG] De cuong v1 (DE-CUONG.md)
[XONG] Phan bien (THAO-LUAN-KetHop.md, 7.0/10)

[CHUA] De cuong v2
[CHUA] Quyet dinh co nen ket hop hay tach rieng
```

### 6.2. File quan trong

| Thu tu | File | Muc dich |
|--------|------|---------|
| 1 | **Plan-KetHop.md** (file nay) | Tong quan, so sanh 3 huong |
| 2 | **DE-CUONG.md** | De cuong Ket hop v1 |
| 3 | **THAO-LUAN-KetHop.md** | Phan bien + goi y |
| 4 | **Plan-HarnessEval.md** | Plan Gap 1 (da hoan chinh nhat) |
| 5 | **Plan-SecureCodeBench.md** | Plan Gap 2 |

### 6.3. Neu quyet dinh lam Ket hop v2

```
1. Doc THAO-LUAN-KetHop.md — 5 van de + goi y
2. Quyet dinh: ket hop THAT hay chi lam Gap 1 + de Gap 2 future work?
3. Neu ket hop:
   a. Lay DE-CUONG-HarnessEval-v2.md lam base (da chinh sua tot)
   b. Them chieu Safety tu DE-CUONG-SecureCodeBench.md
   c. Giam adversarial variants tu 400 → 100
   d. THEM Ethics section
   e. Tao DE-CUONG-KetHop-v2.md
4. Neu khong ket hop:
   → Dung DE-CUONG-HarnessEval-v2.md (da san sang)
   → De SecureCodeBench lam future work trong Chuong 5
```

### 6.4. Y tuong 1 cau

> **"Ket hop = Framework toan dien nhung rui ro cao. Tach rieng = An toan hon, lam tung phan. Master's thesis nen an toan."**

---

## 7. Loi khuyen cuoi

Dua tren toan bo quy trinh (49 papers, 3 de cuong, 3 phan bien):

1. **HarnessEval (Gap 1) la lua chon tot nhat** cho master's thesis 6 thang
2. **SecureCodeBench (Gap 2) lam bai bao rieng** hoac future work
3. **Ket hop chi khi co >9 thang** va da hoan thanh HarnessEval truoc
4. De cuong HarnessEval v2 **da san sang nop** — khong can chinh sua them
5. Buoc tiep theo: **nop cho advisor** va bat dau GD1 (taxonomy + expert validation)
