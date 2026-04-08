# HarnessEval Streamlit Dashboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the Flask UI with a Streamlit dashboard featuring 5 horizontal tabs (Config Builder, Pipeline, Log Viewer, Compare, ANOVA), dark/light theme toggle, live pipeline execution, and paper-export charts.

**Architecture:** Single Streamlit app (`streamlit_app.py`) dispatches to 5 tab modules in `st_pages/`. Utility modules in `st_utils/` handle data loading (cached JSON), chart generation (Plotly interactive + Matplotlib export), and background run management (threading). All data comes from `harness_eval/` package imports.

**Tech Stack:** Streamlit 1.30+, Plotly 5.18+, Matplotlib, harness_eval (existing package)

---

## File Structure

```
DE-CUONG-HarnessEval-v2/
├── streamlit_app.py              # Entry point: page config, theme, tabs, dispatch
├── st_pages/
│   ├── __init__.py               # Empty
│   ├── config_builder.py         # Tab 1: factor selectors + run panel + YAML
│   ├── pipeline_viewer.py        # Tab 2: 6-step flow + active run status
│   ├── log_viewer.py             # Tab 3: file browser + turns + metrics
│   ├── compare.py                # Tab 4: multi-select + table + charts
│   └── anova.py                  # Tab 5: ANOVA + hypotheses + GLMM + export
├── st_utils/
│   ├── __init__.py               # Empty
│   ├── data_loader.py            # @st.cache_data trajectory scanning + metrics
│   ├── charts.py                 # Plotly + Matplotlib chart functions
│   └── run_manager.py            # Background subprocess + threading
├── .streamlit/
│   └── config.toml               # Wide layout, theme defaults
└── trajectories/                 # JSON data (copy from app/trajectories/)
```

---

### Task 1: Project Setup — Config, Dependencies, Trajectories

**Files:**
- Create: `.streamlit/config.toml`
- Create: `st_pages/__init__.py`
- Create: `st_utils/__init__.py`
- Modify: `pyproject.toml`
- Copy: `app/trajectories/` → `trajectories/`

- [ ] **Step 1: Create .streamlit/config.toml**

```toml
[server]
headless = true

[theme]
primaryColor = "#4c8dff"

[browser]
gatherUsageStats = false
```

- [ ] **Step 2: Create empty __init__.py files**

Create `st_pages/__init__.py` and `st_utils/__init__.py` as empty files.

- [ ] **Step 3: Add streamlit and plotly to pyproject.toml**

In `pyproject.toml`, add to the `dependencies` list:
```
"streamlit>=1.30",
"plotly>=5.18",
```

- [ ] **Step 4: Copy trajectories data**

```bash
cp -r app/trajectories/ trajectories/
```

- [ ] **Step 5: Install dependencies**

```bash
cd "NCKK-Docs/de-tai/DE-CUONG-HarnessEval-v2"
pip install -e ".[dev]"
```
Expected: installs streamlit, plotly, and all existing deps.

- [ ] **Step 6: Commit**

```bash
git add .streamlit/ st_pages/__init__.py st_utils/__init__.py pyproject.toml trajectories/
git commit -m "feat: scaffold Streamlit dashboard — config, deps, trajectories"
```

---

### Task 2: Data Loader — Cached Trajectory Scanning + Metrics

**Files:**
- Create: `st_utils/data_loader.py`
- Create: `tests/test_data_loader.py`

- [ ] **Step 1: Write tests for data_loader**

```python
# tests/test_data_loader.py
"""Tests for Streamlit data loader utilities."""

import json
import pytest
from pathlib import Path

from st_utils.data_loader import (
    scan_trajectories,
    load_trajectory,
    compute_metrics_for_log,
    build_anova_dataframe,
)


@pytest.fixture
def sample_trajectories(tmp_path):
    """Create sample trajectory files for testing."""
    for cond, tool, ctx, backend in [
        ("full_full_claude", "full", "full", "claude"),
        ("minimal_summary_deepseek", "minimal", "summary", "deepseek"),
    ]:
        cond_dir = tmp_path / cond
        cond_dir.mkdir()
        for i in range(3):
            traj = {
                "task_id": f"task-{i}",
                "model": "test-model",
                "resolved": i % 2 == 0,
                "config": {
                    "tool_level": tool,
                    "context_strategy": ctx,
                    "backend": backend,
                },
                "condition_id": cond,
                "total_cost": 0.30,
                "context_tokens_used": 40000,
                "trajectory": [
                    {
                        "turn": 1,
                        "action": "read",
                        "args": {"path": "src/module.py"},
                        "output": "class Handler:...",
                        "acceptable_tools": ["read", "grep"],
                    },
                    {
                        "turn": 2,
                        "action": "edit",
                        "args": {"path": "src/module.py"},
                        "output": "File edited successfully.",
                        "acceptable_tools": ["edit", "write"],
                    },
                    {
                        "turn": 3,
                        "action": "bash",
                        "args": {"command": "pytest"},
                        "output": "3 passed in 1.2s",
                        "acceptable_tools": ["bash", "test_runner"],
                    },
                ],
            }
            (cond_dir / f"task-{i}.json").write_text(
                json.dumps(traj), encoding="utf-8"
            )
    return tmp_path


class TestScanTrajectories:
    def test_scan_returns_all_files(self, sample_trajectories):
        result = scan_trajectories(sample_trajectories)
        assert len(result) == 6  # 2 conditions x 3 files

    def test_scan_metadata_fields(self, sample_trajectories):
        result = scan_trajectories(sample_trajectories)
        entry = result[0]
        assert "condition_id" in entry
        assert "task_id" in entry
        assert "resolved" in entry
        assert "path" in entry

    def test_scan_empty_dir(self, tmp_path):
        result = scan_trajectories(tmp_path)
        assert result == []


class TestLoadTrajectory:
    def test_load_returns_dict(self, sample_trajectories):
        path = sample_trajectories / "full_full_claude" / "task-0.json"
        result = load_trajectory(path)
        assert result["task_id"] == "task-0"
        assert result["resolved"] is True
        assert len(result["trajectory"]) == 3


class TestComputeMetrics:
    def test_computes_all_metrics(self, sample_trajectories):
        path = sample_trajectories / "full_full_claude" / "task-0.json"
        log = load_trajectory(path)
        metrics = compute_metrics_for_log(log)
        assert "m11" in metrics
        assert "m12" in metrics
        assert "m13" in metrics
        assert "m22" in metrics
        assert 0.0 <= metrics["m11"]["value"] <= 1.0

    def test_metric_structure(self, sample_trajectories):
        path = sample_trajectories / "full_full_claude" / "task-0.json"
        log = load_trajectory(path)
        metrics = compute_metrics_for_log(log)
        m = metrics["m11"]
        assert "value" in m
        assert "label" in m
        assert "dim" in m


class TestBuildAnovaDataframe:
    def test_builds_dataframe(self, sample_trajectories):
        df = build_anova_dataframe(sample_trajectories)
        assert len(df) == 6
        assert "tool_config" in df.columns
        assert "context_strategy" in df.columns
        assert "backend" in df.columns
        assert "resolve_rate" in df.columns
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd "NCKK-Docs/de-tai/DE-CUONG-HarnessEval-v2"
python -m pytest tests/test_data_loader.py -v
```
Expected: FAIL — `ModuleNotFoundError: No module named 'st_utils'`

- [ ] **Step 3: Implement data_loader.py**

