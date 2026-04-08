# SWE-bench: Cấu hình và cách hoạt động

## SWE-bench là gì?

SWE-bench là **benchmark đánh giá AI coding agent** do Princeton NLP tạo ra (ICLR 2024 Oral). Gồm **issues thật từ GitHub repos thật** — agent phải tự fix bug, rồi chạy test suite thật để kiểm tra.

> Không phải bài tập toy — đây là bugs thật từ Django, Flask, scikit-learn...

---

## Dataset

### 3 variants

| Variant | Số tasks (test) | Mô tả |
|---------|-----------------|--------|
| **SWE-bench Full** | 2,290 | Toàn bộ, 12 Python repos |
| **SWE-bench Lite** | 300 | Subset nhỏ, chạy nhanh |
| **SWE-bench Verified** | 500 | Human-validated, có difficulty level |

> **HarnessEval dùng SWE-bench Verified** — chọn 150/500 tasks.

### 12 Python repos trong dataset

Django, Flask, scikit-learn, SymPy, Matplotlib, Astropy, Sphinx, requests, pydicom, sqlfluff, marshmallow, pvlib-python

### Splits

- **Full**: train (19,000) / dev (225) / test (2,290)
- **Lite**: dev (23) / test (300)
- **Verified**: test only (500)

---

## Cấu trúc 1 instance (1 task)

```json
{
  "instance_id": "django__django-11099",
  "repo": "django/django",
  "base_commit": "abc123def456...",
  "problem_statement": "Issue title + body text mô tả bug...",
  "hints_text": "Comments trên issue trước khi có PR fix...",
  "patch": "diff --git a/django/db/...",
  "test_patch": "diff --git a/tests/...",
  "FAIL_TO_PASS": "[\"test_foo\", \"test_bar\"]",
  "PASS_TO_PASS": "[\"test_baz\", \"test_qux\"]",
  "version": "3.2",
  "created_at": "2023-01-15T10:30:00Z",
  "environment_setup_commit": "def789...",
  "difficulty": "medium"
}
```

### Giải thích các fields

| Field | Ý nghĩa |
|-------|---------|
| `instance_id` | ID duy nhất: `{owner}__{repo}-{issue_number}` |
| `repo` | GitHub repo path (e.g., `django/django`) |
| `base_commit` | Commit SHA **trước** khi fix — agent bắt đầu từ đây |
| `problem_statement` | Nội dung GitHub issue (title + body) — input cho agent |
| `hints_text` | Comments trên issue trước PR (có thể rỗng) |
| `patch` | **Gold patch** — đáp án đúng (diff), KHÔNG bao gồm test files |
| `test_patch` | Test changes từ solution PR — dùng để verify |
| `FAIL_TO_PASS` | Tests phải FAIL trước fix, PASS sau fix → chứng minh fix đúng |
| `PASS_TO_PASS` | Tests phải PASS cả trước và sau fix → không regression |
| `version` | Version của repo dùng để setup environment |
| `difficulty` | Độ khó (chỉ có trong Verified): 4 levels |

### Load data bằng Python

```python
from datasets import load_dataset

# 3 cách load
full = load_dataset('princeton-nlp/SWE-bench', split='test')           # 2,290
lite = load_dataset('princeton-nlp/SWE-bench_Lite', split='test')      # 300
verified = load_dataset('princeton-nlp/SWE-bench_Verified', split='test')  # 500

# Xem 1 instance
print(verified[0]['instance_id'])         # django__django-11099
print(verified[0]['problem_statement'])   # Issue content...
print(verified[0]['FAIL_TO_PASS'])        # ["test_foo"]
```

---

## Cài đặt SWE-bench

### Yêu cầu

- Python 3.8+
- Docker (x86_64 recommended)
- 120GB free disk
- 16GB RAM
- 8+ CPU cores

### Cài đặt

```bash
git clone https://github.com/princeton-nlp/SWE-bench.git
cd SWE-bench
pip install -e .
```

### Verify cài đặt

