# Hướng dẫn sử dụng SWE-Agent gốc (Raw Usage)

## 1. Cài đặt

### Yêu cầu
- Python 3.11+
- Docker (để chạy sandbox)
- API key (Anthropic / OpenAI / hoặc Ollama local)

### Bước cài đặt

```bash
# Clone repo
git clone https://github.com/SWE-agent/SWE-agent.git
cd SWE-agent

# Cài đặt (editable mode)
python -m pip install --upgrade pip && pip install --editable .

# Verify
sweagent --help
```

### Cấu hình API keys

**Cách 1: Environment variables**
```bash
export ANTHROPIC_API_KEY=sk-ant-...
export OPENAI_API_KEY=sk-...
export GITHUB_TOKEN=ghp_...
```

**Cách 2: File .env ở root repo**
```
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
GITHUB_TOKEN=ghp_...
```

**Cách 3: CLI argument**
```bash
--agent.model.api_key="sk-ant-..."
```

---

## 2. CLI Commands

| Command | Alias | Mô tả |
|---------|-------|--------|
| `sweagent run` | `r` | Chạy 1 task (1 GitHub issue) |
| `sweagent run-batch` | `b` | Chạy batch (benchmark SWE-bench) |
| `sweagent run-replay` | — | Replay trajectory đã lưu |
| `sweagent inspect` | `i` | Xem trajectory trong terminal |
| `sweagent inspector` | `I` | Xem trajectory trên web browser |
| `sweagent shell` | `sh` | Interactive shell mode |
| `sweagent merge-preds` | — | Gộp nhiều file predictions |
| `sweagent quick-stats` | `qs` | Thống kê nhanh từ trajectories |
| `sweagent remove-unfinished` | `ru` | Xóa trajectories chưa hoàn thành |
| `sweagent traj-to-demo` | — | Chuyển trajectory thành demo |

---

## 3. Chạy 1 task: `sweagent run`

### Cách đơn giản nhất

```bash
sweagent run \
  --agent.model.name=claude-sonnet-4-20250514 \
  --agent.model.per_instance_cost_limit=2.00 \
  --env.repo.github_url=https://github.com/owner/repo \
  --problem_statement.github_url=https://github.com/owner/repo/issues/123
```

### Với config file

```bash
sweagent run \
  --config config/default.yaml \
  --agent.model.name=gpt-4o \
  --env.repo.github_url=https://github.com/owner/repo \
  --problem_statement.github_url=https://github.com/owner/repo/issues/123
```

### Các loại Problem Statement (chọn 1)

```bash
# Từ GitHub issue
--problem_statement.github_url=https://github.com/owner/repo/issues/123

# Từ file markdown local
--problem_statement.path=/path/to/problem.md

# Từ text trực tiếp
--problem_statement.text="Fix the bug in utils.py where..."
```

### Các loại Repository (chọn 1)

```bash
# Từ GitHub
--env.repo.github_url=https://github.com/owner/repo

# Từ thư mục local
--env.repo.path=/path/to/local/repo
```

### Deployment (nơi code chạy)

```bash
# Docker local (mặc định)
--env.deployment.type=docker
--env.deployment.image=python:3.12

# Modal (cloud)
--env.deployment.type=modal

# Local (không sandbox — nguy hiểm)
--env.deployment.type=local
```

### Cấu hình Model

```bash
--agent.model.name=claude-sonnet-4-20250514    # Tên model
--agent.model.per_instance_cost_limit=2.00     # Giới hạn $/task
--agent.model.total_cost_limit=100.0           # Giới hạn $/session
--agent.model.temperature=0.0                  # Temperature
--agent.model.api_key="sk-..."                 # API key (override env var)
```

### Post-solve Actions

```bash
# Tự động tạo Pull Request sau khi fix xong
--actions.open_pr=true

# Apply patch vào repo local
--actions.apply_patch_locally=true
```

### Output

```bash
# Custom output directory
--output_dir=trajectories/my_experiment/

# Mặc định: trajectories/<user>/<config>__<model>__<problem_id>/
```

---

## 4. Chạy batch: `sweagent run-batch`

### Chạy trên SWE-bench

```bash
sweagent run-batch \
  --config config/default.yaml \
  --agent.model.name gpt-4o \
  --agent.model.per_instance_cost_limit 2.00 \
  --instances.type swe_bench \
  --instances.subset lite \
  --instances.split dev \
  --instances.slice :50
```

### Các loại dataset

**SWE-bench:**
```bash
--instances.type swe_bench
--instances.subset lite          # lite | full | verified
--instances.split dev            # dev | test
--instances.slice :50            # Python slicing (lấy 50 task đầu)
--instances.shuffle=True         # Trộn ngẫu nhiên (deterministic)
```

