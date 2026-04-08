# Giải thích kỹ: Số liệu đầu ra & ANOVA

## Tổng quan metrics

Mỗi condition (ví dụ: `full_sliding_window_claude`) cho ra:

```
resolve_rate           = 45/150 = 30%        ← metric chính (từ SWE-bench)
M1.1 correct_selection = 0.82               ← tool dispatch
M1.2 redundant_call    = 0.15
M1.3 utilization_breadth = 0.75
M2.1 info_retention    = 0.88               ← context
M2.2 effective_token   = 0.62
M3.1 cross_backend_std = 0.05               ← portability
M3.2 min_max_ratio     = 0.85
cost                   = $52.50
avg_turns              = 12.3
```

---

## 1. resolve_rate (Metric chính)

**"Tỷ lệ fix bug thành công"** — từ SWE-bench evaluation, không phải tự tính.

```
150 tasks → Agent chạy → 150 patches → SWE-bench evaluate:
  - 45 tasks: ALL tests pass (FAIL_TO_PASS → PASS, PASS_TO_PASS vẫn PASS) → FULL ✅
  - 105 tasks: tests fail → NO ❌
  
resolve_rate = 45 / 150 = 30%
```

**Ý nghĩa:** Với config `full_sliding_window_claude`, agent fix được 30% bugs.
Thay config khác → tỷ lệ thay đổi → so sánh 27 conditions → ANOVA.

---

## 2. Dimension 1: Tool Dispatch (M1.1, M1.2, M1.3)

**Đo agent dùng tools tốt hay dở.** Tính từ .traj files (log từng bước agent làm).

### M1.1 correct_selection_rate = 0.82 (82%)

**"Agent chọn đúng tool bao nhiêu %?"**

```
Ví dụ 1 trajectory (1 task):

Turn 1: Agent cần tìm file → gọi "grep"          ← Đúng ✅ (grep phù hợp)
Turn 2: Agent cần đọc file → gọi "read"           ← Đúng ✅
Turn 3: Agent cần sửa file → gọi "bash echo >"    ← Sai ❌ (nên dùng "edit")
Turn 4: Agent cần chạy test → gọi "test_runner"   ← Đúng ✅
Turn 5: Agent cần xem diff → gọi "git_diff"       ← Đúng ✅

correct_selection = 4/5 = 0.80
```

**Cách tính:** Với mỗi turn, đánh giá tool agent chọn có nằm trong danh sách "acceptable tools" cho action đó không. Lấy trung bình trên 150 tasks.

**Tại sao quan trọng:**
- FULL config (12 tools) → nhiều lựa chọn phù hợp → M1.1 cao
- MINIMAL (5 tools) → buộc dùng bash cho mọi thứ → M1.1 thấp

### M1.2 redundant_call_rate = 0.15 (15%)

**"Agent gọi tool thừa (output không được dùng) bao nhiêu %?"**

```
Turn 1: grep "def process" → output: "src/utils.py:42"
Turn 2: read src/utils.py  → sử dụng output Turn 1           ✅ Useful
Turn 3: grep "import os"   → output: "src/main.py:1"
Turn 4: grep "import sys"  → output: "src/main.py:2"
Turn 5: edit src/utils.py  → KHÔNG dùng output Turn 3, 4     ❌ Redundant

Turn 3 và 4: output không được reference trong 3 turns tiếp theo → REDUNDANT

redundant_call = 2/5 = 0.40 (ví dụ xấu)
```

**Cách tính:** Với mỗi tool call, kiểm tra output có được agent sử dụng trong 3 turns tiếp theo không. Nếu không → redundant. Tỷ lệ = redundant / tổng calls.

**Tại sao quan trọng:**
- FULL tools: có thể gọi thừa nhiều hơn (nhiều tool để thử)
- MINIMAL tools: ít gọi thừa nhưng cũng kém hiệu quả hơn

### M1.3 utilization_breadth = 0.75 (75%)

**"Agent dùng bao nhiêu % tools có sẵn?"**

```
Config FULL có 12 tools:
  bash, python, read, write, edit, glob, grep, find, 
  git_diff, git_log, git_show, test_runner

Agent thực tế dùng: bash, read, edit, grep, git_diff, 
                     find, test_runner, python, glob = 9 tools

utilization_breadth = 9/12 = 0.75
```

