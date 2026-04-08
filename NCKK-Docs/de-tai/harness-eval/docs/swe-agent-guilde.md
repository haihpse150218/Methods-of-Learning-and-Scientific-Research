# Cách hoạt động của SWE-Agent trong HarnessEval

## SWE-Agent là gì?

SWE-Agent là một **coding agent** của Princeton — nó nhận một GitHub issue, rồi tự động đọc code, chỉnh sửa, chạy test để fix bug. Trong HarnessEval, chúng ta **fork SWE-Agent** để biến nó thành nền tảng thí nghiệm ablation.

---

## Kiến trúc 3 lớp (có thể tháo rời)

```
┌─────────────────────────────────────────────┐
│              SWE-Agent Runner                │
│                                             │
│  ┌───────────┐ ┌──────────┐ ┌────────────┐ │
│  │ D1: Tools  │ │D2: Context│ │D3: Backend │ │
│  │            │ │           │ │            │ │
│  │ FULL (12)  │ │ FULL      │ │ Claude     │ │
│  │ MEDIUM (8) │ │ SLIDING   │ │ GPT-4o     │ │
│  │ MINIMAL (5)│ │ SUMMARY   │ │ DeepSeek   │ │
│  └───────────┘ └──────────┘ └────────────┘ │
└─────────────────────────────────────────────┘
```

Mỗi lớp là **1 file YAML riêng**, ghép lại bằng `--config`:

```bash
python -m sweagent run \
  --config base.yaml \                  # Cấu hình chung
  --config tool_full.yaml \             # D1: 12 tools
  --config ctx_sliding_window.yaml \    # D2: giữ 50K token
  --config be_claude.yaml               # D3: Claude Sonnet 4
```

---

## D1: Tool Dispatch (3 mức)

| Mức | Số tools | Gồm | Parse mode |
|-----|----------|------|------------|
| **FULL** | 12 | bash, python, read, write, edit, glob, grep, find, git_diff, git_log, git_show, test_runner | function_calling |
| **MEDIUM** | 8 | bash, python, read, write, edit, grep, git_diff, test_runner | function_calling |
| **MINIMAL** | 5 | bash, read(cat), write(echo), edit(sed), grep | single_bash_block |

MINIMAL buộc agent chỉ dùng bash thuần — mô phỏng "con người gõ terminal".

### Nguyên tắc thiết kế
- Các mức **lồng nhau**: MINIMAL ⊂ MEDIUM ⊂ FULL
- Giảm dần tool = ablation có kiểm soát, không gây confound

---

## D2: Context Management (3 chiến lược)

| Chiến lược | Token giữ lại | Cách hoạt động |
|------------|---------------|----------------|
| **FULL** | ~200K (unlimited) | Giữ toàn bộ lịch sử, dùng prompt caching |
| **SLIDING_WINDOW** | ~50K | Giữ 15 observation gần nhất, cũ hơn → "X lines omitted" |
| **SUMMARY** | ~2K | Chỉ giữ 3 observation cuối, xóa output >500 ký tự, xóa diff blocks |

### Chi tiết cấu hình

- **FULL** (`ctx_full.yaml`): Dùng `cache_control` với `last_n_messages=2` (Anthropic prompt caching), không giới hạn token.
- **SLIDING_WINDOW** (`ctx_sliding_window.yaml`): Dùng `last_n_observations` (n=15), `closed_window` processor. Output cũ bị thay bằng summary 1 dòng.
- **SUMMARY** (`ctx_summary.yaml`): Dùng `last_n_observations` (n=3), `remove_regex` (xóa output >500 chars), mô phỏng Adaptive Context Compression (ACC) từ literature.

---

## D3: Backend LLM (3 provider)

| Backend | Model | Chi phí/eval |
|---------|-------|-------------|
| **Claude** | claude-sonnet-4-20250514 | ~$0.35 |
| **GPT** | gpt-4o-2025-03-01 | ~$0.30 |
| **DeepSeek** | deepseek-chat (V3) | ~$0.15 |