**Hugging Face:**
```bash
--instances.type huggingface
--instances.dataset_name=SWE_Bench_lite
--instances.split=dev
```

**File JSON local:**
```bash
--instances.type file
--instances.path=/path/to/instances.json
```

### Options cho batch

```bash
--num_workers 3                  # Chạy song song 3 workers
--redo_existing false            # Bỏ qua tasks đã có trajectory
--raise_exceptions false         # Lỗi thì skip, không dừng
--random_delay_multiplier 0.3    # Delay giữa workers (tránh rate limit)
```

### Tự động evaluate trên SWE-bench

```bash
--instances.evaluate=True        # Submit kết quả lên sb-cli
```

---

## 5. Config file structure

### default.yaml (cấu hình mặc định)

```yaml
agent:
  model:
    name: claude-sonnet-4-20250514
    per_instance_cost_limit: 10.0
    temperature: 0.0

  templates:
    system_template: |
      SETTING: You are an autonomous programmer...
    instance_template: |
      We're currently solving the following issue...
      INSTRUCTIONS:
      1. Explore the repo to find relevant files
      2. Create a script to reproduce the error
      3. Edit the source files to resolve the issue
      4. Rerun the reproduce script to confirm
      5. Think about edge cases

  tools:
    bundles:
      - registry
      - edit_anthropic
      - filemap
      - review_on_submit_m
      - bash
    env_variables:
      USE_FILEMAP: "true"
      PAGER: cat
    parse_function: function_calling

  history_processors:
    - type: cache_control
      last_n_messages: 2

env:
  repo:
    github_url: ""
  deployment:
    type: docker
    image: swe-agent/swe-agent

problem_statement:
  github_url: ""

output_dir: DEFAULT
```

### Compose nhiều config files

```bash
# Config sau override config trước
sweagent run \
  --config config/default.yaml \        # Base
  --config my_overrides.yaml \          # Override một số fields
  --agent.model.name=gpt-4o            # CLI override cuối cùng
```

**Thứ tự ưu tiên:** CLI args > config file sau > config file trước > default values

---

## 6. Ví dụ thực tế

### A. Fix 1 GitHub issue (đơn giản nhất)

```bash
# Dùng Claude, fix issue #42 trên repo flask
sweagent run \
  --agent.model.name=claude-sonnet-4-20250514 \
  --agent.model.per_instance_cost_limit=2.00 \
  --env.repo.github_url=https://github.com/pallets/flask \
  --problem_statement.github_url=https://github.com/pallets/flask/issues/42
```

### B. Fix issue từ file mô tả local

```bash
# Dùng GPT-4o, repo local, problem từ file
sweagent run \
  --config config/default.yaml \
  --agent.model.name=gpt-4o \
  --env.repo.path=/home/user/my-project \
  --problem_statement.path=bug_description.md \
  --env.deployment.image=python:3.12
```

### C. Benchmark 50 tasks SWE-bench Lite

```bash
sweagent run-batch \
  --config config/default.yaml \
  --agent.model.name gpt-4o \
  --agent.model.per_instance_cost_limit 2.00 \
  --instances.type swe_bench \
  --instances.subset lite \
  --instances.split dev \
  --instances.slice :50 \
  --num_workers 3 \
  --instances.evaluate=True
```

### D. Chạy trên Modal (cloud — không cần Docker local)

```bash
pip install 'swe-rex[modal]'

sweagent run \
  --agent.model.name=claude-sonnet-4-20250514 \
  --env.deployment.type=modal \
  --env.repo.github_url=https://github.com/owner/repo \
  --problem_statement.github_url=https://github.com/owner/repo/issues/1
```

### E. Test nhanh với Ollama (miễn phí, local)

```bash
# Cài Ollama + pull model
ollama pull qwen2.5-coder:7b

# Chạy SWE-Agent với Ollama
sweagent run \
  --agent.model.name=ollama/qwen2.5-coder:7b \
  --agent.model.per_instance_cost_limit=0 \
  --agent.model.total_cost_limit=0 \
  --env.repo.github_url=https://github.com/SWE-agent/test-repo \
  --problem_statement.github_url=https://github.com/SWE-agent/test-repo/issues/1
```

### F. Fix xong tự tạo PR

```bash
sweagent run \
  --agent.model.name=claude-sonnet-4-20250514 \
  --env.repo.github_url=https://github.com/owner/repo \
  --problem_statement.github_url=https://github.com/owner/repo/issues/123 \
  --actions.open_pr=true
```

---

## 7. Output & Xem kết quả

### Cấu trúc output

```
trajectories/<user>/<config>__<model>__<problem_id>/
├── <issue_id>/
│   ├── config.yaml                # Config đã dùng
│   ├── <issue_id>.trace.log       # Log chi tiết
│   ├── <issue_id>.debug.log       # Debug log
│   ├── <issue_id>.info.log        # Info log
│   └── trajectory.json            # ★ Toàn bộ quá trình
├── preds.json                     # Predictions (batch mode)
└── run_batch_exit_statuses.yaml   # Status (batch mode)
```

