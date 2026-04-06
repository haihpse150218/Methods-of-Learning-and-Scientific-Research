# PLAN: Nghien cuu Coding Agent Harness & Evaluation

> **Boi canh:** Chuong trinh Thac si Ky thuat phan mem AI — FPT
> **Mon hoc:** Methods of Learning and Scientific Research
> **Deadline:** Cuoi tuan 11-12/04/2026
> **Output:** De cuong NCKH ~10 trang

---

## 1. Huong de tai da chon

**Nhanh chinh:** LLM & Generative AI → Agent Framework
**Sub-domain:** Coding Agent Harness & Evaluation

**Boi canh thuc te:**
- Thang 3/2026: Source code Claude Code (Anthropic) bi leak qua npm sourcemap (~1,884 file TypeScript)
- Cong dong bung no fork/rewrite harness (claw-code, OpenDev...)
- Van de: Benchmark hien tai co lo hong nghiem trong (8/10 benchmark co van de, agent "khong lam gi" van pass 38% task)
- Harness design (tool system, context management, safety) quan trong khong kem model capability

**Research Questions (du kien):**
1. Cac coding agent harness hien tai duoc danh gia nhu the nao, va benchmark nao la dang tin cay?
2. Harness design (tool system, context management, planning loop) anh huong the nao den hieu suat agent?
3. Lam the nao de xay dung framework danh gia toan dien cho coding agent harness?

---

## 2. Tien do thu thap papers

### Da co (13 papers tu research truoc)

#### Coding Agent Harness (3 papers chinh)
| # | Paper | arXiv | Nam | Trang thai |
|---|-------|-------|-----|------------|
| 1 | OpenDev — Scaffolding, Harness, Context Engineering (Bui et al.) | 2603.05344 | 2026 | Da tom tat + phan tich |
| 2 | AutoHarness — LLM tu sinh code harness (Lou et al.) | 2603.03329 | 2026 | Da tom tat + phan tich |
| 3 | Coding Agents as Long-Context Processors (Cao et al.) | 2603.20432 | 2026 | Da tom tat + phan tich |

#### Multi-Agent Coding (10 papers)
| # | Paper | arXiv | Nam | Trang thai |
|---|-------|-------|-----|------------|
| 4 | TheBotCompany — Self-Organizing Multi-Agent (Lyu et al.) | 2603.25928 | 2026 | Da tom tat + phan tich |
| 5 | Coverage-Guided Multi-Agent Harness for Fuzzing | 2603.08616 | 2026 | Metadata |
| 6 | From Tool to Teammate — LLM Coding Agents (Chen et al.) | 2603.27440 | 2026 | Metadata |
| 7 | ALMAS — Autonomous Multi-Agent SE Framework | 2510.03463 | 2025 | Metadata |
| 8 | KGACG — Knowledge-Guided Multi-Agent Code Gen | 2510.19868 | 2025 | Metadata |
| 9 | MOSAIC — Multi-agent Scientific Code Gen | 2510.08804 | 2025 | Metadata |
| 10 | LessonL — Multi-Agent Learn and Improve | 2505.23946 | 2025 | Metadata |
| 11 | Survey on Code Gen with LLM-based Agents (Dong et al.) | 2508.00083 | 2025 | Metadata |
| 12 | XL-CoGen — Multi-Language Code Gen | 2509.19918 | 2025 | Metadata |
| 13 | MACOG — Multi-Agent IaC | 2510.03902 | 2025 | Metadata |

#### Surveys quan trong (reference)
| # | Paper | arXiv | Nam |
|---|-------|-------|-----|
| S1 | Survey on LLM-based Autonomous Agents (Wang et al.) | 2308.11432 | 2023 |
| S2 | LLM Multi-Agent Systems: Challenges (Han et al.) | 2402.03578 | 2024 |
| S3 | Memory for Autonomous LLM Agents | 2603.07670 | 2025 |
| S4 | Agentic AI comprehensive survey (Springer) | — | 2025 |
| S5 | Survey on Evaluation of LLM-based Agents | 2503.16416 | 2025 |

### Dang search (2 batch song song)
- **Batch 1 (15 papers):** Agent Evaluation, Agent Safety/Security, Agent Memory
- **Batch 2 (15 papers):** Tool-Use, Planning/Reasoning, Multi-Agent Orchestration
- **Bo sung:** ~7 papers nua de du 50

---

## 3. Cau truc thu muc

```
NCKK-Docs/
├── examples/                     # Da co (IET Ho-Van 2013)
├── de-tai/
│   ├── papers/                   # 50 file PDF goc (tu arXiv)
│   ├── summary/                  # 50 file .md tom tat
│   ├── INDEX.md                  # Bang tong hop tat ca bai
│   └── GAP-ANALYSIS.md           # Bang so sanh tim research gap
```

