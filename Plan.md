# PLAN: Chuẩn bị viết Đề cương NCKH

> **Bối cảnh:** Chương trình Thạc sĩ Kỹ thuật phần mềm AI — FPT
> **Loại tài liệu cần viết:** Đề cương đề tài NCKH (bài tập môn *Methods of Learning and Scientific Research*)
> **Template tham chiếu:** `phuong-phap-viet-de-cuong-nckh.md`
> **Bài báo mẫu đã phân tích:** Ho-Van 2013 — *Exact outage analysis of underlay cooperative cognitive networks* (dùng làm khuôn mẫu cấu trúc 5 chương)

---

## 1. Mục tiêu cuối cùng
Viết được một **Đề cương NCKH ~10 trang** theo đúng template 7 bước, trong đó:
- Có **research gap rõ ràng** (tìm ra bằng cách đọc nhiều bài báo)
- Có **tên đề tài** thỏa mãn: đơn nghĩa, có điểm mới, có từ khóa, phạm vi rõ
- Phân biệt được **mục đích (định tính)** vs **mục tiêu (định lượng)**
- Có **mục lục dự kiến** theo cấu trúc 5 chương

---

## 2. Chiến lược tổng thể (4 giai đoạn)

### Giai đoạn 1 — Chọn hướng đề tài (NARROWING)
**Trạng thái:** ⏸ Đang chờ quyết định của user

Lý do cần làm trước khi tải 50 bài: "AI" quá rộng (hàng triệu paper/năm). Nếu tải 50 bài random → 50 bài thuộc 50 hướng khác nhau → không rút ra được gap.

**Các nhánh AI để chọn (chọn 1-2):**

| # | Nhánh | Ví dụ đề tài |
|---|---|---|
| 1 | **LLM & Generative AI** | RAG, prompt engineering, agent framework, fine-tuning |
| 2 | **Computer Vision** | Nhận dạng ảnh y tế, object detection, deepfake detection, OCR |
| 3 | **NLP (không phải LLM)** | Sentiment analysis tiếng Việt, tóm tắt, chatbot domain-specific |
| 4 | **Recommender Systems** | Gợi ý sản phẩm, học liệu, nội dung |
| 5 | **AI cho Software Engineering** | Code review tự động, bug detection, test generation, copilot |
| 6 | **ML cổ điển / Dự đoán** | Churn, credit scoring, medical prediction |
| 7 | **Reinforcement Learning** | Game AI, robotics, optimization |
| 8 | **AI Ethics / Explainable AI** | Fairness, bias detection, XAI |
| 9 | **MLOps / AI Infrastructure** | Serving, monitoring, drift detection |
| 10 | **Khác** | Tự mô tả |

**Câu hỏi phụ cần trả lời khi quay lại:**
- [ ] Có data/bối cảnh công ty có thể tận dụng không?
- [x] **Kỹ năng mạnh sẵn có:** Python (developer chuyên nghiệp) → ưu tiên đề tài code-heavy, dễ prototype
- [ ] **Giảng viên/advisor:** profile Google Scholar `Xkv264kAAAAJ` — **cần user paste tay thông tin** (tên thầy + research interests + top 8-10 bài báo) vì Google Scholar chặn scraper
- [ ] Deadline nộp đề cương là khi nào?

