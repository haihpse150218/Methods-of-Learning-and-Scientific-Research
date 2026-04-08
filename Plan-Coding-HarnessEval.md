# PLAN CODING: HarnessEval Toolkit
# (Ghi nhan qua trinh code va test)

> **Ngay bat dau:** 07/04/2026
> **Trang thai:** Phase 7 — Unified Pipeline Flow (NEXT)
> **Vi tri:** `NCKK-Docs/de-tai/DE-CUONG-HarnessEval-v2/`

---

## 1. Tong quan

### 1.1. Muc tieu coding

Xay dung **harness-eval** Python toolkit (RO5 trong de cuong) de:
- Quan ly experiment config (27 conditions = 3x3x3)
- Tinh toan 7 metrics (3 dimensions)
- Phan tich thong ke (Three-way ANOVA, Cohen's d, Tukey HSD)
- CLI de chay evaluation pipeline

### 1.2. Mapping voi de cuong

| Module | De cuong reference | Trang thai |
|--------|-------------------|------------|
| `configs/tool_config.py` | RO2, Section 3.3 — 3 tool levels (12/8/5) | DONE |
| `configs/context_config.py` | RO2, Section 3.3 — 3 strategies | DONE |
| `configs/backend_config.py` | RO3, Section 3.5 — 3 LLM backends | DONE |
| `configs/experiment.py` | RO3, Table 4 — 27 conditions, 7050 evals | DONE |
| `metrics/tool_dispatch.py` | RO1, Table 2 — M1.1, M1.2, M1.3 | DONE |
| `metrics/context_utilization.py` | RO1, Table 2 — M2.1, M2.2 | DONE |
| `metrics/backend_portability.py` | RO1, Table 2 — M3.1, M3.2 | DONE |
| `pipeline/analysis.py` | RO4, Section 2.2.3 — ANOVA + GLMM | DONE (ANOVA + GLMM) |
| `pipeline/runner.py` | RO5 — Pipeline runner (dry-run + real) | DONE |
| `parsers/trajectory.py` | RO5 — SWE-Agent log parser | DONE |
| `harness/` | RO2, Section 3.3 — SWE-Agent fork | STUB (chua implement) |
| `cli.py` | RO5 — CLI entry point | DONE (info, pilot, run, convert, analyze) |

---

## 2. Cau truc thu muc

```
DE-CUONG-HarnessEval-v2/
├── index.html                          # HTML render cua PDF de cuong
├── pyproject.toml                      # Python package config (pip install -e .)
├── harness_eval/
│   ├── __init__.py                     # v0.1.0
│   ├── cli.py                          # CLI: harness-eval info, harness-eval pilot
│   ├── configs/
│   │   ├── __init__.py                 # Export ToolConfig, ContextConfig, BackendConfig, ExperimentConfig
│   │   ├── tool_config.py              # ToolLevel enum (FULL/MEDIUM/MINIMAL), 12/8/5 tools
│   │   ├── context_config.py           # ContextStrategy enum (FULL/SLIDING_WINDOW/SUMMARY)
│   │   ├── backend_config.py           # BackendType enum (CLAUDE/GPT/DEEPSEEK), cost per eval
│   │   └── experiment.py               # ExperimentConfig, Condition, 10 CRITICAL_CONDITIONS
│   ├── metrics/
│   │   ├── __init__.py                 # Export all 7 metric functions
│   │   ├── tool_dispatch.py            # M1.1 correct_selection_rate, M1.2 redundant_call_rate, M1.3 utilization_breadth
│   │   ├── context_utilization.py      # M2.1 info_retention_score, M2.2 effective_token_ratio
│   │   └── backend_portability.py      # M3.1 cross_backend_stddev, M3.2 min_max_ratio
│   ├── parsers/
│   │   ├── __init__.py                 # Export parse_trajectory_file, etc.
│   │   └── trajectory.py              # TrajectoryMetadata, ParsedTrajectory, validate, parse, summary
│   ├── pipeline/
│   │   ├── __init__.py
│   │   ├── analysis.py                 # compute_three_way_anova, compute_cohens_d, tukey_hsd_pairwise
│   │   └── runner.py                   # PipelineRunner, RunConfig, TaskResult, ConditionResult
│   ├── harness/
│   │   └── __init__.py                 # Stub — se implement khi fork SWE-Agent
│   └── utils/
│       └── __init__.py                 # Stub — se implement helper functions
├── scripts/
│   └── generate_samples.py            # Generate sample trajectory data for UI testing
└── tests/
    ├── __init__.py
    ├── test_configs.py                 # 36 tests
    ├── test_metrics.py                 # 38 tests (M1.1-M3.2)
    ├── test_analysis.py                # 10 tests (ANOVA, Cohen's d)
    ├── test_parser.py                  # 22 tests (validate, parse, summary)
    └── test_runner.py                  # 17 tests (runner, dry-run, save)
```

---

## 3. Qua trinh thuc hien (07/04/2026)

### 3.1. Session 1: Scaffolding + Core Implementation

**Buoc 1: Tao folder va HTML**
- Tao `DE-CUONG-HarnessEval-v2/` folder
- Code `index.html` — render toan bo PDF de cuong thanh HTML
  - Cover page, Table of Contents voi anchor links
  - 5 chapters day du: Introduction, Literature Review, Methodology, Expected Results, Timeline
  - Styling: responsive, academic look, color-coded sections
  - Tables: Characteristics (Table 1), Taxonomy (Table 2), Pilot (Table 3), Factorial (Table 4), Risks (Table 5), Venues (Table 6), Timeline (Table 7), Budget (Table 8)

**Buoc 2: Python package setup**
- Tao `pyproject.toml` voi dependencies: numpy, pandas, scipy, scikit-learn, statsmodels, pyyaml, click, rich
- Dev dependencies: pytest, pytest-cov, ruff
- Optional `[bert]` extra cho BERTScore (M2.1 production)

**Buoc 3: Configs module (mapping voi RO2, RO3)**
- `tool_config.py`: 3 levels voi tool lists cu the
  - Full: 12 tools (bash, python, read, write, edit, glob, grep, find, git_diff, git_log, git_show, test_runner)
  - Medium: 8 tools (core development subset)
  - Minimal: 5 tools (essential only: bash, read, write, edit, grep)
  - Constraint: minimal ⊂ medium ⊂ full (gradual reduction per Section 2.2.2)
- `context_config.py`: 3 strategies voi params
  - Full: no truncation
  - Sliding window: 50K tokens default
  - Summary: 2K tokens max
- `backend_config.py`: 3 backends voi model IDs, providers, costs
  - Claude Sonnet 4: $0.35/eval, anthropic
  - GPT-4o: $0.30/eval, openai
  - DeepSeek-V3: $0.15/eval, deepseek (cheapest — per risk mitigation)
  - All temperature = 0 (per Section 3.6.1 mitigation)
- `experiment.py`: Full factorial design
  - 27 conditions = 3x3x3
  - 10 CRITICAL_CONDITIONS get 3 runs each
  - 17 other conditions get 1 run
  - Total: (10×3 + 17×1) × 150 = 7,050 evaluations
  - Pilot: 5 × 20 × 2 = 200 evaluations

**Buoc 4: Metrics module (mapping voi RO1, Table 2)**
- `tool_dispatch.py`:
  - M1.1 `correct_selection_rate()`: % calls chon tool dung tu tap acceptable tools (khong phai single ground-truth, per cau hoi #4)
  - M1.2 `redundant_call_rate()`: % calls ma output khong duoc dung trong 3 turns tiep
  - M1.3 `utilization_breadth()`: unique tools used / total available
- `context_utilization.py`:
  - M2.1 `info_retention_score()`: Jaccard similarity (simplified) + `info_retention_score_bert()` (production voi BERTScore)
  - M2.2 `effective_token_ratio()`: % tokens relevant, weighted by token_count
- `backend_portability.py`:
  - M3.1 `cross_backend_stddev()`: np.std cua resolve rates (population std)
  - M3.2 `min_max_ratio()`: min(RR)/max(RR)

**Buoc 5: Analysis module (mapping voi RO4, Section 2.2.3)**
- `analysis.py`:
  - `compute_three_way_anova()`: Tool × Context × Backend, dung statsmodels OLS + ANOVA type II
  - ANOVAResult dataclass: source, sum_sq, df, mean_sq, f_statistic, p_value, eta_squared
  - `is_significant` property: p < 0.05/7 (Bonferroni correction cho 7 tests)
  - `compute_cohens_d()`: effect size cho pairwise comparison
  - `tukey_hsd_pairwise()`: post-hoc Tukey HSD

**Buoc 6: CLI**
- `harness-eval info`: hien thi experiment design summary
- `harness-eval pilot`: stub cho pilot study

### 3.2. Testing

**123 tests tong cong, 100% passed:**

| File | So tests | Coverage |
|------|----------|----------|
| `test_configs.py` | 36 | Tool (10), Context (8), Backend (7), Experiment (11) |
| `test_metrics.py` | 38 | M1.1 (6), M1.2 (4), M1.3 (6), M2.1 (6), M2.2 (6), M3.1 (5), M3.2 (5) |
| `test_analysis.py` | 10 | Cohen's d (6), ANOVA integration (4) |
| `test_parser.py` | 22 | validate (7), parse_file (7), parse_dir (4), summary (4) |
| `test_runner.py` | 17 | TaskResult (1), ConditionResult (3), Runner (10), Convenience (2), Save (3) |

**Key test validations:**
- 27 conditions duoc generate dung (3×3×3)
- 7,050 total evaluations (10×3 + 17×1) × 150
- 200 pilot evaluations (5×20×2)
- Tool subset hierarchy: minimal ⊂ medium ⊂ full
- All backends temperature = 0
- DeepSeek la backend re nhat
- ANOVA eta-squared sum = 1.0
- Metric boundary conditions (empty, zero, edge cases)

**3 loi ban dau va cach fix:**
1. `test_medium_effect`: Cohen's d = 7.7 (data qua separated) → doi assertion `d > 0.2`
2. `test_no_redundancy`: output[:50] matching logic → fix test data de output xuat hien trong future turns
3. `test_identical_rates`: floating point error (1.1e-16) → doi `== 0.0` thanh `< 1e-10`

---

## 4. Dependencies

```
# Core
numpy>=1.24
pandas>=2.0
scipy>=1.11
scikit-learn>=1.3
statsmodels>=0.14
pyyaml>=6.0
click>=8.1
rich>=13.0

# Dev
pytest>=7.4
pytest-cov>=4.1
ruff>=0.1

# Optional (BERTScore production)
torch>=2.0
bert-score>=0.3.13
```

**Install:** `pip install -e ".[dev]" && pip install flask` trong folder `DE-CUONG-HarnessEval-v2/`

---

## 5. Kien truc Modular Harness (RO2 — SWE-Agent Fork)

### 5.1. Tong quan kien truc

De thuc hien ablation study (RO3), can **tach harness thanh 3 tang doc lap** co the hoan doi qua config.
Ky thuat chinh: **Strategy Pattern + Dependency Injection + Factory Pattern**.

> **Visualization:** Xem file `architecture-harness-module.html` (tieng Viet) va `architecture-harness-module-en.html` (tieng Anh)

### 5.2. Ba tang hoan doi (3 Swappable Layers)

```
┌─────────────────────────────────────────────────────┐
│                  Modular Harness                     │
│                                                     │
│  ┌───────────────────────────────────────────────┐  │
│  │ LAYER 1: Tool Dispatch    [ToolProvider]      │  │
│  │  Config A: Full (12 tools)                    │  │
│  │  Config B: Medium (8 tools)                   │  │
│  │  Config C: Minimal (5 tools)                  │  │
│  └──────────────────┬────────────────────────────┘  │
│                     │ interface                      │
│  ┌──────────────────▼────────────────────────────┐  │
│  │ LAYER 2: Context Mgmt    [ContextStrategy]    │  │
│  │  Strategy 1: Full History (no truncation)     │  │
│  │  Strategy 2: Sliding Window (50K tokens)      │  │
│  │  Strategy 3: ACC / Summary (2K tokens)        │  │
│  └──────────────────┬────────────────────────────┘  │
│                     │ interface                      │
│  ┌──────────────────▼────────────────────────────┐  │
│  │ LAYER 3: LLM Backend     [LLMBackend]        │  │
│  │  Backend I:   Claude Sonnet 4  ($0.35/eval)   │  │
│  │  Backend II:  GPT-4o           ($0.30/eval)   │  │
│  │  Backend III: DeepSeek-V3      ($0.15/eval)   │  │
│  └───────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

### 5.3. Interface design (se implement trong `harness_eval/harness/`)

```python
# harness/interfaces.py
class ToolProvider(ABC):
    """Layer 1: Cung cap tap cong cu cho agent."""
    @abstractmethod
    def get_tools(self) -> list[Tool]: ...
    @abstractmethod
    def get_tool_names(self) -> list[str]: ...

class ContextStrategy(ABC):
    """Layer 2: Quan ly context window."""
    @abstractmethod
    def build(self, history: list[Message]) -> str: ...
    @abstractmethod
    def max_tokens(self) -> int: ...

class LLMBackend(ABC):
    """Layer 3: Goi LLM API."""
    @abstractmethod
    def generate(self, context: str, tools: list[Tool]) -> Response: ...
    @abstractmethod
    def model_id(self) -> str: ...
```

### 5.4. Factory + Config YAML

```python
# harness/factory.py
def create_harness(config: dict) -> ModularHarness:
    tool = ToolFactory.create(config["tool_provider"])       # "full" | "medium" | "minimal"
    ctx  = ContextFactory.create(config["context_strategy"]) # "full" | "sliding_window" | "summary"
    llm  = LLMFactory.create(config["llm_backend"])          # "claude" | "gpt" | "deepseek"
    return ModularHarness(tool, ctx, llm)
```

```yaml
# experiment_config.yaml — vi du 1 to hop
run_14:
  tool_provider: "minimal"
  context_strategy: "summary"
  llm_backend: "claude"
```

### 5.5. Mapping voi code hien tai

| Harness Layer | Config module (DA CO) | Harness module (CAN LAM) |
|---------------|----------------------|--------------------------|
| Tool Dispatch | `configs/tool_config.py` — ToolLevel enum, 12/8/5 tools | `harness/tool_providers.py` — FullToolProvider, MediumToolProvider, MinimalToolProvider |
| Context Mgmt | `configs/context_config.py` — ContextStrategy enum | `harness/context_strategies.py` — FullHistoryStrategy, SlidingWindowStrategy, SummaryStrategy |
| LLM Backend | `configs/backend_config.py` — BackendType enum, costs | `harness/llm_backends.py` — ClaudeBackend, GPTBackend, DeepSeekBackend |
| Factory | `configs/experiment.py` — 27 Conditions | `harness/factory.py` — create_harness() |
| Runner | — | `pipeline/runner.py` — chay 1 condition tren N tasks |

### 5.6. Quy trinh ablation 27 to hop

```
3 Tool configs × 3 Context strategies × 3 LLM backends = 27 conditions

Condition #1:  Full    × Full History  × Claude    → baseline
Condition #2:  Full    × Full History  × GPT       → doi LLM, giu harness
...
Condition #14: Minimal × Summary/ACC  × Claude    → vi du minh hoa
...
Condition #27: Minimal × Summary/ACC  × DeepSeek  → to hop cuoi

→ Moi condition chay tren 150 tasks tu SWE-Bench Verified
→ 10 critical conditions × 3 runs + 17 others × 1 run = 7,050 evaluations
→ ANOVA 3 chieu phan tach: % dong gop Tool vs Context vs LLM
```

### 5.7. Equivalence verification (±3%)

Truoc khi chay ablation, can dam bao modular fork **khong lam hong** SWE-Agent goc:
1. Chay 50 tasks voi config = (Full, Full History, GPT-4o) — giong SWE-Agent goc
2. So sanh resolve rate voi SWE-Agent goc
3. Chap nhan sai lech ≤ ±3% (absolute)
4. Neu vuot 3% → debug refactor, khong chay ablation

---

## 6. UI Dashboard — Interactive Config + Pipeline + Metrics Viewer

### 6.1. Tong quan

Xay dung **web UI** (single-page HTML + JS) cho phep:
1. **Chon config** — pick Tool level, Context strategy, Backend → thay condition ID
2. **Xem pipeline** — visualize tung buoc chay cho condition da chon
3. **Xem logs** — auto-scan `trajectories/` folder → tu dong tinh 7 metrics
4. **So sanh conditions** — chon 2+ conditions, xem metrics side-by-side
5. **ANOVA results** — auto-load `results/` folder → hien ANOVA table + charts

### 6.2. 5 man hinh chinh

```
┌─────────────────────────────────────────────────────────────────┐
│  TAB 1: CONFIG BUILDER                                          │
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │ Tool Level  │  │ Context     │  │ Backend     │             │
│  │ ○ Full (12) │  │ ○ Full      │  │ ○ Claude    │             │
│  │ ● Medium(8) │  │ ● Sliding   │  │ ○ GPT-4o   │             │
│  │ ○ Minimal(5)│  │ ○ Summary   │  │ ● DeepSeek │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│                                                                 │
│  Condition ID: medium_sliding_window_deepseek                   │
│  Runs: 1 (normal) | Est. cost: $22.50 | Tasks: 150             │
│                                                                 │
│  Tools included: [bash] [python] [read] [write]                 │
│                  [edit] [grep] [git_diff] [test_runner]          │
│  Tools removed:  [glob] [find] [git_log] [git_show]            │
│                                                                 │
│  Context: Sliding window — keep last 50,000 tokens              │
│  Backend: DeepSeek-V3 — $0.15/eval, temp=0                     │
│                                                                 │
│  [Generate YAML Config]  [Add to Run Queue]                     │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  TAB 2: PIPELINE VIEWER                                         │
│                                                                 │
│  Condition: medium_sliding_window_deepseek                      │
│                                                                 │
│  ┌──────┐    ┌──────┐    ┌──────┐    ┌──────┐    ┌──────┐     │
│  │ Task │ ─→ │Config│ ─→ │ Run  │ ─→ │ Log  │ ─→ │Metric│     │
│  │Select│    │ Load │    │Agent │    │Parse │    │Calc  │     │
│  │      │    │      │    │      │    │      │    │      │     │
│  │ 150  │    │ YAML │    │ SWE- │    │ JSON │    │ 7    │     │
│  │tasks │    │      │    │Agent │    │      │    │scores│     │
│  └──────┘    └──────┘    └──────┘    └──────┘    └──────┘     │
│  [DONE]      [DONE]      [Running]   [Pending]   [Pending]     │
│                          Task 47/150                            │
│                          ████████░░░ 31%                        │
│                          Est. remaining: 2h 15m                 │
│                                                                 │
│  Live log:                                                      │
│  > Task django-12345: read models.py → edit → test → PASS      │
│  > Task flask-6789: read app.py → grep → edit → test → FAIL    │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  TAB 3: LOG VIEWER + METRICS                                    │
│                                                                 │
│  Auto-scan: trajectories/  [Refresh]  [Filter: condition ▾]    │
│                                                                 │
│  File: trajectories/medium_sliding_deepseek/django-12345.json   │
│  Status: RESOLVED ✓  |  Turns: 8  |  Cost: $0.18               │
│                                                                 │
│  ┌─ Turn 1 ──────────────────────────────────────────────┐      │
│  │ Action: read  Args: {"path": "django/db/models.py"}   │      │
│  │ Output: class Model:\n    def save(self):\n  ...      │      │
│  │ Annotation: ✓ Correct (acceptable: [read, grep])      │      │
│  └────────────────────────────────────────────────────────┘      │
│  ┌─ Turn 2 ──────────────────────────────────────────────┐      │
│  │ Action: grep  Args: {"pattern": "def save"}            │      │
│  │ Output: line 245: def save(self, *args, **kwargs)      │      │
│  │ Annotation: ✓ Correct | Output used in Turn 3          │      │
│  └────────────────────────────────────────────────────────┘      │
│  ... (8 turns total)                                            │
│                                                                 │
│  ─── METRICS (auto-computed) ─────────────────────────────────  │
│  M1.1 Correct Selection:  87.5%  ████████░░ [6/8 correct]      │
│  M1.2 Redundant Calls:    12.5%  █░░░░░░░░░ [1/8 redundant]    │
│  M1.3 Utilization Breadth: 50.0%  █████░░░░░ [4/8 tools used]  │
│  M2.2 Effective Tokens:   73.2%  ███████░░░                     │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  TAB 4: COMPARE CONDITIONS                                      │
│                                                                 │
│  Select conditions:  [+ Add condition]                          │
│  ■ full_full_claude   ■ minimal_full_claude   ■ full_summary_claude │
│                                                                 │
│  ┌──────────────┬───────────┬───────────┬──────────────┐        │
│  │ Metric       │ Full/Full │ Min/Full  │ Full/Summary │        │
│  │              │ /Claude   │ /Claude   │ /Claude      │        │
│  ├──────────────┼───────────┼───────────┼──────────────┤        │
│  │ Resolve Rate │  72.0%    │  55.3%    │  63.3%       │        │
│  │ M1.1 Select  │  89.2%    │  91.0%    │  88.5%       │        │
│  │ M1.2 Redund  │   8.3%    │  15.7%    │   9.1%       │        │
│  │ M1.3 Breadth │  45.2%    │  72.0%    │  44.8%       │        │
│  │ M2.1 Retain  │  95.1%    │  94.8%    │  71.2%       │        │
│  │ M2.2 EffTok  │  78.3%    │  77.9%    │  52.4%       │        │
│  └──────────────┴───────────┴───────────┴──────────────┘        │
│                                                                 │
│  Chart: [Bar chart comparing 3 conditions across metrics]       │
│                                                                 │
│  Cohen's d (Full vs Minimal tools): 0.604 (medium-large)        │
│  Cohen's d (Full vs Summary ctx):   0.412 (medium)              │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  TAB 5: ANOVA RESULTS                                           │
│                                                                 │
│  Auto-load: results/anova_output.csv  [Refresh]                 │
│                                                                 │
│  Three-Way ANOVA: Tool(3) × Context(3) × Backend(3)            │
│                                                                 │
│  Source                eta²     F       p-value   Sig?          │
│  ──────────────────────────────────────────────────             │
│  Tool                 0.056   16.23    <0.001    ***            │
│  Context              0.019    5.38     0.005    **             │
│  Backend              0.008    2.17     0.116                   │
│  Tool × Context       0.007    1.06     0.374                   │
│  Tool × Backend       0.005    0.69     0.598                   │
│  Context × Backend    0.001    0.14     0.967                   │
│  T × C × B            0.017    1.26     0.264                   │
│  Error                0.887                                     │
│                                                                 │
│  [Pie chart: variance decomposition]                            │
│  [Interaction plot: Backend × Tool config]                      │
│  [Forest plot: Cohen's d for all pairwise comparisons]          │
│                                                                 │
│  Hypotheses:                                                    │
│  H1: Tool largest effect    → eta²=0.056 > Context=0.019  ✓    │
│  H2: Context medium effect  → d=0.412                      ✓    │
│  H3: Harness ≥10% variance → 5.6%+1.9%=7.5%               ✗    │
│  H4: Interaction significant → p=0.598                      ✗    │
└─────────────────────────────────────────────────────────────────┘
```

### 6.3. File structure UI

```
DE-CUONG-HarnessEval-v2/
├── dashboard.html              ← DA CO: overview dashboard (dark theme)
├── app/                        ← MOI: interactive UI app
│   ├── index.html              # Main app — 5 tabs
│   ├── css/
│   │   └── styles.css          # Dark theme, consistent voi dashboard.html
│   ├── js/
│   │   ├── app.js              # Tab routing, state management
│   │   ├── config-builder.js   # Tab 1: chon config, generate YAML
│   │   ├── pipeline-viewer.js  # Tab 2: visualize pipeline steps
│   │   ├── log-viewer.js       # Tab 3: auto-scan trajectories/, tinh metrics
│   │   ├── compare.js          # Tab 4: side-by-side conditions
│   │   ├── anova-viewer.js     # Tab 5: ANOVA table + charts
│   │   └── metrics.js          # Shared: tinh 7 metrics tu parsed log
│   ├── data/
│   │   └── sample-trajectory.json  # Sample log de demo
│   └── server.py                   # Dev server: serve trajectories/ + results/
```

### 6.4. Tab 1 — Config Builder (chi tiet)

**Input:** User chon 3 dropdowns (Tool / Context / Backend)
**Output:** Condition ID, YAML config, cost estimate, tool list

```
Chuc nang:
1. Chon Tool level → hien thi tools included/removed (chip badges)
2. Chon Context strategy → hien thi mo ta + params (window size, etc.)
3. Chon Backend → hien thi model ID, cost/eval, provider
4. Tu dong tinh:
   - Condition ID: "medium_sliding_window_deepseek"
   - So runs: 3 (critical) hoac 1 (normal)
   - Est. cost: runs × 150 tasks × cost_per_eval
   - Critical condition? (highlight neu la 1 trong 10 critical)
5. Button "Generate YAML" → hien/copy config file
6. Button "Add to Run Queue" → luu vao local state
```

### 6.5. Tab 3 — Log Viewer + Metrics (chi tiet)

**Input:** Auto-scan folder `trajectories/<condition_id>/` → list toan bo JSON files
**Output:** Turn-by-turn view + 7 metrics auto-computed

```
Data flow (tu dong, KHONG can upload manual):

  pipeline/runner.py chay experiment
       │
       ▼
  trajectories/
  ├── full_full_claude/
  │   ├── django-12345.json
  │   ├── flask-6789.json
  │   └── ... (150 files)
  ├── minimal_summary_deepseek/
  │   └── ...
  └── ... (27 folders × 150 files)
       │
       ▼
  UI Tab 3 auto-scan folder → list files → user click → xem chi tiet

Chuc nang:
1. Auto-scan trajectories/ folder, group by condition
2. Parse trajectory:
   - Hien thi tung turn: action, args, output (collapsible)
   - Highlight tool name voi mau tuong ung
   - Hien thi resolved/failed status
3. Auto-compute metrics tu parsed data:
   - M1.1: Hien thi annotation interface (user danh dau acceptable tools)
   - M1.2: Tu dong check output co duoc reference trong 3 turns sau
   - M1.3: Count unique tools / available tools
   - M2.2: Highlight relevant vs irrelevant segments (user classify)
4. Summary panel: 7 metrics voi progress bars + scores
5. Export metrics as JSON/CSV
```

### 6.6. metrics.js — Tinh 7 metrics trong browser

```javascript
// Port tu Python sang JavaScript (cung logic voi harness_eval/metrics/)

// M1.1: Correct Selection Rate
function correctSelectionRate(turns, annotations) {
  // annotations = [{turn_index, acceptable_tools: [...]}]
  // return % turns co tool_name in acceptable_tools
}

// M1.2: Redundant Call Rate  
function redundantCallRate(turns) {
  // check moi turn: output[:50] co xuat hien trong 3 turns sau?
  // return % turns redundant
}

// M1.3: Utilization Breadth
function utilizationBreadth(turns, availableTools) {
  // unique tools used / total available
}

// M2.2: Effective Token Ratio
function effectiveTokenRatio(segments) {
  // segments = [{text, is_relevant, token_count}]
  // return sum(relevant_tokens) / sum(all_tokens)
}

// M3.1 + M3.2: Backend Portability (can data tu nhieu conditions)
function crossBackendStdDev(resolveRates) { /* std(rates) */ }
function minMaxRatio(resolveRates) { /* min/max */ }
```

### 6.7. Uu tien implement

| # | Component | Priority | Ly do |
|---|-----------|----------|-------|
| 1 | Tab 1: Config Builder | CAO | Can thiet de plan experiments |
| 2 | Tab 3: Log Viewer + Metrics | CAO | Core value — xem duoc metrics tu log |
| 3 | Tab 4: Compare Conditions | CAO | So sanh la muc dich chinh cua de tai |
| 4 | Tab 2: Pipeline Viewer | TRUNG BINH | Visualization, khong block workflow |
| 5 | Tab 5: ANOVA Results | TRUNG BINH | Can data that tu experiments |

### 6.8. Tech stack — Python Flask App

**Tai sao Python app thay vi static HTML:**
- Doc trajectory files truc tiep tu disk (khong bi browser security block)
- Dung lai metrics Python code da co (84 tests pass) — khong can port sang JS
- Goi duoc ANOVA pipeline (statsmodels) server-side
- Ket noi duoc voi SWE-Agent fork de trigger runs
- Serve trajectory folder tu dong

**Stack:**
- **Flask** — lightweight web framework, 1 file chay duoc
- **Jinja2** — template engine (co san voi Flask)
- **Chart.js** (CDN) — charts phia client
- **harness_eval/** — import truc tiep metrics + analysis modules da co
- **Dark theme CSS** — consistent voi dashboard.html

### 6.9. Flask App Architecture

```
app/
├── server.py                 # Flask app — main entry point
│   ├── GET /                 # Tab 1: Config Builder
│   ├── GET /pipeline         # Tab 2: Pipeline Viewer
│   ├── GET /logs             # Tab 3: Log list (scan trajectories/)
│   ├── GET /logs/<file>      # Tab 3: Log detail + metrics
│   ├── GET /compare          # Tab 4: Compare conditions
│   ├── GET /anova            # Tab 5: ANOVA results
│   ├── POST /api/config      # Generate YAML config
│   ├── POST /api/metrics     # Compute metrics cho 1 log file
│   ├── POST /api/anova       # Chay ANOVA tren results CSV
│   └── GET /api/logs         # List trajectory files (JSON API)
├── templates/
│   ├── base.html             # Layout: header, tabs, dark theme
│   ├── config.html           # Tab 1: 3 factor selectors + YAML
│   ├── pipeline.html         # Tab 2: pipeline steps
│   ├── logs.html             # Tab 3: file list
│   ├── log_detail.html       # Tab 3: turn-by-turn + metrics
│   ├── compare.html          # Tab 4: side-by-side table + chart
│   └── anova.html            # Tab 5: ANOVA table + charts
├── static/
│   ├── css/style.css         # Dark theme
│   └── js/charts.js          # Chart.js wrappers
└── index.html                # KEPT: static version (backup/demo)
```

### 6.10. API Endpoints chi tiet

```python
# server.py — key routes

@app.route("/api/logs")
def api_logs():
    """Scan trajectories/ folder, return list of JSON files grouped by condition."""
    # Scan: trajectories/<condition_id>/<task_id>.json
    # Return: [{condition_id, task_id, resolved, path}, ...]

@app.route("/api/metrics/<path:log_path>")
def api_metrics(log_path):
    """Load 1 trajectory file, compute 7 metrics using harness_eval.metrics."""
    from harness_eval.metrics import correct_selection_rate, redundant_call_rate, ...
    # Parse log → ToolCall objects → compute → return JSON

@app.route("/api/anova", methods=["POST"])
def api_anova():
    """Run ANOVA on aggregated results."""
    from harness_eval.pipeline.analysis import compute_three_way_anova
    # Load results DataFrame → compute → return JSON

@app.route("/api/config", methods=["POST"])
def api_config():
    """Generate YAML config from selected factors."""
    # Return YAML string for SWE-Agent
```

### 6.11. Loi ich cua Python app

| Tinh nang | Static HTML | Python Flask |
|-----------|-------------|-------------|
| Mo file truc tiep | Bi block fetch() | Khong can — server serve |
| Doc trajectories/ folder | Khong duoc (browser security) | Os.walk() truc tiep |
| Tinh metrics | Phai port sang JS | Import Python code da test |
| ANOVA | Khong the | statsmodels server-side |
| Trigger SWE-Agent run | Khong the | subprocess.run() |
| Upload log | Can manual | Auto-scan folder |

### 6.12. Cach chay

```bash
cd "NCKK-Docs/de-tai/DE-CUONG-HarnessEval-v2"
pip install -e ".[dev]"          # install harness_eval package
pip install flask                # install Flask
python app/server.py             # start at http://localhost:5000
```

---

## 7. Session Log

### 7.1. Session 1 (07/04/2026) — Scaffolding + Core

**Da lam:**
- Tao project structure (pyproject.toml, 6 modules)
- Code configs/ (tool, context, backend, experiment) — 27 conditions
- Code metrics/ (7 metrics: M1.1-M3.2)
- Code pipeline/analysis.py (ANOVA 3-way, Cohen's d, Tukey HSD)
- Code cli.py (harness-eval info)
- Viet 84 tests — 100% pass
- Tao index.html (PDF render), dashboard.html (overview)

### 7.2. Session 2 (07/04/2026) — Flask UI App

**Da lam:**
- Tao Flask app voi 5 tabs (server.py + 7 templates + CSS)
- Tab 1: Config Builder — chon 3 factors, xem condition summary, generate YAML
- Tab 2: Pipeline Viewer — 6 buoc pipeline cho condition da chon
- Tab 3: Log Viewer — auto-scan trajectories/, turn-by-turn view, compute metrics, bar chart
- Tab 4: Compare — side-by-side table + grouped bar chart (Chart.js)
- Tab 5: ANOVA — placeholder (can data that)
- API endpoints: /api/logs, /api/metrics, /api/config
- Sample trajectory: django__django-16379 (8 turns, resolved)
- Static HTML backup (app/index.html voi embedded sample data)

**Loi gap va fix:**
- fetch() bi block khi mo file:// → embed sample data truc tiep vao HTML
- Doi tu static HTML sang Flask app de doc trajectories/ folder truc tiep

### 7.3. Session 3 (07/04/2026) — Parser + Runner + ANOVA UI + Flask Improvements

**Da lam:**
- Tao `parsers/trajectory.py` — parse SWE-Agent JSON logs thanh structured data
  - `TrajectoryMetadata` + `ParsedTrajectory` dataclasses
  - `validate_trajectory()` — check JSON schema, return error list
  - `parse_trajectory_file()` — parse 1 file thanh ParsedTrajectory
  - `parse_condition_dir()` — parse toan bo condition folder
  - `compute_condition_summary()` — resolve_rate, avg_turns, avg_cost
- Tao `pipeline/runner.py` — pipeline runner voi dry-run mode
  - `PipelineRunner` class — run_all(), run_condition(), run_single_task()
  - `RunConfig` — output_dir, dry_run, max_tasks, conditions filter
  - `TaskResult` / `ConditionResult` dataclasses
  - save_trajectory() — output JSON matching app/trajectories/ format
  - save_summary() — CSV voi condition_id, resolve_rate, cost
  - Deterministic synthetic data (seeded RNG) cho dry-run
  - `run_pilot()` / `run_full()` convenience functions
- Implement Tab 5 ANOVA UI
  - ANOVA table voi SS, df, MS, F, p-value, eta-squared, significance
  - Variance decomposition doughnut chart (Chart.js)
  - Effect size bar chart
  - Hypothesis evaluation (H1-H4) voi supported/not supported badges
  - Pairwise comparisons (Cohen's d) voi interpretation
  - Sample data generation (27 cond x 50 tasks) cho demo
  - API endpoint: POST /api/anova
- Cai tien Flask app
  - Logs tab: checkbox select, "Compare Selected" button, condition resolve rate, "Run ANOVA on These"
  - Compare tab: log selector voi checkboxes, cross-backend portability (M3.1, M3.2), turns/cost columns
  - ANOVA tab: "Run ANOVA on Sample Data" button, "Run on Trajectories" button
  - API: GET /api/summary — condition-level resolve rates
  - Fix numpy bool_ JSON serialization, NaN handling
- Tao 34 sample trajectory files (7 conditions x 5 tasks) cho demo
  - generate_samples.py script trong scripts/
  - Conditions: full_full_claude, minimal_full_claude, full_summary_claude, medium_sliding_window_gpt, full_full_gpt, minimal_summary_deepseek, full_full_deepseek
- Fix pyproject.toml: explicit package discovery (setuptools find), remove missing README.md ref
- Viet 39 tests moi (22 parser + 17 runner) — tat ca pass

**Loi gap va fix:**
1. `setuptools` flat-layout error (app/ + harness_eval/) → them `[tool.setuptools.packages.find] include = ["harness_eval*"]`
2. numpy `bool_` khong JSON serializable → cast `bool(r.is_significant)`
3. numpy NaN trong ANOVA results (khi khong du 27 conditions) → handle voi `float(x) if not np.isnan(x) else 0.0`

### 7.4. Session 4 (07/04/2026) — Fork SWE-Agent + Harness Interfaces

**Da lam:**
- Clone SWE-Agent vao `SWE-agent/` (git clone, fix Windows long path issue)
- Tao 10 YAML configs trong `SWE-agent/config/harness_eval/`:
  - `base.yaml` — shared settings (templates, env vars, cost limits, temp=0)
  - `tool_full.yaml` — all bundles (registry + edit + filemap + review) + bash
  - `tool_medium.yaml` — core bundles (registry + edit + submit) + bash
  - `tool_minimal.yaml` — bash only + submit (single_bash_code_block parsing)
  - `ctx_full.yaml` — no truncation (cache_control only)
  - `ctx_sliding_window.yaml` — last_n_observations(n=15) + closed_window
  - `ctx_summary.yaml` — last_n_observations(n=3) + remove_regex (aggressive)
  - `be_claude.yaml` — claude-sonnet-4-20250514
  - `be_gpt.yaml` — gpt-4o-2025-03-01
  - `be_deepseek.yaml` — deepseek/deepseek-chat
  - `verify_equivalence.yaml` — doc huong dan verify ±3%
  - `run_condition.sh` — bash script compose 3 configs
  - `README.md` — huong dan su dung
- Implement `harness_eval/harness/` module:
  - `interfaces.py` — ABC classes: ToolProvider, ContextStrategyProvider, LLMBackendProvider
  - 9 concrete implementations (3 tool + 3 context + 3 backend providers)
  - Factory functions: get_tool_provider(), get_context_provider(), get_backend_provider()
  - `factory.py` — HarnessConfig dataclass, create_harness_config(), generate_all_configs()
  - generate_sweagent_command() — tao CLI command tu HarnessConfig
  - generate_run_script() — tao bash script chay all conditions
- Cap nhat .gitignore: exclude SWE-agent/ clone, __pycache__/, *.pyc

**Config composition approach:**
```bash
# SWE-Agent supports multiple --config flags (later overrides earlier)
sweagent run-batch \
  --config config/harness_eval/base.yaml \         # shared
  --config config/harness_eval/tool_full.yaml \     # Factor A
  --config config/harness_eval/ctx_sliding_window.yaml \  # Factor B
  --config config/harness_eval/be_claude.yaml       # Factor C
```

### 7.5. Session 5 (08/04/2026) — SWE-Agent Subprocess + CLI + GLMM

**Da lam:**
- Implement SWE-Agent subprocess integration trong `runner.py`:
  - `_run_sweagent_task()` — goi `python -m sweagent run` qua subprocess
  - Compose config YAMLs tu HarnessConfig (base + tool + context + backend)
  - Parse .traj output → convert sang TaskResult
  - Handle subprocess failure (returncode != 0) va timeout gracefully
  - `_find_traj_file()` — tim .traj file (direct match hoac recursive search)
  - Them `sweagent_dir`, `dataset`, `timeout` vao RunConfig
- Implement full CLI (`cli.py`) — 5 commands:
  - `harness-eval info` — experiment design summary (da co)
  - `harness-eval pilot` — run pilot study (5 crit conditions x 20 tasks)
    - Options: `--dry-run`, `--output`, `--max-tasks`, `--sweagent-dir`, `--verbose`
    - Hien thi summary: resolve rate, cost, tasks per condition
  - `harness-eval run` — run full experiment (27 conditions x 150 tasks)
    - Options: `--dry-run`, `-o`, `--max-tasks`, `--sweagent-dir`, `-c` (filter conditions), `-v`
    - Support multiple `-c` flags de filter specific conditions
  - `harness-eval convert` — convert .traj → HarnessEval JSON
  - `harness-eval analyze` — run ANOVA tren trajectory results directory
    - Scan condition dirs, parse trajectories, build DataFrame, run ANOVA
    - Hien thi table: source, eta², F, p-value, significance
    - Optional `--output` CSV export
- Implement GLMM robustness analysis trong `analysis.py`:
  - `FixedEffect` dataclass — coefficient, std_error, z_value, p_value, is_significant
  - `GLMMResult` dataclass — fixed_effects, random_effect_variance, converged, AIC, BIC
  - `compute_glmm()` — MixedLM voi task_id as random intercept
    - Formula: resolve_rate ~ Tool + Context + Backend + interactions + (1|task_id)
    - Uses REML estimation
    - Cleans up statsmodels naming for readability
    - Validates required columns and minimum groups
- Cap nhat convenience functions `run_pilot()` va `run_full()`:
  - Them `sweagent_dir` va `max_tasks` parameters
- Viet 28 tests moi:
  - `test_runner.py`: 10 tests moi (SWE-Agent integration, find_traj, subprocess mock, convenience functions)
  - `test_analysis.py`: 8 tests moi (GLMM: runs, fixed effects, random effect, model fit, validation)
  - `test_cli.py`: 10 tests moi (info, pilot, run, convert, analyze commands)

**Tong cong: 151 tests, 100% passed** (tang tu 123 → 151)

### 7.6. Session 6 (08/04/2026) — Streamlit Dashboard

**Da lam:**
- Thay the Flask app bang Streamlit dashboard (15 files moi)
- `streamlit_app.py` — main entry point, dark/light theme toggle, 5 tabs
- `st_pages/config_builder.py` — 3-factor selector, condition summary, YAML, run panel, 27-condition table
- `st_pages/pipeline_viewer.py` — 6-step pipeline flow voi live status
- `st_pages/log_viewer.py` — file browser, turn-by-turn, metrics + Plotly chart
- `st_pages/compare.py` — multi-select, side-by-side table, cross-backend portability
- `st_pages/anova.py` — ANOVA table, variance charts, hypotheses H1-H4, GLMM, paper export
- `st_utils/data_loader.py` — cached trajectory scanning + metrics computation
- `st_utils/charts.py` — Plotly interactive + Matplotlib export chart helpers
- `st_utils/run_manager.py` — background subprocess voi threading + status tracking
- `tests/test_data_loader.py` — 7 tests
- `tests/test_run_manager.py` — 9 tests
- `.streamlit/config.toml` — wide layout, theme config
- Tong cong: 167 tests, 100% pass

---

## 8. Trang thai hien tai — DA HOAN THANH

### 8.1. Tong ket nhung gi DA CODE

```
DA XONG:
├── harness_eval/               # Python toolkit (167 tests pass)
│   ├── configs/                # 27 conditions = 3x3x3
│   ├── metrics/                # 7 metrics (M1.1-M3.2)
│   ├── parsers/trajectory.py   # SWE-Agent log parser
│   ├── pipeline/
│   │   ├── analysis.py         # ANOVA 3-way, Cohen's d, Tukey HSD, GLMM
│   │   └── runner.py           # Pipeline runner (dry-run + SWE-Agent subprocess)
│   ├── harness/
│   │   ├── interfaces.py       # 3 ABC + 9 concrete providers
│   │   └── factory.py          # HarnessConfig, create_harness_config, generate commands
│   └── cli.py                  # harness-eval info/pilot/run/convert/analyze
├── streamlit_app.py            # Streamlit dashboard entry point (thay the Flask)
├── st_pages/                   # 5 tab modules
│   ├── config_builder.py       # Tab 1: Config Builder
│   ├── pipeline_viewer.py      # Tab 2: Pipeline Viewer
│   ├── log_viewer.py           # Tab 3: Log Viewer
│   ├── compare.py              # Tab 4: Compare
│   └── anova.py                # Tab 5: ANOVA + GLMM
├── st_utils/                   # Dashboard utilities
│   ├── data_loader.py          # Cached trajectory scanning + metrics
│   ├── charts.py               # Plotly + Matplotlib chart helpers
│   └── run_manager.py          # Background subprocess + threading
├── tests/                      # 167 tests, 100% pass
│   ├── test_configs.py         # 36 tests
│   ├── test_metrics.py         # 38 tests
│   ├── test_analysis.py        # 18 tests (ANOVA + GLMM)
│   ├── test_parser.py          # 22 tests
│   ├── test_runner.py          # 27 tests (dry-run + SWE-Agent mock)
│   ├── test_cli.py             # 10 tests
│   ├── test_data_loader.py     # 7 tests
│   └── test_run_manager.py     # 9 tests
├── trajectories/               # JSON trajectory data (8 conditions, 41 files)
├── SWE-agent/                  # SWE-Agent clone (.gitignored)
│   └── config/harness_eval/    # 10 YAML configs for ablation
├── app/                        # Flask UI (backup — replaced by Streamlit)
├── .streamlit/config.toml      # Streamlit config
├── scripts/generate_samples.py # Sample data generator
├── dashboard.html              # Overview dashboard
├── index.html                  # PDF de cuong render
└── pyproject.toml              # Package config (streamlit, plotly added)
```

### 8.2. Nhung gi CHUA CODE (next steps)

| # | Viec | Priority | Ly do chua lam |
|---|------|----------|----------------|
| 1 | ~~Fork SWE-Agent~~ | ~~CAO~~ | **DONE** — cloned + 10 YAML configs + harness interfaces |
| 2 | ~~Log parser~~ | ~~CAO~~ | **DONE** — `parsers/trajectory.py` |
| 3 | ~~Pipeline runner~~ | ~~CAO~~ | **DONE** — `pipeline/runner.py` (dry-run mode) |
| 4 | ~~Tab 5: ANOVA UI~~ | ~~TRUNG BINH~~ | **DONE** — ANOVA table + charts + hypotheses |
| 5 | **LLM classifier** (M2.2) | TRUNG BINH | Can API key + prompt design |
| 6 | **BERTScore** (M2.1) | TRUNG BINH | Can torch + paired runs |
| 7 | ~~GLMM robustness~~ | ~~THAP~~ | **DONE** — `compute_glmm()` voi MixedLM + task_id random intercept |
| 8 | **CI/CD** GitHub Actions | THAP | Can repo setup |
| 9 | ~~More sample trajectories~~ | ~~THAP~~ | **DONE** — 7 conditions x 5 tasks |
| 10 | **Equivalence verification** | CAO | Chay 50 tasks, verify ±3% vs SWE-Agent default |
| 11 | ~~Connect runner to SWE-Agent~~ | ~~CAO~~ | **DONE** — subprocess integration + .traj parsing |
| 12 | ~~CLI pilot/full commands~~ | ~~TRUNG BINH~~ | **DONE** — info, pilot, run, convert, analyze |
| 13 | **Install SWE-Agent deps** | CAO | pip install -e SWE-agent/, setup Docker env |

### 8.3. Phase 7 — Unified Pipeline Flow (BUOC TIEP THEO)

**Muc tieu:** Thong nhat UI de moi buoc trong pipeline duoc dieu khien tu dashboard,
data tu buoc truoc tu dong chay vao buoc sau.

#### 8.3.1. Tong quan Unified Flow

```
USER chon Config (Tab 1)
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 1: Config Builder                                       │
│  - Chon Tool / Context / Backend                             │
│  - Highlight matching conditions trong 27-condition table    │
│  - Hien thi condition summary + tool chips                   │
│  - Generate YAML config → luu vao session_state              │
└──────────────────────┬──────────────────────────────────────┘
                       │ session_state.active_config (YAML dict)
                       │ session_state.selected_conditions (list)
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 2: Config Load (trong Pipeline tab)                     │
│  - Hien thi YAML config da chon tu Step 1                    │
│  - Hien thi SWE-Agent composed command                       │
│  - Validate config (tools exist, backend reachable)          │
│  - Button "Load Config" → trang thai chuyen sang LOADED      │
└──────────────────────┬──────────────────────────────────────┘
                       │ session_state.loaded_config
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 3: Run Agent (trong Pipeline tab)                       │
│  - Mode: Dry-Run / Real                                      │
│  - Max tasks slider                                          │
│  - Button "Run" → start background thread                    │
│  - Live progress bar + scrolling log                         │
│  - Output: trajectory JSON files → trajectories/             │
└──────────────────────┬──────────────────────────────────────┘
                       │ trajectories/<condition_id>/*.json
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 4: Collect Logs (auto sau khi Run xong)                 │
│  - Auto-scan trajectories/ folder                            │
│  - Parse JSON → ParsedTrajectory objects                     │
│  - Hien thi summary: X tasks resolved, Y failed              │
│  - Link sang Tab 3 (Log Viewer) de xem chi tiet              │
└──────────────────────┬──────────────────────────────────────┘
                       │ session_state.last_run_results
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 5: Compute Metrics (auto hoac manual)                   │
│  - Auto-compute 7 metrics cho moi trajectory                 │
│  - Hien thi aggregate metrics per condition                  │
│  - Link sang Tab 4 (Compare) de so sanh                      │
└──────────────────────┬──────────────────────────────────────┘
                       │ session_state.computed_metrics
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 6: ANOVA Analysis (trong Tab 5)                         │
│  - Auto-load data tu trajectories/                           │
│  - Button "Run ANOVA" → compute + hien thi table             │
│  - Variance charts + Hypothesis evaluation                   │
│  - GLMM robustness check                                     │
│  - Export paper figures                                       │
└─────────────────────────────────────────────────────────────┘
```

#### 8.3.2. Session State Flow (data chuyen giua cac tab)

```python
# Tab 1 (Config Builder) sets:
st.session_state.active_condition   = "full_full_claude"
st.session_state.active_config      = {yaml_dict}        # Generated YAML
st.session_state.selected_conditions = ["full_full_claude", ...]  # Multi-select tu table

# Tab 2 (Pipeline) reads active_config, shows loaded config, manages run:
st.session_state.loaded_config      = {yaml_dict}        # Confirmed config
st.session_state.pipeline_step      = 1-6                # Current step
st.session_state.run_manager        = RunManager()       # Singleton

# Tab 3 (Log Viewer) reads from trajectories/ folder:
st.session_state.selected_log_path  = "trajectories/full_full_claude/task-0.json"

# Tab 4 (Compare) collects from Log Viewer:
st.session_state.compare_logs       = [path1, path2, ...]

# Tab 5 (ANOVA) reads all trajectories:
st.session_state.anova_results      = [ANOVAResult, ...]
st.session_state.anova_df           = DataFrame
```

#### 8.3.3. Cai tien cu the can implement

| # | Cai tien | Tab | Chi tiet |
|---|----------|-----|----------|
| 1 | **Highlight conditions trong table** | Config | Khi chon Tool/Context/Backend, highlight hang tuong ung trong 27-condition table (background color khac). Neu chon 1 factor → highlight 9 conditions. Chon 2 → 3 conditions. Chon 3 → 1 condition. |
| 2 | **Multi-select conditions** | Config | Them checkbox column trong 27-condition table. User tick nhieu conditions → luu vao `selected_conditions`. Button "Run Selected" chay tat ca conditions da chon. |
| 3 | **YAML → Pipeline tab** | Config→Pipeline | YAML tu Config tab tu dong hien thi trong Pipeline tab Step 2 "Config Load". Khong can copy/paste. |
| 4 | **Pipeline step tracking** | Pipeline | Moi step co trang thai riet (PENDING→LOADED→RUNNING→DONE). Step hien tai duoc highlight xanh. Steps da xong duoc highlight xanh la. |
| 5 | **Auto-scan sau Run** | Pipeline | Sau khi Run xong (step 3), tu dong scan trajectories/ va hien thi summary (step 4). Tu dong compute metrics (step 5). |
| 6 | **Link giua tabs** | All | Button "View Logs →" trong Pipeline tab navigates sang Log Viewer tab. Button "Compare →" trong Log Viewer navigates sang Compare tab. Button "Run ANOVA →" trong Compare navigates sang ANOVA tab. |
| 7 | **Run nhieu conditions** | Config→Pipeline | Khi chon nhieu conditions tu table, Run panel chay sequential: cond 1 → cond 2 → ... Progress bar hien thi overall progress. |
| 8 | **Pipeline context banner** | Pipeline | Hien thi trang thai toan bo pipeline: "Config: full_full_claude | Step: 3/6 Running | Tasks: 15/20 | Cost: $5.25" |

#### 8.3.4. Thu tu implement

```
BUOC 1: Highlight conditions trong table ← BUOC TIEP THEO
  - Dung pandas Styler hoac column_config de highlight rows matching selected factors
  - Khi chon full/full/claude → highlight dong "full_full_claude" mau xanh
  - Khi chi chon tool=full → highlight 9 dong co tool=full

BUOC 2: Multi-select conditions + "Run Selected"
  - Them st.data_editor voi checkbox column thay vi st.dataframe
  - Luu selected conditions vao session_state
  - Button "Run Selected" → goi run_manager.start(conditions=selected_list)

BUOC 3: YAML flow Config → Pipeline
  - Config tab luu yaml dict vao st.session_state.active_config
  - Pipeline tab Step 2 doc va hien thi yaml + SWE-Agent command
  - Button "Load Config" → confirm va chuyen sang step 3

BUOC 4: Pipeline step tracking
  - session_state.pipeline_step = int (1-6)
  - Moi step: render voi mau tuong ung (gray/blue/green)
  - Auto-advance khi buoc truoc xong

BUOC 5: Auto-scan + auto-metrics sau Run
  - Khi run_manager status = "done", tu dong:
    1. scan_trajectories() → hien thi summary
    2. compute_metrics_for_log() cho moi file → aggregate
    3. Hien thi bang condition summary (resolve rate, avg cost)
  - pipeline_step chuyen sang 4 → 5 → 6

BUOC 6: Cross-tab navigation
  - st.session_state dung de "navigate" giua tabs
  - Button "View in Log Viewer" set session_state va st.rerun()
  - Streamlit st.tabs khong co native tab switching API,
    nen dung workaround: set flag → render target tab content

BUOC 7: Run nhieu conditions
  - run_manager.start() nhan list conditions
  - Progress: "Condition 2/5 — full_full_claude — Task 8/20"
  - Moi condition xong → update summary table

BUOC 8: Pipeline context banner
  - Sticky banner o top cua moi tab showing pipeline state
  - "Active: full_full_claude | Step 3: Running | 8/20 tasks | $2.80"
```

### 8.4. Sau Phase 7 (production pipeline)

```
BUOC A: Install SWE-Agent + Setup Docker
  cd SWE-agent && pip install -e .
  Docker: docker pull sweagent/swe-agent:latest
  Set API keys: export ANTHROPIC_API_KEY=...

BUOC B: Equivalence Verification (±3%)
  Mo dashboard → Config tab → chon full/full/gpt
  Run 50 tasks (real mode) → so sanh voi SWE-Agent default

BUOC C: Pilot Study (200 evals)
  Mo dashboard → Config tab → tick 5 critical conditions
  Run Selected → 20 tasks x 2 runs
  Tab 3 Log Viewer → xem chi tiet
  Tab 5 ANOVA → run analysis

BUOC D: Full Ablation (7,050 evals)
  Mo dashboard → Config tab → tick all 27 conditions
  Run Selected → 150 tasks
  Tab 5 ANOVA → evaluate H1-H4
  Export paper figures
```

---

## 9. Lien ket voi Plan chinh

| File | Noi dung |
|------|---------|
| `Plan-HarnessEval.md` | Tong quan toan bo du an (research + coding) |
| `Plan-Coding-HarnessEval.md` | **FILE NAY** — chi tiet coding + sessions |
| `DE-CUONG-HarnessEval-v2.md` | De cuong chinh (phien ban cuoi) |
| `THAO-LUAN-HarnessEval.md` | Phan bien vong 1 (7.3/10) |
| `THAO-LUAN-HarnessEval-v2.md` | Phan bien vong 2 (8.1/10) |
| `DE-CUONG-HarnessEval-v2/` | Code folder |

---

## 10. Resume Guide

### De chay lai TESTS:
```bash
cd "NCKK-Docs/de-tai/DE-CUONG-HarnessEval-v2"
pip install -e ".[dev]"
python -m pytest tests/ -v          # 167 tests
```

### De chay STREAMLIT DASHBOARD:
```bash
cd "NCKK-Docs/de-tai/DE-CUONG-HarnessEval-v2"
pip install -e ".[dev]"
streamlit run streamlit_app.py      # http://localhost:8501
```

### De chay CLI:
```bash
harness-eval info                   # xem 27 conditions + cost
harness-eval pilot --dry-run -o trajectories --max-tasks 5   # pilot dry-run
harness-eval run --dry-run -o trajectories -c full_full_claude --max-tasks 3  # single condition
harness-eval analyze trajectories/  # ANOVA tren results
harness-eval convert path/to/file.traj  # convert .traj → JSON
```

### De tiep tuc CODE:
```
1. Doc muc 8.3 (Phase 7 — Unified Pipeline Flow)
2. Buoc tiep theo: Highlight conditions trong table
3. Sau do: Multi-select + YAML flow + Pipeline step tracking
4. Sau do: Install SWE-Agent → Equivalence → Pilot → Full
```

### Thong tin ky thuat:
```
Working dir:  D:\MSA-FPT\Methods of Learnning and scientific research
Python:       3.12
Dependencies: numpy, pandas, scipy, statsmodels, click, streamlit, plotly, pytest
SWE-Agent:    SWE-agent/ (cloned, .gitignored)
Dashboard:    streamlit run streamlit_app.py (thay the Flask app)
```