---

## 4. Template tom tat moi bai

```markdown
# [YYYY] [Tac gia] — [Ten bai]

## Metadata
- **arXiv:** 
- **Venue:** 
- **Year:** 
- **Authors:** 
- **Citations:** 

## 1. Van de (Problem)
2-3 cau

## 2. Dong co / Gap
Tai sao quan trong? Cong trinh truoc thieu gi?

## 3. Phuong phap (Method)
Model, thuat toan, kien truc

## 4. Dong gop chinh (Contributions)
- 3-5 diem

## 5. Diem manh (Strengths)
- ...

## 6. Han che (Limitations)  
- ...

## 7. Dataset & Metric
- Dataset, benchmark
- Metric danh gia

## 8. Ket qua chinh
Con so cu the, so voi baseline

## 9. Keywords
`keyword1` `keyword2` ...

## 10. Lien quan den de tai cua toi
Tai sao bai nay lien quan?
```

---

## 5. Chien luoc tim Research Gap

### Cac gap ung vien (tu research ban dau)

| # | Gap | Mo ta | Kha thi |
|---|-----|-------|---------|
| G1 | Benchmark Validity | 8/10 benchmark co loi, agent "lam mo" van pass 38% | Rat cao |
| G2 | Harness Design Evaluation | Chua co framework danh gia harness (tool system, context mgmt) | Cao |
| G3 | Cross-Session Memory | Memory xuyên phien chua duoc giai quyet tot | Cao |
| G4 | Selective Forgetting | Agent khong biet quen thong tin cu/sai | Cao |
| G5 | Tool-Use Reliability | Agent chon sai tool, khong co co che phuc hoi | Cao |
| G6 | Agent Security | Prompt injection, source code leak, safety bypass | Cao |
| G7 | Self-Organizing Harness | Tu dong toi uu harness (AutoHarness) chua generalize | Trung binh |

### Phuong phap chot gap (theo Ho-Van 2013)
1. Tong hop keywords tu 50 summaries → top 20 keywords
2. Ve bang research landscape (Table feature comparison)
3. Tim o trong = research gap
4. Danh gia: Kha thi + Moi + Co gia tri
5. Chot 1 gap → viet ten de tai

---

## 6. Literature Review da viet

### Phien ban tieng Anh
> Recent advances in LLM-based coding agents have shifted focus from single-agent systems toward more sophisticated multi-agent architectures... [xem Plan.md cu hoac file rieng]

### Phien ban tieng Viet  
> Cac tien bo gan day trong coding agent dua tren LLM da chuyen huong tu he thong single-agent sang cac kien truc multi-agent phuc tap hon... [xem Plan.md cu hoac file rieng]

---

## 7. Cong cu & Tai nguyen

### Nguon tai papers (hop phap)
- **arXiv.org** — mien phi 100%
- **Semantic Scholar** — mien phi, co API
- **Papers with Code** — mien phi, co code di kem
- **Google Scholar** → nhieu bai link ve arXiv
- **IEEE Xplore / ACM DL** — qua thu vien FPT

### Repo lien quan
- `haihpse150218/claw-code-free` — Clean-room rewrite Claude Code harness
- `haihpse150218/antigravity-awesome-skills` — 1,326+ SKILL.md playbooks
- `instructkr/claw-code` — Python fork pho bien nhat
- `syifan/thebotcompany` — Multi-agent self-organizing framework

### Ky nang co san
- Python (developer chuyen nghiep) → uu tien de tai code-heavy
- Kinh nghiem voi coding agent harness (claw-code-free)

---

## 8. Timeline (deadline: 11-12/04/2026)

| Ngay | Nhiem vu | Trang thai |
|------|----------|------------|
| 06/04 | Chot huong + research 50 papers | Dang lam |
| 07/04 | Hoan thanh 50 summaries | Chua |
| 08/04 | GAP-ANALYSIS + chot de tai | Chua |
| 09/04 | Viet de cuong (Chuong 1-3) | Chua |
| 10/04 | Viet de cuong (Chuong 4-5) + review | Chua |
| 11/04 | Hoan chinh + nop | Chua |

---

## 9. Next Actions
1. ⏳ Cho ket qua 2 batch search (30 papers)
2. Bo sung 7 papers con thieu
3. Tao INDEX.md tong hop 50 papers
4. Doc va tom tat theo template
5. Xay dung GAP-ANALYSIS.md
6. Chot de tai + viet de cuong
