# So sánh SWE-Agent gốc vs Fork HarnessEval

## Nguyên tắc chính

> **KHÔNG sửa source code SWE-Agent.** Toàn bộ customization thông qua YAML config composition + toolkit bên ngoài.

Đây là chiến lược có chủ đích:
- Dễ cập nhật khi upstream SWE-Agent release version mới
- Đảm bảo equivalence test (±3% resolve rate) dễ pass
- Tách biệt rõ ràng giữa "hạ tầng agent" và "công cụ đánh giá"

---

## Tổng quan so sánh

```
SWE-Agent gốc (github.com/swe-agent/swe-agent)
├── sweagent/          ← GIỮA NGUYÊN, KHÔNG SỬA
├── tools/             ← GIỮA NGUYÊN, KHÔNG SỬA
├── config/            ← THÊM config/harness_eval/ (13 files mới)
├── (không có)         ← THÊM convert_results.py
├── (không có)         ← THÊM run_test.sh
└── (không có)         ← THÊM harness_eval/ (toolkit riêng, nằm ngoài SWE-agent/)
```

---

## Chi tiết: Những gì KHÔNG thay đổi

### sweagent/ (Source code chính) — KHÔNG SỬA

| Module | File | Chức năng | Status |
|--------|------|-----------|--------|
| Agent loop | `agent/agents.py` | DefaultAgent, RetryAgent | Giữ nguyên |
| Models | `agent/models.py` | LiteLLM interface | Giữ nguyên |
| History | `agent/history_processors.py` | 8 processors | Giữ nguyên |
| Environment | `environment/swe_env.py` | Docker management | Giữ nguyên |
| Tools | `tools/tools.py` | ToolHandler | Giữ nguyên |
| Parsing | `tools/parsing.py` | Action parsers | Giữ nguyên |
| Runner | `run/run_single.py` | Single instance | Giữ nguyên |
| Batch | `run/run_batch.py` | Batch execution | Giữ nguyên |
| Inspector | `inspector/` | Web UI xem trajectory | Giữ nguyên |

**Lý do giữ nguyên:** SWE-Agent đã có sẵn hệ thống config composition (nhiều `--config` files merge lại). Chúng ta chỉ cần viết YAML mới, không cần sửa code.

### tools/ (Tool bundles) — KHÔNG SỬA

| Bundle | Có trong gốc | Dùng trong HarnessEval |
|--------|--------------|----------------------|
| `registry/` | ✅ | ✅ FULL + MEDIUM |
| `edit_anthropic/` | ✅ | ✅ FULL + MEDIUM |
| `filemap/` | ✅ | ✅ Chỉ FULL |
| `review_on_submit_m/` | ✅ | ✅ Chỉ FULL |
| `submit/` | ✅ | ✅ MEDIUM + MINIMAL |
| `bash/` | ✅ (built-in) | ✅ Tất cả |
| `search/` | ✅ | ❌ Không dùng |
| `web_browser/` | ✅ | ❌ Không dùng |
| `image_tools/` | ✅ | ❌ Không dùng |
| `windowed*/` | ✅ | ❌ Không dùng |

**Cách ablation tools:** Không xóa tool bundles mà chỉ thay đổi `bundles:` list trong YAML config.

---

## Chi tiết: Những gì THÊM MỚI

### 1. config/harness_eval/ — 13 YAML files mới

Đây là phần quan trọng nhất, tạo ra 27 conditions thí nghiệm bằng cách **compose** các file config.

#### base.yaml — Config dùng chung cho mọi condition

```yaml
# Những gì set trong base.yaml:
agent:
  templates:
    system_template: "helpful assistant that can interact with a computer..."
    instance_template: "PR description format..."
  tools:
    env_variables:
      PAGER: cat
      TQDM_DISABLE: "1"
      GIT_PAGER: cat
    parse_function: function_calling    # Override bởi tool_minimal.yaml
  model:
    temperature: 0.0                    # Override bởi be_*.yaml
    per_instance_cost_limit: 3.0
    total_cost_limit: 1500
  max_requeries: 3
```

