# Cấu trúc Source Code SWE-Agent

## Tổng quan thư mục

```
SWE-agent/
├── sweagent/                           # Package chính
│   ├── agent/                          # Logic agent
│   │   ├── agents.py                   # DefaultAgent, RetryAgent (core loop)
│   │   ├── models.py                   # LLM interface (qua litellm)
│   │   ├── history_processors.py       # Xử lý context (cache, elide, window)
│   │   ├── action_sampler.py           # Chiến lược chọn action
│   │   ├── problem_statement.py        # Input: GitHub issue, text, etc.
│   │   ├── reviewer.py                 # Review loop (multi-attempt)
│   │   └── hooks/                      # Lifecycle hooks
│   │
│   ├── environment/                    # Môi trường thực thi
│   │   ├── swe_env.py                  # SWEEnv: quản lý Docker/Modal container
│   │   ├── repo.py                     # Clone & checkout repo
│   │   └── hooks/
│   │
│   ├── tools/                          # Hệ thống tools
│   │   ├── tools.py                    # ToolHandler: load, validate, execute
│   │   ├── commands.py                 # Command + Argument classes
│   │   ├── parsing.py                  # Action parsers (function_calling, backtick, json)
│   │   ├── bundle.py                   # Load tool bundles từ YAML
│   │   └── utils.py
│   │
│   ├── run/                            # Entry points
│   │   ├── run.py                      # CLI dispatcher (sweagent run/run-batch)
│   │   ├── run_single.py               # Chạy 1 instance
│   │   ├── run_batch.py                # Chạy batch (SWE-Bench)
│   │   ├── run_replay.py               # Replay trajectory đã lưu
│   │   └── hooks/                      # Post-run hooks (apply patch, open PR)
│   │
│   ├── inspector/                      # Xem trajectory (web + terminal)
│   ├── types.py                        # StepOutput, Trajectory, HistoryItem
│   ├── exceptions.py
│   └── utils/
│
├── config/                             # YAML configs
│   ├── default.yaml
│   ├── harness_eval/                   # ★ Configs cho HarnessEval
│   ├── benchmarks/
│   └── demo/
│
├── tools/                              # Tool bundle definitions
│   ├── registry/                       # Default tools
│   ├── edit_anthropic/                 # Anthropic edit tool
│   └── review_on_submit_m/            # Multi-model review
│
└── pyproject.toml
```

---

## Agent Loop (vòng lặp chính)

Đây là trái tim của SWE-Agent — file `sweagent/agent/agents.py`:

```
                    ┌──────────────┐
                    │ GitHub Issue │
                    └──────┬───────┘
                           ▼
                ┌──────────────────┐
                │  agent.setup()   │  Install tools, system prompt
                └────────┬─────────┘
                         ▼
              ┌─────────────────────┐
              │  while not done:    │
              │                     │
              │  ┌───────────────┐  │
              │  │ 1. Get history│  │  ← history_processors xử lý
              │  └───────┬───────┘  │
              │          ▼          │
              │  ┌───────────────┐  │
              │  │ 2. Query LLM  │  │  ← model.query(messages)
              │  └───────┬───────┘  │
              │          ▼          │
              │  ┌───────────────┐  │
              │  │ 3. Parse action│  │  ← thought + action
              │  └───────┬───────┘  │
              │          ▼          │
              │  ┌───────────────┐  │
              │  │4. Execute tool │  │  ← env.communicate(cmd)
              │  └───────┬───────┘  │
              │          ▼          │
              │  ┌───────────────┐  │
              │  │5. Observation  │  │  ← output từ container
              │  └───────┬───────┘  │
              │          ▼          │
              │  ┌───────────────┐  │
              │  │6. Save to traj│  │  ← .traj file
              │  └───────┬───────┘  │
              │          ▼          │
              │   Done? / Cost OK?  │
              └─────────────────────┘
                         ▼
                ┌──────────────┐
                │ Submit patch │
                └──────────────┘
```

### Chi tiết từng bước

**Step 1 - Get history**: Lấy `self.history` → chạy qua `history_processors` (cache_control, last_n_observations, closed_window) → ra `self.messages` đã filtered.

**Step 2 - Query LLM**: Gửi messages tới LLM qua `litellm` (hỗ trợ OpenAI, Anthropic, DeepSeek, Ollama...).

**Step 3 - Parse action**: Tùy `parse_function`:
- `function_calling` → LLM trả tool_use → parse ra tên tool + args
- `single_bash_code_block` → LLM trả 1 block bash code

