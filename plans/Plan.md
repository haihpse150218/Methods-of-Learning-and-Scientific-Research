# PLAN: Chuẩn bị viết Đề cương NCKH

> **Bối cảnh:** Chương trình Thạc sĩ Kỹ thuật phần mềm AI — FPT
> **Loại tài liệu cần viết:** Đề cương đề tài NCKH (bài tập môn *Methods of Learning and Scientific Research*)
> **Template tham chiếu:** `phuong-phap-viet-de-cuong-nckh.md`
> **Bài báo mẫu đã phân tích:** Ho-Van 2013 — *Exact outage analysis of underlay cooperative cognitive networks* (dùng làm khuôn mẫu cấu trúc 5 chương)
> **Cập nhật lần cuối:** 2026-04-08

---

## 1. Mục tiêu cuối cùng
Viết được một **Đề cương NCKH ~10 trang** theo đúng template 7 bước, trong đó:
- Có **research gap rõ ràng** (tìm ra bằng cách đọc nhiều bài báo)
- Có **tên đề tài** thỏa mãn: đơn nghĩa, có điểm mới, có từ khóa, phạm vi rõ
- Phân biệt được **mục đích (định tính)** vs **mục tiêu (định lượng)**
- Có **mục lục dự kiến** theo cấu trúc 5 chương

---

## 2. Chiến lược tổng thể (4 giai đoạn + 2 giai đoạn mở rộng)

### Giai đoạn 1 — Chọn hướng đề tài (NARROWING)
**Trạng thái:** ✅ HOÀN THÀNH

**Kết quả:**
- Chọn nhánh **#1 LLM & Generative AI** + **#5 AI cho Software Engineering**
- Sub-domain: **Coding Agent Harness & Evaluation**
- Kỹ năng Python mạnh → phù hợp hoàn hảo với đề tài code-heavy

---

### Giai đoạn 2 — Thu thập 50 bài báo
**Trạng thái:** ✅ HOÀN THÀNH

**Kết quả:**
- 49 papers + 5 surveys tham khảo = **54 bài** trong `NCKK-Docs/de-tai/papers/`
- Phân loại theo 9 nhóm: A (Harness), B (Multi-Agent), C (Benchmarks), D (Security), E (Memory), F (Tool-Use), G (Planning), H (MAS Frameworks), I (Industry/Analytics), S (Surveys)
- Tất cả 2023–2026, ưu tiên arXiv + top venue
- Đặt tên theo chuẩn: `{Group}{#}_{Year}_{Author}_{ShortTitle}.pdf`
- Tổng hợp trong `INDEX.md`

---

### Giai đoạn 3 — Đọc & Tóm tắt 50 bài
**Trạng thái:** ✅ HOÀN THÀNH

**Kết quả:**
- 49+ file summary `.md` trong `NCKK-Docs/de-tai/summary/`
- Mỗi bài theo template chuẩn: Problem → Motivation → Method → Contributions → Dataset & Metric → Kết quả → Hạn chế → Keywords → Relevance

---

### Giai đoạn 4 — Trích xuất Keywords & Chốt đề tài
**Trạng thái:** ✅ HOÀN THÀNH

**Kết quả:**
- `GAP-ANALYSIS.md` hoàn chỉnh:
  - Top 20 keywords + 7 theme clusters
  - Research Landscape Table (49 papers × 13 features)
  - **6 gaps** được xác định và xếp hạng (Feasibility × Novelty × Value)
  - **Gap #1 (Rank 1):** Harness-Level Evaluation Framework — Feasibility 4, Novelty 5, Value 5, Total 14
  - **Gap #2 (Rank 2):** Security-Aware Coding Benchmarks — Total 13
- **Đề tài đã chốt:** HarnessEval — A Multi-Dimensional Evaluation Framework for Coding Agent Harness Infrastructure
- 3 Research Questions, 5 Research Objectives (RO1–RO5) được xác định

---

### Giai đoạn 5 — Viết Đề cương NCKH
**Trạng thái:** ✅ HOÀN THÀNH

**Kết quả:**
- `DE-CUONG.md` — bản draft đầu tiên
- `DE-CUONG-HarnessEval.md` — phiên bản chi tiết cho Topic 1
- `DE-CUONG-SecureCodeBench.md` — phiên bản chi tiết cho Topic 2
- **`DE-CUONG-HarnessEval-v2.md`** — phiên bản chính thức cuối cùng
- **`DE-CUONG-HarnessEval-v2.tex`** → **`DE-CUONG-HarnessEval-v2.pdf`** — bản LaTeX đã compile

---

### Giai đoạn 6 — Xây dựng Prototype (HarnessEval Toolkit)
**Trạng thái:** 🔄 ĐANG THỰC HIỆN — Phase 9/10

**Mục tiêu:** Implement RO5 — Python toolkit minh chứng tính khả thi của đề cương

**Kết quả đạt được (Phase 1–8):**
- ✅ Configs: 27 experiment conditions (3×3×3 factorial design)
- ✅ Metrics: 7 metrics trên 3 dimensions (Tool Dispatch, Context Utilization, Backend Portability)
- ✅ Statistical Analysis: Three-way ANOVA + GLMM + Cohen's d + Tukey HSD
- ✅ Pipeline Runner: dry-run + real mode
- ✅ SWE-Agent Log Parser (trajectory parser)
- ✅ CLI: `harness-eval info | pilot | run | convert | analyze`
- ✅ Streamlit Dashboard: interactive comparison + data overview
- ✅ Dry-run with 150 real SWE-bench Verified tasks
- ✅ One-click setup scripts + `.env.example`

**Phase tiếp theo:**
- Phase 9: Equivalence Verification + Production readiness
- Phase 10: Final documentation + demo

**Chi tiết:** Xem `Plan-Coding-HarnessEval.md`

---

## 3. Output cuối cùng của toàn bộ Plan

- [x] 49+ file PDF trong `de-tai/papers/`
- [x] 49+ file summary `.md` trong `de-tai/summary/`
- [x] `INDEX.md` — bảng tổng hợp 54 bài (49 papers + 5 surveys)
- [x] `GAP-ANALYSIS.md` — bảng so sánh + 6 gaps + ranking
- [x] Đề tài đã chốt: **HarnessEval** (research questions + objectives trong đề cương)
- [x] **`DE-CUONG-HarnessEval-v2.pdf`** — đề cương hoàn chỉnh (LaTeX, đã compile)
- [ ] **HarnessEval Toolkit** — prototype Python (Phase 9–10 còn lại)

---

## 4. Next Action
1. Hoàn thành **Phase 9** của coding plan: Equivalence Verification + Production
2. Hoàn thành **Phase 10**: Final documentation + demo
3. Chuẩn bị nộp đề cương + demo cho giảng viên

---

## 5. Ghi chú
- **Linear thinking:** Mỗi giai đoạn kết thúc mới sang giai đoạn sau. Không nhảy cóc.
- **Bài học từ Ho-Van 2013:** Gap phải nhìn thấy bằng **bảng so sánh**, không phải bằng cảm giác.
- **YAGNI:** Không cố đọc 50 bài đều như nhau — ưu tiên đọc sâu 20 bài cốt lõi.
- **Coding plan chi tiết:** `Plan-Coding-HarnessEval.md` — theo dõi từng phase implement