**Cách tính:** unique_tools_used / total_tools_available, trung bình trên 150 tasks.

**Tại sao quan trọng:**
- Breadth cao = agent tận dụng đa dạng tools → tool design tốt
- Breadth thấp = có tools nhưng agent không dùng → tool design có vấn đề

---

## 3. Dimension 2: Context Utilization (M2.1, M2.2)

**Đo agent giữ và dùng thông tin tốt hay dở** khi context bị cắt/nén.

### M2.1 info_retention_score = 0.88 (88%)

**"Khi context bị nén, agent còn nhớ bao nhiêu % thông tin quan trọng?"**

```
So sánh 2 strategy cho CÙNG 1 task:

Agent với FULL context (giữ hết):
  Turn 10 response: "File src/utils.py dòng 42 có bug, 
                     function process() thiếu check None,
                     liên quan đến import ở dòng 3..."

Agent với SUMMARY context (chỉ giữ 3 obs cuối):
  Turn 10 response: "File src/utils.py có bug,
                     function process() cần fix..."
                     (quên dòng 42, quên import)

So sánh bằng BERTScore / cosine similarity:
info_retention = similarity(full_response, summary_response) = 0.88
```

**Cách tính:** So sánh responses của agent dùng FULL context vs compressed context. Dùng BERTScore hoặc cosine similarity. Càng giống = compression giữ được nhiều info.

**Giá trị mong đợi:**
- FULL context: ~0.95-1.0 (gần perfect — baseline so sánh)
- SLIDING WINDOW: ~0.85-0.90 (mất ít)
- SUMMARY: ~0.60-0.75 (mất nhiều)

### M2.2 effective_token_ratio = 0.62 (62%)

**"Bao nhiêu % tokens gửi cho LLM thực sự hữu ích?"**

```
Context gửi cho LLM ở Turn 10:
  - System prompt: 500 tokens      → USEFUL ✅
  - Instance template: 200 tokens  → USEFUL ✅
  - Turn 1-3 observations: 3,000t  → ĐÃ CŨ, ít hữu ích ❌
  - Turn 4 grep output: 2,000t     → CHỈ CẦN 200 tokens ⚠️
  - Turn 5-9 observations: 4,000t  → USEFUL ✅
  - Turn 10 prompt: 300 tokens     → USEFUL ✅

Total: 10,000 tokens
Useful: ~6,200 tokens

effective_token_ratio = 6,200 / 10,000 = 0.62
```

**Cách tính:** Dùng LLM classifier hoặc heuristic đánh giá mỗi phần context có "relevant" cho turn hiện tại không. Tỷ lệ = relevant tokens / total tokens.

**Giá trị mong đợi:**
- FULL context: ~0.40-0.60 (giữ hết nhưng NHIỀU RÁC)
- SLIDING WINDOW: ~0.60-0.75 (cắt bớt cũ)
- SUMMARY: ~0.75-0.90 (nén mạnh, ÍT RÁC)

**Trade-off quan trọng:**

```
               M2.1 (info giữ lại)    M2.2 (token efficiency)
FULL           ████████████ 0.95       ████░░░░░░░ 0.45         Giữ hết nhưng lãng phí
SLIDING        ████████░░░░ 0.85       ███████░░░░ 0.70         Cân bằng
SUMMARY        ██████░░░░░░ 0.60       █████████░░ 0.85         Hiệu quả nhưng mất info
```

---

## 4. Dimension 3: Backend Portability (M3.1, M3.2)

**Đo harness config hoạt động ổn định cross-backend hay không.** Tính từ resolve_rates của 3 backends.

### M3.1 cross_backend_stddev = 0.05

**"Resolve rate dao động bao nhiêu khi thay LLM?"**

```
Config full_sliding_window chạy trên 3 backends:
  - Claude:   resolve_rate = 32%
  - GPT-4o:   resolve_rate = 28%
  - DeepSeek: resolve_rate = 22%

Mean = (32 + 28 + 22) / 3 = 27.3%

StdDev = sqrt(((32-27.3)² + (28-27.3)² + (22-27.3)²) / 3)
       = sqrt((22.09 + 0.49 + 28.09) / 3)
       = sqrt(16.89)
       = 4.11%
       ≈ 0.05 (normalized to 0-1 scale)
```