**Step 4 - Execute**: Chạy command trong Docker container qua `env.communicate()`.

**Step 5 - Observation**: Nhận stdout/stderr từ container.

**Step 6 - Save**: Ghi vào trajectory file (.traj JSON).

---

## Chi tiết từng module

### 1. Agent (`sweagent/agent/`)

#### agents.py — Core Classes

**DefaultAgent** (single-attempt):
```python
class DefaultAgent:
    setup(env, problem)          # Init agent, install tools, add system/demo messages
    step()                       # 1 bước: think → act → observe → record
    run()                        # Main loop gọi step() đến khi done
    forward_with_handling()      # Query model + error handling + requery
    forward()                    # Query → parse → execute → return StepOutput
    handle_action(action)        # Thực thi action trong environment
```

**RetryAgent** (multi-attempt):
```python
class RetryAgent:
    # Wrap nhiều DefaultAgent instances
    # Dùng ScoreRetryLoop / ChooserRetryLoop để chọn best attempt
    # Reviewer đánh giá mỗi attempt → chọn tốt nhất
```

#### Luồng xử lý lỗi:

```
forward_with_handling():
  while retries < max_requeries:
    try:
      step = forward()
    except FormatError / BashSyntaxError:
      → requery (gửi lại với error message)
    except ContextWindowExceeded / CostLimitExceeded:
      → auto-submit patch hiện tại
    except Timeout:
      → interrupt và retry
```

#### models.py — LLM Interface

```python
GenericAPIModelConfig:
    name: str                       # "claude-sonnet-4-20250514", "gpt-4o", etc.
    temperature: float = 0.0
    per_instance_cost_limit: float  # $/task (mặc định $3.0)
    total_cost_limit: float         # $/session (mặc định $100)
```

- Dùng **litellm** → unified API cho mọi LLM provider
- Tự track tokens, costs, API errors
- Hỗ trợ retries và fallbacks

#### history_processors.py — Quản lý Context

| Processor | Chức năng |
|-----------|-----------|
| `CacheControlHistoryProcessor` | Đánh dấu cache cho Anthropic prompt caching |
| `LastNObservationsHistoryProcessor` | Chỉ giữ N observation gần nhất |
| `ClosedWindowHistoryProcessor` | Thay observation cũ bằng "X lines omitted" |
| `RemoveRegexHistoryProcessor` | Xóa output dài, diff blocks theo regex |

**Mapping sang HarnessEval:**
- **FULL** = chỉ `cache_control` (giữ hết, ~200K tokens)
- **SLIDING_WINDOW** = `cache_control` + `last_n_observations(15)` + `closed_window` (~50K tokens)
- **SUMMARY** = `cache_control` + `last_n_observations(3)` + `closed_window` + `remove_regex` (~2K tokens)

---

### 2. Environment (`sweagent/environment/`)

#### swe_env.py — SWEEnv Class

```python
class SWEEnv:
    start()              # Khởi tạo Docker container (qua swe-rex)
    reset(instance)      # Checkout repo + đúng commit cho task
    communicate(cmd)     # Gửi bash command vào container, nhận output
    close()              # Dọn dẹp container
```

- Mỗi task = 1 Docker container riêng → isolated, reproducible
- Hỗ trợ Docker local hoặc Modal (cloud)
- Container có sẵn repo, dependencies, test suite

#### repo.py — Repository Management

```python
class RepoConfig:
    github_url: str      # "https://github.com/user/repo"
    base_commit: str     # Commit để checkout
```

---

### 3. Tools (`sweagent/tools/`)

#### Tool Bundle Architecture

```
tools/ (thư mục gốc)
├── registry/              # Bundle mặc định
│   ├── config.yaml        # Định nghĩa commands
│   ├── bash.sh            # bash command
│   ├── read.sh            # read file
│   ├── edit.sh            # edit file
│   ├── grep.sh            # search
│   ├── glob.sh            # find files
│   ├── find.sh            # find
│   ├── git_diff.sh        # git diff
│   ├── git_log.sh         # git log
│   ├── git_show.sh        # git show
│   └── test_runner.sh     # run tests
├── edit_anthropic/        # Anthropic-style edit (khác registry edit)
└── review_on_submit_m/    # Multi-model review trước khi submit
```

Mỗi bundle = 1 thư mục chứa `config.yaml` + bash scripts.

#### tools.py — ToolHandler

