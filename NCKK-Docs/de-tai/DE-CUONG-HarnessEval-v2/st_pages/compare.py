"""Compare tab — Tab 4 of HarnessEval Dashboard.

Provides:
  1. Multi-select trajectory log picker (pre-filled from session_state.compare_logs)
  2. Side-by-side metrics comparison table
  3. Grouped bar chart across selected logs
  4. Cross-backend portability metrics (M3.1, M3.2) when 2+ backends are selected
  5. CSV export of comparison table
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from st_utils.data_loader import compute_metrics_for_log, load_trajectory, scan_trajectories
from st_utils.charts import plotly_grouped_comparison
from st_utils.ui_helpers import render_pipeline_banner
from harness_eval.metrics.backend_portability import cross_backend_stddev, min_max_ratio

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

TRAJECTORIES_DIR = Path(__file__).parent.parent / "trajectories"

METRIC_KEYS = ["m11", "m12", "m13", "m22"]

METRIC_DISPLAY_NAMES: dict[str, str] = {
    "m11": "Correct Selection",
    "m12": "Non-Redundant Calls",
    "m13": "Utilization Breadth",
    "m22": "Effective Token Ratio",
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _option_label(item: dict) -> str:
    """Return 'condition_id / task_id' display string for a scanned item."""
    return f"{item['condition_id']} / {item['task_id']}"


def _non_redundant(m12_value: float) -> float:
    """Convert redundant-call rate to non-redundant rate (higher = better)."""
    return round(1.0 - m12_value, 4)


def _build_comparison_row(label: str, item: dict, log: dict, metrics: dict) -> dict:
    """Build a single row dict for the comparison DataFrame."""
    trajectory = log.get("trajectory", [])
    return {
        "Log": label,
        "Resolved": "Yes" if item["resolved"] else "No",
        "Turns": len(trajectory),
        "Cost ($)": round(float(log.get("total_cost", 0.0)), 4),
        "Correct Selection": f"{metrics['m11']['value'] * 100:.1f}%",
        "Non-Redundant Calls": f"{_non_redundant(metrics['m12']['value']) * 100:.1f}%",
        "Utilization Breadth": f"{metrics['m13']['value'] * 100:.1f}%",
        "Effective Token Ratio": f"{metrics['m22']['value'] * 100:.1f}%",
    }


# ---------------------------------------------------------------------------
# Main render function
# ---------------------------------------------------------------------------


def render_compare() -> None:
    theme = st.session_state.get("theme", "dark")

    st.markdown("#### Compare Trajectories")
    render_pipeline_banner()
    st.caption(
        "Select 2 or more trajectory logs to compare side-by-side metrics, "
        "view a grouped bar chart, and inspect cross-backend portability."
    )

    # ------------------------------------------------------------------
    # 1. Scan available trajectories
    # ------------------------------------------------------------------
    if not TRAJECTORIES_DIR.exists():
        st.warning(
            f"Trajectories directory not found: `{TRAJECTORIES_DIR}`. "
            "Run experiments first via the **Config Builder** tab."
        )
        return

    all_items = scan_trajectories(TRAJECTORIES_DIR)

    if not all_items:
        st.info("No trajectory files found. Run experiments to generate logs.")
        return

    # Build option map: label -> item dict
    option_map: dict[str, dict] = {_option_label(item): item for item in all_items}
    option_labels: list[str] = list(option_map.keys())

    # Pre-fill selections from session_state if present
    # compare_logs may contain labels ("cond / task") or file paths — handle both
    default_selection: list[str] = []
    if "compare_logs" in st.session_state:
        stored = st.session_state.compare_logs
        if isinstance(stored, list):
            # Build reverse map: path -> label for path-based lookups
            path_to_label = {item["path"]: _option_label(item) for item in all_items}
            for s in stored:
                if s in option_map:
                    # Already a label
                    default_selection.append(s)
                elif s in path_to_label:
                    # It's a path — convert to label
                    default_selection.append(path_to_label[s])

    # ------------------------------------------------------------------
    # 2. Multi-select widget
    # ------------------------------------------------------------------
    selected_labels: list[str] = st.multiselect(
        "Select trajectory logs to compare",
        options=option_labels,
        default=default_selection,
        help="Format: condition_id / task_id",
    )

    # Persist selection to session_state for cross-tab continuity
    st.session_state.compare_logs = selected_labels

    if len(selected_labels) < 2:
        st.info("Select at least 2 logs to enable comparison.")
        return

    # ------------------------------------------------------------------
    # 3. Load logs and compute metrics
    # ------------------------------------------------------------------
    items_selected: list[dict] = []
    logs_loaded: list[dict] = []
    metrics_list: list[dict] = []
    load_errors: list[str] = []

    for label in selected_labels:
        item = option_map[label]
        try:
            log = load_trajectory(item["path"])
            metrics = compute_metrics_for_log(log)
        except Exception as exc:  # noqa: BLE001
            load_errors.append(f"`{label}`: {exc}")
            continue
        items_selected.append(item)
        logs_loaded.append(log)
        metrics_list.append(metrics)

    if load_errors:
        with st.expander("Load errors", expanded=False):
            for err in load_errors:
                st.error(err)

    if not metrics_list:
        st.error("Could not load any of the selected logs.")
        return

    labels_loaded = [_option_label(item) for item in items_selected]

    # ------------------------------------------------------------------
    # 4. Comparison table
    # ------------------------------------------------------------------
    st.markdown("##### Metrics Comparison Table")

    rows = [
        _build_comparison_row(label, item, log, metrics)
        for label, item, log, metrics in zip(
            labels_loaded, items_selected, logs_loaded, metrics_list
        )
    ]
    df_compare = pd.DataFrame(rows)
    st.dataframe(df_compare, use_container_width=True, hide_index=True)

    # ------------------------------------------------------------------
    # 5. Grouped bar chart
    # ------------------------------------------------------------------
    st.markdown("##### Grouped Bar Chart")

    # plotly_grouped_comparison expects logs as list of flat dicts with metric key -> float value
    flat_logs = [
        {k: metrics[k]["value"] for k in METRIC_KEYS}
        for metrics in metrics_list
    ]
    chart_labels = [_option_label(item) for item in items_selected]

    fig = plotly_grouped_comparison(flat_logs, METRIC_KEYS, chart_labels, theme)
    # Override x-axis tick labels to show human-readable metric names
    fig.update_layout(
        xaxis=dict(
            tickvals=METRIC_KEYS,
            ticktext=[METRIC_DISPLAY_NAMES[k] for k in METRIC_KEYS],
        )
    )
    st.plotly_chart(fig, use_container_width=True)

    # ------------------------------------------------------------------
    # 6. Cross-backend portability
    # ------------------------------------------------------------------
    st.markdown("##### Cross-Backend Portability")

    # Collect backend -> [resolve_rates] from loaded logs
    backend_rates: dict[str, list[float]] = {}
    for item, log in zip(items_selected, logs_loaded):
        config = log.get("config", {})
        backend = config.get("backend", "").strip()
        if not backend:
            backend = "unknown"
        resolved = 1.0 if item["resolved"] else 0.0
        backend_rates.setdefault(backend, []).append(resolved)

    # Average resolve rate per backend
    avg_backend_rates: dict[str, float] = {
        b: sum(rates) / len(rates) for b, rates in backend_rates.items()
    }

    unique_backends = list(avg_backend_rates.keys())

    if len(unique_backends) >= 2:
        m31 = cross_backend_stddev(avg_backend_rates)
        m32 = min_max_ratio(avg_backend_rates)

        col_stddev, col_ratio = st.columns(2)
        with col_stddev:
            st.metric(
                label="M3.1 Cross-Backend StdDev",
                value=f"{m31:.4f}",
                help=(
                    "Standard deviation of average resolve rates across backends. "
                    "Lower = more portable."
                ),
            )
        with col_ratio:
            st.metric(
                label="M3.2 Min/Max Ratio",
                value=f"{m32:.4f}",
                help=(
                    "min(resolve_rate) / max(resolve_rate) across backends. "
                    "Higher (closer to 1.0) = more portable."
                ),
            )

        # Show per-backend breakdown
        with st.expander("Per-backend resolve rates", expanded=False):
            backend_df = pd.DataFrame(
                [
                    {"Backend": b, "Avg Resolve Rate": f"{r * 100:.1f}%", "N logs": len(backend_rates[b])}
                    for b, r in avg_backend_rates.items()
                ]
            )
            st.dataframe(backend_df, use_container_width=True, hide_index=True)
    else:
        st.info(
            f"Cross-backend portability requires logs from 2+ different backends. "
            f"Currently selected backends: **{', '.join(unique_backends) or 'none'}**."
        )

    # ------------------------------------------------------------------
    # 7. CSV export
    # ------------------------------------------------------------------
    st.markdown("##### Export")

    csv_bytes = df_compare.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download comparison as CSV",
        data=csv_bytes,
        file_name="harness_eval_comparison.csv",
        mime="text/csv",
    )

    st.markdown("---")
    st.caption("Next: go to **ANOVA** tab to run Three-Way ANOVA on all trajectory data.")