**Tại sao cần:** Đặt các giá trị chung 1 lần, tránh lặp lại trong 27 config files.

#### Tool configs (3 files) — Kiểm soát D1: Tool Dispatch

**tool_full.yaml** — 12 tools (FULL)
```yaml
agent:
  tools:
    bundles:
      - registry          # read, write, edit, grep, find, glob, git_*
      - edit_anthropic     # Anthropic-style string replacement
      - filemap            # Repository overview
      - review_on_submit_m # Multi-model review trước submit
      - bash               # Shell execution
    env_variables:
      USE_FILEMAP: "true"
```

**Tại sao:** Đây là baseline — agent có đầy đủ công cụ giống SWE-Agent default config. Filemap giúp agent hiểu cấu trúc repo, review giúp kiểm tra trước khi submit.

**tool_medium.yaml** — 8 tools (MEDIUM)
```yaml
agent:
  tools:
    bundles:
      - registry
      - edit_anthropic
      - submit             # Thay review_on_submit_m bằng submit đơn giản
      - bash
    env_variables:
      USE_FILEMAP: "false" # Tắt filemap
```

**Tại sao:** Bỏ filemap (agent phải tự navigate) và review (agent không được kiểm tra lại). Giảm 4 tools → đo tác động của "navigation aids" và "self-review".

**tool_minimal.yaml** — 5 tools (MINIMAL)
```yaml
agent:
  tools:
    bundles:
      - submit
      - bash               # Chỉ có bash
    parse_function: single_bash_code_block  # Không dùng function_calling
  templates:
    system_template: "...one bash command at a time..."
```

**Tại sao:** Mô phỏng agent chỉ có terminal thuần — phải dùng `cat` thay `read`, `sed` thay `edit`, `echo >` thay `write`. Parse mode đổi sang `single_bash_code_block` vì không có tool definitions. Đây là mức ablation mạnh nhất cho D1.

#### Context configs (3 files) — Kiểm soát D2: Context Management

**ctx_full.yaml** — Unlimited context
```yaml
agent:
  history_processors:
    - type: cache_control
      last_n_messages: 2
```

**Tại sao:** Chỉ dùng prompt caching (tiết kiệm $), giữ toàn bộ lịch sử. Agent có thể nhớ mọi thứ đã làm. Đây là baseline cho D2.

**ctx_sliding_window.yaml** — ~50K tokens
```yaml
agent:
  history_processors:
    - type: cache_control
      last_n_messages: 2
    - type: last_n_observations
      n: 15
      polling: 1
    - type: closed_window
```

**Tại sao:** Giữ 15 observation gần nhất, cũ hơn thay bằng "X lines omitted". Mô phỏng window size thực tế (~50K tokens). `closed_window` đảm bảo agent không thấy file content cũ đã bị thay đổi.

**ctx_summary.yaml** — ~2K tokens (aggressive)
```yaml
agent:
  history_processors:
    - type: cache_control
      last_n_messages: 2
    - type: last_n_observations
      n: 3
      polling: 1
      always_remove_output_for_tags: [remove_output]
    - type: closed_window
    - type: remove_regex
      keep_last: 3
      # Xóa output >500 ký tự
      # Xóa <diff> blocks
```

**Tại sao:** Mô phỏng Adaptive Context Compression (ACC) — chỉ giữ 3 observations cuối, xóa output dài và diff blocks. Agent buộc phải làm việc với "trí nhớ ngắn hạn" cực kỳ hạn chế. Đây là mức ablation mạnh nhất cho D2.

#### Backend configs (5 files) — Kiểm soát D3: LLM Backend

**be_claude.yaml**
```yaml
agent:
  model:
    name: claude-sonnet-4-20250514
    per_instance_cost_limit: 3.0
```