```bash
python -m swebench.harness.run_evaluation \
  --predictions_path gold \
  --max_workers 1 \
  --instance_ids sympy__sympy-20590 \
  --run_id validate-gold
```

---

## Repo structure

```
SWE-bench/
├── swebench/
│   ├── harness/                    # ★ Core evaluation engine
│   │   ├── run_evaluation.py       # Entry point chính
│   │   ├── grading.py              # Chấm điểm: FULL/PARTIAL/NO
│   │   ├── docker_build.py         # Build Docker images
│   │   ├── docker_utils.py         # Docker API utilities
│   │   ├── prepare_images.py       # Pre-build optimization
│   │   ├── reporting.py            # Tổng hợp kết quả
│   │   ├── constants/              # Config constants
│   │   ├── dockerfiles/            # Dockerfile templates
│   │   ├── log_parsers/            # Parse test output
│   │   ├── modal_eval/             # Modal cloud integration
│   │   └── test_spec/              # Test specifications
│   ├── inference/                  # Model inference + dataset creation
│   └── collect/                    # Thu thập data từ GitHub
├── tests/
├── docs/
├── pyproject.toml
└── README.md
```

---

## Pipeline evaluation (Docker-based)

### Tổng quan luồng

```
predictions.jsonl (patches từ agent)
        │
        ▼
┌──────────────────────┐
│ 1. Load predictions   │  Match instance_id với dataset
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ 2. Build Docker images│  3 cache levels:
│                       │  - base: OS + Python
│                       │  - env: base + repo + deps (recommended)
│                       │  - instance: env + test patch
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ 3. Apply patch        │  3 fallback strategies:
│                       │  1. git apply --verbose
│                       │  2. git apply --verbose --reject
│                       │  3. patch --batch --fuzz=5 -p1
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ 4. Run test suite     │  Chạy tests THẬT của repo
│                       │  trong Docker container
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ 5. Grading            │
│                       │
│  FAIL_TO_PASS ratio   │  = (F2P tests now PASS) / (total F2P)
│  PASS_TO_PASS ratio   │  = (P2P tests still PASS) / (total P2P)
│                       │
│  FULL    = cả 2 = 1.0 │  ← "Resolved" ✅
│  PARTIAL = F2P < 1.0  │  ← Fix một phần
│  NO      = còn lại    │  ← Fail ❌
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ 6. Report             │
│  results.json         │  resolve_rate = FULL / total
│  instance_results.jsonl│  Chi tiết từng task
└──────────────────────┘
```

### Tiêu chí đánh giá

> **Resolved** = TẤT CẢ `FAIL_TO_PASS` tests giờ PASS **VÀ** TẤT CẢ `PASS_TO_PASS` tests vẫn PASS

- Không có partial credit
- Fix 9/10 tests = vẫn **FAIL**
- 1 regression = **FAIL**

---

## Chạy evaluation

### Command chính

```bash
python -m swebench.harness.run_evaluation \
  --dataset_name princeton-nlp/SWE-bench_Verified \
  --split test \
  --predictions_path predictions.jsonl \
  --max_workers 4 \
  --timeout 1800 \
  --run_id my_experiment \
  --cache_level env
```

### Options

| Option | Default | Mô tả |
|--------|---------|--------|
| `--dataset_name` | `SWE-bench_Lite` | HuggingFace dataset ID |
| `--split` | `test` | Dataset split |
| `--predictions_path` | (required) | Path tới JSONL, hoặc `gold` để validate |
| `--max_workers` | 4 | Số Docker containers song song |
| `--timeout` | 1800 | Timeout/instance (30 phút) |
| `--run_id` | (required) | Tên experiment |
| `--cache_level` | `env` | Docker cache: none/base/env/instance |
| `--instance_ids` | all | Chọn specific instances |
| `--force_rebuild` | false | Force rebuild Docker images |
| `--clean` | false | Xóa images sau evaluation |
| `--namespace` | `swebench` | Docker image namespace |
| `--modal` | false | Chạy trên Modal cloud |