```python
class ToolHandler:
    load_bundles()           # Load tool bundles từ config
    generate_docs()          # Sinh documentation → inject vào system prompt
    parse_actions(response)  # Parse LLM output → action name + args
    validate(command)        # Kiểm tra command hợp lệ (block vim, interactive shells)
    execute(command)         # Gửi tới environment
```

#### parsing.py — Action Parsers

| Parser | Cách parse | Dùng cho |
|--------|-----------|----------|
| `FunctionCallingParser` | LLM trả tool_use JSON | FULL, MEDIUM tools |
| `ThoughtActionParser` | Backtick-wrapped commands | Legacy |
| `ActionOnlyParser` | Chỉ command, không thought | Simple agents |
| `JsonParser` | JSON format | Structured output |

**HarnessEval mapping:**
- FULL + MEDIUM tools → `function_calling` parser
- MINIMAL tools → `single_bash_code_block` parser (agent chỉ trả 1 bash command)

#### commands.py — Command Definitions

```python
@dataclass
class Command:
    name: str              # "read", "edit", "grep"
    docstring: str         # Mô tả cho LLM hiểu cách dùng
    arguments: list[Arg]   # Params: file_path, line_number, etc.
    signature: str         # Cách gọi: "read <file_path> [start_line] [end_line]"
    code: str              # Bash script thực thi
```

---

### 4. Run (`sweagent/run/`)

#### run_single.py — Chạy 1 task

```python
class RunSingle:
    def run():
        env.start()                     # 1. Start Docker
        agent.setup(env, problem)       # 2. Init agent
        while not done:
            step = agent.step()         # 3. Lặp step
            save_trajectory()           # 4. Save .traj
        env.close()                     # 5. Cleanup
        return AgentRunResult
```

#### run_batch.py — Chạy SWE-Bench

```python
class RunBatch:
    def run():
        instances = load_instances()        # 1. Load từ SWE-Bench dataset
        for instance in instances:          # 2. Parallel execution
            run_single = RunSingle(...)
            result = run_single.run()
            save_predictions(result)
        merge_predictions()                 # 3. Tạo preds.json
        evaluate()                          # 4. Chạy SWE-Bench eval
```

#### hooks/ — Post-run Actions

```python
# Các hook chạy sau khi agent xong:
ApplyPatchLocally()     # Apply patch vào repo local
OpenPR()                # Tạo Pull Request trên GitHub
SavePrediction()        # Lưu prediction cho evaluation
```

---

### 5. Data Types (`sweagent/types.py`)

```python
@dataclass
class StepOutput:
    thought: str            # Suy nghĩ của agent
    action: str             # Command được chọn
    observation: str        # Output từ environment
    done: bool              # Đã xong chưa?
    exit_status: str        # "submitted", "cost_limit", "error"
    submission: str          # Git patch nếu submit
    tool_calls: list        # Function calling data
    execution_time: float

@dataclass
class HistoryItem:
    role: str               # "system", "user", "assistant", "tool"
    content: str            # Nội dung message
    tool_calls: list        # Tool use data
    cache_control: dict     # Prompt caching markers

Trajectory = list[TrajectoryStep]   # Toàn bộ quá trình giải quyết
```

---

### 6. Configuration System

#### Hierarchy (ưu tiên từ thấp đến cao):

```
1. Default values (trong Pydantic models)
2. YAML config files (config/*.yaml)
3. CLI arguments (--agent.model.name, --env.repo.path)
```

#### Main Config Classes:

```python
class RunSingleConfig:
    env: EnvironmentConfig          # Docker, repo, post_startup_commands
    agent: AgentConfig              # Model, tools, history_processors
    problem_statement: ProblemConfig # GitHub issue hoặc text
    output_dir: str                 # Nơi lưu trajectory
    actions: PostProcessingConfig   # Apply patch, open PR

class AgentConfig:                  # Polymorphic
    templates:
        system_template: str        # System prompt
        instance_template: str      # Task description format
        next_step_template: str     # Prompt mỗi step
    tools:
        bundles: list[str]          # ["registry", "edit_anthropic", ...]
        env_variables: dict         # PAGER=cat, etc.
        parse_function: str         # "function_calling" hoặc "single_bash_code_block"
    history_processors: list        # [cache_control, last_n_observations, ...]
    model: GenericAPIModelConfig    # LLM settings
    max_requeries: int = 3          # Số lần retry khi format error
```

#### YAML Composition (cách HarnessEval dùng):

```bash
# Nhiều --config → merge từ trái sang phải (sau override trước)
python -m sweagent run \
  --config base.yaml \              # Shared settings
  --config tool_full.yaml \         # Override tools section
  --config ctx_sliding_window.yaml \ # Override history_processors
  --config be_claude.yaml           # Override model section
```