### Xem trajectory

```bash
# Terminal UI
sweagent inspect trajectories/.../trajectory.json

# Web UI (mở browser tại http://localhost:8080)
sweagent inspector
```

### trajectory.json chứa gì?

```json
{
  "trajectory": [
    {
      "action": "find_file utils.py",
      "observation": "Found: src/utils.py",
      "thought": "Tìm file liên quan trước",
      "execution_time": 0.5
    },
    {
      "action": "open_file src/utils.py",
      "observation": "1: def process():\n2:   return x + 1\n...",
      "thought": "Đọc file để hiểu bug",
      "execution_time": 0.3
    },
    {
      "action": "edit_file src/utils.py 2 2\n    return x + 2",
      "observation": "File edited successfully",
      "thought": "Fix bug: phải là +2 không phải +1",
      "execution_time": 0.4
    },
    {
      "action": "submit",
      "observation": "Patch submitted",
      "thought": "Fix hoàn tất, submit patch",
      "execution_time": 0.1
    }
  ],
  "history": [...],
  "info": {
    "model_stats": {
      "tokens_sent": 45000,
      "tokens_received": 2300,
      "api_calls": 15,
      "instance_cost": 0.28
    },
    "exit_status": "submitted",
    "submission": "diff --git a/src/utils.py b/src/utils.py\n..."
  }
}
```

---

## 8. Luồng hoạt động khi chạy

```
sweagent run --config ... --problem_statement.github_url ...
│
├── 1. Load config (merge YAML files + CLI args)
│
├── 2. Start environment
│   ├── Pull Docker image
│   ├── Create container
│   ├── Clone repo vào container
│   └── Checkout đúng commit
│
├── 3. Setup agent
│   ├── Load tool bundles → sinh documentation
│   ├── Inject system prompt + instance prompt
│   └── Initialize history
│
├── 4. Agent loop (lặp đến khi done hoặc hết budget)
│   │
│   ├── Step 1: Lấy history → chạy qua history_processors
│   │
│   ├── Step 2: Gửi messages → LLM (qua litellm)
│   │
│   ├── Step 3: Parse response → thought + action
│   │   ├── function_calling mode: LLM trả tool_use JSON
│   │   └── bash_code_block mode: LLM trả ```bash ... ```
│   │
│   ├── Step 4: Execute action trong Docker container
│   │
│   ├── Step 5: Nhận observation (stdout/stderr)
│   │
│   ├── Step 6: Update history + Save trajectory
│   │
│   └── Error handling:
│       ├── FormatError → requery (tối đa 3 lần)
│       ├── CostLimit → auto-submit patch hiện tại
│       ├── ContextOverflow → auto-submit
│       └── Timeout → interrupt + retry
│
├── 5. Agent submit patch (git diff)
│
├── 6. Post-solve actions
│   ├── Save trajectory.json
│   ├── (Optional) Apply patch locally
│   └── (Optional) Open Pull Request
│
└── 7. Cleanup Docker container
```

---

## 9. Models được hỗ trợ (qua litellm)

| Provider | Models | Env var |
|----------|--------|---------|
| **Anthropic** | claude-sonnet-4, claude-opus-4-1 | `ANTHROPIC_API_KEY` |
| **OpenAI** | gpt-4o, gpt-4-turbo, o1-preview | `OPENAI_API_KEY` |
| **DeepSeek** | deepseek-chat, deepseek-coder | `DEEPSEEK_API_KEY` |
| **Together** | llama, mixtral, etc. | `TOGETHER_API_KEY` |
| **Ollama** | qwen2.5, llama3, codellama | (local, no key) |
| **Azure** | Any Azure-hosted model | `AZURE_API_KEY` |

Dùng prefix cho provider: `ollama/qwen2.5:7b`, `together/meta-llama/...`

---

## 10. Tóm tắt nhanh

```bash
# Cài đặt (1 lần)
git clone https://github.com/SWE-agent/SWE-agent.git && cd SWE-agent
pip install -e .
export ANTHROPIC_API_KEY="sk-ant-..."

# Fix 1 issue
sweagent run \
  --agent.model.name=claude-sonnet-4-20250514 \
  --env.repo.github_url=https://github.com/owner/repo \
  --problem_statement.github_url=https://github.com/owner/repo/issues/123

# Benchmark 50 tasks
sweagent run-batch \
  --config config/default.yaml \
  --agent.model.name gpt-4o \
  --instances.type swe_bench --instances.subset lite --instances.slice :50

# Xem kết quả
sweagent inspector
```