**Ý nghĩa:**
- StdDev **thấp** (~0.02-0.05) = harness ổn định dù thay LLM → **PORTABLE** ✅
- StdDev **cao** (~0.10-0.20) = harness phụ thuộc LLM cụ thể → **FRAGILE** ❌

### M3.2 min_max_ratio = 0.85

**"Backend yếu nhất đạt bao nhiêu % so với backend mạnh nhất?"**

```
Ví dụ harness tốt (portable):
  - Claude:   32%
  - GPT-4o:   30%
  - DeepSeek: 27%
  min_max_ratio = 27/32 = 0.84 ≈ 0.85  → Các backend gần nhau ✅

Ví dụ harness tệ (fragile):
  - Claude:   35%
  - GPT-4o:   25%
  - DeepSeek: 10%
  min_max_ratio = 10/35 = 0.29          → Gap rất lớn ❌
```

**Ý nghĩa:**
- Ratio **cao** (~0.85-1.0) = backend yếu vẫn gần bằng mạnh → harness portable
- Ratio **thấp** (~0.30-0.60) = chênh lệch lớn → harness phụ thuộc model

**Giả thuyết H4:** FULL tools + FULL context → ratio cao (harness tốt giảm sự phụ thuộc vào model).

---

## 5. Cost & avg_turns

### cost = $52.50

```
150 tasks × $0.35/eval (Claude) = $52.50 cho 1 condition

Tổng 27 conditions (với repeats):
- 10 critical × 3 runs = 30 runs
- 17 other × 1 run = 17 runs
- Tổng: 47 runs × 150 tasks × ~$0.27 avg/eval ≈ $1,900
```

### avg_turns = 12.3

```
Trung bình agent mất 12.3 bước (think → act → observe) để hoàn thành 1 task.

Task dễ:              5-8 turns
Task trung bình:      10-15 turns
Task khó:             20-30 turns
Timeout / give up:    250 turns (max call_limit)
```

**Lưu ý:** Turns nhiều ≠ tốt hơn. Có thể agent đang "lạc" hoặc gọi tools thừa.

Mong đợi:
- FULL config: ~10-15 turns (hiệu quả, tools tốt)
- MINIMAL config: ~15-25 turns (phải thử nhiều hơn, ít tools)

---

## 6. ANOVA — Giải thích chi tiết

### Input cho ANOVA

```
Bảng dữ liệu (mỗi row = 1 task × 1 condition):

task_id              | tool    | context | backend  | resolved | M1.1 | M2.1 | ...
─────────────────────┼─────────┼─────────┼──────────┼──────────┼──────┼──────┤
django__django-11099 | full    | full    | claude   | 1        | 0.90 | 0.95 |
django__django-11099 | full    | full    | gpt      | 1        | 0.85 | 0.93 |
django__django-11099 | full    | full    | deepseek | 0        | 0.82 | 0.90 |
django__django-11099 | full    | sliding | claude   | 1        | 0.88 | 0.82 |
...
astropy__astropy-6938| minimal | summary | deepseek | 0        | 0.40 | 0.55 |

Tổng: 150 tasks × 27 conditions = 4,050 rows (+ repeats cho critical conditions)
```

### ANOVA tính gì?

**Phân tách TỔNG variance thành các nguồn:**

```
Total variance trong resolve_rate
    = Variance do Tool Dispatch (D1)
    + Variance do Context Strategy (D2)
    + Variance do LLM Backend (D3)
    + Variance do D1 × D2 interaction
    + Variance do D1 × D3 interaction
    + Variance do D2 × D3 interaction
    + Residual (noise)

η² (eta-squared) = Variance_source / Total_variance × 100%
```

### Đọc bảng ANOVA

