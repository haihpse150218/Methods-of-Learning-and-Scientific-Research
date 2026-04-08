# Luồng dữ liệu tổng quan HarnessEval

## Nguyên tắc cốt lõi

> **Chúng ta KHÔNG tạo data mới.** SWE-bench cung cấp sẵn issues, repos, tests, đáp án. Chúng ta chỉ **thay đổi cách agent chạy** (27 configs) rồi **đo kết quả**.

---

## Tổng quan luồng dữ liệu

```
SWE-bench Verified (dataset)     SWE-Agent (agent)          HarnessEval (toolkit)
─────────────────────────        ──────────────────         ────────────────────
150 tasks thật                   Chạy 27 conditions         Thu thập & phân tích
(issues từ Django,               (thay đổi tools,           (7 metrics + ANOVA)
 Flask, scikit-learn...)         context, backend)
        │                              │                          │
        ▼                              ▼                          ▼
  Input: issue text           Agent fix bug → patch         So sánh 27 conditions
  + repo@commit               → .traj file                 → yếu tố nào quan trọng nhất?
```

---

## SWE-bench cung cấp gì?

| Thứ | Vai trò trong HarnessEval |
|-----|--------------------------|
| **150 GitHub issues** | Bài test cho agent (input) — đề bài |
| **150 repos + commits** | Codebase để agent làm việc — môi trường |
| **150 test suites** | Chấm điểm: patch đúng hay sai — đáp án |
| **FAIL_TO_PASS** | Tests phải PASS sau fix → chứng minh fix đúng |
| **PASS_TO_PASS** | Tests phải vẫn PASS → không regression |
| **Gold patch** | Đáp án tham khảo (chúng ta không dùng trực tiếp) |

### Chúng ta KHÔNG tạo:
- ❌ Không tạo issues mới
- ❌ Không tạo repos mới
- ❌ Không viết tests mới
- ❌ Không tạo ground truth mới

### Chúng ta CHỈ thay đổi:
- ✅ Cấu hình tools (FULL/MEDIUM/MINIMAL)
- ✅ Chiến lược context (FULL/SLIDING/SUMMARY)
- ✅ LLM backend (Claude/GPT/DeepSeek)

---

## Luồng chi tiết cho 1 condition

```
Ví dụ: condition = full_sliding_window_claude

Bước 1: Load 150 tasks từ SWE-bench Verified
         ↓
Bước 2: Với mỗi task (song song hoặc tuần tự):
         ├── Docker container: checkout repo@base_commit
         ├── Agent nhận problem_statement (issue text)
         ├── Agent loop (với config: 12 tools + sliding window + Claude):
         │   ├── Đọc code
         │   ├── Reproduce bug
         │   ├── Sửa code
         │   ├── Chạy test
         │   └── Submit patch
         ├── Output: .traj file + predictions.jsonl
         └── Cleanup container
         ↓
Bước 3: SWE-bench evaluate
         ├── Apply patch vào container
         ├── Chạy test suite thật
         ├── Check FAIL_TO_PASS → PASS?
         ├── Check PASS_TO_PASS → vẫn PASS?
         └── Grading: FULL / PARTIAL / NO
         ↓
Bước 4: Thu thập kết quả
         ├── resolve_rate = FULL / 150
         ├── Parse trajectories → tính 7 metrics
         └── Lưu vào dataset tổng hợp
```

---

## Số liệu đầu ra cho mỗi condition

```
Ví dụ: full_sliding_window_claude
─────────────────────────────────
resolve_rate           = 45/150 = 30%        ← metric chính (từ SWE-bench eval)

M1.1 correct_selection = 0.82               ← tool dispatch metrics
M1.2 redundant_call    = 0.15                  (tính từ .traj files)
M1.3 utilization_breadth = 0.75

M2.1 info_retention    = 0.88               ← context metrics
M2.2 effective_token   = 0.62                  (tính từ .traj files)

M3.1 cross_backend_std = 0.05               ← portability metrics
M3.2 min_max_ratio     = 0.85                  (tính cross-backend)

cost_total             = $52.50
avg_turns_per_task     = 12.3
avg_tokens_per_task    = 45,000
```

### Tổng hợp 27 conditions = 1 bảng lớn

```
┌────────────┬─────────┬──────────┬──────────┬──────────────┬───────┬───────┐
│ Tool       │ Context │ Backend  │ Resolve% │ M1.1  M1.2   │ M2.1  │ Cost  │
├────────────┼─────────┼──────────┼──────────┼──────────────┼───────┼───────┤
│ full       │ full    │ claude   │ 35%      │ 0.85  0.12   │ 0.95  │ $52   │
│ full       │ full    │ gpt      │ 30%      │ 0.82  0.14   │ 0.93  │ $45   │
│ full       │ full    │ deepseek │ 25%      │ 0.80  0.16   │ 0.91  │ $22   │
│ full       │ sliding │ claude   │ 32%      │ 0.83  0.13   │ 0.82  │ $48   │
│ ...        │ ...     │ ...      │ ...      │ ...          │ ...   │ ...   │
│ minimal    │ summary │ deepseek │ 8%       │ 0.45  0.35   │ 0.55  │ $18   │
└────────────┴─────────┴──────────┴──────────┴──────────────┴───────┴───────┘
27 rows × ~10 metrics mỗi row
```

---