- Tất cả đều `temperature=0.0` để giảm randomness
- DeepSeek rẻ nhất (10x so với Claude) → dùng cho non-critical conditions
- Ollama (`qwen2.5:7b`) có sẵn cho test local miễn phí

---

## Quy trình chạy 1 condition

```
GitHub Issue → SWE-Agent đọc issue
    ↓
Agent nhận tools (theo tool_*.yaml)
    ↓
Agent lặp: suy nghĩ → chọn tool → thực thi → nhận output
    ↓
Context manager (theo ctx_*.yaml) quyết định giữ/cắt lịch sử
    ↓
LLM backend (theo be_*.yaml) sinh response
    ↓
Lặp lại đến khi agent submit patch hoặc hết call_limit (250)
    ↓
Output: file .traj (trajectory log)
    ↓
convert_results.py → JSON → Flask UI hiển thị
```

---

## Thiết kế thí nghiệm

### Ma trận 27 conditions (3 × 3 × 3)

```
Tool (3 levels) × Context (3 levels) × Backend (3 levels) = 27 conditions
```

### Phân bổ runs

- **10 critical conditions** → chạy **3 lần** mỗi condition (có thống kê variance)
- **17 remaining conditions** → chạy **1 lần**
- **150 tasks** từ SWE-bench Verified (Python)
- **Tổng: (10×3 + 17×1) × 150 = 7,050 evaluations**

### 10 Critical Conditions

| # | Tool | Context | Backend | Lý do |
|---|------|---------|---------|-------|
| 1 | full | full | claude | Baseline SOTA |
| 2 | full | full | gpt | Baseline cross-backend |
| 3 | full | full | deepseek | Baseline budget |
| 4 | minimal | full | claude | Max tool ablation |
| 5 | minimal | full | gpt | Max tool ablation cross-backend |
| 6 | full | summary | claude | Max context ablation |
| 7 | full | summary | gpt | Max context ablation cross-backend |
| 8 | minimal | summary | claude | Double ablation |
| 9 | minimal | summary | gpt | Double ablation cross-backend |
| 10 | minimal | summary | deepseek | Worst case scenario |

### Pilot Study (chạy trước)

- **5 conditions × 20 tasks × 2 runs = 200 evals** (~$80)
- Mục đích: validate metrics, estimate costs, debug pipeline
- Nếu OK → chạy full 7,050 evals

---

## Kiểm chứng Equivalence

Trước khi ablation, chạy `verify_equivalence.yaml`:
- **50 tasks** từ SWE-Bench Verified
- Config: Full tools + Full context + GPT-4o
- **Tiêu chí**: resolve_rate chênh ≤ ±3% so với SWE-Agent gốc
- Nếu delta > 3% → **DỪNG**, debug trước, KHÔNG chạy ablation

---

## Python Toolkit kết nối thế nào?

```
harness_eval/
├── harness/
│   ├── interfaces.py    → Abstract classes (ToolProvider, ContextProvider, BackendProvider)
│   └── factory.py       → Tạo 27 HarnessConfig, sinh lệnh `sweagent run`
├── configs/
│   ├── tool_config.py      → ToolLevel enum + danh sách tools mỗi mức
│   ├── context_config.py   → ContextStrategy enum + window size
│   ├── backend_config.py   → BackendType enum + model_id + cost
│   └── experiment.py       → 27 conditions, 10 critical, tổng evaluations
├── parsers/
│   └── trajectory.py    → Parse .traj output từ SWE-Agent
├── metrics/
│   ├── tool_dispatch.py       → M1.1 correct_selection, M1.2 redundant_call, M1.3 utilization_breadth
│   ├── context_utilization.py → M2.1 info_retention (BERTScore), M2.2 effective_token_ratio
│   └── backend_portability.py → M3.1 cross_backend_stddev, M3.2 min_max_ratio
├── pipeline/
│   ├── runner.py         → PipelineRunner, dry-run mode, cost tracking
│   └── analysis.py       → ANOVA 2-way, Cohen's d, Tukey HSD
└── cli.py                → CLI: harness-eval info, pilot, run, analyze
```