```
┌──────────────────────┬───────────┬─────────┬──────────────────────────────┐
│ Source               │ η² (%)    │ p-value │ Giải thích                    │
├──────────────────────┼───────────┼─────────┼──────────────────────────────┤
│ Tool Dispatch (D1)   │ ~30%      │ <0.001  │ Thay tools giải thích 30%    │
│                      │           │         │ sự khác biệt resolve_rate    │
│                      │           │         │ → YẾU TỐ QUAN TRỌNG NHẤT    │
├──────────────────────┼───────────┼─────────┼──────────────────────────────┤
│ Context Strategy (D2)│ ~15%      │ <0.01   │ Thay context giải thích 15%  │
│                      │           │         │ → Quan trọng nhưng ít hơn D1 │
├──────────────────────┼───────────┼─────────┼──────────────────────────────┤
│ LLM Backend (D3)     │ ~20%      │ <0.001  │ Thay model giải thích 20%    │
│                      │           │         │ → Model vẫn quan trọng       │
├──────────────────────┼───────────┼─────────┼──────────────────────────────┤
│ D1 × D2 interaction  │ ~8%       │ <0.05   │ MINIMAL tools + SUMMARY      │
│                      │           │         │ context → tệ hơn expected    │
│                      │           │         │ (interaction khuếch đại)     │
├──────────────────────┼───────────┼─────────┼──────────────────────────────┤
│ Harness × Backend    │ ~7%       │ <0.05   │ Harness tốt (FULL) → các    │
│                      │           │         │ backends gần nhau hơn        │
│                      │           │         │ Harness tệ → gap lớn hơn    │
├──────────────────────┼───────────┼─────────┼──────────────────────────────┤
│ Residual             │ ~20%      │         │ Noise: task difficulty,      │
│                      │           │         │ randomness, etc.             │
└──────────────────────┴───────────┴─────────┴──────────────────────────────┘
```

### η² (eta-squared) đọc thế nào?

```
η² = 0.01 (1%)   → Effect nhỏ      (gần như không ảnh hưởng)
η² = 0.06 (6%)   → Effect trung bình
η² = 0.14 (14%)  → Effect lớn
η² = 0.30 (30%)  → Effect rất lớn   ← Tool Dispatch mong đợi ở đây
```

### p-value đọc thế nào?

```
p < 0.001  → Cực kỳ có ý nghĩa (99.9% không phải do ngẫu nhiên)
p < 0.01   → Rất có ý nghĩa
p < 0.05   → Có ý nghĩa (ngưỡng thông thường)
p > 0.05   → Không có ý nghĩa thống kê

Bonferroni correction: vì test 7 metrics, ngưỡng thực = 0.05/7 = 0.007
```

### Cohen's d (effect size giữa 2 nhóm)

```
Ví dụ so sánh FULL tools vs MINIMAL tools:

FULL tools:    resolve_rates = [35%, 30%, 25%, 32%, 28%, ...]
MINIMAL tools: resolve_rates = [12%, 10%, 8%, 11%, 9%, ...]

Cohen's d = (mean_FULL - mean_MINIMAL) / pooled_std
          = (30% - 10%) / 8%
          = 2.5

d = 0.2  → Effect nhỏ
d = 0.5  → Effect trung bình
d = 0.8  → Effect lớn
d = 2.5  → Effect CỰC LỚN ← mong đợi cho tool ablation
```

### Tukey HSD (so sánh cặp)

```
Sau ANOVA biết "Tool Dispatch có ảnh hưởng", Tukey HSD cho biết CẶP NÀO khác nhau:

FULL vs MEDIUM:    diff = +8%, p = 0.003  → Có ý nghĩa ★
FULL vs MINIMAL:   diff = +20%, p < 0.001 → Cực kỳ có ý nghĩa ★★★
MEDIUM vs MINIMAL: diff = +12%, p < 0.001 → Cực kỳ có ý nghĩa ★★★

→ "Cả 3 mức tool đều khác nhau có ý nghĩa thống kê.
    Giảm từ FULL→MINIMAL tệ hơn 20 điểm %."
```

---

## 7. Ví dụ cụ thể: So sánh 2 conditions

```
Condition A: full_full_claude (baseline — mọi thứ tốt nhất)
  resolve_rate = 35%
  M1.1 = 0.85, M1.2 = 0.12, M1.3 = 0.75
  M2.1 = 0.95, M2.2 = 0.45
  cost = $52.50, turns = 11.5

Condition B: minimal_summary_claude (ablation — bỏ hết)
  resolve_rate = 12%
  M1.1 = 0.45, M1.2 = 0.35, M1.3 = 0.60
  M2.1 = 0.55, M2.2 = 0.85
  cost = $35.00, turns = 18.2
```