**be_gpt.yaml**
```yaml
agent:
  model:
    name: gpt-4o-2025-03-01
    per_instance_cost_limit: 3.0
```

**be_deepseek.yaml**
```yaml
agent:
  model:
    name: deepseek-chat
    per_instance_cost_limit: 1.0    # Rẻ hơn → limit thấp hơn
```

**be_ollama.yaml** + **be_ollama_7b.yaml** — Test local miễn phí
```yaml
agent:
  model:
    name: ollama/qwen2.5:7b
    per_instance_cost_limit: 0
    total_cost_limit: 0
```

**Tại sao cần 3+ backends:** Đo backend portability — cùng harness config, thay LLM khác thì kết quả thay đổi bao nhiêu? Nếu harness tốt, kết quả nên ổn định cross-backend.

#### verify_equivalence.yaml — Kiểm chứng fork

```yaml
# Config: Full tools + Full context + GPT-4o
# Dataset: 50 tasks từ SWE-Bench Verified
# Tiêu chí: |resolve_rate_fork - resolve_rate_original| <= 3%
```

**Tại sao:** Trước khi chạy ablation, phải chứng minh fork chạy tương đương SWE-Agent gốc. Nếu chênh >3% → có bug trong config composition → phải fix trước.

#### run_condition.sh — Helper script

```bash
# Usage: ./run_condition.sh <tool> <ctx> <backend> [extra_args]
# Ví dụ: ./run_condition.sh full sliding_window claude

# Script sẽ:
# 1. Validate config files tồn tại
# 2. Compose: base.yaml + tool_*.yaml + ctx_*.yaml + be_*.yaml
# 3. Chạy: python -m sweagent run-batch với composed config
# 4. Output → trajectories/harness_eval/{condition_id}/
```

#### README.md — Tài liệu thiết kế

Giải thích 3×3×3 factorial design, cách compose configs, và ý nghĩa từng level.

---

### 2. convert_results.py — Chuyển đổi trajectory format

**Vị trí:** `SWE-agent/convert_results.py` (52 dòng)

```python
# Input:  trajectories/test_harness/*.traj  (SWE-Agent native format)
# Output: app/trajectories/*.json           (HarnessEval JSON format)

# Dùng: harness_eval.parsers.parse_sweagent_traj()
#        harness_eval.parsers.convert_traj_to_json()

# Trích xuất: condition_id, task_id, resolved, num_turns, cost
```

**Tại sao cần:** SWE-Agent lưu trajectory dạng `.traj` (JSON phức tạp với replay_config, full history). HarnessEval cần format đơn giản hơn để tính metrics và hiển thị trên Flask UI.

---

### 3. run_test.sh — Smoke test 3 conditions

**Vị trí:** `SWE-agent/run_test.sh` (61 dòng)

```bash
# Chạy 3 conditions với Ollama (miễn phí):
# 1. full_full_ollama       — Baseline local
# 2. medium_sliding_window_ollama — Medium ablation
# 3. minimal_summary_ollama — Maximum ablation

# Dùng test repo: github.com/SWE-agent/test-repo (issue #1)
```

**Tại sao cần:** Verify pipeline hoạt động end-to-end trước khi tốn tiền API. Ollama chạy local, $0 cost. Test repo nhỏ, chạy nhanh.

---

### 4. harness_eval/ — Toolkit đánh giá (NẰM NGOÀI SWE-agent/)

Đây là package Python hoàn toàn mới, **không phải phần của SWE-Agent**:

```
harness_eval/                    # 2,579 LOC
├── __init__.py                  # v0.1.0
├── cli.py                       # CLI: harness-eval info/pilot/run/convert/analyze
│
├── configs/                     # Python config classes (mirror YAML configs)
│   ├── tool_config.py           # ToolLevel enum + tool lists
│   ├── context_config.py        # ContextStrategy enum + window sizes
│   ├── backend_config.py        # BackendType enum + model IDs + costs
│   └── experiment.py            # 27 conditions, 10 critical, cost estimation
│
├── parsers/                     # Parse SWE-Agent output
│   └── trajectory.py            # .traj → ParsedTrajectory → JSON
│
├── metrics/                     # 7 metrics, 3 dimensions
│   ├── tool_dispatch.py         # M1.1 correct_selection, M1.2 redundant_call, M1.3 breadth
│   ├── context_utilization.py   # M2.1 info_retention, M2.2 effective_token_ratio
│   └── backend_portability.py   # M3.1 cross_backend_stddev, M3.2 min_max_ratio
│
├── pipeline/                    # Orchestration + Analysis
│   ├── runner.py                # PipelineRunner: pilot, full run, dry-run
│   └── analysis.py              # Two-way ANOVA, Cohen's d, Tukey HSD
│
├── harness/                     # Abstract interfaces
│   ├── interfaces.py            # ToolProvider, ContextProvider, BackendProvider
│   └── factory.py               # HarnessConfig factory, generate_sweagent_command()
│
└── utils/
```

#### Tại sao tách riêng (không đặt trong SWE-agent/)?

1. **Separation of concerns:** SWE-Agent = agent chạy task, harness_eval = công cụ đo lường
2. **Độc lập phiên bản:** Cập nhật SWE-Agent upstream không ảnh hưởng toolkit
3. **Reusable:** harness_eval có thể dùng để đánh giá agent khác (không chỉ SWE-Agent)
4. **Installable:** `pip install -e .` cài harness_eval riêng, không cần sửa SWE-Agent

---

## Bảng so sánh tổng hợp

### Files trong SWE-Agent gốc vs Fork

| Thư mục/File | Gốc | Fork | Thay đổi |
|-------------|-----|------|----------|
| `sweagent/` | ✅ 50+ files | ✅ Giữ nguyên | ❌ Không sửa |
| `tools/` | ✅ 15 bundles | ✅ Giữ nguyên | ❌ Không sửa |
| `config/default.yaml` | ✅ | ✅ Giữ nguyên | ❌ Không sửa |
| `config/benchmarks/` | ✅ | ✅ Giữ nguyên | ❌ Không sửa |
| `config/demo/` | ✅ | ✅ Giữ nguyên | ❌ Không sửa |
| `config/exotic/` | ✅ | ✅ Giữ nguyên | ❌ Không sửa |
| **`config/harness_eval/`** | ❌ | ✅ **13 files** | ✅ **THÊM MỚI** |
| **`convert_results.py`** | ❌ | ✅ **52 dòng** | ✅ **THÊM MỚI** |
| **`run_test.sh`** | ❌ | ✅ **61 dòng** | ✅ **THÊM MỚI** |
| `pyproject.toml` | ✅ | ✅ Giữ nguyên | ❌ Không sửa |
| `tests/` | ✅ | ✅ Giữ nguyên | ❌ Không sửa |
| `docs/` | ✅ | ✅ Giữ nguyên | ❌ Không sửa |

### Package bên ngoài SWE-Agent

| Component | Gốc | Fork | Mục đích |
|-----------|-----|------|----------|
| **`harness_eval/`** | ❌ | ✅ **2,579 LOC** | Toolkit đánh giá |
| **`app/`** | ❌ | ✅ **1,000+ LOC** | Flask web UI |
| **`tests/`** (harness_eval) | ❌ | ✅ **123 tests** | Unit tests cho toolkit |
| **`streamlit_app.py`** | ❌ | ✅ **300+ LOC** | Dashboard thay thế |
| **`pyproject.toml`** (root) | ❌ | ✅ | Package config cho harness_eval |

---

## Cách các phần mới kết nối với SWE-Agent gốc