---

## SWE-Agent Config Files

```
SWE-agent/config/harness_eval/
├── base.yaml                  # Shared: system prompt, template, env vars, limits
├── tool_full.yaml             # 12 tools + filemap + multi-model review
├── tool_medium.yaml           # 8 tools, no filemap
├── tool_minimal.yaml          # 5 tools, bash-only mode
├── ctx_full.yaml              # Unlimited history + cache_control
├── ctx_sliding_window.yaml    # 50K tokens, keep last 15 observations
├── ctx_summary.yaml           # ~2K tokens, aggressive compression
├── be_claude.yaml             # Claude Sonnet 4 ($0.35/eval)
├── be_gpt.yaml                # GPT-4o ($0.30/eval)
├── be_deepseek.yaml           # DeepSeek V3 ($0.15/eval)
├── be_ollama.yaml             # Ollama qwen2.5:7b (free, local)
├── be_ollama_7b.yaml          # Ollama qwen2.5-coder:7b (free, local)
├── verify_equivalence.yaml    # 50-task validation (±3% threshold)
├── run_condition.sh           # Script chạy 1 condition
└── README.md                  # Hướng dẫn sử dụng
```

---

## Ví dụ ghép config

### Baseline (full capability)
```bash
./run_condition.sh full full claude
# → base.yaml + tool_full.yaml + ctx_full.yaml + be_claude.yaml
# → condition_id: "full_full_claude"
# → Expected: SOTA performance, ~$0.35/eval
```

### Context ablation
```bash
./run_condition.sh full summary claude
# → base.yaml + tool_full.yaml + ctx_summary.yaml + be_claude.yaml
# → condition_id: "full_summary_claude"
# → Test: context ảnh hưởng bao nhiêu khi tools đầy đủ?
```

### Worst case (minimal everything + cheapest)
```bash
./run_condition.sh minimal summary deepseek
# → base.yaml + tool_minimal.yaml + ctx_summary.yaml + be_deepseek.yaml
# → condition_id: "minimal_summary_deepseek"
# → Cost: ~$0.15/eval × 150 tasks = ~$22.50
```

### Test local (free)
```bash
./run_condition.sh full full ollama
# → Dùng Ollama local, $0/eval
# → Chỉ để test pipeline, không dùng cho thí nghiệm chính
```

---

## Phân tích thống kê

| Phương pháp | Mục đích |
|-------------|----------|
| **Two-way ANOVA** | Phân tách variance: Harness config (9 levels) × Backend (3 levels) |
| **Cohen's d** | Đo effect size giữa các mức tool/context |
| **Eta-squared (η²)** | % variance giải thích bởi mỗi factor |
| **Tukey HSD** | So sánh cặp (pairwise) post-hoc |
| **Bonferroni** | Hiệu chỉnh multiple comparison |

### Giả thuyết nghiên cứu

- **H1**: Tool system có effect size lớn nhất (Cohen's d > 0.5)
- **H2**: Context management có effect trung bình (d = 0.3-0.5)
- **H3**: Harness giải thích ≥20% variance (η², độc lập với LLM)
- **H4**: Backend variance giảm khi harness tốt hơn (interaction effect)

---

## Tóm tắt

SWE-Agent là **"con chuột thí nghiệm"** trong HarnessEval:
1. **Fork** SWE-Agent gốc → tách thành 3 module độc lập
2. **Ghép YAML** configs để tạo 27 conditions khác nhau
3. **Chạy** trên 150 SWE-bench tasks → thu trajectory logs
4. **Parse** logs → tính 7 metrics trên 3 dimensions
5. **ANOVA** → xác định yếu tố nào (tools/context/backend) ảnh hưởng nhiều nhất

Mục tiêu cuối: chứng minh rằng **chất lượng harness** (không phải LLM) là yếu tố quyết định khả năng fix bug của coding agent.
