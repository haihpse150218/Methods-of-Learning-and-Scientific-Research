"""Compare tab — Tab 4 of HarnessEval Dashboard.

Compare conditions by aggregated metrics (not individual files).
Metric-centric view: rows = metrics, columns = conditions.
Auto-generates insights for each metric comparison.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from st_utils.data_loader import scan_trajectories, load_trajectory, compute_metrics_for_log
from st_utils.charts import plotly_grouped_comparison
from st_utils.ui_helpers import render_pipeline_banner
from harness_eval.metrics.backend_portability import cross_backend_stddev, min_max_ratio

TRAJECTORIES_DIR = Path(__file__).parent.parent / "trajectories"


# ---------------------------------------------------------------------------
# Aggregate metrics per condition
# ---------------------------------------------------------------------------

def _aggregate_condition(entries: list[dict]) -> dict:
    """Compute aggregated metrics for a list of trajectory entries (same condition)."""
    if not entries:
        return {}

    resolved_count = sum(1 for e in entries if e["resolved"])
    total = len(entries)
    resolve_rate = resolved_count / total if total > 0 else 0

    # Compute per-task metrics and average
    all_m11, all_m12, all_m13, all_m22 = [], [], [], []
    total_cost = 0.0
    total_turns = 0

    for entry in entries:
        try:
            log = load_trajectory(entry["path"])
            metrics = compute_metrics_for_log(log)
            all_m11.append(metrics["m11"]["value"])
            all_m12.append(metrics["m12"]["raw_redundant"] if "raw_redundant" in metrics["m12"] else metrics["m12"]["value"])
            all_m13.append(metrics["m13"]["value"])
            all_m22.append(metrics["m22"]["value"])
            total_cost += log.get("total_cost", 0)
            total_turns += len(log.get("trajectory", []))
        except Exception:
            continue

    n = len(all_m11) or 1
    return {
        "resolve_rate": resolve_rate,
        "resolved": resolved_count,
        "total": total,
        "m11": sum(all_m11) / n if all_m11 else 0,
        "m12": sum(all_m12) / n if all_m12 else 0,  # raw redundant rate
        "m13": sum(all_m13) / n if all_m13 else 0,
        "m22": sum(all_m22) / n if all_m22 else 0,
        "cost": total_cost,
        "avg_cost": total_cost / total if total > 0 else 0,
        "avg_turns": total_turns / total if total > 0 else 0,
    }


def _generate_insight(metric: str, val_a: float, val_b: float, label_a: str, label_b: str) -> str:
    """Generate a human-readable insight for a metric comparison."""
    diff = val_a - val_b
    abs_diff = abs(diff)

    if metric == "resolve_rate":
        pct = abs_diff * 100
        if pct < 2:
            return "Nearly identical performance"
        better = label_a if diff > 0 else label_b
        return f"{better} resolves {pct:.0f}% more tasks"

    if metric == "m11":
        if abs_diff < 0.05:
            return "Similar tool selection accuracy"
        better = label_a if diff > 0 else label_b
        return f"{better} selects correct tools {abs_diff:.0%} more often"

    if metric == "m12":
        # Lower is better for redundant calls
        if abs_diff < 0.05:
            return "Similar redundancy levels"
        worse = label_a if diff > 0 else label_b
        return f"{worse} makes {abs_diff:.0%} more redundant calls"

    if metric == "m13":
        if abs_diff < 0.05:
            return "Similar tool utilization"
        better = label_a if diff > 0 else label_b
        return f"{better} uses {abs_diff:.0%} more of available tools"

    if metric == "m22":
        if abs_diff < 0.05:
            return "Similar token efficiency"
        better = label_a if diff > 0 else label_b
        return f"{better} has {abs_diff:.0%} higher token efficiency"

    if metric == "avg_cost":
        if abs_diff < 0.01:
            return "Nearly identical cost"
        cheaper = label_a if diff < 0 else label_b
        pct = abs_diff / max(val_a, val_b) * 100 if max(val_a, val_b) > 0 else 0
        return f"{cheaper} is {pct:.0f}% cheaper per task"

    if metric == "avg_turns":
        if abs_diff < 1:
            return "Similar number of steps"
        fewer = label_a if diff < 0 else label_b
        pct = abs_diff / max(val_a, val_b) * 100 if max(val_a, val_b) > 0 else 0
        return f"{fewer} uses {pct:.0f}% fewer steps"

    return ""


# ---------------------------------------------------------------------------
# Main render
# ---------------------------------------------------------------------------

def render_compare() -> None:
    st.markdown("### Compare Conditions")
    render_pipeline_banner()

    entries = scan_trajectories(TRAJECTORIES_DIR)
    if not entries:
        st.info("No trajectory data. Run experiments first via **Config Builder**.")
        return

    # Group entries by condition
    conditions_map: dict[str, list[dict]] = {}
    for e in entries:
        conditions_map.setdefault(e["condition_id"], []).append(e)

    condition_ids = sorted(conditions_map.keys())

    if len(condition_ids) < 2:
        st.info(f"Only {len(condition_ids)} condition found. Need at least 2 to compare.")
        return

    # ── Selection ────────────────────────────────────────────────────────
    st.markdown("**Select conditions to compare:**")
    col_mode, col_select = st.columns([1, 3])

    with col_mode:
        compare_mode = st.radio(
            "Compare by",
            ["Pick conditions", "By Tool Level", "By Context", "By Backend"],
            key="compare_mode",
            label_visibility="collapsed",
        )

    with col_select:
        if compare_mode == "Pick conditions":
            selected = st.multiselect(
                "Conditions",
                condition_ids,
                default=condition_ids[:min(3, len(condition_ids))],
                key="compare_conditions",
            )
        elif compare_mode == "By Tool Level":
            # Group by tool level, pick best-represented context+backend
            tools = ["full", "medium", "minimal"]
            selected = [c for c in condition_ids if any(c.startswith(t + "_") for t in tools)]
            # Pick one per tool level (same context+backend)
            best = {}
            for c in condition_ids:
                parts = c.split("_")
                tool = parts[0]
                rest = "_".join(parts[1:])
                if tool in tools and rest not in best:
                    best[rest] = []
                if tool in tools:
                    key = "_".join(parts[1:])
                    if key not in best:
                        best[key] = []
                    best[key].append(c)
            # Find context+backend combo with all 3 tools
            for rest, conds in best.items():
                if len(conds) >= 3:
                    selected = sorted(conds)[:3]
                    break
            else:
                selected = condition_ids[:3]
            st.caption(f"Comparing: {', '.join(selected)}")

        elif compare_mode == "By Context":
            contexts = ["full", "sliding_window", "summary"]
            best = {}
            for c in condition_ids:
                parts = c.split("_")
                tool = parts[0]
                backend = parts[-1]
                for ctx in contexts:
                    if f"_{ctx}_" in c or c.endswith(f"_{ctx}_{backend}"):
                        key = f"{tool}_{backend}"
                        if key not in best:
                            best[key] = []
                        best[key].append(c)
            for key, conds in best.items():
                if len(conds) >= 3:
                    selected = sorted(conds)[:3]
                    break
            else:
                selected = condition_ids[:3]
            st.caption(f"Comparing: {', '.join(selected)}")

        elif compare_mode == "By Backend":
            backends = ["claude", "gpt", "deepseek"]
            best = {}
            for c in condition_ids:
                backend = c.split("_")[-1]
                prefix = "_".join(c.split("_")[:-1])
                if backend in backends:
                    if prefix not in best:
                        best[prefix] = []
                    best[prefix].append(c)
            for prefix, conds in best.items():
                if len(conds) >= 3:
                    selected = sorted(conds)[:3]
                    break
            else:
                selected = condition_ids[:3]
            st.caption(f"Comparing: {', '.join(selected)}")

    if len(selected) < 2:
        st.info("Select at least 2 conditions.")
        return

    # ── Aggregate metrics ────────────────────────────────────────────────
    agg = {}
    for cid in selected:
        agg[cid] = _aggregate_condition(conditions_map.get(cid, []))

    # ── Short labels ─────────────────────────────────────────────────────
    # Make labels shorter for display
    def _short_label(cid: str) -> str:
        parts = cid.split("_")
        if len(parts) >= 3:
            return f"{parts[0]}/{parts[-1]}"  # "full/claude"
        return cid

    labels = {cid: _short_label(cid) for cid in selected}

    # ── Metric-centric comparison table ──────────────────────────────────
    st.markdown("---")
    st.markdown("#### Metric Comparison")

    metrics_def = [
        ("resolve_rate", "Resolve Rate", lambda v: f"{v:.0%}", "higher"),
        ("m11", "M1.1 Correct Selection", lambda v: f"{v:.2f}", "higher"),
        ("m12", "M1.2 Redundant Calls", lambda v: f"{v:.2f}", "lower"),
        ("m13", "M1.3 Utilization Breadth", lambda v: f"{v:.2f}", "higher"),
        ("m22", "M2.2 Effective Tokens", lambda v: f"{v:.2f}", "higher"),
        ("avg_cost", "Avg Cost/Task", lambda v: f"${v:.3f}", "lower"),
        ("avg_turns", "Avg Turns/Task", lambda v: f"{v:.1f}", "lower"),
    ]

    # Build table rows
    table_rows = []
    for key, label, fmt, direction in metrics_def:
        row = {"Metric": label}
        values = []
        for cid in selected:
            val = agg[cid].get(key, 0)
            row[labels[cid]] = fmt(val)
            values.append(val)

        # Generate insight (compare first vs second condition)
        if len(selected) >= 2:
            row["Insight"] = _generate_insight(
                key, values[0], values[1], labels[selected[0]], labels[selected[1]]
            )

        # Delta column (first - last)
        if len(values) >= 2:
            delta = values[0] - values[-1]
            if key == "resolve_rate":
                row["Delta"] = f"{delta:+.0%}"
            elif key == "avg_cost":
                row["Delta"] = f"{delta:+.3f}"
            elif key == "avg_turns":
                row["Delta"] = f"{delta:+.1f}"
            else:
                row["Delta"] = f"{delta:+.2f}"

        table_rows.append(row)

    df_compare = pd.DataFrame(table_rows)
    st.dataframe(df_compare, use_container_width=True, hide_index=True)

    # ── Summary cards ────────────────────────────────────────────────────
    st.markdown("#### Condition Summary")
    cols = st.columns(len(selected))
    for i, cid in enumerate(selected):
        a = agg[cid]
        with cols[i]:
            st.markdown(f"**{labels[cid]}**")
            st.caption(f"`{cid}`")
            st.metric("Resolve Rate", f"{a['resolve_rate']:.0%}", f"{a['resolved']}/{a['total']} tasks")
            st.metric("Avg Cost", f"${a['avg_cost']:.3f}/task")
            st.metric("Avg Turns", f"{a['avg_turns']:.1f}")

    # ── Grouped bar chart ────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("#### Visual Comparison")

    theme = st.session_state.get("theme", "dark")
    metric_keys = ["m11", "m12", "m13", "m22"]
    flat_logs = [{k: agg[cid].get(k, 0) for k in metric_keys} for cid in selected]
    chart_labels = [labels[cid] for cid in selected]

    fig = plotly_grouped_comparison(flat_logs, metric_keys, chart_labels, theme)
    fig.update_layout(
        xaxis=dict(
            tickvals=metric_keys,
            ticktext=["Correct Selection", "Redundant Calls", "Utilization", "Token Efficiency"],
        )
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── Cross-backend portability ────────────────────────────────────────
    backends_in_selection = set()
    backend_rates: dict[str, list[float]] = {}
    for cid in selected:
        backend = cid.split("_")[-1]
        backends_in_selection.add(backend)
        a = agg[cid]
        backend_rates.setdefault(backend, []).append(a["resolve_rate"])

    if len(backends_in_selection) >= 2:
        st.markdown("---")
        st.markdown("#### Cross-Backend Portability")

        avg_rates = {b: sum(v) / len(v) for b, v in backend_rates.items()}
        m31 = cross_backend_stddev(avg_rates)
        m32 = min_max_ratio(avg_rates)

        p1, p2, p3 = st.columns(3)
        with p1:
            st.metric("M3.1 StdDev", f"{m31:.4f}", help="Lower = more portable")
        with p2:
            st.metric("M3.2 Min/Max Ratio", f"{m32:.3f}", help="Higher = more portable (1.0 = perfect)")
        with p3:
            for b, rate in sorted(avg_rates.items()):
                st.metric(f"{b.capitalize()}", f"{rate:.0%}")

    # ── Export ───────────────────────────────────────────────────────────
    st.markdown("---")
    csv_data = df_compare.to_csv(index=False).encode("utf-8")
    st.download_button("Download Comparison CSV", csv_data, "condition_comparison.csv", "text/csv")

    st.caption("Next: go to **ANOVA** tab for statistical significance testing across all conditions.")