### Format predictions file (JSONL)

```jsonl
{"instance_id": "django__django-11099", "model_name_or_path": "my-agent", "model_patch": "diff --git a/django/db/models/query.py b/django/db/models/query.py\n..."}
{"instance_id": "astropy__astropy-12907", "model_name_or_path": "my-agent", "model_patch": "diff --git a/astropy/units/core.py b/astropy/units/core.py\n..."}
```

Mỗi dòng = 1 prediction cho 1 instance. Chỉ cần 3 fields: `instance_id`, `model_name_or_path`, `model_patch`.

### Output structure

```
evaluation_results/<run_id>/
├── results.json                    # Tổng hợp: resolve_rate, counts
├── instance_results.jsonl          # Chi tiết từng instance
└── logs/
    ├── django__django-11099/
    │   ├── test_output.txt         # Raw test output
    │   ├── patch_apply.txt         # Patch application log
    │   └── eval_report.json        # Grading result
    └── ...
```

---

## Cloud evaluation options

### Option A: sb-cli (AWS-based, chính thức)

```bash
pip install sb-cli
sb-cli gen-api-key your.email@example.com
export SWEBENCH_API_KEY=your_api_key

# Submit evaluation
sb-cli submit swe-bench_verified test \
  --predictions_path predictions.json \
  --run_id my_run_id

# Get results (~1 phút)
sb-cli get-report swe-bench_verified test my_run_id -o ./reports

# Check quota
sb-cli quota swe-bench_verified test
```

### Option B: Modal (cloud Docker)

```bash
pip install modal swebench[modal]
modal setup

python -m swebench.harness.run_evaluation \
  --modal true \
  --predictions_path preds.jsonl \
  --run_id cloud-eval
```

---

## SWE-Agent kết nối SWE-bench thế nào?

```
SWE-bench (dataset)          SWE-Agent (agent)           SWE-bench (evaluator)
┌──────────────┐      ┌──────────────────────┐      ┌──────────────────┐
│ instance_id   │      │                      │      │                  │
│ repo          │─────>│ 1. Checkout repo     │      │                  │
│ base_commit   │      │    @base_commit      │      │                  │
│ problem_stmt  │      │ 2. Read issue        │      │                  │
│               │      │ 3. Agent loop:       │      │                  │
│               │      │    think→act→observe │      │                  │
│               │      │ 4. Generate patch    │      │                  │
│               │      │ 5. Submit            │─────>│ Apply patch      │
│               │      │                      │      │ Run tests        │
│ FAIL_TO_PASS  │      └──────────────────────┘      │ Grade: FULL/NO   │
│ PASS_TO_PASS  │─────────────────────────────────────>│ Report results  │
│ test_patch    │                                     │                  │
└──────────────┘                                     └──────────────────┘
```

### Bước 1: SWE-Agent load tasks

```bash
sweagent run-batch \
  --instances.type swe_bench \
  --instances.subset verified \
  --instances.split test \
  --instances.slice :150
```

SWE-Agent nhận: `instance_id`, `repo`, `base_commit`, `problem_statement`
SWE-Agent KHÔNG nhận: `patch` (đáp án), `test_patch`, `FAIL_TO_PASS`

### Bước 2: Agent chạy trên mỗi task

```
Với mỗi instance:
  1. Docker container: checkout repo@base_commit
  2. Agent đọc problem_statement (issue)
  3. Agent loop: explore → reproduce → edit → test → submit
  4. Output: git diff (patch)
```

### Bước 3: Thu thập predictions

```
Output: trajectories/.../preds.json
Format: {instance_id → model_patch}
```

### Bước 4: Evaluate

```bash
python -m swebench.harness.run_evaluation \
  --predictions_path preds.json \
  --dataset_name princeton-nlp/SWE-bench_Verified \
  --run_id harness_eval_experiment
```

---

## Trong HarnessEval dùng SWE-bench thế nào?

### Cấu hình

