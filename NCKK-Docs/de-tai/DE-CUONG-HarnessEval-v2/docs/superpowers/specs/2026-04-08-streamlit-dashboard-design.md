# HarnessEval Streamlit Dashboard — Design Spec

> **Date:** 2026-04-08
> **Status:** Approved
> **Replaces:** Flask app (`app/server.py` + `app/templates/`)

## 1. Overview

Single Streamlit app replacing the Flask UI. Provides interactive experiment management with 5 horizontal tabs: Config Builder, Pipeline Viewer, Log Viewer, Compare, and ANOVA. Imports directly from the `harness_eval` Python package (metrics, configs, analysis, parsers, runner).

**Key decisions:**
- Tabs ngang (not sidebar/multi-page)
- Both dry-run and real mode with live log
- Plotly for interactive charts, Matplotlib for paper-export figures
- Auto theme (dark/light toggle via session state + injected CSS)
- JSON files + `@st.cache_data` for data loading (no database)

## 2. File Structure

```
DE-CUONG-HarnessEval-v2/
├── streamlit_app.py              # Main entry point + tab routing + theme toggle
├── st_pages/
│   ├── __init__.py
│   ├── config_builder.py         # Tab 1: 3-factor selector + run panel
│   ├── pipeline_viewer.py        # Tab 2: pipeline steps + status
│   ├── log_viewer.py             # Tab 3: browse logs + turn-by-turn + metrics
│   ├── compare.py                # Tab 4: multi-select + side-by-side
│   └── anova.py                  # Tab 5: ANOVA table + charts + hypotheses + GLMM
├── st_utils/
│   ├── __init__.py
│   ├── data_loader.py            # Cached JSON loading, trajectory scanning
│   ├── charts.py                 # Plotly + Matplotlib chart helpers
│   └── run_manager.py            # Subprocess runner with threading
├── harness_eval/                 # (existing) Python toolkit — no changes
├── trajectories/                 # JSON data (symlink or copy from app/trajectories/)
└── .streamlit/
    └── config.toml               # Streamlit config (wide layout, theme defaults)
```

## 3. Main App (`streamlit_app.py`)

```python
# Responsibilities:
# 1. st.set_page_config(page_title="HarnessEval", layout="wide")
# 2. Theme toggle button (dark/light) in header
# 3. Inject CSS based on st.session_state.theme
# 4. Create 5 tabs via st.tabs()
# 5. Dispatch to st_pages/ modules
```