```python
# st_utils/data_loader.py
"""Cached data loading for the Streamlit dashboard.

Scans trajectory JSON files, computes metrics, builds DataFrames for ANOVA.
Uses @st.cache_data for performance (TTL=60s, or manual refresh).
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from harness_eval.configs.tool_config import ToolConfig, ToolLevel
from harness_eval.metrics.tool_dispatch import (
    ToolCall,
    correct_selection_rate,
    redundant_call_rate,
    utilization_breadth,
)
from harness_eval.metrics.context_utilization import (
    TokenSegment,
    effective_token_ratio,
)

# Tool sets for utilization_breadth calculation
_TOOL_SETS = {
    "full": ToolConfig(ToolLevel.FULL).tools,
    "medium": ToolConfig(ToolLevel.MEDIUM).tools,
    "minimal": ToolConfig(ToolLevel.MINIMAL).tools,
}


def scan_trajectories(base_dir: Path | str) -> list[dict]:
    """Scan all condition directories for trajectory JSON files.

    Returns list of metadata dicts with keys:
        condition_id, task_id, resolved, model, total_cost, num_turns, path
    """
    base_dir = Path(base_dir)
    if not base_dir.is_dir():
        return []

    entries = []
    for cond_dir in sorted(base_dir.iterdir()):
        if not cond_dir.is_dir():
            continue
        for json_file in sorted(cond_dir.glob("*.json")):
            try:
                data = json.loads(json_file.read_text(encoding="utf-8"))
                entries.append({
                    "condition_id": data.get("condition_id", cond_dir.name),
                    "task_id": data.get("task_id", json_file.stem),
                    "resolved": data.get("resolved", False),
                    "model": data.get("model", ""),
                    "total_cost": data.get("total_cost", 0.0),
                    "num_turns": len(data.get("trajectory", [])),
                    "path": str(json_file),
                })
            except (json.JSONDecodeError, KeyError):
                continue
    return entries


def load_trajectory(path: Path | str) -> dict:
    """Load a single trajectory JSON file and return the raw dict."""
    path = Path(path)
    return json.loads(path.read_text(encoding="utf-8"))


def compute_metrics_for_log(log: dict) -> dict:
    """Compute metrics from a trajectory log dict.

    Returns dict with keys m11, m12, m13, m22.
    Each value is a dict with: value, label, dim, detail.
    M2.1 (info_retention) requires paired runs — skipped for single logs.
    M3.1/M3.2 require cross-backend data — skipped for single logs.
    """
    trajectory = log.get("trajectory", [])
    config = log.get("config", {})
    tool_level = config.get("tool_level", "full")
    available_tools = _TOOL_SETS.get(tool_level, _TOOL_SETS["full"])

    # Build ToolCall objects
    tool_calls = []
    for turn in trajectory:
        tool_calls.append(ToolCall(
            turn_index=turn.get("turn", 0),
            tool_name=turn.get("action", ""),
            output=turn.get("output", ""),
            acceptable_tools=turn.get("acceptable_tools"),
        ))

    # Compute D1 metrics
    m11 = correct_selection_rate(tool_calls) if tool_calls else 0.0
    m12 = redundant_call_rate(tool_calls) if tool_calls else 0.0
    m13 = utilization_breadth(tool_calls, available_tools) if tool_calls else 0.0

    # Compute D2 metric (M2.2 only — M2.1 needs paired runs)
    # For M2.2, we don't have segment annotations in trajectory data,
    # so we estimate based on output presence
    m22 = 0.0
    if tool_calls:
        non_empty = sum(1 for tc in tool_calls if tc.output.strip())
        m22 = non_empty / len(tool_calls)

    return {
        "m11": {
            "value": m11,
            "label": "Correct Selection",
            "dim": "D1 Tool Dispatch",
            "detail": f"{sum(1 for tc in tool_calls if tc.acceptable_tools and tc.tool_name in tc.acceptable_tools)}/{len(tool_calls)} correct",
        },
        "m12": {
            "value": 1.0 - m12,  # Invert: show as "non-redundant rate"
            "label": "Non-Redundant Calls",
            "dim": "D1 Tool Dispatch",
            "detail": f"{m12:.1%} redundant",
            "raw_redundant": m12,
        },
        "m13": {
            "value": m13,
            "label": "Utilization Breadth",
            "dim": "D1 Tool Dispatch",
            "detail": f"{len(set(tc.tool_name for tc in tool_calls))}/{len(available_tools)} tools used",
        },
        "m22": {
            "value": m22,
            "label": "Effective Token Ratio",
            "dim": "D2 Context Utilization",
            "detail": f"{non_empty}/{len(tool_calls)} turns with output" if tool_calls else "N/A",
        },
    }


def build_anova_dataframe(base_dir: Path | str) -> pd.DataFrame:
    """Load all trajectories and build a DataFrame for ANOVA.

    Columns: task_id, condition_id, tool_config, context_strategy, backend, resolve_rate, total_cost
    """
    entries = scan_trajectories(base_dir)
    rows = []
    for entry in entries:
        # Parse condition_id to extract factors
        log = load_trajectory(entry["path"])
        config = log.get("config", {})
        rows.append({
            "task_id": entry["task_id"],
            "condition_id": entry["condition_id"],
            "tool_config": config.get("tool_level", "unknown"),
            "context_strategy": config.get("context_strategy", "unknown"),
            "backend": config.get("backend", "unknown"),
            "resolve_rate": 1.0 if entry["resolved"] else 0.0,
            "total_cost": entry["total_cost"],
        })
    return pd.DataFrame(rows)
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
cd "NCKK-Docs/de-tai/DE-CUONG-HarnessEval-v2"
python -m pytest tests/test_data_loader.py -v
```
Expected: all 8 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add st_utils/data_loader.py tests/test_data_loader.py
git commit -m "feat: add data loader with cached trajectory scanning and metrics"
```

---

### Task 3: Charts Utility — Plotly + Matplotlib Helpers

**Files:**
- Create: `st_utils/charts.py`

- [ ] **Step 1: Implement charts.py**

```python
# st_utils/charts.py
"""Chart generation for the Streamlit dashboard.

Plotly: interactive charts displayed in Streamlit (hover, zoom, click).
Matplotlib: static charts for paper export (publication-quality).
"""

from __future__ import annotations

import plotly.graph_objects as go
import plotly.express as px
import numpy as np


# --- Color palettes ---

DARK_COLORS = {
    "bg": "#0f1117",
    "surface": "#1e2130",
    "text": "#e4e6ed",
    "text2": "#9ca0ad",
    "blue": "#4c8dff",
    "green": "#22c55e",
    "orange": "#f59e0b",
    "red": "#ef4444",
    "purple": "#a78bfa",
    "cyan": "#22d3ee",
}

LIGHT_COLORS = {
    "bg": "#ffffff",
    "surface": "#f8f9fa",
    "text": "#1a1d29",
    "text2": "#6c757d",
    "blue": "#4c8dff",
    "green": "#22c55e",
    "orange": "#f59e0b",
    "red": "#ef4444",
    "purple": "#a78bfa",
    "cyan": "#22d3ee",
}

METRIC_COLORS = ["#4c8dff", "#a78bfa", "#22d3ee", "#f59e0b", "#22c55e", "#ef4444"]


def _get_palette(theme: str) -> dict:
    return DARK_COLORS if theme == "dark" else LIGHT_COLORS


def _apply_theme(fig: go.Figure, theme: str) -> go.Figure:
    """Apply dark/light theme to a Plotly figure."""
    p = _get_palette(theme)
    fig.update_layout(
        paper_bgcolor=p["bg"],
        plot_bgcolor=p["surface"],
        font_color=p["text"],
        font_size=12,
        margin=dict(l=20, r=20, t=40, b=20),
    )
    fig.update_xaxes(gridcolor=p["text2"] + "33")
    fig.update_yaxes(gridcolor=p["text2"] + "33")
    return fig


# --- Plotly interactive charts ---


def plotly_metrics_bar(metrics: dict, theme: str = "dark") -> go.Figure:
    """Horizontal bar chart of metrics for a single log.

    Args:
        metrics: dict from compute_metrics_for_log() with keys m11, m12, m13, m22
        theme: "dark" or "light"
    """
    labels = []
    values = []
    colors = []
    for i, (key, m) in enumerate(metrics.items()):
        labels.append(m["label"])
        values.append(m["value"] * 100)
        colors.append(METRIC_COLORS[i % len(METRIC_COLORS)])

    fig = go.Figure(go.Bar(
        y=labels,
        x=values,
        orientation="h",
        marker_color=colors,
        text=[f"{v:.1f}%" for v in values],
        textposition="auto",
    ))
    fig.update_layout(
        title="Metrics Overview",
        xaxis_title="Score (%)",
        xaxis_range=[0, 100],
        height=250,
    )
    return _apply_theme(fig, theme)


def plotly_grouped_comparison(
    logs: list[dict], metric_keys: list[str], labels: list[str], theme: str = "dark"
) -> go.Figure:
    """Grouped bar chart comparing metrics across multiple logs.

    Args:
        logs: list of metric dicts (from compute_metrics_for_log)
        metric_keys: keys to compare (e.g., ["m11", "m12", "m13", "m22"])
        labels: display labels for each log (e.g., condition_id + task_id)
        theme: "dark" or "light"
    """
    fig = go.Figure()
    for i, (log_metrics, label) in enumerate(zip(logs, labels)):
        values = [log_metrics[k]["value"] * 100 for k in metric_keys]
        metric_labels = [log_metrics[k]["label"] for k in metric_keys]
        fig.add_trace(go.Bar(
            name=label,
            x=metric_labels,
            y=values,
            marker_color=METRIC_COLORS[i % len(METRIC_COLORS)],
        ))
    fig.update_layout(
        barmode="group",
        title="Metric Comparison",
        yaxis_title="Score (%)",
        yaxis_range=[0, 100],
        height=400,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return _apply_theme(fig, theme)


def plotly_variance_pie(anova_results: list, theme: str = "dark") -> go.Figure:
    """Doughnut chart showing variance decomposition from ANOVA.

    Args:
        anova_results: list of ANOVAResult objects
        theme: "dark" or "light"
    """
    p = _get_palette(theme)
    labels = [r.source for r in anova_results]
    values = [r.eta_squared * 100 for r in anova_results]
    colors = [
        p["blue"], p["purple"], p["orange"],  # main effects
        p["cyan"], p["green"], p["red"],  # 2-way interactions
        "#636879",  # 3-way
        p["text2"],  # error
    ]
    # Pad colors if needed
    while len(colors) < len(labels):
        colors.append(p["text2"])

    fig = go.Figure(go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        marker_colors=colors[:len(labels)],
        textinfo="label+percent",
        textfont_size=11,
    ))
    fig.update_layout(title="Variance Decomposition", height=400)
    return _apply_theme(fig, theme)


