"""Log Viewer tab for HarnessEval Dashboard.

Allows browsing trajectory logs by condition, viewing turn-by-turn details
with expandable output, and computing/displaying per-log metrics.
"""

from __future__ import annotations

from pathlib import Path
from collections import defaultdict

import streamlit as st

from st_utils.data_loader import scan_trajectories, load_trajectory, compute_metrics_for_log
from st_utils.charts import plotly_metrics_bar

TRAJECTORIES_DIR = Path(__file__).parent.parent / "trajectories"

# ---------------------------------------------------------------------------
# Action-type color mapping
# ---------------------------------------------------------------------------

_ACTION_COLORS: dict[str, str] = {
    "read":        "#4c8dff",
    "grep":        "#4c8dff",
    "glob":        "#4c8dff",
    "find":        "#4c8dff",
    "edit":        "#a78bfa",
    "write":       "#a78bfa",
    "bash":        "#22c55e",
    "python":      "#22c55e",
    "test_runner": "#22c55e",
}

_GIT_COLOR = "#f59e0b"
_DEFAULT_COLOR = "#9ca0ad"


def _action_color(action: str) -> str:
    """Return a hex color for the given action name."""
    if action in _ACTION_COLORS:
        return _ACTION_COLORS[action]
    if action.startswith("git_") or action == "git":
        return _GIT_COLOR
    return _DEFAULT_COLOR


# ---------------------------------------------------------------------------
# Helper: metric card HTML
# ---------------------------------------------------------------------------

def _metric_card_html(metric_id: str, meta: dict) -> str:
    """Render a single metric as an HTML card using .metric-card CSS class."""
    value: float = meta.get("value", 0.0)
    label: str = meta.get("label", metric_id)
    dim: str = meta.get("dim", "")
    detail: str = meta.get("detail", "")
    pct = value * 100

    # Progress bar color
    if value >= 0.8:
        bar_color = "#22c55e"
    elif value >= 0.5:
        bar_color = "#f59e0b"
    else:
        bar_color = "#ef4444"

    return (
        f'<div class="metric-card" style="margin-bottom:12px;">'
        f'  <div class="metric-label">{dim} — {label}</div>'
        f'  <div class="metric-value">{pct:.1f}%</div>'
        f'  <div style="background:#2a2d3e;border-radius:4px;height:6px;margin:6px 0;">'
        f'    <div style="background:{bar_color};width:{min(pct,100):.1f}%;height:6px;border-radius:4px;"></div>'
        f'  </div>'
        f'  <div style="font-size:11px;color:#9ca0ad;margin-top:4px;">{detail}</div>'
        f'</div>'
    )


# ---------------------------------------------------------------------------
# Main render function
# ---------------------------------------------------------------------------

@st.cache_data(show_spinner=False)
def _cached_scan(base_dir: str) -> list[dict]:
    """Cache-wrapped scan_trajectories call. base_dir is str for hashability."""
    results = scan_trajectories(Path(base_dir))
    # Make 'path' JSON-serializable (convert Path → str) for cache compatibility
    for item in results:
        item["path"] = str(item["path"])
    return results