**Hệ quả từ kỹ năng Python mạnh:**
- ✅ Các nhánh **ưu tiên**: LLM/RAG (#1), CV (#2), NLP (#3), AI4SE (#5), MLOps (#9) — đều code Python heavy
- ⚠️ Ít ưu tiên: RL (#7 — cần simulator phức tạp), AI Ethics (#8 — thiên lý thuyết hơn)

**Kết quả cần đạt của giai đoạn 1:** Chốt được **1 sub-domain hẹp** (ví dụ: "RAG cho tài liệu tiếng Việt" hoặc "LLM sinh test unit tự động cho Java").

---

### Giai đoạn 2 — Thu thập 50 bài báo
**Trạng thái:** ⏸ Chờ giai đoạn 1

**Cấu trúc thư mục:**
```
NCKK-Docs/
├── examples/                     # Đã có (IET Ho-Van 2013)
├── de-tai/
│   ├── papers/                   # 50 file PDF gốc
│   ├── summary/                  # 50 file .md tóm tắt (1 file/bài)
│   ├── INDEX.md                  # Bảng tổng hợp tất cả bài
│   └── GAP-ANALYSIS.md           # Bảng so sánh như Table 1 của Ho-Van
```

**Tiêu chí tải bài:**
- [ ] Ưu tiên bài **2022-2026** (mới nhất — vì AI thay đổi rất nhanh)
- [ ] Ưu tiên **top venue**: NeurIPS, ICML, ICLR, ACL, EMNLP, CVPR, AAAI, IEEE Trans., ACM…
- [ ] Mỗi bài phải **liên quan trực tiếp** tới hướng đã chốt ở Giai đoạn 1
- [ ] Lưu tên file dễ tra cứu: `YYYY_Author_ShortTitle.pdf`

**Nguồn tải gợi ý:** Google Scholar, arXiv, Semantic Scholar, Papers with Code, IEEE Xplore, ACM DL.

---

### Giai đoạn 3 — Đọc & Tóm tắt 50 bài
**Trạng thái:** ⏸ Chờ giai đoạn 2

**Template tóm tắt chuẩn** (mỗi bài 1 file `.md` trong `de-tai/summary/`):

```markdown
# [YYYY] [Tác giả] — [Tên bài]

## Metadata
- **Venue:** (NeurIPS/ACL/…)
- **Year:** 
- **Authors:** 
- **DOI/URL:** 
- **Citations:** 

## 1. Vấn đề (Problem)
Bài này giải quyết vấn đề gì? (2-3 câu)

## 2. Động cơ (Motivation / Gap)
Tại sao vấn đề này quan trọng? Các công trình trước thiếu gì?

## 3. Phương pháp (Method)
Tác giả đề xuất gì? (model, thuật toán, kiến trúc)

## 4. Đóng góp chính (Contributions)
- Gạch đầu dòng 3-5 điểm

## 5. Dataset & Metric
- Dataset nào?
- Đánh giá bằng metric gì?

## 6. Kết quả chính
Con số cụ thể, so với baseline nào.

## 7. Hạn chế & Hướng mở rộng
Bài tự nhận còn thiếu gì? (phần này QUAN TRỌNG — là nơi tìm gap)

## 8. Keywords
`keyword1` `keyword2` `keyword3` …

## 9. Relevance to my topic
Tại sao bài này liên quan / không liên quan đến hướng của tôi?
```

**Cách thực hiện hiệu quả (tránh đọc thủ công 50 bài):**
- **Đợt 1 — Sàng nhanh (skim):** Chỉ đọc Abstract + Introduction + Conclusion → loại bỏ bài không liên quan. Mục tiêu: từ 50 → 20-25 bài cốt lõi.
- **Đợt 2 — Đọc sâu:** 20-25 bài cốt lõi đọc kỹ theo template trên.
- **Đợt 3 — Đọc tham khảo:** 25-30 bài còn lại chỉ ghi nhận metadata + 1-2 câu mô tả vai trò làm context.
- **Công cụ hỗ trợ:** Có thể dùng Claude Code với parallel subagents để xử lý batch — mỗi subagent đọc 5-10 PDF và sinh summary.

---

### Giai đoạn 4 — Trích xuất Keywords & Chốt đề tài
**Trạng thái:** ⏸ Chờ giai đoạn 3

**Quy trình:**

1. **Tổng hợp keywords** từ 50 file summary → đếm tần suất → lọc top 20 keywords nổi bật.
2. **Vẽ bảng research landscape** (giống Table 1 của Ho-Van 2013):

```
| Ref | Feature A | Feature B | Feature C | Feature D | Dataset | Metric |
|-----|-----------|-----------|-----------|-----------|---------|--------|
| [1] |     ✓     |     —     |     ✓     |     —     |   ...   |  ...   |
| [2] |     —     |     ✓     |     ✓     |     ✓     |   ...   |  ...   |
```

→ **Ô trống = research gap ứng viên**.

3. **Liệt kê 3-5 gap ứng viên**, đánh giá theo 3 tiêu chí:
   - **Khả thi** (dữ liệu, compute, thời gian)
   - **Mới** (chưa ai làm hoặc làm chưa tốt)
   - **Có giá trị** (khoa học + thực tiễn)

4. **Chốt 1 gap → viết tên đề tài** theo công thức Ho-Van:
   > `[Tính mới] + [Phân tích/Phương pháp] + [Đối tượng] + [Điều kiện/Ràng buộc]`

   Ví dụ: *"Fine-tuning nhẹ LLaMA-3 bằng LoRA cho bài toán tóm tắt văn bản pháp lý tiếng Việt trong điều kiện dữ liệu thấp"*

5. **Viết Research Question + Mục đích + Mục tiêu** theo nguyên tắc phân biệt:
   - Mục đích (why, định tính): 1 câu
   - Mục tiêu (what/how, định lượng): 3-5 điểm đo được

---

## 3. Output cuối cùng của toàn bộ Plan
Sau 4 giai đoạn, bạn sẽ có:

- [ ] 50 file PDF trong `de-tai/papers/`
- [ ] 50 file summary `.md` trong `de-tai/summary/`
- [ ] `INDEX.md` — bảng tổng hợp tất cả bài
- [ ] `GAP-ANALYSIS.md` — bảng so sánh tìm ô trống
- [ ] `TOPIC.md` — tên đề tài đã chốt + research question + mục đích + mục tiêu
- [ ] **DE-CUONG.md** — bản đề cương hoàn chỉnh ~10 trang theo template 7 bước

---

## 4. Next Action (khi quay lại)
1. Quyết định nhánh AI (chọn 1-2 từ Giai đoạn 1)
2. Trả lời 4 câu hỏi phụ (data, kỹ năng, advisor, deadline)
3. Tôi sẽ tạo cấu trúc thư mục `NCKK-Docs/de-tai/...` và template summary chuẩn
4. Bắt đầu thu thập bài

---

## 5. Ghi chú
- **Linear thinking:** Mỗi giai đoạn kết thúc mới sang giai đoạn sau. Không nhảy cóc.
- **Bài học từ Ho-Van 2013:** Gap phải nhìn thấy bằng **bảng so sánh**, không phải bằng cảm giác.
- **YAGNI:** Không cố đọc 50 bài đều như nhau — ưu tiên đọc sâu 20 bài cốt lõi.