### So sánh chi tiết

| Metric | A (full) | B (minimal) | Delta | Nhận xét |
|--------|----------|-------------|-------|----------|
| resolve | 35% | 12% | **-23%** | Harness ảnh hưởng cực lớn |
| M1.1 correct | 0.85 | 0.45 | -0.40 | Chọn sai tool nhiều hơn khi ít tool |
| M1.2 redundant | 0.12 | 0.35 | +0.23 | Gọi thừa 3x (phải thử nhiều) |
| M1.3 breadth | 0.75 | 0.60 | -0.15 | Dùng ít tool hơn (vì có ít hơn) |
| M2.1 retention | 0.95 | 0.55 | -0.40 | Summary mất 40% thông tin |
| M2.2 efficiency | 0.45 | 0.85 | +0.40 | Token efficiency cao hơn (ít rác) |
| cost | $52.50 | $35.00 | -$17.50 | Rẻ hơn 33% (ít tokens gửi LLM) |
| turns | 11.5 | 18.2 | +6.7 | Mất 58% thêm bước (thiếu tools+info) |

### Kết luận từ so sánh

> "Giảm tools từ 12→5 + nén context từ 200K→2K → resolve rate giảm 23 điểm % (35%→12%).
> Agent phải thử nhiều hơn (turns +58%), chọn sai tool nhiều hơn (M1.1 -47%),
> nhưng rẻ hơn 33%. Trade-off rõ ràng giữa performance và cost."

---

## 8. 4 Giả thuyết nghiên cứu & cách kiểm chứng

### H1: Tool system có effect size lớn nhất

```
Kiểm chứng: Cohen's d > 0.5 cho FULL vs MINIMAL (cố định context + backend)
Mong đợi:   d ≈ 1.5-2.5 (rất lớn)
Ý nghĩa:    "Bộ tools là yếu tố quan trọng nhất quyết định resolve rate"
```

### H2: Context management có effect trung bình

```
Kiểm chứng: Cohen's d = 0.3-0.5 cho FULL vs SUMMARY (cố định tools + backend)
Mong đợi:   d ≈ 0.4-0.8
Ý nghĩa:    "Context quan trọng nhưng không bằng tools"
```

### H3: Harness giải thích ≥20% variance

```
Kiểm chứng: η²(D1) + η²(D2) ≥ 0.20 trong ANOVA
Mong đợi:   η²(D1) + η²(D2) ≈ 0.35-0.50
Ý nghĩa:    "Harness (tools + context) giải thích ≥20% kết quả, 
             độc lập với việc dùng LLM nào"
```

### H4: Backend variance giảm khi harness tốt hơn

```
Kiểm chứng: Interaction effect (Harness × Backend) có ý nghĩa (p < 0.05)
Mong đợi:   Với FULL harness: cross_backend_stddev thấp
             Với MINIMAL harness: cross_backend_stddev cao
Ý nghĩa:    "Harness tốt giảm sự phụ thuộc vào model cụ thể"
```

---

## 9. Tóm tắt: Mỗi metric trả lời câu hỏi gì?

| Metric | Câu hỏi | Đo từ đâu |
|--------|---------|-----------|
| **resolve_rate** | Agent fix bug giỏi cỡ nào? | SWE-bench eval |
| **M1.1** | Agent chọn đúng tool không? | .traj files |
| **M1.2** | Agent gọi tool thừa không? | .traj files |
| **M1.3** | Agent tận dụng hết tools không? | .traj files |
| **M2.1** | Nén context mất bao nhiêu info? | So sánh FULL vs compressed |
| **M2.2** | Bao nhiêu % tokens hữu ích? | Phân tích context content |
| **M3.1** | Thay LLM thì kết quả dao động? | Cross-backend comparison |
| **M3.2** | Backend yếu nhất tệ hơn bao nhiêu? | Min/Max resolve rates |
| **ANOVA η²** | Yếu tố nào quan trọng nhất? | Phân tách variance |
| **Cohen's d** | Sự khác biệt lớn cỡ nào? | So sánh cặp conditions |
| **Tukey HSD** | Cặp nào khác nhau có ý nghĩa? | Post-hoc pairwise test |