**Theme toggle:**
- `st.session_state.theme` defaults to "dark"
- Toggle button rendered in header area (st.columns for layout)
- Two CSS presets injected via `st.markdown(<style>..., unsafe_allow_html=True)`
- Dark theme matches Flask app colors (#0f1117 bg, #e4e6ed text, #4c8dff accent)
- Light theme: white bg, dark text, same accent colors

**Header layout:**
```
[HarnessEval v0.1.0 — Modular Harness Evaluation Toolkit]  [theme_toggle]
[Config Builder] [Pipeline] [Log Viewer] [Compare] [ANOVA]
```

## 4. Tab 1 — Config Builder (`st_pages/config_builder.py`)

### 4.1 Factor Selection (3 columns)

```
col1: Tool Level        col2: Context Strategy      col3: LLM Backend
  - Full (12 tools)       - Full History               - Claude Sonnet 4 ($0.35)
  - Medium (8 tools)      - Sliding Window (50K)       - GPT-4o ($0.30)
  - Minimal (5 tools)     - Summary / ACC (2K)         - DeepSeek-V3 ($0.15)
```

Each factor uses `st.radio()` in a styled container. Color-coded top borders (blue/purple/orange).

### 4.2 Active Condition Summary

Computed from selected factors:
- **Condition ID:** `{tool}_{context}_{backend}` (e.g., `full_full_claude`)
- **Critical badge:** green if in `CRITICAL_CONDITIONS`
- **Runs:** 3 (critical) or 1 (normal)
- **Cost estimate:** runs x 150 tasks x cost_per_eval
- **Tools included:** chip badges (green=included, gray+strikethrough=excluded)

Uses `st.metric()` cards and `st.markdown()` for chips.

### 4.3 Run Panel

Two columns: settings (left) + controls (right).

**Settings:**
- Mode toggle: `st.toggle("Dry Run", value=True)`
- Max tasks: `st.number_input(min=1, max=150, value=20)`
- SWE-Agent dir: `st.text_input()` (required if real mode)
- Condition filter: `st.multiselect()` from 27 conditions (default: active condition)

**Controls:**
- `st.button("Run")` — starts background thread
- `st.button("Stop")` — kills subprocess
- `st.progress()` — task progress bar
- `st.empty()` — live log container (auto-refreshes via `st.rerun()`)

### 4.4 YAML Config

- `st.button("Generate YAML")` → shows YAML in `st.code(yaml_str, language="yaml")`
- `st.download_button()` — download as .yaml file

### 4.5 27-Condition Table

- `st.dataframe()` with all 27 conditions
- Columns: condition_id, tool, context, backend, critical, runs, est_cost, status
- Status from scanned trajectories (Pending/Done with task count)
- Row highlighting for active condition
- Checkboxes for batch selection → "Run Selected" button

## 5. Tab 2 — Pipeline Viewer (`st_pages/pipeline_viewer.py`)

### 5.1 Pipeline Steps

6 columns showing the pipeline flow:

```
[Task Select] → [Config Load] → [Run Agent] → [Log Parse] → [Metric Calc] → [ANOVA]
   150 tasks      YAML config     SWE-Agent     JSON parse    7 scores       3-way
```

Each step is a card (st.container) with:
- Step number + icon
- Title + description
- Status badge: Pending (gray), Running (blue pulse), Done (green)

### 5.2 Active Run Status

If a run is active (from Config tab), shows:
- Current condition being processed
- Task progress (X/Y) with progress bar
- Estimated time remaining
- Link to live log (scrolls to Config tab run panel)

If no run active, shows the pipeline diagram as static reference.

## 6. Tab 3 — Log Viewer (`st_pages/log_viewer.py`)

### 6.1 File Browser (sidebar area)

```python
# Left column (narrow):
condition = st.selectbox("Condition", condition_list)
task = st.selectbox("Task", task_list_for_condition)
# Or: single selectbox with "condition/task" combined
```

Shows resolve rate per condition as subtitle. Grouped by condition_id.

### 6.2 Turn-by-Turn View (center)

For selected trajectory:
- **Header:** task_id, resolved badge, model, turns count, cost, condition_id
- **Turns:** `st.expander()` per turn, or list of styled containers
  - Turn number + action name (color-coded by tool type)
  - Args display
  - Correctness badge (if acceptable_tools available)
  - Output in `st.code()` block (collapsible)
  - Acceptable tools list

**Color coding by action type:**
- read/grep/glob/find → blue (information gathering)
- edit/write → purple (modification)
- bash/python/test_runner → green (execution)
- git_* → orange (version control)

### 6.3 Metrics Panel (right column)

For selected trajectory, compute and display:
- M1.1 Correct Selection Rate — progress bar + percentage
- M1.2 Redundant Call Rate — progress bar (inverted: lower is better)
- M1.3 Utilization Breadth — progress bar
- M2.2 Effective Token Ratio — progress bar
- Plotly horizontal bar chart of all metrics

Uses `st.metric()` or custom HTML with `st.markdown()`.

### 6.4 Actions

- "Add to Compare" button → appends to `st.session_state.compare_logs`
- "Export Metrics" → download as JSON/CSV

## 7. Tab 4 — Compare (`st_pages/compare.py`)

### 7.1 Log Selection

`st.multiselect("Select logs to compare", all_log_paths)` — pre-filled from session_state if coming from Log Viewer.

Option to select by condition (all logs in a condition) or individual logs.

### 7.2 Comparison Table

`st.dataframe()` or styled HTML table:

| Metric | full/full/claude | minimal/full/claude | full/summary/claude |
|--------|-----------------|--------------------|--------------------|
| Resolved | Yes | No | Yes |
| Turns | 8 | 12 | 6 |
| Cost | $0.35 | $0.28 | $0.31 |
| M1.1 | 89.2% | 91.0% | 88.5% |
| M1.2 | 8.3% | 15.7% | 9.1% |
| M1.3 | 45.2% | 72.0% | 44.8% |
| M2.2 | 78.3% | 77.9% | 52.4% |

Color-coded cells (green > 80%, orange 50-80%, red < 50%).

### 7.3 Cross-Backend Portability

If selected logs span multiple backends:
- M3.1 Cross-Backend StdDev
- M3.2 Min/Max Ratio
- Per-backend average resolve rate

### 7.4 Charts

- **Plotly grouped bar:** metrics across selected logs (interactive hover)
- **Plotly radar/spider:** optional toggle for radar chart view
- Cohen's d between selected pairs

### 7.5 Export

- `st.download_button()` — comparison table as CSV
- Matplotlib export for paper figures

## 8. Tab 5 — ANOVA (`st_pages/anova.py`)

### 8.1 Data Source

- `st.radio("Data source", ["Trajectory Data", "Sample Data"])`
- Trajectory Data: scans `trajectories/` dir, builds DataFrame
- Sample Data: generates synthetic 27-condition data (for demo)
- `st.button("Run ANOVA")` triggers `compute_three_way_anova()`

### 8.2 ANOVA Table

`st.dataframe()` with conditional formatting:

| Source | SS | df | MS | F | p-value | eta sq | Sig |
|--------|-----|-----|-----|-----|---------|--------|-----|
| Tool | ... | 2 | ... | 16.23 | <0.001 | 0.056 | *** |
| Context | ... | 2 | ... | 5.38 | 0.005 | 0.019 | ** |
| Backend | ... | 2 | ... | 2.17 | 0.116 | 0.008 | ns |
| ... | | | | | | | |
| Error | ... | ... | ... | — | — | 0.887 | |

Color coding: p < 0.001 green, p < 0.05 orange, else gray. eta sq > 0.06 blue, > 0.01 cyan, else gray.

### 8.3 Charts

- **Plotly doughnut:** variance decomposition (all sources)
- **Plotly horizontal bar:** effect sizes (eta squared percentages)
- **Plotly interaction plot:** Backend x Tool config (optional)

### 8.4 Hypothesis Evaluation

4 cards (H1-H4) with:
- Hypothesis text
- Evidence (eta sq values, percentages)
- Supported / Not Supported badge (green/red)

### 8.5 Pairwise Comparisons

- Tukey HSD results table
- Cohen's d for all factor-level pairs
- Color-coded: Large (>0.8) blue, Medium (0.5-0.8) green, Small (0.2-0.5) orange, Negligible (<0.2) gray

### 8.6 GLMM Robustness

- `st.toggle("Run GLMM")` — runs `compute_glmm()` on same data
- Shows: fixed effects table, random effect variance, convergence status
- Comparison with ANOVA results (do conclusions change?)

### 8.7 Export

- `st.download_button("Download ANOVA CSV")` — ANOVA results as CSV
- `st.button("Generate Paper Figures")` — Matplotlib publication-quality figures
  - Variance decomposition pie
  - Effect size forest plot
  - Interaction plots

## 9. Utilities

### 9.1 Data Loader (`st_utils/data_loader.py`)

```python
@st.cache_data(ttl=60)
def scan_trajectories(base_dir: Path) -> list[dict]:
    """Scan all condition dirs, return metadata list."""

@st.cache_data(ttl=60)
def load_trajectory(path: Path) -> ParsedTrajectory:
    """Parse single trajectory JSON."""

@st.cache_data
def compute_metrics_for_log(trajectory: dict) -> dict:
    """Compute 7 metrics from raw trajectory data."""

@st.cache_data(ttl=60)
def build_anova_dataframe(base_dir: Path) -> pd.DataFrame:
    """Load all trajectories, build DataFrame for ANOVA."""
```

### 9.2 Charts (`st_utils/charts.py`)

```python
# Plotly (interactive, shown in Streamlit)
def plotly_metrics_bar(metrics: dict, theme: str) -> go.Figure
def plotly_grouped_comparison(logs: list[dict], theme: str) -> go.Figure
def plotly_variance_pie(anova_results: list, theme: str) -> go.Figure
def plotly_effect_size_bar(anova_results: list, theme: str) -> go.Figure
def plotly_interaction_plot(df: DataFrame, theme: str) -> go.Figure

# Matplotlib (static, for paper export)
def mpl_variance_pie(anova_results: list) -> Figure
def mpl_effect_forest(cohens_d: dict) -> Figure
def mpl_interaction_plot(df: DataFrame) -> Figure
```

All chart functions accept `theme` parameter ("dark"/"light") to adjust colors.

### 9.3 Run Manager (`st_utils/run_manager.py`)

```python
class RunManager:
    """Manages background experiment runs."""

    def start(self, conditions, mode, max_tasks, sweagent_dir=None):
        """Start background thread for pipeline run."""

    def stop(self):
        """Kill current subprocess."""

    def get_status(self) -> dict:
        """Return {status, progress, logs, current_condition}."""

    def clear(self):
        """Reset state to idle."""
```

Uses `threading.Thread` for background execution. Stores state in a module-level dict (not session_state, since threads can't access it). Status polled via `st.rerun()` with `time.sleep(1)` guard.

**Dry-run mode:** Calls `run_pilot()` / `run_full()` with `dry_run=True` directly.
**Real mode:** Calls with `dry_run=False, sweagent_dir=path`.

## 10. Theme System

### 10.1 Toggle

```python
# In streamlit_app.py header:
col1, col2 = st.columns([10, 1])
with col1:
    st.title("HarnessEval")
with col2:
    if st.button("toggle_icon"):
        st.session_state.theme = "light" if current == "dark" else "dark"
```

### 10.2 CSS Injection

Two CSS strings: `DARK_CSS` and `LIGHT_CSS`. Injected via:
```python
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
```

**Dark palette:** bg=#0f1117, surface=#1e2130, text=#e4e6ed, accent=#4c8dff
**Light palette:** bg=#ffffff, surface=#f8f9fa, text=#1a1d29, accent=#4c8dff

### 10.3 Streamlit Config

```toml
# .streamlit/config.toml
[server]
headless = true

[theme]
primaryColor = "#4c8dff"

[browser]
gatherUsageStats = false
```

## 11. Dependencies

Add to `pyproject.toml`:
```
streamlit>=1.30
plotly>=5.18
```

Remove Flask dependency (no longer needed).

## 12. How to Run

```bash
cd "NCKK-Docs/de-tai/DE-CUONG-HarnessEval-v2"
pip install -e ".[dev]"
pip install streamlit plotly
streamlit run streamlit_app.py
```

## 13. Migration from Flask

1. Move `app/trajectories/` → `trajectories/` (or symlink)
2. Port Flask route logic to Streamlit tab modules
3. Port `compute_metrics_from_log()` from `server.py` to `st_utils/data_loader.py`
4. Port run thread logic to `st_utils/run_manager.py`
5. Keep `app/` folder as backup until Streamlit is verified
6. Update `Plan-Coding-HarnessEval.md` with new structure