```
┌─────────────────────────────────────────────────────────┐
│                    HarnessEval Workflow                   │
│                                                          │
│  ┌──────────────┐    ┌──────────────┐    ┌────────────┐ │
│  │ harness_eval/ │    │ SWE-Agent    │    │ harness_eval│ │
│  │ configs/      │───>│ (KHÔNG SỬA)  │───>│ parsers/   │ │
│  │ experiment.py │    │              │    │ metrics/   │ │
│  │               │    │ Chạy qua     │    │ analysis/  │ │
│  │ Sinh 27       │    │ YAML config  │    │            │ │
│  │ conditions    │    │ composition  │    │ Tính 7     │ │
│  └──────────────┘    └──────┬───────┘    │ metrics    │ │
│                             │            └─────┬──────┘ │
│                             ▼                  │        │
│  ┌──────────────┐    ┌──────────────┐         │        │
│  │config/       │    │ .traj files  │─────────┘        │
│  │harness_eval/ │    │ (output)     │                   │
│  │              │    └──────────────┘                   │
│  │ 13 YAML files│                                       │
│  │ (compose vào │    ┌──────────────┐    ┌────────────┐ │
│  │ SWE-Agent    │    │convert_      │    │ Flask UI   │ │
│  │ --config)    │    │results.py    │───>│ app/       │ │
│  └──────────────┘    └──────────────┘    └────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### Luồng dữ liệu chi tiết:

```
1. harness_eval/configs/experiment.py
   → Định nghĩa 27 conditions (Python)

2. harness_eval/harness/factory.py
   → generate_sweagent_command(condition)
   → Sinh lệnh: python -m sweagent run-batch \
       --config base.yaml \
       --config tool_full.yaml \
       --config ctx_sliding_window.yaml \
       --config be_claude.yaml

3. SWE-Agent (KHÔNG SỬA) nhận config → chạy agent loop
   → Output: trajectories/*.traj

4. convert_results.py
   → Parse .traj → JSON format cho Flask UI

5. harness_eval/parsers/trajectory.py
   → Parse .traj → ParsedTrajectory objects

6. harness_eval/metrics/
   → Tính M1.1-M3.2 từ ParsedTrajectory

7. harness_eval/pipeline/analysis.py
   → Two-way ANOVA trên toàn bộ 7,050 results
```

---

## Tại sao thiết kế như vậy?

### 1. Không sửa source = Dễ update upstream

```bash
# Khi SWE-Agent release version mới:
cd SWE-agent
git fetch upstream
git merge upstream/main
# Không conflict vì ta không sửa file nào của họ
```

### 2. YAML composition = Flexible ablation

SWE-Agent đã hỗ trợ nhiều `--config` flags merge lại. Ta chỉ cần viết YAML files mô tả từng level:

```bash
# 27 conditions chỉ cần 10 YAML files (3+3+3+1 base)
# Thay vì 27 config files riêng lẻ
```

### 3. Toolkit riêng = Reusable cho agent khác

```python
# Trong tương lai, có thể dùng harness_eval để đánh giá:
# - OpenDevin
# - Aider
# - Claude Code
# - Bất kỳ agent nào output trajectory format tương tự
```

### 4. Equivalence test = Đảm bảo tính khoa học

Trước khi kết luận "tool X ảnh hưởng Y%", phải chứng minh rằng fork chạy giống gốc. Nếu fork đã khác 5% ở baseline thì mọi kết quả ablation đều vô nghĩa.

---

## Tóm tắt

| Câu hỏi | Trả lời |
|----------|---------|
| Có sửa source SWE-Agent không? | **KHÔNG** — 0 files thay đổi |
| Thêm gì vào SWE-Agent repo? | **13 YAML configs** + 2 scripts (convert + test) |
| Code mới nằm đâu? | **harness_eval/** — package riêng, bên ngoài SWE-Agent |
| Tổng code mới? | ~2,579 LOC (toolkit) + ~1,000 LOC (web UI) + ~500 LOC (configs/scripts) |
| Cách kết nối? | YAML config composition → .traj output → parse → metrics → ANOVA |
| Tại sao không sửa source? | Dễ update, đảm bảo equivalence, tách biệt concerns |