- **Dataset**: SWE-bench Verified (500 tasks, human-validated)
- **Subset**: 150 tasks (chọn đa dạng repos + difficulty levels)
- **Metric chính**: resolve_rate = số tasks FULL / tổng tasks

### Workflow cho 1 condition

```bash
# 1. SWE-Agent chạy với config cụ thể
sweagent run-batch \
  --config config/harness_eval/base.yaml \
  --config config/harness_eval/tool_full.yaml \
  --config config/harness_eval/ctx_sliding_window.yaml \
  --config config/harness_eval/be_claude.yaml \
  --instances.type swe_bench \
  --instances.subset verified \
  --instances.slice :150 \
  --output_dir trajectories/harness_eval/full_sliding_window_claude/

# 2. Evaluate predictions
python -m swebench.harness.run_evaluation \
  --predictions_path trajectories/.../preds.json \
  --run_id full_sliding_window_claude

# 3. Thu thập resolve_rate → đưa vào ANOVA
```

### Toàn bộ thí nghiệm

```
27 conditions × 150 tasks = 4,050 agent runs
+ 10 critical conditions × 2 extra runs × 150 = 3,000 runs nữa
= Tổng 7,050 evaluations

Mỗi evaluation:
  - SWE-Agent chạy (tốn API $) → generate patch
  - SWE-bench evaluate (tốn Docker time) → resolve/no
```

---

## Chi phí & Thời gian ước tính

### Docker image storage

| Dataset | Số images | Dung lượng |
|---------|-----------|-----------|
| Full (2,290) | ~2,290 | ~67 GiB (optimized) |
| Verified (500) | ~500 | ~30 GiB |
| 150 tasks subset | ~150 | ~10 GiB |

### Evaluation runtime (chỉ tính chạy tests, không tính inference)

| Setup | Thời gian/instance | 150 tasks |
|-------|-------------------|-----------|
| Optimized (32 cores) | ~8 giây | ~20 phút |
| Unoptimized | ~10 phút | ~25 giờ |

### Inference costs (tạo patches)

Xem chi tiết trong `harness_eval/configs/backend_config.py`:
- Claude: ~$0.35/eval × 150 = ~$52.50/condition
- GPT-4o: ~$0.30/eval × 150 = ~$45/condition
- DeepSeek: ~$0.15/eval × 150 = ~$22.50/condition

### Leaderboard (tham khảo, tính đến 2025)

| Agent | SWE-bench Verified |
|-------|-------------------|
| Claude 4.5 Opus | 76.8% |
| Gemini 3 Flash | 75.8% |
| SWE-Agent + GPT-4o | ~33% |
| SWE-Agent + Claude Sonnet | ~40% |

---

## Retrieval-Augmented variants (tham khảo)

Cho agents không navigate được full repo, SWE-bench cung cấp pre-computed context:

| Variant | Context size |
|---------|-------------|
| `SWE-bench_Lite_oracle` | Exact relevant files |
| `SWE-bench_Lite_bm25_13K` | BM25 retrieval, 13K tokens |
| `SWE-bench_Lite_bm25_27K` | BM25 retrieval, 27K tokens |
| `SWE-bench_Lite_bm25_40K` | BM25 retrieval, 40K tokens |

> HarnessEval **KHÔNG dùng** retrieval variants — agent tự navigate repo.

---

## Tóm tắt

| Câu hỏi | Trả lời |
|----------|---------|
| SWE-bench là gì? | Benchmark đánh giá AI coding agent trên issues thật |
| Dùng variant nào? | **SWE-bench Verified** (500 tasks, human-validated) |
| Tiêu chí pass? | ALL FAIL_TO_PASS → PASS **VÀ** ALL PASS_TO_PASS vẫn PASS |
| Evaluate bằng gì? | Docker containers chạy test suite thật |
| HarnessEval dùng bao nhiêu tasks? | **150 tasks** (subset từ 500) |
| Metric chính? | **resolve_rate** = FULL / total |
| Agent output gì? | predictions.jsonl (instance_id + git diff patch) |