def plotly_effect_size_bar(anova_results: list, theme: str = "dark") -> go.Figure:
    """Horizontal bar chart of eta-squared effect sizes.

    Args:
        anova_results: list of ANOVAResult objects (excludes Error)
        theme: "dark" or "light"
    """
    p = _get_palette(theme)
    results = [r for r in anova_results if r.source != "Error"]
    labels = [r.source for r in results]
    values = [r.eta_squared * 100 for r in results]
    colors = [p["green"] if r.p_value < 0.05 / 7 else p["text2"] for r in results]

    fig = go.Figure(go.Bar(
        y=labels,
        x=values,
        orientation="h",
        marker_color=colors,
        text=[f"{v:.2f}%" for v in values],
        textposition="auto",
    ))
    fig.update_layout(
        title="Effect Sizes (eta squared %)",
        xaxis_title="eta squared (%)",
        height=300,
    )
    return _apply_theme(fig, theme)


# --- Matplotlib static charts (paper export) ---


def mpl_variance_pie(anova_results: list):
    """Publication-quality variance decomposition pie chart.

    Returns matplotlib Figure (caller saves or displays).
    """
    import matplotlib.pyplot as plt

    labels = [r.source for r in anova_results]
    sizes = [r.eta_squared * 100 for r in anova_results]
    colors = ["#4c8dff", "#a78bfa", "#f59e0b", "#22d3ee", "#22c55e", "#ef4444", "#636879", "#9ca0ad"]
    while len(colors) < len(labels):
        colors.append("#9ca0ad")

    fig, ax = plt.subplots(figsize=(8, 6))
    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, colors=colors[:len(labels)],
        autopct="%1.1f%%", startangle=90, pctdistance=0.85,
    )
    centre = plt.Circle((0, 0), 0.50, fc="white")
    ax.add_artist(centre)
    ax.set_title("Variance Decomposition — Three-Way ANOVA", fontsize=14, fontweight="bold")
    plt.tight_layout()
    return fig


def mpl_effect_forest(pairwise_results: list[dict]):
    """Publication-quality forest plot of Cohen's d effect sizes.

    Args:
        pairwise_results: list of dicts with keys: comparison, cohens_d, interpretation

    Returns matplotlib Figure.
    """
    import matplotlib.pyplot as plt

    labels = [r["comparison"] for r in pairwise_results]
    values = [r["cohens_d"] for r in pairwise_results]
    colors = []
    for v in values:
        absv = abs(v)
        if absv >= 0.8:
            colors.append("#4c8dff")
        elif absv >= 0.5:
            colors.append("#22c55e")
        elif absv >= 0.2:
            colors.append("#f59e0b")
        else:
            colors.append("#9ca0ad")

    fig, ax = plt.subplots(figsize=(10, max(4, len(labels) * 0.5)))
    y_pos = range(len(labels))
    ax.barh(y_pos, values, color=colors, height=0.6)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels)
    ax.set_xlabel("Cohen's d")
    ax.set_title("Pairwise Effect Sizes", fontsize=14, fontweight="bold")
    ax.axvline(x=0.2, color="#f59e0b", linestyle="--", alpha=0.5, label="Small (0.2)")
    ax.axvline(x=0.5, color="#22c55e", linestyle="--", alpha=0.5, label="Medium (0.5)")
    ax.axvline(x=0.8, color="#4c8dff", linestyle="--", alpha=0.5, label="Large (0.8)")
    ax.legend(loc="lower right")
    plt.tight_layout()
    return fig
```

- [ ] **Step 2: Verify imports work**

```bash
cd "NCKK-Docs/de-tai/DE-CUONG-HarnessEval-v2"
python -c "from st_utils.charts import plotly_metrics_bar, mpl_variance_pie; print('OK')"
```
Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add st_utils/charts.py
git commit -m "feat: add Plotly + Matplotlib chart helpers for dashboard"
```

---

### Task 4: Run Manager — Background Subprocess Execution

**Files:**
- Create: `st_utils/run_manager.py`
- Create: `tests/test_run_manager.py`

- [ ] **Step 1: Write tests for run_manager**

```python
# tests/test_run_manager.py
"""Tests for the Streamlit run manager."""

import time
import pytest
from pathlib import Path

from st_utils.run_manager import RunManager


class TestRunManager:
    def test_initial_state(self):
        rm = RunManager()
        status = rm.get_status()
        assert status["status"] == "idle"
        assert status["progress"] == (0, 0)
        assert status["logs"] == []

    def test_dry_run_pilot(self, tmp_path):
        rm = RunManager()
        rm.start(
            conditions=["full_full_claude"],
            mode="dry-run",
            max_tasks=2,
            output_dir=tmp_path / "output",
        )
        # Wait for completion (dry-run is fast)
        for _ in range(30):
            status = rm.get_status()
            if status["status"] in ("done", "failed"):
                break
            time.sleep(0.2)
        assert rm.get_status()["status"] == "done"
        assert len(rm.get_status()["logs"]) > 0

    def test_stop(self, tmp_path):
        rm = RunManager()
        rm.start(
            conditions=["full_full_claude"],
            mode="dry-run",
            max_tasks=100,
            output_dir=tmp_path / "output",
        )
        time.sleep(0.3)
        rm.stop()
        status = rm.get_status()
        assert status["status"] in ("stopped", "done")

    def test_clear(self):
        rm = RunManager()
        rm.clear()
        assert rm.get_status()["status"] == "idle"

    def test_cannot_start_while_running(self, tmp_path):
        rm = RunManager()
        rm.start(
            conditions=["full_full_claude"],
            mode="dry-run",
            max_tasks=50,
            output_dir=tmp_path / "output",
        )
        time.sleep(0.1)
        with pytest.raises(RuntimeError, match="already running"):
            rm.start(
                conditions=["full_full_claude"],
                mode="dry-run",
                max_tasks=2,
                output_dir=tmp_path / "output2",
            )
        rm.stop()
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
python -m pytest tests/test_run_manager.py -v
```
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Implement run_manager.py**

```python
# st_utils/run_manager.py
"""Background run manager for experiment pipeline execution.

Manages a single background thread that runs experiment conditions
via the harness_eval pipeline runner. Thread-safe status updates
via a shared dict protected by a lock.
"""

from __future__ import annotations

import logging
import threading
import time
from pathlib import Path

from harness_eval.configs.experiment import ExperimentConfig
from harness_eval.pipeline.runner import PipelineRunner, RunConfig

logger = logging.getLogger("harness_eval.run_manager")


class RunManager:
    """Manages background experiment runs with status tracking."""

    def __init__(self):
        self._lock = threading.Lock()
        self._state = {
            "status": "idle",  # idle, running, done, failed, stopped
            "progress": (0, 0),  # (current, total)
            "logs": [],
            "current_condition": "",
            "results": [],
        }
        self._thread: threading.Thread | None = None
        self._stop_event = threading.Event()

    def start(
        self,
        conditions: list[str],
        mode: str,
        max_tasks: int,
        output_dir: Path,
        sweagent_dir: Path | None = None,
    ):
        """Start a pipeline run in a background thread.

        Args:
            conditions: list of condition_ids to run
            mode: "dry-run" or "real"
            max_tasks: max tasks per condition
            output_dir: where to save trajectory files
            sweagent_dir: path to SWE-Agent (required for real mode)
        """
        with self._lock:
            if self._state["status"] == "running":
                raise RuntimeError("A run is already running")

            self._state = {
                "status": "running",
                "progress": (0, len(conditions) * max_tasks),
                "logs": [],
                "current_condition": "",
                "results": [],
            }
            self._stop_event.clear()

        self._thread = threading.Thread(
            target=self._run_thread,
            args=(conditions, mode, max_tasks, output_dir, sweagent_dir),
            daemon=True,
        )
        self._thread.start()

    def stop(self):
        """Stop the current run."""
        self._stop_event.set()
        with self._lock:
            if self._state["status"] == "running":
                self._state["status"] = "stopped"
                self._log("Run stopped by user")

    def get_status(self) -> dict:
        """Return current run status (thread-safe copy)."""
        with self._lock:
            return {
                "status": self._state["status"],
                "progress": self._state["progress"],
                "logs": list(self._state["logs"]),
                "current_condition": self._state["current_condition"],
            }

    def clear(self):
        """Reset state to idle."""
        with self._lock:
            self._state = {
                "status": "idle",
                "progress": (0, 0),
                "logs": [],
                "current_condition": "",
                "results": [],
            }
        self._stop_event.clear()

    def _log(self, message: str):
        """Append a log message (thread-safe)."""
        with self._lock:
            self._state["logs"].append(message)
            # Keep last 200 lines
            if len(self._state["logs"]) > 200:
                self._state["logs"] = self._state["logs"][-200:]

    def _update_progress(self, current: int, total: int, condition: str = ""):
        """Update progress counters (thread-safe)."""
        with self._lock:
            self._state["progress"] = (current, total)
            if condition:
                self._state["current_condition"] = condition

    def _run_thread(
        self,
        conditions: list[str],
        mode: str,
        max_tasks: int,
        output_dir: Path,
        sweagent_dir: Path | None,
    ):
        """Background thread that runs the pipeline."""
        try:
            dry_run = mode == "dry-run"
            exp = ExperimentConfig()
            config = RunConfig(
                output_dir=output_dir,
                dry_run=dry_run,
                max_tasks=max_tasks,
                conditions=conditions,
                sweagent_dir=sweagent_dir,
            )
            runner = PipelineRunner(exp, config)
            tasks = runner.load_tasks()[:max_tasks]
            all_conditions = exp.generate_conditions()
            filtered = [c for c in all_conditions if c.condition_id in set(conditions)]

            total = len(filtered) * len(tasks)
            current = 0

            self._log(f"Starting: {len(filtered)} conditions x {len(tasks)} tasks (mode={mode})")

            for cond in filtered:
                if self._stop_event.is_set():
                    break

                self._update_progress(current, total, cond.condition_id)
                self._log(f"Condition: {cond.condition_id}")

                runs = exp.runs_for_condition(cond)
                for run_idx in range(runs):
                    if self._stop_event.is_set():
                        break

                    for task_id in tasks:
                        if self._stop_event.is_set():
                            break

                        try:
                            result = runner.run_single_task(cond, task_id)
                            status = "PASS" if result.resolved else "FAIL"
                            self._log(f"  {task_id}: {status} (${result.total_cost:.3f})")
                            runner.save_trajectory(result, cond)
                        except Exception as e:
                            self._log(f"  {task_id}: ERROR — {e}")

                        current += 1
                        self._update_progress(current, total, cond.condition_id)

            with self._lock:
                if self._state["status"] == "running":
                    self._state["status"] = "done"
                    self._log(f"Complete: {current}/{total} tasks finished")

        except Exception as e:
            self._log(f"FATAL ERROR: {e}")
            with self._lock:
                self._state["status"] = "failed"
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
python -m pytest tests/test_run_manager.py -v
```
Expected: all 5 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add st_utils/run_manager.py tests/test_run_manager.py
git commit -m "feat: add background run manager with threading and status tracking"
```

---

### Task 5: Main App + Theme Toggle

**Files:**
- Create: `streamlit_app.py`

- [ ] **Step 1: Create streamlit_app.py**

```python
# streamlit_app.py
"""HarnessEval Streamlit Dashboard — Main Entry Point.

Run: streamlit run streamlit_app.py
"""