## ANOVA trả lời câu hỏi gì?

### Input: bảng 27 conditions ở trên
### Output: bảng phân tách variance

```
Two-way ANOVA: Harness config (9 levels) × Backend (3 levels)

┌──────────────────────┬───────────┬─────────┬──────────────────────────┐
│ Source               │ η² (%)    │ p-value │ Ý nghĩa                  │
├──────────────────────┼───────────┼─────────┼──────────────────────────┤
│ Tool Dispatch (D1)   │ ~25-35%   │ <0.001  │ ★★★ Ảnh hưởng lớn nhất  │
│ Context Strategy (D2)│ ~10-20%   │ <0.01   │ ★★  Ảnh hưởng trung bình│
│ LLM Backend (D3)     │ ~15-25%   │ <0.001  │ ★★★ Ảnh hưởng lớn       │
│ D1 × D2 interaction  │ ~5-10%    │ <0.05   │ ★   Tool+Context tương tác│
│ Harness × Backend    │ ~5-10%    │ <0.05   │ ★   Harness giảm variance│
│ Residual             │ ~15-25%   │         │     Noise                │
└──────────────────────┴───────────┴─────────┴──────────────────────────┘
```

### Các giả thuyết nghiên cứu

| Giả thuyết | Nội dung | Đo bằng gì |
|------------|---------|-------------|
| **H1** | Tool system ảnh hưởng lớn nhất | Cohen's d > 0.5 |
| **H2** | Context management ảnh hưởng trung bình | Cohen's d = 0.3-0.5 |
| **H3** | Harness giải thích ≥20% variance (không phụ thuộc LLM) | η² ≥ 0.20 |
| **H4** | Backend variance giảm khi harness tốt hơn | Interaction effect |

### Kết luận mong đợi

> "Tool system giải thích ~30% variance → quan trọng nhất"
> "Harness tổng cộng giải thích ≥20% variance → độc lập với LLM"
> "Một harness tốt giảm sự phụ thuộc vào model cụ thể"

---

## Vai trò của từng thành phần

```
┌─────────────────────────────────────────────────────────────┐
│                    HarnessEval Research                       │
│                                                              │
│  SWE-bench          = Sân thi đấu (150 bài, có đáp án)     │
│  SWE-Agent          = Thí sinh (coding agent)                │
│  27 YAML configs    = 27 cách "trang bị" cho thí sinh       │
│  harness_eval/      = Ban giám khảo (tính metrics + ANOVA)  │
│                                                              │
│  Câu hỏi nghiên cứu:                                        │
│  "Trang bị (harness) quan trọng hơn hay                     │
│   năng lực bẩm sinh (LLM) quan trọng hơn?"                  │
│                                                              │
│  Trả lời: Bảng ANOVA phân tách variance                     │
│           → % do harness vs % do LLM vs % do interaction     │
└─────────────────────────────────────────────────────────────┘
```

---

## Pipeline end-to-end

```
                    ┌───────────────────┐
                    │ SWE-bench Verified│
                    │ 150 tasks         │
                    └────────┬──────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
     ┌──────────────┐┌──────────────┐┌──────────────┐
     │ Condition 1  ││ Condition 2  ││ ... ×27      │
     │ full/full/   ││ full/full/   ││              │
     │ claude       ││ gpt          ││              │
     └──────┬───────┘└──────┬───────┘└──────┬───────┘
            │               │               │
            ▼               ▼               ▼
     ┌──────────────┐┌──────────────┐┌──────────────┐
     │ 150 .traj    ││ 150 .traj    ││ 150 .traj    │
     │ + preds.json ││ + preds.json ││ + preds.json │
     └──────┬───────┘└──────┬───────┘└──────┬───────┘
            │               │               │
            ▼               ▼               ▼
     ┌──────────────────────────────────────────────┐
     │           SWE-bench Evaluation               │
     │  Apply patches → Run tests → Grade           │
     │  → resolve_rate per condition                 │
     └──────────────────┬───────────────────────────┘
                        │
                        ▼
     ┌──────────────────────────────────────────────┐
     │         harness_eval/ Analysis               │
     │                                              │
     │  1. Parse .traj → tính 7 metrics             │
     │  2. Tổng hợp 27 conditions → bảng data       │
     │  3. Two-way ANOVA → phân tách variance        │
     │  4. Cohen's d, Tukey HSD → effect sizes       │
     │  5. Bonferroni correction → multiple testing   │
     │                                              │
     │  Output: "Tool system giải thích X% variance" │
     └──────────────────────────────────────────────┘
```

---

## Tóm tắt

| Câu hỏi | Trả lời |
|----------|---------|
| Data từ đâu? | **SWE-bench Verified** (có sẵn, không tạo mới) |
| Bao nhiêu tasks? | **150 tasks** (subset từ 500) |
| Ai chạy tasks? | **SWE-Agent** (fork, không sửa source) |
| Thay đổi gì? | **27 harness configs** (3 tools × 3 context × 3 backend) |
| Đo gì? | **resolve_rate** + 7 metrics trên 3 dimensions |
| Phân tích gì? | **Two-way ANOVA** → % variance mỗi factor |
| Kết luận gì? | Harness quality quan trọng, không chỉ phụ thuộc model |
| Chi phí? | **~$2,500-3,100** (API) hoặc **~$20-40** (local demo) |