---

## Trajectory Output (.traj JSON)

```json
{
  "trajectory": [
    {
      "action": "read /src/main.py",
      "observation": "def solve(): ...",
      "thought": "Cần xem file main.py trước",
      "execution_time": 1.2
    },
    {
      "action": "edit /src/main.py 42 42\n    return result + 1",
      "observation": "File edited successfully",
      "thought": "Fix bug ở dòng 42: thiếu +1",
      "execution_time": 0.8
    }
  ],
  "history": [
    {"role": "system", "content": "You are a helpful assistant..."},
    {"role": "user", "content": "Fix the bug in issue #123..."},
    {"role": "assistant", "content": "Let me read the file first..."},
    {"role": "tool", "content": "def solve(): ..."}
  ],
  "info": {
    "model_stats": {
      "tokens_sent": 45000,
      "tokens_received": 2300,
      "api_calls": 15,
      "instance_cost": 0.28
    },
    "exit_status": "submitted",
    "submission": "diff --git a/src/main.py b/src/main.py\n...",
    "edited_files30": "src/main.py (3 lines changed)"
  },
  "replay_config": "...",
  "environment": "main"
}
```

---

## CLI Commands

```bash
sweagent run              # Chạy 1 instance (1 task)
sweagent run-batch        # Chạy batch (SWE-Bench dataset, parallel)
sweagent run-replay       # Replay trajectory đã save (debug/review)
sweagent inspect          # Xem trajectory (mở web UI)
```

---

## Dependencies chính

| Package | Vai trò |
|---------|---------|
| **swerex** (>=1.4.0) | Runtime abstraction — quản lý Docker/Modal containers |
| **litellm** | Unified LLM API — gọi OpenAI, Anthropic, DeepSeek, Ollama qua 1 interface |
| **pydantic** | Config validation — type-safe, error messages rõ ràng |
| **simple-parsing** | CLI argument parsing — auto-generate CLI từ dataclass |
| **rich** | Terminal UI — progress bars, formatting |
| **ghapi** | GitHub API — tạo PR, đọc issues |
| **unidiff** | Parse git patches — xử lý diff output |
| **datasets** | Load SWE-Bench data — HuggingFace datasets |

---

## Design Patterns

### 1. Composition over Inheritance
Agent + Environment + Model là các component độc lập, plug-and-play. Thay model không cần sửa agent, thay environment không cần sửa tools.

### 2. Strategy Pattern
- History processors → swap context strategy qua config
- Action parsers → swap parsing method qua config
- Tool bundles → swap tool set qua config

### 3. Hooks System
Lifecycle hooks ở mỗi layer:
- **Agent hooks**: before_step, after_step, on_error
- **Environment hooks**: on_start, on_reset, on_close
- **Run hooks**: apply_patch, open_pr, save_prediction

### 4. Error Recovery
```
FormatError          → requery (gửi lại với error message, tối đa 3 lần)
BashSyntaxError      → requery
CostLimitExceeded    → auto-submit patch hiện tại
ContextWindowExceeded → auto-submit patch hiện tại
Timeout              → interrupt + retry
```

### 5. Factory Pattern
Config YAML → Pydantic validation → instantiate đúng class (DefaultAgent vs RetryAgent vs ShellAgent).

---

## Tóm tắt kiến trúc

```
┌────────────────────────────────────────────────────┐
│                    CLI / Config                     │
│  sweagent run --config base.yaml --config tool.yaml │
└──────────────────────┬─────────────────────────────┘
                       ▼
┌────────────────────────────────────────────────────┐
│                   RunSingle                         │
│  Orchestrate: setup → loop → cleanup → save         │
└──────┬──────────────┬──────────────┬───────────────┘
       ▼              ▼              ▼
┌────────────┐ ┌────────────┐ ┌────────────┐
│   Agent    │ │Environment │ │   Model    │
│            │ │            │ │            │
│ step()     │ │ Docker/    │ │ litellm    │
│ forward()  │ │ Modal      │ │ query()    │
│ history    │ │ container  │ │ cost track │
│ processors │ │ communicate│ │ retry      │
└─────┬──────┘ └─────┬──────┘ └────────────┘
      ▼              ▼
┌────────────┐ ┌────────────┐
│   Tools    │ │    Repo    │
│            │ │            │
│ bundles    │ │ git clone  │
│ parse      │ │ checkout   │
│ validate   │ │ apply diff │
└────────────┘ └────────────┘
```