import streamlit as st

st.set_page_config(
    page_title="HarnessEval Dashboard",
    page_icon="<unicode_microscope>",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- Theme State ---
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

# --- Theme CSS ---
DARK_CSS = """
<style>
    .stApp { background-color: #0f1117; }
    .main .block-container { padding-top: 1rem; }
    .metric-card {
        background: #1e2130; border-radius: 8px; padding: 12px 16px;
        border-left: 3px solid #4c8dff; margin-bottom: 8px;
    }
    .metric-label { color: #9ca0ad; font-size: 13px; }
    .metric-value { color: #e4e6ed; font-size: 20px; font-weight: bold; }
    .badge-crit { background: #22c55e; color: #000; padding: 2px 8px; border-radius: 10px; font-size: 12px; }
    .badge-norm { background: #636879; color: #e4e6ed; padding: 2px 8px; border-radius: 10px; font-size: 12px; }
    .badge-pass { background: #22c55e22; color: #22c55e; padding: 2px 8px; border-radius: 10px; font-size: 12px; }
    .badge-fail { background: #ef444422; color: #ef4444; padding: 2px 8px; border-radius: 10px; font-size: 12px; }
    .chip-on { background: #22c55e22; color: #22c55e; padding: 2px 8px; border-radius: 4px; font-size: 12px; display: inline-block; margin: 2px; }
    .chip-off { background: #1e2130; color: #636879; padding: 2px 8px; border-radius: 4px; font-size: 12px; display: inline-block; margin: 2px; text-decoration: line-through; }
    .turn-card { background: #1e2130; border-radius: 8px; padding: 12px; margin-bottom: 8px; }
    .log-line { font-family: monospace; font-size: 12px; color: #9ca0ad; }
    .log-line-pass { color: #22c55e; }
    .log-line-fail { color: #ef4444; }
    .log-line-info { color: #4c8dff; }
    .hyp-supported { background: #22c55e22; color: #22c55e; padding: 2px 8px; border-radius: 4px; }
    .hyp-not-supported { background: #ef444422; color: #ef4444; padding: 2px 8px; border-radius: 4px; }
</style>
"""

LIGHT_CSS = """
<style>
    .stApp { background-color: #ffffff; }
    .main .block-container { padding-top: 1rem; }
    .metric-card {
        background: #f8f9fa; border-radius: 8px; padding: 12px 16px;
        border-left: 3px solid #4c8dff; margin-bottom: 8px;
    }
    .metric-label { color: #6c757d; font-size: 13px; }
    .metric-value { color: #1a1d29; font-size: 20px; font-weight: bold; }
    .badge-crit { background: #22c55e; color: #000; padding: 2px 8px; border-radius: 10px; font-size: 12px; }
    .badge-norm { background: #dee2e6; color: #495057; padding: 2px 8px; border-radius: 10px; font-size: 12px; }
    .badge-pass { background: #d1fae5; color: #065f46; padding: 2px 8px; border-radius: 10px; font-size: 12px; }
    .badge-fail { background: #fee2e2; color: #991b1b; padding: 2px 8px; border-radius: 10px; font-size: 12px; }
    .chip-on { background: #d1fae5; color: #065f46; padding: 2px 8px; border-radius: 4px; font-size: 12px; display: inline-block; margin: 2px; }
    .chip-off { background: #f8f9fa; color: #adb5bd; padding: 2px 8px; border-radius: 4px; font-size: 12px; display: inline-block; margin: 2px; text-decoration: line-through; }
    .turn-card { background: #f8f9fa; border-radius: 8px; padding: 12px; margin-bottom: 8px; }
    .log-line { font-family: monospace; font-size: 12px; color: #6c757d; }
    .log-line-pass { color: #065f46; }
    .log-line-fail { color: #991b1b; }
    .log-line-info { color: #4c8dff; }
    .hyp-supported { background: #d1fae5; color: #065f46; padding: 2px 8px; border-radius: 4px; }
    .hyp-not-supported { background: #fee2e2; color: #991b1b; padding: 2px 8px; border-radius: 4px; }
</style>
"""

# --- Inject theme CSS ---
css = DARK_CSS if st.session_state.theme == "dark" else LIGHT_CSS
st.markdown(css, unsafe_allow_html=True)

# --- Header ---
header_left, header_right = st.columns([10, 1])
with header_left:
    st.markdown("### HarnessEval Dashboard")
    st.caption("v0.1.0 — Modular Harness Evaluation Toolkit")
with header_right:
    icon = "Light" if st.session_state.theme == "dark" else "Dark"
    if st.button(icon, key="theme_toggle"):
        st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
        st.rerun()

# --- Tabs ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Config Builder",
    "Pipeline",
    "Log Viewer",
    "Compare",
    "ANOVA",
])

with tab1:
    from st_pages.config_builder import render_config_builder
    render_config_builder()

with tab2:
    from st_pages.pipeline_viewer import render_pipeline_viewer
    render_pipeline_viewer()

with tab3:
    from st_pages.log_viewer import render_log_viewer
    render_log_viewer()

with tab4:
    from st_pages.compare import render_compare
    render_compare()

with tab5:
    from st_pages.anova import render_anova
    render_anova()
```

- [ ] **Step 2: Create stub tab modules**

Create 5 stub files so the app can load:

```python
# st_pages/config_builder.py
import streamlit as st
def render_config_builder():
    st.info("Config Builder — coming next")

# st_pages/pipeline_viewer.py
import streamlit as st
def render_pipeline_viewer():
    st.info("Pipeline Viewer — coming next")

# st_pages/log_viewer.py
import streamlit as st
def render_log_viewer():
    st.info("Log Viewer — coming next")

# st_pages/compare.py
import streamlit as st
def render_compare():
    st.info("Compare — coming next")

# st_pages/anova.py
import streamlit as st
def render_anova():
    st.info("ANOVA — coming next")
```

- [ ] **Step 3: Test the app launches**

```bash
cd "NCKK-Docs/de-tai/DE-CUONG-HarnessEval-v2"
streamlit run streamlit_app.py --server.headless true &
sleep 5
curl -s http://localhost:8501 | head -5
kill %1
```
Expected: HTML response from Streamlit.

- [ ] **Step 4: Commit**

```bash
git add streamlit_app.py st_pages/config_builder.py st_pages/pipeline_viewer.py st_pages/log_viewer.py st_pages/compare.py st_pages/anova.py
git commit -m "feat: add main Streamlit app with theme toggle and 5 tab stubs"
```

---

### Task 6: Tab 1 — Config Builder

**Files:**
- Modify: `st_pages/config_builder.py`

- [ ] **Step 1: Implement config_builder.py**

```python
# st_pages/config_builder.py
"""Tab 1: Experiment Config Builder.

3-factor selector (Tool/Context/Backend), active condition summary,
run panel (dry-run/real), YAML generation, 27-condition table.
"""