def render_log_viewer():
    # ── Guard: trajectories directory must exist ─────────────────────────────
    if not TRAJECTORIES_DIR.exists():
        st.warning(
            f"Trajectories directory not found: `{TRAJECTORIES_DIR}`. "
            "Run the pipeline first or place trajectory JSON files there."
        )
        return

    # ── Load metadata (cached) ───────────────────────────────────────────────
    all_meta: list[dict] = _cached_scan(str(TRAJECTORIES_DIR))

    if not all_meta:
        st.info("No trajectory files found. Run the pipeline to generate them.")
        return

    # Group by condition
    by_condition: dict[str, list[dict]] = defaultdict(list)
    for item in all_meta:
        by_condition[item["condition_id"]].append(item)

    # Ensure compare_logs exists in session state
    if "compare_logs" not in st.session_state:
        st.session_state.compare_logs = []

    # ── 2-column layout: browser (1) + content (3) ──────────────────────────
    browser_col, content_col = st.columns([1, 3])

    # ────────────────────────────────────────────────────────────────────────
    # BROWSER COLUMN
    # ────────────────────────────────────────────────────────────────────────
    with browser_col:
        st.markdown("#### Browse Logs")

        condition_ids = sorted(by_condition.keys())
        selected_condition = st.selectbox(
            "Condition",
            options=condition_ids,
            key="lv_condition",
        )

        # Resolve rate caption
        tasks_in_cond = by_condition[selected_condition]
        total = len(tasks_in_cond)
        resolved = sum(1 for t in tasks_in_cond if t["resolved"])
        pct = (resolved / total * 100) if total > 0 else 0.0
        st.caption(f"{resolved}/{total} resolved ({pct:.0f}%)")

        # Task selector
        task_options = [t["task_id"] for t in tasks_in_cond]
        selected_task_id = st.selectbox(
            "Task",
            options=task_options,
            key="lv_task",
        )

        # Find the selected task metadata
        selected_meta = next(
            (t for t in tasks_in_cond if t["task_id"] == selected_task_id),
            None,
        )

        # "Add to Compare" button
        if selected_meta is not None:
            task_path = selected_meta["path"]  # str (from cached scan)
            if st.button("Add to Compare", key="lv_add_compare"):
                if task_path not in st.session_state.compare_logs:
                    st.session_state.compare_logs.append(task_path)
                    st.success(f"Added `{selected_task_id}` to compare list.")
                else:
                    st.info("Already in compare list.")

    # ────────────────────────────────────────────────────────────────────────
    # CONTENT COLUMN
    # ────────────────────────────────────────────────────────────────────────
    with content_col:
        if selected_meta is None:
            st.info("Select a task from the browser to view details.")
            return

        # Load full trajectory JSON
        log: dict = load_trajectory(Path(selected_meta["path"]))
        trajectory: list[dict] = log.get("trajectory", [])

        # ── Header ───────────────────────────────────────────────────────────
        resolved_flag = selected_meta["resolved"]
        badge_cls = "badge-pass" if resolved_flag else "badge-fail"
        badge_txt = "RESOLVED" if resolved_flag else "FAILED"
        model = selected_meta.get("model", log.get("model", "—"))
        num_turns = selected_meta.get("num_turns", len(trajectory))
        total_cost = selected_meta.get("total_cost", log.get("total_cost", 0.0))
        condition_id = selected_meta.get("condition_id", "—")

        st.markdown(
            f'<h4 style="margin-bottom:4px;">'
            f'{selected_task_id} '
            f'<span class="{badge_cls}">{badge_txt}</span>'
            f'</h4>'
            f'<div style="color:#9ca0ad;font-size:13px;margin-bottom:12px;">'
            f'Model: <b>{model}</b> &nbsp;|&nbsp; '
            f'Turns: <b>{num_turns}</b> &nbsp;|&nbsp; '
            f'Cost: <b>${total_cost:.4f}</b> &nbsp;|&nbsp; '
            f'Condition: <code>{condition_id}</code>'
            f'</div>',
            unsafe_allow_html=True,
        )

        # ── Sub-columns: turns (2) + metrics (1) ─────────────────────────────
        turns_col, metrics_col = st.columns([2, 1])

        # ── TURNS SUB-COLUMN ─────────────────────────────────────────────────
        with turns_col:
            st.markdown("##### Trajectory Turns")

            if not trajectory:
                st.info("No turns recorded in this trajectory.")
            else:
                for i, turn in enumerate(trajectory):
                    turn_num: int = turn.get("turn", i + 1)
                    action: str = turn.get("action", "unknown")
                    args: dict = turn.get("args", {})
                    output: str = turn.get("output", "") or ""
                    acceptable_tools: list | None = turn.get("acceptable_tools", None)

                    color = _action_color(action)
                    label = (
                        f'<span style="color:{color};font-weight:bold;">{action}</span>'
                    )

                    # First 3 turns expanded by default
                    expanded = i < 3

                    with st.expander(f"Turn {turn_num}: {action}", expanded=expanded):
                        # Color-coded action label
                        st.markdown(
                            f'<div style="margin-bottom:8px;">'
                            f'Action: {label}'
                            f'</div>',
                            unsafe_allow_html=True,
                        )

                        # Args as JSON
                        if args:
                            st.json(args)

                        # Output (truncated to 500 chars)
                        if output:
                            st.code(output[:500], language=None)
                        else:
                            st.caption("_(no output)_")

                        # Acceptable tools / correctness badge
                        if acceptable_tools is not None:
                            is_correct = action in acceptable_tools
                            badge_cls2 = "badge-pass" if is_correct else "badge-fail"
                            badge_text = "Correct" if is_correct else "Wrong"
                            tools_str = ", ".join(acceptable_tools)
                            st.markdown(
                                f'<div style="margin-top:6px;">'
                                f'<span class="{badge_cls2}">{badge_text}</span> '
                                f'<span style="font-size:11px;color:#9ca0ad;">'
                                f'Acceptable: {tools_str}'
                                f'</span>'
                                f'</div>',
                                unsafe_allow_html=True,
                            )

        # ── METRICS SUB-COLUMN ───────────────────────────────────────────────
        with metrics_col:
            st.markdown("##### Evaluation Metrics")

            metrics: dict[str, dict] = compute_metrics_for_log(log)

            # Render each metric as an HTML card
            cards_html = "".join(
                _metric_card_html(mid, meta)
                for mid, meta in metrics.items()
            )
            st.markdown(cards_html, unsafe_allow_html=True)

            # Plotly horizontal bar chart
            fig = plotly_metrics_bar(metrics, theme=st.session_state.get("theme", "dark"))
            st.plotly_chart(fig, use_container_width=True, key=f"lv_chart_{selected_task_id}")