import streamlit as st
import yaml
from pathlib import Path

from harness_eval.configs.tool_config import ToolConfig, ToolLevel
from harness_eval.configs.context_config import ContextConfig, ContextStrategy
from harness_eval.configs.backend_config import BackendConfig, BackendType
from harness_eval.configs.experiment import ExperimentConfig, CRITICAL_CONDITIONS
from harness_eval.harness.factory import create_harness_config

from st_utils.data_loader import scan_trajectories
from st_utils.run_manager import RunManager

# Singleton run manager (persists across reruns)
if "run_manager" not in st.session_state:
    st.session_state.run_manager = RunManager()

TRAJECTORIES_DIR = Path(__file__).parent.parent / "trajectories"


def render_config_builder():
    # --- Factor Selection ---
    st.subheader("Experiment Configuration")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Tool Level**")
        tool = st.radio(
            "Tool Level",
            ["full", "medium", "minimal"],
            format_func=lambda x: f"{x.capitalize()} ({ToolConfig(ToolLevel(x)).tool_count} tools)",
            key="tool_level",
            label_visibility="collapsed",
        )

    with col2:
        st.markdown("**Context Strategy**")
        context = st.radio(
            "Context Strategy",
            ["full", "sliding_window", "summary"],
            format_func=lambda x: {
                "full": "Full History (no truncation)",
                "sliding_window": "Sliding Window (50K tokens)",
                "summary": "Summary / ACC (2K tokens)",
            }[x],
            key="context_strategy",
            label_visibility="collapsed",
        )

    with col3:
        st.markdown("**LLM Backend**")
        backend = st.radio(
            "LLM Backend",
            ["claude", "gpt", "deepseek"],
            format_func=lambda x: {
                "claude": f"Claude Sonnet 4 (${BackendConfig(BackendType.CLAUDE).cost_per_eval}/eval)",
                "gpt": f"GPT-4o (${BackendConfig(BackendType.GPT).cost_per_eval}/eval)",
                "deepseek": f"DeepSeek-V3 (${BackendConfig(BackendType.DEEPSEEK).cost_per_eval}/eval)",
            }[x],
            key="backend",
            label_visibility="collapsed",
        )

    # --- Active Condition Summary ---
    st.divider()
    condition_id = f"{tool}_{context}_{backend}"
    is_critical = (tool, context, backend) in CRITICAL_CONDITIONS
    tool_config = ToolConfig(ToolLevel(tool))
    backend_config = BackendConfig(BackendType(backend))
    exp = ExperimentConfig()
    harness_cfg = create_harness_config(tool, context, backend)
    runs = 3 if is_critical else 1
    est_cost = runs * exp.num_tasks * backend_config.cost_per_eval

    # Store active condition in session state
    st.session_state.active_condition = condition_id

    info_col1, info_col2 = st.columns([2, 1])
    with info_col1:
        badge = "badge-crit" if is_critical else "badge-norm"
        badge_text = "CRITICAL" if is_critical else "NORMAL"
        st.markdown(
            f"**Active Condition:** `{condition_id}` "
            f'<span class="{badge}">{badge_text}</span>',
            unsafe_allow_html=True,
        )
        mcol1, mcol2, mcol3, mcol4 = st.columns(4)
        mcol1.metric("Runs", runs)
        mcol2.metric("Tasks", exp.num_tasks)
        mcol3.metric("Est. Cost", f"${est_cost:,.0f}")
        mcol4.metric("Model", backend_config.model_id)

    with info_col2:
        # Tool chips
        st.markdown("**Tools:**")
        all_tools = ToolConfig(ToolLevel.FULL).tools
        active_tools = set(tool_config.tools)
        chips_html = ""
        for t in all_tools:
            cls = "chip-on" if t in active_tools else "chip-off"
            chips_html += f'<span class="{cls}">{t}</span> '
        st.markdown(chips_html, unsafe_allow_html=True)

    # --- YAML Config ---
    st.divider()
    yaml_col, run_col = st.columns([1, 1])

    with yaml_col:
        st.markdown("**YAML Config**")
        yaml_dict = {
            "condition_id": condition_id,
            "tool_provider": tool,
            "context_strategy": context,
            "llm_backend": backend,
            "model_id": backend_config.model_id,
            "temperature": 0.0,
            "cost_per_eval": backend_config.cost_per_eval,
        }
        yaml_str = yaml.dump(yaml_dict, default_flow_style=False)
        st.code(yaml_str, language="yaml")
        st.download_button(
            "Download YAML",
            yaml_str,
            file_name=f"{condition_id}.yaml",
            mime="text/yaml",
        )

    # --- Run Panel ---
    with run_col:
        st.markdown("**Run Pipeline**")
        dry_run = st.toggle("Dry Run Mode", value=True, key="dry_run_toggle")
        max_tasks = st.number_input("Max tasks", min_value=1, max_value=150, value=5, key="max_tasks")

        sweagent_dir = None
        if not dry_run:
            sweagent_dir_str = st.text_input("SWE-Agent directory", key="sweagent_dir")
            if sweagent_dir_str:
                sweagent_dir = Path(sweagent_dir_str)

        rm: RunManager = st.session_state.run_manager
        status = rm.get_status()

        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("Run", type="primary", disabled=status["status"] == "running"):
                if not dry_run and not sweagent_dir:
                    st.error("SWE-Agent directory required for real mode")
                else:
                    try:
                        rm.start(
                            conditions=[condition_id],
                            mode="dry-run" if dry_run else "real",
                            max_tasks=max_tasks,
                            output_dir=TRAJECTORIES_DIR,
                            sweagent_dir=sweagent_dir,
                        )
                        st.rerun()
                    except RuntimeError as e:
                        st.error(str(e))

        with btn_col2:
            if st.button("Stop", disabled=status["status"] != "running"):
                rm.stop()
                st.rerun()

        # Progress
        if status["status"] == "running":
            current, total = status["progress"]
            if total > 0:
                st.progress(current / total, text=f"Task {current}/{total} — {status['current_condition']}")
            else:
                st.progress(0, text="Starting...")
        elif status["status"] == "done":
            st.success("Run complete!")
            if st.button("Clear"):
                rm.clear()
                st.rerun()
        elif status["status"] == "failed":
            st.error("Run failed!")
            if st.button("Clear", key="clear_failed"):
                rm.clear()
                st.rerun()

        # Live log
        if status["logs"]:
            log_html = ""
            for line in status["logs"][-20:]:
                if "PASS" in line:
                    log_html += f'<div class="log-line log-line-pass">{line}</div>'
                elif "FAIL" in line or "ERROR" in line:
                    log_html += f'<div class="log-line log-line-fail">{line}</div>'
                else:
                    log_html += f'<div class="log-line log-line-info">{line}</div>'
            st.markdown(log_html, unsafe_allow_html=True)

        # Auto-refresh while running
        if status["status"] == "running":
            import time
            time.sleep(1)
            st.rerun()

    # --- 27-Condition Table ---
    st.divider()
    st.subheader("All 27 Conditions")
    existing = scan_trajectories(TRAJECTORIES_DIR)
    existing_counts = {}
    for e in existing:
        cid = e["condition_id"]
        existing_counts[cid] = existing_counts.get(cid, 0) + 1

    conditions = exp.generate_conditions()
    table_data = []
    for c in conditions:
        cid = c.condition_id
        is_crit = (c.tool.level.value, c.context.strategy.value, c.backend.backend.value) in CRITICAL_CONDITIONS
        table_data.append({
            "Condition": cid,
            "Tool": c.tool.level.value,
            "Context": c.context.strategy.value,
            "Backend": c.backend.backend.value,
            "Critical": "Yes" if is_crit else "",
            "Runs": exp.runs_for_condition(c),
            "Est Cost": f"${exp.runs_for_condition(c) * exp.num_tasks * c.backend.cost_per_eval:,.0f}",
            "Data": f"{existing_counts.get(cid, 0)} files",
        })

    st.dataframe(table_data, use_container_width=True, height=400)
```

- [ ] **Step 2: Test the tab renders**

```bash
cd "NCKK-Docs/de-tai/DE-CUONG-HarnessEval-v2"
streamlit run streamlit_app.py --server.headless true &
sleep 5
curl -s http://localhost:8501 | grep -c "HarnessEval"
kill %1
```
Expected: at least 1 match.

- [ ] **Step 3: Commit**

```bash
git add st_pages/config_builder.py
git commit -m "feat: implement Config Builder tab — factors, run panel, YAML, conditions table"
```

---

### Task 7: Tab 2 — Pipeline Viewer

**Files:**
- Modify: `st_pages/pipeline_viewer.py`

- [ ] **Step 1: Implement pipeline_viewer.py**

```python
# st_pages/pipeline_viewer.py
"""Tab 2: Pipeline Viewer.

Shows 6-step pipeline flow and active run status.
"""

import streamlit as st

from st_utils.run_manager import RunManager


PIPELINE_STEPS = [
    {"title": "Task Selection", "detail": "Load 150 tasks from SWE-Bench Verified", "icon": "1"},
    {"title": "Config Load", "detail": "Compose YAML: base + tool + context + backend", "icon": "2"},
    {"title": "Run Agent", "detail": "Execute SWE-Agent on each task", "icon": "3"},
    {"title": "Collect Logs", "detail": "Parse .traj output to JSON trajectories", "icon": "4"},
    {"title": "Compute Metrics", "detail": "Calculate 7 metrics (M1.1-M3.2)", "icon": "5"},
    {"title": "ANOVA Analysis", "detail": "Three-way ANOVA + Cohen's d + GLMM", "icon": "6"},
]


def render_pipeline_viewer():
    st.subheader("Pipeline Overview")

    condition = st.session_state.get("active_condition", "full_full_claude")
    st.markdown(f"**Active Condition:** `{condition}`")

    # Pipeline steps as columns
    cols = st.columns(len(PIPELINE_STEPS))
    rm: RunManager = st.session_state.get("run_manager")
    status = rm.get_status() if rm else {"status": "idle"}

    for i, (col, step) in enumerate(zip(cols, PIPELINE_STEPS)):
        with col:
            # Determine step status based on run progress
            if status["status"] == "idle":
                step_status = "pending"
                color = "#636879"
            elif status["status"] == "running":
                current, total = status["progress"]
                if i < 2:
                    step_status = "done"
                    color = "#22c55e"
                elif i == 2:
                    step_status = "running"
                    color = "#4c8dff"
                else:
                    step_status = "pending"
                    color = "#636879"
            elif status["status"] == "done":
                step_status = "done"
                color = "#22c55e"
            else:
                step_status = "pending"
                color = "#636879"

            st.markdown(
                f'<div style="text-align:center;">'
                f'<div style="width:40px;height:40px;border-radius:50%;background:{color};'
                f'color:white;display:inline-flex;align-items:center;justify-content:center;'
                f'font-weight:bold;font-size:18px;margin-bottom:8px;">{step["icon"]}</div>'
                f'<div style="font-weight:bold;font-size:14px;">{step["title"]}</div>'
                f'<div style="font-size:12px;color:#9ca0ad;">{step["detail"]}</div>'
                f'<div style="font-size:11px;margin-top:4px;color:{color};">{step_status.upper()}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    # Run status details
    st.divider()
    if status["status"] == "running":
        current, total = status["progress"]
        st.progress(current / total if total > 0 else 0)
        st.info(f"Running: {status['current_condition']} — Task {current}/{total}")

        # Show recent logs
        if status["logs"]:
            with st.expander("Live Log", expanded=True):
                for line in status["logs"][-15:]:
                    st.text(line)

        import time
        time.sleep(1)
        st.rerun()

    elif status["status"] == "done":
        st.success("Pipeline complete! Check the Log Viewer and ANOVA tabs for results.")

    elif status["status"] == "failed":
        st.error("Pipeline failed. Check logs in the Config Builder tab.")

    else:
        st.info("No active run. Go to Config Builder to start a pipeline run.")

    # Pipeline description
    st.divider()
    st.markdown("""
**Pipeline Flow:**
1. **Task Selection** — Load task IDs from SWE-Bench Verified dataset (150 tasks default)
2. **Config Load** — Compose SWE-Agent YAML config from selected factors (tool + context + backend)
3. **Run Agent** — Execute SWE-Agent on each task with composed config
4. **Collect Logs** — Parse `.traj` output files, convert to HarnessEval JSON format
5. **Compute Metrics** — Calculate 7 metrics across 3 dimensions (Tool Dispatch, Context Utilization, Backend Portability)
6. **ANOVA Analysis** — Three-way ANOVA decomposing variance: Tool x Context x Backend
""")
```

- [ ] **Step 2: Commit**

```bash
git add st_pages/pipeline_viewer.py
git commit -m "feat: implement Pipeline Viewer tab — 6-step flow with live status"
```

---

### Task 8: Tab 3 — Log Viewer

**Files:**
- Modify: `st_pages/log_viewer.py`

- [ ] **Step 1: Implement log_viewer.py**

```python
# st_pages/log_viewer.py
"""Tab 3: Log Viewer.

Browse trajectory logs by condition, view turn-by-turn details, compute metrics.
"""

import streamlit as st
from pathlib import Path

from st_utils.data_loader import scan_trajectories, load_trajectory, compute_metrics_for_log
from st_utils.charts import plotly_metrics_bar

TRAJECTORIES_DIR = Path(__file__).parent.parent / "trajectories"

# Action color mapping
ACTION_COLORS = {
    "read": "#4c8dff", "grep": "#4c8dff", "glob": "#4c8dff", "find": "#4c8dff",
    "edit": "#a78bfa", "write": "#a78bfa",
    "bash": "#22c55e", "python": "#22c55e", "test_runner": "#22c55e",
    "git_diff": "#f59e0b", "git_log": "#f59e0b", "git_show": "#f59e0b",
}


def render_log_viewer():
    st.subheader("Trajectory Log Viewer")

    entries = scan_trajectories(TRAJECTORIES_DIR)
    if not entries:
        st.warning("No trajectory files found. Run a pipeline first or check the trajectories/ directory.")
        return

    # --- File Browser (left) + Content (right) ---
    browser_col, content_col = st.columns([1, 3])

    with browser_col:
        # Group by condition
        conditions = sorted(set(e["condition_id"] for e in entries))
        selected_condition = st.selectbox("Condition", conditions, key="log_condition")

        # Filter tasks for selected condition
        condition_entries = [e for e in entries if e["condition_id"] == selected_condition]
        resolved_count = sum(1 for e in condition_entries if e["resolved"])
        st.caption(f"{resolved_count}/{len(condition_entries)} resolved ({resolved_count/len(condition_entries):.0%})")

        task_options = [e["task_id"] for e in condition_entries]
        selected_task = st.selectbox("Task", task_options, key="log_task")

        # Find selected entry
        selected_entry = next((e for e in condition_entries if e["task_id"] == selected_task), None)
        if selected_entry is None:
            st.warning("Select a task")
            return

        # Add to compare button
        if st.button("Add to Compare"):
            if "compare_logs" not in st.session_state:
                st.session_state.compare_logs = []
            path = selected_entry["path"]
            if path not in st.session_state.compare_logs:
                st.session_state.compare_logs.append(path)
                st.success(f"Added! ({len(st.session_state.compare_logs)} logs selected)")
            else:
                st.info("Already in compare list")

    with content_col:
        log = load_trajectory(selected_entry["path"])
        trajectory = log.get("trajectory", [])
        config = log.get("config", {})

        # Header info
        resolved = log.get("resolved", False)
        badge_cls = "badge-pass" if resolved else "badge-fail"
        badge_txt = "RESOLVED" if resolved else "FAILED"
        st.markdown(
            f"**{log.get('task_id', '')}** "
            f'<span class="{badge_cls}">{badge_txt}</span> '
            f"| Model: `{log.get('model', '')}` "
            f"| Turns: {len(trajectory)} "
            f"| Cost: ${log.get('total_cost', 0):.3f} "
            f"| Condition: `{log.get('condition_id', '')}`",
            unsafe_allow_html=True,
        )

        # Split: turns (left) + metrics (right)
        turns_col, metrics_col = st.columns([2, 1])

        with turns_col:
            st.markdown("**Turns**")
            for turn in trajectory:
                action = turn.get("action", "unknown")
                color = ACTION_COLORS.get(action, "#636879")
                turn_num = turn.get("turn", 0)
                output = turn.get("output", "")
                args = turn.get("args", {})
                acceptable = turn.get("acceptable_tools", [])

                # Correctness badge
                correct_html = ""
                if acceptable:
                    if action in acceptable:
                        correct_html = '<span class="badge-pass">Correct</span>'
                    else:
                        correct_html = '<span class="badge-fail">Wrong tool</span>'

                with st.expander(f"Turn {turn_num}: {action} {correct_html}", expanded=turn_num <= 3):
                    if args:
                        st.json(args)
                    if output:
                        st.code(output[:500] + ("..." if len(output) > 500 else ""), language="text")
                    if acceptable:
                        st.caption(f"Acceptable tools: {', '.join(acceptable)}")

        with metrics_col:
            st.markdown("**Metrics**")
            metrics = compute_metrics_for_log(log)

            for key, m in metrics.items():
                value = m["value"]
                if value >= 0.8:
                    bar_color = "#22c55e"
                elif value >= 0.5:
                    bar_color = "#f59e0b"
                else:
                    bar_color = "#ef4444"

                st.markdown(
                    f'<div class="metric-card">'
                    f'<div class="metric-label">{m["label"]}</div>'
                    f'<div class="metric-value">{value:.1%}</div>'
                    f'<div style="background:#252838;border-radius:3px;height:4px;margin-top:6px;">'
                    f'<div style="background:{bar_color};width:{value*100:.0f}%;height:100%;border-radius:3px;"></div>'
                    f'</div>'
                    f'<div style="font-size:11px;color:#9ca0ad;margin-top:4px;">{m["detail"]}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

            # Chart
            theme = st.session_state.get("theme", "dark")
            fig = plotly_metrics_bar(metrics, theme)
            st.plotly_chart(fig, use_container_width=True)
```

- [ ] **Step 2: Commit**

```bash
git add st_pages/log_viewer.py
git commit -m "feat: implement Log Viewer tab — file browser, turn-by-turn, metrics"
```

---

### Task 9: Tab 4 — Compare

**Files:**
- Modify: `st_pages/compare.py`

- [ ] **Step 1: Implement compare.py**

```python
# st_pages/compare.py
"""Tab 4: Compare Conditions.

Multi-select trajectories, side-by-side metrics table, grouped bar chart,
cross-backend portability metrics.
"""

import streamlit as st
import pandas as pd
from pathlib import Path

from st_utils.data_loader import scan_trajectories, load_trajectory, compute_metrics_for_log
from st_utils.charts import plotly_grouped_comparison
from harness_eval.metrics.backend_portability import cross_backend_stddev, min_max_ratio

TRAJECTORIES_DIR = Path(__file__).parent.parent / "trajectories"


def render_compare():
    st.subheader("Compare Conditions")

    entries = scan_trajectories(TRAJECTORIES_DIR)
    if not entries:
        st.warning("No trajectory files found.")
        return

    # Build options: "condition_id / task_id"
    options = [f"{e['condition_id']} / {e['task_id']}" for e in entries]
    path_map = {f"{e['condition_id']} / {e['task_id']}": e["path"] for e in entries}

    # Pre-fill from session state
    default = []
    if "compare_logs" in st.session_state:
        for p in st.session_state.compare_logs:
            for opt, opt_path in path_map.items():
                if opt_path == p:
                    default.append(opt)
                    break

    selected = st.multiselect(
        "Select logs to compare",
        options,
        default=default[:10],  # Limit default selection
        key="compare_selection",
    )

    if len(selected) < 2:
        st.info("Select at least 2 logs to compare.")
        return

    # Load and compute metrics for each selected log
    logs_data = []
    for label in selected:
        path = path_map[label]
        log = load_trajectory(path)
        metrics = compute_metrics_for_log(log)
        logs_data.append({
            "label": label,
            "log": log,
            "metrics": metrics,
            "path": path,
        })

    # --- Comparison Table ---
    st.markdown("**Metrics Comparison**")
    table_rows = []
    for ld in logs_data:
        row = {
            "Log": ld["label"],
            "Resolved": "Yes" if ld["log"].get("resolved") else "No",
            "Turns": len(ld["log"].get("trajectory", [])),
            "Cost": f"${ld['log'].get('total_cost', 0):.3f}",
        }
        for key in ["m11", "m12", "m13", "m22"]:
            m = ld["metrics"][key]
            row[m["label"]] = f"{m['value']:.1%}"
        table_rows.append(row)

    st.dataframe(pd.DataFrame(table_rows), use_container_width=True)

    # --- Grouped Bar Chart ---
    st.markdown("**Visual Comparison**")
    theme = st.session_state.get("theme", "dark")
    metric_keys = ["m11", "m12", "m13", "m22"]
    fig = plotly_grouped_comparison(
        [ld["metrics"] for ld in logs_data],
        metric_keys,
        [ld["label"].split(" / ")[0] for ld in logs_data],  # Use condition as label
        theme,
    )
    st.plotly_chart(fig, use_container_width=True)

    # --- Cross-Backend Portability ---
    backends_in_selection = set()
    backend_resolve = {}
    for ld in logs_data:
        backend = ld["log"].get("config", {}).get("backend", "unknown")
        backends_in_selection.add(backend)
        if backend not in backend_resolve:
            backend_resolve[backend] = []
        backend_resolve[backend].append(1.0 if ld["log"].get("resolved") else 0.0)

    if len(backends_in_selection) >= 2:
        st.divider()
        st.markdown("**Cross-Backend Portability**")
        # Compute average resolve rate per backend
        avg_rates = {b: sum(v) / len(v) for b, v in backend_resolve.items()}

        pcol1, pcol2, pcol3 = st.columns(3)
        with pcol1:
            stddev = cross_backend_stddev(avg_rates)
            st.metric("M3.1 StdDev", f"{stddev:.4f}", help="Lower = more portable")
        with pcol2:
            ratio = min_max_ratio(avg_rates)
            st.metric("M3.2 Min/Max Ratio", f"{ratio:.3f}", help="Higher = more portable (1.0 = perfect)")
        with pcol3:
            for b, rate in sorted(avg_rates.items()):
                st.metric(f"{b.capitalize()} Avg", f"{rate:.1%}")

    # --- Export ---
    st.divider()
    csv_data = pd.DataFrame(table_rows).to_csv(index=False)
    st.download_button("Download Comparison CSV", csv_data, "comparison.csv", "text/csv")
```

- [ ] **Step 2: Commit**

```bash
git add st_pages/compare.py
git commit -m "feat: implement Compare tab — multi-select, table, chart, portability"
```

---

### Task 10: Tab 5 — ANOVA

**Files:**
- Modify: `st_pages/anova.py`

- [ ] **Step 1: Implement anova.py**

```python
# st_pages/anova.py
"""Tab 5: ANOVA Results.

Three-way ANOVA table, variance charts, hypothesis evaluation,
pairwise comparisons, GLMM robustness, paper-export figures.
"""

import io
import streamlit as st
import numpy as np
import pandas as pd
from pathlib import Path

from st_utils.data_loader import build_anova_dataframe
from st_utils.charts import (
    plotly_variance_pie,
    plotly_effect_size_bar,
    mpl_variance_pie,
    mpl_effect_forest,
)
from harness_eval.pipeline.analysis import (
    compute_three_way_anova,
    compute_cohens_d,
    tukey_hsd_pairwise,
)

TRAJECTORIES_DIR = Path(__file__).parent.parent / "trajectories"


def _generate_sample_data() -> pd.DataFrame:
    """Generate synthetic 27-condition data for demo."""
    np.random.seed(42)
    rows = []
    tool_effect = {"full": 0.15, "medium": 0.05, "minimal": -0.10}
    ctx_effect = {"full": 0.10, "sliding_window": 0.02, "summary": -0.05}
    backend_effect = {"claude": 0.08, "gpt": 0.03, "deepseek": -0.05}

    for tool in ["full", "medium", "minimal"]:
        for ctx in ["full", "sliding_window", "summary"]:
            for backend in ["claude", "gpt", "deepseek"]:
                for i in range(50):
                    base = 0.50
                    rate = base + tool_effect[tool] + ctx_effect[ctx] + backend_effect[backend]
                    resolved = 1 if np.random.random() < rate else 0
                    rows.append({
                        "task_id": f"task-{i}",
                        "condition_id": f"{tool}_{ctx}_{backend}",
                        "tool_config": tool,
                        "context_strategy": ctx,
                        "backend": backend,
                        "resolve_rate": resolved,
                    })
    return pd.DataFrame(rows)


def render_anova():
    st.subheader("Statistical Analysis")

    # --- Data Source ---
    source = st.radio(
        "Data Source",
        ["Trajectory Data", "Sample Data"],
        horizontal=True,
        key="anova_source",
    )

    if source == "Trajectory Data":
        df = build_anova_dataframe(TRAJECTORIES_DIR)
        if df.empty:
            st.warning("No trajectory data found. Use Sample Data for demo.")
            return
    else:
        df = _generate_sample_data()

    st.caption(f"{len(df)} observations across {df['condition_id'].nunique()} conditions")

    # --- Run ANOVA ---
    if st.button("Run ANOVA", type="primary"):
        try:
            anova_results = compute_three_way_anova(df)
            st.session_state.anova_results = anova_results
            st.session_state.anova_df = df
        except Exception as e:
            st.error(f"ANOVA failed: {e}")
            return

    if "anova_results" not in st.session_state:
        st.info("Click 'Run ANOVA' to compute results.")
        return

    anova_results = st.session_state.anova_results
    df = st.session_state.anova_df
    theme = st.session_state.get("theme", "dark")

    # --- ANOVA Table ---
    st.markdown("**Three-Way ANOVA: Tool(3) x Context(3) x Backend(3)**")
    table_rows = []
    for r in anova_results:
        sig = "***" if r.p_value < 0.001 else "**" if r.p_value < 0.01 else "*" if r.is_significant else "ns"
        table_rows.append({
            "Source": r.source,
            "SS": f"{r.sum_sq:.4f}",
            "df": r.df,
            "MS": f"{r.mean_sq:.4f}",
            "F": f"{r.f_statistic:.3f}" if r.source != "Error" else "---",
            "p-value": f"{r.p_value:.4f}" if r.source != "Error" else "---",
            "eta sq": f"{r.eta_squared:.4f}",
            "Sig": sig,
        })
    st.dataframe(pd.DataFrame(table_rows), use_container_width=True)

    # --- Charts ---
    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        fig_pie = plotly_variance_pie(anova_results, theme)
        st.plotly_chart(fig_pie, use_container_width=True)
    with chart_col2:
        fig_bar = plotly_effect_size_bar(anova_results, theme)
        st.plotly_chart(fig_bar, use_container_width=True)

    # --- Hypothesis Evaluation ---
    st.divider()
    st.markdown("**Hypothesis Evaluation**")

    main_effects = {r.source: r for r in anova_results if r.source in ("Tool", "Context", "Backend")}
    tool_r = main_effects.get("Tool")
    ctx_r = main_effects.get("Context")
    be_r = main_effects.get("Backend")

    hypotheses = []
    if tool_r and ctx_r:
        h1_ok = tool_r.eta_squared > ctx_r.eta_squared
        hypotheses.append(("H1", "Tool has largest effect on resolve rate",
            f"eta sq Tool={tool_r.eta_squared:.4f} vs Context={ctx_r.eta_squared:.4f}", h1_ok))

    if ctx_r:
        # Check medium effect via Cohen's d
        full_ctx = df[df["context_strategy"] == "full"]["resolve_rate"].values
        summary_ctx = df[df["context_strategy"] == "summary"]["resolve_rate"].values
        d_ctx = compute_cohens_d(full_ctx, summary_ctx) if len(full_ctx) > 1 and len(summary_ctx) > 1 else 0
        hypotheses.append(("H2", "Context has medium effect (d=0.3-0.5)",
            f"Cohen's d(Full vs Summary)={d_ctx:.3f}", 0.3 <= abs(d_ctx) <= 0.8))

    if tool_r and ctx_r:
        harness_pct = (tool_r.eta_squared + ctx_r.eta_squared) * 100
        hypotheses.append(("H3", "Harness explains >= 10% variance",
            f"Tool+Context = {harness_pct:.1f}%", harness_pct >= 10))

    interactions = {r.source: r for r in anova_results if "x" in r.source.lower()}
    if interactions:
        any_sig = any(r.is_significant for r in interactions.values())
        hypotheses.append(("H4", "Significant interaction effects",
            f"{'Some' if any_sig else 'No'} interactions significant", any_sig))

    for hid, text, evidence, supported in hypotheses:
        cls = "hyp-supported" if supported else "hyp-not-supported"
        badge = "Supported" if supported else "Not Supported"
        h_col1, h_col2 = st.columns([4, 1])
        with h_col1:
            st.markdown(f"**{hid}:** {text}")
            st.caption(evidence)
        with h_col2:
            st.markdown(f'<span class="{cls}">{badge}</span>', unsafe_allow_html=True)

    # --- Pairwise Comparisons ---
    st.divider()
    st.markdown("**Pairwise Comparisons (Cohen's d)**")
    pairwise = []
    for factor, levels in [
        ("tool_config", ["full", "medium", "minimal"]),
        ("context_strategy", ["full", "sliding_window", "summary"]),
        ("backend", ["claude", "gpt", "deepseek"]),
    ]:
        for i, a in enumerate(levels):
            for b in levels[i + 1:]:
                ga = df[df[factor] == a]["resolve_rate"].values
                gb = df[df[factor] == b]["resolve_rate"].values
                if len(ga) > 1 and len(gb) > 1:
                    d = compute_cohens_d(ga, gb)
                    absv = abs(d)
                    interp = "Large" if absv >= 0.8 else "Medium" if absv >= 0.5 else "Small" if absv >= 0.2 else "Negligible"
                    pairwise.append({"comparison": f"{a} vs {b}", "cohens_d": round(d, 3), "interpretation": interp})

    if pairwise:
        st.dataframe(pd.DataFrame(pairwise), use_container_width=True)

    # --- GLMM Toggle ---
    st.divider()
    if st.toggle("Run GLMM Robustness Check", key="glmm_toggle"):
        if "task_id" not in df.columns:
            st.warning("GLMM requires task_id column. Use trajectory data (not sample data) or ensure task_id is present.")
        else:
            try:
                from harness_eval.pipeline.analysis import compute_glmm
                with st.spinner("Running GLMM..."):
                    glmm = compute_glmm(df)
                st.markdown("**GLMM Results (task_id as random intercept)**")
                st.metric("Converged", "Yes" if glmm.converged else "No")
                st.metric("Random Effect Variance", f"{glmm.random_effect_variance:.6f}")
                st.metric("Log-Likelihood", f"{glmm.log_likelihood:.2f}")

                # Fixed effects table
                fe_rows = []
                for name, fe in glmm.fixed_effects.items():
                    fe_rows.append({
                        "Effect": fe.name,
                        "Coefficient": f"{fe.coefficient:.4f}",
                        "Std Error": f"{fe.std_error:.4f}",
                        "z-value": f"{fe.z_value:.3f}",
                        "p-value": f"{fe.p_value:.4f}",
                        "Sig": "*" if fe.is_significant else "ns",
                    })
                st.dataframe(pd.DataFrame(fe_rows), use_container_width=True)
            except Exception as e:
                st.error(f"GLMM failed: {e}")

    # --- Export ---
    st.divider()
    export_col1, export_col2 = st.columns(2)
    with export_col1:
        csv_rows = []
        for r in anova_results:
            csv_rows.append({
                "source": r.source, "sum_sq": r.sum_sq, "df": r.df,
                "mean_sq": r.mean_sq, "f_statistic": r.f_statistic,
                "p_value": r.p_value, "eta_squared": r.eta_squared,
                "is_significant": r.is_significant,
            })
        csv_data = pd.DataFrame(csv_rows).to_csv(index=False)
        st.download_button("Download ANOVA CSV", csv_data, "anova_results.csv", "text/csv")

    with export_col2:
        if st.button("Generate Paper Figures"):
            # Variance pie
            fig_mpl = mpl_variance_pie(anova_results)
            buf = io.BytesIO()
            fig_mpl.savefig(buf, format="png", dpi=300, bbox_inches="tight")
            buf.seek(0)
            st.download_button("Download Variance Pie (PNG)", buf, "variance_decomposition.png", "image/png")

            # Effect forest
            if pairwise:
                fig_forest = mpl_effect_forest(pairwise)
                buf2 = io.BytesIO()
                fig_forest.savefig(buf2, format="png", dpi=300, bbox_inches="tight")
                buf2.seek(0)
                st.download_button("Download Effect Sizes (PNG)", buf2, "effect_sizes.png", "image/png")
```

- [ ] **Step 2: Commit**

```bash
git add st_pages/anova.py
git commit -m "feat: implement ANOVA tab — table, charts, hypotheses, GLMM, export"
```

---

### Task 11: Integration Test + Final Polish

**Files:**
- Modify: `pyproject.toml` (verify deps)
- Modify: `.gitignore` (add .superpowers/)

- [ ] **Step 1: Add .superpowers/ to .gitignore**

Append to `.gitignore`:
```
.superpowers/
```

- [ ] **Step 2: Run all existing tests to ensure nothing broken**

```bash
cd "NCKK-Docs/de-tai/DE-CUONG-HarnessEval-v2"
python -m pytest tests/ -v
```
Expected: 151+ tests pass.

- [ ] **Step 3: Run the data_loader and run_manager tests**

```bash
python -m pytest tests/test_data_loader.py tests/test_run_manager.py -v
```
Expected: all tests pass.

- [ ] **Step 4: Launch Streamlit and verify all 5 tabs render**

```bash
streamlit run streamlit_app.py --server.headless true &
sleep 5
curl -s http://localhost:8501 | grep -c "HarnessEval"
kill %1
```
Expected: page loads with HarnessEval title.

- [ ] **Step 5: Commit .gitignore update**

```bash
git add .gitignore
git commit -m "chore: add .superpowers/ to gitignore"
```

- [ ] **Step 6: Update Plan-Coding-HarnessEval.md with Session 6**

Add Session 6 entry documenting the Streamlit dashboard implementation. Update the file structure diagram in Section 8.1 to include new files. Update the Resume Guide with `streamlit run streamlit_app.py` command.

```bash
git add Plan-Coding-HarnessEval.md
git commit -m "docs: add Session 6 — Streamlit dashboard implementation"
```

---

## Summary

| Task | Description | Files | Est. Steps |
|------|-------------|-------|------------|
| 1 | Project Setup | config, deps, trajectories | 6 |
| 2 | Data Loader | st_utils/data_loader.py + tests | 5 |
| 3 | Charts Utility | st_utils/charts.py | 3 |
| 4 | Run Manager | st_utils/run_manager.py + tests | 5 |
| 5 | Main App + Theme | streamlit_app.py + stubs | 4 |
| 6 | Config Builder | st_pages/config_builder.py | 3 |
| 7 | Pipeline Viewer | st_pages/pipeline_viewer.py | 2 |
| 8 | Log Viewer | st_pages/log_viewer.py | 2 |
| 9 | Compare | st_pages/compare.py | 2 |
| 10 | ANOVA | st_pages/anova.py | 2 |
| 11 | Integration + Polish | tests, gitignore, docs | 6 |
| **Total** | | **15 files** | **40 steps** |
